"""Challenge actual-changing production inputs with dependency checks bypassed andcommit trapped."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import maria_story_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.validate_Maria_story_policy_v7770 import SEMANTIC
from scripts.Maria_story_final_paths_v7771 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_atomic_challenges_v7776')
POSITIVE=Path('work/analysis/maria_story_atomic_v7775c/positive_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POSITIVE);config=Path(positive['config']);conf=read(config);p=conf['proofs'];cache={}
    def original(path):
        key=str(Path(path).resolve())
        if key not in cache:cache[key]=read(path)
        return cache[key]
    tests=[]
    def add(label,path,keys,value):
        current=original(path)
        for key in keys:current=current[key]
        assert current!=value,'Unchanged mutation:'+label
        tests.append(dict(case=label,modifications=[(str(path),keys,deepcopy(value))]))
    doc=original(SEALED);indices={(r['block'],r['source_record_index']):i for i,r in enumerate(doc['records'])}
    for i,row in enumerate(doc['records']):
        add('prose-'+row['id'],SEALED,['records',i,'english'],row['english']+'!')
        add('formatting-gate-'+row['id'],SEALED,['records',i,'review','formatting'],False)
    for gate in ['source','context','localization','naturalness']:
        add('missing-'+gate+'-gate',SEALED,['records',0,'review',gate],False)
    for label,block,index,old,new in SEMANTIC:
        i=indices[block,index];text=doc['records'][i]['english'];assert old in text
        add('meaning-'+label,SEALED,['records',i,'english'],text.replace(old,new))
    for key,value in [('file_path','/data/SC2.DK4'),('route_identity','Lil'),('route',2),
        ('current_ROM','work/clean.nds'),('current_ROM_sha256','0'*64),('current_ARM9_sha256','0'*64),
        ('current_COMMON_sha256','0'*64),('source_ROM_sha256','0'*64),('target_locale','en-GB'),('translation_policy','natural-dialogue-v1')]:
        add('document-'+key,SEALED,[key],value)
    for number in [34,108,35]:
        i=next(i for i,r in enumerate(doc['records']) if r['block']==number)
        add('source-bytes-B'+str(number),SEALED,['records',i,'source_hex'],doc['records'][i]['source_hex'][:-2]+'00')
        add('whole-context-B'+str(number),SEALED,['records',i,'context'],'Unrelated invented context.')
    retained=next(i for i,r in enumerate(doc['records']) if r['editorial_decision']=='retain-wording')
    add('unjustified-retention',SEALED,['records',retained,'retention_reason'],'')
    add('erased-decision',SEALED,['records'],doc['records'][:-1])
    for flag in owned.FLAGS:add('map-flag-'+flag,MAP,[flag],False)
    for i,group in enumerate(original(MAP)['groups']):
        label='B'+str(group['block'])
        add('source-header-'+label,MAP,['groups',i,'source_header_hex'],'4353000000000000')
        add('target-header-'+label,MAP,['groups',i,'target_header_hex'],'4353000000000000')
        add('approved-identity-'+label,MAP,['groups',i,'approved_manuscript_sha256'],'0'*64)
        add('command-map-'+label,MAP,['groups',i,'command_map',0,'new_extent'],group['command_map'][0]['new_extent']+2)
        add('stored-reference-'+label,MAP,['groups',i,'text_records',0,'new_offset'],group['text_records'][0]['new_offset']+2)
        add('target-tail-'+label,MAP,['groups',i,'target_tail_bytes'],group['target_tail_bytes']+2)
        if group['relative_fixups']:add('relative-endpoint-'+label,MAP,['groups',i,'relative_fixups',0,'new_matched_skip_target'],group['relative_fixups'][0]['new_matched_skip_target']+2)
    font=original(p['native_font_proof']);stored=original(p['native_stored_proof']);actual=original(p['actual_proof'])
    for key,value in [('final_complete_pages',68),('all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption',False)]:
        add('font-'+key,p['native_font_proof'],[key],value)
    add('font-compiled',p['native_font_proof'],['records',0,'compiled_hex'],font['records'][0]['compiled_hex']+'20')
    for key,value in [('stored_alignment_coverage',267),('zero_ink_parity_tails',32),('final_complete_native_pages',68),
        ('all67_final_stored_targets_equal_reviewed_complete_native_ink',False)]:
        add('stored-'+key,p['native_stored_proof'],[key],value)
    add('stored-expanded',p['native_stored_proof'],['records',0,'final_expanded_hex'],stored['records'][0]['final_expanded_hex']+'20')
    add('stored-alignment',p['native_stored_proof'],['records',0,'native_pipeline','cases',0,'output_hex'],stored['records'][0]['native_pipeline']['cases'][0]['output_hex']+'20')
    for i,group in enumerate(actual['groups']):
        add('partial-actual-'+str(i),p['actual_proof'],['groups',i,'incomplete_sampled_holds'],1)
        add('normal-return-'+str(i),p['actual_proof'],['groups',i,'native_terminal_result',0],1)
    en=next(i for i,g in enumerate(actual['groups']) if g['version']=='English')
    for key in ['complete_black_body_mask_equal','ASCII_gray_equal','CP932_gray_equal','complete_name_mask_equal']:
        add('actual-'+key,p['actual_proof'],['groups',en,'speech_observations',0,'pages',0,'complete_body_andname_holds',0,key],False)
    add('earned-unlock-claim',p['actual_proof'],['earned_unlock_verified'],True)
    add('unknown-actual-traces',p['actual_proof'],['groups',en,'unidentified_trace_rows'],[dict(unknown=True)])
    later=original(p['later_scope_proof'])
    for i,group in enumerate(later['groups']):
        add('late-seed-'+str(i),p['later_scope_proof'],['groups',i,'final_PRNG_seeds',1],0)
        add('late-timing-erased-'+str(i),p['later_scope_proof'],['groups',i,'command_comparison_differences'],group['command_comparison_differences'][:-1])
        add('actor-difference-hidden-'+str(i),p['later_scope_proof'],['groups',i,'whole_actors_equal'],not group['whole_actors_equal'])
    for key in ['all207_name_role_alias_review_active','shared155_label_semantic_review_still_unresolved_no_asset_edit']:
        add('name-scope-'+key,p['speaker_name_review'],[key],False)
    add('policy-rejection-erased',p['native_policy_validation'],['negative_cases',0,'rejected'],False)
    add('wrong-loader-count',p['native_loader_proof'],['fresh_native_whole_loads_andcache_hits'],302)
    add('caller-alias-invented',p['native_caller_proof'],['only_original24070_interpreter_call_no_literal_alias'],False)
    add('prerequisite-erased',p['source_entry_proof'],['selected_source_events',1,'must_be_completed'],[])
    add('wrong-action',p['source_entry_proof'],['selected_source_events',0,'action_index'],0)
    add('predicate-forcing-claim',p['source_entry_proof'],['no_predicate_completion_flag_actor_roster_orRNG_forcing'],False)
    for key in ['required_runtime_arm9_sha256','required_runtime_common_sha256','canonical_ROM_sha256','clean_ROM_sha256','parent_ROM_sha256']:
        add('config-'+key,config,[key],'0'*64)
    assert len({t['case'] for t in tests})==len(tests)
    protected=[PARENT,ROM,config,SEALED,MAP,SEAL,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')]
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
                key=str(Path(path).resolve());modified=bundle.setdefault(key,deepcopy(original(path)));parent,last=parent_at(modified,keys);parent[last]=deepcopy(value)
            def injected(path):return deepcopy(bundle.get(str(Path(path).resolve()),original(path)))
            owned.load=injected;start=len(commits)
            try:owned.apply_release(image,baseline,config)
            except ValueError as error:
                assert str(error).strip();results.append(dict(case=test['case'],rejected=True,error=str(error),commit_calls=len(commits)-start,dependency_digests_deliberately_bypassed=True,all_modifications_actual_changes=True))
            except Exception as error:gaps.append(dict(case=test['case'],error_type=type(error).__name__,error=str(error),commit_calls=len(commits)-start,not_counted_as_guard_rejection=True))
            else:gaps.append(dict(case=test['case'],error_type='UnsafeAcceptance',commit_calls=len(commits)-start,not_counted_as_guard_rejection=True))
            assert image.rom.files is files and image.rom.files==oldfiles and list(image.iter_components())==components
            if (i+1)%10==0:save(ROOT/'partial.json',dict(checked=i+1,total=len(tests),rejections=results,gaps=gaps));print(i+1,'/',len(tests),'checked;',len(results),'guards/',len(gaps),'gaps',flush=True)
    finally:owned.load,owned.check_dependencies,owned.commit_files=original_load,original_deps,original_commit
    assert before=={str(path):sha(path.read_bytes()) for path in protected}
    save(ROOT/'negative_cases.json',results);save(ROOT/'non_rejection_gaps.json',gaps)
    save(ROOT/'challenge_report.json',dict(planned_cases=len(tests),guard_rejections=len(results),gaps=gaps,
        all_physical_inputs_ROMs_registry_andledger_unchanged=True,all_dependency_digests_deliberately_bypassed=True,
        no_schema_error_unchanged_mutation_orcommit_attempt_counted_asnegative=True,ready_for_registration=not gaps,
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(dict(planned=len(tests),guards=len(results),gaps=len(gaps),ready=not gaps),flush=True)
    if gaps:raise SystemExit(1)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],
        positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        positive_records=67,negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),
        negative_count=len(results),all_negatives_reject_before_any_files_list_commit=True,
        all_schema_exceptions_unchanged_mutations_andcommit_attempts_excluded_fromnegative_count=True,
        all_dependency_digests_deliberately_bypassed=True,all_shared_files_andROMs_preserved=True,new_credit=0,full_goal_complete=False))
