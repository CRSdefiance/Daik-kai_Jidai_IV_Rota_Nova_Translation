"""Replay Rafael's ordinary Lisbon route and verify the two changed displays."""

import sys
from argparse import ArgumentParser
from types import FunctionType

from PIL import ImageChops

from scripts import headless_desmume_v193 as harness
from scripts import stage_lisbon_roster_galley_20261124 as build
from scripts import verify_ordinary_lisbon_purser_20261124 as baseline
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


OUT = build.ROOT / "paired_gameplay.json"
ROOT = build.ROOT / "ordinary_replay"
BEFORE = baseline.play.ROOT / "capture/capture_report.json"
AFTER = ROOT / "capture_report.json"
GALLEY = {25280, 26580}
ROSTER = 30800
END = 37300
panels = baseline.panels


def previous_capture():
    old, receipt = read(BEFORE), read(build.RELEASE)
    source = read(baseline.play.current.RELEASE)
    assert old["ROM_sha256"] == source["candidate_sha256"]
    assert digest(source["candidate"]) == source["candidate_sha256"]
    assert digest(receipt["candidate"]) == receipt["candidate_sha256"]
    # The original ordinary trace predates the three village article wraps.
    # Invert those exact fields to bind every other ROM component to it.
    original, parent = (NdsImage.open(c["candidate"]) for c in (source, receipt))
    arm = parent.read_file(build.ARM)
    former = build.parent.build.former
    code = former.MainCodeFile(arm, former.BASE)
    for edit in read(build.parent.build.STORED)["changed_pool_spans"]:
        at, size = edit["pool_offset"], edit["extent"]
        assert code.sections[3].data[at:at + size].hex() == edit["after_hex"]
        code.sections[3].data[at:at + size] = bytes.fromhex(edit["before_hex"])
    assert bytes(code.save()) == original.read_file(build.ARM)
    parent.replace_file(build.ARM, bytes(code.save()))
    assert build.sha256(parent.rom.save()).hexdigest() == source["candidate_sha256"]
    _verify_report(old)
    assert old["frames"] == END
    return old, receipt


def _verify_report(report):
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    save = report["battery_save_preloaded"]
    assert save["copied_byte_exact_before_cold_boot"] and digest(save["source"]) == save["source_sha256"]


def replay():
    old, receipt = previous_capture()
    stored = read(build.STORED)
    assert stored["predecessor_sha256"] == receipt["candidate_sha256"] and digest(build.ROM) == stored["candidate_sha256"]
    frames = sorted(panels.shots(old, "_navigation.png"))
    ROOT.mkdir()
    inputs = ROOT / "ordinary_inputs.json"
    write(inputs, old["scripted_input_schedule"])
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(ROOT), "--frames", str(END),
            "--inputs-json", str(inputs), "--battery-save", old["battery_save_preloaded"]["source"],
            "--touchscreen", "--press-start", "-1", "--capture-every", "999999", "--dump-ram",
            "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = argv


def verify():
    old, receipt = previous_capture()
    new, stored, preflight = map(read, (AFTER, build.STORED, build.OUT))
    assert receipt["candidate_sha256"] == stored["predecessor_sha256"] and digest(build.ROM) == new["ROM_sha256"] == stored["candidate_sha256"]
    _verify_report(new)
    assert new["scripted_input_schedule"] == old["scripted_input_schedule"] and old["frames"] == new["frames"] == END
    assert new["battery_save_preloaded"]["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    before, after = panels.shots(old, "_navigation.png"), panels.shots(new, "_cold_boot.png")
    assert before.keys() <= after.keys()
    arm = NdsImage.open(build.ROM).read_file(build.ARM)
    font = panels.GameAsciiFont.from_arm9(arm)
    reflow, = [row for row in preflight["records"] if row["id"] == f"COMMON_MESSAGE_{build.KEY}"]
    summary, changes, identical, figures = None, [], [], []
    for frame in sorted(before):
        a, b = (panels.picture(frames[frame]) for frames in (before, after))
        bounds = ImageChops.difference(a, b).getbbox()
        if frame == ROSTER:
            assert bounds and 72 <= bounds[0] < bounds[2] <= 78 and 333 <= bounds[1] < bounds[3] <= 344
            mask = panels.find_mask(font, "Finance 115", b, (5, 326, 130, 345))
            assert mask["bounds"] == [12, 333, 78, 344] and mask["ink_pixels"] == 122
            summary = dict(frame=frame, complete_summary=mask, exact_difference_bounds=bounds)
            continue
        if frame in GALLEY:
            assert bounds and 64 <= bounds[0] < bounds[2] <= 232 and 79 <= bounds[1] < bounds[3] <= 139
            lines, ink = baseline.shipyard.exact_refit(font, bytes.fromhex(reflow["payload_hex"]).rstrip(), b)
            assert lines == reflow["compiled_lines"]
            changes.append(dict(frame=frame, complete_body_ink=ink, lines=lines, bounds=bounds))
            if not figures:
                figures.extend([("Before / Galley", a), ("Revised / Galley", b)])
            continue
        assert bounds is None, (frame, bounds)
        identical.append(frame)
    assert summary is not None and {r["frame"] for r in changes} == GALLEY and END in identical
    assignment = baseline.assignment(arm, new)
    assert assignment["assigned_actor"] == 6 and assignment["finance"] == 115 and assignment["room_slot"] == 12
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=OUT), argdefs=panels.sheets_for.__defaults__)
    roster = [(label, panels.picture(group[ROSTER])) for label, group in (("Before / roster", before), ("Revised / roster", after))]
    sheets = draw("lisbon_galley_paired", figures, crop=(0, 60, 256, 157))
    sheets += draw("lisbon_roster_paired", roster, crop=(0, 314, 256, 370))
    write(OUT, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=receipt["candidate_sha256"],
        ordinary_play=True, exact_later_clue_inverse=True, before=reference(BEFORE), after=reference(AFTER),
        full_roster_summary=summary, galley=changes, unchanged_frames=identical, assigned_purser=assignment, sheets=sheets))
    print(f"Verified Finance 115, {len(changes)} Galley holds and {len(identical)} matching surrounding frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    globals()[cli.parse_args().action]()
