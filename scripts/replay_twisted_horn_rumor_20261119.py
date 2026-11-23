"""Replay the recorded Lisbon Guild visit with the staged Twisted Horn rumor."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_departure_numerals_20261119 as previous
from scripts import stage_twisted_horn_rumor_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base = stage.base
SOURCE = previous.SOURCE
CAPTURE = stage.ROOT / 'ordinary_lisbon'
INPUT = stage.ROOT / 'ordinary_inputs.json'
STARTUP_DIR = stage.ROOT / 'own_startup'
STARTUP = stage.ROOT / 'own_startup_verification.json'
FRAMES = (55540, 55780, 56260, 56500, 56740, 56980, 57220, 57460, 58660)
END = FRAMES[-1] + 1


def capture():
    recipe = checked_text(getsource(previous.capture), {
        "    assert previous['predecessor']['candidate_sha256'] == prior_hash":
            "    earlier = base.load(stage.parent.parent.RELEASE)\n"
            "    sailing = base.load(stage.parent.parent.parent.RELEASE)\n"
            "    assert previous['predecessor']['candidate_sha256'] == earlier['candidate_sha256']\n"
            "    assert earlier['predecessor']['candidate_sha256'] == sailing['candidate_sha256']\n"
            "    assert sailing['predecessor']['candidate_sha256'] == prior_hash",
    })
    scope = vars(previous) | globals()
    exec(compile(recipe, __file__ + '::recorded-visit', 'exec'), scope)
    scope['capture']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('capture', 'capture-startup', 'startup', 'patch'))
    action = parser.parse_args().action
    precedent = previous.precedent
    adapted = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, STAGED=stage.ROOT, parent=stage.parent)
    scope = vars(precedent) | dict(stage=adapted, STARTUP=STARTUP, STARTUP_DIR=STARTUP_DIR)
    if action == 'capture':
        capture()
    elif action == 'patch':
        FunctionType(precedent.patch.__code__, scope)()
    else:
        FunctionType(precedent.startup.__code__, scope)(action == 'capture-startup')
