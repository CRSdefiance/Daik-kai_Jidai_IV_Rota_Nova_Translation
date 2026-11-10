"""Reserve the existing continuation guard in planning; keep every word and native rule unchanged."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B210_layout_tools_v6507b')
if __name__=='__main__':
    assert not ROOT.exists();old=read('work/analysis/lil_B210_layout_v6507/ten_whole_paragraph_research_plans.json');assert old['failures']==[dict(id='DK4_MES_B210_R0036',error='line-overflow: line is 222px; maximum is 216px')]
    r=derive('scripts/plan_lil_B210_layout_v6507.py','scripts/plan_lil_B210_layout_v6507b.py',{
        'lil_B210_layout_v6507':'lil_B210_layout_v6507b',
        'if length+reserve>36:continue':'if length+reserve+int(line>0)>36:continue',
        '"must\'ve"})':'"must\'ve","blade\'s"})',
        "('sealed','it')}":"('sealed','it'),('incredibly','sharp'),('want','it')}",
        "weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS));tiny=":"ordinary=(row['id']=='DK4_MES_B210_R0008' and pair==('his','hands'));weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS));tiny=",
    });ROOT.mkdir(parents=True);save(ROOT/'original_guard_reservation_and_ordinary_boundary.json',dict(derived=r,earlier_final36_character_continuation_rejected_by_unchanged_shared_linter=True,now_reserves_original6px_continuation_guard_on_all_rows=True,all_English_prose_source_controls_font_codec_and_native_bounds_unchanged=True,exact_R8_his_hands_complete_word_boundary_researched_not_yet_approved=True,boundary_reason='Ordinary possessive/complete-word wrap allows the full70-character acquisition/rumor sentence in two native rows,34/35 characters,with the entire hands on an incredibly sharp sword clause retained on row2. This avoids an unnecessary third row while preserving every word and the native guard. Exact B210 source/prose case only;not a global weak-ending exemption.',full_goal_complete=False));print('B210 planner now reserves the original continuation guard;exact R8 possessive boundary researched. No wording,codec,font or native bound changed.')
