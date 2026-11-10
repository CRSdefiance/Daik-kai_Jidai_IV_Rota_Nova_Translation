"""Audited zero-credit source/prose/native/stored checkpoint; complete goal preserved."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_checkpoint_v8774')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8775')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8759/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B31_B53_allproduction_atomic_shared_pass_pending_registered_release_v8774'
SCOPE='unfinished_editorial_scope_v8774'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
COUNTS=[7234,7237,7237,4489,2745]
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS as ACTUAL_PROOFS
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import validate_approved_batch
from dk4tool.dialogue.hodram_B31_B53_names_v1 import validate_scoped_names
PROOFS={**ACTUAL_PROOFS,
 'actual_review':'work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json',
 'formatting':'work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json',
 'manuscript':'translations/hodram_B31_B53_editorial_manuscript_v5.json',
 'names':'translations/hodram_B31_B53_speaker_name_review_v3.json',
 'metadata':'work/analysis/Hodram_B31_B53_metadata_v8748/explicit_route_binding.json',
 'frozen':'work/analysis/Hodram_B31_B53_policy_v8749/frozen_contract.json',
 'contract':'translations/hodram_B31_B53_native_contract_v1.json',
 'policy_validation':'work/analysis/Hodram_B31_B53_policy_validation_v8750/policy_validation.json',
 'production_reconstruction':'work/analysis/Hodram_B31_B53_reconstruction_validation_v8752/independent_reconstruction_validation.json',
 'production_native':'work/analysis/Hodram_B31_B53_native_validation_v8754/independent_native_validation.json',
 'production_references':'work/analysis/Hodram_B31_B53_reference_validation_v8756/independent_reference_validation.json',
 'production_controls':'work/analysis/Hodram_B31_B53_controls_validation_v8757/independent_controls_validation.json',
 'production_loaders':'work/analysis/Hodram_B31_B53_loader_validation_v8761/independent_loader_validation.json',
 'production_actual':'work/analysis/Hodram_B31_B53_actual_validation_v8764/independent_actual_validation.json',
 'production_comparison':'work/analysis/Hodram_B31_B53_comparison_validation_v8766/independent_comparison_validation.json',
 'release_seal':'work/analysis/Hodram_B31_B53_release_seal_v8769/reference_seal.json',
 'release_config':'translations/hodram_B31_B53_editorial_release_v1.json',
 'atomic_positive':'work/analysis/Hodram_B31_B53_atomic_positive_v8770/atomic_positive.json',
 'wrong_memory':'work/analysis/Hodram_B31_B53_wrong_memory_v8771/wrong_memory_rejections.json',
 'semantic_atomic':'work/analysis/Hodram_B31_B53_atomic_challenges_v8772/semantic_rejections.json',
 'shared_extension':'work/analysis/Hodram_B31_B53_shared_extension_v8773c/shared_extension_validation.json',
 'registered_release':'work/analysis/Hodram_B52_release_v8705/registered_release_verification.json',
 'registered_startup':'work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
}
SUMMARY="""The verified experimental cumulative ROM remains V8704. Coverage remains 7,234 completed, 7,237 credited source/prose and drafts, 4,489 integrated revisions and 2,745 justified retentions. B31/B53's three revisions remain unintegrated and uncredited; B52 stays credited exactly once. Main V4701, canonical baseline and every prior ROM, translation, draft, producer, proof and failure are preserved. No new ROM, emulator capture, promotion, separate package, pruning, commit or push occurs in this checkpoint.

The full all-four-storyline, earlier translated dialogue, shared town/shop, random, Help, remaining player-facing prose, all207 names/roles/aliases/custom names and retrospective premature-break objective remains active. The route subtotal5,634 is not the full-goal denominator; roughly20,000 remaining candidates is only a planning estimate. Every old unfinished-scope key/value/lead and document byte remains preserved. Graphics/all18 plaques and the later older-record technical re-audit stay separate.

Reuse latest approved manuscriptv5/namesv3/nativecontractv1 and all completed clean-first source/context/prose/logical/compiled/stored/name/actual work. The three revisions restore B31 speaker agency without identifying the unnamed frightening man and remove B53's invented bounty while preserving apparent wanted status, culmination and gruff caution. The exact wording, source/current/final references, all five individual gates, full216px automatic pages2/4/3rows and zero warnings/waivers remain unchanged. No ordinary breaks, padding, shortening, viewport, font or QA weakening is introduced.

