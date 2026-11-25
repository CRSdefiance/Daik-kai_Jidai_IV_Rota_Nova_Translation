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

ROOT = Path('work/analysis/Hodram_B52_clean_checkpoint_v8618')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8619')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8615/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B51_registered_build_pending_B52_clean_first_ready_v8618'
SCOPE = 'unfinished_editorial_scope_v8618'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7224, 7227, 7227, 4483, 2741]
PROOFS = {
    'B52_clean': 'work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json',
    'B52_gloss': 'work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json',
    'builder_support_completed': 'work/analysis/Hodram_B51_builder_support_v8596/source_equivalence.json',
    'builder_validation_completed': 'work/analysis/Hodram_B51_builder_validation_v8596/exact_builder_inverse_cases.json',
    'predecessor_compatibility_completed': 'work/analysis/Hodram_B51_predecessor_positive_v8597/whole_V8543_byte_exact.json',
    'atomic_seal': 'work/analysis/Hodram_B51_release_seal_v8598/reference_seal.json',
    'atomic_configuration': 'translations/hodram_B51_editorial_release_v1.json',
    'atomic_positives': 'work/analysis/Hodram_B51_atomic_positive_v8604/atomic_positive.json',
    'atomic_negatives': 'work/analysis/Hodram_B51_atomic_challenges_v8605b/semantic_rejections.json',
    'wrong_memory': 'work/analysis/Hodram_B51_wrong_memory_v8605/wrong_memory_rejections.json',
    'atomic_binding': 'work/analysis/Hodram_B51_atomic_binding_v8606/semantic_binding.json',
    'registration': 'work/analysis/Hodram_B51_registration_v8608/registration_receipt.json',
    'registered_build_plan': 'work/analysis/Hodram_B51_build_v8609/build_plan.json',
    'regressions': 'work/analysis/Hodram_B51_regressions_v8609/terminal.json',
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

SUMMARY = '''Current verified experimental cumulative ROM remains V8543 until the newly registered V8609 build finishes all release/startup checks. MainV4701 and canonical baseline remain unchanged. Counts remain7,224 completed/7,227 credited source-prose and drafts/4,483 integrated revisions/2,741 justified retentions; B51 five decisions remain uncredited. Preserve every ROM, draft, translation, executed producer, proof and failure. No separate requested package, promotion, pruning, commit orpush. Full all-four-storyline/earlier-dialogue/shared town-shop/random/Help/remaining prose/all207 names-roles-aliases-custom names/retrospective premature-break objective remains active; graphics/all18plaques and later older-record technical re-audit stay separate. Roughly20,000 remaining candidates is a planning estimate, not an audited prose denominator.

B51 five individual all-gate decisions remain manuscriptv5/namesv2/nativecontractv1:four revisions/one justified retention, exact source/current/final references, automatic full216px five singlepages, two line-count infos, zero warnings/waivers. All approved words and bytes remain unchanged. Retain gruff southern Mediterranean warning, Hodram clarification, unnamed bad-news advice, conditional Charles echo and unresolved private Gerhard suspicion; invent no identity, rank, rulership, gender, kinship, crime or supernatural fact. Scoped Hodram/Joakim, Gerhard Adernkatz, Charles/Jean and Port Worker approvals do not complete the wider207-name objective.

Compatible builder support8596 now exists:guardv7/namespace-only outcomesv7/B49v4/B50v2 preserve all535/675/756 predecessor dependencies and entire original frozen-builder inverse. Five exact positive builder forms pass;25 genuinely changed mixed/duplicate/reordered/wrong-input/changed-byte forms reject. Predecessor8597 completes outcomes/B49/B50 with all production guards active and reproduces whole registeredV8543 byte-for-byte. No completed producer, native evidence capture or prior compatibility check was replayed.

Atomic module hodram_B51_editorial_v1 and seal8598b/configv1 pin855 dependencies, including all412 frozen B51 dependencies and every compatible predecessor entry. All compiler/QA/independent references/native/control/loader/caller/actual/comparison/inverse gates execute before one complete NDS-object commit. Both direct-current and canonical.source/full-current.rom lifecycles pass, reproduce the entire approved reference and yield value-identical reports. Three genuinely wrong-memory inputs reject with every guard active and zero mutation. Seventeen actually changed semantic inputs reject before commit; only the outer release digest layer is bypassed to reach semantics, while all frozen native/source/editorial and semantic guards remain active. Ten completed cases are reused through exact original/changed-input and diagnostic revalidation; they are not replayed. Original failed seal producer8598 (old result key) and stopped semantic runner8605 (different expected query diagnostic) remain preserved; corrected successors8598b/8605b pass without weakening production guards.

Registration8608 adds experimental profile all-routes-unified-v8609 after entireV8543. Exact prior registry values and every unowned builder byte recover; all114accepted layers/main4701/prior profiles remain. Expected645manifest batches/18release checks/110regressions. Registered build8609 has been launched through the sole builder, with handle15222 and wrapperPID20144 recorded for continuation; poll that specific handle and authoritative terminal before claiming an output or restarting. All110 release/dialogue regressions passed. Registered build, manifest/reference checks, exact clean-input patch, own startup/context/direct review and once-only five-record credit remain pending. Prepared verification8610 and startup/context/review tools8611-8613 are not claims that those checks ran.

Reuse all source/context/native/stored/actual production proofs8555-8593. Source block340 and target400 bytes preserve20commands/five six-byte preambles/eight relatives/two queries/four opaque controls/fullend/zero tail,324unownedblocks/allotherfiles/components/nameasset/font/123264payload. Two initialized entry fixtures20002frames show four speeches perlanguage/eight observed pages/56completeholds; CharlesR32 is explicitly unvisited and offline-tested. Normalends4736/4734 carry[0,0];two short durations and13timing/length rows differ. Sampled boundaryRNG/UIrequests andfive final components/wholeactors/captain1 match, rawcalendar uninterpreted;finalseeds2294662370/3116913577 andfollowing commands withframes differ.86of89laterRGBpairs match;Port-label strip4870/menuhighlight5650/Aprompt5830 remain. No everyframe causality, future RNG/broad simulation, natural activation/original location/earned inventory/custom names/fullroute/hardware claim. Wider town/random captures and representative gameplay/focused concrete risks remain required under the agreed practical coverage scope.

The next source candidate B52 has now been read and glossed from clean Japanese before any existing English:three speeches and both choice labels,all71 selectors,228stored/logical bytes,zero tail,14 native-inventory commands. The speaker asks about intending to oppose ハイレディン一家;choices deny that intention or volunteer to take the group on. Subsequent linguistic reactions advise quick withdrawal before discovery or comment on dangerous boldness. Do not infer actual hostility, kinship from一家,a rank,nationality,crime orapproved named-group spelling. Exact native choice metadata/selection/branches and opaque83c2 at164 remain unreviewed;end166 has00000000 whileend224 has00000080 and must not be assumed the same normal zero-return path. Event52requires30/excludes74,with original outer eligibility/location/activation still unexecuted. All source/current references,source prose and gameplay gates remain pending for B52;no ROM orcredit added. B51 release integration remains the immediate priority.'''

NEXT = '''Continue from verifiedV8615/current verified ROMV8543, with experimentalV8609 registered/build pending and all110 regressions passed. First poll exec session15222 (wrapperPID20144; work/analysis/Hodram_B51_build_v8609/build_plan.json) and inspect its authoritative terminal/log; do not restart from an observation timeout or silence. Build uses scripts/build_Hodram_B51_v8609.py and sole scripts/build_integrated_release.py, profile all-routes-unified-v8609, intended out/all_routes_combined_v8609_candidate.nds. All prior ROMs remain preserved. If terminal fails, retain producer/log/partial artifacts and derive a successor; do not overwrite executed scripts or outputs.

On build success run prepared scripts/verify_Hodram_B51_release_v8610.py, checking645manifest batches/114accepted/18checks/110regressions, exact full reference, all324unownedblocks/files/components, complete prior builder/registry/profile inverse and exact clean-input patch reconstruction. Then scripts/capture_Hodram_B51_registered_v8611.py --route 1 for its own4001frame ordinary coldboot, scripts/bind_Hodram_B51_registered_v8612.py, inspect the generated whole startup sheet directly, and only then scripts/verify_Hodram_B51_registered_startup_v8613.py. Own new context is scripts/Hodram_B51_registered_route_context_v8612.py; use existing V8543/captain1 helper8546 until its new binding passes. Never overlay historical RAM or use captain2. No completed B51 scene fixture/capture/producer or predecessor compatibility check needs replay.

After necessary release/startup checks pass, add exactly five completed source decisions (four revisions/one retention) once only using the ledger encoder and full before/planned inverse audit. Current counts7224/7227/4483/2741 remain unchanged until then. Do not promote main, prune, create a separate requested package, commit orpush. Preserve seal8598 original failure/b successor, semantic8605 original diagnostic failure/b successor/first10reused cases, all proof and reference label8570/qualified8570b history. Builder guardv7/compatible configs outcomesv7/B49v5/B50v2 and B51releasev1 preserve every original dependency; never substitute a mutable builder hash for original inverse guards.

Keep the full copied unfinished inventory and all earlier context/source/translation decisions. All four stories, earlier translated dialogue, shared town/shop/random scenes, Help/remaining prose, all207 names/roles/aliases/custom names and retrospective early-break checks remain active. Retain contraction/question-tag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractors104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159-versus-Retainer and older normal-end/nineteenth-cell/B47/B48/B50 metadata leads. Retain all native versus actual gameplay scope limits, timing/RNG/RGB/calendar/followingcommand differences, and optional activation/effect semantics/location/customname/fullroute/hardware uncertainties. Graphics and later older-record technical re-audit remain separate.

Next clean candidate is already preserved: work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json and work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json. Do not re-open current B52 English until its clean source/menu/branch/opaque/end/name consumers are independently reviewed. Three speeches and two typed-choice labels are five candidate prose objects;the initial speech inventory's3uncredited positions did not yet include typed-choice labels and is not completion credit. Sourceglosses preserve intention versus confirmed hostility,prospective discovery,reckless boldness and一家 as a group rather than invented blood kinship. Bind approved person/faction spelling separately. Review original2100 at68 andits two full Japanese labels,0200/0300 sites,source83c2 at164,two end words and0100 ancestry before assigning native branch semantics or observed paths. Event52/action53 requires30/excludes74;do not infer full chronology from adjacency. Keep the full all-four-story/shared-town-shop/random/Help/name/retro-wrap goal active and graphics/later older-record re-audit separate.'''

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
    from dk4tool.patch import hodram_B51_editorial_v1 as owned
    owned.check_dependencies(data['atomic_configuration'])
    assert data['predecessor_compatibility_completed']['whole_registered_V8543_ROM_byte_exact']
    assert data['builder_validation_completed']['negative_count']==25 and len(data['builder_validation_completed']['positives'])==5
    assert data['atomic_positives']['cases'][0]['report']==data['atomic_positives']['cases'][1]['report']
    assert data['atomic_negatives']['negative_count']==17 and data['atomic_negatives']['zero_commits_andwhole_input_unchanged_forall_failures']
    assert data['wrong_memory']['negative_count']==3 and data['wrong_memory']['no_digest_orsemantic_bypass']
    binding=data['atomic_binding'];registration=data['registration']
    assert binding['all17_actually_changed_semantic_precommit_cases_rejected_without_mutation'] and binding['lifecycle_reports_value_equal'] and binding['all3_genuine_wrong_memory_inputs_rejected_withall_guards_active']
    assert registration['profile']=='all-routes-unified-v8609' and registration['expected_manifest_batches']==645
    assert sha(Path('translations/release_stack.json').read_bytes())==registration['registry_after_sha256']
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==registration['builder_after_sha256']
    tests=data['regressions'];assert tests['terminal'] and tests['returncode']==0 and '110 passed' in Path(tests['log']).read_text('utf-8') and sha(Path(tests['log']).read_bytes())==tests['log_sha256']
    assert data['B52_clean']['source_only_no_current_English_exposed_orused'] and not data['B52_clean']['inventory_failures']
    gloss=data['B52_gloss'];assert gloss['all3_clean_utterances_andtwo_choices_glossed_before_current_English'] and gloss['current_English_dialogue_bodies_andchoice_labels_still_unconsulted']
    assert len(gloss['groups'][0]['records'])==3 and len(gloss['source_typed_choice']['labels'])==2 and len(gloss['groups'][0]['commands'])==14
    assert gloss['source_unresolved_controls']['final_high_bit_end_not_assumed_normal_zero_return'] and gloss['new_credit']==0
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
        pending = dict(status='five-all-gate-decisions-compatible-builder-atomic-pass-registered-V8609-build-patch-startup-credit-pending',
            file_path='/data/SC1.DK4', blocks=[51], records=5, proposed_revisions=4, justified_retentions=1,
            scoped_name_retentions=4, source_commands=20, source_relative_sites=8, source_query_sites=2, source_FE_panels=0,
            source_selector_values=[113, 1, 113, 18, 16], manuscript=PROOFS['manuscript'], names=PROOFS['names'], proofs=PROOFS,
            records_with_exact_source_current_andresearch_final_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True, all_five_formatting_gates_true=True, frozen_policy_negative_cases=322, production_reconstruction_negatives=20, production_native_negatives=10, production_loader_negatives=5, production_comparison_negatives=4, production_control_negatives=6, production_actual_negatives=5, current_English_dialogue_bodies_reviewed=True,
            automatic_fullwidth_pages=5, available_width_px=216, line_count_infos=2, warnings=0, waivers=0,
            logical_alignment_cases=20, compiled_alignment_cases=20, fresh_stored_parity_alignments=4, exact_stored_alignment_reuse=16,
            stored_block_bytes=400, stored_logical_end=400, stored_zero_tail_bytes=0, normal_stored_value_carry_cases=25,
            original_caller_result_channel_cases=50, structural_path_cases=10, actual_B51_emulator_runs=2, actual_B51_frames=20002, actual_B51_complete_body_name_holds=56, actual_observed_speech_count=4, actual_unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
            all324_unowned_blocks_andwhole_source_current_inverses_pass=True, all_independent_production_readers_compatible_builder_andatomic_pass=True,experimental_V8609_registered=True,registered_build_patch_ownstartup_andcredit_pending=True,
            next_clean_B52_source_andgloss=deepcopy(data['B52_gloss']),next_clean_B52_physical_speeches=3,next_clean_B52_typed_choice_labels=2,next_clean_B52_current_English_unread=True,
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
            prefix = ('# Current editorial handoff - V8618; V8543 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8618: B51 registered build pending; B52 three clean speeches and two choices glossed\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8618 staged: six targets, five uncredited all-gate/frozen-policy/all-production decisions. Exact inverse audit next.')
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
            print('V8618 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
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
            print('V8618 applied; V8543 and all completion counters unchanged. Full goal active.')
        else:
            assert read(ROOT / 'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified = deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()), previous_verified_handoff=str(PRIOR), previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT, unfinished_scope=SCOPE, pending_source_batch=KEY, next_clean_exchange_not_selected=False,
                Hodram_B51_build_pending_B52_clean_first_checkpoint=deepcopy(new[KEY]), new_uncredited_source_positions=5,
                physical_speeches_pending=5, typed_choice_labels_pending=0, new_credit=0, new_emulator_runs=0, new_actual_frames=0, new_research_ROMs=0,
                all_new_native_jobs_terminal_andreaped=True, all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True)
            save(VERIFY / 'verified_handoff.json', verified)
            print('Verified V8619/current V8543: 7224 completed; B51 four revisions/one retention/allfivegates/frozenpolicy322/allproduction readers pass; V8609 registered; build/patch/ownstartup/credit pending. Full objective active.')
