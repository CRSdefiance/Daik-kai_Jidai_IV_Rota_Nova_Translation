"""Prepare identical-input read-only source/English scene captures for B47 pagination."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_runner_tools_v7998')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/run_Rafael_B45_scenes_v7893.py','scripts/run_Rafael_B47_scenes_v7998.py',{
        'Rafael_B45_scene_runs_v7893':'Rafael_B47_scene_runs_v7998',
        'Rafael_B45_scene_fixtures_v7892':'Rafael_B47_scene_fixtures_v7997',
        'Rafael_B45_route':'Rafael_B47_route',
        '_v7893':'_v7998',
        'original_exchange_commands=24,original_exchange_speeches=12':'original_exchange_commands=48,original_exchange_speeches=15',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        full_original48_command_block_not_linearized_orcondition_forced=True,
        identical_ordinary_inputs_include_A_at4000_then_every240_frames=True,
        extra_English_R53_page_not_controller_retimed=True,
        selected_path_must_be_observed_not_assumed_from_native_composition=True,
        new_credit=0,full_goal_complete=False))
    print('Prepared full B47 paired16001-frame read-only runner;identical ordinary inputs,observed path andR53 page-turn analysis pending.')
