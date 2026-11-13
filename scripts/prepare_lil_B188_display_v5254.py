"""Prepare complete B188 content cold boots and unforced display/state comparison."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_display_tools_v5254')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B187_display_fixture_v5210.py','scripts/research_lil_B188_display_fixture_v5254.py',{
        'B187':'B188','display_fixture_v5210':'display_fixture_v5254','display_v5210':'display_v5254','combined_v5177':'combined_v5219','relocation_v5202':'relocation_v5246',
        'bank[187]':'bank[188]','source_block=187':'source_block=188','len(commands)==19':'len(commands)==14',
        'len(walk)==28 and len(speeches)==16':'len(walk)==23 and len(speeches)==11','all28_stored_fixture_commands':'all23_stored_fixture_commands',
        'all16_speeches15_progressive1':'all11_speeches10_progressive1','closing_notice_names_Malacca':'closing_notice_names_Osaka','source_event187_not_selected':'source_event188_not_selected',
        'source_all19_commands':'source_all14_commands','stored_speech_objects=16':'stored_speech_objects=11','all19 commands+9 original init commands,15 progressive':'all14 commands+9 original init commands,10 progressive'} )]
    rows.append(derive('scripts/pin_lil_B187_display_v5211.py','scripts/pin_lil_B188_display_v5255.py',{
        'B187':'B188','display_tools_v5211':'display_tools_v5255','display_fixture_v5210':'display_fixture_v5254','source_speeches=16,progressive=15':'source_speeches=11,progressive=10',
        'source_commands=19,stored_fixture_commands=28':'source_commands=14,stored_fixture_commands=23','All16 panels':'All11 panels'}))
    rows.append(derive('scripts/run_lil_B187_display_fixture_v5212.py','scripts/run_lil_B188_display_fixture_v5256.py',{
        'B187':'B188','display_fixture_v5210':'display_fixture_v5254','display_run_v5212':'display_run_v5256','display_v5212':'display_v5256',
        'source_event187_not_selected':'source_event188_not_selected',"'displayed_original_source_block':187":"'displayed_original_source_block':188",
        'all_source19_commands_15_progressive1_FE_A000_C200_end_retained':'all_source14_commands_10_progressive1_FE_A000_C200_end_retained'}))
    rows.append(derive('scripts/audit_lil_B187_actual_v5213.py','scripts/audit_lil_B188_actual_v5257.py',{
        'B187':'B188','actual_v5213':'actual_v5257','display_fixture_v5210':'display_fixture_v5254',
        'fonts_v5200/all16_progressive_FE_native_planes_and128_alignment_cases':'fonts_v5244/all11_progressive_FE_native_planes_and88_alignment_cases',
        'display_run_v5212':'display_run_v5256','display_v5212':'display_v5256','source_event187_not_selected':'source_event188_not_selected',
        'all_source19_commands_15_progressive1_FE_A000_C200_end_retained':'all_source14_commands_10_progressive1_FE_A000_C200_end_retained',
        "source['block']!=187":"source['block']!=188",'original_source_block=187':'original_source_block=188',"r.get('original_source_block')==187":"r.get('original_source_block')==188",
        'len(selected)==len(expected)==28':'len(selected)==len(expected)==23',"len(intervals)==len({r['id'] for r in intervals})==16":"len(intervals)==len({r['id'] for r in intervals})==11",
        "selected[-1]['original_source_offset']==674":"selected[-1]['original_source_offset']==478","ui[0]['original_source_offset']==672":"ui[0]['original_source_offset']==476",
        'single_source_end674':'single_source_end478','len(actual)==16':'len(actual)==11','actual_all16':'actual_all11','fresh_actual_unique_speech_panels=16':'fresh_actual_unique_speech_panels=11',
        'all19_source_commands_stored_and_all28_fixture_commands':'all14_source_commands_stored_and_all23_fixture_commands','all16_speeches15_progressive1':'all11_speeches10_progressive1',
        'actual_source_event187':'actual_source_event188','actual_panels=16':'actual_panels=11'}))
    rows.append(derive('scripts/review_lil_B187_actual_v5214.py','scripts/review_lil_B188_actual_v5258.py',{
        'B187':'B188','actual_review_v5214':'actual_review_v5258','actual_v5213':'actual_v5257','actual_all16':'actual_all11',
        'display_fixture_v5210':'display_fixture_v5254','display_v5212':'display_v5256','display_run_v5212':'display_run_v5256',
        "actual['complete_matching_observations']==16":"actual['complete_matching_observations']==11","len(actual['review_sheets'])==3":"len(actual['review_sheets'])==2",
        "len(v['selected_B22_command_pairs'])==28 and len(v['selected_intervals'])==16":"len(v['selected_B22_command_pairs'])==23 and len(v['selected_intervals'])==11",
        'single_source_end674':'single_source_end478',"v['source_C200']['original_source_offset']==672":"v['source_C200']['original_source_offset']==476",
        "['DK4_MES_B187_R0006','DK4_MES_B187_R0030','DK4_MES_B187_R0045','DK4_MES_B187_R0060']":"['DK4_MES_B188_R0006','DK4_MES_B188_R0022','DK4_MES_B188_R0038','DK4_MES_B188_R0045']",
        'all16_complete_held_planes':'all11_complete_held_planes','all16_speeches15_progressive1':'all11_speeches10_progressive1',
        'source_A0008_C200672_single_end674':'source_A0008_C200476_single_end478','actual28_of28_stored_fixture_commands':'actual23_of23_stored_fixture_commands',
        'paired_all115_samples28_commands16_planes':'paired_all115_samples23_commands11_planes','complete_panels=16':'complete_panels=11',
        'source_event185_natural_eligibility':'source_event188_natural_eligibility'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,source_commands=14,original_B22_initializers=9,stored_fixture_commands=23,
        speeches=11,progressive=10,FE=1,source_A000=1,prelude_A000=4,C200=1,source_end=478,no_predicates_or_relative_sites=True,
        two_cold_boots9001_frames_each_planned=True,all_original_commands_retained_without_flattening=True,
        native_high_integer_constants_and_multiplicities_including_actor_getter_CB184_preserved=True,no_forced_timing_RGB_RNG_or_state_equivalence=True,
        no_natural_event188_eligibility_or_earned_state_claim=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
