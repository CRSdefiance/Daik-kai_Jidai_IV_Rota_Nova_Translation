"""Plan ARM9 andSC2 completely in memory, validate independent evidence, then commit one NDS object."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch,validate_name_transition
from dk4tool.dialogue.gerhard_surname_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.gerhard_surname_rebuild_v1 import rebuild
from dk4tool.patch.gerhard_surname_evidence_v1 import check_evidence
from dk4tool.patch.gerhard_surname_comparison_v1 import check_comparisons
from dk4tool.patch.gerhard_surname_risk_v1 import check_bounded_risk
from scripts.Gerhard_surname_release_paths_v8238 import proofs,FLAGS,APPROVED,MAP,SEAL,PARENT,ROM

CONFIG='translations/gerhard_surname_editorial_release_v1.json'
PATH='/data/SC2.DK4'
ARM='/__arm9__.bin'

def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Gerhard atomic editorial contract: '+message)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
def commit_image(image,rom):image.rom=rom

def check_controls(data,result,sourcegroups,require):
    controls,census,loader=[data[k] for k in ['native_controls','native_caller','native_loader']]
    require(len(controls['final_dispatches'])==5 and len(controls['original_nontext_control_maps'])==51,'five final dispatches/51 original nonrelative controls')
    require(controls['raw_native_evaluations']==30 and len(controls['raw_predicates_andqueries'])==10,'ten original raw sites/thirty native evaluations')
    require(controls['normal_seeded_end_cases']==150 and len(controls['normal_seeded_ends'])==6,'six complete terminals/150 seeded ends')
    require(controls['full_opaque_effect_picture_resource_andchoice_UI_bodies_unexecuted_bythis_native_dispatch_probe'] and controls['ordinary_opening_evaluator_results_not_natural_eligibility_orforced_gameplay_states'],'raw native/control scope limits')
    for end in controls['normal_seeded_ends']:
        require(end['block'] in [27,74] and end['version'] in ['clean','current','target'] and len(end['cases'])==25,'complete original seeded end scope')
        require(end['terminal']['word']==0 and end['terminal']['native_extent']==4 and end['terminal']['whole_command_hex']=='00000000','complete four-byte original terminal')
        require({(c['previous_result'],c['initial_value_word']) for c in end['cases']}=={(a,b) for a in [0,1,2,3,0xFFFFFFFF] for b in [0,1,2,3,0xFFFFFFFF]},'all25 original seed combinations')
        for c in end['cases']:
            require(c['native_result']==[0,c['initial_value_word'],0,0,0,0] and c['native_extent']==4 and c['source_command_hex']=='00000000' and c['source_offset']==end['terminal']['offset'],'normal end retains entire value word')
            require(c['no_leading_or_post_four_byte_payload_read'] and c['all4MiB_owner_input_ABI_output_and_length_guards_exact'],'native terminal read/ABI guards')
    require(loader['archive_block_counts']=={'2':336} and loader['original_action_count']==338 and loader['fresh_native_whole_loads_andcache_hits']==336 and loader['fresh_initial_parent_modes']==672,'complete native whole loads andparent modes')
    require(loader['both_original_parent_modes_begin_payload_plus8'] and loader['all_original_EV2_actions_select_block_indices_not_interior_offsets'] and loader['all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact'],'original index/cache/entry ABI guards')
    for pathkey,hashkey in [('load_proof','load_sha256'),('parent_mode_proof','parent_mode_sha256')]:require(sha(Path(loader[pathkey]).read_bytes())==loader[hashkey],'native load/parent underlying proof integrity')
    require(census['fresh_caller_censuses']==2 and census['original_entry_payload_offset']==8 and census['only_original24070_interpreter_call_no_literal_alias'] and census['no_interior_entry_offsets_orunmapped_nested_relative_targets'],'complete shipped caller census/entry scope')
    require(census['caller_entry_checks_not_actual_event_selection_orarbitrary_dynamic_reference_proof'],'no arbitrary dynamic/natural activation claim')
    totalcontrols=[]
    for group in result['groups']:
        number=group['block'];source=sourcegroups[number];commands=group['all_current_commands'];target=group['all_target_commands'];clean=source['all_source_commands']
        indexed={m['old_offset']:m for m in group['command_map']};cg=next(g for g in census['groups'] if g['block']==number)
        require(cg['all_command_maps']==group['command_map'],'all independently rebuilt caller command maps')
        require(len(cg['relative_operand_maps'])==len(group['relative_fixups']),'all independently rebuilt caller relative maps')
        for a,b in zip(cg['relative_operand_maps'],group['relative_fixups'],strict=True):require(all(a[k]==v for k,v in b.items()),'every native relative operand/target')
        for a,b,c in zip(clean,commands,target,strict=True):
            if b['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
            oldhex,newhex=b['whole_command_hex'],c['whole_command_hex']
            require(oldhex==newhex,'all opaque original effects/menu/end bytes')
            totalcontrols.append(dict(block=number,source_offset=a['offset'],previous_offset=b['offset'],target_offset=c['offset'],word=b['word'],clean_hex=a['whole_command_hex'],previous_andtarget_hex=oldhex,
                source_difference_only_prior_reviewed_translated_choice=a['whole_command_hex']!=oldhex))
        for raw in [r for r in controls['raw_predicates_andqueries'] if r['block']==number]:
            sourcecmd=next(c for c in clean if c['offset']==raw['source_offset']);currentcmd=next(c for c in commands if c['offset']==raw['cases'][1]['offset'])
            targetcmd=next(c for c in target if c['offset']==raw['target_offset'])
            require([c['version'] for c in raw['cases']]==['clean','current','target'],'three original raw query phases')
            for proof,command in zip(raw['cases'],[sourcecmd,currentcmd,targetcmd],strict=True):
                require(proof['source_command_hex']==command['whole_command_hex'] and proof['offset']==command['offset'] and proof['word']==command['word'] and proof['native_extent']==command['native_extent'],'raw evaluator source operand/extent')
                require(proof['no_predicate_or_event_flag_forced'] and proof['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and proof['sole_scratch_restore_recovers_all4MiB_exact'],'original unforced query guards')
            require(raw['cases'][0]['native_result']==raw['cases'][1]['native_result']==raw['cases'][2]['native_result'] and raw['raw_native_results_not_assumed_boolean_menu_orpath_attainability'],'exact raw original results preserved without Boolean inference')
    require(controls['original_nontext_control_maps']==totalcontrols,'all51 source/current/target nonrelative control associations')

def observed_scope(data):
    a,c,f=[data[k] for k in ['actual','actual_comparison','actual_focus']]
    def groups(scope,block):return [g for g in a['groups'] if g['scope']==scope and g['block']==block]
    b27,b74,intro=groups('whole',27),groups('whole',74),groups('intro-display',27)
    return dict(complete_body_holds=a['complete_body_holds'],relevant_name_holds=a['relevant_name_holds'],initial_runs=len(a['groups']),repeat_runs=len(f['groups']),total_scene_frames=f['total_Gerhard_scene_frames_including_replay'],
        selected_wholeB27_speeches=len(b27[0]['speeches']),wholeB27_unvisited=len(b27[0]['unvisited_conditional_text_IDs']),wholeB27_normal_return_frames=[g['normal_return']['frame'] for g in b27],wholeB27_later_final_captains=c['groups'][0]['captain_IDs'],
        selected_wholeB74_speeches=len(b74[0]['speeches']),wholeB74_unvisited=len(b74[0]['unvisited_conditional_text_IDs']),wholeB74_normal_return_frames=[g['normal_return']['frame'] for g in b74],wholeB74_actual_choice_option=0,
        intro_display_speeches=len(intro[0]['speeches']),intro_outercondition_unexecuted=True,intro_normal_return_frames=[g['normal_return']['frame'] for g in intro],
        scene_portrait_pairs=sum(len(g['selected_scene_andportrait_pairs']) for g in c['groups']),duration_difference_counts=[len(g['duration_differences']) for g in c['groups']],command_difference_counts=[len(g['command_comparison_differences']) for g in c['groups']],
        later_RGB_counts=[g['later_sample_count'] for g in c['groups']],later_RGB_difference_counts=[len(g['later_RGB_differences']) for g in c['groups']],
        all_selected_results_UI_andmemberships_equal=True,first7_focused_RAM_components_equal=all(all(g['component_equality'].values()) for g in f['sampled_comparisons'][:7]),
        final_phase_changed_bytes={k:v['changed_bytes'] for k,v in f['sampled_comparisons'][-1]['bounded_native_model_andpersistent_byte_differences'].items() if v['changed_bytes']},raw_final_phase_calendars=f['sampled_comparisons'][-1]['raw_calendar_values'],
        all_exact_replay_rows_exceptpaths_selected_framebuffers_andfinalRAM_equal_perversion=True,no_normal_Lilcontinuity_claim_from_fullB27_tail=True,no_full_original_B27_effects_claim_from_intro_display=True,
        no_broad_simulation_futureoutcome_hardware_fullroute_orall_conditional_visit_claim=True)

def plan_release(image,baseline,config):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Gerhard-five-body-one-name-editorial-release-v1' and conf['manuscripts']==[str(APPROVED)] and conf['proofs']==proofs(),'exact complete source-bound configuration')
    require(conf['reference_map']==str(MAP) and conf['reference_approval']==str(SEAL) and conf['parent_ROM']==str(PARENT) and conf['reference_ROM']==str(ROM),'exact sealed paths')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline identity')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256'] and sha(ROM.read_bytes())==conf['reference_ROM_sha256'],'clean/parent/reference identity')
    require(sha(bytes(image.rom.save()))==conf['parent_ROM_sha256'],'whole exact predecessor ROM before either change')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'every predecessor file/component')
    frozen=validate_runtime(image);doc=load(conf['manuscripts'][0]);validate_approved_batch(doc)
    mapping,seal=load(conf['reference_map']),load(conf['reference_approval']);data={k:load(p) for k,p in conf['proofs'].items()}
    require(data['native_contract']==frozen and conf['required_map_flags']==seal['flags']==FLAGS and all(mapping[k] is True for k in FLAGS),'all independently frozen source/scope flags')
    require(mapping['new_credit']==seal['new_credit']==0 and not mapping['full_goal_complete'] and not seal['full_goal_complete'],'no duplicate editorial credit/fullgoal claim')
    require(seal['manuscript_sha256']==sha(APPROVED.read_bytes()) and seal['reference_map_sha256']==doc['approved_reference_map_sha256']==sha(MAP.read_bytes()),'sealed manuscript/map lineage')
    require(mapping['parent_ROM_sha256']==seal['parent_ROM_sha256']==conf['parent_ROM_sha256'] and mapping['reference_ROM_sha256']==seal['reference_ROM_sha256']==conf['reference_ROM_sha256'],'sealed predecessor/reference bindings')
    require(mapping['proofs']==seal['proofs']==proofs() and mapping['proof_sha256']==seal['proof_sha256'],'all18 proof associations')
    for path,digest in mapping['proof_sha256'].items():require(sha(Path(path).read_bytes())==digest,'sealed proof integrity:'+path)
    policy=data['policy_validation'];require(len(policy['positive_body_records'])==5 and policy['negative_count']==260 and policy['all_rejections_match_expected_semantic_guard'],'all frozen source/prose/name policy cases')
    arm=image.read_file(ARM);archive=image.read_file(PATH);source=data['source_context'];sourcegroups={g['block']:g for g in source['groups']}
    require(doc['current_ROM_sha256']==source['current_ROM_sha256']==conf['parent_ROM_sha256'] and sha(archive)==mapping['source_SC2_sha256']==source['current_archive_sha256'],'document current archive references')
    require(sha(arm)==doc['current_ARM9_sha256']==mapping['source_ARM9_sha256'],'document current ARM9 identity')
    require(doc['current_COMMON_sha256']==source['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'document complete current COMMON identity')
    require(conf['archives']==[dict(file_path=PATH,source_sha256=mapping['source_SC2_sha256'],target_sha256=mapping['target_SC2_sha256'])] and conf['components']==[dict(file_path=ARM,source_sha256=mapping['source_ARM9_sha256'],target_sha256=mapping['target_ARM9_sha256'])],'exact two owned configuration output entries')
    name=doc['name_records'][0];newarm=bytearray(arm);at=name['offset'];newarm[at:at+name['bytes']]=bytes.fromhex(name['target_hex']);newarm=bytes(newarm)
    nameproof=validate_name_transition(arm,newarm)
    require(mapping['name_record']==name and mapping['name_validation']==nameproof and sha(newarm)==mapping['target_ARM9_sha256'],'exact name field independent inverse/pointers/Blades')
    blocks=IlnkContainer.parse(archive).blocks;clean=IlnkContainer.parse(NdsImage.open(conf['clean_ROM']).read_file(PATH)).blocks
    for row in doc['records']:
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);ref=row['source_reference'];current=bytes.fromhex(row['current_hex']);cr=row['current_reference']
        require(clean[row['block']][ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0','exact clean source reference:'+ident)
        require(blocks[row['block']][cr['offset']:cr['offset']+len(current)+1]==current+b'\0','exact previous reference:'+ident)
        p=profile_for(arm,blocks[row['block']],ident,PATH,'progressive')
        encoded=encode_relocatable_dialogue(raw,row['planned_English_markup'],p);qa=audit_relocatable_dialogue_record(raw,row['planned_English_markup'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==frozen['record_bindings'][ident]['compiled_hex'],'independent frozen compiler output:'+ident)
        require(qa['issues']==row['all_original_QA_issues'] and not row['qa_waivers'],'all original QA andzero waivers:'+ident)
        pad=len(encoded.encoded)%2!=len(current)%2;stored=encoded.encoded+(b' ' if pad else b'')
        require(pad==row['compiler_owned_parity_space'] and stored.hex()==row['final_stored_hex'],'exact compiler parity/store:'+ident)
    result=rebuild(archive,arm,doc['records'])
    require(len(mapping['blocks'])==2 and sha(result['target_archive'])==mapping['target_SC2_sha256'],'independent complete archive output')
    for fresh,declared in zip(result['groups'],mapping['blocks'],strict=True):
        require({k:v for k,v in fresh.items() if k not in ['target_block','all_current_commands']}==declared,'every sparse reference/header/tail/command/relative/inverse map')
        for ref in fresh['text_records']:
            row=next(r for r in doc['records'] if r['id']==ref['id'])
            require(row['integrated_reference_pending']==dict(file_path=PATH,block=fresh['block'],offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=fresh['target_block_sha256']),'complete final source-qualified reference')
    check_controls(data,result,sourcegroups,require)
    reference=NdsImage.open(ROM)
    native_actual=check_evidence(data,doc['records'],image,reference,result,load,require)
    comparison=check_comparisons(data['actual_comparison'],data['actual'],image,reference,load,require)
    risk=check_bounded_risk(data['actual_comparison'],data['actual_focus'],data['actual'],load,require,data['reference_receipt'])
    measured=observed_scope(data);require(measured==mapping['actual_scope']==seal['actual_scope'],'every independently measured actual scope/limit field')
    planned=deepcopy(image);planned.replace_file(ARM,newarm);planned.replace_file(PATH,result['target_archive']);validate_runtime(planned,'target')
    require(bytes(planned.rom.save())==ROM.read_bytes(),'whole two-component plan equals approved reference')
    require([p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[PATH] and [p for p,v in image.iter_components() if planned.read_file(p)!=v]==[ARM],'only owned SC2 file andARM9 component change')
    restored=deepcopy(planned);restored.replace_file(ARM,arm);restored.replace_file(PATH,archive)
    require(bytes(restored.rom.save())==PARENT.read_bytes(),'every complete predecessor ROM byte inverses')
    require(planned.read_file(PATH)==reference.read_file(PATH) and planned.read_file(ARM)==reference.read_file(ARM),'whole exact approved archives/components')
    corpus=[v for _,_,v in planned.iter_files()]+[v for _,v in planned.iter_components()]
    require(sum(v.count(b'Adernkatz') for v in corpus)==20 and not any(b'Ardelknatts' in v or b'Ardelnkatts' in v for v in corpus),'twenty consistent final Latin consumers/no old variants')
    changes=[dict(id=r['id'],file_path=PATH,block=r['block'],kind='progressive',old_offset=r['current_reference']['offset'],new_offset=r['integrated_reference_pending']['offset']) for r in doc['records']]
    namechange=dict(id=name['id'],file_path=ARM,kind='owned-name-field',offset=at,bytes=name['bytes'],actor_ID=16)
    return planned.rom,dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes+[namechange],
        files=[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']),changed_records=changes),dict(file_path=ARM,source_sha256=sha(arm),target_sha256=sha(newarm),changed_records=[namechange])],
        one_complete_NDS_object_commit_after_all_gates=True,all_source_sparse_controls_refs_andcomplete_predecessor_inverse_exact=True,
        owned_name12_Blades8_pointerfields_andall_unowned_bytes_exact=True,actual_scope=measured,native_actual=native_actual,comparison=comparison,bounded_risk=risk,
        zero_duplicate_editorial_credit=True,full_goal_complete=False)

def apply_release(image,baseline,config=CONFIG):
    try:planned,report=plan_release(image,baseline,config)
    except (KeyError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        raise ValueError('Gerhard atomic editorial contract: invalid orcontradictory evidence schema: '+str(exc)) from exc
    commit_image(image,planned)
    return report
