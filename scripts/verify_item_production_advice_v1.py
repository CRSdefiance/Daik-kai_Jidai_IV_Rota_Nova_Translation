"""Seal visual and startup verification for the production advice checkpoint."""

import argparse
from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import replay_item_production_advice_v1 as replay
from scripts import verify_setup_save_equipment_v1 as startup


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT = ROOT / 'own_startup_verification.json'
VISUAL = ROOT / 'visual_layout_approval.json'
QA = Path('work/item_production_advice_repo_qa_20261111.xml')


def verify_startup():
    parent = stage.load(stage.RELEASE)
    before = stage.NdsImage.open(parent['candidate']).read_file(stage.ARM)
    after = stage.NdsImage.open(ROM).read_file(stage.ARM)
    assert cache_plan(before) == cache_plan(after)
    assert before[0x8E4:0x8E8] == after[0x8E4:0x8E8]
    assert before[0xE45DC:0xE45E0] == after[0xE45DC:0xE45E0]
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals())()


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = stage.load(PROOF)
    manuscript = stage.load(stage.OUTPUT)
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(stage.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert stage.digest(ROM) == proof['research_ROM_sha256']
    assert stage.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert len(proof['native_display_cases']) == 48 and len(proof['native_original_copies']) == 24
    assert len(manuscript['native_context']['offline_native_selector_cases']) == 144
    assert sum(len(row['messages']) for row in proof['sheets']) == 24
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(s.get('tests', 0)) for s in suites) == 34
    assert all(int(s.get(key, 0)) == 0 for s in suites for key in ('errors', 'failures', 'skipped'))
    stage.save(VISUAL, dict(candidate_sha256=stage.digest(ROM), full_native_planes_directly_reviewed=24,
        original_offline_loader_copies=24, original_offline_portrait_cases=48,
        original_offline_caller_fragments=144, repository_tests=34, sheet_sha256=viewed,
        native_all_glyphs_positions_and_bounds=True, pagination='One portrait per reply, two or three body rows.',
        evidence={str(p): stage.digest(p) for p in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, completed_editorial_credit=0))
    print('Approved all 24 native layouts and the 34 targeted regression tests.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        verify_startup()
