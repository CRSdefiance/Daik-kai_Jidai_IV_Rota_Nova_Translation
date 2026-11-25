"""Verify the story order fallback on exact registered code and saved inputs."""

from collections import Counter

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R5

from scripts import reconcile_fleet_destination_lists_20261123 as lists
from scripts import register_nagasaki_tavern_recruitment_20261124 as active
from scripts import verify_fleet_battery_fields_20261124 as saves
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = lists.OUT.with_name("fleet_authored_fallback_20261124.json")
native = lists.prior
FLEET_GETTER, ACTIVE_INDEX, DOCKING_GETTER = 0x020CB1A8, 0x0202E58C, 0x02034674
START, RAW_READ, WRITER = 0x0202B3DC, 0x0202B42C, native.WRITER
DOCK, ORDER, DESTINATION, FLAGS = 0x3C, 0x3E, 0x3F, 0x50
SPANS = ((START, lists.STORY_ORDER + 4), (DOCKING_GETTER, DOCKING_GETTER + 20), (FLEET_GETTER, FLEET_GETTER + 12),
         (ACTIVE_INDEX, ACTIVE_INDEX + 16), (WRITER, WRITER + 12), (0x0202BED0, 0x0202BF48))


def run_order(cpu, call, fleet, index, operand):
    target_index = (index + 1) % 63
    target = fleet + (target_index - index) * native.FLEET_STRIDE
    before = bytes(cpu.mem_read(target, native.FLEET_STRIDE))
    native.run_fragment(cpu, START, lists.STORY_ORDER, ((UC_ARM_REG_R2, 0x82000000 | operand), (UC_ARM_REG_R5, target)))
    assert cpu.reg_read(UC_ARM_REG_R0) == target and cpu.reg_read(UC_ARM_REG_R1) == 0
    result = cpu.reg_read(UC_ARM_REG_R2)
    call(WRITER - native.BASE, target, 0, result)
    expected = before[:ORDER] + bytes((0, result)) + before[DESTINATION + 1:]
    assert bytes(cpu.mem_read(target, native.FLEET_STRIDE)) == expected
    cpu.mem_write(target, before)
    return result


def main():
    release = read(active.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    ctx = RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=3)
    clean = NdsImage.open(CLEAN)
    original = clean.read_file(active.ARM)
    assert sha256(ctx.arm).hexdigest() == release["target_ARM9_sha256"]
    proof = []
    for start, end in SPANS:
        code = native.code_at(ctx.arm, start, end)
        assert code == native.code_at(original, start, end) == native.code_at(ctx.raw, start, end)
        proof.append(dict(start=start, end=end, exact_hex=code.hex(), sha256=sha256(code).hexdigest()))
    for at, target in ((0x0202BF44, 0x0202B340), (0x0202B404, DOCKING_GETTER), (lists.STORY_ORDER, WRITER)):
        lists.linked(ctx.arm, at, target)

    cpu, call = native.get_machine(ctx.arm, ctx.raw)
    root, index = call(FLEET_GETTER - native.BASE), call(ACTIVE_INDEX - native.BASE)
    assert 0 <= index < 63
    fleet = root + 4 + index * native.FLEET_STRIDE
    raw_reads = Counter()
    cpu.hook_add(UC_HOOK_CODE, lambda _, pc, size, data: raw_reads.update((pc,)), begin=RAW_READ, end=RAW_READ)
    original_flags = cpu.mem_read(fleet + FLAGS, 1)[0]
    pass_counts = []
    for mask in (0, 8):
        cpu.mem_write(fleet + FLAGS, bytes(((original_flags & ~8) | mask,)))
        for slot in range(256):
            cpu.mem_write(fleet + DOCK, bytes((slot,)))
            prior = raw_reads[RAW_READ]
            assert run_order(cpu, call, fleet, index, (slot + 1) % 256) == slot
            assert raw_reads[RAW_READ] - prior == (mask == 8 or slot == 115)
        pass_counts.append(dict(docking_flag=mask, byte_values=256, total_raw_reads=raw_reads[RAW_READ]))
        raw_reads.clear()

    saved = read(saves.OUT)
    observations = []
    for row in saved["ordinary_restores"]:
        snap = row["restored_graphics_hold"]
        raw = native.read_ram(snap)
        assert all(native.code_at(raw, start, end) == native.code_at(ctx.arm, start, end) for start, end in SPANS)
        cpu, call = native.get_machine(ctx.arm, raw)
        root, index = call(FLEET_GETTER - native.BASE), call(ACTIVE_INDEX - native.BASE)
        assert 0 <= index < 63
        fleet = root + 4 + index * native.FLEET_STRIDE
        restored, = [field for field in row["all_read_fields"] if field["index"] == index and field["field"] == "docking"]
        flag, docking = (raw[fleet + offset - native.BASE] for offset in (FLAGS, DOCK))
        assert restored["live_address"] == fleet + DOCK and restored["saved"] == docking and docking != 114
        assert run_order(cpu, call, fleet, index, 114) == docking
        observations.append(dict(case=row["case"], active_index=index, docking_flag=flag & 8, observed_docking=docking,
            exact_saved_field=restored, gameplay_snapshot=snap, offline_fallback_result=docking))

    old, installed = map(lists.story_order_candidates, (clean, ctx.image))
    authored = []
    for source, current in zip(old, installed, strict=True):
        assert source["path"] == current["path"]
        groups = [[r for r in archive["commands"] if not r["order"] and r["usual_marker"]] for archive in (source, current)]
        assert [(r["block"], r["exact_hex"]) for r in groups[0]] == [(r["block"], r["exact_hex"]) for r in groups[1]]
        authored.append(dict(path=source["path"], clean_archive_sha256=source["sha256"], installed_archive_sha256=current["sha256"],
                             clean_marker_candidates=groups[0], installed_marker_candidates=groups[1]))
    assert sum(len(row["clean_marker_candidates"]) for row in authored[:4]) == 11
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], fallback_copies_original_docking_byte=True,
        source_and_installed_spans=proof, original_selector_fixture_cases=pass_counts, real_saved_inputs=observations,
        usual_marker_candidates=authored, fixture_boundaries="The isolated selector and writer run with numeric fixtures in copied RAM. The two docking values come from ordinary save loads. The corresponding story commands were not activated in that gameplay.",
        remaining="A saved or runtime producer could still supply 114. Exact marker scans locate candidates without asserting reachability or command boundaries. Direct headquarters and alternate saved inputs stay open.",
        native_input=ctx.receipt() | {"captain": 3}, proof_sources=list(map(reference, (lists.OUT, saves.OUT, active.RELEASE))),
        new_gameplay=False, ROM_changed=False, new_editorial_credit=0))
    print("Verified 512 authored fallback cases, two original saved inputs and 11 matching retail markers.")


if __name__ == "__main__":
    main()
