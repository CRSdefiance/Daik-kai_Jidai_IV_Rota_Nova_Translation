"""Credit32 exact newly integrated reviews once and preserve the complete historical ledger."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.checkpoint_maria_B97_v5019 import WIDER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_completion_v5034')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5035')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/maria_B97_editorial_manuscript_v6.json')
FINAL=Path('translations/maria_B97_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/maria_B97_release_v5031/registered_release_verification.json')
START=Path('work/analysis/maria_B97_startup_v5033/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=Path('work/analysis/maria_B97_registration_v5029b/registration_receipt.json')
ACTUAL=Path('work/analysis/maria_B97_actual_approval_v5018/all32_native_actual_approval_and_remaining_release_gates.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5020/verified_handoff.json')
NEXT_SOURCE=Path('work/analysis/lil_B184_clean_context_v5038b/all9_clean_exchange_and_fresh_glosses.json')
FAMILY='Maria-B97-Sao-Jorge-bandits-revenge-political-alternative-invitation-and-tablet32'
KEY='Maria_B97_completion_v5034'
PARENT_KEY='previous_integrated_candidate_before_Maria_B97_completion_v5034'
PREVIOUS='previous_latest_checkpoint_before_Maria_B97_completion_v5034'
SCOPE='unfinished_editorial_scope_v5034'
WATCH='Maria_B97_v5034'
NEXT=('Continue Lil SC2B184 from nine fresh clean-only glosses5038b and full inventory5037 before comparing older English. '
    'Bind A4/A5 names,voices and complete native speaker/context behavior without assuming spouses,kinship or a rank. The exchange enjoys tea,wonders that it had not caught on,criticizes others\' taste,requests buying more tomorrow because household tea is low,agrees,describes calm and ends with personal hyperbole plus a separate prospective Sofala Tea notice. '
    'The low supply is household tea,not a town shortage or trading tip. Bind approved Tea/Sofala forms and keep the closing notice prospective;no earned boom,profit,medical effect or earlier scene location. '
    'Preserve all12 commands/nine complete preambles,A0008 raw00a0ffff011f22a1,C200426,end428 and432 stored bytes. Do not inherit B97\'s resource,item presentation,FO or two-page counts. These nine remain uncredited. '
    'Maria B97 is now integrated once in V5030;do not repeat its sealed source/native/actual/reference/release checks without a concrete risk. Preserve the original source72 A continuation and6px first-row guard,all40 commands/eight leaves and all disclosed fixture/state differences. '+WIDER)
DETAILS=('V5034 completes32 Maria SC3B97 whole-exchange reviews once in registered cumulative V5030:23 revisions and9 individually justified retentions. '
    'Restore the bandits\' loss of livelihood rather than invented starvation,the accusation that Maria talks as though she knows everything,the great powers\' use of Proofs as a pretext to partition the world,and Maria\'s at-least-equal confidence. '
    'Preserve village devastation,slave trading and military plunder,her challenge to indiscriminate attacks,the cycle of conflict,political aims,voluntary invitation,consideration,trust,welcome and tentative ruins/tablet handover. '
    'Keep character judgments as speech without invented historical absolution,casualties,kinship,rank,retaliatory act or completed Proof. Approved Maria Huamei Li/progressive Maria Li,Xien Yan,Bandit,Li Clan runtime FO,Sao Jorge and current Help\'s Proof of Conquest bind. Older exact Proof variants and the separate Japanese city alias remain open.\n\n'
    'All40 source commands,32 complete preambles,eight exact non-speech leaves,one FO,31 progressive objects and one impersonal FE remain.1904 stored/1902 logical becomes2048 stored/2046 logical,with two trailing alignment zeros. '
    'Setup6000/4620/resource633E stay at8/10/14;A0001750 maps1874,item4820_1884 maps2028,A0001888 maps2032,hide4700_1896 maps2040,end1898 maps2042. Exact inverse restores every predecessor byte and302 other SC3 blocks remain exact. '
    'All32 current-font matrices,256 initial plus128 final stored alignments (72 fresh/56 exact-byte reuses),24 source-consumer/42 formatter negatives,six name consumers,three entry censuses,two guarded halfword-aligned ends and32 relocated dispatches pass. '
    'Both current/reference images freshly pass303 loads/cache hits and606 parent modes. The hide comparison retains original R3 command cursor:stream+1896 maps exactly tostream+2040;descriptor,other registers,guards and all4MiB remain checked. '
    'The atomic compiler\'s wrong-reference-offset negative exposed missing metadata validation in v1. Frozen v2 adds exact new header/text/index and source/current extent checks;all56 meaningful negatives now reject before mutation. Preserve both diagnostics and executed predecessors.78 release/dialogue regressions and18 cumulative checks pass.\n\n'
    'Two prior disclosed Japanese/English B33 content cold boots31000 frames each execute all40 original B97 commands and32 speeches.33 complete actual pages and327 held planes/paired upper-portrait-name samples match,with no nontext difference. '
    'All six actual sheets and four full item/final screens were viewed. Source72 has five rows:original A15401 advances after four rows to the full final sentence with an original6px first-row guard indent. Fresh native continuation matches10 holds;first page matches11. No word,compiled byte,font,width,guard,code or authored break changed. '
    'The original tablet display/hide and normal end work;source/English item-display whole RGB agrees.34 timings differ;ends23222/23822 and later whole RGB,actor hashes and PRNG347786248/2289475870 differ and remain disclosed. '
    'This is source content in a B33 New Game fixture with the existing unearned system-unlock battery,not naturally selected event97,earned recruitment/tablet,full route or hardware proof. No causal PRNG,future-world or full-RAM equivalence claim. '
    'Two fresh V5030 New Game4001 and inherited ordinary-town17401 cold boots match V4987 across31 whole frames and five actor/captain controls;the original donor remains unchanged. Four batch-relevant cold boots total83402 frames;this goal turn adds only the two21402-frame startup runs.\n\n'
    'V5030 contains the full V4987 stack:567 manifest batches/114 accepted layers. Only SC3B97 changes from V4987;the original B33 opening,all other stories,messages,fonts,graphics,ARM9/ARM7,components and123040-byte staged pool remain exact. '
    'The cumulative ROM equals the one-block reference and exact clean-input patch reconstruction. Immutable canonical inputs,promoted main V4701 and every earlier ROM,translation,draft,producer,proof,failure and ledger history stay preserved. No promotion or pruning.\n\n'
    'Coverage becomes5998 completed contextual rereads,6001 source/prose,3803 integrated revisions/2195 retentions,SC24113/SC396 and routes4399/4399,with zero pending credited route drafts. These32 were approved but uncredited before this completion and are counted once. '
    'The full editorial goal remains active. Lil B184 has nine fresh clean-only glosses with zero credit;all remaining storylines/shared town-shop/random scenes/Help/player prose stay in scope.\n\n')

def gates():
    release,start,view,reg,actual=map(read,[RELEASE,START,VIEW,REG,ACTUAL])
    assert release['all567_manifest_batches_and114_accepted_layers_present'] and release['all18_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['reference_ROM_byte_exact']
    assert start['all_current_requested_and_final_framebuffers_equal_V4987'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==56 and reg['all_negatives_reject_before_mutation'] and actual['source_native_actual_records']==32 and actual['actual_panel_pages']==33 and actual['complete_actual_matching_holds']==327
    tests=read('work/analysis/maria_B97_release_tools_v5030/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['stdout']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(manifest['batches'])==567 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/maria_B97_retention_v5034/pin_receipt.json')['all_existing_ROMs_and_pins_preserved']
    nextsource=read(NEXT_SOURCE);assert len(nextsource['records'])==9 and nextsource['read_no_predecessor_English'] and nextsource['new_review_credit']==0
    return release

def restore(new):
    inverse=deepcopy(new);entry=inverse.pop(KEY);back=entry['inverse_preserved_values'];inverse['current_integrated_candidate']=inverse.pop(PARENT_KEY);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(SCOPE)
    assert inverse['completed_editorial_families'].pop()['id']==FAMILY;inverse.update(back['root_values'])
    fresh=inverse['contextual_story_natural_dialogue_pass_v1871']
    for key in ['record_keys','integrated_record_keys']:assert fresh[key][-32:]==entry['record_keys'];del fresh[key][-32:]
    assert fresh['record_IDs'][-32:]==entry['record_IDs'];del fresh['record_IDs'][-32:];assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values'])
    active=inverse['active_source_prose_drafts'];assert active['manuscripts'].pop()==str(DOC);assert active['route_record_subsets_pending'].pop(str(DOC))==[];active['note']=back['active_note']
    assert inverse['coverage_units'].pop()['id']==FAMILY;inverse['coverage_units'][back['route_unit_index']]=back['route_unit'];inverse['formatting_watchlist'].pop(WATCH)
    return inverse

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':23,'retain-wording':9} and old['Maria_B97_contextual_native_actual_v5019']['source_prose_or_completion_credit_added']==0
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC3.DK4')).blocks[97];refs={r['id']:r for r in mapping['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for row in rows:
            ref=refs[row['id']];at=ref['new_text_offset'];value=bytes.fromhex(ref['stored_text_hex']);assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','current_raw_storage_English','current_stored_English','current_effective_runtime_English','current_effective_macro_template_hex','current_effective_macro_template_English','current_effective_paragraph','registered_runtime_catalog_entry','source_prose_or_completion_credit_added']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row};body=value[1:];expanded=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan');newref=dict(block=97,offset=at,header_offset=at-5,bytes=len(value),record_index=block[:at].count(b'\0'))
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),record_index=newref['record_index'],current_record_index=newref['record_index'],current_English=body.decode('ascii'),current_stored_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),current_effective_runtime_English=expanded.decode('ascii'),current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=body.decode('ascii'),current_effective_paragraph=' '.join(expanded.decode('ascii').split()),registered_runtime_catalog_entry=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release')
            assert all(row['review'].values()) and row['source_meaning'] and row['localization_note']
        oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows};assert len(oldkeys)==5966 and len(keys)==32 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==5966 and not fresh['pending_record_keys']
        summary=DETAILS+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,RELEASE,START,VIEW,REG,ACTUAL,PRIOR,NEXT_SOURCE,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path('work/analysis/maria_B97_release_tools_v5030/regression_test_results.json'),Path('work/analysis/maria_B97_retention_v5034/pin_receipt.json'),Path(__file__)]}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=23,retained=9,source_prose_and_completion_credit_added_once=32,previous_Maria_B97_objects_uncredited=True,all32_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_unique_speeches=32,actual_panel_pages=33,actual_source97_natural_activation_not_claimed=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);rootnames=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file'];freshnames=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note'];routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
        back=dict(root_values={k:deepcopy(old[k]) for k in rootnames},fresh_values={k:deepcopy(fresh[k]) for k in freshnames},active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC3.DK4',blocks=[97],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=23,retained_count=9,fresh_revisions=23,fresh_retentions=9,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=5998,records_with_source_and_prose_pass=6001,records_with_source_prose_drafts=6001,records_revised_and_integrated=3803,retained_wordings_editorially_completed=2195)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC3.DK4']==64;new[key]['/data/SC3.DK4']=96
        keyrows=[dict(file_path='/data/SC3.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871'];note='5998 contextual rereads integrated;source/prose6001. Maria B97 counted once;all wider families and earlier premature wrapping remain open.'
        for k in ['record_keys','integrated_record_keys']:f[k].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=5998,fresh_pass_records_integrated=5998,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=32,final_review=str(FINAL),new_revisions=23,justified_retentions=9,new_completed_records=32,historical_reconciliation_only=False,actual_selected_source97_events=[],actual_B33_content_speeches=32,actual_panel_pages=33,new_current_candidate_emulator_runs=2,prior_explicit_content_fixture_runs=2,goal_turn_new_frames=21402))
        active=new['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'] and str(DOC) not in active['route_record_subsets_pending'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
        new['coverage_units'][routeindex].update(reviewed_route_records=4399,completed_route_records=4399,next=NEXT);new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC3.DK4',blocks=[97],completion_credit_added=32,final_review=str(FINAL),actual_source_event97_selected=False,goal_turn_new_emulator_runs=2,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all32-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),source72_original_A_continuation_and6px_guard_verified=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False);current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        new[PARENT_KEY]=old['current_integrated_candidate'];new['current_integrated_candidate']=current;new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=summary
        inventory=deepcopy(read(old['unfinished_editorial_scope_v4992']['path']));inventory['next_focus']=NEXT;inventory['Maria_B97_completed_v5034']=dict(final_review=str(FINAL),completed_objects=32,registered_candidate=release['candidate'],natural_event97_not_selected=True);inventory['next_Lil_B184_clean_only_v5038b']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=9,uncredited=True)
        for u in inventory['broader_coverage_units']:
            if u['id']=='all-route-scenes':u.update(reviewed_route_records=4399,completed_route_records=4399,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Maria_B97_previously_uncredited_objects_completed=32,Lil_B184_clean_only_uncredited_objects=9,incomplete_COMMON=3,incomplete_credited_route_drafts=0,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=32,new_completed_records=32,revised=23,retained=9,goal_turn_classification='progress',goal_turn_new_emulator_runs=2,goal_turn_new_frames=21402,batch_relevant_runs=4,batch_relevant_frames=83402,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys and new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5034:32 Maria B97 reviews integrated once in cumulative V5030\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5034\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=32,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six files staged;32 reviews counted once in the proposed ledger. Audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5998,6001,3803,2195)
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates();assert new['current_integrated_candidate']['sha256']==release['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,exactly32_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False));print('Six targets,all prior history and exactly32 disjoint new keys audited.')
        elif mode=='apply':
            assert not (ROOT/'native_application_receipt.json').exists();a=read(ROOT/'independent_preapplication_audit.json');assert a['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as f:f.write(Path(e['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False));print('Six audited completion files applied byte-exactly.')
        else:
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();final=read(FINAL);assert len(final['records'])==32
            oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};allkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']};assert len(oldkeys)==5966 and len(allkeys)==5998
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly32_new_disjoint_source_prose_and_completed_records=True,completed=5998,source_prose=6001,revised=3803,retained=2195,SC2=4113,SC3=96,reviewed_routes=4399,completed_routes=4399,all567_manifest_batches114_accepted18_checks_verified=True,actual_unique_Maria_speeches=32,actual_panel_pages=33,source72_two_pages_and_original6px_guard_verified=True,startup31_frames_and_five_actor_controls_match_V4987=True,source97_natural_eligibility_and_earned_inventory_not_claimed=True,postscene_RGB_actor_PRNG_differences_preserved=True,new_clean_only_Lil_B184_uncredited_objects=9,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())));print('V5030 integration verified;5998 completed/6001 source-prose. Lil B184 nine clean-only objects pending;full goal active.')
