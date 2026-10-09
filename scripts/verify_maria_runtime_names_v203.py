"""Measure default Maria macros from a real cold-boot player object, without bridges."""

import json
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/maria_widgets_v203")
CAPTURE = Path("work/emulation_v193/maria_widgets_v203/player_object")
INPUT, OUTPUT = 0x02430020, 0x02431020


def main():
    manifest = json.loads((ROOT / "fixture_manifest.json").read_text(encoding="utf-8"))
    capture = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert capture["ROM_sha256"] == manifest["research_ROM_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    snapshot = capture["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    assert len(ram) == 4194304 and sha(ram) == snapshot["sha256"]
    arm = NdsImage.open(manifest["research_ROM"]).read_file("/__arm9__.bin")
    assert sha(arm) == manifest["ARM9_sha256"]
    uc = initialized(arm)
    uc.mem_write(0x02000000, ram)
    assert bytes(uc.mem_read(0x02053914, 0x1A4)) == arm[0x53914:0x53AB8]
    defaults = {"FI": ("Maria", 0x020539C4), "FA": ("Li", 0x020539D8),
                "FO": ("Li Clan", 0x020539FC), "FU": ("Maria Huamei Li", 0x020539EC)}
    cases = []
    for token, (text, branch) in defaults.items():
        for alignment in range(4):
            uc.mem_write(INPUT - 32, b"\xA5" * 640)
            uc.mem_write(INPUT + alignment, token.encode("ascii") + b"\0")
            before = bytes(uc.mem_read(INPUT - 32, 640))
            uc.mem_write(OUTPUT - 32, b"\xA5" * 1088)
            for reg, value in ((UC_ARM_REG_R0, OUTPUT), (UC_ARM_REG_R1, INPUT + alignment),
                               (UC_ARM_REG_R2, 0), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
                uc.reg_write(reg, value)
            trace = set()

            def observe(u, address, size, _, trace=trace):
                trace.add(address)

            handle = uc.hook_add(UC_HOOK_CODE, observe)
            try:
                uc.emu_start(0x02053914, STOP, count=100000)
            finally:
                uc.hook_del(handle)
            expected = text.encode("ascii")
            assert bytes(uc.mem_read(OUTPUT - 32, 1088)) == b"\xA5" * 32 + expected + b"\0" + b"\xA5" * (1055 - len(expected))
            assert bytes(uc.mem_read(INPUT - 32, 640)) == before
            assert uc.reg_read(UC_ARM_REG_PC) == STOP and uc.reg_read(UC_ARM_REG_SP) == STACK
            assert uc.reg_read(UC_ARM_REG_R0) == 0 and branch in trace
            cases.append({"macro": token, "source_alignment": alignment, "output": text,
                          "ASCII_bytes": len(expected), "native_macro_branch_executed": branch,
                          "source_output_NUL_and_stack_guards_preserved": True, "getter_bridges": []})
    preparation = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    profiles = {r["proposed_profile"] for r in preparation["records"] if r["file_path"] == "/data/SC3.DK4"}
    for key in profiles:
        profile = preparation["proposed_profiles_not_registered"][key]
        for token in ("FI", "FA", "FO"):
            text = defaults[token][0]
            assert profile["macro_ascii_lengths"][token] == len(text)
            assert profile["macro_widths"][token] == len(text) * 6
    proof = {"format": "dk4-maria-actual-player-default-macro-proof-v1",
             "research_ROM_sha256": manifest["research_ROM_sha256"], "actual_RAM_snapshot": snapshot,
             "cases": cases, "no_getter_or_expander_function_bridges": True,
             "default_macro_calibration": {token: {"text": text, "ASCII_bytes": len(text),
                                                  "native_font_width_px": len(text) * 6}
                                           for token, (text, _) in defaults.items()},
             "prepared_Maria_profile_FI_FA_FO_calibrations_match": True,
             "prepared_Maria_FU_records": [r["id"] for r in preparation["records"]
                                          if r["file_path"] == "/data/SC3.DK4" and "{MACRO:FU}" in r["english"]],
             "scope": "Default names/faction/full name from actual Maria player state initialized through the test-only selector fixture. Not arbitrary custom names, complete macro consumers/layout or legitimate unlock progression.",
             "not_for_normal_gameplay_release_or_handoff": True, "registered_ROM_changed": False,
             "goal_complete": False}
    (ROOT / "native_default_macro_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"actual_player_macro_cases": len(cases), "macro_default_lengths": {k: len(v[0]) for k, v in defaults.items()},
                      "prepared_Maria_profiles_match": True, "no_getter_bridges": True}))


if __name__ == "__main__":
    main()
