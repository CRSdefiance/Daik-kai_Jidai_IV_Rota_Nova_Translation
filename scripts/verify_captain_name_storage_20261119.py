"""Verify captain name owners and all four native save and load field loops."""

import json
from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.verify_rafael_custom_name_20261119 import (
    NAME,
    REPORT,
    ROM_HASH,
    ROOT,
    digest,
    read,
    require_string,
    snapshot,
)

OWNER, INPUT_RECORD, IO = 0x02414000, 0x02415000, 0x02416000
ROUNDTRIP = ROOT / "save_roundtrip_v2"
# Save and load order differs from the editor's visible middle/last order.
FIELDS = (
    ("first", 0x20, 0x08, 17, 0x830B0, 0x82FB8, 0x20),
    ("last", 0x31, 0x2A, 17, 0x830D8, 0x82FE0, 0x24),
    ("middle", 0x42, 0x19, 17, 0x83100, 0x83008, 0x28),
    ("company", 0x55, 0x3B, 19, 0x83148, 0x83050, None),
)


def value(cpu, address):
    return unpack_from("<I", cpu.mem_read(address, 4))[0]


def exercise_save_loop(cpu, offset, storage, start, payload, loading):
    address = OWNER + offset
    cpu.mem_write(OWNER, b"\xA5" * 128)
    cpu.mem_write(IO + 0x28, pack("<I", 0))
    if not loading:
        cpu.mem_write(address, payload)
    before = bytes(cpu.mem_read(OWNER, 128))
    cpu.reg_write(UC_ARM_REG_R4, IO)
    cpu.reg_write(UC_ARM_REG_R5, OWNER)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    backend = BASE + (0xD01AC if loading else 0xD010C)
    observed = []

    def io_contract(uc, at, size, unused):
        cursor = len(observed)
        assert cursor < storage, (hex(start), storage, cursor, loading, hex(uc.reg_read(UC_ARM_REG_R1)))
        assert (uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)) == (
            IO, address + cursor, 1)
        if loading:
            uc.mem_write(address + cursor, payload[cursor:cursor + 1])
        observed.extend(uc.mem_read(address + cursor, 1))
        uc.reg_write(UC_ARM_REG_R0, 1)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    end = BASE + start + 0x28
    hook = cpu.hook_add(UC_HOOK_CODE, io_contract, begin=backend, end=backend)
    exit_hook = cpu.hook_add(UC_HOOK_CODE, lambda uc, *_: uc.emu_stop(), begin=end, end=end)
    try:
        cpu.emu_start(BASE + start, 0, count=10000)
    finally:
        cpu.hook_del(hook)
        cpu.hook_del(exit_hook)
    assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_PC) == end
    assert bytes(observed) == payload and value(cpu, IO + 0x28) == storage, (
        hex(start), loading, bytes(observed).hex(), payload.hex(), value(cpu, IO + 0x28))
    assert bytes(cpu.mem_read(OWNER, 128)) == before[:offset] + payload + before[offset + storage:]


def editor_owners(cpu, memory):
    cpu.mem_write(BASE, memory)
    call(cpu, 0xCB184, ())
    actor = cpu.reg_read(UC_ARM_REG_R0) + 0x19E4
    vtable = value(cpu, actor)
    assert (actor, vtable) == (0x022D5D24, 0x02148E94)
    call(cpu, 0x7F244, ())
    assert cpu.reg_read(UC_ARM_REG_R0) == 0
    assert value(cpu, vtable + 0x18) == BASE + 0x830A0 and value(cpu, vtable + 0x1C) == BASE + 0x82FA8
    assert bytes(cpu.mem_read(actor + 0x20, len(NAME) + 1)) == NAME + b"\0"
    fields = {}
    for name, offset, input_offset, storage, save, load, slot in FIELDS:
        if slot is not None:
            getter = value(cpu, vtable + slot)
            call(cpu, getter - BASE, (actor,))
            assert cpu.reg_read(UC_ARM_REG_R0) == actor + offset
        else:
            getter = None
        data = bytes(cpu.mem_read(actor + offset, storage))
        assert b"\0" in data
        fields[name] = {"actor_offset": offset, "editor_result_offset": input_offset, "storage": storage,
                        "save_loop": hex(BASE + save), "load_loop": hex(BASE + load), "getter": getter,
                        "live_field_hex": data.hex()}
    return fields


