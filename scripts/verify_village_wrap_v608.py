"""Verify integrated village wrapping, real scene pixels and ordinary regressions."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_portrait_wrap import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.run_village_wrap_v608 import relocate
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path("work/analysis/village_wrap_v608")
CAP = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ROM = Path("out/all_routes_combined_v608_candidate.nds")
PARENT = Path("out/all_routes_combined_v604_candidate.nds")
DIGEST = "1bf4f00b6117d6a9a16daca8a8d3a4a8e1dc5e9f24aeac984023db8d1c73ab7f"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def report(name, frames, digest):
    path = CAP / name / "capture_report.json"
    d = read(path)
    assert d["ROM_sha256"] == digest and d["frames"] == frames
    assert d["cold_boot"] and not d["savestate_loaded"] and not d["callback_errors"]
    shots = {}
    for row in d["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        shots[row["frame"]] = row
    return d, shots, {"path": str(path), "sha256": sha(path.read_bytes())}


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    old_rom, rom = NdsImage.open(PARENT), NdsImage.open(ROM)
    before = {p: data for _, p, data in old_rom.iter_files()} | dict(old_rom.iter_components())
    after = {p: data for _, p, data in rom.iter_files()} | dict(rom.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ["/__arm9__.bin"]
    arm = after["/__arm9__.bin"]
    expected, transform = apply_release(before["/__arm9__.bin"], "translations/village_portrait_wrap_v1.json")
    assert expected == arm
    assert len(transform["compiled_contexts"]) == 28 and len(transform["changed_records"]) == 11
    manifest, previous = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    registry = read("translations/release_stack.json")
    assert manifest["profile"] == "all-routes-unified-v608" and manifest["candidate_sha256"] == DIGEST
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["base_sha256"] == registry["canonical_baseline"]["sha256"]
    assert sha(Path(manifest["base_rom"]).read_bytes()) == manifest["base_sha256"]
    assert manifest["batches"] == previous["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == previous["required_batches"] and len(registry["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    assert manifest["relocations"]["/__arm9__.bin"]["village_portrait_wrap"]["target_arm9_sha256"] == sha(arm)
    assert sha((ROOT / "patch_reconstructed.nds").read_bytes()) == DIGEST
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == "ef97e56eedd0370bf48d6bd83072791451d7082ca13c97baaa80be55719e8e91"
    preservation = read(ROOT / "preservation_proof.json")
    assert preservation["candidate_sha256"] == DIGEST and preservation["current921_format_palette_extent_checks"]
    assert preservation["all57_embedded_block_extents_exact"]
    native = read(ROOT / "actual_canvas_proof.json")
    assert native["script_sha256"] == sha(Path("scripts/probe_village_canvas_v608.py").read_bytes())
    assert native["research_ARM9_sha256"] == sha(arm)
    assert len(native["all28_contexts"]) == 28 and native["whole_replayed_canvas_bytes"] == 193536
    assert native["actual_scene_binding"]["whole_captured_VRAM_plane_bytes_exact"] == 6912
    village, shots, binding = report("village_wrap_v608_inuvik", 8600, DIGEST)
    donor = village["battery_save_preloaded"]
    assert donor["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
    assert sha(Path(donor["source"]).read_bytes()) == donor["source_sha256"]
    raw = (CAP / "village_wrap_v608_inuvik/frame_005200_arm9_ram.bin").read_bytes()
    _, replay = relocate(arm, raw, 0)
    assert village["synthetic_location_fixtures"] == [dict(replay, frame=5200)]
    for key, value in village.items():
        if key.startswith("synthetic_") and key != "synthetic_location_fixtures":
            assert not value
    font = GameAsciiFont.from_arm9(arm)
    image = Image.open(shots[7800]["path"]).convert("RGB")
    masks = []
    wanted = set()
    for text, x, y in (("Captain, the village chief asks to", 22, 296),
                       ("hear the promised words.", 22, 312)):
        count, bounds = complete_mask(font, text, image, x, y, (0, 8, 0))
        masks.append({"text": text, "bounds": bounds, "complete_native_ink_pixels": count})
        for n, char in enumerate(text):
            glyph = font.decode(char)
            wanted |= {(x + n * 6 + xx, y + yy) for yy in range(11) for xx in range(6)
                       if glyph.getpixel((xx, yy))}
    # Complete old-width region includes both blank tails and the now-empty third row.
    for y in range(296, 344):
        for x in range(16, 240):
            assert (image.getpixel((x, y)) == (0, 8, 0)) == ((x, y) in wanted)
    old, old_shots, old_binding = report("village_water_v607_inuvik", 17800, sha(PARENT.read_bytes()))
    assert old["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    unchanged_village = []
    for frame in (5600, 6000, 6400, 6900, 8200, 8600):
        a, b = [Image.open(rows[frame]["path"]).convert("RGB") for rows in (shots, old_shots)]
        assert a.tobytes() == b.tobytes()
        unchanged_village.append(frame)
    old_image = Image.open(old_shots[7800]["path"]).convert("RGB")
    assert old_image.crop((0, 0, 256, 288)).tobytes() == image.crop((0, 0, 256, 288)).tobytes()
    # First verify the actual former split, rather than trusting an issue label.
    complete_mask(font, "Captain, the village chief asks to h", old_image, 16, 296, (0, 8, 0))
    complete_mask(font, "ear", old_image, 16, 312, (0, 8, 0))
    complete_mask(font, "the promised words.", old_image, 22, 328, (0, 8, 0))
    market, market_shots, market_binding = report("village_wrap_v608_market", 24100, DIGEST)
    old_market, previous_shots, previous_binding = report("race_controls_v604_market_candidate", 24100, sha(PARENT.read_bytes()))
    for d in (market, old_market):
        assert not d.get("battery_save_preloaded")
        assert not any(value for key, value in d.items() if key.startswith("synthetic_"))
    assert market["scripted_input_schedule"] == old_market["scripted_input_schedule"]
    assert set(market_shots) == set(previous_shots) and len(market_shots) == 19
    for frame in market_shots:
        assert Image.open(market_shots[frame]["path"]).tobytes() == Image.open(previous_shots[frame]["path"]).tobytes()
    save(ROOT / "release_proof.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
        "script_sha256": sha(Path(__file__).read_bytes()), "parent": str(PARENT), "parent_sha256": sha(PARENT.read_bytes()),
        "canonical_base": manifest["base_rom"], "canonical_base_sha256": manifest["base_sha256"],
        "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()), "exact_clean_ROM_patch_reconstruction": True,
        "complete_470_batches_114_accepted_layers": True, "only_ARM9_changed_all_art_scripts_components_preserved": True,
        "transform": transform, "native_canvas_proof": str(ROOT / "actual_canvas_proof.json"),
        "native_canvas_proof_sha256": sha((ROOT / "actual_canvas_proof.json").read_bytes()),
        "actual_complete_request_masks": masks, "entire_224x48_foreground_region_checked": True,
        "request_words_complete_both_rows_left_aligned": True, "third_row_and_old_tails_blank": True,
        "original_bad_split_independently_reproduced": True, "six_other_village_frames_whole_exact": unchanged_village,
        "ordinary_market_regression_frames": 24100, "ordinary_regression_whole_frame_matches": sorted(market_shots),
        "reports": {"village": binding, "former_village": old_binding, "market": market_binding, "former_market": previous_binding},
        "village_is_authorized_coordinate_fixture_not_normal_travel": True,
        "all28_paragraphs_GPU_event_screens_or_successful_password_not_claimed": True,
        "Japanese_village_menu_and_name_still_open": True, "all8_village_card_contexts_still_open": True,
        "all18_plaques_incomplete_all22_historical_requirements_retained": True,
        "human_accepted": False, "full_goal_complete": False})
    print("V608: complete native request;28 real-canvas replays;19 ordinary whole-frame matches;registered full stack and exact patch pass.")


if __name__ == "__main__":
    main()
