"""Prepare read-only paired English scene runs; retain full observer, input and cold-boot guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_scene_run_tools_v8225')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/run_Rafael_B50_scenes_v8155.py','scripts/run_Gerhard_scenes_v8225.py',{
        'Paired source/English initialized scene tests, ordinary identical inputs and readonly trace.':'Paired previous/revised English full-script entry fixtures;ordinary identical inputs andreadonly traces.',
        'Rafael_B50_scene_runs_v8155':'Gerhard_scene_runs_v8225',
        'Rafael_B50_scene_fixtures_v8154/two_complete_source_English_original_Rafael_prelude_fixtures.json':'Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json',
        "ap.add_argument('--route',type=int,choices=[0],required=True);ap.add_argument('--version',choices=['clean_Japanese','English'],required=True);args=ap.parse_args()":
        "ap.add_argument('--route',type=int,choices=[2],required=True);ap.add_argument('--block',type=int,choices=[27,74],required=True);ap.add_argument('--version',choices=['parent_English','revised_English'],required=True);args=ap.parse_args()",
        "route,version=args.route,args.version;selected=next(f for f in read(FIXTURES)['fixtures'] if f['route']==route and f['version']==version)":
        "route,version,block=args.route,args.version,args.block;selected=next(f for f in read(FIXTURES)['fixtures'] if f['route']==route and f['version']==version and f['source_block']==block)",
        "folder=ROOT/f'route{route}_{version}'":"folder=ROOT/f'route{route}_B{block}_{version}'",
        'Rafael_B50_route{route}_{version}_v8155':'Gerhard_B{block}_route{route}_{version}_v8225',
        "Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/ordinary_NewGame_inputs.json')":"Path('work/analysis/lil_B111_B119_runs_v3253/newgame_inputs.json')",
        'range(4000,15521,240)':'range(4000,31521,240)','range(2350,16001,60)':'range(2350,32001,60)','|{16000}':'|{32000}',
        'frames=16001':'frames=32001',"'--frames','16001'":"'--frames','32001'","report['frames']==16001":"report['frames']==32001",
        'original_exchange_commands=37,original_exchange_speeches=28':"original_exchange_commands=len(selected['all_original_exchange_commands']),original_exchange_speeches=len(selected['original_text_records'])",
        'no_controller_retiming_between_source_andEnglish':'no_controller_retiming_between_previous_andrevised_English',
        "terminal=True,route=route,version=version":"terminal=True,route=route,source_block=block,version=version",
        "route{route} {version}:16001-frame fixture capture terminal":"route{route} B{block} {version}:32001-frame fixture capture terminal",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        previous_revised_pair_not_Japanese_source_gameplay=True,full_original_conditional_script_membership_retained=True,
        actual_selected_branch_andnormal_return_must_be_measured=True,original_observer_readonly_host_restoration_andsource_contract_guards_preserved=True,
        no_savestate_RAM_flags_roles_funds_RNG_orresults_forced=True,new_credit=0,full_goal_complete=False))
    print('Prepared paired32k-frame whole-script tests;originalobserver and all coldboot/runtime guards preserved.')
