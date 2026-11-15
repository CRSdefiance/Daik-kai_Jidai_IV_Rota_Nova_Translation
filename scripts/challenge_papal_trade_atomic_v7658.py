"""Challenge production guards with actual-changing data and dependency digests bypassed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import papal_trade_editorial_v1 as owned
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_final_paths_v7655 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_atomic_challenges_v7658')
POSITIVE=Path('work/analysis/papal_trade_atomic_v7657/positive_receipt.json')
def parent_at(value,keys):
    for key in keys[:-1]:value=value[key]
    return value,keys[-1]
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POSITIVE);config=Path(positive['config']);conf=read(config)
    assert sha(config.read_bytes())==positive['config_sha256'] and positive['positive_records']==36 and positive['one_final_files_list_commit_after_both_complete_reconstructions']
    tests=[];cache={}
    def original(path):
        key=str(Path(path).resolve())
        if key not in cache:cache[key]=read(path)
        return cache[key]
    def add(label,path,keys,value,additional=None):
        modifications=[(path,keys,value),*(additional or [])]
        for p,k,v in modifications:
            obj,key=parent_at(original(p),k);assert obj[key]!=v,(label,k)
        tests.append(dict(case=label,modifications=modifications))
    def root(label,key,value):add(label,config,[key],value)
    for route,docpath in SEALED.items():
        d=original(docpath);indices={r['source_record_index']:i for i,r in enumerate(d['records'])};ap=APPROVED[route]
        def row(label,index,key,value):
            loc=['records',indices[index],key];add(f'route{route}-'+label,docpath,loc,value,[(ap,loc,value)])
        row('source-reference-shifted',9,'source_reference',{**d['records'][indices[9]]['source_reference'],'offset':29})
        row('wrong-file-qualification',9,'file_path',owned.PATHS[1-route])
        row('wrong-captain-route',9,'route',1-route)
        row('wrong-block',9,'block',[237,246][route])
        row('incomplete-preamble',16,'source_complete_preamble_hex','0040ffff0013ff')
        row('voice-class-changed',16,'source_voice_class',0)
        row('speaker-identity-changed',16,'speaker','Filippo')
        row('missing-context',33,'context','')
        row('missing-retention-reason',12,'retention_reason','')
        row('lost-formatting-gate',33,'review',{**d['records'][indices[33]]['review'],'formatting':False})
        row('lost-read-aloud-context',57,'full_exchange_read_aloud_review',False)
        row('invented-page',57,'native_page_count',2)
        row('expanded-physical-page',57,'original_physical_native_rows_per_page',8)
        row('lost-actual-glyph-proof',9,'actual_record_observed',False)
        row('unscoped-warning',9,'qa_waivers',['weak-line-ending'])
        row('R33-warning-reason-erased',33,'qa_waiver_reason',None)
        row('source-silence-ASCII-compiled',5,'compiled_hex','682e2e2e')
        semantic=[(9,'Filippo','my brother'),(16,'stopped by on business','returned home forever'),(19,'back to your old self','cured of your disease'),(23,"I'm aboard their ship now","I'm only sailing beside their ship now"),(26,'great-grandfather','father'),(33,'almost to Venice','over Venice itself'),(37,'They say','I guarantee'),(40,'donate','pay in taxes'),(43,'My ancestors','Our shared ancestors'),(54,"I've heard",'I know for certain'),(57,'might carry a blessing','guarantees trade profits'),(60,'Divine aid...','Treasure obtained!'),(64,'If we found','Now that we own')]
        for index,before,after in semantic:
            old=d['records'][indices[index]]['english'];assert before in old;row('semantic-source-fact-'+str(index),index,'english',old.replace(before,after))
        row('manual-break',33,'english',d['records'][indices[33]]['english']+'{LB}')
        row('invented-macro',57,'english',d['records'][indices[57]]['english']+'{MACRO:FI}')
        for k in ['source_logical_end','source_tail_bytes','target_logical_end','target_tail_bytes']:
            value=original(MAP)['groups'][route][k];add(f'route{route}-wrong-'+k,MAP,['groups',route,k],value+2)
        add(f'route{route}-A000-operand',MAP,['groups',route,'original_A000_map',0,'source_hex'],'00a0ffff61000110')
        add(f'route{route}-end-offset',MAP,['groups',route,'complete_end_map',0,'target_offset'],1504)
        add(f'route{route}-mapped-command-extent',MAP,['groups',route,'command_map',0,'new_extent'],2)
        add(f'route{route}-stored-reference-offset',MAP,['groups',route,'text_records',0,'new_offset'],14)
        add(f'route{route}-false-storage-parity-tail',MAP,['groups',route,'text_records',1,'parity_space_added'],not original(MAP)['groups'][route]['text_records'][1]['parity_space_added'])
        add(f'route{route}-wrong-archive-source',config,['archives',route,'source_sha256'],'0'*64)
        add(f'route{route}-wrong-archive-target',config,['archives',route,'target_sha256'],'0'*64)
    p=conf['proofs']
    for label,k,key,value in [
      ('native-glyph-oracle-lost','native_font_proof','all_first_internal_final_glyphs_bounds_canaries_consumption_andpair_phase_verified',False),
      ('native-single-page-lost','native_font_proof','all36_single_original_four_row_pages',False),
      ('stored-tail-count-wrong','native_stored_proof','zero_ink_parity_tail_count',0),
      ('stored-fresh-count-wrong','native_stored_proof','fresh_alignment_cases',144),
      ('stored-ink-lost','native_stored_proof','all36_final_stored_targets_equal_reviewed_complete_ink',False),
      ('policy-count-wrong','native_policy_validation','negative_count',0),
      ('actual-unreaped','actual_proof','all_jobs_terminal_andreaped',False),
      ('actual-glyph-proof-lost','actual_proof','all72_complete_leading_internal_final_body_andname_glyphs_bounds_andone_page_verified',False),
      ('actual-R5-CP932-palette-lost','actual_proof','all_four_R5_three_ellipsis_black18_lightgray18_masks_exact',False),
      ('actual-view-lost','actual_view','all72_complete_source_English_speech_panes_individually_viewed',False),
      ('late-equivalence-overclaim','later_scope_proof','no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim',False),
      ('late-differences-erased','later_scope_proof','all_measured_differences_preserved_for_later_older_record_technical_reaudit',False),
      ('name-full-review-overclaim','speaker_name_review','all_broader207_name_role_alias_andearlier_consumers_open',False),
      ('name-font-reuse-reported-fresh','native_name_proof','fresh_name_font_renderer_executions',5),
      ('name-literal-cases-lost','native_name_proof','fresh_native_literal_alignment_cases',0),
      ('loader-entry-modes-lost','native_loader_proof','fresh_initial_parent_modes',0),
      ('caller-alias-scope-lost','native_caller_proof','only_original_24070_interpreter_call_no_literal_alias',False),
    ]:add(label,p[k],[key],value)
    add('accepted-policy-corruption',p['native_policy_validation'],['negative_cases',0,'rejected'],False)
    add('spoken-Filippo-alias-changed',p['speaker_name_review'],['spoken_alias','English'],'Philip')
    for i,r in enumerate(original(p['speaker_name_review'])['records']):
        add(f'name{i}-new-kinship',p['speaker_name_review'],['records',i,'english'],"Carlo's Father")
        add(f'name{i}-null-middle-changed',p['speaker_name_review'],['records',i,'source_fields',2,'current_null'],False)
        if r['actor_ID']==104:add(f'name{i}-relative-as-physical-offset',p['speaker_name_review'],['records',i,'source_fields',1,'current_storage_offset'],960)
    item=p['source_named_item_binding']
    for label,key,value in [('regional-relative-as-absolute','current_deployed_payload_offset',1518924),('regional-absolute-as-relative','current_physical_ARM9_storage_offset',960),('regional-pointer-retargeted','current_pointer',37255712)]:
        add(label,item,['actor104_regional_secondary_storage_contract',key],value)
    for label,key,value in [('item106-wrong-ID','record_ID','DK4_ITEM_POINTER_097'),('item106-wrong-field','pointer_field',1174312),('item106-wrong-static-offset','current_storage_offset',132),('item106-other-consumers-overapproved','current_native_item_getter_card_bounds_mechanics_and_all_other_consumers_not_reviewed_here',False)]:
        add(label,item,['source_named_item',key],value)
    for route in [0,1]:
        add(f'route{route}-invented-prerequisite',p['source_entry_proof'],['groups',route,'selected_source_events',0,'must_be_completed'],[234])
        add(f'route{route}-wrong-action',p['source_entry_proof'],['groups',route,'selected_source_events',0,'action_index'],0)
        add(f'route{route}-seeded-end-result',p['relocated_control_proof'],['groups',route,'normal_terminal_seed_cases',0,'native_result',0],1)
        add(f'route{route}-late-seed-erased',p['later_scope_proof'],['groups',route,'final_PRNG_seeds',1],0)
        add(f'route{route}-late-timing-row-erased',p['later_scope_proof'],['groups',route,'command_comparison_differences'],original(p['later_scope_proof'])['groups'][route]['command_comparison_differences'][:-1])
        add(f'route{route}-late-duration-erased',p['later_scope_proof'],['groups',route,'duration_differences'],original(p['later_scope_proof'])['groups'][route]['duration_differences'][:-1])
        add(f'route{route}-actual-partial-hold',p['actual_proof'],['groups',route*2+1,'incomplete_sampled_holds'],1)
        add(f'route{route}-R5-wrong-ASCII-shadow',p['actual_proof'],['groups',route*2+1,'speech_observations',0,'complete_body_holds',0,'body_shadow_RGB'],[98,97,98])
        add(f'route{route}-incomplete-body-mask',p['actual_proof'],['groups',route*2+1,'speech_observations',1,'complete_body_holds',0,'complete_independent_native_body_mask_equal'],False)
        add(f'route{route}-incomplete-name-mask',p['actual_proof'],['groups',route*2+1,'speech_observations',1,'complete_name_holds',0,'complete_name_first_internal_final_glyphs_andblank_guards_equal'],False)
    add('Hodram-actor-difference-hidden',p['later_scope_proof'],['groups',1,'whole_actors_equal'],True)
    add('Hodram-model-difference-hidden',p['later_scope_proof'],['groups',1,'five_native_component_equality','models'],True)
    root('runtime-wrong','required_runtime_arm9_sha256','0'*64)
    root('COMMON-wrong','required_runtime_common_sha256','0'*64)
    root('canonical-wrong','canonical_ROM_sha256','0'*64)
    root('clean-wrong','clean_ROM_sha256','0'*64)
    require_count=len(tests);assert require_count==len({t['case'] for t in tests}) and require_count>=120
    protected=[PARENT,ROM,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),config,*SEALED.values(),MAP,SEAL]
    before={str(p):sha(p.read_bytes()) for p in protected};image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file_list=image.rom.files;before_files=list(file_list);before_components=list(image.iter_components());results=[]
    ROOT.mkdir(parents=True);save(ROOT/'planned_actual_changing_cases.json',[dict(case=t['case'],targets=[dict(path=str(p),keys=k) for p,k,v in t['modifications']]) for t in tests])
    saved_load,saved_dependencies,saved_commit=owned.load,owned.check_dependencies,owned.commit_files
    def forbidden(*args):raise RuntimeError('Commit attempted during a negative case')
    try:
        owned.check_dependencies=lambda conf:None;owned.commit_files=forbidden
        for i,test in enumerate(tests):
            bundle={}
            for path,keys,value in test['modifications']:
                key=str(Path(path).resolve());doc=bundle.setdefault(key,deepcopy(original(path)));parent,last=parent_at(doc,keys);parent[last]=deepcopy(value)
            def injected(path):return deepcopy(bundle.get(str(Path(path).resolve()),original(path)))
            owned.load=injected
            try:owned.apply_release(image,baseline,config)
            except ValueError as e:
                assert str(e).strip();results.append(dict(case=test['case'],rejected=True,error=str(e),commit_calls=0,dependency_digests_deliberately_bypassed=True,all_modifications_actual_changes=True))
            else:raise RuntimeError('Unsafe input accepted:'+test['case'])
            assert image.rom.files is file_list and image.rom.files==before_files and list(image.iter_components())==before_components
            if (i+1)%20==0:save(ROOT/'partial_negative_cases.json',results);print(f'{i+1}/{require_count} production corruptions rejected before commit',flush=True)
    finally:owned.load,owned.check_dependencies,owned.commit_files=saved_load,saved_dependencies,saved_commit
    assert before=={str(p):sha(p.read_bytes()) for p in protected} and len(results)==require_count
    cases=ROOT/'negative_cases.json';save(cases,results)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=36,negative_cases=str(cases),negative_cases_sha256=sha(cases.read_bytes()),negative_count=len(results),all_negatives_reject_before_any_files_list_commit=True,all_schema_exceptions_unchanged_mutations_andcommit_attempts_excluded_fromnegative_count=True,all_dependency_digests_deliberately_bypassed=True,source_owned_guard_failures_not_dependency_hash_shortcuts=True,all_shared_ledger_registry_ROMs_andsource_evidence_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(f'36-record positive /{len(results)} production corruptions:all rejected before the single commit boundary. Inputs/ROM/registry/ledger unchanged;zero credit.',flush=True)
