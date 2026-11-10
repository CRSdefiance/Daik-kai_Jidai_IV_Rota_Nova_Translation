"""Source-lock the sole cumulative builder andthe unchanged required110 regressions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_build_tools_v7779');assert not root.exists()
    a=derive('scripts/build_Maria_B207_v7717.py','scripts/build_Maria_story_v7779.py',{
        'maria_B207_build_v7717':'maria_story_build_v7779','all_routes_combined_v7717_candidate':'all_routes_combined_v7779_candidate',
        'maria_B207_registration_v7716':'maria_story_registration_v7778','all-routes-unified-v7717':'all-routes-unified-v7779',
    })
    b=derive('scripts/run_Maria_B207_regressions_v7717.py','scripts/run_Maria_story_regressions_v7779.py',{
        'maria_B207_regressions_v7717':'maria_story_regressions_v7779',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=[a,b],
        sole_registered_cumulative_builder_unchanged=True,existing110_required_release_dialogue_regressions_unchanged=True,
        no_separate_test_package_orpromotion=True,new_credit=0,full_goal_complete=False))
