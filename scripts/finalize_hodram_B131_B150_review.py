"""Close individual research gates after exact stored checks and representative gameplay."""
from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B131_B150_checked_20261102')
DOC = Path('translations/hodram_B131_B150_editorial_manuscript_v2.json')
FINAL = Path('translations/hodram_B131_B150_contextual_final_review_v1.json')
REBUILT = Path('work/analysis/Hodram_B131_B150_rebuilt_20261102/reconstruction.json')
STORED = Path('work/analysis/Hodram_B131_B150_stored_20261102/stored_native_verification.json')
LOADERS = Path('work/analysis/Hodram_B131_B150_loaders_20261102/verification.json')
DISPLAY = Path('work/analysis/Hodram_B131_B150_editorial_20261102')
VISUAL = DISPLAY / 'visual_review_progress_v7.json'
MENU = DISPLAY / 'menus_v1/menu_provider_and_planes_reviewed.json'
STYLES = DISPLAY / 'style_v1/compiled_style_objects.json'
NAME = Path('work/analysis/Hodram_B131_B150_name_native_20261102/native_name_fields_verification_reviewed.json')
NAMES = Path('translations/hodram_B131_B150_speaker_name_review_v1.json')
PIXELS = Path('work/analysis/Hodram_B131_B150_actual_pixels_20261102/focused_actual_pixels.json')
CONTROL = Path('work/analysis/Hodram_B133_source_control_20261102/source_control_result.json')
SHEETS = [Path('work/analysis/Hodram_B131_B150_actual_20261102/capture_sheets.json'),
          Path('work/analysis/Hodram_B131_B150_actual_second_choice_20261102/capture_sheets.json')]


