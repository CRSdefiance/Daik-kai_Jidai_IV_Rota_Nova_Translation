"""Prepare terminal-gated cumulative build,exact patch and fresh startup tools."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_release_tools_v4445')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/build_lil_B172_v4404.py','scripts/build_lil_B173_v4445.py',{
        'lil_B172_build_v4404':'lil_B173_build_v4445','all_routes_combined_v4404':'all_routes_combined_v4445',
        'lil_B172_registration_v4403':'lil_B173_registration_v4444','all-routes-unified-v4404':'all-routes-unified-v4445',
    })]
    tools.append(derive('scripts/verify_lil_B172_release_v4405.py','scripts/verify_lil_B173_release_v4446.py',{
        'B172':'B173','lil_B172_release_v4405':'lil_B173_release_v4446',
        'all_routes_combined_v4404':'all_routes_combined_v4445','all_routes_combined_v4353':'all_routes_combined_v4404',
        'lil_B172_registration_v4403':'lil_B173_registration_v4444','lil_B172_build_v4404':'lil_B173_build_v4445',
        'all-routes-unified-v4404':'all-routes-unified-v4445','all-routes-unified-v4353':'all-routes-unified-v4404',
        "registry['latest_promoted_build']['profile']=='all-routes-unified-v4353'":"registry['latest_promoted_build']['profile']=='all-routes-unified-v4353'",
        "len(manifest['batches'])==548":"len(manifest['batches'])==549",'all548':'all549',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4353':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4404',
        'manifest_batches=548':'manifest_batches=549',
    }))
    tools.append(derive('scripts/run_lil_B172_startup_v4406.py','scripts/run_lil_B173_startup_v4447.py',{
        'lil_B172_runs_v4406':'lil_B173_runs_v4447','lil_B172_v4406':'lil_B173_v4447',
        'version=4404':'version=4445','B172':'B173',
    }))
    tools.append(derive('scripts/verify_lil_B172_startup_v4407.py','scripts/verify_lil_B173_startup_v4448.py',{
        'lil_B172_startup_v4407':'lil_B173_startup_v4448','lil_B172_runs_v4406':'lil_B173_runs_v4447',
        'all_routes_combined_v4404':'all_routes_combined_v4445','all_routes_combined_v4353':'all_routes_combined_v4404',
        'lil_B171_runs_v4355':'lil_B172_runs_v4406','V4353':'V4404','Current4404':'Current4445','B172':'B173',
    }))
    tools.append(derive('scripts/record_lil_B172_startup_view_v4407.py','scripts/record_lil_B173_startup_view_v4448.py',{
        'lil_B172_startup_v4407':'lil_B173_startup_v4448','V4353':'V4404','B172':'B173',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=549,accepted_layers=114,
        existing_V4353_promotion_preserved=True,exact_patch_verifier_requires_successful_terminal_builder=True,
        no_build_patch_or_startup_claim_yet=True,full_goal_complete=False))
    print('Prepared V4445 cumulative build/exact patch/fresh startup tools;549 batches expected;mainV4353 preserved.')
