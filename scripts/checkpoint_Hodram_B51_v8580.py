"""Audited zero-credit B51 contextual/native/stored checkpoint; full goal intact."""
import argparse
import gzip
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_checkpoint_v8580')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8581')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8568/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B51_actual_reviewed_pending_policy_atomic_registered_v8580'
SCOPE = 'unfinished_editorial_scope_v8580'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7224, 7227, 7227, 4483, 2741]
PROOFS = {
    'independent': 'work/analysis/Hodram_B51_independent_v8569/independent_reconstruction.json',
    'reference': 'work/analysis/Hodram_B51_reference_v8570b/research_image_receipt.json',
    'reference_qualification': 'work/analysis/Hodram_B51_reference_v8570b/qualification.json',
    'loaders': 'work/analysis/Hodram_B51_loaders_v8571/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
    'references': 'work/analysis/Hodram_B51_references_v8572/references.json',
    'fixtures': 'work/analysis/Hodram_B51_fixtures_v8573/two_whole_scripts.json',
    'models': 'work/analysis/Hodram_B51_models_v8575/native_models.json',
    'actual': 'work/analysis/Hodram_B51_actual_v8576/B51/paired_actual_dialogue_headers_flow_returns.json',
    'comparison': 'work/analysis/Hodram_B51_comparison_v8577/paired_selected_path_comparison.json',
    'differences': 'work/analysis/Hodram_B51_difference_view_v8578/sheet.json',
    'actual_review': 'work/analysis/Hodram_B51_actual_review_v8579/whole_exchange_review.json',
    'clean': 'work/analysis/Hodram_B51_clean_v8548/complete_clean_SC1_B51_EV1_andcoverage_before_current_English.json',
    'gloss': 'work/analysis/Hodram_B51_clean_gloss_v8549/five_first_clean_glosses_warning_andconditional_reactions.json',
    'source_controls': 'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json',
    'source_display': 'work/analysis/Hodram_B51_source_display_v8556/source_display.json',
    'source_view': 'work/analysis/Hodram_B51_source_view_v8557/source_view.json',
    'result_flow': 'work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    'current': 'work/analysis/Hodram_B51_current_v8559/current_effective.json',
    'prose': 'work/analysis/Hodram_B51_prose_v8560/contextual_review.json',
    'manuscript': 'translations/hodram_B51_editorial_manuscript_v3.json',
    'names': 'translations/hodram_B51_speaker_name_review_v1.json',
    'logical': 'work/analysis/Hodram_B51_logical_v8561/logical_paragraphs.json',
    'plan': 'work/analysis/Hodram_B51_layout_v8562/automatic_plans.json',
    'pages': 'work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json',
    'native_view': 'work/analysis/Hodram_B51_native_review_v8564/native_body_review.json',
    'relocation': 'work/analysis/Hodram_B51_relocation_v8565/reconstruction.json',
    'stored': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
    'own_input': 'work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json',
    'release': 'work/analysis/Hodram_B50_release_v8544/registered_release_verification.json',
}

