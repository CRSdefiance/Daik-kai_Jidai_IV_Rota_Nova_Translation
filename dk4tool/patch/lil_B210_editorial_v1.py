"""Atomic ten-record B210 reconstruction; every guard precedes the sole SC2 write."""
import json,struct
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.lil_B210_profile_v1 import profile_for,contract
from dk4tool.dialogue import lil_B210_layout_v1 as codec
from dk4tool.patch.grand_race_menu_release import sha
from scripts.seal_lil_B210_references_v6530 import FLAGS
PATH='/data/SC2.DK4'
CONFIG='translations/lil_B210_editorial_release_v1.json'
def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Lil B210 '+message)
def exact(data,fields,label):
    for k,v in fields.items():require(data.get(k)==v,label+':'+k)

def observations(doc,mapping,conf):
    keys=['native_font_proof','native_stored_proof','relocated_control_proof','actual_English_proof','actual_English_view','native_approval','native_name_source_proof','native_policy_validation']
    p={k:load(doc[k]) for k in keys};f,s,c,a,v,n,names,q=p.values()
    exact(f,dict(complete_native_pages=10,logical_compiled_input_alignment_cases=80,all10_objects_one_original_four_row_native_page=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,each216x64_plane_exact_independent_current_font_and_all_canaries=True,only_original_static_selectors2_17_no_D0_role=True),'native glyphs')
    exact(s,dict(final_stored_alignment_cases=40,fresh_alignment_cases=16,exact_reused_alignment_cases=24,fresh_parity_tail_records=4,complete_pages=10,all_final_stored_targets_equal_reviewed_complete_native_ink=True,no_extra_blank_page_or_lost_leading_trailing_internal_glyph=True),'stored glyphs')
    exact(q,dict(positive_count=10,negative_count=52,all_rejections_before_ROM_or_archive_mutation=True,no_unwaived_warning_or_error=True),'policy')
    require(len(q['negative_cases'])==52 and all(r['rejected'] for r in q['negative_cases']) and len(q['row_count_reasons'])==5,'52 negatives/five row reasons')
    exact(n,dict(all10_five_gates_approved=True,native_pages=10,original_viewport=[216,64],native_rows_per_page=4,logical_compiled_alignments=80,stored_alignments=40,name_literal_alignments=32,layout_negative_controls=52,actual_objects=10,actual_native_pages=10,complete_body_name_holds=39,offline_only_objects=0,all6timing4RNG_three_durations116later_RGB_and_final_state_limits_retained=True),'individual approval')
    require(n['manuscript_sha256']==doc['native_approved_manuscript_sha256']==sha(Path(doc['native_approved_manuscript']).read_bytes()),'native approved predecessor')
    exact(c,dict(original_A000_source_offset=674,original_A000_target_offset=642,original_A000_hex='00a0ffff24000110',source688_logical686_tail2_target656_logical654_tail2_end650_bound=True,no_FE_typed_role_predicate_relative_or_choice_consumer_inherited=True,opaque_A000_effect_body_bridged_not_full_quest_stat_item_or_eligibility_claim=True),'controls')
    require(len(c['relocated_dispatch_cases'])==10 and len(c['target_five_complete_end_cases'])==5,'ten target dispatches/five ends')
    exact(a,dict(actual_unique_objects=10,actual_complete_native_pages=10,complete_native_body_holds=39,complete_native_name_holds=39,all21_stored_commands_observed=True,source_exit_frame=5254,English_exit_frame=5256,normal_English_port_sample_frame=5350,final_PRNG_seeds=[1345055542,3753373325],five_native_component_equality=dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True),whole_actor_and_captain_equal=False,final_PRNG_equal=False,source_and_English_runs_terminal_reaped=True,natural_event210_original_location_earned_progress_full_effects_routes_and_hardware_unclaimed=True),'actual scope')
    for key,count in [('actual_panels',10),('offline_only_objects',0),('failures',0),('command_pairs',21),('command_result_differences',0),('command_UI_word_differences',0),('command_timing_differences',6),('command_RNG_differences',4),('command_duration_changes',3),('later_same_frame_RGB_differences',116),('semantic_upper_region_differences',0)]:require(len(a[key])==count,'actual count:'+key)
    exact(v,dict(visual_review_pending=False,no_missing_clipped_duplicate_or_extra_blank_page_observed=True,no_full_RAM_future_sequence_broad_simulation_or_complete_cause_claim=True,all_measured_differences_retained_for_later_older_record_technical_reaudit=True,final_source_rats_food_safe_notice_and_English_dizzy_starving_notice_viewed=True),'viewed limits')
    require(len(v['prompt_bounded_differences'])==16 and len(v['broader_later_differences'])==100 and [r['frame'] for r in v['following_B120_end_frames']]==[10056,10053],'later/following scope')
    require(names['name_literal_alignment_count']==32 and names['actual_complete_progressive_name_holds']==39 and names['full_catalogue_UI_unvisited'],'name scope')
    require({r['text'] for r in names['name_planes'] if r['actual_matching_header_holds']}=={'Lil Argot','Al Shin'},'source matched names')
    loader,census,entry=[load(conf[k]) for k in ['loader','census','entry']]
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and loader['SDK_IO_bridges_only_no_loader_or_cache_success_stub'],'whole loaders')
    require(census['all12_clean_current_target_commands_and_no_relative_sites_reexecuted'] and census['blocks'][0]['mapped_commands']==[dict(**m,source_0100_ancestors=[],target_0100_ancestors=[]) for m in mapping['blocks'][0]['mapped_native_commands']],'independent command census')
    require([(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in entry['selected_B210_source_events']]==[(210,210,211,[],[])],'source event')
    return p

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']=='dk4-lil-B210-editorial-release-v1','config format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical SC2')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'current runtime')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM');jp=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(jp)==conf['clean_SC2_sha256'],'clean SC2')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']];validate_natural_dialogue_batch(doc)
    exact(doc,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',formatting_review_pending=False,all10_five_individual_gates_true=True,actual_objects=10,actual_pages=10,actual_complete_body_name_holds=39,offline_only_objects=0,source_weapon_identity_remains_unstated=True,no_unsupported_purchase_absolute_sharpness_victims_magic_or_search_promise=True,approved_names_Rafael_Hodram_Joakim_Maria_Camille_preserved=True),'manuscript')
    require(doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and Path(doc['reference_map'])==Path(conf['reference_map']),'sealed map')
    require(seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==doc['reference_map_sha256'] and seal['all10_five_gates_and_exact_references_approved'],'reference approval')
    require(conf['required_map_flags']==FLAGS and all(mapping.get(k) is True for k in FLAGS),'complete map flags')
    require(mapping['format']=='dk4-lil-B210-source-relocation-map-v1' and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'] and mapping['required_runtime_ARM9_sha256']==sha(arm),'source-bound map')
    proof=observations(doc,mapping,conf);rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==10 and Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':4} and Counter(r['source_selector'] for r in rows)=={17:6,2:4},'ten decisions/actors')
    require(all(r['kind']=='progressive' and r['file_path']==PATH and r['block']==210 and all(r['review'].values()) and r['full_exchange_read_aloud_review'] for r in rows),'individual gates/kinds')
    require(len(mapping['blocks'])==1,'one block');spec=mapping['blocks'][0];blocks=list(IlnkContainer.parse(source).blocks);block=blocks[210];original=IlnkContainer.parse(jp).blocks[210]
    require(len(blocks)==336 and spec['block']==210 and sha(block)==spec['source_block_sha256'] and sha(original)==spec['clean_block_sha256'],'exact source blocks')
    require((len(block),spec['source_bytes'],spec['source_logical_end'],spec['source_tail_bytes'],spec['target_bytes'],spec['target_logical_end'],spec['target_tail_bytes'])==(688,688,686,2,656,654,2),'source/target extents')
    require(block[:4]==b'CS\0\1' and 8+struct.unpack_from('<H',block,4)[0]==686 and block[682:]==bytes(6),'source header/end/tail')
    require(not any(spec[k] for k in ['actor_style_commands','choice_commands','relative_skip_fixups','target_native_skip_cases']),'no invented controls')
    refs={r['id']:r for r in spec['text_records']};fonts={r['id']:r for r in proof['native_font_proof']['records']};stores={r['id']:r for r in proof['native_stored_proof']['records']};dispatch={r['id']:r for r in proof['relocated_control_proof']['relocated_dispatch_cases']};actual={r['id']:r for r in proof['actual_English_proof']['actual_panels']}
    require(set(refs)==set(fonts)==set(stores)==set(dispatch)==set(actual)==set(ids),'all individual proof sets');bindings=contract()['record_bindings'];patches=[];changes=[];rowcount=boundaries=pads=0
    for row in rows:
        ident=row['id'];ref,f,st,di,panel=[d[ident] for d in [refs,fonts,stores,dispatch,actual]];raw,old=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex']);a=row['current_reference']['offset'];sa=row['source_reference']['offset'];selector=row['source_selector']
        for side,bank,value in [('source',original,raw),('current',block,old)]:
            r=row[side+'_reference'];at=r['offset'];require(r['block']==210 and r['header_offset']==at-5 and r['bytes']==len(value) and r['record_index']==bank[:at].count(b'\0') and bank[at:at+len(value)+1]==value+b'\0','complete '+side+' reference:'+ident)
        require(old[0]==raw[0]==selector and block[a-5:a+1]==original[sa-5:sa+1]==bytes.fromhex(row['source_complete_preamble_hex'])==b'\0\x40\xff\xff\0'+raw[:1],'complete preamble:'+ident)
        require(row['speaker']=={2:'Lil Argot',17:'Al Shin'}[selector] and row['current_record_index']==ref['current_record_index']==ref['record_index']==row['current_reference']['record_index'],'speaker/index:'+ident)
        require(ref['source_reference']==row['source_reference'] and ref['current_reference']==row['current_reference'] and ref['old_offset']==a and ref['old_length']==len(old),'sealed references:'+ident)
        require(row['current_registered_catalogue_match'] is None and di['registered_catalog_match'] is None and di['source_selector']==di['resolved_actor_ID']==selector and di['source_voice_class']=={2:3,17:4}[selector],'catalogue/voice:'+ident)
        prose=row['english'].split('}',1)[1];require(' '.join(old[1:].decode('cp932').split())==row['current_effective_paragraph'] and (prose!=row['current_effective_paragraph'])==(row['editorial_decision']=='revise'),'revision decision:'+ident)
        require(row['editorial_decision']!='retain-wording' or bool(row.get('retention_reason')),'retention reason:'+ident)
        profile=profile_for(arm,block,ident);encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==ref['compiled_hex']==f['compiled_hex'] and not [i for i in qa['issues'] if i['severity'] in ['warning','error']],'exact compiled QA:'+ident)
        reason=bindings[ident]['row_count_reason'];require(row.get('qa_waivers',[])==(['line-break-count'] if reason else []) and (not reason or row.get('qa_waiver_reason')==reason),'individual rowcount reason:'+ident);rowcount+=bool(reason)
        require(row['reviewed_ordinary_boundaries']==qa['reviewed_ordinary_boundaries'],'source-bound ordinary wrap:'+ident);boundaries+=len(row['reviewed_ordinary_boundaries'])
        require(row['native_profile_maximum_total_rows']==row['original_physical_native_rows_per_page']==4 and row['native_page_count']==len(f['pages'])==1 and f['total_bytes']==f['complete_consumed_bytes'] and f['all_visible_first_internal_final_characters_in_order'] and f['no_blank_or_overlap_page'],'complete native page:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        pads+=pad;require(value.hex()==ref['target_hex']==st['final_target_hex']==di['target_hex'] and len(value)==ref['new_length'] and ref['parity_space_added']==pad and st['unchanged_words_glyphs_page_count_and_zero_ink_tail'],'stored target:'+ident)
        fp,sp=f['pages'][0],st['complete_pages']['pages'][0];require(Path(fp['native_plane']).read_bytes()==Path(sp['native_plane']).read_bytes() and sha(Path(fp['native_plane']).read_bytes())==fp['native_plane_sha256']==sp['native_plane_sha256'],'stored complete ink:'+ident)
        require(row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay'] and panel['native_pages']==1 and panel['complete_body_holds'] and panel['complete_name_holds'],'individual actual scope:'+ident)
        patches.append(dict(start=a,end=a+len(old),old=old,value=value));changes.append(dict(id=ident,block=210,kind='progressive',old_offset=a,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require((rowcount,boundaries,pads)==(5,2,4),'five reasons/two boundaries/four parity tails');patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping patches')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'undeclared interior reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:686]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(686)==654,'target logical extent');struct.pack_into('<H',logical,4,646);target=bytes(logical)+bytes(2);require(sha(target)==spec['target_block_sha256'],'target block hash')
    commands=spec['mapped_native_commands'];require(len(commands)==12 and sum(c['word']==0x4000 for c in commands)==10,'twelve commands')
    require([dict(word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],old_extent=c['old_native_extent'],new_extent=c['new_native_extent']) for c in commands]==spec['command_map'],'independent map agreement')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(mapped(a)==b and mapped(a+c['old_native_extent'])==b+c['new_native_extent'] and struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0]==c['word'],'command boundary/type')
        size=6 if c['word']==0x4000 else c['old_native_extent'];require(block[a:a+size]==target[b:b+size],'preamble/opaque operands')
    require([(c['old_offset'],c['new_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in commands if c['word']!=0x4000]==[(674,642,'00a0ffff24000110'),(682,650,'00000000')],'exact A000 and complete end')
    require(spec['complete_end_map']==dict(source_offset=682,target_offset=650,extent=4) and target[650:]==bytes(6),'end/tail map')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset']);require(at==ref['new_offset']==stores[change['id']]['final_target_offset']==dispatch[change['id']]['new_offset'] and target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:at].count(b'\0')==ref['new_record_index'],'integrated reference:'+change['id'])
    inverse=bytearray(logical);struct.pack_into('<H',inverse,4,678)
    for p in reversed(patches):at=mapped(p['start']);inverse[at:at+len(p['value'])]=p['old']
    require(bytes(inverse)+block[686:]==block,'all688 predecessor bytes inverse');newblocks=list(blocks);newblocks[210]=target;result=IlnkContainer(newblocks).to_bytes();require(sha(result)==conf['target_SC2_sha256'],'target SC2')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'] and result==NdsImage.open(conf['reference_ROM']).read_file(PATH),'approved reference')
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],reference_map=conf['reference_map'],source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),changed_records=changes,blocks=[dict(block=210,source_bytes=688,target_bytes=656,source_logical_end=686,target_logical_end=654,source_commands=12,relative_operands=0,inverse_restores_every_original_stored_byte=True)],all335_other_SC2_blocks_unchanged=True,all10_preambles_static_voices_zero_macros_A000_and_end_preserved=True,actual10_objects10_pages39_body_name_holds_and_all_measured_later_limits_preserved=True,approved_name_typography_layer_separate=True,full_goal_complete=False)
