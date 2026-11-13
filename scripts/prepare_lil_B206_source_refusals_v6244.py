"""Use ordinary DOWN presses inside measured original menu intervals;never inject a choice result."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B206_source_refusal_tools_v6244')
if __name__=='__main__':
    assert not ROOT.exists();run=Path('work/analysis/lil_B206_source_run_v6243_buy');terminal=read(run/'terminal.json');plan=read(run/'run_plan.json');cap=Path(plan['capture_folder']);trace=read(cap/'observer/commands.json');assert terminal['terminal'] and terminal['observer_host_slots_restored'] and not trace['errors'] and trace['mismatches']==0
    menus=[]
    for row in trace['rows']:
        if row['kind']=='after_command' and row['source']['block']==22 and row['source']['first_word']==0x2100:
            e=trace['rows'][row['entry_row']];menus.append(dict(fixture_offset=e['source']['instruction_offset'],start=e['frame'],returned=row['frame'],native_result=row['result_words']))
    assert menus==[dict(fixture_offset=900,start=6217,returned=6445,native_result=[2,0]),dict(fixture_offset=1068,start=7175,returned=7407,native_result=[2,0])]
    key="save(inputs,read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,15501,240)]);"
    tools=[]
    for tag,version,frame in [('high_price',6245,7300),('pitch_refusal',6246,6300)]:
        tools.append(derive('scripts/run_lil_B206_source_buy_v6243.py',f'scripts/run_lil_B206_source_{tag}_v{version}.py',{'source_run_v6243_buy':f'source_run_v{version}_{tag}','source_v6243_buy':f'source_v{version}_{tag}',key:key.replace(']);',"]+[dict(start="+str(frame)+",duration=5,buttons=['DOWN'])]);")}))
    ROOT.mkdir(parents=True);save(ROOT/'measured_original_menu_intervals_and_ordinary_down_schedules.json',dict(tools=tools,baseline_actual_menus=menus,ordinary_high_price_DOWN_frame=7300,ordinary_pitch_refusal_DOWN_frame=6300,all_original_commands_retained_no_branch_or_result_fixture=True,expected_outcome_not_claimed_before_actual_observation=True,evidence={str(p):sha(p.read_bytes()) for p in [run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',Path(__file__)]},new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Two source refusal runs prepared:DOWN6300 in first menu or DOWN7300 in second. No choice results,state,funds or effects forced.')
