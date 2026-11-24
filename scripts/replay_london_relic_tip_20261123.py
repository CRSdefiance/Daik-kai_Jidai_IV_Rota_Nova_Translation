"""Cold-boot the staged relic clue and verify the original Tavern flow."""

import sys
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType

from PIL import ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import headless_desmume_v193 as harness
from scripts import stage_london_relic_tip_20261123 as build
from scripts import verify_london_tavern_20261123 as london
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


ROOT = build.ROOT
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in (
    "translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CAPTURE = ROOT / "revised/capture/capture_report.json"
REPORT = ROOT / "paired_london_relic_tip.json"
SHEET = ROOT / "paired_london_relic_tip_1_20261123.png"


def play(stored):
    original = read(london.OUT)
    previous = read(original["capture"]["path"])
    assert reference(original["capture"]["path"]) == original["capture"]
    assert previous["ROM_sha256"] == original["candidate_sha256"] == stored["previous_sha256"]
    assert digest(build.ROM) == stored["candidate_sha256"]
    donor = previous["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    folder = CAPTURE.parent.parent
    folder.mkdir()
    schedule = folder / "ordinary_inputs.json"
    write(schedule, previous["scripted_input_schedule"])
    frames = sorted(london.genoa.shots(previous, "_navigation.png"))
    original_argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(CAPTURE.parent), "--frames", str(frames[-1]),
            "--inputs-json", str(schedule), "--press-start", "-1", "--touchscreen", "--battery-save", donor["source"],
            "--capture-every", "999999", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = original_argv


def verify(stored):
    original = read(london.OUT)
    previous, current = map(read, (original["capture"]["path"], CAPTURE))
    assert reference(original["capture"]["path"]) == original["capture"]
    assert original["candidate_sha256"] == stored["previous_sha256"] == previous["ROM_sha256"]
    assert stored["candidate_sha256"] == current["ROM_sha256"] == digest(build.ROM)
    assert current["cold_boot"] and not current["savestate_loaded"] and not current["callback_errors"]
    assert not any(v for k, v in current.items() if k.startswith("synthetic_"))
    assert current["frames"] == previous["frames"] == 24300
    assert current["scripted_input_schedule"] == previous["scripted_input_schedule"]
    assert current["battery_save_preloaded"]["source_sha256"] == previous["battery_save_preloaded"]["source_sha256"]
    assert digest(current["battery_save_preloaded"]["source"]) == current["battery_save_preloaded"]["source_sha256"]
    before = london.genoa.shots(previous, "_navigation.png")
    after = london.genoa.shots(current, "_cold_boot.png")
    assert set(before) == set(current["exact_requested_capture_frames"]) <= set(after)
    hint, = (row for row in original["records"] if row["message_ID"] == build.KEY)
    changed = {hold["frame"] for hold in hint["holds"]}
    assert changed == {16700, 19900, 23100}
    layout, = (row["display"] for row in stored["samples"] if row["version"] == "revised"
               and row["arguments"] == list(london.ITEM_ARGS))
    lines = layout["lines"]
    rom = NdsImage.open(build.ROM)
    arm = rom.read_file(build.ARM)
    installed = london.common_rows(rom.read_file(build.COMMON), arm)[build.KEY]
    assert (installed.text % tuple(s.encode("ascii") for s in london.ITEM_ARGS)).decode("ascii").split() == " ".join(lines).split()
    font = GameAsciiFont.from_arm9(arm)
    checked, controls, menus, images = [], [], [], []
    return_menus = {17100, 20300, 23500}
    for frame, anchor in sorted(before.items()):
        older, revised = london.genoa.picture(anchor), london.genoa.picture(after[frame])
        bounds = ImageChops.difference(older, revised).getbbox()
        if frame in changed:
            assert bounds and 16 <= bounds[0] < bounds[2] <= 244 and 296 <= bounds[1] < bounds[3] <= 360
            assert london.genoa.nameplate(font, hint["speaker"], older) == london.genoa.nameplate(font, hint["speaker"], revised)
            checked.append(dict(frame=frame, lines=lines, body_ink_pixels=london.genoa.exact_body(font, lines, revised),
                                diff_bounds=bounds, previous=anchor, revised=after[frame]))
            images.extend(((f"{frame} / before", older), (f"{frame} / revised", revised)))
        elif frame in return_menus:
            assert bounds == (86, 258, 170, 278)
            differences = Counter((a, b) for a, b in zip(
                older.crop(bounds).get_flattened_data(), revised.crop(bounds).get_flattened_data(), strict=True) if a != b)
            assert differences == {((205, 198, 180), (0, 165, 172)): 1550}
            menus.append(dict(frame=frame, bounds=bounds, background_pixels=1550, all_caption_pixels_identical=True))
        else:
            assert not bounds, (frame, bounds)
            controls.append(frame)
    assert {23900, 24300} <= set(controls) and len(menus) == 3
    images.extend((("23500 / menu before", london.genoa.picture(before[23500])),
                   ("23500 / menu revised", london.genoa.picture(after[23500]))))
    sheets_for = FunctionType(london.genoa.sheets_for.__code__, london.genoa.sheets_for.__globals__ | {"OUT": REPORT})
    visual, = sheets_for("paired_london_relic_tip", images, (0, 248, 256, 376))
    assert visual == reference(SHEET)
    write(REPORT, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["previous_sha256"],
        revised_tip_holds=checked, ordinary_battery_save_gameplay=True, fixture=False,
        returned_to_tavern_and_town=True, identical_control_frames=controls, original_menu_highlight_frames=menus, visual=visual,
        original_capture=original["capture"], revised_capture=reference(CAPTURE)))
    print(f"Verified three revised hints, {len(controls)} exact controls and three menu-highlight phases.")


def main(action):
    stored = read(build.STORED)
    if action == "replay":
        play(stored)
        return
    if action == "verify":
        verify(stored)
        return
    previous = read(build.parent.RELEASE)
    proof = stored | dict(candidate=str(build.ROM), clean_input_sha256=previous["clean_input_sha256"],
                          predecessor_sha256=previous["candidate_sha256"])
    scope = vars(checks) | dict(RELEASE=build.parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT,
                                STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(build.ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify", "patch", "startup"))
    main(cli.parse_args().action)
