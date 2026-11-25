"""Atomic source-bound B196 speech, six-menu and seven-ending integration."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B196_layout_v3 as codec
from dk4tool.dialogue.lil_B196_profile_v2 import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B196_editorial_release_v1.json'
SELECTORS={2,6,19,20,25,173,254}
MENUS=[218,582,832,1156,1370,1588]
END_MAP=[(364,316),(694,624),(938,838),(1266,1144),(1464,1334),(1708,1560),(1810,1664)]

def load(path):return json.loads(Path(path).read_bytes())
def require(value,message):
    if not value:raise ValueError('Lil B196 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B196-editorial-release-v1','unknown release format')
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
    require(seal['all36_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_unchanged'],'source/reference approval required')
    require(seal['manuscripts']=={conf[k]:sha(Path(conf[k]).read_bytes()) for k in ['manuscript','choices']},'sealed manuscript changed')
    require(seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed reference map changed')
    require(mapping['format']=='dk4-lil-B196-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8
        and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    for name in conf['required_map_flags']:require(mapping.get(name) is True,'required source shape:'+name)
    proofs={k:load(doc[k]) for k in ['native_font_proof','final_padding_proof','final_choice_proof','relocated_control_proof','termination_decode_proof','representative_proof','postscene_native_state_proof','source_bound_wrap_retention_proof']}
    native,stored,typed,control,ends,sample,observed,wrap=[proofs[k] for k in proofs]
    approval=load(conf['native_approval']);actual=load(observed['actual_proof'])
    require(len(native['cases'])==24 and native['current_original_macro_alignment_calls']==192 and native['complete_progressive_planes']==23
        and native['complete_FE_logical_and_physical_planes']==1 and len(native['negative_controls'])==30,'complete native consumers/negatives required')
    require(all(r['rejected'] for r in native['negative_controls']) and len(approval['formatter_negatives'])==28,'formatter/consumer negatives required')
    require(len(stored['final_target_parity_cases'])==24 and stored['current_final_stored_macro_alignment_cases']==96
        and stored['new_parity_macro_alignment_cases']==40 and stored['exact_byte_identical_reused_macro_alignment_cases']==56
        and stored['all24_final_targets_complete_native_planes_equal_reviewed_planes'],'stored speech proof required')
    require(typed['all_six_stored_objects_and_twelve_actual_offsets_record_indices_labels_and_counts_exact']
        and typed['fresh_count_calls']==12 and typed['fresh_label_pointer_calls']==24 and typed['reused_native_selection_cancel_cases']==36
        and typed['reused_complete_current_reviewed_style_planes']==48,'stored menu proof required')
    require(len(control['relocated_dispatch_cases'])==24 and len(control['all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==37
        and len(control['relocated_unforced_predicates'])==7 and len(control['relocated_picture_boundaries'])==len(control['relocated_menu_getters'])==6,'relocated controls required')
    require(ends['all14_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==14
        and ends['no_relative_destination_at_or_beyond_logical_end'],'all seven guarded endings required')
    require(sample['actual_buy_menu_offsets']==[218,1588] and sample['actual_pass_menu_offsets']==MENUS
        and sample['all_six_label_pairs_seen_and_native_order_bound_but_not_all_six_Buy_outcomes_played'],'honest representative menu scope required')
    require(observed['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not observed['visual_review_pending']
        and observed['no_open_translation_specific_display_menu_control_or_return_finding']
        and observed['actual_new_cold_boot_runs']==6 and observed['total_frames']==78006,'viewed actual approval required')
    require(not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_timing_differences'] and not actual['later_whole_RGB_differences'],'measured actual differences changed')
    require(len(actual['actual_panels'])==13 and len(actual['all_actual_speech_observations'])==24 and len(actual['actual_menu_cases'])==13,'actual scope differs')
    views=observed['all_actual_consumer_menu_sheets_viewed']+observed['paired_full_screen_views']+[observed['first_buy_postscene_view']]
    require(len(views)==9 and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views),'viewed screens changed')
    require(all(all(p['five_native_component_equality'].values()) and p['whole1A04_actor_and_captain2_equal'] and p['PRNG_equal'] for p in observed['paired_final_state_measurements']),'scoped final-state comparison changed')
    terms=load(doc['actor_terminology_reconciliation']);funds=load(doc['source_financial_context'])
    require(terms['money_term']=='gold' and terms['stat_term']['English']=='Charm' and terms['current_source_FI_expansion']=='Lil','source terms differ')
    require(terms['approved_prose_names']=={'2':'Lil Argot','6':'Julio Erneco','19':'Carlo Sinat','20':'Fernando Dias','25':'Yifa Sol','173':'Suspicious Person'},'approved prose names differ')
    for flag in conf['required_term_flags']:require(terms.get(flag) is True,'source context required:'+flag)
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh6_actor_names']['rows']}=={2:3,6:5,19:7,20:4,25:3,173:0},'six source voices differ')
    require(funds['six_source_prices_match_six_exact_native_payment_amounts'] and len(funds['cases'])==36,'six price contracts required')
    require(wrap['all24_words_source_controls_compiled_bytes_and_native_planes_unchanged'] and (wrap['paragraph_ASCII_characters'],wrap['paragraph_words'])==(129,23)
        and len(wrap['six_source_or_prose_changes_do_not_inherit_review'])==6,'exact R74 wrap proof required')
    rows,labels=doc['records'],menu['records'];ids={r['id'] for r in rows};label_ids={r['id'] for r in labels}
    require(len(rows)==len(ids)==24 and len(labels)==len(label_ids)==12 and not ids&label_ids,'36 unique objects required')
    require({r['source_selector'] for r in rows}==SELECTORS and Counter(r['kind'] for r in rows)=={'progressive':23,'system-FE':1},'speaker/consumer scope differs')
    require(Counter(r['editorial_decision'] for r in rows+labels)=={'revise':15,'retain-wording':21}
        and all(r.get('fresh_retained_wording_justification') for r in rows+labels if r['editorial_decision']=='retain-wording'),'individual decisions required')
    observed_ids=set(mapping['actual_sampled_display_IDs']);offline=set(mapping['offline_only_display_IDs'])
    require(len(observed_ids)==13 and len(offline)==11 and not observed_ids&offline and observed_ids|offline==ids
        and observed_ids=={r['id'] for r in actual['actual_panels']} and offline==set(actual['offline_only_display_IDs']),'actual/offline ownership differs')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==196,'one exact block required');spec=mapping['blocks'][0]
    oldblocks=list(IlnkContainer.parse(source).blocks);block=oldblocks[196];original=IlnkContainer.parse(japanese).blocks[196]
    require(len(oldblocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'])==(1816,1814,1668,1668) and len(block)==1816,'source/target extent metadata differs')
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
        require(row['block']==row['source_reference']['block']==196 and row['file_path']==PATH and row['source_record_index']==original[:sa].count(b'\0')
            and row['current_record_index']==row['record_index']==block[:at].count(b'\0'),'record identity differs:'+ident)
        require(row['source_selector']==raw[0]==old[0] and raw[0] in SELECTORS and (raw[0]==254)==fe and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}'),'selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0 and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'full preamble differs:'+ident)
        require(ref['record_index']==row['record_index'] and ref['old_offset']==at and ref['old_length']==len(old),'relocation owner differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode() for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])];require(sm==tm,'substitution order differs:'+ident);macros.update(sm)
        p=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        require(qa.get('reviewed_ordinary_boundaries',[])==row.get('reviewed_ordinary_boundaries',[]),'ordinary boundary approval differs:'+ident)
        if row['source_record_index']==74:require(row['english']==wrap['exact_target'] and row['compiled_hex']==wrap['retained_compiled_hex'] and row['reviewed_ordinary_boundaries']==wrap['exact_source_prose_boundaries'],'exact R74 approval differs')
        else:require(not qa.get('reviewed_ordinary_boundaries'),'unexpected ordinary boundary exception')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),old=old,value=value));changes.append(dict(id=ident,block=196,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(macros=={b'FI':1},'exact one FI required')
    require(not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'] and [c['old_offset'] for c in spec['choice_commands']]==MENUS,'typed object scope differs')
    for command in spec['choice_commands']:
        at=command['old_offset'];rs=sorted([r for r in labels if r['command_offset']==at],key=lambda r:r['option_index'])
        require(len(rs)==2 and [r['option_index'] for r in rs]==[0,1] and [r['id'] for r in rs]==command['record_IDs'],'menu index ownership differs')
        require(block[at:at+2]==original[at:at+2]==b'\0\x21' and command['count']==2,'menu source count differs')
        chunks=[];offsets=[];cursor=0
        for i,row in enumerate(rs):
            sa,ca=row['source_reference']['offset'],row['current_reference']['offset'];raw,old=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
            require(row['file_path']==PATH and row['block']==196 and row['native_display_consumer']=='original2100_two_option_modal51FC0','choice consumer differs')
            require(original[sa:sa+len(raw)]==raw and block[ca:ca+len(old)]==old and original[sa+len(raw)]==block[ca+len(old)]==0 and raw.decode('cp932')==['買う','買わない'][i]
                and sa==at+6+struct.unpack_from('<H',original,at+2+i*2)[0] and ca==at+6+struct.unpack_from('<H',block,at+2+i*2)[0],'choice source pointer differs')
            value=row['english'].encode('ascii');require(value==[b'Buy',b'Pass'][i] and row['editorial_decision']=='retain-wording' and row.get('fresh_retained_wording_justification'),'choice prose differs')
            offsets.append(cursor);chunk=value+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
            changes.append(dict(id=row['id'],block=196,kind='typed-choice-label',old_offset=ca,new_offset=command['label_references'][i]['new_offset'],old_bytes=len(old),new_bytes=len(value)))
        value=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
        require(command['old_length']==22 and command['new_length']==len(value)==16 and command['target_hex']==value.hex() and all(r['typed_target_object_hex']==value.hex() for r in rs),'whole menu object differs')
        patches.append(dict(start=at,end=at+command['old_length'],old=block[at:at+command['old_length']],value=value))
    patches.sort(key=lambda p:p['start']);require(len(patches)==30 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping text/menu ownership')
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            require(not p['start']<at<p['end'],'unclassified interior reference')
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==1814 and block[end:]==bytes(2),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));edges=spec['relative_skip_fixups']
    require(len(edges)==52 and len(spec['target_native_skip_cases'])==260 and len(logical)==mapped(end)==1668,'relative scope differs')
    for e in edges:
        a,target=mapped(e['offset']),mapped(e['matched_skip_target']);span=target-a-4
        require(a==e['new_offset'] and target==e['new_matched_skip_target'] and mapped(e['unmatched_next_offset'])==e['new_unmatched_next'] and span==e['target_span']
            and e['span_field_offset']==e['offset']+2 and e['matched_skip_target']==e['offset']+4+e['source_span']
            and struct.unpack_from('<H',block,e['span_field_offset'])[0]==e['source_span'] and 0<=span<=65535 and span%2==0,'relative target differs')
        struct.pack_into('<H',logical,a+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(sha(target)==spec['target_block_sha256'] and len(target)==1668,'target block differs')
    commands=spec['mapped_native_commands'];counts=Counter(c['word'] for c in commands)
    require(len(commands)==119 and counts[0x4000]==24 and counts[0x2100]==6 and counts[0x8000]==7 and counts[0xA000]==14 and counts[0x4821]==6
        and counts[0x632E]==counts[0x6302]==counts[0x6003]==1 and counts[0]==7 and sum(counts[w] for w in [0x100,0x200,0x300,0x400])==52,'complete command scope differs')
    boundaries={c['new_offset'] for c in commands};require(all(e['new_matched_skip_target'] in boundaries and e['new_unmatched_next'] in boundaries for e in edges),'relative destination leaves commands')
    leaves=[]
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'mapped command boundary differs')
        require(struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0]==c['word'],'command opcode differs')
        require(c['target_0100_ancestors']==[mapped(p) for p in c['source_0100_ancestors']],'nested ancestor differs')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'full speech preamble differs')
        elif c['word'] not in [0x100,0x200,0x300,0x400,0x2100]:
            require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
            leaves.append((c['word'],a,b,block[a:a+c['old_native_extent']].hex()))
    require(leaves==[(r['word'],r['old_offset'],r['new_offset'],r['source_current_target_hex']) for r in control['all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves']],'all37 original opaque leaves required')
    stops=[c for c in commands if c['word']==0];require([(c['old_offset'],c['new_offset']) for c in stops]==END_MAP and stops[-1]['new_offset']+4==len(logical),'seven separate ends differ')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    for r in spec['text_records']:
        require(target[r['new_offset']:r['new_offset']+r['new_length']].hex()==r['target_hex'] and target[:r['new_offset']].count(b'\0')==r['new_record_index'],'final speech index differs')
    for c in spec['choice_commands']:
        for r in c['label_references']:require(target[:r['new_offset']].count(b'\0')==r['new_record_index'],'final label record index differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for e in edges:struct.pack_into('<H',restored,e['new_offset']+2,e['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse must restore every1816 predecessor byte')
    newblocks=list(oldblocks);newblocks[196]=target;result=IlnkContainer(newblocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(oldblocks,newblocks,strict=True)) if a!=b]==[196],'whole SC2 target differs')
    # All approval,metadata,prose,control and inverse checks precede this sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=conf['manuscript'],choices=conf['choices'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=196,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=52,source_commands=119,inverse_restores_every_original_logical_and_stored_byte=True)],
        all335_other_SC2_blocks_unchanged=True,all36_reviewed_objects_six_menus_seven_ends_FI_and37_leaves_preserved=True,
        actual13_speech_panels11_offline_only_speeches13_menu_cases_three_endings_not_natural_event_eligibility=True,native_code_and123040_staged_payload_unchanged=True)