SUMMARY = '''Registered experimental cumulative V8543 remains current and unchanged:7,224 completed/7,227 credited source-prose and drafts/4,483 integrated revisions/2,741 justified retentions. B50's three decisions remain credited once. MainV4701 and the canonical baseline remain unchanged. Preserve every ROM, translation, draft, executed producer, proof and failure; no separate requested package, promotion, pruning, commit or push. The full four-storyline and wider editorial objective remains active, with no new completion credit.

B51 manuscriptv3 preserves its five complete clean-first contextual decisions: four revisions and one individually justified retention. Restore the southern Mediterranean setting and Hodram's explanatory question; remove the unsupported monster/rulership assertion; express the unnamed alarming person and well-meant self-preservation advice naturally; keep Charles's hesitant questioning echo free of invented gender; retain Gerhard's parenthesized (Could it be?) as a sudden, private, unresolved possibility. Exact source/current/final references, old English, meanings and individual reasons are retained. All approved wording, compiled bytes and review gates are identical to the already reviewed manuscriptv2. All four prose gates are true and all five formatting gates remain false until the remaining required production checks pass.

Reuse source8555-8557/result-channel8558c/current8559/prose8560/logical8561/plan8562/pages8563/native-review8564/relocation8565/stored8566 without unchanged replay. Five source and five English native pages, twenty logical/twenty compiled alignments, one parity tail/four fresh stored alignments and four byte-identical bodies/sixteen reused alignments pass. Full216px width, complete first/internal/final glyphs, bounds, consumption and five single English pages pass with two line-count infos, zero warnings or waivers. Twenty commands/five full six-byte preambles/eight relative sites/two queries/four opaque controls/full four-byte terminal/separate tails and source/current block/archive/whole-image inverses remain bound. Research B51 is400 logical/stored bytes with zero tail;324 other blocks and every other file/component/name/font/123264-byte payload remain exact.

Independent8569 reconstructs all twenty commands as disjoint atoms and computes all eight branch targets separately, matching the entire sparse block/archive and both inverses. The pinned fullV8543-based reference8570 changes onlySC1B51. Its inherited numeric receipt label50 was caught and corrected to51 only in verified successor8570b, with fresh whole-file/block/parent-ROM-inverse checks. The original producer, receipt, ROM and pins remain untouched. Use qualified8570b as current reference evidence; do not silently edit the historical label. Loaders8571 pass all325 complete native loads/cache hits and650 initial parent modes. References8572 bind all command maps, five exact text references, eight relocated targets/forty cases, original event51 entry and shipped interpreter caller census. Event51 has no listed prerequisite; neither outer eligibility nor chronology or original location is established.

Two full clean-Japanese/revised-English entry fixtures8573 preserve the eight original opening initializers and every B51 command under a constant34-byte shift. Two read-only observed cold boots8574 cover20,002 frames with identical ordinary inputs and no savestate, battery save, RAM/code patch, role/roster/funds/inventory/RNG/condition/result forcing or retiming. They are disclosed initialized entry fixtures, not naturally reached optional activation or original event location. All observed source/English bodies, names and portraits match independent native models8575 in audit8576. Four speeches per language produce28 complete body/name holds each,56 total. Both runs follow the same23 selected commands: the original event30 and raw predicate both return zero; Charles is skipped by the original nested branch and Gerhard's private thought follows. Native structural rules are kept separate from actual observed paths.

The eight observed pages and complete Port Worker/Hodram Bergstrom/Gerhard Adernkatz headers/portraits were directly viewed. Charles R32 remains explicitly unvisited in both runs; his complete source/compiled/stored page, actor18/name/voice, alignments, bounds/pagination and all branch extents pass offline. The agreed representative-test scope does not require forcing this predicate or individually visiting every conditional line. The four scoped name retentions remain, with approved Hodram/Joakim and registered Gerhard Adernkatz; Charles Jean Rochefort is preserved in the full getter. No new name asset or full207-name credit is added; wider Port Worker contexts stay open.

Both complete normal ends carry[0,0], at4736 Japanese/4734 English. Hodram's question and Gerhard's final thought each return one frame earlier in English. There are thirteen selected-boundary comparison rows with timing or decoded-length differences; all native results agree. No sampled script-boundary RNG or UI request values differ, and five checked final components/whole actors/captain1 match. Raw calendar0/[0,0,0] remains uninterpreted. Final sampled PRNG seeds2294662370/3116913577 differ and following commands with frames are not identical. Of89 later RGB pairs,86 match. All three nonidentical pairs were viewed:4870 a two-row pixel strip in the Port label area [210,242,250,244],5650 the later All right. first-row highlight,5830 A-button prompt visibility. Preserve these findings without inventing causality or claiming future RNG outcomes/broad simulation equivalence.

Actual review8579/manuscriptv3 binds the five exact source/current/final records without changing prose, controls or gates. There are three new pinned research ROMs (one reference and two entry fixtures), two actual emulator runs, no new registered candidate and zero completion credit. All jobs are terminal and reaped. Full practical town/random capture and representative gameplay/focused risks remain required; exhaustive natural playthroughs and individual conditional-line visits are not required. Preserve all prior B50/B49/Gerhard/Rafael/Hodram/B48 timing/RNG/component/calendar/RGB/fixture-entry limitations. All four storylines, earlier translated dialogue, shared town/shop/random, Help/remaining prose, all207 names/roles/aliases/custom names and retrospective premature breaks remain in the complete inverse-preserved scope inventory. Graphics/all18plaques and later older-record technical re-audit remain separate. Roughly20,000 remaining candidates is a planning estimate, not an audited prose denominator.'''

