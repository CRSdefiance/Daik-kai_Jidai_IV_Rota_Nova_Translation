"""Source-lock disjoint read-only menu/command observation for both bounded-tail choices."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_tail_tools_v8416');assert not root.exists()
    result=derive('scripts/run_Rafael_B46_scenes_v7945.py','scripts/run_Hodram_B49_tail_v8416.py',{
        'Full B46 entry fixtures, ordinary choices':'Bounded original B49 possession-dialogue tail fixtures, ordinary choices',
        'Rafael_B46_scene_runs_v7945':'Hodram_B49_tail_runs_v8416',
        'work/analysis/Rafael_B46_scene_fixtures_v7944/two_complete_source_English_original_Rafael_prelude_fixtures.json':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
        'MENU_SNAPSHOT_FRAMES=[4810,4870,4930]':'MENU_SNAPSHOT_FRAMES=[4310,4370,4430]',
        'choices=[0]':'choices=[1]',
        "choices=['clean_Japanese','English']":"choices=['clean_Japanese','revised_English']",
        '4725<=args.down_frame<4960':'4250<=args.down_frame<4480',
        'Rafael_B46_route':'Hodram_B49_tail_route',
        '_v7945':'_v8416',
        "Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/ordinary_NewGame_inputs.json')":"Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')",
        'range(4000,15501,240)':'range(4000,9501,240)',
        'range(2350,16001,60)':'range(2350,10001,60)',
        '{16000,*MENU_SNAPSHOT_FRAMES}':'{10000,*MENU_SNAPSHOT_FRAMES}',
        'frames=16001':'frames=10001',
        'displayed_original_block=46,entry_opening_block=44':'displayed_original_block=49,entry_opening_block=42',
        'original_exchange_commands=37,original_exchange_stored_speeches=24,original_menu_choices=2,original_initializer_commands=10':'original_exchange_commands=23,original_exchange_stored_speeches=8,original_menu_choices=2,original_initializer_commands=8,original_B49_entry_commands=2,bounded_possession_dialogue_tail_not_whole_script_orinventory_eligibility=True',
        "'--frames','16001'":"'--frames','10001'",
        "'--capture-every','999999','--capture-at',*map(str,captures),'--dump-ram']":"'--capture-every','999999','--capture-at',*map(str,captures),'--capture-native-state-at','4870','4930','5110','5530','5590','5650','--dump-ram']",
        "report['frames']==16001":"report['frames']==10001",
        "print(f'B46 {version} {choice}:16001 frames terminal;readonly command/caption/menu snapshots captured. Actual path/display/return analysis pending.'":"print(f'B49 bounded-tail {version} {choice}:10001frames terminal;readonly command/caption/menu/native snapshots captured. Actual display/return analysis pending.'",
    })
    root.mkdir(parents=True);save(root/'runner_derivation.json',dict(derivation=result,all_native_high_integer_constants_andmultiplicity_preserved=True,original_disjoint_host_callback_slots_CPU_WRAM_TCM_andconfiguration_guards_preserved=True,identical_source_English_A_schedule_accept_default_decline_DOWN4350_before_next_A4480=True,menu_readonly_snapshot_frames=[4310,4370,4430],native_readonly_export_frames=[4870,4930,5110,5530,5590,5650],bounded_original_tail_not_whole_scene_orpossession_eligibility=True,new_credit=0,full_goal_complete=False))
