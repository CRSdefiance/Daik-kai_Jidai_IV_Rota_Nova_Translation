"""Prepare immutable cumulative builder, reconstruction and startup runners from their last verified versions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_release_runner_tools_v6641')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/build_lil_B211_v6584.py','scripts/build_lil_B212_v6641.py',{'B211':'B212','build_v6584':'build_v6641','registration_v6583':'registration_v6640','all_routes_combined_v6584':'all_routes_combined_v6641','all-routes-unified-v6584':'all-routes-unified-v6641'}))
    proofs.append(derive('scripts/run_lil_B211_regressions_v6584.py','scripts/run_lil_B212_regressions_v6641.py',{'lil_B211_regressions_v6584':'lil_B212_regressions_v6641'}))
    proofs.append(derive('scripts/verify_lil_B211_release_v6585.py','scripts/verify_lil_B212_release_v6642.py',{'lil_B211_editorial_v2':'lil_B212_editorial_v2','B211':'B212','release_v6585':'release_v6642','build_v6584':'build_v6641','all_routes_combined_v6584':'all_routes_combined_v6641','all_routes_combined_v6541':'all_routes_combined_v6584','registration_v6583':'registration_v6640','all-routes-unified-v6584':'all-routes-unified-v6641','all-routes-unified-v6541':'all-routes-unified-v6584','==603':'==604','manifest_batches=603':'manifest_batches=604','all603_manifest_batches':'all604_manifest_batches','reference_v6566':'reference_v6624','V6541':'V6584',"b\"profile_config.get('Al_Ferid_name')\"":"b\"profile_config.get('lil_B211_editorial')\""}))
    proofs.append(derive('scripts/pin_lil_B211_v6586.py','scripts/pin_lil_B212_v6643.py',{'B211':'B212','retention_v6586':'retention_v6643','release_v6585':'release_v6642','V6584':'V6641'}))
    proofs.append(derive('scripts/run_lil_B211_startup_v6587.py','scripts/run_lil_B212_startup_v6644.py',{'B211':'B212','runs_v6587':'runs_v6644','v6587_':'v6644_','version=6584':'version=6641'}))
    proofs.append(derive('scripts/verify_lil_B211_startup_v6588.py','scripts/verify_lil_B212_startup_v6645.py',{'B211':'B212','startup_v6588':'startup_v6645','runs_v6587':'runs_v6644','all_routes_combined_v6584':'all_routes_combined_v6641','all_routes_combined_v6541':'all_routes_combined_v6584','B210_Ferid_runs_v6543':'lil_B211_runs_v6587','V6541':'V6584','Current6584':'Current6641'}))
    proofs.append(derive('scripts/record_lil_B211_startup_view_v6588.py','scripts/record_lil_B212_startup_view_v6645.py',{'B211':'B212','startup_v6588':'startup_v6645','V6541':'V6584'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_runners.json',dict(proofs=proofs,all_original_native_constants_and_previous_producers_preserved=True,current_startup_not_repeated_content_boots=True,full_goal_complete=False));print('Seven immutable B212 release runners prepared.')