All independent production readers now pass. Policy8750 has236 changed-input rejections; reconstruction8752 has51; native8754 has12; references8756 has20; controls8757 has12; loaders8761 has8; actual8764 has13; comparison8766 has12. These364 production cases retain frozen/trusted guards. Loader/census independently binds325 loads,650 parent modes,326 original actions, both event entries and a fresh shipped-code census. The actual reader independently reconstructs all four full fixture ROM inverses, original initializer prefix, complete resident scripts, read-only traces, inputs, body/name holds and returns. The comparison reader recomputes all four saved final snapshots, five components, whole actors, captain1, raw calendar/RNG and68 later full RGB pairs. Completed native/reference models are hydrated by exact prior hashes for reader tests; no earlier producer or gameplay run is replayed.

The seal8769 and release configuration translations/hodram_B31_B53_editorial_release_v1.json preserve all734 frozen dependencies and every previous B52 release dependency,1424 total. Production planner dk4tool/patch/hodram_B31_B53_editorial_v2.py passes both direct-current and canonical-source/full-current-memory lifecycles8770. Each commits one complete NDS object only after every gate, yields exactly the reviewed research ROM and three disjoint record IDs, and preserves the original object/files/components/serialized bytes until commit. All three genuinely wrong-memory cases8771 reject with every guard active and zero commits. Four representative early editorial, middle reference, late actual and final scope defects8772 reject with whole inputs unchanged; only the outer digest layer is bypassed for those in-memory evidence injections, while frozen/native/editorial/semantic guards remain active. The real shared-hook extension8773 passes with one final whole-object commit; a wrong late target hash rejects with zero commits. Six unchanged generic shared-framework cases are reused by exact framework source hash, not replayed. Stable lowercase wrapper is dk4tool/patch/hodram_b31_b53_extension_v2.py. These are disposable in-memory checks, not a disk ROM or completion credit.

Shared reader8773 completed its positive case before stopping on a Windows-versus-literal path key. Successor preparation8773b stopped on a duplicate separator before creating its target. Qualified8773c reuses the exact completed positive by hash and runs only the missing late-target failure, preserving all original guards and stopped files. No completed positive, native or actual capture is replayed.

Preserve the stopped seal preparer8769: it asserted a nonexistent current_ROM_sha256 context key before writing any seal/config. Qualified8769b binds the existing candidate_sha256 field. Prepared atomicv1 remains preserved; v2 qualifies the existing four-sheet approval key before any atomic execution. Neither correction changes evidence, prose, ROMs or guards. Keep earlier stopped8742 wrong result-channel audit, qualified8742b, source-name8733 one-row failure/8733b19-glyph qualification and formatting8745 receipt failure/8745b. No executed producer is overwritten.

Actual coverage stays four terminal/reaped initialized whole-block cold boots24,004frames,76 complete body/name holds and four page occurrences. Long B31R0018 and B53R0007 are observed in both languages; short B31R0013 remains offline-only and its condition is never forced. B31 returns[0,1] at4016; B53 returns[0,0] at4013 while separate interpreter mode is1. The normal end preserves the prior parser-result second word independently of r3. Only three decoded-length differences occur; command duration, UI requests, boundary RNG and following commands match. All five sampled final components/whole actors/captain1/raw calendar/final seed3325064553 match, as do68 later RGB pairs through6001frames. Source52->31->53 prerequisites do not establish a continuous conversation, original location, earned chronology, B52 choice effects or the unnamed man's identity. Opaque controls stay structural without invented effects. No natural activation, full catalogue UI, all207/custom names, every-frame causality, future simulation, full-route or hardware proof is claimed. Earlier B52/B51/B50/B49/Gerhard/Rafael/Hodram/Lil limitations remain intact.

Actor34 source progressive/full getters include the actual Fazul middle field. Current sourced components/order and mixed-width storage remain unchanged. The original full getter's19th glyph wraps in the literal216px test with all characters complete; actual progressive headers34/113 are verified. Wider catalogue UI, Port Worker contexts, all207 names and custom names remain open. All five research ROMs and every earlier ROM remain pinned and preserved.

Next bind the passed atomic/shared proofs into an additive final release closure, append this extension after unchanged B52 in a new registered experimental profile, use the sole cumulative builder, verify exact clean-input patch reconstruction and the new ROM's own startup, then credit exactly three disjoint source decisions once. Reuse completed production/atomic/gameplay work; no live builder change or repeat of old prefix compatibility tests is needed merely to append the existing shared hook. Keep the full editorial objective intact."""
NEXT='Bind completed B31/B53 atomic/shared proofs into the additive release closure; register after unchanged B52; sole cumulative builder/exact clean-input patch/own startup; then exactly three once-only credits. CurrentV8704/7234completed unchanged; full goal active.'

