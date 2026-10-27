"""Atomic B175 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B175_layout_v1 as codec
from dk4tool.dialogue.lil_B175_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B175_editorial_release_v1.json'
SELECTORS={2,9,183,184,185,254}
FLAGS=['all39_structural_commands_verified','all32_active_speech_targets_preserved',
    'all7_leaves_three_presentations_resource_C200_and_both_ends_exact','both_declared_endwords_preserved',
    'progressive23_FE9_and_FI4_FA1_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause',
    'no_source_relative_sites_predicates_or_A000','first_end1702_actual_second_end1706_offline','representative_shared_rules_approved']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B175 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B175-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping=load(conf['manuscript']),load(conf['reference_map']);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and doc['formatting_review_pending'] is False and doc['all32_five_review_gates_true'],'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(doc['reference_map']).read_bytes()),'approved map differs')
    require(mapping['format']=='dk4-lil-B175-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source map required')
    for flag in FLAGS:require(mapping.get(flag) is True,'missing map approval:'+flag)
    proof_keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof']
    for key in proof_keys:require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'proof differs:'+key)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B175_layout_v1.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B175_profile.py'),'scoped formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(len(native['cases'])==32 and native['current_original_macro_alignment_calls']==256
        and native['all32_current_native_speech_planes_pass'] and (native['progressive_planes'],native['FE_planes'])==(23,9),'complete native consumers required')
    for key,count in [('source_bound_formatter_negatives',28),('source_consumer_negative_controls',24),('source_macro_preservation_negatives',9)]:
        require(len(native[key])==count and all(c['rejected'] for c in native[key]),'native negative controls differ:'+key)
    require(len(stored['final_target_parity_cases'])==32 and stored['current_final_stored_macro_alignment_cases']==128
        and stored['new_parity_macro_alignment_cases']==68 and stored['exact_byte_identical_reused_macro_alignment_cases']==60
        and stored['all32_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==32 and len(controls['all7_source_current_target_nonrelative_nonspeech_leaves'])==7
        and len(controls['relocated_C200_pairs'])==1 and controls['all23_progressive_actors9_null_actor_FE_and_FI4_FA1_macro_expansions_exact']
        and controls['source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime']
        and controls['source_three_presentation_structures_reused_only_by_exact_whole_commands_and_runtime']
        and controls['original_no_relative_predicate_A000_pause_or_typed_objects_preserved']
        and controls['second_end_preserved_but_actual_reachability_pending'] and controls['source_presentation_operand_semantics_not_inferred'],'relocated consumer/control scope required')
    ui=controls['relocated_C200_pairs'][0]
    require(ui['source_offset']==1700 and ui['target_offset']==1688 and len(ui['cases'])==2
        and all(c['native_result']==[3,0,0,0,0,0] and c['native_extent']==2 and c['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            and len(c['source_owned_UI_writes'])==9 and c['all_other4MiB_actor_roster_event_RNG_and_models_exact']
            and c['original_input_owner_guards_and_ABI_exact'] for c in ui['cases'])
        and ui['cases'][0]['source_owned_UI_writes']==ui['cases'][1]['source_owned_UI_writes'],'C200 ownership differs')
    require(ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==4
        and ends['B175_second_end_finishes_declared_logical_end'],'four guarded endword decodes required')
    require([(c['version'],c['end_offset']) for c in ends['cases']]==[('current',1702),('current',1706),('research',1690),('research',1694)]
        and all(c['native_result']==[0]*6 and c['native_extent']==4 and not c['post_logical_payload_reads'] for c in ends['cases']),'endword cases differ')
    require(names['approved_prose_names']=={'2':'Lil','9':'Camille','183':'Angel','184':'Snake','185':'Dandy'}
        and names['progressive_nameplate_values']=={'2':'Lil Argot','9':'Camille Overijssel','183':'Angel','184':'Snake','185':'Dandy'}
        and names['full_catalogue_values']['9']=='Camille Marinus Overijssel','source-bound names differ')
    namecases=names['native_ten_consumer_cases']['rows']
    require(len(namecases)==10 and {r['actor_ID'] for r in namecases}==SELECTORS-{254}
        and all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in namecases),'ten native name consumers required')
    owned=[r for r in namecases if r['actor_ID'] in [2,9]];readonly=[r for r in namecases if r['actor_ID'] in [183,184,185]]
    require(len(owned)==4 and all(r['original_scratch_rings'] and r['original_getter_writes'] for r in owned),'four owned name paths required')
    require(len(readonly)==6 and all(r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring'
        and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in readonly),'six read-only names required')
    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['content_frames_each']==16001 and sample['new_emulator_runs']==2
        and sample['all32_panels23_progressive9_FE_three_presentations_resource_C200_first_end_and_normal_town_return_pass']
        and sample['original39_commands_and_both_declared_endwords_preserved'] and sample['no_B175_source_command_omitted']
        and sample['first_end1702_actual_second_end1706_offline_native_only'] and sample['original_B22_four_A000_initialization_commands_retained']
        and sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_B175_source_events']==[]
        and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all32_complete_held_planes_and_source_paired_regions_match'] and observed['all32_speeches23_progressive9_FE_actually_observed']
        and len(observed['all232_sampled_nontext_region_checks'])==232 and observed['nontext_equal_samples']==218
        and len(observed['nontext_difference_samples'])==14 and observed['two_original_presentation_transition_differences_at_equal_duration_one_frame_offset']
        and observed['twelve_following_sailing_foreground_cloud_differences_bounded_and_unmasked']
        and observed['whole_RGB_town10570_through10870_equal'] and observed['final16001_whole_RGB_equality_not_claimed']
        and all(observed['postscene16001_native_component_equality'].values()) and observed['postscene16001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality_causal_trace_and_future_world_equivalence_not_claimed'] and observed['all_content_jobs_terminal'],'actual planes/state and explicit differences required')
    require(observed['exact_timing_difference_counts']==dict(total=30,speech=26,control_or_end=4),'exact command timing scope required')
    require(observed['source_C2001700_and_first_end1702_actually_reached'] and observed['second_declared_end1706_offline_native_only'],'actual/offline end scope required')
    actual_paths=[p for p in sample['evidence'] if p.endswith('actual_all32_progressive_FE_controls_C200_and_first_end.json')]
    require(len(actual_paths)==1,'one exact actual proof required');actual=load(actual_paths[0])
    require(sha(Path(actual_paths[0]).read_bytes())==sample['evidence'][actual_paths[0]] and not actual['failures'] and not actual['paired_region_differences']
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==32 and actual['offline_only_display_IDs']==[]
        and len(actual['versions'])==2 and actual['frames_per_boot']==16001 and actual['actual_new_cold_boot_runs']==2,'two complete actual paths required')
    require([v['fixture_exit_frame'] for v in actual['versions']]==[10534,10535],'observed exits differ')
    for version in actual['versions']:
        require(len(version['selected_B22_command_pairs'])==47 and len(version['selected_intervals'])==32
            and sum(r['prefix']==254 for r in version['selected_intervals'])==9 and version['first_source_end1702_actually_reached']
            and version['second_source_end1706_stored_but_unvisited_offline_decoder_only']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0] and version['selected_B22_command_pairs'][-1]['original_source_offset']==1702
            and version['source_C200']['original_source_offset']==1700 and version['source_C200']['result_words']==[3,0]
            and [r['word'] for r in version['source_three_presentations']]==[0x6000,0x4696,0x4635]
            and [r['word'] for r in version['source_resource']]==[0x6344],'actual source command scope differs')
    require(len(native['review_sheets'])==4 and len(sample['viewed_actual_sheets'])==6,'all viewed sheets required')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require((sheet.get('viewed') is True or sheet.get('viewed_in_full_current_turn') is True)
            and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet differs')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==32 and {r['source_selector'] for r in rows}==SELECTORS,'32 exact records required')
    require(Counter(r['kind'] for r in rows)=={'progressive':23,'system-FE':9}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':19,'retain-wording':13},'consumer/decision scope differs')
    require(sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids
        and all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']),'actual display keys differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==175,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[175],IlnkContainer.parse(japanese).blocks[175]
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
        require(row['block']==175 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
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
        changes.append(dict(id=ident,block=175,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(macros=={b'FI':4,b'FA':1},'complete macro scope differs')
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
    end=8+struct.unpack_from('<H',block,4)[0];require(end==1710 and len(block)==1712 and not any(block[end:]),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==1698,'target logical extent differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==1700 and sha(target)==spec['target_block_sha256'],'target block differs')
    commands=spec['mapped_native_commands'];require(len(commands)==39 and sum(c['word']==0x4000 for c in commands)==32,'command scope differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset']
        require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0],'opcode differs')
        require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command boundary differs')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'invented ancestor')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([(c['old_offset'],c['new_offset']) for c in stops]==[(1702,1690),(1706,1694)] and stops[-1]['new_offset']+4==len(logical),'both source endwords required')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word']!=0x4000]
    exact=[(8,'0060'),(10,'4463'),(72,'9646ca80'),(1264,'35467d80'),(1700,'00c2'),(1702,'00000000'),(1706,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'seven exact leaves required')
    require([c['word'] for c in leaves]==[0x6000,0x6344,0x4696,0x4635,0xC200,0,0],'numeric leaf scope differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end],'inverse does not restore every predecessor logical byte')
    new_blocks=list(old_blocks);new_blocks[175]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[175],'whole SC2 target differs')
    # Every check above is read-only. This is the sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=175,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=0,
            source_commands=39,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,
        all32_progressive_FE_speeches_FI4_FA1_three_presentations_resource_C200_and_both_ends_preserved=True,
        actual_two_retained_B22_fixtures_and_scoped_visual_differences_not_natural_source_activation=True,native_code_and123040_staged_payload_unchanged=True)
