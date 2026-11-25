"""Prepare all three Ladies and complete cooking-source display/return fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_display_tools_v5469')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B192_display_fixture_v5428.py','scripts/research_lil_B193_display_fixture_v5469.py',{
        'B192':'B193','display_fixture_v5428':'display_fixture_v5469','display_v5428':'display_v5469','combined_v5396':'combined_v5437','relocation_v5420':'relocation_v5461',
        'bank[192]':'bank[193]','source_block=192':'source_block=193','len(commands)==11':'len(commands)==18',
        'len(walk)==20 and len(speeches)==8':'len(walk)==27 and len(speeches)==15','all20_stored_fixture_commands':'all27_stored_fixture_commands',
        'all8_speeches7_progressive1':'all15_speeches14_progressive1','closing_notice_names_Istanbul':'closing_notice_names_Seoul','source_event192_not_selected':'source_event193_not_selected',
        'source_all11_commands':'source_all18_commands','stored_speech_objects=8':'stored_speech_objects=15','all11 commands+9 original init commands,7 progressive':'all18 commands+9 original init commands,14 progressive'} )]
    rows.append(derive('scripts/pin_lil_B192_display_v5429.py','scripts/pin_lil_B193_display_v5470.py',{
        'B192':'B193','display_tools_v5429':'display_tools_v5470','display_fixture_v5428':'display_fixture_v5469','source_speeches=8,progressive=7':'source_speeches=15,progressive=14',
        'source_commands=11,stored_fixture_commands=20':'source_commands=18,stored_fixture_commands=27','All8 panels':'All15 panels'}))
    rows.append(derive('scripts/run_lil_B192_display_fixture_v5430.py','scripts/run_lil_B193_display_fixture_v5471.py',{
        'B192':'B193','display_fixture_v5428':'display_fixture_v5469','display_run_v5430':'display_run_v5471','display_v5430':'display_v5471',
        'source_event192_not_selected':'source_event193_not_selected',"'displayed_original_source_block':192":"'displayed_original_source_block':193",
        'all_source11_commands_7_progressive1_FE_A000_C200_end_retained':'all_source18_commands_14_progressive1_FE_A000_C200_end_retained'}))
    rows.append(derive('scripts/audit_lil_B192_actual_v5431.py','scripts/audit_lil_B193_actual_v5472.py',{
        'B192':'B193','actual_v5431':'actual_v5472','display_fixture_v5428':'display_fixture_v5469',
        'fonts_v5418/all8_progressive_FE_native_planes_and64_alignment_cases':'fonts_v5459/all15_progressive_FE_native_planes_and120_alignment_cases',
        'display_run_v5430':'display_run_v5471','display_v5430':'display_v5471','source_event192_not_selected':'source_event193_not_selected',
        'all_source11_commands_7_progressive1_FE_A000_C200_end_retained':'all_source18_commands_14_progressive1_FE_A000_C200_end_retained',
        "source['block']!=192":"source['block']!=193",'original_source_block=192':'original_source_block=193',"r.get('original_source_block')==192":"r.get('original_source_block')==193",
        'len(selected)==len(expected)==20':'len(selected)==len(expected)==27',"len(intervals)==len({r['id'] for r in intervals})==8":"len(intervals)==len({r['id'] for r in intervals})==15",
        "selected[-1]['original_source_offset']==398":"selected[-1]['original_source_offset']==662","ui[0]['original_source_offset']==396":"ui[0]['original_source_offset']==660",
        'single_source_end398':'single_source_end662','len(actual)==8':'len(actual)==15','actual_all8':'actual_all15','fresh_actual_unique_speech_panels=8':'fresh_actual_unique_speech_panels=15',
        'all11_source_commands_stored_and_all20_fixture_commands':'all18_source_commands_stored_and_all27_fixture_commands','all8_speeches7_progressive1':'all15_speeches14_progressive1',
        'actual_source_event192':'actual_source_event193','actual_panels=8':'actual_panels=15'}))
    rows.append(derive('scripts/review_lil_B192_actual_v5432.py','scripts/review_lil_B193_actual_v5473.py',{
        'B192':'B193','actual_review_v5432':'actual_review_v5473','actual_v5431':'actual_v5472','actual_all8':'actual_all15',
        'display_fixture_v5428':'display_fixture_v5469','display_v5430':'display_v5471','display_run_v5430':'display_run_v5471',
        "actual['complete_matching_observations']==8":"actual['complete_matching_observations']==15","len(actual['review_sheets'])==2":"len(actual['review_sheets'])==3",
        "len(v['selected_B22_command_pairs'])==20 and len(v['selected_intervals'])==8":"len(v['selected_B22_command_pairs'])==27 and len(v['selected_intervals'])==15",
        'single_source_end398':'single_source_end662',"v['source_C200']['original_source_offset']==396":"v['source_C200']['original_source_offset']==660",
        "['DK4_MES_B192_R0016','DK4_MES_B192_R0020','DK4_MES_B192_R0023','DK4_MES_B192_R0030']":"['DK4_MES_B193_R0006','DK4_MES_B193_R0025','DK4_MES_B193_R0044','DK4_MES_B193_R0059']",
        'all8_complete_held_planes':'all15_complete_held_planes','all8_speeches7_progressive1':'all15_speeches14_progressive1',
        'source_A0008_C200396_single_end398':'source_A0008_C200660_single_end662','actual20_of20_stored_fixture_commands':'actual27_of27_stored_fixture_commands',
        'paired_all115_samples20_commands8_planes':'paired_all115_samples27_commands15_planes','complete_panels=8':'complete_panels=15','source_event192_natural_eligibility':'source_event193_natural_eligibility'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,source_commands=18,original_B22_initializers=9,stored_fixture_commands=27,
        speeches=15,progressive=14,FE=1,source_A000=1,prelude_A000=4,C200=1,source_end=662,no_predicates_or_relative_sites=True,
        three_original_speakers_and_complete_cooking_offer_and_friendship_to_be_observed=True,two_cold_boots9001_frames_each_planned=True,
        all_original_commands_retained_without_flattening=True,native_high_integer_constants_and_multiplicities_preserved=True,no_forced_timing_RGB_RNG_or_state_equivalence=True,
        no_natural_event193_eligibility_or_earned_state_claim=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