def main():
    assert not ROOT.exists() and not FINAL.exists()
    doc, rebuilt, stored, loaders, visual, menu, styles, name, names, pixels, control = map(load,
        [DOC, REBUILT, STORED, LOADERS, VISUAL, MENU, STYLES, NAME, NAMES, PIXELS, CONTROL])
    assert (len(doc['records']), doc['revised'], doc['retained']) == (329, 180, 149)
    assert stored['complete_stored_pages'] == visual['total_final_speech_pages'] == 328
    assert stored['typed_labels_checked'] == 10 and len(stored['records']) == 311 and len(stored['style_records']) == 8
    assert stored['fresh_relocated_native_relative_cases'] == 640
    assert (loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (38, 612)
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and visual['all_final_speech_pages_approved']
    assert pixels['all_required_distinct_display_cases_match'] and pixels['both_two_choice_highlights_anddecline_branch_observed']
    assert {s['selected_option'] for s in pixels['menu_samples']} == {0, 1}
    assert menu['offline_visual_approved'] and name['offline_visual_approved'] and styles['native_target_slot_cases'] == 8
    assert len(names['records']) == 20 and names['all_five_gates_pass_in_scoped_context']
    assert control['Japanese_core_message_exactly_same'] and control['final_framebuffers_identical']
    runs = [r for path in SHEETS for r in load(path)['runs']]
    sheets = [s for r in runs for s in r['review_sheets']]
    assert len(runs) == 5 and len(sheets) == 19 and sum(r['frames'] for r in runs) == 59005
    for run in runs:
        assert run['cold_boot'] and not run['savestate'] and not run['hardware_verification']
        assert sha(Path(run['capture_report']).read_bytes()) == run['capture_report_sha256']
        for sheet in run['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    ROOT.mkdir(parents=True)
    actual_path = ROOT / 'actual_review.json'
    actual = dict(runs=runs, total_frames=59005, all_review_sheets_directly_viewed=sheets,
        focused_actual_pixels=str(PIXELS), focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        source_control=str(CONTROL), source_control_sha256=sha(CONTROL.read_bytes()),
        source_control_extra_frames=5001, source_control_runs=1,
        representative_progressive_FE_actor0_style_two_choice_pagination_andscene_transition_observed=True,
        all_required_distinct_display_cases_match=True, both_two_choice_highlights_anddecline_branch_observed=True,
        observations=[
            'B133: original role7 fallback Sailor/personality4 line matches native pixels. After the original C600 battle command the initialized English and clean-Japanese controls reach the same invalid instruction and identical final framebuffer. Natural monster-battle setup/transition remains unvisited; no ROM workaround was applied.',
            'B136: complete cargo-hold explanation occupies four FE rows without a split word or extra blank row. Both complete menu captions/highlights match native pixels; ordinary Down selects Don\'t sell it and the correct leave-it-aboard response and port return follow.',
            'B142: source Foreign Girl headings stay complete inside the FE body. Both reassurance pages, the conditional shelter wording, repeated FI Hodram naming example, Sera identity/acquisition and port return are readable; no adoption, marriage or proven language comprehension is invented.',
            'B143: the deliberate three-row wait, Barkeep and Sera headers, original actor0 Rafael portrait/name, complete smile, closing departure and port return are observed. Exact native masks also match the complete Someone she knows? No. panel.'],
        unvisited='Other B131–B150 blocks/conditional branches, seven other personality classes, four other menus and all three changed full-catalogue UIs remain offline-only. B133 natural battle transition is not covered. Identical short text is bound only to native-plane equivalence unless source occurrence is independently qualified.',
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        no_whole_live_backing_RAM_VRAM_palette_orVM_register_ownership_claim=True,
        following_content_limits='Repeated A after target completion also enters existing port/tutorial/sailing content; these frames do not add target dialogue approval. Future changed-only reruns may stop at the already observed target return rather than repeating that following content.',
        purpose='Focused editorial/display QA; no guide photo collection.', new_credit=0)
    save(actual_path, actual)
    final = deepcopy(doc)
    final.update(format='dk4-editorial-final-review-v1', encoder='dialogue-relocatable-v1',
        all_formatting_gates_false=False, all_five_individual_review_gates_passed=True,
        previous_manuscript=str(DOC), previous_manuscript_sha256=sha(DOC.read_bytes()),
        registered_release_pending=True, new_credit=0,
        stage_status=dict(prose=True, offline_display=True, stored=True, representative_English_gameplay=True, registered_release=False))
    ordinary = {r['id']: r for r in stored['records']}
    style_rows = {r['id']: r for r in stored['style_records']}
    choices = {r['id']: (item, r) for item in stored['typed_objects'] for r in item['label_references']}
    blocks = IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    for row in final['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        row['review']['formatting'] = True
        row['registered_release_andcompletion_credit_pending'] = True
        if row['id'] == 'DK4_MES_B142_R0159':
            reason = load(DISPLAY / 'visual_formatting_preferences_v3.json')['records'][row['id']]['QA_line_ending_retention']['reason']
            row['qa_waivers'] = ['weak-line-ending']
            row['qa_waiver_reason'] = reason
        if row['kind'] == 'typed-choice-label':
            item, binding = choices[row['id']]
            at = binding['offset']
            raw = bytes.fromhex(binding['stored_hex'])
            reference = dict(file_path=row['file_path'], block=row['block'], command_offset=item['offset'],
                             source_index=row['source_index'], offset=at, record_index=binding['record_index'],
                             bytes=len(raw), exact_stored_hex=raw.hex(), native_command_word=item['word'])
        else:
            binding = style_rows[row['id']] if row.get('native_object_kind') == '4100-style-alternative' else ordinary[row['id']]
            at = binding['new_offset']
            raw = bytes.fromhex(binding['stored_hex'])
            reference = dict(file_path=row['file_path'], block=row['block'], offset=at,
                             record_index=binding['new_record_index'], bytes=len(raw), exact_stored_hex=raw.hex())
            if row.get('native_object_kind') == '4100-style-alternative':
                reference.update(command_offset=binding['final_command_offset'], source_style_indices=row['source_style_indices'],
                                 native_command_word=0x4100, virtual_prefix_not_stored=True, final_header_hex=binding['final_header_hex'])
            else:
                assert blocks[row['block']][at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        assert blocks[row['block']][at:at + len(raw) + 1] == raw + b'\0'
        reference['target_archive_sha256'] = rebuilt['target_archive_sha256']
        row['planned_integrated_reference'] = reference
        row['formatting_evidence'] = dict(stored=str(STORED), visual=str(VISUAL), actual=str(actual_path),
                                        native_menu=str(MENU) if row['kind'] == 'typed-choice-label' else None,
                                        native_styles=str(STYLES) if row.get('native_object_kind') == '4100-style-alternative' else None,
                                        representative_gameplay_not_individual_activation=True)
    plans = {r['id']: r for r in load(rebuilt['plan'])['records']}
    for group in rebuilt['groups']:
        for obj in group['native_objects']:
            members = {r['id'] for r in obj['records']}
            rows = [r for r in final['records'] if r['id'] in members]
            rows.sort(key=(lambda r: r['source_reference']['offset']) if obj['word'] == 0x4100 else (lambda r: r['source_index']))
            source, current = map(bytes.fromhex, [obj['source_hex'], obj['current_hex']])
            value = compile_styles(source, current, rows, plans) if obj['word'] == 0x4100 else compile_choices(source, current, rows)
            assert value.hex() == obj['compiled_hex']
    final['scoped_speaker_name_review'] = dict(manuscript=str(NAMES), sha256=sha(NAMES.read_bytes()), actors=20,
        name_native=str(NAME), name_native_sha256=sha(NAME.read_bytes()), full_207_review_still_open=True)
    final['formatting_evidence'] = {str(p): sha(p.read_bytes()) for p in [STORED, LOADERS, VISUAL, MENU, STYLES, NAME, NAMES, PIXELS, CONTROL, actual_path, REBUILT]}
    validate_natural_dialogue_batch(final)
    save(FINAL, final)
    # One record per reviewed owner; two physical spans are changed exactly once.
    proposal = load(name['proposal'])
    fields = []
    for field in proposal['fields']:
        for owner in field['owners']:
            actor = owner['actor']
            reviewed = next(r for r in names['records'] if r['actor_ID'] == actor)
            fields.append(dict(id=f'actor{actor}_column8_localized_name_field', english={36: 'Geronimo de Espinosa', 42: 'Vasquez de Maldonado', 49: 'Alonso de Rosa'}[actor],
                speaker=reviewed['english'], context='Exact clean full-name consumer and complete shared-owner group; actor49 is an ownership extension, not a newly observed scene participant.',
                source_meaning={36: 'ジェロニモ・デ・エスピノサ', 42: 'バスケス・デ・マルドナード', 49: 'アロンソ・デ・ローサ'}[actor],
                localization_note=reviewed['finding'], review={g: True for g in ['source', 'context', 'localization', 'naturalness', 'formatting']},
                physical_field_group_actor=field['actor'], owned_field=field, reviewed_owner=owner,
                native=str(NAME), full_catalogue_UI_unvisited=True, decision='name-component-localization'))
    field_doc = dict(format='dk4-scoped-owned-name-fields-review-v3', translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=fields,
        owned_field_proposal=name['proposal'], owned_field_proposal_sha256=name['proposal_sha256'],
        physical_fields=2, individually_reviewed_owners=3, owned_span_bytes=4, no_new_dialogue_credit=True,
        native_andrepresentative_gameplay_checked_registered_deployment_pending=True, full_207_review_still_open=True, new_credit=0)
    validate_natural_dialogue_batch(field_doc)
    field_path = Path('translations/geronimo_vasquez_alonso_owned_name_review_v1.json')
    assert not field_path.exists()
    save(field_path, field_doc)
    save(ROOT / 'formatting_checkpoint.json', dict(final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()),
        actual=str(actual_path), actual_sha256=sha(actual_path.read_bytes()), source_control=str(CONTROL),
        reconstruction=str(REBUILT), stored=str(STORED), loaders=str(LOADERS), name_review=str(NAMES), name_fields_review=str(field_path),
        total_reviews=329, revised=180, retained=149, native_pages=328, resolved_layout_findings=23,
        scoped_names=20, name_identity_revisions=3, name_identity_retentions=17, owned_name_fields=2, owned_name_field_owners=3, owned_name_bytes=4,
        native_relative_cases=640, whole_archive_loads=325, actual_runs=5, actual_frames=59005, source_control_runs=1, source_control_frames=5001,
        directly_viewed_actual_sheets=19, actual_body_plane_comparisons=83, actual_header_comparisons=2, actual_menu_highlight_comparisons=2,
        all_individual_five_gates_pass_in_research=True, registered_release_andcompletion_credit_pending=True,
        current_registered_ROM_andmain_unchanged=True, full_goal_complete=False, new_credit=0,
        terminal_sessions=dict(rebuild=93925, stored=36067, fixtures=2423, English_runs=43591, Japanese_control=70115, second_choice=16535),
        pending=['Register a source-qualified release successor for the 13 documented structural/dramatic layouts and this exact mixed batch.',
                 'Append the reviewed grouped-name-field stage after all existing runtime/Emilio/Fernando/Samwell/Follower/Diogo stages; preserve ASCII right-bound correction.',
                 'Build/qualify the registered cumulative candidate, reconstruct from exact clean input and run its own startup; then add329 completion credits once only.'],
        evidence={str(p): sha(p.read_bytes()) for p in [FINAL, field_path, NAMES, PIXELS, CONTROL, actual_path, REBUILT, STORED, LOADERS, Path(__file__)]}))
    print('PASS329 individual five-gate research reviews;20 names;640 relative cases;5 English runs/59005frames plus source control. Registration/patch/own startup/credit pending.')


if __name__ == '__main__':
    main()
