"""Prepare immutable cumulative release, reconstruction, regression and representative startup runners."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_release_runner_tools_v6584')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/build_lil_B209_v6488.py','scripts/build_lil_B211_v6584.py',{'B209':'B211','build_v6488':'build_v6584','registration_v6487':'registration_v6583','all_routes_combined_v6488':'all_routes_combined_v6584','all-routes-unified-v6488':'all-routes-unified-v6584'}))
    proofs.append(derive('scripts/run_lil_B209_regressions_v6488.py','scripts/run_lil_B211_regressions_v6584.py',{'lil_B209_regressions_v6488':'lil_B211_regressions_v6584'}))
    proofs.append(derive('scripts/verify_lil_B209_release_v6489.py','scripts/verify_lil_B211_release_v6585.py',{'lil_B209_editorial_v3':'lil_B211_editorial_v2','B209':'B211','release_v6489':'release_v6585','build_v6488':'build_v6584','all_routes_combined_v6488':'all_routes_combined_v6584','all_routes_combined_v6439':'all_routes_combined_v6541','registration_v6487':'registration_v6583','all-routes-unified-v6488':'all-routes-unified-v6584','all-routes-unified-v6439':'all-routes-unified-v6541','==600':'==603','manifest_batches=600':'manifest_batches=603','all600_manifest_batches':'all603_manifest_batches','reference_v6468':'reference_v6566','V6439':'V6541','lil_B208_editorial':'Al_Ferid_name'}))
    proofs.append(derive('scripts/pin_lil_B209_v6490.py','scripts/pin_lil_B211_v6586.py',{'B209':'B211','retention_v6490':'retention_v6586','release_v6489':'release_v6585','V6488':'V6584'}))
    proofs.append(derive('scripts/run_lil_B209_startup_v6491.py','scripts/run_lil_B211_startup_v6587.py',{'B209':'B211','runs_v6491':'runs_v6587','v6491_':'v6587_','version=6488':'version=6584'}))
    proofs.append(derive('scripts/verify_lil_B209_startup_v6492.py','scripts/verify_lil_B211_startup_v6588.py',{'B209':'B211','startup_v6492':'startup_v6588','runs_v6491':'runs_v6587','all_routes_combined_v6488':'all_routes_combined_v6584','all_routes_combined_v6439':'all_routes_combined_v6541','lil_B208_runs_v6442':'B210_Ferid_runs_v6543','V6439':'V6541','Current6488':'Current6584'}))
    proofs.append(derive('scripts/record_lil_B209_startup_view_v6492.py','scripts/record_lil_B211_startup_view_v6588.py',{'B209':'B211','startup_v6492':'startup_v6588','V6439':'V6541'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_runners.json',dict(proofs=proofs,all_original_native_constants_and_previous_producers_preserved=True,new_current_startup_not_repeated_content_boots=True,full_goal_complete=False));print('Seven B211 release runners prepared;prior producers/native constants preserved.')
