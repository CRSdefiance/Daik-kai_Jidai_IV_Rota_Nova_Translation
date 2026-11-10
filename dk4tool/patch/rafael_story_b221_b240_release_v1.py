"""Register the mixed Rafael B221–B240 transaction with the existing complete-block rebuilder."""
from pathlib import Path

from dk4tool.patch import rafael_story_b141_b160_release_v1 as common
from scripts.source_locked_derivation_v5118 import checked_text

load, require, sha = (common.env[name] for name in ('load', 'require', 'sha'))


def qualify_evidence(conf, doc, stored):
    native, names, visual, actual, lookup, loaders, menu, styles, ready = [
        load(conf[key]) for key in ('compiled_native', 'scoped_names', 'visual_review', 'actual', 'stored_lookup',
                                    'loaders', 'typed_menu', 'native_styles', 'research_completion')
    ]
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
            and (ready['records'], ready['revisions'], ready['retentions']) == (270, 221, 49),
            'complete research coverage')
    for path, digest in ready['evidence'].items():
        require(sha(Path(path).read_bytes()) == digest, 'sealed research input changed: ' + path)
    require(all(ready['evidence'].get(conf[key]) == sha(Path(conf[key]).read_bytes()) for key in
                ('manuscript', 'plan', 'reconstruction', 'compiled_native', 'stored_native', 'stored_lookup',
                 'loaders', 'visual_review', 'actual', 'scoped_names', 'typed_menu', 'native_styles')),
            'registered inputs match the sealed research receipt')
    require(native['runtime'] == stored['runtime'] == lookup['runtime'] == menu['runtime'] == styles['runtime']
            and native['runtime']['captain'] == 0, 'qualified Rafael runtime')
    common.validate(names)
    require(names['all_individual_five_gates_pass_for_public_nameplanes'] and len(names['records']) == 26,
            'all 26 public name and role decisions')
    require(native['pages'] == stored['complete_stored_pages'] == visual['body_pages'] == conf['native_pages'] == 279
            and visual['all_body_caption_andname_planes_approved'] and visual['all_actual_pages_and_menus_directly_viewed'],
            'all native, stored and inspected pages')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
            and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
            and stored['fresh_relocated_native_relative_cases'] == conf['relative_cases'] == 170,
            'exact stored pixels and native branch cases')
    entries = {row['id']: row for row in stored['records'] + stored['style_records']}
    planes = {row['id']: row for row in native['records']}
    require(len(entries) == len(planes) == len(lookup['records']) == conf['speech_count'] == 263
            and entries.keys() == planes.keys() == {row['id'] for row in lookup['records']}
            and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],
            'exact pre-macro catalogue membership')
    require(len(stored['style_records']) == styles['physical_alternatives'] == conf['style_count'] == 29
            and len(styles['objects']) == 4 and styles['native_target_slot_cases'] == 32
            and styles['source_alias_equivalence_exact']
            and sum(len(row['rejected']) for row in styles['compiler_negatives']) == 36,
            'all native personality slots and alias rejections')
    speech = [row for row in doc['records'] if row['kind'] != 'typed-choice-label']
    require({row['id'] for row in speech} == entries.keys() and sum(row['kind']=='system-FE' for row in speech) == 3,
            'complete scoped speech and FE membership')
    for row in speech:
        ident = row['id']
        entry, plane, ref = entries[ident], planes[ident], row['planned_integrated_reference']
        require((entry['new_offset'], entry['new_record_index'], entry['stored_hex'])
                == (ref['offset'], ref['record_index'], ref['exact_stored_hex']), 'exact tested stored reference')
        require(all(row[key] == plane[key] for key in ('source_reference','current_reference'))
                and row['english'] == plane['logical_English'], 'source, current and reviewed prose binding')
        if row.get('native_object_kind') == '4100-style-alternative':
            require(entry['virtual_prefix_not_stored'] and ref['virtual_prefix_not_stored']
                    and row['source_style_indices'] == entry['source_style_indices'] == ref['source_style_indices'],
                    'original style aliases and virtual prefix ownership')
        display = plane['complete_native_English_display']
        if row['kind'] == 'system-FE':
            require(display['planned_native_row_comparison']['complete_glyph_row_membership_exact'],
                    'original FE selector and complete staged rows')
        for page in ([display] if row['kind']=='system-FE' else display['pages']):
            require(sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256'],
                    'reviewed native plane matches exactly')
    require((loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'],
            loaders['exact_reused_parent_cases']) == (343,38,648)
            and loaders['prior_executed_parent_instructions_match_current_runtime'],
            'whole archive and source-qualified loader modes')
    require(len(stored['typed_objects']) == len(menu['menus']) == conf['menu_count'] == 3
            and menu['typed_labels'] == stored['typed_labels_checked'] == conf['typed_choice_count'] == 7
            and menu['offline_visual_approved'] and not menu['direct_view_pending'], 'all original choices')
    for item in menu['menus']:
        receipt = Path(item['native_receipt'])
        proof = load(receipt)
        count = len(item['record_IDs'])
        require((item['source_word'], count) in ((0x2100,2),(0x2200,3))
                and sha(receipt.read_bytes()) == item['native_receipt_sha256']
                and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
                and item['target_object_hex'] == item['versions'][-1]['object_hex'],
                'exact native menu word, caption order and tested bytes')
    require((actual['total_frames'], actual['initialized_fixture_runs'], actual['source_speech_variants_observed'],
             actual['native_body_pages_observed'], actual['actual_choice_labels'], actual['offline_only_speech_variants'])
            == (33202,2,86,94,7,177), 'observed and offline scope')
    require(actual['all_four_complete_style_commands_observed_under_unmodified_default_roles']
            and actual['all_three_menu_instances_default_cursor_and_following_fixture_speech_observed']
            and actual['other_cursor_states_VM_returns_branches_andcancellation_offline_only']
            and not any(actual[key] for key in ('natural_activation','original_location','earned_chronology','full_route','hardware')),
            'observed default style and menu transitions with original outcomes unvisited')
    require({(row['block'], row['source_command_offset']) for row in actual['menus']}
            == {(row['block'], row['offset']) for row in stored['typed_objects']}
            and all(row['observed_selected_options'] == [0] for row in actual['menus']), 'live menus match stored occurrences')
    renderer = common.env['NdsImage'].open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes()) == conf['final_dependency_ROM_sha256']
            and sha(renderer.read_file('/__arm9__.bin')) == native['runtime']['ARM9_sha256'] == conf['final_runtime_ARM9_sha256']
            and sha(renderer.read_file('/GRP/KANJI.FNT')) == native['font_sha256'],
            'verified final renderer, font and right-bound dependency')


