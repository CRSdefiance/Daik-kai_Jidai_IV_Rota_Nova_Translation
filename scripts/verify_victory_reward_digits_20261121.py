"""Replay fleet victory and compare the complete restored English number masks."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from scripts import stage_victory_reward_digits_20261121 as stage
from scripts import verify_clifford_declaration_wrap_20261121 as history


base = stage.base
ROOT = stage.ROOT / "playback"
RUN = ROOT / "attack"
PROOF = stage.ROOT / "verified_gameplay.json"
SHEET = stage.ROOT / "victory_rewards_live.png"
HOLDS = {8800: (303, ("109", "103")), 9100: (301, ("6055",)), 9200: (301, ("6055",))}


def verify():
    assert not PROOF.exists()
    draft = base.load(stage.PROOF)
    folders = (history.RUN, RUN)
    paths = [folder / "capture/capture_report.json" for folder in folders]
    reports = list(map(base.load, paths))
    assert [r["ROM_sha256"] for r in reports] == [draft["parent_sha256"], draft["candidate_sha256"]]
    assert base.digest(stage.ROM) == draft["candidate_sha256"]
    assert all(r["cold_boot"] and r["frames"] == 9200 and not r["savestate_loaded"] and not r["callback_errors"]
               for r in reports)
    for key in ("core_options", "scripted_input_schedule", "exact_requested_capture_frames", "core_DLL_sha256"):
        assert reports[0][key] == reports[1][key], key
    for key in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
        assert reports[0]["battery_save_preloaded"][key] == reports[1]["battery_save_preloaded"][key], key
    expected_fixture = ("frame", "changes", "original_existing_enemy_fleet",
                        "all_other4MiB_enemy_health_crew_equipment_actors_IDs_RNG_eligibility_and_results_exact")
    before, after = (r["synthetic_battle_recovery_proximity_fixtures"][0] for r in reports)
    assert all(before[key] == after[key] for key in expected_fixture)
    assert after["frame"] == 4800 and len(after["owned_bytes"]) == 40
    traces = [base.load(folder / "requests.json") for folder in folders]
    assert traces[0]["source_requests"] == traces[1]["source_requests"]
    assert all(r["callbacks"] == 44 and not r["errors"] and not r["mismatches"] for r in traces)

    views = [{r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
             for report in reports]
    assert views[0].keys() == views[1].keys()
    unchanged, changed = [], []
    cal = stage.discovery.mixed
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = (image.read_file(p) for p in (stage.shared.ARM, "/GRP/KANJI.FNT"))
    raster, _, _ = cal.font_tools(image)
    sheet = Image.new("RGB", (1024, 2 * 248), "#263238")
    labels = ImageDraw.Draw(sheet)
    for frame, before in views[0].items():
        after = views[1][frame]
        for row in (before, after):
            assert base.digest(row["path"]) == row["PNG_sha256"]
        if frame not in HOLDS:
            assert before["framebuffer_sha256"] == after["framebuffer_sha256"], frame
            unchanged.append(frame)
            continue
        ident, args = HOLDS[frame]
        sample, = [r for r in draft["native_display_cases"] if r["message_ID"] == ident and tuple(r["arguments"]) == args]
        formatted = bytes.fromhex(sample["native_wrapper_output_hex"])
        native, glyphs = cal.render(raster, arm, kanji, formatted)
        pair = [Image.open(row["path"]).convert("RGB") for row in (before, after)]
        box = (16, 296, 244, 344)
        assert bytes(pixel == (0, 8, 0) for pixel in pair[1].crop(box).get_flattened_data()) == native, frame
        rect = ImageChops.difference(*pair).getbbox()
        assert rect and box[0] <= rect[0] < rect[2] <= box[2] and box[1] <= rect[1] < rect[3] <= box[3], (frame, rect)
        changed.append(dict(frame=frame, message_ID=ident, values=list(args), before=before, after=after,
                            lines=sample["lines"], exact_native_ink=True, changed_rectangle=rect, glyphs=len(glyphs)))
        if frame in (8800, 9200):
            top = 248 if frame == 9200 else 0
            for i, panel in enumerate(pair):
                left = i * 512
                outcome = "Food and water" if frame == 8800 else "Captured gold"
                labels.text((left + 6, top + 7), outcome + (" before" if i == 0 else " corrected"), fill="white")
                sheet.paste(panel.crop((0, 270, 256, 384)).resize((512, 228), Image.Resampling.NEAREST),
                            (left, top + 20))
    sheet.save(SHEET)
    assert len(changed) == 3 and len(unchanged) == 19
    base.save(PROOF, dict(candidate_sha256=draft["candidate_sha256"], parent_sha256=draft["parent_sha256"],
        original_controls=True, original_victory_amounts=[109, 103, 6055], changed_number_calls=4,
        read_only_trace_matches=True, exact_unchanged_framebuffers=unchanged, held_notices=changed,
        national_reward_observed=False, hardware_verified=False, sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        source_evidence={str(p): base.digest(p) for p in (*paths, *(f / "requests.json" for f in folders))}))
    print("Food, water and capture proceeds render in the regular font. The other 19 frames match.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="Verify a completed paired capture.")
    if not parser.parse_args().verify_only:
        FunctionType(history.playback.__code__, vars(history) | {"ROOT": ROOT, "stage": stage, "__file__": __file__})()
    verify()
