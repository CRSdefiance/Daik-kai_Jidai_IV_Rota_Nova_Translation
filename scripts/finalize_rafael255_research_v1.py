"""Seal the mixed255 research review without claiming registered integration or natural activation."""
from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael255_checked_v1_20261105')
BASE = Path('work/analysis/Rafael255_reconstruction_inputs_v1_20261105')
REBUILD = Path('work/analysis/Rafael255_rebuilt678_v2_20261105/reconstruction.json')
STORED = Path('work/analysis/Rafael255_stored_native_v3_20261105/stored_native_verification.json')
CAT = Path('work/analysis/Rafael255_stored_catalogue_v1_20261105/all_stored_effective_body_bindings.json')
LOADERS = Path('work/analysis/Rafael255_loaders_v1_20261105/verification.json')
NAMES = Path('work/analysis/Rafael241_scoped_name_planes_v1_20261105/native_name_planes.json')
FINAL = Path('translations/rafael_B101_B120_contextual_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B101_B120_scoped_names_final_v1.json')
ACTUAL = [Path('work/analysis') / f'Rafael255_{name}_actual_pixels_v1_20261105/focused_actual_pixels.json'
          for name in ['Julio', 'dynamic']]
CONTACTS = [Path('work/analysis') / f'Rafael255_{name}_compact_sheets_v1_20261105/receipt.json'
            for name in ['Julio', 'dynamic']]
MENU = Path('work/analysis/Rafael255_menu_actual_pixels_v1_20261105/menu_actual_pixels.json')
SELECTION = Path('translations/rafael255_focused_actual_selection_v1.json')


def bound_evidence(doc):
    for name, digest in doc.get('evidence', {}).items():
        assert sha(Path(name).read_bytes()) == digest, name


