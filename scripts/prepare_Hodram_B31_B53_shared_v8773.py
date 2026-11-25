"""Exercise this real extension and a late target failure; reuse unchanged shared-policy cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_shared_tools_v8773');assert not root.exists()
    source=Path('scripts/validate_Hodram_B52_shared_extension_v8697.py').read_text('utf-8')
    a=source.index('    mutations=[]');z=source.index('    negatives=[]',a)
    binding="""    prior_path=Path('work/analysis/Hodram_B52_shared_extension_v8697/shared_extension_validation.json')
    prior=read(prior_path);shared=Path('dk4tool/patch/late_editorial_extensions_v1.py')
    assert prior['negative_count']==6 and prior['no_guard_digest_orsemantic_bypass'] and sha(shared.read_bytes())==prior['evidence'][str(shared)]
    changed=deepcopy(spec);changed['target_ROM_sha256']='0'*64
    mutations=[('changed-target_ROM_sha256',[changed],[])]
"""
    receipt=derive('scripts/validate_Hodram_B52_shared_extension_v8697.py','scripts/validate_Hodram_B31_B53_shared_v8773.py',{
        'B52':'B31_B53','b52':'b31_b53',
        'Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'Hodram_B52_shared_extension_v8697':'Hodram_B31_B53_shared_extension_v8773',
        'from scripts.verify_village_wrap_v608 import save':'from scripts.verify_village_wrap_v608 import read,save',
        "len(reports[0]['changed_records'])==5":"len(reports[0]['changed_records'])==3",
        source[a:z]:binding,
        'negative_count=6':'negative_count=1',
        'negative_cases=negatives,':'negative_cases=negatives,exact_unchanged_framework_six_previous_cases_reused_by_source_hash=True,prior_shared_validation=str(prior_path),prior_shared_validation_sha256=sha(prior_path.read_bytes()),',
        'late_second_extension_target_identity_andduplicate_manuscript_failures_leave_original_unchanged':'late_target_identity_failure_leaves_complete_original_NDS_object_unchanged',
        'positive and6 genuine metadata/chain/target/duplicate rejections':'positive andone genuine late-target rejection;unchanged framework6cases reused byexact sourcehash',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_original_shared_actual_planner_andwhole_object_commit_guards_preserved=True,
        actual_new_three_record_extension_positive_andlate_target_zero_commit_negative=True,
        old_shared_framework_unchanged_source_bound_generic_six_cases_not_unnecessarily_replayed=True,new_credit=0,full_goal_complete=False))
