"""Preserve the v2 checker failure; bind the saved integer native-case count exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_production_tools_v7775c');assert not root.exists()
    a=derive('dk4tool/patch/maria_story_editorial_v2.py','dk4tool/patch/maria_story_editorial_v3.py',{
        "len(branches['native_cases'])==200":"branches['native_cases']==200",
    })
    b=derive('scripts/validate_Maria_story_atomic_v7775b.py','scripts/validate_Maria_story_atomic_v7775c.py',{
        'maria_story_editorial_v2':'maria_story_editorial_v3','maria_story_atomic_v7775b':'maria_story_atomic_v7775c',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=[a,b],
        v1_positive_andv2_TypeError_failure_preserved_not_ROM_failure_ornegative_guard_credit=True,
        native_branch_count_is_integer200_not_list=True,all_native_numeric_constants_andownership_guards_preserved=True,
        no_ROM_registry_orcredit_change=True,full_goal_complete=False))