if __name__ == '__main__':
    assert not any(p.exists() for p in [ROOT, FINAL, FINAL_NAMES])
    rebuilt, stored, cat, loaders, names = map(load, [REBUILD, STORED, CAT, LOADERS, NAMES])
    doc, plan = map(load, [rebuilt['manuscript'], rebuilt['plan']])
    actuals, contacts, menu = list(map(load, ACTUAL)), list(map(load, CONTACTS)), load(MENU)
    assert len(doc['records']) == 255 and (doc['proposed_revisions'], doc['justified_retentions']) == (135, 120)
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
               for r in doc['records'])
    assert (len(stored['records']), len(stored['style_records']), stored['typed_labels_checked'], stored['complete_stored_pages']) == (229, 14, 12, 248)
    assert stored['reconstruction_sha256'] == sha(REBUILD.read_bytes())
    assert stored['native_sha256'] == sha(Path(rebuilt['native']).read_bytes())
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['fresh_relocated_native_relative_cases'] == 180
    assert len(cat['records']) == 243 and cat['all243_ordinary_andphysical_style_bodies_checked']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (343, 36, 650)
    assert load(BASE/'visual_andinventory_approval.json')['all14_fresh_style_pages_directly_viewed']
    prior_visual = load('work/analysis/Rafael241_native_final_v6_20261105/direct_visual_approval.json')
    assert prior_visual['all18_scoped_names_and17_strings_onboth_sheets_directly_viewed']
    assert prior_visual['all12_caption_labels_both_native_styles_andboth_sheets_directly_viewed']
    sourceids, pageids, expected_actors, source_selectors, public_names = set(), set(), set(), set(), set()
    for actual in actuals:
        bound_evidence(actual)
        assert actual['all_selected_pages_observed_in_exact_fixture_order']
        assert actual['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(actual[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware'])
        sourceids.update(r['id'] for r in actual['body_pages'])
        pageids.update((r['id'], r['page']) for r in actual['body_pages'])
        expected_actors.update(r['expected_actor_ID'] for r in actual['headers'])
        source_selectors.update(r['source_selector'] for r in actual['headers'])
        public_names.update(r['text'] for r in actual['headers'])
    assert (len(sourceids), len(pageids), len(expected_actors), len(public_names)) == (75, 77, 15, 14)
    assert {207, 208} <= source_selectors
    assert all(h['expected_ID_from_offline_role_proof_not_pixels'] for a in actuals for h in a['headers'] if h['source_selector'] >= 207)
    assert {'SC0_B113_STYLE_10_48', 'SC0_B119_STYLE_16_92'} <= sourceids
    assert {(m['source_command_offset'], tuple(m['observed_selected_options'])) for m in menu['menus']} == {
        (296, (0, 1, 2)), (534, (0, 1, 2)), (370, (0, 1, 2)), (336, (0, 1, 2))}
    assert len(menu['menus']) == 4 and all(m['count'] == 3 for m in menu['menus'])
    assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    planned_controls = load(SELECTION)['fixtures'][1]['planned_menu_controls']
    following = {296: 'DK4_MES_B114_R0096', 534: 'DK4_MES_B114_R0185',
                 370: 'DK4_MES_B118_R0055', 336: 'DK4_MES_B119_R0066'}
    transitions = []
    for control in planned_controls:
        opened, accepted = control['open_A_frame'], control['ordinary_accept_A_frame']
        samples = [s for s in menu['menu_samples'] if s['source_command_offset'] == control['source_command_offset']
                   and opened < s['frame'] < accepted]
        assert {s['visible_selected_option'] for s in samples} >= {0, 1, 2}
        last = max(samples, key=lambda s: s['frame'])
        assert last['visible_selected_option'] == control['accepted_index'] and accepted-last['frame'] <= 45
        call = next(c for c in actuals[1]['ordered_selected_source_calls'] if c['frame'] >= accepted)
        assert call['id'] == following[control['source_command_offset']] and call['page'] == 1
        assert accepted < call['frame'] < accepted+120
        transitions.append(dict(**control, last_complete_menu_frame=last['frame'],
                                following_selected_source_call=call,
                                numeric_return_register_andoriginal_branch_unobserved=True))
    sheets = []
    for receipt_path, receipt in zip(CONTACTS, contacts, strict=True):
        assert sha(Path(receipt['actual_pixel_proof']).read_bytes()) == receipt['actual_pixel_proof_sha256']
        sheets += receipt['bottom_screen_sheets']+receipt['full_scene_sheets']
    sheets.append(menu['review_sheet'])
    assert (len(contacts[0]['bottom_screen_sheets']), len(contacts[0]['full_scene_sheets']), len(contacts[1]['bottom_screen_sheets'])) == (5, 1, 2)
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    for name in ['Julio_capture', 'Julio_pixels', 'dynamic_capture', 'dynamic_pixels']:
        terminal = load(Path('work/analysis')/f'Rafael255_{name}_gc_v1_20261105/completion.json')
        assert terminal['terminal'] and terminal['completed_without_exception'] and terminal['all_locked_sources_unchanged']
        assert not terminal['garbage_collection']['errors']
    ROOT.mkdir()
    visual_path, actual_path = ROOT/'complete_visual_approval.json', ROOT/'actual_review.json'
    save(visual_path, dict(all248_native_body_pages_and12_captions_and18_names_approved=True,
        prior_composite_visual=str(BASE/'visual_andinventory_approval.json'),
        all77_actual_body_pages_onseven_readable_sheets_directly_viewed=True,
        six_full_context_samples_and12_menu_cursor_states_directly_viewed=True,
        reviewed_sheets=sheets, all_prose_retained_after_actual_review=True,
        retention_note='The Julio grandfather joke, the priest misunderstanding and blessing, and the village exchange read coherently in order. Keep the individual justified prose decisions and ten approved wrap refinements; both FE guards now display complete final characters and the bean premise consumes four rows correctly.',
        initialized_background_is_the_unchanged_NewGame_scene_not_each_original_location=True,
        new_credit=0, guide_photos=False))
    save(actual_path, dict(total_frames=sum(a['frames'] for a in actuals), initialized_fixture_runs=2,
        source_speech_variants_observed=75, native_body_pages_observed=77, actual_choice_labels=12,
        source_editorial_objects_observed=87, offline_only_speech_variants=168,
        ordinary_speeches_observed=73, physical_style_variants_observed=2, other12_style_variants_offline_only=True,
        source_IDs_observed=sorted(sourceids), offline_only_source_IDs=sorted({r['id'] for r in plan['records']}-sourceids),
        observed_source_selectors=sorted(source_selectors), matched_public_names=sorted(public_names),
        expected_actor_IDs_from_offline_binding_not_inferred_pixels=sorted(expected_actors),
        complete_body_holds=sum(a['complete_body_planes'] for a in actuals),
        complete_header_holds=sum(a['complete_header_planes'] for a in actuals),
        all11_newly_scoped_public_names_observed=True, both_dynamic_selectors_andboth_complete_style_objects_observed=True,
        all_four_menus_allthree_cursor_states_andordinary_A_to_following_dialogue_observed=True,
        menu_transitions=transitions, repaired_FE_period_andfour_row_bean_premise_observed=True,
        Julio_andsect_leader_two_page_transitions_observed=True,
        numeric_modal_returns_original_story_branches_stat_effects_andcancellation_unvisited=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        initialized_native_command_copies_not_original_event_activation=True,
        evidence={str(p): sha(p.read_bytes()) for p in [*ACTUAL, *CONTACTS, MENU, SELECTION, visual_path]},
        new_credit=0, guide_photos=False))
    name_doc = deepcopy(load('translations/rafael_B101_B120_scoped_names_androles_v1.json'))
    for row in name_doc['records']:
        row['review']['formatting'] = True
        row['actual_header_observed_in_current_fixture'] = row['actor_ID'] in expected_actors
    name_doc.update(all_scoped_name_planes_andrepresentative_actual_headers_pending=False,
        all18_individual_five_gates_pass_in_scoped_context=True,
        actor_IDs_unvisited_in_current_batch=sorted({r['actor_ID'] for r in names['actors']}-expected_actors),
        unvisited_names_retain_exact_qualified_prior_proofs=True,
        numeric_dynamic_actor_IDs_bound_offline_not_inferred_from_header_pixels=True,
        actual_review=str(actual_path), actual_review_sha256=sha(actual_path.read_bytes()))
    validate_natural_dialogue_batch(name_doc)
    save(FINAL_NAMES, name_doc)
    raw_archive = Path(rebuilt['target_archive']).read_bytes()
    assert sha(raw_archive) == rebuilt['target_archive_sha256']
    blocks = IlnkContainer.parse(raw_archive).blocks
    speech_rows = {r['id']: r for r in stored['records']+stored['style_records']}
    labels = {r['id']: (obj, r) for obj in stored['typed_objects'] for r in obj['label_references']}
    plans = {r['id']: r for r in plan['records']}
    before = deepcopy(doc)
    for row in doc['records']:
        if row['id'] in speech_rows:
            item = speech_rows[row['id']]; at = item['new_offset']; raw = bytes.fromhex(item['stored_hex'])
            ref = dict(file_path=row['file_path'], block=row['block'], offset=at,
                       record_index=item['new_record_index'], exact_stored_hex=raw.hex(),
                       target_archive_sha256=sha(raw_archive))
            if row['id'].startswith('SC0_'):
                ref.update(command_offset=item['final_command_offset'], source_style_indices=item['source_style_indices'],
                           exact_command_header_hex=item['final_header_hex'], virtual_prefix_not_stored=True)
            else:
                ref['header_offset'] = at-5
                assert blocks[row['block']][at-5:at+1].hex() == row['source_complete_preamble_hex']
            row['planned_English_markup'] = plans[row['id']]['formatted_markup']
            row['actual_utterance_observed_in_disclosed_fixture'] = row['id'] in sourceids
        else:
            obj, item = labels[row['id']]; at = item['offset']; raw = bytes.fromhex(item['stored_hex'])
            assert raw.decode('ascii') == row['english']
            ref = dict(file_path=row['file_path'], block=row['block'], offset=at,
                       command_offset=obj['offset'], source_index=item['source_index'],
                       record_index=item['record_index'], exact_stored_hex=raw.hex(), target_archive_sha256=sha(raw_archive))
            row['actual_caption_andallthree_cursor_states_observed'] = True
        assert blocks[row['block']][at:at+len(raw)+1] == raw+b'\0'
        row.update(planned_integrated_reference=ref, fresh_formatting_binding_pending=False,
                   all_fresh_display_andregistered_integration_pending=False,
                   native_style_dispatch_andall_five_review_gates_pending=False,
                   registered_release_andcompletion_credit_pending=True, new_credit=0)
        row['review']['formatting'] = True
    assert all((old['english'], old['decision'], old['finding']) == (new['english'], new['decision'], new['finding'])
               for old, new in zip(before['records'], doc['records'], strict=True))
    doc.update(all_fifth_formatting_gates_pending=False, all255_individual_five_gates_pass=True,
        all_native_visual_stored_gameplay_andregistered_integration_pending=False,
        source_name_terms_resolved_but_combined_name_term_formatting_pending_until_fifth_gate=False,
        registered_release_andcompletion_credit_pending=True, native_body_pages=248,
        actual_source_speech_variants=75, actual_body_pages=77, offline_only_source_speech_variants=168,
        scoped_name_review=str(FINAL_NAMES), scoped_name_review_sha256=sha(FINAL_NAMES.read_bytes()),
        parent_manuscript=rebuilt['manuscript'], parent_manuscript_sha256=rebuilt['manuscript_sha256'],
        formatting_evidence=dict(native=rebuilt['native'], stored=str(STORED), catalogue=str(CAT), loaders=str(LOADERS),
                                 visual=str(visual_path), actual=str(actual_path)))
    validate_natural_dialogue_batch(doc)
    save(FINAL, doc)
    plan.update(manuscript=str(FINAL), manuscript_sha256=sha(FINAL.read_bytes()), exact_all_prose_andcompiled_bytes_unchanged=True)
    save(ROOT/'release_plans.json', plan)
    save(ROOT/'research_completion.json', dict(manuscript=str(FINAL), manuscript_sha256=sha(FINAL.read_bytes()),
        all255_individual_five_gates_pass=True, revisions=135, retentions=120, body_pages=248, typed_labels=12,
        scoped_names=18, new_credit=0, registered_integration_pending=True, main_unchanged=True,
        evidence={str(p): sha(p.read_bytes()) for p in [FINAL, FINAL_NAMES, REBUILD, STORED, CAT, LOADERS, NAMES,
            BASE/'visual_andinventory_approval.json', *ACTUAL, *CONTACTS, MENU, visual_path, actual_path, Path(__file__)]}))
    print('255 five-gate research reviews sealed:135 revisions/120 retentions;77 actual pages/12 captions,168 speech variants offline-only. Registered integration pending;no credit.')
