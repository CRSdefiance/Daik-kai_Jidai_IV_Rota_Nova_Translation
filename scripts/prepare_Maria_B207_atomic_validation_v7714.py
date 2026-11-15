"""Source-lock static dependency closure andthe one-file positive reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_atomic_validation_tools_v7714')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/validate_papal_trade_atomic_v7657.py','scripts/validate_Maria_B207_atomic_v7714.py',{
        'Freeze static evidence closure and prove one final two-file commit matches the reference.':'Freeze static evidence closure andprove one final Maria single-file commit matches the reference.',
        'papal_trade_editorial_v1':'maria_B207_editorial_v1',
        'papal_trade_atomic_support_v1':'maria_B207_atomic_support_v1',
        'papal_trade_profile_v1':'maria_B207_profile_v1','papal_trade_layout_v1':'maria_B207_layout_v1',
        'scripts.papal_trade_final_paths_v7655':'scripts.Maria_B207_final_paths_v7712',
        'scripts/papal_trade_final_paths_v7655':'scripts/Maria_B207_final_paths_v7712',
        'scripts/seal_papal_trade_references_v7656':'scripts/seal_Maria_B207_references_v7713',
        'papal_trade_atomic_v7657':'maria_B207_atomic_v7714',
        'dk4-papal-trade-editorial-release-v1':'dk4-Maria-B207-editorial-release-v1',
        "len(calls[0]['changed_indices'])==2 and len(proof['changed_records'])==36":"len(calls[0]['changed_indices'])==1 and len(proof['changed_records'])==18",
        'papal_trade_reference_v7642':'maria_B207_reference_v7698',
        'positive_records=36':'positive_records=18',
        'one_final_files_list_commit_after_both_complete_reconstructions':'one_final_files_list_commit_after_complete_reconstruction',
        'two_changed_file_indices':'single_changed_file_indices',
        'source1468_logical1468_tail0_target1508_logical1506_tail2_each_full_inverse':'source1468_logical1468_tail0_target1472_logical1470_tail2_full_clean_andpredecessor_inverse',
        'all36_actual_pages_complete_headers_andlate_limits_bound':'all18_actual_pages_complete_headers_andlate_limits_bound',
        '36-record positive reconstruction passes one two-file commit':'18-record Maria positive reconstruction passes one single-file commit',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validation.json',dict(derivation=tool,no_native_high_constants_changed=True,new_credit=0,full_goal_complete=False))
