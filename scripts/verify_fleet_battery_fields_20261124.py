"""Bind the loaded fleet and headquarters bytes to their original save slots."""

from collections import Counter
from pathlib import Path
from struct import pack_into, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import observe_fleet_battery_fields_20261124 as play
from scripts import verify_copenhagen_docking_20261124 as docking
from scripts.probe_button_prompt_native import call, machine
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = docking.OUT.with_name("fleet_battery_fields_20261124.json")
BASE = play.BASE
READER, WRITER, READ_STREAM, WRITE_STREAM = 0x02046A1C, 0x02046C20, 0x020D01AC, 0x020D010C
SRAM_LENGTH, SLOT_LENGTH = 0x3C000, 0xA000
LAYOUT = {"docking": (0x022CFD70, 132, 63), "destination": (0x022CFD70, 132, 63),
          "headquarters": (0x022D8E68, 76, 20)}
SPANS = ((0x02034228, 0x02034360), (0x02034360, 0x02034424), (0x0203CD80, 0x0203CD9C),
         (0x0203CE78, 0x0203CE94), (READER, 0x02046A5C), (WRITER, 0x02046C60),
         (READ_STREAM, 0x020D0274), (WRITE_STREAM, 0x020D0170), (0x020D7650, 0x020D7670),
         (0x020EEC78, 0x020EECA0))


def source_contract(clean, arm):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ops, spans = {}, []
    for lo, hi in SPANS:
        data = arm[lo - BASE:hi - BASE]
        assert data == clean[lo - BASE:hi - BASE]
        spans.append(dict(start=lo, end=hi, exact_sha256=sha256(data).hexdigest()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in decoder.disasm(data, lo)})
    expected = {0x020342B0: "add r1, sl, #0x3c", 0x020342E0: "add r1, sl, #0x3f", 0x0203CD90: "add r1, r5, #0xb",
        0x02046A30: "mov r2, #1", 0x02046A34: "bl #0x20d01ac",
        0x02046C34: "mov r2, #1", 0x02046C38: "bl #0x20d010c",
        0x020D0228: "ldr r3, [r5, #0x20]", 0x020D022C: "mov r0, r1", 0x020D0230: "add r1, ip, r3",
        0x020D0234: "bl #0x20d7650", 0x020D012C: "ldr r0, [r5, #0x20]", 0x020D0130: "add r0, r3, r0",
        0x020D0134: "bl #0x20d7650", 0x020D765C: "ldrb r3, [r1], #1", 0x020D7664: "strb r3, [ip], #1"}
    for pc in play.READS:
        expected[pc] = "bl #0x2046a1c"
    for pc in (0x020343F0, 0x02034420, 0x0203CE90):
        expected[pc] = "bl #0x2046c20"
    assert all(ops[pc] == value for pc, value in expected.items())
    return dict(spans=spans, instructions=expected)


def all_values(arm):
    cpu = machine(arm)
    context, buffer, field = 0x023F1000, 0x023F1200, 0x023F1300
    for value in range(256):
        stream = bytearray(0x48)
        pack_into("<I", stream, 8, 8)
        pack_into("<2I", stream, 0x1C, buffer, 3)
        raw = bytes((0x5A, 0x5A, 0x5A, value, 0x5A, 0x5A, 0x5A, 0x5A))
        cpu.mem_write(context, bytes(stream))
        cpu.mem_write(buffer, raw)
        cpu.mem_write(field - 1, bytes((0xA5, value ^ 255, 0xA5)))
        call(cpu, READER - BASE, (context, field, 0))
        assert bytes(cpu.mem_read(field - 1, 3)) == bytes((0xA5, value, 0xA5))
        assert bytes(cpu.mem_read(buffer, len(raw))) == raw
        assert unpack_from("<I", cpu.mem_read(context + 0x20, 4))[0] == 4
    return dict(byte_values_tested=256, value_114_transfers_directly=True, emulator_gameplay=False,
                scope="Isolated memory-backed reader test. No fabricated battery file or checksum was used.")


