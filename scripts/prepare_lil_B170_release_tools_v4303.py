"""Prepare the complete V4303 build, terminal-gated patch audit and startup runs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_release_tools_v4303')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/build_lil_B169_v4251.py', 'scripts/build_lil_B170_v4303.py', {
        'lil_B169_build_v4251': 'lil_B170_build_v4303',
        'all_routes_combined_v4251': 'all_routes_combined_v4303',
        'lil_B169_registration_v4250b': 'lil_B170_registration_v4302b',
        'all-routes-unified-v4251': 'all-routes-unified-v4303',
    })]
    tools.append(derive('scripts/verify_lil_B169_release_v4252.py', 'scripts/verify_lil_B170_release_v4304.py', {
        'lil_B169_editorial_v2': 'lil_B170_editorial_v1',
        'lil_B169_release_v4252': 'lil_B170_release_v4304',
        'all_routes_combined_v4251': 'all_routes_combined_v4303',
        'all_routes_combined_v4204': 'all_routes_combined_v4251',
        'lil_B169_registration_v4250b': 'lil_B170_registration_v4302b',
        'all-routes-unified-v4251': 'all-routes-unified-v4303',
        'all-routes-unified-v4204': 'all-routes-unified-v4251',
        'lil_B169_editorial': 'lil_B170_editorial',
        "len(manifest['batches'])==545": "len(manifest['batches'])==546",
        'all545_manifest_batches_and114_accepted_layers_present': 'all546_manifest_batches_and114_accepted_layers_present',
        'all_earlier_profiles_and_V4204_promotion_unchanged': 'all_earlier_profiles_and_V4251_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4204': 'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4251',
        'manifest_batches=545': 'manifest_batches=546',
        "    assert not ROOT.exists();manifest,prior=": "    terminal=read('work/analysis/lil_B170_build_v4303/build_terminal.json');assert terminal['terminal'] and terminal['returncode']==0 and terminal['candidate_exists']\n    assert not ROOT.exists();manifest,prior=",
    }))
    tools.append(derive('scripts/run_lil_B169_startup_v4253.py', 'scripts/run_lil_B170_startup_v4305.py', {
        'lil_B169_runs_v4253': 'lil_B170_runs_v4305', 'lil_B169_v4253': 'lil_B170_v4305',
        'version=4251': 'version=4303', 'B169': 'B170',
    }))
    tools.append(derive('scripts/verify_lil_B169_startup_v4254.py', 'scripts/verify_lil_B170_startup_v4306.py', {
        'lil_B169_startup_v4254': 'lil_B170_startup_v4306',
        'lil_B169_runs_v4253': 'lil_B170_runs_v4305',
        'all_routes_combined_v4251': 'all_routes_combined_v4303',
        'all_routes_combined_v4204': 'all_routes_combined_v4251',
        'lil_B168_runs_v4206': 'lil_B169_runs_v4253',
        'V4204': 'V4251', 'Current4251': 'Current4303', 'B169': 'B170',
    }))
    tools.append(derive('scripts/record_lil_B169_startup_view_v4254.py', 'scripts/record_lil_B170_startup_view_v4306.py', {
        'lil_B169_startup_v4254': 'lil_B170_startup_v4306', 'V4204': 'V4251', 'B169': 'B170',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, expected_manifest_batches=546, accepted_layers=114,
        existing_V4251_promotion_preserved=True, release_verifier_requires_successful_terminal_builder=True,
        no_build_patch_or_startup_claim_yet=True, full_goal_complete=False))
    print('V4303 cumulative build/exact patch/startup tools prepared;546 batches expected;main remainsV4251.')
