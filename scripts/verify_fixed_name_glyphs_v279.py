"""Route-specific real-player expansion and independent fixed-body pixels."""

import argparse
import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.codec import parse_markup
from dk4tool.patch.confirmed_name_message_catalog import MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_name_catalog_glyphs_v278 import HEIGHT, WIDTH, expected_pixels, raster
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/fixed_names_v279")
BASE_ROM = Path("work/analysis/name_macro_v278/final/name_macro_research_only.nds")
CONTEXTS = {
    "/data/SC0.DK4": ("rafael", BASE_ROM, Path("work/emulation_v193/name_macro_v278_final")),
    "/data/SC1.DK4": ("hodram", BASE_ROM, Path("work/emulation_v193/fixed_names_v279_hodram")),
    "/data/SC2.DK4": ("lil", BASE_ROM, Path("work/emulation_v193/fixed_names_v279_lil")),
    "/data/SC3.DK4": ("maria", ROOT / "maria_selection_research_only.nds", Path("work/emulation_v193/fixed_names_v279_maria")),
}
INPUT, OUTPUT = 0x02430020, 0x02431020


def expand(cpu, text):
    cpu.mem_write(INPUT - 32, b"\xA5" * 640)
    cpu.mem_write(INPUT, text + b"\0")
    before = bytes(cpu.mem_read(INPUT - 32, 640))
    cpu.mem_write(OUTPUT - 32, b"\xA5" * 576)
    cpu.reg_write(UC_ARM_REG_R0, OUTPUT)
    cpu.reg_write(UC_ARM_REG_R1, INPUT)
    cpu.reg_write(UC_ARM_REG_R2, 0)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.emu_start(MACRO, STOP, count=200000)
    assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
    result = bytes(cpu.mem_read(OUTPUT, 512)).split(b"\0", 1)[0]
    assert bytes(cpu.mem_read(INPUT - 32, 640)) == before
    assert bytes(cpu.mem_read(OUTPUT - 32, 576)) == b"\xA5" * 32 + result + b"\0" + b"\xA5" * (543 - len(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-dir", type=Path)
    parser.add_argument("--out", type=Path, default=ROOT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    active_contexts = CONTEXTS
    if args.fixture_dir:
        active_contexts = {
            f"/data/SC{i}.DK4": (name, args.fixture_dir / (
                "maria_selection_research_only.nds" if name == "maria" else "named_catalog_research_only.nds"),
                Path(f"work/emulation_v193/name_editorial_v280_{name}"))
            for i, name in enumerate(("rafael", "hodram", "lil", "maria"))
        }
    proposal = json.loads((ROOT / "fixed_record_proposal.json").read_text(encoding="utf-8"))
    contexts, cases, failures, pictures = [], [], [], []
    for path, (name, rompath, directory) in active_contexts.items():
        rom = NdsImage.open(rompath)
        arm = rom.read_file("/__arm9__.bin")
        capture = json.loads((directory / "capture_report.json").read_text(encoding="utf-8"))
        assert capture["ROM_sha256"] == sha(rompath.read_bytes())
        assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
        snapshot = capture["read_only_RAM_snapshot"]
        ram = Path(snapshot["path"]).read_bytes()
        assert snapshot["read_only_export"] and len(ram) == 4194304 and sha(ram) == snapshot["sha256"]
        cpu = initialized(arm)
        cpu.mem_write(0x02000000, ram)
        pool = bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48])
        assert bytes(cpu.mem_read(POOL, len(pool))) == pool
        defaults = {macro: expand(cpu, macro.encode("ascii")) for macro in ("FI", "FA", "FO", "FU")}
        print(name, {k: v.decode("cp932") for k, v in defaults.items()}, flush=True)
        contexts.append({"route": path, "player": name, "research_ROM_sha256": capture["ROM_sha256"],
                         "actual_RAM_snapshot": snapshot, "actual_macro_defaults": {k: v.decode("cp932") for k, v in defaults.items()},
                         "getter_or_macro_function_bridges": [], "Maria_selection_is_test_only_not_legitimate_unlock": name == "maria"})
        for row in [r for r in proposal["records"] if r["file_path"] == path]:
            target = bytes.fromhex(row["target_hex"])
            tokens = parse_markup(row["formatted_markup"])
            if tokens and tokens[0].kind == "speaker":
                target = target[1:]
            try:
                profile = proposal["profiles_not_registered"][row["current_profile"]]
                for token in parse_markup(row["compiler_safe_markup"]):
                    if token.kind == "macro":
                        assert token.value in defaults
                        assert len(defaults[token.value]) == profile["macro_ascii_lengths"][token.value]
                expected = target
                for macro, value in defaults.items():
                    expected = expected.replace(macro.encode("ascii"), value)
                output = expand(cpu, target)
                assert output == expected
                pixels, events, font = raster(arm, output)
                assert pixels == expected_pixels(arm, font, events)
                semantic = [("ascii", ord(c)) if len(c.encode("cp932")) == 1 else
                            ("cp932", int.from_bytes(c.encode("cp932"), "big"))
                            for c in output.decode("cp932") if c not in " \n"]
                assert [(e["kind"], e["code"]) for e in events if e["code"] != 32] == semantic
                lines = sorted({e["y"] for e in events if e["code"] != 32})
                assert lines == list(range(0, len(lines) * 16, 16)) and len(lines) <= 4
                colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
                image = Image.new("RGB", (WIDTH, HEIGHT))
                image.putdata([colors[c] for c in pixels])
                pictures.append((path + " " + row["id"], image.resize((WIDTH * 2, HEIGHT * 2), Image.Resampling.NEAREST)))
                cases.append({"file_path": path, "id": row["id"], "expanded_body_hex": output.hex(),
                              "native_macro_output_and512byte_guards_exact": True,
                              "all_visible_cells_independent_pixels_first_final_glyphs_and_bounds_exact": True,
                              "lines": lines, "full_fixed_padding_bytes_retained": row["padding_bytes"]})
            except (ValueError, AssertionError) as error:
                failures.append({"file_path": path, "id": row["id"], "error": str(error)})
        assert bytes(cpu.mem_read(POOL, len(pool))) == pool
    sheets = []
    for start in range(0, len(pictures), 8):
        sheet = Image.new("RGB", (WIDTH * 4, 4 * (HEIGHT * 2 + 26)), "#333333")
        draw = ImageDraw.Draw(sheet)
        for n, (label, image) in enumerate(pictures[start:start + 8]):
            x, y = n % 2 * WIDTH * 2, n // 2 * (HEIGHT * 2 + 26)
            draw.text((x + 3, y + 4), label, fill="white")
            sheet.paste(image, (x, y + 26))
        out = args.out / f"native_review_{start // 8:02d}.png"
        sheet.save(out)
        sheets.append(str(out))
    proof = {"format": "dk4-fixed-name-real-macro-native-glyphs-v279", "proposal_sha256": sha((ROOT / "fixed_record_proposal.json").read_bytes()),
             "contexts": contexts, "cases": cases, "failures": failures, "sheets": sheets,
             "fixed_records_expected": proposal["fixed_records"],
             "all_fixed_records_native_pixels_verified": len(cases) == proposal["fixed_records"],
             "scope": "Actual route player RAM, native expansion and controlled216x64 bitmap; original progressive scenes and source editorial gates remain separate.",
             "source_editorial_and_sheet_review_pending": True, "full_integrated_release_pending": True,
             "all18_plaque_hint_entries_remain_incomplete": True, "full_goal_complete": False}
    (args.out / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verified": len(cases), "failed": len(failures), "sheets": len(sheets)}), flush=True)
    if failures:
        print(json.dumps(failures[:8]), flush=True)


if __name__ == "__main__":
    main()
