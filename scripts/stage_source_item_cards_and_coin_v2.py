"""Stage the source-item review in the existing runtime allocation."""

import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch import source_item_cards_and_coin_v2 as patch
from scripts import stage_source_item_cards_and_coin_v1 as initial
from scripts import verify_source_item_cards_offline_v2 as offline_model
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = initial.ROOT.with_name('source_item_cards_and_coin_staged_20261111_v2')
ROM, PREP, PROOF = (ROOT / p.name for p in (initial.ROM, initial.PREP, initial.PROOF))
OUTPUT, ITEM_PLAN = initial.OUTPUT, initial.ITEM_PLAN
AMENDMENTS = initial.AMENDMENTS
active_rows = initial.active_rows


def build(arm, common, rows):
    return FunctionType(initial.build.__code__, vars(initial) | {'patch': patch})(arm, common, rows)


def stage():
    source = checked_text(inspect.getsource(initial.stage), {
        'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(initial.__file__), initial.PREP, Path(__file__)',
    })
    env = vars(initial) | globals()
    exec(compile(source, __file__ + '::same-stored-inverse-fixed-item-payload', 'exec'), env)
    env['stage']()


def offline():
    source = checked_text(inspect.getsource(initial.offline), {
        'Path(make_execute.__code__.co_filename))':
            'Path(make_execute.__code__.co_filename), Path(offline_model.__file__), Path(__file__))',
    })
    env = vars(initial) | globals()
    env['sheets'] = FunctionType(initial.sheets.__code__, env)
    env['parent_crops'] = FunctionType(offline_model.parent_crops.__code__,
                                      vars(offline_model) | {'stage': __import__(__name__, fromlist=['ROOT'])})
    env['NdsImage'] = initial.NdsImage
    exec(compile(source, __file__ + '::same-native-display-fixed-item-payload', 'exec'), env)
    env['offline']()


if __name__ == '__main__':
    import sys
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()

