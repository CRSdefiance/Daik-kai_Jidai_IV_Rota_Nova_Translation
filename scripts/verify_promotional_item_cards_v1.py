"""Verify the selected promotional relic and generated fragment in Lisbon Items."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from scripts import replay_promotional_item_cards_v1 as replay
from scripts import verify_figurehead_navigation_gift_cards_v1 as previous
from scripts.probe_promotional_item_full import verify as initialize
from scripts.source_locked_derivation_v5118 import checked_text

stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
PREDECESSOR = replay.parent.ROOT
LIVE = ROOT / 'promotional_items_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/promotional_item_cards_repo_qa_20261111.xml')
OBSERVED = [2815 + ident for ident in replay.FIXTURE_ITEMS]


def seed_for_title(arm, ident, title):
    for seed in range(128):
        case = initialize(arm, seed)
        if case['names'][ident - 188]['name'] == title:
            return seed
    raise AssertionError(f'No native initializer case for the observed slot and title {ident}, {title!r}')


source = checked_text(inspect.getsource(previous.verify_live), {
    """    assert [(row['item_id'], row['category'], row['name']) for row in inventory['items']] == [
        (114, 5, 'Eagle Figurehead'), (127, 7, 'Frozen Rose')]""": """    assert [(row['item_id'], row['category']) for row in inventory['items']] == [(194, 4), (198, 12)]
    live_titles = {row['item_id']: row['name'] for row in inventory['items']}
    assert live_titles[194] == 'Witch Idol' and live_titles[198].endswith('Map 1')""",
    """        native = execute(arm, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                         kanji_font=font, mode=4, item_resource_index=ident, item_common=common)
        case, = [row for row in proof['item_cases']
                 if (row['message_ID'], row['page'], row['mode']) == (number, 'main', 4)]
        assert stage.sha256(native['pixels']).hexdigest() == case['native_ink_sha256']""": """        seed = seed_for_title(arm, ident, live_titles[ident])
        native = execute(arm, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                         kanji_font=font, mode=4, item_resource_index=ident, item_common=common,
                         item_promotional_seed=seed)
        expected, _ = stage.oracle()
        assert native['pixels'] == expected(arm, font, native['glyph_events'], 4, background=0)
        case = next(row for row in proof['item_cases']
                    if (row['message_ID'], row['page'], row['mode']) == (number, 'main', 4))
        assert native['item_actual_common_ids'] == [number]
        assert [row['text'] for row in native['item_draws'] if 36 <= row['y'] < 84] == case['lines']""",
    "capture_frames=[shots[n] for n, _ in title_matches], lines=case['lines']": """capture_frames=[shots[n] for n, _ in title_matches], lines=case['lines'],
                                title=live_titles[ident], matching_native_initializer_seed=seed""",
    'navigation_fixture=inventory, original_sextant_already_held=True,': 'inventory_fixture=inventory,',
    'complete Eagle Figurehead, Sextant and Frozen Rose cards': 'complete promotional relic and generated map-fragment cards',
})
env = previous.env | vars(previous) | globals()
exec(compile(source, __file__ + '::native-promotional-card-display', 'exec'), env)
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
