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

ROOT = Path('work/analysis/Hodram_B51_checkpoint_v8590')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8591')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8581/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B51_frozen_policy_native_reference_loader_comparison_pending_controls_actual_atomic_registered_v8590'
SCOPE = 'unfinished_editorial_scope_v8590'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7224, 7227, 7227, 4483, 2741]
PROOFS = {
    'format_approval': 'work/analysis/Hodram_B51_format_v8582b/formatting_approval.json',
    'native_contract': 'translations/hodram_B51_native_contract_v1.json',
    'frozen_policy': 'work/analysis/Hodram_B51_policy_v8583/frozen_contract.json',
    'policy_validation': 'work/analysis/Hodram_B51_policy_validation_v8584/policy_validation.json',
    'production_reconstruction': 'work/analysis/Hodram_B51_reconstruction_v8585/independent_reconstruction_validation.json',
    'production_references': 'work/analysis/Hodram_B51_reference_binding_v8586/production_reference_binding.json',
    'production_native': 'work/analysis/Hodram_B51_native_production_v8587/native_production_validation.json',
    'production_loaders': 'work/analysis/Hodram_B51_loaders_production_v8588/loader_production_validation.json',
    'production_comparison': 'work/analysis/Hodram_B51_comparison_production_v8589/comparison_production_validation.json',
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
    'manuscript': 'translations/hodram_B51_editorial_manuscript_v5.json',
    'names': 'translations/hodram_B51_speaker_name_review_v2.json',
    'logical': 'work/analysis/Hodram_B51_logical_v8561/logical_paragraphs.json',
    'plan': 'work/analysis/Hodram_B51_layout_v8562/automatic_plans.json',
    'pages': 'work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json',
    'native_view': 'work/analysis/Hodram_B51_native_review_v8564/native_body_review.json',
    'relocation': 'work/analysis/Hodram_B51_relocation_v8565/reconstruction.json',
    'stored': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
    'own_input': 'work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json',
    'release': 'work/analysis/Hodram_B50_release_v8544/registered_release_verification.json',
}

