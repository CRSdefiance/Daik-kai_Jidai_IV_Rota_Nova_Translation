"""Freeze all18 complete native pages and unmodified QA, including source R5 punctuation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_native_tools_v7587')
if __name__=='__main__':
    assert not ROOT.exists();common={'B233':'B234','layout_v7538c/eleven_whole_paragraph_plans':'layout_v7586d/eighteen_whole_paragraph_plans','native_pages_v7539':'native_pages_v7587','base_QA_v7540':'base_QA_v7588','source_pages_v7534b/all11':'source_pages_v7582/all18','current_V7514_native_v7519':'current_V7563_native_v7568','[2,23]':'[19,104]','all11':'all18','all11_paragraphs11_complete_native_pages88_alignments':'all18_paragraphs18_complete_native_pages144_alignments','only_original_static_selectors2_23':'only_original_static_selectors19_104','all_English_body_prose_ASCII_without_new_substitution_or_font_change':'all_English_body_prose_ASCII_except_exact_retained_R5_source_three_CP932_ellipses_without_new_substitution_orfont_change'};jobs=[]
    for a,b,extra in [
      ('verify_lil_B233_native_pages_v7539','verify_lil_B234_native_pages_v7587',{"len(plan['records'])==11":"len(plan['records'])==18",'len(cases)==11 and len(pictures)==11 and alignments==88':'len(cases)==18 and len(pictures)==18 and alignments==144','complete_native_pages=11,logical_compiled_input_alignment_cases=88':'complete_native_pages=18,logical_compiled_input_alignment_cases=144','11 paragraphs/11 complete native pages/88 alignments':'18 paragraphs/18 complete native pages/144 alignments'}),
      ('probe_lil_B233_base_QA_v7540','probe_lil_B234_base_QA_v7588',{'eleven':'eighteen'}),
    ]:
        src=Path('scripts/'+a+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};changes.update(extra);checked_text(src,changes);assert not Path('scripts/'+b+'.py').exists();jobs.append(('scripts/'+a+'.py','scripts/'+b+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_native_andunmodified_QA.json',dict(tools=rows,all18_complete_original_pages144_logical_compiled_alignments_required=True,only_exact_original_R5_three_CP932_ellipsis_glyphs_allowed=True,complete_original_printable68_speaker_bound=True,original_width_font_bounds_guards_pairphase_literal_I_andbase_QA_preserved=True,all_diagnostics_pending_individual_review=True,new_credit=0,full_goal_complete=False))
