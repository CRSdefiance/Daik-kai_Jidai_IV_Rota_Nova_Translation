"""Seal all five editorial gates against exact stored, rendered and observed evidence."""
from collections import Counter
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.assemble_rafael_B221_B240_offline_v2 import FINAL_MANUSCRIPT, FINAL_NATIVE, FINAL_PLAN, OUT, ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_rafael_B221_B240_visual_v1 import VISUAL
from scripts.write_rafael_B221_B240_contextual_v1 import LABELS, digest

REBUILT = ROOT / 'rebuilt_research_v1/reconstruction.json'
STORED = ROOT / 'stored_native_v1/stored_native_verification.json'
LOOKUP = ROOT / 'stored_catalogue_all_v1/all263_stored_effective_body_bindings.json'
LOADERS = ROOT / 'loaders_v1/verification.json'
MENU_ACTUAL = ROOT / 'actual_menus_v1/menu_actual_pixels.json'
FINAL = Path('translations/rafael_B221_B240_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B221_B240_scoped_names_final_v1.json')
RESEARCH = ROOT / 'research_final_v1'
RUNS = (('rafael_letters_swans_and_names', 51, 55, 18161), ('rafael_books_guard_and_town', 35, 39, 15041))
PASSES = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)


def observed(rebuilt, records, layouts):
    found, actors, styles, sheets, paths = {}, set(), set(), [], []
    for name, utterances, pages, frames in RUNS:
        files = (ROOT/f'actual_fixtures_v1/{name}_fixture.json', ROOT/f'actual_{name}_v1/terminal.json',
                 ROOT/f'actual_pixels_{name}_v1/focused_actual_pixels.json')
        paths.extend(files)
        fixture, terminal, proof = map(load, files)
        assert fixture['frames'] == terminal['frames'] == proof['frames'] == frames and terminal['terminal']
        assert fixture['parent_sha256'] == rebuilt['research_ROM_sha256']
        assert proof['all_selected_pages_observed_in_exact_fixture_order']
        assert proof['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert proof['actual_gameplay'] and not any(proof[k] for k in ('natural_activation', 'original_location',
            'earned_chronology', 'full_route', 'hardware'))
        assert all(digest(Path(path)) == checksum for path, checksum in proof['evidence'].items())
        actors.update(row['expected_actor_ID'] for row in proof['headers'])
        sheets.extend(proof['review_sheets'])
        selected = fixture['selected_records']
        assert len(selected) == utterances and len(proof['ordered_selected_source_calls']) == pages
        assert [r['id'] for r in proof['ordered_selected_source_calls']] == [
            row['id'] for row in selected for _ in range(layouts[row['id']]['expected_native_pages'])]
        copied = {row['fixture_offset']: row for row in fixture['copied_commands']}
        by_page = {}
        for sample in proof['body_pages']:
            by_page.setdefault((sample['id'], sample['page']), sample)
        assert len(by_page) == pages and found.keys().isdisjoint(by_page)
        for row in selected:
            ident = row['id']
            native = records[ident]
            display = native['complete_native_English_display']
            planes = [display] if row['selector'] == 254 else display['pages']
            for index, plane in enumerate(planes, 1):
                sample = by_page[ident, index]
                assert sample['native_plane_sha256'] == plane['native_plane_sha256']
                assert digest(Path(sample['capture']['path'])) == sample['capture']['PNG_sha256']
                body = bytes.fromhex(row['expected_expanded_body_hex'])
                assert sample['text_hex'] == body[plane.get('start', 0):].hex()
            if row.get('native_object_kind') == '4100-style-alternative':
                command = copied[row['fixture_offset']]
                assert command['word'] == 0x4100 and row['selector'] == 208 and row['expected_style'] == 4
                assert row['expected_header_actor_ID'] == 151 and row['whole_eight_slot_command_copied_without_state_override']
                styles.add((row['block'], command['original_offset']))
        found.update(by_page)
    assert (len(found), len(actors), len(styles), len(sheets)) == (94, 16, 4, 7)
    assert len({ident for ident, _ in found}) == 86
    assert all(digest(Path(sheet['path'])) == sheet['sha256'] for sheet in sheets)
    return found, actors, styles, sheets, paths


