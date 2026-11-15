"""Credit25 previously uncredited B183 reviews after all registered gates."""
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

ROOT=Path('work/analysis/lil_B183_completion_v4971')
DOC=Path('translations/lil_B183_editorial_manuscript_v8.json')
FINAL=Path('translations/lil_B183_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B183_release_v4967/registered_release_verification.json')
START=Path('work/analysis/lil_B183_startup_v4969/cold_boot_Lil_startup_town_verification.json')
VISUAL=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B183_actual_v4960/actual_all25_progressive_FE_A000_C200_and_single_end.json')
TRANSITIONS=Path('work/analysis/lil_B183_actual_review_v4961/all5_actual_sheets25_planes_fullscreens_return_and_final_state.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4956/verified_handoff.json')
REG=Path('work/analysis/lil_B183_registration_v4965/registration_receipt.json')
FAMILY='Lil-B183-art-collectors-competing-tastes-candor-secrecy-and-prospective-Basra25'
SOURCE=Path('work/analysis/lil_B183_clean_context_v4923/all25_clean_exchange_and_fresh_glosses.json')
ACTUAL_SCOPE='Two disclosed Japanese/English B22 content cold boots11001 frames each show all25 B183 panels,23 progressive and two impersonal FE. All28 source commands plus9 original B22 initializers remain stored and all37 execute,including five A000s,C200 and one end. Five distinct progressive roles and source Sailor153 voice4 are preserved;the full-catalogue Retainer153 stays separate. All25 complete native planes,five actual sheets,149 paired nontext samples and14 full screens are viewed. The fitting R35 question remains intact;Slam! clears portrait/name and the shopkeeper returns afterward;the closing notice stays prospective. Returns8855/8854;11 timings differ (9 speech/2 control or end). All sampled postscene RGB from8890 and final11001 agree without masking or retiming. Five native state groups and whole1A04 actor/captain2 agree;final PRNG1228390232/713326998 differs and remains disclosed. Actual C200 request[1,2,13,0,2,0,1] is measured rather than forced to isolated resource-zero fields. No causal PRNG,future-world or full-RAM equivalence claim. Two current cumulative V4966 New Game4001 and inherited-battery town17401 cold boots reuse exact-font V4914 controls. Four new cold boots total43404 frames. No natural event183 eligibility,earned fashion,earlier shop location,full-route or hardware claim. Following B120 adds no credit.'
NEXT='Continue the full editorial objective from verified cumulative V4966. The complete B183 exchange is integrated once;do not repeat its passed gates without a concrete risk. Revisit earlier premature wrapping,including COMMON682/764/774/775 and analogous fitting-question or complete-locative cases. Begin with exact clean/current whole-exchange references and consumer-specific native widths/controls;retain good prose and meaningful pacing. Apply source-bound successors only where the contextual and native evidence warrants them;do not modify frozen historical compilers or add duplicate editorial credit. The B183 v3 fix preserves the fitting first question and complete over there without changing any word,width,font,metric,guard or authored break. Continue every remaining storyline,shared town/shop exchange,random scene,Help and other player prose,including earlier translations,retentions and premature wrapping. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance,untranslated Sao Jorge alias15E5D4/pointer122504 and wrapping leads682/764/774/775. Keep graphics/all18 plaques and later older-record technical re-audit/queued0D separate and open. Preserve all ROMs,translations,drafts,executed producers,proofs,failures and complete historical ledger. The full editorial goal remains active.'
SUMMARY='V4971 completes25 B183 whole-exchange reviews once in registered cumulative V4966:16 revisions and9 individually justified retentions. Restore the lasting-fame prediction,recommendation to acquire work,competing art judgments and purchase intentions,private irritation after polite service,rich-person pastime echo,limited connoisseurship,candid laughter and secrecy request. Retain praise,skeptical Really?/Oh.,blunt preference,service thanks,Slam!,commotion question,Rich folks at play and Of course with individual reasons. Artwork may become popular in Basra remains prospective. No named artist,title,rank,kinship,unshown pointing direction,price,currency,guaranteed fame,objective art verdict,earned boom or earlier location is invented. All25 exact source/predecessor/runtime/logical/integrated references bind.\n\nA concrete premature-wrap finding was corrected:What are you two talking about? now fits intact on line1,then That one over there / is obviously better! The source-bound v3 planner recognizes the complete locative and prioritizes an intact fitting first sentence after weak-boundary,orphan and row-count rules. All words and the other24 encoded targets/native planes stay exact. No authored break,prose shortening,font,metric,width or guard changes. Historical v1/v2,partial-question finding and all earlier compilers are preserved. Analogous earlier wrapping remains a retroactive contextual review obligation.\n\nAll28 commands,25 complete preambles,leading A0008 raw00a0ffff013926a1,C200 and four-byte end are preserved.956 source bytes become1056 stored/1054 logical,C200950 maps1048,end952 maps1050,two trailing alignment zeros. No predicates,relative sites,typed objects,pauses,resources,presentations or FI/FA/FO exist. Inverse reconstruction restores every predecessor logical byte;335 other SC2 blocks remain exact. All200 initial and100 stored alignments,24 source-consumer/28 formatter negatives,ten role-name consumers,336 fresh loaders/672 modes,exact parent reuse,three entry censuses,guarded ends and25 relocated dispatches pass. The atomic compiler rejects57 meaningful negatives before mutation;78 release/dialogue regressions and18 cumulative checks pass.\n\nTwo disclosed Japanese/English B22 content cold boots11001 frames each show all25 B183 panels,23 progressive and two impersonal FE. All28 source commands plus9 original B22 initializers remain stored and all37 execute,including five A000s,C200 and one end. Five distinct progressive roles and source Sailor153 voice4 are preserved;the full-catalogue Retainer153 stays separate. All25 complete native planes,five actual sheets,149 paired nontext samples and14 full screens are viewed. The fitting R35 question remains intact;Slam! clears portrait/name and the shopkeeper returns afterward;the closing notice stays prospective. Returns8855/8854;11 timings differ (9 speech/2 control or end). All sampled postscene RGB from8890 and final11001 agree without masking or retiming. Five native state groups and whole1A04 actor/captain2 agree;final PRNG1228390232/713326998 differs and remains disclosed. Actual C200 request[1,2,13,0,2,0,1] is measured rather than forced to isolated resource-zero fields. No causal PRNG,future-world or full-RAM equivalence claim. Two current cumulative V4966 New Game4001 and inherited-battery town17401 cold boots reuse exact-font V4914 controls. Four new cold boots total43404 frames. No natural event183 eligibility,earned fashion,earlier shop location,full-route or hardware claim. Following B120 adds no credit.\n\nThe complete V4914 stack remains included:565 manifest batches/114 accepted layers. Only SC2 block183 differs;all other files,fonts,graphics,stories,ARM9/ARM7 and components remain exact. The candidate equals the reviewed one-block reference and exact clean-input patch reconstruction. Promoted main V4701/pushed4d63fd3/tag promoted-v4701 and immutable inputs remain preserved. This is an experimental verified editorial checkpoint.\n\nCoverage becomes5966 completed contextual rereads,5969 source/prose,3780 integrated revisions/2186 retentions,SC24113 and route4367/4367,zero pending credited route drafts. B183 previously had25 approved uncredited objects;source/prose and completion each advance exactly25. The full editorial objective stays active.\n\n'

