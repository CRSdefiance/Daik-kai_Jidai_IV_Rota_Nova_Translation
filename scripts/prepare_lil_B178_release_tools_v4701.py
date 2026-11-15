"""Prepare cumulative V4701, exact clean-input patch verification and current startup gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_release_tools_v4701');assert not ROOT.exists()
tools=[derive('scripts/build_lil_B177_v4655.py','scripts/build_lil_B178_v4701.py',{
    'lil_B177_build_v4655':'lil_B178_build_v4701','all_routes_combined_v4655':'all_routes_combined_v4701',
    'lil_B177_registration_v4654':'lil_B178_registration_v4700b','all-routes-unified-v4655':'all-routes-unified-v4701',
}),derive('scripts/verify_lil_B177_release_v4656.py','scripts/verify_lil_B178_release_v4702.py',{
    'lil_B177_editorial_v1':'lil_B178_editorial_v2','lil_B177_release_v4656':'lil_B178_release_v4702',
    'all_routes_combined_v4655':'all_routes_combined_v4701','all_routes_combined_v4595':'all_routes_combined_v4655',
    'lil_B177_registration_v4654':'lil_B178_registration_v4700b','lil_B177_build_v4655':'lil_B178_build_v4701',
    "manifest['profile']=='all-routes-unified-v4655'":"manifest['profile']=='all-routes-unified-v4701'",
    "registry['profiles']['all-routes-unified-v4595']":"registry['profiles']['all-routes-unified-v4655']",
    "len(manifest['batches'])==553":"len(manifest['batches'])==554",'all553':'all554','manifest_batches=553':'manifest_batches=554',
    'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4595':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4655',
    "assert result.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha":
        "assert result.read_bytes()==ROM.read_bytes()==Path('out/lil_B178_reference_v4686_RESEARCH_ONLY.nds').read_bytes() and sha(clean.read_bytes())==clean_sha",
    'lil_B177_editorial':'lil_B178_editorial',
}),derive('scripts/run_lil_B177_startup_v4657.py','scripts/run_lil_B178_startup_v4703.py',{
    'lil_B177_runs_v4657':'lil_B178_runs_v4703','lil_B177_v4657':'lil_B178_v4703','version=4655':'version=4701','B177':'B178',
}),derive('scripts/verify_lil_B177_startup_v4658.py','scripts/verify_lil_B178_startup_v4704.py',{
    'lil_B177_startup_v4658':'lil_B178_startup_v4704','lil_B177_runs_v4657':'lil_B178_runs_v4703',
    'all_routes_combined_v4655':'all_routes_combined_v4701','all_routes_combined_v4595':'all_routes_combined_v4655',
    'lil_B176_runs_v4597':'lil_B177_runs_v4657','V4595':'V4655','Current4655':'Current4701','B177':'B178',
}),derive('scripts/record_lil_B177_startup_view_v4658.py','scripts/record_lil_B178_startup_view_v4704.py',{
    'lil_B177_startup_v4658':'lil_B178_startup_v4704','V4595':'V4655','B177':'B178',
})]
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=554,accepted_layers=114,
    promoted_main_V4595_preserved=True,exact_patch_also_requires_whole_ROM_equal_reviewed_V4686=True,
    no_build_patch_orstartup_claim_yet=True,full_goal_complete=False))
print('Prepared V4701 sole cumulative builder, exact patch/current startup gates;main V4595 preserved.')
