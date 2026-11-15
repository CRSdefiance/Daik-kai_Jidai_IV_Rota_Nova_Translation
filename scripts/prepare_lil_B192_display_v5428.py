"""Prepare complete tobacco-curiosity fixtures and measured original transitions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_display_tools_v5428')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B188_display_fixture_v5254.py','scripts/research_lil_B192_display_fixture_v5428.py',{
        'B188':'B192','display_fixture_v5254':'display_fixture_v5428','display_v5254':'display_v5428','combined_v5219':'combined_v5396','relocation_v5246':'relocation_v5420',
        'bank[188]':'bank[192]','source_block=188':'source_block=192','len(commands)==14':'len(commands)==11',
        'len(walk)==23 and len(speeches)==11':'len(walk)==20 and len(speeches)==8','all23_stored_fixture_commands':'all20_stored_fixture_commands',
        'all11_speeches10_progressive1':'all8_speeches7_progressive1','closing_notice_names_Osaka':'closing_notice_names_Istanbul','source_event188_not_selected':'source_event192_not_selected',
        'source_all14_commands':'source_all11_commands','stored_speech_objects=11':'stored_speech_objects=8','all14 commands+9 original init commands,10 progressive':'all11 commands+9 original init commands,7 progressive'} )]
    rows.append(derive('scripts/pin_lil_B188_display_v5255.py','scripts/pin_lil_B192_display_v5429.py',{
        'B188':'B192','display_tools_v5255':'display_tools_v5429','display_fixture_v5254':'display_fixture_v5428','source_speeches=11,progressive=10':'source_speeches=8,progressive=7',
        'source_commands=14,stored_fixture_commands=23':'source_commands=11,stored_fixture_commands=20','All11 panels':'All8 panels'}))
    rows.append(derive('scripts/run_lil_B188_display_fixture_v5256.py','scripts/run_lil_B192_display_fixture_v5430.py',{
        'B188':'B192','display_fixture_v5254':'display_fixture_v5428','display_run_v5256':'display_run_v5430','display_v5256':'display_v5430',
        'source_event188_not_selected':'source_event192_not_selected',"'displayed_original_source_block':188":"'displayed_original_source_block':192",
        'all_source14_commands_10_progressive1_FE_A000_C200_end_retained':'all_source11_commands_7_progressive1_FE_A000_C200_end_retained'}))
    rows.append(derive('scripts/audit_lil_B188_actual_v5257.py','scripts/audit_lil_B192_actual_v5431.py',{
        'B188':'B192','actual_v5257':'actual_v5431','display_fixture_v5254':'display_fixture_v5428',
        'fonts_v5244/all11_progressive_FE_native_planes_and88_alignment_cases':'fonts_v5418/all8_progressive_FE_native_planes_and64_alignment_cases',
        'display_run_v5256':'display_run_v5430','display_v5256':'display_v5430','source_event188_not_selected':'source_event192_not_selected',
        'all_source14_commands_10_progressive1_FE_A000_C200_end_retained':'all_source11_commands_7_progressive1_FE_A000_C200_end_retained',
        "source['block']!=188":"source['block']!=192",'original_source_block=188':'original_source_block=192',"r.get('original_source_block')==188":"r.get('original_source_block')==192",
        'len(selected)==len(expected)==23':'len(selected)==len(expected)==20',"len(intervals)==len({r['id'] for r in intervals})==11":"len(intervals)==len({r['id'] for r in intervals})==8",
        "selected[-1]['original_source_offset']==478":"selected[-1]['original_source_offset']==398","ui[0]['original_source_offset']==476":"ui[0]['original_source_offset']==396",
        'single_source_end478':'single_source_end398','len(actual)==11':'len(actual)==8','actual_all11':'actual_all8','fresh_actual_unique_speech_panels=11':'fresh_actual_unique_speech_panels=8',
        'all14_source_commands_stored_and_all23_fixture_commands':'all11_source_commands_stored_and_all20_fixture_commands','all11_speeches10_progressive1':'all8_speeches7_progressive1',
        'actual_source_event188':'actual_source_event192','actual_panels=11':'actual_panels=8'}))
    rows.append(derive('scripts/review_lil_B188_actual_v5258.py','scripts/review_lil_B192_actual_v5432.py',{
        'B188':'B192','actual_review_v5258':'actual_review_v5432','actual_v5257':'actual_v5431','actual_all11':'actual_all8',
        'display_fixture_v5254':'display_fixture_v5428','display_v5256':'display_v5430','display_run_v5256':'display_run_v5430',
        "actual['complete_matching_observations']==11":"actual['complete_matching_observations']==8",
        "len(v['selected_B22_command_pairs'])==23 and len(v['selected_intervals'])==11":"len(v['selected_B22_command_pairs'])==20 and len(v['selected_intervals'])==8",
        'single_source_end478':'single_source_end398',"v['source_C200']['original_source_offset']==476":"v['source_C200']['original_source_offset']==396",
        "['DK4_MES_B188_R0006','DK4_MES_B188_R0022','DK4_MES_B188_R0038','DK4_MES_B188_R0045']":"['DK4_MES_B192_R0016','DK4_MES_B192_R0020','DK4_MES_B192_R0023','DK4_MES_B192_R0030']",
        'all11_complete_held_planes':'all8_complete_held_planes','all11_speeches10_progressive1':'all8_speeches7_progressive1',
        'source_A0008_C200476_single_end478':'source_A0008_C200396_single_end398','actual23_of23_stored_fixture_commands':'actual20_of20_stored_fixture_commands',
        'paired_all115_samples23_commands11_planes':'paired_all115_samples20_commands8_planes','complete_panels=11':'complete_panels=8',
        'source_event188_natural_eligibility':'source_event192_natural_eligibility'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,source_commands=11,original_B22_initializers=9,stored_fixture_commands=20,
        speeches=8,progressive=7,FE=1,source_A000=1,prelude_A000=4,C200=1,source_end=398,no_predicates_or_relative_sites=True,
        two_cold_boots9001_frames_each_planned=True,all_original_commands_retained_without_flattening=True,
        native_high_integer_constants_and_multiplicities_including_actor_getter_CB184_preserved=True,no_forced_timing_RGB_RNG_or_state_equivalence=True,
        no_natural_event192_eligibility_or_earned_state_claim=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
