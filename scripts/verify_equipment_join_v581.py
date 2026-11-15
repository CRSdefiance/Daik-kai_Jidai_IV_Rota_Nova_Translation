"""Original wood mapping, widest native equipment labels and release continuity."""

import argparse
import json
import shutil
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.equipment_grain_join import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.native_inventory_fixture_v481 import transfer
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_equipment_long_names_v536 import CASES
from scripts.verify_occupied_weapon_v477 import item_state
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/equipment_material_v580")
ROM = Path("out/all_routes_combined_v581_candidate.nds")
PARENT = Path("out/all_routes_combined_v573_candidate.nds")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
OLD = CAPTURE / "equipment_material_v580_current"
NEW = CAPTURE / "equipment_join_v581_slots"
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V581 Equipment wood joins")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def report(folder, digest):
    r = read(folder / "capture_report.json")
    assert r["ROM_sha256"] == digest and r["cold_boot"] and not r["savestate_loaded"]
    assert not r["callback_errors"]
    for row in r["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots"):
        for row in r.get(key, []):
            assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
    return r, {row["frame"]: row for row in r["frames_captured"]}


def source_tile(donor, shifted):
    """Independent original donor coordinates; no generated-tile expectation."""
    tile = bytearray()
    for y in range(16):
        for x in range(44):
            if 2 <= x < 42 and 2 <= y < 14:
                sx, sy = x + int(shifted), 60 + y
            else:
                sx = 8 + x if x < 2 else 46 + x - 42 if x >= 42 else 10 + (x - 2) % 36
                sy = 20 + y
            r, g, b = native5(donor.palette[donor.indices[sy * donor.width + sx]])
            tile.extend(struct.pack("<H", 0x8000 | r | g << 5 | b << 10))
    return bytes(tile)


