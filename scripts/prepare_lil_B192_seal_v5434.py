"""Bind all eight source/native/reference and inspected actual approvals."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_seal_tools_v5434')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/seal_lil_B188_references_v5260.py');text=source.read_text(encoding='utf-8')
    row=derive(source,'scripts/seal_lil_B192_references_v5434.py',{
        'B188':'B192','Seal the sixteen':'Seal all eight','prepare_lil_B188_research_v5248':'prepare_lil_B192_research_v5422',
        'reference_approval_v5260':'reference_approval_v5434','reference_census_v5251/all14':'reference_census_v5425/all11',
        'relocated_controls_v5253/all11':'relocated_controls_v5427/all8','stored_v5247/all11_final_stored_targets44':'stored_v5421/all8_final_stored_targets32',
        'ends_v5252':'ends_v5426','actual_v5257/actual_all11':'actual_v5431/actual_all8','display_fixture_v5254':'display_fixture_v5428',
        'actual_review_v5258/all11_panels36_fullscreens':'actual_review_v5432/all8_panels26_fullscreens','relocation_tools_v5246':'relocation_tools_v5420',
        'all14':'all11','all11_active':'all8_active','progressive10':'progressive7','single_end478_actual_target420':'single_end398_actual_target372',
        "len(control['relocated_dispatch_cases'])==11":"len(control['relocated_dispatch_cases'])==8",
        "stored['current_final_stored_macro_alignment_cases']==44":"stored['current_final_stored_macro_alignment_cases']==32",'all11_final_targets':'all8_final_targets','==(28,16)':'==(16,16)',
        "actual['fresh_actual_unique_speech_panels']==11":"actual['fresh_actual_unique_speech_panels']==8",'==[23,23]':'==[20,20]','==[5495,5497]':'==[4775,4777]',
        "len(f['all23_stored_fixture_commands'])==23":"len(f['all20_stored_fixture_commands'])==20",
        "len(visual['paired_full_screen_views'])==9":"len(visual['paired_full_screen_views'])==7",'dict(total=11,speech=9,control_or_end=2)':'dict(total=9,speech=7,control_or_end=2)',
        "len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==12":"len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==7",
        'eleven_timing_twelve_original_indicator':'nine_timing_seven_original_indicator','[403514907,1520957695]':'[790984746,3723009301]',
        'len(set(ids))==11':'len(set(ids))==8','all11_panels10_progressive1':'all8_panels7_progressive1','original14_commands':'original11_commands',
        'source_end478_actual_target420':'source_end398_actual_target372','and43_native_holds':'and31_native_holds','and12_sampled_original_indicator':'and7_sampled_original_indicator',
        "block['block']==checked['block']==188 and len(block['command_map'])==14 and len(block['text_records'])==11":
        "block['block']==checked['block']==192 and len(block['command_map'])==11 and len(block['text_records'])==8",'==[(478,420)]':'==[(398,372)]',
        'all11_source_native_reference':'all8_source_native_reference','B188 sealed:11 objects,14 commands,43 native holds':'B192 sealed:8 objects,11 commands,31 native holds',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({403514907:1,1520957695:1}) and new-old==Counter({790984746:1,3723009301:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_seal.json',dict(derivation=row,only_measured_PRNG_data_high_integer_changes=True,
        complete_source_native_reference_actual_and_individual_layout_reasons_required=True,new_review_credit=0,full_goal_complete=False))
