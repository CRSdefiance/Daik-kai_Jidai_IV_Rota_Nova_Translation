"""Source-bound SC0 integration of229 speeches,14 style bodies and12 choice captions."""
from pathlib import Path
from dk4tool.patch import reviewed_rafael_plain_scene_release_v1 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_evidence(conf, doc, stored):
    load, require, sha = previous.previous.load, previous.previous.require, previous.previous.sha
    native, names, visual, actual, lookup, loaders, menu, styles, first, second, menus, reuse = [load(conf[k]) for k in
        ['compiled_native','scoped_names','visual_review','actual','stored_lookup','loaders','typed_menu','native_styles',
         'focused_pixels','menu_body_pixels','menu_pixels','dependency_qualification']]
    original = load(conf['research_reconstruction'])
    integration = load(conf['reconstruction'])
    require(stored['reconstruction_sha256'] == sha(Path(conf['research_reconstruction']).read_bytes()), 'exact original stored proof')
    require(reuse['original_reconstruction_sha256'] == stored['reconstruction_sha256'] and
        reuse['rebased_reconstruction_sha256'] == sha(Path(conf['reconstruction']).read_bytes()), 'qualified rebase identities')
    require(integration['groups'] == original['groups'], 'all complete local source/target block proofs unchanged')
    require(len(reuse['exact_all20_owned_source_andtarget_blocks']) == 20 and
        reuse['complete_ARM9_COMMON_font_own_context_macro_andname_dependencies_exact'] and
        reuse['all_original_local_display_storage_catalogue_andload_inputs_identical'] and
        reuse['all_other_files_components_andtwo_complete_serialized_inverses_exact'], 'complete foreign-block dependency reuse')
    require(native['runtime'] == stored['runtime'] == lookup['runtime'] == menu['runtime'] == styles['runtime'] and
        native['runtime']['captain'] == 0, 'exact current own Rafael consumer context')
    require(stored['native_sha256'] == sha(Path(conf['compiled_native']).read_bytes()), 'native plane identities')
    validate_natural_dialogue_batch(names)
    require(names['all18_individual_five_gates_pass_in_scoped_context'] and len(names['records']) == conf['scoped_name_count'] == 18,
        'all individual scoped names androles')
    require(native['pages'] == stored['complete_stored_pages'] == conf['native_pages'] == 248 and
        visual['all248_native_body_pages_and12_captions_and18_names_approved'], 'complete native/stored/viewed pages')
    require(visual['all77_actual_body_pages_onseven_readable_sheets_directly_viewed'] and
        visual['six_full_context_samples_and12_menu_cursor_states_directly_viewed'], 'all actual contact sheets reviewed')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
        stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and
        stored['fresh_relocated_native_relative_cases'] == conf['relative_cases'] == 180, 'complete stored glyphs/rows andnative branches')
    entries = {r['id']:r for r in stored['records']+stored['style_records']}
    compiled = {r['id']:r for r in native['records']}
    speeches = [r for r in doc['records'] if r['kind'] != 'typed-choice-label']
    require(set(entries) == set(compiled) == {r['id'] for r in speeches} and len(entries) == conf['speech_count'] == 243,
        'complete ordinary andphysical style membership')
    require(len(stored['records']) == 229 and len(stored['style_records']) == 14 and stored['typed_labels_checked'] == 12,
        'exact distinct stored consumers')
    for row in speeches:
        entry, plane, ref = entries[row['id']], compiled[row['id']], row['planned_integrated_reference']
        require((ref['offset'],ref['record_index'],ref['exact_stored_hex']) ==
            (entry['new_offset'],entry['new_record_index'],entry['stored_hex']), 'complete stored reference')
        require(all(plane[k] == row[k] for k in ['source_reference','current_reference']) and plane['logical_English'] == row['english'],
            'exact source/current/logical prose binding')
        if row.get('native_object_kind') == '4100-style-alternative':
            require(entry['virtual_prefix_not_stored'] and ref['virtual_prefix_not_stored'] and
                entry['source_style_indices'] == row['source_style_indices'], 'native style body andalias membership')
        display = plane['complete_native_English_display']
        if row['kind'] == 'system-FE':
            require(row['source_selector'] == 254 and display['planned_native_row_comparison']['complete_glyph_row_membership_exact'],
                'FE complete row membership')
        for page in ([display] if row['kind'] == 'system-FE' else display['pages']):
            require(sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256'], 'complete approved native plane')
    require(sum(r['kind'] == 'system-FE' for r in speeches) == conf['FE_count'] == 22, 'all FE consumers')
    require(len(lookup['records']) == 243 and lookup['all243_ordinary_andphysical_style_bodies_checked'] and
        lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'], 'all pre-macro catalogue lookups')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases']) ==
        (343,36,650) and loaders['prior_executed_parent_instructions_match_current_runtime'], 'all original block loads/cache modes')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus']) == conf['menu_count'] == 4 and
        menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'], 'complete native menu objects')
    require((menu['native_provider_alignments'],menu['bridged_modal_returns'],menu['complete_English_caption_style_planes']) == (24,96,48),
        'all native menu alignments/returns/caption styles')
    require(len(styles['objects']) == 2 and styles['physical_alternatives'] == 14 and styles['native_target_slot_cases'] == 16 and
        styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives']) == 18,
        'all personality slots/aliases andsemantic rejections')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['source_speech_variants_observed'],
        actual['native_body_pages_observed'],actual['actual_choice_labels'],actual['offline_only_speech_variants']) ==
        (29362,2,75,77,12,168), 'honest actual andoffline scope')
    require(actual['source_speech_variants_observed']+actual['offline_only_speech_variants'] == len(speeches) and
        not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and
        actual['numeric_modal_returns_original_story_branches_stat_effects_andcancellation_unvisited'], 'unvisited content explicit')
    require(actual['both_dynamic_selectors_andboth_complete_style_objects_observed'] and
        actual['all_four_menus_allthree_cursor_states_andordinary_A_to_following_dialogue_observed'] and
        actual['repaired_FE_period_andfour_row_bean_premise_observed'] and actual['Julio_andsect_leader_two_page_transitions_observed'],
        'all distinct controls/rendering/transitions')
    for proof in [first,second]:
        require(proof['all_selected_pages_observed_in_exact_fixture_order'] and
            proof['all_complete_native_body_andheader_planes_andblank_guards_match'], 'complete ordered actual pixels')
    ids = {r['id'] for p in [first,second] for r in p['body_pages']}
    pages = {(r['id'],r['page']) for p in [first,second] for r in p['body_pages']}
    require(len(ids) == 75 and len(pages) == 77 and sorted(ids) == actual['source_IDs_observed'], 'exact observed source/page membership')
    require(menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches'] and
        {(m['source_command_offset'],tuple(m['observed_selected_options'])) for m in menus['menus']} ==
        {(m['source_command_offset'],(0,1,2)) for m in menu['menus']}, 'all cursor states for each menu')
    renderer = previous.previous.NdsImage.open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes()) == conf['final_dependency_ROM_sha256'], 'verified final renderer reference')
    require(sha(renderer.read_file('/__arm9__.bin')) == native['runtime']['ARM9_sha256'] == conf['final_runtime_ARM9_sha256'] and
        sha(renderer.read_file('/GRP/KANJI.FNT')) == native['font_sha256'], 'exact final registered renderer andfont')


source = checked_text(previous.source, {
    "'dk4-reviewed-rafael-plain-scene-release-v1'": "'dk4-reviewed-rafael-mixed-scene-release-v1'",
    "len(speech) == conf['speech_count'] and len(choices) == conf['typed_choice_count'] and not styles['objects']\n            and not any(r.get('native_object_kind') == '4100-style-alternative' for r in speech)":
        "len(speech) == conf['speech_count'] and len(choices) == conf['typed_choice_count'] and len(styles['objects']) == 2\n            and sum(r.get('native_object_kind') == '4100-style-alternative' for r in speech) == 14",
    "rows = [r for r in speech if r['block'] == number]":
        "rows = [r for r in speech if r['block'] == number and r.get('native_object_kind') != '4100-style-alternative']",
})
env = {**previous.plan_release.__globals__, 'qualify_evidence': qualify_evidence}
exec(compile(source, __file__+'::same-source-bound-complete-transaction-with-qualified-native-style-objects', 'exec'), env)
plan_release = env['plan_release']
