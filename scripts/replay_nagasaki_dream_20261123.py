"""Replay the Nagasaki Inn visit on the staged scene and check its full pages."""

import sys
from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from PIL import ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import headless_desmume_v193 as harness
from scripts import stage_nagasaki_dream_20261123 as build
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check


review = build.discovery
panels = review.panels
CAPTURE = build.ROOT / "revised/capture/capture_report.json"
REPORT = build.ROOT / "paired_nagasaki_dream.json"
ORIGINAL = review.run.ROOT / "capture/capture_report.json"


def play(stored, before):
    assert build.digest(build.ROM) == stored["candidate"]["sha256"]
    donor = before["battery_save_preloaded"]
    assert build.digest(donor["source"]) == donor["source_sha256"]
    folder = CAPTURE.parent.parent
    folder.mkdir()
    inputs = folder / "ordinary_inputs.json"
    build.write(inputs, before["scripted_input_schedule"])
    frames = sorted(panels.shots(before, "_navigation.png"))
    original_argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(CAPTURE.parent),
            "--frames", str(frames[-1]), "--inputs-json", str(inputs), "--press-start", "-1", "--touchscreen",
            "--battery-save", donor["source"], "--capture-every", "999999", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = original_argv


def verify(stored, before):
    current = build.read(CAPTURE)
    assert current["ROM_sha256"] == stored["candidate"]["sha256"] == build.digest(build.ROM)
    assert before["ROM_sha256"] == stored["previous"]["sha256"]
    assert current["cold_boot"] and not current["savestate_loaded"] and not current["callback_errors"]
    assert not any(v for k, v in current.items() if k.startswith("synthetic_"))
    assert current["scripted_input_schedule"] == before["scripted_input_schedule"]
    for key in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
        assert current["battery_save_preloaded"][key] == before["battery_save_preloaded"][key]
    assert current["frames"] == before["frames"] == 12640
    old, new = panels.shots(before, "_navigation.png"), panels.shots(current, "_cold_boot.png")
    assert set(old) == set(current["exact_requested_capture_frames"]) <= set(new)
    changed = {review.FRAMES[key]: key for key in review.PROPOSALS if key in review.FRAMES}
    assert set(changed) == {9440, 10440, 11240}
    rom = build.NdsImage.open(build.ROM)
    arm, kanji = rom.read_file(build.ARM), rom.read_file("/GRP/KANJI.FNT")
    paint = panels.town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    font = GameAsciiFont.from_arm9(arm)
    records = {int(r["id"].rsplit("_R", 1)[1]): r for r in stored["records"]}
    live, controls, views = [], [], []
    for frame, anchor in sorted(old.items()):
        older, revised = panels.picture(anchor), panels.picture(new[frame])
        diff = ImageChops.difference(older, revised).getbbox()
        if frame not in changed:
            assert diff is None, (frame, diff)
            controls.append(frame)
            continue
        row = records[changed[frame]]
        page = stored["stored_native_pages"][row["id"]]
        content = bytes.fromhex(page["content_hex"])
        rendered, = paint(arm, kanji, content)["pages"]
        plane = bytes.fromhex(rendered["native_plane_hex"])
        assert build.sha256(plane).hexdigest() == page["page_sha256"] and mask_check(plane, 216, revised)
        assert diff and 16 <= diff[0] < diff[2] <= 232 and 296 <= diff[1] < diff[3] <= 360, (frame, diff)
        nameplate = panels.nameplate(font, row["speaker"], revised)
        assert nameplate == panels.nameplate(font, row["speaker"], older)
        live.append(dict(id=row["id"], frame=frame, previous=anchor, revised=new[frame],
                         nameplate=nameplate, changed_pixel_bounds=diff, native_plane_sha256=page["page_sha256"]))
        views.extend(((f"{frame} previous", older), (f"{frame} revised", revised)))
    assert {11440, 11640, 11840, 12040, 12240, 12640} <= set(controls)
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": REPORT})
    visual, = sheets("paired_nagasaki_dream", views, (0, 272, 256, 380))
    build.write(REPORT, dict(ordinary_controller_gameplay=True, fixture=False,
        candidate_sha256=current["ROM_sha256"], predecessor_sha256=before["ROM_sha256"],
        original_capture=build.reference(ORIGINAL), revised_capture=build.reference(CAPTURE),
        changed_holds=live, identical_control_frames=controls, cleaver_and_Inn_return=True,
        conditional_Angelo_panels_observed=False, visual=visual))
    print(f"Verified {len(live)} revised full pages and {len(controls)} exact control frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    action = cli.parse_args().action
    (play if action == "replay" else verify)(build.read(build.STORED), build.read(ORIGINAL))
