"""Qualify existing B52 captures, exact input prefixes and all measured limits.

This reader does not run an emulator or native CPU probe and adds no review credit.
"""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_actual_review_v8659')
PROOFS = {
    'stored': 'work/analysis/Hodram_B52_stored_v8643/stored_native_controls_andrefs.json',
    'independent': 'work/analysis/Hodram_B52_independent_v8644/independent_reconstruction.json',
    'reference': 'work/analysis/Hodram_B52_reference_v8645/research_image_receipt.json',
    'loaders': 'work/analysis/Hodram_B52_loaders_v8646/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
    'references': 'work/analysis/Hodram_B52_references_v8647/source_current_final_map.json',
    'fixtures': 'work/analysis/Hodram_B52_fixtures_v8648/two_whole_scripts.json',
    'withdrawal': 'work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json',
    'opposition': 'work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json',
    'menu': 'work/analysis/Hodram_B52_actual_menu_RGB_v8654/actual_menu_RGB_glyph_geometry_highlight.json',
    'long_comparison': 'work/analysis/Hodram_B52_comparison_v8655/paired_selected_path_comparison.json',
    'focus_basis': 'work/analysis/Hodram_B52_postreturn_focus_tools_v8656/focus_basis.json',
    'focus': 'work/analysis/Hodram_B52_focus_actual_v8657/B52/paired_actual_dialogue_headers_flow_returns.json',
    'focus_comparison': 'work/analysis/Hodram_B52_focus_comparison_v8658/paired_selected_path_comparison.json',
    'manuscript': 'translations/hodram_B52_editorial_manuscript_v3.json',
    'names': 'translations/hodram_B52_speaker_name_review_v1.json',
}


def bound(path, expected=None):
    path = Path(path)
    digest = sha(path.read_bytes())
    if expected is not None:
        assert digest == expected, str(path)
    return {'path': str(path), 'sha256': digest}


