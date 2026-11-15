"""Validate the complete reviewed B45 batch, reconstruct from source, then commit one archive."""
import json
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.rafael_B45_profile_v1 import contract,profile_for,validate_runtime
from dk4tool.dialogue import rafael_B45_layout_v1 as codec
from dk4tool.patch.rafael_B45_reconstruction_v1 import reconstruct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B45_release_paths_v7903 import FLAGS,proofs
CONFIG='translations/rafael_B45_editorial_release_v2.json'
PATHS=('/data/SC0.DK4',)
SOURCE_FONT='work/analysis/Rafael_B45_source_name_planes_v7894/12_complete_source_pages2_names8_literal_alignments_distinct_FE.json'
def load(path):return json.loads(Path(path).read_bytes())
def require(value,label):
    if not value:raise ValueError('Rafael B45 editorial contract: '+label)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
def commit_files(image,files):image.rom.files=files
def summary(group):
    return dict(source_English_exits=group['source_English_exits'],command_difference_rows=len(group['command_comparison_differences']),
        duration_difference_rows=len(group['duration_differences']),later_RGB_differences=len(group['later_RGB_differences']),
        later_samples=group['later_sample_count'],five_component_equality=group['five_native_component_equality'],
        whole_actor_equality=group['whole_actors_equal'],final_PRNG_seeds=group['final_PRNG_seeds'])
