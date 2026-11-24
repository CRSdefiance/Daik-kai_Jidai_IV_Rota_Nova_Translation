"""Replay Claudio's reflow from a cold New Game and verify the exact live change."""

import sys

from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont

from scripts import headless_desmume_v193 as harness
from scripts import stage_claudio_opening_wrap_20261124 as stage
from scripts import verify_rafael_new_game_fleet_20261124 as original
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write

OUT = original.OUT.with_name("claudio_opening_wrap_paired_20261124.json")
SHEET = OUT.with_suffix(".png")
ROOT = stage.ROOT / "ordinary_new_game"
HOLD = 12000


def replay():
    stored = read(stage.STORED)
    assert stored["candidate"] == reference(stage.ROM) and stored["complete_parent_inverse"]
    assert stored["previous"] == reference(stage.parent.ROM)
    prior = original.read(original.OUT)
    assert prior["candidate_sha256"] == stored["previous"]["sha256"]
    expiry = original.play.FRAMES[-1] + 1
    ROOT.mkdir()
    events, frames, end, _, donor = original.play.schedule(original.play.CASE)
    assert end == expiry and donor is None
    inputs = ROOT / "inputs.json"
    write(inputs, events)
    args = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(stage.ROM), "--out", str(ROOT / "capture"), "--frames", str(end),
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
            "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = args


def verify():
    stored, native = map(read, (stage.STORED, stage.NATIVE))
    assert stored["candidate"] == reference(stage.ROM) and stored["preview"] == reference(stage.NATIVE)
    assert native["sheet"] == reference(stage.SHEET)
    base = original.read(original.OUT)
    initial = original.play.ROOT / original.play.CASE / "capture/capture_report.json"
    assert reference(initial) in base["evidence"]
    final = ROOT / "capture/capture_report.json"
    old, new = map(read, (initial, final))
    assert old["ROM_sha256"] == stored["previous"]["sha256"] and new["ROM_sha256"] == stored["candidate"]["sha256"]
    assert old["frames"] == new["frames"] == original.play.FRAMES[-1] + 1
    for result in (old, new):
        assert result["cold_boot"] and not result["savestate_loaded"] and not result["callback_errors"]
        assert not result.get("battery_save_preloaded")
        assert not any(v for k, v in result.items() if k.startswith("synthetic_"))
    assert old["scripted_input_schedule"] == new["scripted_input_schedule"]

    panels = original.gameplay.panels
    old_frames, new_frames = (panels.shots(result, "_cold_boot.png") for result in (old, new))
    assert set(old_frames) == set(new_frames)
    before, after = (panels.picture(frames[HOLD]) for frames in (old_frames, new_frames))
    companions = [frame for frame in sorted(old_frames) if frame != HOLD]
    assert all(old_frames[frame]["framebuffer_sha256"] == new_frames[frame]["framebuffer_sha256"]
               for frame in companions)

    arm = NdsImage.open(stage.ROM).read_file(stage.parent.ARM)
    font = GameAsciiFont.from_arm9(arm)
    revised = next(row for row in native["layouts"] if row["scope"] == "Revised with Rafael")
    old_rows = base["story"]["encounter_records"][original.WRAP_ID]["observed_lines"]
    new_rows = revised["lines"]
    assert " ".join(old_rows) == " ".join(new_rows)
    assert "at his side." in new_rows[1]
    complete_masks = [panels.exact_body(font, rows, screen) for rows, screen in ((old_rows, before), (new_rows, after))]
    plates = [panels.nameplate(font, "Claudio Manaus", screen) for screen in (before, after)]
    assert plates[0] == plates[1]
    cards = Image.new("RGB", (528, 424), "#263238")
    names = ImageDraw.Draw(cards)
    for index, (label, frame) in enumerate((("Registered candidate", before), ("Staged wrap with Rafael", after))):
        x = index * 264 + 4
        names.text((x, 3), label, fill="white")
        cards.paste(frame, (x, 20))
    cards.save(SHEET)
    write(OUT, dict(candidate=stored["candidate"], current=stored["previous"], native=reference(stage.NATIVE),
        cold_boot_ordinary_new_game=True, same_controller_inputs=True, matching_companion_frames=companions,
        reviewed_record=original.WRAP_ID, revised_frame=HOLD, previous_rows=old_rows, proposed_rows=new_rows,
        exact_bodies_and_nameplate=complete_masks, nameplate=plates[0], current_capture=old_frames[HOLD],
        revised_capture=new_frames[HOLD], evidence=list(map(reference, (initial, final, stage.STORED))),
        contact_sheet=reference(SHEET), registered_build_pending=True))
    print(f"Verified Claudio's complete phrase in ordinary New Game and {len(companions)} matching companion frames.")


if __name__ == "__main__":
    replay()
    verify()
