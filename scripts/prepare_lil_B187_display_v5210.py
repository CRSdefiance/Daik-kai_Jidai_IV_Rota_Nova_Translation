"""Prepare complete linear B187 content fixtures and paired actual display audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_display_tools_v5210')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B185_display_fixture_v5113.py','scripts/research_lil_B187_display_fixture_v5210.py',{
        'B185':'B187','display_fixture_v5113':'display_fixture_v5210','display_v5113':'display_v5210',
        'combined_v5076':'combined_v5177','relocation_v5105':'relocation_v5202','editorial_manuscript_v4':'editorial_manuscript_v3',
        'bank[185]':'bank[187]','source_block=185':'source_block=187','len(commands)==11':'len(commands)==19',
        'len(walk)==20 and len(speeches)==8':'len(walk)==28 and len(speeches)==16',
        'all20_stored_fixture_commands':'all28_stored_fixture_commands','all8_speeches7_progressive1':'all16_speeches15_progressive1',
        'closing_notice_names_Stockholm':'closing_notice_names_Malacca','source_event185_not_selected':'source_event187_not_selected',
        'source_all11_commands':'source_all19_commands','stored_speech_objects=8':'stored_speech_objects=16',
        'all11 commands+9 original init commands,7 progressive':'all19 commands+9 original init commands,15 progressive',
    })]
    rows.append(derive('scripts/pin_lil_B185_display_v5114.py','scripts/pin_lil_B187_display_v5211.py',{
        'B185':'B187','display_tools_v5114':'display_tools_v5211','display_fixture_v5113':'display_fixture_v5210',
        'source_speeches=8,progressive=7':'source_speeches=16,progressive=15',
        'source_commands=11,stored_fixture_commands=20':'source_commands=19,stored_fixture_commands=28','All8 panels':'All16 panels',
    }))
    rows.append(derive('scripts/run_lil_B185_display_fixture_v5115.py','scripts/run_lil_B187_display_fixture_v5212.py',{
        'B185':'B187','display_fixture_v5113':'display_fixture_v5210','display_run_v5115':'display_run_v5212','display_v5115':'display_v5212',
        'source_event185_not_selected':'source_event187_not_selected',"'displayed_original_source_block':185":"'displayed_original_source_block':187",
        'all_source11_commands_7_progressive1_FE_A000_C200_end_retained':'all_source19_commands_15_progressive1_FE_A000_C200_end_retained',
    }))
    rows.append(derive('scripts/audit_lil_B185_actual_v5116.py','scripts/audit_lil_B187_actual_v5213.py',{
        'B185':'B187','actual_v5116':'actual_v5213','display_fixture_v5113':'display_fixture_v5210',
        'fonts_v5102/all8_progressive_FE_native_planes_and64_alignment_cases':'fonts_v5200/all16_progressive_FE_native_planes_and128_alignment_cases',
        'display_run_v5115':'display_run_v5212','display_v5115':'display_v5212','source_event185_not_selected':'source_event187_not_selected',
        'all_source11_commands_7_progressive1_FE_A000_C200_end_retained':'all_source19_commands_15_progressive1_FE_A000_C200_end_retained',
        "source['block']!=185":"source['block']!=187",'original_source_block=185':'original_source_block=187',
        "r.get('original_source_block')==185":"r.get('original_source_block')==187",
        'len(selected)==len(expected)==20':'len(selected)==len(expected)==28',
        "len(intervals)==len({r['id'] for r in intervals})==8":"len(intervals)==len({r['id'] for r in intervals})==16",
        "selected[-1]['original_source_offset']==384":"selected[-1]['original_source_offset']==674",
        "ui[0]['original_source_offset']==382":"ui[0]['original_source_offset']==672",
        'single_source_end384':'single_source_end674','len(actual)==8':'len(actual)==16','actual_all8':'actual_all16',
        'fresh_actual_unique_speech_panels=8':'fresh_actual_unique_speech_panels=16',
        'all11_source_commands_stored_and_all20_fixture_commands':'all19_source_commands_stored_and_all28_fixture_commands',
        'all8_speeches7_progressive1':'all16_speeches15_progressive1','actual_source_event185':'actual_source_event187','actual_panels=8':'actual_panels=16',
    }))
    rows.append(derive('scripts/review_lil_B185_actual_v5117b.py','scripts/review_lil_B187_actual_v5214.py',{
        'B185':'B187','actual_review_v5117b':'actual_review_v5214','actual_v5116':'actual_v5213','actual_all8':'actual_all16',
        'display_fixture_v5113':'display_fixture_v5210','display_v5115':'display_v5212','display_run_v5115':'display_run_v5212',
        "actual['complete_matching_observations']==8":"actual['complete_matching_observations']==16",
        "len(actual['review_sheets'])==2":"len(actual['review_sheets'])==3",
        "len(v['selected_B22_command_pairs'])==20 and len(v['selected_intervals'])==8":"len(v['selected_B22_command_pairs'])==28 and len(v['selected_intervals'])==16",
        'single_source_end384':'single_source_end674',"v['source_C200']['original_source_offset']==382":"v['source_C200']['original_source_offset']==672",
        "['DK4_MES_B185_R0013','DK4_MES_B185_R0016','DK4_MES_B185_R0026','DK4_MES_B185_R0029']":
        "['DK4_MES_B187_R0006','DK4_MES_B187_R0030','DK4_MES_B187_R0045','DK4_MES_B187_R0060']",
        'all8_complete_held_planes':'all16_complete_held_planes','all8_speeches7_progressive1':'all16_speeches15_progressive1',
        'source_A0008_C200382_single_end384':'source_A0008_C200672_single_end674','actual20_of20_stored_fixture_commands':'actual28_of28_stored_fixture_commands',
        'paired_all115_samples20_commands8_planes':'paired_all115_samples28_commands16_planes','complete_panels=8':'complete_panels=16',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,
        source_commands=19,original_B22_initializers=9,stored_fixture_commands=28,speeches=16,progressive=15,FE=1,
        source_A000=1,prelude_A000=4,C200=1,source_end=674,no_predicates_or_relative_sites=True,
        two_cold_boots9001_frames_each_planned=True,all_original_commands_retained_without_flattening=True,
        native_high_integer_constants_and_multiplicities_including_actor_getter_CB184_preserved=True,
        no_forced_timing_RGB_RNG_or_state_equivalence=True,no_natural_event187_eligibility_or_earned_state_claim=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared complete B187 paired content fixtures,9001-frame cold boots and16-panel actual display/transition review.')
