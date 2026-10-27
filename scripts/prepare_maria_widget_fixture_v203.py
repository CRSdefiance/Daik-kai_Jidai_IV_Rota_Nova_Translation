"""Create an explicit research-only fourth-captain widget/display fixture."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R10, UC_ARM_REG_SP

from dk4tool.patch.confirmed_character_names import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/maria_widgets_v203")
SOURCE = Path("out/all_routes_combined_v190_candidate.nds")
OPCODE = 0x9F068
OBJECT = 0x02460000


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(SOURCE.read_bytes()) == "9ccff57aec0326722b89b85877fb5be23e63dc466022b1f7c2e0a984ccdd9424"
    rom = NdsImage.open(SOURCE)
    clean = NdsImage.open("work/clean.nds")
    arm = rom.read_file("/__arm9__.bin")
    named, names = transform(arm, clean.read_file("/__arm9__.bin"))
    assert struct.unpack_from("<I", named, OPCODE)[0] == 0x03A00003
    # Original: MOVEQ r0,#3 after the native saved-flag predicate returns zero.
    # Fixture: MOVEQ r0,#4. No save data or predicate is changed. This is not a
    # legitimate unlock, ordinary gameplay ROM, translation release or handoff.
    fixture = bytearray(named)
    struct.pack_into("<I", fixture, OPCODE, 0x03A00004)
    fixture = bytes(fixture)
    assert [i for i, (a, b) in enumerate(zip(named, fixture, strict=True)) if a != b] == [OPCODE]
    assert fixture[0x46DFC:0x46E30] == arm[0x46DFC:0x46E30] == clean.read_file("/__arm9__.bin")[0x46DFC:0x46E30]
    saved_object = struct.unpack_from("<I", arm, 0x9F0D0)[0]
    assert saved_object == 0x02279824
    cases = []
    for payload, kind in ((named, "original-limit"), (fixture, "fixture-limit")):
        uc = machine(payload)
        for flags in range(16):
            for initial in (2, 3, 4, 0xA5A5A5A5):
                uc.mem_write(saved_object + 0x38, struct.pack("<H", flags))
                uc.mem_write(OBJECT - 16, b"\xA5" * (0x940 + 32))
                uc.mem_write(OBJECT + 0x930, struct.pack("<I", initial))
                original = bytes(uc.mem_read(OBJECT - 16, 0x940 + 32))
                uc.reg_write(UC_ARM_REG_R10, OBJECT)
                uc.reg_write(UC_ARM_REG_SP, STACK)
                uc.emu_start(0x0209F05C, 0x0209F070, count=1000)
                expected = (3 if kind == "original-limit" else 4) if flags == 0 else initial
                actual = struct.unpack("<I", uc.mem_read(OBJECT + 0x930, 4))[0]
                assert actual == expected
                assert uc.reg_read(UC_ARM_REG_PC) == 0x0209F070 and uc.reg_read(UC_ARM_REG_SP) == STACK
                after = bytearray(uc.mem_read(OBJECT - 16, 0x940 + 32))
                after[0x940:0x944] = original[0x940:0x944]
                assert bytes(after) == original
                assert bytes(uc.mem_read(saved_object + 0x38, 2)) == struct.pack("<H", flags)
                cases.append({"kind": kind, "predicate_low_flags": flags, "initial_count": initial,
                              "result_count": actual, "save_flags_and_unowned_object_bytes_preserved": True})
    original_files = {path: bytes(raw) for _, path, raw in rom.iter_files()}
    original_arm7 = bytes(rom.rom.arm7)
    rom.replace_file("/__arm9__.bin", fixture)
    output = ROOT / "maria_widget_selection_fixture_research_only.nds"
    rom.save(output)
    check = NdsImage.open(output)
    assert {path: bytes(raw) for _, path, raw in check.iter_files()} == original_files
    assert bytes(check.rom.arm7) == original_arm7
    assert check.read_file("/__arm9__.bin") == fixture
    inputs = [{"start": frame, "duration": 12, "buttons": [button]}
              for frame, button in ((1000, "START"), (1200, "A"), (1450, "RIGHT"),
                                    (1600, "RIGHT"), (1750, "RIGHT"), (1950, "A"))]
    (ROOT / "inputs.json").write_text(json.dumps(inputs, indent=2) + "\n", encoding="utf-8")
    manifest = {"format": "dk4-maria-widget-research-fixture-v1", "research_ROM": output.as_posix(),
                "research_ROM_sha256": sha(output.read_bytes()), "source_ROM": SOURCE.as_posix(),
                "source_ROM_sha256": sha(SOURCE.read_bytes()), "ARM9_sha256": sha(fixture), "name_fields": names,
                "test_only_selection_limit": {"offset": OPCODE, "original_word": "03A00003", "fixture_word": "03A00004",
                                             "reason": "Expose the fourth captain's unmodified native portrait/widgets for visual verification. This does not prove a legitimate gameplay unlock."},
                "native_selection_predicate_cases": cases,
                "all_script_graphics_files_and_ARM7_exact_to_V190": True,
                "only_difference_after_guarded_names_is_one_test_instruction_byte": True,
                "not_for_normal_gameplay_release_or_handoff": True, "live_capture_pending": True,
                "goal_complete": False}
    (ROOT / "fixture_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_selection_cases": len(cases), "research_ROM_sha256": manifest["research_ROM_sha256"],
                      "test_instruction_changed_bytes": 1, "no_script_or_graphics_changes": True}))


if __name__ == "__main__":
    main()
