"""Atomic24-record B208 progressive/thought/FE release; all validation precedes its sole mutation."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B208_layout_v5 as codec
from dk4tool.dialogue.lil_B208_profile_v1 import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.lil_B208_editorial_guards_v1 import validate_observations
PATH='/data/SC2.DK4'
CONFIG='translations/lil_B208_editorial_release_v2.json'
FLAGS=['all29_commands24_preambles_five_opaque_leaves_no_relative_menu_macro', 'all1188_predecessor_bytes_inverse_source1186_tail2_target1194_tail2', 'all24_actual_panels95_native_holds_thought_named_FE_and_town_sailing_return', 'Cristina_Erneco_Mysterious_Old_Man_contextual_name_retentions_style11_no_asset_change', 'same_current_ARM9_COMMON_all_components_and_ordinary_inputs_source_baseline_bound', 'all16_timing18_RNG44_broader_RGB_eight_duration_and_different_final_states_retained', 'state_tasks_equal_other_queried_groups_actor_calendar_and_PRNG_differ_no_world_equivalence', 'source_face_presence_conjecture_hearsay_limited_commitment_thought_and_Charm_plus1_preserved', 'proven_exact_phase_reservation_one_it_during_boundary_four_rowcount_reasons_no_blanket_waiver', 'natural_activation_original_location_earned_progress_full_effects_routes_hardware_unclaimed']
def load(p):return json.loads(Path(p).read_bytes())
def require(v,message):
    if not v:raise ValueError('Lil B208 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf.get('format')=='dk4-lil-B208-editorial-release-v2','release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical SC2')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean SC2')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']];validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'individual five-gate manuscript')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed map')
    require(seal['all24_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'] and seal['all_measured_timing_RNG_state_and_RGB_scopes_preserved'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'seal')
    require(mapping['format']=='dk4-lil-B208-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'source-bound map')
    require(mapping.keys()>=set(conf['required_map_flags']) and all(mapping[k] is True for k in conf['required_map_flags']),'all map approvals')
    require(conf['required_map_flags']==FLAGS,'complete flag contract')
    for k in ['native_font_proof','final_padding_proof','relocated_control_proof','loader_proof','source_census','termination_decode_proof','actual_proof','postscene_native_state_proof','representative_proof','native_approval','speaker_name_approval','scoped_profile_module','native_formatter_module','phase_capacity_proof']:
        require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash:'+k)
    require(Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B208_profile_v1.py') and Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B208_layout_v5.py'),'exact scoped formatter')
    proofs=validate_observations(doc,mapping,conf,load,require);rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==24 and Counter(r['editorial_decision'] for r in rows)=={'revise':15,'retain-wording':9} and Counter(r['source_selector'] for r in rows)=={7:12,170:11,254:1} and Counter(r['kind'] for r in rows)=={'progressive':23,'system-FE':1},'exact24 decisions/actors/consumers')
    require(doc['broader207_name_and_full_editorial_scope_remain_open'] and doc['existing88_Christina23_Cristina_individual_consumer_queue_remains_open'],'open name/alias scope')
    require(len(mapping['blocks'])==1,'one block');spec=mapping['blocks'][0];blocks=list(IlnkContainer.parse(source).blocks);block=blocks[208];original=IlnkContainer.parse(japanese).blocks[208]
    require(len(blocks)==336 and spec['block']==208 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'],spec['source_alignment_tail_bytes'],spec['target_alignment_tail_bytes'])==(1188,1186,1196,1194,2,2),'exact extents')
    commands=spec['mapped_native_commands'];require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in commands]==spec['command_map'],'independent command agreement')
    require(not any(spec[k] for k in ['choice_commands','actor_style_commands','original2000_pause_and_resume_maps','relative_skip_fixups','target_native_skip_cases']),'no invented controls')
    fonts={r['id']:r for r in proofs['native_font_proof']['cases']};refs={r['id']:r for r in spec['text_records']};stored={r['id']:r for r in proofs['final_padding_proof']['final_target_parity_cases']};dispatch={r['id']:r for r in proofs['relocated_control_proof']['relocated_dispatch_cases']}
    require(set(fonts)==set(refs)==set(stored)==set(dispatch)==set(ids),'complete individual proof sets')
    patches=[];changes=[];boundaries=0;rowcount=0
    for row in rows:
        ident=row['id'];case,ref,st,di=[d[ident] for d in [fonts,refs,stored,dispatch]];at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['block']==208 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0] and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}'),'selector:'+ident)
        for side,bank,offset,value,idx in [('source',original,sa,raw,row['source_record_index']),('current',block,at,old,row['current_record_index'])]:
            r=row[side+'_reference'];require((r['block']==208 and r['record_index']==idx if side=='source' else row['block']==208) and idx==bank[:offset].count(b'\0') and r['bytes']==len(value) and r['header_offset']==offset-5 and bank[offset:offset+len(value)]==value and bank[offset+len(value)]==0,'source/current reference:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'preamble:'+ident)
        require(row['record_index']==row['current_record_index']==ref['record_index'] and ref['old_offset']==at and ref['old_length']==len(old) and row['current_text_hex']==old.hex(),'current record:'+ident)
        require(not re.findall(rb'FI|FA|FO|FU',raw[1:]) and '{MACRO:' not in row['english'] and not any(t in row['english'] for t in ['{LB','{ALIGN','{PAD}']),'no authored controls/macros')
        profile=profile_for(arm,block,'FE-paper' if row['kind']=='system-FE' else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and row['native_font_case']==case,'compiled/native agreement:'+ident)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not (i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved layout:'+ident)
        require(row.get('qa_waivers') in [None,['line-break-count']],'no safety waiver');require(not row.get('qa_waivers') or bool(row.get('qa_waiver_reason')),'individual rowcount reason');rowcount+=bool(row.get('qa_waivers'))
        require(row.get('reviewed_ordinary_boundaries',[])==qa.get('reviewed_ordinary_boundaries',[]),'exact ordinary boundary');boundaries+=len(row.get('reviewed_ordinary_boundaries',[]))
        require(all(case[k] for k in ['complete_native_independent228x48_plane_equal' if row['kind']=='system-FE' else 'complete_native_independent216x64_plane_equal','all_first_final_internal_glyphs_in_order_and_unique_cells','all_visible_origins_zero_and_within_four_rows','one_native_page_consumes_complete_target']) and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete glyphs/bounds/page:'+ident)
        require(row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked'] and not row['current_native_UI_body_explicit_unexecuted_boundary'] and row['native_display_consumer']==('original_null_actor_FE_24310_then5473C' if row['kind']=='system-FE' else 'original_progressive_54020'),'individual actual scope')
        oldprose=' '.join(old[1:].decode('cp932').split());prose=row['english'].split('}',1)[1]
        require(row['effective_predecessor_paragraph']==oldprose and (prose!=oldprose)==(row['editorial_decision']=='revise'),'decision:'+ident)
        require(row['editorial_decision']!='retain-wording' or row.get('fresh_retained_wording_justification'),'retention reason')
        require(row['registered_runtime_catalog_entry'] is None and row['previous_registered_catalog_entry'] is None and di['registered_catalog_match'] is None and di['source_selector']==raw[0] and di['resolved_actor_ID']==(None if raw[0]==254 else raw[0]) and di['source_voice_class']==(None if raw[0]==254 else {7:3,170:0}[raw[0]]),'current catalogue/voice')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex']==st['stored_target_hex']==di['stored_target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added']==st['parity_space_added'] and st['complete_final_target_native_plane_equals_reviewed_plane'] and st['tail_padding_consumed_without_blank_page_or_lost_glyph'] and st['native_plane_sha256']==case['whole_native_plane_sha256'],'stored plane/parity:'+ident)
        require(len(st['current_final_target_macro_alignment_cases']['cases'])==4,'stored alignment')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old));changes.append(dict(id=ident,block=208,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(boundaries==1 and rowcount==4,'one exact boundary/four row reasons')
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlap')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'interior reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-(p['end']-p['start'])
        return offset+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==1186 and len(block)==1188 and block[end:]==bytes(2),'source end/tail')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==1194,'target logical extent');struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(sha(target)==spec['target_block_sha256'],'target hash')
    for c in changes:
        r=refs[c['id']];at=mapped(c['old_offset']);require(at==c['new_offset']==r['new_offset']==stored[c['id']]['stored_offset']==dispatch[c['id']]['new_offset'] and target[:at].count(b'\0')==r['new_record_index'],'integrated reference:'+c['id'])
    require(len(commands)==29 and sum(c['word']==0x4000 for c in commands)==24,'29 commands')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0] and mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command extent')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'no ancestors')
        require(block[a:a+(6 if c['word']==0x4000 else c['old_native_extent'])]==target[b:b+(6 if c['word']==0x4000 else c['new_native_extent'])],'opaque/preamble preservation')
    leaves=[c for c in commands if c['word']!=0x4000]
    require([(c['old_offset'],c['new_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==[(1118,1142,'0560'),(1120,1144,'2e63'),(1166,1174,'00a0ffff01020760'),(1174,1182,'00a0ffff28000110'),(1182,1190,'00000000')],'five exact leaves including6005,632E,two A000 and complete end')
    require([(c['old_offset'],c['new_offset'],4) for c in leaves if c['word']==0]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'declared end map')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)+block[end:]==block,'every1188 predecessor byte inverse')
    newblocks=list(blocks);newblocks[208]=target;result=IlnkContainer(newblocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(blocks,newblocks,strict=True)) if a!=b]==[208],'sole target block')
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],reference_map=conf['reference_map'],source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),changed_records=changes,blocks=[dict(block=208,source_bytes=1188,target_bytes=1196,source_logical_end=1186,target_logical_end=1194,relative_operands=0,source_commands=29,inverse_restores_every_original_stored_byte=True)],all335_other_SC2_blocks_unchanged=True,all23_progressive_one_FE_private_thought24_preambles_five_leaves_and_zero_macros_preserved=True,native_code_and123264_staged_payload_unchanged=True,actual24_panels95_holds_and_return_approved_with_measured_timing_RNG_broader_RGB_and_different_final_states=True,full_goal_complete=False)
