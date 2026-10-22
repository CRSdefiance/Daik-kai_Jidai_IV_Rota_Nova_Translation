"""One-branch original regional-background selection; research evidence only."""

import argparse
import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine

ROOT = Path("work/analysis/regional_plaques_v611")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, nargs='+', choices=(610, 611), default=(610, 611))
    versions = parser.parse_args().version
    ROOT.mkdir(parents=True, exist_ok=True)
    inputs = json.loads(Path("work/analysis/fleet_detail_v368/replay_inputs.json").read_text(encoding="utf-8"))
    (ROOT / "fleet_inputs.json").write_text(json.dumps(inputs, indent=2) + "\n", encoding="utf-8")
    for version in versions:
        source = Path(f"out/all_routes_combined_v{version}_candidate.nds")
        rom = NdsImage.open(source)
        before = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
        arm = before["/__arm9__.bin"]
        original = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
        assert arm[0x8E12C:0x8E284] == original[0x8E12C:0x8E284]
        # Force only the existing original regional backdrop branch. The earlier
        # original fleet checks, financial data, input, models and flags stay exact.
        at, target = 0x8E140, 0x0208E1EC
        assert struct.unpack_from("<I", arm, at)[0] == 0x0A000002
        changed = bytearray(arm)
        struct.pack_into("<I", changed, at, 0xEA000000 | ((target - (0x02000000 + at) - 8) // 4 & 0xFFFFFF))
        assert changed[:at] == arm[:at] and changed[at + 4:] == arm[at + 4:]
        rom.replace_file("/__arm9__.bin", bytes(changed))
        path = ROOT / f"V{version}_regional_background_RESEARCH_ONLY.nds"
        assert not path.exists()
        rom.save(path)
        saved = NdsImage.open(path)
        after = {p: d for _, p, d in saved.iter_files()} | dict(saved.iter_components())
        assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == ["/__arm9__.bin"]
        u = machine(arm)
        # Execute the original filename resource constructor through its final
        # stores rather than pairing neighbouring words in the literal pool.
        from unicorn.arm_const import UC_ARM_REG_PC
        u.emu_start(0x0210FAB0, 0x0210FAD4, count=100)
        assert u.reg_read(UC_ARM_REG_PC) == 0x0210FAD4
        owner = 0x02313380
        filename = struct.unpack("<I", u.mem_read(owner + 12, 4))[0]
        assert bytes(u.mem_read(filename, 23)).split(b"\0")[0] == b"_pxl/chihofleetinfo.pxl"
        proof = {"research_only": True, "parent": str(source), "parent_sha256": sha(source.read_bytes()),
                 "research_ROM": str(path), "research_ROM_sha256": sha(path.read_bytes()),
                 "one_original_backdrop_branch_address": 0x02000000 + at, "target": target,
                 "original_financial_checks_data_models_input_and_flags_unchanged": True,
                 "source_initialized_resource_owner": owner, "source_initialized_filename": "_pxl/chihofleetinfo.pxl",
                 "ordinary_regional_fleet_formation_or_reachability_not_claimed": True,
                 "source_parent_complete_background_extent": [0, 0, 256, 192], "full_goal_complete": False}
        path.with_suffix(".fixture.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(versions)} explicit original-background-selector research ROM(s); production code unchanged.")


if __name__ == "__main__":
    main()
