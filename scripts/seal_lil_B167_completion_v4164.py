"""Seal completion only after every staged ledger/document byte has been applied."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_completion_v4164')
if __name__=='__main__':
    assert ROOT.exists() and not (ROOT/'completion_receipt.json').exists()
    plan=read(ROOT/'staged_completion.json');p=Path(plan['staged_receipt'])
    assert sha(p.read_bytes())==plan['staged_receipt_sha256'];receipt=read(p)
    assert len(plan['files'])==6
    for r in plan['files']:
        assert sha(Path(r['target']).read_bytes())==sha(Path(r['planned']).read_bytes())==r['planned_sha256']
        assert sha((ROOT/(Path(r['target']).name+'.before')).read_bytes())==r['before_sha256']
    for p,h in {**receipt['updated_files'],**receipt['evidence']}.items():assert sha(Path(p).read_bytes())==h,p
    ledger=read('translations/editorial_review_current_v1.json');fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5602,5602,0)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5605,5602,3567,2035)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(ROOT/'completion_receipt.json',receipt)
    save(ROOT/'native_application_seal.json',dict(staged_plan=str(ROOT/'staged_completion.json'),staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),receipt=str(ROOT/'completion_receipt.json'),receipt_sha256=sha((ROOT/'completion_receipt.json').read_bytes()),all_six_files_applied_exactly=True,no_duplicate_source_prose_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4164 completion sealed:5602 integrated,29 B167 completions,source/prose5605 unchanged. Independent final audit required;full goal active.')
