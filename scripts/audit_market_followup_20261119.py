"""Verify the current recommendation, its instructions and the Market return."""

from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from scripts import stage_market_followup_20261119 as build
from scripts import verify_market_reward_dialogue_20261115 as earlier
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold

base = build.base
PROOF = build.ROOT / "verified_market_followup.json"
SHEET = build.ROOT / "market_reward_replay.png"


def main():
    assert not PROOF.exists() and not SHEET.exists()
    stored = base.load(build.PROOF)
    candidate = base.digest(build.ROM)
    assert candidate == stored["candidate_sha256"]
    bind = FunctionType(earlier.read_run.__code__, vars(earlier) | {"ROOT": build.ROOT})
    report, captures, shots, evidence = bind("reviewed", candidate)
    path = build.ROOT / "reviewed/capture/common_observer/requests.json"
    trace = base.load(path)
    all_requests = [r["source_request"]["ID"] for r in trace["rows"] if r.get("source_request")]
    assert not {750, 751, 752}.intersection(all_requests)
    assert [r["source_request"]["ID"] for r in captures] == earlier.CHAIN
    evidence[str(path)] = base.digest(path)
    rom = base.NdsImage.open(build.ROM)
    arm, kanji = (rom.read_file(p) for p in (build.ARM, "/GRP/KANJI.FNT"))
    painter, _, _ = build.workflow.font_tools(rom)
    rows = {r["message_ID"]: r for r in stored["records"]}
    frames = {n: earlier.captured(shot) for n, shot in shots.items()}
    panels, observed = [], []
    for index, capture in enumerate(captures):
        number = capture["source_request"]["ID"]
        case, = rows[number]["native_displays"]
        assert capture["bounds"] == [0, 0, 228, 48] and capture["text_hex"] == case["display_hex"]
        plane, glyphs = build.rewards.render_portrait(painter, arm, kanji, bytes.fromhex(case["display_hex"]))
        assert build.native.digest(plane) == case["ink_sha256"] and len(glyphs) == case["glyph_count"]
        begin = capture["frame"]
        end = captures[index+1]["frame"] if index+1 < len(captures) else report["frames"]
        matched = []
        for n, photo in sorted(frames.items()):
            if not begin < n < end:
                continue
            try:
                ink = native_hold(photo, plane)
            except AssertionError:
                continue
            matched.append((n, ink))
        assert matched, (number, begin, end)
        n, ink = matched[0]
        evidence[shots[n]["path"]] = shots[n]["PNG_sha256"]
        panels.append((f"COMMON {number}, frame {n}", frames[n]))
        observed.append(dict(message_ID=number, occurrence_frame=begin, frame=n, complete_ink_pixels=ink,
                             text_hex=case["display_hex"], capture=shots[n]))

    final = report["frames"]
    baseline_path = earlier.ROOT / "reviewed/capture/capture_report.json"
    old = base.load(baseline_path)
    assert old["scripted_input_schedule"] == report["scripted_input_schedule"]
    old_frames = earlier.shots(old)
    back = 12000
    old_end = old_frames[back]
    assert earlier.captured(old_end).tobytes() == frames[back].tobytes()
    terminal_diff = ImageChops.difference(earlier.captured(old_frames[final]), frames[final]).getbbox()
    assert terminal_diff == (208, 243, 252, 258)  # Selected Port label highlight.
    panels.append(("Return from the Market", frames[back]))
    evidence[str(baseline_path)] = base.digest(baseline_path)
    evidence[old_end["path"]] = old_end["PNG_sha256"]
    evidence[old_frames[final]["path"]] = old_frames[final]["PNG_sha256"]
    for n in (back, final):
        evidence[shots[n]["path"]] = shots[n]["PNG_sha256"]
    sheet = Image.new("RGB", (1040, 456), "#263238")
    label = ImageDraw.Draw(sheet)
    for i, (title, photo) in enumerate(panels):
        x, y = i % 2 * 520, i // 2 * 228
        label.text((x+4, y+4), title, fill="white")
        body = photo.crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST)
        sheet.paste(body, (x+4, y+18))
    sheet.save(SHEET)
    evidence.update({str(p): base.digest(p) for p in (build.PROOF, SHEET, Path(__file__))})
    base.save(PROOF, dict(candidate_sha256=candidate, original_sequences_initialized=True,
        natural_random_selection_verified=False, hardware=False,
        outcomes=[dict(event="market_recommendation", observed=observed, original_return_screen_matches=True,
                       matching_return_frame=shots[back], final_frame=shots[final],
                       final_frame_difference_bounds=terminal_diff, legacy_keys_750_to_752_requested=False)],
        sheets=[dict(path=str(SHEET), sha256=base.digest(SHEET))], evidence=evidence))
    print("Verified the complete recommendation, instructions, farewell and return.")


if __name__ == "__main__":
    main()
