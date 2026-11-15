"""Prepare complete two-pair ceramics fixtures and actual display comparison."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_display_tools_v5295')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B188_display_fixture_v5254.py','scripts/research_lil_B189_display_fixture_v5295.py',{
        'B188':'B189','display_fixture_v5254':'display_fixture_v5295','display_v5254':'display_v5295','combined_v5219':'combined_v5263','relocation_v5246':'relocation_v5287',
        'bank[188]':'bank[189]','source_block=188':'source_block=189','len(commands)==14':'len(commands)==20',
        'len(walk)==23 and len(speeches)==11':'len(walk)==29 and len(speeches)==17','all23_stored_fixture_commands':'all29_stored_fixture_commands',
        'all11_speeches10_progressive1':'all17_speeches16_progressive1','closing_notice_names_Osaka':'closing_notice_names_Hamburg','source_event188_not_selected':'source_event189_not_selected',
        'source_all14_commands':'source_all20_commands','stored_speech_objects=11':'stored_speech_objects=17','all14 commands+9 original init commands,10 progressive':'all20 commands+9 original init commands,16 progressive'} )]
    rows.append(derive('scripts/pin_lil_B188_display_v5255.py','scripts/pin_lil_B189_display_v5296.py',{
        'B188':'B189','display_tools_v5255':'display_tools_v5296','display_fixture_v5254':'display_fixture_v5295','source_speeches=11,progressive=10':'source_speeches=17,progressive=16',
        'source_commands=14,stored_fixture_commands=23':'source_commands=20,stored_fixture_commands=29','All11 panels':'All17 panels'}))
    rows.append(derive('scripts/run_lil_B188_display_fixture_v5256.py','scripts/run_lil_B189_display_fixture_v5297.py',{
        'B188':'B189','display_fixture_v5254':'display_fixture_v5295','display_run_v5256':'display_run_v5297','display_v5256':'display_v5297',
        'source_event188_not_selected':'source_event189_not_selected',"'displayed_original_source_block':188":"'displayed_original_source_block':189",
        'all_source14_commands_10_progressive1_FE_A000_C200_end_retained':'all_source20_commands_16_progressive1_FE_A000_C200_end_retained'}))
    rows.append(derive('scripts/audit_lil_B188_actual_v5257.py','scripts/audit_lil_B189_actual_v5298.py',{
        'B188':'B189','actual_v5257':'actual_v5298','display_fixture_v5254':'display_fixture_v5295',
        'fonts_v5244/all11_progressive_FE_native_planes_and88_alignment_cases':'fonts_v5285/all17_progressive_FE_native_planes_and136_alignment_cases',
        'display_run_v5256':'display_run_v5297','display_v5256':'display_v5297','source_event188_not_selected':'source_event189_not_selected',
        'all_source14_commands_10_progressive1_FE_A000_C200_end_retained':'all_source20_commands_16_progressive1_FE_A000_C200_end_retained',
        "source['block']!=188":"source['block']!=189",'original_source_block=188':'original_source_block=189',"r.get('original_source_block')==188":"r.get('original_source_block')==189",
        'len(selected)==len(expected)==23':'len(selected)==len(expected)==29',"len(intervals)==len({r['id'] for r in intervals})==11":"len(intervals)==len({r['id'] for r in intervals})==17",
        "selected[-1]['original_source_offset']==478":"selected[-1]['original_source_offset']==766","ui[0]['original_source_offset']==476":"ui[0]['original_source_offset']==764",
        'single_source_end478':'single_source_end766','len(actual)==11':'len(actual)==17','actual_all11':'actual_all17','fresh_actual_unique_speech_panels=11':'fresh_actual_unique_speech_panels=17',
        'all14_source_commands_stored_and_all23_fixture_commands':'all20_source_commands_stored_and_all29_fixture_commands','all11_speeches10_progressive1':'all17_speeches16_progressive1',
        'actual_source_event188':'actual_source_event189','actual_panels=11':'actual_panels=17'}))
    rows.append(derive('scripts/review_lil_B188_actual_v5258.py','scripts/review_lil_B189_actual_v5299.py',{
        'B188':'B189','actual_review_v5258':'actual_review_v5299','actual_v5257':'actual_v5298','actual_all11':'actual_all17',
        'display_fixture_v5254':'display_fixture_v5295','display_v5256':'display_v5297','display_run_v5256':'display_run_v5297',
        "actual['complete_matching_observations']==11":"actual['complete_matching_observations']==17","len(actual['review_sheets'])==2":"len(actual['review_sheets'])==3",
        "len(v['selected_B22_command_pairs'])==23 and len(v['selected_intervals'])==11":"len(v['selected_B22_command_pairs'])==29 and len(v['selected_intervals'])==17",
        'single_source_end478':'single_source_end766',"v['source_C200']['original_source_offset']==476":"v['source_C200']['original_source_offset']==764",
        "['DK4_MES_B188_R0006','DK4_MES_B188_R0022','DK4_MES_B188_R0038','DK4_MES_B188_R0045']":"['DK4_MES_B189_R0026','DK4_MES_B189_R0038','DK4_MES_B189_R0046','DK4_MES_B189_R0065']",
        'all11_complete_held_planes':'all17_complete_held_planes','all11_speeches10_progressive1':'all17_speeches16_progressive1',
        'source_A0008_C200476_single_end478':'source_A0008_C200764_single_end766','actual23_of23_stored_fixture_commands':'actual29_of29_stored_fixture_commands',
        'paired_all115_samples23_commands11_planes':'paired_all115_samples29_commands17_planes','complete_panels=11':'complete_panels=17',
        'source_event188_natural_eligibility':'source_event189_natural_eligibility'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,source_commands=20,original_B22_initializers=9,stored_fixture_commands=29,
        speeches=17,progressive=16,FE=1,four_source_speakers_and_pair_transition_required=True,source_A000=1,prelude_A000=4,C200=1,source_end=766,no_predicates_or_relative_sites=True,
        two_cold_boots9001_frames_each_planned=True,all_original_commands_retained_without_flattening=True,
        native_high_integer_constants_and_multiplicities_including_actor_getter_CB184_preserved=True,no_forced_timing_RGB_RNG_or_state_equivalence=True,
        no_natural_event189_eligibility_or_earned_state_claim=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
