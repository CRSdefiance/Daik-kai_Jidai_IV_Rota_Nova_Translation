"""Replay the ordinary preparation menu and check the new reply against its stored page."""

import sys
from argparse import ArgumentParser
from types import FunctionType

from PIL import ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_rafael_prepare_alone_20261123 as build


review = build.review
panels = review.panels
REPLAY = build.ROOT / "replay/capture/capture_report.json"
PAIRED = build.ROOT / "paired_prepare_alone.json"
SHEET = build.ROOT / "paired_rafael_prepare_alone_1_20261123.png"


def replay(stored):
    assert build.digest(build.ROM) == stored["candidate"]["sha256"]
    old = build.read(review.run.REPORT)
    assert old["ROM_sha256"] == stored["previous"]["sha256"]
    area = REPLAY.parent.parent
    area.mkdir()
    inputs = area / "ordinary_inputs.json"
    build.write(inputs, old["scripted_input_schedule"])
    frames = [row["frame"] for row in old["frames_captured"] if row["frame"] <= review.RETURN_FRAME]
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(REPLAY.parent), "--frames", str(review.RETURN_FRAME),
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999", "--capture-at", *map(str, frames)]
        review.run.emulator.main()
    finally:
        sys.argv = argv


def verify(stored):
    old, new = map(build.read, (review.run.REPORT, REPLAY))
    assert old["ROM_sha256"] == stored["previous"]["sha256"]
    assert new["ROM_sha256"] == stored["candidate"]["sha256"] == build.digest(build.ROM)
    assert new["cold_boot"] and not new["callback_errors"] and not new["savestate_loaded"]
    assert not new.get("battery_save_preloaded")
    assert not any(value for key, value in new.items() if key.startswith("synthetic_"))
    assert old["frames"] == new["frames"] == review.RETURN_FRAME
    assert old["scripted_input_schedule"] == new["scripted_input_schedule"]
    old_shots, new_shots = ({row["frame"]: row for row in run["frames_captured"]} for run in (old, new))
    assert old_shots.keys() == new_shots.keys()
    font = GameAsciiFont.from_arm9(build.NdsImage.open(build.ROM).read_file(build.ARM))
    plane = bytes.fromhex(stored["native_proof"]["pages"][0]["native_plane_hex"])
    unchanged = []
    for frame in sorted(old_shots):
        a, b = (panels.picture(shots[frame]) for shots in (old_shots, new_shots))
        bounds = ImageChops.difference(a, b).getbbox()
        if frame == review.RESPONSE_FRAME:
            assert bounds and 16 <= bounds[0] < bounds[2] <= 232 and 296 <= bounds[1] < bounds[3] <= 360
            assert review.mask_check(plane, 216, b)
            name = panels.nameplate(font, "Julio Erneco", b)
            assert name == panels.nameplate(font, "Julio Erneco", a)
            sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": PAIRED})
            visual, = sheets("paired_rafael_prepare_alone", [("Previous reply", a), ("Revised reply", b)], (0, 272, 256, 380))
        else:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
    assert visual == build.reference(SHEET)
    assert {review.RETURN_FRAME, *review.CHOICE_FRAMES} <= set(unchanged)
    build.write(PAIRED, dict(candidate_sha256=new["ROM_sha256"], previous_sha256=old["ROM_sha256"],
        source_run=build.reference(review.run.REPORT), replay=build.reference(REPLAY), stored=build.reference(build.STORED),
        visual=visual, separate_native_preview=stored["visual"], changed_frame=new_shots[review.RESPONSE_FRAME],
        unchanged_frames=unchanged, complete_Julio_nameplate=name, complete_page_sha256=build.sha256(plane).hexdigest(),
        original_choice_and_town_return_unchanged=True, ordinary_new_game=True))
    print(f"Verified the revised native page and {len(unchanged)} exact context and transition frames from New Game.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    globals()[cli.parse_args().action](build.read(build.STORED))
