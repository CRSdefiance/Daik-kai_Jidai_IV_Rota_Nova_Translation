"""Seal305 mixed source reviews after exact stored and representative display approval."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B176_B195_clean_20261110')
FINAL = Path('translations/maria_B176_B195_final_review_v1.json')
NAMES = Path('translations/maria_B176_B195_scoped_names_final_v1.json')
OUT = ROOT/'research_completion_v1'
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']


def main():
    assert not any(p.exists() for p in [FINAL, NAMES, OUT])
    paths = dict(source=ROOT/'formatting_v1/formatting_input.json',
        prose=Path('translations/maria_B176_B195_contextual_review_v1.json'),
        names=Path('translations/maria_B176_B195_scoped_names_v1.json'),
        plan=ROOT/'plan_v8/automatic_plans.json', native=ROOT/'final_native_v1.json',
        styles=ROOT/'compiled_styles_v2/compiled_style_objects.json', menus=ROOT/'menu_native_approved_v1.json',
        rebuilt=ROOT/'reconstruction_v1/reconstruction.json', stored=ROOT/'stored_v1/stored_native_verification.json',
        catalogue=ROOT/'stored_catalogue_all_v1/all_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v1/verification.json', visual=ROOT/'offline_display_approval_v1.json',
        actual=ROOT/'gameplay_review_v1.json', name_planes=ROOT/'name_planes_v1/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json', roles=ROOT/'formatting_v1/role_bindings.json',
        terms=ROOT/'scoped_terms_reference_v1.json')
    d = {k:load(p) for k,p in paths.items()}
    doc = deepcopy(d['source'])
    rebuilt, stored, native, plan, actual = [d[k] for k in ['rebuilt', 'stored', 'native', 'plan', 'actual']]
    assert len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}
    assert len(native['records']) == len(plan['records']) == len(d['catalogue']['records']) == 294
    assert len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11
    assert (native['pages'], stored['complete_stored_pages'], native['selected_alignment_cases']) == (302, 302, 1176)
    assert (stored['fresh_parity_dependent_pages'], stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (148, 154, 170)
    assert native['manuscript_sha256'] == d['styles']['manuscript_sha256'] == d['menus']['manuscript_sha256'] == digest(paths['source'])
    assert native['plan_sha256'] == d['styles']['plan_sha256'] == digest(paths['plan'])
    assert all(d[k]['runtime'] == native['runtime'] for k in ['source', 'stored', 'catalogue', 'styles', 'menus', 'name_planes', 'macros', 'roles'])
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['reconstruction_sha256'] == d['loaders']['reconstruction_sha256'] == digest(paths['rebuilt'])
    assert d['catalogue']['stored_sha256'] == digest(paths['stored']) and d['catalogue']['all_scoped_ordinary_and_style_bodies_checked']
    assert d['catalogue']['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (d['loaders']['fresh_whole_archive_loads_andcache_hits'], d['loaders']['fresh_parent_cases']) == (303, 606)
    assert d['loaders']['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact']
    assert d['visual']['all_final_body_pages_directly_viewed'] and d['visual']['all_names_andcaptions_directly_viewed']
    assert d['visual']['all_native_controls_substitutions_words_glyphs_bounds_andpagination_pass']
    assert (d['styles']['physical_alternatives'], d['styles']['native_target_slot_cases'], len(d['styles']['objects'])) == (22, 24, 3)
    assert d['styles']['source_alias_equivalence_exact'] and d['styles']['complete_source_current_alias_target_body_andfinal_plan_recompiled_exact']
    assert sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27
    assert len(d['menus']['menus']) == 5 and d['menus']['offline_visual_approved'] and not d['menus']['direct_view_pending']
    assert not plan['failures'] and not any(i['severity'] in ['warning', 'error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert (actual['frames'], actual['initialized_runs'], actual['distinct_source_body_objects'], actual['distinct_body_pages']) == (63843, 3, 127, 132)
    assert actual['observed_pages_including_repeats'] == 135 and actual['offline_only_source_body_objects'] == 167
    assert actual['all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed']
    assert actual['all_selected_current_pages_match_current_compiled_native_planes'] and actual['all_five_two_page_turns_andfollowing_calls_observed']
    assert actual['repaired_B177_FE_panel_complete_andnormal_A_return_observed'] and actual['both_fullwidth_I_replacements_original_FA_andGuan_Yu_translation_observed']
    assert actual['parrot_complete_echo_exchange_andEmilio_first_person_replies_observed'] and actual['both_letter_page_turns_signatures_andSailor_headers_observed']
    assert actual['complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed']
    assert not any(actual[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware', 'full_original_story_scene_control_flow_preserved'])
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['all_other_files_components_exact']
    assert rebuilt['source_editorial_objects'] == 305 and rebuilt['FE_continuation_owners'] == rebuilt['FE_inserted_commands'] == 0
    for receipt in [d['visual'], actual]:
        for p,h in receipt['evidence'].items():
            assert digest(p) == h
    for sheet in actual['review_sheets']:
        assert sheet['directly_viewed'] and digest(sheet['path']) == sheet['sha256']
    assert digest(rebuilt['target_archive']) == rebuilt['target_archive_sha256']
    blocks = IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    bodies = {r['id']:r for r in stored['records']+stored['style_records']}
    captions = {r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    plans = {r['id']:r for r in plan['records']}
    prose = {r['id']:r for r in d['prose']['records']}
    assert set(bodies) == set(plans) == {r['id'] for r in native['records']}
    assert set(bodies).isdisjoint(captions) and set(bodies)|set(captions) == set(prose)
    observed = set(actual['observed_body_IDs'])
    observed_captions = set(actual['observed_caption_IDs'])
    for row in doc['records']:
        ident = row['id']
        prior = prose[ident]
        assert re.sub(r'\{MACRO:([A-Z]{2})\}', lambda m:m[1], row['english']) == prior['proposed_English']
        assert all(row[k] == prior[k] for k in ['source_hex', 'current_hex', 'source_reference', 'current_reference', 'decision', 'finding'])
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        block = blocks[row['block']]
        if ident in bodies:
            item = bodies[ident]
            at = item['new_offset']
            raw = bytes.fromhex(item['stored_hex'])
            ref = dict(file_path=row['file_path'], block=row['block'], offset=at, record_index=item['new_record_index'],
                exact_stored_hex=raw.hex(), target_archive_sha256=rebuilt['target_archive_sha256'])
            if row.get('native_object_kind') == '4100-style-alternative':
                header = bytes.fromhex(item['final_header_hex'])
                assert block[item['final_command_offset']:item['final_command_offset']+len(header)] == header
                ref.update(command_offset=item['final_command_offset'], source_style_indices=item['source_style_indices'],
                    exact_command_header_hex=item['final_header_hex'], virtual_prefix_not_stored=True)
            else:
                assert block[at-5:at+1].hex() == row['source_complete_preamble_hex']
                ref['header_offset'] = at-5
            assert plans[ident]['logical_English'] == row['english']
            row['planned_English_markup'] = plans[ident]['formatted_markup']
            seen = ident in observed
            row['actual_utterance_observed_in_disclosed_fixture'] = seen
        else:
            obj, item = captions[ident]
            at = item['offset']
            raw = bytes.fromhex(item['stored_hex'])
            assert raw.decode('ascii') == row['english']
            ref = dict(file_path=row['file_path'], block=row['block'], offset=at, command_offset=obj['offset'],
                source_index=item['source_index'], record_index=item['record_index'], exact_stored_hex=raw.hex(),
                target_archive_sha256=rebuilt['target_archive_sha256'])
            seen = ident in observed_captions
            row['actual_caption_display_observed_in_disclosed_fixture'] = seen
        assert block[at:at+len(raw)+1] == raw+b'\0'
        row['review']['formatting'] = True
        row.update(planned_integrated_reference=ref, fresh_formatting_binding_pending=False,
            registered_release_andcompletion_credit_pending=True, new_credit=0,
            review_evidence=dict(offline_visual=str(paths['visual']), stored=str(paths['stored']), gameplay=str(paths['actual']),
                coverage='observed-disclosed-QA' if seen else 'offline-native-andstored-only'))
    doc.update(encoder='dialogue-relocatable-v1', review_gates=GATES, all_individual_five_gates_pass=True,
        all305_individual_five_gates_pass=True, all_fifth_formatting_gates_pending=False,
        native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127,
        actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167,
        actual_caption_strings=7, offline_only_caption_strings=4, registered_release_andcompletion_credit_pending=True,
        parent_manuscript=str(paths['source']), parent_manuscript_sha256=digest(paths['source']), new_credit=0, full_goal_complete=False)
    assert all(a['english']==b['english'] and a['finding']==b['finding'] for a,b in zip(d['source']['records'], doc['records'], strict=True))
    validate_natural_dialogue_batch(doc)
    names = deepcopy(d['names'])
    actors = {r['expected_actor_ID'] for r in actual['name_headers']}
    texts = {r['text'] for r in d['name_planes']['planes']}
    assert len(names['records']) == 27
    for row in names['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        assert all(c['text'] in texts for c in row['current_consumers'])
        row['review']['formatting'] = True
        row.update(actual_progressive_header_observed_in_disclosed_fixture=row['actor_ID'] in actors,
            numeric_actor_identity_from_offline_dispatch_not_header_pixels=True, full_catalogue_UI_layout_unvisited=True,
            full_catalogue_string_font_only_not_UI_layout_approval=True, name_localization_andfresh_display_approval_pending=False,
            fresh_native_display_orcompatible_proof_binding_pending=False, registered_release_andcompletion_credit_pending=True, new_credit=0)
    names.update(encoder='dialogue-relocatable-v1', review_gates=GATES,
        all27_individual_five_gates_pass_in_scoped_context=True, all_name_formatting_gates_pending=False,
        full_catalogue_UI_andfuture_role_assignments_unvisited=True, actual_review=str(paths['actual']), actual_review_sha256=digest(paths['actual']))
    validate_natural_dialogue_batch(names)
    OUT.mkdir()
    save(FINAL, doc)
    save(NAMES, names)
    source_plan = OUT/'source294_release_plans.json'
    final_plan = deepcopy(plan)
    final_plan.update(manuscript=str(FINAL), manuscript_sha256=digest(FINAL), source_editorial_objects=305,
        source_body_objects=294, physical_native_bodies=294, new_credit=0)
    save(source_plan, final_plan)
    save(OUT/'research_completion.json', dict(manuscript=str(FINAL), manuscript_sha256=digest(FINAL),
        names=str(NAMES), names_sha256=digest(NAMES), source_release_plans=str(source_plan), source_release_plans_sha256=digest(source_plan),
        all_individual_five_gates_pass=True, records=305, revisions=205, retentions=100, complete_exchanges=19,
        physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31,
        source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16,
        FE_continuation_owners=0, additional_native_commands=0, source_credit_not_duplicated=True,
        source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2,
        observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127,
        actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7,
        offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3,
        original_optional_conditions_locations_rewards_full_scene_flow_andhardware_unvisited=True,
        registered_integration_pending=True, main_unchanged=True, new_credit=0, full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(), FINAL, NAMES, source_plan, Path(__file__)]}))
    print('Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.')


if __name__ == '__main__':
    main()
