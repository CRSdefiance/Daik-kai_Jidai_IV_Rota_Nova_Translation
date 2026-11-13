"""Credit fifteen disjoint integrated B47 decisions after release/startup; recover prior ledger exactly."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.Rafael_B47_release_paths_v8006 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_completion_v8018')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8019')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8008/verified_handoff.json')
RELEASE=Path('work/analysis/Rafael_B47_release_v8014/registered_release_verification.json')
START=Path('work/analysis/Rafael_B47_context_binding_v8016/own_Rafael_startup_andstrict_captain0_context.json')
START_VIEW=Path('work/analysis/Rafael_B47_startup_view_v8017/own_Rafael_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/Rafael_B47_atomic_challenges_v8011/atomic_validation_receipt.json')
REGISTRATION=Path('work/analysis/Rafael_B47_registration_v8012/registration_receipt_corrected.json')
FINAL=Path('translations/rafael_B47_contextual_final_review_v1.json')
KEY='Rafael_SC0B47_completion_v8018'
FAMILY='Rafael_SC0B47_contextual_Mediterranean_advice_v8018'
SCOPE='unfinished_editorial_scope_v8018'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6976,6979,6979,4361,2615)
AFTER=(6991,6994,6994,4369,2622)
UNVISITED=['DK4_MES_B47_R0017','DK4_MES_B47_R0063','DK4_MES_B47_R0092','DK4_MES_B47_R0122']
INTRO="Rafael B47 is complete in current registered experimental cumulative V8013:15 speeches,eight revisions andseven individually justified retentions credited once. Totals are6,991 completed/6,994 source-prose records anddrafts/4,369 integrated revisions/2,622 retentions;SC0 188 androute subset5,391. All636 manifest batches/114 accepted layers/18 release checks/110 regressions,whole-reference equality andexact clean-input patch reconstruction pass. MainV4701 remains unchanged. The full editorial goal is active."
DETAILS="""Fresh clean Japanese,complete B37 prerequisite context,source glosses,names andall six original conditional text paths preceded current English. Exact source/current/effective/compiled/stored/actual/integrated references andindividual retention reasons are in translations/rafael_B47_contextual_final_review_v1.json. Preserve Hayreddin's ambiguous intent andguarded passage relief,approximate eastern-half Ottoman/Pasha domain andconditional danger,exclusive R63/R70 Mediterranean conclusions,practical caution about trading contracts,qualified navigator recruitment,ship andpersonal preparation,brief overwhelm andrenewed resolve. No invented kinship,rank,alliance,guaranteed recruitment orprotection.

All15 native paragraphs/16 pages/60 compiled alignments pass. Eight stored parity tails pass32 fresh alignments;seven exact bodies reuse28. Every full glyph,leading/trailing character,bound andconsumed byte is accounted for. Complete six-byte preambles,five source00 actors,zero macros,48 commands,24 nested relative spans,six raw predicates,61FF,A000 andfull normal end remain. Source/relocated branch cases each cover120;625 source-result compositions/six paths remain offline evidence. Clean/predecessor blocks andwhole predecessor archive invert exactly;342 other SC0 blocks andevery other file/component match V7964. Native loaders343/cache paths686parent modes andshipped callers are bound.

Two disclosed original-entry fixtures preserve all B47 controls after the original ten-command B44 setup;ordinary-input cold boots run32,002 frames total. Eleven unique speeches each language/22speech occurrences/23page observations/88 complete body-name holds are actual coverage. R17,R63,R92,R122 andJanus's header remain native-only. All eight review sheets were directly viewed. R53's English first page ends atterritory.;ordinary A4720 turns from4690 to4750 within the same command to the complete conditional warning,then R70 displays. Full initial I/native[6,0] origin/final chance. andcomplete nameplates survive. These fixtures do not prove natural event selection,earned prerequisites,original location,fullroute orhardware verification.

Source/English normal returns[0,0] occur at6416/6655,English239frames later. All45selected command results/UI requests and11paired upper scenes/portraits/headers match. Preserve24comparison rows/four duration differences. R53 lasts241/481frames with58/116LCGadvances;English is58steps ahead at B47exit. Later all157sampled wholeRGBpairs differ;state/tasks match,models/persistent objects/calendar/whole actors differ. Final seeds19668379/4016462114 correspond to English7833steps behind in bounded phase arithmetic. Raw calendars ticks1900/[1,8,28] versus1123/[0,23,19] retain original zero-based fields. Original wait/generator code equality is not an every-call causal trace orfuture random/fullsimulation equivalence. Every measurement remains forlater older-record technical re-audit;incidental B127/Sailor prose receives no credit.

