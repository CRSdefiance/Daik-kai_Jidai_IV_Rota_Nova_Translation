"""Bind the clean patch and initialize the original Rafael name processor."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import headless_desmume_v193 as harness
from scripts import replay_london_guild_assignments_20261118 as prior
from scripts import stage_papal_states_titis_20261118 as build

base = build.base


def patch():
    clean, delta, rebuilt = Path("work/clean.nds"), build.ROOT / "translation.xdelta", build.ROOT / "clean_rebuilt.nds"
    assert not delta.exists() and not rebuilt.exists()
    make_xdelta(clean, build.ROM, delta)
    apply_xdelta(clean, delta, rebuilt)
    assert rebuilt.read_bytes() == build.ROM.read_bytes()
    print(f"Exact clean-input reconstruction: {base.digest(rebuilt)}")


def snapshot():
    root = build.ROOT / "rafael_snapshot"
    inputs = build.ROOT / "rafael_snapshot_inputs.json"
    assert not root.exists()
    base.save(inputs, base.load(prior.precedent.stage.CAPTURE)["scripted_input_schedule"])
    sys.argv = [sys.argv[0], "--rom", str(build.ROM), "--out", str(root),
                "--frames", "3901", "--inputs-json", str(inputs), "--capture-every",
                "999999", "--capture-at", "3900", "--dump-capture-ram"]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "snapshot"))
    globals()[parser.parse_args().action]()
