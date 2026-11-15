"""Distinguish the original captain-selection inputs from the later A-only scene inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_source_audit_tools_v6614b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/audit_lil_B212_source_v6614.py','scripts/audit_lil_B212_source_v6614b.py',{'lil_B212_source_actual_v6614':'lil_B212_source_actual_v6614b',"not any(set(r['buttons'])-{'A','B','START'} for r in schedule)":"[r for r in schedule if r['start']<2300]==read('work/analysis/movie_viewport_v303/lil_start_inputs.json') and all(r['buttons']==['A'] for r in schedule if r['start']>=2300)"});ROOT.mkdir(parents=True);save(ROOT/'source_locked_original_captain_inputs_and_scene_inputs.json',dict(proof=proof,failed_predecessor_preserved='scripts/audit_lil_B212_source_v6614.py',reason='The unchanged Lil startup schedule contains RIGHT at1450/1600 to choose Lil. Verify the entire original startup schedule exactly and A-only inputs after2300, rather than rejecting those source-owned navigation inputs.',no_new_boot_or_input_change=True,no_forced_choice_or_result=True,new_credit=0,full_goal_complete=False))
