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

ROOT=Path('work/analysis/lil_B182_completion_v4919')
DOC=Path('translations/lil_B182_editorial_manuscript_v4.json')
FINAL=Path('translations/lil_B182_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B182_release_v4915/registered_release_verification.json')
START=Path('work/analysis/lil_B182_startup_v4917/cold_boot_Lil_startup_town_verification.json')
VISUAL=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B182_actual_v4906/actual_all8_progressive_FE_RNG_effect_C200_and_single_end.json')
TRANSITIONS=Path('work/analysis/lil_B182_actual_review_v4907/all8_panels_48_fullscreens_conditional_return_and_measured_differences_v2.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4911/verified_handoff.json')
REG=Path('work/analysis/lil_B182_registration_v4913/registration_receipt.json')
FAMILY='Lil-B182-princess-engagement-dukes-son-extravagant-ring-and-unknown-gem-London8'
B183=Path('work/analysis/lil_B183_clean_context_v4923/all25_clean_exchange_and_fresh_glosses.json')
ACTUAL_SCOPE='Two disclosed Japanese/English B22 content cold boots9001 frames each display all8 B182 speeches,seven progressive Lady166/167 and one impersonal FE. All25 source commands plus9 original B22 initializers remain stored;both conditional paths execute23 commands. Both unforced roll52/result0 select source effect532;C200,end and normal return are observed. All8 complete native text planes,115 paired nontext samples,2 actual sheets and48 full screens are viewed. Returns4776/4775;13 timings differ (7 speech/6 control/end). All18 later whole-RGB differences are the original A-button indicator at x224-240/y360-376. Final9001 RGB,five native state groups and whole1A04 actor/captain2 agree;final RNG seeds3723009301/403514907 differ and remain disclosed. No PRNG causal,future-world or full-RAM equivalence claim. Two current cumulative V4914 New Game4001 and inherited-battery town17401 cold boots reuse exact-font V4867 controls. Four new cold boots total39404 frames. No natural event182 eligibility,earned fashion,earlier London location,full-route or hardware claim.'
NEXT="Continue B183 from clean-only full inventory4922 and25 fresh glosses/context4923 before predecessor English. Read the collectors' competing judgments and buying declarations,the shopkeeper's polite service then private complaint,rich-person pastime exchange,laughing candor and secrecy request as one scene. Bind native names,roles and voices for99/94/6E/84/55;do not assume a player identity,Lady roles,rank or kinship. Preserve the source male-artist pronoun without naming an artist,claiming objective quality,or inventing paintings,prices,profits,investment mechanics or physical pointing directions. Bind approved Basra and painting goods/category terminology. Keep the FE impact sound separate from spoken dialogue and the closing city-specific fashion forecast prospective. There are25 physical speeches and28 commands;bind complete controls from this block without inheriting B182 conditional/effect counts or alignment. Do not repeat completed B182 gates without a concrete risk. Continue every remaining storyline,shared town/shop exchange,random scene,Help and other player prose,including earlier translations,retentions and premature wrapping. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance,untranslated Sao Jorge alias15E5D4/pointer122504 and wrapping leads682/764/774/775. Keep graphics/all18 plaques and later older-record technical re-audit/queued0D separate and open. Preserve all ROMs,translations,drafts,executed producers,proofs,failures and complete historical ledger. The full editorial goal remains active."

