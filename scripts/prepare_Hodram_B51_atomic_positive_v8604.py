"""Source-lock both original-object atomic lifecycle checks for five B51 records."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_atomic_positive_tools_v8604');assert not root.exists()
    result=derive('scripts/validate_Hodram_B50_atomic_v8539.py','scripts/validate_Hodram_B51_atomic_v8604.py',{
        'hodram_B50_editorial_v1':'hodram_B51_editorial_v1',
        'scripts.Hodram_B50_release_paths_v8537':'scripts.Hodram_B51_release_paths_v8595',
        'Hodram_B50_atomic_positive_v8539':'Hodram_B51_atomic_positive_v8604',
        "len({r['id'] for r in report['changed_records']})==3":"len({r['id'] for r in report['changed_records']})==5",
        'B50':'B51','3IDs':'5IDs'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,whole_object_commit_andoriginal_identity_files_components_bytes_guards_preserved=True,new_credit=0,full_goal_complete=False))
