"""Reuse exact compiled planes and freshly test eleven parity tails plus relocated menu alignment."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_stored_tools_v7939');assert not root.exists()
    view="""    viewed=read('work/analysis/Rafael_B46_native_review_v7935/24_pages2_choices_full_native_review_individual_wrap_reasons.json')
    assert viewed['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and len(viewed['directly_viewed_sheets'])==5 and all(s['directly_viewed'] for s in viewed['directly_viewed_sheets'])
    assert native['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes())
"""
    menu="""    from scripts.source_locked_derivation_v5118 import checked_text
    from scripts import verify_ship_advice_choice_centering_20261022 as original
    cp=Path('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
    fp=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
    choice,flow=map(read,[cp,fp]);m=relocation['groups'][0]['choice_commands'][0];start=m['new_offset']
    obj=target[start:start+m['new_length']];assert obj.hex()==m['target_hex']==choice['target_menu_object_hex']
    adapter=checked_text(flow['source_owned_VM_adapter'],{
        'def choice_vm(arm, object_bytes):':'def choice_vm(arm, object_bytes, alignment):',
        "    cpu.mem_write(text - 16, b'\\\\xA5' * 96)":"    assert alignment in [0,2];text+=alignment\\n    cpu.mem_write(text - 16, b'\\\\xA5' * 96)",
    })
    env=dict(original.__dict__);exec(compile(adapter,__file__+'::aligned-complete-relocated-menu','exec'),env)
    menus=[]
    for alignment in [0,2]:
        result=env['choice_vm'](arm,obj,alignment);assert result==choice['native_target_VM']
        menus.append(dict(object_alignment_mod4=alignment,actual_relocated_menu_alignment=alignment==start%4,native_VM=result,modal_loop_bridged_not_actual_controller_selection=True))
    assert start%4==2 and len(m['label_references'])==2
    for r in m['label_references']:
        at=r['new_offset'];value=bytes.fromhex(r['target_hex'])
        assert target[at:at+len(value)+1]==value+b'\\0' and value.decode('ascii')==doc['typed_choice_records'][r['option_index']]['english']
    save(ROOT/'two_stored_menu_labels_exact8_viewed_planes_two_header_alignments.json',dict(
        research_block=str(blockpath),research_block_sha256=sha(target),menu=m,stored_menu_hex=obj.hex(),
        complete_original_VM_provider_geometry_andthree_returns_at_both_even_header_alignments=menus,
        label_font_proof=str(cp),label_font_proof_sha256=sha(cp.read_bytes()),all8_current_target_style_planes_reused_by_exact_label_andwidth=True,
        source_owned_alignment_adapter=adapter,actual_backing_highlights_andcontroller_selection_pending=True,
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [cp,fp,Path(__file__)]},full_goal_complete=False))
"""
    row=derive('scripts/prove_Rafael_B45_stored_v7885.py','scripts/prove_Rafael_B46_stored_v7939.py',{
        'Check seven compiler parity tails freshly; reuse five exact already-viewed stored bodies.':'Check eleven compiler parity tails freshly;reuse thirteen exact viewed bodies andverify relocated two-choice alignment.',
        'Rafael_B45_stored_v7885':'Rafael_B46_stored_v7939',
        'Rafael_B45_relocation_v7884/one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json':'Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json',
        'Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json':'Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json',
        'rafael_B45_editorial_manuscript_v3':'rafael_B46_editorial_manuscript_v2',
        'Rafael_B45_logical_refined_v7876b/12_refined_logical_bindings44_reused4_fresh_alignments.json':'Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json',
        "    assert native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and native['visual_review_pending'] is False":view.rstrip(),
        'blocks[45]':'blocks[46]',
        "block=45,source_selector":"block=46,source_selector",
        '    assert len(rows)==12 and len(fresh)==7 and len(reused)==5 and not ctx.machines':menu+'    assert len(rows)==24 and len(fresh)==11 and len(reused)==13 and not ctx.machines',
        'all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json':'all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json',
        'fresh_native_alignment_cases=28,exact_reused_native_alignment_cases=20':'fresh_native_alignment_cases=44,exact_reused_native_alignment_cases=52',
        'all12_complete_native_pages_full_first_internal_final_glyphs_bounds_andconsumption_pass':'all24_complete_native_pages_full_first_internal_final_glyphs_bounds_andconsumption_pass',
        'all12_native_ink_planes_exact_to_already_viewed':'all24_native_ink_planes_exact_to_already_viewed',
        'seven_parity_tails_create_no_blank_oradditional_page':'eleven_parity_tails_create_no_blank_oradditional_page',
        'all12_complete_six_byte_preambles_andonly_source00_prefix_zeros_preserved':'all24_complete_six_byte_preambles_andonly_source00_prefix_zeros_preserved',
        'FE_original_null_actor_FO20_percent_logical_andphysical_planes_exact':'all12_FE_original_null_actor_zero_macro_logical_andphysical_planes_exact',
        'All12 stored bodies pass:seven parity tails fresh/28alignments;five exact bodies reuse20cases. All viewed ink planes exact;no extra orblank pages. Actual/caller/loader/release pending.':'All24 stored bodies pass:11 parity tails fresh/44 alignments;13 exact bodies reuse52 cases. All viewed planes exact. Menu both-even alignments pass. Actual/caller/loader/release pending.',
    })
    root.mkdir(parents=True);save(root/'provenance.json',row)
