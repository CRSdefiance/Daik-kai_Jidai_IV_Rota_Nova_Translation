"""Credit16 disjoint integrated decisions once; reversibly preserve every previous ledger value."""
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
from scripts.Maria_B36_final_paths_v7816b import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B36_completion_v7826')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7827')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7817d/verified_handoff.json')
RELEASE=Path('work/analysis/maria_B36_release_v7822/registered_release_verification.json')
START=Path('work/analysis/maria_B36_startup_verification_v7824/own_Maria_startup_exact_V7779_andstrict_current_input.json')
START_VIEW=Path('work/analysis/maria_B36_startup_view_v7825/own_Maria_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/maria_B36_atomic_challenges_v7819/atomic_validation_receipt.json')
FINAL=Path('translations/maria_B36_contextual_final_review_v1.json')
KEY='Maria_SC3B36_completion_v7826'
FAMILY='Maria_SC3B36_contextual_confrontation_v7826'
SCOPE='unfinished_editorial_scope_v7826'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6922,6925,6925,4338,2584)
AFTER=(6938,6941,6941,4347,2591)
INTRO="Maria's confrontation with Lil, SC3 B36, is integrated in registered cumulative V7821. The complete clean Japanese exchange was reviewed before current English: 16 disjoint records receive credit once, with nine revisions and seven individually justified retentions. Exact clean, previous effective English, compiled, stored, actual and integrated references are in translations/maria_B36_contextual_final_review_v1.json.\n\nThe ledger now has 6,938 completed records, 6,941 source/prose records and drafts, 4,347 integrated revisions and 2,591 retentions. Completed file counts are SC0 135, SC1 91, SC2 4,915, SC3 197 and COMMON 1,600; COMMON retains three source/prose drafts. Route 5,338/5,338 is a subset, not the whole-goal denominator. V7821 preserves 631 batches and 114 accepted layers, passes 18 registered release checks and 110 regressions, equals the approved reference ROM and reconstructs byte for byte from its clean-input patch. Main V4701 remains unchanged."
DETAILS="All 16 English speeches fit complete original 216px/four-row single pages. Complete first, internal and final characters, independent font planes, bounds, canaries, guards, consumption and pagination pass. Final logical, compiled and stored checks each cover 64 alignments; 11 storage parity spaces add zero ink. Nine row-count infos have individual reasons, with no warnings or waivers. A scoped automatic soft-wrap preference keeps He's a great merchant! together without authored line breaks, prose changes or wider geometry.\n\nAll 16 six-byte preambles, original selectors, FI2/FO1 substitution order, 22 native commands, six numeric leaves and complete ends remain. There are no relative or in-block predicate commands. Resource and structural boundary tests are scoped evidence, not complete mechanics. Clean and previous B36 blocks and the entire previous archive invert exactly. Only B36 changes; all 302 other SC3 blocks and all other files/components remain exact to V7779. The original native loaders pass 303 full loads/cache hits and 606 parent modes. Policy passes 16 positives and 81 actual-changing rejections. Production passes one complete positive and 120 actual-changing corruptions, all rejected before any files-list commit with dependency checks bypassed.\n\nTwo initialized source/English gameplay fixtures each play all 16 speeches and 29 original fixture commands. Together they provide 32 complete pages and 132 complete body/nameplate holds, with no partial sampled holds, unidentified traces or unplayed lines. All 32 exact panes and nine sheets were viewed. All 16 paired upper scenes, portraits and nameplates agree, as do command results and UI requests. These are targeted headless emulator tests using ordinary inputs and the existing exact system-only unlock, earned=false; natural optional activation, original location, complete mechanics, full routes and hardware coverage remain unproved.\n\nPreserve exits 8213/8216, 18 command-comparison rows, six duration differences and 108/131 later RGB differences. State/tasks/calendar agree; models/persistent objects and whole actors differ. Final seeds are 164302531/4157282706. All raw timing, RNG, component, actor, calendar, following-command and RGB evidence remains, without broad simulation or causal-equivalence claims. Initialized Hangzhou return8300 and incidental later navigation/level-up text earn no source-prose credit.\n\nThe fresh own-V7821 Maria startup runs 4001 frames and matches all seven prior whole-frame pairs plus captain3 and whole-actor controls. Its strict own-ROM input is work/analysis/current_V7821_native_v7824/route3/current_native_input.json. Unaffected route startup evidence is retained without replay. All three selected B36 progressive nameplates were observed: Lil Argot, Maria Li and Xien Yan. Actor0A is Xien, not Camille09. No global name asset changes; full catalogue UI and the complete 207-name/role/alias review remain open.\n\nAll earlier drafts, translations, failed and corrected producers, ROMs and proofs remain. Preserve the source normal-end value-carry finding and B35 R65 source-only nineteenth-cell glyph for the later older-record technical re-audit. All four storylines, earlier dialogue, broad practical town/shop/random capture, Help, remaining prose and retrospective premature wrapping remain active. Graphics and all 18 plaques remain separate. The separate unified test package stays canceled; no promotion, pruning, commit or push occurs."
NEXT="Continue the full editorial objective from verified V7827 and current registered V7821. B36 is complete; retain its source/native/actual/policy/production/inverse/patch/startup proofs without unnecessary replay. Use the new own-V7821 captain3 context for further Maria native work; obtain another route's own current context when needed.\n\nContinue all four storylines and earlier translated exchanges, broad practical shared shop/town/random captures, Help and remaining player prose. Continue all 207 names/roles/aliases, including actor151-159 Sailor/Retainer and the remaining indirect, typed, COMMON and UI consumers. The 147-block/484-use/3150-context-speech census and nine-exchange/129-speech sample are evidence, not full approval. Check the original Japanese progressive-name consumer before inferring a global label from internal fields.\n\nRetain the retrospective contracted-predicate early-wrap lead and every earlier unfinished inventory, counterpart conversation, role/item/display lead and family. Compare exact current consumers and complete clean exchanges before revisions; heuristic candidates add no credit. Integrate reviewed batches once their necessary checks pass. Preserve all generated ROMs and earlier translations. Graphics/all18 plaques and the later older-record technical re-audit remain separate. Main V4701 remains unchanged; do not create the canceled separate unified test package, promote, prune, commit or push."
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
    assert manifest['profile']=='all-routes-unified-v7821' and len(manifest['batches'])==631 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_current_requested_andfinal_frames_equal_V7779'] and start['actual_original_captain_ID']==3 and start['strict2b6_COMMON_directory_andall123264_payload_bytes_verified']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==16 and atomic['negative_count']==120 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['all_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['all16_five_gates_andexact_references_approved']
    assert len(doc['records'])==16 and all(all(r['review'].values()) for r in doc['records'])
    return release
