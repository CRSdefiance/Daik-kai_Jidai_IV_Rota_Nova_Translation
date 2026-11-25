"""Validate the complete mixed B46 exchange before one atomic archive commit."""
import json
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.rafael_B46_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue import rafael_B46_layout_v1 as codec
from dk4tool.dialogue.rafael_B46_choices_v1 import compile_choices
from dk4tool.patch.rafael_B46_reconstruction_v1 import reconstruct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B46_release_paths_v7958 import FLAGS,proofs,RELOCATION,DRAFT
from scripts.seal_Rafael_B46_references_v7958 import summary

CONFIG='translations/rafael_B46_editorial_release_v2.json'
PATH='/data/SC0.DK4'
def load(path):return json.loads(Path(path).read_bytes())
def require(value,label):
    if not value:raise ValueError('Rafael B46 editorial contract: '+label)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
def commit_files(image,files):image.rom.files=files

def check_actual(actual,sourcefont,native,names,rows):
    require(not actual['unresolved'] and len(actual['groups'])==4,'four complete actual groups')
    require({(g['version'],g['choice']) for g in actual['groups']}=={(v,c) for v in ['clean_Japanese','English'] for c in ['accept','decline']},'both choices each language')
    require(actual['actual_normal_type0_value0_accept_value1_decline_carry_both_languages'] and actual['original_ten_command_B44_ROM_entry_fixture_not_natural_B46_activation_original_location_orfull_route'],'normal carry anddisclosed fixture')
    require(sum(g['complete_body_holds'] for g in actual['groups'])==214 and sum(g['complete_progressive_header_holds'] for g in actual['groups'])==142 and sum(g['complete_FE_absent_header_holds'] for g in actual['groups'])==72,'complete body/name/FE hold counts')
    wanted={r['id'] for r in rows}
    require(len(sourcefont['source_records'])==24 and {r['id'] for r in sourcefont['source_records']}==wanted,'complete unique independent source font records')
    require(len(native['records'])==24 and {r['id'] for r in native['records']}==wanted,'complete unique native font records')
    expected_names={r['actor_ID']:r['name'] for r in names['records']}
    unions={v:set() for v in ['clean_Japanese','English']};commands_union={v:set() for v in unions}
    for g in actual['groups']:
        selected=0 if g['choice']=='accept' else 1;version=g['version'];fixture=g['fixture']
        count=22 if selected==0 else 7;command_count=43 if selected==0 else 28
        require(g['route']==fixture['route']==0 and fixture['source_block']==46 and fixture['fixture_block']==44,'actual original route/block')
        require(g['actual_unique_speeches']==len(g['speech_observations'])==count and len({s['id'] for s in g['speech_observations']})==count,'unique actual path speeches')
        require(not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows'] and not g['unreturned_following_dialogues'],'complete actual scope')
        expected_exit={('clean_Japanese','accept'):9295,('English','accept'):9294,('clean_Japanese','decline'):5695,('English','decline'):5696}[(version,g['choice'])]
        require(g['exit_frame']==expected_exit and g['native_terminal_result']==[0,selected] and len(g['command_pairs'])==command_count and g['observed_original_exchange_commands']==command_count-10,'actual full path andnormal result')
        require(g['actual_menu_pair']['native_result']==[2,selected] and g['actual_menu_pair'] in g['command_pairs'],'actual original menu result')
        for k in ['capture_report','observer_report']:require(sha(Path(g[k]).read_bytes())==g[k+'_sha256'],'actual report/trace hash')
        report,trace=load(g['capture_report']),load(g['observer_report'])
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and report['frames']==16001 and not report['hardware_device_verification'],'actual cold-boot limits')
        require(not any(v for k,v in report.items() if k.startswith('synthetic_')),'no synthetic state inputs')
        require(report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()),'fixture ROM identity')
        require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'read-only observer scope')
        photos={p['frame']:p for p in report['frames_captured']};expected={p['offset']:p for p in fixture['all_fixture_commands']}
        require(len(expected)==47 and len(fixture['all_original_exchange_commands'])==37 and len(fixture['original_text_records'])==24,'all original fixture commands')
        require(fixture['no_original_speech_branch_resource_effect_orend_omitted'],'full original fixture preserved')
        paired={p['fixture_offset']:p for p in g['command_pairs']};previous_next=None
        for pair in g['command_pairs']:
            before,after=trace['rows'][pair['entry_row']],trace['rows'][pair['return_row']]
            require(before['kind']=='before_command' and after['kind']=='after_command' and after['entry_row']==pair['entry_row'],'actual entry/return association')
            require(before['frame']==pair['start'] and after['frame']==pair['returned'] and after['decoded_length']==pair['decoded_length'] and after['result_words']==pair['native_result'],'actual result/timing association')
            at=pair['fixture_offset'];command=expected[at];word=command['word']
            require(before['source']['instruction_offset']==after['source']['instruction_offset']==at and before['source']['first_word']==word==pair['word'],'actual command source offset/opcode')
            for observed in [before,after]:
                resident=observed['source']
                require(resident['classification']=='original_SC_cache' and resident['route']==0 and resident['block']==44,'actual cache route/block')
                require(resident['actual_sha256']==resident['registered_sha256']==fixture['fixture_block_sha256'] and resident['payload_bytes']==fixture['fixture_stored_bytes'],'actual resident fixture identity')
                require(resident['instruction_pointer']==resident['payload_address']+at and sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256'],'actual resident payload/entry')
                require(resident['whole_resident_payload_exact_ROM'] and observed['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],'resident callback integrity')
            if previous_next is not None:require(at==previous_next,'actual original conditional flow')
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');last=pair['observed_previous_result']
                taken=word==0x100 or word==0x200 and last==0 or word==0x300 and last==1 or word==0x400 and last==2
                require(pair['decoded_length']==4+(span if taken else 0),'actual original relative branch')
            else:require(pair['decoded_length']==command['native_extent'],'actual complete native extent')
            previous_next=at+pair['decoded_length']
            if pair['exchange_command_ordinal'] is not None:commands_union[version].add(pair['exchange_command_ordinal'])
        require(g['command_pairs'][-1]['native_result']==[0,g['command_pairs'][-2]['native_result'][1]]==[0,selected],'normal end retains original value')
        for scene in g['speech_observations']:
            unions[version].add(scene['id']);row=next(r for r in rows if r['id']==scene['id']);is_FE=row['source_selector']==254
            require(scene['source_selector']==row['source_selector'] and scene['kind']==row['kind'] and scene['native_page_count']==1 and not scene['incomplete_sampled_holds'],'actual individual speaker/page')
            require(scene['actual_name']==(None if is_FE else expected_names[row['source_selector']]),'actual source-bound name')
            model=next(r for r in (sourcefont['source_records'] if version=='clean_Japanese' else native['records']) if r['id']==row['id'])
            require(scene['native_plane']==model['pages'][0]['native_plane'] and scene['native_plane_sha256']==model['pages'][0]['native_plane_sha256']==sha(Path(scene['native_plane']).read_bytes()),'actual independent native plane')
            interval=scene['interval'];require(interval==paired[interval['fixture_offset']] and scene['complete_body_holds'],'actual speech interval/holds')
            for hold in scene['complete_body_holds']:
                frame=hold['frame'];require(frame in photos and interval['start']+20<frame<interval['returned']-4,'hold inside actual speech interval')
                capture=photos[frame]
                require(hold['capture']==capture['path'] and hold['sha256']==capture['PNG_sha256']==sha(Path(hold['capture']).read_bytes()),'actual capture association/hash')
                require(hold['complete_black_ASCII_gray_CP932_gray_masks_equal'] and hold['native_page']==1,'actual complete body/palette')
                require(hold['original_FE_absent_nameplate_preserved'] is is_FE and hold['complete_name_mask_equal'] is (not is_FE),'distinct actual FE/progressive header')
    require(all(s==wanted for s in unions.values()) and all(s==set(range(37)) for s in commands_union.values()),'all24 speech/all37 command union each language')

def check_menu(menu,actual):
    require(not menu['unresolved'] and len(menu['groups'])==4,'four complete actual menus')
    require(menu['source_highlight_off_samples']==[dict(version='clean_Japanese',choice='accept',frame=4930,logical_selected_option=0)] and menu['exact_cross_language_highlight_phase_equality_not_claimed'],'preserve original highlight-off phase')
    require(menu['all_owned_caption_backing_matches_independent_CP932_ASCII_font_oracle'] and menu['all24_visible_source_English_label_samples_full_first_internal_final_glyphs_bounds_andnative_backgrounds_exact'],'complete owned backing/visible labels')
    seen=set()
    for g in menu['groups']:
        version,choice=g['version'],g['choice'];selected=0 if choice=='accept' else 1
        require((version,choice) not in seen,'unique actual menu group');seen.add((version,choice))
        require(g['menu_native_result']==[2,selected] and any(a['version']==version and a['choice']==choice and a['actual_menu_pair']['native_result']==g['menu_native_result'] for a in actual['groups']),'actual menu path association')
        require(g['actual_physical_backing']==[256,36] and g['actual_caption_view']==([84,12] if version=='clean_Japanese' else [66,12]),'original backing andprovider width')
        require(g['original_native_menu_rectangle']==([70,64,186,128] if version=='clean_Japanese' else [79,64,177,128]),'original two-option rectangle')
        require(len(g['samples'])==3 and [s['frame'] for s in g['samples']]==[4810,4870,4930],'all original snapshot samples')
        require(g['independent_current_font_owned_backing_andall_visible_pixels_equal'],'independent backing equality')
        for sample in g['samples']:
            require(sample['actual_owned_pixels_sha256']==sample['independent_owned_pixels_sha256'] and sample['no_claim_that_unowned_backing_is_blank_oridentical'],'owned backing/no unowned equality claim')
            require(len(sample['labels'])==2 and [l['option_index'] for l in sample['labels']]==[0,1],'both visible labels')
            for i,label in enumerate(sample['labels']):
                require(label['full_visible_black_glyph_mask_andblank_guards_equal'] and label['exact_native_background_pixels_equal'],'complete visible glyphs/background')
                require(label['caption_size']==g['actual_caption_view'] and label['caption_origin']==[g['original_native_menu_rectangle'][0]+16,272+20*i],'original caption origin/size')
                require(label['selected_highlight_visible'] is (sample['visible_selected_option_index']==i),'measured visible highlight phase')
    require(seen=={(v,c) for v in ['clean_Japanese','English'] for c in ['accept','decline']},'both menu paths each language')

def apply_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Rafael26-B46-editorial-release-v1' and len(conf['manuscripts'])==2 and conf['proofs']==proofs(),'sealed mixed speech/menu configuration')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'] and sha(Path(conf['parent_ROM']).read_bytes())==conf['parent_ROM_sha256'],'clean/current parent ROM')
    validate_runtime(image);arm=image.read_file('/__arm9__.bin')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'complete predecessor files/components')
    mapping,seal=load(conf['reference_map']),load(conf['reference_approval'])
    require(conf['required_map_flags']==FLAGS and mapping['format']=='dk4-Rafael26-B46-source-relocation-map-v1' and all(mapping[k] is True for k in FLAGS),'all sealed map flags')
    require(mapping['source_ROM']==conf['parent_ROM'] and mapping['source_ROM_sha256']==conf['parent_ROM_sha256'] and mapping['clean_ROM_sha256']==conf['clean_ROM_sha256'],'source/current map identity')
    require(seal['all26_five_gates_andexact_references_approved'] and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'reference seal')
    data={k:load(path) for k,path in conf['proofs'].items()}
    packet,native,stored,controls,actual,later,approval,rng,policy,names,branches,loader,census=[data[k] for k in [
        'source_context','native_font_proof','native_stored_proof','relocated_control_proof','actual_proof','later_scope_proof','actual_approval',
        'RNG_scope_proof','native_policy_validation','speaker_name_review','source_branch_proof','native_loader_proof','native_caller_proof']]
    frozen=contract();require(data['native_contract']==frozen,'exact independently frozen contract')
    require(native['fresh_compiled_alignment_cases']==96 and native['complete_progressive_pages']==native['complete_FE_logical_andphysical_pages']==12,'all native paragraph alignments')
    require(stored['fresh_native_alignment_cases']==44 and stored['exact_reused_native_alignment_cases']==52 and len(stored['fresh_parity_tail_records'])==11 and stored['all24_native_ink_planes_exact_to_already_viewed'],'complete stored coverage/tails')
    require(policy['positive_speeches']==len(policy['positive_cases'])==24 and policy['positive_choice_labels']==2 and policy['positive_menu']==frozen['choice_object_hex'] and policy['negative_count']==len(policy['negative_cases'])==300 and all(r['rejected'] and r['expected_guard'] in r['error'] for r in policy['negative_cases']),'actual-changing policy guards')
    require(len(approval['directly_viewed_sheets'])==14 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['directly_viewed_sheets']),'direct actual visual review')
    require(names['full207_name_role_alias_review_active'] and {r['actor_ID']:r['name'] for r in names['records']}=={0:'Rafael Castor',5:'Claudio Manaus',6:'Julio Erneco'} and all(r['actual_B46_progressive_nameplate_verified'] for r in names['records']),'scoped names/broader limits')
    require(loader['fresh_native_whole_loads_andcache_hits']==343 and loader['fresh_initial_parent_modes']==686 and census['only_original24070_interpreter_call_no_literal_alias'] and len(census['all_command_maps'])==37 and len(census['relative_operand_maps'])==4,'all original loader/caller paths')
    require(len(controls['final_dispatches'])==24 and sum(len(r['cases']) for r in controls['relocated_relative_cases'])==20 and len(controls['normal_seeded_ends'])==25,'original final dispatch/relative/end coverage')
    require(all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in controls['normal_seeded_ends']),'native seeded normal value carry')
    require(controls['all_five_A000630061FF_andcomplete_normal_end_exact'] and controls['exact_two_choices_andboth_even_header_alignments_bound'],'all nontext controls/typed menu alignment')
    require(data['stored_menu_proof']['stored_menu_hex']==frozen['choice_object_hex'] and data['stored_menu_proof']['all8_current_target_style_planes_reused_by_exact_label_andwidth'],'complete stored menu labels')
    require(len(later['groups'])==len(rng['groups'])==2 and [summary(g) for g in later['groups']]==mapping['observed_comparison_contract'],'all measured comparison metadata')
    for i,g in enumerate(later['groups']):
        is_accept=i==0;expected_choice='accept' if is_accept else 'decline';r=rng['groups'][i]
        require(g['choice']==expected_choice and g['source_English_exits']==([9295,9294] if is_accept else [5695,5696]),'measured path exits')
        require(len(g['command_comparison_differences'])==(27 if is_accept else 12) and len(g['duration_differences'])==(6 if is_accept else 2),'all measured timing differences')
        require(g['final_PRNG_seeds']==r['final_seeds']==([1622437796,3229979821] if is_accept else [3730749937,3562773357]),'actual final RNG differences')
        require(g['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=not is_accept) and g['whole_actors_equal'] is False,'actual later component/calendar/actor differences')
        require(len(g['later_RGB_differences'])==r['later_RGB_differences']==(41 if is_accept else 96) and len(g['later_full_RGB_comparisons'])==g['later_sample_count']==r['later_samples']==(113 if is_accept else 173),'all later RGB measurements')
        require(g['all_original_initializer_andexchange_results_equal'] and g['all_UI_request_words_equal'] and g['all_measured_whole_upper_scene_portrait_andheader_RGB_equal'],'selected results/UI/scenes equal')
        require(r['same_initial_seed']==848781860 and r['exit_English_phase']==1 and r['final_English_phase']==(-159 if is_accept else -316),'bounded measured RNG phases')
        require(r['first_observed_phase_difference']['word']==0x2100 and r['first_observed_phase_difference']['source_duration']==232 and r['first_observed_phase_difference']['English_duration']==234,'first measured menu phase difference')
    require(rng['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified'] and rng['all_raw_measurements_kept_for_later_older_record_technical_reaudit'] and rng['earlier_contract_reused_only_for_exact_unchanged_code_not_fresh_every_call_causal_trace'],'future-state/causal/re-audit limits')
    doc,menu=[load(p) for p in conf['manuscripts']];validate_approved_batch(doc)
    require(menu['translation_policy']=='natural-dialogue-v2' and menu['encoder']=='typed-menu-relocatable-v1' and menu['target_locale']=='en-US' and menu['records']==doc['typed_choice_records'],'separate exact two-choice manifest')
    require(seal['manuscript_sha256']==sha(Path(conf['manuscripts'][0]).read_bytes()) and seal['choice_manuscript_sha256']==sha(Path(conf['manuscripts'][1]).read_bytes()),'sealed mixed manuscript identities')
    require(doc['native_approved_manuscript']==str(DRAFT) and doc['native_approved_manuscript_sha256']==approval['manuscript_sha256']==sha(DRAFT.read_bytes()),'approved manuscript lineage')
    require(doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and doc['current_ROM']==conf['parent_ROM']==packet['current_ROM'] and doc['current_ROM_sha256']==conf['parent_ROM_sha256']==packet['current_ROM_sha256'],'complete map/parent references')
    require(doc['current_ARM9_sha256']==packet['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==packet['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'complete document runtime identity')
    rows=doc['records'];choices=doc['typed_choice_records']
    require(sum(r['decision']=='revision' for r in rows+choices)==7 and sum(r['decision']=='retention' for r in rows+choices)==19,'seven revisions/nineteen retentions')
    check_actual(actual,data['source_font_proof'],native,names,rows);check_menu(data['actual_menu_proof'],actual)
    source=image.read_file(PATH);require(sha(source)==mapping['source_archive_sha256']==packet['current_archive_sha256'],'complete predecessor archive')
    blocks=IlnkContainer.parse(source).blocks;cleanblocks=IlnkContainer.parse(NdsImage.open(conf['clean_ROM']).read_file(PATH)).blocks
    require(len(blocks)==len(cleanblocks)==343 and len(mapping['groups'])==1,'complete one-block archive scope')
    group=mapping['groups'][0];require(group['block']==46 and group['route']==0 and group['file_path']==PATH and group['external_references_complete'],'one original Rafael entry')
    original=load(RELOCATION)['groups'][0]
    require(original['external_references_complete'] is False and group['external_references_complete'] is True,'pending relocation promoted only after complete census seal')
    require(all(group.get(k)==v for k,v in original.items() if k!='external_references_complete'),'exact independently reconstructed relocation')
    require(group['command_map']==census['all_command_maps'] and group['relative_fixups']==census['relative_operand_maps'],'complete census associations')
    fonts={r['id']:r for r in native['records']};stores={r['id']:r for r in stored['records']};dispatch={r['id']:r for r in controls['final_dispatches']}
    require(len(stores)==len(stored['records'])==24 and set(stores)==set(fonts)==set(dispatch)==set(frozen['record_bindings']),'all individual proof IDs')
    for row in rows:
        ident=row['id'];b=frozen['record_bindings'][ident];font=fonts[ident];store=stores[ident];ref=next(r for r in group['text_records'] if r['id']==ident)
        profile=profile_for(arm,blocks[46],ident,PATH,b['consumer'])
        encoded=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile);qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==font['compiled_hex']==b['compiled_hex'] and qa==row['base_QA_report'],'compiled text/QA:'+ident)
        require(row['qa_waivers']==[] and row['qa_waiver_reason'] is None and row['row_count_reason']==load(DRAFT)['records'][rows.index(row)]['row_count_reason'] and row['native_page_count']==1,'individual original display reasons:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(bytes.fromhex(row['current_hex']))%2
        if pad:value+=b' '
        require(value.hex()==row['stored_target_hex']==store['stored_hex']==dispatch[ident]['final_stored_hex'] and pad==row['stored_parity_space']==store['compiler_owned_parity_space'],'exact stored parity:'+ident)
        require(value[1:].hex()==store['expanded_stored_hex'] and b'%' not in value[1:] and all(token not in value[1:] for token in [b'FI',b'FA',b'FO']),'no added macro/printf conversion:'+ident)
        pipeline=store['complete_native_stored_proof']['native_alignment']
        require(len(pipeline['cases'])==4 and all(r['output_hex']==value[1:].hex() for r in pipeline['cases']),'all stored native alignments:'+ident)
        require(len(font['pages'])==1 and all(sha(Path(pg['native_plane']).read_bytes())==pg['native_plane_sha256'] for pg in font['pages']),'complete native ink:'+ident)
        require(row['target_reference']==dict(block=46,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index']) and row['actual_record_observed'],'final speech reference/actual approval:'+ident)
    typed=compile_choices(choices)
    for row,ref in zip(choices,group['choice_commands'][0]['label_references'],strict=True):
        require(row['target_reference']==dict(block=46,command_offset=242,offset=ref['new_offset'],bytes=ref['new_length'],relative_table_field=ref['relative_table_field'],relative_base=ref['relative_base'],relative_offset=ref['relative_offset'],record_index=ref['new_record_index']) and row['actual_record_observed'],'final choice reference/actual approval')
    targetblocks=list(blocks)
    targetblocks[46]=reconstruct(blocks[46],cleanblocks[46],group,packet['groups'][0],rows,branches['operands_requiring_adjustment_when_resizing'],choices,typed)
    payload=IlnkContainer(targetblocks).to_bytes()
    require(sha(payload)==mapping['target_archive_sha256']==conf['archives'][0]['target_sha256'],'complete reconstructed target archive')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'],'research reference ROM identity')
    reference=NdsImage.open(conf['reference_ROM']);require(payload==reference.read_file(PATH),'whole approved reference archive')
    require([i for i,(a,b) in enumerate(zip(blocks,targetblocks,strict=True)) if a!=b]==[46],'only owned B46 block')
    require(all(reference.read_file(p)==v for _,p,v in image.iter_files() if p!=PATH) and all(reference.read_file(p)==v for p,v in image.iter_components()),'all other files/components unchanged')
    restored=list(targetblocks);restored[46]=blocks[46];require(IlnkContainer(restored).to_bytes()==source,'complete archive inverse')
    files=list(image.rom.files);index=image.path_map()[PATH];files[index]=payload
    require([i for i,(a,b) in enumerate(zip(image.rom.files,files,strict=True)) if a!=b]==[index],'one SC0 file slot')
    changes=[dict(id=r['id'],file_path=PATH,block=46,kind=r['kind'],old_offset=r['current_reference']['offset'],new_offset=r['target_reference']['offset']) for r in rows+choices]
    require(len(changes)==len({r['id'] for r in changes})==26,'all26 unique manifest changes')
    commit_files(image,files)
    return dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,
        files=[dict(file_path=PATH,source_sha256=sha(source),target_sha256=sha(payload),changed_records=changes)],
        one_files_list_commit_after_all_gates=True,complete_clean_predecessor_block_andarchive_inverse_exact=True,
        all24_preambles12_FE_source00_two_choices37_commands4_relatives_preserved=True,
        both_actual_paths_andall_highlight_timing_RNG_simulation_limits_preserved=True,full_goal_complete=False)
