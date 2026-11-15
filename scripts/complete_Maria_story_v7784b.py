"""Credit67 disjoint integrated decisions once; reversibly preserve every previous ledger value."""
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
from scripts.Maria_story_final_paths_v7771 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_completion_v7784b')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7785b')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7774/verified_handoff.json')
RELEASE=Path('work/analysis/maria_story_release_v7780/registered_release_verification.json')
START=Path('work/analysis/maria_story_startup_verification_v7782/own_Maria_startup_exact_V7717_andstrict_current_input.json')
START_VIEW=Path('work/analysis/maria_story_startup_view_v7783/own_Maria_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/maria_story_atomic_challenges_v7776/atomic_validation_receipt.json')
FINAL=Path('translations/maria_B34_B108_B35_contextual_final_review_v1.json')
KEY='Maria_SC3B34_B108_B35_completion_v7784b'
FAMILY='Maria_SC3B34_B108_B35_contextual_linked_arc_v7784b'
SCOPE='unfinished_editorial_scope_v7784b'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6855,6858,6858,4290,2565)
AFTER=(6922,6925,6925,4338,2584)
INTRO="""The linked Maria story exchanges SC3 B34, B108 and B35 are integrated in registered cumulative V7779. All 67 positions were reviewed as complete exchanges from clean Japanese: 48 revisions and 19 individually justified retentions receive credit once. The exact clean, previous effective English, compiled, stored, actual and integrated references are in translations/maria_B34_B108_B35_contextual_final_review_v1.json.

The ledger now has 6,922 completed records, 6,925 source/prose records and drafts, 4,338 integrated revisions and 2,584 retentions. Completed file counts are SC0 135, SC1 91, SC2 4,915, SC3 181 and COMMON 1,600; COMMON still has three source/prose drafts. The route subset is 5,322/5,322 and does not represent the full goal denominator. V7779 retains all 630 batches and 114 accepted layers, passes 18 registered release checks and 110 regressions, equals the reviewed reference ROM, and reconstructs byte for byte from the clean-input xdelta patch. Main V4701 remains unchanged."""
DETAILS="""The final 67 English speeches each fit a complete native four-row page using the validated 216px geometry. All leading, internal and trailing characters, line guards, native font planes, bounds, consumption and pagination pass. There are 22 individually justified row-count infos, no warnings or waivers, 33 zero-ink storage parity spaces and 268 final logical, compiled and stored alignment cases. Scoped FI5/FA2/FO7 measurements preserve all 12 actual substitutions without altering the stale generic Maria profile.

All 116 original commands, 67 complete speaker/layout preambles, 20 nested/relative sites, mapped branch targets, resource/setup/wait/effect controls and complete four-byte ends are preserved. All three clean and previous blocks and the full previous archive invert exactly. Only SC3 B34/B35/B108 change; the other 300 blocks and all other files/components remain exact to V7717. The original native loaders pass 303 full loads/cache hits and 606 parent modes. Policy checks pass 67 positives and 200 actual-changing rejections. Atomic production passes one full-ROM positive and 256 actual-changing corruptions with dependency checks bypassed; every corruption rejects before any file commit.

The final source/English fixtures cover 65 distinct speeches in each language, 130 complete pages and 528 complete body/nameplate holds, with no incomplete sampled holds or unidentified traces. Two Julian-dependent B108 lines remain explicitly offline. Four unchanged actual groups were reused by exact hashes; only the two affected English scenes were recaptured after final prose refinement. All 65 paired upper scenes, portraits and nameplates match, as do command results and UI requests. All earlier drafts, successful two-page evidence, failures, traces and screenshots remain.

Retain every measured command/duration, RNG, actor/component/calendar and later RGB difference. Final exits are B34 6295/6295, B108 11336/11335 and B35 11335/11334; later RGB differences are 0/163, 60/79 and 60/79. This is targeted initialized gameplay, not natural optional activation, original scene location, earned unlock, full mechanics, complete routes or hardware coverage. The exact existing system-only unlock is disclosed and earned=false. A fresh own-V7779 Maria startup matches the previous whole-frame and actor/captain controls and supplies a strict own-ROM captain3 snapshot; unaffected route startup checks were retained without replay.

The broader name review remains active. Seven scene headers were observed; Julian is offline-only and the full catalogue UI was not visited. Approved Hodram/Joakim, Maria and Camille and source-supported Xien Yan, Julian Lopes, Richard Townsend and Port Worker remain. Actor155 still has the unresolved Sailor/Retainer discrepancy; no global name asset was changed. The four-route direct-speaker census covers 147 blocks, 484 uses and 3,150 context speeches. Nine complete clean exchanges/129 speeches and 18 getters were examined, not all 3,150 speeches. Sales, hostile-subordinate, player-aide and pirate contexts do not support a blanket nautical job label. Indirect, typed, COMMON and other UI consumers remain open.

Preserve the normal-end result-type/value-carry finding and source-only B35 R65 nineteenth-cell question mark for the later older-record technical re-audit. Neither finding changes the English 216px rules. Preserve every earlier completed family, open lead, ROM, translation, producer, failed check and proof. All four storylines, earlier translations, practical broad town/shop/random capture, Help, remaining player prose, all 207 names/roles/aliases and retrospective early wrapping remain in scope. Graphics and all 18 plaques remain separate. No separate test package, promotion, pruning, commit or push occurred."""
NEXT="""Continue the full editorial goal from current V7779 and verified handoff V7785b. Maria B34/B108/B35 is complete; do not repeat its unchanged source, native, actual, policy, inverse, loader, production, patch or startup checks. For further Maria native work use work/analysis/current_V7779_native_v7782/route3/current_native_input.json; do not substitute another route's RAM or claim an older capture is from V7779. Capture another route's own current context when it is needed.

Continue the contextual review across all four storylines and earlier translated conversations, and the broad practical town/shop/random/Help/player-prose and premature-wrap pass. Continue the 207-name review, including the unresolved actor151–159 Sailor/Retainer family using the full 147-block census and remaining indirect/typed/COMMON/UI consumers. The nine reviewed exchanges are a scoped sample, not approval of the full family. Retain all earlier unfinished inventories, shared role and item leads and counterpart conversations. Integrate reviewed batches after their necessary checks pass; preserve all prior artifacts. Keep graphics and the later older-record technical re-audit separate. Main V4701 remains; no canceled separate unified test package, automatic promotion, pruning, commit or push."""
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
    release,start,view,atomic,doc,seal=map(read,[RELEASE,START,START_VIEW,ATOMIC,SEALED,SEAL])
    rom=Path(release['candidate']);manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert sha(rom.read_bytes())==release['candidate_sha256']==manifest['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']
    assert manifest['profile']=='all-routes-unified-v7779' and len(manifest['batches'])==630 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_current_requested_andfinal_frames_equal_V7717'] and start['actual_original_captain_ID']==3 and start['strict2b6_COMMON_directory_andall123264_payload_bytes_verified']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==67 and atomic['negative_count']==256 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['all_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['all67_five_gates_andexact_references_approved']
    assert len(doc['records'])==67 and all(all(r['review'].values()) for r in doc['records'])
    return release
