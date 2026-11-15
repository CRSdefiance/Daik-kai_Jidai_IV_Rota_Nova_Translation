"""Atomic B223 compiler: all gates precede the sole archive write."""
from dk4tool.patch.lil_B223_atomic_support_v2 import *

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']=='dk4-lil-B223-editorial-release-v1','release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical SC2')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'current runtime')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean SC2')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']];validate_natural_dialogue_batch(doc)
    exact(doc,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',formatting_review_pending=False,all17_five_individual_gates_true=True,actual_objects=9,actual_pages=11,actual_complete_body_holds=37,actual_complete_name_holds=37,offline_only_objects=8,all207_name_alias_and_full_four_storyline_editorial_objective_open=True,three_personal_name_retentions_actor151_review_separate_no_duplicate_credit=True,source_prose_or_completion_credit_added=0),'manuscript')
    require(doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and Path(doc['reference_map'])==Path(conf['reference_map']),'sealed map')
    require(seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'seal hashes')
    exact(seal,dict(all17_five_gates_and_exact_references_approved=True,all22_commands_four_relatives_typed_aliases_and19_native_pages_bound=True,actual9_objects11_pages37_body37_headers8_offline_objects_explicit=True,all_measured_later_differences_and_final_captain0_2_retained=True,original_event223_dependency90_not_natural_activation_or_earned_progress=True),'seal obligations')
    require(conf['required_map_flags']==FLAGS and all(mapping.get(k) is True for k in FLAGS),'complete map flag contract')
    require(mapping['format']=='dk4-lil-B223-source-relocation-map-v1' and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'] and len(mapping['blocks'])==1,'source-bound map')
    font,stored,actual,controls=observations(doc,mapping,conf);rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==17 and Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':1} and Counter(r['kind'] for r in rows)=={'progressive':10,'typed-4100-actor-style-alternative':7},'17 exact decisions/kinds')
    require(all(set(r['review'])=={'source','context','localization','naturalness','formatting'} and all(r['review'].values()) and r['full_exchange_read_aloud_review'] and r['fresh_source_gloss'] and r['context'] and r['localization_note'] for r in rows),'individual five gates and full exchange')
    spec=mapping['blocks'][0];blocks=list(IlnkContainer.parse(source).blocks);block=blocks[223];original=IlnkContainer.parse(japanese).blocks[223]
    require(len(blocks)==336 and spec['block']==223 and sha(block)==spec['source_block_sha256'] and sha(original)==spec['clean_block_sha256'],'source/clean block')
    require((len(block),spec['source_bytes'],spec['source_logical_end'],spec['source_tail_bytes'],spec['target_bytes'],spec['target_logical_end'],spec['target_tail_bytes'])==(1316,1316,1316,0,1384,1384,0) and block[:4]==b'CS\0\1' and block[1312:]==bytes(4),'exact source/target end/tails')
    refs={r['id']:r for r in spec['all_object_references']};fonts={r['id']:r for r in font['records']};stores={r['id']:r for r in stored['records']};dispatch={r['id']:r for r in controls['dispatch_cases']};actualids={r['id'] for r in actual['actual_panels']}
    require(set(refs)==set(fonts)==set(stores)==set(dispatch)==set(ids),'individual proof IDs')
    bindings=contract()['record_bindings'];values={};changes=[];rowcount=0
    for row in rows:
        ident=row['id'];ref=refs[ident];f=fonts[ident];st=stores[ident];di=dispatch[ident];raw=bytes.fromhex(row['source_hex']);old=bytes.fromhex(row['current_hex']);typed=row['kind']!='progressive';selector=row['source_selector']
        require(row['block']==223 and row['file_path']==PATH and row['source_kind']==row['kind'],'record consumer:'+ident)
        for side,bank,value in [('source',original,raw),('current',block,old)]:
            r=row[side+'_reference'];at=r['offset'];require(r['block']==223 and r['bytes']==len(value) and bank[at:at+len(value)+1]==value+b'\0','exact '+side+' reference:'+ident)
        require(row['current_record_index']==block[:row['current_reference']['offset']].count(b'\0'),'current record index:'+ident)
        require(row['current_registered_catalogue_match'] is None and di['registered_catalog_match'] is None,'no catalogue override')
        require((row['english'].split('}',1)[1]!=row['current_effective_paragraph'])==(row['editorial_decision']=='revise'),'decision:'+ident)
        require(row['editorial_decision']!='retain-wording' or bool(row.get('retention_reason')),'retention reason:'+ident)
        require(row['speaker']==('Source D0 role1 speaker;automatic original voice style '+(','.join(map(str,row['style_indices']))) if typed else {2:'Lil Argot',13:'Cesare Tony',21:'Ian Dukov'}.get(selector)),'source-mapped speaker label:'+ident)
        if typed:
            require(selector==208 and row['virtual_formatter_selector_not_stored_in_actor_style_body'] and row['style_indices'] and row['compiled_hex'].startswith('d0'),'typed virtual selector:'+ident)
            compiler_raw=b'\xd0'+raw
        else:
            at=row['current_reference']['offset'];sa=row['source_reference']['offset'];require(raw[0]==old[0]==selector and block[at-5:at+1]==original[sa-5:sa+1]==bytes.fromhex(row['source_complete_preamble_hex'])==b'\0\x40\xff\xff\0'+raw[:1],'complete speech preamble:'+ident);compiler_raw=raw
        require(di['source_selector']==selector and di['resolved_actor_ID']==(151 if typed else selector),'resolved original actor:'+ident)
        profile=profile_for(arm,block,ident);encoded=codec.encode_relocatable_dialogue(compiler_raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(compiler_raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==ref['compiled_hex']==f['compiled_hex'],'compiled native target:'+ident)
        require(not [x for x in qa['issues'] if x['severity'] in ['warning','error']],'unapproved QA:'+ident)
        require(row['reviewed_ordinary_boundaries']==qa['reviewed_ordinary_boundaries']==bindings[ident]['ordinary_wrap_reasons'] and row['qa_waivers']==qa['qa_waivers']==bindings[ident]['qa_waivers'] and row['base_QA_report']['base_QA_issues']==qa['base_QA_issues']==bindings[ident]['base_QA_issues'] and row['exact_reviewed_base_warnings']==qa['exact_reviewed_base_warnings']==bindings[ident]['exact_reviewed_base_warnings'] and qa['all_original_base_QA_issues_preserved'],'exact ordinary boundaries/waivers:'+ident)
        require(row['row_count_reason']==bindings[ident]['row_count_reason'] and row['qa_waiver_reason']==bindings[ident]['qa_waiver_reason'],'individual rowcount reason:'+ident);rowcount+=bool(bindings[ident]['row_count_reason'])
        require(row['native_profile_maximum_total_rows']==profile.max_lines and row['original_physical_native_rows_per_page']==4 and row['native_page_count']==len(f['pages'])==bindings[ident]['native_page_count'],'physical pages:'+ident)
        require(f['total_bytes']==f['complete_consumed_bytes'] and f['all_visible_first_internal_final_characters_in_order'] and f['no_blank_or_overlap_page'],'whole glyphs/consumption:'+ident)
        value=encoded.encoded[1:] if typed else encoded.encoded
        if not typed and len(value)%2!=len(old)%2:value+=b' '
        require(value.hex()==ref['target_hex']==st['final_target_hex']==di['target_hex'] and st['unchanged_words_glyphs_page_count_and_zero_ink_tail'],'stored target:'+ident)
        require(ref['old_offset']==row['current_reference']['offset'] and ref['old_length']==len(old) and ref['new_length']==len(value),'relocation reference:'+ident)
        require(row['actual_record_observed']==(ident in actualids) and row['native_plane_verified_not_actual_English_gameplay']==(ident not in actualids),'actual/offline scope:'+ident)
        values[ident]=value;changes.append(dict(id=ident,block=223,kind=row['kind'],old_offset=ref['old_offset'],new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(rowcount==6 and sum(r['actual_record_observed'] for r in rows)==9,'six rowcount reasons/six actual objects')
    patches=[]
    for row in rows:
        if row['kind']=='progressive':
            at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);patches.append(dict(start=at,end=at+len(old),old=old,value=values[row['id']]))
    require(len(spec['actor_style_commands'])==1 and not spec['choice_commands'],'two automatic objects/no player choice')
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
    patches.sort(key=lambda p:p['start']);require(len(patches)==11 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'seven nonoverlapping patches')
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
    pieces.append(block[last:1316]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(1316)==1384,'logical target extent')
    edges=spec['relative_skip_fixups'];require([(e['offset'],e['word'],e['span'],e['skip_target']) for e in edges]==[(1146,512,4,1154),(1150,768,4,1158),(1154,256,146,1304),(1300,256,0,1304)],'all four source relative sites')
    for e in edges:
        a=mapped(e['offset']);b=mapped(e['skip_target']);span=b-a-4
        require(struct.unpack_from('<HH',block,e['offset'])==(e['word'],e['span']) and (a,a+4,b,span)==(e['new_offset'],e['new_fallthrough'],e['new_skip_target'],e['new_span']),'mapped relative operand')
        struct.pack_into('<H',logical,a+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical);require(sha(target)==spec['target_block_sha256'] and len(target)==1384,'target block hash')
    commands=spec['mapped_native_commands'];require(len(commands)==22 and [{k:c[k] for k in ['word','old_offset','new_offset']}|{'old_extent':c['old_native_extent'],'new_extent':c['new_native_extent']} for c in commands]==spec['command_map'],'all22 independent command maps')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0] and mapped(a)==b and mapped(a+c['old_native_extent'])==b+c['new_native_extent'],'command extent/type')
        if c['word'] not in [256,512,768,1024,16384,16640]:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque instruction exact')
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];require(target[at:at+ref['new_length']+1]==values[row['id']]+b'\0' and target[:at].count(b'\0')==ref['new_record_index'] and at==stores[row['id']]['final_target_offset']==dispatch[row['id']]['new_offset'],'complete integrated text reference')
        if row['kind']=='progressive':require(at==mapped(ref['old_offset']),'mapped progressive reference')
        else:require(at==mapped(ref['old_command_offset'])+ref['new_relative_offset'],'mapped typed reference')
    require(spec['complete_end_map']==dict(source_offset=1312,target_offset=1380,extent=4) and target[1380:]==bytes(4),'complete four-byte end/tail')
    cases=spec['target_native_skip_cases'];require(len(cases)==20 and {(r['new_offset'],r['previous_value']) for r in cases}=={(e['new_offset'],p) for e in edges for p in [0,1,2,3,0xFFFFFFFF]},'20 distinct original branch values')
    for r in cases:
        e=next(e for e in edges if e['new_offset']==r['new_offset']);p=r['previous_value'];take=e['word']==256 or (e['word']==512 and p==0) or (e['word']==768 and p==1) or (e['word']==1024 and p==2)
        require(e['new_offset']+r['extent']==(e['new_skip_target'] if take else e['new_fallthrough']) and r['all_ABI_actor_RNG_4MiB_and_canaries_exact'],'original branch extent/guards')
    inverse=bytearray(logical);struct.pack_into('<H',inverse,4,1308)
    for e in edges:struct.pack_into('<H',inverse,e['new_offset']+2,e['span'])
    for p in reversed(patches):at=mapped(p['start']);inverse[at:at+len(p['value'])]=p['old']
    require(bytes(inverse)==block,'all1316 predecessor bytes inverse')
    newblocks=list(blocks);newblocks[223]=target;result=IlnkContainer(newblocks).to_bytes();require(sha(result)==conf['target_SC2_sha256'],'complete target SC2')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'] and result==NdsImage.open(conf['reference_ROM']).read_file(PATH),'approved reference')
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],reference_map=conf['reference_map'],source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),changed_records=changes,blocks=[dict(block=223,source_bytes=1316,target_bytes=1384,source_logical_end=1316,target_logical_end=1384,relative_operands=4,source_commands=22,inverse_restores_every_original_stored_byte=True)],all335_other_SC2_blocks_unchanged=True,all10_preambles_one_D0_object_seven_bodies_eight_slots_and_aliases_preserved=True,native19_pages_actual9_objects11_pages37_holds_offline8_explicit=True,all_measured_later_differences_and_final_scope_limits_retained=True,all207_name_alias_and_full_editorial_scope_open=True,full_goal_complete=False)
