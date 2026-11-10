"""Atomic source-bound B206 compiler:24 progressive speeches,two typed choices,eight spans."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B206_layout_v3 as codec
from dk4tool.dialogue.lil_B206_profile_v1 import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B206_references_v6322b import FLAGS
PATH='/data/SC2.DK4'
CONFIG='translations/lil_B206_editorial_release_v1.json'

def load(path):return json.loads(Path(path).read_bytes())
def require(value,message):
    if not value:raise ValueError('Lil B206 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf.get('format')=='dk4-lil-B206-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source,arm,common=[image.read_file(p) for p in [PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']]
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'current runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    clean=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(clean)==conf['clean_SC2_sha256'],'clean script differs')
    doc,menu,mapping,seal=[load(conf[k]) for k in ['manuscript','choice_manuscript','reference_map','reference_approval']]
    require(conf['required_map_flags']==FLAGS and all(mapping.get(k) is True for k in FLAGS),'all approved map flags required')
    for batch,key in [(doc,'manuscript'),(menu,'choice_manuscript')]:
        require(batch['translation_policy']=='natural-dialogue-v2' and batch['target_locale']=='en-US' and not batch['formatting_review_pending'],'policy/format differs')
        validate_natural_dialogue_batch({**batch,'encoder':'dialogue-relocatable-v1'} if batch is menu else batch)
        require(all(all(r['review'].values()) for r in batch['records']),'all five gates required')
        require(batch['reference_map']==conf['reference_map'] and batch['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'map binding differs')
        require(seal['manuscripts'][conf[key]]==sha(Path(conf[key]).read_bytes()),'sealed manuscript differs')
    require(doc['encoder']=='dialogue-relocatable-v1' and menu['encoder']=='typed-menu-relocatable-v1','distinct speech/menu encoders required')
    require(doc['typed_choice_manuscript']==conf['choice_manuscript'] and doc['typed_choice_manuscript_sha256']==sha(Path(conf['choice_manuscript']).read_bytes()),'companion differs')
    require(seal['all28_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'] and seal['all_measured_timing_RNG_state_and_RGB_differences_preserved'] and seal['all207_names_alias_queue_and_full_editorial_goal_open'],'sealed review/scope required')
    require(mapping['format']=='dk4-lil-B206-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['preserve_record_parity'] and mapping['entry_point_offset']==8,'complete map required')
    require(mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'] and mapping['required_runtime_ARM9_sha256']==sha(arm),'map source/runtime differs')
    proofs={}
    keys=['native_font_proof','final_padding_proof','final_typed_menu_proof','relocated_control_proof','termination_decode_proof','loader_proof','source_census','representative_proof','actual_proof','native_approval','native_formatter_module','scoped_profile_module']
    for key in keys:
        require(doc[key+'_sha256']==sha(Path(doc[key]).read_bytes()),'proof hash differs:'+key)
        if Path(doc[key]).suffix=='.json':proofs[key]=load(doc[key])
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B206_layout_v3.py') and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B206_profile_v1.py'),'exact formatter/profile required')
    native,stored,typed,controls,ends,loader,census,view,actual,approval=[proofs[k] for k in keys if k not in ['native_formatter_module','scoped_profile_module']]
    require(len(native['cases'])==24 and native['covered_native_alignment_cases']==192 and native['current_original_macro_alignment_calls']==24 and native['exact_input_byte_identical_reused_native_alignment_cases']==168 and native['complete_progressive_planes']==24 and native['source_FE_planes']==0,'complete native consumers required')
    require(approval['all28_five_gates_approved'] and approval['source_and_formatter_negative_controls']==41 and len(approval['ten_individual_source_target_rowcount_reasons'])==10 and len(approval['five_reviewed_ordinary_boundaries'])==5,'individual formatter approvals required')
    require(len(stored['final_target_parity_cases'])==24 and stored['current_final_stored_macro_alignment_cases']==96 and stored['new_parity_macro_alignment_cases']==72 and stored['exact_byte_identical_reused_macro_alignment_cases']==24 and stored['all24_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored native proof required')
    require(typed['all2_stored_objects_four_refs_record_indices_and_counts_exact'] and len(typed['final_typed_menu_cases'])==2 and typed['fresh_count_calls']==4 and typed['fresh_label_pointer_calls']==8 and typed['reused_native_selection_cancel_cases']==12 and typed['reused_complete_current_reviewed_style_planes']==24,'both typed objects/four pointers required')
    require(len(controls['relocated_dispatch_cases'])==24 and len(controls['all8_source_current_target_nonchoice_leaves'])==8 and len(controls['picture_and_three_short47xx_pairs'])==4 and len(controls['fresh_current_three_A000_structural_cases'])==3 and len(controls['fresh_current_target10_complete_end_cases'])==10 and controls['all24_progressive_no_FE_or_macros_preserved'] and controls['picture138_descriptor_and_layout_exact'] and controls['original_names_Lil_Argot_Cristina_Erneco_and_Shady_Man_preserved'],'complete relocated controls/names required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',1518),('research',1576)] and ends['no_end_decode_zero_tail_dependency'],'guarded complete end required')
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and loader['B206_fits_original_0x2400_cache'] and loader['all_payload_cache_metadata_and_tail_guards_exact'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'] and census['only_original24070_interpreter_call_no_literal_alias'] and census['all335_other_SC2_blocks_preserved'],'whole loader/entry references required')
    require(not any(actual[k] for k in ['failures','paired_nontext_region_differences','command_result_differences','command_UI_word_differences','offline_only_display_IDs']),'actual findings unresolved')
    require((actual['actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_native_text_and_nameplate_holds'])==(24,55,217) and len(actual['actual_menu_cases'])==5 and sum(len(r['holds']) for r in actual['actual_menu_cases'])==13,'complete actual coverage required')
    require([len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[81,8,114],'measured differences must remain explicit')
    require(actual['all_command_paths_and_results_preserved'] and actual['source_and_English_all51_commands42_source_plus9_initializers_observed'] and actual['source_and_English_same_ARM9_COMMON_components_all_other_files_all335_other_blocks_and_input_schedules'] and actual['all_jobs_terminal_and_reaped'] and actual['no_capture_masking_pixel_edit_or_retiming'],'honest paired path scope required')
    require(view['actual_proof_sha256']==sha(Path(doc['actual_proof']).read_bytes()) and not view['visual_review_pending'] and view['no_open_translation_specific_display_menu_control_or_return_finding'] and view['broad_postscene_full_RAM_future_world_equivalence_unproven'] and view['original_source_asking9000_not_completed_debit_affordability_or_outer_event_proof'] and view['natural_event206_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed'],'viewed honest scope required')
    require(view['paired_command_timing_differences']==actual['command_timing_differences'] and view['within_scene_RNG_differences']==actual['command_RNG_differences'] and view['postscene_RGB_differences']==actual['later_whole_RGB_differences'],'measured differences binding differs')
    require(len(view['viewed_sheets'])==9 and len(view['viewed_acquisition_frames'])==2 and all(r['viewed'] and r['viewed_after_image_return'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in view['viewed_sheets']+view['viewed_acquisition_frames']),'viewed actual/transition sheets required')
    require(view['all207_name_role_alias_and_individual_Cristina_consumers_remain_open'] and doc['broader207_name_and_full_editorial_scope_remain_open'] and not any(p.get('full_goal_complete') for p in [doc,menu,mapping,seal,*proofs.values()]),'full editorial/name objective remains incomplete')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==24 and Counter(r['kind'] for r in rows)=={'progressive':24} and Counter(r['editorial_decision'] for r in rows)=={'revise':14,'retain-wording':10} and Counter(r['source_selector'] for r in rows)=={2:4,7:7,173:13},'exact speech identities/decisions required')
    require(ids==mapping['actual_sampled_display_IDs'] and set(ids)=={r['id'] for r in actual['actual_panels']} and mapping['offline_only_display_IDs']==[],'actual IDs differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==206,'one block required');spec=mapping['blocks'][0]
    old_blocks=list(IlnkContainer.parse(source).blocks);block=old_blocks[206];original=IlnkContainer.parse(clean).blocks[206]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'])==(1524,1522,1580,1580) and spec['external_references_complete'] and spec['entry_point_offset']==8,'logical/stored/reference bounds differ')
    fonts={r['id']:r for r in native['cases']};refs={r['id']:r for r in spec['text_records']};parities={r['id']:r for r in stored['final_target_parity_cases']};invariants={r['id']:r for r in approval['paragraph_invariants']}
    require(set(fonts)==set(refs)==set(parities)==set(invariants)==set(ids),'complete native/reference IDs required')
    patches=[];changes=[];ordinary=[];rowreasons={r['id']:r['reason'] for r in approval['ten_individual_source_target_rowcount_reasons']}
    for row in rows:
        ident=row['id'];case,ref=fonts[ident],refs[ident];at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['block']==row['source_reference']['block']==206 and row['file_path']==PATH and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0') and row['current_record_index']==row['record_index']==block[:at].count(b'\0'),'source/current identity differs:'+ident)
        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5 and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'reference bounds differ:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0 and row['current_text_hex']==old.hex(),'source/current bytes differ:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex() and row['source_selector']==old[0]==raw[0],'complete speaker preamble differs:'+ident)
        require(row['native_font_case']==case and row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked'],'individual native/actual scope differs:'+ident)
        require(all(case[k] for k in ['all_first_final_internal_glyphs_in_order_and_unique_cells','one_native_page_consumes_complete_target','all_visible_origins_zero_and_within_four_rows','complete_native_independent216x64_plane_equal']),'complete native bounds differ:'+ident)
        require(not re.findall(rb'FI|FA|FO',raw[1:]) and '{MACRO:' not in row['english'] and '{LB}' not in row['english'],'zero macros/authored breaks required:'+ident)
        profile=profile_for(arm,block,'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and sha(encoded.encoded)==invariants[ident]['encoded_sha256'],'compiled wording differs:'+ident)
        require(row.get('qa_waivers') in [None,['line-break-count']] and not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved wrapping QA:'+ident)
        require(qa.get('reviewed_ordinary_boundaries',[])==row.get('reviewed_ordinary_boundaries',[])==case.get('reviewed_ordinary_boundaries',[]),'source-bound ordinary boundary differs:'+ident)
        ordinary.extend(dict(id=ident,**b) for b in qa.get('reviewed_ordinary_boundaries',[]))
        if row.get('qa_waivers'):require(row.get('qa_waiver_reason')==rowreasons.get(ident),'individual rowcount reason differs:'+ident)
        paragraph=row['english'].split('}',1)[1];require((paragraph!=row['effective_predecessor_paragraph'])==(row['editorial_decision']=='revise'),'editorial decision differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row.get('fresh_retained_wording_justification'),'individual retention reason required')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(ref['old_offset']==at and ref['old_length']==len(old) and ref['target_hex']==value.hex() and ref['new_length']==len(value) and ref['parity_space_added']==pad,'stored parity/reference differs:'+ident)
        require(parities[ident]['stored_target_hex']==value.hex() and parities[ident]['complete_final_target_native_plane_equals_reviewed_plane'] and parities[ident]['tail_padding_consumed_without_blank_page_or_lost_glyph'],'complete final plane required:'+ident)
        patches.append(dict(start=at,end=at+len(old),value=value,old=old));changes.append(dict(id=ident,block=206,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(ordinary==approval['five_reviewed_ordinary_boundaries'],'all five exact ordinary boundary reasons required')
    labels=menu['records'];require(len(labels)==4 and [r['command_offset'] for r in labels]==[852,852,1020,1020] and [r['option_index'] for r in labels]==[0,1,0,1] and [r['english'] for r in labels]==['Got it','So?',"I'll take them!","That's expensive..."] and Counter(r['editorial_decision'] for r in labels)=={'retain-wording':2,'revise':2},'four ordered labels required')
    require(len(spec['choice_commands'])==2 and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'],'typed object scope differs')
    for choice,group in zip(spec['choice_commands'],[labels[:2],labels[2:]],strict=True):
        chunks=[];offsets=[];cursor=0
        for r in group:
            require(r['block']==206 and r['actual_label_visible'] and r['actual_choice_all_outcomes_observed'],'actual menu association differs')
            require((r['english']!=r['effective_predecessor_paragraph'])==(r['editorial_decision']=='revise'),'menu editorial decision differs')
            if r['editorial_decision']=='retain-wording':require(r.get('fresh_retained_wording_justification'),'menu retention reason required')
            offsets.append(cursor);chunk=r['english'].encode('ascii')+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
            for data,key in [(original,'source'),(block,'current')]:
                ref=r[key+'_reference'];require(data[ref['offset']:ref['offset']+ref['bytes']].hex()==r[key+'_hex'] and data[ref['offset']+ref['bytes']]==0,'choice source/current reference differs')
        value=b'\0\x21'+struct.pack('<2H',*offsets)+b''.join(chunks);at=choice['old_offset'];old=block[at:at+choice['old_length']]
        require(choice['new_length']==len(value) and choice['target_hex']==value.hex() and all(r['typed_target_object_hex']==value.hex() for r in group),'typed menu encoding differs')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.extend(dict(id=r['id'],block=206,kind=r['kind'],old_offset=r['current_reference']['offset'],new_offset=choice['label_references'][i]['new_offset'],old_bytes=r['current_reference']['bytes'],new_bytes=len(r['english'])) for i,r in enumerate(group))
    patches.sort(key=lambda p:p['start']);require(len(patches)==26 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'object overlap')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'reference inside replaced object')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    require(8+struct.unpack_from('<H',block,4)[0]==1522 and len(block)==1524 and block[1522:]==bytes(2),'source declared end/tail differs');pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:1522]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(1522)==1580,'target logical end differs')
    fixups=spec['relative_skip_fixups'];require([r['offset'] for r in fixups]==[878,882,1044,1048,1116,1356,1360,1514] and len(spec['target_native_skip_cases'])==40,'all eight relative sites required')
    for edge in fixups:
        start,target=mapped(edge['offset']),mapped(edge['matched_skip_target']);span=target-start-4
        require(0<=span<=65535 and span%2==0 and edge['new_offset']==start and edge['new_matched_skip_target']==target and edge['new_unmatched_next']==mapped(edge['unmatched_next_offset']) and edge['target_span']==span and struct.unpack_from('<H',block,edge['span_field_offset'])[0]==edge['source_span'] and edge['word']==struct.unpack_from('<H',logical,start)[0],'relative operand mapping differs')
        struct.pack_into('<H',logical,start+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)
    require(len(target)==1580 and sha(target)==spec['target_block_sha256'],'target block differs')
    commands=spec['mapped_native_commands'];require(len(commands)==42 and len(spec['command_map'])==42,'all commands required');boundaries={c['new_offset'] for c in commands}
    for c,cm in zip(commands,spec['command_map'],strict=True):
        a,b=c['old_offset'],c['new_offset'];w=c['word'];require(cm==dict(word=w,old_offset=a,new_offset=b,old_extent=c['old_native_extent'],new_extent=c['new_native_extent']),'independent command map differs')
        require(mapped(a)==b and w==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0] and mapped(a+c['old_native_extent'])-b==c['new_native_extent'] and c['target_0100_ancestors']==[mapped(x) for x in c['source_0100_ancestors']],'command boundary/ancestor differs')
        if w==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        elif w not in [0x2100,0x100,0x200,0x300,0x400]:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque command differs')
    require([(c['old_offset'],c['new_offset']) for c in commands if c['word']==0]==[(1518,1576)] and target[1576:1580]==bytes(4),'complete single end required')
    for edge in fixups:require(edge['new_matched_skip_target'] in boundaries and edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target']<1580,'branch destination bounds differ')
    for r in spec['text_records']:require(mapped(r['old_offset'])==r['new_offset'] and target[:r['new_offset']].count(b'\0')==r['new_record_index'],'target record identity differs')
    for choice in spec['choice_commands']:
        require(mapped(choice['old_offset'])==choice['new_offset'],'typed command mapping differs')
        for r in choice['label_references']:require(target[:r['new_offset']].count(b'\0')==r['new_record_index'],'typed label record identity differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,1514)
    for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)+bytes(2)==block,'inverse must restore every1524 predecessor byte')
    for panel in actual['actual_panels']:
        require(panel['id'] in fonts and panel['native_plane_sha256']==fonts[panel['id']]['whole_native_plane_sha256'] and panel['holds'] and panel['actual_complete_dialogue_and_nameplate_observed'],'individual observed panel differs')
        require(panel['prefix']==fonts[panel['id']]['source_selector'] and panel['name']=={2:'Lil Argot',7:'Cristina Erneco',173:'Shady Man'}[panel['prefix']],'source-bound actual speaker name differs')
        for h in panel['holds']:
            require(all(h[k] for k in ['all216x64_ink_gray_pixels_equal_complete_native_plane','complete_current_nameplate_glyphs_and_blank_guards_equal','both_versions_in_same_semantic_speech_at_this_frame','paired_upper_portrait_name_item_region_equal']) and sha(Path(h['capture']).read_bytes())==h['capture_sha256'] and sha(Path(h['source_capture']).read_bytes())==h['source_capture_sha256'],'complete source-paired actual hold required')
    expected=[('buy',852,0),('buy',1020,0),('high_price',852,0),('high_price',1020,1),('pitch_refusal',852,1)]
    require([(m['path'],m['source_command_offset'],m['observed_selected_option']) for m in actual['actual_menu_cases']]==expected,'actual branch/option associations differ')
    for m in actual['actual_menu_cases']:
        require(m['actual_choice_label_order_selection_and_VM_return_bound'] and m['interval']['native_result']==[2,m['observed_selected_option']] and m['holds'] and all(h['both_full_labels_and_actual_selected_background_equal'] and sha(Path(h['capture']).read_bytes())==h['capture_sha256'] for h in m['holds']),'actual two-option result/highlight differs')
    byversion={(v['path'],v['language']):v for v in actual['versions']}
    for path in ['buy','high_price','pitch_refusal']:
        jp,en=[byversion[path,c] for c in ['source','English']];shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
        require(shape(jp)==shape(en) and jp['input_schedule_sha256']==en['input_schedule_sha256'],'complete actual path/results/input differs')
    new_blocks=list(old_blocks);new_blocks[206]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[206],'whole archive differs')
    # All source,semantic,native,actual and inverse checks precede this sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=conf['manuscript'],choice_manuscript=conf['choice_manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=206,source_bytes=1524,source_logical_end=1522,target_bytes=1580,target_logical_end=1580,source_commands=42,relative_operands=8,inverse_restores_every_predecessor_byte=True)],
        all335_other_SC2_blocks_unchanged=True,all24_speeches_four_labels_two_menus8spans_native_controls_and_end_preserved=True,actual24_panels55observations217holds_five_menus13holds_and_three_paths=True,
        timing_RNG_state_later_RGB_differences_and_limited_gameplay_scope_preserved=True,all207_names_alias_queue_remains_open=True,native_code_name_data_fonts_graphics_unchanged=True,full_goal_complete=False)
