"""Inject changed valid-shape metadata with production dependency checks bypassed; never commit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B218_retrospective_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.retrospective_B218_final_paths_v7853 import *
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_atomic_challenges_v7855')
POSITIVE=Path('work/analysis/retrospective_B218_atomic_v7854b/positive_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(POSITIVE);config=Path(receipt['config']);conf=read(config)
    assert receipt['positive_records']==13 and receipt['one_final_files_list_commit_after_complete_reconstruction']
    assert sha(config.read_bytes())==receipt['config_sha256'] and receipt['whole_ROM_equals_pinned_research_reference']
    paths={str(config),str(SEALED),str(APPROVED),str(MAP),str(SEAL),*proofs().values()}
    originals={str(Path(p).resolve()):read(p) for p in paths}
    configs={str(config):conf,**{key:value for key,value in proofs().items()}}
    cases=[]
    def case(label,changes,guard):
        changes=[(str(Path(p).resolve()),path,value) for p,path,value in changes]
        for file,path,value in changes:
            parent,key=parent_at(originals[file],path)
            assert parent[key]!=value,(label,'no-op',path)
        cases.append(dict(label=label,changes=changes,expected_guard=guard))
    C=str(config);D=str(SEALED);A=str(APPROVED);M=str(MAP);S=str(SEAL);P=proofs()
    def rowcase(label,i,key,value,guard):
        case(label,[(D,['records',i,key],value),(A,['records',i,key],value)],guard)
    case('wrong-policy-format',[(C,['format'],'dk4-unreviewed-release-v1')],'sealed configuration')
    case('redirect-proof-map',[(C,['proofs','actual'],P['policy'])],'sealed configuration')
    case('wrong-parent',[(C,['parent_ROM_sha256'],'0'*64)],'current parent')
    case('wrong-canonical',[(C,['canonical_ROM_sha256'],'0'*64)],'canonical baseline')
    case('wrong-clean',[(C,['clean_ROM_sha256'],'0'*64)],'clean ROM')
    for key in ['required_runtime_arm9_sha256','required_runtime_common_sha256']:
        case(key,[(C,[key],'0'*64)],'exact runtime')
    case('foreign-file-matrix',[(C,['predecessor_file_hashes','/data/SC0.DK4'],'0'*64)],'complete predecessor')
    for flag in FLAGS:case('map-flag-'+flag,[(M,[flag],False)],'sealed map flags')
    for key,value in [('source_bytes',1018),('source_logical_end',1014),('source_tail_bytes',2),
                      ('target_bytes',1024),('target_logical_end',1020),('target_tail_bytes',0)]:
        case('extent-'+key,[(M,['groups',0,key],value)],'exact block extents')
    case('wrong-route',[(M,['groups',0,'route'],3)],'original block entry')
    case('wrong-entry',[(M,['groups',0,'original_entry_payload_offset'],10)],'original block entry')
    case('unapproved-reference',[(S,['all13_individual_gates_andexact_references_sealed'],False)],'complete reference seal')
    case('invented-duplicate-credit',[(D,['new_credit'],1)],'retrospective no duplicate credit')
    case('unapproved-locale',[(D,['target_locale'],'en-GB')],'reviewed en-US policy')
    case('unapproved-natural-dialogue-policy',[(D,['translation_policy'],'natural-dialogue-v1')],'reviewed en-US policy')
    case('wrong-archive-reference',[(C,['archives',0,'target_sha256'],'0'*64)],'complete target archive')
    for i,row in enumerate(originals[str(SEALED.resolve())]['records']):
        ident=row['id']
        rowcase(ident+'-invented-family',i,'english',row['english']+" She's my sister.",'reviewed unchanged wording')
        review=deepcopy(row['review']);review['formatting']=False
        rowcase(ident+'-unapproved-formatting',i,'review',review,'reviewed unchanged wording')
        rowcase(ident+'-no-retention-reason',i,'retrospective_wording_reason','','individual wording retention')
        rowcase(ident+'-missing-final-compiled-glyph',i,'compiled_hex',row['compiled_hex'][:-2],'exact compiled/QA')
        reference=deepcopy(row['current_reference']);reference['offset']+=2
        rowcase(ident+'-wrong-current-offset',i,'current_reference',reference,'exact source/current')
    for key,value in [('total_actual_pages',25),('total_actual_complete_body_andheader_holds',101),('total_incomplete_sampled_holds',1)]:
        case('actual-'+key,[(P['actual'],[key],value)],'complete actual English scope')
    case('undisclosed-Japanese-claim',[(P['actual'],['previous_andproposed_English_only_no_new_Japanese_capture'],False)],'honest actual scope')
    case('unviewed-sheets',[(P['actual_view'],['all_eight_sheets_directly_viewed'],False)],'actual visual binding')
    case('unviewed-native-plane',[(P['native_font'],['all_first_internal_andfinal_characters_complete_in_order'],False)],'changed native display')
    case('unproved-parity-tail',[(P['stored_controls'],['changed_parity_tail_zero_ink_complete_characters_bounds_andconsumption'],False)],'final stored coverage')
    case('loader-gap',[(P['loader'],['whole_SC2_loads_andcache_hits'],335)],'original archive loader')
    case('caller-alias',[(P['caller'],['only_original24070_interpreter_call_andno_literal_alias'],False)],'bounded original caller')
    case('empty-policy-rejection-count',[(P['policy'],['negative_count'],220)],'actual-changing policy checks')
    case('late-RGB-evidence-corruption',[(P['actual'],['later_sampled_whole_frame_comparisons',0,'whole_RGB_equal'],False)],'later sampled RGB')
    case('hidden-duration-difference',[(P['actual'],['duration_difference_rows'],1)],'complete measured comparison contract')
    case('hidden-actor-difference',[(P['actual'],['final_native_values',1,'whole_actor_sha256'],'0'*64)],'measured actors andRNG')
    case('hidden-RNG-difference',[(P['actual'],['final_native_values',1,'seed'],3000421370)],'measured actors andRNG')
    for gi in [0,1]:
        path=['groups',gi]
        case(f'group{gi}-wrong-return',[(P['actual'],path+['normal_terminal_result'],[0,1])],'complete actual return')
        case(f'group{gi}-wrong-header',[(P['actual'],path+['panels',0,'speaker_name'],'Maria Li')],'actual source speaker andpage')
        case(f'group{gi}-partial-body',[(P['actual'],path+['incomplete_sampled_holds'],1)],'all complete actual speeches')
        case(f'group{gi}-unproved-complete-hold',[(P['actual'],path+['panels',0,'complete_body_andheader_holds',0,'complete_native_body_black_gray_andnameplate_masks_equal'],False)],'complete actual native masks')
        interval=deepcopy(originals[str(Path(P['actual']).resolve())]['groups'][gi]['panels'][0]['interval']);interval['returned']+=1
        case(f'group{gi}-wrong-interval',[(P['actual'],path+['panels',0,'interval'],interval)],'actual interval/source association')
        case(f'group{gi}-wrong-body-plane',[(P['actual'],path+['panels',0,'native_stored_plane_sha256'],'0'*64)],'actual final stored plane association')
        changed_result=deepcopy(originals[str(Path(P['actual']).resolve())]['groups'][gi]['command_pairs'][0]['native_result']);changed_result[0]^=1
        case(f'group{gi}-changed-result-evidence',[(P['actual'],path+['command_pairs',0,'native_result'],changed_result)],'actual measurements equal original trace')
        report=originals[str(Path(P['actual']).resolve())]['groups'][gi]['capture_report']
        report_key=str(Path(report).resolve());originals[report_key]=read(report)
        case(f'group{gi}-savestate-claim',[(report,['savestate_loaded'],True)],'actual cold boot')
        observer=originals[str(Path(P['actual']).resolve())]['groups'][gi]['observer_report']
        observer_key=str(Path(observer).resolve());originals[observer_key]=read(observer)
        case(f'group{gi}-mutating-observer',[(observer,['mismatches'],1)],'read-only original observation')
    changed_seed=originals[str(Path(P['actual']).resolve())]['command_comparisons'][0]['previous']['before_RNG']^1
    case('comparison-RNG-omission',[(P['actual'],['command_comparisons',0,'previous','before_RNG'],changed_seed)],'complete command comparison association')
    require_count=len(cases);assert require_count>=120
    ROOT.mkdir(parents=True);save(ROOT/'planned_cases.json',cases)
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    protected={str(p):sha(Path(p).read_bytes()) for p in [PARENT,ROM,SEALED,APPROVED,MAP,SEAL,
        Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/release_stack.json'),
        Path('translations/rom_retention_pins.json'),Path(owned.__file__),config]}
    original_load,original_dependencies,original_commit=owned.load,owned.check_dependencies,owned.commit_files
    results=[];gaps=[]
    class EarlyCommit(RuntimeError):pass
    try:
        owned.check_dependencies=lambda _:None
        for index,spec in enumerate(cases):
            overrides={}
            for file,path,value in spec['changes']:
                if file not in overrides:overrides[file]=deepcopy(originals[file])
                parent,key=parent_at(overrides[file],path);parent[key]=deepcopy(value)
            def injected(path):
                key=str(Path(path).resolve())
                return deepcopy(overrides[key]) if key in overrides else original_load(path)
            owned.load=injected;calls=[];image=NdsImage.open(PARENT);files=image.rom.files;before=tuple(files)
            def forbidden(im,values):
                calls.append(True);raise EarlyCommit('Production attempted to commit before rejecting corruption')
            owned.commit_files=forbidden;error=None;rejected=False
            try:owned.apply_release(image,baseline,config)
            except ValueError as e:
                error=str(e);rejected=spec['expected_guard'] in error
            except Exception as e:error=type(e).__name__+': '+str(e)
            unchanged=image.rom.files is files and tuple(image.rom.files)==before
            row=dict(index=index,label=spec['label'],expected_guard=spec['expected_guard'],rejected=rejected,
                error=error,commit_calls=len(calls),input_file_list_andall_file_bytes_unchanged=unchanged,
                actual_changed_metadata=True,production_dependency_check_bypassed=True)
            results.append(row)
            if not rejected or calls or not unchanged:gaps.append(row)
            save(ROOT/'partial_cases.json',results)
            if index%10==0:print('Production challenge',index+1,'/',require_count,'gaps',len(gaps),flush=True)
    finally:
        owned.load=original_load;owned.check_dependencies=original_dependencies;owned.commit_files=original_commit
    assert protected=={path:sha(Path(path).read_bytes()) for path in protected}
    save(ROOT/'negative_cases.json',results);save(ROOT/'non_rejection_gaps.json',gaps)
    save(ROOT/'challenge_report.json',dict(count=len(results),gaps=gaps,all_physical_protected_files_unchanged=True,
        no_schema_exception_ornoop_orcommit_attempt_counted_as_success=True,full_goal_complete=False))
    assert not gaps and len(results)==require_count
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),
        positive_proof=receipt['positive_proof'],positive_proof_sha256=receipt['positive_proof_sha256'],
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=13,changed_records=1,
        negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),
        negative_count=len(results),all_negatives_reject_before_any_files_list_commit=True,
        all_dependency_digests_deliberately_bypassed=True,dependency_bypass_scope='Production config dependency checks;frozen policy guards remain active andno physical files are altered.',
        every_case_changes_input_with_same_valid_shape_andall_errors_match_guard=True,
        complete_input_files_list_andall_physical_protected_artifacts_unchanged=True,
        no_duplicate_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Atomic B218 retrospective:',len(results),'actual-changing rejections/zero commits;all physical files unchanged.')
