"""Check catalog ABI/startup and native expansion with a real player fixture."""

import argparse
import json
import re
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.patch.confirmed_name_message_catalog import MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.prepare_name_catalog_v233 import ROM, ROOT
from scripts.probe_persistent_name_arm7_boot_overlap import execute
from scripts.verify_confirmed_name_catalog_v200 import REGS
from scripts.verify_ordinary_name_fidelity_research import initialized

INPUT, OUTPUT = 0x02430020, 0x02431020
DEFAULTS = {b"FI": b"Rafael", b"FA": b"Castor", b"FO": b"Castor Co.", b"FU": b"Rafael Castor"}


def main():
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    ROOT = parser.parse_args().root
    plan = json.loads((ROOT / "catalog_plan.json").read_text(encoding="utf-8"))
    raw = (ROOT / "catalog_research_arm9.bin").read_bytes()
    if sha(raw) != plan["target_arm9_sha256"]:
        raise ValueError("Catalog research binary differs")
    image = NdsImage.open(ROM)
    stage = MainCodeFile(raw, BASE).sections[3]
    boot = execute(raw, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                   plan["copy_entry"], bytes(stage.data[:-48]))
    if (boot["arm7_source_changed_bytes_after_arm9_autoload"]
            or not all(r["matches_original"] for r in boot["arm7_native_loaded_sections"])
            or not all(boot[k] for k in ("repaired_pool_matches_complete_payload",
                                        "repair_returns_with_stack_preserved",
                                        "actual_startup_call_preserves_r0_r3"))):
        raise ValueError("Expanded catalog startup/ARM7 ownership fails")
    machine = initialized(raw)
    scoped = [site + 4 for site in plan["scoped_call_sites"]]
    foreign = 0x020154AC
    lookup = []
    for row in plan["records"]:
        key = bytes.fromhex(row["key_hex"])
        for alignment in range(4):
            pointer = INPUT + alignment
            for caller in (*scoped, foreign):
                machine.mem_write(INPUT - 32, b"\xa5" * 640)
                machine.mem_write(pointer, key + b"\0")
                source_before = bytes(machine.mem_read(INPUT - 32, 640))
                registers = {reg: 0x12345000 + index * 0x100 for index, reg in enumerate(REGS)}
                registers[UC_ARM_REG_R0], registers[UC_ARM_REG_R2] = OUTPUT, 0
                for reg, value in registers.items():
                    machine.reg_write(reg, value)
                machine.reg_write(UC_ARM_REG_R1, pointer)
                machine.reg_write(UC_ARM_REG_LR, caller)
                machine.reg_write(UC_ARM_REG_SP, STACK)

                def stop(uc, address, size, _):
                    if address == MACRO:
                        uc.emu_stop()

                def writes(uc, access, address, size, value, _):
                    if not STACK - 256 <= address < address + size <= STACK:
                        raise ValueError("Lookup writes outside its temporary stack")

                a = machine.hook_add(UC_HOOK_CODE, stop)
                b = machine.hook_add(UC_HOOK_MEM_WRITE, writes)
                machine.emu_start(plan["entry"], STOP, count=50000)
                machine.hook_del(a)
                machine.hook_del(b)
                expected = row["target_pointer"] if caller in scoped else pointer
                if (machine.reg_read(UC_ARM_REG_PC) != MACRO or machine.reg_read(UC_ARM_REG_R1) != expected
                        or machine.reg_read(UC_ARM_REG_LR) != caller or machine.reg_read(UC_ARM_REG_SP) != STACK
                        or any(machine.reg_read(reg) != value for reg, value in registers.items())
                        or bytes(machine.mem_read(INPUT - 32, 640)) != source_before):
                    raise ValueError("Lookup scope/alignment/register/source guard differs")
                lookup.append({"key_hex": row["key_hex"], "alignment": alignment,
                               "caller": caller, "catalog_selected": caller in scoped})

    keys = {bytes.fromhex(row["key_hex"]) for row in plan["records"]}
    negatives = []
    for key in keys:
        variants = [("extended-before-NUL", key + b"X"), ("truncated", key[:-1]),
                    ("first-byte-changed", bytes((key[0] ^ 1,)) + key[1:])]
        for kind, variant in variants:
            if not variant or variant in keys:
                continue
            machine.mem_write(INPUT - 32, b"\xa5" * 640)
            machine.mem_write(INPUT, variant + b"\0")
            original = bytes(machine.mem_read(INPUT - 32, 640))
            machine.reg_write(UC_ARM_REG_R0, OUTPUT)
            machine.reg_write(UC_ARM_REG_R1, INPUT)
            machine.reg_write(UC_ARM_REG_R2, 0)
            machine.reg_write(UC_ARM_REG_LR, scoped[0])
            machine.reg_write(UC_ARM_REG_SP, STACK)

            def stop_negative(uc, address, size, _):
                if address == MACRO:
                    uc.emu_stop()

            hook = machine.hook_add(UC_HOOK_CODE, stop_negative)
            machine.emu_start(plan["entry"], STOP, count=50000)
            machine.hook_del(hook)
            if (machine.reg_read(UC_ARM_REG_PC) != MACRO or machine.reg_read(UC_ARM_REG_R1) != INPUT
                    or machine.reg_read(UC_ARM_REG_SP) != STACK
                    or bytes(machine.mem_read(INPUT - 32, 640)) != original):
                raise ValueError("Exact-NUL lookup matches an altered or incomplete source")
            negatives.append({"kind": kind, "input_hex": variant.hex(), "original_input_retained": True})

    # The snapshot comes from the earlier named research cold boot, not an
    # alleged current-V218 physical playthrough. Keep its real player/heap and
    # alter only static code/data differences plus the new owned pool payload.
    capture_path = Path("work/emulation_v193/confirmed_name_catalog_v201/smoke/capture_report.json")
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    snapshot = capture["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    captured_rom = NdsImage.open(capture["ROM"])
    if (sha(Path(capture["ROM"]).read_bytes()) != capture["ROM_sha256"]
            or not capture["cold_boot"] or capture["savestate_loaded"] or capture["callback_errors"]
            or len(ram) != 0x400000 or sha(ram) != snapshot["sha256"]):
        raise ValueError("Actual named-player cold-boot fixture identity differs")
    machine.mem_write(BASE, ram)
    before = MainCodeFile(captured_rom.read_file("/__arm9__.bin"), BASE).sections[0]
    after = MainCodeFile(raw, BASE).sections[0]
    if before.ramAddress != after.ramAddress or len(before.data) != len(after.data):
        raise ValueError("Player fixture static-section ownership differs")
    changed = 0
    for index, (old, new) in enumerate(zip(before.data, after.data, strict=True)):
        if old != new:
            machine.mem_write(BASE + index, bytes((new,)))
            changed += 1
    machine.mem_write(POOL, bytes(stage.data[:-48]))
    protected_pool = bytes(machine.mem_read(POOL, plan["pool_payload_bytes"]))
    copies = []
    for row in plan["records"]:
        key, target = bytes.fromhex(row["key_hex"]), bytes.fromhex(row["target_hex"])
        # CP932 bytes and macros are independent; the reserved literals use the
        # existing full-width glyphs. This expected replacement is not a bridge.
        expected = re.sub(rb"F[IAOU]", lambda match: DEFAULTS[match[0]], target)
        for caller in scoped:
            machine.mem_write(INPUT - 32, b"\xa5" * 640)
            machine.mem_write(INPUT, key + b"\0")
            source_before = bytes(machine.mem_read(INPUT - 32, 640))
            machine.mem_write(OUTPUT - 32, b"\xa5" * 1088)
            machine.reg_write(UC_ARM_REG_R0, OUTPUT)
            machine.reg_write(UC_ARM_REG_R1, INPUT)
            machine.reg_write(UC_ARM_REG_R2, 0)
            machine.reg_write(UC_ARM_REG_SP, STACK)
            machine.reg_write(UC_ARM_REG_LR, caller)
            visited = []

            def observe(uc, address, size, _, visited=visited):
                if address == MACRO:
                    visited.append(address)
                    # Explicit return boundary for this direct invocation. No
                    # name getter, player function or expander result is bridged.
                    uc.reg_write(UC_ARM_REG_LR, STOP)

            hook = machine.hook_add(UC_HOOK_CODE, observe)
            machine.emu_start(plan["entry"], STOP, count=100000)
            machine.hook_del(hook)
            actual = bytes(machine.mem_read(OUTPUT - 32, 1088))
            wanted = b"\xa5" * 32 + expected + b"\0" + b"\xa5" * (1055 - len(expected))
            if (actual != wanted or bytes(machine.mem_read(INPUT - 32, 640)) != source_before
                    or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
                    or visited != [MACRO]):
                rendered = bytes(machine.mem_read(OUTPUT, 512)).split(b"\0", 1)[0]
                raise ValueError(f"Native macro copy differs: key={key.hex()}, expected={expected.hex()}, actual={rendered.hex()}")
            copies.append({"key_hex": row["key_hex"], "caller": caller, "complete_output_hex": expected.hex(),
                           "source_output_NUL_and_guards_preserved": True, "getter_or_expander_bridges": []})
    if bytes(machine.mem_read(POOL, plan["pool_payload_bytes"])) != protected_pool:
        raise ValueError("Native copies mutate inherited/catalog pool bytes")
    result = {"format": "dk4-name-catalog-native-proof-v233", "target_arm9_sha256": sha(raw),
              "boot": boot, "lookup_cases": lookup, "negative_exact_match_cases": negatives,
              "native_copy_cases": copies,
              "actual_player_fixture_capture": capture_path.as_posix(), "player_fixture_snapshot": snapshot,
              "static_bytes_patched_from_named_research_fixture": changed,
              "all_inherited_and_catalog_pool_bytes_preserved": True,
              "all_prepared_records_and_unique_keys_covered": True,
              "prepared_record_count": len(plan["prepared_records"]), "unique_key_count": len(plan["records"]),
              "no_getter_or_macro_result_bridges": True,
              "scope": "Current-V218 startup and catalog ABI; full native expansion with an explicit earlier real named-player fixture. Not current-V218 physical pixels, original deep scenes or a playable whole-name migration.",
              "research_only_no_ROM_created": True, "full_goal_complete": False}
    (ROOT / "native_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"lookup_cases": len(lookup), "negative_exact_match_cases": len(negatives),
                      "native_copies": len(copies),
                      "startup_ARM7_and_cache_pass": True, "no_getter_bridges": True, "research_only": True}))


if __name__ == "__main__":
    main()
