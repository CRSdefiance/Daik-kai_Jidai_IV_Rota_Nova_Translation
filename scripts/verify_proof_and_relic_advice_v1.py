"""Seal the native layout review and verify the original Advice transitions."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import replay_proof_and_relic_advice_v1 as replay
from scripts import verify_item_production_advice_v1 as offline
from scripts import verify_weapon_armor_advice_v1 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_approval.json'
LIVE = ROOT / 'proof_and_relic_advice_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/proof_and_relic_advice_repo_qa_20261111.xml')
CASES = replay.CASES
OBSERVED = tuple(row[0] for row in CASES)
REFERENCE = Path('releases/all_routes_editorial_20261111_relic_map_item_cards_candidate'
                 '/verification/relic_map_items_gameplay_verification.json')


def verify_startup():
    FunctionType(offline.verify_startup.__code__, vars(offline) | globals())()


def approve_layout(viewed):
    code = checked_text(getsource(offline.approve_layout), {
        "len(proof['native_display_cases']) == 48": "len(proof['native_display_cases']) == 140",
        "len(proof['native_original_copies']) == 24": "len(proof['native_original_copies']) == 70",
        "len(manuscript['native_context']['offline_native_selector_cases']) == 144":
            "len(manuscript['native_context']['offline_native_selector_cases']) == 420",
        "proof['sheets']) == 24": "proof['sheets']) == 70",
        'full_native_planes_directly_reviewed=24': 'full_native_planes_directly_reviewed=70',
        'original_offline_loader_copies=24': 'original_offline_loader_copies=70',
        'original_offline_portrait_cases=48': 'original_offline_portrait_cases=140',
        'original_offline_caller_fragments=144': 'original_offline_caller_fragments=420',
        'two or three body rows': 'one to four body rows',
        'Approved all 24 native layouts': 'Approved all 70 native layouts',
    })
    env = vars(offline) | globals()
    exec(compile(code, __file__ + '::approved-proof-and-relic-layouts', 'exec'), env)
    env['approve_layout'](viewed)


def item_fields(font, image, number):
    earlier = stage.load(REFERENCE)
    assert earlier['original_Items_screen'] and earlier['complete_description_foreground_and_blank_cells_exact']
    card = earlier['observed'][str(number - 218)]
    frame, = card['capture_frames']
    title = next(row for row in card['title_role_effect_and_description_fields']
                 if row['native_source_origin'] == [48, 0] and row['frame'] == frame['frame'])
    x, y = title['destination']
    width, height = title['size']
    assert [x, y, width, height] == [56, 24, 144, 12]
    crop = (x, y, x + width, y + height)
    expected = precedent.portrait.captured(frame).crop(crop)
    assert image.crop(crop).tobytes() == expected.tobytes()
    names = dict(zip((3184, 3188, 3195, 3207), replay.ITEM_NAMES, strict=True))
    fields = [dict(text=names[number], crop=crop, exact_registered_card_title=title,
                   reference=str(REFERENCE), reference_sha256=stage.digest(REFERENCE), exact_reference_capture=frame)]
    if number == 3188:
        fields.append(precedent.find_mask(font, 'Advice', image, (113, 365, 171, 384)))
        fields.append(precedent.find_mask(font, 'Use', image, (171, 365, 211, 384)))
    else:
        fields.append(precedent.find_mask(font, 'Advice', image, (152, 365, 209, 384)))
    return fields


def verify_live():
    code = checked_text(getsource(precedent.verify_live), {
        'sha, 11800': 'sha, replay.TOWN',
        "(24, 2, 'Black Rapier', 0), (72, 3, 'Charles Martel Armor', 0),":
            "(151, 8, 'Rigveda', 0), (155, 9, 'Thales Paper Map', 0),\n"
            "        (162, 10, 'Stone Circle Map', 0), (174, 6, 'Old Parchment', 0),",
        '((3057, 1, 9600, 9900, 10200), (3105, 4, 10400, 10700, 11000))': 'CASES',
        "footer = find_mask(font, 'Advice', returned, (152, 365, 209, 384))":
            'footer = item_fields(font, returned, message)',
        '(8400, 11800)': '(8400, replay.TOWN)',
        'stored_cases=50, viewed_pages=50': 'stored_cases=70, viewed_pages=70',
        'Verified the one-row weapon and four-row armor Advice portraits and exact Items/Lisbon returns.':
            'Verified four original Proof and map Advice paths and the exact Items and Lisbon returns.',
    })
    env = vars(precedent) | globals()
    exec(compile(code, __file__ + '::proof-and-map-advice-gameplay', 'exec'), env)
    env['verify_live']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'live'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        (verify_startup if args.action == 'startup' else verify_live)()
