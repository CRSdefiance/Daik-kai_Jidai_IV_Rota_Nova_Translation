"""Seal the complete inspected three-Lady source/native/reference/actual scope."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_seal_tools_v5475')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/seal_lil_B192_references_v5434.py');text=source.read_text(encoding='utf-8')
    a=text.index("    assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])");b=text.index("    assert visual['whole_RGB_final9001_equal']",a)
    measured="    assert not visual['sampled_postscene_whole_RGB_differences_unmasked'] and visual['all_sampled_postscene_whole_RGB_equal']\n    assert visual['ten_speech_timing_differences_retained_without_masking_retiming_or_equivalence_claim'] and visual['three_distinct_original_Lady_portraits_and_four_row_explanation_cooking_offer_and_friendship_observed']\n"
    row=derive(source,'scripts/seal_lil_B193_references_v5475.py',{
        text[a:b]:measured,'B192':'B193','all eight':'all fifteen','prepare_lil_B192_research_v5422':'prepare_lil_B193_research_v5463',
        'reference_approval_v5434':'reference_approval_v5475','reference_census_v5425/all11':'reference_census_v5466/all18','relocated_controls_v5427/all8':'relocated_controls_v5468/all15',
        'stored_v5421/all8_final_stored_targets32':'stored_v5462/all15_final_stored_targets60','ends_v5426':'ends_v5467',
        'actual_v5431/actual_all8':'actual_v5472/actual_all15','display_fixture_v5428':'display_fixture_v5469',
        'actual_review_v5432/all8_panels26_fullscreens_linear_return':'actual_review_v5473/all15_panels12_fullscreens_three_Ladies_return',
        'relocation_tools_v5420/viewed_layout_retention_reasons.json':'relocation_tools_v5461/viewed_layout_retention_reasons_v2.json',
        'all11':'all18','all8_active':'all15_active','progressive7':'progressive14','single_end398_actual_target372':'single_end662_actual_target672',
        "len(control['relocated_dispatch_cases'])==8":"len(control['relocated_dispatch_cases'])==15", "stored['current_final_stored_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==60",
        'all8_final_targets':'all15_final_targets','==(16,16)':'==(32,28)',"actual['fresh_actual_unique_speech_panels']==8":"actual['fresh_actual_unique_speech_panels']==15",'==[20,20]':'==[27,27]','==[4775,4777]':'==[6457,6457]',
        "len(f['all20_stored_fixture_commands'])==20":"len(f['all27_stored_fixture_commands'])==27",
        "len(visual['all_actual_consumer_sheets_viewed'])==2":"len(visual['all_actual_consumer_sheets_viewed'])==3","len(visual['paired_full_screen_views'])==7":"len(visual['paired_full_screen_views'])==3",
        'dict(total=9,speech=7,control_or_end=2)':'dict(total=10,speech=10,control_or_end=0)',"assert not visual['PRNG_equality']":"assert visual['PRNG_equality']",'[790984746,3723009301]':'[463267532,463267532]',
        'len(set(ids))==8':'len(set(ids))==15','all8_panels7_progressive1':'all15_panels14_progressive1','original11_commands':'original18_commands',
        'source_end398_actual_target372':'source_end662_actual_target672','and31_native_holds':'and59_native_holds','PRNG_equality=False':'PRNG_equality=True',
        'final9001_RGB_equal_and7_sampled_original_indicator_differences_disclosed':'all_sampled_postscene_and_final9001_RGB_equal',
        "block['block']==checked['block']==192 and len(block['command_map'])==11 and len(block['text_records'])==8":
        "block['block']==checked['block']==193 and len(block['command_map'])==18 and len(block['text_records'])==15",'==[(398,372)]':'==[(662,672)]','all8_source_native_reference':'all15_source_native_reference',
        'B192 sealed:8 objects,11 commands,31 native holds':'B193 sealed:15 objects,18 commands,59 native holds'} )
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({790984746:1,3723009301:1}) and new-old==Counter({463267532:2})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_seal.json',dict(derivation=row,only_measured_PRNG_high_integer_changes=True,
        corrected111_character_layout_receipt_and_original_receipt_both_preserved=True,three_portraits_four_rows_cooking_friendship_and_measured_timing_scope_required=True,new_review_credit=0,full_goal_complete=False))
