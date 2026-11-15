"""Actual-changing production challenges with config dependency checks bypassed and commit trapped."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import rafael_B45_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.validate_Rafael_B45_policy_v7902b import SEMANTIC
from scripts.Rafael_B45_release_paths_v7903 import PARENT,ROM,APPROVED,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_atomic_challenges_v7906')
POSITIVE=Path('work/analysis/Rafael_B45_atomic_positive_v7905/positive_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POSITIVE);config=Path(positive['config']);conf=read(config);p=proofs();cache={}
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
        add('formatting-gate-'+row['id'],APPROVED,['records',i,'review','formatting'],False)
    for gate in ['source','context','localization','naturalness']:add('missing-'+gate,APPROVED,['records',0,'review',gate],False)
    for label,index,old,new in SEMANTIC:
        i=indices[index];text=doc['records'][i]['english'];assert old in text
        add('meaning-'+label,APPROVED,['records',i,'english'],text.replace(old,new))
    for field,value in [('file_path','/data/SC2.DK4'),('route',2),('route_identity','Lil'),('block',44),
        ('current_ROM','work/clean.nds'),('current_ROM_sha256','0'*64),('current_ARM9_sha256','0'*64),('current_COMMON_sha256','0'*64),
        ('complete_clean_glosses_precede_current_comparison',False),('target_locale','en-GB'),('translation_policy','natural-dialogue-v1')]:
        add('document-'+field,APPROVED,[field],value)
    for field,value in [('source_hex',doc['records'][0]['source_hex'][:-2]+'00'),('context','Unrelated invented context.'),
        ('speaker','Grandpa'),('compiled_hex',doc['records'][0]['compiled_hex']+'20'),
        ('source_complete_preamble_hex','000000000000')]:
        add('individual-'+field,APPROVED,['records',0,field],value)
    add('unjustified-retention',APPROVED,['records',0,'retention_reason'],'')
    add('erased-record',APPROVED,['records'],doc['records'][:-1])
    add('duplicate-record',APPROVED,['records',1],doc['records'][0])
    add('wrong-zero-selector',APPROVED,['records',0,'source_selector'],6)
    add('wrong-FE-consumer',APPROVED,['records',indices[52],'kind'],'progressive')
    add('wrong-target-reference',APPROVED,['records',0,'target_reference','offset'],doc['records'][0]['target_reference']['offset']+2)
    add('lost-row-reason',APPROVED,['records',0,'row_count_reason'],'')
    for flag in owned.FLAGS:add('map-flag-'+flag,MAP,[flag],False)
    group=original(MAP)['groups'][0]
    for field,value in [('source_header_hex','4353000000000000'),('target_header_hex','4353000000000000'),
        ('approved_manuscript_sha256','0'*64),('source_block_sha256','0'*64),('target_tail_bytes',group['target_tail_bytes']+2)]:
        add('map-group-'+field,MAP,['groups',0,field],value)
    add('command-extent',MAP,['groups',0,'command_map',0,'new_extent'],group['command_map'][0]['new_extent']+2)
    add('stored-reference',MAP,['groups',0,'text_records',0,'new_offset'],group['text_records'][0]['new_offset']+2)
    add('preamble-reference',MAP,['groups',0,'text_records',0,'source_complete_preamble_hex'],'000000000000')
    for i,edge in enumerate(group['relative_fixups']):
        add('relative-endpoint-'+str(i),MAP,['groups',0,'relative_fixups',i,'new_matched_skip_target'],edge['new_matched_skip_target']+2)
    native=original(p['native_font_proof']);stored=original(p['native_stored_proof'])
    for key,value in [('fresh_compiled_alignment_cases',47),('complete_progressive_pages',10),('complete_FE_logical_andphysical_pages',0)]:
        add('native-'+key,p['native_font_proof'],[key],value)
    add('native-compiled',p['native_font_proof'],['records',0,'compiled_hex'],native['records'][0]['compiled_hex']+'20')
    duplicate=deepcopy(native['records']);duplicate[1]=deepcopy(duplicate[0])
    add('native-duplicate-ID',p['native_font_proof'],['records'],duplicate)
    for key,value in [('fresh_native_alignment_cases',27),('exact_reused_native_alignment_cases',19),('all12_native_ink_planes_exact_to_already_viewed',False)]:
        add('stored-'+key,p['native_stored_proof'],[key],value)
    add('stored-expanded',p['native_stored_proof'],['records',0,'expanded_stored_hex'],stored['records'][0]['expanded_stored_hex']+'20')
    add('stored-macro-alignment',p['native_stored_proof'],['records',0,'complete_native_stored_proof','native_alignment','cases',0,'output_hex'],'00')
    actual=original(p['actual_proof'])
    for i,language in enumerate(actual['groups']):
        add('partial-actual-'+str(i),p['actual_proof'],['groups',i,'incomplete_sampled_holds'],1)
        add('wrong-normal-carry-'+str(i),p['actual_proof'],['groups',i,'native_terminal_result',1],0)
        add('wrong-normal-type-'+str(i),p['actual_proof'],['groups',i,'native_terminal_result',0],1)
        add('unknown-trace-'+str(i),p['actual_proof'],['groups',i,'unidentified_trace_rows'],[dict(unknown=True)])
    en=next(i for i,g in enumerate(actual['groups']) if g['version']=='English')
    add('actual-body-mask',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'complete_black_ASCII_gray_CP932_gray_masks_equal'],False)
    add('actual-header-mask',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'complete_name_mask_equal'],False)
    fe=next(i for i,s in enumerate(actual['groups'][en]['speech_observations']) if s['source_selector']==254)
    add('FE-stale-header',p['actual_proof'],['groups',en,'speech_observations',fe,'complete_body_holds',0,'original_FE_absent_nameplate_preserved'],False)
    add('hold-outside-interval',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'frame'],1)
    add('wrong-predicate-result',p['relocated_control_proof'],['relocated_predicate','native_result',1],0)
    add('lost-native-carry',p['relocated_control_proof'],['normal_seeded_ends',1,'native_result',1],0)
    add('wrong-loader-count',p['native_loader_proof'],['fresh_native_whole_loads_andcache_hits'],342)
    add('wrong-parent-mode-count',p['native_loader_proof'],['fresh_initial_parent_modes'],685)
    add('invented-caller-alias',p['native_caller_proof'],['only_original24070_interpreter_call_no_literal_alias'],False)
    add('policy-negative-erased',p['native_policy_validation'],['negative_cases',0,'rejected'],False)
    add('name-scope-closed',p['speaker_name_review'],['full207_name_role_alias_review_active'],False)
    add('wrong-name',p['speaker_name_review'],['records',1,'name'],'Julio Ernesto')
    add('RNG-difference-erased',p['later_scope_proof'],['groups',0,'final_PRNG_seeds',1],2420418440)
    add('RNG-future-limit-erased',p['RNG_scope_proof'],['exact_random_state_andfuture_random_outcome_equality_NOT_verified'],False)
    late=original(p['later_scope_proof'])['groups'][0]
    add('timing-difference-erased',p['later_scope_proof'],['groups',0,'command_comparison_differences'],late['command_comparison_differences'][:-1])
    add('actor-difference-hidden',p['later_scope_proof'],['groups',0,'whole_actors_equal'],False)
    add('later-RGB-difference-hidden',p['later_scope_proof'],['groups',0,'later_full_RGB_comparisons',0,'whole_RGB_equal'],False)
    sf=owned.SOURCE_FONT;add('source-font-record-erased',sf,['source_records'],original(sf)['source_records'][1:])
    actual_en=actual['groups'][en];trace_path=actual_en['observer_report'];trace=original(trace_path)
    first_return=actual_en['command_pairs'][0]['return_row']
    add('trace-result-mismatch',trace_path,['rows',first_return,'result_words',0],0)
    first_entry=actual_en['command_pairs'][0]['entry_row']
    add('trace-wrong-source-route',trace_path,['rows',first_entry,'source','route'],2)
    for key in ['canonical_ROM_sha256','clean_ROM_sha256','parent_ROM_sha256']:
        add('config-'+key,config,[key],'0'*64)
    add('config-proof-path',config,['proofs','actual_proof'],'not-an-approved-proof.json')
    assert len({t['case'] for t in tests})==len(tests)
    protected=[PARENT,ROM,config,APPROVED,MAP,SEAL,Path(owned.__file__),Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')]
    before={str(path):sha(path.read_bytes()) for path in protected}
    image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    files=image.rom.files;oldfiles=list(files);components=list(image.iter_components());results=[];gaps=[];commits=[]
    ROOT.mkdir(parents=True);save(ROOT/'planned_actual_changing_cases.json',tests)
    original_load,original_deps,original_commit=owned.load,owned.check_dependencies,owned.commit_files
    class CommitAttempt(RuntimeError):pass
    def forbidden(*args):commits.append(True);raise CommitAttempt('Commit attempted innegative case')
    try:
        owned.check_dependencies=lambda conf:None;owned.commit_files=forbidden
        for i,test in enumerate(tests):
            bundle={}
            for path,keys,value in test['modifications']:
                key=str(Path(path).resolve());modified=bundle.setdefault(key,deepcopy(original(path)))
                container,last=parent_at(modified,keys);container[last]=deepcopy(value)
                assert modified!=original(path)
            def injected(path):return deepcopy(bundle.get(str(Path(path).resolve()),original(path)))
            owned.load=injected;start=len(commits)
            try:owned.apply_release(image,baseline,config)
            except ValueError as error:
                message=str(error)
                assert any(s in message for s in ['editorial contract:','reconstruction:','Rafael-B45','v2 requires','natural-dialogue-v1']),message
                results.append(dict(case=test['case'],rejected=True,error=message,commit_calls=len(commits)-start,
                    dependency_digests_deliberately_bypassed=True,all_modifications_actual_changes=True))
            except Exception as error:gaps.append(dict(case=test['case'],error_type=type(error).__name__,error=str(error),commit_calls=len(commits)-start))
            else:gaps.append(dict(case=test['case'],unsafe_acceptance=True,commit_calls=len(commits)-start))
            assert image.rom.files is files and image.rom.files==oldfiles and list(image.iter_components())==components
            if (i+1)%10==0:
                save(ROOT/'partial.json',dict(checked=i+1,total=len(tests),rejections=results,gaps=gaps))
                print(i+1,'/',len(tests),'checked;',len(results),'guards/',len(gaps),'gaps',flush=True)
    finally:owned.load,owned.check_dependencies,owned.commit_files=original_load,original_deps,original_commit
    assert before=={str(path):sha(path.read_bytes()) for path in protected}
    save(ROOT/'negative_cases.json',results);save(ROOT/'non_rejection_gaps.json',gaps)
    save(ROOT/'challenge_report.json',dict(planned_cases=len(tests),guard_rejections=len(results),gaps=gaps,
        all_physical_inputs_ROM_registry_ledger_policy_andpins_unchanged=True,
        config_dependency_digests_deliberately_bypassed=True,
        no_schema_error_unchanged_mutation_orcommit_attempt_counted_asvalid_rejection=True,
        ready_for_registration=not gaps,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(dict(planned=len(tests),guards=len(results),gaps=len(gaps),ready=not gaps),flush=True)
    if gaps:raise SystemExit(1)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),
        positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],
        positive_records=12,negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),
        negative_count=len(results),all_negatives_reject_before_any_files_list_commit=True,
        config_dependency_digests_deliberately_bypassed=True,all_shared_files_andROMs_preserved=True,new_credit=0,full_goal_complete=False))