def inverse(value,operations):
    result=deepcopy(value)
    for op in reversed(operations):
        if op['existed']:result[op['key']]=deepcopy(op['before'])
        else:del result[op['key']]
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7234 and prior['candidate_sha256']==data['manuscript']['current_ROM_sha256']==data['registered_release']['candidate_sha256']
    for k,p in [('candidate','candidate_sha256'),('patch','patch_sha256'),('manifest',None)]:
        path=Path(prior[k]);assert path.exists()
        if p:assert sha(path.read_bytes())==prior[p]
    assert data['source_controls']['complete_source_commands']==18 and data['source_controls']['normal_seeded_end_cases']==50
    assert data['formatting']['all3_five_gates_true'] and data['formatting']['standard_natural_dialogue_v2_validation_pass']
    assert data['metadata']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and data['metadata']['predecessor_sha256']==data['formatting']['manuscript_sha256']
    assert data['formatting']['names_sha256']==sha(Path(PROOFS['names']).read_bytes())
    validate_approved_batch(data['manuscript']);validate_scoped_names(data['names'])
    assert data['frozen']['contract_sha256']==sha(Path(PROOFS['contract']).read_bytes()) and data['frozen']['dependency_count']==734
    assert data['frozen']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())
    assert [data[k]['negative_count'] for k in ['policy_validation','production_reconstruction','production_native','production_references','production_controls']]==[236,51,12,20,12]
    assert data['production_native']['native_summary']['native_body_pages_recomputed']==6
    assert data['production_references']['positive_entire_archive_whole_reference_ROM_all323_unownedblocks_files_components_andallinverses']
    assert data['production_controls']['native_control_summary']['normal_seeded_ends']==50 and data['production_controls']['native_control_summary']['original_result_channel_cases']==50
    assert all(all(r['review'].values()) for r in data['manuscript']['records']) and not data['plan']['failures'] and all(not r['base_QA']['issues'] for r in data['plan']['records'])
    assert (data['actual_review']['total_runs'],data['actual_review']['total_frames'],data['actual_review']['total_holds'])==(4,24004,76)
    assert data['actual_review']['offline_only_text_IDs']==['DK4_MES_B31_R0013'] and data['actual_review']['all_four_sheets_directly_viewed']
    assert data['independent']['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert data['loaders']['fresh_native_whole_loads_andcache_hits']==325 and data['loaders']['fresh_initial_parent_modes']==650
    assert data['relocation']['other323_blocks_byte_exact'] and data['relocation']['whole_inmemory_NDS_inverse_andall_other_files_components_exact']
    assert data['stored']['complete3stored_first_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    assert data['registered_startup']['viewed'] and data['registered_startup']['whole_actors_equal']
    assert [data[k]['negative_count'] for k in ['production_loaders','production_actual','production_comparison']]==[8,13,12]
    assert data['production_actual']['actual_summary']['complete_actual_holds']==76 and data['production_comparison']['comparison_summary']['later_full_RGB_pairs_recomputed']==68
    assert data['atomic_positive']['positive_lifecycles']==2 and data['atomic_positive']['one_complete_NDS_commit_percase']
    assert data['atomic_positive']['cases'][0]['report']==data['atomic_positive']['cases'][1]['report']
    assert data['wrong_memory']['negative_count']==3 and data['wrong_memory']['no_digest_orsemantic_bypass']
    assert data['semantic_atomic']['negative_count']==4 and data['semantic_atomic']['zero_commits_andwhole_original_input_object_exact_forall_failures']
    assert data['shared_extension']['positive_lifecycles']==1 and data['shared_extension']['negative_count']==1 and data['shared_extension']['exact_unchanged_framework_six_previous_cases_reused_by_source_hash']
    assert len(data['release_config']['dependencies'])==1424
    from dk4tool.patch.hodram_B31_B53_editorial_v2 import check_dependencies
    check_dependencies(data['release_config'])
    for key in ['production_loaders','production_actual','production_comparison','atomic_positive','wrong_memory','shared_extension']:
        for path,digest in data[key]['evidence'].items():assert sha(Path(path).read_bytes())==digest,(key,path)
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and [old[k] for k in COUNTERS]==COUNTS and old['goal_status']=='active' and not old['full_goal_complete']
        completed={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};assert len(completed)==7234
        records=data['manuscript']['records'];assert not completed&{historical_key(r) for r in records} and len(records)==3
        new=deepcopy(old);ops=[]
        def put(k,v):
            ops.append(dict(key=k,existed=k in new,before=deepcopy(new.get(k))));new[k]=deepcopy(v)
        pending=dict(status='three-approved-revisions-all-production-readers-both-atomic-lifecycles-wrongmemory-semantic-shared-pass-registered-release-pending',file_path='/data/SC1.DK4',blocks=[31,53],
            physical_speeches=3,typed_choice_labels=0,proposed_revisions=3,justified_retentions=0,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,
            records_with_exact_source_current_compiled_andstored_references=deepcopy(records),stored_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True,all_formatting_gates_false=False,all_five_individual_gates_true=True,full_name_resolution=deepcopy(data['names']['full_name_resolution']),
            source_commands=18,source_relative_sites=4,source_rawqueries=1,opaque_controls=8,source_seeded_end_cases=50,source_relative_cases=20,current_relative_cases=20,relocated_relative_cases=20,
            source_dispatches=3,current_dispatches=3,stored_dispatches=3,source_alignment_cases=12,logical_alignment_cases=12,compiled_alignment_cases=12,stored_exact_reused_alignment_cases=12,
            complete_source_pages=3,complete_English_pages=3,automatic_fullwidth_px=216,QAissues=0,warnings=0,waivers=0,
            actual_B31_B53_emulator_runs=4,actual_B31_B53_frames=24004,actual_body_andname_holds=76,actual_unique_text_IDs=['DK4_MES_B31_R0018','DK4_MES_B53_R0007'],offline_only_text_IDs=['DK4_MES_B31_R0013'],registered_integration_andcredit_pending=True,source_positions_credited=0,new_credit=0,full_goal_complete=False)
        descriptor=old[prior['unfinished_scope']];assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
        scope=deepcopy(read(descriptor['path']));assert KEY not in scope
        ROOT.mkdir(parents=True);scope[KEY]=deepcopy(pending);scope['latest_next_focus_v8774']=NEXT
        scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,scopepath,Path(__file__),*map(Path,PROOFS.values())]}
        put('latest_checkpoint',SUMMARY+'\n\n'+NEXT)
        put(SCOPE,dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),all_prior_scope_keys_values_history_andfull_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,new_uncredited_contextual_revisions=3,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put(KEY,dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,goal_turn_classification='progress',
            prior_count_question_turn_was_status_only_no_progress=True,current_turn_revalidated_current_handoff_andcompleted_production_atomic_andshared_progress=True,
            prior_clean_gloss_checkpoint_retained_as_historical_state=prior['pending_source_batch'],all_new_jobs_terminal=True))
        new[KEY]['inverse_operations']=deepcopy(ops)
        assert inverse(new,ops)==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8774; V8704 current\n\n' if name=='editorial_handoff_current.md' else '')
            prefix+='## V8774: B31/B53 agency and bounty revisions; all production readers, atomic lifecycles and shared hook pass; registered release remains\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
            targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        protected=[Path(prior[k]) for k in ['candidate','patch','manifest']]+[Path('translations/release_stack.json'),Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds'),Path('translations/rom_retention_pins.json'),Path(data['reference']['research_ROM'])]+[Path(f['research_ROM']) for f in data['fixtures']['fixtures']]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},inverse_operations=ops,unchanged_counters=COUNTS,new_credit=0,full_goal_complete=False))
        print('V8774 staged:three uncredited revisions/native/stored proof,six exact targets. Inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert inverse(new,plan['inverse_operations'])==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes())==row['planned_sha256'] and sha(Path(row['target']).read_bytes())==row['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in {**plan['evidence'],**plan['protected']}.items():assert sha(Path(path).read_bytes())==digest
        descriptor=old[prior['unfinished_scope']];oldscope=read(descriptor['path']);newscope=read(new[SCOPE]['path'])
        assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={KEY,'latest_next_focus_v8774'}
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            for i,row in enumerate(plan['files'][1:],start=1):
                original=gzip.decompress((ROOT/f'{i:02d}.before.gz').read_bytes());assert sha(original)==row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),every_prior_ledger_value_family_record_counter_andcandidate_recovers_exactly=True,
                every_prior_scope_key_andvalue_anddocument_byte_preserved=True,protected_ROMs_patch_registry_unchanged=True,new_credit=0))
            print('V8774 audit:whole oldledger inverse,allscope keys,allold documentbytes,counters/candidate/registry/ROMs exact.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target,planned=Path(row['target']),Path(row['planned']);assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:stream.write(planned.read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(target.read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_registry_orcompletion_counter_change=True,new_credit=0,full_goal_complete=False))
            print('V8774 applied;currentV8704 andall7234completed unchanged;fullgoalactive.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,next_clean_exchange_not_selected=False,
                Hodram_B31_B53_complete_production_atomic_shared_checkpoint=deepcopy(new[KEY]),new_uncredited_source_positions=3,physical_speeches_pending=3,typed_choice_labels_pending=0,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0,total_B31_B53_actual_runs=4,total_B31_B53_actual_frames=24004,all_new_native_jobs_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8775/currentV8704:three approved revisions/all production readers andatomic/shared pass;registered release pending;zero completion credit;fullgoalactive.')
