"""Checkpoint15 contextual decisions andnative/stored proofs;no completion credit before actual/release."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B46_v7969 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_native_stored_checkpoint_v7992')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7993')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7975/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/rafael_B47_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B47_speaker_name_review_v2.json')
KEY='Rafael_SC0B47_source_prose_native_stored_pending_actual_release_v7992'
OLD_KEY='Rafael_SC0B47_clean_source_gloss_pending_native_current_v7974'
SCOPE='unfinished_editorial_scope_v7992'
WRAP='retrospective_inherited_weak_before_rows_wrap_lead_v7992'
PROOFS={
    'names':'work/analysis/Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',
    'source_controls':'work/analysis/Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json',
    'source_paths':'work/analysis/Rafael_B47_source_paths_v7978/625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json',
    'source_gloss':'work/analysis/Rafael_B47_branch_gloss_v7979/15_fresh_glosses_six_source_paths_names_bound_before_current_English.json',
    'current':'work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json',
    'effective':'work/analysis/Rafael_B47_effective_v7981/all15_effective_English_templates30_original_progressive_dispatches.json',
    'prose':'work/analysis/Rafael_B47_prose_v7982/15_contextual_decisions_six_complete_path_reviews_eight_revisions_seven_retentions.json',
    'logical':'work/analysis/Rafael_B47_logical_v7983/15_logical_paragraphs60_original_native_progressive_alignments.json',
    'plan':'work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json',
    'pages':'work/analysis/Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json',
    'source_name_pages':'work/analysis/Rafael_B47_source_name_planes_v7986/15_complete_source_pages4_names16_literal_alignments_all_progressive.json',
    'native_review':'work/analysis/Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json',
    'relocation':'work/analysis/Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json',
    'stored':'work/analysis/Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json',
    'final_controls':'work/analysis/Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json',
}
SUMMARY="""Current registered cumulative ROM remains V7964; main V4701 is unchanged. B46 is complete and credited. Counts remain 6,976 completed records, 6,979 source/prose records and drafts, 4,361 integrated wording revisions and 2,615 retentions; SC0 173 and route subset 5,376. All 635 batches, 114 accepted layers, 18 release checks, 110 regressions, exact clean-input patch reconstruction and own-current startup evidence remain verified. B47 has no completion or source/prose credit yet and is not integrated.

B47 now has a full contextual draft at translations/rafael_B47_editorial_manuscript_v2.json: 15 speeches, eight revisions and seven individually justified retentions. The complete clean Japanese and 72-speech B37 prerequisite context, fresh glosses, names and native branch compositions preceded current English. All 15 effective current templates are bound through 30 original dispatches; none has a catalogue replacement. Review covers six complete text paths rather than one flattened transcript. Preserve guarded relief about passage, the approximate eastern-half Ottoman/Pasha domain and conditional danger, the Mediterranean conclusion, caution about trading contracts, qualified navigator recruitment, ship and personal preparation, brief overwhelm and renewed resolve. All four source/context/localization/naturalness gates pass; final formatting gates remain false pending stored/actual/release completion.

Original source identities are Rafael Castor, Janus Pasar, Claudio Manaus and Julio Erneco. Eight native name getters, clean/current fields and voice classes 2/0/4/5 pass in own-current captain0 context. Janus's パサー/Pasar is distinct from パシャ/Pasha in the force references; no political association or rank follows from similar spellings. Valdes, Pasha and Hayreddin have scoped surname-component retentions only. Their full names and middle fields are not newly approved: Pedro Valdes's current middleデ and Hayreddin's sourceファーズル/current absent middle remain wider207-name leads. Four complete style11 nameplanes and 16 literal alignments pass and were viewed. Full catalogue UI, custom player names and actual B47 nameplates remain pending.

The complete 48-command source block contains 24 relative sites and six8000 raw predicates, plus61FF, oneA000 effect and the normal four-byte end. Source and relocated relative cases each cover all five structural inputs: 120 cases apiece. Raw predicates are not generally normalized to booleans. Composing four unique operands over five result values yields625 structural compositions and six distinct text paths of5,7,11 or14 speeches. R63 (Ottoman-only) and R70 (Spanish Valdes plus Ottoman Pasha) are exclusive. Janus's R17/R92/R122 share04FE0030; R92 also requires the main advice block. The unforced opening values compose11 speeches withR70 andwithout Janus, not actual B47 gameplay or proof of natural event activation. Original EV0 event47/action48 requires37;37 requires36. The independently gated A000 effect is preserved without inventing its plot semantics.

Native logical processing passes60 alignments; all15 compiled paragraphs produce16 complete native pages with independent full-glyph masks, exact bounds, consumption and original216x64/four-row geometry. R53 needs two pages without shortening its meaning: the automatic turn follows territory., then the second page contains the full conditional warning on two balanced rows. No new runtime page control, font or viewport is authored. All five source00 actors remain in their complete six-byte preambles, separate from the unchanged body-NUL guard. All source macros are zero; FI6/FA6/FO10 defaults remain measured and none are added.

