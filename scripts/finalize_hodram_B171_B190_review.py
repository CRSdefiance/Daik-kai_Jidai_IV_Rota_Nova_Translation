"""Close individual research gates using immutable source/prose/native/actual evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_checked_20261104')
INPUT = Path('work/analysis/Hodram_B171_B190_storage_inputs_20261104')
PIXELS = Path('work/analysis/Hodram_B171_B190_actual_pixels_v2_20261104/focused_actual_pixels.json')
EARLIER_PIXELS = Path('work/analysis/Hodram_B171_B190_actual_pixels_20261104/focused_actual_pixels.json')
STORED = Path('work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json')
LOADERS = Path('work/analysis/Hodram_B171_B190_loaders_20261104/verification.json')
BINDINGS = Path('work/analysis/Hodram_B171_B190_storage_checked_20261104/stored_record_bindings_v1.json')
NAMES = Path('translations/hodram_B171_B190_scoped_names_andterms_v1.json')
NAME_PLANES = Path('work/analysis/Hodram_B171_B190_scoped_name_planes_20261104/native_name_planes.json')
FINAL = Path('translations/hodram_B171_B190_contextual_final_review_v1.json')
NAMES_FINAL = Path('translations/hodram_B171_B190_scoped_names_final_v1.json')


if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not NAMES_FINAL.exists()
    doc, pixels, stored, loaders, bindings, names, name_planes = map(load, [INPUT / 'storage_manuscript.json', PIXELS, STORED, LOADERS, BINDINGS, NAMES, NAME_PLANES])
    assert len(doc['records']) == 435 and (doc['proposed_revisions'], doc['wording_retentions']) == (195, 240)
    assert pixels['all_required_distinct_display_cases_match'] and not pixels['missing_required_cases'] and not pixels['header_findings']
    assert pixels['actual_frames'] == 85005 and len(pixels['runs']) == 5
    assert (len(pixels['body_pages']), len(pixels['name_headers']), len(pixels['menu_samples'])) == (413, 27, 2)
    assert len(pixels['review_sheets']) == 8 and pixels['full_pirate30_andtown130_native_body_sequence_matches_copied_source_commands']
    assert stored['complete_stored_pages'] == 439 and stored['fresh_relocated_native_relative_cases'] == 390
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['typed_labels_checked'] == 2
    assert (loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (40, 610)
    earlier = load(EARLIER_PIXELS)
    assert all(a['sha256'] == b['sha256'] for a, b in zip(earlier['review_sheets'][:5], pixels['review_sheets'][:5], strict=True))
    for sheet in pixels['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    # Source-attributed town contacts use the complete ordered native body calls.
    # The older equivalence-only gallery's town first/last labels are superseded.
    ROOT.mkdir()
    actual_visual = ROOT / 'actual_visual_review.json'
    save(actual_visual, dict(reviewed_sheets=pixels['review_sheets'], all8_sheets_directly_viewed_or_exact_image_reuse=True,
        first5_exact_hash_reuse_from_directly_viewed_original_sheets=True, final3_sheets_directly_viewed=True,
        prior_first5=str(EARLIER_PIXELS), prior_first5_sha256=sha(EARLIER_PIXELS.read_bytes()),
        findings=[], complete_names_portraits_text_pagination_andmenu_captions_readable=True,
        original_default_menu_samples_are_partial_cursor_phases=True,
        default_complete_highlight_frame4498_andrefusal_complete_highlight_frame4680_pass=True,
        no_ROM_orinput_change_to_resolve_cursor_sampling=True, guide_photos=False, new_credit=0))
    actual_path = ROOT / 'actual_review.json'
    actual = dict(runs=pixels['runs'], total_frames=85005, all_review_sheets_directly_viewed=pixels['review_sheets'],
        focused_actual_pixels=str(PIXELS), focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        representative_progressive_FE_two_choice_name_pagination_andscene_transition_observed=True,
        all_required_distinct_display_cases_match=True, all_target_sampled_paragraphs_andheaders_complete=True,
        both_two_choice_highlights_andbranches_observed=True,
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        observations=[
            'B171: original full source scene with its two-choice object and relative branches. Normal controller input observes both selections and their distinct source responses. First has the normal F; all sampled speaker names/portraits are complete.',
            'B171 R75/R95/R98: both pages of all three refined transitions match native planes. R101 is complete on one page. Generated bottom spacing and continuation guards preserve every visible character.',
            'B179: all30 original speech-body calls match the copied source sequence. All original transition/effect/cleanup commands remain. Thirteen FE panels, including the exact terminal-space/zero-ink case R47, display complete text; following port dialogue confirms the return.',
            'B180–B190: all130 native speech-body calls match the exact ordered copied source commands. Opening/ending text from all11 exchanges is visually reviewed. Source town-condition and market-effect commands are explicitly excluded; original location/event activation and economic outcomes are unvisited.',
            'The extra5001-frame run changes only screenshot density in the existing initial-menu window. A complete default highlight is observed at4498; the earlier partial samples show other cursor phases. Both complete captions, turquoise/gray backgrounds and both ordinary selections match native output.'],
        unvisited='B172–B178 and other B171 conditional branches remain offline-only. Full catalogues and individual item/city/sail widgets are unvisited. The town run verifies initialized dialogue/headers/FE text, not original town layout/control effects, natural conditional activation or market consequences.',
        target_capture_intervals=pixels['target_capture_intervals'],
        following_opening_port_sailing_text_not_added_to_editorial_or_target_gameplay_coverage=True,
        duplicate_pixels_alone_are_equivalence_only_ordered_scene_calls_also_required_for_source_attribution=True,
        no_whole_live_backing_RAM_VRAM_palette_orVM_register_ownership_claim=True, guide_photos=False, new_credit=0)
    save(actual_path, actual)
    final = deepcopy(doc)
    final.update(format='dk4-editorial-final-review-v1', encoder='dialogue-relocatable-v1',
        all_five_individual_review_gates_passed=True, all_individual_fifth_gates_still_pending=False,
        formatting_andvisual_stored_gameplay_integration_still_pending=False,
        registered_release_pending=True, new_credit=0)
    bound_by = {r['id']: r for r in bindings['records']}
    for row in final['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        bound = bound_by[row['id']]
        assert all(row[k] == bound[k] for k in ['source_reference', 'current_reference', 'finding', 'decision'])
        row['review']['formatting'] = True
        row['all_fifth_formatting_gates_still_pending'] = False
        row['formatting_visual_stored_gameplay_andregistered_release_pending'] = False
        row['registered_release_andcompletion_credit_pending'] = True
        ref = deepcopy(bound['stored_research_reference'])
        if row['kind'] == 'typed-choice-label':
            ref['native_command_word'] = 0x2100
        row['planned_integrated_reference'] = ref
        row['formatting_evidence'] = dict(stored=str(STORED), individual_storage_bindings=str(BINDINGS),
            speech_visual='work/analysis/Hodram_B171_B190_formatting_20261102/speech_display_approved_20261104/visual_approval.json',
            actual=str(actual_path), representative_gameplay_not_individual_natural_activation=True)
    for group in load('work/analysis/Hodram_B171_B190_rebuilt_20261104/reconstruction.json')['groups']:
        for obj in group['native_objects']:
            rows = sorted([r for r in final['records'] if r['id'] in {r['id'] for r in obj['records']}], key=lambda r: r['source_index'])
            assert compile_choices(bytes.fromhex(obj['source_hex']), bytes.fromhex(obj['current_hex']), rows).hex() == obj['compiled_hex']
    names_final = deepcopy(names)
    assert name_planes['all_current_names_ASCII_andfull_characters_fit_original216px'] and len(names_final['records']) == 49
    for row in names_final['records']:
        assert all(v for g, v in row['review'].items() if g != 'formatting')
        row['review']['formatting'] = True
        row['native_display_proof_reuse_orfresh_plane_binding_pending'] = False
        row['formatting_evidence'] = dict(name_planes=str(NAME_PLANES), actual=str(actual_path),
            source_term_field_bindings_unchanged=True, no_name_orstatic_term_data_change=True,
            full_catalogue_andindividual_item_city_sail_widgets_unvisited=True)
    names_final.update(encoder='dialogue-relocatable-v1', all_five_gates_pass_in_scoped_context=True,
        all_fifth_formatting_gates_pending=False, no_new_dialogue_credit=True, global_207_name_review_still_open=True)
    validate_natural_dialogue_batch(names_final)
    save(NAMES_FINAL, names_final)
    final.update(scoped_name_review=str(NAMES_FINAL), scoped_name_review_sha256=sha(NAMES_FINAL.read_bytes()),
        formatting_evidence={str(p): sha(p.read_bytes()) for p in [STORED, LOADERS, BINDINGS, PIXELS, NAME_PLANES,
            NAMES_FINAL, actual_path, actual_visual, Path(__file__)]})
    validate_natural_dialogue_batch(final)
    save(FINAL, final)
    plan = load(INPUT / 'all433_compiled_plans.json')
    save(ROOT / 'release_plans.json', plan)
    save(ROOT / 'formatting_checkpoint.json', dict(final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()),
        scoped_names=str(NAMES_FINAL), scoped_names_sha256=sha(NAMES_FINAL.read_bytes()), actual=str(actual_path),
        actual_sha256=sha(actual_path.read_bytes()), prose_reviews=435, revised=195, retained=240, final_speech_pages=439,
        layout_corrections=15, native_relative_cases=390, whole_archive_loads=325, actual_runs=5, actual_frames=85005,
        actual_review_sheets=8, actual_body_planes=413, actual_header_planes=27, actual_menu_highlights=2,
        all_individual_five_gates_pass_in_research=True, registered_release_andcompletion_credit_pending=True,
        current_registered_ROM_andmain_unchanged=True, guide_photos=False, full_goal_complete=False, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [FINAL, NAMES_FINAL, actual_path, actual_visual, ROOT / 'release_plans.json', Path(__file__)]}))
    print('PASS435 individual five-gate research reviews;439 pages;5 focused runs/85005frames. Registered integration/clean patch/own startup/credit remain.')
