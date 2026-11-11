"""Exercise Advice on a Proof, completed map, ruin map and map material."""

from inspect import getsource
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_item_production_advice_v1 as previous
from scripts import stage_proof_and_relic_advice_v2 as candidate
from scripts.source_locked_derivation_v5118 import checked_text


first = candidate.first
stage = SimpleNamespace(**(vars(first.base) | vars(candidate) | {
    'PREP': candidate.PROOF, 'RELEASE': first.parent.RELEASE,
    'ARM': first.editorial.previous.ARM, 'review': first.editorial.previous,
}))
PRIOR = first.parent.TEST.parent / 'figurehead_navigation_gift_advice_staged_20261111_v2' / 'own_startup'
STARTUP, ITEMS = stage.ROOT / 'own_startup', stage.ROOT / 'items_advice_second_row'
ITEM_IDS = (151, 155, 162, 174)
ITEM_NAMES = ('Rigveda', 'Thales Paper Map', 'Stone Circle Map', 'Old Parchment')
CASES = ((3207, 4, 10200, 10500, 10800), (3184, 1, 11100, 11400, 11700),
         (3188, 2, 12000, 12300, 12600), (3195, 1, 13200, 13500, 13800))
TOWN = 14600
COMMANDS = (
    dict(until=8800, inventory_items=list(ITEM_IDS), buttons=['X'], duration=8),
    dict(until=9200, touch=[143, 54], duration=8),
    dict(until=9600, buttons=['A'], duration=8),
    dict(until=9900, buttons=['RIGHT'], duration=8),
    dict(until=10200, buttons=['RIGHT'], duration=8),
    dict(until=10500, buttons=['X'], duration=8),
    dict(until=10800, buttons=['A'], duration=8),
    dict(until=11100, buttons=['RIGHT'], duration=8),
    dict(until=11400, buttons=['X'], duration=8),
    dict(until=11700, buttons=['A'], duration=8),
    dict(until=12000, buttons=['RIGHT'], duration=8),
    dict(until=12300, buttons=['X'], duration=8),
    dict(until=12600, buttons=['A'], duration=8),
    dict(until=12900, buttons=['RIGHT'], duration=8),
    dict(until=13200, buttons=['DOWN'], duration=8),
    dict(until=13500, buttons=['X'], duration=8),
    dict(until=13800, buttons=['A'], duration=8),
    dict(until=14200, buttons=['B'], duration=8),
    dict(until=TOWN, buttons=['B'], duration=8),
    dict(stop=True),
)


def run(action):
    env = vars(previous) | globals()
    if action == 'startup':
        FunctionType(previous.cold_boot.__code__, env)()
        return
    code = checked_text(getsource(previous.replay), {
        "'category not in (2, 3, 4)': 'category != 0'": "'category not in (2, 3, 4)': 'category not in (6, 8, 9, 10)'",
        'item_ids == [ITEM]': 'item_ids == list(ITEM_IDS)',
        "receipt['items'][0]['name'] == 'Baby Shark'":
            "tuple(row['name'] for row in receipt['items']) == ITEM_NAMES",
        "'--frames', '11001'": "'--frames', str(TOWN + 1)",
        "'--capture-at', '9700', '9800', '9900', '--dump-capture-ram'":
            "'--capture-at', *(str(row[3]) for row in CASES), '--dump-capture-ram'",
    })
    exec(compile(code, __file__ + '::original-proof-and-map-advice-inputs', 'exec'), env)
    env['replay']()


if __name__ == '__main__':
    assert sys.argv[1:] in (['items'], ['startup'])
    run(sys.argv[1])
