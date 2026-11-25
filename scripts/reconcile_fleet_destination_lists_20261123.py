"""Bind remaining Fleet Info selector branches to the original port lists."""

from collections import Counter
from pathlib import Path
from re import DOTALL, compile as regex
from struct import iter_unpack, pack, unpack

from dk4tool.formats.ilnk import IlnkContainer
from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R5

from scripts import reconcile_fleet_destination_copies_20261123 as previous
from scripts import reconcile_fleet_destination_name_caller_20261123 as picker


prior = previous.prior
ROOT = Path("releases/all_routes_editorial_20261123_nagasaki_dream_candidate")
RELEASE = ROOT / "verification/registered_release_verification.json"
CAPTURE = Path(".codex-release-work/nagasaki_dream_20261123/startup/capture/capture_report.json")
OUT = previous.OUT.with_name("fleet_destination_lists_20261123.json")
NEIGHBORS, EDGE_ROWS = 0x02290A3C, 0x02290D64
PORT_MANAGER, RANDOM = 0x020CB178, 0x020519D4
FLEET_ORDER = 0x0208B000
STORY_ORDER = 0x0202B438
PICKER = 0x0208BD5C
SCRATCH = 0x023F0000
PACKED_FLEET_ORDER = regex(rb"(?=\x00\xa0.{5}\x82)", DOTALL)

# Complete caller fragments containing the candidate list, its selection and the write.
LIST_SITES = {
    0x0202F07C: (0x0202F044, 0x0202F080, "Three town-search loops plus nearby faction ports."),
    0x0202F7F8: (0x0202F7B4, 0x0202F7FC, "Nearby ports with a faction predicate."),
    0x0203554C: (0x02035468, 0x02035558, "Nearby ports and an optional region filter."),
    0x02035610: (0x020355B0, 0x02035614, "Nearby ports with a faction predicate and any-region fallback."),
    0x020357E4: (0x02035720, 0x020357E8, "Two filtered nearby lists and two nearby fallbacks."),
    0x020359A4: (0x0203596C, 0x020359B0, "Nearby ports around the fleet's stored docking slot."),
    0x02035A18: (0x020359E0, 0x02035A24, "Nearby ports around the fleet's stored docking slot."),
}
PRODUCERS = ((0x0202F4C0, 0x0202F798), (0x020B1720, 0x020B1760),
    (0x020B1864, 0x020B19D8), (0x020B2628, 0x020B2850), (0x020B28B8, 0x020B2978),
    (0x020B2AC8, 0x020B2B48), (0x02089DB8, 0x02089EC4), (0x0208A10C, 0x0208A198),
    (0x0208A6C0, 0x0208A6E8), (0x020B5600, 0x020B5630), (PORT_MANAGER, PORT_MANAGER + 12),
    (RANDOM, RANDOM + 0x48), (0x0208ABFC, 0x0208AD30), (0x0208AE5C, 0x0208B010),
    (PICKER, 0x0208BDC0), (prior.WRITER, prior.WRITER + 12), (0x0202BE8C, 0x0202BF50),
    (0x0202B340, 0x0202B444), (0x02034674, 0x02034688))


def linked(arm, address, target):
    assert prior.direct_bl_target(prior.word(arm, address), address) == target, (hex(address), hex(target))


