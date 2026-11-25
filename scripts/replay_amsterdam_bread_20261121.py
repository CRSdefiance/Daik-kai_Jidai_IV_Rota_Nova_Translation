"""Visit the Amsterdam bread scene on the registered ROM using ordinary inputs."""

import argparse
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import observe_amsterdam_square_current_20261114 as town
from scripts.run_activity_special_live_v989 import GrowingCommands
from scripts import register_hodram_execution_20261121 as active


base = active.parent.base
ROOT = Path("work/amsterdam_bread_gameplay_20261121")
END = 16900


def button(n, key):
    return dict(start=n, duration=12, buttons=[key])


def touch(n, x, y):
    return dict(start=n, duration=8, buttons=[], touch=[x, y])


def schedule(navigate=False):
    old, _, _, _, _ = town.schedule("square")
    prefix = [row for row in old if row["start"] <= 1800]
    edit = [
        button(2001, "B"), button(2401, "Y"), touch(2801, 137, 122), button(3201, "A"),
        touch(3601, 44, 77), button(4001, "A"), button(4401, "X"), button(4801, "A"), button(5201, "A"),
    ]
    # Replay the opening speech advances after accepting the birthday.
    offset = 3000
    opening = [row | {"start": row["start"] + offset} for row in old if 2500 <= row["start"] <= 8701]
    square = [button(11751, "B")]
    if navigate:
        return prefix + edit + opening + square
    square.append(touch(12151, 180, 29))
    event = [button(n, "A") for n in range(12501, END - 140, 290)]
    return prefix + edit + opening + square + event


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument("--navigate", action="store_true")
    args = parser.parse_args()
    assert not args.out.exists()
    release = base.load(active.RELEASE)
    assert base.digest(active.ROM) == release["candidate_sha256"]
    args.out.mkdir()
    inputs = args.out / "inputs.json"
    base.save(inputs, schedule(args.navigate))
    frames = [3400, 3800, 4550, 5100, 11590, 11960, 12380, *range(12720, END, 290)]
    sys.argv = [harness.__file__, "--rom", str(active.ROM), "--out", str(args.out / "capture"),
                "--frames", str(END), "--inputs-json", str(inputs), "--touchscreen", "--dump-ram",
                "--capture-every", "999999", "--capture-at", *map(str, frames)]
    if not args.navigate:
        harness.main()
        return
    journal = args.out / "navigation.jsonl"
    journal.touch(exist_ok=False)
    events = GrowingCommands(journal)
    sys.argv.extend(["--pause-at", "11960"])
    try:
        sys.stdin = events
        harness.main()
    finally:
        events.close()


if __name__ == "__main__":
    main()