def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR)
    before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
    assert tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping,actual=map(read,[SEALED,MAP,ACTUAL]);image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    rows=[];keys={historical_key(r) for r in doc['records']};assert len(oldkeys)==6922 and len(keys)==16 and not oldkeys&keys
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
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':9,'retain-wording':7}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    paths=[PRIOR,SEALED,MAP,SEAL,APPROVAL,RELEASE,START,START_VIEW,ATOMIC,*map(Path,proofs().values()),
        Path('work/analysis/maria_B36_atomic_v7818b/positive_receipt.json'),Path('work/analysis/maria_B36_registration_v7820/registration_receipt.json'),
        Path('work/analysis/maria_B36_production_tools_v7818b/provenance.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=9,retained=7,source_prose_and_completion_credit_added_once=16,
        actual_speeches_each_language=16,actual_total_complete_pages=32,complete_body_andheader_holds=132,
        offline_only_object_IDs=[],all16_complete_native_single_pages=True,
        all_source_current_effective_compiled_stored_actual_andintegrated_refs_bound=True,
        all22_commands_no_relative_sites16_preambles3_substitutions_andcomplete_ends_preserved=True,
        clean_predecessor_block_andwhole_archive_inverse_exact=True,
        names_shared155_semantics_andfull207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy_positive16_negative81_andatomic_positive16_negative120=True,
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
        assert new[key][file]==181;put([key,file],197)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[36],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=9,retained_count=7,fresh_revisions=9,fresh_retentions=7,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=6938,fresh_pass_records_integrated=6938,latest_contextual_manuscript=str(SEALED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=16,final_review=str(FINAL),new_revisions=9,justified_retentions=7,new_completed_records=16,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=16,actual_pages=16,offline_only_objects=0,
        all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(SEALED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5322
    for key,value in dict(reviewed_route_records=5338,completed_route_records=5338,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[36],completion_credit_added=16,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=16,actual_pages=16,offline_only_objects=0,full_goal_complete=False)])
    put(['formatting_watchlist','Maria_SC3B36_v7826'],dict(status='16-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        final_review=str(FINAL),final16_single_pages=True,row_infos9_no_waivers=True,all_measured_limits_andearlier_proofs_preserved=True,
        shared155_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    for pending in ['Maria_SC3B36_sealed_pending_v7817c']:
        put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
            all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior_scope=old['unfinished_editorial_scope_v7817c'];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=16,revisions=9,retentions=7,registered_candidate=release['candidate'],
        shared155_names_full_goal_andall_late_limits_preserved=True)
    for pending in ['Maria_SC3B36_sealed_pending_v7817c']:
        if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5338,completed_route_records=5338,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=16,new_completed_records=16,revised=9,retained=7,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V7826: Maria confrontation integrated in cumulative V7821; full editorial review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7826; V7821 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:2d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:2d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all16_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:16disjoint Maria decisions/9revisions/7retentions.Deep inverse audit next.')
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
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly16_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly16_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;6938completed/4347revisions/2591retentions,currentV7821.Fullgoal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for family in new['completed_editorial_families'] for r in family['records']}
            assert len(completed)==6938 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=deepcopy(read(PRIOR));verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=6938,records_with_source_and_prose_pass=6941,records_revised_and_integrated=4347,retained_wordings_editorially_completed=2591,
                source_prose_drafts=6941,route_subset_completed=5338,SC3_completed=197,manifest_batches=631,accepted_layers=114,release_checks=18,regressions=110,
                Maria_B36_sealed_uncredited=False,Maria_B36_completed_once=True,
                completed=6938,source_prose=6941,revised=4347,retained=2591,SC3=197,reviewed_routes=5338,completed_routes=5338,
                Maria_B36_actual_pages=32,Maria_B36_complete_body_andheader_holds=132,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
                all_formatting_gates_false=False,planned_pages=16,focused_two_page_risk=None,actual_final_pages=32,actual_complete_body_andheader_holds=132,
                shared_actor155_Sailor_Retainer_conflict_open=True,strict_own_Maria_current_input=read(START)['strict_current_native_input'],
                next_required=NEXT,unfinished_scope=SCOPE,latest_completion=KEY,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,new_credit=16,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7826/V7821:6938completed/6941source-prose/4347revisions/2591retentions;16creditedonce.Fullgoal/names/graphicsseparation/lateraudit preserved.')
