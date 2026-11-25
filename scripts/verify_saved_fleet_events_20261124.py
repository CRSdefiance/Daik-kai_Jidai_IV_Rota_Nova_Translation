"""Verify the scheduled fleet event records loaded by the original game."""

from collections import Counter
from pathlib import Path
from struct import pack, pack_into, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import audit_fleet_save_backups_20261124 as backups
from scripts import observe_saved_fleet_events_20261124 as play
from scripts import verify_fleet_battery_fields_20261124 as fleet
from scripts.probe_button_prompt_native import call, machine
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = fleet.OUT.with_name("saved_fleet_events_current_20261124.json")
BASE, OWNER, VTABLE = fleet.BASE, 0x022E082C, 0x0214C618
READER, WRITER = 0x02093C04, 0x02093C90
EVENTS, STRIDE, SIZE, FIRST = 24, 16, 10, 0x7F1F
SPANS = ((0x02093BAC, 0x02093D28), (0x02091464, 0x02091478),
         (0x0204691C, 0x02046958), (0x02046B20, 0x02046B5C),
         (fleet.READER, fleet.READER + 0x3C), (fleet.WRITER, fleet.WRITER + 0x3C),
         (fleet.READ_STREAM, 0x020D0274), (fleet.WRITE_STREAM, 0x020D0170),
         (0x020D7650, 0x020D7670), (0x020EEC78, 0x020EECA0),
         (0x020CB130, 0x020CB13C), (VTABLE + 0x18, VTABLE + 0x20),
         (0x020925E4, 0x02092604), (0x02092774, 0x02092794))


def native_contract(clean, arm):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ops, spans = {}, []
    for start, end in SPANS:
        raw = arm[start - BASE:end - BASE]
        assert raw == clean[start - BASE:end - BASE]
        spans.append(dict(start=start, end=end, sha256=sha256(raw).hexdigest()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in decoder.disasm(raw, start)})
    expected = {pc: "bl #0x2046a1c" for pc in play.READS}
    expected.update({0x02093CAC + i * 0x10: "bl #0x2046c20" for i in range(6)})
    expected.update({0x02093C80: "bl #0x204691c", 0x02093D0C: "bl #0x2046b20",
                     0x02093D1C: "mov r1, #0xb", 0x02093D20: "strb r1, [r0, #4]",
                     0x02092778: "bl #0x20b5600"})
    assert all(ops[pc] == op for pc, op in expected.items()), {pc: ops.get(pc) for pc in expected}
    assert unpack_from("<2I", arm, VTABLE + 0x18 - BASE) == (WRITER, READER)
    assert unpack_from("<I", arm, 0x020CB138 - BASE) == (OWNER - 4,)
    return dict(exact_clean_installed_spans=spans, required_instructions=expected,
                fleet_effect_instructions={pc: op for pc, op in ops.items()
                    if 0x020925E4 <= pc < 0x02092604 or 0x02092774 <= pc < 0x02092794})