def main():
    assert not any(path.exists() for path in (FINAL, FINAL_NAMES, RESEARCH))
    paths = (REBUILT, STORED, LOOKUP, LOADERS, VISUAL, MENU_ACTUAL, FINAL_MANUSCRIPT, FINAL_PLAN, FINAL_NATIVE,
             OUT/'menu.json', OUT/'styles.json', LABELS)
    rebuilt, stored, lookup, loaders, visual, live_menus, doc, plan, native, menu, styles, names = map(load, paths)
    assert all(value['runtime'] == doc['runtime'] for value in (stored, lookup, visual, native, menu, styles, names))
    assert rebuilt['manuscript_sha256'] == native['manuscript_sha256'] == digest(FINAL_MANUSCRIPT)
    assert rebuilt['plan_sha256'] == native['plan_sha256'] == digest(FINAL_PLAN)
    assert rebuilt['native_sha256'] == stored['native_sha256'] == visual['native_sha256'] == digest(FINAL_NATIVE)
    assert stored['reconstruction_sha256'] == loaders['reconstruction_sha256'] == digest(REBUILT)
    assert lookup['stored_sha256'] == digest(STORED) and lookup['all263_ordinary_and_style_bodies_checked']
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (len(stored['records']), len(stored['style_records']), len(lookup['records'])) == (234, 29, 263)
    assert (stored['complete_stored_pages'], stored['fresh_parity_dependent_pages'],
            stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (279, 127, 152, 170)
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'],
            loaders['exact_reused_parent_cases']) == (343, 38, 648)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert rebuilt['unchanged_control_only_blocks'] == [231] and len(rebuilt['changed_blocks']) == 19
    assert digest(Path(rebuilt['research_ROM'])) == rebuilt['research_ROM_sha256']
    archive = Path(rebuilt['target_archive']).read_bytes()
    assert digest(Path(rebuilt['target_archive'])) == rebuilt['target_archive_sha256']
    blocks = IlnkContainer.parse(archive).blocks
    records = {row['id']: row for row in native['records']}
    layouts = {row['id']: row for row in plan['records']}
    speech = {row['id']: row for row in stored['records'] + stored['style_records']}
    assert records.keys() == layouts.keys() == speech.keys() == {row['id'] for row in lookup['records']}
    captions = {row['id']: (item, row) for item in stored['typed_objects'] for row in item['label_references']}
    assert len(captions) == 7 and len(menu['menus']) == 3
    assert visual['all_final_body_caption_and_name_sheets_directly_viewed'] and visual['scoped_name_count'] == 26
    found, actors, observed_styles, actual_sheets, actual_paths = observed(rebuilt, records, layouts)
    found_ids = {ident for ident, _ in found}
    assert len(found_ids & {row['id'] for row in stored['style_records']}) == 4
    assert observed_styles == {(group['block'], item['new_offset']) for group in rebuilt['groups']
                               for item in group.get('native_objects', []) if item['word'] == 0x4100}
    assert live_menus['ordinary_A_return_to_next_fixture_speech_observed']
    assert live_menus['observed_each_menu_between_its_own_exact_preceding_and_following_speech']
    assert live_menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert live_menus['complete_live_caption_samples'] == 6
    assert all(row['observed_selected_options'] == [0] for row in live_menus['menus'])
    assert {(row['block'], row['source_command_offset']) for row in live_menus['menus']} == {
        (row['block'], row['offset']) for row in stored['typed_objects']}
    assert digest(Path(live_menus['review_sheet']['path'])) == live_menus['review_sheet']['sha256']
    assert {'DK4_MES_B224_R0072', 'DK4_MES_B227_R0019', 'DK4_MES_B223_R0017'} <= found_ids

    for row in doc['records']:
        ident, block = row['id'], row['block']
        assert row['review'] == PASSES
        if ident in speech:
            saved = speech[ident]
            offset = saved['new_offset']
            ref = dict(offset=offset, record_index=saved['new_record_index'])
            if row.get('native_object_kind') == '4100-style-alternative':
                assert saved['virtual_prefix_not_stored'] and saved['source_style_indices'] == row['source_style_indices']
                ref.update(command_offset=saved['final_command_offset'], source_style_indices=saved['source_style_indices'],
                           virtual_prefix_not_stored=True)
                row.update(complete_native_style_binding_andformatting_pending=False)
            else:
                assert blocks[block][offset-5:offset+1].hex() == row['source_complete_preamble_hex']
                ref['header_offset'] = offset - 5
            if row['kind'] == 'system-FE':
                row.update(native_FE_presentation_binding_pending=False, original_event_background_unvisited=True)
            if row.get('source_staged_progressive') or row.get('source_staged_FE'):
                row.update(source_signature_presentation_pending=False,
                           source_staged_native_rows=records[ident]['exact_native_English_rows'])
            row.update(actual_utterance_observed_in_disclosed_fixture=ident in found_ids)
            if 'formatted_markup' in layouts[ident]:
                row['planned_English_markup'] = layouts[ident]['formatted_markup']
        else:
            item, saved = captions[ident]
            offset = saved['offset']
            assert item['block'] == block and item['word'] == row['source_word']
            assert bytes.fromhex(saved['stored_hex']).decode('ascii') == row['english']
            ref = dict(offset=offset, command_offset=item['offset'], source_index=saved['source_index'],
                       record_index=saved['record_index'])
            row.update(actual_caption_visible_with_default_cursor=True,
                       other_cursor_and_return_cases_verified_offline=True,
                       complete_native_menu_binding_andformatting_pending=False)
        raw = bytes.fromhex(saved['stored_hex'])
        assert blocks[block][offset:offset+len(raw)+1] == raw+b'\0'
        row.update(planned_integrated_reference=dict(**ref, file_path=row['file_path'], block=block,
            exact_stored_hex=raw.hex(), target_archive_sha256=rebuilt['target_archive_sha256']),
            review={**PASSES, 'formatting': True}, fresh_formatting_binding_pending=False,
            registered_release_and_completion_credit_pending=True)
    assert Counter(row['decision'] for row in doc['records']) == {'revision': 221, 'retention': 49}
    for row in names['records']:
        assert row['review'] == PASSES
        row.update(review={**PASSES, 'formatting': True},
                   actual_header_observed_in_disclosed_fixture=row['actor_ID'] in actors)

    RESEARCH.mkdir()
    actual_path, visual_path, release_plan = [RESEARCH/name for name in (
        'actual_review.json', 'complete_visual_approval.json', 'release_plans.json')]
    evidence = {str(path): digest(path) for path in (*paths, *actual_paths, Path(__file__))}
    sheets = visual['sheets'] + actual_sheets + [live_menus['review_sheet']]
    save(visual_path, dict(all_body_caption_andname_planes_approved=True, all_actual_pages_and_menus_directly_viewed=True,
        body_pages=279, observed_pages=94, reviewed_caption_planes=28, scoped_public_names=26, typed_labels=7,
        reviewed_sheets=sheets, evidence=evidence, new_credit=0, guide_photos=False))
    save(actual_path, dict(total_frames=33202, initialized_fixture_runs=2, source_speech_variants_observed=86,
        native_body_pages_observed=94, actual_choice_labels=7, offline_only_speech_variants=177, offline_only_caption_count=0,
        source_IDs_observed=sorted(found_ids), offline_only_source_IDs=sorted(set(speech)-found_ids),
        exact_observed_pages=[dict(id=row['id'],page=row['page'],frame=row['frame'],capture=row['capture'])
                              for row in found.values()],
        observed_public_name_actor_IDs=sorted(actors),
        observed_FE_source_IDs=sorted(found_ids & {row['id'] for row in doc['records'] if row['kind']=='system-FE'}),
        all_four_complete_style_commands_observed_under_unmodified_default_roles=True,
        all_three_menu_instances_default_cursor_and_following_fixture_speech_observed=True,
        menus=live_menus['menus'], other_cursor_states_VM_returns_branches_andcancellation_offline_only=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        evidence=evidence, new_credit=0, guide_photos=False))
    names.update(all_name_formatting_gates_pending=False, all_individual_five_gates_pass_for_public_nameplanes=True,
                 actual_review=str(actual_path), actual_review_sha256=digest(actual_path))
    validate_natural_dialogue_batch(names)
    save(FINAL_NAMES, names)
    doc.update(all_fifth_formatting_gates_pending=False, all_individual_five_gates_pass=True,
        native_macro_tokens_still_require_formatter_marking=False, only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=279, actual_source_speech_variants=86, actual_body_pages=94,
        offline_only_source_speech_variants=177, scoped_name_review=str(FINAL_NAMES),
        scoped_name_review_sha256=digest(FINAL_NAMES), parent_manuscript=str(FINAL_MANUSCRIPT),
        parent_manuscript_sha256=digest(FINAL_MANUSCRIPT), registered_release_and_completion_credit_pending=True,
        formatting_evidence=dict(native=str(FINAL_NATIVE), stored=str(STORED), catalogue=str(LOOKUP),
                                 loaders=str(LOADERS), visual=str(visual_path), actual=str(actual_path)))
    validate_natural_dialogue_batch(doc)
    save(FINAL, doc)
    save(release_plan, {**plan, 'manuscript': str(FINAL), 'manuscript_sha256': digest(FINAL),
                       'exact_all_prose_and_compiled_bytes_unchanged': True})
    save(RESEARCH/'research_completion.json', dict(manuscript=str(FINAL), manuscript_sha256=digest(FINAL),
        plan=str(release_plan), plan_sha256=digest(release_plan), all_individual_five_gates_pass=True,
        records=270, revisions=221, retentions=49, body_pages=279, typed_labels=7, scoped_public_names=26,
        actual_source_variants=86, actual_pages=94, actual_choice_labels=7, actual_menus=3,
        actual_name_headers=16, offline_only_source_variants=177, registered_integration_pending=True,
        new_credit=0, full_goal_complete=False,
        evidence={**evidence, **{str(p):digest(p) for p in (FINAL, FINAL_NAMES, release_plan, visual_path, actual_path)}}))
    print('Sealed 270 five-gate reviews, 279 offline and stored pages, and 94 focused emulator pages.')


if __name__ == '__main__':
    main()

