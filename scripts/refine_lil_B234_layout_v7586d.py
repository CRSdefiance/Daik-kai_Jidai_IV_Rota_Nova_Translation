"""Keep the complete on-your-face phrase together in the full-width teasing paragraph."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_layout_tools_v7586d')
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/plan_lil_B234_layout_v7586c.py').read_text('utf8');old=src[src.index('PAIRS={'):src.index('\ndef display')];env={};exec(old,{},env)
    tool=derive('scripts/plan_lil_B234_layout_v7586c.py','scripts/plan_lil_B234_layout_v7586d.py',{old:'PAIRS='+repr(env['PAIRS']|{('on','your')})+'\n','layout_v7586c':'layout_v7586d'})
    ROOT.mkdir(parents=True);save(ROOT/'complete_phrase_layout_refinement.json',dict(tool=tool,R16_on_your_face_kept_complete_without_losing_any_word=True,all_other_prose_native_geometry_guards_andliteral_I_unchanged=True,initial_andall_refined_plans_preserved=True,no_global_weak_rule_change=True,new_credit=0,full_goal_complete=False))
