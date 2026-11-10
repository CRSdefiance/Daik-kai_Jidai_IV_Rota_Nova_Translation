"""Credit eleven previously uncredited B180 reviews after all registered gates."""
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

ROOT=Path('work/analysis/lil_B180_completion_v4826')
DOC=Path('translations/lil_B180_editorial_manuscript_v4.json')
FINAL=Path('translations/lil_B180_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B180_release_v4822/registered_release_verification.json')
START=Path('work/analysis/lil_B180_startup_v4824/cold_boot_Lil_startup_town_verification.json')
VISUAL=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B180_actual_v4811c/actual_all11_progressive_FE_RNG_effect_C200_and_single_end.json')
TRANSITIONS=Path('work/analysis/lil_B180_actual_review_v4812/all2_actual_sheets11_planes_fullscreens_and_resolved_effect_state.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4818b/verified_handoff.json')
REG=Path('work/analysis/lil_B180_registration_v4820d/registration_receipt.json')
FAMILY='Lil-B180-three-person-fragrance-reference-two-Ladies-and-prospective-Lisbon-Scents11'
B181=Path('work/analysis/lil_B181_clean_context_v4831/all10_clean_exchange_and_fresh_glosses.json')
ACTUAL_SCOPE=(
    'Two disclosed Japanese/English B22 content cold boots9001 frames each show all11 B180 speeches,ten progressive Lady166/167 and one null-actor FE,selected original RNG/effect paths,C200 and normal return. All28 source commands plus9 original initialization commands remain stored;conditional paths select31/26 commands. Two additional6001-frame cold boots export read-only effect boundaries to resolve the measured town difference. All common boundaries reproduce original runs exactly,including WRAM hashes. Original effects504/472 write town11 field102 from125 to315/317;the final four-array difference is exactly low byte59/61 at town-array1294. Actor,item,goods arrays and whole1A04 actor/captain2 agree. Final PRNG seeds differ2467799992/790984746;no forced RNG or future-world equivalence claim. Eleven actual panels,115 nontext samples,12 timings,12 original indicator-only RGB differences and36 full screens are retained. New cumulative V4821 New Game4001 and inherited-battery town17401 cold boots match31 framebuffers and5 actor/captain controls against exact-font V4766;one fresh V4766 town control17401 frames was needed. Seven new actual runs across content/focus/current-startup/parent-control,total68807 frames. Source event180 not naturally selected;no earned fashion,earlier location,full-route or hardware verification claim.')
NEXT=(
    'Continue B181 from its clean-only complete exchange inventory4830 and fresh glosses4831 before any predecessor English. Ten physical speeches,three courteous speakers,nine progressive and one FE,A000/C200/end are leads,not a project denominator or credited review. Bind exact current speakers/voices/names,Athens/Ruby terminology,source controls and event context;review the complete ruby-necklace admiration,wistful wish for a gift from a man and three successive sighs. Do not invent nobility,kinship,spouse,suitor,provenance of the admired necklace,price,shortage or earned boom. No need to repeat completed B180 gates without a concrete new risk. Continue every remaining storyline,shared town/shop exchange,random scene,Help and other player prose,including earlier retained translations and premature wrapping. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance,untranslated Sao Jorge alias15E5D4/pointer122504 and wrapping leads682/764/774/775. Keep graphics/all18 plaques and the later older-record technical re-audit/queued0D gap separate and open. Preserve all ROMs,translations,drafts,executed producers,proofs,failures and complete historical ledger. The full editorial goal remains active.')