The early-wrap pass caught an inherited planner preference that added short rows solely to avoid soft word boundaries. Source-locked B47 successors now prioritize orphan avoidance, sentence boundaries at required page turns, fewer added rows, soft boundary preferences and balanced final rows. R5 andR63 move from four to three rows with every word unchanged. Two original weak-line-ending warnings remain verbatim: R5 line2 to/get andR63 line2 with/Pasha's. Each has an exact source/text/compiled-plan/line-bound exception and written reason; no global warning or native guard is removed. Six row-count infos and individual reasons are preserved. All16 body pages and four names were directly viewed in four sheets. Earlier compilers and plans remain unchanged. This creates a retrospective lead for other inherited weak-before-row decisions; do not mechanically minimize rows or override an earlier justified phrase-preserving retention.

Research-only block reconstruction changes B47 from1284stored/logical/tail0 to1344stored/logical/tail0. All15 complete preambles,48 commands,24 nested relative spans, six exact predicate operands,61FF,A000 andthe complete end remain. Both full clean/predecessor block inverses and the entire predecessor archive inverse pass;342 otherSC0 blocks are exact. Eight zero-ink parity tails pass32 fresh alignments and seven exact bodies reuse28 alignments. All16 stored planes equal the viewed pages with no blank or extra pages. Final15 body/actor/voice dispatches, six relocated raw predicates with scratch restoration,120 relocated branch cases and25 seeded normal value-carry ends pass. The research archive is work/analysis/Rafael_B47_relocation_v7989/SC0_B47_RESEARCH_ONLY.DK4; it is not a ROM or registered release.

