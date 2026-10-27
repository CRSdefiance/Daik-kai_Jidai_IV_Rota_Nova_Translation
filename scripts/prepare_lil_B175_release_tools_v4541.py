"""Prepare registered V4541 build, exact-patch and current startup verification gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B175_release_tools_v4541')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/build_lil_B174_v4496.py','scripts/build_lil_B175_v4541.py',{
        'lil_B174_build_v4496':'lil_B175_build_v4541','all_routes_combined_v4496':'all_routes_combined_v4541',
        'lil_B174_registration_v4495':'lil_B175_registration_v4540b','all-routes-unified-v4496':'all-routes-unified-v4541',
    }),derive('scripts/verify_lil_B174_release_v4497.py','scripts/verify_lil_B175_release_v4542.py',{
        'lil_B174_editorial_v1':'lil_B175_editorial_v2','lil_B174_release_v4497':'lil_B175_release_v4542',
        'all_routes_combined_v4496':'all_routes_combined_v4541','all_routes_combined_v4445':'all_routes_combined_v4496',
        'lil_B174_registration_v4495':'lil_B175_registration_v4540b','lil_B174_build_v4496':'lil_B175_build_v4541',
        'all-routes-unified-v4496':'all-routes-unified-v4541','all-routes-unified-v4445':'all-routes-unified-v4496',
        "len(manifest['batches'])==550":"len(manifest['batches'])==551",'all550':'all551',
        'all_earlier_profiles_and_V4445_promotion_unchanged':'all_earlier_profiles_and_V4496_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4445':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4496',
        'manifest_batches=550':'manifest_batches=551','lil_B174_editorial':'lil_B175_editorial',
    }),derive('scripts/run_lil_B174_startup_v4498.py','scripts/run_lil_B175_startup_v4543.py',{
        'lil_B174_runs_v4498':'lil_B175_runs_v4543','lil_B174_v4498':'lil_B175_v4543','version=4496':'version=4541','B174':'B175',
    }),derive('scripts/verify_lil_B174_startup_v4499.py','scripts/verify_lil_B175_startup_v4544.py',{
        'lil_B174_startup_v4499':'lil_B175_startup_v4544','lil_B174_runs_v4498':'lil_B175_runs_v4543',
        'all_routes_combined_v4496':'all_routes_combined_v4541','all_routes_combined_v4445':'all_routes_combined_v4496',
        'lil_B173_runs_v4447':'lil_B174_runs_v4498','V4445':'V4496','Current4496':'Current4541','B174':'B175',
    }),derive('scripts/record_lil_B174_startup_view_v4499.py','scripts/record_lil_B175_startup_view_v4544.py',{
        'lil_B174_startup_v4499':'lil_B175_startup_v4544','V4445':'V4496','B174':'B175',
    })]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=551,accepted_layers=114,
        existing_V4496_promotion_preserved=True,exact_patch_verifier_requires_successful_terminal_builder=True,
        no_build_patch_orstartup_claim_yet=True,full_goal_complete=False))
    print('Prepared V4541 sole cumulative build,exact clean-input patch and current startup gates;551 batches expected,main V4496 preserved.')
