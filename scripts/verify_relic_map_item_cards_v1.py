"""Verify the four proof and map categories in the original Items menu."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from scripts import replay_relic_map_item_cards_v2 as replay
from scripts import verify_figurehead_navigation_gift_cards_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
PREDECESSOR = replay.parent.ROOT
LIVE = ROOT / 'relic_map_items_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/relic_map_item_cards_repo_qa_20261111.xml')
OBSERVED = [2815 + ident for ident in replay.FIXTURE_ITEMS]
EXPECTED = [(151, 8, 'Rigveda'), (155, 9, 'Thales Paper Map'),
            (162, 10, 'Stone Circle Map'), (174, 6, 'Old Parchment')]
source = checked_text(inspect.getsource(previous.verify_live), {
    """    assert [(row['item_id'], row['category'], row['name']) for row in inventory['items']] == [
        (114, 5, 'Eagle Figurehead'), (127, 7, 'Frozen Rose')]""":
        """    assert [(row['item_id'], row['category'], row['name'].strip())
                  for row in inventory['items']] == EXPECTED""",
    '== 11600': '== replay.TOWN',
    'shots[11600]': 'shots[replay.TOWN]',
    'shots[11200]': 'shots[replay.BACK_MENU]',
    'navigation_fixture=inventory, original_sextant_already_held=True,': 'inventory_fixture=inventory,',
    'complete Eagle Figurehead, Sextant and Frozen Rose cards': 'complete Rigveda, Thales Paper Map, Stone Circle Map and Old Parchment cards',
})
env = previous.env | vars(previous) | globals()
exec(compile(source, __file__ + '::original-proof-and-map-display', 'exec'), env)
verify_live = env['verify_live']
verify_startup = FunctionType(previous.verify_startup.__code__, env)
approve = FunctionType(previous.approve.__code__, env)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    else:
        (verify_live if args.action == 'live' else verify_startup)()
