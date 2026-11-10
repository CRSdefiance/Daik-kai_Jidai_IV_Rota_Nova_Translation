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

ROOT = Path('work/analysis/Hodram_B51_checkpoint_v8600')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8601')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8591/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B51_all_production_readers_pass_pending_builder_atomic_registered_v8600'
SCOPE = 'unfinished_editorial_scope_v8600'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7224, 7227, 7227, 4483, 2741]
PROOFS = {
    'production_controls': 'work/analysis/Hodram_B51_controls_production_v8592/control_production_validation.json',
    'production_actual': 'work/analysis/Hodram_B51_actual_production_v8593/actual_production_validation.json',
    'builder_inspection': 'work/analysis/Hodram_B51_builder_inspection_v8594/builder_inspection.json',
    'release_path_plan': 'work/analysis/Hodram_B51_release_plan_v8595/release_path_plan.json',
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

SUMMARY = '''Current registered experimental cumulative V8543 remains unchanged, as do mainV4701 and the canonical baseline. Counts remain7,224 completed/7,227 credited source-prose and drafts/4,483 integrated revisions/2,741 justified retentions. B50 remains credited once; B51's five decisions remain unintegrated and uncredited. Preserve every ROM, translation, draft, executed producer, proof and failure. No separate requested package, promotion, pruning, commit orpush. The full objective remains active.

B51 is manuscriptv5/namesv2/nativecontractv1 with all five individual natural-dialogue-v2 gates true, four proposed revisions and one justified retention. All approved wording, complete source/current/final references and compiled bytes remain unchanged. Preserve the source-qualified gruff southern Mediterranean warning, complete Hodram clarification, unnamed bad-news description/well-meant self-preservation advice, conditional Charles echo and private unresolved Gerhard (Could it be?) retention. Add no identity, rulership, rank, gender, crime, supernatural fact, kinship or biography. Four scoped names remain Hodram/Joakim/Bergstrom, registered Gerhard Adernkatz, Charles/Jean/Rochefort and Port Worker; no new name asset or full207-name credit is added. Wider role/custom-name contexts remain open.

Reuse formatting8582/qualified count-note8582b/frozen contract8583/policy8584/reconstruction8585/reference binding8586/native8587/loaders8588/comparison8589.412 immutable dependencies and original full216px width/guard/pair-phase/font/macro rules remain frozen. Five compiler positives and322 actually changed policy inputs pass/reject as expected. Independent reconstruction matches the complete400-byte target with eight relatives/two queries/end/tail/inverses and twenty semantic defects rejected. Reference binding passes both direct-current and canonical.source/full-current.rom lifecycles, with complete five-record references/all twenty commands/all other files/components and whole-ROM inverses. Native production independently recomputes ten source/stored pages and four style11 nameplanes with ten changed defects rejected. Loaders bind325 complete load/cache paths,650 modes,326 actions and shipped callers with five changed defects rejected. Comparison rederives all89 later RGB pairs and native/timing/RNG scope, rejecting four false-equivalence/coverage changes. Every frozen guard remains enabled; no source/editorial/global QA/native metric is weakened.

New production controls8592 independently execute five full dispatches, eight relative sites/forty native branch cases, two unforced queries with all six result words, four clean/current opaque structural pairs, twenty-five full normal value-carry ends and fifty original caller result-channel fragment cases. All original event30/event51 getter fields, source six-byte preambles, native actors/voices, input/output/ABI/unowned4MiB/canary guards and full terminal/tail are bound. Six genuinely changed adapter/branch/query/return/caller-value defects reject, with zero ROM commits. Trusted source artifacts and the exact caller-fragment source are independently hash-bound; the temporary current-context plan is copied into the permanent validation record. No opaque-effect semantics, eligibility or natural activation is inferred.

New production actual reader8593 independently reconstructs both complete entry-fixture ROMs from the original eight initializers and all twenty B51 commands, including eight unchanged relative operands under the constant34-byte shift. It checks full source-qualified resident payloads, CPU/stack observer association, every selected command/result/extent/native branch, exact ordinary input schedules/read-only callbacks, complete native glyph/name masks, normal ends and following original commands. It independently recovers all eight observed pages/56 complete body-name holds; five real initializer/query/hold/conditional-coverage/name defects reject. No capture or completed producer is replayed. Charles R32 remains explicitly unvisited and offline-tested, with no forced predicate or fabricated actual header observation.

Builder inspection8594 inventories all profile.get accesses and validates current outcomesv6/B49v3/B50v1 order before final percent safety, plus the entire original frozen-builder inverse. The existing shared late_story_editorial_release hook was inspected: it requires dialogue-fixed-v1/equal allocations and executes before the later frozen route stages. B51 needs340-to400-byte relocation/eight mapped relatives after the fullV8543 stack, so that existing hook is unsuitable without weakening its contract. No builder or registry changed. Immutable release path/scope helper8595 and its validation bind all completed readers, eight actual page occurrences/56holds/four observed speeches and offline-only Charles. Three compatible-builder/predecessor proof paths, seal/config and atomic/registered stages are declared pending, not fabricated or approved.

Preserve all B51 source/context/native/stored/actual evidence8555-8579 and the three earlier pinned research ROMs. Research B51 remains400 logical/stored bytes/zero tail, versus340 before, with every324 other block and all other files/components/names/font/123264-byte payload exact. One compiler parity tail/four fresh stored alignments and four exact bodies/sixteen reused alignments preserve complete first/internal/final glyphs/bounds/pagination. Five English singlepages use the full216px width with two original line-count infos, zero warnings/waivers, no manual prose breaks/padding/shortening/font changes.

Actual scope remains two initialized whole-script entry fixtures/20,002 frames, four speeches per language/56holds and matching full name/portrait regions. Both queries return zero and the same23-command path omits Charles. Normal ends4736 Japanese/4734 English carry[0,0]. Two short durations differ by one frame; thirteen timing/decoded-length comparison rows differ. Boundary RNG/UI requests and five sampled final components/whole actors/captain1 match; raw calendar0/[0,0,0] remains uninterpreted. Final seeds2294662370/3116913577 and following commands with frames differ.86of89 laterRGB pairs match; all three viewed differences4870 Port-label pixels,5650 All right. highlight,5830 A-prompt remain. Matching samples prove neither every-frame causality nor future RNG/broad simulation equivalence. These are disclosed entry fixtures, not natural optional activation, original location, earned inventory, custom names, fullroute or hardware coverage. Original effect semantics/outer eligibility stay unproven.

No new ROM, emulator run, registry layer or completion credit was added this turn; all jobs are terminal and reaped. Full all-four-storyline/earlier-dialogue/shared town-shop/random/Help/remaining prose/all207 names-roles-aliases-custom names/retrospective early-break objective and every earlier lead/history remain in the inverse-preserved inventory. Broad practical town/random capture and representative gameplay/focused risks remain required; exhaustive natural playthroughs and individually visiting every conditional line are not required. Graphics/all18plaques and later older-record technical re-audit remain separate. Roughly20,000 remaining candidates remains a planning estimate, not an audited prose denominator.'''

NEXT = '''Continue from verifiedV8601/current registeredV8543. B51 latest manuscriptv5/namesv2/nativecontractv1 has all five gates and every independent production reader passing. Reuse policy322 rejections8584/reconstruction20 rejections8585/two lifecycle references8586/native10 rejections8587/loaders5 rejections8588/comparison4 rejections8589/controls6 rejections8592/actual5 rejections8593 without unchanged replay. Current counts7224/7227/4483/2741 remain unchanged; five decisions (four revisions/one retention) still need atomic registered integration and once-only credit. Keep the full objective and every prior artifact intact.

Next prepare source-locked compatible builder support/guardv7 after inspection8594. Existing fixed late-story hook is unsuitable because of equal-allocation restrictions and early ordering; preserve it. Current builder/registry remain unchanged. Add one explicit B51 stage after complete outcomesv6/B49v3/B50v1 and before final percent safety through known compatible namespace successors. Preserve every original predecessor dependency and the exact entire original-builder inverse; do not replace frozen original fingerprints with mutable current hashes. Inspect existing B50 builder-support8534/validation8535/predecessor8536 patterns before choosing the exact compatibility updates, including nested profile/QA/name/control dependencies rather than merely changing an outer import. Prove positive supported old/new builder forms plus actual-changing unsupported/mixed/reordered/duplicate/wrong-location forms and whole registeredV8543 predecessor equality.

The immutable planned paths are scripts/Hodram_B51_release_paths_v8595.py: builder_support work/analysis/Hodram_B51_builder_support_v8596/source_equivalence.json; builder_validation work/analysis/Hodram_B51_builder_validation_v8596/exact_builder_inverse_cases.json; predecessor compatibility work/analysis/Hodram_B51_predecessor_positive_v8597/whole_V8543_byte_exact.json; seal work/analysis/Hodram_B51_release_seal_v8598/reference_seal.json; config translations/hodram_B51_editorial_release_v1.json. These are explicitly pending. The ready proof list and exact observed_scope are checked in work/analysis/Hodram_B51_release_plan_v8595/release_path_plan.json. Use qualified reference8570b (actual block51); preserve the original8570 wrong numeric label50 receipt as history.

Then freeze production paths/seal/config/dependencies and implement the B51 atomic stage using independent modules hodram_B51_reconstruction_v1/references_v1/native_guards_v1/native_evidence_v1/loaders_v1/comparison_v1/controls_v1/actual_evidence_v1. Controls signature check_controls(data,rows,parent,reference,rebuilt,native,load,require); actual signature check_actual(data,rows,parent,clean,rebuilt,native,load,require). Native returns bodies/names/summary, actual returns summary/canonical_fixtures. Source8555 uses flat all_original_source_commands/source_owned_entry_adapter, not B50 groups/source_owned_EV1_entry_adapter; stored8566 combines bodies/controls. Preserve these actual schemas and detailed guards. Trusted source adapter hashes survive release-dependency challenges.

The atomic stage must validate all approved compiler bytes/QA/native/control/loader/caller/actual/comparison and measured scope, then commit one complete NDS object once after every gate. Test direct-current and canonical.source/full-current.rom lifecycles with byte-value-equal reports, meaningful actual-changing semantic failure cases and genuine wrong-memory inputs with every native/frozen guard active and zero partial commits. Only then integrate through the sole registered cumulative builder, all accepted layers, exact clean-input patch reconstruction and own startup/context. Credit the five source decisions once only after necessary checks pass. CurrentregisteredV8543/main4701/canonical baseline and all ROMs remain preserved; no promotion, pruning, separate package, commit orpush.

Use own V8543 Hodram captain1 native input8546 and scripts/Hodram_B50_registered_route_context_v8546.py until a new registered build has its own verified startup. Never overlay historical RAM or borrow captain2. Retain four actually observed B51 speeches versus offline-only Charles R32; no new gameplay is needed absent a distinct concrete unresolved risk. All two-run timing/boundary-final RNG/UI/native-component/raw-calendar/following-command/89RGB findings and source opaque/eligibility/fixture limitations remain explicit. Full copied inventory preserves all four stories/earlier dialogue/shared town-shop/random/Help/remaining prose/all207 names/custom names/retroactive wrapping and every older contraction/question-tag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractor104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159 versus Retainer and older normal-end/nineteenth-cell/B47/B48/B50 metadata lead. Graphics and later older-record re-audit stay separate.'''

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
    control=data['production_controls'];actual=data['production_actual']
    assert control['negative_count']==6 and control['summary']['native_relative_cases']==40 and control['summary']['original_result_channel_cases']==50
    assert control['every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled']
    assert actual['negative_count']==5 and actual['summary']['complete_actual_page_occurrences']==8 and actual['summary']['complete_actual_holds']==56
    assert actual['every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled']
    assert data['builder_inspection']['no_suitable_existing_registered_hook_for_this_relocatable_late_B51_contract']
    assert data['builder_inspection']['current_outcomesv6_B49v3_B50v1_order_andentire_original_builder_inverse_exact']
    assert data['release_path_plan']['all_completed_production_native_controls_actual_references_loaders_andcomparisons_bound']
    assert data['release_path_plan']['observed_scope']['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']
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
        pending = dict(status='five-all-gate-decisions-frozen-policy322-all-production-readers-pass-pending-builder-atomic-registered-integration',
            file_path='/data/SC1.DK4', blocks=[51], records=5, proposed_revisions=4, justified_retentions=1,
            scoped_name_retentions=4, source_commands=20, source_relative_sites=8, source_query_sites=2, source_FE_panels=0,
            source_selector_values=[113, 1, 113, 18, 16], manuscript=PROOFS['manuscript'], names=PROOFS['names'], proofs=PROOFS,
            records_with_exact_source_current_andresearch_final_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True, all_five_formatting_gates_true=True, frozen_policy_negative_cases=322, production_reconstruction_negatives=20, production_native_negatives=10, production_loader_negatives=5, production_comparison_negatives=4, production_control_negatives=6, production_actual_negatives=5, current_English_dialogue_bodies_reviewed=True,
            automatic_fullwidth_pages=5, available_width_px=216, line_count_infos=2, warnings=0, waivers=0,
            logical_alignment_cases=20, compiled_alignment_cases=20, fresh_stored_parity_alignments=4, exact_stored_alignment_reuse=16,
            stored_block_bytes=400, stored_logical_end=400, stored_zero_tail_bytes=0, normal_stored_value_carry_cases=25,
            original_caller_result_channel_cases=50, structural_path_cases=10, actual_B51_emulator_runs=2, actual_B51_frames=20002, actual_B51_complete_body_name_holds=56, actual_observed_speech_count=4, actual_unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
            all324_unowned_blocks_andwhole_source_current_inverses_pass=True, all_independent_production_native_controls_actual_references_loaders_andcomparisons_pass_builder_atomic_registered_pending=True,
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
            prefix = ('# Current editorial handoff - V8600; V8543 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8600: B51 all production readers pass; compatible builder and atomic registered integration next\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8600 staged: six targets, five uncredited all-gate/frozen-policy/all-production decisions. Exact inverse audit next.')
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
            print('V8600 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
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
            print('V8600 applied; V8543 and all completion counters unchanged. Full goal active.')
        else:
            assert read(ROOT / 'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified = deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()), previous_verified_handoff=str(PRIOR), previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT, unfinished_scope=SCOPE, pending_source_batch=KEY, next_clean_exchange_not_selected=False,
                Hodram_B51_all_production_readers_checkpoint=deepcopy(new[KEY]), new_uncredited_source_positions=5,
                physical_speeches_pending=5, typed_choice_labels_pending=0, new_credit=0, new_emulator_runs=0, new_actual_frames=0, new_research_ROMs=0,
                all_new_native_jobs_terminal_andreaped=True, all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True)
            save(VERIFY / 'verified_handoff.json', verified)
            print('Verified V8601/current V8543: 7224 completed; B51 four revisions/one retention/allfivegates/frozenpolicy322/allproduction readers pass; compatiblebuilder/atomic/registered pending. Full objective active.')
