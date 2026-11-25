"""Separate the Missionary object's market-trend state from Fleet Info destinations."""

from collections import Counter
from pathlib import Path
from struct import pack, pack_into, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import audit_fleet_save_backups_20261124 as saves
from scripts import observe_riga_port_trend_20261124 as play
from scripts import observe_riga_port_trend_restore_20261124 as restore
from scripts import observe_riga_port_trend_stores_20261124 as stores
from scripts import verify_personal_gameplay_v841 as runtime
from scripts.reconcile_class_names_20261123 import type_name, word
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write

BASE, OBJECT = play.BASE, play.OBJECT
FLEET_ROOT, TOWN_ROOT = 0x022CFD6C, 0x022D5D94
VTABLE = 0x02134D80
RESOLVE, TYPE6_BRANCH = 0x020211E4, 0x02021264
RESET, READ, WRITE = 0x0202C134, 0x0202C0BC, 0x0202C0F8
RUNTIME_SPANS = (
    (RESOLVE, 0x02021278), (0x02021464, 0x02021468), (0x0204F100, 0x0204F118),
    (0x0204F920, 0x0204F934), (0x0202BFDC, 0x0202BFF4), (0x0202BFF8, 0x0202C148),
    (0x02046A1C, 0x02046A58), (0x02046C20, 0x02046C5C), (0x0205E458, 0x0205E538),
    (0x020B1B9C, 0x020B1CD8), (0x020B29B4, 0x020B29CC), (0x020B2A18, 0x020B2A30),
    (0x020B2A7C, 0x020B2A94), (0x020B676C, 0x020B6818), (0x020B6BA4, 0x020B6BA8),
    (0x020CB178, 0x020CB184), (0x020CB1A8, 0x020CB1B4), (VTABLE, VTABLE + 32),
    (0x020347A4, 0x020347A8), (0x02035A28, 0x02035A2C),
)
OUT = saves.OUT.with_name("riga_port_trend_object_20261124.json")


def native_contract(clean, arm, resident):
    def span(blob, start, end):
        return blob[start - BASE:end - BASE]

    exact = []
    for start, end in RUNTIME_SPANS:
        value = span(arm, start, end)
        assert value == span(clean, start, end) == span(resident, start, end), hex(start)
        exact.append(dict(start=start, end=end, exact_hex=value.hex()))
    assert word(arm, 0x02021464) == word(arm, 0x020B6BA4) == OBJECT - TOWN_ROOT == 0x301C
    assert tuple(word(arm, VTABLE + n * 4) for n in range(8)) == (
        0x0202BFDC, 0x0202BFE4, 0x0202BFEC, 0x0202BFF8, 0x0202C000, RESET, WRITE, READ)
    checks = {
        0x020211F0: "lsr r0, r4, #0x18", 0x02021218: "b #0x2021264",
        TYPE6_BRANCH: "bl #0x20cb178", 0x02021270: "add r0, r0, r1",
        0x0204F108: "ldr r1, [r1, #0xc]", 0x0204F10C: "blx r1",
        0x0202C0D8: "bl #0x2046a1c", 0x0202C0E8: "bl #0x2046a1c",
        0x0202C114: "bl #0x2046c20", 0x0202C124: "bl #0x2046c20",
        0x020347A4: "strb r5, [r6, #0x3c]", 0x02035A28: "strb r2, [r0, #0x3f]",
        0x020B1C40: "strb r0, [r4, #4]", 0x020B1CA0: "strb r0, [r4, #5]",
        0x020B1CB8: "strbeq r0, [r4, #5]", 0x020B6800: "strb r5, [r0, #0x20]",
        0x020B1CD0: "bl #0x202c014", 0x020B6814: "bl #0x202c014",
    }
    engine = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for pc, expected in checks.items():
        instruction, = engine.disasm(span(arm, pc, pc + 4), pc)
        assert f"{instruction.mnemonic} {instruction.op_str}" == expected
    assert type_name(resident, VTABLE) == "6CAdman"
    assert word(resident, OBJECT) == VTABLE
    assert word(resident, 0x020CB180) == TOWN_ROOT and word(resident, 0x020CB1B0) == FLEET_ROOT
    return dict(spans=exact, exact_instructions=checks, address=OBJECT, vtable=VTABLE, slot=114)


