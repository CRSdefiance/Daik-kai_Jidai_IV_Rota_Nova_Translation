"""Prepare terminal-gated V4353 build, exact patch audit and fresh startup checks."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_release_tools_v4353')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/build_lil_B170_v4303.py','scripts/build_lil_B171_v4353.py',{
        'lil_B170_build_v4303':'lil_B171_build_v4353','all_routes_combined_v4303':'all_routes_combined_v4353',
        'lil_B170_registration_v4302b':'lil_B171_registration_v4352','all-routes-unified-v4303':'all-routes-unified-v4353',
    })]
    tools.append(derive('scripts/verify_lil_B170_release_v4304.py','scripts/verify_lil_B171_release_v4354.py',{
        'lil_B170_editorial_v1':'lil_B171_editorial_v1','lil_B170_release_v4304':'lil_B171_release_v4354',
        'all_routes_combined_v4303':'all_routes_combined_v4353','all_routes_combined_v4251':'all_routes_combined_v4303',
        'lil_B170_registration_v4302b':'lil_B171_registration_v4352',
        'all-routes-unified-v4303':'all-routes-unified-v4353','all-routes-unified-v4251':'all-routes-unified-v4303',
        'lil_B170_editorial':'lil_B171_editorial',
        "len(manifest['batches'])==546":"len(manifest['batches'])==547",
        'all546_manifest_batches_and114_accepted_layers_present':'all547_manifest_batches_and114_accepted_layers_present',
        'all_earlier_profiles_and_V4251_promotion_unchanged':'all_earlier_profiles_and_V4303_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4251':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4303',
        'manifest_batches=546':'manifest_batches=547','lil_B170_build_v4303':'lil_B171_build_v4353',
    }))
    tools.append(derive('scripts/run_lil_B170_startup_v4305.py','scripts/run_lil_B171_startup_v4355.py',{
        'lil_B170_runs_v4305':'lil_B171_runs_v4355','lil_B170_v4305':'lil_B171_v4355',
        'version=4303':'version=4353','B170':'B171',
    }))
    tools.append(derive('scripts/verify_lil_B170_startup_v4306.py','scripts/verify_lil_B171_startup_v4356.py',{
        'lil_B170_startup_v4306':'lil_B171_startup_v4356','lil_B170_runs_v4305':'lil_B171_runs_v4355',
        'all_routes_combined_v4303':'all_routes_combined_v4353','all_routes_combined_v4251':'all_routes_combined_v4303',
        'lil_B169_runs_v4253':'lil_B170_runs_v4305','V4251':'V4303','Current4303':'Current4353','B170':'B171',
    }))
    tools.append(derive('scripts/record_lil_B170_startup_view_v4306.py','scripts/record_lil_B171_startup_view_v4356.py',{
        'lil_B170_startup_v4306':'lil_B171_startup_v4356','V4251':'V4303','B170':'B171',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=547,accepted_layers=114,
        existing_V4303_promotion_preserved=True,release_verifier_requires_successful_terminal_builder=True,
        no_build_patch_or_startup_claim_yet=True,full_goal_complete=False))
    print('Prepared V4353 cumulative build/terminal-gated exact patch/fresh startup tools;547 batches expected;main V4303 preserved.')
