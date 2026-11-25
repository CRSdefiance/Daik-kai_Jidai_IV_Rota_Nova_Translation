"""Prepare complete paired B190 fixtures and read-only actual-display audits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_display_tools_v5337')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B186_display_fixture_v5166.py','scripts/research_lil_B190_display_fixture_v5337.py',{
        'B186':'B190','display_fixture_v5166':'display_fixture_v5337','display_v5166':'display_v5337',
        'combined_v5122':'combined_v5304','relocation_v5157':'relocation_v5328','editorial_manuscript_v5':'editorial_manuscript_v3',
        'bank[186]':'bank[190]','source_block=186':'source_block=190','len(commands)==24':'len(commands)==29',
        'len(walk)==33 and len(speeches)==12':'len(walk)==38 and len(speeches)==17','all33_stored':'all38_stored',
        'all12_speeches11_progressive1':'all17_speeches16_progressive1','closing_notice_names_Alexandria':'closing_notice_names_Havana',
        'source_event186':'source_event190','source_all24_commands':'source_all29_commands','stored_speech_objects=12':'stored_speech_objects=17',
        'all24 commands+9 original init commands,eleven progressive':'all29 commands+9 original init commands,sixteen progressive',
    })]
    rows.append(derive('scripts/pin_lil_B186_display_v5167.py','scripts/pin_lil_B190_display_v5338.py',{
        'B186':'B190','display_tools_v5167':'display_tools_v5338','display_fixture_v5166':'display_fixture_v5337',
        'source_speeches=12,progressive=11':'source_speeches=17,progressive=16','source_commands=24,stored_fixture_commands=33':'source_commands=29,stored_fixture_commands=38',
        'All12 panels':'All17 panels',
    }))
    rows.append(derive('scripts/run_lil_B186_display_fixture_v5168.py','scripts/run_lil_B190_display_fixture_v5339.py',{
        'B186':'B190','display_fixture_v5166':'display_fixture_v5337','display_run_v5168':'display_run_v5339','display_v5168':'display_v5339',
        'source_event186':'source_event190',"'displayed_original_source_block':186":"'displayed_original_source_block':190",
        'all_source24_commands_11_progressive1':'all_source29_commands_16_progressive1',
    }))
    rows.append(derive('scripts/audit_lil_B186_actual_v5169.py','scripts/audit_lil_B190_actual_v5340.py',{
        'B186':'B190','actual_v5169':'actual_v5340','display_fixture_v5166':'display_fixture_v5337',
        'fonts_v5154/all12_progressive_FE_native_planes_and96_alignment_cases':'fonts_v5326/all17_progressive_FE_native_planes_and136_alignment_cases',
        'display_run_v5168':'display_run_v5339','display_v5168':'display_v5339','source_event186':'source_event190',
        'all_source24_commands_11_progressive1':'all_source29_commands_16_progressive1',"source['block']!=186":"source['block']!=190",'original_source_block=186':'original_source_block=190',
        "pair.get('original_source_block')==186":"pair.get('original_source_block')==190","r.get('original_source_block')==186":"r.get('original_source_block')==190",
        'all33_stored':'all38_stored','==33':'==38','roll<700':'roll<500','roll==700':'roll==500',
        "selected[-1]['original_source_offset']==646":"selected[-1]['original_source_offset']==602",
        "len(intervals)==len({r['id'] for r in intervals})==12":"len(intervals)==len({r['id'] for r in intervals})==17",
        "predicates[0]['source_offset']==540":"predicates[0]['source_offset']==8",'in [560,572,584]':'in [28,40,52]',
        "ui[0]['original_source_offset']==644":"ui[0]['original_source_offset']==600",'single_source_end646':'single_source_end602',
        'len(actual)==12':'len(actual)==17','actual_all12':'actual_all17','fresh_actual_unique_speech_panels=12':'fresh_actual_unique_speech_panels=17',
        'all24_source_commands':'all29_source_commands','all12_speeches11_progressive1':'all17_speeches16_progressive1','actual_source_event186':'actual_source_event190','actual_panels=12':'actual_panels=17',
    }))
    rows.append(derive('scripts/review_lil_B186_actual_v5170.py','scripts/review_lil_B190_actual_v5341.py',{
        'B186':'B190','actual_review_v5170':'actual_review_v5341','actual_v5169':'actual_v5340','actual_all12':'actual_all17',
        'display_fixture_v5166':'display_fixture_v5337','display_v5168':'display_v5339','display_run_v5168':'display_run_v5339',
        "actual['complete_matching_observations']==12":"actual['complete_matching_observations']==17","len(actual['review_sheets'])==2":"len(actual['review_sheets'])==3",
        "len(v['selected_intervals'])==12":"len(v['selected_intervals'])==17",'single_source_end646':'single_source_end602',
        "['DK4_MES_B186_R0005','DK4_MES_B186_R0013','DK4_MES_B186_R0036','DK4_MES_B186_R0063']":"['DK4_MES_B190_R0032','DK4_MES_B190_R0056','DK4_MES_B190_R0067','DK4_MES_B190_R0085']",
        'all12_complete_held_planes':'all17_complete_held_planes','all12_speeches11_progressive1':'all17_speeches16_progressive1',
        'source_selected_effect_C200_single_end646':'source_selected_effect_C200_single_end602','source_event186':'source_event190',
        'conditional_commands12_planes':'conditional_commands17_planes','complete_panels=12':'complete_panels=17',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_complete_content_fixture_tools.json',dict(tools=rows,source_commands=29,original_B22_init_commands=9,stored_fixture_commands=38,
        speeches=17,progressive=16,FE=1,predicates=1,threshold=500,relative_sites=6,source_effects=3,
        two_cold_boots_9001_frames_each_planned=True,all_source_objects_stored_no_flattening=True,
        actual_outcome_RNG_timing_RGB_state_and_return_to_be_measured_without_forcing=True,
        no_natural_event190_eligibility_or_earned_state_claim=True,no_review_credit=True,full_goal_complete=False))
    print('Prepared complete B190 paired content fixtures and17-panel actual-display checks.')
