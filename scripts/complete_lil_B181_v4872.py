"""Credit eleven previously uncredited B181 reviews after all registered gates."""
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B181_completion_v4872')
DOC=Path('translations/lil_B181_editorial_manuscript_v4.json')
FINAL=Path('translations/lil_B181_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B181_release_v4868/registered_release_verification.json')
START=Path('work/analysis/lil_B181_startup_v4870/cold_boot_Lil_startup_town_verification.json')
VISUAL=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B181_actual_v4861/actual_all10_progressive_FE_A000_C200_and_single_end.json')
TRANSITIONS=Path('work/analysis/lil_B181_actual_review_v4862/all2_actual_sheets10_planes_fullscreens_return_and_final_state.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4850/verified_handoff.json')
REG=Path('work/analysis/lil_B181_registration_v4866b/registration_receipt.json')
FAMILY='Lil-B181-three-Ladies-ruby-necklace-wistful-gift-three-sighs-and-prospective-Athens10'
B182=Path('work/analysis/lil_B182_clean_context_v4877/all8_clean_exchange_and_fresh_glosses.json')
ACTUAL_SCOPE='Two disclosed Japanese/English B22 content cold boots9001 frames each show all10 B181 speeches,nine progressive Lady166/167/168 and one impersonal FE. All13 source commands plus9 original B22 initializers remain stored and execute as22 commands,including five A000s,C200 and one end. Ten complete native text planes,115 paired nontext samples and12 full screens are viewed. Both versions return at5257;no measured command timing or postscene RGB differences. Five native state groups,whole1A04 actor/captain2 and PRNG790984746 agree at9001. These observations do not prove future-world or full-RAM equality. Current cumulative V4867 New Game4001 and inherited-battery town17401 cold boots compare against exact-font V4821;two prior-build controls are reused. Four new cold boots total39404 frames. No natural event181 eligibility,earned fashion state,prior scene location,full-route or hardware verification claim.'
NEXT="Continue B182 from its complete clean-only inventory4876 and eight fresh glosses4877 before any predecessor English. Read the reported princess engagement to the duke's son,the extravagant mountain-price ring gossip,anticipated fashion,and comic admission that the gemstone identity is unknown as one exchange. Preserve source-explicit royal/ducal ranks and kinship without inventing names,house,age,currency,date,a completed wedding or a specific gemstone. Bind current voices/names,London and gemstone category,all25 commands,eight speeches,two original500 RNG predicates,ten relative sites,three alternative A000s,C200 and end. Do not inherit B181 linear/no-predicate assumptions or guess Ruby from the prior exchange. No need to repeat completed B181 checks without a concrete risk. Continue every remaining storyline,shared town/shop exchange,random scene,Help and player prose,including prior retentions and premature wrapping. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,Proof consistency,Samwell catalog middle-field lead,B157 provenance,untranslated Sao Jorge alias15E5D4/pointer122504 and wrapping leads682/764/774/775. Keep graphics/all18 plaques and later older-record technical re-audit/queued0D separate and open. Preserve every ROM,translation,draft,producer,proof,failure and full historical ledger. The full goal remains active."

