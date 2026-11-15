"""Credit nine newly integrated reviews once;preserve the complete ledger history."""
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

ROOT=Path('work/analysis/lil_B185_completion_v5127')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5128')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B185_editorial_manuscript_v5.json')
FINAL=Path('translations/lil_B185_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B185_release_v5123/registered_release_verification.json')
START=Path('work/analysis/lil_B185_startup_v5125b/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=Path('work/analysis/lil_B185_registration_v5121/registration_receipt.json')
ACTUAL=Path('work/analysis/lil_B185_actual_v5116/actual_all8_progressive_FE_A000_C200_and_single_end.json')
TRANSITIONS=Path('work/analysis/lil_B185_actual_review_v5117b/all2_actual_sheets8_planes_fullscreens_return_and_final_state.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5082/verified_handoff.json')
NEXT_SOURCE=Path('work/analysis/lil_B186_clean_context_v5131/all12_clean_exchange_and_fresh_glosses.json')
FAMILY='Lil-B185-cold-fur-coat-reported-sales-rising-prices-and-prospective-Stockholm8'
KEY='Lil_B185_completion_v5127'
PARENT_KEY='previous_integrated_candidate_before_Lil_B185_completion_v5127'
PREVIOUS='previous_latest_checkpoint_before_Lil_B185_completion_v5127'
SCOPE='unfinished_editorial_scope_v5127'
WATCH='Lil_B185_v5127'
NEXT=('Continue Lil SC2B186 from full clean-only inventory5130 and12 fresh glosses5131 before predecessor English. '
    'Read the sweetness discussion,customer/guest satisfaction claim,comic English-loan sweet emphasis,hesitant replies,self-authority assertion,practical question,job retort,two perfunctory acknowledgments,confident fashion prediction and stylized laugh as one exchange. '
    'Preserve food/flavor preparation context;do not turn it into a trading tip or invent a dish,ingredient or recipe. Bind AE174/AF175 names,voices and approved sweet-goods/Alexandria labels before choosing profession,rank or customer versus guest wording. '
    'Do not guess Sugar,marriage,kinship,ownership or nobility from polished speech and laughter. Character certainty stays confident character speech;the final FE notice stays tentative. '
    'Preserve all24 source commands and12 speeches. This block has one raw700 RNG predicate540,six relative commands,three alternative A000s560/572/584,C200644,end646 and652 stored/650 logical bytes with2 trailing zeros. '
    'Bind its own conditional paths;do not inherit B185 linear/no-predicate/no-tail assumptions or require every conditional line to be visited naturally. '
    'B185 is integrated once in V5122;do not repeat sealed source/native/reference/actual/release/startup checks without a concrete risk. Preserve its exact R16 ordinary boundary,all11 commands and disclosed8 timing/7 later indicator/unequal PRNG differences. '
    'Preserve stopped5117 analysis and unexecuted5125 verifier drafts,corrected successors and the native-number derivation guard. Original actor getter remains0xCB184;batch-label changes must never alter native constants. '
    'Main V4701 remains promoted;all earlier ROMs and translations stay preserved. No promotion or pruning. '+WIDER)
DETAILS=('V5127 completes eight Lil SC2B185 whole-exchange reviews once in registered cumulative V5122:4 revisions and4 individually justified retentions. '
    'Restore the fur-coat wish and freezing hyperbole,both reported fur sales and rising prices,and the later cold-weather concession. Retain the natural cold/Brr reactions,casual recollection,hearsay acknowledgment and wish for warmth with individual reasons. '
    'The clean source explicitly reports sales and rising prices because of the cold;preserve those details and reportedness rather than applying a blanket no-price rule. The separate Furs/Stockholm notice stays prospective. '
    'Bind both current Stockholm aliases,Furs56 and clean couple roles164/165 without invented marriage,age,kinship,date,temperature,price amount,scarcity,guaranteed profit,purchase,medical/gameplay effect or earlier conversation location.\n\n'
    'Visual review caught premature three-row R16 wrapping despite room for two safe rows. The frozen exact source/prose-bound v2 reviews one ordinary complete-word boundary after in,keeping this cold and prices are going up coherent. '
    'Every word and7 other compiled targets/native planes remain exact. Six mutation controls prevent transfer of the boundary review;its exact shared warning and reason are recorded on R16. '
    'All8 native panels on1 sheet,64 initial alignments and32 final stored cases (16 fresh/16 exact-byte reuse),18 source-consumer/28 formatter negatives,four original name consumers,three entry censuses,guarded ends and8 relocated dispatches pass. '
    '336 target loads/cache hits and672 parent modes are fresh;the336/672 current-parent proofs are reused only after exact whole-ROM equality to the already tested V5076 reference. '
    'All11 source commands,eight complete preambles,A0008 raw00a0ffff013807a1,C200 and four-byte end remain.388 source stored/logical bytes become376 stored/logical;C200382 maps370,end384 maps372,with no trailing bytes. '
    'There are7 progressive objects/one null-actor FE and no source substitutions,predicates,relatives,typed objects,pauses,resources or presentations. Exact inverse recovers every predecessor byte;335 other SC2 blocks stay exact. '
    'The atomic compiler checks complete references,source/target extents,both command maps,reported sales/prices and the exact boundary reason.73 meaningful negatives reject before mutation;78 regression tests and18 cumulative release checks pass.\n\n'
    'Two disclosed Japanese/English B22 content cold boots9001 frames each execute all11 source commands plus9 original initializers:20 commands,all8 panels,five A000s,C200 and normal end. '
    '31 complete held text planes and115 paired upper/portrait/name samples match. Both actual sheets and26 full paired screens were viewed. Both couple portraits/nameplates,the two-row market comment,the restored concession and null-actor FE transition remain complete. '
    'Returns4777/4775 and8 timings differ. Seven later original A-indicator differences at5530/5710/6310/6730/6910/7450/7630 remain inside x224..239/y360..375,the first two affecting its lower shadow. '
    'Final RGB,five measured native groups and whole1A04 actor/captain2 agree;PRNG463267532/790984746 differs. Retain all differences without masking,retiming or claiming causal PRNG,future-world or full-RAM equivalence. '
    'No natural event185 selection,earned fashion,earlier conversation location,full-route or hardware claim. Later dialogue adds no editorial credit. '
    'The initial exported-copy state analyzer stopped at an accidentally renamed0xCB185 address;corrected5117b restores original0xCB184 without rerunning or altering emulator captures. '
    'A numeric-constant derivation guard now rejects that substitution before writing. The unexecuted startup draft is preserved;guarded5125b retains every native high integer constant and multiplicity. '
    'Fresh V5122 New Game4001 and inherited-battery town17401 cold boots match exact-font V5076 across31 whole frames/five actor controls;donor hashes stay exact. The six-frame sheet was viewed after its image call returned. '
    'Four new content/current boots total39404 frames and all jobs are terminal/reaped.\n\n'
    'V5122 preserves the full V5076 stack:569 manifest batches/114 accepted layers. Only SC2B185 changes;all other stories,messages,fonts,graphics,ARM9/ARM7,components and123040-byte staged pool stay exact. '
    'The cumulative ROM equals the one-block reference and exact clean-input patch reconstruction. Immutable inputs,promoted main V4701 and every previous ROM,translation,draft,executed producer,proof,failure and nested ledger value are preserved. No promotion or pruning.\n\n'
    'Coverage becomes6015 completed contextual rereads,6018 source/prose,3811 integrated revisions/2204 retentions,SC24130/SC396 and routes4416/4416,with zero pending credited route drafts. '
    'These8 were uncredited and are counted once. B186 has12 fresh clean-only glosses with zero credit. The full editorial objective remains active.\n\n')

def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all569_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert start['all_current_requested_and_final_framebuffers_equal_V5076'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==73 and reg['all_negatives_reject_before_mutation']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==8 and not actual['failures']
    assert sum(len(r['holds']) for r in actual['actual_panels'])==31
    assert transitions['fixture_return_frames']==[4777,4775] and transitions['exact_timing_difference_counts']==dict(total=8,speech=6,control_or_end=2)
    assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==7 and transitions['later_seven_original_A_indicator_differences_reviewed_without_masking_or_retiming']
    assert transitions['whole_RGB_final9001_equal'] and transitions['postscene9001_PRNG_seeds']==[463267532,790984746] and not transitions['PRNG_equality']
    assert transitions['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and transitions['no_open_translation_specific_display_or_control_finding']
    tests=read('work/analysis/lil_B185_release_tools_v5122/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['stdout']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==569 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B185_retention_v5126/pin_receipt.json')['all_prior_pins_preserved']
    source=read(NEXT_SOURCE);assert len(source['records'])==12 and source['read_no_predecessor_English'] and source['new_review_credit']==0
    return release

def restore(new):
    inverse=deepcopy(new);entry=inverse.pop(KEY);back=entry['inverse_preserved_values']
    inverse['current_integrated_candidate']=inverse.pop(PARENT_KEY);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(SCOPE)
    assert inverse['completed_editorial_families'].pop()['id']==FAMILY;inverse.update(back['root_values'])
    fresh=inverse['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert fresh[k][-8:]==entry['record_keys'];del fresh[k][-8:]
    assert fresh['record_IDs'][-8:]==entry['record_IDs'];del fresh['record_IDs'][-8:]
    assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values'])
    active=inverse['active_source_prose_drafts'];assert active['manuscripts'].pop()==str(DOC)
    assert active['route_record_subsets_pending'].pop(str(DOC))==[];active['note']=back['active_note']
    assert inverse['coverage_units'].pop()['id']==FAMILY;inverse['coverage_units'][back['route_unit_index']]=back['route_unit'];inverse['formatting_watchlist'].pop(WATCH)
    return inverse

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':4,'retain-wording':4} and (doc['source_prose_or_completion_credit_added']==0 and old['unfinished_editorial_scope_v5081']['Lil_B185_clean_only_uncredited_objects']==8)
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[185]
        refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex'])
            assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','source_prose_or_completion_credit_added']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
            body=value[1:];assert not any(m in body for m in [b'FI',b'FA',b'FO'])
            newref=dict(block=185,offset=at,header_offset=at-5,bytes=len(value),record_index=block[:at].count(b'\0'))
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),
                record_index=newref['record_index'],current_record_index=newref['record_index'],current_English=body.decode('ascii'),current_stored_English=body.decode('ascii'),
                current_raw_storage_English=body.decode('ascii'),current_effective_runtime_English=body.decode('ascii'),current_effective_macro_template_hex=body.hex(),
                current_effective_macro_template_English=body.decode('ascii'),current_effective_paragraph=' '.join(body.decode('ascii').split()),registered_runtime_catalog_entry=None,
                completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,
                current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,
                decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release')
            assert row['current_effective_paragraph']==row['english'].split('}',1)[1] and all(row['review'].values())
        oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
        assert len(oldkeys)==6007 and len(keys)==8 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6007 and not fresh['pending_record_keys']
        summary=DETAILS+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS,PRIOR,NEXT_SOURCE,Path(doc['reference_map']),Path(doc['native_font_proof']),
            Path('work/analysis/lil_B185_release_tools_v5122/regression_test_results.json'),Path('work/analysis/lil_B185_retention_v5126/pin_receipt.json'),Path(__file__)]}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
            revised=4,retained=4,source_prose_and_completion_credit_added_once=8,previous_B185_objects_uncredited=True,all8_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,
            actual_unique_speeches=8,actual_matching_holds=31,natural_event185_not_selected=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);rootnames=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated',
            'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']
        freshnames=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']
        routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
        back=dict(root_values={k:deepcopy(old[k]) for k in rootnames},fresh_values={k:deepcopy(fresh[k]) for k in freshnames},
            active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[185],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,
            revised_count=4,retained_count=4,fresh_revisions=4,fresh_retentions=4,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=6015,records_with_source_and_prose_pass=6018,records_with_source_prose_drafts=6018,records_revised_and_integrated=3811,retained_wordings_editorially_completed=2204)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC2.DK4']==4122;new[key]['/data/SC2.DK4']=4130
        keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871']
        note='6015 contextual rereads integrated;source/prose6018. B185 counted once;all wider families and earlier premature wrapping remain open.'
        for key in ['record_keys','integrated_record_keys']:f[key].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=6015,fresh_pass_records_integrated=6015,latest_contextual_manuscript=str(DOC),
            latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=8,final_review=str(FINAL),new_revisions=4,justified_retentions=4,new_completed_records=8,historical_reconciliation_only=False,
            actual_selected_source185_events=[],actual_B22_content_speeches=8,new_current_candidate_emulator_runs=2,explicit_content_fixture_runs=2,goal_turn_new_frames=39404))
        active=new['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'] and str(DOC) not in active['route_record_subsets_pending']
        active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
        new['coverage_units'][routeindex].update(reviewed_route_records=4416,completed_route_records=4416,next=NEXT)
        new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[185],
            completion_credit_added=8,final_review=str(FINAL),actual_source_event185_selected=False,goal_turn_new_emulator_runs=4,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all8-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),
            exact_R16_ordinary_boundary_reviewed_without_word_change=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
            patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        new[PARENT_KEY]=old['current_integrated_candidate'];new['current_integrated_candidate']=current;new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=summary
        inventory=deepcopy(read(old['unfinished_editorial_scope_v5081']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B185_completed_v5127']=dict(final_review=str(FINAL),completed_objects=8,registered_candidate=release['candidate'],natural_event185_not_selected=True)
        inventory['next_Lil_B186_clean_only_v5131']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=12,uncredited=True)
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4416,completed_route_records=4416,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B185_previously_uncredited_objects_completed=8,Lil_B186_clean_only_uncredited_objects=12,incomplete_COMMON=3,
            incomplete_credited_route_drafts=0,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,
            record_IDs=[r['id'] for r in rows],new_source_prose_reviews=8,new_completed_records=8,revised=4,retained=4,goal_turn_classification='progress',goal_turn_new_emulator_runs=4,
            goal_turn_new_frames=39404,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
        assert new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5127: Eight Lil B185 reviews integrated once in cumulative V5122\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5127\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=8,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six targets staged;eight reviews counted once in proposed ledger. Audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6015,6018,3811,2204)
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates();assert new['current_integrated_candidate']['sha256']==release['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists()
            save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,
                exactly8_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False))
            print('Six targets,all historical values and eight disjoint new keys audited.')
        elif mode=='apply':
            assert not (ROOT/'native_application_receipt.json').exists();assert read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False))
            print('Six audited completion files applied exactly.')
        else:
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();assert len(read(FINAL)['records'])==8
            oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};allkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(oldkeys)==6007 and len(allkeys)==6015
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly8_new_disjoint_source_prose_and_completed_records=True,
                completed=6015,source_prose=6018,revised=3811,retained=2204,SC2=4130,SC3=96,reviewed_routes=4416,completed_routes=4416,
                all569_manifest_batches114_accepted18_checks_verified=True,actual_unique_B185_speeches=8,actual_matching_holds=31,
                startup31_frames_and_five_actor_controls_match_V5076=True,source185_natural_eligibility_and_earned_fashion_not_claimed=True,
                eight_timing_seven_later_indicator_and_unequal_PRNG_differences_preserved=True,new_clean_only_Lil_B186_uncredited_objects=12,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5122 integration verified;6015 completed/6018 source-prose. Twelve B186 clean-only glosses pending;full goal active.')
