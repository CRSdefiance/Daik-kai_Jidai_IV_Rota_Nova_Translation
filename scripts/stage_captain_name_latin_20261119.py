"""Stage the caption glyph correction and replay the verified ordinary paths."""

import argparse
import json
import sys
from pathlib import Path
from struct import pack, unpack_from

from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch import captain_name_latin as patch
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.verify_captain_name_storage_20261119 import ROUNDTRIP
from scripts.verify_rafael_custom_name_20261119 import REPORT, ROM_HASH, ROOT, digest, read

STAGED = ROOT / "staged_latin_v2"
ROM_NAME = "Captain_Name_Latin_RESEARCH_ONLY.nds"
PROOF_NAME = "native_and_stored.json"
CLEAN = Path("work/clean.nds")
ARM = "/__arm9__.bin"
FIELD = 0x02414000


def expected(field):
    if b"\0" not in field:
        return field
    original, tail = field.split(b"\0", 1)
    text = original.decode("cp932", errors="surrogateescape")
    converted = "".join(chr(ord(c) - 0xFEE0) if "Ａ" <= c <= "Ｚ" or "ａ" <= c <= "ｚ" else c for c in text)
    result = converted.encode("cp932", errors="surrogateescape")
    return result.ljust(len(original) + 1, b"\0") + tail


def check_field_matrix(cpu, entry):
    cases = []
    alphabet = ''.join(chr(n) for n in (*range(0xFF21, 0xFF3B), *range(0xFF41, 0xFF5B)))
    for capacity in (3, 17, 19, 20):
        names = [b"", b"FIFI", b"W" * (capacity - 1), b"X" * capacity, b"\x82",
                 b"Rafael" + "Ｍａａ".encode("cp932"), "カＦＩ一ａ〜".encode("cp932")]
        names.extend(c.encode("cp932") for c in alphabet)
        names.extend(b"X" * n + "Ｚ".encode("cp932") for n in range(capacity - 2))
        for name in names:
            field = (name + b"\0").ljust(capacity, b"\xA5")[:capacity]
            cpu.mem_write(FIELD - 4, b"\x5A" * 4 + field + b"\x5A" * 4)
            call(cpu, entry - BASE, (FIELD, capacity))
            after = expected(field)
            assert bytes(cpu.mem_read(FIELD - 4, capacity + 8)) == b"\x5A" * 4 + after + b"\x5A" * 4
            call(cpu, entry - BASE, (FIELD, capacity))
            assert bytes(cpu.mem_read(FIELD, capacity)) == after
            cases.append({"capacity": capacity, "input_hex": field.hex(), "output_hex": after.hex()})
    return cases


