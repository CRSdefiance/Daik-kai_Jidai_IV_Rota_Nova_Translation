"""Repeat exact B50 inputs only to sample a concrete later-state difference at bounded phases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_risk_tools_v8159')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/run_Rafael_B50_scenes_v8155.py','scripts/run_Rafael_B50_risk_v8159.py',{
        'Rafael_B50_scene_runs_v8155':'Rafael_B50_risk_runs_v8159',
        'Rafael_B50_route':'Rafael_B50_risk_route','_v8155':'_v8159',
        'captures=sorted(set(range(2350,16001,60))|{16000})':'captures=[3970,5170,5770,10930,11890,15310,15550,16000]',
        "'--dump-ram']":"'--dump-capture-ram','--dump-ram']",
        'body/header/return/transition analysis pending;zero credit.':'bounded picture/postreturn/later-state risk analysis pending;zero credit.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=receipt,
        concrete_risk='Later final models,actors,towns and17of87RGB samples differ after all28 B50 speeches andnormalreturn;locate earlier versuslater sampled state without claiming a complete causal trace.',
        exact_existing_fixtures_inputs_and16001frame_horizon=True,only_capture_RAM_export_schedule_added=True,
        readonly_observation_no_RNG_state_orinput_retiming=True,no_new_prose_orcredit=True,
        no_exhaustive_playthrough_orbroad_simulation_equivalence_claim=True,full_goal_complete=False))
    print('Prepared bounded B50 picture/postreturn/later-state sampling with exact earlier inputs andfixtures.')
