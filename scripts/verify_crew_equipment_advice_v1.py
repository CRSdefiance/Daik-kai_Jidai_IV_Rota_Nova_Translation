"""Verify the crew-equipment Advice pages and the original Mikhail replay."""

import argparse
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import replay_crew_equipment_advice_v1 as replay
from scripts import verify_item_production_advice_v1 as offline
from scripts import verify_weapon_armor_advice_v1 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT = ROOT / 'own_startup_verification.json'
VISUAL = ROOT / 'visual_layout_approval.json'
LIVE = ROOT / 'crew_equipment_advice_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/crew_equipment_advice_repo_qa_20261111.xml')
OBSERVED = (3140, 3143)
NAMEPLATE = 'Mikhail Letzel'


def verify_startup():
    FunctionType(offline.verify_startup.__code__, vars(offline) | globals())()


def approve_layout(viewed):
    code = checked_text(getsource(offline.approve_layout), {
        "len(proof['native_display_cases']) == 48": "len(proof['native_display_cases']) == 80",
        "len(proof['native_original_copies']) == 24": "len(proof['native_original_copies']) == 40",
        "len(manuscript['native_context']['offline_native_selector_cases']) == 144":
            "len(manuscript['native_context']['offline_native_selector_cases']) == 240",
        "proof['sheets']) == 24": "proof['sheets']) == 40",
        'full_native_planes_directly_reviewed=24': 'full_native_planes_directly_reviewed=40',
        'original_offline_loader_copies=24': 'original_offline_loader_copies=40',
        'original_offline_portrait_cases=48': 'original_offline_portrait_cases=80',
        'original_offline_caller_fragments=144': 'original_offline_caller_fragments=240',
        'two or three body rows': 'one to three body rows',
        'Approved all 24 native layouts': 'Approved all 40 native layouts',
    })
    env = vars(offline) | globals()
    exec(compile(code, __file__ + '::approved-crew-advice-layouts', 'exec'), env)
    env['approve_layout'](viewed)


def check_maria_snapshot(raw):
    assert len(raw) == 0x400000
    assert unpack_from('<I', raw, 0x2796B0)[0] == 3
    assert raw[replay.FLAG_OWNER + 4 - 0x02000000] == 17


def verify_live():
    code = checked_text(getsource(precedent.verify_live), {
        'sha, 11800': 'sha, 7200',
        "(24, 2, 'Black Rapier', 0), (72, 3, 'Charles Martel Armor', 0),":
            "(107, 4, 'Illustrated Bible', 0), (110, 4, 'Gupta Spirit Beast', 0),",
        "    assert inventory['synthetic_advice_unlock']":
            "    assert inventory['synthetic_advice_unlock'] and inventory['original_captain'] == inventory['original_route_state'] == 3",
        'dict(address=replay.previous.FLAG_OWNER + 4, before=0, after=16)':
            'dict(address=replay.FLAG_OWNER + 4, before=1, after=17)',
        '((3057, 1, 9600, 9900, 10200), (3105, 4, 10400, 10700, 11000))':
            '((3140, 1, 4900, 5200, 5500), (3143, 3, 5800, 6100, 6400))',
        "        assert len(raw) == 0x400000": "        check_maria_snapshot(raw)",
        "(message, 75)": "(message, 76)",
        "'Hans Letzel'": 'NAMEPLATE',
        "footer = find_mask(font, 'Advice', returned, (152, 365, 209, 384))":
            "footer = [find_mask(font, 'Advice', returned, (102, 365, 160, 384)),\n"
            "                  find_mask(font, 'Equip', returned, (160, 365, 211, 384))]",
        '(8400, 11800)': '(3400, 7200)',
        'stored_cases=50, viewed_pages=50': 'stored_cases=40, viewed_pages=40',
        'Verified the one-row weapon and four-row armor Advice portraits and exact Items/Lisbon returns.':
            'Verified Mikhail’s complete one-row and three-row portraits and exact Items/Nagasaki returns.',
    })
    env = vars(precedent) | globals()
    exec(compile(code, __file__ + '::maria-save-mikhail-advice', 'exec'), env)
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
