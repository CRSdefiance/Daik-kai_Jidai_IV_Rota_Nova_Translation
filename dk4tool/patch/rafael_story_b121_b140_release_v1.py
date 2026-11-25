"""Source-bound integration of307 ordinary bodies,34 style bodies and10 captions."""
from pathlib import Path
from dk4tool.patch import rafael_story_b101_b120_release_v1 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_evidence(conf, doc, stored):
    load, require, sha = previous.previous.previous.load, previous.previous.previous.require, previous.previous.previous.sha
    native, names, visual, actual, lookup, loaders, menu, styles, first, second, first_menu, second_menu, reuse = [load(conf[k]) for k in
        ['compiled_native','scoped_names','visual_review','actual','stored_lookup','loaders','typed_menu','native_styles',
         'focused_pixels','menu_body_pixels','tutorial_menu_pixels','story_menu_pixels','dependency_qualification']]
    original, integration, metadata = [load(conf[k]) for k in ['research_reconstruction','reconstruction','metadata_qualification']]
    require(stored['reconstruction_sha256'] == sha(Path(conf['research_reconstruction']).read_bytes()), 'exact original stored proof')
    require(reuse['original351_reconstruction_sha256'] == stored['reconstruction_sha256'] and
        integration['original_reconstruction_sha256'] == reuse['rebased_reconstruction_sha256'], 'qualified cumulative rebase')
    require(integration['groups'] == original['groups'] and len(reuse['all20_local_source_andtarget_blocks']) == 20,
        'all complete local source/target block proofs unchanged')
    require(reuse['full_ARM9_COMMON_font_names_andall_unowned_files_components_exact'] and reuse['three_complete_serialized_inverses_exact']
        and reuse['original_display_storage_catalogue_andlocal_loader_inputs_exact'], 'exact dependency-compatible block rebase')
    require(metadata['all_source_current_references_wording_decisions_findings_controls_five_gates_andstored_bytes_unchanged'] and
        metadata['all_ROMs_andoriginal_proofs_unchanged'], 'metadata-only successor preserves all reviewed bytes')
    require(native['runtime'] == stored['runtime'] == lookup['runtime'] == menu['runtime'] == styles['runtime'] and
        native['runtime']['captain'] == 0, 'current own Rafael consumer context')
    require(stored['native_sha256'] == sha(Path(conf['compiled_native']).read_bytes()), 'exact native planes')
    validate_natural_dialogue_batch(names)
    require(len(names['records']) == conf['scoped_name_count'] == 22 and all(all(r['review'].values()) for r in names['records']) and
        names['all22_individual_five_gates_pass_for_public_nameplanes'] and not names['all22_name_formatting_gates_pending'], 'individual scoped public names')
    require(native['pages'] == stored['complete_stored_pages'] == conf['native_pages'] == 344 and
        visual['all344_body_pages_10_captions_22_public_names_approved'], 'complete native/stored/viewed pages')
    require(visual['all134_observed_body_pages_andall5_menu_captures_directly_viewed'] and
        visual['all12_compact_2_fullscene_2_menu_sheets_directly_viewed'], 'complete readable actual visual review')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
        stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['fresh_relocated_native_relative_cases'] == conf['relative_cases'] == 405,
        'stored bytes/glyphs/rows/guards/branches')
    entries = {r['id']:r for r in stored['records']+stored['style_records']}
    compiled = {r['id']:r for r in native['records']}
    speeches = [r for r in doc['records'] if r['kind'] != 'typed-choice-label']
    require(set(entries) == set(compiled) == {r['id'] for r in speeches} and len(entries) == conf['speech_count'] == 341, 'complete body membership')
    require(len(stored['records']) == 307 and len(stored['style_records']) == 34 and stored['typed_labels_checked'] == 10, 'distinct stored consumers')
    for row in speeches:
        entry, plane, ref = entries[row['id']], compiled[row['id']], row['planned_integrated_reference']
        require((ref['offset'],ref['record_index'],ref['exact_stored_hex']) ==
            (entry['new_offset'],entry['new_record_index'],entry['stored_hex']), 'exact tested stored reference')
        require(all(plane[k] == row[k] for k in ['source_reference','current_reference']) and plane['logical_English'] == row['english'], 'source/current/logical prose')
        if row.get('native_object_kind') == '4100-style-alternative':
            require(entry['virtual_prefix_not_stored'] and ref['virtual_prefix_not_stored'] and entry['source_style_indices'] == row['source_style_indices'], 'style aliases andphysical storage')
        display = plane['complete_native_English_display']
        if row['kind'] == 'system-FE':
            require(row['source_selector'] == 254 and display['planned_native_row_comparison']['complete_glyph_row_membership_exact'], 'FE selector/complete row membership')
        for page in ([display] if row['kind']=='system-FE' else display['pages']):
            require(sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256'], 'approved complete native plane')
    require(sum(r['kind']=='system-FE' for r in speeches) == conf['FE_count'] == 15, 'complete FE membership')
    require(len(lookup['records']) == 341 and lookup['all341_ordinary_andphysical_style_bodies_checked'] and
        lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'], 'all effective pre-macro bodies')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases']) == (343,36,650)
        and loaders['prior_executed_parent_instructions_match_current_runtime'], 'all native archive loads andcache modes')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus']) == conf['menu_count'] == 5 and
        menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'], 'complete menu objects')
    require((menu['native_provider_alignments'],menu['bridged_modal_returns'],menu['complete_English_caption_style_planes']) == (30,90,40), 'menu provider/return/style cases')
    require(len(styles['objects']) == 6 and styles['physical_alternatives'] == 34 and styles['native_target_slot_cases'] == 48 and
        styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives']) == 54, 'complete personality slots/aliases/negative cases')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['source_speech_variants_observed'],actual['native_body_pages_observed'],
        actual['actual_choice_labels'],actual['offline_only_speech_variants']) == (43282,2,132,134,10,209), 'honest actual/offline scope')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and
        actual['all_six_complete_style_commands_observed_under_unmodified_default_roles'] and
        actual['other_cursor_states_VM_returns_branches_andcancellation_offline_only'], 'unvisited content anddefault roles explicit')
    for proof in [first,second]:
        require(proof['all_selected_pages_observed_in_exact_fixture_order'] and proof['all_complete_native_body_andheader_planes_andblank_guards_match'], 'actual complete planes andorder')
    ids = {r['id'] for p in [first,second] for r in p['body_pages']}
    pages = {(r['id'],r['page']) for p in [first,second] for r in p['body_pages']}
    require(len(ids)==132 and len(pages)==134 and sorted(ids)==actual['source_IDs_observed'], 'individual observed source/page membership')
    observed = []
    for proof in [first_menu,second_menu]:
        require(proof['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches'] and
            proof['numeric_modal_return_register_original_story_branches_andcancellation_unvisited'], 'complete actual menu pixels andscope')
        observed.extend(proof['menus'])
    require(len(observed)==5 and all(r['observed_selected_options']==[0] for r in observed), 'only default actual cursor state')
    require({r['source_command_offset'] for r in observed} == {r['source_command_offset'] for r in menu['menus']}, 'all selected menu objects')
    renderer = previous.previous.previous.NdsImage.open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes()) == conf['final_dependency_ROM_sha256'] and
        sha(renderer.read_file('/__arm9__.bin')) == native['runtime']['ARM9_sha256'] == conf['final_runtime_ARM9_sha256'] and
        sha(renderer.read_file('/GRP/KANJI.FNT')) == native['font_sha256'], 'exact verified final renderer andfont')


source = checked_text(previous.source, {
    "len(styles['objects']) == 2": "len(styles['objects']) == 6",
    "for r in speech) == 14": "for r in speech) == 34",
})
env = {**previous.plan_release.__globals__, 'qualify_evidence': qualify_evidence}
exec(compile(source, __file__+'::same-source-bound-mixed-transaction-six-style-objects', 'exec'), env)
plan_release = env['plan_release']