def check_routes(cpu, plan):
    hooks, provider = plan["hooks"], plan["provider"]
    editor = FIELD
    stock, village = 0x0215591C, 0x01FF9E38
    assert bytes(cpu.mem_read(provider, 8)) == bytes(cpu.mem_read(stock, 8))
    titles = (*patch.TITLES, 0x023885B4, 0x02156074)
    for title in titles:
        cpu.mem_write(editor + 4, pack("<I", stock))
        cpu.reg_write(UC_ARM_REG_R0, editor)
        cpu.reg_write(UC_ARM_REG_R3, title)
        cpu.emu_start(hooks[patch.EDIT_CONSTRUCTOR], 0x020AFBB0, count=128)
        assert cpu.reg_read(UC_ARM_REG_PC) == 0x020AFBB0
        marked = provider if title in patch.TITLES else village if title == titles[-2] else stock
        assert unpack_from("<I", cpu.mem_read(editor + 4, 4))[0] == marked
    key = FIELD + 0x200
    for kind in (stock, village, provider):
        cpu.mem_write(editor + 4, pack("<I", kind))
        for char in ("Ｆ", "Ｉ", "ａ", "ん", "９", "　"):
            raw = char.encode("cp932") + b"\0"
            cpu.mem_write(key, raw + b"\x5A")
            cpu.reg_write(UC_ARM_REG_R0, editor + 0x38)
            cpu.reg_write(UC_ARM_REG_R1, key)
            cpu.emu_start(hooks[patch.EDIT_APPEND], 0x020B08D8, count=256)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x020B08D8
            result = raw
            if kind == provider:
                result = expected(raw)
            elif kind == village:
                result = {"９": b"9\0\0", "　": b" \0\0"}.get(char, expected(raw))
            assert bytes(cpu.mem_read(key, 4)) == result + b"\x5A"
    sample = "ＦＩゆａ".encode("cp932")
    actor = bytearray(b"\xA5" * 112)
    changed = bytearray(actor)
    for off, size in ((0x20, 17), (0x31, 17), (0x42, 17), (0x55, 19)):
        actor[off:off + len(sample) + 1] = sample + b"\0"
        changed[off:off + size] = expected(actor[off:off + size])
    cpu.mem_write(FIELD, bytes(actor))
    cpu.reg_write(UC_ARM_REG_R5, FIELD)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.emu_start(hooks[patch.MODEL_RESTORE], STOP, count=4096)
    assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
    assert cpu.reg_read(UC_ARM_REG_R5) == FIELD
    assert cpu.reg_read(UC_ARM_REG_R0) == 1 and bytes(cpu.mem_read(FIELD, 112)) == bytes(changed)
    slot = bytearray(b"\xA5" * 96)
    slot[0x30:0x30 + len(sample) + 1] = sample + b"\0"
    expected_slot = bytes(slot[:0x30]) + expected(slot[0x30:0x44]) + bytes(slot[0x44:])
    cpu.mem_write(FIELD, bytes(slot))
    cpu.reg_write(UC_ARM_REG_R2, FIELD)
    cpu.emu_start(hooks[patch.SLOT_DISPLAY], 0x020EFCDC, count=512)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x020EFCDC and cpu.reg_read(UC_ARM_REG_R2) == FIELD
    assert bytes(cpu.mem_read(FIELD, 96)) == expected_slot
    return {"editor_titles": len(titles), "key_cases": 18, "actor_fields": 4, "slot_display_fields": 1}


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def stage(output):
    assert not output.exists()
    initial = read(REPORT)
    parent = Path(initial["ROM"])
    assert digest(parent.read_bytes()) == initial["ROM_sha256"] == ROM_HASH
    image, clean = NdsImage.open(parent), NdsImage.open(CLEAN)
    old = image.read_file(ARM)
    arm, plan = patch.stage(old, clean.read_file(ARM), image.rom.arm9OverlayTable)
    cpu = machine(arm)
    plan["field_cases"] = check_field_matrix(cpu, plan["normalizer"])
    plan["route_cases"] = check_routes(cpu, plan)
    image.replace_file(ARM, arm)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, old)
    assert bytes(image.rom.save()) == parent.read_bytes()
    output.mkdir()
    (output / ROM_NAME).write_bytes(candidate)
    write(output / PROOF_NAME, plan | {"parent_sha256": ROM_HASH, "candidate_sha256": digest(candidate),
                         "whole_parent_inverse": True, "clean_input_sha256": digest(CLEAN.read_bytes())})
    print(f"Staged the four native hooks. Passed {len(plan['field_cases'])} byte-boundary cases and all scope checks.")


def replay(mode, output):
    initial_report = REPORT if mode == "opening" else ROUNDTRIP / "continue/capture/capture_report.json"
    reference = read(initial_report)
    proof = read(output / PROOF_NAME)
    rom = output / ROM_NAME
    assert digest(rom.read_bytes()) == proof["candidate_sha256"]
    root = output / mode
    root.mkdir()
    frames = (2790, 3270, 5130, 5340, 6890, 7220) if mode == "opening" else (2400, 2800, 3850)
    inputs = root / "inputs.json"
    events = reference["scripted_input_schedule"]
    if mode == "save":
        frames += (4150, 4480, 4750, 5080)
        events = [*events, {"start": 3851, "duration": 8, "buttons": ["X"]},
                  {"start": 4151, "duration": 8, "buttons": [], "touch": [123, 91]},
                  {"start": 4481, "duration": 8, "buttons": ["A"]},
                  {"start": 4751, "duration": 8, "buttons": ["A"]}]
    write(inputs, events)
    args = [harness.__file__, "--rom", str(rom), "--out", str(root / "capture"), "--press-start", "-1",
            "--frames", str(frames[-1] + 1), "--touchscreen", "--capture-every", "999999", "--capture-at",
            *map(str, frames), "--dump-capture-ram", "--inputs-json", str(inputs)]
    battery = reference.get("battery_save_preloaded")
    if battery:
        assert digest(Path(battery["source"]).read_bytes()) == battery["source_sha256"]
        args.extend(["--battery-save", battery["source"]])
    old_args = sys.argv
    try:
        sys.argv = args
        harness.main()
    finally:
        sys.argv = old_args
    assert read(root / "capture/capture_report.json")["ROM_sha256"] == proof["candidate_sha256"]


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "opening", "continue", "save"))
    cli.add_argument("--output", type=Path, default=STAGED)
    args = cli.parse_args()
    if args.action == "stage":
        stage(args.output)
    else:
        replay(args.action, args.output)
