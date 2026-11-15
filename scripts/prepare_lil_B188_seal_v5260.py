"""Prepare the complete source/native/reference/actual B188 approval."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_seal_tools_v5260')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/seal_lil_B187_references_v5216.py');text=source.read_text(encoding='utf-8')
    row=derive(source,'scripts/seal_lil_B188_references_v5260.py',{
        'B187':'B188','prepare_lil_B187_research_v5204':'prepare_lil_B188_research_v5248','reference_approval_v5216':'reference_approval_v5260',
        'reference_census_v5207/all19':'reference_census_v5251/all14','relocated_controls_v5209/all16':'relocated_controls_v5253/all11',
        'stored_v5203/all16_final_stored_targets64':'stored_v5247/all11_final_stored_targets44','ends_v5208':'ends_v5252',
        'actual_v5213/actual_all16':'actual_v5257/actual_all11','display_fixture_v5210':'display_fixture_v5254',
        'actual_review_v5214/all16_panels12_fullscreens':'actual_review_v5258/all11_panels36_fullscreens',
        'all19':'all14','all16':'all11','progressive15':'progressive10','15_progressive':'10_progressive','11_progressive1':'10_progressive1',
        'single_end674_actual_target710':'single_end478_actual_target420',
        "len(control['relocated_dispatch_cases'])==16":"len(control['relocated_dispatch_cases'])==11",
        "stored['current_final_stored_macro_alignment_cases']==64":"stored['current_final_stored_macro_alignment_cases']==44",'==(32,32)':'==(28,16)',
        "actual['fresh_actual_unique_speech_panels']==16":"actual['fresh_actual_unique_speech_panels']==11",'==[28,28]':'==[23,23]','==[6694,6695]':'==[5495,5497]',
        'all28_stored_fixture_commands':'all23_stored_fixture_commands',"len(f['all28_stored_fixture_commands'])==28":"len(f['all23_stored_fixture_commands'])==23",
        "len(visual['all_actual_consumer_sheets_viewed'])==len(visual['paired_full_screen_views'])==3":"len(visual['all_actual_consumer_sheets_viewed'])==2 and len(visual['paired_full_screen_views'])==9",
        'dict(total=16,speech=14,control_or_end=2)':'dict(total=11,speech=9,control_or_end=2)',
        "assert not visual['sampled_postscene_whole_RGB_differences_unmasked'] and visual['all_sampled_postscene_whole_RGB_equal']":
        "assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==12 and not visual['all_sampled_postscene_whole_RGB_equal']\n    assert visual['eleven_timing_twelve_original_indicator_and_unequal_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim']",
        "assert visual['PRNG_equality']":"assert not visual['PRNG_equality']",'[2467799992,2467799992]':'[403514907,1520957695]',
        'len(set(ids))==16':'len(set(ids))==11','original19_commands':'original14_commands','source_end674_actual_target710':'source_end478_actual_target420',
        'all115_upper_portrait_name_samples_and63_native_holds_equal':'all115_upper_portrait_name_samples_and43_native_holds_equal',
        'PRNG_equality=True':'PRNG_equality=False','sampled_postscene_RGB_and_final9001_equal=True':'final9001_RGB_equal_and12_sampled_original_indicator_differences_disclosed=True',
        "block['block']==checked['block']==187 and len(block['command_map'])==19 and len(block['text_records'])==16":
        "block['block']==checked['block']==188 and len(block['command_map'])==14 and len(block['text_records'])==11",'==[(674,710)]':'==[(478,420)]',
        "paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path(__file__)]":
        "paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path('work/analysis/lil_B188_relocation_tools_v5246/viewed_layout_retention_reasons.json'),Path(__file__)]",
        "    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)":
        "    layout=Path('work/analysis/lil_B188_relocation_tools_v5246/viewed_layout_retention_reasons.json')\n    doc.update(layout_retention_review_proof=str(layout),layout_retention_review_proof_sha256=sha(layout.read_bytes()))\n    reasons={r['id']:r['reason'] for r in read(layout)['retained_layouts']}\n    for r in doc['records']:\n        if r['id'] in reasons:r['native_layout_retention_reason']=reasons[r['id']]\n    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)",
        'B187 sealed:16 objects,19 commands,63 native holds':'B188 sealed:11 objects,14 commands,43 native holds',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({2467799992:2}) and new-old==Counter({403514907:1,1520957695:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_seal.json',dict(derivation=row,measured_PRNG_data_only_high_integer_change=True,
        exact_native_gates_and_viewed_actual_evidence_required=True,layout_retention_reasons_preserved=True,new_review_credit=0,full_goal_complete=False))
