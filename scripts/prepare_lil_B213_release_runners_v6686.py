"""Prepare immutable cumulative build, patch reconstruction, regression and current-startup runners."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_release_runner_tools_v6686')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/build_lil_B212_v6641.py','scripts/build_lil_B213_v6686.py',{'B212':'B213','build_v6641':'build_v6686','registration_v6640':'registration_v6685','all_routes_combined_v6641':'all_routes_combined_v6686','all-routes-unified-v6641':'all-routes-unified-v6686'}))
    proofs.append(derive('scripts/run_lil_B212_regressions_v6641.py','scripts/run_lil_B213_regressions_v6686.py',{'lil_B212_regressions_v6641':'lil_B213_regressions_v6686'}))
    proofs.append(derive('scripts/verify_lil_B212_release_v6642.py','scripts/verify_lil_B213_release_v6687.py',{'lil_B212_editorial_v2':'lil_B213_editorial_v1','B212':'B213','release_v6642':'release_v6687','build_v6641':'build_v6686','all_routes_combined_v6641':'all_routes_combined_v6686','all_routes_combined_v6584':'all_routes_combined_v6641','registration_v6640':'registration_v6685','all-routes-unified-v6641':'all-routes-unified-v6686','all-routes-unified-v6584':'all-routes-unified-v6641','==604':'==605','manifest_batches=604':'manifest_batches=605','all604_manifest_batches':'all605_manifest_batches','reference_v6624':'reference_v6673','V6584':'V6641',"b\"profile_config.get('lil_B211_editorial')\"":"b\"profile_config.get('lil_B212_editorial')\""}))
    proofs.append(derive('scripts/pin_lil_B212_v6643.py','scripts/pin_lil_B213_v6688.py',{'B212':'B213','retention_v6643':'retention_v6688','release_v6642':'release_v6687','V6641':'V6686'}))
    proofs.append(derive('scripts/run_lil_B212_startup_v6644.py','scripts/run_lil_B213_startup_v6689.py',{'B212':'B213','runs_v6644':'runs_v6689','v6644_':'v6689_','version=6641':'version=6686'}))
    proofs.append(derive('scripts/verify_lil_B212_startup_v6645.py','scripts/verify_lil_B213_startup_v6690.py',{'B212':'B213','startup_v6645':'startup_v6690','runs_v6644':'runs_v6689','all_routes_combined_v6641':'all_routes_combined_v6686','all_routes_combined_v6584':'all_routes_combined_v6641','lil_B211_runs_v6587':'lil_B212_runs_v6644','V6584':'V6641','Current6641':'Current6686'}))
    proofs.append(derive('scripts/record_lil_B212_startup_view_v6645.py','scripts/record_lil_B213_startup_view_v6690.py',{'B212':'B213','startup_v6645':'startup_v6690','V6584':'V6641'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_runners.json',dict(proofs=proofs,all_original_native_constants_and_previous_producers_preserved=True,current_startup_not_repeated_content_boots=True,full_goal_complete=False));print('Seven immutable B213 release runners prepared.')
