"""Atomic B194 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B194_layout_v1 as codec
from dk4tool.dialogue.lil_B194_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B194_editorial_release_v1.json'
SELECTORS={6,117,156,254}
FLAGS=['all21_structural_commands_verified', 'all11_active_speech_targets_preserved', 'all6_leaves_A000_predicate_resource42_two_C200_and_single_end_exact', 'single_declared_tail_endword_preserved', 'progressive10_impersonal_FE1_and_FI1_FA0_FO0_preserved', 'all4_relative_sites_and20_target_native_skip_cases_verified', 'changed_predicate_alignment_has_exact_owned_scratch_restore', 'source_A000_raw_operand_bytes_preserved_without_inferred_semantics', 'single_end536_actual_target510_offline', 'representative_shared_rules_approved']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B194 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B194-editorial-release-v1','unknown release format')
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
    require(mapping['format']=='dk4-lil-B194-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source map required')
    for flag in FLAGS:require(mapping.get(flag) is True,'missing map approval:'+flag)
    proof_keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','layout_QA_proof']
    for key in proof_keys:require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'proof differs:'+key)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B194_layout_v1.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B194_profile.py'),'scoped formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(len(native['cases'])==11 and native['current_original_macro_alignment_calls']==88
        and native['complete_progressive_planes']==10 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==24 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28,'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==11 and stored['current_final_stored_macro_alignment_cases']==44
        and stored['new_parity_macro_alignment_cases']==20 and stored['exact_byte_identical_reused_macro_alignment_cases']==24
        and stored['all11_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==11 and len(controls['all6_source_current_target_nonrelative_nonspeech_leaves'])==6,'complete relocated controls required')
    require(controls['changed_unaligned_operand_scratch_owned_and_restored'] and len(controls['unforced_relocated_predicate_cases'])==1,'relocated predicate proof required')
    pred=controls['unforced_relocated_predicate_cases'][0]
    require((pred['source_offset'],pred['target_offset'])==(312,274) and pred['case']['native_result']==[2,0,0,0,0,0]
        and len(pred['case']['original_unaligned_operand_read_scratch_writes'])==1
        and pred['case']['sole_scratch_restore_recovers_all4MiB_exact'],'unaligned availability scratch differs')
    priors=[0,1,2,3,0xFFFFFFFF]
    ui=controls['relocated_C200_prior_result_cases'];resources=controls['relocated_resource42_prior_result_cases'];end_prior=controls['relocated_end_prior_result_cases']
    require(len(ui)==10 and {(r['source_offset'],r['target_offset'],r['prior_result']) for r in ui}=={
        (a,b,p) for a,b in [(494,464),(534,508)] for p in priors},'both UI sites/all priors required')
    require(all(r['case']['native_result']==[3,r['prior_result'],0,0,0,0]
        and r['case']['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui),'C200 ownership/carried result differs')
    require(len(resources)==10 and all((r['source_offset'],r['target_offset'])==(406,376) for r in resources)
        and {(r['case']['previous_result'],r['case']['incidental_boundary_return']) for r in resources}=={(p,v) for p in priors for v in [0,priors[-1]]}
        and all(r['case']['native_result']==[3,r['case']['previous_result'],0,0,0,0] for r in resources),'resource42 boundary/all priors differ')
    require(len(end_prior)==5 and {r['prior_result'] for r in end_prior}==set(priors)
        and all(r['target_offset']==510 and r['native_result']==[0,r['prior_result'],0,0,0,0] for r in end_prior),'end carried result differs')
    require([len(p['speech_record_indices']) for p in controls['relocated_structural_predicate0_1_paths']]==[9,11],'conditional path scope differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',536),('research',510)],'guarded end decodes required')
    progressive={'6':'Julio Erneco','117':'Port Worker','156':'Sailor'}
    full={'6':'Julio Erneco','117':'Port Worker','156':'Retainer'}
    require(names['progressive_nameplate_values']==progressive and names['full_catalogue_values']==full,'exact original names/roles required')
    name_rows=names['native_six_consumer_cases']['rows']
    require(len(name_rows)==6 and {(r['consumer'],r['actor_ID']):r['text'] for r in name_rows}=={
        **{('progressive-nameplate',int(i)):v for i,v in progressive.items()},**{('full-catalogue',int(i)):v for i,v in full.items()}},'six original name consumers required')
    require(sum(r['ownership_mode']=='original-owned-name-scratch-ring' for r in name_rows)==2
        and all(r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] and r['all_actor_models_and_unowned4MiB_exact'] for r in name_rows)
        and all((r['actor_ID']==6)==bool(r['original_scratch_rings']) for r in name_rows),'mixed name ownership differs')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}=={6:5,117:0,156:4},'three original voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']==progressive and terms['full_catalogue_names']==full
        and terms['commodity_index']==37 and terms['source_commodity']=='清酒' and terms['commodity']=='Sake'
        and terms['city']=='Hangzhou' and terms['one_source_current_city_alias']['text']=='Hangzhou'
        and terms['commodity_binding']['text']=='Sake' and terms['original_commodity_metadata_hex']=='d00705db84030100'
        and terms['FI_default_expansion']=='Lil' and terms['FI_default_ASCII_bytes']==3
        and terms['source_title']=='提督' and terms['source_supported_English_title']=='Admiral','exact names/commodity/FI title required')
    for flag in ['two_owned_Julio_scratch_consumers_and_four_original_readonly_role_consumers_preserve_unowned4MiB',
        'source_recent_experiences_casual_taste_rice_hearsay_surprise_thirst_invitation_acceptance_and_urgency_preserved',
        'rice_ingredient_remains_reported_not_recipe_technical_process_origin_or_narrator_fact',
        'legendary_liquor_is_Julios_excited_inference_not_certified_identity_award_or_earned_item',
        'conditional_Julio5_voice_and_source_explicit_FI_Admiral_address_not_invented_kinship_or_new_rank',
        'no_invented_brotherhood_player_employment_shared_drinking_history_or_new_personal_name',
        'source_now_drink_invitation_and_later_urgent_purchase_are_intentions_not_completed_actions',
        'no_price_amount_measured_serving_venue_recipe_origin_health_effect_intoxication_or_reward_invented',
        'Sake37_individual_commodity_and_one_Hangzhou_alias_not_category_or_new_UI_fidelity_credit',
        'Sake37_older_UI_fidelity_review_remains_open_separate_from_dialogue',
        'tentative_Sake_Hangzhou_FE_not_earlier_location_or_earned_fashion',
        'source21_commands_one_predicate_four_relatives_resource42_two_C200_one_FI_and_single_end_preserved',
        'all11_clean_first_glosses_precede_predecessor_English_prose_comparison',
        'raw_current_dispatch_hex_is_structural_evidence_not_translation_source']:
        require(terms.get(flag) is True,'source context required:'+flag)
    layout=load(doc['layout_QA_proof'])
    require(not layout['failures'] and len(layout['records'])==11 and len(layout['row_count_notes'])==3
        and doc['all11_current_native_previews_viewed_on_two_sheets'] and doc['viewed_phrases_use_full_verified_width_and_complete_clauses']
        and doc['no_record_specific_ordinary_boundary_exception_required'] and doc['no_shared_metric_guard_or_manual_break_change'],'viewed layout/reasons differ')
    require(sample['all11_panels10_progressive1_FE_one_FI_and_normal_returns_pass'] and sample['original21_commands_four_relative_sites_and_one_declared_end_preserved']
        and sample['default_source_availability0_and_original_recruitment_setup_availability1_observed_without_forcing']
        and sample['source_resource42_and_two_C200_paths_observed_in_conditional_setup']
        and sample['extra_original_B165_recruitment_initializer_is_disclosed_test_setup_not_earned_progress']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['unique_actual_display_objects']==11 and observed['actual_panel_observations_across_setups']==20
        and observed['sampled_nontext_pairs']==230 and observed['total_paired_fullscreen_views']==24
        and observed['all_content_jobs_terminal_and_reaped'] and observed['actual_new_cold_boot_runs']==4 and observed['total_frames']==36004
        and not observed['visual_review_pending'] and observed['default_name_Lil_actual_FI_display_verified_all_custom_name_lengths_not_claimed']
        and observed['no_PRNG_causal_future_world_full_RAM_or_hardware_equivalence_claim'],'complete viewed actual scope required')
    require(len(observed['versions'])==2 and observed['offline_only_display_IDs']==[],'two distinct actual setups required')
    actuals=[]
    for index,v in enumerate(observed['versions']):
        expected,selected,stored_count,outcome,exit_frame=[(9,24,30,0,5017),(11,30,31,1,5737)][index]
        require(v['predicate_result']==outcome and v['actual_selected_fixture_commands']==selected and v['stored_fixture_commands']==stored_count
            and v['return_frames']==[exit_frame,exit_frame] and v['complete_native_holds']==[35,44][index]
            and v['timing_differences']==dict(total=0,speech=0,control_or_end=0) and v['sampled_nontext_pairs']==115
            and v['sampled_postscene_and_final_RGB_equal'] and v['all_five_native_groups_and_whole1A04_actor_and_captain2_equal']
            and v['final_PRNG_seeds']==[3723009301,3723009301],'measured per-setup timing/state differs')
        require(sha(Path(v['actual_proof']).read_bytes())==v['actual_proof_sha256']
            and sha(Path(v['visual_analysis']).read_bytes())==v['visual_analysis_sha256'],'actual evidence differs')
        actual=load(v['actual_proof']);analysis=load(v['visual_analysis']);actuals.append(actual)
        require(actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==expected
            and not actual['failures'] and not actual['paired_region_differences'],'actual native planes differ')
        require(analysis['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
            and not analysis['actual_timing_differences'] and not analysis['nontext_difference_samples'],'measured raw state/timing differs')
        require(len(v['viewed_sheets'])==5 and all(s['viewed_after_image_return'] and not s['visual_review_pending']
            and sha(Path(s['path']).read_bytes())==s['sha256'] for s in v['viewed_sheets']),'actual views differ')
        for version in actual['versions']:
            require(len(version['selected_B22_command_pairs'])==selected and len(version['selected_intervals'])==expected
                and version['fixture_exit_frame']==exit_frame and version['single_source_end536_actually_reached']
                and version['selected_B22_command_pairs'][-1]['result_words']==[0,outcome]
                and version['selected_B22_command_pairs'][-1]['original_source_offset']==536,'actual source path/end differs')
            require(len(version['actual_predicate_transitions'])==1 and version['actual_predicate_transitions'][0]['source_offset']==312
                and version['actual_predicate_transitions'][0]['result']==outcome,'actual original availability differs')
            ui=version['source_C200']
            require([r['original_source_offset'] for r in ui]==([534] if index==0 else [494,534])
                and all(r['word']==0xC200 and r['extent']==2 and r['result_words']==[3,outcome] for r in ui),'actual UI path differs')
            require(len(version['source_A000'])==1 and version['source_A000'][0]['original_source_offset']==8,'source A000 differs')
            if index==1:
                require(sum(r.get('disclosed_original_recruitment_initializer',False) for r in version['selected_B22_command_pairs'])==1
                    and sum(r['word']==0x632A for r in version['selected_B22_command_pairs'])==1,'original recruitment/resource42 setup differs')
    require(load(conf['actual_proof'])==observed,'combined actual proof differs')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets'],'native sheet approval differs')
    for s in approval['reviewed_sheets']:require(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'],'native view differs')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==11 and {r['source_selector'] for r in rows}==SELECTORS,'eleven exact records required')
    require(Counter(r['kind'] for r in rows)=={'progressive':10,'system-FE':1}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':4,'retain-wording':7},'consumer/decision scope differs')
    require(sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids
        and observed['actual_sampled_display_IDs']==ids and all([r['id'] for r in v['selected_intervals']]==ids for v in actuals[1]['versions']),'actual display keys differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==194,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[194],IlnkContainer.parse(japanese).blocks[194]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require(spec['source_bytes']==len(block)==540 and spec['source_logical_end']==540 and spec['research_bytes']==516 and spec['research_logical_end']==514,'source/target extent metadata differs')
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
        require(row['source_reference']['block']==194 and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0') and row['current_record_index']==block[:at].count(b'\0'),'complete source/current record identity differs:'+ident)
        require(row['block']==194 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
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
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification'],'unjustified retention')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=194,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(macros==Counter({b'FI':1}),'one original FI required')
    require(not spec['choice_commands'] and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps']
        and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20,'invented control object')
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping text objects')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'interior text reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-(p['end']-p['start'])
        return offset+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==540 and len(block)==540 and block[end:]==bytes(),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==514,'target logical extent differs')
    expected_edges=[(320,0x200,4,328),(324,0x300,4,332),(328,0x100,168,500),(496,0x100,0,500)]
    fixups=spec['relative_skip_fixups']
    require([(r['offset'],r['word'],r['source_span'],r['matched_skip_target']) for r in fixups]==expected_edges,'source relative sites differ')
    for edge in fixups:
        a,b=edge['offset'],edge['new_offset'];finish=mapped(edge['matched_skip_target']);span=finish-b-4
        require(b==mapped(a) and edge['span_field_offset']==a+2 and edge['unmatched_next_offset']==a+4
            and edge['new_unmatched_next']==b+4 and edge['new_matched_skip_target']==finish and edge['target_span']==span
            and struct.unpack_from('<H',block,a+2)[0]==edge['source_span'] and 0<=span<=0xFFFF and span%2==0,'relative map differs')
        struct.pack_into('<H',logical,b+2,span)
    cases=spec['target_native_skip_cases']
    require({(r['new_offset'],r['last_result']) for r in cases}=={(r['new_offset'],p) for r in fixups for p in priors},'all target skip inputs required')
    for case in cases:
        edge=next(e for e in fixups if e['new_offset']==case['new_offset']);p=case['last_result'];word=edge['word']
        take=word==0x100 or (word==0x200 and p==0) or (word==0x300 and p==1)
        require(case['native_extent']==4+(edge['target_span'] if take else 0)
            and case['ABI_all4MiB_owner_stream_result_length_and_guards_exact'],'target skip extent/ownership differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==516 and target[514:]==bytes(2) and sha(target)==spec['target_block_sha256'],'target block differs')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\0')==ref['new_record_index'],
            'relocated record offset/index differs:'+change['id'])
    commands=spec['mapped_native_commands'];require(len(commands)==21 and sum(c['word']==0x4000 for c in commands)==11,'command scope differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset']
        require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0],'opcode differs')
        require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command boundary differs')
        require(c['target_0100_ancestors']==[mapped(a) for a in c['source_0100_ancestors']],'relative ancestry differs')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        elif c['word'] not in [0x100,0x200,0x300]:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([(c['old_offset'],c['new_offset']) for c in stops]==[(536,510)] and stops[-1]['new_offset']+4==len(logical),'single source tail endword required')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300]]
    exact=[(8,'00a0ffff012536a1'),(312,'0080ffff06fe0030'),(406,'2a63'),(494,'00c2'),(534,'00c2'),(536,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'six exact leaves required')
    require([c['word'] for c in leaves]==[0xA000,0x8000,0x632A,0xC200,0xC200,0],'numeric leaf scope differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse does not restore every predecessor byte')
    new_blocks=list(old_blocks);new_blocks[194]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[194],'whole SC2 target differs')
    # Every check above is read-only. This is the sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=194,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=4,
            source_commands=21,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,
        all11_progressive_FE_speeches_one_FI_A000_availability_resource42_two_C200_and_single_end_preserved=True,
        actual_four_B22_fixtures_two_unforced_paths_original_recruitment_setup_230_regions79_holds_equal_measured_postscene_state_not_natural_activation=True,native_code_and123040_staged_payload_unchanged=True)
