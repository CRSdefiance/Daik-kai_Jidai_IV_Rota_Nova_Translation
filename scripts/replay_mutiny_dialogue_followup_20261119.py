"""Replay the shared mutiny incident and select Quell Mutiny on the original menu."""

import argparse
from inspect import getsource
import json
from types import FunctionType

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import replay_sea_event_dialogue_followup_20261118 as ancestor
from scripts import run_mutiny_replay_v1 as historical
from scripts import stage_mutiny_dialogue_followup_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base = stage.base
OUT = stage.ROOT / "quell"
STARTUP = stage.ROOT / "startup_fixture"
set_condition = FunctionType(historical.set_condition.__code__, vars(historical) | {"ROM": stage.ROM})


def patch():
    delta, rebuilt = stage.ROOT / "clean_input.xdelta", stage.ROOT / "clean_rebuilt.nds"
    assert not delta.exists() and not rebuilt.exists()
    make_xdelta(stage.CLEAN, stage.ROM, delta)
    apply_xdelta(stage.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == stage.ROM.read_bytes()
    print(base.digest(rebuilt))


def startup():
    run = FunctionType(ancestor.startup.__code__, vars(ancestor) | dict(stage=stage, STARTUP=STARTUP))
    run()


def gameplay():
    path = historical.OUT / "commands.jsonl"
    old = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    prefix = [row for row in old if row.get("until", 14000) <= 10027]
    assert len(prefix) == 5 and prefix[-1] == dict(until=10027, buttons=["A"], duration=8)
    tail = [dict(until=10127)] + [dict(until=n, buttons=["A"], duration=8) for n in range(10327, 11528, 200)]
    schedule = [*prefix, *tail, dict(stop=True)]
    original = getsource(historical.main)
    start = original.index("    schedule = [")
    end = original.index("    commands.write_text", start)
    source = checked_text(original, {
        "['research_ROM_sha256']": "['candidate_sha256']",
        original[start:end]: "    schedule = QUELL_SCHEDULE\n",
        "'from scripts.run_mutiny_replay_v1 import set_condition'":
        "'from scripts.replay_mutiny_dialogue_followup_20261119 import set_condition'",
    })
    env = vars(historical) | dict(ROM=stage.ROM, PROOF=stage.PROOF, OUT=OUT, QUELL_SCHEDULE=schedule)
    exec(compile(source, __file__ + "::quell", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("patch", "startup", "gameplay"))
    globals()[parser.parse_args().action]()

