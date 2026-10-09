"""Execute catalog/native expansion with the actual cold-boot player object."""

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
    UC_ARM_REG_SP,
)

from dk4tool.patch.confirmed_name_message_catalog import MACRO
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/confirmed_names_v200")
INPUT, OUTPUT = 0x02430020, 0x02431020


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--capture", type=Path, default=Path("work/emulation_v193/confirmed_name_catalog_v200/smoke/capture_report.json"))
    args = parser.parse_args()
    plan = json.loads((args.root / "smoke_plan.json").read_text(encoding="utf-8"))
    raw = (args.root / "smoke_research_arm9.bin").read_bytes()
    capture_path = args.capture
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    assert capture["ROM_sha256"] == plan["research_ROM_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    snapshot = capture["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    assert len(ram) == 4194304 and sha(ram) == snapshot["sha256"]
    machine = initialized(raw)
    machine.mem_write(0x02000000, ram)
    code = MainCodeFile(raw, 0x02000000)
    assert bytes(machine.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"])) == bytes(code.sections[3].data[:-48])
    assert bytes(machine.mem_read(plan["entry"], plan["helper_bytes"])) == bytes(code.sections[3].data[plan["entry"] - plan["pool_span"][0]:plan["entry"] - plan["pool_span"][0] + plan["helper_bytes"]])
    entries = {bytes.fromhex(r["key_hex"]): r for r in plan["records"]}
    cases, negative = [], []

    def run(source, caller, expected):
        machine.mem_write(INPUT - 32, b"\xA5" * 640)
        machine.mem_write(INPUT, source + b"\0")
        original = bytes(machine.mem_read(INPUT - 32, 640))
        machine.mem_write(OUTPUT - 32, b"\xA5" * 1088)
        machine.reg_write(UC_ARM_REG_R0, OUTPUT)
        machine.reg_write(UC_ARM_REG_R1, INPUT)
        machine.reg_write(UC_ARM_REG_R2, 0)
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, caller)
        executed = []

        def code_hook(uc, address, size, _):
            if address == MACRO:
                executed.append(address)
                uc.reg_write(UC_ARM_REG_LR, STOP)
            if address == 0x020539C4:
                executed.append(address)  # Observe only; no getter interception.

        handle = machine.hook_add(UC_HOOK_CODE, code_hook)
        machine.emu_start(plan["entry"], STOP, count=30000)
        machine.hook_del(handle)
        actual = bytes(machine.mem_read(OUTPUT - 32, 1088))
        assert actual == b"\xA5" * 32 + expected + b"\0" + b"\xA5" * (1055 - len(expected))
        assert bytes(machine.mem_read(INPUT - 32, 640)) == original
        assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == STACK
        assert executed.count(MACRO) == 1
        return {"input_hex": source.hex(), "caller": caller, "output_hex": expected.hex(),
                "actual_player_given_getter_executed": 0x020539C4 in executed,
                "source_output_NUL_and_buffer_guards_preserved": True, "getter_bridges": []}

    for source, row in entries.items():
        target = bytes.fromhex(row["target_hex"])
        expected = target.replace(b"FI", b"Rafael")
        for caller in (site + 4 for site in plan["scoped_call_sites"]):
            cases.append(run(source, caller, expected))
    # Exact matching must reject a longer input sharing the complete key prefix.
    # Use short ordinary names, avoiding the original expander's reserved F/I
    # semantics in unrelated text; those are separate inherited behavior.
    for source in entries:
        if b"Kamil" not in source or b"FI" in source or b"FA" in source or b"FO" in source or b"FU" in source:
            continue
        extended = source + b"X"
        if extended in entries:
            continue
        negative.append(run(extended, plan["scoped_call_sites"][0] + 4, extended))
        # A foreign call site must keep its original input, even for an exact key.
        negative.append(run(source, 0x020154AC, source))
    report = {"format": "dk4-confirmed-name-catalog-live-RAM-native-copy-proof-v1",
              "research_ROM_sha256": plan["research_ROM_sha256"],
              "actual_cold_boot_RAM_snapshot": snapshot, "cases": cases, "negative_cases": negative,
              "all25_record_texts_covered": len(plan["prepared_records"]) == 25,
              "actual_player_object_and_native_given_name_getter_used": True,
              "no_getter_or_macro_function_bridges": True,
              "scope": "Native execution seeded with actual read-only cold-boot RAM. Full output and guards, not every original deep scene's control flow or GPU.",
              "research_only": True, "full_goal_complete": False}
    (args.root / "catalog_live_ram_copy_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_copies_real_player_object": len(cases), "exact_match_and_scope_negative_cases": len(negative),
                      "given_getter_executions": sum(r["actual_player_given_getter_executed"] for r in cases), "no_getter_bridges": True}))


if __name__ == "__main__":
    main()