NEXT = '''Continue from verifiedV8581/current registeredV8543. B51 is at manuscriptv3/namesv1, complete source/context/prose/native/stored/independent-reference-loader-caller and representative-actual review, with four proposed revisions/one justified retention and zero new credit. Reuse completed8555-8579 evidence and both terminal8574 captures without unchanged replay. Current source/current/final records and all five formatting gates remain unintegrated; counts7224/7227/4483/2741 and all prior families are unchanged. Keep the full objective intact.

Next freeze a source-qualified natural-dialogue-v2 B51 profile/compiler/native contract and bind all per-record gates, the original full216px native rules, stored relative/query/result-channel/end constraints, exact references and qualified8570b research receipt. Independently read native/stored/control/loader/caller/actual/comparison evidence in production and use meaningful actual-changing negative tests without weakening frozen guards. Keep the four observed speeches versus offline-only Charles R32 explicit; further gameplay is needed only for a distinct concrete unresolved risk, not an exhaustive optional-event playthrough or forced visit to every line. Source opaque-effect semantics, outer eligibility, original location, custom names, legitimately earned inventory, future RNG and broad simulation equivalence remain unproven. Retain all measured timing/RNG/RGB differences.

Then implement one complete-NDS-object atomic commit after all gates in both direct-current and canonical.source/full-current.rom lifecycles. Preserve every original prior stage and dependency. Inspect supported registered extension facilities before adding B51; current builder stages are outcomesv6, B49v3 and B50v1 before percent safety with guardv6. Prefer a supported shared hook if present; otherwise source-lock compatible successors, preserve the entire original builder inverse and prove wholeV8543 byte-exact compatibility plus focused actually changed builder/semantic negatives. Never replace a frozen original fingerprint with a mutable current hash. Integrate through the sole registered cumulative builder, exact clean-input patch reconstruction and own startup. Credit five source decisions once only after necessary checks pass. No main promotion, pruning, separate package, commit or push.

Use own currentV8543 Hodram captain1 native input8546 and scripts/Hodram_B50_registered_route_context_v8546.py until the new registered candidate has its own verified startup/context. Never overlay historical RAM or borrow captain2. The full copied unfinished inventory preserves all four stories/earlier dialogue/shared town-shop/random/Help/remaining prose/all207 names/aliases/custom names/retroactive breaks and every older contraction/question-tag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractor104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159 versus Retainer and older normal-end/nineteenth-cell/B47/B48/B50 metadata lead. Graphics and later older-record re-audit stay separate.'''

def parent_at(value, path):
    for key in path[:-1]:
        value = value[key]
    return value, path[-1]

def restore(value):
    result = deepcopy(value)
    for op in reversed(value[KEY]['inverse_operations']):
        parent, key = parent_at(result, op['path'])
        if op['existed']:
            parent[key] = deepcopy(op['before'])
        else:
            parent.pop(key)
    return result

