"""Prepare complete conditional content fixtures and read-only actual display checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_display_tools_v5166')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B182_display_fixture_v4903.py','scripts/research_lil_B186_display_fixture_v5166.py',{
        'B182':'B186','display_fixture_v4903':'display_fixture_v5166','display_v4903':'display_v5166',
        'combined_v4867':'combined_v5122','relocation_v4893':'relocation_v5157','editorial_manuscript_v3':'editorial_manuscript_v5',
        'bank[182]':'bank[186]','source_block=182':'source_block=186',
        'len(commands)==25':'len(commands)==24','len(walk)==34 and len(speeches)==8':'len(walk)==33 and len(speeches)==12',
        "sum(c['word']==0x8000 for c in walk)==2":"sum(c['word']==0x8000 for c in walk)==1",
        "sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==10":"sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==6",
        'all34_stored_fixture_commands':'all33_stored_fixture_commands',
        'all8_speeches7_progressive1_FE_two_predicates_ten_branches':'all12_speeches11_progressive1_FE_one_predicate_six_branches',
        'closing_notice_names_London':'closing_notice_names_Alexandria','source_event182_not_selected':'source_event186_not_selected',
        'source_all25_commands':'source_all24_commands','two_original_predicates_ten_relative_sites_preserved':'one_original_predicate_six_relative_sites_preserved',
        'stored_speech_objects=8':'stored_speech_objects=12',
        'all25 commands+9 original init commands,seven progressive/one impersonal FE,two predicates,ten relative sites':
        'all24 commands+9 original init commands,eleven progressive/one impersonal FE,one predicate,six relative sites',
    })]
    rows.append(derive('scripts/pin_lil_B182_display_v4904.py','scripts/pin_lil_B186_display_v5167.py',{
        'B182':'B186','display_tools_v4904':'display_tools_v5167','display_fixture_v4903':'display_fixture_v5166',
        'source_speeches=8,progressive=7':'source_speeches=12,progressive=11',
        'source_commands=25,stored_fixture_commands=34':'source_commands=24,stored_fixture_commands=33',
        'All8 panels':'All12 panels',
    }))
    rows.append(derive('scripts/run_lil_B182_display_fixture_v4905.py','scripts/run_lil_B186_display_fixture_v5168.py',{
        'B182':'B186','display_fixture_v4903':'display_fixture_v5166','display_run_v4905':'display_run_v5168','display_v4905':'display_v5168',
        'source_event182_not_selected':'source_event186_not_selected',"'displayed_original_source_block':182":"'displayed_original_source_block':186",
        'all_source25_commands_7_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained':
        'all_source24_commands_11_progressive1_FE_one_predicate_six_branches_three_A000_C200_end_retained',
    }))
    rows.append(derive('scripts/audit_lil_B182_actual_v4906.py','scripts/audit_lil_B186_actual_v5169.py',{
        'B182':'B186','actual_v4906':'actual_v5169','display_fixture_v4903':'display_fixture_v5166',
        'fonts_v4891/all8_progressive_FE_native_planes_and64_alignment_cases':'fonts_v5154/all12_progressive_FE_native_planes_and96_alignment_cases',
        'display_run_v4905':'display_run_v5168','display_v4905':'display_v5168','source_event182_not_selected':'source_event186_not_selected',
        'all_source25_commands_7_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained':
        'all_source24_commands_11_progressive1_FE_one_predicate_six_branches_three_A000_C200_end_retained',
        "source['block']!=182":"source['block']!=186",'original_source_block=182':'original_source_block=186',
        "pair.get('original_source_block')==182":"pair.get('original_source_block')==186",
        "r.get('original_source_block')==182":"r.get('original_source_block')==186",
        'all34_stored_fixture_commands':'all33_stored_fixture_commands','==34':'==33',
        'roll<500':'roll<700','roll==500':'roll==700',
        "selected[-1]['original_source_offset']==632":"selected[-1]['original_source_offset']==646",
        "len(intervals)==len({r['id'] for r in intervals})==8":"len(intervals)==len({r['id'] for r in intervals})==12",
        "len(predicates) in [1,2] and predicates[0]['source_offset']==512":"len(predicates)==1 and predicates[0]['source_offset']==540",
        'in [532,564,576]':'in [560,572,584]',"ui[0]['original_source_offset']==630":"ui[0]['original_source_offset']==644",
        'single_source_end632':'single_source_end646','len(actual)==8':'len(actual)==12','actual_all8':'actual_all12',
        'fresh_actual_unique_speech_panels=8':'fresh_actual_unique_speech_panels=12','all25_source_commands':'all24_source_commands',
        'all8_speeches7_progressive1':'all12_speeches11_progressive1','actual_source_event182':'actual_source_event186','actual_panels=8':'actual_panels=12',
    }))
    rows.append(derive('scripts/review_lil_B182_actual_v4907.py','scripts/review_lil_B186_actual_v5170.py',{
        'B182':'B186','actual_review_v4907':'actual_review_v5170','actual_v4906':'actual_v5169',
        'actual_all8':'actual_all12','display_fixture_v4903':'display_fixture_v5166','display_v4905':'display_v5168','display_run_v4905':'display_run_v5168',
        "actual['complete_matching_observations']==8":"actual['complete_matching_observations']==12",
        "len(v['selected_intervals'])==8":"len(v['selected_intervals'])==12",'single_source_end632':'single_source_end646',
        "['DK4_MES_B182_R0005','DK4_MES_B182_R0014','DK4_MES_B182_R0025','DK4_MES_B182_R0062']":
        "['DK4_MES_B186_R0005','DK4_MES_B186_R0013','DK4_MES_B186_R0036','DK4_MES_B186_R0063']",
        'all8_complete_held_planes':'all12_complete_held_planes','all8_speeches7_progressive1':'all12_speeches11_progressive1',
        'source_selected_effect_C200_single_end632':'source_selected_effect_C200_single_end646',
        'source_event182_natural':'source_event186_natural','conditional_commands8_planes':'conditional_commands12_planes','complete_panels=8':'complete_panels=12',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,
        source_commands=24,original_B22_init_commands=9,stored_fixture_commands=33,speeches=12,progressive=11,FE=1,
        predicates=1,threshold=700,relative_sites=6,source_effects=3,prelude_effects=4,
        two_cold_boots_9001_frames_each_planned=True,all_source_objects_stored_no_flattening=True,
        actual_outcome_RNG_timing_RGB_state_and_return_to_be_measured_without_forcing=True,
        no_actual_natural_event186_eligibility_or_earned_state_claim=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared complete B186 Japanese/English fixtures,paired cold boots and12-panel conditional display audit.')
