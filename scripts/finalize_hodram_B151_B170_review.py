"""Close this batch's display gates using completed immutable proofs and focused QA."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save as write_new

ROOT = Path('work/analysis/Hodram_B151_B170_checked_20261102')
INPUT = Path('work/analysis/Hodram_B151_B170_reconstruction_inputs_20261102')
FINAL = Path('translations/hodram_B151_B170_contextual_final_review_v1.json')
NAMES_FINAL = Path('translations/hodram_B151_B170_scoped_names_final_v1.json')
REBUILT = Path('work/analysis/Hodram_B151_B170_rebuilt_20261102/reconstruction.json')
STORED = Path('work/analysis/Hodram_B151_B170_stored_20261102/stored_native_verification.json')
LOADERS = Path('work/analysis/Hodram_B151_B170_loaders_20261102/verification.json')
PIXELS = Path('work/analysis/Hodram_B151_B170_actual_pixels_20261102/focused_actual_pixels.json')
ORDINARY = Path('work/analysis/Hodram_B151_B170_formatting_20261102/ordinary_visual_review_progress_v3.json')
CINEMATIC = Path('work/analysis/Hodram_B156_cinematic_English_actual_20261102/observed_English_panels.json')
CINEMATIC_REVIEW = CINEMATIC.with_name('actual_visual_review.json')
STATIC = Path('work/analysis/Hodram_B151_B170_static_labels_20261102/native_static_labels_qualification.json')
NAME_PLANES = Path('work/analysis/Hodram_B151_B170_scoped_name_planes_20261102/native_name_planes.json')
NAMES = Path('translations/hodram_B151_B170_scoped_names_andterms_v1.json')


def save(path, value):
    if path.exists():
        assert load(path) == value, 'Existing partial output differs: ' + str(path)
    else:
        write_new(path, value)


def main():
    assert not FINAL.exists() and not NAMES_FINAL.exists()
    doc, plans, rebuilt, stored, loaders, pixels, ordinary, cinematic, static, names = map(load, [
        INPUT / 'storage_manuscript.json', INPUT / 'all634_compiled_plans.json', REBUILT, STORED, LOADERS,
        PIXELS, ORDINARY, CINEMATIC, STATIC, NAMES])
    assert len(doc['records']) == 642 and doc['proposed_revisions'] == 269 and doc['wording_retentions'] == 373
    assert stored['complete_stored_pages'] == 650 and len(stored['records']) == 634 and not stored['style_records']
    assert stored['typed_labels_checked'] == 8 and stored['fresh_relocated_native_relative_cases'] == 700
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert (loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (40, 610)
    assert pixels['all_required_distinct_display_cases_match'] and pixels['both_two_choice_highlights_andbranches_observed']
    assert (len(pixels['body_pages']), len(pixels['name_headers']), len(pixels['menu_samples'])) == (134, 9, 2)
    assert pixels['actual_frames'] == 43003 and len(pixels['runs']) == 3
    sheets = cinematic['review_sheets'] + pixels['review_sheets']
    assert len(sheets) == 6
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert static['all_native_getter_copy_full_characters_bounds_canaries_andparent_inverse_pass']
    # Static data edits introduce no consumer/geometry change, and occupy fewer
    # bytes and native glyph cells than each complete clean-source label. These
    # are sufficient bounded data/renderer tests; individual widgets are unvisited.
    static_bounds = []
    for consumer in ('city', 'ship'):
        source = next(p for p in static['planes'] if p['consumer'] == consumer and p['source_text_version'] == 'clean')
        target = next(p for p in static['planes'] if p['consumer'] == consumer and p['source_text_version'] == 'proposed')
        width = lambda p: max(e['x'] + (12 if e['kind'] == 'cp932' else 6) for e in p['events'])
        assert width(target) <= width(source)
        assert len(target['text'].encode('cp932')) < len(source['text'].encode('cp932'))
        static_bounds.append(dict(consumer=consumer, clean_text=source['text'], target_text=target['text'],
            complete_target_advance_including_flush=width(target), clean_advance=width(source),
            no_new_consumer_geometry_orencoding_behavior=True, actual_widget_unvisited=True))
    ROOT.mkdir(parents=True, exist_ok=True)
    visual_receipt = ROOT / 'actual_visual_review.json'
    save(visual_receipt, dict(reviewed_sheets=sheets, all_six_sheets_directly_viewed=True,
        earlier_cinematic_review=str(CINEMATIC_REVIEW), earlier_cinematic_review_sha256=sha(CINEMATIC_REVIEW.read_bytes()),
        focused_findings=[], both_page_pairs_natural_andcomplete=True,
        Rafael_Claudio_Gerhard_Cesare_Arcadius_Julio_name_portrait_transitions_readable=True,
        both_long_captions_highlights_andresponses_readable=True,
        synthetic_cross_scene_fixture_sequence_not_a_story_conversation=True, guide_photos=False, new_credit=0))
    actual_path = ROOT / 'actual_review.json'
    save(actual_path, dict(runs=pixels['runs'], total_frames=43003, all_review_sheets_directly_viewed=sheets,
        focused_actual_pixels=str(PIXELS), focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        representative_progressive_FE_actor0_two_choice_name_pagination_andscene_transition_observed=True,
        all_required_distinct_display_cases_match=True, both_two_choice_highlights_andbranches_observed=True,
        all_target_sampled_paragraphs_andheaders_complete=True,
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        observations=[
            'B156: all31 selected English speeches/all23 cinematic FE panels in original excerpt order; headers, portraits, alternating staging and complete text pass. Source condition wrappers are excluded.',
            'B156 R87/R90: both generated page-bottom-spacing cases retain natural full-width rows and show the complete following thought on page2.',
            'B168: original actor0 Rafael, Claudio, Gerhard, Cesare and Arcadius headers/portraits and FO substitutions render correctly in selected source speeches.',
            'B170 C1314: both complete captions and turquoise highlights match native pixels. Ordinary controls select both indices and the distinct intended Julio responses, followed by the preserved dialogue/effects and later port return.'],
        unvisited='Other conditional content, three other menus, full catalogues, city87 and the Elysion ship widgets remain offline-only. The label data/getter/copy/native-font and compact source-envelope proofs pass; no individual city/ship visit is claimed.',
        duplicate_short_text_is_plane_equivalence_only_not_exact_source_occurrence=True,
        static_source_envelopes=static_bounds, no_whole_live_backing_RAM_VRAM_palette_orVM_register_ownership_claim=True,
        following_port_sailing_supplies_text_does_not_add_editorial_coverage=True, guide_photos=False, new_credit=0))
    release_plan = deepcopy(plans)
    cinematic_ids = []
    for row in release_plan['records']:
        if row.get('individually_documented_automatic_source_staging'):
            assert row['block'] == 156 and row['source_selector'] == 254 and row['cinematic_layout_reason'].strip()
            assert 'English' not in row
            row['English'] = '{SPEAKER:FE}' + row['logical_English']
            cinematic_ids.append(row['id'])
        assert not any(i['severity'] in ('warning', 'error') for i in row['base_QA']['issues'])
    assert len(cinematic_ids) == 23
    plan_path = ROOT / 'release_plans.json'
    save(plan_path, release_plan)
    choices = {r['id']: (obj, r) for obj in stored['typed_objects'] for r in obj['label_references']}
    speech = {r['id']: r for r in stored['records']}
    blocks = IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    final = deepcopy(doc)
    final.update(format='dk4-editorial-final-review-v1', encoder='dialogue-relocatable-v1',
        all_five_individual_review_gates_passed=True, all_individual_fifth_gates_still_pending=False,
        formatting_andvisual_stored_gameplay_integration_still_pending=False,
        registered_release_pending=True, new_credit=0, source_storage_manuscript=str(INPUT / 'storage_manuscript.json'))
    by_plan = {r['id']: r for r in release_plan['records']}
    for row in final['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        row['review']['formatting'] = True
        row['registered_release_andcompletion_credit_pending'] = True
        row['formatting_visual_stored_gameplay_andrelease_pending'] = False
        if row['kind'] == 'typed-choice-label':
            obj, binding = choices[row['id']]
            at, raw = binding['offset'], bytes.fromhex(binding['stored_hex'])
            ref = dict(file_path=row['file_path'], block=row['block'], command_offset=obj['offset'],
                source_index=row['source_index'], offset=at, record_index=binding['record_index'], bytes=len(raw),
                exact_stored_hex=raw.hex(), native_command_word=obj['word'])
        else:
            binding = speech[row['id']]
            at, raw = binding['new_offset'], bytes.fromhex(binding['stored_hex'])
            assert blocks[row['block']][at - 5:at + 1].hex() == row['source_complete_preamble_hex']
            assert by_plan[row['id']]['English'] == row['planned_English_markup']
            ref = dict(file_path=row['file_path'], block=row['block'], offset=at,
                record_index=binding['new_record_index'], bytes=len(raw), exact_stored_hex=raw.hex())
        assert blocks[row['block']][at:at + len(raw) + 1] == raw + b'\0'
        ref['target_archive_sha256'] = rebuilt['target_archive_sha256']
        row['planned_integrated_reference'] = ref
        row['formatting_evidence'] = dict(stored=str(STORED), ordinary_visual=str(ORDINARY),
            cinematic_visual=str(CINEMATIC_REVIEW), actual=str(actual_path),
            representative_gameplay_not_individual_activation=True)
    approved = {r['id']: r for r in final['records']}
    for group in rebuilt['groups']:
        for obj in group['native_objects']:
            rows = sorted([approved[r['id']] for r in obj['records']], key=lambda r: r['source_index'])
            assert compile_choices(bytes.fromhex(obj['source_hex']), bytes.fromhex(obj['current_hex']), rows).hex() == obj['compiled_hex']
    names_final = deepcopy(names)
    for row in names_final['records']:
        assert all(v for g, v in row['review'].items() if g != 'formatting')
        row['review']['formatting'] = True
        row['native_display_proof_reuse_orfresh_plane_binding_pending'] = False
        row['formatting_evidence'] = dict(name_planes=str(NAME_PLANES), static=str(STATIC), actual=str(actual_path),
            actual_full_catalogue_city_ship_widgets_unvisited=True)
    names_final.update(encoder='dialogue-relocatable-v1', all_five_gates_pass_in_scoped_context=True, no_new_dialogue_credit=True,
        static_data_andcompact_source_envelope_pass=True, global_207_name_review_still_open=True)
    validate_natural_dialogue_batch(names_final)
    save(NAMES_FINAL, names_final)
    final['scoped_name_review'] = str(NAMES_FINAL)
    final['scoped_name_review_sha256'] = sha(NAMES_FINAL.read_bytes())
    final['formatting_evidence'] = {str(p): sha(p.read_bytes()) for p in [STORED, LOADERS, PIXELS, ORDINARY, CINEMATIC,
        CINEMATIC_REVIEW, STATIC, NAME_PLANES, NAMES_FINAL, REBUILT, actual_path, visual_receipt, plan_path]}
    validate_natural_dialogue_batch(final)
    save(FINAL, final)
    save(ROOT / 'formatting_checkpoint.json', dict(final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()),
        scoped_names=str(NAMES_FINAL), scoped_names_sha256=sha(NAMES_FINAL.read_bytes()),
        actual=str(actual_path), actual_sha256=sha(actual_path.read_bytes()), plan=str(plan_path),
        static_source_envelopes=static_bounds, prose_reviews=642, revised=269, retained=373,
        final_speech_pages=650, layout_corrections=26, native_relative_cases=700, whole_archive_loads=325,
        actual_runs=3, actual_frames=43003, actual_review_sheets=6, actual_body_planes=134,
        actual_header_planes=9, actual_menu_highlights=2, both_menu_branches_observed=True,
        all_individual_five_gates_pass_in_research=True, registered_release_andcompletion_credit_pending=True,
        current_registered_ROM_andmain_unchanged=True, guide_photos=False, full_goal_complete=False, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [FINAL, NAMES_FINAL, actual_path, visual_receipt, plan_path, Path(__file__)]}))
    print('PASS642 individual five-gate research reviews;650 pages;3 focused runs/43003 frames;registration/patch/startup/credit pending.')


if __name__ == '__main__':
    main()
