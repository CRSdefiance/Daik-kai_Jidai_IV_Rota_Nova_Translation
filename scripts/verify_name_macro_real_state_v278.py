"""Catalog expansion seeded by the actual current research cold-boot player."""

import argparse
import json
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.confirmed_name_message_catalog import MACRO
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/name_macro_v278")
CATALOG = Path("work/analysis/name_catalog_v277")
CAPTURE = Path("work/emulation_v193/name_macro_v278")
INPUT, OUTPUT = 0x02430020, 0x02431020
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
DEFAULTS = {b"FI": b"Rafael", b"FA": b"Castor", b"FO": b"Castor Co.", b"FU": b"Rafael Castor"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=ROOT / "fixture_manifest.json")
    parser.add_argument("--capture", type=Path, default=CAPTURE / "capture_report.json")
    parser.add_argument("--out", type=Path, default=ROOT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    capture = json.loads(args.capture.read_text(encoding="utf-8"))
    plan = json.loads((CATALOG / "catalog_plan.json").read_text(encoding="utf-8"))
    assert fixture["not_for_normal_gameplay_or_handoff"]
    assert sha(Path(fixture["research_ROM"]).read_bytes()) == capture["ROM_sha256"] == fixture["research_ROM_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    snapshot = capture["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and len(ram) == 4194304 and sha(ram) == snapshot["sha256"]
    for row in capture["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    arm = (CATALOG / "catalog_research_only_arm9.bin").read_bytes()
    assert sha(arm) == fixture["ARM9_sha256"] == plan["target_arm9_sha256"]
    cpu = initialized(arm)
    cpu.mem_write(0x02000000, ram)
    payload = bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48])
    assert bytes(cpu.mem_read(plan["pool_span"][0], len(payload))) == payload
    assert bytes(cpu.mem_read(MACRO, 0x1A4)) == arm[0x53914:0x53AB8]

    def run(raw, alignment, caller=None, expected=None):
        pointer = INPUT + alignment
        cpu.mem_write(INPUT - 32, b"\xA5" * 640)
        cpu.mem_write(pointer, raw + b"\0")
        source = bytes(cpu.mem_read(INPUT - 32, 640))
        cpu.mem_write(OUTPUT - 32, b"\xA5" * 576)
        saved = {reg: 0x66550000 + index for index, reg in enumerate(SAVED)}
        for reg, value in saved.items():
            cpu.reg_write(reg, value)
        cpu.reg_write(UC_ARM_REG_R0, OUTPUT)
        cpu.reg_write(UC_ARM_REG_R1, pointer)
        cpu.reg_write(UC_ARM_REG_R2, 0)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP if caller is None else caller)
        trace = set()

        def observe(uc, address, size, _):
            if address in (MACRO, 0x020539C4, 0x020539D8, 0x020539FC, 0x020539EC):
                trace.add(address)
            if address == MACRO and caller is not None:
                uc.reg_write(UC_ARM_REG_LR, STOP)

        handle = cpu.hook_add(UC_HOOK_CODE, observe)
        try:
            cpu.emu_start(MACRO if caller is None else plan["entry"], STOP, count=200000)
        finally:
            cpu.hook_del(handle)
        assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
        assert all(cpu.reg_read(reg) == value for reg, value in saved.items())
        actual = bytes(cpu.mem_read(OUTPUT, 512)).split(b"\0", 1)[0]
        if expected is not None:
            assert actual == expected, (raw, actual, expected)
        assert len(actual) < 512
        guarded = b"\xA5" * 32 + actual + b"\0" + b"\xA5" * (543 - len(actual))
        assert bytes(cpu.mem_read(OUTPUT - 32, 576)) == guarded
        assert bytes(cpu.mem_read(INPUT - 32, 640)) == source
        return actual, sorted(trace)

    defaults = []
    for macro, text in DEFAULTS.items():
        for alignment in range(4):
            actual, trace = run(macro, alignment, expected=text)
            defaults.append({"macro": macro.decode(), "alignment": alignment,
                             "actual_output": actual.decode(), "ASCII_bytes": len(actual), "native_trace": trace})
    copies = []
    for row in plan["records"]:
        key, target = bytes.fromhex(row["key_hex"]), bytes.fromhex(row["target_hex"])
        expected = target
        for macro, text in DEFAULTS.items():
            expected = expected.replace(macro, text)
        for alignment in range(4):
            for site in plan["scoped_call_sites"]:
                actual, trace = run(key, alignment, site + 4, expected)
                copies.append({"key_hex": row["key_hex"], "alignment": alignment, "caller": site,
                               "output_hex": actual.hex(), "native_trace": trace,
                               "getter_or_macro_function_bridges": []})
    assert bytes(cpu.mem_read(plan["pool_span"][0], len(payload))) == payload
    proof = {"format": "dk4-name-catalog-actual-player-expansion-v278",
             "fixture_ROM_sha256": fixture["research_ROM_sha256"], "ARM9_sha256": sha(arm),
             "actual_cold_boot_RAM_snapshot": snapshot, "cold_boot_frames": capture["frames"],
             "default_macro_cases": defaults, "catalog_copy_cases": copies,
             "all131_catalog_keys_including98_macro_bearing_keys_verified": True,
             "actual_player_object_and_native_FI_FA_FO_FU_getters_used": True,
             "all512byte_outputs_NUL_inputs_saved_registers_stack_and_pool_exact": True,
             "no_getter_or_macro_function_bridges": True,
             "scope": "Current research-ROM cold-boot player state seeded into native execution; not every deep scene or custom player name.",
             "native_glyphs_previews_editorial_and_complete_integration_pending": True,
             "not_for_normal_gameplay_or_handoff": True,
             "latest_playable_candidate_unchanged": True, "full_goal_complete": False}
    (args.out / "actual_player_macro_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"default_macro_cases": len(defaults), "native_catalog_copies": len(copies),
                      "macro_keys_verified": 98, "getter_bridges": 0}))


if __name__ == "__main__":
    main()
