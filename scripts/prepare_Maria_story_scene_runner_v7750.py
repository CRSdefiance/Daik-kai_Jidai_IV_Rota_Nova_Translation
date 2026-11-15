"""Freeze identical ordinary-input observer runs for all three full story fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_scene_runner_tools_v7750');assert not root.exists()
    result=derive('scripts/run_Maria_B207_scenes_v7705.py','scripts/run_Maria_story_scenes_v7750.py',{
        'maria_B207_scene_runs_v7705':'maria_story_scene_runs_v7750',
        'maria_B207_scene_fixtures_v7704/Maria_two_complete_source_English_original_prelude_fixtures':
        'maria_story_scene_fixtures_v7749/six_complete_source_English_original_prelude_fixtures',
        'args=ap.parse_args()':"ap.add_argument('--block',type=int,choices=[34,108,35],required=True);args=ap.parse_args()",
        'route,version=args.route,args.version':'route,version,block=args.route,args.version,args.block',
        "if f['route']==route and f['version']==version":"if f['route']==route and f['version']==version and f['source_block']==block",
        "ROOT/f'route{route}_{version}'":"ROOT/f'route{route}_B{block}_{version}'",
        'Maria_B207_route{route}_{version}_v7705':'Maria_story_B{block}_route{route}_{version}_v7750',
        'original_exchange_commands=20,original_exchange_speeches=18':
        "original_exchange_commands=len(selected['all_original_exchange_commands']),original_exchange_speeches=len(selected['original_text_records'])",
        'route{route} {version}:16001-frame':'route{route} B{block} {version}:16001-frame',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,original_observer_andall_native_high_constants_preserved=True,
        original16001_frame_schedule_A4200_and240frame_A_intervals_unchanged=True,source_English_inputs_identical=True,
        source_branch_conditions_roster_roles_RNG_andresults_unforced=True,new_credit=0,full_goal_complete=False))
    print('Frozen source-owned ordinary16001-frame fixture runner forB34/B108/B35;source/English controller schedule unchanged.')
