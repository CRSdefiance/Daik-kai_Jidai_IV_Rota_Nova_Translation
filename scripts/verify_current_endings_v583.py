"""Current original Hodram/Lil/Maria ending playback and source-bound effects."""

import json
import shutil
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.search_ending_effect_v583 import matches, source_points
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_ending_credits_v578 import quantized, verify_captures, verify_split_pans

ROOT = Path("work/analysis/endings_current_v583")
ROM = Path("out/all_routes_combined_v581_candidate.nds")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V583 Current endings")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    provenance = read(ROOT / "fixture_provenance.json")
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    assert digest == provenance["candidate_sha256"]
    arm = rom.read_file("/__arm9__.bin")
    assert sha(arm) == provenance["ARM9_sha256"]
    for donor in provenance["original_donors"]:
        assert sha(Path(donor["path"]).read_bytes()) == donor["sha256"]
    for row in provenance["original_code_ranges"]:
        lo, hi = row["offset"]
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
        assert sha(arm[lo:hi]) == row["sha256"]
    for path, expected in provenance["original_ending_movies"].items():
        assert rom.read_file(path) == clean.read_file(path) and sha(rom.read_file(path)) == expected
    fls_code_ranges = []
    for lo, hi in ((0xFD4F8, 0xFDC60), (0xFEB28, 0xFEFCC), (0x100390, 0x1003CC), (0xDFA88, 0xDFD00)):
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
        fls_code_ranges.append({"offset": [lo, hi], "sha256": sha(arm[lo:hi]), "exact_clean": True})
    previous = read("work/analysis/ending_native_v578/native_ending_credit_proof.json")
    historical = {c["captain_id"]: c for c in previous["historical_V534_credit_planes"]}
    current, tables, runs, comparisons = {}, {}, {}, []
    for config in provenance["cases"]:
        captain, label = config["captain"], config["label"]
        folder = CAPTURE / f"endings_current_v583_{label}"
        run = read(folder / "capture_report.json")
        assert run["frames"] == config["frames"] and run["scripted_input_schedule"] == read(config["inputs"])
        for snapshot in run.get("read_only_capture_RAM_snapshots", []) + run.get("read_only_pause_RAM_snapshots", []):
            assert sha(Path(snapshot["path"]).read_bytes()) == snapshot["sha256"]
        if config["capture_window"]:
            first, last = config["capture_window"]
            recorded = {r["frame"] for r in run["frames_captured"]}
            assert set(range(first, last + 1)) <= recorded
        for key in ("source_save", "test_save"):
            if key in config:
                assert sha(Path(config[key]).read_bytes()) == config[key + "_sha256"]
        index = {1: 10, 2: 8, 3: 6}[captain]
        case, table = verify_captures(folder, ROM, captain, index)
        current[captain], tables[captain], runs[captain] = case, table, run
        old_report_path = Path(config["historical_report"])
        assert sha(old_report_path.read_bytes()) == config["historical_report_sha256"]
        old_table = {r["frame"]: r for r in read(old_report_path)["frames_captured"]}
        baseline = historical[captain]
        frame_bounds = [r["frame"] for r in baseline["full_scene_cases"] + baseline["credit_cases"]]
        if captain in (1, 2):
            pan = next(p for p in previous["historical_split_pan_compositions"] if p["captain_id"] == captain)
            frame_bounds += [r["frame"] for r in pan["exact_full_upper_frame_composites"]]
        selected = sorted(f for f in table.keys() & old_table.keys() if min(frame_bounds) <= f <= max(frame_bounds))
        assert selected
        for frame in selected:
            assert sha(Path(old_table[frame]["path"]).read_bytes()) == old_table[frame]["PNG_sha256"]
            assert quantized(table[frame]["path"]).crop((0, 0, 256, 192)).tobytes() == quantized(
                old_table[frame]["path"]).crop((0, 0, 256, 192)).tobytes(), (label, frame)
        prompt_frame = {1: 20280, 2: 26280, 3: 11280}[captain]
        prompt_image = Image.open(table[prompt_frame]["path"]).convert("RGB")
        ink, bounds = complete_mask(GameAsciiFont.from_arm9(arm), "Save the ending data?", prompt_image,
                                    16, 296, (0, 8, 0))
        comparisons.append({"captain": captain, "historical_movie_frame_range": [min(frame_bounds), max(frame_bounds)],
                            "whole_upper_current_historical_frames_exact": selected,
                            "complete_ending_save_prompt": {"frame": prompt_frame, "ink": ink, "bounds": bounds}})
        # Keep negative fixture guards current; no permissive version bypass.
        raw = (folder / f"frame_{config['pause_at']:06d}_arm9_ram.bin").read_bytes()
        for wrong_arm, wrong_captain in ((arm, (captain + 1) % 4), (arm + b"\0", captain)):
            try:
                request_ending(wrong_arm, raw, wrong_captain)
            except ValueError:
                pass
            else:
                raise AssertionError("Ending fixture accepted a wrong captain/version")
    pans = verify_split_pans(rom, current, tables)
    for pan in pans:
        pan["current_report"] = pan.pop("historical_report")
        del pan["fresh_current_playback_not_claimed"]
        pan["fresh_current_playback_verified"] = True
    effect = read(ROOT / "M30_effect_search.json")
    points = source_points(rom)
    assert effect["full_source_streak_matches"]
    star_frames = []
    for row in effect["full_source_streak_matches"]:
        frame = row["frame"]
        assert tables[1][frame]["PNG_sha256"] == row["PNG_sha256"]
        with Image.open(row["path"]) as image:
            assert matches(image, points) == row["all46_original_opaque_source_points_exact_at_origins"]
        star_frames.append(frame)
    assert len(star_frames) == 25 and max(star_frames) - min(star_frames) < 100
    source_timeline_path = Path("work/analysis/fls_frames_v312/all_files_proof.json")
    source_timeline = next(r for r in read(source_timeline_path)["cases"] if r["path"] == "/FLS/M30.fls")
    assert source_timeline["clean_source_native_states_and_geometry_exact"]
    texture_mapping = {slot["texture_input"]: slot["native_texture_index"]
                       for state in source_timeline["frames"]["states"] for slot in state["slots"]}
    source_poses = {}
    for state in source_timeline["frames"]["states"]:
        for draw in state["previous_buffer_geometry"]:
            if texture_mapping[draw["texture_input"]] == 4:
                source_poses[state["native_frame_counter"]] = draw["native_corners_fx12_before_clipping_or_GPU"][0]
    trajectory = []
    for row in effect["full_source_streak_matches"]:
        for x, y in row["all46_original_opaque_source_points_exact_at_origins"]:
            selected = [counter for counter, (fx, fy) in source_poses.items()
                        if abs(x - fx / 4096) <= 1 and abs(y - fy / 4096) <= 1]
            assert len(selected) == 1
            trajectory.append({"frame": row["frame"], "native_origin": [x, y],
                               "source_counter": selected[0], "source_preclip_fx12": source_poses[selected[0]]})
    assert sorted({r["source_counter"] for r in trajectory}) == [328, 329, 330, 331, 332, 333]
    partials = read(ROOT / "M30_partial_streak_diagnostic.json")
    assert len(partials) == 8 and {r["source_native_counter"] for r in partials} == {327, 334}
    for row in partials:
        frame = row["frame"]
        x0, y0 = row["origin"]
        fx, fy = source_poses[row["source_native_counter"]]
        assert abs(x0 - fx / 4096) <= 1 and abs(y0 - fy / 4096) <= 1
        visible = [(x, y, color) for x, y, color in points if 0 <= x0 + x < 256 and 0 <= y0 + y < 192]
        assert len(visible) == row["visible_source_points"] and 46 - len(visible) == row["clipped_source_points"]
        pixels = quantized(tables[1][frame]["path"]).load()
        assert all(pixels[x0 + x, y0 + y] == color for x, y, color in visible)
    all_effect_frames = sorted(star_frames + [r["frame"] for r in partials])
    assert all_effect_frames == list(range(13333, 13366))
    for frame in (13332, 13366):
        with Image.open(tables[1][frame]["path"]) as image:
            assert not matches(image, points)
    effect.update(source_timeline_proof=str(source_timeline_path),
                  source_timeline_proof_sha256=sha(source_timeline_path.read_bytes()),
                  current_FLS_update_projection_and_upload_code_exact_clean=fls_code_ranges,
                  complete_source_pattern_trajectory=trajectory,
                  original_viewport_entry_exit_clipping=partials,
                  continuous_native_effect_frames=all_effect_frames,
                  visible_source_stroke_pixel_checks=25 * 46 + sum(r["visible_source_points"] for r in partials),
                  full_pattern_negative_controls=[13332, 13366],
                  native_positions_agree_with_original_preclip_model_within_one_pixel=True,
                  not_an_instruction_trace_or_complete_background_pixel_model=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    screenshots = []
    selections = []
    for captain, case in current.items():
        selections.extend((captain, row["frame"], f"texture_{row['texture']}") for row in
                          [next(r for r in case["full_scene_cases"] if r["texture"] == index)
                           for index in case["distinct_complete_scene_textures"]])
        selections.append((captain, next(r["frame"] for r in case["credit_cases"] if r["native_gray_level"] == 31), "credits"))
        selections.append((captain, {1: 20280, 2: 26280, 3: 11280}[captain], "ending_save_prompt"))
    for pan in pans:
        rows = pan["exact_full_upper_frame_composites"]
        selections.extend((pan["captain_id"], row["frame"], "pan") for row in (rows[0], rows[len(rows) // 2], rows[-1]))
    selections.extend((1, f, "source_streak") for f in sorted({star_frames[0], star_frames[len(star_frames) // 2], star_frames[-1]}))
    selections.extend((1, frame, "clipped_source_streak") for frame in (13333, 13365))
    for captain, frame, context in selections:
        source = Path(tables[captain][frame]["path"])
        dest = ARCHIVE / f"V581_captain{captain}_{frame}_{context}.png"
        shutil.copyfile(source, dest)
        screenshots.append({"path": str(dest), "sha256": sha(dest.read_bytes()), "captain": captain,
                            "frame": frame, "context": context, "synthetic_ending_fixture": True})
    result = {"candidate": str(ROM), "candidate_sha256": digest, "production_ROM_changed": False,
              "fresh_current_ending_cases": list(current.values()), "current_split_pan_compositions": pans,
              "current_historical_whole_upper_comparisons_and_prompts": comparisons,
              "M30_complete_source_streak": effect,
              "additional_original_illustrations_review": read(ROOT / "additional_source_illustration_review.json"),
              "all_four_movie_files_and_five_ending_code_ranges_exact_clean": True,
              "source_and_fixture_copy_saves_unchanged": True,
              "one_byte_authorized_ending_state_per_run": True,
              "wrong_captain_and_wrong_version_guards_rejected": True,
              "current_Rafael_not_repeated_prior_V573_evidence_retained": True,
              "normal_earned_endings_and_hardware_not_verified": True,
              "not_every_intermediate_pixel_or_internal_GPU_alpha_verified": True,
              "underlying_lower_gameplay_can_persist_in_synthetic_ending_fixture": True,
              "all18_plaques_remain_incomplete_and22_historical_requirements_retained": True,
              "archive": str(ARCHIVE), "screenshots": screenshots, "full_goal_complete": False}
    proof = ROOT / "current_endings_proof.json"
    proof.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for config in provenance["cases"]:
        shutil.copyfile(CAPTURE / f"endings_current_v583_{config['label']}" / "capture_report.json",
                        ARCHIVE / f"{config['label']}_capture_report.json")
        shutil.copyfile(config["inputs"], ARCHIVE / Path(config["inputs"]).name)
    for path in (proof, ROOT / "fixture_provenance.json", ROOT / "M30_effect_search.json",
                 ROOT / "M30_streak_sequence_native.png", ROOT / "additional_source_illustration_review.json"):
        shutil.copyfile(path, ARCHIVE / path.name)
    print({"current_ending_runs": 3, "credit_frames": [len(c["credit_cases"]) for c in current.values()],
           "pan_frames": [len(p["exact_full_upper_frame_composites"]) for p in pans],
           "source_streak_frames": len(star_frames), "archived_screenshots": len(screenshots)})


if __name__ == "__main__":
    main()
