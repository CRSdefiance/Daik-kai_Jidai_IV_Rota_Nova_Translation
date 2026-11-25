"""Reuse 287 complete passing record proofs; check only the remaining 65 records fresh."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_native_resume_inputs_20261104')
DOC = Path('work/analysis/Hodram_B191_B210_formatting_20261104/formatting_input.json')
PLAN = Path('work/analysis/Hodram_B191_B210_formatting_20261104/guard_and_opening_v4/automatic_plans.json')
PRIOR = Path('work/analysis/Hodram_B191_B210_native_20261104/initial_v2')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, plans = map(load, [DOC, PLAN])
    by_id = {r['id']: r for r in plans['records']}
    old = []
    receipts = []
    for block in range(191, 208):
        path = PRIOR / f'B{block}_checked.json'
        receipt = load(path)
        receipts.append(dict(path=str(path), sha256=sha(path.read_bytes()), records=len(receipt['records'])))
        old.extend(receipt['records'])
    assert len(old) == 288
    reused = []
    for row in old:
        if row['id'] == 'DK4_MES_B201_R0074':
            continue
        assert row['compiled_hex'] == by_id[row['id']]['encoded_hex']
        reused.append(dict(id=row['id'], block=row['block'], native_record=row))
    assert len(reused) == 287
    reused_ids = {r['id'] for r in reused}
    remaining = [r for r in doc['records'] if r['kind'] != 'typed-choice-label' and r['id'] not in reused_ids]
    assert len(remaining) == 65 and {r['block'] for r in remaining} == {201, 208, 209, 210}
    subset = deepcopy(doc)
    subset.update(records=remaining, blocks=sorted({r['block'] for r in remaining}), physical_speech_objects=65,
        ordinary_speech_objects=65, typed_choice_objects=0, typed_choice_commands=0,
        subset_of=str(DOC), subset_of_sha256=sha(DOC.read_bytes()))
    ROOT.mkdir()
    subset_path = ROOT / 'remaining65_manuscript.json'
    save(subset_path, subset)
    planned = deepcopy(plans)
    planned.update(records=[by_id[r['id']] for r in remaining], manuscript=str(subset_path), manuscript_sha256=sha(subset_path.read_bytes()),
        parent_complete_plan=str(PLAN), parent_complete_plan_sha256=sha(PLAN.read_bytes()),
        exact_parent_plan_subset_no_reformatting=True)
    save(ROOT / 'remaining65_plans.json', planned)
    save(ROOT / '287_exact_record_proofs_reused.json', dict(records=reused, receipts=receipts,
        original_job_terminal_failure=74976, original_failure_after_all17_complete_block_receipts=True,
        later_failure_does_not_invalidate_prior_complete_record_proofs=True,
        unchanged_registered_runtime='work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json',
        new_complete_plan=str(PLAN), new_complete_plan_sha256=sha(PLAN.read_bytes()), new_credit=0))
    print('287 exact passing native records reused; only 65 remaining/reformatted records need fresh checks.')
