"""Atomic B205 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B205_layout_v2 as codec
from dk4tool.dialogue.lil_B205_profile_v2 import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B205_editorial_release_v1.json'
SELECTORS={2,15,254}
FLAGS=['all25_commands17_preambles8_leaves_complete_no_relative_or_menu', 'all620_predecessor_bytes_inverse_source620_target580_logical578_target_tail2', 'all17_actual_panels63_complete_native_holds_five_echoes_two_sounds', 'two_source_actors_voices10_progressive7_FE_no_FI_FA_FO_preserved', 'five_word_exact_echo_pairs_and_complete_capture_joke_preserved', 'Rainbow_Parrot_item_card_and7150_acquired_notice_retained_without_duplicate_credit', 'same_current_ARM9_COMMON_all_components_and_ordinary_inputs_source_baseline_bound', 'all34_command_timings_and_interval_RNG_equal_98_later_whole_RGB_samples_equal', 'queried_native_groups_actor_and_PRNG_equal_no_broad_world_equivalence', 'representative_shared_rules_approved_natural_activation_original_location_full_effects_and_hardware_unclaimed']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B205 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B205-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all17_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'] and seal['all_measured_timing_RNG_state_and_RGB_scopes_preserved'] and seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed references differ')
    require(mapping['format']=='dk4-lil-B205-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source-bound map required')
    require(conf['required_map_flags']==FLAGS,'complete map flag list required')
    for flag in FLAGS:require(mapping.get(flag) is True,'map approval required:'+flag)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof','source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','actual_proof','actor_terminology_reconciliation','contextual_reconciliation','actor_voice_contract']
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B205_layout_v2.py') and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B205_profile_v2.py'),'exact formatter/profile required')
    from dk4tool.patch.lil_B205_editorial_guards_v1 import validate
    native,stored,controls,sample,ends,names,fields,terms,voices,state,approval,actual,rows,ids,spec,old_blocks,block,original=validate(doc,mapping,seal,conf,source,arm,japanese)
    fonts={c['id']:c for c in native['cases']};refs={r['id']:r for r in spec['text_records']}
    require(set(fonts)==set(refs)==set(ids),'native/reference coverage differs')
    require({c['id'] for c in controls['relocated_dispatch_cases']}==set(ids)
        and all(c['resolved_actor_ID']==(None if c['source_selector']==254 else c['source_selector']) and c['registered_catalog_match'] is None
            for c in controls['relocated_dispatch_cases']),'individual dispatch scope differs')
    patches=[];changes=[];macros=Counter()
    for row in rows:
        ident=row['id'];case,ref=fonts[ident],refs[ident];fe=row['kind']=='system-FE'
        require(row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked']
            and not row['current_native_UI_body_explicit_unexecuted_boundary'],'individual actual scope differs')
        require(case['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal']
            and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and_within_four_rows']
            and case['one_native_page_consumes_complete_target'] and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete native plane differs:'+ident)
        if fe:require(all(c['null_source_actor'] for p in case['current_native_macro_pipelines'] for c in p['cases']),'FE null actor differs')
        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5 and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'complete source/current reference metadata differs:'+ident)
        require(row['source_reference']['block']==205 and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0') and row['current_record_index']==block[:at].count(b'\0'),'complete source/current record identity differs:'+ident)
        require(row['block']==205 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
            and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}') and (raw[0]==254)==fe,'source selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0
            and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1]
            and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'complete preamble differs:'+ident)
        require(block[:at].count(b'\0')==row['record_index']==ref['record_index'] and ref['old_offset']==at and ref['old_length']==len(old)
            and row['native_display_consumer']==('original_null_actor_FE_24310_then5473C' if fe else 'original_progressive_54020'),'current reference differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])]
        require(sm==tm,'source substitution/order differs:'+ident);macros.update(sm)
        profile=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning'
            and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        require(not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries'),'unapproved inherited boundary exception')
        require(row.get('qa_waivers') in [None,['line-break-count']],'no additional safety waiver')
        require(row['native_font_case']==case,'approved native reference differs:'+ident)
        effective=old[1:]
        require(row.get('registered_runtime_catalog_entry',row['previous_registered_catalog_entry']) is None,'no current B205 runtime override belongs here')
        old_prose=' '.join(effective.decode('cp932').split())
        logical_prose=row['english'].split('}',1)[1]
        for macro in ['FI','FA','FO']:logical_prose=logical_prose.replace('{MACRO:'+macro+'}',macro)
        require(row['effective_predecessor_paragraph']==old_prose,'effective predecessor differs:'+ident)
        require((logical_prose!=old_prose)==(row['editorial_decision']=='revise'),'revision/retention decision differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row.get('fresh_retained_wording_justification'),'individual retention reason required')
        require(not logical_prose.startswith('(') and not logical_prose.endswith(')'),'no private thought objects belong to B205')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=205,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(macros==Counter(),'B205 requires no original FI/FA/FO')
    require(not spec['choice_commands'] and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps']
        and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases'],'invented control object')
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping text objects')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'interior text reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-(p['end']-p['start'])
        return offset+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==620 and len(block)==620 and block[end:]==bytes(0),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==578,'target logical extent differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==580 and len(logical)==578 and sha(target)==spec['target_block_sha256'],'target block differs')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\0')==ref['new_record_index'],
            'relocated record offset/index differs:'+change['id'])
    commands=spec['mapped_native_commands'];require(len(commands)==25 and sum(c['word']==0x4000 for c in commands)==17,'command scope differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset']
        require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0],'opcode differs')
        require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command boundary differs')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'invented ancestor')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([(c['old_offset'],c['new_offset']) for c in stops]==[(616,574)] and stops[-1]['new_offset']+4==len(logical),'single source tail endword required')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word']!=0x4000]
    exact=[(32,'414893a8'),(346,'0c63'),(348,'2d63'),(590,'00a0ffff010d0260'),(598,'2147'),(600,'00a0ffff010d0f60'),(608,'00a0ffff01009330'),(616,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'8 exact leaves required')
    require([c['word'] for c in leaves]==[0x4841,0x630C,0x632D,0xA000,0x4721,0xA000,0xA000,0],'numeric leaf scope differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse does not restore every predecessor byte')
    new_blocks=list(old_blocks);new_blocks[205]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[205],'whole SC2 target differs')
    # Every check above is read-only. This is the sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=205,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=0,
            source_commands=25,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,
        all10_progressive_seven_FE_echoes_sounds_two63xx_picture47xx_three_A000_and_single_end_preserved=True,
        actual_two_complete_same_code_scopes17_panels63_holds_timing_RNG98_later_RGB_matches_not_natural_activation=True,native_code_and123264_staged_payload_unchanged=True)
