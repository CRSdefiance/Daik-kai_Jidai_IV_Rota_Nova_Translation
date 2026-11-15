"""Verify the armor layouts, the native Lisbon Items return and cold startup."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from scripts import replay_armor_item_cards_v1 as replay
from scripts import verify_utility_weapon_item_cards_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
PREDECESSOR = replay.parent.ROOT
LIVE = ROOT / 'armor_items_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/armor_item_cards_repo_qa_20261111.xml')
OBSERVED = [replay.ITEM + 2815]

env = vars(previous) | globals()
live_source = checked_text(inspect.getsource(previous.verify_live), {
    "replay.earlier.ITEM and item['name'] == 'Black Rapier' and item['category'] == 2":
        "replay.ITEM and item['name'] == 'Charles Martel Armor' and item['category'] == 3",
    'replay.earlier.MENU_FRAMES': 'replay.previous.MENU_FRAMES',
    'complete relocated Black Rapier card': 'complete relocated Charles Martel Armor card',
})
exec(compile(live_source, __file__ + '::original-native-armor-card', 'exec'), env)
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
