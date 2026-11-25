"""Source-locked original readonly whole-exchange capture harness, captain1 only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_scene_run_tools_v8280')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/run_Gerhard_scenes_v8225.py','scripts/run_Hodram_scenes_v8280.py',{
        'Paired previous/revised English full-script entry fixtures;ordinary identical inputs andreadonly traces.':'Paired clean/revised Hodram whole-script entry fixtures;ordinary identical inputs andreadonly traces.',
        'Gerhard_scene_runs_v8225':'Hodram_scene_runs_v8280',
        'work/analysis/Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json':'work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json',
        'choices=[2]':'choices=[1]', 'choices=[27,74]':'choices=[137,45,46]',
        "choices=['parent_English','revised_English']":"choices=['clean_Japanese','revised_English']",
        'route,version,block=args.route,args.version,args.block;selected=':'route,version,block=args.route,args.version,args.block;frames={137:24001,45:10001,46:16001}[block];selected=',
        "f'Gerhard_B{block}_route{route}_{version}_v8225'":"f'Hodram_B{block}_route{route}_{version}_v8280'",
        'work/analysis/lil_B111_B119_runs_v3253/newgame_inputs.json':'work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json',
        'range(4000,31521,240)':'range(4000,frames-480,240)',
        'range(2350,32001,60)':'range(2350,frames,60)', '{32000}':'{frames-1}',
        'frames=32001':'frames=frames', "'32001'":"str(frames)", "==32001":"==frames",
        'no_controller_retiming_between_previous_andrevised_English':'no_controller_retiming_between_clean_Japanese_andrevised_English',
        ':32001-frame fixture capture terminal':':{frames}-frame fixture capture terminal',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_capture_harness.json',dict(derivation=result,
        identical_original_readonly_observer_andnative_constants_preserved=True,
        frames_by_block={137:24001,45:10001,46:16001},six_runs_total_frames=100006,
        no_inputs_retimed_to_text_orforced_state=True,full_goal_complete=False))
    print('Hodram readonly capture successor prepared: six paired whole-script runs,100006 frames total.')
