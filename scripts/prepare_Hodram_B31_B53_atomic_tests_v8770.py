"""Preserve both established whole-NDS lifecycles and three actual wrong-memory challenges."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_atomic_test_tools_v8770');assert not root.exists()
    positive=derive('scripts/validate_Hodram_B52_atomic_v8690b.py','scripts/validate_Hodram_B31_B53_atomic_v8770.py',{
        'B52':'B31_B53','Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'Hodram_B52_atomic_positive_v8690b':'Hodram_B31_B53_atomic_positive_v8770',
        "==5 and len(report['files'])==1":"==3 and len(report['files'])==1",
        '/5IDs each':'/3IDs each',
    })
    negative=derive('scripts/validate_Hodram_B52_wrong_memory_v8691b.py','scripts/validate_Hodram_B31_B53_wrong_memory_v8771.py',{
        'B52':'B31_B53','Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'Hodram_B52_wrong_memory_v8691b':'Hodram_B31_B53_wrong_memory_v8771',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(positive=positive,wrong_memory=negative,
        all_original_object_identity_files_components_serialization_andwhole_NDS_commit_guards_preserved=True,
        canonical_source_full_current_memory_anddirect_current_both_retained=True,
        three_genuinely_wrong_memory_cases_no_digest_orsemantic_bypass=True,new_credit=0,full_goal_complete=False))