def hint(font, tile, image, name, slot):
    width = len(name) * 6 + 4
    left = min(slot, 224 - width)
    ink, bounds = complete_mask(font, name, image, left + 2, 210, (0, 8, 0))
    points = {(left + 2 + n * 6 + x, 210 + y) for n, c in enumerate(name)
              for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    visible_joins = 0
    for y in range(16):
        for x in range(width):
            dx = x if x < 2 else 42 + x - width + 2 if x >= width - 2 else 2 + (x - 2) % 40
            value = struct.unpack_from("<H", tile, (y * 44 + dx) * 2)[0]
            point = left + x, 208 + y
            expected = (0, 1, 0) if point in points else (value & 31, value >> 5 & 31, value >> 10 & 31)
            assert native5(image.getpixel(point)) == expected, (name, point, expected)
            if point not in points and 2 <= y < 14 and x in (41, 42, 81, 82, 121, 122):
                visible_joins += 1
    return {"name": name, "bounds": [left, 208, left + width, 224], "font_bounds": bounds,
            "complete_font_ink": ink, "whole_paper_pixels": width * 16,
            "visible_repeat_boundary_points": visible_joins}


def main():
    old, new, clean = NdsImage.open(PARENT), NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    manifest, parent_manifest = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    stack = read("translations/release_stack.json")
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v581"
    assert manifest["base_sha256"] == parent_manifest["base_sha256"] == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert manifest["batches"] == parent_manifest["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == parent_manifest["required_batches"] and len(stack["accepted_layers"]) == 114
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    before = {p: d for _, p, d in old.iter_files()} | dict(old.iter_components())
    after = {p: d for _, p, d in new.iter_files()} | dict(new.iter_components())
    assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == ["/__arm9__.bin"]
    arm = after["/__arm9__.bin"]
    expected, stage = apply_release(before["/__arm9__.bin"], clean, "translations/equipment_grain_join_v1.json")
    assert arm == expected
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    tiles = [source_tile(donor, shifted) for shifted in (False, True)]
    plan = read("work/analysis/direct_equipment_v270/runtime_plan.json")
    at = plan["tile_pointer"] - POOL
    for version, tile in zip((before["/__arm9__.bin"], arm), tiles, strict=True):
        assert bytes(MainCodeFile(version, BASE).sections[3].data[at:at + 1408]) == tile
    painter = read(ROOT / "v581_native_width_proof.json")
    assert painter["arm9_sha256"] == sha(arm) and painter["tile_sha256"] == sha(tiles[1])
    assert painter["probe_script_sha256"] == sha(Path("scripts/verify_source_plaque_bevels_v546.py").read_bytes())
    assert [(r["screen"], r["width"]) for r in painter["cases"]] == [
        (screen, width) for screen in (0, 1) for width in range(10, 245)]
    assert painter["invalid_contracts"] == 9
    assert all(r["all_bytes_bounds_and_saved_register_stack_ABI_exact"] for r in painter["cases"])
    runs = [report(folder, sha(path.read_bytes())) for folder, path in ((OLD, PARENT), (NEW, ROM))]
    assert runs[0][0]["scripted_input_schedule"] == runs[1][0]["scripted_input_schedule"]
    assert runs[0][0]["core_options"] == runs[1][0]["core_options"]
    fixture_proofs = []
    for folder, version, (run, _) in zip((OLD, NEW), (before["/__arm9__.bin"], arm), runs, strict=True):
        ram = (folder / "frame_003000_arm9_ram.bin").read_bytes()
        _, replay = transfer(version, ram, [c[0] for c in CASES])
        assert run["synthetic_inventory_fixtures"] == [dict(replay, frame=3000)]
        assert len(replay["changes"]) == 11 and not run["normal_acquisition_verified"]
        fixture_proofs.append(replay)
    assert {k: v for k, v in fixture_proofs[0].items() if k not in ("before_RAM_sha256", "after_RAM_sha256")} == {
        k: v for k, v in fixture_proofs[1].items() if k not in ("before_RAM_sha256", "after_RAM_sha256")}
    copies = read(ROOT / "save_copy_provenance.json")
    for key in ("original", "historical_test_source", "new_test_copy"):
        assert sha(Path(copies[key]).read_bytes()) == copies[key + "_sha256"]
    font = GameAsciiFont.from_arm9(arm)
    atlas = PxlImage.from_bytes(after["/_pxl/item.pxl"]).render().convert("RGB")
    equipment = []
    u = machine(arm)
    u.mem_write(BASE, (NEW / "frame_003000_arm9_ram.bin").read_bytes())
    call(u, 0xCB190, ())
    store = u.reg_read(UC_ARM_REG_R0)
    catalog = {2: [], 3: [], 4: []}
    for index in range(218):
        item = store + 4 + index * 20
        call(u, 0x4A448, (item,))
        category = u.reg_read(UC_ARM_REG_R0)
        if category not in catalog:
            continue
        call(u, 0x4A53C, (item,))
        name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b"\0")[0].decode("cp932")
        catalog[category].append({"id": index, "name": name, "width": len(name) * 6 + 4})
    assert [len(catalog[n]) for n in (2, 3, 4)] == [28, 26, 49]
    assert {str(k): v for k, v in catalog.items()} == read(ROOT / "current_equipment_name_widths.json")
    sheet = Image.new("RGB", (1800, 740), "#293239")
    draw = ImageDraw.Draw(sheet)
    draw.text((15, 8), "V573 original repeat (left) / V581 original strip shifted one pixel inward (right)", fill="white")
    archive_rows = []
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for n, (item, name, frame, slot) in enumerate(CASES):
        images = [Image.open(table[frame]["path"]).convert("RGB") for _, table in runs]
        cases = [hint(font, tile, image, name, slot) for tile, image in zip(tiles, images, strict=True)]
        state = item_state(arm, NEW / f"frame_{frame:06d}_arm9_ram.bin", item)
        assert state["name"] == name and state["owner_descriptor_type"] == 2
        assert state["owner_index_or_city_if_type2_or4"] == 3
        assert len(name) * 6 + 4 == max(r["width"] for r in catalog[state["category"]])
        a, b = images
        l, t, r, bottom = cases[1]["bounds"]
        outside = 0
        for y in range(384):
            for x in range(256):
                if not (l + 2 <= x < r - 2 and t + 2 <= y < bottom - 2):
                    assert a.getpixel((x, y)) == b.getpixel((x, y)), (frame, x, y)
                    outside += 1
        assert [native5(c) for c in b.crop((slot, 224, slot + 32, 256)).get_flattened_data()] == [
            native5(c) for c in atlas.crop((0, item * 32, 32, (item + 1) * 32)).get_flattened_data()]
        draw.text((15, n * 140 + 28), name, fill="white")
        for column, image in enumerate(images):
            sheet.paste(image.crop((l, t, r, bottom)).resize(((r - l) * 6, 96), Image.Resampling.NEAREST),
                        (15 + column * 900, n * 140 + 48))
            dest = ARCHIVE / f"{'V573' if column == 0 else 'V581'}_{item}_{frame}.png"
            shutil.copyfile(runs[column][1][frame]["path"], dest)
            archive_rows.append({"path": str(dest), "sha256": sha(dest.read_bytes()), "synthetic_inventory_fixture": True})
        equipment.append({"item": item, "frame": frame, "native_owner": state,
                          "maximum_width_in_category": True, "old": cases[0], "new": cases[1],
                          "all_outside_texture_interior_pixels_exact": outside, "original_icon_pixels_exact": 1024})
    sheet.save(ROOT / "native_before_after_6x.png")
    shutil.copyfile(ROOT / "native_before_after_6x.png", ARCHIVE / "native_before_after_6x.png")
    empty = []
    for name, frame, slot in (("Weapon", 6200, 16), ("Armor", 7000, 64), ("Equipped Items", 12000, 208)):
        image = Image.open(runs[1][1][frame]["path"]).convert("RGB")
        empty.append(hint(font, tiles[1], image, name, slot))
    fresh, fresh_frames = report(CAPTURE / "equipment_join_v581_fresh", digest)
    previous, previous_frames = report(CAPTURE / "confirm_material_v573_fresh", sha(PARENT.read_bytes()))
    assert fresh["scripted_input_schedule"] == previous["scripted_input_schedule"]
    assert fresh["core_options"] == previous["core_options"]
    assert {f: row["PNG_sha256"] for f, row in fresh_frames.items()} == {
        f: row["PNG_sha256"] for f, row in previous_frames.items()}
    assert len(fresh_frames) == 56
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(Path("work/clean.nds"), ROM, patch)
    reconstructed = ROOT / "v581_reconstructed.nds"
    apply_xdelta(Path("work/clean.nds"), patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    snapshots = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, snapshot in snapshots.items():
        audit = read(Path("translations") / filename)
        assert audit.get("historical_pending_items_retained") == snapshot["historical_pending_items_retained"]
        assert audit.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == snapshot["ongoing_plaque_inventory"]
    result = {"candidate": str(ROM), "candidate_sha256": digest, "profile": manifest["profile"],
              "base_sha256": manifest["base_sha256"], "patch_sha256": sha(patch.read_bytes()),
              "exact_patch_reconstruction": True, "all470_batches114_layers_retained": True,
              "only_changed_file_from_V573": "/__arm9__.bin", "source_transform": stage,
              "all921_graphics_and57_embedded_blocks_exact_V573": True,
              "all_code_frame_palette_and_section_geometry_unchanged": True,
              "source_donor_is_original_wood_not_hidden_pixel_recovery": True,
              "all103_equipment_names_native_catalog": catalog, "native_painter_cases": len(painter["cases"]),
              "native_invalid_contract_checks": 9, "five_longest_native_cases": equipment,
              "three_empty_hints": empty, "unchanged_startup_frames": 56,
              "original_and_test_saves_unchanged": copies,
              "inventory_fixture_replay": fixture_proofs[1], "ordinary_acquisition_not_claimed": True,
              "all18_plaques_remain_incomplete_and22_historical_objects_exact": True,
              "experimental": True, "canonical_promoted": False, "full_goal_complete": False,
              "archive": str(ARCHIVE), "screenshots": archive_rows}
    proof = ROOT / "v581_release_proof.json"
    proof.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for folder, name in ((OLD, "V573"), (NEW, "V581")):
        shutil.copyfile(folder / "capture_report.json", ARCHIVE / f"{name}_capture_report.json")
    shutil.copyfile(proof, ARCHIVE / proof.name)
    print("V581: five category-maximum labels, three empty hints, 470 widths, original wood, 56 startup frames and exact patch pass.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-widths", action="store_true")
    if parser.parse_args().probe_widths:
        from scripts.verify_source_plaque_bevels_v546 import renderer_cases

        arm = NdsImage.open(ROM).read_file("/__arm9__.bin")
        plan = read("work/analysis/direct_equipment_v270/runtime_plan.json")
        pool = MainCodeFile(arm, BASE).sections[3].data
        at = plan["tile_pointer"] - POOL
        tile = bytes(pool[at:at + 1408])
        result = {"cases": renderer_cases(arm, tile, plan), "invalid_contracts": 9,
                  "arm9_sha256": sha(arm), "tile_sha256": sha(tile),
                  "probe_script_sha256": sha(Path("scripts/verify_source_plaque_bevels_v546.py").read_bytes())}
        (ROOT / "v581_native_width_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        main()
