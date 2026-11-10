"""Bind the final three-option object and every exact relocated label reference."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.map_lil_B197_source_v5647 import choice_getters3
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_stored_choices_v5673')
PLAN=Path('work/analysis/lil_B197_relocation_v5671/nested_source_relocation_research.json')
DOC=Path('translations/lil_B197_choice_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,doc=map(read,[PLAN,DOC])
    assert sha(DOC.read_bytes())==plan['choices_sha256']
    arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin')
    summary=read(doc['typed_choice_proof']);assert len(summary['menus'])==1
    block=plan['blocks'][0];target=Path(block['research_block']).read_bytes()
    assert block['block']==197 and sha(target)==block['research_block_sha256']
    assert len(block['choice_commands'])==1 and len(doc['records'])==3
    menu=block['choice_commands'][0];at=menu['new_offset'];raw=bytes.fromhex(menu['target_hex'])
    assert menu['old_offset']==230 and menu['old_length']==34 and menu['new_length']==len(raw)==40
    assert target[at:at+len(raw)]==raw and menu['text_base']==8 and menu['count']==3
    item=summary['menus'][0];path=Path(item['proof']);proof=read(path)
    assert sha(path.read_bytes())==item['sha256'] and proof['candidate_sha256']==doc['current_ROM_sha256']
    assert proof['typed_target_object_hex']==menu['target_hex']
    assert proof['eight_original_VM_selection_and_cancel_cases_pass'] and proof['twelve_complete_native_style_label_planes_pass']
    rows=sorted(doc['records'],key=lambda r:r['option_index'])
    assert [r['id'] for r in rows]==menu['record_IDs']
    assert [r['english'] for r in rows]==menu['labels']==["Let's buy it",'Pass','You decide']
    command=dict(offset=at,word=0x2200,native_extent=len(raw),whole_command_hex=raw.hex())
    cases=choice_getters3(arm,command);assert len(cases)==2
    for c in cases:
        assert c['count']==3 and [r['text'] for r in c['labels']]==menu['labels']
        for label,ref in zip(c['labels'],menu['label_references'],strict=True):
            assert (label['option_index'],label['offset'],len(bytes.fromhex(label['hex'])))==(ref['option_index'],ref['new_offset'],ref['new_length'])
            assert target[:ref['new_offset']].count(b'\0')==ref['new_record_index']
    ROOT.mkdir(parents=True);save(ROOT/'one_final_typed_object_three_exact_references_and_both_even_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),stored_command_offset=at,stored_target_hex=raw.hex(),
        actual_target_record_references=menu['label_references'],native_two_alignment_count_and_pointer_cases=cases,
        fresh_count_calls=2,fresh_label_pointer_calls=6,reused_native_selection_cancel_cases=8,reused_complete_current_reviewed_style_planes=12,
        reused_VM_selection_cancel_and_font_proof=str(path),reused_VM_selection_cancel_and_font_proof_sha256=sha(path.read_bytes()),
        exact_object_reuse_matches_viewed_native_geometry_all_labels_and_both_styles=True,
        source_count3_option_order_and_original_selection_cancel_results_preserved=True,
        no_new_geometry_font_input_loop_or_actual_English_branch_claim=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,DOC,path,Path(doc['typed_choice_proof']),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B197 stored2200:all3 exact label offsets,lengths,null-record indices and two native count/six pointer calls pass.8 VM cases/12 style planes reused by exact bytes;English actual pending.')
