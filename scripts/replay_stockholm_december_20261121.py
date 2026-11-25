"""Replay an ordinary voyage to Stockholm on the cumulative candidate."""
from argparse import ArgumentParser
from pathlib import Path
import sys

from scripts import register_athens_london_trends_20261121 as active
from scripts import replay_town_trends_saved_game_20261121 as precedent


base, harness = precedent.base, precedent.harness
ROOT = Path("out/stockholm_december_gameplay_20261121")
HISTORY = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
DEPARTURES = {
    "london": (HISTORY / "condition_rumor_v774_london_pilot_v773/capture_report.json", 3760, 2801),
    "riga": (HISTORY / "auto_move_riga_v399/capture_report.json", 8000, 7601),
}


def main(root, departure):
    release = base.load(active.RELEASE)
    assert base.digest(active.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    source, first, last_input = DEPARTURES[departure]
    original = base.load(source)
    donor = original["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    inputs = [row for row in original["scripted_input_schedule"] if row["start"] <= last_input]
    assert [row["buttons"] for row in inputs[:4]] == [["START"], ["A"], ["A"], ["A"]]
    root.mkdir(parents=True)
    base.save(root / "source_save.json", dict(source_capture=str(source), source_capture_sha256=base.digest(source),
        donor=donor["source"], sha256=donor["source_sha256"], working_ROM_sha256=release["candidate_sha256"]))
    plan, controls = root / "inputs.json", root / "navigation.jsonl"
    base.save(plan, inputs)
    controls.touch(exist_ok=False)
    stream = precedent.common.GrowingCommands(controls)
    argv, stdin = sys.argv, sys.stdin
    try:
        sys.stdin = stream
        sys.argv = [harness.__file__, "--rom", str(active.ROM), "--out", str(root / "capture"),
            "--frames", "145000", "--inputs-json", str(plan), "--battery-save", donor["source"],
            "--press-start", "-1", "--touchscreen", "--capture-every", "999999", "--pause-at", str(first), "--dump-ram"]
        harness.main()
    finally:
        sys.argv, sys.stdin = argv, stdin
        stream.close()
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument("--departure", choices=DEPARTURES, default="london")
    args = parser.parse_args()
    main(args.out, args.departure)
