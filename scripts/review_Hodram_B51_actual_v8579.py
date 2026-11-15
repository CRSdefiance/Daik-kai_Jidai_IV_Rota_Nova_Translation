"""Review all observed B51 pages, headers, returns and later visual differences."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_actual_review_v8579')
ACTUAL = Path('work/analysis/Hodram_B51_actual_v8576/B51/paired_actual_dialogue_headers_flow_returns.json')
COMPARE = Path('work/analysis/Hodram_B51_comparison_v8577/paired_selected_path_comparison.json')
DIFFERENCES = Path('work/analysis/Hodram_B51_difference_view_v8578/sheet.json')
STORED = Path('work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json')
OLD = Path('translations/hodram_B51_editorial_manuscript_v2.json')
DOC = Path('translations/hodram_B51_editorial_manuscript_v3.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists()
    actual, comparison, differences, stored, old = map(read, [ACTUAL, COMPARE, DIFFERENCES, STORED, OLD])
    assert not actual['unresolved'] and actual['all_observed_complete_body_name_holds_andnative_flow_pass']
    groups = actual['groups']
    g = comparison['groups'][0]
    assert len(groups) == 2 and [len(x['speeches']) for x in groups] == [4, 4]
    assert [sum(len(s['complete_holds']) for s in x['speeches']) for x in groups] == [28, 28]
    assert [x['normal_return']['frame'] for x in groups] == [4736, 4734]
    assert [x['normal_return']['native_result'] for x in groups] == [[0, 0], [0, 0]]
    assert all(x['unvisited_conditional_text_IDs'] == ['DK4_MES_B51_R0032'] and len(x['command_pairs']) == 23 for x in groups)
    observed = ['DK4_MES_B51_R0006', 'DK4_MES_B51_R0010', 'DK4_MES_B51_R0014', 'DK4_MES_B51_R0039']
    assert all([s['id'] for s in group['speeches']] == observed for group in groups)
    assert comparison['total_actual_frames'] == 20002 and len(g['later_RGB_comparisons']) == 89 and g['later_RGB_difference_count'] == 3
    assert all(g['five_native_component_equality'].values()) and g['whole_actors_equal']
    assert [v['captain_ID'] for v in g['final_native_values']] == [1, 1]
    assert g['final_PRNG_seeds'] == list(map(int, ['2294662370', '3116913577']))
    rng = [c for c in g['command_comparison_differences'] if any('RNG' in key for key in c['different_fields'])]
    assert not rng and not g['UI_request_differences'] and len(g['duration_differences']) == 2
    assert [(r['source_command_ordinal'], r['clean'], r['revised']) for r in g['duration_differences']] == [(3, 241, 240), (14, 241, 240)]
    assert [r['frame'] for r in differences['all_nonidentical_later_pairs']] == [4870, 5650, 5830]
    assert all(s['upper_scene_portrait_RGB_equal'] and s['complete_header_region_RGB_equal'] for s in g['scene_pairs'])
    sheets = actual['review_sheets'] + comparison['review_sheets'] + [differences['sheet']]
    assert len(sheets) == 3
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    findings = [
        '4870: a two-row strip of pixels differs in the Port label area, bounding box[210,242,250,244]. The measured difference is retained without assigning a scheduling/rendering cause.',
        '5650: the later original All right. menu first-row highlight differs.',
        '5830: the original A-button prompt visibility differs.',
    ]
    refs = {r['id']: r for r in stored['records']}
    assert stored['manuscript_sha256'] == sha(OLD.read_bytes()) and len(refs) == 5
    rows = []
    for original in old['records']:
        row = deepcopy(original)
        ref = refs[row['id']]
        assert all(row[key] == ref[key] for key in ['source_reference', 'current_reference', 'source_hex', 'current_hex', 'compiled_hex'])
        row.update(final_reference=deepcopy(ref['final_reference']), final_stored_hex=ref['stored_hex'],
            compiler_owned_parity_space=ref['compiler_owned_parity_space'], exact_final_reference_proof=str(STORED), exact_final_reference_proof_sha256=sha(STORED.read_bytes()),
            actual_B51_source_andEnglish_body_header_covered=row['id'] in observed,
            actual_B51_contextual_scope='complete initialized opening entry fixture with original source branches and identical ordinary inputs',
            actual_B51_conditional_not_visited=row['id'] not in observed,
            actual_B51_unvisited_scope_reason=None if row['id'] in observed else 'Charles is omitted by the original unforced raw predicate result0. His complete native body, exact actor18/name/voice, guarded alignments, bounds/pagination and all relocated branch extents already pass offline. No individual gameplay visit or forced predicate is required by the agreed representative-test scope.',
            formal_frozen_policy_independent_production_atomic_andregistered_integration_pending=True)
        assert row['english'] == original['english'] and row['review'] == original['review'] and not row['review']['formatting']
        rows.append(row)
    doc = deepcopy(old)
    doc.update(records=rows, predecessor_manuscript=str(OLD), predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        source_current_final_references_complete=True, actual_evidence=str(ACTUAL), actual_evidence_sha256=sha(ACTUAL.read_bytes()),
        actual_comparison=str(COMPARE), actual_comparison_sha256=sha(COMPARE.read_bytes()),
        actual_observed_source_speech_IDs=observed, unvisited_conditional_source_speech_IDs=['DK4_MES_B51_R0032'],
        actual_observed_name_header_actor_IDs=[1, 16, 113], actor18_name_header_native_offline_only=True,
        actual_frames=20002, actual_emulator_runs=2,
        original_unforced_query_results_andselected_relative_flow_normal_returns_andtransitions_pass=True,
        source_opaque_effect_semantics_outer_eligibility_original_location_natural_activation_customnames_fullroute_hardware_andfuture_simulation_unproven=True,
        all_five_formatting_gates_still_false=True,
        status='contextual-native-stored-reference-andrepresentative-actual-reviewed-frozen-policy-atomic-registered-pending')
    save(DOC, doc)
    ROOT.mkdir(parents=True)
    save(ROOT / 'whole_exchange_review.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), predecessor_manuscript=str(OLD),
        predecessor_manuscript_sha256=sha(OLD.read_bytes()), actual=str(ACTUAL), actual_sha256=sha(ACTUAL.read_bytes()),
        comparison=str(COMPARE), comparison_sha256=sha(COMPARE.read_bytes()), directly_viewed_sheets=sheets, all_three_sheets_directly_viewed=True,
        actual_frames=20002, actual_emulator_runs=2, actual_source_speech_IDs=observed,
        actual_complete_source_andEnglish_body_name_holds=56, all_eight_observed_native_singlepages_andfull_name_headers_directly_viewed=True,
        actual_progressive_actor_IDs=[113, 1, 16], actual_full_nameplates=['Port Worker', 'Hodram Bergstrom', 'Gerhard Adernkatz'],
        complete_first_internal_final_characters_bounds_singlepages_names_andportraits_pass=True,
        unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
        Charles_actor18_complete_source_compiled_stored_macro_name_glyph_bounds_andrelocated_branches_bound_offline_not_actual=True,
        both_actual_queries_result0_preserved_without_forcing=True, all_selected_relative_targets_andoriginal_opaque_controls_normalends_preserved=True,
        normal_returns=g['normal_returns'], timing_differences=g['duration_differences'], different_script_boundary_RNG_values=rng,
        UI_request_differences=g['UI_request_differences'], later_RGB_direct_view_findings=findings, later_RGB_equal_pairs=86, later_RGB_total_pairs=89,
        final_PRNG_seeds=g['final_PRNG_seeds'], five_checked_native_components_equal=g['five_native_component_equality'], whole_actors_equal=True,
        raw_calendar_values_uninterpreted=g['raw_calendars_uninterpreted'], following_original_commands_with_frames_not_identical=not g['following_commands_equal'],
        representative_entry_fixture_not_natural_optional_activation_original_location_earnedinventory_customnames_fullroute_orhardware=True,
        no_every_frame_causality_future_RNG_outcomes_orbroad_simulation_equivalence_claim=True,
        no_input_retiming_capture_replay_orstate_flag_roster_role_inventory_seed_result_forcing=True,
        source_current_final_refs_added_without_word_control_orreview_gate_changes=True, all_five_formatting_gates_false=True,
        no_ROM_registration_orcompletion_credit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [ACTUAL, COMPARE, DIFFERENCES, STORED, OLD, DOC, Path(__file__)]}))
    print('Viewed eight actual B51 pages/56 complete body-name holds, portraits/headers, normal transitions and all three later RGB differences. Charles stays explicitly offline/unvisited. Manuscriptv3 adds exact final references; frozen policy/atomic/registered pending, zero credit.')
