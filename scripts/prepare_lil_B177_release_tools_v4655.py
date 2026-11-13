"""Prepare the sole cumulative builder, exact patch gate and current startup tests."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_release_tools_v4655')
assert not ROOT.exists()
tools=[derive('scripts/build_lil_B176_v4595.py','scripts/build_lil_B177_v4655.py',{
    'lil_B176_build_v4595':'lil_B177_build_v4655','all_routes_combined_v4595':'all_routes_combined_v4655',
    'lil_B176_registration_v4594':'lil_B177_registration_v4654','all-routes-unified-v4595':'all-routes-unified-v4655',
}),derive('scripts/verify_lil_B176_release_v4596.py','scripts/verify_lil_B177_release_v4656.py',{
    'lil_B176_editorial_v2':'lil_B177_editorial_v1','lil_B176_release_v4596':'lil_B177_release_v4656',
    'all_routes_combined_v4595':'all_routes_combined_v4655','all_routes_combined_v4541':'all_routes_combined_v4595',
    'lil_B176_registration_v4594':'lil_B177_registration_v4654','lil_B176_build_v4595':'lil_B177_build_v4655',
    'all-routes-unified-v4595':'all-routes-unified-v4655','all-routes-unified-v4541':'all-routes-unified-v4595',
    "len(manifest['batches'])==552":"len(manifest['batches'])==553",'all552':'all553',
    'manifest_batches=552':'manifest_batches=553','lil_B176_editorial':'lil_B177_editorial','V4541':'V4595',
}),derive('scripts/run_lil_B176_startup_v4597.py','scripts/run_lil_B177_startup_v4657.py',{
    'lil_B176_runs_v4597':'lil_B177_runs_v4657','lil_B176_v4597':'lil_B177_v4657','version=4595':'version=4655','B176':'B177',
}),derive('scripts/verify_lil_B176_startup_v4598.py','scripts/verify_lil_B177_startup_v4658.py',{
    'lil_B176_startup_v4598':'lil_B177_startup_v4658','lil_B176_runs_v4597':'lil_B177_runs_v4657',
    'all_routes_combined_v4595':'all_routes_combined_v4655','all_routes_combined_v4541':'all_routes_combined_v4595',
    'lil_B175_runs_v4543':'lil_B176_runs_v4597','V4541':'V4595','Current4595':'Current4655','B176':'B177',
}),derive('scripts/record_lil_B176_startup_view_v4598.py','scripts/record_lil_B177_startup_view_v4658.py',{
    'lil_B176_startup_v4598':'lil_B177_startup_v4658','V4541':'V4595','B176':'B177',
})]
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=553,accepted_layers=114,
    existing_V4595_promotion_preserved=True,no_build_patch_orstartup_claim_yet=True,full_goal_complete=False))
print('Prepared V4655 cumulative builder,exact patch,current New Game/town cold boots and verification.')
