"""Prepare sole-build, exact-patch and fresh-startup gates for cumulative V4496."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_release_tools_v4496')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/build_lil_B173_v4445.py','scripts/build_lil_B174_v4496.py',{
        'lil_B173_build_v4445':'lil_B174_build_v4496','all_routes_combined_v4445':'all_routes_combined_v4496',
        'lil_B173_registration_v4444':'lil_B174_registration_v4495','all-routes-unified-v4445':'all-routes-unified-v4496',
    }),derive('scripts/verify_lil_B173_release_v4446.py','scripts/verify_lil_B174_release_v4497.py',{
        'B173':'B174','lil_B173_release_v4446':'lil_B174_release_v4497',
        'all_routes_combined_v4445':'all_routes_combined_v4496','all_routes_combined_v4404':'all_routes_combined_v4445',
        'lil_B173_registration_v4444':'lil_B174_registration_v4495','lil_B173_build_v4445':'lil_B174_build_v4496',
        'all-routes-unified-v4445':'all-routes-unified-v4496','all-routes-unified-v4404':'all-routes-unified-v4445',
        'all-routes-unified-v4353':'all-routes-unified-v4445',
        "len(manifest['batches'])==549":"len(manifest['batches'])==550",'all549':'all550',
        'all_earlier_profiles_and_V4353_promotion_unchanged':'all_earlier_profiles_and_V4445_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4404':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4445',
        'manifest_batches=549':'manifest_batches=550',
    }),derive('scripts/run_lil_B173_startup_v4447.py','scripts/run_lil_B174_startup_v4498.py',{
        'lil_B173_runs_v4447':'lil_B174_runs_v4498','lil_B173_v4447':'lil_B174_v4498','version=4445':'version=4496','B173':'B174',
    }),derive('scripts/verify_lil_B173_startup_v4448.py','scripts/verify_lil_B174_startup_v4499.py',{
        'lil_B173_startup_v4448':'lil_B174_startup_v4499','lil_B173_runs_v4447':'lil_B174_runs_v4498',
        'all_routes_combined_v4445':'all_routes_combined_v4496','all_routes_combined_v4404':'all_routes_combined_v4445',
        'lil_B172_runs_v4406':'lil_B173_runs_v4447','V4404':'V4445','Current4445':'Current4496','B173':'B174',
    }),derive('scripts/record_lil_B173_startup_view_v4448.py','scripts/record_lil_B174_startup_view_v4499.py',{
        'lil_B173_startup_v4448':'lil_B174_startup_v4499','V4404':'V4445','B173':'B174',
    })]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=550,accepted_layers=114,
        existing_V4445_promotion_preserved=True,exact_patch_verifier_requires_successful_terminal_builder=True,
        no_build_patch_orstartup_claim_yet=True,full_goal_complete=False))
    print('Prepared V4496 sole cumulative build, clean-input patch and startup tools;550 batches expected, main V4445 preserved.')
