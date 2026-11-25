"""Prepare cumulative V4749, exact clean-input patch and fresh startup verification."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_release_tools_v4749')
assert not ROOT.exists()
tools=[derive('scripts/build_lil_B178_v4701.py','scripts/build_lil_B179_v4749.py',{
    'lil_B178_build_v4701':'lil_B179_build_v4749','all_routes_combined_v4701':'all_routes_combined_v4749',
    'lil_B178_registration_v4700b':'lil_B179_registration_v4748','all-routes-unified-v4701':'all-routes-unified-v4749',
}),derive('scripts/verify_lil_B178_release_v4702.py','scripts/verify_lil_B179_release_v4750.py',{
    'lil_B178_editorial_v2':'lil_B179_editorial_v1','lil_B178_release_v4702':'lil_B179_release_v4750',
    'all_routes_combined_v4701':'all_routes_combined_v4749','all_routes_combined_v4655':'all_routes_combined_v4701',
    'lil_B178_registration_v4700b':'lil_B179_registration_v4748','lil_B178_build_v4701':'lil_B179_build_v4749',
    "manifest['profile']=='all-routes-unified-v4701'":"manifest['profile']=='all-routes-unified-v4749'",
    "registry['profiles']['all-routes-unified-v4655']":"registry['profiles']['all-routes-unified-v4701']",
    "registry['latest_promoted_build']['profile']=='all-routes-unified-v4595'":
        "registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'",
    "len(manifest['batches'])==554":"len(manifest['batches'])==555",'all554':'all555','manifest_batches=554':'manifest_batches=555',
    'all_earlier_profiles_and_V4595_promotion_unchanged':'all_earlier_profiles_and_V4701_promotion_unchanged',
    'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4655':
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4701',
    'out/lil_B178_reference_v4686_RESEARCH_ONLY.nds':'out/lil_B179_reference_v4734_RESEARCH_ONLY.nds',
    'lil_B178_editorial':'lil_B179_editorial',
}),derive('scripts/run_lil_B178_startup_v4703.py','scripts/run_lil_B179_startup_v4751.py',{
    'lil_B178_runs_v4703':'lil_B179_runs_v4751','lil_B178_v4703':'lil_B179_v4751','version=4701':'version=4749','B178':'B179',
}),derive('scripts/verify_lil_B178_startup_v4704.py','scripts/verify_lil_B179_startup_v4752.py',{
    'lil_B178_startup_v4704':'lil_B179_startup_v4752','lil_B178_runs_v4703':'lil_B179_runs_v4751',
    'all_routes_combined_v4701':'all_routes_combined_v4749','all_routes_combined_v4655':'all_routes_combined_v4701',
    'lil_B177_runs_v4657':'lil_B178_runs_v4703','V4655':'V4701','Current4701':'Current4749','B178':'B179',
}),derive('scripts/record_lil_B178_startup_view_v4704.py','scripts/record_lil_B179_startup_view_v4752.py',{
    'lil_B178_startup_v4704':'lil_B179_startup_v4752','V4655':'V4701','B178':'B179',
})]
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=555,accepted_layers=114,
    promoted_main_V4701_preserved=True,exact_patch_requires_whole_ROM_equal_reviewed_V4734=True,
    no_build_patch_orstartup_claim_yet=True,full_goal_complete=False))
print('Prepared sole V4749 cumulative build,exact patch and fresh startup gates;main V4701 preserved.')
