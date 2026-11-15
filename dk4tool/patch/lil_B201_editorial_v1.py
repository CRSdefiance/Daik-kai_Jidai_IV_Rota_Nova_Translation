"""Atomic, source-bound B201 whole-exchange and two-option release compiler."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B201_layout_v4 as codec
from dk4tool.dialogue.lil_B201_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
PATH='/data/SC2.DK4'
CONFIG='translations/lil_B201_editorial_release_v1.json'
FLAGS=['all44_commands24_preambles15_opaque_leaves_one2100_four_relative_sites_complete',
 'all1452_predecessor_bytes_inverse_target1222_logical1224_stored_two_tailzeros',
 'all24_actual_panels37_observations144_complete_native_holds_source_regions_equal',
 'both_actual_choice_indices_labels_and_visible_highlights_complete',
 'two_FI_three_null_FE_and_seven_prices_final100000_preserved',
 'measured54_timing30_RNG21_later_RGB_differences_preserved_no_world_equivalence',
 'Trader_contextual_retention_no_name_bytes_or_global_name_completion_credit',
 'representative_shared_rules_approved_natural_activation_earned_affordability_hardware_unclaimed']
def load(path):return json.loads(Path(path).read_bytes())
def require(value,message):
    if not value:raise ValueError('Lil B201 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf.get('format')=='dk4-lil-B201-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source,arm,common=[image.read_file(p) for p in [PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']]
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'current runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    clean=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(clean)==conf['clean_SC2_sha256'],'clean script differs')
    doc,menu,mapping,seal=[load(conf[k]) for k in ['manuscript','choice_manuscript','reference_map','reference_approval']]
    require(conf['required_map_flags']==FLAGS and all(mapping.get(k) is True for k in FLAGS),'complete approved map flags required')
    for batch in [doc,menu]:
        require(batch['translation_policy']=='natural-dialogue-v2' and batch['target_locale']=='en-US' and not batch['formatting_review_pending'],'policy/format differs')
        validate_natural_dialogue_batch({**batch,'encoder':'dialogue-relocatable-v1'} if batch is menu else batch)
        require(all(all(r['review'].values()) for r in batch['records']),'all five gates required')
        require(batch['reference_map']==conf['reference_map'] and batch['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'map binding differs')
        require(seal['manuscripts'][conf['manuscript' if batch is doc else 'choice_manuscript']]==sha(Path(conf['manuscript' if batch is doc else 'choice_manuscript']).read_bytes()),'sealed manuscript differs')
    require(doc['encoder']=='dialogue-relocatable-v1' and menu['encoder']=='typed-menu-relocatable-v1','distinct speech/menu encoders required')
    require(doc['typed_choice_manuscript']==conf['choice_manuscript'] and doc['typed_choice_manuscript_sha256']==sha(Path(conf['choice_manuscript']).read_bytes()),'companion differs')
    require(seal['all26_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'] and seal['all_measured_timing_RNG_state_and_RGB_differences_preserved'],'sealed review required')
    require(mapping['format']=='dk4-lil-B201-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['preserve_record_parity'] and mapping['entry_point_offset']==8,'complete map required')
    require(mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'] and mapping['required_runtime_ARM9_sha256']==sha(arm),'map source/runtime differs')
    proofs={}
    for key in ['native_font_proof','final_padding_proof','final_typed_menu_proof','relocated_control_proof','termination_decode_proof','representative_proof','actual_proof','native_approval','source_nameplate_consumer_proof','actor_terminology_reconciliation','actor_voice_contract','native_formatter_module','scoped_profile_module']:
        require(doc[key+'_sha256']==sha(Path(doc[key]).read_bytes()),'proof hash differs:'+key)
        if Path(doc[key]).suffix=='.json':proofs[key]=load(doc[key])
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B201_layout_v4.py') and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B201_profile.py'),'exact formatter/profile required')
    native,stored,controls,ends,view,actual,approval,names,terms,voices=[proofs[k] for k in ['native_font_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','representative_proof','actual_proof','native_approval','source_nameplate_consumer_proof','actor_terminology_reconciliation','actor_voice_contract']]
    require(len(native['cases'])==24 and native['current_original_macro_alignment_calls']==192 and native['complete_progressive_planes']==21 and native['complete_FE_logical_and_physical_planes']==3 and len(native['negative_controls'])==24 and all(c['rejected'] for c in native['negative_controls']),'complete native consumers required')
    require(approval['all26_five_gates_approved'] and len(approval['formatter_negatives'])==28 and len(approval['thirteen_individual_rowcount_reasons'])==13,'formatter and individual rowcount approvals required')
    require(len(stored['final_target_parity_cases'])==24 and stored['current_final_stored_macro_alignment_cases']==96 and stored['new_parity_macro_alignment_cases']==52 and stored['exact_byte_identical_reused_macro_alignment_cases']==44 and stored['all24_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored native proof required')
    require(len(controls['relocated_dispatch_cases'])==24 and len(controls['all15_source_current_target_control_leaves'])==15 and len(controls['picture_and_short47xx_pairs'])==3 and controls['all21_progressive_three_null_actor_FE_and_two_FI_preserved'],'complete relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',1448),('research',1218)],'guarded complete end required')
    expected_names={'2':'Lil Argot','19':'Carlo Sinat','105':'Trader'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected_names,'current speaker labels differ')
    require(terms['source_FI_FA_FO_counts']=={'FI':2,'FA':0,'FO':0} and terms['source_native_payment_saturates_at_zero_not_affordability_or_outer_eligibility_proof'] and terms['spoken_item_stays_unnamed_no_new_item_title_widget_or_full_effect_fidelity_credit'],'source context scope differs')
    require(voices['all207_names_and_eight_voice_classes_freshly_executed_on_current_snapshot'] and doc['existing_Trader_label_contextual_retention_recorded_no_name_bytes_or_global_name_credit'],'source voices/name scope required')
    require(not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences'] and not actual['offline_only_display_IDs'],'actual display/control findings unresolved')
    require(actual['actual_unique_speech_panels']==24 and actual['actual_English_speech_observations']==37 and actual['complete_native_holds']==144 and len(actual['actual_menu_cases'])==2,'complete actual coverage required')
    require([len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[54,30,21],'measured differences must remain explicit')
    require(view['actual_proof_sha256']==sha(Path(doc['actual_proof']).read_bytes()) and not view['visual_review_pending'] and view['no_open_translation_specific_display_menu_control_or_return_finding'] and view['broad_postscene_full_RAM_future_world_equivalence_unproven'],'viewed honest scope required')
    require(view['paired_command_timing_differences']==actual['command_timing_differences'] and view['within_scene_RNG_differences']==actual['command_RNG_differences'] and view['postscene_RGB_differences']==actual['later_whole_RGB_differences'],'measured differences binding differs')
    require(len(view['viewed_sheets'])==6 and all(r['viewed'] and r['viewed_after_image_return'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in view['viewed_sheets']),'viewed actual/transition sheets required')
    require(not any(p.get('full_goal_complete') for p in [doc,menu,mapping,seal,*proofs.values()]),'full editorial objective remains incomplete')
    rows=doc['records'];ids=[r['id'] for r in rows];require(len(rows)==len(set(ids))==24 and Counter(r['kind'] for r in rows)=={'progressive':21,'system-FE':3} and Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':12},'exact speech decisions required')
    require(ids==mapping['actual_sampled_display_IDs']==[r['id'] for r in actual['actual_panels']] and mapping['offline_only_display_IDs']==[],'actual IDs differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==201,'one block required');spec=mapping['blocks'][0]
    old_blocks=list(IlnkContainer.parse(source).blocks);block=old_blocks[201];original=IlnkContainer.parse(clean).blocks[201]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'])==(1452,1452,1224,1222),'logical/stored bounds differ')
    fonts={r['id']:r for r in native['cases']};refs={r['id']:r for r in spec['text_records']};require(set(fonts)==set(refs)==set(ids),'complete native/reference IDs required')
    patches=[];changes=[];macros=Counter()
    for row in rows:
        ident=row['id'];case,ref=fonts[ident],refs[ident];fe=row['kind']=='system-FE';at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['block']==row['source_reference']['block']==201 and row['file_path']==PATH and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0') and row['current_record_index']==row['record_index']==block[:at].count(b'\0'),'source/current identity differs:'+ident)
        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5 and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'reference bounds differ:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0 and row['current_text_hex']==old.hex(),'source/current bytes differ:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex() and row['source_selector']==old[0]==raw[0],'complete speaker preamble differs:'+ident)
        require(row['native_font_case']==case and row['actual_B22_display_fixture_observed'] and not row['current_native_UI_body_explicit_unexecuted_boundary'] and not row['offline_only_native_display_checked'],'individual native/actual scope differs:'+ident)
        require(case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['one_native_page_consumes_complete_target'] and case['all_visible_origins_zero_and_within_four_rows'],'complete native bounds differ:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])];require(sm==tm,'source macro order differs:'+ident);macros.update(sm)
        profile=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled wording differs:'+ident)
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(row.get('qa_waivers') in [None,['line-break-count']] and not row.get('reviewed_ordinary_boundaries') and not qa.get('reviewed_ordinary_boundaries'),'unapproved safety waiver:'+ident)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved wrapping QA:'+ident)
        paragraph=row['english'].split('}',1)[1]
        for macro in ['FI','FA','FO']:paragraph=paragraph.replace('{MACRO:'+macro+'}',macro)
        require((paragraph!=row['effective_predecessor_paragraph'])==(row['editorial_decision']=='revise'),'editorial decision differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row.get('fresh_retained_wording_justification'),'individual retention reason required')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(ref['old_offset']==at and ref['old_length']==len(old) and ref['target_hex']==value.hex() and ref['new_length']==len(value) and ref['parity_space_added']==pad,'stored parity/reference differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),value=value,old=old));changes.append(dict(id=ident,block=201,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(macros=={b'FI':2},'exact two FI required')
    labels=menu['records'];require(len(labels)==2 and [r['option_index'] for r in labels]==[0,1] and [r['english'] for r in labels]==['Buy','Pass'] and all(r['editorial_decision']=='retain-wording' and r.get('fresh_retained_wording_justification') for r in labels),'two retained ordered labels required')
    require(len(spec['choice_commands'])==1 and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'],'typed object scope differs')
    choice=spec['choice_commands'][0];chunks=[];offsets=[];cursor=0
    for r in labels:
        require(r['command_offset']==880 and r['block']==201 and r['actual_label_visible'] and r['actual_choice_all_outcomes_observed'],'actual menu association differs')
        offsets.append(cursor);chunk=r['english'].encode('ascii')+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
        for data,key in [(original,'source'),(block,'current')]:
            ref=r[key+'_reference'];require(data[ref['offset']:ref['offset']+ref['bytes']].hex()==r[key+'_hex'],'choice source/current reference differs')
    value=b'\0\x21'+struct.pack('<2H',*offsets)+b''.join(chunks);old=block[880:902]
    require(len(value)==16 and choice['old_offset']==880 and choice['old_length']==22 and choice['new_length']==16 and choice['target_hex']==value.hex() and all(r['typed_target_object_hex']==value.hex() for r in labels),'typed menu encoding differs')
    patches.append(dict(start=880,end=902,value=value,old=old));changes.extend(dict(id=r['id'],block=201,kind=r['kind'],old_offset=r['current_reference']['offset'],new_offset=choice['label_references'][i]['new_offset'],old_bytes=r['current_reference']['bytes'],new_bytes=len(r['english'])) for i,r in enumerate(labels))
    patches.sort(key=lambda p:p['start']);require(len(patches)==25 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'object overlap')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'reference inside replaced object')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    require(8+struct.unpack_from('<H',block,4)[0]==len(block)==1452,'source declared end differs');pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(1452)==1222,'target logical end differs')
    fixups=spec['relative_skip_fixups'];require([r['offset'] for r in fixups]==[902,906,1172,1444] and len(spec['target_native_skip_cases'])==20,'all four relative sites required')
    for edge in fixups:
        start,target=mapped(edge['offset']),mapped(edge['matched_skip_target']);span=target-start-4
        require(0<=span<=65535 and span%2==0 and edge['new_offset']==start and edge['new_matched_skip_target']==target and edge['target_span']==span and struct.unpack_from('<H',block,edge['span_field_offset'])[0]==edge['source_span'] and edge['word']==struct.unpack_from('<H',logical,start)[0],'relative operand mapping differs')
        struct.pack_into('<H',logical,start+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(2)
    require(len(target)==1224 and sha(target)==spec['target_block_sha256'],'target block differs')
    commands=spec['mapped_native_commands'];require(len(commands)==44 and len(spec['command_map'])==44,'all commands required')
    boundaries={c['new_offset'] for c in commands}
    for c,cm in zip(commands,spec['command_map'],strict=True):
        a,b=c['old_offset'],c['new_offset'];w=c['word'];require(cm==dict(word=w,old_offset=a,new_offset=b,old_extent=c['old_native_extent'],new_extent=c['new_native_extent']),'independent command map differs')
        require(mapped(a)==b and w==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0] and mapped(a+c['old_native_extent'])-b==c['new_native_extent'] and c['target_0100_ancestors']==[mapped(x) for x in c['source_0100_ancestors']],'command boundary/ancestor differs')
        if w==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        elif w not in [0x2100,0x100,0x200,0x300,0x400]:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque command differs')
    require([(c['old_offset'],c['new_offset']) for c in commands if c['word']==0]==[(1448,1218)] and target[1218:1222]==bytes(4),'complete single end required')
    for edge in fixups:require(edge['new_matched_skip_target'] in boundaries and edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target']<1222,'branch destination bounds differ')
    for r in spec['text_records']:require(mapped(r['old_offset'])==r['new_offset'] and target[:r['new_offset']].count(b'\0')==r['new_record_index'],'target record identity differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,1444)
    for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block,'inverse must restore every1452 predecessor byte')
    for panel in actual['all_actual_speech_observations']:
        require(panel['id'] in fonts and panel['native_plane_sha256']==fonts[panel['id']]['whole_native_plane_sha256'] and panel['holds'],'individual native observed panel differs')
        for h in panel['holds']:require(h['complete_ink_gray_masks_equal_native_plane'] and h['shared_source_speech_hold'] and all(h['paired_region_equality'].values()) and sha(Path(h['capture']).read_bytes())==h['capture_sha256'] and sha(Path(h['clean_capture']).read_bytes())==h['clean_capture_sha256'],'complete source-paired actual hold required')
    for i,m in enumerate(actual['actual_menu_cases']):require(m['source_menu_offset']==880 and m['native_result_words']==[2,i] and any(h['selected_highlight_matches_return_when_visible'] for h in m['holds']) and all(h['complete_both_native_label_masks_equal'] for h in m['holds']),'actual two-option result/highlight differs')
    byversion={(v['path'],v['case']):v for v in actual['versions']}
    for path in ['buy','decline']:
        jp,en=[byversion[path,c] for c in ['clean_Japanese','reviewed_English']];shape=lambda v:[(r.get('original_source_offset'),r['word'],r['result_words']) for r in v['selected_B22_command_pairs']]
        require(shape(jp)==shape(en) and jp['input_schedule_sha256']==en['input_schedule_sha256'],'complete actual path/results/input differs')
    new_blocks=list(old_blocks);new_blocks[201]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[201],'whole archive differs')
    # All validation and inverse reconstruction precede this sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=conf['manuscript'],choice_manuscript=conf['choice_manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=201,source_bytes=1452,target_bytes=1224,target_logical_end=1222,source_commands=44,relative_operands=4,inverse_restores_every_predecessor_byte=True)],
        all335_other_SC2_blocks_unchanged=True,all24_speeches_two_labels_three_FE_two_FI_native_controls_and_end_preserved=True,actual24_panels37_observations144_complete_holds_both_options=True,
        timing_RNG_state_later_RGB_differences_and_limited_gameplay_scope_preserved=True,native_code_name_data_fonts_graphics_unchanged=True,full_goal_complete=False)