def make_summary(release):
    return SUMMARY+"Candidate SHA256 "+release["candidate_sha256"]+". Patch SHA256 "+release["patch_sha256"]+".\n\n"+NEXT

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');before_raw=lp.read_bytes();ledger=json.loads(before_raw);before=deepcopy(ledger)
    assert sha(before_raw)==read(PRIOR)['ledger_sha256']
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all565_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4914'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==25 and not actual['failures']
    assert transitions['actual_new_cold_boot_runs']==2 and transitions['whole_RGB_final11001_equal']
    assert transitions['exact_timing_difference_counts']==dict(total=11,speech=9,control_or_end=2)
    assert not transitions['sampled_postscene_whole_RGB_differences_unmasked'] and transitions['all_sampled_postscene_whole_RGB_equal']
    assert transitions['postscene11001_PRNG_seeds']==[1228390232,713326998] and not transitions['PRNG_equality']
    assert reg['negative_count']==57 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B183_release_tools_v4966/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['stdout']
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert len(rows)==25 and Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':9}
    image=NdsImage.open(release['candidate']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[183]
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    stage={r['id']:r for r in release['stage']['changed_records']}
    sampled={r['id'] for r in actual['actual_panels']};assert sampled==set(refs) and len(sampled)==25
    for row in rows:
        spec=refs[row['id']];at=spec['new_offset'];value=bytes.fromhex(spec['target_hex']);body=value[1:]
        assert all(row['review'].values()) and row['source_meaning'] and row['localization_note']
        assert block[at:at+len(value)]==value and block[at+len(value)]==0 and stage[row['id']]['new_offset']==at
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and value[0]==row['source_selector']
        fields=['current_reference','current_hex','current_English','current_record_index','record_index','current_raw_storage_English',
            'current_effective_runtime_English','current_effective_macro_template_hex','current_effective_macro_template_English',
            'current_effective_paragraph','registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
        ref=dict(block=183,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
        paragraph=row['english'].split('}',1)[1]
        row.update(current_reference=ref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=ref,integrated_hex=value.hex(),
            current_record_index=ref['record_index'],record_index=ref['record_index'],completed_candidate_reference=release['candidate'],
            completed_candidate_sha256=release['candidate_sha256'],current_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),
            current_effective_runtime_English=body.decode('ascii'),current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=body.decode('ascii'),
            current_effective_paragraph=paragraph,registered_runtime_catalog_entry=None,effective_predecessor_macro_paragraph=row['effective_predecessor_paragraph'],
            historical_editorial_decision=row['editorial_decision'],actual_B22_display_fixture_observed=True,offline_only_complete_native_display_verified=False,
            actual_source_event182_selected=False,individual_actual_source_event_activation_not_claimed=True,current_complete_native_display_pending=False,
            registered_integration_pending=False,status='complete-contextual-current-native-references-representative-and-registered-release')
        if row['editorial_decision']=='retain-wording':assert paragraph==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    old_keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};selected={historical_key(r) for r in rows}
    assert len(old_keys)==5941 and len(selected)==25 and not old_keys&selected
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert not fresh['pending_record_keys']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'])==(5941,5941)
    assert ledger['lil_B183_contextual_native_reference_v4955']['source_prose_or_completion_credit_added']==0
    ROOT.mkdir(parents=True);docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    proof_paths=[DOC,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,SOURCE,Path(doc['reference_map']),Path(doc['representative_proof']),
        Path('work/analysis/lil_B183_release_tools_v4966/regression_test_results.json'),Path('work/analysis/lil_B183_retention_v4970/pin_receipt.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in proof_paths};summary=make_summary(release)
    final=dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),
        manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        records=rows,revised=16,retained=9,source_prose_and_completion_credit_added_once=25,previous_B183_objects_uncredited=True,
        all25_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,actual_sampled_B22_display_IDs=sorted(sampled),
        offline_only_display_IDs=[],actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=summary,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[183],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=16,retained_count=9,fresh_revisions=16,fresh_retentions=9,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5966,records_with_source_and_prose_pass=5969,records_with_source_prose_drafts=5969,
        records_revised_and_integrated=3780,retained_wordings_editorially_completed=2186)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:ledger[key]['/data/SC2.DK4']=4113
    key_rows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:fresh[key].extend(deepcopy(key_rows))
    fresh['record_IDs'].extend(r['id'] for r in rows)
    note='5966 contextual rereads integrated;source/prose5969. B18325 integrated once;all wider families and earlier premature wrapping remain open.'
    fresh.update(fresh_pass_records_explicitly_reread=5966,fresh_pass_records_integrated=5966,latest_contextual_manuscript=str(DOC),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
    fresh['reconciled_families'].append(dict(id=FAMILY,records=25,final_review=str(FINAL),new_revisions=16,justified_retentions=9,new_completed_records=25,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=16,retained=9),actual_selected_B183_source_events=[],
        actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=[],new_current_candidate_emulator_runs=2,
        new_explicit_display_fixture_runs=2,new_focused_repeat_runs=0,new_parent_control_runs=0))
    active=ledger['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'];active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4367,completed_route_records=4367,next=NEXT)
    ledger['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',
        file_path='/data/SC2.DK4',blocks=[183],completion_credit_added=25,final_review=str(FINAL),actual_sampled_B22_display_IDs=sorted(sampled),
        actual_source_event182_selected=False,new_emulator_runs=4,full_goal_complete=False))
    ledger['formatting_watchlist']['lil_B183_v4971']=dict(status='all25-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),
        no_glyph_bounds_pagination_or_control_waivers=True,actual11_timing_and_final_RNG_differences_with_sampled_RGB_equality_disclosed=True,evidence=evidence)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    candidate.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});ledger['current_integrated_candidate']=candidate
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4971']['path']));inventory['next_focus']=NEXT
    inventory['historical_B183_lead_before_v4971']=deepcopy(inventory['next_B183_clean_context_v4923'])
    inventory['remaining_B183_unreviewed_uncredited']=dict(physical_speeches=0,typed_choice_command_leads=0,completed_final_review=str(FINAL),not_full_Lil_or_project_denominator=True)
    inventory['lil_B183_completed_v4971']=dict(completed_targets=25,final_review=str(FINAL),registered_candidate=release['candidate'],actual_unique_speeches=25,actual_FE_panels=2,source_event183_not_naturally_selected=True)
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4367,completed_route_records=4367,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4971']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,
        completed_B183_previously_uncredited_objects=25,next_earlier_wrap_revisit_leads=[682,764,774,775],later_storylines_shared_town_shop_random_help_prose_open=True,
        canonical_Maria32_pending_uncredited=True,Proof_terminology_consistency_open=True,full_goal_complete=False)
    ledger['lil_B183_completion_v4971']=dict(summary=summary,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=summary
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert len(old_keys|selected)==5966 and old_keys|selected=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    staged=[];planned=ROOT/(lp.name+'.planned');planned.write_bytes(encode_ledger(ledger));assert planned.stat().st_size<100*1024*1024
    staged.append(dict(target=str(lp.resolve()),before_sha256=sha(before_raw),planned=str(planned.resolve()),planned_sha256=sha(planned.read_bytes())))
    section='## V4971:25 B183 reviews completed in cumulative V4966\n\n'+summary+'\n\nFinal review: '+FINAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);text=('# Current editorial handoff - V4971' if i==0 else first)+'\n\n'+section+rest
        planned=ROOT/(p.name+'.planned');data=text.replace('\n','\r\n').encode('utf-8');planned.write_bytes(data)
        staged.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    receipt=dict(checkpoint='V4971',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,
        updated_files={r['target']:r['planned_sha256'] for r in staged},new_source_prose_reviews=25,new_completed_records=25,revised=16,retained=9,
        completed=5966,source_prose=5969,historical_revised=3780,historical_retained=2186,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=565,accepted_layers=114,new_actual_emulator_runs=4,
        actual_unique_speech_panels=25,actual_FE_panels=2,completed_B183_previously_uncredited_objects=25,all_jobs_terminal=True,full_goal_complete=False)
    rp=ROOT/'staged_completion_receipt.json';save(rp,receipt);save(ROOT/'staged_completion.json',dict(files=staged,staged_receipt=str(rp),staged_receipt_sha256=sha(rp.read_bytes()),no_current_ledger_or_document_mutation_yet=True))
    print('B183 completion staged:25 new source/prose and25 completions once;5966 integrated. Independent audit/application pending.')