def selector_references(rom):
    targets = {0x0208AE5C, 0x0208A10C}
    calls, pointers = ({target: [] for target in targets} for _ in range(2))
    for area, base, data in prior.loaded_components(rom):
        for index, (value,) in enumerate(iter_unpack("<I", data[:len(data) // 4 * 4])):
            address = base + index * 4
            target = prior.direct_bl_target(value, address)
            if target in targets:
                calls[target].append([area, address])
            if value in targets:
                pointers[value].append([area, address])
    assert calls[0x0208AE5C] == [["arm9_section_0", 0x0208ACFC]]
    assert calls[0x0208A10C] == [["arm9_section_0", 0x02089E94], ["arm9_section_0", 0x02089EA0]]
    assert not any(pointers.values())
    return calls


def port_graph(raw):
    graph = prior.code_at(raw, NEIGHBORS, NEIGHBORS + 8 + 90 * 7)
    edges = prior.code_at(raw, EDGE_ROWS, EDGE_ROWS + 177 * 28)
    assert unpack("<I", graph[4:8]) == (1,) and len(edges) == 177 * 28
    adjacent = [[] for _ in range(90)]
    pairs = []
    for start in range(0, len(edges), 28):
        words = unpack("<7I", edges[start:start + 28])
        a, b = words[1] & 0xFFFFFF, words[6] & 0xFFFFFF
        assert 0 <= a < 90 and 0 <= b < 90 and a != b
        pairs.append((a, b))
        for source, target in ((a, b), (b, a)):
            if target not in adjacent[source]:
                adjacent[source].append(target)
    assert max(map(len, adjacent)) == 6
    assert graph[8:] == b"".join(bytes(row + [115] * (6 - len(row)) + [len(row)]) for row in adjacent)
    return adjacent, dict(edges_address=EDGE_ROWS, neighbor_address=NEIGHBORS, edge_count=len(pairs), edges=pairs,
        edge_bytes_sha256=prior.digest_bytes(edges), exact_neighbor_rows_hex=graph[8:].hex(),
        counts=dict(Counter(map(len, adjacent))))


def native_lists(cpu, call, adjacent):
    ports = call(PORT_MANAGER - prior.BASE)

    def result(address, expected, args, stack_value=8):
        cpu.mem_write(SCRATCH, b"\xEF" * 0x200)
        cpu.mem_write(picker.STACK, pack("<I", stack_value))
        count = call(address - prior.BASE, *args)
        assert 0 <= count <= len(expected), (hex(address), count, args)
        data = bytes(cpu.mem_read(SCRATCH, count * 4 + 4))
        assert data[-4:] == b"\xEF" * 4
        values = [v for v, in iter_unpack("<I", data[:-4])]
        assert values == [v for v in expected if v in values], (hex(address), values, expected)
        return values

    totals = Counter()
    for town, expected in enumerate(adjacent):
        assert result(0x02089DB8, expected, (NEIGHBORS, town, SCRATCH)) == expected
        native = result(0x020B1954, expected, (ports, SCRATCH, town, 8))
        totals["raw_neighbor_rows"] += 1
        totals["active_neighbor_rows"] += 1
        for faction in (0, 1, 20):
            for address in (0x020B1864, 0x020B18DC):
                result(address, native, (ports, SCRATCH, town, faction))
                totals["faction_filtered_neighbor_rows"] += 1
    # These producers scan their own index ranges, independent of the neighbor rows.
    for town in range(114):
        for address, end in ((0x020B2628, 114), (0x020B26E0, 90), (0x020B27B4, 90)):
            expected = [i for i in range(end) if i != town]
            if address == 0x020B27B4:
                result(address, expected, (ports, SCRATCH, town, 0))
            else:
                # Two stack arguments follow r0-r3. Use a valid first goods slot and any region.
                cpu.mem_write(picker.STACK + 4, pack("<I", 8))
                result(address, expected, (ports, SCRATCH, town, 0), stack_value=0)
            totals["finite_port_searches"] += 1
    result(0x020B28B8, list(range(90)), (ports, SCRATCH, 8))
    totals["main_port_list_without_a_center"] += 1
    return dict(totals)


def check_picker(arm, cpu):
    linked(arm, 0x0208ACC8, PICKER)
    linked(arm, 0x0208ACFC, 0x0208AE5C)
    linked(arm, FLEET_ORDER, prior.WRITER)
    # The only aligned caller suppresses the cancel value. The order helper stores the selected
    # index at entry and loads it into r2 at the final write.
    assert prior.code_at(arm, 0x0208ACE8, 0x0208ACF0).hex() == "730056e30e00000a"
    assert prior.code_at(arm, 0x0208AE6C, 0x0208AE70).hex() == "00208de5"
    assert prior.code_at(arm, 0x0208AFF4, 0x0208AFF8).hex() == "00209de5"
    summary = picker.regional_picker(cpu)
    assert summary["tail_address"] == 0x0208BD84
    return dict(writer=FLEET_ORDER, consumer_entry=0x0208AE5C, picker=summary, cancelled_selection_skips_writer=True)


def story_order_candidates(image):
    archives = []
    for directory in ("data", "testdata"):
        for route in range(4):
            path = f"/{directory}/SC{route}.DK4"
            archive = image.read_file(path)
            blocks = IlnkContainer.parse(archive).blocks
            commands = []
            for number, block in enumerate(blocks):
                for match in PACKED_FLEET_ORDER.finditer(block):
                    at = match.start()
                    raw = block[at:at + 8]
                    commands.append(dict(block=number, block_offset=at, exact_hex=raw.hex(),
                        usual_marker=raw[2:4] == b"\xff\xff", explicit_slot=raw[4] if raw[5] else None,
                        order=raw[5], source="explicit operand" if raw[5] else "protagonist fleet docking byte"))
            archives.append(dict(path=path, sha256=prior.digest_bytes(archive), blocks=len(blocks), commands=commands))
    assert sum(row["blocks"] for row in archives[:4]) == 1307
    assert sum(row["blocks"] for row in archives[4:]) == 1310
    assert all(row["explicit_slot"] is None or row["explicit_slot"] < 90
               for arc in archives for row in arc["commands"])
    return archives


def check_story_orders(arm, cpu, clean, current):
    linked(arm, 0x0202BF44, 0x0202B340)
    linked(arm, STORY_ORDER, prior.WRITER)
    assert prior.word(arm, 0x0202BED0) == 0xEA00001B  # Family 8 dispatches to 0x0202BF44.
    source, installed = map(story_order_candidates, (clean, current))

    def usual_commands(archives):
        return {arc["path"]: [(r["block"], r["exact_hex"]) for r in arc["commands"] if r["usual_marker"]]
                for arc in archives}

    assert usual_commands(source) == usual_commands(installed)
    for order in (1, 3, 255):
        for slot in range(256):
            value = 0x82000000 | (order << 8) | slot
            prior.run_fragment(cpu, 0x0202B3DC, STORY_ORDER, ((UC_ARM_REG_R2, value), (UC_ARM_REG_R5, SCRATCH)))
            assert cpu.reg_read(UC_ARM_REG_R1) == order and cpu.reg_read(UC_ARM_REG_R2) == slot
    return dict(writer=STORY_ORDER, clean_archive_scan=source, installed_archive_scan=installed,
        explicit_operand_native_cases=3 * 256, missionary_slot_absent_from_explicit_operands=True,
        fallback_dependency_open="Protagonist fleet docking byte at +0x3C when the order operand is zero.")


def main():
    release = prior.read(RELEASE)
    assert prior.digest(prior.REGISTRY) == release["registry_sha256"]
    assert prior.digest(prior.CLEAN) == release["clean_input_sha256"]
    assert prior.digest(release["candidate"]) == release["candidate_sha256"]
    current, clean = map(prior.NdsImage.open, (release["candidate"], prior.CLEAN))
    arm, original = [rom.read_file(prior.ARM) for rom in (current, clean)]
    assert prior.digest_bytes(arm) == release["target_ARM9_sha256"]
    inherited = prior.read(previous.OUT)
    census = prior.references(current)[prior.WRITER]
    assert census == inherited["writer_census"] == prior.references(clean)[prior.WRITER]
    helper_calls = selector_references(current)
    assert helper_calls == selector_references(clean)
    open_before = set(inherited["other_writer_calls"])
    assert len(open_before) == 15 and (set(LIST_SITES) | {FLEET_ORDER, STORY_ORDER}) <= open_before
    report = prior.read(CAPTURE)
    assert report["ROM_sha256"] == release["candidate_sha256"] and report["cold_boot"] and not report["savestate_loaded"]
    snapshot = report["read_only_RAM_snapshot"]
    raw = prior.read_ram(snapshot)
    before = prior.read(ROOT.with_name("all_routes_editorial_20261123_missionary_destination_candidate") / "release_manifest.json")
    parent_arm = prior.NdsImage.open(before["candidate"]).read_file(prior.ARM)
    assert parent_arm == arm and before["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    ranges = []
    for start, stop in (*PRODUCERS, *((start, stop) for start, stop, _ in LIST_SITES.values())):
        code = prior.code_at(arm, start, stop)
        assert code == prior.code_at(original, start, stop) == prior.code_at(raw, start, stop)
        ranges.append(dict(address=start, end=stop, exact_hex=code.hex(), sha256=prior.digest_bytes(code)))
    for address in LIST_SITES:
        linked(arm, address, prior.WRITER)
    for address, target in ((0x0202F060, 0x0202F4C0), (0x0202F5A4, 0x020B26E0), (0x0202F5D0, 0x020B26E0),
            (0x0202F68C, 0x020B2628), (0x0202F6B0, 0x020B2628), (0x0202F714, 0x020B18DC),
            (0x0202F744, 0x020B27B4), (0x0202F768, 0x020B27B4), (0x0202F7D4, 0x020B1864),
            (0x020354B4, 0x020B1954), (0x020355D8, 0x020B18DC), (0x020355F4, 0x020B1954),
            (0x0203575C, 0x020B18DC), (0x02035790, 0x020B18DC), (0x020357AC, 0x020B1954),
            (0x020357C8, 0x020B1954), (0x0203597C, 0x020B1954), (0x020359F0, 0x020B1954),
            (0x020B1880, 0x020B1954), (0x020B18F8, 0x020B1954), (0x020B1978, 0x020B2AC8),
            (0x020B2AE4, 0x02089DB8), (0x02089E94, 0x0208A10C), (0x02089EA0, 0x0208A10C)):
        linked(arm, address, target)
    adjacent, graph = port_graph(raw)
    cpu, call = prior.get_machine(arm, raw)
    counts = native_lists(cpu, call, adjacent)
    selected = check_picker(arm, cpu)
    scripted = check_story_orders(arm, cpu, clean, current)
    sites = [dict(call=site, producer_start=start, producer_end=stop, findings=note,
        scoped_neighbor_center_range=[0, 89], possible_port_slots=[0, 113 if site == 0x0202F07C else 89],
        conditional_scope="Neighbor lookups use a main port center; separate global searches can include hidden ports.")
        for site, (start, stop, note) in LIST_SITES.items()]
    prior.write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=prior.reference(RELEASE),
        parent_ARM9_matches=True, startup=prior.reference(CAPTURE), read_only_snapshot=snapshot,
        mode="offline native execution and static dispatch binding", prior_census=prior.reference(previous.OUT),
        aligned_helper_calls=helper_calls, independently_verified_picker=selected, conditional_list_writer_sites=sites, native_cases=counts,
        story_fleet_orders=scripted,
        initialized_port_graph=graph, matched_clean_installed_and_resident_ranges=ranges,
        other_open_direct_writers=sorted(open_before - set(LIST_SITES) - {FLEET_ORDER, STORY_ORDER}),
        unproven_neighbor_center_inputs_outside_main_ports=sorted(LIST_SITES),
        ordinary_missionary_reachability_open=True, editorial_credit_added=0))
    print(f"Verified the player picker and {len(sites)} bounded list paths across {sum(counts.values())} port-list cases.")
    print("Checked 768 authored-order dispatch cases and both sets of story archives.")


if __name__ == "__main__":
    main()
