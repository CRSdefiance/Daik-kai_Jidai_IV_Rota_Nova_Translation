"""Challenge production guards with actual-changing data andhash checks bypassed; report gaps honestly."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria_B207_editorial_v1 as owned
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_B207_final_paths_v7712 import *
from scripts.validate_Maria_B207_policy_v7695 import SEMANTIC
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_atomic_challenges_v7715')
POSITIVE=Path('work/analysis/maria_B207_atomic_v7714/positive_receipt.json')
def parent_at(value,keys):
    for key in keys[:-1]:value=value[key]
    return value,keys[-1]
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POSITIVE);config=Path(positive['config']);conf=read(config)
    assert sha(config.read_bytes())==positive['config_sha256'] and positive['positive_records']==18 and positive['one_final_files_list_commit_after_complete_reconstruction']
    tests=[];cache={}
    def original(path):
        key=str(Path(path).resolve())
        if key not in cache:cache[key]=read(path)
        return cache[key]
    def add(label,path,keys,value,additional=None):
        modifications=[(path,keys,value),*(additional or [])]
        for p,k,v in modifications:obj,key=parent_at(original(p),k);assert obj[key]!=v,(label,k)
        tests.append(dict(case=label,modifications=modifications))
    docpath=SEALED[3];ap=APPROVED[3];d=original(docpath);indices={r['source_record_index']:i for i,r in enumerate(d['records'])}
    def row(label,index,key,value):
        loc=['records',indices[index],key];add(label,docpath,loc,value,[(ap,loc,value)])
    def doc(label,key,value):add(label,docpath,[key],value,[(ap,[key],value)])
    for r in d['records']:
        raw=bytes.fromhex(r['source_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);row('source-container-'+r['id'],r['source_record_index'],'source_hex',bad.hex())
        raw=bytes.fromhex(r['compiled_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);row('compiled-container-'+r['id'],r['source_record_index'],'compiled_hex',bad.hex())
    row('source-reference-shifted',8,'source_reference',{**d['records'][indices[8]]['source_reference'],'offset':29})
    row('wrong-file-qualification',8,'file_path','/data/SC2.DK4');row('wrong-route',8,'route_identity','Lil');row('wrong-block',8,'block',206)
    row('incomplete-preamble',15,'source_complete_preamble_hex','0040ffff0013ff');row('wrong-voice',15,'source_voice_class',0);row('wrong-speaker',15,'speaker','Filippo')
    row('missing-context',32,'context','');row('missing-retention-reason',11,'retention_reason','')
    row('lost-formatting-gate',32,'review',{**d['records'][indices[32]]['review'],'formatting':False})
    row('lost-whole-exchange-cadence',56,'whole_English_exchange_cadence_andemotional_progression_reviewed',False)
    row('invented-page',56,'native_page_count',2);row('expanded-physical-page',56,'original_physical_native_rows_per_page',8)
    row('lost-actual-record',8,'actual_record_observed',False);row('unscoped-waiver',8,'qa_waivers',['weak-line-ending'])
    row('source-gloss-corrupted',56,'source_meaning','This proves a guaranteed cash reward.')
    row('Japanese-source-corrupted',8,'source_Japanese','兄弟だよ');row('row-reason-erased',36,'row_count_reason',None)
    for label,index,old,new in SEMANTIC:
        text=d['records'][indices[index]]['english'];assert old in text;row('semantic-'+label,index,'english',text.replace(old,new))
    row('manual-break',32,'english',d['records'][indices[32]]['english']+'{LB}');row('invented-macro',56,'english',d['records'][indices[56]]['english']+'{MACRO:FI}')
    for label,key,value in [('wrong-document-file','file_path','/data/SC2.DK4'),('wrong-document-route','route_identity','Lil'),('wrong-document-current-ROM','current_ROM','work/clean.nds'),('wrong-document-current-ROM-hash','current_ROM_sha256','0'*64),('wrong-document-ARM9-hash','current_ARM9_sha256','0'*64),('wrong-document-COMMON-hash','current_COMMON_sha256','0'*64),('wrong-document-clean-hash','source_ROM_sha256','0'*64)]:doc(label,key,value)
    for k in owned.FLAGS:add('map-flag-'+k,MAP,[k],False)
    for k in ['source_logical_end','source_tail_bytes','target_logical_end','target_tail_bytes']:
        add('map-wrong-'+k,MAP,['groups',0,k],original(MAP)['groups'][0][k]+2)
    add('A000-operand',MAP,['groups',0,'original_A000_map',0,'source_hex'],'00a0ffff61000110')
    add('end-offset',MAP,['groups',0,'complete_end_map',0,'target_offset'],1468)
    add('mapped-command-extent',MAP,['groups',0,'command_map',0,'new_extent'],2)
    add('stored-reference-offset',MAP,['groups',0,'text_records',0,'new_offset'],14)
    add('stored-parity-tail',MAP,['groups',0,'text_records',1,'parity_space_added'],not original(MAP)['groups'][0]['text_records'][1]['parity_space_added'])
    add('stored-record-index',MAP,['groups',0,'text_records',1,'new_record_index'],0)
    for key in ['source_sha256','target_sha256']:add('wrong-archive-'+key,config,['archives',0,key],'0'*64)
    p=conf['proofs']
    for label,pk,key,value in [
        ('native-glyph-oracle','native_font_proof','all_first_internal_final_glyphs_bounds_canaries_consumption_andpair_phase_verified',False),
        ('native-page','native_font_proof','all18_single_original_four_row_pages',False),
        ('stored-tail-count','native_stored_proof','zero_ink_parity_tail_count',0),
        ('stored-fresh-count','native_stored_proof','fresh_alignment_cases',72),
        ('stored-ink','native_stored_proof','all18_final_stored_targets_equal_reviewed_complete_ink',False),
        ('policy-count','native_policy_validation','negative_count',0),
        ('actual-unreaped','actual_proof','all_jobs_terminal_andreaped',False),
        ('actual-glyph-proof','actual_proof','all36_occurrences_complete_leading_internal_final_body_andname_glyphs_bounds_andone_page_verified',False),
        ('actual-CP932-palette','actual_proof','both_R4_three_ellipsis_black18_lightgray18_masks_exact',False),
        ('actual-view','actual_view','all36_complete_source_English_speech_panes_individually_viewed',False),
        ('late-overclaim','later_scope_proof','no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim',False),
        ('late-differences-erased','later_scope_proof','all_measured_differences_preserved_for_later_older_record_technical_reaudit',False),
        ('name-full-review-overclaim','speaker_name_review','all_broader207_name_role_alias_andearlier_consumers_open',False),
        ('name-font-reuse-fresh','native_name_proof','fresh_name_font_renderer_executions',5),
        ('name-literal-cases','native_name_proof','fresh_native_literal_alignment_cases',0),
        ('loader-modes','native_loader_proof','fresh_initial_parent_modes',0),
        ('caller-alias','native_caller_proof','only_original_24070_interpreter_call_no_literal_alias',False),
        ('earned-unlock-overclaim','actual_proof','earned_unlock_verified',True),
    ]:add(label,p[pk],[key],value)
    add('policy-corruption',p['native_policy_validation'],['negative_cases',0,'rejected'],False)
    add('spoken-alias',p['speaker_name_review'],['spoken_alias','English'],'Philip')
    for i,r in enumerate(original(p['speaker_name_review'])['records']):
        add('name-kinship-'+str(i),p['speaker_name_review'],['records',i,'english'],"Carlo's Father")
        add('name-middle-'+str(i),p['speaker_name_review'],['records',i,'source_fields',2,'current_null'],False)
        if r['actor_ID']==104:add('name-relative-as-physical',p['speaker_name_review'],['records',i,'source_fields',1,'current_storage_offset'],960)
    item=p['source_named_item_binding']
    for label,key,value in [('regional-relative-as-absolute','current_deployed_payload_offset',1518924),('regional-absolute-as-relative','current_physical_ARM9_storage_offset',960),('regional-pointer','current_pointer',37255712)]:add(label,item,['actor104_regional_secondary_storage_contract',key],value)
    for label,key,value in [('item-ID','record_ID','DK4_ITEM_POINTER_097'),('item-field','pointer_field',1174312),('item-offset','current_storage_offset',132),('item-other-consumers','current_native_item_getter_card_bounds_mechanics_and_all_other_consumers_not_reviewed_here',False)]:add(label,item,['source_named_item',key],value)
    add('invented-prerequisite',p['source_entry_proof'],['selected_source_event','must_be_completed'],[234]);add('wrong-action',p['source_entry_proof'],['selected_source_event','action_index'],0)
    add('seeded-end-result',p['relocated_control_proof'],['normal_terminal_seed_cases',0,'native_result',0],1)
    for label,keys,value in [('late-seed',['final_PRNG_seeds',1],0),('actor-difference-hidden',['whole_actors_equal'],True),('model-difference-hidden',['five_native_component_equality','models'],True),('calendar-difference-hidden',['five_native_component_equality','calendar'],True),('late-timing-erased',['command_comparison_differences'],original(p['later_scope_proof'])['groups'][0]['command_comparison_differences'][:-1]),('late-duration-erased',['duration_differences'],original(p['later_scope_proof'])['groups'][0]['duration_differences'][:-1])]:add(label,p['later_scope_proof'],['groups',0,*keys],value)
    en=next(i for i,g in enumerate(original(p['actual_proof'])['groups']) if g['version']=='English')
    add('actual-partial',p['actual_proof'],['groups',en,'incomplete_sampled_holds'],1)
    add('R4-ASCII-shadow',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'body_shadow_RGB'],[98,97,98])
    add('incomplete-body',p['actual_proof'],['groups',en,'speech_observations',1,'complete_body_holds',0,'complete_independent_native_body_mask_equal'],False)
    add('incomplete-name',p['actual_proof'],['groups',en,'speech_observations',1,'complete_name_holds',0,'complete_name_first_internal_final_glyphs_andblank_guards_equal'],False)
    for k in ['required_runtime_arm9_sha256','required_runtime_common_sha256','canonical_ROM_sha256','clean_ROM_sha256']:add('config-'+k,config,[k],'0'*64)
    assert len(tests)==len({t['case'] for t in tests}) and len(tests)>=120
    protected=[PARENT,ROM,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),config,*SEALED.values(),MAP,SEAL];before={str(p):sha(p.read_bytes()) for p in protected}
    image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');files=image.rom.files;oldfiles=list(files);components=list(image.iter_components());results=[];gaps=[];commit_calls=[]
    ROOT.mkdir(parents=True);save(ROOT/'planned_actual_changing_cases.json',[dict(case=t['case'],targets=[dict(path=str(p),keys=k) for p,k,v in t['modifications']]) for t in tests])
    saved_load,saved_deps,saved_commit=owned.load,owned.check_dependencies,owned.commit_files
    class CommitAttempt(RuntimeError):pass
    def forbidden(*args):commit_calls.append(True);raise CommitAttempt('Commit attempted during a negative case')
    try:
        owned.check_dependencies=lambda conf:None;owned.commit_files=forbidden
        for i,test in enumerate(tests):
            bundle={}
            for path,keys,value in test['modifications']:
                key=str(Path(path).resolve());value_doc=bundle.setdefault(key,deepcopy(original(path)));parent,last=parent_at(value_doc,keys);parent[last]=deepcopy(value)
            def injected(path):return deepcopy(bundle.get(str(Path(path).resolve()),original(path)))
            owned.load=injected;start_commits=len(commit_calls)
            try:owned.apply_release(image,baseline,config)
            except ValueError as e:
                assert str(e).strip();results.append(dict(case=test['case'],rejected=True,error=str(e),commit_calls=len(commit_calls)-start_commits,dependency_digests_deliberately_bypassed=True,all_modifications_actual_changes=True))
            except Exception as e:gaps.append(dict(case=test['case'],error_type=type(e).__name__,error=str(e),commit_calls=len(commit_calls)-start_commits,not_counted_as_guard_rejection=True))
            else:gaps.append(dict(case=test['case'],error_type='UnsafeAcceptance',commit_calls=len(commit_calls)-start_commits,not_counted_as_guard_rejection=True))
            assert image.rom.files is files and image.rom.files==oldfiles and list(image.iter_components())==components
            if (i+1)%20==0:save(ROOT/'partial.json',dict(rejections=results,gaps=gaps));print(f'{i+1}/{len(tests)} checked;{len(results)} guards/{len(gaps)} gaps',flush=True)
    finally:owned.load,owned.check_dependencies,owned.commit_files=saved_load,saved_deps,saved_commit
    assert before=={str(p):sha(p.read_bytes()) for p in protected}
    save(ROOT/'negative_cases.json',results);save(ROOT/'non_rejection_gaps.json',gaps)
    save(ROOT/'challenge_report.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],planned_cases=len(tests),guard_rejections=len(results),gaps=gaps,all_physical_inputs_ROMs_registry_ledger_unchanged=True,all_dependency_digests_deliberately_bypassed=True,no_schema_error_orcommit_attempt_counted_as_rejection=True,ready_for_registration=not gaps,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(dict(planned=len(tests),guard_rejections=len(results),gaps=len(gaps),ready_for_registration=not gaps),flush=True)
    if gaps:raise SystemExit(1)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=18,negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),negative_count=len(results),all_negatives_reject_before_any_files_list_commit=True,all_schema_exceptions_unchanged_mutations_andcommit_attempts_excluded_fromnegative_count=True,all_dependency_digests_deliberately_bypassed=True,source_owned_guard_failures_not_dependency_hash_shortcuts=True,all_shared_ledger_registry_ROMs_andsource_evidence_unchanged=True,new_credit=0,full_goal_complete=False))
