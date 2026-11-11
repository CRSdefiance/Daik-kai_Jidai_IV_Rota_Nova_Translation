"""Replay Advice on a mounted tool, a figurehead and a regional gift."""

from inspect import getsource
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_item_production_advice_v1 as previous
from scripts import stage_figurehead_navigation_gift_advice_v2 as candidate
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(candidate.first.base) | vars(candidate) | {
    'PREP': candidate.PROOF,
    'RELEASE': candidate.first.parent.RELEASE,
    'ARM': candidate.first.editorial.previous.ARM,
    'review': candidate.first.editorial.previous,
}))
PRIOR = candidate.first.parent.TEST.parent / 'crew_equipment_advice_staged_20261111_v2' / 'own_startup'
STARTUP = stage.ROOT / 'own_startup'
ITEMS = stage.ROOT / 'items_advice'
ITEM_IDS = (114, 127)
ITEM_NAMES = ('Eagle Figurehead', 'Frozen Rose')
COMMANDS = (
    dict(until=8800, inventory_items=list(ITEM_IDS), buttons=['X'], duration=8),
    dict(until=9200, touch=[143, 54], duration=8),
    dict(until=9600, buttons=['A'], duration=8),
    dict(until=9900, buttons=['X'], duration=8),
    dict(until=10200, buttons=['A'], duration=8),
    dict(until=10500, buttons=['RIGHT'], duration=8),
    dict(until=10800, buttons=['RIGHT'], duration=8),
    dict(until=11100, buttons=['X'], duration=8),
    dict(until=11400, buttons=['A'], duration=8),
    dict(until=11700, buttons=['RIGHT'], duration=8),
    dict(until=12000, buttons=['X'], duration=8),
    dict(until=12300, buttons=['A'], duration=8),
    dict(until=12700, buttons=['B'], duration=8),
    dict(until=13100, buttons=['B'], duration=8),
    dict(stop=True),
)


def run(action):
    env = vars(previous) | globals()
    if action == 'startup':
        FunctionType(previous.cold_boot.__code__, env)()
        return
    code = checked_text(getsource(previous.replay), {
        "'category not in (2, 3, 4)': 'category != 0'": "'category not in (2, 3, 4)': 'category not in (5, 7)'",
        'item_ids == [ITEM]': 'item_ids == list(ITEM_IDS)',
        "receipt['items'][0]['name'] == 'Baby Shark'":
            "tuple(row['name'] for row in receipt['items']) == ITEM_NAMES",
        "'--frames', '11001'": "'--frames', '13101'",
        "'--capture-at', '9700', '9800', '9900', '--dump-capture-ram'":
            "'--capture-at', '9900', '11100', '12000', '--dump-capture-ram'",
    })
    exec(compile(code, __file__ + '::three-catalogue-advice-paths', 'exec'), env)
    env['replay']()


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    run(sys.argv[1])