SUMMARY = '''Current registered experimental cumulative V8543 and mainV4701/canonical baseline remain unchanged. Counts remain7,224 completed/7,227 credited source-prose and drafts/4,483 integrated revisions/2,741 justified retentions; B50's three decisions remain credited once. B51's five decisions are not yet integrated or credited. Preserve every ROM, translation, draft, executed producer, proof and failure. No separate requested package, promotion, pruning, commit or push. The full objective remains active.

B51 now has all five individual natural-dialogue-v2 gates approved in manuscriptv5 with four proposed revisions and one contextual retention, exact source/current/final references and unchanged approved prose/compiled bytes. Four scoped name retentions are preserved in namesv2. Formatting approval8582 binds complete source/stored/native/control/reference evidence and representative actual coverage; qualified8582b corrects only an overstated alignment-count sentence to four alignments per logical or compiled body with byte-identical stored evidence explicitly reused. The original note, approval and manuscript remain preserved. Standard natural-dialogue-v2 validation passes without changing the global validator.

Frozen native contract8583/profile-layout-plan-namesv1 binds all five progressive pages, original full216px width, selectors71/01/12/10, zero source macros, measured FI6/FA9/FO15, two line-count infos, zero warnings/waivers and412 immutable dependencies. Its source control binding preserves twenty commands/five full preambles/eight relatives/two queries/four opaque controls/full four-byte end. No ordinary prose break, padding, shortening, font/viewport/global QA change or native consumer widening is introduced. The mutable integrated builder is excluded from native dependency discovery; original fingerprints remain preserved.

Policy validation8584 passes five exact compiler positives and322 actually changed-input rejections, including individual gates, wording, source/current/final references, speaker/control bytes, macros/metrics/guards, names and false actual-versus-unvisited coverage claims. All frozen guards stay enabled and every protected file/ROM/source/ledger/registry/pin is byte-identical during the test. These historical protected hashes are test snapshots, not mutable current-ledger dependencies to reassert after a later checkpoint.

Independent production reconstruction8585 equals the entire tested400-byte B51 block, preserves all eight relative targets/two queries/terminal/tails/both block inverses and rejects twenty genuine structured control/reference defects. Production references8586 bind all five source/current/final identities, all twenty commands, full archive/whole-ROM equality and inverse in both direct-current and canonical.source/full-current.rom lifecycles. Both leave the caller image unchanged and make zero commits. Qualified current reference remains8570b; historical8570 numeric block50 receipt label remains preserved as history, with actual changed block51 independently proven.

Native production8587 independently recomputes ten Japanese/stored English pages and four complete style11 nameplanes through exact trusted source adapters. First/internal/final characters, bounds, consumption, glyph events, full planes, font and original pair flushes match. Ten actually changed native-evidence inputs reject with frozen dependency guards enabled. Production loaders8588 independently bind325 complete load/cache paths,650 initial parent modes,326 original actions, all command/record references and shipped callers; five changed count/reference/eligibility-scope inputs reject. Production comparison8589 independently recomputes all89 later RGB pairs, both final read-only native snapshots/components/whole actors/captain1, timing/RNG/UI/normal returns and following commands. Four attempts to hide RGB, timing, final-RNG or unvisited-Charles evidence reject. No completed producer or emulator run was replayed and no new ROM was written this turn.

Preserve the full earlier B51 evidence8555-8579: five source/five English complete native pages, twenty logical/twenty compiled alignments, one parity tail/four fresh stored alignments/four exact bodies/sixteen reused alignments, forty relative cases, fifty native result-channel fragment cases, independent disjoint-atom reconstruction and all source/current/final references. Research B51 remains400 stored/logical bytes with zero tail; every324 other block and every other file/component/name/font/123264-byte deployed payload remains exact. Three earlier pinned research ROMs remain (one reference/two full entry fixtures); no new registered release exists.

Representative actual coverage remains two complete initialized opening fixtures/20,002 frames with identical ordinary inputs, four speeches per language/56 complete body-name holds, matching name/portrait regions and normal returns4736 Japanese/4734 English carrying[0,0]. Both actual queries return zero; the same23-command path omits Charles R32. His actor18/name/voice, full source/English/stored page and all branch/display checks remain offline-only. Do not force a conditional visit or claim actual Charles-header coverage. The agreed scope requires representative/focused checks, not every conditional line or exhaustive natural playthrough.

Two short speech durations differ by one frame each; thirteen boundary rows have timing or decoded-length differences. All selected native results, sampled boundary RNG and UI requests match. Five checked final components/whole actors/captain1 match; raw calendar0/[0,0,0] remains uninterpreted. Final sampled seeds2294662370/3116913577 differ; following commands with frames differ.86of89 later RGB pairs match; viewed differences4870 Port-label pixels [210,242,250,244],5650 All right. highlight,5830 A-prompt visibility remain. Do not infer every-frame causality, future RNG outcomes or broad simulation equivalence. These are disclosed entry fixtures, not natural optional activation, original location, earned inventory, custom names, fullroute or hardware coverage. Source opaque-effect semantics and outer eligibility remain unproven.

Full all-four-storyline/earlier-dialogue/shared-town-shop/random/Help/remaining prose/all207 names-roles-aliases-custom names/retrospective premature-break objective and every prior lead/history remain in the inverse-preserved scope inventory. Broad practical town/random capture and representative gameplay/focused risks remain required. Graphics/all18plaques and later older-record technical re-audit remain separate. Roughly20,000 remaining candidates is a planning estimate, not an audited prose denominator.'''