def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR)
    before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
    assert tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping,actual=map(read,[SEALED,MAP,ACTUAL]);image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    rows=[];keys={historical_key(r) for r in doc['records']};assert len(oldkeys)==6855 and len(keys)==67 and not oldkeys&keys
    for original in doc['records']:
        row=deepcopy(original);group=next(g for g in mapping['groups'] if g['block']==row['block']);ref=next(r for r in group['text_records'] if r['id']==row['id']);block=bank[row['block']]
        at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index'] and sha(block)==group['target_block_sha256']
        observations=[dict(block=g['block'],version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        assert len(observations)==(2 if row['actual_record_observed'] else 0)
        row.update(integrated_reference=dict(file_path=row['file_path'],block=row['block'],offset=at,record_index=ref['new_record_index'],
            bytes=len(raw),stored_hex=raw.hex(),block_sha256=sha(block),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            exact_stored_reference=deepcopy(ref),actual_source_andEnglish_observations=observations,
            source_prose_andcompletion_credit_added_once=True,registered_integration_pending=False)
        rows.append(row)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':48,'retain-wording':19}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    paths=[PRIOR,SEALED,MAP,SEAL,APPROVAL,RELEASE,START,START_VIEW,ATOMIC,*map(Path,proofs().values()),
        Path('work/analysis/maria_story_atomic_v7775c/positive_receipt.json'),Path('work/analysis/maria_story_registration_v7778/registration_receipt.json'),
        Path('work/analysis/maria_story_production_tools_v7775c/provenance.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=48,retained=19,source_prose_and_completion_credit_added_once=67,
        actual_speeches_each_language=65,actual_total_complete_pages=130,complete_body_andheader_holds=528,
        offline_only_object_IDs=['DK4_MES_B108_R0020','DK4_MES_B108_R0125'],all67_complete_native_single_pages=True,
        all_source_current_effective_compiled_stored_actual_andintegrated_refs_bound=True,
        all116_commands20_relative_sites67_preambles12_substitutions_andcomplete_ends_preserved=True,
        all_three_clean_predecessor_blocks_andwhole_archive_inverse_exact=True,
        names_shared155_semantics_andfull207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy_positive67_negative200_andatomic_positive67_negative256=True,
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
    file='/data/SC3.DK4'
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[key][file]==114;put([key,file],181)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[34,108,35],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=48,retained_count=19,fresh_revisions=48,fresh_retentions=19,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=6922,fresh_pass_records_integrated=6922,latest_contextual_manuscript=str(SEALED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=67,final_review=str(FINAL),new_revisions=48,justified_retentions=19,new_completed_records=67,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=65,actual_pages=65,offline_only_objects=2,
        all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(SEALED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5255
    for key,value in dict(reviewed_route_records=5322,completed_route_records=5322,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[34,108,35],completion_credit_added=67,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=65,actual_pages=65,offline_only_objects=2,full_goal_complete=False)])
    put(['formatting_watchlist','Maria_SC3B34_B108_B35_v7784b'],dict(status='67-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        final_review=str(FINAL),final67_single_pages=True,row_infos22_no_waivers=True,all_measured_limits_andold_two_page_proofs_preserved=True,
        shared155_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    for pending in ['Maria_SC3B34_B108_B35_contextual_pending_v7736b','Maria_SC3B34_B108_B35_sealed_pending_v7773']:
        put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
            all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior_scope=old['unfinished_editorial_scope_v7773'];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=67,revisions=48,retentions=19,registered_candidate=release['candidate'],
        shared155_names_full_goal_andall_late_limits_preserved=True)
    for pending in ['Maria_SC3B34_B108_B35_contextual_pending_v7736b','Maria_SC3B34_B108_B35_sealed_pending_v7773']:
        if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5322,completed_route_records=5322,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=67,new_completed_records=67,revised=48,retained=19,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V7784b: Maria linked arc integrated in cumulative V7779; full editorial review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7784b; V7779 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all67_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:67disjoint Maria decisions/48revisions/19retentions.Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest_value in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest_value
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly67_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly67_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;6922completed/4338revisions/2584retentions,currentV7779.Fullgoal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for family in new['completed_editorial_families'] for r in family['records']}
            assert len(completed)==6922 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=deepcopy(read(PRIOR));verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=6922,records_with_source_and_prose_pass=6925,records_revised_and_integrated=4338,retained_wordings_editorially_completed=2584,
                source_prose_drafts=6925,route_subset_completed=5322,SC3_completed=181,manifest_batches=630,accepted_layers=114,release_checks=18,regressions=110,
                Maria_story67_uncredited=False,Maria_story67_completed_once=True,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
                all_formatting_gates_false=False,planned_pages=67,focused_two_page_risk=None,actual_final_pages=130,actual_complete_body_andheader_holds=528,
                shared_actor155_Sailor_Retainer_conflict_open=True,strict_own_Maria_current_input=read(START)['strict_current_native_input'],
                next_required=NEXT,unfinished_scope=SCOPE,latest_completion=KEY,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,new_credit=67,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7784b/V7779:6922completed/6925source-prose/4338revisions/2584retentions;67creditedonce.Fullgoal/names/graphicsseparation/lateraudit preserved.')
