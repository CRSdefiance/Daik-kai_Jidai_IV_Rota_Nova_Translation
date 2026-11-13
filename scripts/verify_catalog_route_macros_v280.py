"""Current catalog targets from each owner's actual route player context."""

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
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK
from scripts.verify_fixed_name_glyphs_v279 import expand
from scripts.verify_name_catalog_glyphs_v278 import HEIGHT, WIDTH, expected_pixels, raster
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/name_editorial_v280")
CATALOG = Path("work/analysis/name_catalog_v277")


def main():
    plan = json.loads((CATALOG / "catalog_plan.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "fixture_manifest.json").read_text(encoding="utf-8"))
    records = {(r["file_path"], r["id"]): r for r in plan["prepared_records"]}
    cases, pictures, contexts, failures, native_copies = [], [], [], [], []
    for i, name in enumerate(("rafael", "hodram", "lil", "maria")):
        path = f"/data/SC{i}.DK4"
        rompath = Path(manifest["Maria_test_ROM"] if name == "maria" else manifest["base_research_ROM"])
        arm = NdsImage.open(rompath).read_file("/__arm9__.bin")
        capture = json.loads(Path(f"work/emulation_v193/name_editorial_v280_{name}/capture_report.json").read_text(encoding="utf-8"))
        assert capture["ROM_sha256"] == sha(rompath.read_bytes())
        assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
        snapshot = capture["read_only_RAM_snapshot"]
        ram = Path(snapshot["path"]).read_bytes()
        assert snapshot["read_only_export"] and len(ram) == 4194304 and sha(ram) == snapshot["sha256"]
        cpu = initialized(arm)
        cpu.mem_write(0x02000000, ram)
        pool = bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48])
        assert bytes(cpu.mem_read(POOL, len(pool))) == pool
        defaults = {k: expand(cpu, k.encode("ascii")) for k in ("FI", "FA", "FO", "FU")}
        contexts.append({"route": path, "actual_RAM_snapshot": snapshot, "actual_macro_defaults": {k: v.decode("cp932") for k, v in defaults.items()}})
        for key_row in plan["records"]:
            if not any(request["owner"][0] == path for request in key_row["requests"]):
                continue
            key, target = bytes.fromhex(key_row["key_hex"]), bytes.fromhex(key_row["target_hex"])
            expected = target
            for macro, value in defaults.items():
                expected = expected.replace(macro.encode("ascii"), value)
            for alignment in range(4):
                for caller in plan["scoped_call_sites"]:
                    source, destination = 0x02430020 + alignment, 0x02431020
                    cpu.mem_write(0x02430000, b"\xA5" * 640)
                    cpu.mem_write(source, key + b"\0")
                    guard = bytes(cpu.mem_read(0x02430000, 640))
                    cpu.mem_write(destination - 32, b"\xA5" * 576)
                    for reg, value in [(UC_ARM_REG_R0, destination), (UC_ARM_REG_R1, source),
                                       (UC_ARM_REG_R2, 0), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, caller + 4)]:
                        cpu.reg_write(reg, value)

                    try:
                        # Stop at the real return address. Adding a new code hook
                        # after warming macro getters can miss cached blocks.
                        cpu.emu_start(plan["entry"], caller + 4, count=200000)
                    except Exception:
                        print("FAILED", path, key_row["requests"], "target", repr(target),
                              "PC", hex(cpu.reg_read(UC_ARM_REG_PC)),
                              "R0/R1/R2", [hex(cpu.reg_read(r)) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)],
                              "completed", len(native_copies), "alignment/caller", alignment, hex(caller), flush=True)
                        raise
                    assert cpu.reg_read(UC_ARM_REG_PC) == caller + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
                    assert bytes(cpu.mem_read(0x02430000, 640)) == guard
                    assert bytes(cpu.mem_read(destination - 32, 576)) == b"\xA5" * 32 + expected + b"\0" + b"\xA5" * (543 - len(expected))
                    native_copies.append({"route": path, "key_hex": key_row["key_hex"], "alignment": alignment,
                                          "caller": caller, "complete_expanded_output_hex": expected.hex(), "getter_bridges": []})
        for owner, record in records.items():
            if owner[0] != path:
                continue
            target = bytes.fromhex(record["target_hex"])
            tokens = parse_markup(record["formatted_markup"])
            if tokens and tokens[0].kind == "speaker":
                target = target[1:]
            expected = target
            for macro, value in defaults.items():
                expected = expected.replace(macro.encode("ascii"), value)
            try:
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
                image = Image.new("RGB", (WIDTH, HEIGHT))
                colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
                image.putdata([colors[c] for c in pixels])
                pictures.append((path + " " + record["id"], image.resize((WIDTH * 2, HEIGHT * 2), Image.Resampling.NEAREST)))
                cases.append({"file_path": path, "id": record["id"], "expanded_body_hex": output.hex(),
                              "actual_route_macros_no_getter_bridges": True,
                              "all_native_glyph_pixels_cells_first_final_letters_and_bounds_exact": True})
            except (ValueError, AssertionError) as error:
                failures.append({"file_path": path, "id": record["id"], "error": str(error)})
        assert bytes(cpu.mem_read(POOL, len(pool))) == pool
    sheets = []
    for start in range(0, len(pictures), 8):
        sheet = Image.new("RGB", (WIDTH * 4, 4 * (HEIGHT * 2 + 26)), "#333333")
        draw = ImageDraw.Draw(sheet)
        for n, (label, image) in enumerate(pictures[start:start + 8]):
            x, y = n % 2 * WIDTH * 2, n // 2 * (HEIGHT * 2 + 26)
            draw.text((x + 3, y + 4), label, fill="white")
            sheet.paste(image, (x, y + 26))
        out = ROOT / f"catalog_review_{start // 8:02d}.png"
        sheet.save(out)
        sheets.append(str(out))
    proof = {"format": "dk4-catalog-real-route-expansion-glyphs-v280",
             "current_catalog_ARM9_sha256": plan["target_arm9_sha256"], "contexts": contexts,
             "native_scoped_catalog_copy_cases": native_copies,
             "cases": cases, "failures": failures, "sheets": sheets,
             "all83_bodies_actual_route_expansion_and_complete_glyphs_verified": len(cases) == 83,
             "lookup_all145_keys_verified_separately": True,
             "scope": "Actual per-route player state and controlled native text painting; original deep scene behavior and full integration remain unproved.",
             "not_for_normal_gameplay_or_handoff": True, "full_goal_complete": False}
    (ROOT / "catalog_native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"catalog_bodies": len(cases), "native_catalog_copies": len(native_copies), "failures": len(failures), "sheets": len(sheets)}), flush=True)
    if failures:
        print(json.dumps(failures[:8]), flush=True)


if __name__ == "__main__":
    main()
