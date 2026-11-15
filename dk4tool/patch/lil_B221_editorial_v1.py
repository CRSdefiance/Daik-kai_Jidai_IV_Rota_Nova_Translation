"""Atomically reconstruct the sealed B221 exchange, one menu and all four relative operands."""
import json,struct
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B221_profile_v1 import contract,profile_for
from dk4tool.dialogue import lil_B221_layout_v1 as codec
from dk4tool.dialogue.lil_B221_choices_v1 import compile_choices
from scripts.seal_lil_B221_references_v7007 import FLAGS

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B221_editorial_release_v1.json'

def load(path):return json.loads(Path(path).read_bytes())

def require(value,label):
    if not value:raise ValueError('B221 editorial contract: '+label)

def apply_release(image,baseline,config=CONFIG):
    conf=load(config)
    require(conf['format']=='dk4-lil-B221-editorial-release-v1','config format')
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['source_files'],'complete cumulative source files')
    require({p:sha(v) for p,v in image.iter_components()}==conf['source_components'],'complete cumulative source components')
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin')
    require(sha(source)==conf['source_SC2_sha256'] and sha(arm)==conf['required_runtime_arm9_sha256'],'exact archive/runtime')
    require(sha(image.read_file('/COMMON/MESFILE.DK4'))==conf['required_runtime_common_sha256'],'exact COMMON')
    require(sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'canonical baseline')
    clean=Path(conf['clean_ROM']);require(sha(clean.read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    japanese=NdsImage.open(clean).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean archive')
    doc,menu,mapping,seal=[load(conf[k]) for k in ['manuscript','choice_manuscript','reference_map','reference_approval']]
    for value,encoder in [(doc,'dialogue-relocatable-v1'),(menu,'typed-menu-relocatable-v1')]:
        require(value['translation_policy']=='natural-dialogue-v2' and value['target_locale']=='en-US' and value['encoder']==encoder and not value['formatting_review_pending'],'v2 reviewed manuscript')
    require(seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['choice_manuscript_sha256']==sha(Path(conf['choice_manuscript']).read_bytes()),'sealed manuscripts')
    require(seal['reference_map_sha256']==doc['reference_map_sha256']==menu['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and seal['all16_five_gates_and_exact_references_approved'],'approval seal')
    require(conf['required_map_flags']==FLAGS and all(mapping.get(k) is True for k in FLAGS),'complete map flags')
    require(mapping['format']=='dk4-lil-B221-source-relocation-map-v1' and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'] and mapping['required_runtime_ARM9_sha256']==sha(arm),'exact map/runtime')
    for value,key in [(doc,'manuscript_sha256'),(menu,'choice_manuscript_sha256')]:
        approved=load(value['native_approved_manuscript'])
        require(sha(Path(value['native_approved_manuscript']).read_bytes())==value['native_approved_manuscript_sha256']==mapping[key] and approved['records']==value['records'],'individually approved records')
    rows=doc['records'];choice_rows=menu['records'];ids={r['id'] for r in rows};choice_ids={r['id'] for r in choice_rows}
    require(len(rows)==len(ids)==14 and len(choice_rows)==len(choice_ids)==2 and not ids&choice_ids,'sixteen distinct objects')
    require(Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':6} and Counter(r['source_selector'] for r in rows)=={2:4,17:4,85:6},'decisions/actors')
    require(all(r['block']==221 and r['file_path']==PATH and r['kind']=='progressive' and all(r['review'].values()) and r['full_exchange_read_aloud_review'] and (r['editorial_decision']!='retain-wording' or r['retention_reason']) for r in rows),'individual speech gates')
    require(all(all(r['review'].values()) and r['editorial_decision']=='retain-wording' and r['fresh_retained_wording_justification'] for r in choice_rows),'individual choice gates')
    require(len(mapping['blocks'])==1,'one block');spec=mapping['blocks'][0]
    require((spec['block'],spec['source_bytes'],spec['source_logical_end'],spec['source_tail_bytes'],spec['target_bytes'],spec['target_logical_end'],spec['target_tail_bytes'])==(221,1208,1208,0,1224,1224,0),'exact extents')
    require(len(spec['choice_commands'])==1 and not spec['actor_style_commands'] and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20 and not spec['original_C200_map'],'source typed/relative scope')
    blocks=list(IlnkContainer.parse(source).blocks);block=blocks[221];original=IlnkContainer.parse(japanese).blocks[221]
    require(len(blocks)==336 and sha(block)==spec['source_block_sha256'] and sha(original)==spec['clean_block_sha256'],'exact source blocks')
    require(len(block)==1208 and block[:4]==b'CS\0\1' and 8+struct.unpack_from('<H',block,4)[0]==1208 and block[1204:]==bytes(4),'source header/full end/no tail')
    packet=load(doc['source_context']);source_rows={r['id']:r for r in packet['records']};source_choices={r['id']:r for r in packet['typed_choice_records']}
    frozen=contract();bindings=frozen['record_bindings'];refs={r['id']:r for r in spec['text_records']};allrefs={r['id']:r for r in spec['all_object_references']}
    fonts={r['id']:r for r in load(doc['native_font_proof'])['records']};stores={r['id']:r for r in load(doc['native_stored_proof'])['records']}
    controls=load(doc['relocated_control_proof']);dispatch={r['id']:r for r in controls['dispatch_cases']};actual=load(doc['actual_English_proof'])
    panels={}
    for version in actual['versions']:
        require(version['normal_terminal_result']==[0,version['selected_original_option']] and version['exit_frame']==6693 and version['normal_port_sample_frame']==6790,'actual normal result/value')
        require(version['actual_menu']['interval']['native_result']==[2,version['selected_original_option']] and version['actual_menu']['holds'],'actual choice')
        for panel in version['actual_panels']:panels.setdefault(panel['id'],[]).append(panel)
    require(set(source_rows)==set(bindings)==set(refs)==set(fonts)==set(stores)==set(dispatch)==set(panels)==ids,'all speech proof sets')
    require(set(source_choices)==set(frozen['choice_bindings'])==choice_ids and set(allrefs)==ids|choice_ids,'all choice proof sets')
    require(controls['target_block_sha256']==spec['target_block_sha256'] and len(controls['normal_terminal_seed_cases'])==25 and controls['normal_state0_retains_existing_value_word_in_all25_cases'],'normal residual ends')
    require(controls['source_A000']['source_command_hex']=='00a0ffff47000110' and controls['relocated_A000']['error'] is None,'exact A000 structural scope')
    require(not actual['failures'] and actual['actual_unique_speeches']==14 and actual['actual_complete_native_page_observations']==30 and actual['actual_complete_body_holds']==actual['actual_complete_name_holds']==118 and actual['all30_stored_commands_executed_in_union'] and actual['all_jobs_terminal_and_reaped'],'complete actual source/English scope')
    require(not load(doc['actual_English_view'])['visual_review_pending'],'visual review')
    naming=load(doc['speaker_name_review']);names={r['actor_ID']:r for r in naming['records']}
    require(set(names)=={2,17,85} and all(all(names[i]['review'].values()) for i in [2,17]),'personal name retentions')
    require(names[85]['review']['naturalness'] is False and names[85]['technical_preservation_not_natural_label_or_target_Shopkeeper_approval'] and naming['actor85_wider_ten_role_Shopkeeper_layer_still_pending'] and naming['full_catalogue_UI_unvisited'],'separate wider role localization remains open')
    later=load(doc['later_scope_proof'])
    require(later['actual_proof_sha256']==sha(Path(doc['actual_English_proof']).read_bytes()) and later['all_measured_differences_retained_for_later_older_record_technical_reaudit'] and later['no_full_RAM_every_frame_future_sequence_broad_simulation_or_complete_causal_claim'],'later measurement limits')
    require(all(not r['command_result_differences'] and not r['command_UI_word_differences'] for r in later['measurements']),'all measured results/UI preserved')
    patches=[];changes=[];pads=0
    for row in rows:
        ident=row['id'];ref=refs[ident];binding=bindings[ident];oldrow=source_rows[ident]
        raw=bytes.fromhex(row['source_hex']);old=bytes.fromhex(row['current_hex']);at=row['current_reference']['offset'];cleanat=row['source_reference']['offset']
        require(ref==allrefs[ident] and row['source_reference']==oldrow['source_reference']==ref['source_reference'] and row['current_reference']==oldrow['current_reference']==ref['current_reference'],'exact references:'+ident)
        require(row['source_hex']==oldrow['source_hex'] and row['current_hex']==oldrow['current_hex'] and original[cleanat:cleanat+len(raw)+1]==raw+b'\0' and block[at:at+len(old)+1]==old+b'\0' and block[:at].count(b'\0')==row['current_record_index'],'literal records:'+ident)
        require(raw[0]==old[0]==row['source_selector']==binding['source_selector']==ref['source_selector'] and row['source_voice_class']==ref['source_voice_class']=={2:3,17:4,85:0}[raw[0]],'original selector/voice:'+ident)
        require(block[at-5:at+1].hex()==row['source_complete_preamble_hex']==ref['source_preamble_hex'],'complete preamble:'+ident)
        profile=profile_for(arm,block,ident);encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==ref['compiled_hex']==fonts[ident]['compiled_hex'] and qa==row['base_QA_report'],'compiled text/QA:'+ident)
        require(row['qa_waivers']==[] and row['qa_waiver_reason'] is None and row['informational_row_count_reason']==binding['row_count_reason'] and row['reviewed_ordinary_boundaries']==binding['ordinary_wrap_reasons'] and row['reviewed_native_page_boundary']==binding['page_boundary_reason'],'individual row/wrap/page reasons:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        pads+=pad
        require(value.hex()==ref['target_hex']==stores[ident]['final_target_hex']==dispatch[ident]['target_hex'] and ref['parity_space_added']==pad and stores[ident]['all_words_glyphs_native_page_count_and_guards_preserved'],'final stored bytes:'+ident)
        require(all(raw[1:].count(k)==value[1:].count(k)==0 for k in [b'FI',b'FA',b'FO']),'no substitutions:'+ident)
        require(len(stores[ident]['native_pipeline']['cases'])==4 and all(r['output_hex']==value[1:].hex() for r in stores[ident]['native_pipeline']['cases']),'final native processor:'+ident)
        expected_pages=2 if ident in frozen['scoped_two_page_record_IDs'] else 1
        require(len(fonts[ident]['pages'])==len(stores[ident]['complete_pages']['pages'])==row['native_page_count']==expected_pages and row['native_profile_maximum_total_rows']==(8 if expected_pages==2 else 4) and row['original_physical_native_rows_per_page']==4,'original physical pages:'+ident)
        for first,second in zip(fonts[ident]['pages'],stores[ident]['complete_pages']['pages'],strict=True):
            require(Path(first['native_plane']).read_bytes()==Path(second['native_plane']).read_bytes() and sha(Path(second['native_plane']).read_bytes())==first['native_plane_sha256']==second['native_plane_sha256'],'complete native ink:'+ident)
        observed=panels[ident]
        require(row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay'] and all(p['native_pages']==expected_pages and all(p['actual_complete_page_holds']) and not p['partial_or_transition_holds'] for p in observed),'complete actual pages:'+ident)
        require(sum(len(h) for p in observed for h in p['actual_complete_page_holds'])==row['actual_complete_body_holds'] and sum(len(p['complete_name_holds']) for p in observed)==row['actual_complete_name_holds'],'actual counts:'+ident)
        for panel in observed:
            require(len(panel['ordinary_page_transitions'])==expected_pages-1,'ordinary page progression:'+ident)
            for holds in panel['actual_complete_page_holds']:
                for hold in holds:require(hold['complete_native_black_gray_all_glyphs_equal'] and sha(Path(hold['capture']).read_bytes())==hold['sha256'],'actual body:'+ident)
            for hold in panel['complete_name_holds']:require(hold['complete_name_and_blank_guards_equal'] and sha(Path(hold['capture']).read_bytes())==hold['sha256'],'actual header:'+ident)
        patches.append(dict(start=at,end=at+len(old),old=old,value=value))
        changes.append(dict(id=ident,kind='progressive',block=221,old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(pads==5,'five zero-ink parity tails')
    typed=compile_choices(choice_rows);choice=spec['choice_commands'][0]
    require(choice['old_offset']==150 and choice['old_length']==28 and choice['new_offset']==126 and choice['new_length']==14 and choice['target_hex']==typed.hex() and choice['labels']==['Yes','No'] and choice['record_IDs']==[r['id'] for r in choice_rows],'exact complete menu')
    old_choice=block[150:178];require(old_choice.hex()==next(r['whole_command_hex'] for r in packet['blocks'][0]['all_current_native_commands'] if r['word']==0x2100),'old complete menu')
    for row,ref in zip(choice_rows,choice['label_references'],strict=True):
        oldrow=source_choices[row['id']]
        require(row['source_hex']==oldrow['source_hex'] and row['current_hex']==oldrow['current_hex'] and row['source_reference']==oldrow['source_reference']==ref['source_reference'] and row['current_reference']==oldrow['current_reference']==ref['current_reference'] and ref==allrefs[row['id']],'choice references:'+row['id'])
        require(ref['option_index']==row['option_index'] and ref['target_hex']==row['english'].encode('ascii').hex(),'choice index/text')
        changes.append(dict(id=row['id'],kind='typed-choice-label',block=221,old_offset=ref['old_offset'],new_offset=ref['new_offset'],old_bytes=ref['old_length'],new_bytes=ref['new_length']))
    patches.append(dict(start=150,end=178,old=old_choice,value=typed));patches.sort(key=lambda p:p['start'])
    require(len(patches)==15 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'disjoint complete objects')
    def mapped(at):
        delta=0
        for patch in patches:
            if at<patch['start']:break
            require(not patch['start']<at<patch['end'],'unmapped interior reference')
            if at==patch['start']:return at+delta
            delta+=len(patch['value'])-len(patch['old'])
        return at+delta
    parts=[];last=0
    for patch in patches:parts.extend([block[last:patch['start']],patch['value']]);last=patch['end']
    parts.append(block[last:1208]);logical=bytearray(b''.join(parts));require(len(logical)==mapped(1208)==1224,'target logical extent')
    edges=spec['relative_skip_fixups'];source_edges=load('work/analysis/lil_B221_branches_v6970/original_relative_skip_operand_proof.json')['operands_requiring_adjustment_when_resizing']
    require([e['offset'] for e in edges]==[178,182,256,360],'four source relative sites')
    for edge,old in zip(edges,source_edges,strict=True):
        require(all(edge[k]==v for k,v in old.items()),'original relative semantics')
        start=mapped(edge['offset']);dest=mapped(edge['matched_skip_target']);span=dest-start-4
        require(edge['new_offset']==start and edge['new_unmatched_next']==start+4 and edge['new_matched_skip_target']==dest and edge['source_span']==struct.unpack_from('<H',block,edge['span_field_offset'])[0] and edge['target_span']==span and 0<=span<=0xFFFF and span%2==0,'relative relocation')
        struct.pack_into('<H',logical,start+2,span)
    struct.pack_into('<H',logical,4,1216);target=bytes(logical)
    require(sha(target)==spec['target_block_sha256'],'complete target block')
    require(len(spec['command_map'])==21,'twenty-one mapped commands')
    for old,cm in zip(packet['blocks'][0]['all_current_native_commands'],spec['command_map'],strict=True):
        first,second=old['offset'],cm['new_offset']
        require(first==cm['old_offset'] and mapped(first)==second and old['native_extent']==cm['old_extent'] and mapped(first+cm['old_extent'])==second+cm['new_extent'] and struct.unpack_from('<H',target,second)[0]==cm['word']==old['word'],'complete command map')
        require(cm['source_0100_ancestors']==old['ancestor_0100_offsets'] and cm['target_0100_ancestors']==[mapped(a) for a in old['ancestor_0100_offsets']],'nested branch ancestors')
        if old['word']==0x4000:require(block[first:first+6]==target[second:second+6],'speaker/layout preamble')
        elif old['word'] not in [0x100,0x200,0x300,0x2100]:require(bytes.fromhex(old['whole_command_hex'])==target[second:second+cm['new_extent']],'opaque command/full end')
    require(spec['original_A000_map']==[dict(source_offset=1196,target_offset=1212,extent=8,source_hex='00a0ffff47000110')] and target[1212:1220].hex()=='00a0ffff47000110','A000 operands')
    require(spec['complete_end_map']==[dict(source_offset=1204,target_offset=1220,extent=4,source_hex='00000000',source_four_zero_bytes_exact=True)] and target[1220:]==bytes(4),'complete normal end retaining existing result word')
    for ref in spec['text_records']:
        require(mapped(ref['old_offset'])==ref['new_offset'] and target[ref['new_offset']:ref['new_offset']+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:ref['new_offset']].count(b'\0')==ref['new_record_index'],'final complete speech reference')
    for ref in choice['label_references']:
        at=126+6+struct.unpack_from('<H',target,128+ref['option_index']*2)[0]
        require(at==ref['new_offset'] and target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:at].count(b'\0')==ref['new_record_index'],'final complete choice reference')
    inverse=bytearray(target);struct.pack_into('<H',inverse,4,1200)
    for edge in edges:struct.pack_into('<H',inverse,edge['new_offset']+2,edge['source_span'])
    for patch in reversed(patches):at=mapped(patch['start']);inverse[at:at+len(patch['value'])]=patch['old']
    require(bytes(inverse)==block,'complete1208-byte inverse')
    newblocks=list(blocks);newblocks[221]=target;result=IlnkContainer(newblocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'] and result==NdsImage.open(conf['reference_ROM']).read_file(PATH),'approved whole target archive')
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],choice_manuscript=conf['choice_manuscript'],reference_map=conf['reference_map'],
        source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),changed_records=changes,
        blocks=[dict(block=221,source_bytes=1208,target_bytes=1224,source_logical_end=1208,target_logical_end=1224,source_commands=21,relative_operands=4,typed_menus=1,inverse_restores_every_original_stored_byte=True)],
        all335_other_SC2_blocks_unchanged=True,all16_speech_choice_objects_and16_native_pages_actual_complete=True,
        actual_complete_body_holds=118,actual_complete_name_holds=118,
        original_A000_four_relatives_menu_and_normal_end_value_words0_1_preserved=True,
        personal_names_retained_shared_Shopkeeper_layer_still_open=True,
        all_measured_source_English_scope_and_later_limits_preserved=True,full_goal_complete=False)
