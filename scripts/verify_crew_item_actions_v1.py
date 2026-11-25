"""Record approval of the native portraits and verify cold startup."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_crew_item_actions_v1 as replay
from scripts import verify_item_production_advice_v1 as prior


stage = replay.stage
base = replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_approval.json'
QA = Path('work/crew_item_actions_repo_qa_20261111.xml')


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof, draft = base.load(PROOF), base.load(stage.OUTPUT)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert sum(len(row['messages']) for row in proof['sheets']) == proof['native_pages'] == 40
    assert sum(len(row['displays']) for row in proof['records']) == proof['native_cases'] == 46
    assert len(proof['records']) == 33 and draft['counts'] == {'revision': 24, 'retention': 9}
    for row in proof['records']:
        for display in row['displays']:
            item = display['item_name']
            if item:
                assert any(item['item_name'] in line for line in display['visible_lines'])
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert all(int(row.get(key, 0)) == 0 for row in tests for key in ('errors', 'failures', 'skipped'))
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], all_pages_viewed=True,
        native_pages=40, native_cases=46, original_stored_lookups=33, repository_tests=34,
        both_runtime_item_names_unbroken=True, complete_glyphs_and_bounds=True, sheet_sha256=viewed,
        evidence={str(p): base.digest(p) for p in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved all 40 final portrait pages and 34 targeted tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=stage.first.review.parent.RELEASE,
                             NdsImage=base.NdsImage, ARM=stage.first.ARM)
    FunctionType(prior.verify_startup.__code__, vars(prior) | globals() | {'stage': loader})()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('startup', 'layout'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        verify_startup()