Rafael Castor,Janus Pasar,Claudio Manaus andJulio Erneco retain exact source-bound identities. Three actual progressive headers are verified;Janus is native-only. Pasar/パサー differs from Pasha/パシャ. Valdes/Pasha/Hayreddin havecomponent-only retentions;Pedro's middleデ andHayreddin's omitted sourceファーズル remain full207-name leads. Fullcatalogue UI,custom player names andother consumers remain open.

The frozen source-bound policy permitsR53 alone8 totalrows/two original four-row pages;all other records4/onepage. Global216px/four-row geometry,bodyNULguard andFI6/FA6/FO10 measurements remain. Six original row-count infos andtwo exact warning exceptions remain:R5line2to/get andR63line2with/Pasha's. Each exception binds source/id/English/compiledbytes/line andwritten reason;no diagnostic is removed orglobal rule relaxed. R5/R63 use fuller three-row wraps without lost words. All15positive plans/302actual-changing policy rejections pass. Atomic reconstruction commits one files list only aftercomplete checks;wholeROM equals pinned reference. All202independent corruptions reject precommit withdependency hashes bypassed. Preserve theoriginal registration receipt's stale187/635diagnostic counts andstdout;the separately verified corrected receipt binds202/636/one15-record manifest/V8013 without replay.

Fresh ordinary own-V8013 Rafael startup runs4,001frames,withsix wholeRGBpairs/captain0/wholeactor controls equal toV7964 andstrict2b6/COMMON/directory/123264payload guards. The sheet is directly viewed. Own-current input is work/analysis/current_V8013_Rafael_native_v8016/current_native_input.json. Earlier source/native/stored/actual B47 checks are reused byexact full-reference equality. All earlier translations,ROMs,drafts,failed/executed producers andproofs remain. Graphics/all18plaques andlater older-record technical re-audit remain separate. No separate unified package,promotion,pruning,commit orpush."""
NEXT="""Continue the full editorial goal from verifiedV8019/current registeredV8013. B47's15 speeches are complete andcredited once;reuse all verified source/context/names/native/stored/representative-actual/policy/atomic/release/patch/startup evidence without needless replay. Use own-current Rafael input work/analysis/current_V8013_Rafael_native_v8016/current_native_input.json. Other routes' earlier contexts remain historical until properly rebound orrecaptured.

Select the next untouched complete clean exchange withits exact EV/caller/conditional/prerequisite context before reading current English;block order alone is not chronology. B47/B37 context andincidental B127/Sailor captures are previously exposed leads,not newly unread sources. Preserve full coverage across allfour storylines,earlier translations,sharedshop/town/random/Help/remaining prose,all207names/roles/aliases andretrospective prematurewrapping. Keep allprior unfinished inventories,thetwelve contraction/question-tag leads,unscanned records beyond558plans andinherited weak-before-row lead. Do not mechanically minimize rows orreverse a justified phrase retention such asB46R23 may challenge.

Preserve historical JanusPasha counterpart queues whiledistinguishing Pasar from Pasha;no global replacement. Retain every older item/counterpart/display lead,Trader/PortWorker/Guildmaster,Sailor151-159 versusRetainer consumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andother recorded open work. Keep graphics/all18plaques andlater older-record technical re-audit separate,including normal-end valuecarry,B35R65's source-only nineteenthcell andall measured timing/highlight/RNG/component/calendar/RGB limits. Preserve every ROM,translation,draft,failure,executedproducer andproof. MainV4701 unchanged;fullgoal active,no separate unified package,promotion,pruning,commit orpush."""