def restored(case, release):
    root = play.ROOT / case
    paths = [root / name for name in ("capture/capture_report.json", "requests.json", "terminal.json", "source_contract.json")]
    cap, trace, terminal, contract = map(read, paths)
    inputs, holds, end, _, donor = play.schedule(case)
    assert cap["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert cap["cold_boot"] and not cap["savestate_loaded"] and not cap["callback_errors"]
    assert not any(v for k, v in cap.items() if k.startswith("synthetic_"))
    assert cap["scripted_input_schedule"] == inputs and cap["frames"] == terminal["completed_frames"] == end
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(paths[-1]) and contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {item["PC"] for item in contract["targets"]} == play.CALLS.keys()
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert cap["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert cap["battery_save_preloaded"]["source_sha256"] == digest(donor["source"]) == donor["source_sha256"]
    pairs = list(zip(trace["rows"][::2], trace["rows"][1::2], strict=True))
    assert trace["rows"] == terminal["caption_calls"] and len(pairs) == 146
    restore_frames = sorted({a["frame"] for a, _ in pairs})
    assert len(restore_frames) == 2 and restore_frames[1] == restore_frames[0] + 1 < holds[0]
    offsets, counts, rows = {}, Counter(), []
    for before, after in pairs:
        label, _, field = play.READS[before["PC"]]
        start, stride, count = LAYOUT[label]
        index = counts[label]
        assert before["phase"] == "before" and after["phase"] == "after" and before["field"] == after["field"] == label
        assert before["frame"] == after["frame"] == restore_frames[int(label == "headquarters")]
        assert after["PC"] == before["PC"] + 4 and after["success"] == 1
        assert before["owner"] == after["owner"] == start + stride * index and index < count
        assert before["saved_byte"] == after["value"] and (0 <= after["value"] < 90 or after["value"] == 115)
        assert before["buffer_offset"] not in offsets
        offsets[before["buffer_offset"]] = before["saved_byte"]
        counts[label] += 1
        rows.append(dict(field=label, index=index, live_address=before["owner"] + field,
                         serialized_offset=before["buffer_offset"], saved=before["saved_byte"], prior_live=before["value"]))
    assert dict(counts) == {field: count for field, (_, _, count) in LAYOUT.items()}
    raw = Path(donor["source"]).read_bytes()
    base, = [at for at in range(SRAM_LENGTH - max(offsets)) if all(raw[at + pos] == v for pos, v in offsets.items())]
    assert base % SLOT_LENGTH == 0 and raw[base:base + 4] == b"DK4R"
    slot = raw[base:base + SLOT_LENGTH]
    checksum = sum(value if value < 128 else value - 256 for value in slot[8:]) & 0xFFFFFFFF
    assert unpack_from("<I", slot, 4)[0] == checksum
    assert counts["docking"] == 63 and counts["headquarters"] == 20
    snapshots, = cap["read_only_capture_RAM_snapshots"]
    assert snapshots["frame"] in holds and digest(snapshots["path"]) == snapshots["sha256"]
    return dict(case=case, restore_frames=restore_frames, verified_slot_index=base // SLOT_LENGTH, slot_start=base,
        slot_sha256=sha256(slot).hexdigest(), confirmed_saved_checksum=checksum, pristine_donor=reference(donor["source"]),
        all_read_fields=rows, totals=dict(counts), evidence=list(map(reference, paths)), restored_graphics_hold=snapshots)


def main():
    release = read(play.current.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    clean, arm = (NdsImage.open(p).read_file(play.current.ARM) for p in (CLEAN, play.current.ROM))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    source = source_contract(clean, arm)
    genuine = [restored(case, release) for case in ("copenhagen", "nagasaki")]
    offsets = [{(r["field"], r["index"]): r["serialized_offset"] for r in run["all_read_fields"]} for run in genuine]
    assert offsets[0] == offsets[1] and len(offsets[0]) == 146
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], original_restore_source=source, ordinary_restores=genuine,
        isolated_native_reader=all_values(arm),
        scope="Both observed original slots store original port IDs or 115. Their fields are transferred without remapping at the restore step. Ordinary writers producing special IDs, later load-time processing outside these instructions, and alternate save slots remain outside the observed runs.",
        native_loaded_field_bytes=292, ROM_changed=False, new_editorial_credit=0))
    print("Verified 292 loaded field bytes against two original save slots and all 256 raw byte values in the isolated reader.")


if __name__ == "__main__":
    main()
