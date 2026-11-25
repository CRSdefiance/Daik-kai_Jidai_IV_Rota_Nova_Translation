"""Prepare paired complete cheese-specialty content cold boots and unmasked display/return audits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B195_display_tools_v5569')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B193_display_fixture_v5469.py','scripts/research_lil_B195_display_fixture_v5569.py',{
        'B193':'B195','display_fixture_v5469':'display_fixture_v5569','display_v5469':'display_v5569','combined_v5437':'combined_v5531','relocation_v5461':'relocation_v5561',
        'bank[193]':'bank[195]','source_block=193':'source_block=195','len(commands)==18':'len(commands)==23',
        'len(walk)==27 and len(speeches)==15':'len(walk)==32 and len(speeches)==20','all27_stored_fixture_commands':'all32_stored_fixture_commands',
        'all15_speeches14_progressive1':'all20_speeches19_progressive1','closing_notice_names_Seoul':'closing_notice_names_Veracruz',
        'source_event193_not_selected':'source_event195_not_selected','source_all18_commands':'source_all23_commands','stored_speech_objects=15':'stored_speech_objects=20',
        'all18 commands+9 original init commands,14 progressive':'all23 commands+9 original init commands,19 progressive'} )]
    rows.append(derive('scripts/pin_lil_B193_display_v5470.py','scripts/pin_lil_B195_display_v5570.py',{
        'B193':'B195','display_tools_v5470':'display_tools_v5570','display_fixture_v5469':'display_fixture_v5569',
        'source_speeches=15,progressive=14':'source_speeches=20,progressive=19','source_commands=18,stored_fixture_commands=27':'source_commands=23,stored_fixture_commands=32','All15 panels':'All20 panels'}))
    rows.append(derive('scripts/run_lil_B193_display_fixture_v5471.py','scripts/run_lil_B195_display_fixture_v5571.py',{
        'B193':'B195','display_fixture_v5469':'display_fixture_v5569','display_run_v5471':'display_run_v5571','display_v5471':'display_v5571',
        'source_event193_not_selected':'source_event195_not_selected',"'displayed_original_source_block':193":"'displayed_original_source_block':195",
        'all_source18_commands_14_progressive1_FE_A000_C200_end_retained':'all_source23_commands_19_progressive1_FE_A000_C200_end_retained'}))
    rows.append(derive('scripts/audit_lil_B193_actual_v5472.py','scripts/audit_lil_B195_actual_v5572.py',{
        'B193':'B195','actual_v5472':'actual_v5572','display_fixture_v5469':'display_fixture_v5569',
        'fonts_v5459/all15_progressive_FE_native_planes_and120_alignment_cases':'fonts_v5553/all20_progressive_FE_native_planes_and160_alignment_cases',
        'display_run_v5471':'display_run_v5571','display_v5471':'display_v5571','source_event193_not_selected':'source_event195_not_selected',
        'all_source18_commands_14_progressive1_FE_A000_C200_end_retained':'all_source23_commands_19_progressive1_FE_A000_C200_end_retained',
        "source['block']!=193":"source['block']!=195",'original_source_block=193':'original_source_block=195',"r.get('original_source_block')==193":"r.get('original_source_block')==195",
        'len(selected)==len(expected)==27':'len(selected)==len(expected)==32',"len(intervals)==len({r['id'] for r in intervals})==15":"len(intervals)==len({r['id'] for r in intervals})==20",
        "selected[-1]['original_source_offset']==662":"selected[-1]['original_source_offset']==706","ui[0]['original_source_offset']==660":"ui[0]['original_source_offset']==704",
        'single_source_end662':'single_source_end706','len(actual)==15':'len(actual)==20','actual_all15':'actual_all20','fresh_actual_unique_speech_panels=15':'fresh_actual_unique_speech_panels=20',
        'all18_source_commands_stored_and_all27_fixture_commands':'all23_source_commands_stored_and_all32_fixture_commands','all15_speeches14_progressive1':'all20_speeches19_progressive1',
        'actual_source_event193':'actual_source_event195','actual_panels=15':'actual_panels=20'}))
    rows.append(derive('scripts/review_lil_B193_actual_v5473.py','scripts/review_lil_B195_actual_v5573.py',{
        'B193':'B195','actual_review_v5473':'actual_review_v5573','actual_v5472':'actual_v5572','actual_all15':'actual_all20',
        'display_fixture_v5469':'display_fixture_v5569','display_v5471':'display_v5571','display_run_v5471':'display_run_v5571',
        "actual['complete_matching_observations']==15":"actual['complete_matching_observations']==20","len(actual['review_sheets'])==3":"len(actual['review_sheets'])==4",
        "len(v['selected_B22_command_pairs'])==27 and len(v['selected_intervals'])==15":"len(v['selected_B22_command_pairs'])==32 and len(v['selected_intervals'])==20",
        'single_source_end662':'single_source_end706',"v['source_C200']['original_source_offset']==660":"v['source_C200']['original_source_offset']==704",
        "['DK4_MES_B193_R0006','DK4_MES_B193_R0025','DK4_MES_B193_R0044','DK4_MES_B193_R0059']":
        "['DK4_MES_B195_R0017','DK4_MES_B195_R0043','DK4_MES_B195_R0069','DK4_MES_B195_R0077']",
        'all15_complete_held_planes':'all20_complete_held_planes','all15_speeches14_progressive1':'all20_speeches19_progressive1',
        'source_A0008_C200660_single_end662':'source_A0008_C200704_single_end706','actual27_of27_stored_fixture_commands':'actual32_of32_stored_fixture_commands',
        'paired_all115_samples27_commands15_planes':'paired_all115_samples32_commands20_planes','complete_panels=15':'complete_panels=20',
        'source_event193_natural_eligibility':'source_event195_natural_eligibility'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,
        source_commands=23,original_B22_initializers=9,stored_fixture_commands=32,speeches=20,progressive=19,FE=1,
        source_A000=1,prelude_A000=4,C200=1,source_end=706,no_predicates_or_relative_sites_or_macros=True,
        three_original_roles_chewing_beats_R17_guarded_three_rows_and_personal_intention_to_be_observed=True,
        two_cold_boots9001_frames_each_planned=True,all_original_commands_retained_without_flattening=True,
        no_forced_timing_RGB_RNG_or_state_equivalence=True,no_natural_event195_eligibility_or_earned_state_claim=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