def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256']
            del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    release,start,view,atomic,doc,seal,reg=map(read,[RELEASE,START,START_VIEW,ATOMIC,APPROVED,SEAL,REGISTRATION])
    rom=Path(release['candidate']);manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert sha(rom.read_bytes())==release['candidate_sha256']==manifest['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']
    assert manifest['profile']=='all-routes-unified-v8013' and len(manifest['batches'])==636 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==15 and atomic['negative_count']==reg['negative_count']==202
    assert reg['expected_manifest_batches']==636 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['config_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(APPROVED.read_bytes()) and seal['all15_five_gates_andexact_references_approved']
    assert len(doc['records'])==15 and not doc.get('typed_choice_records') and all(all(r['review'].values()) for r in doc['records'])
    assert sum(bool(r['qa_waivers']) for r in doc['records'])==2
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR)
    before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
    assert tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping,actual=map(read,[APPROVED,MAP,proofs()['actual_proof']])
    image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    rows=[];keys={historical_key(r) for r in doc['records']}
    assert len(oldkeys)==6976 and len(keys)==15 and not oldkeys&keys and KEY not in old
    for original in doc['records']:
        row=deepcopy(original);group=mapping['groups'][0];block=bank[47]
        ref=next(r for r in group['text_records'] if r['id']==row['id']);at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index'] and sha(block)==group['target_block_sha256']
        observations=[dict(block=47,version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        observed=row['id'] not in UNVISITED
        assert bool(observations)==observed and row['actual_record_observed'] is observed
        if observed:assert {o['version'] for o in observations}=={'clean_Japanese','English'} and len(observations)==2 and all(o['speech']['complete_body_holds'] for o in observations)
        row.update(actual_source_andEnglish_observations=observations,
            integrated_reference=dict(file_path=row['file_path'],block=47,offset=at,record_index=ref['new_record_index'],
                bytes=len(raw),stored_hex=raw.hex(),block_sha256=sha(block),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            exact_stored_reference=deepcopy(ref),source_prose_andcompletion_credit_added_once=True,registered_integration_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=False)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':8,'retention':7}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [
        PRIOR,APPROVED,MAP,SEAL,RELEASE,START,START_VIEW,ATOMIC,REGISTRATION,*map(Path,proofs().values()),
        Path('work/analysis/Rafael_B47_atomic_positive_v8010/positive_receipt.json'),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=8,retained=7,source_prose_and_completion_credit_added_once=15,
        actual_unique_speeches_each_language=11,actual_speech_occurrences=22,actual_total_complete_page_occurrences=23,
        actual_unique_pages_both_languages=23,complete_body_andheader_holds=88,offline_only_object_IDs=UNVISITED,
        native_all15_paragraphs16_pages_andR53_only_two_pages=True,
        all_source_current_effective_compiled_stored_scoped_actual_andintegrated_refs_bound=True,
        all48_commands24_relatives15_preambles_six_predicates_zero_macros_andcomplete_ends_preserved=True,
        clean_predecessor_block_andwhole_archive_inverse_exact=True,
        three_actual_names_Janus_native_only_full207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy15_positives302_negatives_atomic15_positive202_negatives=True,
        original_QA_six_infos_two_exact_warning_exceptions_retained=True,
        own_ROM_new_startup_runs=1,own_ROM_new_startup_frames=read(START)['actual_frames'],
        all_prior_artifacts_full_scope_graphics_separation_andlater_audit_preserved=True,
        evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
        ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)))
        parent[key].extend(deepcopy(values))
    for key,value in zip(COUNTERS,AFTER,strict=True):put([key],value)
    file='/data/SC0.DK4'
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[key][file]==173;put([key,file],188)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[47],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=8,retained_count=7,fresh_revisions=8,fresh_retentions=7,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=6991,fresh_pass_records_integrated=6991,latest_contextual_manuscript=str(APPROVED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=15,final_review=str(FINAL),new_revisions=8,justified_retentions=7,new_completed_records=15,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=11,
        actual_pages=12,offline_only_objects=4,all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(APPROVED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5376
    for key,value in dict(reviewed_route_records=5391,completed_route_records=5391,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[47],completion_credit_added=15,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=11,actual_pages=12,offline_only_objects=4,full_goal_complete=False)])
    put(['formatting_watchlist','Rafael_SC0B47_v8018'],dict(status='15-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        final_review=str(FINAL),native_pages16_R53_only_two_pages=True,row_infos6_two_exact_warning_exceptions=True,
        all_measured_limits_andearlier_proofs_preserved=True,full207_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    pending=prior['pending_source_batch']
    put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
        all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=15,revisions=8,retentions=7,registered_candidate=release['candidate'],
        full207_names_full_goal_andall_late_limits_preserved=True)
    if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5391,completed_route_records=5391,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=15,new_completed_records=15,revised=8,retained=7,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V8018: Rafael B47 Mediterranean advice integrated in cumulative V8013; full review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8018; V8013 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all15_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:15 disjoint Rafael decisions/8 revisions/7 retentions.Deep inverse audit next.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly15_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly15_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;6991 completed/4369 revisions/2622 retentions,currentV8013.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(completed)==6991 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=6991,records_with_source_and_prose_pass=6994,records_with_source_prose_drafts=6994,
                records_revised_and_integrated=4369,retained_wordings_editorially_completed=2622,
                completed=6991,source_prose=6994,revised=4369,retained=2622,SC0=188,SC1=91,SC2=4915,SC3=197,
                reviewed_routes=5391,completed_routes=5391,manifest_batches=636,accepted_layers=114,release_checks=18,regressions=110,
                Rafael_B47_completed_once=True,Rafael_B47_policy_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_unique_pages_both_languages=23,
                actual_speech_occurrences=22,actual_complete_body_andheader_holds=88,native_only_object_IDs=UNVISITED,
                strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,
                full_goal_active=True,full_goal_complete=False,all_current_andearlier_limits_preserved=True,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8019/currentV8013:6991completed/6994source-prose/4369revisions/2622retentions;15credited once.Full objective active.')
