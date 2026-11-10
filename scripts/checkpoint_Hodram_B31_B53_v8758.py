"""Audited zero-credit source/prose/native/stored checkpoint; complete goal preserved."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_checkpoint_v8758')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8759')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8747/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B31_B53_frozen_policy_production_progress_pending_atomic_andrelease_v8758'
SCOPE='unfinished_editorial_scope_v8758'
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
 'registered_release':'work/analysis/Hodram_B52_release_v8705/registered_release_verification.json',
 'registered_startup':'work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
}
SUMMARY="""The current verified experimental cumulative ROM is still V8704. Coverage remains 7,234 completed, 7,237 credited source/prose and drafts, 4,489 integrated revisions and 2,745 justified retentions. The three B31/B53 revisions have not been integrated or credited. B52 remains credited exactly once. Main V4701 and the canonical baseline are unchanged. Preserve every ROM, translation, draft, executed producer, proof and failure; no promotion, separate package, pruning, commit or push.

The full objective remains active: all four storylines and earlier translated dialogue, shared town/shop exchanges, random scenes, Help, remaining player-facing prose, all207 names/roles/aliases/custom names and retrospective premature breaks. The route subtotal5,634 is not the full-goal denominator; roughly20,000 remaining candidates is only a planning estimate. Every prior unfinished-scope key, value and lead is preserved. Graphics/all18 plaques and the later older-record technical re-audit remain separate.

Latest approved manuscript is translations/hodram_B31_B53_editorial_manuscript_v5.json; names remain v3. Metadata8748 adds explicit route1/Hodram/SC1/blocks31and53 to unchanged v4 rows. Every approved word, compiled/stored byte, source/current/final reference, individual reason and five gates is retained. B31 restores the speaker's own agency without naming the frightening man; B53 removes the invented bounty while retaining apparent wanted status and gruff caution. All three complete full216px pages use2/4/3 rows, zero QAissues, warnings or waivers, and no authored ordinary breaks or shortening.

Frozen contract8749 binds all approved batch keys, all three complete rows, two scoped name reviews, runtime, source/control/reference/native/actual evidence and734 immutable dependencies. It preserves the original full-width planner, base QA, font metrics, guards, pair phase and FI6/FA9/FO15 with zero source macros. The mutable integrated builder, registry, ledger and retention pins are deliberately excluded from accidental dependency pinning. All prior dependency entries and artifacts remain. Production modules are dk4tool/dialogue/hodram_B31_B53_{profile,layout,plan,names}_v1.py and dk4tool/patch/hodram_B31_B53_{reconstruction,native_guards,native_evidence,references,controls}_v1.py.

Policy8750 passes all three compiler positives, both scoped names and236 genuinely changed-input rejections. Production reconstruction8752 reproduces both independent blocks, the entire archive and whole reviewed ROM;51 changed control/reference/byte defects reject. Independent native8754 recomputes six complete Japanese/stored English pages and two current progressive name planes;12 semantic defects reject. Production references8756 independently parses all18 source/current/final commands, binds three disjoint canonical references and every inverse/unowned byte;20 defects reject without changing the original NDS object or its bytes. Native controls8757 independently executes three dispatches, four relative sites20cases, one unforced query, eight paired opaque structural decodes,50 normal-end cases,50 caller fragments and four EV1 getters;12 defects reject. These331 negative cases keep every frozen/trusted guard active and every protected file/ROM/registry/ledger unchanged.

The control reader uses the exact own-V8704 captain1 snapshot and original adapters. It reuses the already verified native glyph and whole-reference inputs by exact hashes rather than rerunning those stages. Normal ends preserve the existing parser-result second word independently of interpreter r3; the source's50 seeded cases and50 caller fragments preserve both channels. Keep the stopped8742 wrong-channel audit, qualified8742b reader, source-name8733 one-row failure and8733b19-glyph qualification, and formatting8745 receipt-path failure with8745b qualification. No original producer or artifact is rewritten.

Actual coverage is unchanged from8744: four terminal/reaped initialized whole-block cold boots,24,004 frames,76 complete body/name holds and four page occurrences. Long B31R0018 and B53R0007 are observed in both languages. Short B31R0013 remains offline-only; no original predicate or flag was forced to visit it. Source52->31->53 prerequisites do not establish a continuous conversation, original location, earned chronology, either B52 choice effect or the frightening man's identity. Opaque6311/6000/633F/623F/A000 are preserved without invented effect semantics.

B31 returns[0,1] at4016 in both languages; B53 returns[0,0] at4013 with separate interpreter mode1. Only the three documented decoded-length differences remain. Command duration, UI requests, boundary RNG and following commands match. All five sampled final components, whole actors, captain1, raw calendar and seed3325064553 match;68 later RGB pairs match through6001 frames. These remain bounded fixture observations, not natural activation, original eligibility/location, full catalogue UI, custom names, every-frame causality, broad future simulation, full-route or hardware proof. Source text fixtures use current English names/UI/code/font and eight original initializers34bytes. All earlier B52/B51/B50/B49/Gerhard/Rafael/Hodram/Lil limits remain intact.

Actor34 retention preserves the actual clean progressive/full-getter components and Fazul middle field; exact current mixed-width Ｆ storage remains. The source full getter's19th glyph wraps in the explicit216px literal test, with all characters complete. Actual progressive headers34/113 are verified; wider catalogue UI, all207 entries and wider Port Worker contexts remain open. Five existing research ROMs remain pinned; this turn creates no ROM or emulator capture.

