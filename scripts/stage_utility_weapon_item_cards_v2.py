"""Reflow the phrases identified during the first contact-sheet review."""

import inspect
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import stage_utility_weapon_item_cards_v1 as initial
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = initial.ROOT.with_name('utility_weapon_item_cards_staged_20261111_v2')
ROM = ROOT / initial.ROM.name
PREP = ROOT / initial.PREP.name
PROOF = ROOT / initial.PROOF.name
EXTRA_PHRASES = (
    'a tiny dose', 'the mark of a hero', 'no known reason', "a close ally's life",
    'Aztec water god', 'this superb greatsword', 'god of war', 'tremendous force',
)
AMENDMENTS = initial.AMENDMENTS | {
    2838: ('The recipe comes from Hua Tuo, a famed physician of China’s Three Kingdoms era. They say a tiny dose cures any contagious disease.',
           'Attribute the remedy’s recipe to the renowned physician and the efficacy claim to the game’s tradition. Keep the small dose together.'),
}
compiler = initial.patch.compile_item
compile_item = FunctionType(compiler.__code__, compiler.__globals__ | {
    'PROTECTED_PHRASES': compiler.__globals__['PROTECTED_PHRASES'] + EXTRA_PHRASES,
})
transform = FunctionType(initial.patch.transform.__code__, vars(initial.patch) | {'compile_item': compile_item})
patch = SimpleNamespace(**(vars(initial.patch) | {'transform': transform}))
env = vars(initial) | globals()
active_rows = FunctionType(initial.active_rows.__code__, env)
build = FunctionType(initial.build.__code__, env | {'active_rows': active_rows})
context = env | {'active_rows': active_rows, 'build': build}
stage_source = checked_text(inspect.getsource(initial.stage), {
    'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(initial.__file__), Path(__file__)',
})
exec(compile(stage_source, __file__ + '::final-phrase-layout', 'exec'), context)
stage = context['stage']
offline = FunctionType(initial.offline.__code__, context)


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
