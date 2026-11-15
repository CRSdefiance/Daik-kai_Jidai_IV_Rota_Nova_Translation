"""Close individual gates from existing exact prose, native, stored and actual proofs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B191_B210_checked_20261104')
INPUT = Path('work/analysis/Hodram_B191_B210_storage_inputs_20261104')
PIXELS = Path('work/analysis/Hodram_B191_B210_actual_pixels_20261104/focused_actual_pixels.json')
STORED = Path('work/analysis/Hodram_B191_B210_stored_20261104/stored_native_verification.json')
LOADERS = Path('work/analysis/Hodram_B191_B210_loaders_20261104/verification.json')
BINDINGS = Path('work/analysis/Hodram_B191_B210_storage_checked_20261104/stored_record_bindings_v1.json')
NAMES = Path('translations/hodram_B191_B210_scoped_names_andterms_v1.json')
NAME_PLANES = Path('work/analysis/Hodram_B191_B210_scoped_name_planes_20261104/native_name_planes.json')
FINAL = Path('translations/hodram_B191_B210_contextual_final_review_v1.json')
NAMES_FINAL = Path('translations/hodram_B191_B210_scoped_names_final_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not NAMES_FINAL.exists()
    doc, pixels, stored, loaders, bindings, names, name_planes = map(load, [INPUT / 'storage_manuscript.json', PIXELS, STORED, LOADERS, BINDINGS, NAMES, NAME_PLANES])
    assert len(doc['records']) == 373 and (doc['proposed_revisions'], doc['wording_retentions']) == (154, 219)
    assert pixels['all_required_distinct_display_cases_match'] and not pixels['missing_required_cases'] and not pixels['header_findings']
    assert pixels['actual_frames'] == 98006 and len(pixels['runs']) == 6
    assert (len(pixels['body_pages']), len(pixels['name_headers']), len(pixels['menu_samples'])) == (468, 36, 4)
    assert len(pixels['review_sheets']) == 9
    assert {k:v['calls'] for k,v in pixels['ordered_linear_scene_sequences'].items()} == dict(town_exchanges=128, castle_letter=20, parrot=17)
    menu_cases = {(r['block'], r['source_command_offset'], r['selected_option']) for r in pixels['menu_samples']}
    assert menu_cases == {(201,230,0), (201,230,2), (210,956,0), (210,1126,0)}
    assert stored['complete_stored_pages'] == 355 and stored['fresh_relocated_native_relative_cases'] == 540
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['typed_labels_checked'] == 21
    assert (loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (40, 610)
    for sheet in pixels['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    ROOT.mkdir()
    actual_visual = ROOT / 'actual_visual_review.json'
    save(actual_visual, dict(reviewed_sheets=pixels['review_sheets'], all9_sheets_directly_viewed=True,
        findings=[], complete_names_portraits_text_pagination_andmenu_captions_readable=True,
        three_choice_indices0_and2_andtwo_distinct_two_choice_objects_observed=True,
        actual_replays_for_dense_cursor_sampling_needed=False, guide_photos=False, new_credit=0))
    actual_path = ROOT / 'actual_review.json'
    actual = dict(runs=pixels['runs'], total_frames=98006, all_review_sheets_directly_viewed=pixels['review_sheets'],
        focused_actual_pixels=str(PIXELS), focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        representative_progressive_FE_mixed_choice_name_pagination_andscene_transition_observed=True,
        all_required_distinct_display_cases_match=True, all_target_sampled_paragraphs_andheaders_complete=True,
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        observations=[
            'B191–B199: all128 speech calls match the copied source command order. Opening/ending samples from allnine exchanges were directly viewed. Conditions/market effects andoriginal town layout are excluded.',
            'B201: original complete three-choice scene commands/relative branches retained. Normal inputs choose0 and2 with distinct source responses. Allthree captions andboth sampled highlights match complete native planes. Ian R74 uses the reviewed two-row opening.',
            'B208: all20 source speech calls match in order,with the retained native Shachihoko award effect between them. Allfour letter panels are viewed,including R65 with its corrected FE guard width.',
            'B209: all17 source speech calls match in order. Progressive/FE echo staging,portrait changes andreturn to the opening port are observed.',
            'B210: both pages of R37 andR70 are complete;the planned final sentence stays together on page2. Allfour captions in its two menus are complete;ordinary default selections observe their source responses.',
            'Retained 0xA000 item-award commands generate interstitial modal text. These are explicitly listed separately andadd no SC1 speech coverage ornew editorial credit.'],
        unvisited='B200 andB202–B207 remain offline-only. B201 Pass/index1 response andother conditional branches,including the roster-dependent Sera passage inB210,are unvisited. Full catalogues andindividual item/city widgets are not established by name literal planes. Initialized fixtures do not establish outer activation,earned wealth/items,original location,full chronology,full route orhardware behavior.',
        target_capture_intervals=pixels['target_capture_intervals'],
        following_opening_port_sailing_text_not_added_to_editorial_or_target_gameplay_coverage=True,
        duplicate_pixels_alone_are_equivalence_only_ordered_scene_calls_required_for_linear_source_attribution=True,
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
        row['planned_integrated_reference'] = deepcopy(bound['stored_research_reference'])
        row['formatting_evidence'] = dict(stored=str(STORED), individual_storage_bindings=str(BINDINGS),
            speech_visual='work/analysis/Hodram_B191_B210_formatting_20261104/speech_display_approved_20261104/visual_approval.json',
            actual=str(actual_path), representative_gameplay_not_individual_natural_activation=True)
    for group in load('work/analysis/Hodram_B191_B210_rebuilt_20261104/reconstruction.json')['groups']:
        for obj in group['native_objects']:
            rows = sorted([r for r in final['records'] if r['id'] in {r['id'] for r in obj['records']}], key=lambda r:r['source_index'])
            assert compile_choices(bytes.fromhex(obj['source_hex']), bytes.fromhex(obj['current_hex']), rows).hex() == obj['compiled_hex']
    names_final = deepcopy(names)
    assert name_planes['all_current_names_ASCII_andfull_characters_fit_original216px'] and len(names_final['records']) == 70
    for row in names_final['records']:
        assert all(v for g,v in row['review'].items() if g != 'formatting')
        row['review']['formatting'] = True
        row['native_display_proof_reuse_orfresh_plane_binding_pending'] = False
        row['formatting_evidence'] = dict(name_planes=str(NAME_PLANES), actual=str(actual_path),
            visual=str(INPUT / 'scoped_name_visual_approval.json'), source_term_field_bindings_unchanged=True,
            no_name_orstatic_term_data_change=True, full_catalogue_andindividual_item_city_widgets_unvisited=True)
    names_final.update(encoder='dialogue-relocatable-v1', all_five_gates_pass_in_scoped_context=True,
        all_fifth_formatting_gates_pending=False, no_new_dialogue_credit=True, global_207_name_review_still_open=True)
    validate_natural_dialogue_batch(names_final); save(NAMES_FINAL, names_final)
    final.update(scoped_name_review=str(NAMES_FINAL), scoped_name_review_sha256=sha(NAMES_FINAL.read_bytes()),
        formatting_evidence={str(p):sha(p.read_bytes()) for p in [STORED, LOADERS, BINDINGS, PIXELS, NAME_PLANES,
            NAMES_FINAL, actual_path, actual_visual, INPUT / 'scoped_name_visual_approval.json', Path(__file__)]})
    validate_natural_dialogue_batch(final); save(FINAL, final)
    save(ROOT / 'release_plans.json', load(INPUT / 'all352_compiled_plans.json'))
    save(ROOT / 'formatting_checkpoint.json', dict(final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()),
        scoped_names=str(NAMES_FINAL), scoped_names_sha256=sha(NAMES_FINAL.read_bytes()), actual=str(actual_path),
        actual_sha256=sha(actual_path.read_bytes()), prose_reviews=373, revised=154, retained=219, final_speech_pages=355,
        layout_corrections=4, native_relative_cases=540, whole_archive_loads=325, actual_runs=6, actual_frames=98006,
        actual_review_sheets=9, actual_body_planes=468, actual_header_planes=36, actual_menu_highlights=4,
        all_individual_five_gates_pass_in_research=True, registered_release_andcompletion_credit_pending=True,
        current_registered_ROM_andmain_unchanged=True, guide_photos=False, full_goal_complete=False, new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [FINAL, NAMES_FINAL, actual_path, actual_visual, ROOT / 'release_plans.json', Path(__file__)]}))
    print('PASS373 individual five-gate research reviews;355 pages;six focused runs/98006frames. Registered integration remains.')
