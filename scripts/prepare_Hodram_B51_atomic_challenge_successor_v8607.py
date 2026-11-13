"""Resume after ten completed semantic cases; use the independently measured query guard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_atomic_challenge_successor_v8607');assert not root.exists()
    resume="""    previous=Path('work/analysis/Hodram_B51_atomic_challenges_v8605')
    assert len(list(previous.glob('case*.json')))==10
    for index,(label,path,key,new,expected) in enumerate(specs[:10]):
        row=read(previous/f'case{index:02d}.json');prior=read(path);changed=deepcopy(prior);setpath(changed,key,new)
        assert row['case']==label and row['original_value_sha256']==digest(prior) and row['changed_value_sha256']==digest(changed)
        assert row['rejected'] and row['actual_changed_input'] and row['commit_calls']==0 and row['original_object_files_components_andserialized_bytes_unchanged']
        assert row['expected_guard']==expected and expected in row['error']
        cases.append(row)
    ROOT.mkdir(parents=True);original_load,dependencies,commit=owned.load,owned.check_dependencies,owned.commit_image
"""
    result=derive('scripts/challenge_Hodram_B51_atomic_v8605.py','scripts/challenge_Hodram_B51_atomic_v8605b.py',{
        "ROOT=Path('work/analysis/Hodram_B51_atomic_challenges_v8605')":"ROOT=Path('work/analysis/Hodram_B51_atomic_challenges_v8605b')",
        "'both unforced queries and all six return words'":"'complete relocated query ABI/scratch/input/return records'",
        '    ROOT.mkdir(parents=True);original_load,dependencies,commit=owned.load,owned.check_dependencies,owned.commit_image\n':resume,
        'enumerate(specs):':'enumerate(specs[10:],start=10):',
        'all_changed_inputs_distinct_andexpected_semantic_guards_match=True,':'all_changed_inputs_distinct_andexpected_semantic_guards_match=True, prior_ten_cases_reused_after_exact_original_changed_input_andguard_revalidation=True, prior_case_root=str(previous),',
    })
    binding=derive('scripts/bind_Hodram_B51_atomic_v8606.py','scripts/bind_Hodram_B51_atomic_v8606b.py',{
        'Hodram_B51_atomic_challenges_v8605/semantic_rejections.json':'Hodram_B51_atomic_challenges_v8605b/semantic_rejections.json'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(semantic=result,binding=binding,stopped_original_preserved=True,actual_query_defect_rejected_at_complete_return_record_comparison=True,no_completed_semantic_case_replayed=True,all_native_guards_andzero_commit_assertions_preserved=True,new_credit=0,full_goal_complete=False))
