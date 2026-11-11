"""Verify all Advice layouts and the three original Items contexts."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import replay_figurehead_navigation_gift_advice_v1 as replay
from scripts import verify_item_production_advice_v1 as offline
from scripts import verify_weapon_armor_advice_v1 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT = ROOT / 'own_startup_verification.json'
VISUAL = ROOT / 'visual_layout_approval.json'
LIVE = ROOT / 'figurehead_navigation_gift_advice_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/figurehead_navigation_gift_advice_repo_qa_20261111.xml')
OBSERVED = (3158, 3147, 3160)
CASES = ((3158, 1, 9600, 9900, 10200), (3147, 2, 10800, 11100, 11400), (3160, 3, 11700, 12000, 12300))
ITEM_NAMES = {3158: 'Sextant', 3147: 'Eagle Figurehead', 3160: 'Frozen Rose'}


def verify_startup():
    FunctionType(offline.verify_startup.__code__, vars(offline) | globals())()


def approve_layout(viewed):
    code = checked_text(getsource(offline.approve_layout), {
        "len(proof['native_display_cases']) == 48": "len(proof['native_display_cases']) == 68",
        "len(proof['native_original_copies']) == 24": "len(proof['native_original_copies']) == 34",
        "len(manuscript['native_context']['offline_native_selector_cases']) == 144":
            "len(manuscript['native_context']['offline_native_selector_cases']) == 204",
        "proof['sheets']) == 24": "proof['sheets']) == 34",
        'full_native_planes_directly_reviewed=24': 'full_native_planes_directly_reviewed=34',
        'original_offline_loader_copies=24': 'original_offline_loader_copies=34',
        'original_offline_portrait_cases=48': 'original_offline_portrait_cases=68',
        'original_offline_caller_fragments=144': 'original_offline_caller_fragments=204',
        'two or three body rows': 'one to four body rows',
        'Approved all 24 native layouts': 'Approved all 34 native layouts',
    })
    env = vars(offline) | globals()
    exec(compile(code, __file__ + '::approved-figurehead-navigation-gift-layouts', 'exec'), env)
    env['approve_layout'](viewed)


def item_fields(font, image, number):
    footer = (102, 365, 160, 384) if number == 3158 else (152, 365, 209, 384)
    fields = [
        precedent.find_mask(font, ITEM_NAMES[number], image, (47, 18, 250, 43)),
        precedent.find_mask(font, 'Advice', image, footer),
    ]
    if number == 3158:
        fields.append(precedent.find_mask(font, 'Remove', image, (160, 365, 211, 384)))
    return fields


def verify_live():
    code = checked_text(getsource(precedent.verify_live), {
        'sha, 11800': 'sha, 13100',
        "(24, 2, 'Black Rapier', 0), (72, 3, 'Charles Martel Armor', 0),":
            "(114, 5, 'Eagle Figurehead', 0), (127, 7, 'Frozen Rose', 0),",
        '((3057, 1, 9600, 9900, 10200), (3105, 4, 10400, 10700, 11000))': 'CASES',
        "footer = find_mask(font, 'Advice', returned, (152, 365, 209, 384))":
            'footer = item_fields(font, returned, message)',
        '(8400, 11800)': '(8400, 13100)',
        'stored_cases=50, viewed_pages=50': 'stored_cases=34, viewed_pages=34',
        'Verified the one-row weapon and four-row armor Advice portraits and exact Items/Lisbon returns.':
            'Verified Hans’s tool, figurehead and gift Advice portraits and exact Items/Lisbon returns.',
    })
    env = vars(precedent) | globals()
    exec(compile(code, __file__ + '::three-original-items-advice-contexts', 'exec'), env)
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
