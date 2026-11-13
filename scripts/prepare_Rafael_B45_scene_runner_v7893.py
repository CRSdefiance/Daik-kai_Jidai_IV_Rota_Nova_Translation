"""Reuse the original readonly observer and identical ordinary inputs for the twelve-line paired test."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_scene_tools_v7893');assert not root.exists()
    result=derive('scripts/run_papal_trade_scenes_v7649.py','scripts/run_Rafael_B45_scenes_v7893.py',{
        'work/analysis/papal_trade_scene_runs_v7649':'work/analysis/Rafael_B45_scene_runs_v7893',
        'work/analysis/papal_trade_scene_fixtures_v7648/four_complete_source_English_original_route_prelude_fixtures.json':
        'work/analysis/Rafael_B45_scene_fixtures_v7892/two_complete_source_English_original_Rafael_prelude_fixtures.json',
        'choices=[0,1]':'choices=[0]',
        "f'papal_trade_route{route}_{version}_v7649'":"f'Rafael_B45_route{route}_{version}_v7893'",
        'original_exchange_commands=20,original_exchange_speeches=18':'original_exchange_commands=24,original_exchange_speeches=12',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        all_original_native_high_constants_observer_instruction_contract_input_andreadonly_guards_preserved=True,
        no_retiming_orcondition_state_forcing=True,paired16001_frame_jobs_no_actual_coverage_claim_until_observed=True,
        new_credit=0,full_goal_complete=False))
