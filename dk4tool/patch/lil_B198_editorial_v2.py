"""Atomic source-bound B198 seventeen-speech and common-ending integration."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B198_layout_v2 as codec
from dk4tool.dialogue.lil_B198_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B198_editorial_release_v1.json'
SELECTORS={12,15,254}
MENUS=[]
FLAGS=['all37_commands_and8_relative_sites_verified', 'all17_speech_targets_and12_control_leaves_preserved', 'eleven_progressive_six_null_actor_FE_no_macros_preserved', 'all544_predecessor_bytes_restored_by_inverse_zero_tailzeros', 'original_story_style11_complete_native_CP932_pause_reference_bound', 'fifteen_actual_panels56_holds_and_two_offline_conditional_speeches_scope_explicit', 'original_predicates_results_and_common_end_actual_verified', 'representative_shared_rules_approved']
TERM_FLAGS=['source_15_speeches_and_dream_transition_viewed', 'source_end540_returns_normally_at6697', 'source_FE_is_unattributed_speaking_voice_not_impersonal_notice', 'source_four_chant_occurrences_and_three_direct_questions_preserved', 'external_references_not_game_facts', 'source_dream_explicit_but_no_confirmed_Namahage_identity_cause_or_item_powers', 'spoken_this_remains_unnamed', 'tomorrow_morning_Admiral_handover_remains_prospective_not_completed', 'source_predicate_results_zero_for_both_sites_not_full_roster_membership_semantics_proof', 'both_conditional_Angelo_questions_need_shared_context_valid_without_first_question', 'source_blank_FE_portrait_name_and_source_controlled_progressive_visibility_preserved', 'no_added_age_kinship_rank_marriage_room_sharing_ritual_date_or_scene_location', 'source_initialized_B22_fixture_not_natural_event198_activation_original_location_full_route_or_hardware', 'all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison', 'source_effect_and_resource_bodies_not_fully_executed_offline']
END_MAP=[(540,640)]

def load(path):return json.loads(Path(path).read_bytes())
def require(value,message):
    if not value:raise ValueError('Lil B198 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B198-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and not doc['formatting_review_pending']
        and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all17_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'],'source/reference approval required')
    require(seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'sealed manuscript changed')
    require(seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed reference map changed')
    require(mapping['format']=='dk4-lil-B198-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8
        and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    require(conf['required_map_flags']==FLAGS,'complete map requirements required')
    for name in FLAGS:require(mapping.get(name) is True,'required source shape:'+name)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','representative_proof',
        'postscene_native_state_proof','source_bound_wrap_retention_proof','source_original_progressive_style_proof']
    proofs={k:load(doc[k]) for k in keys}
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    native,stored,control,ends,sample,observed,wrap,style=[proofs[k] for k in keys]
    approval=load(conf['native_approval']);actual=load(observed['actual_proof'])
    require(len(native['cases'])==17 and native['current_original_macro_alignment_calls']==136 and native['complete_progressive_planes']==11
        and native['complete_FE_logical_and_physical_planes']==6 and len(native['negative_controls'])==18,'complete native consumers required')
    require(all(r['rejected'] for r in native['negative_controls']) and len(approval['formatter_negatives'])==28,'consumer/formatter negatives required')
    require(len(stored['final_target_parity_cases'])==17 and stored['current_final_stored_macro_alignment_cases']==68
        and stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
        and stored['all17_final_targets_complete_native_planes_equal_reviewed_planes'],'stored speech proof required')
    require(native['source_original_progressive_caller_style']==stored['source_original_progressive_caller_style']==11
        and style['source_explicit_style']==11 and style['source_context_style_field']==0x30
        and len(style['cases'])==3 and all(c['exact_actual_ink'] and c['exact_actual_gray']
            and all(e['style']==11 for e in c['native_events']) for c in style['cases']),'original story style11 required')
    require(native['source_original_progressive_style_proof']==stored['source_original_progressive_style_proof']==doc['source_original_progressive_style_proof']
        and native['source_original_progressive_style_proof_sha256']==stored['source_original_progressive_style_proof_sha256']==doc['source_original_progressive_style_proof_sha256'],
        'source-correct native style proof required')
    require(len(control['relocated_dispatch_cases'])==17 and len(control['all12_source_current_target_control_leaves'])==12
        and len(control['original_unforced_predicate_pairs'])==2 and len(control['original4835_picture_pair'])==1,'relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['no_relative_destination_at_or_beyond_logical_end']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',540),('research',640)],'guarded original ending required')
    require(not actual['failures'] and not actual['paired_region_differences'] and not actual['actual_timing_differences']
        and not actual['later_whole_RGB_differences'] and actual['same_observed_source_path_original_results_predicates_and_end540'],
        'source/English display and control results differ')
    require(len(actual['actual_panels'])==actual['complete_matching_observations']==15 and actual['complete_matching_holds']==56
        and actual['offline_only_source_indices']==[65,95],'actual/offline scope differs')
    require([len(v['command_pairs']) for v in actual['versions']]==[40,40]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[6697,6697]
        and all(len(v['selected_intervals'])==15 for v in actual['versions']),'source path/return scope differs')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1])
        and actual['versions'][0]['input_schedule_sha256']==actual['versions'][1]['input_schedule_sha256'],
        'measured source/English command results or inputs differ')
    for version in actual['versions']:
        require([(r['source_offset'],r['native_result']) for r in version['command_pairs'] if r['word']==0x8000]==[(306,[2,0]),(480,[2,0])],
            'both original unforced predicate results required')
        require(version['command_pairs'][-1]['source_offset']==540 and version['command_pairs'][-1]['native_result']==[0,0],
            'observed original source ending required')
        require([r['source_record_index'] for r in version['selected_intervals']]==[10,14,18,22,26,30,34,38,42,49,53,72,76,80,84],
            'fifteen actual source IDs required')
    require(sample['fifteen_actual_native_panels56_holds_and_two_offline_conditionals_explicit']
        and sample['all37_source_commands_plus9_initializers_stored_without_omission']
        and sample['source_story_style11_binds_complete_CP932_pause_planes_without_ROM_change']
        and sample['original_predicate_results_and_single_source540_target640_end_and_return_preserved']
        and sample['representative_shared_rules_approved'] and sample['no_open_translation_specific_display_or_control_finding'],
        'representative display/control approval required')
    require(sample['sampled_nontext_frames']==observed['sampled_nontext_frames']==len(actual['all_sampled_frame_comparisons'])==182
        and all(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])
        and sample['source_and_English_return_frames']==observed['source_and_English_return_frames']==[6697,6697]
        and sample['command_timing_difference_count']==observed['command_timing_difference_count']==0
        and sample['later_sampled_whole_RGB_difference_count']==observed['later_sampled_whole_RGB_difference_count']==0,
        'measured scene scope differs')
    require(sample['final_13001_PRNG_seeds']==observed['final_13001_PRNG_seeds'] and len(set(observed['final_13001_PRNG_seeds']))==1
        and sample['no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim']
        and observed['no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim'],'honest postscene scope required')
    require(observed['all17_native_glyphs_complete_15_actual_panels56_complete_holds_match']
        and observed['source_story_caller_style11_CP932_pause_reference_corrected_without_ROM_or_prose_change']
        and observed['source_matched_name_portrait_item_and_background_visibility_not_normalized']
        and observed['no_open_changed_scene_translation_display_or_control_finding'],'viewed actual approval required')
    views=observed['all_current_native_sheets_viewed']+observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views']
    require(len(views)==9 and all(s['viewed_in_full_current_turn'] and s['viewed_after_image_return'] and s['original_detail']
        and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views),'viewed screens changed')
    require(observed['actual_source_English_cold_boots']==2 and observed['new_English_runs']==1 and observed['total_successful_frames']==26002
        and observed['original_source_run_reused_not_a_new_run'] and observed['offline_only_source_indices']==[65,95],
        'run counts and conditional limits required')
    terms=load(doc['actor_terminology_reconciliation']);voices=load(doc['actor_voice_contract']);names=load(doc['source_nameplate_consumer_proof'])
    require(terms['approved_prose_names']=={'12':'Yukihisa Shiraki','15':'Angelo Puccini'},'approved names differ')
    require(conf['required_term_flags']==TERM_FLAGS,'complete source-context requirements required')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'source context required:'+flag)
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={12:1,15:4},'two source voices differ')
    require(names['progressive_nameplate_values']=={'12':'Yukihisa Shiraki','15':'Angelo Puccini'}
        and names['full_catalogue_values']=={'12':'Yukihisa Genjo Shiraki','15':'Angelo Puccini'}
        and len(names['native_four_consumer_cases']['rows'])==4,'source-bound name consumers required')
    require(wrap['exact_source_indices']==[10,14] and wrap['phrase_protection']==['any','naughty']
        and wrap['all_words_native_metrics_width_guard_phase_bounds_pagination_and_runtime_unchanged']
        and wrap['no_authored_line_break_or_exact_row_override'],'complete repeated-call phrase grouping required')
    rows=doc['records'];ids={r['id'] for r in rows}
    require(len(rows)==len(ids)==17,'17 unique objects required')
    require({r['source_selector'] for r in rows}==SELECTORS and Counter(r['kind'] for r in rows)=={'progressive':11,'system-FE':6},'speaker/consumer scope differs')
    require(Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':5}
        and all(r.get('fresh_retained_wording_justification') for r in rows if r['editorial_decision']=='retain-wording'),'individual decisions required')
    observed_ids=set(mapping['actual_sampled_display_IDs']);offline=set(mapping['offline_only_display_IDs'])
    require(len(observed_ids)==15 and offline=={'DK4_MES_B198_R0065','DK4_MES_B198_R0095'} and not observed_ids&offline and observed_ids|offline==ids
        and observed_ids=={r['id'] for r in actual['actual_panels']}
        and observed_ids==set(sample['actual_sampled_display_IDs'])==set(observed['actual_sampled_display_IDs'])
        and offline==set(sample['offline_only_display_IDs']),'actual/offline ownership differs')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==198,'one exact block required');spec=mapping['blocks'][0]
    oldblocks=list(IlnkContainer.parse(source).blocks);block=oldblocks[198];original=IlnkContainer.parse(japanese).blocks[198]
    require(len(oldblocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'])==(544,544,644,644) and len(block)==544,'source/target extent metadata differs')
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
        require(row['block']==row['source_reference']['block']==198 and row['file_path']==PATH and row['source_record_index']==original[:sa].count(b'\0')
            and row['current_record_index']==row['record_index']==block[:at].count(b'\0'),'record identity differs:'+ident)
        require(row['source_selector']==raw[0]==old[0] and raw[0] in SELECTORS and (raw[0]==254)==fe and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}'),'selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0 and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'full preamble differs:'+ident)
        require(ref['record_index']==row['record_index'] and ref['old_offset']==at and ref['old_length']==len(old),'relocation owner differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode() for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])];require(sm==tm,'substitution order differs:'+ident);macros.update(sm)
        p=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        require(row.get('qa_waivers') in [None,['line-break-count']],'unapproved safety waiver')
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning'
            and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        if row['source_record_index'] in [10,14]:
            require(qa['visible_lines']==['Any naughty children here?','Any naughty children here?']
                and row.get('native_layout_retention_reason'),'complete repeated call rows required')
        require(row['native_font_case']==case,'source-correct native reference differs:'+ident)
        old_prose=' '.join(old[1:].decode('cp932').split())
        require(row['effective_predecessor_paragraph']==old_prose,'predecessor prose differs:'+ident)
        require((row['english'].split('}',1)[1]!=old_prose)==(row['editorial_decision']=='revise'),'revision/retention differs:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),old=old,value=value));changes.append(dict(id=ident,block=198,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(not macros,'no source macros may be invented')
    require(not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'] and [c['old_offset'] for c in spec['choice_commands']]==MENUS,'typed object scope differs')
    patches.sort(key=lambda p:p['start']);require(len(patches)==17 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping text/menu ownership')
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            require(not p['start']<at<p['end'],'unclassified interior reference')
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==544 and block[end:]==bytes(0),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));edges=spec['relative_skip_fixups']
    require(len(edges)==8 and len(spec['target_native_skip_cases'])==40 and len(logical)==mapped(end)==644,'relative scope differs')
    for e in edges:
        a,target=mapped(e['offset']),mapped(e['matched_skip_target']);span=target-a-4
        require(a==e['new_offset'] and target==e['new_matched_skip_target'] and mapped(e['unmatched_next_offset'])==e['new_unmatched_next'] and span==e['target_span']
            and e['span_field_offset']==e['offset']+2 and e['matched_skip_target']==e['offset']+4+e['source_span']
            and struct.unpack_from('<H',block,e['span_field_offset'])[0]==e['source_span'] and 0<=span<=65535 and span%2==0,'relative target differs')
        struct.pack_into('<H',logical,a+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(sha(target)==spec['target_block_sha256'] and len(target)==644,'target block differs')
    commands=spec['mapped_native_commands'];counts=Counter(c['word'] for c in commands)
    require(counts==Counter({0x4000:17,0x6000:1,0x4500:1,0x633F:1,0xA000:2,0x623F:1,0x4621:1,0x61FF:1,0x8000:2,0x4835:1,0:1,0x100:4,0x200:2,0x300:2}),'complete command scope differs')
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
    require(leaves==[(r['word'],r['old_offset'],r['new_offset'],r['source_current_target_hex']) for r in control['all12_source_current_target_control_leaves']],'all12 original control leaves required')
    stops=[c for c in commands if c['word']==0];require([(c['old_offset'],c['new_offset']) for c in stops]==END_MAP and stops[-1]['new_offset']+4==len(logical),'single common end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    for r in spec['text_records']:
        require(target[r['new_offset']:r['new_offset']+r['new_length']].hex()==r['target_hex'] and target[:r['new_offset']].count(b'\0')==r['new_record_index'],'final speech index differs')
    for c in spec['choice_commands']:
        for r in c['label_references']:require(target[:r['new_offset']].count(b'\0')==r['new_record_index'],'final label record index differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for e in edges:struct.pack_into('<H',restored,e['new_offset']+2,e['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse must restore every544 predecessor byte')
    newblocks=list(oldblocks);newblocks[198]=target;result=IlnkContainer(newblocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(oldblocks,newblocks,strict=True)) if a!=b]==[198],'whole SC2 target differs')
    # All approval,metadata,prose,control and inverse checks precede this sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=198,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=8,source_commands=37,inverse_restores_every_original_logical_and_stored_byte=True)],
        all335_other_SC2_blocks_unchanged=True,all17_reviewed_objects_common_end_no_macros_and12_leaves_preserved=True,
        actual15_speech_panels56_holds_two_offline_conditionals_not_natural_event_eligibility=True,native_code_and123040_staged_payload_unchanged=True)
