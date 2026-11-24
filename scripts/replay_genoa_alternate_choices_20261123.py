"""Use ordinary Genoa controls to take Julio's two remaining recruitment paths."""

import sys
from argparse import ArgumentParser
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import register_genoa_dialogue_20261123 as current
from scripts import replay_genoa_dialogue_20261123 as previous
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, reference, write


ROOT = Path(".codex-release-work/shared_display_20261123/genoa_alternate_choices")
CASES = {"no_liquor": (13500, 12), "test_julio": (15100, 14)}


def plan(branch, release):
    source = previous.CAPTURE
    assert digest(source) == read(previous.REPORT)["revised_capture"]["sha256"]
    run = read(source)
    assert run["ROM_sha256"] == release["candidate_sha256"]
    assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
    assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
    menu, length = CASES[branch]
    controls = [event for event in run["scripted_input_schedule"] if event["start"] <= menu]
    shifted = menu + 150
    holds = [shifted + 230 * step for step in range(1, length + 1)]
    actions = [(menu + 1, "DOWN"), (shifted + 1, "A"), *((frame + 1, "A") for frame in holds[:-1])]
    controls += [dict(start=frame, buttons=[button], duration=8) for frame, button in actions]
    captures = [3500, 5800, 9700, menu, shifted, *holds]
    donor = run["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    return dict(source=reference(source), donor=reference(donor["source"]), controls=controls,
                captures=captures, menu=menu, selected=shifted, holds=holds)


def replay(branch):
    release = read(current.RELEASE)
    assert digest(current.ROM) == release["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"]
    spec = plan(branch, release)
    folder = ROOT / branch
    folder.mkdir(parents=True)
    manifest, schedule = folder / "replay_plan.json", folder / "inputs.json"
    write(manifest, spec)
    write(schedule, spec["controls"])
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(current.ROM), "--out", str(folder / "capture"),
                    "--frames", str(spec["captures"][-1]), "--inputs-json", str(schedule),
                    "--press-start", "-1", "--touchscreen", "--battery-save", spec["donor"]["path"],
                    "--capture-every", "999999", "--capture-at", *map(str, spec["captures"])]
        harness.main()
    finally:
        sys.argv = argv
    assert reference(spec["donor"]["path"]) == spec["donor"]


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("branch", choices=CASES)
    replay(cli.parse_args().branch)
