"""Prepare cumulative V4595 build, exact clean-input patch and fresh startup gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_release_tools_v4595')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/build_lil_B175_v4541.py','scripts/build_lil_B176_v4595.py',{
        'lil_B175_build_v4541':'lil_B176_build_v4595','all_routes_combined_v4541':'all_routes_combined_v4595',
        'lil_B175_registration_v4540b':'lil_B176_registration_v4594','all-routes-unified-v4541':'all-routes-unified-v4595',
    }),derive('scripts/verify_lil_B175_release_v4542.py','scripts/verify_lil_B176_release_v4596.py',{
        'lil_B175_editorial_v2':'lil_B176_editorial_v2','lil_B175_release_v4542':'lil_B176_release_v4596',
        'all_routes_combined_v4541':'all_routes_combined_v4595','all_routes_combined_v4496':'all_routes_combined_v4541',
        'lil_B175_registration_v4540b':'lil_B176_registration_v4594','lil_B175_build_v4541':'lil_B176_build_v4595',
        'all-routes-unified-v4541':'all-routes-unified-v4595','all-routes-unified-v4496':'all-routes-unified-v4541',
        "len(manifest['batches'])==551":"len(manifest['batches'])==552",'all551':'all552',
        'all_earlier_profiles_and_V4496_promotion_unchanged':'all_earlier_profiles_and_V4541_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4496':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4541',
        'manifest_batches=551':'manifest_batches=552','lil_B175_editorial':'lil_B176_editorial',
    }),derive('scripts/run_lil_B175_startup_v4543.py','scripts/run_lil_B176_startup_v4597.py',{
        'lil_B175_runs_v4543':'lil_B176_runs_v4597','lil_B175_v4543':'lil_B176_v4597','version=4541':'version=4595','B175':'B176',
    }),derive('scripts/verify_lil_B175_startup_v4544.py','scripts/verify_lil_B176_startup_v4598.py',{
        'lil_B175_startup_v4544':'lil_B176_startup_v4598','lil_B175_runs_v4543':'lil_B176_runs_v4597',
        'all_routes_combined_v4541':'all_routes_combined_v4595','all_routes_combined_v4496':'all_routes_combined_v4541',
        'lil_B174_runs_v4498':'lil_B175_runs_v4543','V4496':'V4541','Current4541':'Current4595','B175':'B176',
    }),derive('scripts/record_lil_B175_startup_view_v4544.py','scripts/record_lil_B176_startup_view_v4598.py',{
        'lil_B175_startup_v4544':'lil_B176_startup_v4598','V4496':'V4541','B175':'B176',
    })]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=552,accepted_layers=114,
        existing_V4541_promotion_preserved=True,exact_patch_verifier_requires_successful_terminal_builder=True,
        no_build_patch_orstartup_claim_yet=True,full_goal_complete=False))
    print('Prepared V4595 sole cumulative build,exact clean-input patch and current startup gates;552 batches expected,main V4541 preserved.')
