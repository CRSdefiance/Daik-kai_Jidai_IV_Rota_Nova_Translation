"""Bind all six final typed menu objects,actual references and both alignments."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_stored_choices_v5933')
PLAN=Path('work/analysis/lil_B201_relocation_v5931/nested_source_relocation_research.json')
DOC=Path('translations/lil_B201_choice_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,doc=read(PLAN),read(DOC)
    assert sha(DOC.read_bytes())==plan['choices_sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    summary=read(doc['typed_choice_proof']);oldproofs={r['command_offset']:r for r in summary['menus']}
    block=plan['blocks'][0];target=Path(block['research_block']).read_bytes()
    assert block['block']==201 and sha(target)==block['research_block_sha256']
    assert len(block['choice_commands'])==1 and len(doc['records'])==2
    cases=[];evidence={str(p):sha(p.read_bytes()) for p in [PLAN,DOC,Path(doc['typed_choice_proof']),Path(__file__)]}
    for menu in block['choice_commands']:
        at=menu['new_offset'];raw=bytes.fromhex(menu['target_hex'])
        assert menu['old_length']==22 and menu['new_length']==len(raw)==16 and target[at:at+16]==raw
        old=oldproofs[menu['old_offset']];path=Path(old['proof']);proof=read(path)
        assert sha(path.read_bytes())==old['sha256'] and proof['candidate_sha256']==doc['current_ROM_sha256']
        assert proof['typed_target_object_hex']==menu['target_hex']
        assert proof['six_original_VM_selection_and_cancel_cases_pass'] and proof['eight_complete_native_style_label_planes_pass']
        rows=sorted([r for r in doc['records'] if r['command_offset']==menu['old_offset']],key=lambda r:r['option_index'])
        assert [r['id'] for r in rows]==menu['record_IDs'] and [r['english'] for r in rows]==menu['labels']==['Buy','Pass']
        command=dict(offset=at,word=0x2100,native_extent=16,whole_command_hex=raw.hex())
        alignments=choice_getters(arm,command);assert len(alignments)==2
        for case in alignments:
            assert case['count']==2 and [r['text'] for r in case['labels']]==['Buy','Pass']
            for label,ref in zip(case['labels'],menu['label_references'],strict=True):
                assert (label['option_index'],label['offset'],len(bytes.fromhex(label['hex'])))==(ref['option_index'],ref['new_offset'],ref['new_length'])
                assert target[:ref['new_offset']].count(b'\0')==ref['new_record_index']
        evidence[str(path)]=sha(path.read_bytes())
        cases.append(dict(old_command_offset=menu['old_offset'],stored_command_offset=at,stored_target_hex=raw.hex(),
            actual_target_record_references=menu['label_references'],native_two_alignment_count_and_pointer_cases=alignments,
            complete_object_byte_identical_to_viewed_native_geometry_and8_style_planes=True,
            reused_VM_selection_cancel_and_font_proof=str(path),reused_VM_selection_cancel_and_font_proof_sha256=sha(path.read_bytes()),
            source_count_two_option_order_selection_and_cancel_semantics_unchanged=True,
            final_stored_selection_font_and_geometry_reuse_not_new_actual_gameplay=True))
    ROOT.mkdir(parents=True);save(ROOT/'one_final_typed_object_two_references_and_both_even_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),final_typed_menu_cases=cases,
        fresh_count_calls=2,fresh_label_pointer_calls=4,reused_native_selection_cancel_cases=6,reused_complete_current_reviewed_style_planes=8,
        one_stored_object_and_two_actual_offsets_record_indices_labels_and_counts_exact=True,
        no_new_choice_geometry_font_input_loop_or_actual_branch_claim=True,evidence=evidence,
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('One stored menu/two label references match native counts/pointers in both even alignments.six selection/cancel cases andeight style planes reused by exact object bytes;no gameplay claim.')
