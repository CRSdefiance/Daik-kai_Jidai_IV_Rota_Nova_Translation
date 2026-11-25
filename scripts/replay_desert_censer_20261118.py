"""Sample the censer conversation and its pauses, plus the desert injury notice."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_rafael_mosque_20261118 as replay
from scripts import stage_desert_censer_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / "censer_v2"
ROM = ROOT / "Rafael_Censer_RESEARCH_ONLY.nds"
SETUP, LIVE = ROOT / "fixture.json", ROOT / "verified.json"
LAST = 8301
EXCERPTS = (
    (329, (142, 170, 212, 219)),
    (330, (6, 10, 14, 19, 28, 33, 37, 41, 45)),
    (331, (6, 10, 14, 18, 22, 26)),
)

scope = replay.scope | globals()
audit = checked_text(replay.audit, {
    "    observed, cursor = [], 3650": "    observed, cursor, previous_plane = [], 3650, None",
    "            n = next((n for n, bits in masks": """            if wanted == previous_plane:
                cursor = next(action["start"] + 25 for action in report["scripted_input_schedule"]
                              if action["start"] > cursor and action["buttons"] == ["A"])
            previous_plane = wanted
            n = next((n for n, bits in masks""",
})
for source, label in ((replay.prep, "exact-original-commands"), (audit, "native-body-pixels")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)
capture = FunctionType(replay.capture.__code__, scope)
startup = FunctionType(replay.startup.__code__, scope)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    actions = {"prepare": scope["prepare"], "capture": capture, "verify": scope["verify"], "startup": startup}
    actions[parser.parse_args().action]()
