"""Pure SC0 integration with the full checked tutorial, names and display contract."""
import inspect
from dk4tool.patch import reviewed_scene_batch_v1 as previous
from dk4tool.script.rafael_early_tutorial_rebuild_v1 import rebuild_block
from scripts.source_locked_derivation_v5118 import checked_text

require = previous.require
load = previous.load


def qualify_display(conf, doc, stored):
    native, visual, names, name_visual, FE = [load(conf[k]) for k in
        ['compiled_native','visual_review','scoped_names','name_visual','FE_layout']]
    previous.validate_natural_dialogue_batch(names)
    require(len(names['records']) == 4 and all(all(r['review'].values()) for r in names['records']), 'four individual name reviews')
    require(names['no_name_data_change'] and {r['actor_ID'] for r in names['records']} == {0,4,5,6}, 'unchanged source-bound identities')
    require(native['runtime'] == stored['runtime'] and native['runtime']['captain'] == 0, 'own Rafael context')
    require(native['all42_final_pages_directly_viewed'] and visual['all_final_pages_directly_viewed_or_exact_plane_reuse'], 'all final pages viewed')
    require(stored['all_stored_planes_equal_directly_viewed_compiled_planes'], 'every stored plane equals viewed plane')
    require(name_visual['four_complete_name_planes_directly_viewed'] and name_visual['all_eight_current_Rafael_getters_pass'], 'complete scoped names')
    require(FE['FE_records'] == 1 and not FE['findings'] and FE['unexpected_blank_rows_orwraps_absent'], 'strict FE rows')
    require(sum(r['source_selector'] == 0 for r in doc['records']) == 5 and sum(r['source_selector'] == 254 for r in doc['records']) == 1, 'full selector00/FE membership')
    observed = {r['id']:r for r in stored['records']}
    compiled = {r['id']:r for r in native['records']}
    require(set(observed) == set(compiled) == {r['id'] for r in doc['records']}, 'complete stored and native membership')
    for row in doc['records']:
        entry, ref, plane = observed[row['id']], row['planned_integrated_reference'], compiled[row['id']]
        require(ref['offset'] == entry['new_offset'] and ref['record_index'] == entry['new_record_index'] and ref['exact_stored_hex'] == entry['stored_hex'], 'individual proposed storage reference')
        require(plane['source_reference'] == row['source_reference'] and plane['current_reference'] == row['current_reference'] and plane['logical_English'] == row['english'], 'individual source/current/prose binding')
        if row['source_selector'] == 254:
            require(plane['complete_native_English_display']['planned_native_row_comparison']['complete_glyph_row_membership_exact'], 'complete FE glyph membership')


def qualify_actual(conf, actual):
    pixels = load(conf['focused_pixels'])
    require(actual['total_frames'] == 25002 and len(actual['runs']) == 2 and len(actual['all_review_sheets_directly_viewed']) == 2, 'two completed coldboots')
    require(actual['all_target_sampled_paragraphs_andnormal_F_headers_complete'] and actual['all42_target_pages_observed_in_order'], 'complete observed text and normal F')
    require(actual['both_corrected_two_page_utterances_observed'] and actual['source00_FI_FE_andfollowing_port_transitions_observed'], 'distinct controls, macros, pagination and transitions')
    require(actual['no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim'], 'honest gameplay scope')
    require(pixels['actual_frames'] == 25002 and pixels['all_required_distinct_display_cases_match'], 'focused pixel cases')
    require(len(pixels['body_pages']) == 92 and len(pixels['name_headers']) == 5 and len(pixels['observed_record_pages']) == 42, 'complete pixel membership')
    require({r['actor_ID'] for r in pixels['name_headers']} == {0,4,5,6}, 'all four observed headers')
    require(all(r['complete_native_glyph_plane_andblank_guards_equal'] for r in pixels['body_pages']), 'all complete actual body planes')
    require({r['run']:r['calls'] for r in pixels['ordered_linear_scene_sequences']} == {'first_voyage':29,'crew_duties':13}, 'all copied calls in order')
    require(all(r['complete_ordered_calls_match_all_copied_source_speeches'] for r in pixels['ordered_linear_scene_sequences']), 'ordered source attribution')
    observed = {tuple(r) for r in pixels['observed_record_pages']}
    require({tuple(r) for r in pixels['required_distinct_display_cases']} <= observed, 'every required page observed')


source = checked_text(inspect.getsource(previous.plan_release), {
    "'dk4-reviewed-scene-release-v1'": "'dk4-rafael-early-tutorial-release-v1'",
    "conf['record_count'] == 224": "conf['record_count'] == 40",
    'set(range(61, 71))': '{42,43}',
    "native['complete_stored_pages'] == 229": "native['complete_stored_pages'] == 42",
    "native['fresh_relocated_native_relative_cases'] == 300": "native['fresh_relocated_native_relative_cases'] == 0",
    "    require(native['unchanged_directly_viewed_planes_reused_exactly'] == 227 and\n            native['changed_stored_planes_match_two_new_directly_viewed_pages'], 'visual review inheritance')":
        '    qualify_display(conf,approved,native)',
    "loaders['fresh_whole_archive_loads_andcache_hits'] == 325": "loaders['fresh_whole_archive_loads_andcache_hits'] == 343",
    "loaders['fresh_parent_cases'] == 20 and loaders['exact_reused_parent_cases'] == 630":
        "loaders['fresh_parent_cases'] == 4 and loaders['exact_reused_parent_cases'] == 682",
    "    require(actual['total_frames'] == 43003 and len(actual['runs']) == 3 and\n            len(actual['all15_contact_sheets_directly_viewed']) == 15 and\n            actual['both_changed_glyph_records_observed_with_normal_I_andcomplete_text'] and\n            actual['scene_ends_andfollowing_town_UI_visually_observed'], 'representative gameplay')\n    require(len(actual['five_two_page_utterances_observed']) == 5 and\n            actual['not_natural_optional_event_activation_ororiginal_location_chronology'] and\n            actual['no_world_state_equivalence_orhardware_full_route_claim'], 'pagination and honest coverage')":
        '    qualify_actual(conf,actual)',
    "'/data/SC1.DK4'": "'/data/SC0.DK4'",
    'len(clean_blocks) == 325': 'len(clean_blocks) == 343',
    'native_pages=229, fresh_relative_cases=300, native_loads=325,': 'native_pages=42, fresh_relative_cases=0, native_loads=343,',
    'parent_modes=dict(fresh=20, exact_reused=630), actual_frames=43003,':
        'parent_modes=dict(fresh=4, exact_reused=682), actual_frames=25002,',
})
env = {**previous.plan_release.__globals__, 'rebuild_block': rebuild_block,
    'qualify_display':qualify_display, 'qualify_actual':qualify_actual}
exec(compile(source, __file__ + '::same-pure-complete-inverse-SC0-qualified-prior-Julio-relocation', 'exec'), env)
plan_release = env['plan_release']