if __name__ == '__main__':
    assert not ROOT.exists()
    data = {key: read(path) for key, path in PROOFS.items()}
    dependencies = {str(p): sha(Path(p).read_bytes()) for p in PROOFS.values()}
    # Revalidate recorded identities without replaying completed measurements.
    for key, packet in data.items():
        for path, digest in packet.get('evidence', {}).items():
            if isinstance(digest, str) and len(digest) == 64:
                bound(path, digest)
                dependencies[path] = digest
    records, total_frames, total_holds, pages = [], 0, 0, 0
    unique = set()
    run_roots = {
        'withdrawal': 'work/analysis/Hodram_B52_scene_runs_v8649',
        'opposition': 'work/analysis/Hodram_B52_opposition_runs_v8652',
        'focus': 'work/analysis/Hodram_B52_postreturn_focus_runs_v8656',
    }
    input_sets = {}
    for case in ['withdrawal', 'opposition', 'focus']:
        packet = data[case]
        assert not packet['unresolved'] and packet['all_observed_complete_body_name_holds_andnative_flow_pass']
        assert len(packet['groups']) == 2
        case_holds = 0
        for group in packet['groups']:
            version = group['version']
            root = Path(run_roots[case]) / ('route1_B52_' + version)
            terminal, plan = read(root / 'terminal.json'), read(root / 'run_plan.json')
            assert terminal['terminal'] and terminal['all_callbacks_readonly_andhost_slots_restored']
            bound(terminal['report'], terminal['report_sha256'])
            bound(terminal['observer'], terminal['observer_sha256'])
            bound(terminal['run_plan'], terminal['run_plan_sha256'])
            bound(plan['inputs'], plan['inputs_sha256'])
            schedule = read(plan['inputs'])
            input_sets[case, version] = schedule
            for p in [root / 'terminal.json', root / 'run_plan.json', Path(plan['inputs'])]:
                dependencies[str(p)] = sha(p.read_bytes())
            assert group['all_selected_payloads_exact_own_ROM_andcallbacks_readonly']
            assert group['all_selected_command_boundaries_follow_native_relative_results']
            expected_ids = ['DK4_MES_B52_R0006', 'DK4_MES_B52_R0033' if case == 'opposition' else 'DK4_MES_B52_R0021']
            assert [r['id'] for r in group['speeches']] == expected_ids
            result = group['script_return' if case == 'opposition' else 'normal_return']
            assert result['native_result'] == ([1, 0] if case == 'opposition' else [0, 0])
            assert result['complete_four_byte_end']
            for speech in group['speeches']:
                unique.add(speech['id'])
                assert speech['name'] == 'Port Worker' and speech['source_selector'] == 113 and speech['pages'] == 1
                pages += speech['pages']
                assert speech['complete_holds']
                for hold in speech['complete_holds']:
                    bound(hold['capture'], hold['sha256'])
                    assert hold['complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal']
                    assert hold['complete_name_mask_equal'] and hold['actual_name'] == 'Port Worker'
                    # Historical FE-specific booleans are inapplicable here: no B52 FE site.
                    assert hold['native_geometry'] == [216, 64]
                case_holds += len(speech['complete_holds'])
            assert len(group['command_pairs']) == (18 if case == 'opposition' else 14)
            total_frames += group['actual_frames']
        assert input_sets[case, 'clean_Japanese'] == input_sets[case, 'revised_English']
        assert case_holds == 46
        total_holds += case_holds
        records.append(dict(case=case, complete_holds=case_holds, actual_runs=2,
                            frames=sum(g['actual_frames'] for g in packet['groups']),
                            original_actual_results=deepcopy(packet['groups'])))
    for version in ['clean_Japanese', 'revised_English']:
        long_inputs = input_sets['withdrawal', version]
        focused = input_sets['focus', version]
        assert focused == [entry for entry in long_inputs if entry['start'] < 4485]
        assert focused[-1] == dict(start=4480, duration=5, buttons=['A'])
        assert input_sets['opposition', version] == sorted(
            long_inputs + [dict(start=4100, duration=5, buttons=['DOWN'])], key=lambda r: r['start'])
    assert (total_frames, total_holds, pages) == (50406, 138, 12)
    assert unique == {'DK4_MES_B52_R0006', 'DK4_MES_B52_R0021', 'DK4_MES_B52_R0033'}
    menu = data['menu']
    assert menu['actual_menu_samples'] == 12 and menu['complete_actual_caption_glyph_andbackground_checks'] == 24
    assert menu['original_Japanese_andreviewed_English_two_choices_glyphs_centering_bounds_andselected_highlights_pass']
    assert menu['no_new_owner_pointer_RAM_VRAM_palette_orunowned_backing_byte_identity_claim']
    comparisons = data['long_comparison']['groups'] + data['focus_comparison']['groups']
    assert len(comparisons) == 3
    long0, long1, focus = comparisons
    assert [g['later_RGB_difference_count'] for g in comparisons] == [46, 13, 0]
    assert [len(g['later_RGB_comparisons']) for g in comparisons] == [93, 93, 13]
    assert long0['five_native_component_equality'] == dict(state=False, models=False, persistent_objects=False, tasks=True, calendar=False)
    assert long0['whole_actors_equal'] is False
    assert all(all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] for g in [long1, focus])
    assert focus['final_PRNG_seeds'] == [613908813, 613908813] and focus['following_commands'] == [[], []]
    assert focus['raw_calendars_uninterpreted'] == [dict(ticks=0, original_zero_based_date=[0, 0, 0])] * 2
    sheets = []
    for key in ['withdrawal', 'opposition', 'focus', 'long_comparison', 'focus_comparison']:
        sheets.extend(deepcopy(data[key]['review_sheets']))
    sheets.append(deepcopy(menu['review_sheet']))
    for sheet in sheets:
        bound(sheet['path'], sheet['sha256'])
    doc = deepcopy(data['manuscript'])
    doc['predecessor_manuscript'] = PROOFS['manuscript']
    doc['predecessor_manuscript_sha256'] = dependencies[PROOFS['manuscript']]
    for collection, source_rows in [('records', data['stored']['records']), ('typed_choice_records', data['stored']['typed_choice_records'])]:
        by_id = {r['id']: r for r in source_rows}
        for row in doc[collection]:
            stored = by_id[row['id']]
            assert row['source_reference'] == stored['source_reference'] and row['current_reference'] == stored['current_reference']
            row['stored_final_reference'] = deepcopy(stored['final_reference'])
            row['stored_native_evidence'] = bound(PROOFS['stored'])
            row['actual_review_evidence'] = str(ROOT / 'qualified_actual_review.json')
            row['actual_selected_path_coverage'] = ['withdrawal', 'opposition'] if row['id'].endswith('R0006') else (['opposition'] if row['id'].endswith(('R0013', 'R0033')) else ['withdrawal'])
            row['historical_pending_flags_are_retained_as_predecessor_evidence'] = True
            row['formal_policy_atomic_registered_release_andcompletion_credit_pending'] = True
            assert row['review']['formatting'] is False
    doc['status'] = 'stored-native-andactual-body-header-two-choice-paths-reviewed-formal-policy-andregistered-integration-pending'
    doc['actual_review_evidence'] = str(ROOT / 'qualified_actual_review.json')
    doc['no_new_ROM_registered_integration_orcompletion_credit'] = False
    doc['three_research_ROMs_exist_no_registered_B52_integration_orcompletion_credit'] = True
    doc['actual_controller_andinitialized_entry_scope'] = 'Six cold boots, identical paired schedules, all three unique speeches, two ordinary choice selections and both original end kinds. Current registered English names/UI are used in both Japanese-body and revised-English fixtures. Original optional-event eligibility/location/earned chronology, cancel availability, full routes and hardware remain unobserved.'
    doc['long_run_withdrawal_divergence_retained'] = deepcopy(long0)
    doc['focus_only_immediate_state_matches_without_future_equivalence_orcausality_claim'] = deepcopy(focus)
    names = deepcopy(data['names'])
    names['predecessor'] = bound(PROOFS['names'])
    names['actual_review_evidence'] = str(ROOT / 'qualified_actual_review.json')
    names['actual_Port_Worker_header_holds'] = 138
    names['source_actor113_label_retained_complete_actual_glyphs_andportrait_scoped_to_B52'] = True
    names['no_actor34_actual_header_catalogue_orfull_name_review_claim'] = True
    # Preserve the earlier context's unvisited wording as history and qualify it explicitly.
    names['historical_context_pending_clauses_superseded_only_for_B52_initialized_selected_paths'] = True
    names_path = Path('translations/hodram_B52_speaker_name_review_v2.json')
    manuscript_path = Path('translations/hodram_B52_editorial_manuscript_v4.json')
    assert not names_path.exists() and not manuscript_path.exists()
    ROOT.mkdir(parents=True)
    save(names_path, names)
    doc['names_packet'] = str(names_path)
    doc['names_packet_sha256'] = sha(names_path.read_bytes())
    save(manuscript_path, doc)
    result = dict(
        existing_capture_results=records, comparisons=deepcopy(comparisons),
        all_recorded_dependencies_revalidated_without_native_oractual_replay=True,
        all_six_terminal_runs_callbacks_readonly_host_slots_restored=True,
        main_runs=4, main_frames=40004, main_holds=92, main_page_occurrences=8,
        focused_runs=2, focused_frames=10402, focused_holds=46, focused_page_occurrences=4,
        total_runs=6, total_frames=total_frames, total_holds=total_holds, total_page_occurrences=pages,
        unique_speeches=sorted(unique), actual_menu_samples=12, actual_caption_checks=24,
        exact_focus_schedule_is_unretimed_default_prefix_before4485=True,
        opposition_schedule_only_adds_ordinary_DOWN4100_duration5=True,
        source_andEnglish_both_ordinary_choices_andoriginal_normal0_flagged1_returns_observed=True,
        directly_viewed_sheets=sheets,
        review='Complete Japanese/English speech and Port Worker headers, actual choice glyphs/centering/highlights, portraits and following transitions reviewed. The focused sheet displays the same Stockholm resupply prompt at4570/4930/5201. Historical source-specific FE and pending flags are retained, not treated as new B51 or FE coverage.',
        long_withdrawal_later_component_actor_calendar_PRNG_and46_RGB_differences_preserved=True,
        long_opposition_matching_components_actors_butdifferent_PRNG_and13_RGB_differences_preserved=True,
        focused_withdrawal_all5_components_actors_PRNG_and13_RGB_pairs_match=True,
        no_causal_explanation_orfuture_simulation_equivalence_established=True,
        no_actual_owner_pointer_RAM_VRAM_palette_orunowned_backing_identity_claim=True,
        native_backing_bounds_remain_separate_offline_menu8636_proof=True,
        no_actual_cancel_availability_natural_activation_original_location_earned_story_fullroute_orhardware_claim=True,
        manuscript=bound(manuscript_path), names=bound(names_path),
        three_research_ROMs_preserved_registered_current_V8609_andmainV4701_unchanged=True,
        all_five_formatting_gates_still_false_formal_policy_atomic_registered_release_andcredit_pending=True,
        new_native_runs=0, new_emulator_runs=0, new_credit=0, full_goal_complete=False,
        evidence=dependencies, producer=bound(__file__))
    save(ROOT / 'qualified_actual_review.json', result)
    print('B52: six existing runs/50406 frames/138 complete holds/12 pages, all3 speeches, both choices/end kinds; focus input prefix exact. Long divergences retained. No replay/credit; formal integration pending.')
