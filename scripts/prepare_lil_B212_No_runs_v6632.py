"""Focus the distinct ordinary terminator through one real DOWN press; preserve both full scripts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_No_run_tools_v6632')
if __name__=='__main__':
    assert not ROOT.exists();old="read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,15501,240)]";new="sorted(read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,5901,240)]+[dict(start=3250,duration=5,buttons=['DOWN'])],key=lambda r:r['start'])";proofs=[]
    for language,version in [('source','6612'),('English','6628')]:
        source=f'scripts/run_lil_B212_{language}_v{version}.py';target=f'scripts/run_lil_B212_No_{language}_v6632.py';changes={f'lil_B212_{language}_run_v{version}':f'lil_B212_No_{language}_run_v6632',f'lil_B212_{language}_v{version}':f'lil_B212_No_{language}_v6632',old:new,'16001':'6001'};proofs.append(derive(source,target,changes))
    ROOT.mkdir(parents=True);save(ROOT/'two_focused_normal_return_runners.json',dict(proofs=proofs,original_source_English_fixtures_reused_no_new_ROM=True,identical_original_startup_A_inputs_plus_one_DOWN3250=True,ordinary_menu_selection_not_forced_result_RNG_or_state=True,specific_risk='Unlike the already observed flagged Zhao terminator, No reaches the early ordinary00000000 terminator. Bind the real index1 path, complete recommendation and caller return in both languages.',all26_original_commands_stored_no_omission=True,unvisited_Guan_Zhuge_alternatives_still_explicit=True,frames_each=6001,new_credit=0,full_goal_complete=False))
