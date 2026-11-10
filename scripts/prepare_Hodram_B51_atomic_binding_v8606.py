"""Bind equal lifecycle reports, semantic rejection cases and all-guard wrong-memory checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_atomic_binding_tools_v8606');assert not root.exists()
    extra="""    assert positive['cases'][0]['report']==positive['cases'][1]['report']
    wrong_path=Path('work/analysis/Hodram_B51_wrong_memory_v8605/wrong_memory_rejections.json');wrong=read(wrong_path)
    assert wrong['negative_count']==3 and wrong['every_wrong_image_rejected_before_commit_withall_guards_active'] and wrong['no_digest_orsemantic_bypass']
    assert all(c['actual_wrong_inmemory_image'] and c['commit_calls']==0 and c['whole_original_input_object_files_components_andserialized_bytes_unchanged'] for c in wrong['cases'])
    for path,digest in wrong['evidence'].items():assert sha(Path(path).read_bytes())==digest
    for p,h in positive['evidence'].items():assert sha(Path(p).read_bytes())==h
"""
    result=derive('scripts/bind_Hodram_B50_atomic_v8541.py','scripts/bind_Hodram_B51_atomic_v8606.py',{
        "    for p,h in positive['evidence'].items():assert sha(Path(p).read_bytes())==h\n":extra,
        'hodram_B50_editorial_v1':'hodram_B51_editorial_v1','scripts.Hodram_B50_release_paths_v8537':'scripts.Hodram_B51_release_paths_v8595',
        'Hodram_B50_atomic_binding_v8541':'Hodram_B51_atomic_binding_v8606','Hodram_B50_atomic_positive_v8539':'Hodram_B51_atomic_positive_v8604','Hodram_B50_atomic_challenges_v8540':'Hodram_B51_atomic_challenges_v8605',
        "len(p['report']['changed_records'])==3":"len(p['report']['changed_records'])==5",
        "len(negative['cases'])==16":"len(negative['cases'])==17",
        'all16_actually_changed':'all17_actually_changed',
        'both_input_lifecycles_one_complete_commit_exact_reference=True,':'both_input_lifecycles_one_complete_commit_exact_reference=True, lifecycle_reports_value_equal=True, wrong_memory=str(wrong_path),wrong_memory_sha256=sha(wrong_path.read_bytes()),all3_genuine_wrong_memory_inputs_rejected_withall_guards_active=True,',
        'B50 sealedmodule':'B51 sealedmodule','/16actual-changing':'/17actual-changing'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_prior_binding_assertions_preserved_andwrong_memory_equal_report_checks_added=True,new_credit=0,full_goal_complete=False))