def check_actual(actual,sourcefont,native,names,rows):
    require(not actual['unresolved'] and len(actual['groups'])==2 and {g['version'] for g in actual['groups']}=={'clean_Japanese','English'},'two complete actual language groups')
    require(actual['actual_FE_condition_result1_preserved_without_result_orstate_forcing'] and actual['actual_normal_type0_value1_carry_both_languages'],'original FE condition andnormal carry')
    require(actual['original_ten_command_B44_ROM_entry_fixture_not_natural_B45_activation_Ceuta_location_orfull_route'],'disclosed original-entry fixture scope')
    require(sum(g['complete_body_holds'] for g in actual['groups'])==90 and sum(g['complete_progressive_header_holds'] for g in actual['groups'])==84 and sum(g['complete_FE_absent_header_holds'] for g in actual['groups'])==6,'all actual body/header/FE holds')
    wanted_ids={r['id'] for r in rows}
    require(len(sourcefont['source_records'])==12 and {r['id'] for r in sourcefont['source_records']}==wanted_ids and len({r['id'] for r in sourcefont['source_records']})==12,'complete unique independent source font records')
    require(len(native['records'])==12 and {r['id'] for r in native['records']}==wanted_ids and len({r['id'] for r in native['records']})==12,'complete unique native font records')
    expected_names={r['actor_ID']:r['name'] for r in names['records']}
    for group in actual['groups']:
        fixture=group['fixture'];version=group['version']
        require(group['route']==0 and fixture['route']==0 and fixture['source_block']==45 and fixture['fixture_block']==44,'actual original route/block')
        require(group['actual_unique_speeches']==len(group['speech_observations'])==12 and not group['incomplete_sampled_holds'] and not group['unidentified_trace_rows'] and not group['unreturned_following_dialogues'],'complete actual speech observations')
        require(group['exit_frame']==6653 and group['native_terminal_result']==[0,1] and len(group['command_pairs'])==32 and group['observed_original_exchange_commands']==22,'actual command count andnormal type0 value1')
        require([r['word'] for r in group['original_structural_commands_not_selected']]==[0x400,0x100],'explicit unselected structural controls')
        for key in ['capture_report','observer_report']:require(sha(Path(group[key]).read_bytes())==group[key+'_sha256'],'actual report/trace hash')
        report,trace=load(group['capture_report']),load(group['observer_report'])
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and report['frames']==16001 and not report['hardware_device_verification'],'actual cold-boot limits')
        require(not any(v for k,v in report.items() if k.startswith('synthetic_')),'no synthetic state inputs')
        require(report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()),'fixture ROM identity')
        require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'read-only observer scope')
        photos={p['frame']:p for p in report['frames_captured']};commands={p['fixture_offset']:p for p in group['command_pairs']}
        expected_commands={p['offset']:p for p in fixture['all_fixture_commands']}
        require(len(expected_commands)==34 and len(fixture['all_original_exchange_commands'])==24 and len(fixture['original_text_records'])==12,'complete original fixture objects')
        require(fixture['all_five_relative_spans_unchanged_under_constant32_byte_shift'] and fixture['no_original_speech_branch_resource_effect_orend_omitted'],'full fixture controls preserved')
        previous_next=None
        for pair in group['command_pairs']:
            before,after=trace['rows'][pair['entry_row']],trace['rows'][pair['return_row']]
            require(before['kind']=='before_command' and after['kind']=='after_command' and after['entry_row']==pair['entry_row'],'actual entry/return association')
            require(before['frame']==pair['start'] and after['frame']==pair['returned'] and after['decoded_length']==pair['decoded_length'] and after['result_words']==pair['native_result'],'exact observed command result/timing')
            at=pair['fixture_offset'];command=expected_commands[at];word=command['word']
            require(before['source']['instruction_offset']==after['source']['instruction_offset']==at and before['source']['first_word']==word==pair['word'],'actual command source offset/opcode')
            for observed in [before,after]:
                resident=observed['source']
                require(resident['classification']=='original_SC_cache' and resident['route']==0 and resident['block']==44,'actual original cache route/block identity')
                require(resident['actual_sha256']==resident['registered_sha256']==fixture['fixture_block_sha256'] and resident['payload_bytes']==fixture['fixture_stored_bytes'],'exact actual resident fixture identity')
                require(resident['instruction_pointer']==resident['payload_address']+at and sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256'],'actual complete resident payload andentry offset')
            require(before['source']['whole_resident_payload_exact_ROM'] and after['source']['whole_resident_payload_exact_ROM'] and before['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] and after['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],'resident command/callback integrity')
            if previous_next is not None:require(at==previous_next,'actual original conditional flow')
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');last=pair['observed_previous_result']
                taken=word==0x100 or word==0x200 and last==0 or word==0x300 and last==1 or word==0x400 and last==2
                require(pair['decoded_length']==4+(span if taken else 0),'actual original relative branch')
            else:require(pair['decoded_length']==command['native_extent'],'actual complete native extent')
            previous_next=at+pair['decoded_length']
        require(group['command_pairs'][-1]['native_result']==[0,group['command_pairs'][-2]['native_result'][1]]==[0,1],'original normal end preserves value1')
        require({s['id'] for s in group['speech_observations']}=={r['id'] for r in rows},'all twelve actual IDs')
        for scene in group['speech_observations']:
            row=next(r for r in rows if r['id']==scene['id']);is_FE=row['source_selector']==254
            require(scene['source_selector']==row['source_selector'] and scene['kind']==row['kind'] and scene['native_page_count']==1 and not scene['incomplete_sampled_holds'],'actual individual speaker/page')
            require(scene['actual_name']==(None if is_FE else expected_names[row['source_selector']]),'actual source-bound name')
            model=next(r for r in (sourcefont['source_records'] if version=='clean_Japanese' else native['records']) if r['id']==row['id'])
            require(scene['native_plane']==model['pages'][0]['native_plane'] and scene['native_plane_sha256']==model['pages'][0]['native_plane_sha256']==sha(Path(scene['native_plane']).read_bytes()),'actual independent native plane association')
            interval=scene['interval'];require(interval==commands[interval['fixture_offset']],'actual speech interval association')
            require(scene['complete_body_holds'],'actual complete holds')
            for hold in scene['complete_body_holds']:
                frame=hold['frame'];capture=photos[frame]
                require(interval['start']+20<frame<interval['returned']-4,'hold inside actual speech interval')
                require(hold['capture']==capture['path'] and hold['sha256']==capture['PNG_sha256']==sha(Path(hold['capture']).read_bytes()),'actual capture association/hash')
                require(hold['complete_black_ASCII_gray_CP932_gray_masks_equal'] and hold['native_page']==1,'actual complete body/palette')
                require(hold['original_FE_absent_nameplate_preserved'] is is_FE and hold['complete_name_mask_equal'] is (not is_FE),'distinct actual FE/progressive header')
def apply_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Rafael12-B45-editorial-release-v1' and len(conf['manuscripts'])==1 and conf['proofs']==proofs(),'single sealed manuscript/proof configuration')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'] and sha(Path(conf['parent_ROM']).read_bytes())==conf['parent_ROM_sha256'],'clean/current parent ROM')
    validate_runtime(image);arm=image.read_file('/__arm9__.bin')
    require({path:sha(value) for _,path,value in image.iter_files()}==conf['predecessor_file_hashes'] and {path:sha(value) for path,value in image.iter_components()}==conf['predecessor_component_hashes'],'complete predecessor files/components')
    mapping,seal=load(conf['reference_map']),load(conf['reference_approval'])
    require(conf['required_map_flags']==FLAGS and mapping['format']=='dk4-Rafael12-B45-source-relocation-map-v1' and all(mapping[k] is True for k in FLAGS),'all sealed map flags')
    require(mapping['source_ROM']==conf['parent_ROM'] and mapping['source_ROM_sha256']==conf['parent_ROM_sha256'] and mapping['clean_ROM_sha256']==conf['clean_ROM_sha256'],'source/current map identity')
    require(len(mapping['groups'])==1 and mapping['groups'][0]['block']==45 and mapping['groups'][0]['route']==0 and mapping['groups'][0]['file_path']==PATHS[0] and mapping['groups'][0]['external_references_complete'],'one original Rafael entry')
    require(seal['all12_five_gates_andexact_references_approved'] and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'reference approval seal')
    data={k:load(path) for k,path in conf['proofs'].items()}
    packet,native,stored,controls,actual,later,approval,rng,policy,names,branches,loader,census=[data[k] for k in [
        'source_context','native_font_proof','native_stored_proof','relocated_control_proof','actual_proof','later_scope_proof','actual_approval','RNG_scope_proof',
        'native_policy_validation','speaker_name_review','source_branch_proof','native_loader_proof','native_caller_proof']]
    require(len(native['records'])==12 and native['fresh_compiled_alignment_cases']==48 and native['complete_progressive_pages']==11 and native['complete_FE_logical_andphysical_pages']==1,'complete native paragraph coverage')
    require(len(stored['records'])==12 and stored['fresh_native_alignment_cases']==28 and stored['exact_reused_native_alignment_cases']==20 and len(stored['fresh_parity_tail_records'])==7 and stored['all12_native_ink_planes_exact_to_already_viewed'],'complete stored coverage/tails')
    require(policy['positive_count']==len(policy['positive_cases'])==12 and policy['negative_count']==len(policy['negative_cases'])==159 and all(r['rejected'] and r['expected_guard'] in r['error'] for r in policy['negative_cases']),'actual-changing policy guards')
    require(len(approval['directly_viewed_sheets'])==7 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['directly_viewed_sheets']),'direct actual visual review')
    require(names['full207_name_role_alias_review_active'] and {r['actor_ID']:r['name'] for r in names['records']}=={0:'Rafael Castor',6:'Julio Erneco'} and all(r['actual_B45_progressive_headers_verified'] for r in names['records']),'scoped names andbroader review limits')
    require(loader['fresh_native_whole_loads_andcache_hits']==343 and loader['fresh_initial_parent_modes']==686 and census['only_original24070_interpreter_call_no_literal_alias'] and len(census['all_command_maps'])==24 and len(census['relative_operand_maps'])==5,'all original loader/caller/reference paths')
    require(len(controls['final_dispatches'])==12 and len(controls['relocated_relative_fixups'])==5 and sum(len(r['cases']) for r in controls['relocated_relative_cases'])==25 and len(controls['normal_seeded_ends'])==25,'original dispatch/relative/end coverage')
    require(all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in controls['normal_seeded_ends']),'native seeded normal value carry')
    require(controls['relocated_predicate']['native_result']==[2,1,0,0,0,0] and controls['resource_boundaries_not_executed_effects_orcontract_payment'],'original predicate andresource limits')
    require(len(later['groups'])==1 and later['groups'][0]['route']==0,'one measured comparison group')
    measured=summary(later['groups'][0])
    require(measured==mapping['observed_comparison_contract'] and measured==dict(source_English_exits=[6653,6653],command_difference_rows=21,duration_difference_rows=7,
        later_RGB_differences=0,later_samples=157,five_component_equality={k:True for k in ['state','models','persistent_objects','tasks','calendar']},whole_actor_equality=True,final_PRNG_seeds=[2420418440,1937175841]),'complete measured timing/RNG/components/RGB limits')
    require(rng['source_andEnglish_final_seeds']==measured['final_PRNG_seeds'] and rng['English_exactly_one_LCG_step_ahead_at_end_andfinal'] and rng['exact_random_state_andfuture_random_outcome_equality_NOT_verified'] and rng['no_fresh_every_RNG_call_caller_trace_orcomplete_causal_equivalence_claim'],'preserve real RNG difference andlimits')
    require(len(later['groups'][0]['later_full_RGB_comparisons'])==157 and all(r['whole_RGB_equal'] for r in later['groups'][0]['later_full_RGB_comparisons']),'all later actual RGB pairs')
    manuscript=conf['manuscripts'][0];doc=load(manuscript);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and doc['formatting_review_pending'] is False,'complete natural-dialogue-v2 approval')
    require(doc['file_path']==PATHS[0] and doc['route']==0 and doc['route_identity']=='Rafael' and doc['block']==45,'complete source document route/file/block identity')
    require(doc['current_ROM']==conf['parent_ROM']==packet['current_ROM'] and doc['current_ROM_sha256']==conf['parent_ROM_sha256']==packet['current_ROM_sha256'],'complete source document parent identity')
    require(doc['current_ARM9_sha256']==packet['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==packet['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'complete source document runtime identity')
    require(doc['complete_clean_glosses_precede_current_comparison'] is True,'clean glosses before current comparison')
    header_group=mapping['groups'][0];header_packet=packet['groups'][0]
    current_header=IlnkContainer.parse(image.read_file(PATHS[0])).blocks[45][:8].hex()
    require(header_group['source_header_hex']==header_packet['current_header_hex']==current_header,'complete predecessor header metadata')
    require(header_group['approved_manuscript_sha256']==doc['native_approved_manuscript_sha256']==sha(Path(doc['native_approved_manuscript']).read_bytes()),'approved manuscript map lineage')
    require(seal['manuscript_sha256']==sha(Path(manuscript).read_bytes()) and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed manuscript identity')
    bindings=contract()['record_bindings'];rows=doc['records']
    require(len(rows)==12 and {r['id'] for r in rows}==set(bindings) and len({r['id'] for r in rows})==12,'complete unique approved records')
    require(sum(r['decision']=='revision' for r in rows)==7 and sum(r['decision']=='retention' for r in rows)==5,'seven revisions/five contextual retentions')
    check_actual(actual,load(SOURCE_FONT),native,names,rows)
    source=image.read_file(PATHS[0]);require(sha(source)==mapping['source_archive_sha256']==packet['current_archive_sha256'],'complete predecessor archive')
    clean=NdsImage.open(conf['clean_ROM']);japanese=clean.read_file(PATHS[0])
    blocks=IlnkContainer.parse(source).blocks;cleanblocks=IlnkContainer.parse(japanese).blocks;targetblocks=list(blocks)
    require(len(blocks)==len(cleanblocks)==343,'complete SC0 archive')
    sources={r['id']:r for r in packet['records']};fonts={r['id']:r for r in native['records']};stores={r['id']:r for r in stored['records']}
    for row in rows:
        ident=row['id'];b=bindings[ident];before=sources[ident];font=fonts[ident];store=stores[ident]
        require(row['route']==0 and row['route_identity']=='Rafael' and row['file_path']==PATHS[0] and row['block']==45 and row['source_selector']==b['source_selector'] and row['kind']==b['source_kind'],'individual source identity:'+ident)
        require(row['speaker']=={0:'Rafael',6:'Julio',254:'System information panel'}[row['source_selector']],'individual source speaker label:'+ident)
        require(row['source_hex']==before['source_hex']==b['compiler_source_hex'] and row['current_hex']==before['current_hex'] and row['source_reference']==before['source_reference'] and row['current_reference']==before['current_reference'],'individual exact source/current:'+ident)
        require(row['source_meaning']==before['fresh_clean_source_gloss'] and row['context']==before['full_source_exchange_context'] and row['source_Japanese']==before['source_Japanese'],'individual source gloss/context:'+ident)
        require(row['review']=={g:True for g in ['source','context','localization','naturalness','formatting']} and row['whole_exchange_situation_voice_andprogression_reviewed'] and row['localization_note'] and row['editorial_finding'] and (row['decision']!='retention' or row['retention_reason']),'individual review andretention reason:'+ident)
        require(row['english']==b['planning_record']['english'] and row['logical_English']==font['logical_English'],'exact reviewed prose:'+ident)
        profile=profile_for(arm,blocks[45],ident,PATHS[0],b['consumer'])
        encoded=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==font['compiled_hex']==b['compiled_hex'] and qa==row['base_QA_report'],'compiled text/QA:'+ident)
        require(row['qa_waivers']==[] and row['qa_waiver_reason'] is None and row['row_count_reason']==b['row_count_reason'] and row['native_page_count']==1,'individual display reasons:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(bytes.fromhex(row['current_hex']))%2
        if pad:value+=b' '
        expected=value[1:].replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        require(value.hex()==row['stored_target_hex']==store['stored_hex'] and pad==row['stored_parity_space']==store['compiler_owned_parity_space'] and expected.hex()==store['expanded_stored_hex'] and b'%' not in value[1:],'exact stored parity/substitution/percent:'+ident)
        pipeline=store['complete_native_stored_proof']['native_alignment']
        require(len(pipeline['cases'])==4 and all(r['output_hex']==expected.hex() for r in pipeline['cases']),'stored original macro/literal alignments:'+ident)
        if row['source_selector']==254:require(all(r['null_source_actor'] for r in pipeline['cases']),'original null-actor FE macros')
        require(len(font['pages'])==1 and all(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] for page in font['pages']),'complete native ink:'+ident)
        require(row['target_reference']==store['target_reference']|{'block':45} and row['actual_record_observed'] is True,'final exact target/actual references:'+ident)
    group=mapping['groups'][0]
    targetblocks[45]=reconstruct(blocks[45],cleanblocks[45],group,packet['groups'][0],rows,branches['operands_requiring_adjustment_when_resizing'])
    payload=IlnkContainer(targetblocks).to_bytes()
    require(sha(payload)==mapping['target_archive_sha256']==conf['archives'][0]['target_sha256'],'complete reconstructed target archive')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'],'research reference ROM identity')
    reference=NdsImage.open(conf['reference_ROM']);require(payload==reference.read_file(PATHS[0]),'pinned approved reference archive')
    require([i for i,(a,b) in enumerate(zip(blocks,targetblocks,strict=True)) if a!=b]==[45],'only owned B45 block changes')
    require(all(reference.read_file(path)==value for _,path,value in image.iter_files() if path not in PATHS) and all(reference.read_file(path)==value for path,value in image.iter_components()),'all other files/components unchanged')
    restored=list(targetblocks);restored[45]=blocks[45];require(IlnkContainer(restored).to_bytes()==source,'complete predecessor archive inverse')
    files=list(image.rom.files);index=image.path_map()[PATHS[0]];files[index]=payload
    require([i for i,(a,b) in enumerate(zip(image.rom.files,files,strict=True)) if a!=b]==[index],'one SC0 file slot')
    changes=[dict(id=r['id'],file_path=PATHS[0],block=45,old_offset=r['current_reference']['offset'],new_offset=r['target_reference']['offset']) for r in rows]
    commit_files(image,files)
    return dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,
        files=[dict(file_path=PATHS[0],source_sha256=sha(source),target_sha256=sha(payload),changed_records=changes)],
        one_files_list_commit_after_all_gates=True,complete_clean_predecessor_block_andarchive_inverse_exact=True,
        all12_original_sixbyte_preambles_source00_FE_macros24commands5relative_sites_preserved=True,
        all12_actual_eachlanguage_andRNG_one_step_limits_preserved=True,full_goal_complete=False)
