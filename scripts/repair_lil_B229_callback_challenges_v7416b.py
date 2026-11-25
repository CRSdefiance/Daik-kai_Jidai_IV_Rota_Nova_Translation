"""Preserve malformed callback-fixture failure; reuse only identical,fully recorded earlier cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_callback_challenge_repair_v7416b')
if __name__=='__main__':
    assert not ROOT.exists()
    anchor="    save(ROOT/'challenge_plan.json',dict(negative_count=len(tests),cases=[dict(case=l,target=str(p)) for l,p,e in tests],dependency_digests_deliberately_bypassed=True,positive_receipt_sha256=sha((POS/'positive_receipt.json').read_bytes())))"
    reuse="""    priorroot=Path('work/analysis/lil_B229_atomic_v7416');priorplan=read(priorroot/'challenge_plan.json');previous=read(priorroot/'partial_negative_cases.json');assert len(previous)==225
    assert priorplan['negative_count']==len(tests)==242 and priorplan['positive_receipt_sha256']==sha((POS/'positive_receipt.json').read_bytes())
    assert priorplan['cases'][:225]==[dict(case=l,target=str(p)) for l,p,e in tests[:225]]
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    assert all(r['case']==tests[i][0] and r['target']==str(tests[i][1]) and r['rejected'] and r['archive_writes']==0 for i,r in enumerate(previous))
    results=deepcopy(previous)
    for r in results:r['proof_mode']='exact-earlier-case-output-reused'
    save(ROOT/'verified_case_reuse.json',dict(prior_plan=str(priorroot/'challenge_plan.json'),prior_plan_sha256=sha((priorroot/'challenge_plan.json').read_bytes()),prior_results=str(priorroot/'partial_negative_cases.json'),prior_results_sha256=sha((priorroot/'partial_negative_cases.json').read_bytes()),reused_cases=225,fresh_cases_required=17,positive_receipt_unchanged=True,all_production_modules_andclosed_dependencies_exact=True,only_two_later_callback_mutations_repaired_with_valid_speaker_markup=True,first225_case_generator_data_unchanged_by_source_locked_successor=True,old_producer_sha256=sha(Path('scripts/challenge_lil_B229_atomic_v7416.py').read_bytes()),source_locked_repair='work/analysis/lil_B229_callback_challenge_repair_v7416b/source_locked_callback_fixture_repair.json',source_locked_repair_sha256=sha(Path('work/analysis/lil_B229_callback_challenge_repair_v7416b/source_locked_callback_fixture_repair.json').read_bytes()),full_goal_complete=False))
"""+anchor
    changes={'atomic_v7416':'atomic_v7416b',"english='Different pitch!'":"english='{SPEAKER:16}Different pitch!'","english='Different reassurance!'":"english='{SPEAKER:02}Different reassurance!'",anchor:reuse,"    for i,(label,path,edit) in enumerate(tests):":"    for i,(label,path,edit) in enumerate(tests):\n        if i<225:continue"}
    r=derive('scripts/challenge_lil_B229_atomic_v7416.py','scripts/challenge_lil_B229_atomic_v7416b.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_callback_fixture_repair.json',dict(tool=r,only_two_callback_semantic_mutations_keep_valid_speaker_markup=True,malformed_fixture_schema_exception_not_counted_as_rejection=True,reuse_requires225_actual_recorded_identical_cases_andunchanged_positive_closure=True,no_production_policy_orruntime_change=True,new_credit=0,full_goal_complete=False))
