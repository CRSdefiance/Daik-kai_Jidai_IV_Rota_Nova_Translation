"""Five occupied slots, short hints, heading, preservation and exact patch."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.equipment_source_grain import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.native_inventory_fixture_v481 import transfer
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_equipment_long_names_v536 import CASES
from scripts.verify_occupied_weapon_v477 import item_state
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path("out/all_routes_combined_v543_candidate.nds")
ROOT = Path("work/analysis/equipment_texture_v543")
CAPTURES = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def report(folder, digest):
    result = read(folder / "capture_report.json")
    assert result["ROM_sha256"] == digest and result["cold_boot"]
    assert not result["savestate_loaded"] and not result["callback_errors"]
    for row in result["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    return result


def hint(font, donor, shot, text, slot):
    width = len(text) * 6 + 4
    left = min(slot, 224 - width)
    ink, bounds = complete_mask(font, text, shot, left + 2, 210, (0, 8, 0))
    expected_ink = {(left + 2 + n * 6 + x, 210 + y) for n, c in enumerate(text)
                    for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    old_tile = Path("work/analysis/direct_equipment_v270/paper_tile.bin").read_bytes()
    for y in range(16):
        for x in range(width):
            point = left + x, 208 + y
            dx = x if x < 2 else 42 + x - (width - 2) if x >= width - 2 else 2 + (x - 2) % 40
            if point in expected_ink:
                color = (0, 1, 0)
            elif 2 <= y < 14 and 2 <= x < width - 2:
                color = native5(donor.palette[donor.indices[(60 + y) * donor.width + dx]])
            else:
                value = struct.unpack_from("<H", old_tile, (y * 44 + dx) * 2)[0]
                color = (value & 31, (value >> 5) & 31, (value >> 10) & 31)
            assert native5(shot.getpixel(point)) == color, (text, point, color)
    return {"english": text, "width": width, "bounds": [left, 208, left + width, 224],
            "complete_ink_pixels": ink, "font_bounds": bounds,
            "all_source_grain_retained_bevel_and_complete_letters_exact": True}


def main():
    parent = NdsImage.open("out/all_routes_combined_v542_candidate.nds")
    current = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix(".manifest.json"))
    old_manifest = read("out/all_routes_combined_v542_candidate.manifest.json")
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v543"
    assert manifest["batches"] == old_manifest["batches"] and len(manifest["batches"]) == 470
    stack = read("translations/release_stack.json")
    assert len(stack["accepted_layers"]) == 114
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys() and [p for p in old if old[p] != new[p]] == ["/__arm9__.bin"]
    expected, plan = apply_release(old["/__arm9__.bin"], NdsImage.open("work/clean.nds"),
                                   "translations/equipment_source_grain_v1.json")
    arm = new["/__arm9__.bin"]
    assert arm == expected
    native = read(ROOT / "native_painter_proof.json")
    assert native["plan"]["target_arm9_sha256"] == sha(arm)
    assert len(native["complete_native_painter_cases"]) == 470
    run = report(CAPTURES / "equipment_texture_v543_slots", digest)
    assert len(run["synthetic_inventory_fixtures"]) == 1
    before = (CAPTURES / "equipment_texture_v543_slots/frame_003000_arm9_ram.bin").read_bytes()
    _, replay = transfer(arm, before, [40, 71, 92, 98, 126])
    assert run["synthetic_inventory_fixtures"][0] == dict(replay, frame=3000)
    copy = read(ROOT / "save_copy_manifest.json")
    assert sha(Path(copy["source"]).read_bytes()) == copy["source_sha256"]
    assert sha(Path(copy["test_copy"]).read_bytes()) == copy["test_copy_sha256"]
    frames = {row["frame"]: row for row in run["frames_captured"]}
    font = GameAsciiFont.from_arm9(arm)
    donor = PxlImage.from_bytes(NdsImage.open("work/clean.nds").read_file("/_pxl/towninfo.pxl"))
    icons = PxlImage.from_bytes(new["/_pxl/item.pxl"]).render().convert("RGB")
    plaque_batch = read("translations/person_info_graphics_v3.json")
    plaques_asset = PxlImage.from_bytes(new[plaque_batch["file_path"]])
    plaque_cases = []
    cases = []
    for item, text, frame, slot in CASES:
        shot = Image.open(frames[frame]["path"]).convert("RGB")
        exact = hint(font, donor, shot, text, slot)
        assert [native5(c) for c in shot.crop((slot, 224, slot + 32, 256)).get_flattened_data()] == [
            native5(c) for c in icons.crop((0, item * 32, 32, (item + 1) * 32)).get_flattened_data()]
        state = item_state(arm, CAPTURES / f"equipment_texture_v543_slots/frame_{frame:06d}_arm9_ram.bin", item)
        assert state["name"] == text and state["owner_descriptor_type"] == 2
        assert state["owner_index_or_city_if_type2_or4"] == 3
        for row in plaque_batch["records"]:
            l, t, r, b = row["plaque_box"]
            assert all(native5(shot.getpixel((x, y))) == native5(
                plaques_asset.palette[plaques_asset.indices[y * plaques_asset.width + x]])
                for y in range(t, b) for x in range(l, r))
            plaque_cases.append({"frame": frame, "id": row["id"],
                                 "complete_V542_plaque_pixels_exact": (r - l) * (b - t)})
        cases.append({"item_id": item, "frame": frame, "display": exact,
                      "owner": state, "full_icon_pixels_exact": 1024, "capture": frames[frame]["path"]})
    empty = []
    for text, frame, slot in [("Weapon", 6200, 16), ("Armor", 7000, 64), ("Equipped Items", 12000, 208)]:
        shot = Image.open(frames[frame]["path"]).convert("RGB")
        empty.append({"frame": frame, "display": hint(font, donor, shot, text, slot),
                      "capture": frames[frame]["path"]})
    fresh = report(CAPTURES / "equipment_texture_v543_fresh", digest)
    previous = report(CAPTURES / "plaque_texture_v542_fresh", sha(parent.source.read_bytes()))
    assert fresh["scripted_input_schedule"] == previous["scripted_input_schedule"]
    assert fresh["core_options"] == previous["core_options"]
    frame_sets = [{r["frame"]: r["PNG_sha256"] for r in rep["frames_captured"]}
                  for rep in (fresh, previous)]
    assert frame_sets[0] == frame_sets[1] and len(frame_sets[0]) == 56
    preservation = read("work/analysis/plaque_texture_v542/preservation_proof.json")
    assert len(preservation["entries"]) == 921
    assert all(old[row["path"]] == new[row["path"]] for row in preservation["entries"])
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        parent_proof="work/analysis/plaque_texture_v542/preservation_proof.json")
    (ROOT / "preservation_proof.json").write_text(json.dumps(preservation, indent=2) + "\n", encoding="utf-8")
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(Path("work/clean.nds"), ROM, patch)
    reconstruction = ROOT / "reconstructed.nds"
    apply_xdelta(Path("work/clean.nds"), patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    plaques = read("translations/graphics_completion_campaign_v1.json")["plaque_style_v247"]["ongoing_plaque_inventory"]
    assert len(plaques) == 18 and all(not p["fully_completed"] for p in plaques)
    assert len(read("translations/graphics_completion_requirements_v313.json")["historical_pending_items_retained"]) == 22
    proof = {"candidate": str(ROM), "candidate_sha256": digest, "profile": manifest["profile"],
             "base": manifest["base_rom"], "base_sha256": manifest["base_sha256"],
             "patch_sha256": sha(patch.read_bytes()), "exact_clean_patch_reconstruction": True,
             "native_painter_width_cases": 470, "nine_invalid_contracts_no_new_writes": True,
             "five_occupied_slot_native_cases": cases, "short_hints_and_heading": empty,
             "all50_native_Sailor_Info_plaque_crops_preserved": plaque_cases,
             "all5120_icon_pixels_preserved": True, "all56_regression_frames_exact_V542": True,
             "only_existing_tile_interior_and_three_dispatch_instructions_changed": plan,
             "all_470_batches114_layers_and921_graphics_entries_retained": True,
             "source_and_test_copy_saves_unchanged": True,
             "synthetic_inventory_fixture_normal_acquisition_not_claimed": True,
             "all18_audit_entries_remain_incomplete": True,
             "experimental": True, "canonical_promoted": False, "full_goal_complete": False,
             "remaining": "Original bevel comparison, other plaques and contexts, embedded/legacy graphics remain open."}
    (ROOT / "release_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("V543: five occupied slots, three short/heading hints, 470 native widths, 56 regression frames and exact patch pass.")


if __name__ == "__main__":
    main()
