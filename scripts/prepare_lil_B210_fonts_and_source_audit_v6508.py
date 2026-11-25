"""Prepare ten-object native display and actual Japanese source audits without B209 style assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B210_font_audit_tools_v6508')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/verify_lil_B209_research_fonts_v6463.py','scripts/verify_lil_B210_research_fonts_v6508.py',{
        'all20 compiled native bodies, both continuations and160':'all10 compiled native bodies, one original page each and80','B209':'B210',
        'from scripts.research_lil_B209_native_pages_v6461 import pages':'from scripts.research_lil_B209_native_pages_v6461 import pages as pages',
        'lil_B209_layout_research_v6462e/all20_research_plans_no_word_changes_or_approval.json':'lil_B210_layout_v6507c/ten_whole_paragraph_research_plans.json',
        'current_V6439_native_v6449':'current_V6488_native_v6497','research_fonts_v6463':'research_fonts_v6508',"len(plan['records'])==20":"len(plan['records'])==10",
        "    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==(151 if prefix==208 else prefix) and captain==2'})":"    adapter=inspect.getsource(expand)",
        "expected_pages=2 if record['id'] in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] else 1":"expected_pages=1",
        'len(cases)==20 and len(pictures)==22 and alignments==160':'len(cases)==10 and len(pictures)==10 and alignments==80',
        'all20_complete_pages_sheet':'all10_complete_pages_sheet','all20_bodies22_complete_native_pages_and160_alignments_RESEARCH.json':'all10_bodies10_complete_native_pages_and80_alignments_RESEARCH.json',
        'complete_native_pages=22,logical_compiled_input_alignment_cases=160':'complete_native_pages=10,logical_compiled_input_alignment_cases=80',
        'both_first_and_second_letter_use_original_four_row_native_continuation=True,all_other18_objects_one_native_page=True':'all10_objects_one_original_four_row_native_page=True,no_B209_page_footer_or_typed_style_exception_inherited=True',
        'D0_fallback151_unchanged=True':'only_original_static_selectors2_17_no_D0_role=True','all20_formatting_gates_remain_false':'all10_formatting_gates_remain_false',
        'All20 bodies/22 complete current native pages/160 alignments pass. Four sheets await viewing;actual page buttons,names and release remain pending.':'All10 bodies/10 complete current native pages/80 alignments pass. Two sheets await viewing;actual source/English,names and release remain pending.',
    }))
    rows.append(derive('scripts/audit_lil_B208_source_v6399.py','scripts/audit_lil_B210_source_v6510.py',{
        'complete24-panel source run to all38':'complete10-panel source run to all21','B208':'B210','source_actual_v6399':'source_actual_v6510','source_fixture_v6397':'source_fixture_v6503','source_run_v6398':'source_run_v6504','all29_source_commands_retained':'all12_source_commands_retained','source_event208':'source_event210',
        "len(observations)==24 and [r['source_record_index'] for r in observations]==[5,9,13,17,21,25,28,32,36,40,44,48,51,55,59,62,66,70,73,76,79,82,86,90]":"len(observations)==10 and [r['source_record_index'] for r in observations]==[5,8,11,15,19,23,26,29,33,36]",
        'len(pairs)==38':'len(pairs)==21','all38_stored_fixture_commands':'all21_stored_fixture_commands',"pairs[-1]['source_offset']==1182":"pairs[-1]['source_offset']==682",'==[1166,1174]':'==[674]',
        'range(0,24,6)':'range(0,10,6)','all24_complete_Japanese_source_sheet':'all10_complete_Japanese_source_sheet','all24_source_panels_all38_commands':'all10_source_panels_all21_commands','source_distinct_speech_observations=24,total_speech_observations=24':'source_distinct_speech_observations=10,total_speech_observations=10','all29_source_commands_and9_original_initializers_observed':'all12_source_commands_and9_original_initializers_observed','source_effect_offsets_executed=[1166,1174]':'source_effect_offsets_executed=[674]',
        'initialized_Amsterdam_B22_not_natural_event208':'initialized_Amsterdam_B22_not_natural_event210','Cristina_Erneco_Mysterious_Old_Man_names_and_private_thought_named_FE_notice_localization_pending':'Lil_Al_progressive_names_and_full_additional_name_field_typography_review_separate','source_speeches=24':'source_speeches=10',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,expected_source_objects10_commands21=True,expected_English_native_pages10_alignment_cases80=True,all_native_instruction_constants_preserved=True,no_global_name_or_source_pagination_exception=True,full_goal_complete=False));print('B210 ten-page/80-alignment native proof and10-panel/21-command actual source audit prepared.')
