"""Prepare complete four-speaker source/native/reference/actual approval."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_seal_tools_v5301')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/seal_lil_B187_references_v5216.py');text=source.read_text(encoding='utf-8')
    row=derive(source,'scripts/seal_lil_B189_references_v5301.py',{
        'B187':'B189','prepare_lil_B187_research_v5204':'prepare_lil_B189_research_v5289','reference_approval_v5216':'reference_approval_v5301',
        'reference_census_v5207/all19':'reference_census_v5292/all20','relocated_controls_v5209/all16':'relocated_controls_v5294/all17',
        'stored_v5203/all16_final_stored_targets64':'stored_v5288/all17_final_stored_targets68','ends_v5208':'ends_v5293',
        'actual_v5213/actual_all16':'actual_v5298/actual_all17','display_fixture_v5210':'display_fixture_v5295',
        'actual_review_v5214/all16_panels12_fullscreens_linear_return':'actual_review_v5299/all17_panels12_fullscreens_two_pair_return',
        'all19':'all20','all16':'all17','progressive15':'progressive16','15_progressive':'16_progressive','single_end674_actual_target710':'single_end766_actual_target844',
        "len(control['relocated_dispatch_cases'])==16":"len(control['relocated_dispatch_cases'])==17",
        "stored['current_final_stored_macro_alignment_cases']==64":"stored['current_final_stored_macro_alignment_cases']==68",'==(32,32)':'==(40,28)',
        "actual['fresh_actual_unique_speech_panels']==16":"actual['fresh_actual_unique_speech_panels']==17",'==[28,28]':'==[29,29]','==[6694,6695]':'==[6937,6937]',
        "len(f['all28_stored_fixture_commands'])==28":"len(f['all29_stored_fixture_commands'])==29",'all28_stored_fixture_commands':'all29_stored_fixture_commands',
        'dict(total=16,speech=14,control_or_end=2)':'dict(total=8,speech=8,control_or_end=0)',
        "assert visual['PRNG_equality']":"assert not visual['PRNG_equality']",'[2467799992,2467799992]':'[463267532,3723009301]',
        'len(set(ids))==16':'len(set(ids))==17','original19_commands':'original20_commands','source_end674_actual_target710':'source_end766_actual_target844',
        'all115_upper_portrait_name_samples_and63_native_holds_equal':'all115_upper_portrait_name_samples_and67_native_holds_equal','PRNG_equality=True':'PRNG_equality=False',
        "block['block']==checked['block']==187 and len(block['command_map'])==19 and len(block['text_records'])==16":
        "block['block']==checked['block']==189 and len(block['command_map'])==20 and len(block['text_records'])==17",'==[(674,710)]':'==[(766,844)]',
        "paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path(__file__)]":
        "paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path('work/analysis/lil_B189_relocation_tools_v5287/viewed_layout_retention_reasons.json'),Path('work/analysis/lil_B189_source_tools_v5273/hex_decimal_selector_correction.json'),Path(__file__)]",
        "    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)":
        "    layout=Path('work/analysis/lil_B189_relocation_tools_v5287/viewed_layout_retention_reasons.json')\n    doc.update(layout_retention_review_proof=str(layout),layout_retention_review_proof_sha256=sha(layout.read_bytes()))\n    reasons={r['id']:r['reason'] for r in read(layout)['retained_layouts']}\n    for r in doc['records']:\n        if r['id'] in reasons:r['native_layout_retention_reason']=reasons[r['id']]\n    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)",
        'B187 sealed:16 objects,19 commands,63 native holds':'B189 sealed:17 objects,20 commands,67 native holds',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({2467799992:2}) and new-old==Counter({463267532:1,3723009301:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_seal.json',dict(derivation=row,measured_PRNG_data_only_high_integer_change=True,
        exact_native_gates_four_speakers_and_viewed_actual_evidence_required=True,layout_retention_and_selector_correction_preserved=True,new_review_credit=0,full_goal_complete=False))
