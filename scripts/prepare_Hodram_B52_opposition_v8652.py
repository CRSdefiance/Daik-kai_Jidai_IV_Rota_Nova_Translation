"""Choose the second original B52 menu option through one paired ordinary DOWN input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_opposition_tools_v8652');assert not root.exists()
    intervals=[]
    for version in ['clean_Japanese','revised_English']:
        folder=Path('work/analysis/Hodram_B52_scene_runs_v8649')/('route1_B52_'+version)
        terminal=read(folder/'terminal.json');trace=read(terminal['observer']);assert terminal['terminal'] and sha(Path(terminal['observer']).read_bytes())==terminal['observer_sha256']
        selected=[r for r in trace['rows'] if r['kind']=='after_command' and r['source'].get('route')==1 and r['source'].get('block')==42 and r['source'].get('first_word')==0x2100]
        assert len(selected)==1 and selected[0]['result_words']==[2,0]
        returned=selected[0];entry=trace['rows'][returned['entry_row']]
        assert entry['frame']<4100<returned['frame'] and not any(r['kind']=='before_command' and r['source'].get('first_word')==0x2100 and r['frame']==4100 for r in trace['rows'])
        intervals.append(dict(version=version,start=entry['frame'],returned=returned['frame'],default_selection=0,observer=terminal['observer'],observer_sha256=terminal['observer_sha256']))
    gate="""    measured=read('work/analysis/Hodram_B52_opposition_tools_v8652/input_basis.json')
    assert measured['ordinary_DOWN_frame']==4100 and all(r['start']<4100<r['returned'] for r in measured['observed_default_menu_intervals'])
"""
    result=derive('scripts/run_Hodram_B52_v8649.py','scripts/run_Hodram_B52_opposition_v8652.py',{
        'Hodram_B52_scene_runs_v8649':'Hodram_B52_opposition_runs_v8652',
        '_v8649':'_v8652',
        "    route,version,block=args.route,args.version,args.block;":gate+"    route,version,block=args.route,args.version,args.block;",
        'identical_ordinary_A_inputs.json':'identical_ordinary_A_andone_DOWN_inputs.json',
        "    save(inputs,base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,frames-480,240)])":"    save(inputs,sorted(base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,frames-480,240)]+[dict(start=4100,duration=5,buttons=['DOWN'])],key=lambda r:r['start']))",
        'no_controller_retiming_between_clean_Japanese_andrevised_English=True':'no_controller_retiming_between_clean_Japanese_andrevised_English=True,ordinary_input_case="one_DOWN_at4100_to_second_option",measured_input_basis="work/analysis/Hodram_B52_opposition_tools_v8652/input_basis.json",measured_input_basis_sha256=sha(Path("work/analysis/Hodram_B52_opposition_tools_v8652/input_basis.json").read_bytes())',
    })
    root.mkdir(parents=True);save(root/'input_basis.json',dict(ordinary_DOWN_frame=4100,ordinary_DOWN_duration=5,observed_default_menu_intervals=intervals,all_other_NewGame_andA_inputs_unchanged=True,same_extra_controller_input_inboth_languages=True,no_predicate_eventflag_RNG_roster_orresult_forcing=True,actual_second_choice_andflagged_end_must_be_observed_not_assumed=True,derivation=result,new_credit=0,full_goal_complete=False))