No new B47 emulator job or ROM was created this turn. Actual selected paths, headers, normal carry and especially R53's page turn remain untested. Source/target timing, RNG and later simulation equality have not been measured forB47. Preserve the actual measured B46 differences as scoped historical evidence, without treating them as B47 results. The V7984 import-time QA-source error and V7989 duplicated-path error stopped before output-family creation; their failed producers and source-locked successors remain. No ROM, registry, pins, main promotion, pruning, commit or push changed."""
NEXT="""Continue from verifiedV7993/current registeredV7964 using translations/rafael_B47_editorial_manuscript_v2.json and translations/rafael_B47_speaker_name_review_v2.json. Reuse all completed source/context/identity/branch/current/effective/prose/native/stored/inverse checks unless a new change or concrete risk requires more testing. The final automatic plan is work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json, not the earlier b/c/d plans. Keep the two exact warning exceptions, all six infos, sentence-aware R53 page turn and untouched English. All15 formatting gates remain false.

Next construct and pin a full isolated research reference from V7964 plus the exact reviewed SC0 archive; prove all other files/components and342 blocks unchanged. Bind all343 native load/cache paths and686 parent modes, all48 command maps,24 relocated relative operands, original EV0 block entry and shipped callers. Use the current own-Rafael input at work/analysis/current_V7964_Rafael_native_v7967/current_native_input.json. Other routes' earlier contexts remain historical.

Use representative source/English actual tests and focused risk coverage. Preserve the entire B47 block and every original setup, predicate, effect, branch and end in any disclosed opening-entry fixture. Do not force RAM, seed, conditions, roles, roster or interpreter results. The current opening results suggest11 speeches; observe the actual selection rather than forcing that expectation. The key new display risk is R53's original four-row pagination: verify both complete English pages, ordinary input turn, leading/trailing characters, complete nameplate and return to the following dialogue. Native-only Janus/R63 and other conditional content may remain explicitly offline if no concrete distinct display risk warrants another scene; exhaustive natural visits are not required. Distinguish initialized fixtures, native result compositions and natural event activation.

Audit actual normal value carry, all selected command results/UI requests, complete body/header masks, transitions and measured timing/RNG/later components/calendar/RGB with honest limits. The extra English page may alter waits; do not retime inputs or force random state to hide differences. Only then approve final formatting and freeze the exact source-bound15-record policy, R53-only two-page capacity and both narrow QA exceptions. Challenge real source/prose/profile/guard/consumer/runtime/reference/waiver changes, implement atomic reconstruction before one final files-list commit, and reject corrupted proofs independently of dependency hashes. Integrate after necessary checks through the complete registered stack afterV7964 and an exact clean-input patch. Credit15 objects/eight revisions/seven retentions once only after registered integration and appropriate startup: expected totals6991 completed/6994 source-prose anddrafts/4369 revisions/2622 retentions,SC0 188,route subset5391. Current totals stay6976/6979/4361/2615.

Keep the full objective across allfour storylines, earlier translated dialogue, broad practical shared shop/town/random capture, Help and remaining prose, all207 names/roles/aliases and premature wrapping. Preserve all earlier inventories, twelve contraction/question-tag wrap leads, unscanned records beyond558 plans and the new inherited weak-before-row lead. Preserve Janus Pasar versus Pasha identity distinctions when revisiting the historical JanusPasha counterpart queue; no global replacement is authorized by these scoped findings. Retain all older item/counterpart/display leads, Sailor151-159 versusRetainer consumer distinctions and uncredited incidental B127/Sailor captures. Graphics/all18 plaques and the later older-record technical re-audit remain separate, including normal-end value carry,B35R65's source-only nineteenth cell and every prior measured timing/highlight/RNG/component/calendar/RGB limit. Preserve every ROM, translation, draft, failure, executed producer and proof. MainV4701 remains unchanged; no separate unified package, promotion, pruning, commit orpush."""

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==6976 and prior['manifest_batches']==635 and prior['Rafael_B46_completed_once']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==15 and doc['revisions']==8 and doc['retentions']==7
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert data['native_review']['manuscript_sha256']==sha(DOC.read_bytes()) and data['native_review']['names_sha256']==sha(NAMES.read_bytes())
    assert data['native_review']['native_page_count']==16 and data['native_review']['original_row_count_infos']==6
    assert len(data['native_review']['preserved_warning_exceptions'])==2 and len(names['records'])==4
    assert all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in data['native_review']['directly_viewed_sheets'])
    assert len(data['relocation']['groups'][0]['command_map'])==48 and data['relocation']['relocated_native_skip_cases']==120
    assert data['relocation']['complete_clean_source_block_reconstructed_exactly'] and data['relocation']['all_full_predecessor_archive_bytes_reconstructed_exactly']
    assert data['stored']['fresh_native_alignment_cases']==32 and data['stored']['exact_reused_native_alignment_cases']==28
    assert len(data['final_controls']['final_dispatches'])==15 and len(data['final_controls']['relocated_predicates'])==6 and len(data['final_controls']['normal_seeded_ends'])==25
    return prior,data
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER and old['goal_status']=='active' and not old['full_goal_complete']
        assert KEY not in old and SCOPE not in old and OLD_KEY in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='15-source-context-prose-native-stored-approved-pending-actual-policy-atomic-registered-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            file_path='/data/SC0.DK4',block=47,objects=15,revisions=8,retentions=7,current_English_unread=False,
            exact_source_current_compiled_stored_references_in_manuscript_andproofs=True,
            all15_final_formatting_gates_false=True,native_pages=16,source_speech_objects=15,source_commands=48,
            source_andrelocated_relative_sites=24,source_andrelocated_relative_cases_each=120,
            native_only_result_compositions=625,distinct_text_paths=6,native_actual_B47_gameplay_runs=0,
            final_plan=PROOFS['plan'],all_proofs=PROOFS,all_original_QA_infos_andtwo_exact_warning_exceptions_preserved=True,
            R53_actual_two_page_turn_required=True,current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            new_credit=0,new_emulator_runs=0,full_goal_complete=False)
        lead=dict(status='open-retrospective-editorial-wrap-lead-no-duplicate-credit',
            source_bound_examples=[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],
                prior_four_row_plan='work/analysis/Rafael_B47_layout_v7984b/15_automatic_plans_full_native_width_zero_preamble_separate_body.json',
                reviewed_three_row_plan=PROOFS['plan'],reason=r['row_count_reason'])
                for r in read(DOC)['records'] if r['source_record_index'] in [5,63]],
            native_review=PROOFS['native_review'],frozen_historical_compilers_preserved=True,
            older_inherited_weak_before_row_priority_to_review_in_complete_context=True,
            not_mechanical_minimum_rows_orrevocation_ofjustified_phrase_retention=True,new_credit=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending);inventory[WRAP]=deepcopy(lead)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,current_English_now_read=True,all_historical_source_first_flags_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,current_English_now_read=True,all_historical_source_first_flags_preserved=True,new_credit=0))
        put([WRAP],lead);put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,
            goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7992: B47 contextual/native/stored review prepared; actual and integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7992; V7964 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('B47 full source/prose/native/stored checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,
                full_goal_all_previous_leads_andnew_retrospective_wrap_lead_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('B47 native/stored checkpoint applied;currentV7964 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                B47_current_English_unread=False,B47_prose_records=15,B47_prose_revisions=8,B47_prose_retentions=7,
                B47_native_pages=16,B47_stored_all16_viewed_pages_exact=True,B47_actual_gameplay_runs=0,
                B47_frozen_policy_atomic_registered_integration_pending=True,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7993/currentV7964:6976completed;B47 15 decisions/16 native-stored pages,8revisions7retentions pending actual/policy/release.Full goal active.')
