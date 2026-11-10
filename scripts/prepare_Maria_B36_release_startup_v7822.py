"""Freeze exact release/patch verification andonly the affected own-ROM Maria startup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B36_release_startup_tools_v7822')
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/verify_Maria_story_release_v7780.py','scripts/verify_Maria_B36_release_v7822.py',{
        'maria_story_editorial_v3':'maria_B36_editorial_v1',
        'maria_story_release_v7780':'maria_B36_release_v7822',
        'all_routes_combined_v7779_candidate':'all_routes_combined_v7821_candidate',
        'all_routes_combined_v7717_candidate':'all_routes_combined_v7779_candidate',
        'maria_story_registration_v7778':'maria_B36_registration_v7820',
        'maria_story_build_v7779':'maria_B36_build_v7821',
        'maria_story_regressions_v7779':'maria_B36_regressions_v7821',
        'all-routes-unified-v7779':'all-routes-unified-v7821',
        'all-routes-unified-v7717':'all-routes-unified-v7779',
        "'maria_story_editorial'":"'maria_B36_editorial'",
        'maria_story_atomic_v7775c':'maria_B36_atomic_v7818b',
        'len(ids)==67':'len(ids)==16',
        '[34,35,108]':'[36]',
        "builder.index(b\"profile_config.get('maria_B207_editorial')\")":"builder.index(b\"profile_config.get('maria_story_editorial')\")",
        '630':'631',
        'only_SC3_B34_B35_B108_change_all300others_exact':'only_SC3_B36_change_all302others_exact',
        'cumulative Maria67 editorial':'cumulative Maria B36 editorial',
        'Maria67 candidate':'Maria B36 candidate',
    }))
    results.append(derive('scripts/run_Maria_story_startup_v7781.py','scripts/run_Maria_B36_startup_v7823.py',{
        'maria_story_startup_runs_v7781':'maria_B36_startup_runs_v7823',
        'maria_story_release_v7780':'maria_B36_release_v7822',
        'all-routes-unified-v7779':'all-routes-unified-v7821',
        "Path('work/analysis/maria_B207_startup_runs_v7719/route3')":"Path('work/analysis/maria_story_startup_runs_v7781/route3')",
        'Maria_story_V7779_{case}_v7781':'Maria_B36_V7821_{case}_v7823',
        'V7779':'V7821',
        'B34/B108/B35 activation':'B36 activation',
    }))
    results.append(derive('scripts/verify_Maria_story_startup_v7782.py','scripts/verify_Maria_B36_startup_v7824.py',{
        'maria_story_startup_verification_v7782':'maria_B36_startup_verification_v7824',
        'maria_story_startup_runs_v7781':'maria_B36_startup_runs_v7823',
        'current_V7779_native_v7782':'current_V7821_native_v7824',
        'maria_story_release_v7780':'maria_B36_release_v7822',
        'all_routes_combined_v7717_candidate':'all_routes_combined_v7779_candidate',
        'all-routes-unified-v7779':'all-routes-unified-v7821',
        'V7717':'V7779','V7779':'V7821',
    }))
    results.append(derive('scripts/record_Maria_story_startup_view_v7783.py','scripts/record_Maria_B36_startup_view_v7825.py',{
        'maria_story_startup_view_v7783':'maria_B36_startup_view_v7825',
        'maria_story_startup_verification_v7782':'maria_B36_startup_verification_v7824',
        'own_Maria_startup_exact_V7717_andstrict_current_input':'own_Maria_startup_exact_V7779_andstrict_current_input',
        'V7717':'V7779',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        all_original_native_high_constants_manifest_reference_inverse_clean_patch_andownership_guards_preserved=True,
        complete631_batches114accepted_18checks110regressions_required=True,
        only_affected_Maria_own_ROM_startup_repeated_prior_other_route_evidence_preserved=True,
        original_ordinary_inputs_andexisting_system_only_unlock_earned_false=True,
        no_separate_test_package_promotion_orcredit_change=True,full_goal_complete=False))
