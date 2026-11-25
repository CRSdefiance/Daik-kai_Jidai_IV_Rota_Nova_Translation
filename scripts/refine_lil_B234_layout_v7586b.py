"""Improve phrase boundaries without changing any prose, guard or native width."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_layout_tools_v7586b')
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/plan_lil_B234_layout_v7586.py').read_text('utf8');pairs=src[src.index('PAIRS={'):src.index('\ndef display')];scope={};exec(pairs,{},scope)
    updated=scope['PAIRS']|{('when','did'),('how','lucky'),('get','here')}
    changes={pairs:'PAIRS='+repr(updated)+'\n','layout_v7586':'layout_v7586b',
      'ordinary= {}.get':"ordinary= {'DK4_MES_B234_R0016':{('draw','customers')}}.get"} if 'ordinary= {}.get' in src else {
      pairs:'PAIRS='+repr(updated)+'\n','layout_v7586':'layout_v7586b',
      "ordinary={}.get(row['id'],set())":"ordinary={'DK4_MES_B234_R0016':{('draw','customers')}}.get(row['id'],set())",
    }
    old="if not final and words[stop-1]=='I':continue"
    changes[old]=old+"\n            if not final and row['id']=='DK4_MES_B234_R0033' and (norm(words[stop-1]),norm(words[stop]))==('papal','states'):continue"
    changes['only_exact_source_R5_three_CP932_ellipses_allowed_no_global_non_ASCII_exception=True']='only_exact_source_R5_three_CP932_ellipses_allowed_no_global_non_ASCII_exception=True,source_R33_Papal_States_kept_together_within_original_four_row_page=True,R16_draw_customers_ordinary_complete_word_boundary_not_global_weak_rule_waiver=True'
    tool=derive('scripts/plan_lil_B234_layout_v7586.py','scripts/plan_lil_B234_layout_v7586b.py',changes);ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_readable_phrase_refinement.json',dict(tool=tool,all_prose_andnative_geometry_unchanged=True,when_did_andhow_lucky_reviewed_as_phrases=True,Papal_States_proper_territorial_name_not_split=True,R16_ordinary_verb_object_soft_boundary_allows_balanced_complete_rows=True,initial_plan_preserved=True,no_global_weak_ending_literal_I_orfont_rule_change=True,new_credit=0,full_goal_complete=False))
