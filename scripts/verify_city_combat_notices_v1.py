"""Bind reviewed combat portraits, glyph scope and cold startup to the exact ROM."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_city_combat_notices_v1 as replay
from scripts import verify_fleet_reports_v1 as prior
from scripts import verify_item_production_advice_v1 as prior_startup
from scripts.source_locked_derivation_v5118 import checked_text


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.STARTUP.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
QA = Path('work/city_combat_notices_repo_qa_20261111.xml')


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == 35 and proof['native_pages'] == proof['native_cases'] == 80
    assert sum(len(row['messages']) for row in proof['sheets']) == 80
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert all(int(row.get(key, 0)) == 0 for row in tests for key in ('errors', 'failures', 'skipped'))
    arm = base.NdsImage.open(ROM).read_file(stage.first.review.ARM)
    source = checked_text(getsource(prior.amount_controls), {
        'AMOUNT_TABLES[1] + 4': 'AMOUNT_TABLES[0] + 4',
        '0x02117AE0, 0x274, renderer': '0x02117AE0, 0x274, legacy',
    })
    env = vars(prior) | {'AMOUNT_TABLES': stage.first.AMOUNT_TABLES}
    exec(compile(source, __file__ + '::spoils-digit-controls', 'exec'), env)
    amount = env['amount_controls'](arm, proof['ownership'])
    assert len(amount) == 9
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], native_pages=80, stored_cases=35,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34,
        names_unbroken_in_tested_variants=True, original_amount_control_cases=amount,
        original_formatter_input_unchanged=True, sheet_sha256=viewed,
        evidence={str(p): base.digest(p) for p in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Verified all 80 viewed pages, nine digit-scope controls and 34 repository tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=stage.first.review.parent.RELEASE,
                             NdsImage=base.NdsImage, ARM=stage.first.review.ARM)
    FunctionType(prior_startup.verify_startup.__code__, vars(prior_startup) | globals() | {'stage': loader})()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'startup':
        verify_startup()
    else:
        approve_layout(args.viewed_sheets)
