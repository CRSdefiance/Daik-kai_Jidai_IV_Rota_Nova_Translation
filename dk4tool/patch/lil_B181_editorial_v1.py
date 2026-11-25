"""Atomic B181 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B181_layout_v1 as codec
from dk4tool.dialogue.lil_B181_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B181_editorial_release_v1.json'
SELECTORS={166,167,168,254}
FLAGS=['all13_structural_commands_verified', 'all10_active_speech_targets_preserved', 'all3_leaves_one_A000_C200_and_single_end_exact', 'single_declared_tail_endword_preserved', 'progressive9_impersonal_FE1_and_FI0_FA0_FO0_preserved', 'no_source_relative_sites_predicates_pause_resources_presentations_or_typed_objects', 'source_A000_raw_operand_bytes_preserved_without_inferred_semantics', 'single_end392_actual_target376_offline', 'representative_shared_rules_approved']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B181 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B181-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping=load(conf['manuscript']),load(conf['reference_map']);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and doc['formatting_review_pending'] is False and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(doc['reference_map']).read_bytes()),'approved map differs')
    require(mapping['format']=='dk4-lil-B181-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source map required')
    for flag in FLAGS:require(mapping.get(flag) is True,'missing map approval:'+flag)
    proof_keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof']
    for key in proof_keys:require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'proof differs:'+key)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B181_layout_v1.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B181_profile.py'),'scoped formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(len(native['cases'])==10 and native['current_original_macro_alignment_calls']==80
        and native['complete_progressive_planes']==9 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==20 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28,'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==10 and stored['current_final_stored_macro_alignment_cases']==40
        and stored['new_parity_macro_alignment_cases']==12 and stored['exact_byte_identical_reused_macro_alignment_cases']==28
        and stored['all10_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==10 and len(controls['all3_source_current_target_nonrelative_nonspeech_leaves'])==3
        and len(controls['relocated_C200_pairs'])==len(controls['relocated_A000_structural_pairs'])==1,'complete relocated controls required')
    ui=controls['relocated_C200_pairs'][0]['cases']
    require(len(ui)==2 and all(r['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui)
        and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes'],'isolated C200 ownership differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',392),('research',376)],'guarded end decodes required')
    require(names['approved_prose_names']=={'166':'Lady','167':'Lady','168':'Lady'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_six_consumer_cases']['rows']}=={
            (c,i):'Lady' for i in [166,167,168] for c in ['progressive-nameplate','full-catalogue']},'six original role consumers required')
    require(sample['all10_panels9_progressive1_FE_A000_C200_end_and_normal_parent_return_pass']
        and sample['original13_commands_and_single_declared_tail_endword_preserved'] and sample['no_B181_source_command_omitted']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all10_complete_held_planes_and_source_paired_regions_match']
        and observed['all10_speeches9_progressive1_impersonal_FE_actually_observed']
        and observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_final9001_equal'],'all actual panels/regions required')
    require(observed['exact_timing_difference_counts']==dict(total=0,speech=0,control_or_end=0) and not observed['actual_timing_differences']
        and observed['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'],'measured state/timing scope differs')
    require(observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[790984746,790984746]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured equal RNG scope required')
    require(not observed['sampled_postscene_whole_RGB_differences_unmasked'] and observed['all_sampled_postscene_whole_RGB_equal'],'postscene RGB evidence differs')
    require(len(observed['all2_actual_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==3
        and all(s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all2_actual_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==10 and not actual['failures']
        and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'two complete actual paths required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[22,22]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[5257,5257],'actual linear source paths differ')
    for v in actual['versions']:
        require(len(v['selected_intervals'])==10 and v['single_source_end392_actually_reached']
            and v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and v['selected_B22_command_pairs'][-1]['original_source_offset']==392
            and len(v['source_A000'])==1 and v['source_A000'][0]['original_source_offset']==8
            and v['source_A000'][0]['word']==0xA000 and v['source_A000'][0]['extent']==8
            and v['source_C200']['original_source_offset']==390 and v['source_C200']['word']==0xC200
            and v['source_C200']['extent']==2 and v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1],'actual source controls differ')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets'],'native sheet approval differs')
    for s in approval['reviewed_sheets']:require(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'],'native sheet view differs')
    for s in sample['viewed_actual_sheets']:require(s['viewed'] and s['review'] and sha(Path(s['path']).read_bytes())==s['sha256'],'actual sheet view differs')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==10 and {r['source_selector'] for r in rows}==SELECTORS,'ten exact records required')
    require(Counter(r['kind'] for r in rows)=={'progressive':9,'system-FE':1}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':5},'consumer/decision scope differs')
    require(sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids
        and all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']),'actual display keys differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==181,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[181],IlnkContainer.parse(japanese).blocks[181]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
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
        require(row['block']==181 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
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
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification'],'unjustified retention')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=181,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(not macros,'source has no FI/FA/FO substitutions')
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
    end=8+struct.unpack_from('<H',block,4)[0];require(end==396 and len(block)==396 and not any(block[end:]),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==380,'target logical extent differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==380 and sha(target)==spec['target_block_sha256'],'target block differs')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\0')==ref['new_record_index'],
            'relocated record offset/index differs:'+change['id'])
    commands=spec['mapped_native_commands'];require(len(commands)==13 and sum(c['word']==0x4000 for c in commands)==10,'command scope differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset']
        require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0],'opcode differs')
        require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command boundary differs')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'invented ancestor')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([(c['old_offset'],c['new_offset']) for c in stops]==[(392,376)] and stops[-1]['new_offset']+4==len(logical),'single source tail endword required')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word']!=0x4000]
    exact=[(8,'00a0ffff014913a1'),(390,'00c2'),(392,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'three exact leaves required')
    require([c['word'] for c in leaves]==[0xA000,0xC200,0],'numeric leaf scope differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end],'inverse does not restore every predecessor logical byte')
    new_blocks=list(old_blocks);new_blocks[181]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[181],'whole SC2 target differs')
    # Every check above is read-only. This is the sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=181,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=0,
            source_commands=13,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,
        all10_progressive_FE_speeches_no_macros_A000_C200_and_single_end_preserved=True,
        actual_two_retained_B22_fixtures_115_regions_equal_zero_timing_or_RGB_differences_and_equal_PRNG_not_natural_activation=True,native_code_and123040_staged_payload_unchanged=True)