def make_summary(release):
    return (
        'V4919 completes8 B182 whole-exchange reviews once in registered cumulative V4914:6 revisions and2 individually justified retentions. '
        'Restore reported forthcoming engagement to the duke\'s son,reported extravagant engagement-ring price,admiration for the duke,anticipated princess appearance,increased interested ladies rather than every lady,and the question setting up the unknown-gem joke. '
        'Retain the brisk admission/ask-at-once reply and natural prospective Gems may catch on in London notice with individual reasons. Source-explicit princess,duke and son remain;no guessed gemstone,personal name,house,age,currency,date,completed wedding,active boom,shortage,profit or earlier scene location. '
        'All8 source/predecessor/runtime/logical/integrated references bind. No authored break,phrase exception,prose shortening,font,metric or guard change.\n\n'
        'All25 source commands,eight complete preambles,two raw500 predicates,ten relative operands,three alternative A000s,C200 and four-byte end are preserved. Source636 becomes652 stored/logical bytes;predicates512/544 map530/562,C200630 maps646,end632 maps648. '
        'All335 other SC2 blocks remain exact and inverse reconstruction restores every predecessor byte. Eight native planes,64 initial plus32 stored alignments,18 source-consumer/28 formatter negatives,336 fresh loaders/672 parent modes,exact whole-ROM parent reuse,three entry censuses,guarded ends and25 structural paths pass. '
        'Focused proof4896 binds24 aligned/unaligned cases to the original optional operand scratch02279600 writer0202A5D8 and RNG02168EB8 writer020D984C,with all other4MiB preserved. No emulator seed/outcome is forced. '
        'The atomic compiler rejects58 meaningful negatives before mutation;78 release/dialogue regressions and18 release checks pass.\n\n'+ACTUAL_SCOPE+'\n\n'
        'The entire V4867 stack remains included:564 manifest batches/114 accepted layers. Only SC2 block182 differs from that parent;all other files,fonts,graphics,stories,ARM9/ARM7 and components remain exact. '
        'The candidate equals the reviewed one-block reference and exact clean-input patch reconstruction. Main V4701/pushed4d63fd3/tag promoted-v4701 and immutable inputs remain preserved. This is an experimental verified editorial checkpoint.\n\n'
        'Coverage becomes5941 completed contextual rereads,5944 source/prose,3764 integrated revisions/2177 retentions,SC24088 and route4342/4342,zero pending credited route drafts. '
        'B182\'s prior8 approved objects were uncredited;source/prose and completion each advance exactly8. B183 has25 clean-only fresh glosses and zero credit;the full objective remains open.\n\n'
        'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT)

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');before_raw=lp.read_bytes();ledger=json.loads(before_raw);before=deepcopy(ledger)
    assert sha(before_raw)==read(PRIOR)['ledger_sha256']
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all564_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4867'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==8 and not actual['failures']
    assert transitions['actual_new_cold_boot_runs']==2 and transitions['whole_RGB_final9001_equal']
    assert transitions['exact_timing_difference_counts']==dict(total=13,speech=7,control_or_end=6)
    assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==18
    assert transitions['postscene9001_PRNG_seeds']==[3723009301,403514907] and not transitions['PRNG_equality']
    assert reg['negative_count']==58 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B182_release_tools_v4914/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['output']
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert len(rows)==8 and Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':2}
    image=NdsImage.open(release['candidate']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[182]
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    stage={r['id']:r for r in release['stage']['changed_records']}
    sampled={r['id'] for r in actual['actual_panels']};assert sampled==set(refs) and len(sampled)==8
    for row in rows:
        spec=refs[row['id']];at=spec['new_offset'];value=bytes.fromhex(spec['target_hex']);body=value[1:]
        assert all(row['review'].values()) and row['source_meaning'] and row['localization_note']
        assert block[at:at+len(value)]==value and block[at+len(value)]==0 and stage[row['id']]['new_offset']==at
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and value[0]==row['source_selector']
        fields=['current_reference','current_hex','current_English','current_record_index','record_index','current_raw_storage_English',
            'current_effective_runtime_English','current_effective_macro_template_hex','current_effective_macro_template_English',
            'current_effective_paragraph','registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
        ref=dict(block=182,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
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
    assert len(old_keys)==5933 and len(selected)==8 and not old_keys&selected
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert not fresh['pending_record_keys']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'])==(5933,5933)
    assert ledger['lil_B182_contextual_reference_v4910']['source_prose_or_completion_credit_added']==0
    ROOT.mkdir(parents=True);docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    proof_paths=[DOC,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,B183,Path(doc['reference_map']),Path(doc['representative_proof']),
        Path('work/analysis/lil_B182_release_tools_v4914/regression_test_results.json'),Path('work/analysis/lil_B182_retention_v4918/pin_receipt.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in proof_paths};summary=make_summary(release)
    final=dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),
        manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        records=rows,revised=6,retained=2,source_prose_and_completion_credit_added_once=8,previous_B182_objects_uncredited=True,
        all8_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,actual_sampled_B22_display_IDs=sorted(sampled),
        offline_only_display_IDs=[],actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=summary,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[182],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=6,retained_count=2,fresh_revisions=6,fresh_retentions=2,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5941,records_with_source_and_prose_pass=5944,records_with_source_prose_drafts=5944,
        records_revised_and_integrated=3764,retained_wordings_editorially_completed=2177)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:ledger[key]['/data/SC2.DK4']=4088
    key_rows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:fresh[key].extend(deepcopy(key_rows))
    fresh['record_IDs'].extend(r['id'] for r in rows)
    note='5941 contextual rereads integrated;source/prose5944. B183 has25 clean-only uncredited leads;all wider families and earlier wrapping remain open.'
    fresh.update(fresh_pass_records_explicitly_reread=5941,fresh_pass_records_integrated=5941,latest_contextual_manuscript=str(DOC),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
    fresh['reconciled_families'].append(dict(id=FAMILY,records=8,final_review=str(FINAL),new_revisions=6,justified_retentions=2,new_completed_records=8,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=6,retained=2),actual_selected_B182_source_events=[],
        actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=[],new_current_candidate_emulator_runs=2,
        new_explicit_display_fixture_runs=2,new_focused_repeat_runs=0,new_parent_control_runs=0))
    active=ledger['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'];active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4342,completed_route_records=4342,next=NEXT)
    ledger['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',
        file_path='/data/SC2.DK4',blocks=[182],completion_credit_added=8,final_review=str(FINAL),actual_sampled_B22_display_IDs=sorted(sampled),
        actual_source_event182_selected=False,new_emulator_runs=4,full_goal_complete=False))
    ledger['formatting_watchlist']['lil_B182_v4919']=dict(status='all8-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),
        no_glyph_bounds_pagination_or_control_waivers=True,actual_timing_and_final_RNG_differences_and18_indicator_differences_disclosed=True,evidence=evidence)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    candidate.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});ledger['current_integrated_candidate']=candidate
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4872']['path']));inventory['next_focus']=NEXT
    inventory['historical_B182_lead_before_v4919']=deepcopy(inventory['next_B182_clean_context_v4877'])
    inventory['remaining_B182_unreviewed_uncredited']=dict(physical_speeches=0,typed_choice_command_leads=0,completed_final_review=str(FINAL),not_full_Lil_or_project_denominator=True)
    inventory['lil_B182_completed_v4919']=dict(completed_targets=8,final_review=str(FINAL),registered_candidate=release['candidate'],
        actual_unique_speeches=8,actual_FE_panels=1,source_event182_not_naturally_selected=True)
    inventory['next_B183_clean_context_v4923']=dict(path=str(B183),sha256=sha(B183.read_bytes()),physical_speeches=25,review_credit=0)
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4342,completed_route_records=4342,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4919']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,
        next_B183_physical_speeches_uncredited=25,later_storylines_shared_town_shop_random_help_prose_open=True,canonical_Maria32_pending_uncredited=True,
        Proof_terminology_consistency_open=True,full_goal_complete=False)
    ledger['lil_B182_completion_v4919']=dict(summary=summary,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=summary
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert len(old_keys|selected)==5941 and old_keys|selected=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    staged=[];planned=ROOT/(lp.name+'.planned');planned.write_bytes(encode_ledger(ledger));assert planned.stat().st_size<100*1024*1024
    staged.append(dict(target=str(lp.resolve()),before_sha256=sha(before_raw),planned=str(planned.resolve()),planned_sha256=sha(planned.read_bytes())))
    section='## V4919:8 B182 reviews completed in cumulative V4914\n\n'+summary+'\n\nFinal review: '+FINAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);text=('# Current editorial handoff - V4919' if i==0 else first)+'\n\n'+section+rest
        planned=ROOT/(p.name+'.planned');data=text.replace('\n','\r\n').encode('utf-8');planned.write_bytes(data)
        staged.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    receipt=dict(checkpoint='V4919',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,
        updated_files={r['target']:r['planned_sha256'] for r in staged},new_source_prose_reviews=8,new_completed_records=8,revised=6,retained=2,
        completed=5941,source_prose=5944,historical_revised=3764,historical_retained=2177,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=564,accepted_layers=114,new_actual_emulator_runs=4,
        actual_unique_speech_panels=8,actual_FE_panels=1,next_B183_uncredited_speeches=25,all_jobs_terminal=True,full_goal_complete=False)
    rp=ROOT/'staged_completion_receipt.json';save(rp,receipt);save(ROOT/'staged_completion.json',dict(files=staged,staged_receipt=str(rp),staged_receipt_sha256=sha(rp.read_bytes()),no_current_ledger_or_document_mutation_yet=True))
    print('B182 completion staged:8 new source/prose and8 completions once;5941 integrated. Independent audit/application pending.')