def make_summary(release):
    return 'V4872 completes10 B181 whole-exchange reviews once in registered cumulative V4867:5 revisions and5 individually justified retentions. Preserve the red-ruby question,enthusiastic reply,the third speaker joining,the necklace explanation and recognition. Make the once-in-a-lifetime wish for a gift from a man explicit and preserve three separately voiced wistful Ahh... sighs. The neutral prospective Rubies/Athens notice preserves the approved commodity and city. No noble rank,spouse,suitor,giver identity,necklace gift provenance,price,shortage,earned boom or earlier location is invented. All ten source/predecessor/runtime/logical/integrated references bind. No new manual break,phrase exception,font,metric,guard or prose shortening.\n\nAll13 commands,ten complete preambles,A0008 raw00a0ffff014913a1,C200390 and end392 are preserved. Source396 maps reversibly to380 stored/logical bytes,C200374/end376. No predicates,relative sites,typed objects,source substitutions,pauses,resources or presentations exist. Ten current-font native planes,80 logical/compiled and40 final stored alignments pass,with20 source-consumer and28 formatter negatives. Exact whole-current-ROM loader proof is reused;336 fresh target loaders/672 parent modes,three entry censuses,guarded end decodes and relocated dispatch/control pairs pass. The atomic compiler rejects48 meaningful negatives before mutation;78 release/dialogue regressions and18 cumulative release checks pass.\n\nTwo disclosed Japanese/English B22 content cold boots9001 frames each show all10 B181 speeches,nine progressive Lady166/167/168 and one impersonal FE. All13 source commands plus9 original B22 initializers remain stored and execute as22 commands,including five A000s,C200 and one end. Ten complete native text planes,115 paired nontext samples and12 full screens are viewed. Both versions return at5257;no measured command timing or postscene RGB differences. Five native state groups,whole1A04 actor/captain2 and PRNG790984746 agree at9001. These observations do not prove future-world or full-RAM equality. Current cumulative V4867 New Game4001 and inherited-battery town17401 cold boots compare against exact-font V4821;two prior-build controls are reused. Four new cold boots total39404 frames. No natural event181 eligibility,earned fashion state,prior scene location,full-route or hardware verification claim.\n\nThe complete V4821 stack remains included:563 manifest batches and114 accepted layers. Only SC2 block181 differs from that parent;all other files,fonts,graphics,stories,ARM9/ARM7 and components remain exact. The candidate equals the reviewed one-block reference and the clean-input patch reconstruction. Main V4701/pushed4d63fd3/tag promoted-v4701 and the immutable baseline remain unchanged. This is an experimental verified editorial checkpoint.\n\nCoverage becomes5933 completed contextual rereads,5936 source/prose,3758 integrated revisions/2175 retentions,SC24080 and route4334/4334,with zero pending credited route drafts. The prior ten B181 approved objects had zero credit;source/prose and completion each advance exactly10. B182 has eight fresh clean-source glosses and zero credit;the full editorial objective remains open.\n\n'+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');before_raw=lp.read_bytes();ledger=json.loads(before_raw);before=deepcopy(ledger)
    assert sha(before_raw)==read(PRIOR)['ledger_sha256']
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all563_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4821'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==10 and not actual['failures']
    assert transitions['actual_new_cold_boot_runs']==2 and transitions['all_sampled_postscene_whole_RGB_equal']
    assert reg['negative_count']==48 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B181_release_tools_v4867/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['output']
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert len(rows)==10 and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':5}
    image=NdsImage.open(release['candidate']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[181]
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    stage={r['id']:r for r in release['stage']['changed_records']}
    sampled={r['id'] for r in actual['actual_panels']};assert sampled==set(refs) and len(sampled)==10
    for row in rows:
        spec=refs[row['id']];at=spec['new_offset'];value=bytes.fromhex(spec['target_hex']);body=value[1:]
        assert all(row['review'].values()) and row['source_meaning'] and row['localization_note']
        assert block[at:at+len(value)]==value and block[at+len(value)]==0 and stage[row['id']]['new_offset']==at
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and value[0]==row['source_selector']
        fields=['current_reference','current_hex','current_English','current_record_index','record_index','current_raw_storage_English',
            'current_effective_runtime_English','current_effective_macro_template_hex','current_effective_macro_template_English',
            'current_effective_paragraph','registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
        ref=dict(block=181,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
        paragraph=row['english'].split('}',1)[1]
        row.update(current_reference=ref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=ref,integrated_hex=value.hex(),
            current_record_index=ref['record_index'],record_index=ref['record_index'],completed_candidate_reference=release['candidate'],
            completed_candidate_sha256=release['candidate_sha256'],current_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),
            current_effective_runtime_English=body.decode('ascii'),current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=body.decode('ascii'),
            current_effective_paragraph=paragraph,registered_runtime_catalog_entry=None,effective_predecessor_macro_paragraph=row['effective_predecessor_paragraph'],
            historical_editorial_decision=row['editorial_decision'],actual_B22_display_fixture_observed=True,offline_only_complete_native_display_verified=False,
            actual_source_event181_selected=False,individual_actual_source_event_activation_not_claimed=True,current_complete_native_display_pending=False,
            registered_integration_pending=False,status='complete-contextual-current-native-references-representative-and-registered-release')
        if row['editorial_decision']=='retain-wording':assert paragraph==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    old_keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};selected={historical_key(r) for r in rows}
    assert len(old_keys)==5923 and len(selected)==10 and not old_keys&selected
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert not fresh['pending_record_keys']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'])==(5923,5923)
    assert ledger['lil_B181_contextual_native_v4849']['source_prose_or_completion_credit_added']==0
    ROOT.mkdir(parents=True);docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    proof_paths=[DOC,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,B182,Path(doc['reference_map']),Path(doc['representative_proof']),
        Path('work/analysis/lil_B181_release_tools_v4867/regression_test_results.json'),Path('work/analysis/lil_B181_retention_v4871/pin_receipt.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in proof_paths};summary=make_summary(release)
    final=dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),
        manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        records=rows,revised=5,retained=5,source_prose_and_completion_credit_added_once=10,previous_B181_objects_uncredited=True,
        all10_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,actual_sampled_B22_display_IDs=sorted(sampled),
        offline_only_display_IDs=[],actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=summary,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[181],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=5,retained_count=5,fresh_revisions=5,fresh_retentions=5,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5933,records_with_source_and_prose_pass=5936,records_with_source_prose_drafts=5936,
        records_revised_and_integrated=3758,retained_wordings_editorially_completed=2175)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:ledger[key]['/data/SC2.DK4']=4080
    key_rows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:fresh[key].extend(deepcopy(key_rows))
    fresh['record_IDs'].extend(r['id'] for r in rows)
    note='5933 contextual rereads integrated;source/prose5936. B182 has8 clean-only uncredited leads;all wider families and earlier wrapping remain open.'
    fresh.update(fresh_pass_records_explicitly_reread=5933,fresh_pass_records_integrated=5933,latest_contextual_manuscript=str(DOC),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
    fresh['reconciled_families'].append(dict(id=FAMILY,records=10,final_review=str(FINAL),new_revisions=5,justified_retentions=5,new_completed_records=10,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=5,retained=5),actual_selected_B181_source_events=[],
        actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=[],new_current_candidate_emulator_runs=2,
        new_explicit_display_fixture_runs=2,new_focused_repeat_runs=0,new_parent_control_runs=0))
    active=ledger['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'];active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4334,completed_route_records=4334,next=NEXT)
    ledger['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',
        file_path='/data/SC2.DK4',blocks=[181],completion_credit_added=10,final_review=str(FINAL),actual_sampled_B22_display_IDs=sorted(sampled),
        actual_source_event181_selected=False,new_emulator_runs=4,full_goal_complete=False))
    ledger['formatting_watchlist']['lil_B181_v4826']=dict(status='all10-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),
        no_glyph_bounds_pagination_or_control_waivers=True,actual_zero_timing_RGB_and_state_differences_with_scope_disclosed=True,evidence=evidence)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    candidate.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});ledger['current_integrated_candidate']=candidate
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4826']['path']));inventory['next_focus']=NEXT
    inventory['historical_B181_lead_before_v4872']=deepcopy(inventory['next_B181_clean_context_v4831'])
    inventory['remaining_B181_unreviewed_uncredited']=dict(physical_speeches=0,typed_choice_command_leads=0,completed_final_review=str(FINAL),not_full_Lil_or_project_denominator=True)
    inventory['lil_B181_completed_v4826']=dict(completed_targets=10,final_review=str(FINAL),registered_candidate=release['candidate'],
        actual_unique_speeches=10,actual_FE_panels=1,source_event181_not_naturally_selected=True)
    inventory['next_B182_clean_context_v4877']=dict(path=str(B182),sha256=sha(B182.read_bytes()),physical_speeches=8,review_credit=0)
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4334,completed_route_records=4334,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4872']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,
        next_B182_physical_speeches_uncredited=8,later_storylines_shared_town_shop_random_help_prose_open=True,canonical_Maria32_pending_uncredited=True,
        Proof_terminology_consistency_open=True,full_goal_complete=False)
    ledger['lil_B181_completion_v4872']=dict(summary=summary,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=summary
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert len(old_keys|selected)==5933 and old_keys|selected=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    staged=[];planned=ROOT/(lp.name+'.planned');planned.write_bytes(encode_ledger(ledger));assert planned.stat().st_size<100*1024*1024
    staged.append(dict(target=str(lp.resolve()),before_sha256=sha(before_raw),planned=str(planned.resolve()),planned_sha256=sha(planned.read_bytes())))
    section='## V4872:10 B181 reviews completed in cumulative V4867\n\n'+summary+'\n\nFinal review: '+FINAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);text=('# Current editorial handoff - V4872' if i==0 else first)+'\n\n'+section+rest
        planned=ROOT/(p.name+'.planned');data=text.replace('\n','\r\n').encode('utf-8');planned.write_bytes(data)
        staged.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    receipt=dict(checkpoint='V4872',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,
        updated_files={r['target']:r['planned_sha256'] for r in staged},new_source_prose_reviews=10,new_completed_records=10,revised=5,retained=5,
        completed=5933,source_prose=5936,historical_revised=3758,historical_retained=2175,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=563,accepted_layers=114,new_actual_emulator_runs=4,
        actual_unique_speech_panels=10,actual_FE_panels=1,next_B182_uncredited_speeches=8,all_jobs_terminal=True,full_goal_complete=False)
    rp=ROOT/'staged_completion_receipt.json';save(rp,receipt);save(ROOT/'staged_completion.json',dict(files=staged,staged_receipt=str(rp),staged_receipt_sha256=sha(rp.read_bytes()),no_current_ledger_or_document_mutation_yet=True))
    print('B181 completion staged:10 new source/prose and10 completions once;5933 integrated. Independent audit/application pending.')