def gates():
    prior = read(PRIOR)
    data = {k: read(p) for k, p in PROOFS.items()}
    assert [prior[k] for k in ['completed', 'source_prose', 'revised', 'retained']] == [7224, 7227, 4483, 2741]
    assert prior['candidate_sha256'] == data['release']['candidate_sha256'] == data['own_input']['current_ROM_sha256']
    assert sha(Path(prior['candidate']).read_bytes()) == prior['candidate_sha256']
    doc = data['manuscript']
    assert len(doc['records']) == 5 and doc['revised'] == 4 and doc['retained'] == 1
    assert all(all(r['review'][k] for k in ['source', 'context', 'localization', 'naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert data['gloss']['all5_clean_utterances_glossed_before_current_English']
    assert data['current']['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert data['result_flow']['original_parser_r3_receives_carried_value_word'] and len(data['result_flow']['caller_fragment_cases']) == 50
    assert len(data['names']['records']) == 4 and data['names']['no_new_name_asset_orall207_name_review_credit']
    assert data['native_view']['manuscript_sha256'] == data['relocation']['manuscript_sha256'] == data['stored']['manuscript_sha256'] == sha(Path(doc['predecessor_manuscript']).read_bytes())
    assert not data['plan']['failures'] and len(data['pages']['records']) == 5 and len(data['native_view']['original_infos']) == 2
    assert not any(i['severity'] in ['warning', 'error'] for row in data['plan']['records'] for i in row['base_QA']['issues'])
    for sheet in [data['source_view']['directly_viewed_sheet'], data['native_view']['directly_viewed_sheet']]:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    stored = data['stored']
    assert stored['whole_current_inmemory_ROM_inverse_byte_exact'] and stored['all324_other_blocks_andall_other_files_components_exact']
    assert stored['whole_ROM_not_written_orregistered'] and stored['fresh_native_alignment_cases'] == 4 and stored['exact_reused_native_alignment_cases'] == 16
    assert len(stored['stored_dispatches']) == 5 and len(stored['stored_queries']) == 2 and len(stored['normal_seeded_ends']) == 25
    assert data['relocation']['source_relative_sites'] == 8 and data['relocation']['relocated_native_skip_cases'] == 40
    assert data['independent']['whole_target_block_andarchive_byte_equal_to_sparse_rebuild']
    assert data['reference']['only_changed_blocks']==[51] and data['reference_qualification']['actual_changed_blocks']==[51]
    assert data['loaders']['fresh_native_whole_loads_andcache_hits']==325 and data['loaders']['fresh_initial_parent_modes']==650
    assert data['references']['external_references_complete'] and len(data['references']['all_command_maps'])==20
    assert not data['actual']['unresolved'] and data['actual']['all_observed_complete_body_name_holds_andnative_flow_pass']
    assert data['actual_review']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())
    assert data['actual_review']['actual_frames']==20002 and data['actual_review']['actual_complete_source_andEnglish_body_name_holds']==56
    assert data['actual_review']['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']
    assert data['actual_review']['later_RGB_equal_pairs']==86 and data['actual_review']['later_RGB_total_pairs']==89
    assert doc['source_current_final_references_complete'] and doc['all_five_formatting_gates_still_false']
    for sheet in data['actual_review']['directly_viewed_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    return prior, data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['stage', 'audit', 'apply', 'verify'])
    mode = parser.parse_args().phase
    prior, data = gates()
    if mode == 'stage':
        assert not ROOT.exists()
        before = LEDGER.read_bytes()
        old = json.loads(before)
        assert sha(before) == prior['ledger_sha256'] and [old[k] for k in COUNTERS] == COUNTS and old['goal_status'] == 'active'
        new, ops = deepcopy(old), []
        def put(path, value):
            parent, key = parent_at(new, path)
            ops.append(dict(path=path, existed=key in parent, before=deepcopy(parent.get(key))))
            parent[key] = deepcopy(value)
        pending = dict(status='five-contextual-decisions-native-stored-independent-reference-loader-caller-andrepresentative-actual-pass-pending-policy-atomic-registered-integration',
            file_path='/data/SC1.DK4', blocks=[51], records=5, proposed_revisions=4, justified_retentions=1,
            scoped_name_retentions=4, source_commands=20, source_relative_sites=8, source_query_sites=2, source_FE_panels=0,
            source_selector_values=[113, 1, 113, 18, 16], manuscript=PROOFS['manuscript'], names=PROOFS['names'], proofs=PROOFS,
            records_with_exact_source_current_andresearch_final_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True, all_five_formatting_gates_false=True, current_English_dialogue_bodies_reviewed=True,
            automatic_fullwidth_pages=5, available_width_px=216, line_count_infos=2, warnings=0, waivers=0,
            logical_alignment_cases=20, compiled_alignment_cases=20, fresh_stored_parity_alignments=4, exact_stored_alignment_reuse=16,
            stored_block_bytes=400, stored_logical_end=400, stored_zero_tail_bytes=0, normal_stored_value_carry_cases=25,
            original_caller_result_channel_cases=50, structural_path_cases=10, actual_B51_emulator_runs=2, actual_B51_frames=20002, actual_B51_complete_body_name_holds=56, actual_observed_speech_count=4, actual_unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
            all324_unowned_blocks_andwhole_source_current_inverses_pass=True, independent_loaders_callers_andrepresentative_actual_pass_frozen_policy_atomic_registered_pending=True,
            new_source_prose_counter_credit=0, new_credit=0, full_goal_complete=False)
        oldpending = prior['pending_source_batch']
        marker = dict(checkpoint=KEY, prior_unread_andpending_flags_historical_not_deleted=True, new_credit=0)
        put([oldpending, 'superseded_by_contextual_native_stored_checkpoint'], marker)
        put(['latest_checkpoint'], SUMMARY + '\n\n' + NEXT)
        descriptor = old[prior['unfinished_scope']]
        assert sha(Path(descriptor['path']).read_bytes()) == descriptor['sha256']
        inventory = deepcopy(read(descriptor['path']))
        inventory[KEY] = deepcopy(pending)
        inventory['next_focus'] = NEXT
        if oldpending in inventory:
            inventory[oldpending]['superseded_by_contextual_native_stored_checkpoint'] = marker
        ROOT.mkdir(parents=True)
        scope = ROOT / 'unfinished_editorial_scope_inventory.json'
        save(scope, inventory)
        put([SCOPE], dict(path=str(scope), sha256=sha(scope.read_bytes()),
            all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            five_uncredited_contextual_decisions=5, graphics_andlater_older_record_technical_reaudit_separate=True, full_goal_complete=False))
        evidence = {str(p): sha(Path(p).read_bytes()) for p in [PRIOR, scope, Path(__file__), *map(Path, PROOFS.values())]}
        put([KEY], dict(**pending, summary=SUMMARY, next=NEXT, evidence=evidence, goal_turn_classification='progress', all_new_native_jobs_terminal_andreaped=True))
        new[KEY]['inverse_operations'] = deepcopy(ops)
        assert restore(new) == old and [new[k] for k in COUNTERS] == COUNTS
        assert new['completed_editorial_families'] == old['completed_editorial_families'] and new['current_integrated_candidate'] == old['current_integrated_candidate']
        (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before, mtime=0))
        targets = {LEDGER: encode_ledger(new)}
        for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']:
            path = Path('docs') / name
            prefix = ('# Current editorial handoff - V8580; V8543 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8580: B51 representative actual review/reference-loaders pass; frozen policy and registered integration next\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8580 staged: six targets, five uncredited contextual/native/stored/representative-actual decisions. Exact inverse audit next.')
    else:
        plan = read(ROOT / 'staged_checkpoint.json')
        old = json.loads(gzip.decompress((ROOT / 'ledger.before.json.gz').read_bytes()))
        new = read(plan['files'][0]['planned'])
        assert restore(new) == old and [new[k] for k in COUNTERS] == COUNTS and new['completed_editorial_families'] == old['completed_editorial_families']
        assert new['current_integrated_candidate'] == old['current_integrated_candidate'] and new['goal_status'] == 'active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes()) == row['planned_sha256']
            assert sha(Path(row['target']).read_bytes()) == row['planned_sha256' if mode == 'verify' else 'before_sha256']
        for path, digest in plan['evidence'].items():
            assert sha(Path(path).read_bytes()) == digest
        if mode == 'audit':
            assert not (ROOT / 'preapplication_audit.json').exists()
            for index, row in enumerate(plan['files'][1:], start=1):
                original = gzip.decompress((ROOT / f'{index:02d}.before.gz').read_bytes())
                assert sha(original) == row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT / 'preapplication_audit.json', dict(staged_plan_sha256=sha((ROOT / 'staged_checkpoint.json').read_bytes()),
                every_prior_value_counter_candidate_andfamily_recovers_exactly=True, every_prior_document_preserved_byte_exact=True, new_credit=0))
            print('V8580 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
        elif mode == 'apply':
            assert not (ROOT / 'application_receipt.json').exists()
            assert read(ROOT / 'preapplication_audit.json')['staged_plan_sha256'] == sha((ROOT / 'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target, planned = Path(row['target']), Path(row['planned'])
                assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:
                    stream.write(planned.read_bytes())
                    stream.truncate()
                    stream.flush()
                    os.fsync(stream.fileno())
                assert sha(target.read_bytes()) == row['planned_sha256']
            save(ROOT / 'application_receipt.json', dict(all_six_targets_hash_exact=True, no_ROM_registry_orcompletion_counter_change=True, new_credit=0, full_goal_complete=False))
            print('V8580 applied; V8543 and all completion counters unchanged. Full goal active.')
        else:
            assert read(ROOT / 'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified = deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()), previous_verified_handoff=str(PRIOR), previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT, unfinished_scope=SCOPE, pending_source_batch=KEY, next_clean_exchange_not_selected=False,
                Hodram_B51_representative_actual_checkpoint=deepcopy(new[KEY]), new_uncredited_source_positions=5,
                physical_speeches_pending=5, typed_choice_labels_pending=0, new_credit=0, new_emulator_runs=2, new_actual_frames=20002, new_research_ROMs=3,
                all_new_native_jobs_terminal_andreaped=True, all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True)
            save(VERIFY / 'verified_handoff.json', verified)
            print('Verified V8581/current V8543: 7224 completed; B51 four revisions/one retention at representative-actual checkpoint; frozen policy/atomic/registered integration pending. Full objective active.')
