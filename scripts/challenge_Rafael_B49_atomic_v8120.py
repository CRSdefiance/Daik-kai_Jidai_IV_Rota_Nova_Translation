"""Independently corrupt real B49 proofs with dependency checks bypassed and commits trapped."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import rafael_B49_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.validate_Rafael_B49_policy_v8113 import SEMANTIC
from scripts.Rafael_B49_release_paths_v8114 import PARENT,ROM,APPROVED,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_atomic_challenges_v8120')
POSITIVE=Path('work/analysis/Rafael_B49_atomic_positive_v8119/positive_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists()
    positive=read(POSITIVE);config=Path(positive['config']);p=proofs();cache={}
    def original(path):
        key=str(Path(path).resolve())
        if key not in cache:cache[key]=read(path)
        return cache[key]
    tests=[]
    def add(label,path,keys,value):
        old=original(path)
        for key in keys:old=old[key]
        assert old!=value,'Unchanged mutation:'+label
        tests.append(dict(case=label,modifications=[(str(path),keys,deepcopy(value))]))
    doc=original(APPROVED);indices={r['source_record_index']:i for i,r in enumerate(doc['records'])}
    for i,row in enumerate(doc['records']):
        add('prose-'+row['id'],APPROVED,['records',i,'english'],row['english']+'!')
        add('formatting-'+row['id'],APPROVED,['records',i,'review','formatting'],False)
        add('target-reference-'+row['id'],APPROVED,['records',i,'target_reference','offset'],row['target_reference']['offset']+2)
    for gate in ['source','context','localization','naturalness']:
        add('speech-gate-'+gate,APPROVED,['records',0,'review',gate],False)
    for label,index,old,new in SEMANTIC:
        i=indices[index];text=doc['records'][i]['english'];assert old in text
        add('meaning-'+label,APPROVED,['records',i,'english'],text.replace(old,new))
    for key,value in [('file_path','/data/SC2.DK4'),('route',2),('route_identity','Lil'),('block',46),
        ('current_ROM','work/clean.nds'),('current_ROM_sha256','0'*64),('current_ARM9_sha256','0'*64),('current_COMMON_sha256','0'*64),
        ('target_locale','en-GB'),('translation_policy','natural-dialogue-v1')]:
        add('document-'+key,APPROVED,[key],value)
    for key,value in [('source_hex',doc['records'][0]['source_hex'][:-2]+'00'),('context','Invented context.'),('speaker','Grandpa'),
        ('compiled_hex',doc['records'][0]['compiled_hex']+'20'),('source_complete_preamble_hex','000000000000')]:
        add('individual-'+key,APPROVED,['records',0,key],value)
    retention=next(i for i,r in enumerate(doc['records']) if r['decision']=='retention')
    add('unjustified-retention',APPROVED,['records',retention,'retention_reason'],'')
    add('missing-speech',APPROVED,['records'],doc['records'][:-1])
    add('duplicate-speech',APPROVED,['records',1],doc['records'][0])
    add('lost-row-reason',APPROVED,['records',0,'row_count_reason'],'')
    r347=indices[244]
    add('invented-second-page',APPROVED,['records',r347,'native_page_count'],2)
    add('invented-conditional-gameplay',APPROVED,['records',indices[32],'actual_record_observed'],True)
    for i,row in enumerate(doc['records']):
        if row['qa_waivers']:
            add('waiver-erased-'+row['id'],APPROVED,['records',i,'qa_waivers'],[])
            add('waiver-broadened-'+row['id'],APPROVED,['records',i,'qa_waivers'],['weak-line-ending','long-line'])
            add('waiver-reason-'+row['id'],APPROVED,['records',i,'qa_waiver_reason'],'A general exception.')
            for field in ['id','source_hex','compiled_hex','line','last_word','next_word','exact_issue']:
                value=3 if field=='line' else ('changed' if field!='exact_issue' else dict(code='weak-line-ending',message='changed',severity='warning'))
                add('waiver-scope-'+field+'-'+row['id'],APPROVED,['records',i,'qa_waiver_scope',field],value)
    for flag in owned.FLAGS:add('map-flag-'+flag,MAP,[flag],False)
    group=original(MAP)['groups'][0]
    for key,value in [('source_header_hex','4353000000000000'),('target_header_hex','4353000000000000'),
        ('source_block_sha256','0'*64),('target_tail_bytes',4)]:
        add('map-group-'+key,MAP,['groups',0,key],value)
    for i,edge in enumerate(group['relative_fixups']):
        add('relative-endpoint-'+str(i),MAP,['groups',0,'relative_fixups',i,'new_matched_skip_target'],edge['new_matched_skip_target']+2)
    add('command-extent',MAP,['groups',0,'command_map',0,'new_extent'],group['command_map'][0]['new_extent']+2)
    for key,value in [('fresh_compiled_alignment_cases',59),('complete_progressive_paragraphs',14),('complete_progressive_pages',15)]:
        add('native-'+key,p['native_font_proof'],[key],value)
    native=original(p['native_font_proof'])
    add('native-compiled',p['native_font_proof'],['records',0,'compiled_hex'],native['records'][0]['compiled_hex']+'20')
    duplicate=deepcopy(native['records']);duplicate[1]=deepcopy(duplicate[0])
    add('native-duplicate',p['native_font_proof'],['records'],duplicate)
    add('native-single-page-missing',p['native_font_proof'],['records',r347,'pages'],[])
    for key,value in [('fresh_native_alignment_cases',31),('exact_reused_native_alignment_cases',27),('all61_native_ink_planes_exact_to_already_viewed',False),('all61_complete_stored_single_pages_exact_to_viewed',False)]:
        add('stored-'+key,p['native_stored_proof'],[key],value)
    stored=original(p['native_stored_proof'])
    add('stored-native-alignment',p['native_stored_proof'],['records',0,'complete_native_stored_proof','native_alignment','cases',0,'output_hex'],'00')
    add('stored-byte',p['native_stored_proof'],['records',0,'stored_hex'],stored['records'][0]['stored_hex']+'20')
    add('stored-extra-native-alignment',p['native_stored_proof'],['records',0,'complete_native_stored_proof','native_alignment','cases'],stored['records'][0]['complete_native_stored_proof']['native_alignment']['cases'][:3])
    controls=original(p['relocated_control_proof'])
    add('native-carry-erased',p['relocated_control_proof'],['normal_seeded_ends',1,'native_result',1],controls['normal_seeded_ends'][1]['native_result'][1]^1)
    add('fourteenth-predicate-query-lost',p['relocated_control_proof'],['relocated_predicates_andqueries'],controls['relocated_predicates_andqueries'][:-1])
    add('control-byte-not-preserved',p['relocated_control_proof'],['all37_nonrelative_controls_sevenA000_C281_andcomplete_end_bytes_exact'],False)
    add('raw-predicate-result-not-preserved',p['relocated_control_proof'],['all13_raw_predicates_andone_completion_query_current_unforced_values_andunaligned_scratch_restore_preserved'],False)
    add('loader-343',p['native_loader_proof'],['fresh_native_whole_loads_andcache_hits'],342)
    add('loader-parent-modes',p['native_loader_proof'],['fresh_initial_parent_modes'],685)
    add('caller-alias',p['native_caller_proof'],['only_original24070_interpreter_call_no_literal_alias'],False)
    add('caller-relative-endpoint',p['native_caller_proof'],['relative_operand_maps',0,'new_matched_skip_target'],group['relative_fixups'][0]['new_matched_skip_target']+2)
    policy=original(p['native_policy_validation'])
    add('policy-positive-missing',p['native_policy_validation'],['positives'],policy['positives'][:-1])
    add('policy-negative-unrejected',p['native_policy_validation'],['negatives',0,'rejected'],False)
    add('policy-wrong-guard',p['native_policy_validation'],['negatives',0,'expected_guard'],'guard-not-present')
    add('actual-sheet-unviewed',p['actual_approval'],['directly_viewed_sheets',0,'directly_viewed'],False)
    add('actual-conditional-scope-erased',p['actual_approval'],['eleven_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage'],False)
    add('actual-warning-scope-erased',p['actual_approval'],['exact_three_QA_waivers22_infos_all_original_diagnostics_preserved'],False)
    add('actual-native-only-list-erased',p['actual_proof'],['native_only_unvisited_speech_IDs'],[])
    names=original(p['speaker_name_review'])
    janus=next(i for i,n in enumerate(names['records']) if n['actor_ID']==4)
    add('wrong-Janus-name',p['speaker_name_review'],['records',janus,'name'],'Janus Pasha')
    add('invented-Janus-actual-header',p['speaker_name_review'],['records',janus,'actual_B49_progressive_nameplate_verified'],True)
    actual=original(p['actual_proof'])
    for i,g in enumerate(actual['groups']):
        for key,value in [('incomplete_sampled_holds',1),('native_terminal_result',[0,1]),
            ('observed_original_exchange_commands',163),('exit_frame',g['exit_frame']+1),
            ('unidentified_trace_rows',[dict(unknown=True)])]:
            add('actual-'+key+'-'+str(i),p['actual_proof'],['groups',i,key],value)
    en=next(i for i,g in enumerate(actual['groups']) if g['version']=='English')
    for key in ['complete_black_ASCII_gray_CP932_gray_masks_equal','complete_name_mask_equal']:
        add('actual-'+key,p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,key],False)
    add('hold-outside-interval',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'frame'],1)
    add('actual-first-page-unobserved',p['actual_proof'],['groups',en,'speech_observations',0,'actual_complete_page_holds',0],[])
    add('invented-second-page',p['actual_proof'],['groups',en,'speech_observations',0,'native_page_count'],2)
    add('invented-page-turn',p['actual_proof'],['groups',en,'speech_observations',0,'ordinary_page_transitions'],[dict(from_page=1,to_page=2)])
    add('wrong-native-plane',p['actual_proof'],['groups',en,'speech_observations',0,'native_planes',0,'sha256'],'0'*64)
    add('wrong-actual-canonical-source',p['actual_proof'],['groups',en,'command_pairs',12,'canonical_source_offset'],74)
    for gi,g in enumerate(actual['groups']):
        ci=next(i for i,c in enumerate(g['command_pairs']) if c['word']==0xC281)
        for field,value in [('decoded_length',4),('native_result',[3,1]),('canonical_source_offset',74)]:
            add('actual-C281-'+field+'-'+str(gi),p['actual_proof'],['groups',gi,'command_pairs',ci,field],value)
    flow=original(p['source_path_proof'])
    add('source-composition-count',p['source_path_proof'],['structural_compositions_evaluated'],1)
    add('source-branch-union-erased',p['source_path_proof'],['all154_commands61_speeches_in_structural_union'],False)
    add('source-representative-paths-erased',p['source_path_proof'],['representative_text_paths'],[])
    focus=original(p['focused_C281_transition'])
    add('C281-opaque-bridge-misclaimed',p['focused_C281_transition'],['groups',0,'original_C281_effect_body_executed_in_core_no_opaque_bridge'],False)
    add('C281-focused-result',p['focused_C281_transition'],['groups',0,'C281_command','native_result'],[0,0])
    add('focused-Camille-truncated-name',p['focused_C281_transition'],['groups',0,'actual_complete_Lil_Camille_nameplates',1,'name'],'Camille Overijsse')
    add('focused-conditional-header-invented',p['focused_C281_transition'],['groups',0,'observed_nameplate_actors'],[0,2,4,5,9])
    for key,value in [('source_English_exits',[6416,6416]),('whole_actors_equal',False),('final_PRNG_seeds',[19668379,19668379]),('later_sample_count',156)]:
        add('later-'+key,p['later_scope_proof'],['groups',0,key],value)
    add('later-calendar-equality-erased',p['later_scope_proof'],['groups',0,'five_native_component_equality','calendar'],False)
    later=original(p['later_scope_proof'])
    add('later-RGB-difference-erased',p['later_scope_proof'],['groups',0,'later_RGB_differences'],later['groups'][0]['later_RGB_differences'][:-1])
    for key,value in [('same_initial_seed',1),('exit_English_phase',0),('final_English_phase',0)]:
        add('RNG-'+key,p['RNG_scope_proof'],['groups',0,key],value)
    add('RNG-causal-limit-erased',p['RNG_scope_proof'],['earlier_contract_reused_only_for_exact_unchanged_code_not_fresh_every_call_causal_trace'],False)
    add('RNG-future-limit-erased',p['RNG_scope_proof'],['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified'],False)
    # Reuse only the trusted, immutable frozen contract during changed-proof cases.
    # Its dependency bytes are fully checked before and after the loop; all semantic
    # comparisons, modified proof loads, profile equality and commit traps remain active.
    from dk4tool.dialogue import rafael_B49_profile_v1 as frozen_module
    original_native_contract=frozen_module.contract
    trusted_contract=original_native_contract()
    trusted_snapshot=deepcopy(trusted_contract)
    original_owned_contract=owned.contract
    for group_index,g in enumerate(actual['groups']):
        add('later-reentry-scope-erased-'+str(group_index),p['actual_proof'],['groups',group_index,'complete_first_exchange_distinguished_from_later_fixture_reentry'],False)
    r370=indices[388]
    add('stored-FI-expansion-erased',p['native_stored_proof'],['records',r370,'expanded_stored_hex'],stored['records'][r370]['stored_hex'][2:])
    protected=[config,PARENT,ROM,APPROVED,MAP,SEAL,*map(Path,p.values()),
        Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        Path('dk4tool/patch/rafael_B49_editorial_v1.py')]
    before={str(path):sha(path.read_bytes()) for path in protected}
    image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    files=image.rom.files;oldfiles=list(files);components=list(image.iter_components());results=[];gaps=[];commits=[]
    ROOT.mkdir(parents=True);save(ROOT/'planned_actual_changing_cases.json',tests)
    original_load,original_deps,original_commit=owned.load,owned.check_dependencies,owned.commit_files
    class CommitAttempt(RuntimeError):pass
    def forbidden(*args):commits.append(True);raise CommitAttempt('Commit attempted in negative case')
    try:
        owned.check_dependencies=lambda conf:None;owned.commit_files=forbidden
        frozen_module.contract=lambda:trusted_contract
        owned.contract=lambda:trusted_contract
        for i,test in enumerate(tests):
            bundle={}
            for path,keys,value in test['modifications']:
                key=str(Path(path).resolve());modified=bundle.setdefault(key,deepcopy(original(path)))
                container,last=parent_at(modified,keys);container[last]=deepcopy(value);assert modified!=original(path)
            def injected(path):return bundle.get(str(Path(path).resolve()),original(path))
            owned.load=injected;start=len(commits)
            try:owned.apply_release(image,baseline,config)
            except ValueError as error:
                message=str(error)
                assert any(s in message for s in ['editorial contract:','reconstruction:','Rafael-B49','B49','v2 requires','natural-dialogue-v1']),message
                results.append(dict(case=test['case'],rejected=True,error=message,commit_calls=len(commits)-start,
                    dependency_digests_deliberately_bypassed=True,all_modifications_actual_changes=True))
            except Exception as error:gaps.append(dict(case=test['case'],error_type=type(error).__name__,error=str(error),commit_calls=len(commits)-start))
            else:gaps.append(dict(case=test['case'],unsafe_acceptance=True,commit_calls=len(commits)-start))
            assert image.rom.files is files and image.rom.files==oldfiles and list(image.iter_components())==components
            if (i+1)%5==0:
                save(ROOT/'partial.json',dict(checked=i+1,total=len(tests),rejections=results,gaps=gaps))
                print(i+1,'/',len(tests),'checked;',len(results),'guards/',len(gaps),'gaps',flush=True)
    finally:
        owned.load,owned.check_dependencies,owned.commit_files=original_load,original_deps,original_commit
        frozen_module.contract=original_native_contract;owned.contract=original_owned_contract
    assert trusted_contract==trusted_snapshot==original_native_contract()
    assert before=={str(path):sha(path.read_bytes()) for path in protected}
    save(ROOT/'negative_cases.json',results);save(ROOT/'non_rejection_gaps.json',gaps)
    save(ROOT/'challenge_report.json',dict(planned_cases=len(tests),guard_rejections=len(results),gaps=gaps,
        all_physical_inputs_ROM_registry_ledger_policy_andpins_unchanged=True,config_dependency_digests_deliberately_bypassed=True,
        no_schema_error_unchanged_mutation_orcommit_attempt_counted_asvalid_rejection=True,
        ready_for_registration=not gaps,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(dict(planned=len(tests),guards=len(results),gaps=len(gaps),ready=not gaps),flush=True)
    if gaps:raise SystemExit(1)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),
        positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],
        positive_records=61,negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),
        negative_count=len(results),all_negatives_reject_before_any_files_list_commit=True,
        config_dependency_digests_deliberately_bypassed=True,trusted_frozen_contract_read_once_revalidated_after_all_cases=True,all_semantic_guards_andcommit_traps_active=True,all_shared_files_andROMs_preserved=True,new_credit=0,full_goal_complete=False))