Continue from verifiedV8759/currentV8704 without replaying completed source, prose, layout, native, independent reconstruction, name, actual or production checks. Remaining B31/B53 work: production loader/census, actual-scene and comparison evidence readers with meaningful changed-input tests; one whole-NDS atomic commit in both supported lifecycles and wrong-memory zero-commit checks; shared registered cumulative build, exact clean-input patch and own startup; then exactly three once-only completion decisions. Keep the full editorial objective and every previous artifact."""
NEXT='Finish B31/B53 production loader/census, actual andcomparison readers, then whole-NDS atomic validation/shared registered cumulative integration/exact clean-input patch/own startup andthree once-only credits. Latest immutable manuscriptv5/namesv3/contractv1;331 changed-input rejections pass. Keep actual shortB31 andfullcatalogue UI scope honest andall full-goal leads active.'

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
        pending=dict(status='three-reviewed-revisions-frozen-policy-reconstruction-native-references-controls-pass-production-loaders-actual-comparison-atomic-registered-pending',file_path='/data/SC1.DK4',blocks=[31,53],
            physical_speeches=3,typed_choice_labels=0,proposed_revisions=3,justified_retentions=0,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,
            records_with_exact_source_current_compiled_andstored_references=deepcopy(records),stored_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True,all_formatting_gates_false=False,all_five_individual_gates_true=True,full_name_resolution=deepcopy(data['names']['full_name_resolution']),
            source_commands=18,source_relative_sites=4,source_rawqueries=1,opaque_controls=8,source_seeded_end_cases=50,source_relative_cases=20,current_relative_cases=20,relocated_relative_cases=20,
            source_dispatches=3,current_dispatches=3,stored_dispatches=3,source_alignment_cases=12,logical_alignment_cases=12,compiled_alignment_cases=12,stored_exact_reused_alignment_cases=12,
            complete_source_pages=3,complete_English_pages=3,automatic_fullwidth_px=216,QAissues=0,warnings=0,waivers=0,
            actual_B31_B53_emulator_runs=4,actual_B31_B53_frames=24004,actual_body_andname_holds=76,actual_unique_text_IDs=['DK4_MES_B31_R0018','DK4_MES_B53_R0007'],offline_only_text_IDs=['DK4_MES_B31_R0013'],registered_integration_andcredit_pending=True,source_positions_credited=0,new_credit=0,full_goal_complete=False)
        descriptor=old[prior['unfinished_scope']];assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
        scope=deepcopy(read(descriptor['path']));assert KEY not in scope
        ROOT.mkdir(parents=True);scope[KEY]=deepcopy(pending);scope['latest_next_focus_v8758']=NEXT
        scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,scopepath,Path(__file__),*map(Path,PROOFS.values())]}
        put('latest_checkpoint',SUMMARY+'\n\n'+NEXT)
        put(SCOPE,dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),all_prior_scope_keys_values_history_andfull_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,new_uncredited_contextual_revisions=3,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put(KEY,dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,goal_turn_classification='progress',
            prior_goal_turn_was_concrete_independent_names_actual_andformat_progress=True,current_turn_frozen_policy_andindependent_production_progress=True,
            prior_clean_gloss_checkpoint_retained_as_historical_state=prior['pending_source_batch'],all_new_jobs_terminal=True))
        new[KEY]['inverse_operations']=deepcopy(ops)
        assert inverse(new,ops)==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8758; V8704 current\n\n' if name=='editorial_handoff_current.md' else '')
            prefix+='## V8758: B31/B53 agency and bounty revisions; frozen policy and production native/reference/control checks pass;atomic/registered work remains\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
            targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        protected=[Path(prior[k]) for k in ['candidate','patch','manifest']]+[Path('translations/release_stack.json'),Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds'),Path('translations/rom_retention_pins.json'),Path(data['reference']['research_ROM'])]+[Path(f['research_ROM']) for f in data['fixtures']['fixtures']]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},inverse_operations=ops,unchanged_counters=COUNTS,new_credit=0,full_goal_complete=False))
        print('V8758 staged:three uncredited revisions/native/stored proof,six exact targets. Inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert inverse(new,plan['inverse_operations'])==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes())==row['planned_sha256'] and sha(Path(row['target']).read_bytes())==row['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in {**plan['evidence'],**plan['protected']}.items():assert sha(Path(path).read_bytes())==digest
        descriptor=old[prior['unfinished_scope']];oldscope=read(descriptor['path']);newscope=read(new[SCOPE]['path'])
        assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={KEY,'latest_next_focus_v8758'}
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            for i,row in enumerate(plan['files'][1:],start=1):
                original=gzip.decompress((ROOT/f'{i:02d}.before.gz').read_bytes());assert sha(original)==row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),every_prior_ledger_value_family_record_counter_andcandidate_recovers_exactly=True,
                every_prior_scope_key_andvalue_anddocument_byte_preserved=True,protected_ROMs_patch_registry_unchanged=True,new_credit=0))
            print('V8758 audit:whole oldledger inverse,allscope keys,allold documentbytes,counters/candidate/registry/ROMs exact.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target,planned=Path(row['target']),Path(row['planned']);assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:stream.write(planned.read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(target.read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_registry_orcompletion_counter_change=True,new_credit=0,full_goal_complete=False))
            print('V8758 applied;currentV8704 andall7234completed unchanged;fullgoalactive.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,next_clean_exchange_not_selected=False,
                Hodram_B31_B53_frozen_policy_production_checkpoint=deepcopy(new[KEY]),new_uncredited_source_positions=3,physical_speeches_pending=3,typed_choice_labels_pending=0,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0,total_B31_B53_actual_runs=4,total_B31_B53_actual_frames=24004,all_new_native_jobs_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8759/currentV8704:three approved revisions/frozenpolicy/production reconstruction-native-references-controls pass;remaining readers/atomic/registered pending;zero completion credit;fullgoalactive.')