NEXT = '''Continue from verifiedV8591/current registeredV8543. B51 latest is manuscriptv5/namesv2/nativecontractv1 and profile/layout/plan/namesv1. All five editorial gates are true; five decisions (four revisions/one retention) remain uncredited pending registered integration. Reuse formatting8582/qualified note8582b/frozen contract8583/policy322 rejections8584/production reconstruction20 rejections8585/two reference lifecycles8586/native production10 rejections8587/loader production5 rejections8588/comparison production4 rejections8589 without unchanged replay. No new ROM/capture/registry orcompletion credit this turn; count7224 remains unchanged. Keep every earlier artifact and full objective intact.

Next independently bind B51 production control evidence and complete actual entry-fixture/native-body/name/observed-flow/normal-return evidence. Preserve exact20commands, five six-byte preambles, eight relatives, event30 query plus separate raw8000 query, source event51/no listed prerequisites, original result-channel value carry, opaque controls/full end/tails and rich source/current/final references. Existing actual evidence covers four speeches and56holds, with offline-only Charles R32; do not require exhaustive optional activation or force a predicate merely to visit that line. A new gameplay test is warranted only for a distinct concrete unresolved risk. Keep all timing/final-RNG/later-RGB and scope limits.

Production modules now exist: hodram_B51_reconstruction_v1/references_v1/native_guards_v1/native_evidence_v1/loaders_v1/comparison_v1. Bind trusted original source adapters through their exact source artifact hashes and immutable code, not through challenged mutable release evidence. The remaining controls/actual readers must independently consume detailed evidence rather than trust producer summary booleans. Source8555 has flat all_original_source_commands/source_owned_entry_adapter fields, not B50's older groups/source_owned_EV1_entry_adapter schema. Source8556 has scoped_clean_current_four_names_andreused_native_consumers and no FE adapter; stored8566 combines stored bodies/controls and has final_reference/stored_hex records. Use the actual B51 schemas. Avoid claiming fresh execution for reused byte-identical evidence or borrowing old captain2 RAM.

Use own registeredV8543 Hodram captain1 input8546 and scripts/Hodram_B50_registered_route_context_v8546.py until the new registered candidate has its own startup/context. Then freeze production paths/seal/dependencies, implement one complete-NDS atomic commit only after all gates, verify both direct-current and canonical.source/full-current.rom lifecycles and meaningful actually changed semantic failures/wrong-memory inputs with no partial commits. Preserve every frozen prior dependency, original builder inverse and exact wholeV8543 compatibility. Inspect supported registered extension hooks before adding B51: current stages are outcomesv6/B49v3/B50v1 before percent safety with guardv6. Prefer a supported shared hook if present; otherwise use source-locked compatible successors and focused changing builder tests. Never pin a mutable whole-builder fingerprint in place of the frozen original.

Integrate through the sole registered cumulative builder with all accepted layers, exactly reconstructable clean-input patch and own startup. Credit five decisions once only after necessary checks pass. Main/canonical baseline and all ROMs remain preserved; no promotion, pruning, separate package, commit orpush. The full copied unfinished inventory preserves all four stories/earlier translations/shared town-shop/random/Help/remaining prose/all207 names/aliases/custom names/retroactive wrapping, every older contraction/question-tag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractor104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159 versus Retainer and older normal-end/nineteenth-cell/B47/B48/B50 metadata lead. Graphics and later older-record re-audit stay separate.'''

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
    assert all(all(r['review'][k] for k in ['source', 'context', 'localization', 'naturalness', 'formatting']) for r in doc['records'])
    assert data['gloss']['all5_clean_utterances_glossed_before_current_English']
    assert data['current']['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert data['result_flow']['original_parser_r3_receives_carried_value_word'] and len(data['result_flow']['caller_fragment_cases']) == 50
    assert len(data['names']['records']) == 4 and data['names']['no_new_name_asset_orall207_name_review_credit']
    assert data['native_view']['manuscript_sha256'] == data['relocation']['manuscript_sha256'] == data['stored']['manuscript_sha256'] == sha(Path(data['native_view']['manuscript']).read_bytes())
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
    assert data['actual_review']['manuscript_sha256']==sha(Path(data['actual_review']['manuscript']).read_bytes())
    assert data['actual_review']['actual_frames']==20002 and data['actual_review']['actual_complete_source_andEnglish_body_name_holds']==56
    assert data['actual_review']['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']
    assert data['actual_review']['later_RGB_equal_pairs']==86 and data['actual_review']['later_RGB_total_pairs']==89
    assert doc['source_current_final_references_complete'] and doc['all_five_individual_five_gates_true'] and not doc['all_five_formatting_gates_still_false']
    for sheet in data['actual_review']['directly_viewed_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    from dk4tool.dialogue.hodram_B51_profile_v1 import contract,validate_approved_batch
    from dk4tool.dialogue.hodram_B51_names_v1 import validate_scoped_names
    assert contract()==data['native_contract']
    validate_approved_batch(doc);validate_scoped_names(data['names'])
    assert data['format_approval']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and data['format_approval']['all5_five_gates_true']
    assert data['frozen_policy']['contract_sha256']==sha(Path(PROOFS['native_contract']).read_bytes()) and data['frozen_policy']['dependency_count']==412
    policy=data['policy_validation'];assert policy['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())
    assert policy['negative_count']==322 and len(policy['positive_speech_compilers'])==5 and policy['every_negative_actual_input_changed_andguard_rejected']
    assert policy['all_frozen_dependency_guards_remained_enabled']
    assert data['production_reconstruction']['negative_count']==20 and data['production_reconstruction']['entire_research_block_byte_exact']
    assert len(data['production_references']['positive_lifecycles'])==2 and data['production_references']['complete_source_current_block_archive_andwhole_inmemory_ROM_inverses_exact']
    assert data['production_native']['negative_count']==10 and data['production_native']['positive_native_pages']==10 and data['production_native']['positive_scoped_nameplanes']==4
    assert data['production_loaders']['negative_count']==5 and data['production_loaders']['original325_loads_cache_hits650_modes326_actions_andshipped_callers_independently_bound']
    assert data['production_comparison']['negative_count']==4 and data['production_comparison']['summary']['later_full_RGB_pairs_recomputed']==89
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
        pending = dict(status='five-all-gate-decisions-frozen-policy322-native-reference-loader-comparison-production-pass-pending-controls-actual-production-atomic-registered-integration',
            file_path='/data/SC1.DK4', blocks=[51], records=5, proposed_revisions=4, justified_retentions=1,
            scoped_name_retentions=4, source_commands=20, source_relative_sites=8, source_query_sites=2, source_FE_panels=0,
            source_selector_values=[113, 1, 113, 18, 16], manuscript=PROOFS['manuscript'], names=PROOFS['names'], proofs=PROOFS,
            records_with_exact_source_current_andresearch_final_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True, all_five_formatting_gates_true=True, frozen_policy_negative_cases=322, production_reconstruction_negatives=20, production_native_negatives=10, production_loader_negatives=5, production_comparison_negatives=4, current_English_dialogue_bodies_reviewed=True,
            automatic_fullwidth_pages=5, available_width_px=216, line_count_infos=2, warnings=0, waivers=0,
            logical_alignment_cases=20, compiled_alignment_cases=20, fresh_stored_parity_alignments=4, exact_stored_alignment_reuse=16,
            stored_block_bytes=400, stored_logical_end=400, stored_zero_tail_bytes=0, normal_stored_value_carry_cases=25,
            original_caller_result_channel_cases=50, structural_path_cases=10, actual_B51_emulator_runs=2, actual_B51_frames=20002, actual_B51_complete_body_name_holds=56, actual_observed_speech_count=4, actual_unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
            all324_unowned_blocks_andwhole_source_current_inverses_pass=True, independent_loaders_callers_representative_actual_frozen_policy_native_reference_loader_comparison_production_pass_controls_actual_production_atomic_registered_pending=True,
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
            prefix = ('# Current editorial handoff - V8590; V8543 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8590: B51 frozen policy322/native-reference-loader-comparison production pass; controls-actual production and registered integration next\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8590 staged: six targets, five uncredited all-gate/frozen-policy/partial-production decisions. Exact inverse audit next.')
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
            print('V8590 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
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
            print('V8590 applied; V8543 and all completion counters unchanged. Full goal active.')
        else:
            assert read(ROOT / 'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified = deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()), previous_verified_handoff=str(PRIOR), previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT, unfinished_scope=SCOPE, pending_source_batch=KEY, next_clean_exchange_not_selected=False,
                Hodram_B51_frozen_policy_production_checkpoint=deepcopy(new[KEY]), new_uncredited_source_positions=5,
                physical_speeches_pending=5, typed_choice_labels_pending=0, new_credit=0, new_emulator_runs=0, new_actual_frames=0, new_research_ROMs=0,
                all_new_native_jobs_terminal_andreaped=True, all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True)
            save(VERIFY / 'verified_handoff.json', verified)
            print('Verified V8591/current V8543: 7224 completed; B51 four revisions/one retention/allfivegates/frozenpolicy322/partialproduction pass; controls-actual production/atomic/registered pending. Full objective active.')
