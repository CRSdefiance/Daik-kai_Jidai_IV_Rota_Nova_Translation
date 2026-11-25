"""Check the execution-scene edits in an initialized Hodram play sequence."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_moonlit_violin_20261121 as prior
from scripts import verify_hodram_execution_20261121 as offline
from scripts.source_locked_derivation_v5118 import checked_text


build = offline.build
ROOT = build.ROOT / "playback"
PROOF = ROOT / "verified.json"
CONFIG = {"hodram": (1, 42, 42, 40, (15, 19, 27, 58, 65, 76, 79, 82, 116, 125, 129))}
scope = vars(prior) | globals()
actions = {action: FunctionType(getattr(prior, action).__code__, scope)
           for action in ("prepare", "capture")}
exec(compile(checked_text(getsource(prior.verify), {
    "across Rafael and Hodram": "in Hodram's route",
}), __file__, "exec"), scope)
actions["verify"] = scope["verify"]


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=tuple(actions))
    action = cli.parse_args().action
    if action == "verify":
        actions[action]()
    else:
        actions[action]("hodram")