source = checked_text(common.source, {
    """require(len(speech) == conf['speech_count'] and len(choices) == conf['typed_choice_count'] and not styles['objects']
            and not any(r.get('native_object_kind') == '4100-style-alternative' for r in speech), 'exact qualified consumers')""":
        """require(len(speech) == conf['speech_count'] and len(choices) == conf['typed_choice_count']
            and len(styles['objects']) == 4 and sum(r.get('native_object_kind') == '4100-style-alternative' for r in speech)
            == conf['style_count'], 'exact mixed speech, voice and menu membership')""",
    """        require(row['english'] == plan['logical_English'] and row['planned_English_markup'] == plan['formatted_markup'], 'logical andformatted plan binding')""":
        """        require(row['english'] == plan['logical_English'], 'reviewed logical prose')
        if row.get('source_staged_FE') or row.get('source_staged_progressive'):
            require(row['source_staging_reason'] == plan['source_staging_reason']
                and row['source_staged_native_rows'] == plan['approved_native_structural_layout'], 'exact source-staged layout')
        else:
            require(row['planned_English_markup'] == plan['formatted_markup'], 'exact automatically formatted plan')""",
    "rows = [deepcopy(r) for r in speech if r['block'] == number]":
        "rows = [deepcopy(r) for r in speech if r['block'] == number and r.get('native_object_kind') != '4100-style-alternative']",
})
env = {**common.env, 'qualify_evidence': qualify_evidence, 'validate': common.validate, '__file__': __file__}
exec(compile(source, __file__+'::same-complete-transaction-with-source-staged-and-mixed-native-records', 'exec'), env)
plan_release = env['plan_release']

