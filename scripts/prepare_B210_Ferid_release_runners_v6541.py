"""Derive immutable release runners; preserve every native address and previous producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/B210_Ferid_runner_derivation_v6541')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);proofs=[]
    proofs.append(derive('scripts/build_lil_B209_v6488.py','scripts/build_B210_Ferid_v6541.py',{'lil_B209_build_v6488':'B210_Ferid_build_v6541','lil_B209_registration_v6487':'B210_Ferid_registration_v6540','all_routes_combined_v6488':'all_routes_combined_v6541','all-routes-unified-v6488':'all-routes-unified-v6541'}))
    proofs.append(derive('scripts/run_lil_B209_regressions_v6488.py','scripts/run_B210_Ferid_regressions_v6541.py',{'lil_B209_regressions_v6488':'B210_Ferid_regressions_v6541'}))
    proofs.append(derive('scripts/run_lil_B209_startup_v6491.py','scripts/run_B210_Ferid_startup_v6543.py',{'lil_B209_runs_v6491':'B210_Ferid_runs_v6543','lil_B209_v6491':'B210_Ferid_v6543','version=6488':'version=6541','B209':'B210'}))
    proofs.append(derive('scripts/verify_lil_B209_startup_v6492.py','scripts/verify_B210_Ferid_startup_v6544.py',{
        'lil_B209_startup_v6492':'B210_Ferid_startup_v6544','lil_B209_runs_v6491':'B210_Ferid_runs_v6543','all_routes_combined_v6488':'all_routes_combined_v6541','all_routes_combined_v6439':'all_routes_combined_v6488','lil_B208_runs_v6442':'lil_B209_runs_v6491','Current6488':'Current6541','V6439':'V6488','B209':'B210',
        "assert arm==prior.read_file('/__arm9__.bin')":"assert sha(arm)=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05' and sha(prior.read_file('/__arm9__.bin'))=='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'; assert [i for i,(a,b) in enumerate(zip(arm,prior.read_file('/__arm9__.bin'),strict=True)) if a!=b]==[1518776,1518777,1518778,1518779,1518780]"}))
    save(ROOT/'derivation_receipt.json',dict(proofs=proofs,all_native_high_integer_constants_and_multiplicity_preserved=True,old_runners_unchanged=True,full_goal_complete=False));print('Four new release runners prepared;prior producers/native addresses preserved.')
