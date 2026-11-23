"""Open the London Market Info report from the ordinary Hodram battery save."""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
import sys

from scripts import stage_market_english_region_20261120 as stage


HISTORY = Path("work/emulation_v193/condition_rumor_v774_london_pilot_v773/capture_report.json")
FRAMES = (3400, 3800, 4200, 4600, 5000, 5400, 5800, 6200, 6300, 6600)
MARKET_INPUTS = [(3601, "A"), (4001, "A"), (4401, "DOWN"), (4801, "DOWN"), (5201, "A"),
                 (5601, "A"), (6001, "A"), (6201, "A"), (6401, "B")]


def replay(revised, output, plan):
    history = stage.base.load(HISTORY)
    donor = history["battery_save_preloaded"]
    assert stage.base.digest(donor["source"]) == donor["source_sha256"]
    staged = stage.base.load(stage.PROOF)
    rom = stage.ROM if revised else stage.parent.ROM
    assert stage.base.digest(rom) == staged["candidate_sha256" if revised else "parent_sha256"]
    inputs = [row for row in history["scripted_input_schedule"] if row["start"] < 3201]
    if plan is None:
        inputs.append(dict(start=3201, duration=8, buttons=[], touch=[25, 30]))
        inputs.extend(dict(start=frame, duration=8, buttons=[button]) for frame, button in MARKET_INPUTS)
    else:
        inputs.extend(stage.base.load(plan))
    output.mkdir(parents=True)
    schedule = output / "inputs.json"
    stage.base.save(schedule, inputs)
    run([sys.executable, "-B", "-m", "scripts.headless_desmume_v193",
         "--rom", str(rom), "--out", str(output / "capture"),
         "--frames", str(FRAMES[-1] + 1), "--capture-every", "999999",
         "--capture-at", *map(str, FRAMES), "--inputs-json", str(schedule),
         "--dump-capture-ram", "--touchscreen", "--press-start", "-1",
         "--battery-save", donor["source"]], check=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--revised", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--plan", type=Path)
    args = parser.parse_args()
    replay(args.revised, args.out, args.plan)
