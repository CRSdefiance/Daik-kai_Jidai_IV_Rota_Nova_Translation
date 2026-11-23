"""Replay Sofala, Malacca and Osaka through the original Lil scene commands."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_seville_stockholm_trends_20261121 as precedent
from scripts import sofala_malacca_osaka_trends_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
VALIDATION = Path("out/sofala_malacca_osaka_validation_20261121_v2")
ROOT = VALIDATION / "emulator"
PRIOR_BEFORE = stage.WORK / "research_v1/emulator"
CASES = {"sofala": (184, 9), "malacca": (187, 16), "osaka": (188, 11)}
LIVE, SHEET = ROOT / "gameplay.json", ROOT / "comparison.png"
build = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, ROOT=VALIDATION, parent=stage.parent,
                        review=SimpleNamespace(OUTPUT=stage.OUTPUT))
offline = SimpleNamespace(PROOF=stage.NATIVE_PROOF)
REPLAY_SUFFIX = ""
env = vars(precedent) | {name: globals()[name] for name in (
    "ROOT", "PRIOR_BEFORE", "CASES", "LIVE", "SHEET", "build", "offline", "REPLAY_SUFFIX",
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
        program = checked_text(getsource(precedent.verify), {
            "All 18 Lil": "All 36 Lil",
            'path = folder / (side + REPLAY_SUFFIX) / "capture_report.json"':
                'path = (PRIOR_BEFORE / name if side == "before" else folder) / side / "capture_report.json"',
        })
        exec(compile(program, __file__ + "::complete-exchanges", "exec"), env)
        env["verify"]()
    elif args.action == "prepare":
        program = checked_text(getsource(precedent.prepare), {
            '            image.save(target)':
                '            if side == "before":\n'
                '                target = PRIOR_BEFORE / name / target.name\n'
                '                assert target.read_bytes() == bytes(image.rom.save())\n'
                '            else:\n'
                '                image.save(target)',
        })
        exec(compile(program, __file__ + "::preserve-complete-baselines", "exec"), env)
        env["prepare"]()
    else:
        FunctionType(precedent.capture.__code__, env)(args.action, args.side)
