"""Validate complete B50 prose, controls and representative actual evidence before one commit."""
HISTORICAL_B47_FINAL_SEED_LITERALS=(19668379,4016462114)
import json
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.rafael_B50_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue import rafael_B50_layout_v1 as codec
from dk4tool.patch.rafael_B50_reconstruction_v1 import reconstruct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B50_release_paths_v8164 import FLAGS,proofs,RELOCATION,DRAFT
from scripts.seal_Rafael_B50_references_v8164 import summary

from dk4tool.patch.rafael_B50_risk_v1 import check_bounded_risk
CONFIG='translations/rafael_B50_editorial_release_v1.json'
PATH='/data/SC0.DK4'
UNVISITED=[]

def load(path):return json.loads(Path(path).read_bytes())
def require(value,label):
    if not value:raise ValueError('Rafael B50 editorial contract: '+label)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
def commit_files(image,files):image.rom.files=files

def check_actual(actual,sourcefont,native,names,rows,packet,flow,focus):
    require(not actual['unresolved'] and len(actual['groups'])==2 and {g['version'] for g in actual['groups']}=={'clean_Japanese','English'},'two complete actual groups')
    require(actual['actual_normal_type0_value0_carry_both_languages'] and actual['original_ten_command_B44_ROM_entry_fixture_not_natural_B50_activation_original_location_orfullroute'],'normal carry/disclosed fixture')
    require(actual['native_only_unvisited_speech_IDs']==UNVISITED,'no unvisited B50 speeches')
    require(sum(g['complete_body_holds'] for g in actual['groups'])==184 and sum(g['complete_progressive_header_holds'] for g in actual['groups'])==184 and sum(g['complete_FE_absent_header_holds'] for g in actual['groups'])==0,'complete actual body/name hold counts')
    wanted={r['id'] for r in rows};observed=wanted-set(UNVISITED)
    require(len(sourcefont['source_records'])==28 and {r['id'] for r in sourcefont['source_records']}==wanted,'complete unique source font records')
    require(len(native['records'])==28 and {r['id'] for r in native['records']}==wanted,'complete unique native font records')
    expected_names={r['actor_ID']:r['name'] for r in names['records']}
    require(len(flow['groups'])==1 and flow['groups'][0]['block']==50 and flow['groups'][0]['commands']==packet['groups'][0]['all_source_commands'] and len(flow['groups'][0]['records'])==28,'complete linear source scope')
    for g in actual['groups']:
        version=g['version'];fixture=g['fixture']
        require(g['route']==fixture['route']==0 and fixture['source_block']==50 and fixture['fixture_block']==44,'actual original route/block')
        require(g['actual_unique_speeches']==len(g['speech_observations'])==28 and {s['id'] for s in g['speech_observations']}==observed,'actual selected all twentyeight speeches')
        require(g['native_only_unvisited_speech_IDs']==UNVISITED and not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows'] and g['complete_first_exchange_distinguished_from_later_fixture_reentry'] and not g['unreturned_following_dialogues'] and not g['later_fixture_reentry_frames'],'explicit actual/offline scope')
        require(g['exit_frame']==(10822 if version=='clean_Japanese' else 10824) and g['native_terminal_result']==[0,0] and len(g['command_pairs'])==47 and g['observed_original_exchange_commands']==37,'actual selected path and normal result')
        for k in ['capture_report','observer_report']:require(sha(Path(g[k]).read_bytes())==g[k+'_sha256'],'actual report/trace hash')
        report,trace=load(g['capture_report']),load(g['observer_report'])
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and report['frames']==16001 and not report['hardware_device_verification'],'actual cold-boot limits')
        require(not any(v for k,v in report.items() if k.startswith('synthetic_')),'no synthetic state inputs')
        require(report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()),'fixture ROM identity')
        require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'readonly observer scope')
        photos={p['frame']:p for p in report['frames_captured']};expected={p['offset']:p for p in fixture['all_fixture_commands']}
        require(len(expected)==47 and len(fixture['all_original_exchange_commands'])==37 and len(fixture['original_text_records'])==28,'all original fixture commands')
        require(fixture['no_original_speech_branch_resource_effect_orend_omitted'] and fixture['zero_relative_sites_no_span_relocation_under_constant32_byte_shift'],'full fixture controls retained')
        paired={p['fixture_offset']:p for p in g['command_pairs']};previous_next=None
        for pair in g['command_pairs']:
            before,after=trace['rows'][pair['entry_row']],trace['rows'][pair['return_row']]
            require(before['kind']=='before_command' and after['kind']=='after_command' and after['entry_row']==pair['entry_row'],'actual entry/return association')
            require(before['frame']==pair['start'] and after['frame']==pair['returned'] and after['decoded_length']==pair['decoded_length'] and after['result_words']==pair['native_result'],'actual result/timing association')
            at=pair['fixture_offset'];command=expected[at];word=command['word']
            original=next(((i,o) for i,o in enumerate(fixture['all_original_exchange_commands']) if o['fixture_command_offset']==at),None)
            require(pair['exchange_command_ordinal']==(None if original is None else original[0]) and pair['canonical_source_offset']==(None if original is None else packet['groups'][0]['all_source_commands'][original[0]]['offset']),'actual canonical command/source association')
            require(before['source']['instruction_offset']==after['source']['instruction_offset']==at and before['source']['first_word']==word==pair['word'],'actual command offset/opcode')
            for o in [before,after]:
                resident=o['source']
                require(resident['classification']=='original_SC_cache' and resident['route']==0 and resident['block']==44,'actual cache route/block')
                require(resident['actual_sha256']==resident['registered_sha256']==fixture['fixture_block_sha256'] and resident['payload_bytes']==fixture['fixture_stored_bytes'],'actual resident fixture identity')
                require(resident['instruction_pointer']==resident['payload_address']+at and sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256'],'actual resident payload/entry')
                require(resident['whole_resident_payload_exact_ROM'] and o['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],'resident callback integrity')
            if previous_next is not None:require(at==previous_next,'actual original conditional flow')
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');last=pair['observed_previous_result']
                taken=word==0x100 or word==0x200 and last==0 or word==0x300 and last==1 or word==0x400 and last==2
                require(pair['decoded_length']==4+(span if taken else 0),'actual original relative branch')
            else:require(pair['decoded_length']==command['native_extent'],'actual complete native extent')
            previous_next=at+pair['decoded_length']
        require(g['command_pairs'][-1]['native_result']==[0,g['command_pairs'][-2]['native_result'][1]]==[0,0],'normal end retains original value')
        focused=next(v for v in focus['groups'] if v['version']==version)
        actualcontrols=[p for p in g['command_pairs'] if p['canonical_source_offset'] is not None and p['word'] in [0x4821,0xA000,0x4720,0x4681]]
        require(focused['controls']==actualcontrols,'focused original picture/effect/departure associations')
        require([(c['word'],c['canonical_source_offset'],c['decoded_length']) for c in actualcontrols]==[(0x4821,244,4),(0xA000,340,8),(0x4720,348,2),(0x4681,1510,4)],'actual original picture/effect/departure extents')
        require([c['returned']-c['start'] for c in actualcontrols]==[60,240,0,88] and all(c['native_result']==[3,0] for c in actualcontrols),'actual original effect results/durations')
        require([expected[c['fixture_offset']]['whole_command_hex'] for c in actualcontrols]==['2148b5a8','00a0ffff0100b530','2047','81460002'],'actual complete original effect bytes')
        require(focused['original_andrepeat_all_observer_rows_exact_except_output_paths'] and focused['all_eight_capture_PNGs_framebuffers_andfinal_whole_RAM_exact_to_first_run'],'same-input focused repeat integrity')
        visited=[p['canonical_source_offset'] for p in g['command_pairs'] if p['exchange_command_ordinal'] is not None]
        require(visited==[c['offset'] for c in packet['groups'][0]['all_source_commands']] and [s['id'] for s in g['speech_observations']]==[r['id'] for r in rows],'actual all37 linear source commands/all28 speeches in order')
        count=0
        for scene in g['speech_observations']:
            row=next(r for r in rows if r['id']==scene['id'])
            model=next(r for r in (sourcefont['source_records'] if version=='clean_Japanese' else native['records']) if r['id']==scene['id'])
            pages=1
            require(scene['source_selector']==row['source_selector'] and scene['kind']==row['kind'] and scene['kind']=='progressive' and scene['native_page_count']==pages and not scene['incomplete_sampled_holds'],'actual individual speaker/page')
            require(scene['actual_name']==expected_names.get(row['source_selector']),'actual source-bound name')
            require(scene['native_planes']==[dict(path=p['native_plane'],sha256=p['native_plane_sha256']) for p in model['pages']],'actual independent page association')
            require(all(sha(Path(p['path']).read_bytes())==p['sha256'] for p in scene['native_planes']),'actual native planes hash')
            interval=scene['interval'];require(interval==paired[interval['fixture_offset']] and scene['complete_body_holds'],'actual speech interval/holds')
            pageholds=scene['actual_complete_page_holds']
            require(len(pageholds)==pages and all(pageholds) and [h for page in pageholds for h in page]==scene['complete_body_holds'],'all complete pages in order')
            require(all(all(h['native_page']==i+1 for h in holds) for i,holds in enumerate(pageholds)),'actual numbered complete page holds')
            for hold in scene['complete_body_holds']:
                frame=hold['frame'];require(frame in photos and interval['start']+20<frame<interval['returned']-4,'hold inside actual speech interval')
                photo=photos[frame]
                require(hold['capture']==photo['path'] and hold['sha256']==photo['PNG_sha256']==sha(Path(hold['capture']).read_bytes()),'actual capture association/hash')
                require(hold['complete_black_ASCII_gray_CP932_gray_masks_equal'] and hold['complete_name_mask_equal'] and hold['actual_name']==scene['actual_name'] and hold['native_geometry']==[216,64],'actual complete body/name masks and geometry')
            require(not scene['ordinary_page_transitions'],'no invented single-page transitions')
            count+=len(scene['complete_body_holds'])
        require(count==g['complete_body_holds'] and sum(s['native_page_count'] for s in g['speech_observations'])==g['actual_complete_native_pages']==28,'actual totals consistent with holds/pages')

def apply_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Rafael28-B50-editorial-release-v1' and len(conf['manuscripts'])==1 and conf['proofs']==proofs(),'sealed speech-only configuration')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'] and sha(Path(conf['parent_ROM']).read_bytes())==conf['parent_ROM_sha256'],'clean/current parent ROM')
    validate_runtime(image);arm=image.read_file('/__arm9__.bin')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'complete predecessor files/components')
    mapping,seal=load(conf['reference_map']),load(conf['reference_approval'])
    require(conf['required_map_flags']==FLAGS and mapping['format']=='dk4-Rafael28-B50-source-relocation-map-v1' and all(mapping[k] is True for k in FLAGS),'all sealed map flags')
    require(mapping['source_ROM']==conf['parent_ROM'] and mapping['source_ROM_sha256']==conf['parent_ROM_sha256'] and mapping['clean_ROM_sha256']==conf['clean_ROM_sha256'],'source/current map identity')
    require(seal['all28_five_gates_andexact_references_approved'] and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'reference seal')
    data={k:load(path) for k,path in conf['proofs'].items()}
    packet,native,stored,controls,actual,later,approval,rng,policy,names,branches,loader,census=[data[k] for k in [
        'source_context','native_font_proof','native_stored_proof','relocated_control_proof','actual_proof','later_scope_proof','actual_approval',
        'RNG_scope_proof','native_policy_validation','speaker_name_review','source_branch_proof','native_loader_proof','native_caller_proof']]
    frozen=contract();require(data['native_contract']==frozen,'exact independently frozen contract')
    require(native['fresh_compiled_alignment_cases']==20 and native['reused_compiled_alignment_cases']==92 and native['total_bound_compiled_alignment_cases']==112 and native['complete_progressive_paragraphs']==28 and native['complete_progressive_pages']==28 and native['FE_null_actor_alignment_cases']==0,'complete native paragraph alignments')
    require(stored['fresh_native_alignment_cases']==60 and stored['exact_reused_native_alignment_cases']==52 and len(stored['fresh_parity_tail_records'])==15 and stored['all28_native_ink_planes_exact_to_already_viewed'] and stored['all28_complete_stored_single_pages_exact_to_viewed'],'complete stored coverage/tails')
    require(policy['positive_count']==len(policy['positives'])==28 and policy['negative_count']==len(policy['negatives'])==511 and all(r['rejected'] and r['expected_guard'] in r['error'] for r in policy['negatives']),'actual-changing policy guards')
    require(len(approval['directly_viewed_sheets'])==14 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['directly_viewed_sheets']),'direct actual visual review')
    require(approval['native_only_unvisited_speech_IDs']==UNVISITED and approval['observed_all37_original_commands_eachlanguage_and10_initializers'] and approval['exact_two_QA_waivers18_infos_all_original_diagnostics_preserved'],'scoped actual/QA approval')
    require(names['full207_name_role_alias_review_active'] and {r['actor_ID']:r['name'] for r in names['records']}=={0:'Rafael Castor',2:'Lil Argot',9:'Camille Overijssel'},'scoped names/broader review')
    require(all(r['actual_B50_progressive_nameplate_verified'] is (r['actor_ID'] in [0,2,9]) and r['native_only_unvisited_B50_header'] is (r['actor_ID'] in []) for r in names['records']),'actual three names/no native-only headers')
    require(loader['fresh_native_whole_loads_andcache_hits']==343 and loader['fresh_initial_parent_modes']==686 and census['only_original24070_interpreter_call_no_literal_alias'] and len(census['all_command_maps'])==37 and not census['relative_operand_maps'],'all original loader/caller paths')
    require(len(controls['final_dispatches'])==28 and not controls['relocated_relative_cases'] and not controls['relocated_predicates_andqueries'] and len(controls['normal_seeded_ends'])==25,'original final dispatch/relative/predicate/end coverage')
    require(all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in controls['normal_seeded_ends']),'native seeded normal value carry')
    require(controls['all_nine_nonrelative_controls_oneA000_4821_4720_4681_andcomplete_end_bytes_exact'] and controls['zero_relative_predicate_query_sites_not_fabricated_execution_coverage'] and controls['source_relocated4821_descriptor_layout_calls_andall_4MiB_ABI_guards_equal'],'original nontext controls/raw predicate results')
    require(len(later['groups'])==len(rng['groups'])==1 and summary(later['groups'][0])==mapping['observed_comparison_contract']==seal['observed_comparison_contract'],'all measured comparison metadata')
    g=later['groups'][0];r=rng['groups'][0]
    require(g['source_English_exits']==[10822,10824] and len(g['command_comparison_differences'])==35 and len(g['duration_differences'])==11,'measured exits/timing differences')
    require(g['final_PRNG_seeds']==r['final_seeds']==[int('3888306843'),int('2225786845')] and r['same_initial_seed']==848781860 and r['exit_English_phase']==2 and r['final_English_phase']==-10,'measured RNG phases')
    require(g['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True) and not g['whole_actors_equal'],'actual later sampled component/calendar/actor differences with bounded limits')
    require(len(g['later_RGB_differences'])==r['later_RGB_differences']==17 and len(g['later_full_RGB_comparisons'])==g['later_sample_count']==r['later_samples']==87,'all later RGB measurements')
    require(g['all_original_initializer_andexchange_results_equal'] and g['all_UI_request_words_equal'] and g['all_observed_whole_upper_scene_portrait_andheader_RGB_equal'],'selected results/UI/scenes equal')
    require(r['first_observed_phase_difference']['word']==0x4000 and r['first_observed_phase_difference']['canonical_source_offset']==350 and r['first_observed_phase_difference']['source_duration']==237 and r['first_observed_phase_difference']['English_duration']==241,'first measured phase and original single-page wait timing')
    require([(m['word'],m['canonical_source_offset'],m['source_duration'],m['English_duration']) for m in r['original_4821_A000_4720_4681_measurements'] if m['canonical_source_offset'] is not None]==[(0x4821,244,60,60),(0xA000,340,240,240),(0x4720,348,0,0),(0x4681,1510,88,88)],'original effect wait measurements')
    check_bounded_risk(data['focused_picture_transition_andrisk'],actual,later)
    require(rng['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified'] and rng['all_raw_measurements_kept_for_later_older_record_technical_reaudit'] and rng['earlier_contract_reused_only_for_exact_unchanged_code_not_fresh_every_call_causal_trace'],'future-state/causal/re-audit limits')
    doc=load(conf['manuscripts'][0]);validate_approved_batch(doc)
    require(seal['manuscript_sha256']==sha(Path(conf['manuscripts'][0]).read_bytes()),'sealed manuscript identity')
    require(doc['native_approved_manuscript']==str(DRAFT) and doc['native_approved_manuscript_sha256']==approval['manuscript_sha256']==sha(DRAFT.read_bytes()),'approved manuscript lineage')
    require(doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and doc['current_ROM']==conf['parent_ROM']==packet['current_ROM'] and doc['current_ROM_sha256']==conf['parent_ROM_sha256']==packet['current_ROM_sha256'],'complete map/parent references')
    require(doc['current_ARM9_sha256']==packet['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==packet['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'document runtime identity')
    rows=doc['records'];require(sum(r['decision']=='revision' for r in rows)==13 and sum(r['decision']=='retention' for r in rows)==15,'thirteen revisions/fifteen retentions')
    check_actual(actual,data['source_font_proof'],native,names,rows,packet,data['source_path_proof'],data['focused_picture_transition_andrisk'])
    source=image.read_file(PATH);require(sha(source)==mapping['source_archive_sha256']==packet['current_archive_sha256'],'complete predecessor archive')
    blocks=IlnkContainer.parse(source).blocks;cleanblocks=IlnkContainer.parse(NdsImage.open(conf['clean_ROM']).read_file(PATH)).blocks
    require(len(blocks)==len(cleanblocks)==343 and len(mapping['groups'])==1,'complete one-block archive scope')
    group=mapping['groups'][0];require(group['block']==50 and group['route']==0 and group['file_path']==PATH and group['external_references_complete'],'one original Rafael entry')
    original=load(RELOCATION)['groups'][0]
    require(original['external_references_complete'] is False and group['external_references_complete'] is True,'pending relocation promoted only after census seal')
    require(all(group.get(k)==v for k,v in original.items() if k!='external_references_complete'),'exact independently reconstructed relocation')
    require(group['command_map']==census['all_command_maps'] and group['relative_fixups']==census['relative_operand_maps'],'complete census associations')
    fonts={r['id']:r for r in native['records']};stores={r['id']:r for r in stored['records']};dispatch={r['id']:r for r in controls['final_dispatches']}
    require(len(stores)==len(stored['records'])==28 and set(stores)==set(fonts)==set(dispatch)==set(frozen['record_bindings']),'all individual proof IDs')
    for row in rows:
        ident=row['id'];b=frozen['record_bindings'][ident];font=fonts[ident];store=stores[ident];ref=next(r for r in group['text_records'] if r['id']==ident)
        p=profile_for(arm,blocks[50],ident,PATH,b['consumer'])
        encoded=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],p);qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==font['compiled_hex']==b['compiled_hex'] and qa==row['base_QA_report'],'compiled text/QA:'+ident)
        require(row['qa_waivers']==b['qa_waivers'] and row['qa_waiver_reason']==b['qa_waiver_reason'] and row['qa_waiver_scope']==b['qa_waiver_scope'] and row['native_page_count']==b['native_page_count'],'exact narrow warning/page scope:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(bytes.fromhex(row['current_hex']))%2
        if pad:value+=b' '
        require(value.hex()==row['stored_target_hex']==store['stored_hex']==dispatch[ident]['final_stored_hex'] and pad==row['stored_parity_space']==store['compiler_owned_parity_space'],'exact stored parity:'+ident)
        expanded=value[1:].replace(b'FI',b'Rafael').replace(b'FA',b'Castor')
        require(expanded.hex()==store['expanded_stored_hex'] and b'%' not in value[1:] and b'FO' not in value[1:] and value[1:].count(b'FI')==int(ident=='DK4_MES_B50_R0108') and value[1:].count(b'FA')==int(ident in ['DK4_MES_B50_R0040','DK4_MES_B50_R0061']),'exact original FA2/FI1 sites/no added macro orprintf:'+ident)
        pipeline=store['complete_native_stored_proof']['native_alignment']
        require(len(pipeline['cases'])==4 and all(r['output_hex']==expanded.hex() for r in pipeline['cases']),'all stored native alignments:'+ident)
        require(len(font['pages'])==b['native_page_count'] and all(sha(Path(pg['native_plane']).read_bytes())==pg['native_plane_sha256'] for pg in font['pages']),'complete native ink:'+ident)
        require(row['target_reference']==dict(block=50,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index']) and row['actual_record_observed'] is (ident not in UNVISITED),'final reference/scoped actual approval:'+ident)
    targetblocks=list(blocks)
    targetblocks[50]=reconstruct(blocks[50],cleanblocks[50],group,packet['groups'][0],rows,branches['operands_requiring_adjustment_when_resizing'])
    payload=IlnkContainer(targetblocks).to_bytes()
    require(sha(payload)==mapping['target_archive_sha256']==conf['archives'][0]['target_sha256'],'complete reconstructed target archive')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'],'research reference ROM identity')
    reference=NdsImage.open(conf['reference_ROM']);require(payload==reference.read_file(PATH),'whole approved reference archive')
    require([i for i,(a,b) in enumerate(zip(blocks,targetblocks,strict=True)) if a!=b]==[50],'only owned B50 block')
    require(all(reference.read_file(p)==v for _,p,v in image.iter_files() if p!=PATH) and all(reference.read_file(p)==v for p,v in image.iter_components()),'all other files/components unchanged')
    restored=list(targetblocks);restored[50]=blocks[50];require(IlnkContainer(restored).to_bytes()==source,'complete archive inverse')
    files=list(image.rom.files);index=image.path_map()[PATH];files[index]=payload
    require([i for i,(a,b) in enumerate(zip(image.rom.files,files,strict=True)) if a!=b]==[index],'one SC0 file slot')
    changes=[dict(id=r['id'],file_path=PATH,block=50,kind=r['kind'],old_offset=r['current_reference']['offset'],new_offset=r['target_reference']['offset']) for r in rows]
    require(len(changes)==len({r['id'] for r in changes})==28,'all twentyeight unique manifest changes')
    commit_files(image,files)
    return dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,
        files=[dict(file_path=PATH,source_sha256=sha(source),target_sha256=sha(payload),changed_records=changes)],
        one_files_list_commit_after_all_gates=True,complete_clean_predecessor_block_andarchive_inverse_exact=True,
        all28_preambles37_commands_zero_relative_predicate_query_sites_FA2_FI1_nine_nontext_controls_andfull_end_preserved=True,
        all28_single_pages_two_exact_warnings18_infos_all28_actual_speeches_preserved=True,
        all_measured_timing_RNG_component_calendar_RGB_limits_preserved=True,full_goal_complete=False)
