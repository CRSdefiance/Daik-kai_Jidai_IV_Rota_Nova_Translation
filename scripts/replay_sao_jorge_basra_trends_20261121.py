"""Replay the original Sao Jorge and Basra commands using Lil's opening prelude."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_seville_stockholm_trends_20261121 as precedent
from scripts import sao_jorge_basra_trends_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "emulator"
CASES = {"sao_jorge": (179, 14), "basra": (183, 25)}
LIVE, SHEET = ROOT / "gameplay.json", ROOT / "comparison.png"
build = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, ROOT=stage.ROOT, parent=stage.parent,
                        review=SimpleNamespace(OUTPUT=stage.OUTPUT))
offline = SimpleNamespace(PROOF=stage.NATIVE_PROOF)
REPLAY_SUFFIX = ""
env = vars(precedent) | {name: globals()[name] for name in (
    "ROOT", "CASES", "LIVE", "SHEET", "build", "offline", "REPLAY_SUFFIX",
)}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "verify", "startup", *CASES))
    parser.add_argument("side", nargs="?", choices=("before", "after"))
    args = parser.parse_args()
    if args.action == "startup":
        run = precedent.precedent.startup
        FunctionType(run.__code__, run.__globals__ | {"build": build})()
    elif args.action == "verify":
        program = checked_text(getsource(precedent.verify), {"All 18 Lil": "All 39 Lil"})
        exec(compile(program, __file__ + "::complete-exchanges", "exec"), env)
        env["verify"]()
    elif args.action == "prepare":
        FunctionType(precedent.prepare.__code__, env)()
    else:
        FunctionType(precedent.capture.__code__, env)(args.action, args.side)