def save_roundtrip(cpu, arm):
    reports = {key: ROUNDTRIP / key / "capture/capture_report.json" for key in ("save", "continue")}
    runs = {key: read(path) for key, path in reports.items()}
    assert [runs[key]["frames"] for key in reports] == [28750, 3850]
    for report in runs.values():
        assert report["ROM_sha256"] == ROM_HASH and report["cold_boot"] and not report["savestate_loaded"]
        assert not report["callback_errors"] and not report["hardware_device_verification"]
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert not runs["save"].get("battery_save_preloaded")
    battery = runs["continue"]["battery_save_preloaded"]
    cartridge = Path(battery["source"]).read_bytes()
    assert battery["copied_byte_exact_before_cold_boot"] and not battery["savestate_loaded"]
    assert digest(cartridge) == battery["source_sha256"] == digest(Path(battery["destination"]).read_bytes())
    assert len(cartridge) == 262266
    for offset in (0x34, 0x2729):
        assert cartridge[offset:offset + len(NAME) + 1] == NAME + b"\0"

    cases = (
        ("Save list", "save", 28400, (0x021905A8, 0x022D5D44)),
        ("Continue list", "continue", 2400, (0x02192410, 0x02374F54)),
        ("After loading", "continue", 3850, (0x02249C74, 0x022D5D44)),
    )
    sheet = Image.new("RGB", (256 * len(cases), 404), "white")
    labels = ImageDraw.Draw(sheet)
    evidence = []
    for column, (label, key, frame, addresses) in enumerate(cases):
        report = runs[key]
        memory, ram = snapshot(report["read_only_pause_RAM_snapshots"], frame, "sha256")
        navigation = [row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")]
        _, png = snapshot(navigation, frame, "PNG_sha256")
        with Image.open(png["path"]) as image:
            sheet.paste(image, (256 * column, 20))
        labels.text((4 + 256 * column, 3), label, fill="black")
        evidence.append({"label": label, "frame": frame, "read_only_RAM": ram, "capture": png,
                         "buffers": [require_string(memory, address, NAME) for address in addresses]})
        if label == "After loading":
            evidence[-1]["restored_actor_fields"] = editor_owners(cpu, memory)
    sheet_path = ROUNDTRIP / "saved_name_roundtrip.png"
    sheet.save(sheet_path)
    assert unpack_from("<I", arm, 0xEF4B0)[0] == 0xE2804030
    assert unpack_from("<I", arm, 0xEFE2C)[0] == 0xE2861030
    return {"battery_bytes_identical_after_continue": True, "battery_sha256": battery["source_sha256"],
            "slot_summary_file_offset": 0x34, "captain_model_file_offset": 0x2729,
            "save_detail_summary_name_pointer_instruction": "0x020EF4B0",
            "continue_detail_summary_name_pointer_instruction": "0x020EFE2C",
            "screens": evidence, "sheet": sheet_path.as_posix(), "sheet_sha256": digest(sheet_path.read_bytes()),
            "reports": {p.as_posix(): digest(p.read_bytes()) for p in reports.values()}}


def main():
    report = read(REPORT)
    assert digest(Path(report["ROM"]).read_bytes()) == report["ROM_sha256"] == ROM_HASH
    clean, current = [NdsImage.open(path).read_file("/__arm9__.bin") for path in ("work/clean.nds", report["ROM"])]
    spans = [(0x82FA8, 0x83198), (0xCD6E0, 0xCD710), (0x469DC, 0x46A1C), (0x46BE0, 0x46C20),
             (0xF8EC4, 0xF8F00), (0xF9C34, 0xF9C70)]
    assert all(clean[start:end] == current[start:end] for start, end in spans)
    evidence = read(ROOT / "custom_name_evidence.json")
    raw = evidence["frames"]["6890"]["read_only_RAM"]
    memory = Path(raw["path"]).read_bytes()
    assert digest(memory) == raw["sha256"]
    fields = editor_owners(machine(current), memory)
    cpu = machine(current)
    count = 0
    for data in (NAME, b"FIFI", b"", b"W" * 16, "テストＦＩ".encode("cp932")):
        cpu.mem_write(OWNER, b"\xA5" * 128)
        expected = bytearray(cpu.mem_read(OWNER, 128))
        for _, offset, input_offset, storage, *_ in FIELDS:
            cpu.mem_write(INPUT_RECORD + input_offset, data + b"\0")
            expected[offset:offset + len(data) + 1] = data + b"\0"
        cpu.reg_write(UC_ARM_REG_R4, INPUT_RECORD)
        cpu.reg_write(UC_ARM_REG_R5, OWNER)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.emu_start(BASE + 0xCD6E0, BASE + 0xCD710, count=10000)
        assert bytes(cpu.mem_read(OWNER, 128)) == expected
        for _, offset, _, storage, save, load, _ in FIELDS:
            for start, loading in ((save, False), (load, True)):
                payload = bytes(expected[offset:offset + storage])
                exercise_save_loop(cpu, offset, storage, start, payload, loading)
                count += 1
    for data in (b"W" * 18, "カ".encode("cp932") * 9):
        for start, loading in ((0x83148, False), (0x83050, True)):
            exercise_save_loop(cpu, 0x55, 19, start, data + b"\0", loading)
            count += 1
    proof = {"candidate_sha256": ROM_HASH, "clean_equal_spans": spans, "live_snapshot": raw,
             "fields": fields, "setter_cases": 20, "save_or_load_cases": count,
             "native_byte_helpers_executed": True, "physical_byte_io_backend_modelled": True,
             "live_getters_read_original_model_fields": True, "hardware_verified": False,
             "ordinary_emulator_battery_save_roundtrip": save_roundtrip(cpu, current)}
    (ROOT / "name_storage_ownership.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"Verified all four name fields, 20 native copies and {count} storage cases.")


if __name__ == "__main__":
    main()
