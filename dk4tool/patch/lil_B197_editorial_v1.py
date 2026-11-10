"""Atomic source-bound B197 speech, three-option and common-ending integration."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B197_layout_v1 as codec
from dk4tool.dialogue.lil_B197_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B197_editorial_release_v1.json'
SELECTORS={21,169,254}
MENUS=[230]
END_MAP=[(874,998)]

def load(path):return json.loads(Path(path).read_bytes())
def require(value,message):
    if not value:raise ValueError('Lil B197 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B197-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,menu,mapping,seal=[load(conf[k]) for k in ['manuscript','choices','reference_map','reference_approval']]
    for batch in [doc,menu]:
        validate_natural_dialogue_batch(batch)
        require(batch['translation_policy']=='natural-dialogue-v2' and batch['target_locale']=='en-US' and not batch['formatting_review_pending']
            and all(all(r['review'].values()) for r in batch['records']),'five-gate manuscript required')
        require(batch['reference_map']==conf['reference_map'] and batch['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all24_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_unchanged'],'source/reference approval required')
    require(seal['manuscripts']=={conf[k]:sha(Path(conf[k]).read_bytes()) for k in ['manuscript','choices']},'sealed manuscript changed')
    require(seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed reference map changed')
    require(mapping['format']=='dk4-lil-B197-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8
        and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    for name in conf['required_map_flags']:require(mapping.get(name) is True,'required source shape:'+name)
    proofs={k:load(doc[k]) for k in ['native_font_proof','final_padding_proof','final_choice_proof','relocated_control_proof','termination_decode_proof','representative_proof','postscene_native_state_proof','source_bound_wrap_retention_proof']}
    native,stored,typed,control,ends,sample,observed,wrap=[proofs[k] for k in proofs]
    approval=load(conf['native_approval']);actual=load(observed['actual_proof'])
    require(len(native['cases'])==21 and native['current_original_macro_alignment_calls']==168 and native['complete_progressive_planes']==20
        and native['complete_FE_logical_and_physical_planes']==1 and len(native['negative_controls'])==18,'complete native consumers/negatives required')
    require(all(r['rejected'] for r in native['negative_controls']) and len(approval['formatter_negatives'])==28,'formatter/consumer negatives required')
    require(len(stored['final_target_parity_cases'])==21 and stored['current_final_stored_macro_alignment_cases']==84
        and stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==56
        and stored['all21_final_targets_complete_native_planes_equal_reviewed_planes'],'stored speech proof required')
    require(typed['source_count3_option_order_and_original_selection_cancel_results_preserved'] and len(typed['actual_target_record_references'])==3
        and typed['fresh_count_calls']==2 and typed['fresh_label_pointer_calls']==6 and typed['reused_native_selection_cancel_cases']==8
        and typed['reused_complete_current_reviewed_style_planes']==12,'stored menu proof required')
    require(len(control['relocated_dispatch_cases'])==21 and len(control['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==11
        and len(control['picture_and47xx_current_relocated_pairs'])==3 and control['original47xx_R3_is_exact_mapped_stream_instruction_pointer'],'relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['no_relative_destination_at_or_beyond_logical_end'],'guarded common ending required')
    require(sample['actual_original_menu_indices']==[0,1,2] and sample['original_menu_offset']==230
        and sample['all_three_label_meanings_and_visible_selection_return_associations_verified'],'honest representative menu scope required')
    require(observed['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not observed['visual_review_pending']
        and observed['no_open_translation_specific_display_menu_control_or_return_finding']
        and observed['new_successful_English_runs']==4 and observed['new_successful_English_frames']==43604
        and observed['reused_prior_source_runs']==3 and observed['total_successful_frames']==82607,'viewed actual approval required')
    require(not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences'],'actual display/control differences changed')
    require(len(actual['actual_panels'])==21 and len(actual['all_actual_speech_observations'])==35 and len(actual['actual_menu_cases'])==3
        and actual['complete_native_holds']==128,'actual scope differs')
    require(len(actual['command_timing_differences'])==59 and len(actual['later_whole_RGB_differences'])==82
        and observed['paired_command_timing_differences']==actual['command_timing_differences'] and observed['postscene_whole_RGB_differences']==actual['later_whole_RGB_differences']
        and observed['broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks']
        and observed['no_causal_explanation_of_timing_RNG_or_world_differences_certified'],'honest difference accounting required')
    require(observed['source_matched_blank_portrait_name_additional_records']==[64,89]
        and observed['all128_complete_native_holds_match_source_upper_portrait_name_and_picture_regions'],'source display baseline required')
    require(observed['all_three_actual_indices0_1_2_complete_labels_and_visible_highlights_verified']
        and observed['initial_menu_sampling_failure_resolved_by16_new_complete_active_highlight_holds_without_retiming'],'visible menu evidence required')
    views=observed['all_actual_consumer_menu_sheets_viewed']+observed['paired_full_screen_views']
    require(len(views)==9 and all(s['viewed'] and s['viewed_after_image_return'] and s['original_detail'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views),'viewed screens changed')
    require(len(observed['paired_final_state_measurements'])==3 and observed['no_buy_five_native_groups_actor_captain_and_PRNG_equal']
        and observed['buy_delegate_models_persistent_objects_actor_and_PRNG_differ_buy_calendar_group_also_differs'],'measured state scope differs')
    terms=load(doc['actor_terminology_reconciliation']);funds=load(doc['source_financial_context'])
    require(terms['money_term']=='gold' and terms['stat_term']['English']=='Charm' and terms['exact_native_payment_amount']==8500,'source terms differ')
    require(terms['approved_prose_names']=={'21':'Ian Dukov','169':'Alluring Woman'},'approved prose names differ')
    for flag in conf['required_term_flags']:require(terms.get(flag) is True,'source context required:'+flag)
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={21:1,169:0},'two source voices differ')
    require(funds['source8500_price_matches_exact_native_payment_amount'] and len(funds['cases'])==6,'exact8500 source price required')
    require(wrap['exact_record']=='DK4_MES_B197_R0074' and wrap['visible_rows']==["I'd like to buy it, but I don't",'have that kind of money.']
        and wrap['formatter_font_width_phase_guard_and_all_prose_bytes_unchanged'] and wrap['no_global_weak_word_waiver'],'exact R74 wrap proof required')
    rows,labels=doc['records'],menu['records'];ids={r['id'] for r in rows};label_ids={r['id'] for r in labels}
    require(len(rows)==len(ids)==21 and len(labels)==len(label_ids)==3 and not ids&label_ids,'24 unique objects required')
    require({r['source_selector'] for r in rows}==SELECTORS and Counter(r['kind'] for r in rows)=={'progressive':20,'system-FE':1},'speaker/consumer scope differs')
    require(Counter(r['editorial_decision'] for r in rows+labels)=={'revise':16,'retain-wording':8}
        and all(r.get('fresh_retained_wording_justification') for r in rows+labels if r['editorial_decision']=='retain-wording'),'individual decisions required')
    observed_ids=set(mapping['actual_sampled_display_IDs']);offline=set(mapping['offline_only_display_IDs'])
    require(len(observed_ids)==21 and len(offline)==0 and not observed_ids&offline and observed_ids|offline==ids
        and observed_ids=={r['id'] for r in actual['actual_panels']} and offline==set(actual['offline_only_display_IDs']),'actual/offline ownership differs')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==197,'one exact block required');spec=mapping['blocks'][0]
    oldblocks=list(IlnkContainer.parse(source).blocks);block=oldblocks[197];original=IlnkContainer.parse(japanese).blocks[197]
    require(len(oldblocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'])==(880,878,1004,1002) and len(block)==880,'source/target extent metadata differs')
    require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in spec['mapped_native_commands']]==spec['command_map'],'both command maps must agree')
    fonts={r['id']:r for r in native['cases']};refs={r['id']:r for r in spec['text_records']}
    require(set(fonts)==set(refs)==ids,'native/reference coverage differs')
    require({r['id'] for r in control['relocated_dispatch_cases']}==ids and all(r['resolved_actor_ID']==(None if r['source_selector']==254 else r['source_selector']) and r['registered_catalog_match'] is None for r in control['relocated_dispatch_cases']),'dispatch ownership differs')
    patches=[];changes=[];macros=Counter()
    for row in rows:
        ident=row['id'];fe=row['kind']=='system-FE';case,ref=fonts[ident],refs[ident]
        require(row['actual_B22_display_fixture_observed']==(ident in observed_ids) and row['offline_only_native_display_checked']==(ident in offline),'individual display scope differs:'+ident)
        require(case['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
            and case['all_visible_origins_zero_and_within_four_rows'] and case['one_native_page_consumes_complete_target']
            and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete native plane differs:'+ident)
        if fe:require(all(c['null_source_actor'] for p in case['current_native_macro_pipelines'] for c in p['cases']),'FE null actor differs')
        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5 and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'reference extent differs:'+ident)
        require(row['block']==row['source_reference']['block']==197 and row['file_path']==PATH and row['source_record_index']==original[:sa].count(b'\0')
            and row['current_record_index']==row['record_index']==block[:at].count(b'\0'),'record identity differs:'+ident)
        require(row['source_selector']==raw[0]==old[0] and raw[0] in SELECTORS and (raw[0]==254)==fe and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}'),'selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0 and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'full preamble differs:'+ident)
        require(ref['record_index']==row['record_index'] and ref['old_offset']==at and ref['old_length']==len(old),'relocation owner differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode() for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])];require(sm==tm,'substitution order differs:'+ident);macros.update(sm)
        p=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        if row['source_record_index']==74:
            require(row['source_hex']==wrap['source_hex'] and row['english']==wrap['english'] and row['qa_waiver_reason']==wrap['reason']
                and qa['visible_lines']==row['exact_reviewed_soft_wrap_rows']==wrap['visible_rows'] and row.get('qa_waivers')==['weak-line-ending']
                and [i['code'] for i in qa['issues']]==['weak-line-ending'],'exact R74 ordinary soft wrap differs')
        else:
            require(row.get('qa_waivers') in [None,['line-break-count']],'waiver transferred outside exact record')
            require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),old=old,value=value));changes.append(dict(id=ident,block=197,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(not macros,'no source macros may be invented')
    require(not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'] and [c['old_offset'] for c in spec['choice_commands']]==MENUS,'typed object scope differs')
    for command in spec['choice_commands']:
        at=command['old_offset'];rs=sorted([r for r in labels if r['command_offset']==at],key=lambda r:r['option_index'])
        require(len(rs)==3 and [r['option_index'] for r in rs]==[0,1,2] and [r['id'] for r in rs]==command['record_IDs'],'menu index ownership differs')
        require(block[at:at+2]==original[at:at+2]==b'\0\x22' and command['count']==3,'menu source count differs')
        chunks=[];offsets=[];cursor=0
        for i,row in enumerate(rs):
            sa,ca=row['source_reference']['offset'],row['current_reference']['offset'];raw,old=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
            require(row['file_path']==PATH and row['block']==197 and row['native_display_consumer']=='original2200_three_option_modal51FC0','choice consumer differs')
            require(original[sa:sa+len(raw)]==raw and block[ca:ca+len(old)]==old and original[sa+len(raw)]==block[ca+len(old)]==0 and raw.decode('cp932')==['買おう','買わない','任せる'][i]
                and sa==at+8+struct.unpack_from('<H',original,at+2+i*2)[0] and ca==at+8+struct.unpack_from('<H',block,at+2+i*2)[0],'choice source pointer differs')
            value=row['english'].encode('ascii');require(value==[b"Let's buy it",b'Pass',b'You decide'][i] and row['editorial_decision']==['revise','retain-wording','revise'][i] and (i!=1 or row.get('fresh_retained_wording_justification')),'choice prose differs')
            offsets.append(cursor);chunk=value+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
            changes.append(dict(id=row['id'],block=197,kind='typed-choice-label',old_offset=ca,new_offset=command['label_references'][i]['new_offset'],old_bytes=len(old),new_bytes=len(value)))
        for i,row in enumerate(rs):
            ref=command['label_references'][i]
            require(ref['id']==row['id'] and ref['option_index']==i and ref['new_offset']==command['new_offset']+8+offsets[i]
                and ref['new_length']==len(row['english']) and row['compiled_hex']==command['target_hex'],'complete typed label metadata differs')
            require(row['source_reference']['bytes']==len(bytes.fromhex(row['source_hex'])) and row['current_reference']['bytes']==len(bytes.fromhex(row['current_hex'])),'source/current choice byte extent differs')
        value=struct.pack('<4H',0x2200,*offsets)+b''.join(chunks)
        require(command['old_length']==34 and command['new_length']==len(value)==40 and command['target_hex']==value.hex() and all(r['typed_target_object_hex']==value.hex() for r in rs),'whole menu object differs')
        patches.append(dict(start=at,end=at+command['old_length'],old=block[at:at+command['old_length']],value=value))
    patches.sort(key=lambda p:p['start']);require(len(patches)==22 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping text/menu ownership')
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            require(not p['start']<at<p['end'],'unclassified interior reference')
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==878 and block[end:]==bytes(2),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));edges=spec['relative_skip_fixups']
    require(len(edges)==6 and len(spec['target_native_skip_cases'])==30 and len(logical)==mapped(end)==1002,'relative scope differs')
    for e in edges:
        a,target=mapped(e['offset']),mapped(e['matched_skip_target']);span=target-a-4
        require(a==e['new_offset'] and target==e['new_matched_skip_target'] and mapped(e['unmatched_next_offset'])==e['new_unmatched_next'] and span==e['target_span']
            and e['span_field_offset']==e['offset']+2 and e['matched_skip_target']==e['offset']+4+e['source_span']
            and struct.unpack_from('<H',block,e['span_field_offset'])[0]==e['source_span'] and 0<=span<=65535 and span%2==0,'relative target differs')
        struct.pack_into('<H',logical,a+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(sha(target)==spec['target_block_sha256'] and len(target)==1004,'target block differs')
    commands=spec['mapped_native_commands'];counts=Counter(c['word'] for c in commands)
    require(counts==Counter({0x4000:21,0x2200:1,0xA000:5,0x4821:1,0x4720:1,0x4735:1,0x632E:1,0x6003:1,0:1,0x100:3,0x200:1,0x300:1,0x400:1}),'complete command scope differs')
    boundaries={c['new_offset'] for c in commands};require(all(e['new_matched_skip_target'] in boundaries and e['new_unmatched_next'] in boundaries for e in edges),'relative destination leaves commands')
    leaves=[]
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'mapped command boundary differs')
        require(struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0]==c['word'],'command opcode differs')
        require(c['target_0100_ancestors']==[mapped(p) for p in c['source_0100_ancestors']],'nested ancestor differs')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'full speech preamble differs')
        elif c['word'] not in [0x100,0x200,0x300,0x400,0x2200]:
            require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
            leaves.append((c['word'],a,b,block[a:a+c['old_native_extent']].hex()))
    require(leaves==[(r['word'],r['old_offset'],r['new_offset'],r['source_current_target_hex']) for r in control['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves']],'all11 original opaque leaves required')
    stops=[c for c in commands if c['word']==0];require([(c['old_offset'],c['new_offset']) for c in stops]==END_MAP and stops[-1]['new_offset']+4==len(logical),'single common end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    for r in spec['text_records']:
        require(target[r['new_offset']:r['new_offset']+r['new_length']].hex()==r['target_hex'] and target[:r['new_offset']].count(b'\0')==r['new_record_index'],'final speech index differs')
    for c in spec['choice_commands']:
        for r in c['label_references']:require(target[:r['new_offset']].count(b'\0')==r['new_record_index'],'final label record index differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for e in edges:struct.pack_into('<H',restored,e['new_offset']+2,e['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse must restore every880 predecessor byte')
    newblocks=list(oldblocks);newblocks[197]=target;result=IlnkContainer(newblocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(oldblocks,newblocks,strict=True)) if a!=b]==[197],'whole SC2 target differs')
    # All approval,metadata,prose,control and inverse checks precede this sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=conf['manuscript'],choices=conf['choices'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=197,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=6,source_commands=39,inverse_restores_every_original_logical_and_stored_byte=True)],
        all335_other_SC2_blocks_unchanged=True,all24_reviewed_objects_three_labels_common_end_no_macros_and11_leaves_preserved=True,
        actual21_speech_panels35_observations_three_options_common_end_not_natural_event_eligibility=True,native_code_and123040_staged_payload_unchanged=True)