def restored(case, release, prior, arm):
    root = play.ROOT / case
    paths = [root / name for name in ("capture/capture_report.json", "requests.json", "terminal.json", "source_contract.json")]
    cap, trace, terminal, contract = map(read, paths)
    inputs, holds, end, _, donor = play.saves.schedule(case)
    assert cap["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert cap["cold_boot"] and not cap["savestate_loaded"] and not cap["callback_errors"]
    assert not any(value for key, value in cap.items() if key.startswith("synthetic_"))
    assert cap["scripted_input_schedule"] == inputs and cap["frames"] == terminal["completed_frames"] == end
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(paths[-1])
    assert trace["observer_sha256"] == digest(play.__file__)
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == play.CALLS.keys()
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert cap["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert cap["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == prior["pristine_donor"]["sha256"]
    raw = Path(donor["source"]).read_bytes()
    assert sha256(raw).hexdigest() == donor["source_sha256"]
    start = prior["verified_slot_index"] * backups.SLOT_BYTES
    slot = raw[start:start + backups.SLOT_BYTES]
    assert sha256(slot).hexdigest() == prior["slot_sha256"]
    assert slot[:4] == b"DK4R" and unpack_from("<I", slot, 4)[0] == prior["confirmed_saved_checksum"]

    pairs = list(zip(trace["rows"][::2], trace["rows"][1::2], strict=True))
    assert trace["rows"] == terminal["caption_calls"] and len(pairs) == EVENTS * len(play.READS)
    frames = {row["frame"] for row in trace["rows"]}
    frame, = frames
    assert frame < holds[0]
    for number, (before, after) in enumerate(pairs):
        index, field = divmod(number, len(play.READS))
        pc = tuple(play.READS)[field]
        name, _, offset = play.READS[pc]
        assert before["PC"] == pc and after["PC"] == pc + 4
        assert before["phase"] == "before" and after["phase"] == "after" and after["success"] == 1
        assert before["field"] == after["field"] == name and offset == field + 4
        assert before["owner"] == after["owner"] == OWNER + index * STRIDE
        assert before["buffer_offset"] == FIRST + index * SIZE + field
        assert before["saved_byte"] == after["value"] == slot[before["buffer_offset"]]

    snapshot, = cap["read_only_capture_RAM_snapshots"]
    assert snapshot["frame"] == holds[0] and digest(snapshot["path"]) == snapshot["sha256"]
    resident = Path(snapshot["path"]).read_bytes()
    for lo, hi in SPANS:
        assert resident[lo - BASE:hi - BASE] == arm[lo - BASE:hi - BASE], hex(lo)
    events = []
    for i in range(EVENTS):
        address = OWNER + i * STRIDE
        live = resident[address - BASE:address - BASE + STRIDE]
        at = FIRST + i * SIZE
        saved = slot[at:at + SIZE]
        assert live[:4] == pack("<I", VTABLE) and live[4:10] + live[12:16] == saved
        events.append(dict(index=i, resident_address=address, slot_offset=at, serialized_hex=saved.hex(),
                           type=saved[0], destination_byte=saved[4]))
    return dict(case=case, load_frame=frame, hold_frame=holds[0], slot_sha256=prior["slot_sha256"],
                verified_slot_index=prior["verified_slot_index"], original_save=reference(donor["source"]),
                traced_byte_calls=len(pairs), records=events, snapshot=snapshot, evidence=list(map(reference, paths)))


def backup_inventory():
    audited = read(backups.OUT)
    fields = {"scheduled_events": list(range(FIRST, FIRST + EVENTS * SIZE))}
    checked, vectors, types, pairs = [], {}, Counter(), Counter()
    for before in audited["backups"]:
        after = backups.backup_slots(Path(before["path"]), fields)
        assert before["sha256"] == after["sha256"]
        slots = []
        for old, new in zip(before["slots"], after["slots"], strict=True):
            assert all(old[key] == new[key] for key in ("slot_index", "sha256", "status"))
            if new["status"] == "valid":
                vector = new["fields_hex_by_index"]["scheduled_events"]
                raw = bytes.fromhex(vector)
                assert len(raw) == EVENTS * SIZE
                key = new["sha256"]
                assert vectors.setdefault(key, vector) == vector
                types.update(raw[::SIZE])
                pairs.update(zip(raw[::SIZE], raw[4::SIZE], strict=True))
            slots.append({key: new[key] for key in ("slot_index", "sha256", "status")})
        checked.append(dict(path=after["path"], sha256=after["sha256"], slots=slots))
    count = audited["slot_states"]["valid"]
    assert len(vectors) == audited["distinct_valid_slots"] and sum(types.values()) == count * EVENTS
    return dict(previous_inventory=reference(backups.OUT), backup_count=len(checked), valid_slots=count,
                distinct_valid_slots=len(vectors), event_type_counts=types,
                type_and_destination_counts=[dict(type=a, destination=b, occurrences=n) for (a, b), n in sorted(pairs.items())],
                backups=checked, event_vectors_by_slot_hash=vectors)


def round_trip(arm):
    cpu = machine(arm)
    context, buffer, owner = 0x023F1000, 0x023F1200, 0x023F1300
    stream = bytearray(0x48)
    pack_into("<I", stream, 8, 16)
    pack_into("<2I", stream, 0x1C, buffer, 3)
    baseline = b"\xa5" * 20
    for kind in (6, 11):
        for destination in range(256):
            raw = bytes((kind, 0x91, 0x32, 0x53, destination, 0xF4)) + pack("<I", 0x01020304 ^ destination)
            serialized = b"\x5a" * 3 + raw + b"\x5a" * 3
            expected = baseline[:6] + raw[:6] + baseline[12:14] + raw[6:] + baseline[18:]
            cpu.mem_write(context, bytes(stream))
            cpu.mem_write(buffer, serialized)
            cpu.mem_write(owner - 2, baseline)
            call(cpu, READER - BASE, (owner, context))
            assert bytes(cpu.mem_read(owner - 2, len(expected))) == expected, (kind, destination)
            assert bytes(cpu.mem_read(buffer, len(serialized))) == serialized
            assert unpack_from("<I", cpu.mem_read(context + 0x20, 4)) == (13,)
            cpu.mem_write(context, bytes(stream))
            cpu.mem_write(buffer, b"\x5a" * 16)
            call(cpu, WRITER - BASE, (owner, context))
            assert bytes(cpu.mem_read(buffer, len(serialized))) == serialized
            assert bytes(cpu.mem_read(owner - 2, len(expected))) == expected
            assert unpack_from("<I", cpu.mem_read(context + 0x20, 4)) == (13,)
    return dict(event_types=[6, 11], destination_values=256, exact_round_trips=512,
                observed_gameplay=False, guard_bytes_checked=True)


def main():
    release = read(play.current.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    clean, arm = (NdsImage.open(p).read_file(play.current.ARM) for p in (CLEAN, play.current.ROM))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    source = native_contract(clean, arm)
    legacy = read(fleet.OUT)
    captures = [restored(prior["case"], release, prior, arm) for prior in legacy["ordinary_restores"]]
    inventory = backup_inventory()
    isolated = round_trip(arm)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], source=source, ordinary_loads=captures,
                    backup_inventory=inventory, isolated_native_serialization=isolated,
                    prior_slot_proof=reference(fleet.OUT), ROM_changed=False, new_editorial_credit=0))
    print(f"Verified two ordinary loads and {inventory['valid_slots']} checksum-valid backup slots. "
          f"Event types across the backups: {dict(inventory['event_type_counts'])}. "
          f"Passed {isolated['exact_round_trips']} isolated native round-trips.")


if __name__ == "__main__":
    main()
