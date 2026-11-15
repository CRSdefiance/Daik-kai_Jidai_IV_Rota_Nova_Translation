"""Atomic B209 reconstruction: five speeches, two typed objects and four relative operands."""
import json
import struct
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.lil_B209_profile_v1 import profile_for,contract
from dk4tool.dialogue import lil_B209_layout_v1 as codec
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B209_editorial_release_v2.json'
FLAGS=['external_references_complete','all20_records5_speeches15_stored_alternatives16_slots_two_typed_objects_bound',
       'all_four_relative_source_target_operands_and20_native_cases_bound',
       'source1148_full_inverse_target1336_logical1334_tail2_complete_end1330',
       'native_original_four_row_pagination_and_source_names_controls_preserved',
       'representative_English6_objects8_pages25_holds_and14_offline_objects_explicit',
       'all_measured_later_limits_preserved']

def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Lil B209 '+message)
def exact(d,fields,label):
    for k,v in fields.items():require(k in d and d[k]==v,label+':'+k)

def observations(doc,mapping,conf):
    font,stored,policy,approval,names,actual,view=[load(doc[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_names_review','actual_English_proof','actual_English_view']]
    exact(font,dict(complete_native_pages=22,logical_compiled_input_alignment_cases=160,both_first_and_second_letter_use_original_four_row_native_continuation=True,all_other18_objects_one_native_page=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,each216x64_plane_exact_independent_current_font_and_all_canaries=True,continuation_first_row_retains_original6px_guard_indent=True,D0_fallback151_unchanged=True),'complete native planes')
    exact(stored,dict(final_stored_alignment_cases=80,fresh_alignment_cases=12,exact_reused_alignment_cases=68,fresh_parity_tail_records=3,complete_pages=22,all_final_stored_targets_equal_reviewed_complete_native_ink=True,no_extra_blank_page_or_lost_leading_trailing_internal_glyph=True,all15_style_bodies_exclude_virtual_D0_and_have_independent_terminators=True),'stored native planes')
    exact(policy,dict(positive_count=20,negative_count=54,all_rejections_before_ROM_or_archive_mutation=True,no_unwaived_warning_or_error=True,source_bound_ordinary_boundary_rules_not_global_waivers=True),'native policy')
    require(len(policy['negative_cases'])==54 and all(r['rejected'] for r in policy['negative_cases']) and len(policy['row_count_reasons'])==6,'54 meaningful policy rejections/six reasons')
    exact(approval,dict(all20_five_gates_approved=True,native_pages=22,original_viewport=[216,64],native_rows_per_page=4,two_exact_native_continuations_no_taller_viewport=True,logical_compiled_alignments=160,final_stored_alignments=80,name_literal_alignments=112,layout_negative_controls=54,actual_unique_objects=6,actual_native_pages=8,complete_body_name_holds=25,offline_only_objects=14,all12timing12RNG_two_duration187broader_RGB_and_final_world_limits_retained=True,original_event209_dependency85_not_naturally_selected=True,no_full_effects_earned_progress_routes_hardware_or_broad_simulation_claim=True),'approval scope')
    require(sha(Path(doc['native_approved_manuscript']).read_bytes())==approval['manuscript_sha256']==doc['native_approved_manuscript_sha256'],'native approved predecessor')
    exact(names,dict(proper_name_revision_count=0,full_source_signature='白樹玄丞行尚（ユキヒサ）',retained_current_full_signature='Yukihisa Genjo Shiraki',four_complete_progressive_name_planes112_literal_alignments_and17_actual_source_header_holds=True,Jam_actual_header_unvisited_native_plane_complete=True,full_catalogue_UI_unvisited_native_full_name_getters_bound=True,fallback151_progressive_Sailor_full_catalogue_Retainer_not_global_editorial_approval=True,no_name_asset_change_no_new_name_UI_or_dialogue_credit=True,no_new_user_approval_or_original_Latin_artwork_claim=True,all207_names_aliases_earlier_consumers_and_full_editorial_goal_open=True),'name retention and open scope')
    fields=load(names['source_name_fields'])['source_name_fields']
    require(names['proper_name_retentions']==[r for r in fields if r['actor_ID'] in [2,11,12]] and names['fallback151_consumer_specific_open_lead']==next(r for r in fields if r['actor_ID']==151),'exact proper/full/additional/fallback name fields')
    require([(r['actor_ID'],r['progressive'],r['catalogue']) for r in names['proper_name_retentions']]==[(2,'Lil Argot','Lil Argot'),(11,'Jam Ludwyan','Jam Jack Ludwyan'),(12,'Yukihisa Shiraki','Yukihisa Genjo Shiraki')],'existing source-bound spellings')
    exact(actual,dict(actual_unique_objects=6,actual_complete_native_pages=8,complete_native_body_holds=25,complete_native_name_holds=25,stored_commands=27,source_exit_frame=4294,English_exit_frame=4774,English_normal_port_sample_frame=4870,ordinary_original_A_schedule_identical_to_source=True,original_predicate_type2_Boolean0_and_branches_preserved=True,all335_other_blocks_and_all_other_files_components_runtime_and_names_equal_source_fixture=True,explicit_Jam_R65_and13_other_stored_style_bodies_unvisited=True,whole_RAM_final_PRNG_and_future_simulation_equivalence_unproven=True),'actual scope')
    for k,n in [('failures',0),('command_result_differences',0),('command_UI_word_differences',0),('command_pairs',24),('command_timing_differences',12),('command_RNG_differences',12),('command_duration_changes',2),('later_same_frame_RGB_differences',187)]:require(len(actual[k])==n,'actual count:'+k)
    exact(view,dict(visual_review_pending=False,all_eight_actual_pages_and_complete_native_names_viewed=True,all25_complete_body_and_style11_name_holds_match_independent_native_models=True,no_clipped_missing_duplicate_or_extra_blank_native_page_observed=True,Jam_R65_and13_other_stored_alternatives_native_only_not_actual_gameplay=True,no_same_frame_or_whole_RGB_equivalence_claim_from_semantic_pairs=True,all12timing12RNG_two_duration187_broader_RGB_differences_retained=True,no_broad_final_RAM_future_simulation_or_complete_causal_equivalence_claim=True,later_older_record_technical_reaudit_retains_all_measured_differences=True,natural_event209_dependency85_location_earned_progress_full_effects_routes_hardware_unclaimed=True,final_PRNG_seeds=[4169795564,1095690386],final_calendar_ticks=[2496,2401]),'viewed actual and later limits')
    require(len(view['upper_scene_and_portrait_semantic_pairs'])==25 and not view['upper_scene_and_portrait_differences'],'semantic scene regions')
    controls=load(conf['controls']);entry=load(conf['entry']);loader=load(conf['loader']);census=load(conf['census'])
    exact(controls,dict(predicate_type2_Boolean0_preserved=True,twenty_target_relative_cases_bound=True,no_FE_or_player_choice_invented=True,all18_commands5_speech_preambles15_stored_bodies16_slots_and_aliases_preserved=True),'relocated controls')
    require(len(controls['relocated_dispatch_cases'])==20 and len(controls['whole_relocated4100_commands'])==2 and len(controls['all207_actor_two_style_command_pointer_cases']['cases'])==414 and len(controls['structural_source4500_4621_A000_cases'])==len(controls['target_five_complete_end_cases'])==5,'dispatch/style/staging/end coverage')
    require([(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in entry['selected_B209_source_events']]==[(209,209,210,[85],[])],'source event/dependency')
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and census['all18_clean_current_target_commands_and_four_relative_sites_reexecuted'],'loaders and shipped census')
    return font,stored,actual,controls

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']=='dk4-lil-B209-editorial-release-v2','release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical SC2')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'current runtime')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean SC2')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']];validate_natural_dialogue_batch(doc)
    exact(doc,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',formatting_review_pending=False,all20_five_individual_gates_true=True,actual_objects=6,actual_pages=8,actual_complete_body_name_holds=25,offline_only_objects=14,all207_name_alias_review_and_full_four_storyline_editorial_objective_open=True,no_name_asset_change_or_new_name_UI_credit=True,source_prose_or_completion_credit_added=0),'manuscript')
    require(doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and Path(doc['reference_map'])==Path(conf['reference_map']),'sealed map')
    require(seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'seal hashes')
    exact(seal,dict(all20_five_gates_and_exact_reference_obligations_approved=True,all_names_controls_slots_aliases_relative_spans_bounds_and_native_pages_bound=True,actual6_objects8_pages25_body_name_holds_not_all20_gameplay=True,all12_timing12_RNG_two_duration187_broader_RGB_and_final_state_limits_preserved=True,original_event209_dependency85_not_natural_activation_or_earned_progress=True),'seal obligations')
    require(conf['required_map_flags']==FLAGS and all(mapping.get(k) is True for k in FLAGS),'complete map flag contract')
    require(mapping['format']=='dk4-source-bound-nested-relocation-map-v1' and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'] and len(mapping['blocks'])==1,'source-bound map')
    font,stored,actual,controls=observations(doc,mapping,conf);rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==20 and Counter(r['editorial_decision'] for r in rows)=={'revise':17,'retain-wording':3} and Counter(r['kind'] for r in rows)=={'progressive':5,'typed-4100-actor-style-alternative':15},'20 exact decisions/kinds')
    require(all(set(r['review'])=={'source','context','localization','naturalness','formatting'} and all(r['review'].values()) and r['full_exchange_read_aloud_review'] and r['fresh_source_gloss'] and r['context'] and r['localization_note'] for r in rows),'individual five gates and full exchange')
    spec=mapping['blocks'][0];blocks=list(IlnkContainer.parse(source).blocks);block=blocks[209];original=IlnkContainer.parse(japanese).blocks[209]
    require(len(blocks)==336 and spec['block']==209 and sha(block)==spec['source_block_sha256'] and sha(original)==spec['clean_block_sha256'],'source/clean block')
    require((len(block),spec['source_bytes'],spec['source_logical_end'],spec['source_tail_bytes'],spec['target_bytes'],spec['target_logical_end'],spec['target_tail_bytes'])==(1148,1148,1148,0,1336,1334,2) and block[:4]==b'CS\0\1' and block[1144:]==bytes(4),'exact source/target end/tails')
    refs={r['id']:r for r in spec['text_records']};fonts={r['id']:r for r in font['records']};stores={r['id']:r for r in stored['records']};dispatch={r['id']:r for r in controls['relocated_dispatch_cases']};actualids={r['id'] for r in actual['actual_panels']}
    require(set(refs)==set(fonts)==set(stores)==set(dispatch)==set(ids),'individual proof IDs')
    bindings=contract()['record_bindings'];values={};changes=[];rowcount=0
    for row in rows:
        ident=row['id'];ref=refs[ident];f=fonts[ident];st=stores[ident];di=dispatch[ident];raw=bytes.fromhex(row['source_hex']);old=bytes.fromhex(row['current_hex']);typed=row['kind']!='progressive';selector=row['source_selector']
        require(row['block']==209 and row['file_path']==PATH and row['source_kind']==row['kind'],'record consumer:'+ident)
        for side,bank,value in [('source',original,raw),('current',block,old)]:
            r=row[side+'_reference'];at=r['offset'];require(r['block']==209 and r['bytes']==len(value) and bank[at:at+len(value)+1]==value+b'\0','exact '+side+' reference:'+ident)
        require(row['current_record_index']==block[:row['current_reference']['offset']].count(b'\0'),'current record index:'+ident)
        require(row['current_registered_catalogue_match'] is None and di['registered_catalog_match'] is None,'no catalogue override')
        require((row['english'].split('}',1)[1]!=row['current_effective_paragraph'])==(row['editorial_decision']=='revise'),'decision:'+ident)
        require(row['editorial_decision']!='retain-wording' or bool(row.get('retention_reason')),'retention reason:'+ident)
        require(row['speaker']==('Source D0 role1 speaker,automatic original actor voice style '+('/'.join(map(str,row['style_indices']))) if typed else {2:'Lil Argot',11:'Jam Jack Ludwyan',12:'Yukihisa Genjo Shiraki'}.get(selector)),'source-mapped speaker label:'+ident)
        if typed:
            require(selector==208 and row['virtual_formatter_selector_not_stored_in_actor_style_body'] and row['style_indices'] and row['compiled_stored_alternative_hex']==row['compiled_hex'][2:],'typed virtual selector:'+ident)
            compiler_raw=b'\xd0'+raw
        else:
            at=row['current_reference']['offset'];sa=row['source_reference']['offset'];require(raw[0]==old[0]==selector and block[at-5:at+1]==original[sa-5:sa+1]==bytes.fromhex(row['source_complete_preamble_hex'])==b'\0\x40\xff\xff\0'+raw[:1],'complete speech preamble:'+ident);compiler_raw=raw
        require(di['source_selector']==selector and di['resolved_actor_ID']==(151 if typed else selector),'resolved original actor:'+ident)
        profile=profile_for(arm,block,ident);encoded=codec.encode_relocatable_dialogue(compiler_raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(compiler_raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==ref['compiled_hex']==f['compiled_hex'],'compiled native target:'+ident)
        require(not [x for x in qa['issues'] if x['severity'] in ['warning','error']],'unapproved QA:'+ident)
        require(row['reviewed_ordinary_boundaries']==qa['reviewed_ordinary_boundaries'] and row.get('qa_waivers',[])==(['line-break-count'] if bindings[ident]['row_count_reason'] else []),'exact ordinary boundaries/waivers:'+ident)
        require(not bindings[ident]['row_count_reason'] or row.get('qa_waiver_reason')==bindings[ident]['row_count_reason'],'individual rowcount reason:'+ident);rowcount+=bool(bindings[ident]['row_count_reason'])
        require(row['native_profile_maximum_total_rows']==profile.max_lines and row['original_physical_native_rows_per_page']==4 and row['native_page_count']==len(f['pages'])==bindings[ident]['native_page_count'],'physical pages:'+ident)
        require(f['total_bytes']==f['complete_consumed_bytes'] and f['all_visible_first_internal_final_characters_in_order'] and f['no_blank_or_overlap_page'],'whole glyphs/consumption:'+ident)
        value=encoded.encoded[1:] if typed else encoded.encoded
        if not typed and len(value)%2!=len(old)%2:value+=b' '
        require(value.hex()==ref['target_hex']==st['final_target_hex']==di['target_hex'] and st['unchanged_words_glyphs_page_count_and_zero_ink_tail'],'stored target:'+ident)
        require(ref['old_offset']==row['current_reference']['offset'] and ref['old_length']==len(old) and ref['new_length']==len(value),'relocation reference:'+ident)
        require(row['actual_record_observed']==(ident in actualids) and row['native_plane_verified_not_actual_English_gameplay']==(ident not in actualids),'actual/offline scope:'+ident)
        values[ident]=value;changes.append(dict(id=ident,block=209,kind=row['kind'],old_offset=ref['old_offset'],new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(rowcount==6 and sum(r['actual_record_observed'] for r in rows)==6,'six rowcount reasons/six actual objects')
    patches=[]
    for row in rows:
        if row['kind']=='progressive':
            at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);patches.append(dict(start=at,end=at+len(old),old=old,value=values[row['id']]))
    require(len(spec['actor_style_commands'])==2 and not spec['choice_commands'],'two automatic objects/no player choice')
    for obj in spec['actor_style_commands']:
        at=obj['old_offset'];old=block[at:at+obj['old_length']];table=[None]*8;chunks=[];cursor=0;oldtable=list(struct.unpack_from('<8H',old,2));candidates=sorted([r for r in rows if r['kind']!='progressive' and r['command_offset']==at],key=lambda r:r['current_reference']['offset'])
        require(old[:2]==original[at:at+2]==b'\0\x41' and old[18:20]==original[at+18:at+20]==b'\0\xd0','source typed header')
        require(oldtable==obj['old_style_offsets'] and oldtable==list(struct.unpack_from('<8H',original,at+2)),'source typed table')
        for row in candidates:
            ref=refs[row['id']];require([i for i,v in enumerate(oldtable) if at+20+v==row['current_reference']['offset']]==row['style_indices'],'all source slots/aliases')
            require(ref['old_command_offset']==at and ref['new_relative_offset']==20+cursor and ref['virtual_formatter_selector_not_stored'] and ref['virtual_D0_excluded_from_stored_body'],'typed reference body')
            for i in row['style_indices']:require(table[i] is None,'duplicate style slot');table[i]=cursor
            part=values[row['id']]+b'\0';part+=bytes(-len(part)%2);chunks.append(part);cursor+=len(part)
        require(all(isinstance(v,int) for v in table) and table==obj['new_style_offsets'] and all((oldtable[i]==oldtable[j])==(table[i]==table[j]) for i in range(8) for j in range(8)),'all8 slots/aliases preserved')
        value=old[:2]+struct.pack('<8H',*table)+old[18:20]+b''.join(chunks);require(value.hex()==obj['target_hex'] and len(value)==obj['new_length'],'whole typed object')
        patches.append(dict(start=at,end=at+len(old),old=old,value=value))
    patches.sort(key=lambda p:p['start']);require(len(patches)==7 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'seven nonoverlapping patches')
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
    pieces.append(block[last:]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(1148)==1334,'logical target extent')
    edges=spec['relative_skip_fixups'];require([(e['offset'],e['word'],e['span'],e['skip_target']) for e in edges]==[(694,512,4,702),(698,768,338,1040),(1036,256,54,1094),(1090,256,0,1094)],'all four source relative sites')
    for e in edges:
        a=mapped(e['offset']);b=mapped(e['skip_target']);span=b-a-4
        require(struct.unpack_from('<HH',block,e['offset'])==(e['word'],e['span']) and (a,a+4,b,span)==(e['new_offset'],e['new_fallthrough'],e['new_skip_target'],e['new_span']),'mapped relative operand')
        struct.pack_into('<H',logical,a+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(2);require(sha(target)==spec['target_block_sha256'] and len(target)==1336,'target block hash')
    commands=spec['mapped_native_commands'];require(len(commands)==18 and [{k:c[k] for k in ['word','old_offset','new_offset']}|{'old_extent':c['old_native_extent'],'new_extent':c['new_native_extent']} for c in commands]==spec['command_map'],'all18 independent command maps')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0] and mapped(a)==b and mapped(a+c['old_native_extent'])==b+c['new_native_extent'],'command extent/type')
        if c['word'] not in [256,512,768,1024,16384,16640]:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque instruction exact')
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];require(target[at:at+ref['new_length']+1]==values[row['id']]+b'\0' and target[:at].count(b'\0')==ref['new_record_index'] and at==stores[row['id']]['final_target_offset']==dispatch[row['id']]['new_offset'],'complete integrated text reference')
        if row['kind']=='progressive':require(at==mapped(ref['old_offset']),'mapped progressive reference')
        else:require(at==mapped(ref['old_command_offset'])+ref['new_relative_offset'],'mapped typed reference')
    require(spec['complete_end_map']==dict(source_offset=1144,target_offset=1330,extent=4) and target[1330:]==bytes(6),'complete four-byte end/tail')
    cases=spec['target_native_skip_cases'];require(len(cases)==20 and {(r['new_offset'],r['previous_value']) for r in cases}=={(e['new_offset'],p) for e in edges for p in [0,1,2,3,0xFFFFFFFF]},'20 distinct original branch values')
    for r in cases:
        e=next(e for e in edges if e['new_offset']==r['new_offset']);p=r['previous_value'];take=e['word']==256 or (e['word']==512 and p==0) or (e['word']==768 and p==1) or (e['word']==1024 and p==2)
        require(e['new_offset']+r['extent']==(e['new_skip_target'] if take else e['new_fallthrough']) and r['all_ABI_actor_RNG_4MiB_and_canaries_exact'],'original branch extent/guards')
    inverse=bytearray(logical);struct.pack_into('<H',inverse,4,1140)
    for e in edges:struct.pack_into('<H',inverse,e['new_offset']+2,e['span'])
    for p in reversed(patches):at=mapped(p['start']);inverse[at:at+len(p['value'])]=p['old']
    require(bytes(inverse)==block,'all1148 predecessor bytes inverse')
    newblocks=list(blocks);newblocks[209]=target;result=IlnkContainer(newblocks).to_bytes();require(sha(result)==conf['target_SC2_sha256'],'complete target SC2')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'] and result==NdsImage.open(conf['reference_ROM']).read_file(PATH),'approved reference')
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],reference_map=conf['reference_map'],source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),changed_records=changes,blocks=[dict(block=209,source_bytes=1148,target_bytes=1336,source_logical_end=1148,target_logical_end=1334,relative_operands=4,source_commands=18,inverse_restores_every_original_stored_byte=True)],all335_other_SC2_blocks_unchanged=True,all5_preambles2_D0_objects15_bodies16_slots_and_aliases_preserved=True,native22_pages_actual6_objects8_pages25_holds_offline14_explicit=True,all_timing_RNG_broader_RGB_and_final_state_limits_retained=True,all207_name_alias_and_full_editorial_scope_open=True,full_goal_complete=False)
