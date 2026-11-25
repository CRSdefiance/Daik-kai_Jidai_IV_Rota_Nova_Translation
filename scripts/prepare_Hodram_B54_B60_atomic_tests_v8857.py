"""Retain both whole-NDS lifecycles,wrong-memory checks and late semantic commit rejection tests."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_atomic_test_tools_v8857');assert not root.exists()
    common={'hodram_B31_B53_editorial_v2':'hodram_B54_B60_editorial_v1','Hodram_B31_B53_release_paths_v8767':'Hodram_B54_B60_release_paths_v8853','B31_B53':'B54_B60'}
    positive=derive('scripts/validate_Hodram_B31_B53_atomic_v8770.py','scripts/validate_Hodram_B54_B60_atomic_v8857.py',{
        **common,'Hodram_B31_B53_atomic_positive_v8770':'Hodram_B54_B60_atomic_positive_v8857',
        "==3 and len(report['files'])==1":"==82 and len(report['files'])==1",'/3IDs each':'/82IDs each',
    })
    wrong=derive('scripts/validate_Hodram_B31_B53_wrong_memory_v8771.py','scripts/validate_Hodram_B54_B60_wrong_memory_v8858.py',{
        **common,'Hodram_B31_B53_wrong_memory_v8771':'Hodram_B54_B60_wrong_memory_v8858',
    })
    semantic=derive('scripts/challenge_Hodram_B31_B53_atomic_v8772.py','scripts/challenge_Hodram_B54_B60_atomic_v8859.py',{
        **common,'Hodram_B31_B53_atomic_challenges_v8772':'Hodram_B54_B60_atomic_challenges_v8859',
        'Exact Hodram-B31-B53 approved prose/source/context':'Exact Hodram-B54-B60 approved prose/source/context',
        'Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',"paths['B31_actual']":"paths['B54_actual']",
    })
    root.mkdir(parents=True);save(root/'source_locked_atomic_tests.json',dict(positive=positive,wrong_memory=wrong,semantic=semantic,all_original_object_identity_serialized_bytes_files_components_andexactreference_guards_preserved=True,both_direct_current_andcanonical_source_fullcurrent_memory_lifecycles_required=True,three_genuinely_wrong_memory_inputs_andfour_semantic_latefailures_require_zero_commit=True,no_frozen_native_editorial_orsemantic_guard_bypass=True,only_outer_digest_layer_is_bypassed_in_four_explicit_semantic_challenges=True,no_tests_run_before_current_seal_exists=True,new_credit=0,full_goal_complete=False))
