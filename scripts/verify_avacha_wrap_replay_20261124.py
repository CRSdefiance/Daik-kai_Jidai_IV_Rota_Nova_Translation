"""Check the Avacha clue and its surrounding live panels with position-only setup."""

import io
import json
import sys
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import ImageChops

from scripts import observe_narvik_focused_visit_20261124 as fixture
from scripts import stage_village_article_wraps_20261124 as build
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts import headless_desmume_v193 as harness
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_narvik_lookout_replay_20261124 import coordinate_proof


VILLAGE = 22
ROOT = build.ROOT / "avacha_complete_inputs"
OUT = build.ROOT / "paired_gameplay.json"
HISTORIC = Path("E:/Rota Nova translations/Generated/work/emulation_v193/village_development_v665_22_first")
INITIAL = Path("work/analysis/village_visits_v664/inputs_chief_22.json")
END, CLUE = 10980, 10180


def receipt(case):
    previous = read(build.RELEASE)
    if case == "before":
        return previous
    staged = read(build.STORED)
    assert staged["predecessor_sha256"] == previous["candidate_sha256"] and staged["whole_parent_inverse"]
    return previous | {key: staged[key] for key in ("candidate", "candidate_sha256", "target_ARM9_sha256")}


def historical():
    report = read(HISTORIC / "capture_report.json")
    progress = read(HISTORIC / "controller_progress.json")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert progress["error"] is None and progress["answer"] == "Avacha"
    assert progress["phases"]["accepted_clue"] == CLUE and progress["phases"]["developed_village_menu"] == END
    position, = report["synthetic_location_fixtures"]
    assert position["frame"] == 5200 and position["village_id"] == VILLAGE and position["only_eight_ship_coordinate_bytes_owned"]
    commands = [row["command"] for row in progress["commands"] if row["frame"] < END] + [{"stop": True}]
    donor = report["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_") and key != "synthetic_location_fixtures")
    return report, position, commands, donor


def replay(case):
    current = receipt(case)
    assert digest(current["candidate"]) == current["candidate_sha256"]
    archive, position, commands, donor = historical()
    root = ROOT / case
    root.mkdir(parents=True)
    inputs = root / "before_fixture_inputs.json"
    base_schedule = read(INITIAL)
    assert archive["scripted_input_schedule"][:len(base_schedule)] == base_schedule
    inputs.write_text(json.dumps(base_schedule), encoding="utf-8")
    water = tuple(position["expected_selector_point_after_original_update"])
    code = checked_text(getsource(fixture.visit_position), {
        "release = replay.base.load(active.RELEASE)": "release = authorized_release",
        "water = (x, y - 22)": "water = route_water\n    assert (x - water[0]) ** 2 + (y - water[1]) ** 2 < 32 ** 2",
    })
    env = vars(fixture) | dict(NARVIK=VILLAGE, authorized_release=current, route_water=water, __file__=__file__)
    exec(compile(code, __file__ + "::known-Avacha-water", "exec"), env)
    old, stdin, argv = fixture.location.relocate, sys.stdin, sys.argv
    controller = io.StringIO("".join(json.dumps(c) + "\n" for c in commands))
    try:
        fixture.location.relocate, sys.stdin = env["visit_position"], controller
        sys.argv = [__file__, "--rom", current["candidate"], "--out", str(root), "--frames", str(END + 100),
            "--inputs-json", str(inputs), "--battery-save", donor["source"], "--pause-at", "5200",
            "--allow-location-fixtures", "--touchscreen", "--press-start", "-1", "--capture-every", "999999"]
        harness.main()
    finally:
        sys.argv, sys.stdin, fixture.location.relocate = argv, stdin, old


def captures(case, commands, donor, water):
    path = ROOT / case / "capture_report.json"
    r = read(path)
    assert r["ROM_sha256"] == receipt(case)["candidate_sha256"] and r["frames"] == END
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert r["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    event, = r["synthetic_location_fixtures"]
    assert event["frame"] == 5200 and event["only_eight_ship_coordinate_bytes_owned"]
    assert event["expected_selector_point_after_original_update"] == water
    assert not any(value for key, value in r.items() if key.startswith("synthetic_") and key != "synthetic_location_fixtures")
    journal = ROOT / case / "navigation_command_journal.json"
    assert [row["command"] for row in read(journal)["commands_received"]] == commands
    return panels.shots(r, "_navigation.png"), dict(capture=reference(path), journal=reference(journal), location_fixture=event)


def verify():
    _, position, controls, donor = historical()
    water = position["expected_selector_point_after_original_update"]
    before, a = captures("before", controls, donor, water)
    after, b = captures("after", controls, donor, water)
    assert coordinate_proof(a) == coordinate_proof(b) and before.keys() == after.keys()
    arm = NdsImage.open(receipt("after")["candidate"]).read_file(build.ARM)
    font = panels.GameAsciiFont.from_arm9(arm)
    clue, = [row for row in read(build.OUT)["native_cases"] if row["index"] == VILLAGE]
    figures, checks, identical = [], {}, []
    for frame in sorted(before):
        old, new = (panels.picture(group[frame]) for group in (before, after))
        bounds = ImageChops.difference(old, new).getbbox()
        if frame != CLUE:
            assert bounds is None, (frame, bounds)
            identical.append(frame)
            continue
        assert bounds and 16 <= bounds[0] < bounds[2] <= 244 and 296 <= bounds[1] < bounds[3] <= 360
        for key, shot, text in (("before", old, clue["previous"]), ("after", new, clue["proposed"])):
            rows = tuple(line.strip() for line in text.splitlines())
            checks[key] = dict(lines=rows, pixels=panels.exact_body(font, rows, shot),
                               nameplate=panels.nameplate(font, "Charles Rochefort", shot))
            figures.append(("Avacha / " + key, shot))
        assert checks["before"]["nameplate"] == checks["after"]["nameplate"]
    assert checks and {9780, 10580, END} <= set(identical)
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=OUT),
                        argdefs=panels.sheets_for.__defaults__)
    write(OUT, dict(candidate_sha256=receipt("after")["candidate_sha256"], predecessor_sha256=receipt("before")["candidate_sha256"],
        history=reference(HISTORIC / "capture_report.json"), controller_history=reference(HISTORIC / "controller_progress.json"),
        initial_schedule=reference(INITIAL),
        before=a, after=b, verified_frame=CLUE, verified_clue=checks, unchanged_frames=identical,
        position_only_focused_gameplay=True, sheets=draw("paired_avacha_article_wrap", figures)))
    print(f"Verified Avacha and {len(identical)} unchanged gameplay frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("before", "after", "verify"))
    action = cli.parse_args().action
    if action == "verify":
        verify()
    else:
        replay(action)
