"""Bind the complete final B221 menu and both relocated label pointers in both even alignments."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B221_stored_choices_v6996')
PLAN=Path('work/analysis/lil_B221_relocation_v6994/all16_objects21_commands_four_relatives_full1208_inverse_RESEARCH.json')
DOC=Path('translations/lil_B221_choice_manuscript_v1.json')
NATIVE=Path('work/analysis/lil_B221_choices_v6977/three_original_choice_decoders_nine_modal_cases_twelve_complete_label_planes.json')
if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc,proof=map(read,[PLAN,DOC,NATIVE])
    assert sha(DOC.read_bytes())==plan['choice_manuscript_sha256']
    assert plan['candidate_sha256']==proof['candidate_sha256']==doc['current_ROM_sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    block=plan['blocks'][0];target=Path(block['research_block']).read_bytes()
    assert block['block']==221 and sha(target)==block['research_block_sha256']
    assert len(block['choice_commands'])==1 and len(doc['records'])==2
    menu=block['choice_commands'][0];at=menu['new_offset'];raw=bytes.fromhex(menu['target_hex'])
    assert menu['old_offset']==150 and menu['old_length']==28 and menu['new_length']==len(raw)==14
    assert target[at:at+14]==raw and proof['typed_target_object_hex']==raw.hex()
    assert proof['native_selection_cancel_cases']==9 and proof['complete_current_and_reviewed_style_label_planes']==12
    rows=sorted(doc['records'],key=lambda r:r['option_index'])
    assert [r['id'] for r in rows]==menu['record_IDs'] and [r['english'] for r in rows]==menu['labels']==['Yes','No']
    alignments=choice_getters(arm,dict(offset=at,word=0x2100,native_extent=14,whole_command_hex=raw.hex()))
    assert len(alignments)==2
    for case in alignments:
        assert case['count']==2 and [r['text'] for r in case['labels']]==['Yes','No']
        for label,ref in zip(case['labels'],menu['label_references'],strict=True):
            assert (label['option_index'],label['offset'],len(bytes.fromhex(label['hex'])))==(ref['option_index'],ref['new_offset'],ref['new_length'])
            assert target[:ref['new_offset']].count(b'\0')==ref['new_record_index']
    ROOT.mkdir(parents=True)
    save(ROOT/'one_final_typed_object_two_references_and_both_even_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),
        final_typed_menu_cases=[dict(old_command_offset=150,stored_command_offset=at,stored_target_hex=raw.hex(),
            actual_target_record_references=menu['label_references'],native_two_alignment_count_and_pointer_cases=alignments,
            complete_object_byte_identical_to_viewed_native_geometry_and_twelve_style_planes=True,
            reused_VM_selection_cancel_and_font_proof=str(NATIVE),reused_VM_selection_cancel_and_font_proof_sha256=sha(NATIVE.read_bytes()),
            source_count_two_option_order_selection_and_cancel_semantics_unchanged=True)],
        fresh_count_calls=2,fresh_label_pointer_calls=4,reused_native_selection_cancel_cases=9,reused_complete_current_reviewed_style_planes=12,
        one_stored_object_and_two_actual_offsets_record_indices_labels_and_counts_exact=True,
        final_stored_selection_font_and_geometry_reuse_not_new_actual_gameplay=True,
        no_new_choice_geometry_font_input_loop_or_actual_branch_claim=True,new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,DOC,NATIVE,Path(choice_getters.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print('One final menu/two label references pass both even alignments;9 VM cases/12 style planes reused by exact bytes. Actual English pending.')
