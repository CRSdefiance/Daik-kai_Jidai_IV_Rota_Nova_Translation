"""Prepare one registered cumulative build,terminal-gated patch audit and startup."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_release_tools_v4404')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/build_lil_B171_v4353.py','scripts/build_lil_B172_v4404.py',{
        'lil_B171_build_v4353':'lil_B172_build_v4404','all_routes_combined_v4353':'all_routes_combined_v4404',
        'lil_B171_registration_v4352':'lil_B172_registration_v4403','all-routes-unified-v4353':'all-routes-unified-v4404',
    })]
    tools.append(derive('scripts/verify_lil_B171_release_v4354.py','scripts/verify_lil_B172_release_v4405.py',{
        'B171':'B172','lil_B171_release_v4354':'lil_B172_release_v4405',
        'all_routes_combined_v4353':'all_routes_combined_v4404','all_routes_combined_v4303':'all_routes_combined_v4353',
        'lil_B171_registration_v4352':'lil_B172_registration_v4403',
        'all-routes-unified-v4353':'all-routes-unified-v4404','all-routes-unified-v4303':'all-routes-unified-v4353',
        'lil_B171_build_v4353':'lil_B172_build_v4404',
        "len(manifest['batches'])==547":"len(manifest['batches'])==548",'all547':'all548',
        'V4303':'V4353','manifest_batches=547':'manifest_batches=548',
    }))
    tools.append(derive('scripts/run_lil_B171_startup_v4355.py','scripts/run_lil_B172_startup_v4406.py',{
        'lil_B171_runs_v4355':'lil_B172_runs_v4406','lil_B171_v4355':'lil_B172_v4406',
        'version=4353':'version=4404','B171':'B172',
    }))
    tools.append(derive('scripts/verify_lil_B171_startup_v4356.py','scripts/verify_lil_B172_startup_v4407.py',{
        'lil_B171_startup_v4356':'lil_B172_startup_v4407','lil_B171_runs_v4355':'lil_B172_runs_v4406',
        'all_routes_combined_v4353':'all_routes_combined_v4404','all_routes_combined_v4303':'all_routes_combined_v4353',
        'lil_B170_runs_v4305':'lil_B171_runs_v4355','V4303':'V4353','Current4353':'Current4404','B171':'B172',
    }))
    tools.append(derive('scripts/record_lil_B171_startup_view_v4356.py','scripts/record_lil_B172_startup_view_v4407.py',{
        'lil_B171_startup_v4356':'lil_B172_startup_v4407','V4303':'V4353','B171':'B172',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=548,accepted_layers=114,
        existing_V4353_promotion_preserved=True,release_verifier_requires_successful_terminal_builder=True,
        no_build_patch_or_startup_claim_yet=True,full_goal_complete=False))
    print('Prepared V4404 cumulative build,exact patch and fresh startup tools;548 batches expected;main V4353 preserved.')
