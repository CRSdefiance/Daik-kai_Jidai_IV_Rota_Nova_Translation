"""Atomic B200 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B200_layout_v2 as codec
from dk4tool.dialogue.lil_B200_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B200_editorial_release_v1.json'
SELECTORS={19,172,254}
FLAGS=['all31_source_commands_no2000_pause_verified', 'all19_source_targets_and12_control_leaves_preserved', 'seventeen_progressive_two_distinct_null_actor_FE_zero_macros_preserved', 'all932_predecessor_bytes_inverse_source_two_tailzeros_target_zero', 'all19_actual_panels73_holds_and_no_offline_only_scope', 'opaque_control_durations_and_results_preserved', 'eight_duration_changes19_shifted_pairs16_later_prompt_sky_and_PRNG_differences_explicit', 'queried_final_components_equal_no_future_world_equivalence_claim', 'representative_shared_rules_approved', 'Stranger_target_not_applied_no_global_name_completion_credit']
TERM_FLAGS=['actor19_Carlo_Sinat_existing_project_spelling_retained_from_clean_fields', 'explicit_not_a_doctor_denial_preserved', 'spoken_thankyou_object_stays_unnamed_no_new_item_title_widget_or_full_effect_fidelity_credit', 'source_portrait_name_absence_and_outdoor_inn_picture_and_stat_transitions_preserved', 'source_roster_funds_RNG_conditions_and_effect_results_unforced', 'initialized_Amsterdam_B22_fixture_not_natural_event200_activation_original_location_full_route_or_hardware']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B200 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B200-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all19_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged']
        and seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())
        and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed references differ')
    require(mapping['format']=='dk4-lil-B200-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    require(conf['required_map_flags']==FLAGS and conf['required_term_flags']==TERM_FLAGS,'complete required flags differ')
    for flag in FLAGS:require(mapping.get(flag) is True,'map approval required:'+flag)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','source_bound_wrap_retention_proof']
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B200_layout_v2.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B200_profile.py'),'exact formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in keys[:6]]
    state=load(doc['postscene_native_state_proof']);actual=load(sample['actual_proof']);approval=load(conf['native_approval'])
    require(len(native['cases'])==19 and native['current_original_macro_alignment_calls']==152 and native['complete_progressive_planes']==17
        and native['complete_FE_logical_and_physical_planes']==2 and len(native['negative_controls'])==18
        and all(r['rejected'] for r in native['negative_controls']),'complete native consumers required')
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28,'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==19 and stored['current_final_stored_macro_alignment_cases']==76
        and stored['new_parity_macro_alignment_cases']==36 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
        and stored['all19_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored proof required')
    require(len(controls['relocated_dispatch_cases'])==19 and len(controls['all12_source_current_target_control_leaves'])==12
        and len(controls['picture_and_short47xx_pairs'])==2 and controls['no_FI_FA_FO_inherited']
        and controls['all17_progressive_and_two_distinct_null_actor_FE_objects_preserved'],'relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',926),('research',824)],'complete guarded end required')
    expected_names={'19':'Carlo Sinat','172':'Collapsed Person'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected_names,'current name values differ;Stranger target remains separate')
    name_cases=names['native_four_consumer_cases']['rows']
    require(len(name_cases)==4 and {(r['actor_ID'],r['consumer']) for r in name_cases}=={(i,c) for i in [19,172] for c in ['progressive-nameplate','full-catalogue']}
        and all(r['text']==expected_names[str(r['actor_ID'])] and r['all_actor_models_and_unowned4MiB_exact'] for r in name_cases),'four complete current name consumers required')
    voices=load(doc['actor_voice_contract']);terms=load(doc['actor_terminology_reconciliation'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={19:7,172:0},'source voices differ')
    require(terms['approved_prose_names']=={'19':'Carlo','172':'Stranger'} and terms['source_FE_impact_index']==5 and terms['source_FE_stat_notice_index']==72
        and terms['source_FI_FA_FO_counts']=={'FI':0,'FA':0,'FO':0},'source names/FE roles differ')
    draft=terms['actor172_label_localization_draft']
    require(draft['current']=='Collapsed Person' and draft['proposed']=='Stranger' and draft['source']=='行き倒れ'
        and draft['source_secondary_field']=='アフリカ水夫' and draft['secondary_field_retained_as_evidence_not_silently_promoted_to_player_label']
        and draft['target_not_encoded_or_applied'] and draft['new_name_completion_credit']==0,'anonymous label target scope differs')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no transferred weak-boundary exceptions')
    wrap=load(doc['source_bound_wrap_retention_proof'])
    require(wrap['all19_prose_wordings_controls_metrics_guards_phase_and_four_row_limits_unchanged']
        and wrap['protected_pairs']==[['still','you'],['take','care'],['care','of'],['please','accept'],['accept','it']],'complete request/courtesy phrase planning required')
    require(len(approval['six_individual_rowcount_reasons'])==6 and approval['stale_rowcount_waiver_removed']==['DK4_MES_B200_R0065'],'individual source-rowcount reasons required')
    require(not actual['failures'] and not actual['paired_region_differences'] and actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19
        and actual['complete_matching_holds']==73 and actual['offline_only_source_indices']==[],'19 actual panels/73 holds required')
    require(len(actual['actual_panels'])==19 and [p['id'] for p in actual['actual_panels']]==mapping['actual_sampled_display_IDs']
        and sum(len(p['holds']) for p in actual['actual_panels'])==73,'individual actual panels/holds required')
    for panel,row in zip(actual['actual_panels'],doc['records'],strict=True):
        require(panel['id']==row['id'] and panel['prefix']==row['source_selector'] and panel['holds']
            and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'],'actual panel identity/native plane differs')
        for hold in panel['holds']:
            require(hold['complete_ink_gray_masks_equal_native_plane'] and hold['upper_portrait_name_and_item_regions_equal_source']
                and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256']
                and sha(Path(hold['clean_capture']).read_bytes())==hold['clean_capture_sha256'],'complete source-paired actual capture required')
    require([len(v['command_pairs']) for v in actual['versions']]==[40,40] and [v['fixture_exit_frame'] for v in actual['versions']]==[7676,7677]
        and actual['versions'][0]['input_schedule_sha256']==actual['versions'][1]['input_schedule_sha256'],'actual paths/inputs/return differ')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1]),'actual command results differ')
    expected_ids=[(r['id'],r['source_record_index'],r['source_selector']) for r in doc['records']]
    expected_source_offsets=[None]*9+[r['old_offset'] for r in mapping['blocks'][0]['command_map']]
    for version in actual['versions']:
        require([(r['id'],r['source_record_index'],r['prefix']) for r in version['selected_intervals']]==expected_ids,'individual actual source identity differs')
        require([r['source_offset'] for r in version['command_pairs']]==expected_source_offsets,'complete actual source-command identity differs')
        report=load(version['capture_report'])
        require(report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==13001,'cold-boot scope differs')
        for photo in report['frames_captured']:require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'sampled capture hash differs')
    timed=[dict(source=a,English=b) for a,b in zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'],strict=True) if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    require(actual['actual_timing_differences']==timed and len(timed)==19 and len(actual['later_whole_RGB_differences'])==16,'measured differences must remain explicit')
    require(state['actual_proof_sha256']==sample['actual_proof_sha256']==sha(Path(sample['actual_proof']).read_bytes()),'actual proof binding differs')
    duration_changes=[dict(source_offset=a['source_offset'],word=a['word'],source_duration=a['returned']-a['start'],English_duration=b['returned']-b['start'],
        duration_delta=b['returned']-b['start']-a['returned']+a['start']) for a,b in zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'],strict=True)
        if a['returned']-a['start']!=b['returned']-b['start']]
    require(duration_changes==state['actual_command_duration_changes'] and len(duration_changes)==8
        and [r['duration_delta'] for r in duration_changes]==[-1,4,-1,-1,-4,5,-4,3] and all(r['word']==0x4000 for r in duration_changes),
        'all opaque-control durations must remain exact;measured speech differences required')
    require(state['native_final_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and state['native_final_component_values'][0]==state['native_final_component_values'][1],'queried final native outcomes differ')
    require(state['final_PRNG_seeds_equal'] is False and sample['PRNG_seeds_differ']
        and sample['final_13001_PRNG_seeds']==state['final_13001_PRNG_seeds'] and len(set(state['final_13001_PRNG_seeds']))==2
        and state['complete_RNG_timing_cause_not_traced'] and sample['native_cloud_object_and_complete_RNG_timing_cause_not_traced']
        and state['no_full_RAM_future_random_sequence_or_broad_world_equivalence_claim'],'honest measured RNG scope required')
    require(state['later_whole_RGB_differences_unmodified']==actual['later_whole_RGB_differences'] and state['no_pixels_masked_retimed_or_edited'],'unmodified later differences required')
    prompt=[];sky=[]
    for diff in actual['later_whole_RGB_differences']:
        if diff['nontext_region_difference_bbox'] is None:
            require(diff['difference_bbox'][0:3:2]==[224,240] and diff['difference_bbox'][1]==360 and diff['difference_bbox'][3]<=376,'advance-prompt difference bounds differ');prompt.append(diff)
        else:
            require(diff['difference_bbox']==diff['nontext_region_difference_bbox']==[137,192,191,243] and diff['frame']>=12490,'following sky difference bounds differ');sky.append(diff)
    require(len(prompt)==6 and len(sky)==10 and sample['following_sailing_cloud_position_difference_not_masked_or_retimed'],'explicit prompt and sky samples required')
    require(sample['sampled_nontext_frames']==len(actual['all_sampled_frame_comparisons'])==182 and sample['nontext_equal_samples']==172
        and sum(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])==172
        and [r for r in actual['all_sampled_frame_comparisons'] if r['nontext_region_difference_bbox'] is not None]==sky
        and sample['all19_actual_native_panels73_complete_holds_and_changed_scene_source_regions_match']
        and sample['all31_source_commands_plus9_initializers_stored_and40_observed_without_omission']
        and sample['original_inn_transition_picture47xx6003_two_A000_final4640_and_complete_end_results_preserved']
        and sample['six_prompt_blink_samples_and_ten_following_sailing_cloud_samples_visually_reviewed']
        and sample['no_open_translation_specific_display_or_control_finding'] and sample['representative_shared_rules_approved'],'complete representative scene evidence required')
    views=sample['four_actual_and_six_paired_sheets_viewed']
    require(len(views)==10 and all(r['viewed_in_full_current_turn'] and r['viewed_after_image_return'] and r['original_detail']
        and sha(Path(r['path']).read_bytes())==r['sha256'] for r in views),'viewed actual and paired screens required')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets']
        and all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['reviewed_sheets']),'native screen approvals differ')
    require(not any(p.get('full_goal_complete') for p in [doc,mapping,seal,native,stored,controls,sample,state,approval]),'full editorial goal remains incomplete')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==19 and {r['source_selector'] for r in rows}==SELECTORS
        and Counter(r['kind'] for r in rows)=={'progressive':17,'system-FE':2}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':13,'retain-wording':6},'exact19 decisions/consumers required')
    require(all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']) and sample['actual_sampled_display_IDs']==ids
        and mapping['actual_sampled_display_IDs']==ids and sample['offline_only_display_IDs']==mapping['offline_only_display_IDs']==[],
        'all19 actual display IDs required')
    original_dispatch=load(doc['control_contract']);catalog=load(original_dispatch['registered_catalog_binding'])
    require(catalog['all467_rows_complete_keys_targets_route_masks_and_current_calls_verified'] and len(catalog['records'])==467 and all(c['registered_catalog_match'] is None for c in original_dispatch['speech_dispatch_cases']),'complete current name catalog binding required')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==200,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[200],IlnkContainer.parse(japanese).blocks[200]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require(spec['source_bytes']==len(block)==932 and spec['source_logical_end']==930 and spec['research_bytes']==828 and spec['research_logical_end']==828,'source/target extent metadata differs')
    require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in spec['mapped_native_commands']]==spec['command_map'],'both complete command maps must agree')
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
        require(row['source_reference']['block']==200 and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0') and row['current_record_index']==block[:at].count(b'\0'),'complete source/current record identity differs:'+ident)
        require(row['block']==200 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
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
        require(row['registered_runtime_catalog_entry'] is None,'no current B200 runtime override belongs here')
        old_prose=' '.join(effective.decode('cp932').split())
        logical_prose=row['english'].split('}',1)[1]
        for macro in ['FI','FA','FO']:logical_prose=logical_prose.replace('{MACRO:'+macro+'}',macro)
        require(row['effective_predecessor_paragraph']==old_prose,'effective predecessor differs:'+ident)
        require((logical_prose!=old_prose)==(row['editorial_decision']=='revise'),'revision/retention decision differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row.get('fresh_retained_wording_justification'),'individual retention reason required')
        require(not logical_prose.startswith('(') and not logical_prose.endswith(')'),'no private thought objects belong to B200')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=200,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(not macros,'B200 has no source FI/FA/FO')
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
    end=8+struct.unpack_from('<H',block,4)[0];require(end==930 and len(block)==932 and block[end:]==bytes(2),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==828,'target logical extent differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==828 and len(logical)==828 and sha(target)==spec['target_block_sha256'],'target block differs')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\0')==ref['new_record_index'],
            'relocated record offset/index differs:'+change['id'])
    commands=spec['mapped_native_commands'];require(len(commands)==31 and sum(c['word']==0x4000 for c in commands)==19,'command scope differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset']
        require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0],'opcode differs')
        require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command boundary differs')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'invented ancestor')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([(c['old_offset'],c['new_offset']) for c in stops]==[(926,824)] and stops[-1]['new_offset']+4==len(logical),'single source tail endword required')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word']!=0x4000]
    exact=[(8,'2d63'),(94,'0143'),(96,'00460b80'),(100,'8143'),(618,'304865a8'),(718,'3547'),(864,'0360'),(866,'2e63'),(906,'00a0ffff01021360'),(914,'00a0ffff01006530'),(922,'4046081d'),(926,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'12 exact leaves required')
    require([c['word'] for c in leaves]==[0x632D,0x4301,0x4600,0x4381,0x4830,0x4735,0x6003,0x632E,0xA000,0xA000,0x4640,0],'numeric leaf scope differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse does not restore every predecessor byte')
    new_blocks=list(old_blocks);new_blocks[200]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[200],'whole SC2 target differs')
    # Every check above is read-only. This is the sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=200,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=0,
            source_commands=31,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,
        all19_progressive_two_FE_no_macros_inn_picture47xx6003_two_A000_and_single_end_preserved=True,
        actual_two_complete_B22_fixtures19_panels73_holds172_equal_regions19_timings6_prompt10_sky_differences_unequal_PRNG_not_natural_activation=True,native_code_and123040_staged_payload_unchanged=True)
