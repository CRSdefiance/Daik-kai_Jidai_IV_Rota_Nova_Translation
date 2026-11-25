"""Measure final complete B230 paragraphs using current V7418's own strict input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_native_tools_v7442')
if __name__=='__main__':
    assert not ROOT.exists();common={'B229':'B230','layout_v7393c':'layout_v7441b','native_pages_v7394':'native_pages_v7442','base_QA_v7395':'base_QA_v7443','source_pages_v7389':'source_pages_v7437','current_V7371_native_v7376':'current_V7418_native_v7423'};jobs=[]
    for old,new in [('verify_lil_B229_native_pages_v7394','verify_lil_B230_native_pages_v7442'),('probe_lil_B229_base_QA_v7395','probe_lil_B230_base_QA_v7443')]:
        src=Path('scripts/'+old+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};checked_text(src,changes);assert not Path('scripts/'+new+'.py').exists();jobs.append(('scripts/'+old+'.py','scripts/'+new+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_native_andunmodified_QA.json',dict(tools=rows,registered_V7418_own_native_input=True,all17_prose_paragraphs_unchanged=True,all_original_native_geometry_font_guards_literal_I_andQA_rules_preserved=True,new_credit=0,full_goal_complete=False))
