"""Prepare final stored planes, original pauses/menus, loaders and censuses."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B122_B127_reference_tools_v3289');assert not root.exists();pairs=[]
    def generate(old,new,swaps):
        old,new=Path(old),Path(new);assert not new.exists();text=old.read_text(encoding='utf-8')
        for a,b in swaps.items():assert a in text,a;text=text.replace(a,b)
        return old,new,text
    old,new,text=generate('scripts/prepare_lil_B111_B119_research_v3240b.py','scripts/prepare_lil_B122_B127_research_v3289b.py',{
        'lil_B111_B119_research_v3240b':'lil_B122_B127_research_v3289b',
        'lil_B111_B119_V3204_derived_RESEARCH_ONLY.nds':'lil_B122_B127_V3251_derived_RESEARCH_ONLY.nds',
        'all_routes_combined_v3204_candidate.nds':'all_routes_combined_v3251_candidate.nds',
        'lil_B111_B119_relocation_v3239b':'lil_B122_B127_relocation_v3288b',
        'lil_B111_B119_font_approval_v3236/all150_native_macro_font_reconciliation.json':'lil_B122_B127_native_approval_v3285/all159_native_macro_font_choice_reconciliation.json',
        'verify_lil_B111_B119_fonts_v3234c':'verify_lil_B122_B127_fonts_v3283',
        'verify_lil_B111_B119_FE_v3231':'verify_lil_B122_B127_FE_v3284',
        'lil_B111_B119_fonts_v3234c':'lil_B122_B127_fonts_v3283',
        'all116speech_34aliased_alternatives_no_choices_and64_relative_operands_preserved':'all155speech_four_choice_labels_and64_relative_operands_preserved',
        'range(111,120)':'range(122,128)',
        'value[0] in [2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220,254]':'value[0] in [2,6,9,20,26,92,95,151,254]',
        'len(parity)==150 and macro_calls==600':'len(parity)==155 and macro_calls==620',
        'all327_other_SC2_blocks_every_other_file_and_native_component_exact':'all330_other_SC2_blocks_every_other_file_and_native_component_exact',
        'all150_final_targets_complete_native_planes_equal_reviewed_planes':'all155_final_targets_complete_native_planes_equal_reviewed_planes',
        'current_final_padded_macro_alignment_cases=600':'current_final_padded_macro_alignment_cases=620',
        'all34_actual_virtual_prefixes_excluded_from_physical_alternative_body':'all155_complete_source_static_or_FE_prefixes_preserved',
        'all1_FE_final_plane_and4_macro_alignments_bound':'all10_FE_final_planes_and40_macro_alignments_bound',
        'all149_progressive_final_planes_and596_macro_alignments_bound':'all145_progressive_final_planes_and580_macro_alignments_bound',
        'actual_selected_B111_B119_IDs':'actual_selected_B122_B127_IDs',
        'V3204-derived nine-block':'V3251-derived six-block',
        'Research image:nine selectedSC2blocks only;327otherblocks/allotherfiles/components exact.150final nativeplanes/600macro cases pass;not a release ornewparent.':'Research image:six selectedSC2blocks only;330otherblocks/allotherfiles/components exact.155final nativeplanes/620macro cases,menus andsource2000resume bindings pass;not a release ornewparent.'})
    anchor='    parity=[];macro_calls=0';assert anchor in text
    text=text.replace(anchor,"    from scripts.map_lil_B122_B127_source_v3260c import choice_getters,control2000\n    from scripts.verify_ship_advice_choice_centering_20261022 import choice_vm\n    menus=[];pauses=[]\n"+anchor)
    anchor='        container.blocks[n]=target';assert anchor in text
    text=text.replace(anchor,'''        for c in block['choice_commands']:
            value=bytes.fromhex(c['target_hex']);assert target[c['new_offset']:c['new_offset']+len(value)]==value
            getters=choice_getters(arm,dict(whole_command_hex=value.hex(),offset=c['new_offset'],native_extent=len(value)))
            assert all([r['text'] for r in g['labels']]==c['labels'] for g in getters)
            approved=next(m for m in font['menu_targets'] if (m['block'],m['command_offset'])==(n,c['old_offset']))
            assert approved['object_hex']==value.hex() and approved['labels']==c['labels']
            vm=choice_vm(arm,value);assert vm['labels']==c['labels'] and vm['native_menu_rectangle']==approved['native_geometry'] and [r['modal_selection'] for r in vm['VM_cases']]==[0,1,-1]
            menus.append(dict(block=n,old_offset=c['old_offset'],new_offset=c['new_offset'],whole_target_object_hex=value.hex(),getters=getters,original_VM_selection_cancel_and_geometry=vm,complete_label_planes_bound_by_exact_approved_object=True))
        for c in block['original2000_pause_and_resume_maps']:
            assert target[c['new_offset']:c['target_resume']]==b'\\0\\x20' and c['target_resume']==c['new_offset']+2
            cases=control2000(arm,dict(whole_command_hex='0020',native_extent=2))
            assert len(cases)==10
            pauses.append(dict(block=n,**c,current_original_decoder_cases=cases,UI_body_explicit_unexecuted_boundary=True))
'''+anchor)
    anchor='    data=container.to_bytes()';assert anchor in text;text=text.replace(anchor,"    assert len(menus)==2 and len(pauses)==2\n"+anchor)
    anchor='        padded_tail_creates_no_extra_page_or_lost_boundary_glyph=True,';assert anchor in text
    text=text.replace(anchor,anchor+"\n        final_menu_cases=menus,all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound=True,final2000_pause_cases=pauses,both_original_pause_resume_words_and20_decoder_cases_bound=True,")
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8');pairs.append((old,new))
    for oldname,newname,swaps in [
        ('scripts/verify_lil_B111_B119_loader_v3241.py','scripts/verify_lil_B122_B127_loader_v3290.py',{'prepare_lil_B111_B119_research_v3240b':'prepare_lil_B122_B127_research_v3289b','lil_B111_B119_research_v3240b':'lil_B122_B127_research_v3289b','lil_B111_B119_loader_v3241':'lil_B122_B127_loader_v3290','nine_selected':'six_selected','B111-B119':'B122-B127'}),
        ('scripts/verify_lil_B111_B119_references_v3242.py','scripts/verify_lil_B122_B127_references_v3291.py',{'prepare_lil_B111_B119_research_v3240b':'prepare_lil_B122_B127_research_v3289b','lil_B111_B119_reference_census_v3242':'lil_B122_B127_reference_census_v3291','lil_B111_B119_loader_v3241':'lil_B122_B127_loader_v3290','nine_selected':'six_selected','range(111,120)':'range(122,128)','==305':'==312','all305_':'all312_','all327_other_SC2_blocks_preserved':'all330_other_SC2_blocks_preserved','native_commands_each=305':'native_commands_each=312','305-command/64-span nine-block':'312-command/64-span six-block','0x2200':'0x2100'})]:
        old,new,text=generate(oldname,newname,swaps);compile(text,str(new),'exec');new.write_text(text,encoding='utf-8');pairs.append((old,new))
    root.mkdir(parents=True);save(root/'source_bound_reference_successors.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],preserve_every_ROM_and_source_producer=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