def make_summary(release):
    return (
        'V4826 completes11 B180 whole-exchange reviews once in registered cumulative V4821:5 revisions and6 individually justified retentions. Preserve the clean-source shared-impression question,gender-unspecified third person,explicit knowledge limit,confident fashion prediction,surprised first-to-acquire urgency,future proposal to work up the nerve,warm replies and courteous farewells. The final impersonal forecast uses approved Scents in Lisbon rather than wrong Spices. No invented relationship,rank,gender,brand,ingredient,price,shortage,active boom or earlier location. All11 source/current/predecessor/runtime/logical/integrated references bind. No authored line break,prose shortening,font,metric or shared guard change.\n\n'
        'All28 commands,11 complete preambles,ten relative span fields,two original threshold500 RNG predicates,three alternative A000 leaves,C200 and one end are preserved. The576-byte source maps reversibly to548 stored/546 logical bytes;end572 maps to542. Eleven complete current-font planes,88 initial and44 final stored alignment cases,source/formatter negatives,672 fresh loaders,1344 parent modes,three entry censuses,guarded end decodes and25 mapped structural paths pass. The atomic compiler adds52 meaningful pre-mutation rejection cases. All78 release/dialogue regressions and18 cumulative release checks pass.\n\n'+ACTUAL_SCOPE+'\n\n'
        'The complete prior V4766 stack is preserved. The new manifest contains562 batches and114 accepted layers;only SC2 B180 differs from that parent,and every other file,font,graphic,story,ARM9,ARM7 and runtime component remains exact. The whole ROM equals the reviewed one-block research reconstruction and its clean-input patch reconstruction. Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'. Main V4701/pushed4d63fd3/tag promoted-v4701 and the immutable baseline remain unchanged. This is an experimental verified editorial build.\n\n'
        'Coverage becomes5923 completed contextual rereads,5926 source/prose,3753 integrated revisions and2170 retentions. SC2 source/prose and completion become4070;route reviewed/completed4324/4324 with zero pending credited route drafts. The prior11 B180 approved objects had zero credit;this checkpoint adds exactly11 to both source/prose and completion. B181 clean-source context/glosses has10 uncredited leads. Every wider editorial family,earlier wrapping revisit,graphics and later older-record technical re-audit remains open. Full goal active.\n\n'+NEXT)

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');before_raw=lp.read_bytes();ledger=json.loads(before_raw);before=deepcopy(ledger)
    assert sha(before_raw)==read(PRIOR)['ledger_sha256']
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all562_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4766'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==11 and not actual['failures']
    assert transitions['actual_new_cold_boot_runs']==4 and transitions['measured_persistent_town_difference_resolved_to_original_effect']
    assert reg['negative_count']==52 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B180_release_tools_v4822/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['output']
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert len(rows)==11 and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':6}
    image=NdsImage.open(release['candidate']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[180]
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    stage={r['id']:r for r in release['stage']['changed_records']}
    sampled={r['id'] for r in actual['actual_panels']};assert sampled==set(refs) and len(sampled)==11
    for row in rows:
        spec=refs[row['id']];at=spec['new_offset'];value=bytes.fromhex(spec['target_hex']);body=value[1:]
        assert all(row['review'].values()) and row['source_meaning'] and row['localization_note']
        assert block[at:at+len(value)]==value and block[at+len(value)]==0 and stage[row['id']]['new_offset']==at
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and value[0]==row['source_selector']
        fields=['current_reference','current_hex','current_English','current_record_index','record_index','current_raw_storage_English',
            'current_effective_runtime_English','current_effective_macro_template_hex','current_effective_macro_template_English',
            'current_effective_paragraph','registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
        ref=dict(block=180,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
        paragraph=row['english'].split('}',1)[1]
        row.update(current_reference=ref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=ref,integrated_hex=value.hex(),
            current_record_index=ref['record_index'],record_index=ref['record_index'],completed_candidate_reference=release['candidate'],
            completed_candidate_sha256=release['candidate_sha256'],current_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),
            current_effective_runtime_English=body.decode('ascii'),current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=body.decode('ascii'),
            current_effective_paragraph=paragraph,registered_runtime_catalog_entry=None,effective_predecessor_macro_paragraph=row['effective_predecessor_paragraph'],
            historical_editorial_decision=row['editorial_decision'],actual_B22_display_fixture_observed=True,offline_only_complete_native_display_verified=False,
            actual_source_event180_selected=False,individual_actual_source_event_activation_not_claimed=True,current_complete_native_display_pending=False,
            registered_integration_pending=False,status='complete-contextual-current-native-references-representative-and-registered-release')
        if row['editorial_decision']=='retain-wording':assert paragraph==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    old_keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};selected={historical_key(r) for r in rows}
    assert len(old_keys)==5912 and len(selected)==11 and not old_keys&selected
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert not fresh['pending_record_keys']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'])==(5912,5912)
    assert ledger['lil_B180_contextual_references_v4817']['source_prose_or_completion_credit_added']==0
    ROOT.mkdir(parents=True);docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    proof_paths=[DOC,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,B181,Path(doc['reference_map']),Path(doc['representative_proof']),
        Path('work/analysis/lil_B180_release_tools_v4822/regression_test_results.json'),Path('work/analysis/lil_B180_retention_v4825/pin_receipt.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in proof_paths};summary=make_summary(release)
    final=dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),
        manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        records=rows,revised=5,retained=6,source_prose_and_completion_credit_added_once=11,previous_B180_objects_uncredited=True,
        all11_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,actual_sampled_B22_display_IDs=sorted(sampled),
        offline_only_display_IDs=[],actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=summary,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[180],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=5,retained_count=6,fresh_revisions=5,fresh_retentions=6,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5923,records_with_source_and_prose_pass=5926,records_with_source_prose_drafts=5926,
        records_revised_and_integrated=3753,retained_wordings_editorially_completed=2170)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:ledger[key]['/data/SC2.DK4']=4070
    key_rows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:fresh[key].extend(deepcopy(key_rows))
    fresh['record_IDs'].extend(r['id'] for r in rows)
    note='5923 contextual rereads integrated;source/prose5926. B181 has10 clean-only uncredited leads;all wider families and earlier wrapping remain open.'
    fresh.update(fresh_pass_records_explicitly_reread=5923,fresh_pass_records_integrated=5923,latest_contextual_manuscript=str(DOC),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
    fresh['reconciled_families'].append(dict(id=FAMILY,records=11,final_review=str(FINAL),new_revisions=5,justified_retentions=6,new_completed_records=11,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=5,retained=6),actual_selected_B180_source_events=[],
        actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=[],new_current_candidate_emulator_runs=2,
        new_explicit_display_fixture_runs=2,new_focused_repeat_runs=2,new_parent_control_runs=1))
    active=ledger['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'];active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4324,completed_route_records=4324,next=NEXT)
    ledger['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',
        file_path='/data/SC2.DK4',blocks=[180],completion_credit_added=11,final_review=str(FINAL),actual_sampled_B22_display_IDs=sorted(sampled),
        actual_source_event180_selected=False,new_emulator_runs=7,full_goal_complete=False))
    ledger['formatting_watchlist']['lil_B180_v4826']=dict(status='all11-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),
        no_glyph_bounds_pagination_or_control_waivers=True,original_RNG_and_effect_differences_disclosed=True,evidence=evidence)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    candidate.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});ledger['current_integrated_candidate']=candidate
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4753']['path']));inventory['next_focus']=NEXT
    inventory['historical_B180_remaining_scope_before_v4826']=deepcopy(inventory['remaining_B180_unreviewed_uncredited'])
    inventory['remaining_B180_unreviewed_uncredited']=dict(physical_speeches=0,typed_choice_command_leads=0,completed_final_review=str(FINAL),not_full_Lil_or_project_denominator=True)
    inventory['lil_B180_completed_v4826']=dict(completed_targets=11,final_review=str(FINAL),registered_candidate=release['candidate'],
        actual_unique_speeches=11,actual_FE_panels=1,source_event180_not_naturally_selected=True)
    inventory['next_B181_clean_context_v4831']=dict(path=str(B181),sha256=sha(B181.read_bytes()),physical_speeches=10,review_credit=0)
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=4324,completed_route_records=4324,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4826']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,
        next_B181_physical_speeches_uncredited=10,later_storylines_shared_town_shop_random_help_prose_open=True,canonical_Maria32_pending_uncredited=True,
        Proof_terminology_consistency_open=True,full_goal_complete=False)
    ledger['lil_B180_completion_v4826']=dict(summary=summary,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=summary
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert len(old_keys|selected)==5923 and old_keys|selected=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    staged=[];planned=ROOT/(lp.name+'.planned');planned.write_bytes(encode_ledger(ledger));assert planned.stat().st_size<100*1024*1024
    staged.append(dict(target=str(lp.resolve()),before_sha256=sha(before_raw),planned=str(planned.resolve()),planned_sha256=sha(planned.read_bytes())))
    section='## V4826:11 B180 reviews completed in cumulative V4821\n\n'+summary+'\n\nFinal review: '+FINAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);text=('# Current editorial handoff - V4826' if i==0 else first)+'\n\n'+section+rest
        planned=ROOT/(p.name+'.planned');data=text.replace('\n','\r\n').encode('utf-8');planned.write_bytes(data)
        staged.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    receipt=dict(checkpoint='V4826',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,
        updated_files={r['target']:r['planned_sha256'] for r in staged},new_source_prose_reviews=11,new_completed_records=11,revised=5,retained=6,
        completed=5923,source_prose=5926,historical_revised=3753,historical_retained=2170,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=562,accepted_layers=114,new_actual_emulator_runs=7,
        actual_unique_speech_panels=11,actual_FE_panels=1,next_B181_uncredited_speeches=10,all_jobs_terminal=True,full_goal_complete=False)
    rp=ROOT/'staged_completion_receipt.json';save(rp,receipt);save(ROOT/'staged_completion.json',dict(files=staged,staged_receipt=str(rp),staged_receipt_sha256=sha(rp.read_bytes()),no_current_ledger_or_document_mutation_yet=True))
    print('B180 completion staged:11 new source/prose and11 completions once;5923 integrated. Independent audit/application pending.')