def trace_files(root, release, observer, frames, last_frame):
    leaf = root / "riga"
    paths = [leaf / p for p in ("capture/capture_report.json", "requests.json", "source_contract.json", "terminal.json")]
    report, trace, contract, terminal = map(read, paths)
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == last_frame == terminal["completed_frames"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert [row["frame"] for row in report["read_only_capture_RAM_snapshots"]] == list(frames)
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert all(digest(p) == sha for p, sha in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["observer_sha256"] == digest(observer) and trace["source_contract_sha256"] == digest(paths[2])
    assert trace["rows"] == terminal["caption_calls"] and len(trace["source_requests"]) == terminal["COMMON_requests"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    return report, trace, list(map(reference, paths))


def ordinary_fields(report, trace):
    check_pairs = []
    for before, after in zip(trace["rows"][::2], trace["rows"][1::2], strict=True):
        field, _, offset = restore.READS[before["PC"]]
        assert after["phase"] == "after" and before["phase"] == "before" and before["frame"] == after["frame"]
        assert after["PC"] == before["PC"] + 4 and before["owner"] == after["owner"] == OBJECT
        assert before["field"] == after["field"] == field and before["saved_byte"] == after["value"] and after["success"] == 1
        check_pairs.append(dict(field=field, runtime_address=OBJECT + offset, serialized_offset=before["buffer_offset"],
                                value=after["value"], before=before, after=after))
    assert len(check_pairs) == 2 and [r["value"] for r in check_pairs] == [32, 25]
    offsets = {r["field"]: [r["serialized_offset"]] for r in check_pairs}
    assert list(offsets.values()) == [[20476], [20477]]
    donor = Path(report["battery_save_preloaded"]["source"])
    physical, = [s for s in saves.backup_slots(donor, offsets)["slots"] if s["status"] == "valid"
                 and tuple(s["fields_hex_by_index"].values()) == ("20", "19")]
    assert physical["slot_index"] == 2
    previous = read(saves.OUT)
    backups = [saves.backup_slots(Path(old["path"]), offsets) for old in previous["backups"]]
    values = {field: Counter() for field in offsets}
    checked = 0
    for old, new in zip(previous["backups"], backups, strict=True):
        assert old["sha256"] == new["sha256"]
        assert [(s["sha256"], s["status"]) for s in old["slots"]] == [(s["sha256"], s["status"]) for s in new["slots"]]
        for slot in new["slots"]:
            if slot["status"] == "valid":
                checked += 1
                for field, hex_value in slot["fields_hex_by_index"].items():
                    values[field][int(hex_value, 16)] += 1
    assert checked == previous["slot_states"]["valid"] == 125
    return dict(native_reads=check_pairs, Riga_active_slot=physical, exact_prior_backup_inventory=reference(saves.OUT),
                backup_files=len(backups), checksum_valid_slot_copies=checked, serialized_value_counts=values)


def snapshot_fields(report, trace):
    rows, live = [], None
    for data in report["read_only_capture_RAM_snapshots"]:
        live = Path(data["path"]).read_bytes()
        assert data["read_only_export"] and sha256(live).hexdigest() == data["sha256"]
        assert word(live, OBJECT) == VTABLE
        values = list(live[OBJECT - BASE + 4:OBJECT - BASE + 6])
        fleet = live[FLEET_ROOT - BASE + 4:FLEET_ROOT - BASE + 4 + 64 * 132]
        counts = {name: Counter(fleet[at::132]) for name, at in (("docking", 0x3C), ("destination", 0x3F))}
        assert len(fleet) == 64 * 132 and all(sum(c.values()) == 64 and set(c) <= {*range(90), 115} for c in counts.values())
        rows.append(dict(snapshot=data, trend_town=values[0], trend_good=values[1], fleet_value_counts=counts))
    assert [(r["trend_town"], r["trend_good"]) for r in rows] == [(32, 25)] * 7 + [(69, 76)] * 2
    changed = []
    field_writers = {0x020B1C40: ("trend_town", 4), 0x020B1CA0: ("trend_good", 4), 0x020B1CB8: ("trend_good", 4)}
    for row in trace["rows"]:
        if row["PC"] in field_writers:
            field, owner_register = field_writers[row["PC"]]
            regs = row["registers_r0_to_r8"]
            assert regs[owner_register] == OBJECT
            changed.append(dict(PC=row["PC"], frame=row["frame"], field=field, value=regs[0] & 255, live_trace=row))
    assert [(r["field"], r["value"]) for r in changed] == [
        ("trend_town", 71), ("trend_town", 69), ("trend_good", 125), ("trend_good", 76)]
    trend_calls = [r for r in trace["rows"] if r["PC"] == 0x0202C014]
    assert len(trend_calls) == 26 and all(r["registers_r0_to_r8"][0] == OBJECT and r["caller_LR"] == 0x020B1CD4 for r in trend_calls)
    fleet = [r for r in trace["rows"] if r["kind"] == "fleet_byte"]
    assert {r["PC"] for r in fleet} == set(play.WRITERS) and all(0 <= r["value"] < 90 for r in fleet)
    assert len({(r["PC"], r["caller_LR"], r["value"]) for r in fleet}) == len(fleet)
    assert all((r["owner"] - FLEET_ROOT - 4) % 132 == 0 and 0 <= r["owner"] - FLEET_ROOT - 4 < 64 * 132 for r in fleet)
    return live, dict(holds=rows, trend_field_writes=changed, ordinary_trend_update_calls=trend_calls,
        fleet_writer_distinct_call_and_value_rows=fleet, original_Missionary_label_getter_called=False)


def offline(arm, raw):
    cpu, get = runtime.get_machine(arm, raw)
    scratch, stream, buffer, objects = 0x023F0200, 0x023F0300, 0x023F0400, 0x023F0500
    assert get(0xCB178) == TOWN_ROOT
    assert get(0x2BFDC, OBJECT) == get(0x2BFF8, OBJECT) == 6
    cases = [0, 1, 32, 90, 113, 114, 115, 125, 255, 256, 0xFFFFFF]
    cpu.mem_write(scratch + 0x74, pack("<I", objects))
    for i, low in enumerate(cases):
        token = 0x06000000 | low
        assert get(RESOLVE - BASE, token) == OBJECT
        cpu.mem_write(objects + 4 * i, pack("<I", token))
        assert get(0x4F920, scratch, i) == OBJECT
    guard = pack("<I", VTABLE) + b"\xCA\xFE" + b"\xA5" * 10
    cpu.mem_write(scratch, guard)
    get(RESET - BASE, scratch)
    assert bytes(cpu.mem_read(scratch, len(guard))) == guard[:4] + b"\x73\x7D" + guard[6:]
    for values in ((0, 0), (32, 25), (69, 76), (114, 114), (115, 125)):
        payload = bytearray(0x48)
        pack_into("<I", payload, 8, 8)
        pack_into("<2I", payload, 0x1C, buffer, 3)
        example = b"AAA" + bytes(values) + b"AAA"
        cpu.mem_write(stream, bytes(payload))
        cpu.mem_write(buffer, example)
        assert get(READ - BASE, scratch, stream) == 1
        assert bytes(cpu.mem_read(scratch, len(guard))) == guard[:4] + bytes(values) + guard[6:]
        assert bytes(cpu.mem_read(buffer, len(example))) == example
        assert unpack_from("<I", cpu.mem_read(stream + 0x20, 4))[0] == 5
        cpu.mem_write(stream, bytes(payload))
        cpu.mem_write(buffer, b"B" * len(example))
        assert get(WRITE - BASE, scratch, stream) == 1
        assert bytes(cpu.mem_read(buffer, len(example))) == b"BBB" + bytes(values) + b"BBB"
        assert unpack_from("<I", cpu.mem_read(stream + 0x20, 4))[0] == 5
    return dict(type_6_lookup_low_24_bit_cases=cases, list_forwarder_checked=True, reset_bytes=[115, 125],
                native_save_load_two_byte_cases=5, no_gameplay_or_battery_file_modified=True)


def main():
    current = play.current
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    clean, arm = (NdsImage.open(path).read_file(current.ARM) for path in (CLEAN, current.ROM))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    report, trace, evidence = trace_files(stores.ROOT, release, stores.__file__, play.FRAMES, play.END)
    cold, fields, other = trace_files(restore.ROOT, release, restore.__file__, (3200,), 3201)
    paired = read(play.HISTORY)
    assert report["scripted_input_schedule"] == paired["scripted_input_schedule"]
    frames = current.paired.panels
    baseline, trial = (frames.shots(case, "_cold_boot.png") for case in (paired, report))
    for f in play.FRAMES:
        assert frames.picture(baseline[f]).tobytes() == frames.picture(trial[f]).tobytes()
    assert len(trace["source_requests"]) == 18
    assert {r["message_ID"] for r in trace["source_requests"]} == {8, 9, 11, 28, 85, 86, 97, 814, 1494}
    assert not any(r["PC"] == 0x0202BFEC for r in trace["rows"])
    raw, bound = snapshot_fields(report, trace)
    assert raw is not None
    code = native_contract(clean, arm, raw)
    paths = evidence + other + [reference(play.HISTORY)]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE), evidence=paths,
                    code=code, ordinary_gameplay=bound, ordinary_loaded_state=ordinary_fields(cold, fields),
                    offline_options=offline(arm, raw), exact_matching_companion_frames=play.FRAMES,
                    source_requests=trace["source_requests"], ROM_changed=False, new_editorial_credit=0,
                    naturally_produced_Fleet_Info_destination_114_observed=False))
    print("Verified both saved trend fields, four ordinary updates, and",
          len(bound["fleet_writer_distinct_call_and_value_rows"]), "distinct ordinary fleet writer inputs.")


if __name__ == "__main__":
    main()
