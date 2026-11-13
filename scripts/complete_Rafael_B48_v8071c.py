"""Credit fifteen disjoint integrated B48 decisions after release/startup; recover prior ledger exactly."""
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
from scripts.Rafael_B48_release_paths_v8060 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_completion_v8071')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8072')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8045/verified_handoff.json')
RELEASE=Path('work/analysis/Rafael_B48_release_v8067/registered_release_verification.json')
START=Path('work/analysis/Rafael_B48_context_binding_v8069/own_Rafael_startup_andstrict_captain0_context.json')
START_VIEW=Path('work/analysis/Rafael_B48_startup_view_v8070/own_Rafael_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/Rafael_B48_atomic_challenges_v8064/atomic_validation_receipt.json')
REGISTRATION=Path('work/analysis/Rafael_B48_registration_v8065/registration_receipt.json')
FINAL=Path('translations/rafael_B48_contextual_final_review_v1.json')
KEY='Rafael_SC0B48_completion_v8071'
FAMILY='Rafael_SC0B48_contextual_Athens_naturalist_Proof_exchange_v8071'
SCOPE='unfinished_editorial_scope_v8071'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6991,6994,6994,4369,2622)
AFTER=(7082,7085,7085,4411,2671)
UNVISITED=['DK4_MES_B48_R0017', 'DK4_MES_B48_R0032', 'DK4_MES_B48_R0049', 'DK4_MES_B48_R0081', 'DK4_MES_B48_R0086', 'DK4_MES_B48_R0232', 'DK4_MES_B48_R0236', 'DK4_MES_B48_R0239', 'DK4_MES_B48_R0273', 'DK4_MES_B48_R0385', 'DK4_MES_B48_R0389', 'DK4_MES_B48_R0393', 'DK4_MES_B48_R0396']
INTRO='Rafael B48 is complete in registered experimental cumulative V8066: 91 speeches, 42 revisions and 49 individually justified retentions credited once. Totals are 7,082 completed, 7,085 source/prose records and drafts, 4,411 integrated revisions and 2,671 retentions. SC0 has 279 completed records; the route subset has 5,482. All 637 manifest batches, 114 accepted layers, 18 release checks, 110 regressions, whole-reference equality and exact clean-input patch reconstruction pass. Main V4701 is unchanged. The full editorial goal remains active.'
DETAILS="The complete clean Japanese exchange, nine clean identities, B128's sailing-errand callback context and previously read B37 context preceded current English. Exact references, findings, 42 revisions and 49 individual retention reasons are in translations/rafael_B48_contextual_final_review_v1.json. The review preserves Athens banter, Julio's errand, refused free passage, Hans's natural-history passion, Claudio's reversal, assistant Arcadius's introduction, Julio and Hans's acquaintance, seven regional treasures, the ancient Seven Sages and maps, reported destiny, Rafael's ambition, the optional Hayreddin challenge and the uncertain recent southern African rumor. The four system panels preserve Hans Letzel's complete joining name, the navigator/Deck restriction, item information and the X instruction. R38 remains unnamed second person. No kinship, rank, romance, concealed identity, biography or guaranteed location is invented. R370 retains effective catalogue-selected English and its original FI substitution.\n\nAll 91 native paragraphs produce 92 complete pages. Final compiled evidence has four fresh R140 alignments and 360 exact reused cases. Stored evidence has 192 fresh parity-tail alignments for 48 records and 172 reused cases for 43. Source selector 00 occurs in 28 objects with 27 unique bodies. Complete preambles and selectors 00/04/05/06/07/08/0D/4B/71/FE remain. English uses the validated 216-pixel width and four physical rows per page; fonts, global profile and body NUL guard are unchanged. Exact private macro lengths are FI6/FA6/FO10. Four FE consumers retain 216 usable pixels inside their original 228x48 logical and 228x64 physical paper. R171 retains its source CP932 ellipsis. All 163 commands, 28 relative sites, five raw predicates, two completion queries, three A000 effects, scene controls and full end survive. All 140 relocated relative cases, 25 seeded value-carry ends, 343 load/cache paths, 686 parent modes and shipped callers pass. The 500 source-result compositions cover 32 text paths. Complete clean/predecessor block and archive inverses are exact; the other 342 blocks and all other files/components match V8013.\n\nTwo disclosed B44-entry fixtures preserve the entire B48 exchange after the original ten-command initialization. Ordinary-input cold boots run 80,002 frames total. Actual coverage is 78 speeches per language, 156 speech occurrences, 157 page observations and 486 complete body holds, including all four FE panels and six progressive headers. Thirteen conditional speeches and the Janus/Cesare/Cristina headers remain native-only. All 31 final actual sheets were directly viewed; the earlier focus sheet with its corrected caption is preserved. R347 uses five fuller rows over two pages. Ordinary A18400 turns between frames 18370 and 18430 within the same command; R350 follows. Page two starts with complete sealed at [6,0] and ends with shapes. Japanese R129's question mark is complete in the nineteenth 12-pixel cell at [216,16]; an isolated native 228-pixel source glyph span matches black and CP932-shadow masks. English rules remain unchanged. Keep this finding and B35 R65 for the later technical re-audit. These fixtures do not establish natural Athens activation, earned prerequisites, original location, full-route or hardware coverage. Full catalogue UI, custom names and the wider 207-name review remain open.\n\nAll 146 selected initialization/exchange results and UI requests match, as do all 78 upper-scene/portrait/header pairs. Normal [0,0] returns occur at frames 22735 and 22973, a 238-frame English delay. Preserve 129 comparison rows and 34 duration differences. The first RNG phase difference occurs at source offset 832: 173 versus 177 frames. R347 takes 241 versus 481 frames and advances 58 additional generator steps, from English phase 4 to 62. Exit phase is +63; final phase is -393, with final seeds 1328542105/448695880. All 285 later RGB samples differ. State, models, tasks and calendar match; persistent objects and whole actors differ. Both raw calendars are ticks 0/[0,0,0], without an invented date interpretation. Continued inputs re-enter the fixture at 35462/35702 and end during that later visit; distinguish this from the complete first exchange. No input retiming, state/seed/result forcing, every-call causal trace, future-state or full-simulation equivalence is claimed. Incidental B127, Sailor and resource prose earns no new credit.\n\nWrapping keeps R140's aren't you? together and avoids four short R347 rows solely to end a page at a sentence boundary. All 37 row-count infos and two exact weak-ending warnings remain: R86 line 1 the/Proof and R406 line 2 of/Conquest. Each exception binds the ID, source, logical English, compiled bytes, line, original issue and reason. No diagnostic is removed or global weak rule relaxed. Frozen policy passes 91 positives and 1,454 actual-changing guard rejections. The whole-ROM atomic positive commits one files list after all checks. All 455 independent proof corruptions reject before commit with configuration digests bypassed. The trusted frozen contract is read once and revalidated after the negative cases; semantic checks and commit traps remain active. Registration accurately records 455 negatives, 637 batches and one new 91-object manifest.\n\nFresh ordinary startup of registered V8066 runs 4,001 frames. Six whole-RGB pairs, captain 0 and whole-actor controls match V8013; strict 2b6/COMMON/directory/123264-payload guards pass. The startup sheet is directly viewed. Own-current input is work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json. Reuse earlier verified checks through exact reference equality. Preserve all prior ROMs, translations, drafts, failures, executed producers and proofs. Graphics, all 18 plaques and the later older-record technical re-audit remain separate. No separate unified package, promotion, pruning, commit or push."
NEXT="B49 source-only progress is already saved: 61 complete first clean glosses and seven original identities for Lil and Camille's North Sea confrontation. Current English bodies and name fields remain unread. Event49 requires39 and excludes151; review full event39 context and prove native entry, the apparent 0xC281 control, predicates/queries, branch alternatives R238/R244, callers and names before comparison or a localized manuscript. Do not infer chronology from block order or turn the proposed 協定 into a formal alliance without mechanic/context evidence. Source packet: work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json. Clean identities: work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json. Fresh glosses: work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json. These source-only artifacts bind the verified V8045 ledger while B48 tests ran; the clean ROM remains exact. B49 has no completion or source/prose credit. Continue from these files without redoing first-source work.\n\nContinue the full editorial goal from verified V8072/current registered V8066. B48's 91 speeches are complete and credited once. Reuse its verified source, context, nine names, 32 paths, native/stored display, representative actual, policy, atomic, release, patch and startup checks without needless replay. Use work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json. Other-route contexts remain historical until rebound or recaptured.\n\nSelect the next untouched complete clean exchange using exact EV/caller/conditional/prerequisite context before current English. Block order alone does not prove chronology. B128/B37 context and incidental B127/Sailor/resource captures are previously exposed leads. Preserve the objective across all four storylines, earlier translated dialogue, shared shops/towns, random scenes, Help, remaining prose, all 207 names/roles/aliases and retrospective premature wrapping. Keep every prior unfinished inventory, twelve contraction/question-tag leads, unscanned records beyond 558 plans, and the inherited weak-before-row and page-boundary-before-readability leads. Do not mechanically minimize rows or reverse justified phrasing.\n\nKeep Pasar distinct from Pasha; retain the historical counterpart queues without global replacement. Preserve every recorded item, counterpart and display lead, including Cristina/Christina, Hans Retzel/Letzel consistency, Trader/Port Worker/Guildmaster, Sailor151-159 versus Retainer consumers, COMMON750-752, preLF6435, Armadillo Hide/Steel Hide, Herophilus Medicine, Aksum Gold Seal, Al Shin/Al Ferid Shin and イギリス. Graphics/all 18 plaques and the later technical re-audit stay separate, including normal-end value carry, source-only B35 R65/B48 R129 nineteenth cells and all measured timing/highlight/RNG/component/calendar/RGB/fixture-reentry limits. Preserve every artifact. Main V4701 stays unchanged. The full goal is active; no separate unified package, promotion, pruning, commit or push."

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
    assert manifest['profile']=='all-routes-unified-v8066' and len(manifest['batches'])==637 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==91 and atomic['negative_count']==reg['negative_count']==455
    assert reg['expected_manifest_batches']==637 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['config_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(APPROVED.read_bytes()) and seal['all91_five_gates_andexact_references_approved']
    assert len(doc['records'])==91 and not doc.get('typed_choice_records') and all(all(r['review'].values()) for r in doc['records'])
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
    assert len(oldkeys)==6991 and len(keys)==91 and not oldkeys&keys and KEY not in old
    for original in doc['records']:
        row=deepcopy(original);group=mapping['groups'][0];block=bank[48]
        ref=next(r for r in group['text_records'] if r['id']==row['id']);at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index'] and sha(block)==group['target_block_sha256']
        observations=[dict(block=48,version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        observed=row['id'] not in UNVISITED
        assert bool(observations)==observed and row['actual_record_observed'] is observed
        if observed:assert {o['version'] for o in observations}=={'clean_Japanese','English'} and len(observations)==2 and all(o['speech']['complete_body_holds'] for o in observations)
        row.update(actual_source_andEnglish_observations=observations,
            integrated_reference=dict(file_path=row['file_path'],block=48,offset=at,record_index=ref['new_record_index'],
                bytes=len(raw),stored_hex=raw.hex(),block_sha256=sha(block),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            exact_stored_reference=deepcopy(ref),source_prose_andcompletion_credit_added_once=True,registered_integration_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=False)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':42,'retention':49}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [
        PRIOR,APPROVED,MAP,SEAL,RELEASE,START,START_VIEW,ATOMIC,REGISTRATION,*map(Path,proofs().values()),
        Path('work/analysis/Rafael_B48_atomic_positive_v8063/positive_receipt.json'),Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json'),Path('work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json'),Path('work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json'),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=42,retained=49,source_prose_and_completion_credit_added_once=91,
        actual_unique_speeches_each_language=78,actual_speech_occurrences=156,actual_total_complete_page_occurrences=157,
        actual_unique_pages_both_languages=157,complete_body_andheader_holds=486,offline_only_object_IDs=UNVISITED,
        native_all91_paragraphs92_pages_fourFE_andR347_only_two_pages=True,
        all_source_current_effective_compiled_stored_scoped_actual_andintegrated_refs_bound=True,
        all163_commands28_relatives91_preambles_five_predicates_two_queries_oneFI_fourFE_andcomplete_ends_preserved=True,
        clean_predecessor_block_andwhole_archive_inverse_exact=True,
        six_actual_names_three_native_only_full207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy91_positives1454_negatives_atomic91_positive455_negatives=True,
        original_QA_37_infos_two_exact_warning_exceptions_retained=True,
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
        assert new[key][file]==188;put([key,file],279)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[48],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=42,retained_count=49,fresh_revisions=42,fresh_retentions=49,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=7082,fresh_pass_records_integrated=7082,latest_contextual_manuscript=str(APPROVED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=91,final_review=str(FINAL),new_revisions=42,justified_retentions=49,new_completed_records=91,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=78,
        actual_pages=79,offline_only_objects=13,all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(APPROVED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5391
    for key,value in dict(reviewed_route_records=5482,completed_route_records=5482,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[48],completion_credit_added=91,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=78,actual_pages=79,offline_only_objects=13,full_goal_complete=False)])
    put(['formatting_watchlist','Rafael_SC0B48_v8071'],dict(status='91-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        final_review=str(FINAL),native_pages92_R347_only_two_pages_fourFE=True,row_infos37_two_exact_warning_exceptions=True,
        all_measured_limits_andearlier_proofs_preserved=True,full207_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    pending=prior['pending_source_batch']
    put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
        all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    put(['Rafael_SC0B49_source_gloss_pending_controls_current_andrelease_v8071'],dict(source_packet='work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json',clean_names='work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json',fresh_gloss='work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json',physical_source_objects=61,clean_static_identities=7,current_English_bodies_andnames_unread=True,source_gloss_only_no_localized_manuscript=True,native_controls_event39_context_paths_names_current_comparison_andrelease_pending=True,completion_credit_added=0,source_prose_credit_added=0,full_goal_complete=False))
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory['Rafael_SC0B49_source_gloss_pending_controls_current_andrelease_v8071']=dict(source_packet='work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json',clean_names='work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json',fresh_gloss='work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json',physical_source_objects=61,clean_static_identities=7,current_English_bodies_andnames_unread=True,source_gloss_only_no_localized_manuscript=True,native_controls_event39_context_paths_names_current_comparison_andrelease_pending=True,completion_credit_added=0,source_prose_credit_added=0,full_goal_complete=False)
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=91,revisions=42,retentions=49,registered_candidate=release['candidate'],
        full207_names_full_goal_andall_late_limits_preserved=True)
    if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5482,completed_route_records=5482,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=91,new_completed_records=91,revised=42,retained=49,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V8071: Rafael B48 Athens naturalist exchange integrated in cumulative V8066; full review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8071; V8066 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all91_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:91 disjoint Rafael decisions/42 revisions/49 retentions.Deep inverse audit next.')

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
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly91_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly91_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;7082 completed/4411 revisions/2671 retentions,currentV8066.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(completed)==7082 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=7082,records_with_source_and_prose_pass=7085,records_with_source_prose_drafts=7085,
                records_revised_and_integrated=4411,retained_wordings_editorially_completed=2671,
                completed=7082,source_prose=7085,revised=4411,retained=2671,SC0=279,SC1=91,SC2=4915,SC3=197,
                reviewed_routes=5482,completed_routes=5482,manifest_batches=637,accepted_layers=114,release_checks=18,regressions=110,
                Rafael_B48_completed_once=True,Rafael_B48_policy_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_unique_pages_both_languages=157,
                actual_speech_occurrences=156,actual_complete_body_andheader_holds=486,native_only_object_IDs=UNVISITED,
                strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch='Rafael_SC0B49_source_gloss_pending_controls_current_andrelease_v8071',
                full_goal_active=True,full_goal_complete=False,all_current_andearlier_limits_preserved=True,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8072/currentV8066:7082completed/7085source-prose/4411revisions/2671retentions;91credited once.Full objective active.')
