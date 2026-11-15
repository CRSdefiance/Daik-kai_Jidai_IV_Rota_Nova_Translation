"""Credit26 disjoint integrated B46 speech/menu decisions;recover all prior ledger values exactly."""
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
from scripts.Rafael_B46_release_paths_v7958 import *
SEALED=APPROVED
ACTUAL=Path(proofs()['actual_proof'])
APPROVAL=Path(proofs()['actual_approval'])
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_completion_v7969')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7970')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7955/verified_handoff.json')
RELEASE=Path('work/analysis/Rafael_B46_release_v7965/registered_release_verification.json')
START=Path('work/analysis/Rafael_B46_context_binding_v7967/own_Rafael_startup_andstrict_captain0_context.json')
START_VIEW=Path('work/analysis/Rafael_B46_startup_view_v7968/own_Rafael_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/Rafael_B46_atomic_challenges_v7962/atomic_validation_receipt.json')
FINAL=Path('translations/rafael_B46_contextual_final_review_v1.json')
KEY='Rafael_SC0B46_completion_v7969'
FAMILY='Rafael_SC0B46_contextual_sea_actions_two_choices_v7969'
SCOPE='unfinished_editorial_scope_v7969'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6950,6953,6953,4354,2596)
AFTER=(6976,6979,6979,4361,2615)
INTRO="Rafael SC0 B46 is integrated in registered experimental cumulative V7964:24 speeches andtwo menu labels,seven wording revisions andnineteen individually justified retentions. Fresh clean Japanese,the complete B38 prerequisite exchange andcorrected native branch context preceded current English. Accepting Julio's offer enters the sea-action lesson,understanding check andthanks;declining enters his caution andRafael's acknowledgment. Both share Rafael's unfinished private thought. Preserve relief,unease,teaching andcaution without invented family,rank,alliance,guaranteed discovery orcompleted ambition. Y/L/R/A instructions,opposite mode orders,icons,city/fleet targets andland inside the gray search frame remain faithful. Exact source,current,compiled,stored,actual andintegrated references are in translations/rafael_B46_contextual_final_review_v1.json.\n\nThe ledger now has6976 completed records,6979 source/prose records anddrafts,4361 integrated wording revisions and2615 retentions. Completed counts:SC0 173,SC1 91,SC2 4915,SC3 197,COMMON1600;COMMON hasthree source/prose drafts. Route5376/5376 is only a subset. V7964 contains all635 manifest batches/114 accepted layers,passes18 release checks/110 regressions,equals the approved research reference ROM andreconstructs exactly from its clean-input xdelta patch. Two new manifest batches carry24 speeches andtwo choices exactly once. MainV4701,every earlier ROM andtranslation remain."
DETAILS="All24 complete native single pages,first/internal/final characters,bounds,consumption andpagination pass. Full216px usable text width is source-bound;the twelve FE panels retain distinct228px bitmap geometry with216px usable text. The four original actor00 records keep their complete six-byte preambles separate from the unchanged body-NUL guard. FI6/FA6/FO10 defaults remain measured,withzero source macros;none are added. All96 compiled alignments,44 fresh stored and52 exact reused alignments pass. Eleven compiler parity spaces addzero ink. All14 original row-count infos have individual reasons,no warnings orwaivers. The30-byte two-choice object retains labels/order andnative provider sizing66px rather than padding;both even header alignments pass.\n\nAll37 commands,24 six-byte preambles,five A000 commands,6300,61FF,four relative/nested spans andthe four-byte normal end remain. Twenty relocated native cases,343 native load/cache paths and686 initial parent modes pass. Both complete clean/predecessor blocks andthe whole predecessor archive invert exactly. OnlyB46 changes from1696stored/1694logical/tail2 to1528stored/1526logical/tail2;all342 otherSC0 blocks andevery other file/component remain exact. Frozen policy passes24 speech positives,two choice labels and300 actual-changing expected-guard rejections. Atomic production passes a whole-ROM positive withone final files-list commit and187 independent rejections before any commit,withconfig dependency digests deliberately bypassed. Preserve the first precommit V7960 failure:it compared the prior pending census flagFalse tosealedTrue;the source-locked V7961 successor explicitly validates this transition andequality ofevery other original relocation field.\n\nFour16001-frame targeted headless emulator runs play clean Japanese andEnglish,accepting anddeclining through ordinary inputs:64004 frames. Acceptance plays22 speeches/43 total commands,returns[0,0] at9295/9294;decline plays7/28,returns[0,1] at5695/5696. Each language's union coversall24 speeches andall37 original B46 commands. Original menu results are[2,0]/[2,1];other seeded values remain offline coverage. Across58 speech occurrences,214 complete body/name/FE holds match independent masks withzero eligible partials,unidentified orunfinished calls. All48 unique source/English panes andfour transition,menu andlater-comparison sheets were directly viewed:14sheets. These use the original ten-command B44 prelude andfull B46 exchange in initialized Lisbon opening fixtures,not natural B46 event activation,earned prerequisites,original location,full mechanics,full route orhardware verification. No RAM,seed,condition,result,role,roster,battery orcontroller retiming is forced.\n\nAll29 paired upper scenes,portraits andheaders,selected command results andUI requests match. Twelve read-only snapshots/24 visible menu-label samples confirmfull native glyphs/backgrounds andthe original256x36 backing/source84px,target66px views. Source accept4930 hasno visible highlight despite eventual selection0;English4930 still shows0. Preserve this real phase difference without inventing blink causality,excluding frames orclaiming cross-language phase equality.\n\nPreserve27 accept/six duration and12 decline/two duration comparison differences. Both startRNG848781860;the first phase difference is the menu:source232frames/77LCGadvances,English234/78. English is one LCG step ahead atboth B46 exits. Later actual samples differ:accept41/113RGB pairs,finalseeds1622437796/3229979821,English159steps behind;decline96/173,3730749937/3562773357,English316behind. State/tasks match;models,persistent objects andwhole actors differ onboth paths. Accept calendar differs(ticks810/816,raw zero-based dates[0,16,42]/[0,17,0]);decline calendar matches. Original wait/generator code equality supports consistency withtiming,nota complete causal trace,future random-outcome equality orfull simulation equivalence. Retain all measurements forlater technical re-audit.\n\nFresh own-V7964 ordinary Rafael NewGame runs4001 frames,withsix prior whole-RGB pairs andcaptain0/whole-actor controls matchingV7911. Strict current input:work/analysis/current_V7964_Rafael_native_v7967/current_native_input.json. Existing native/stored/actual scene proofs are reused byexact whole-reference equality without replay. Rafael Castor,Claudio Manaus andJulio Erneco remain supported byclean fields/original getters andactual nameplates. Hayreddin hasonly scoped component retention;full catalogue UI,custom names andall207 names/roles/aliases remain open. Incidental B127/Sailor captures remain leads without editorial credit. All translations,drafts,executed/failing producers,proofs andROMs remain;graphics/all18 plaques andthe later older-record technical re-audit stay separate. No separate unified package,promotion,pruning,commit orpush."
NEXT="Continue the full editorial objective from verifiedV7970/current registeredV7964. B46's24speeches/two choices are complete;reuse source/context/names/native/stored/actual/policy/atomic/release/patch/startup proofs unless a new change orconcrete unresolved risk warrants more tests. Use own-current Rafael input atwork/analysis/current_V7964_Rafael_native_v7967/current_native_input.json. Lil's ownV7857 andMaria's ownV7821 contexts remain historical until properly rebound orrecaptured.\n\nSelect the next untouched clean complete exchange withits exact EV/caller/conditional context before reading current English;numeric block order doesnot establish chronology oractivation. Incidental B127/Sailor captures are previously exposed leads,not evidence ofunread current English. Keep allfour storylines,earlier translations,broad practical shared shop/town/random capture,Help/remaining prose,all207 names/roles/aliases andretrospective premature wrapping in scope. Retain allprior unfinished inventories,twelve remaining contraction/question-tag wrap leads andthe unscanned records beyond558 recorded plans,Sailor151-159 progressive versusRetainer indirect/fullname/typed/COMMON/UI consumers,andallolder item/counterpart/display leads including750-752,preLF6435,JanusPasha,Trader/PortWorker/Guildmaster,AlShin/AlFeridShin,ArmadilloHide,HerophilusMedicine,イギリス andAksumGoldSeal.\n\nThe full goal remains active. Preserve every generated ROM andearlier translation. Keep graphics/all18 plaques andthe later older-record technical re-audit separate,including normal-end value carry,B35R65's source-only nineteenth cell andallactual timing/highlight/RNG/component/calendar/RGB differences. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush."

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
    assert manifest['profile']=='all-routes-unified-v7964' and len(manifest['batches'])==635 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==26 and atomic['negative_count']==187 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['config_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['all26_five_gates_andexact_references_approved']
    assert len(doc['records'])==24 and len(doc['typed_choice_records'])==2 and all(all(r['review'].values()) for r in doc['records']+doc['typed_choice_records'])
    assert read(MENU)['records']==doc['typed_choice_records'] and seal['choice_manuscript_sha256']==sha(MENU.read_bytes())
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR)
    before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
    assert tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping,actual=map(read,[SEALED,MAP,ACTUAL]);image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    rows=[];objects=doc['records']+doc['typed_choice_records'];keys={historical_key(r) for r in objects}
    assert len(oldkeys)==6950 and len(keys)==26 and not oldkeys&keys
    menu_actual=read(proofs()['actual_menu_proof'])
    for original in objects:
        row=deepcopy(original);group=mapping['groups'][0];block=bank[46]
        refs=group['choice_commands'][0]['label_references'] if row['kind']=='typed-choice' else group['text_records']
        ref=next(r for r in refs if r['id']==row['id']);at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index'] and sha(block)==group['target_block_sha256']
        if row['kind']=='typed-choice':
            observations=[dict(version=g['version'],choice=g['choice'],sample=s,label=l) for g in menu_actual['groups'] for s in g['samples'] for l in s['labels'] if l['option_index']==row['option_index']]
            assert len(observations)==12 and all(o['label']['full_visible_black_glyph_mask_andblank_guards_equal'] for o in observations)
            row['actual_source_andEnglish_menu_observations']=observations
        else:
            observations=[dict(block=46,version=g['version'],choice=g['choice'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
            assert {o['version'] for o in observations}=={'clean_Japanese','English'} and len(observations) in [2,4]
            assert all(o['speech']['complete_body_holds'] for o in observations)
            row['actual_source_andEnglish_observations']=observations
        row.update(integrated_reference=dict(file_path=row['file_path'],block=46,offset=at,record_index=ref['new_record_index'],
            bytes=len(raw),stored_hex=raw.hex(),block_sha256=sha(block),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            exact_stored_reference=deepcopy(ref),source_prose_andcompletion_credit_added_once=True,registered_integration_pending=False)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':7,'retention':19}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    paths=[PRIOR,SEALED,MENU,MAP,SEAL,APPROVAL,RELEASE,START,START_VIEW,ATOMIC,*map(Path,proofs().values()),
        Path('work/analysis/Rafael_B46_atomic_positive_v7961/positive_receipt.json'),Path('work/analysis/Rafael_B46_registration_v7963/registration_receipt.json'),
        Path('work/analysis/Rafael_B46_sealed_guard_v7961/source_locked_successors.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=7,retained=19,source_prose_and_completion_credit_added_once=26,
        actual_unique_speeches_each_language=24,actual_total_complete_page_occurrences=58,actual_unique_pages_both_languages=48,complete_body_andheader_holds=214,actual_choice_labels=2,
        offline_only_object_IDs=[],all24_complete_native_single_pages=True,
        all_source_current_effective_compiled_stored_actual_andintegrated_refs_bound=True,
        all37_commands_four_relative_sites24_preambles_two_choices_zero_macros_andcomplete_ends_preserved=True,
        clean_predecessor_block_andwhole_archive_inverse_exact=True,
        names_Rafael_Claudio_Julio_FE_andfull207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy24_speeches_two_choices_negative300_andatomic26_negative187=True,
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
        assert new[key][file]==147;put([key,file],173)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[46],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=7,retained_count=19,fresh_revisions=7,fresh_retentions=19,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=6976,fresh_pass_records_integrated=6976,latest_contextual_manuscript=str(SEALED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=26,final_review=str(FINAL),new_revisions=7,justified_retentions=19,new_completed_records=26,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=24,actual_pages=24,actual_menu_labels=2,offline_only_objects=0,
        all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(SEALED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5350
    for key,value in dict(reviewed_route_records=5376,completed_route_records=5376,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[46],completion_credit_added=26,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=26,actual_pages=24,offline_only_objects=0,full_goal_complete=False)])
    put(['formatting_watchlist','Rafael_SC0B46_v7969'],dict(status='26-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        final_review=str(FINAL),final24_single_pages=True,two_native_choices=True,row_infos14_no_waivers=True,all_measured_limits_andearlier_proofs_preserved=True,
        full207_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    for pending in ['Rafael_SC0B46_actual_approved_pending_production_v7954']:
        put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
            all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior_scope=old['unfinished_editorial_scope_v7954'];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=26,revisions=7,retentions=19,registered_candidate=release['candidate'],
        full207_names_full_goal_andall_late_limits_preserved=True)
    for pending in ['Rafael_SC0B46_actual_approved_pending_production_v7954']:
        if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5376,completed_route_records=5376,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=26,new_completed_records=26,revised=7,retained=19,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V7969: Rafael sea-actions dialogue andtwo choices integrated in cumulative V7964;full review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7969; V7964 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:2d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:2d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all26_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:26 disjoint Rafael speech/menu decisions/7 revisions/19 retentions. Deep inverse audit next.')
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
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly26_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly26_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;6976 completed/4361 revisions/2615 retentions,currentV7964. Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for family in new['completed_editorial_families'] for r in family['records']}
            assert len(completed)==6976 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=6976,records_with_source_and_prose_pass=6979,records_with_source_prose_drafts=6979,
                records_revised_and_integrated=4361,retained_wordings_editorially_completed=2615,
                completed=6976,source_prose=6979,revised=4361,retained=2615,SC0=173,SC1=91,SC2=4915,SC3=197,
                reviewed_routes=5376,completed_routes=5376,manifest_batches=635,accepted_layers=114,release_checks=18,regressions=110,
                Rafael_B46_completed_once=True,Rafael_B46_policy_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_unique_pages_both_languages=48,
                actual_speech_occurrences=58,actual_complete_body_andheader_holds=214,actual_menu_label_samples=24,
                strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,latest_completion=KEY,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                new_credit=26,new_emulator_runs=1,new_actual_frames=4001,main_V4701_preserved=True,all_sessions_terminal_andreaped=True,
                all_highlight_timing_RNG_simulation_calendar_RGB_andactual_scope_limits_retained=True,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('Verified V7970/current V7964:6976 completed/6979 source-prose/4361 revisions/2615 retentions;26 credited once.Full objective active.')
