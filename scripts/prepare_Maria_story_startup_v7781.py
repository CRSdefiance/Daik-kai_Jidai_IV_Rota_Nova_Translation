"""Freeze only the affected own-ROM Maria startup; unchanged runtime/other route evidence stays."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_startup_tools_v7781');assert not root.exists()
    d=derive('scripts/run_Maria_B207_startup_v7719.py','scripts/run_Maria_story_startup_v7781.py',{
        'maria_B207_startup_runs_v7719':'maria_story_startup_runs_v7781',
        'maria_B207_release_v7718':'maria_story_release_v7780',
        "choices=['route0','route1','route2','route3','town']":"choices=['route3']",
        "Path('work/analysis/maria_B207_route_run_v7680')":"Path('work/analysis/maria_B207_startup_runs_v7719/route3')",
        'all-routes-unified-v7717':'all-routes-unified-v7779',
        'V7717':'V7779','B207 activation':'B34/B108/B35 activation','no_optional_B207_activation':'no_optional_story_arc_activation',
        'Maria_B207_V7717_{case}_v7719':'Maria_story_V7779_{case}_v7781',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=d,
        affected_SC3_archive_own_registered_Maria_startup_fresh=True,
        exact_previous_inputs_andexisting_system_only_unlock_earned_false=True,
        unchanged_other_three_routes_ARM9_COMMON_fonts_components_andcompleted_prior_startups_not_repeated=True,
        not_fullroute_natural_optional_activation_orhardware=True,new_credit=0,full_goal_complete=False))
