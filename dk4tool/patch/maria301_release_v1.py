"""Register the reviewed SC3 transaction over the exact cumulative predecessor."""
from pathlib import Path
from dk4tool.patch import hodram_residual_release_v2 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text

load, sha, require = previous.env['load'], previous.env['sha'], previous.env['require']


def qualify_evidence(conf, doc, stored):
    ready = load(conf['research_completion'])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
        and (ready['records'],ready['revisions'],ready['retentions']) == (301,178,123), '301 sealed individual reviews')
    require(ready['manuscript'] == conf['manuscript'] and ready['manuscript_sha256'] == sha(Path(conf['manuscript']).read_bytes()), 'exact final manuscript')
    for path, digest in ready['evidence'].items():
        require(sha(Path(path).read_bytes()) == digest, 'research dependency: '+path)
    sealed = load(conf['sealed_inputs'])
    require(sealed['research_completion_sha256'] == sha(Path(conf['research_completion']).read_bytes()), 'sealed research identity')
    for key in ['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native','typed_menu','native_styles','actual','visual_review','scoped_names']:
        require(sealed['inputs'][key] == dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())), 'sealed input: '+key)
    native, lookup, loaders, names, menu, styles, actual, visual = [load(conf[k]) for k in
        ['compiled_native','stored_lookup','loaders','scoped_names','typed_menu','native_styles','actual','visual_review']]
    require(native['runtime'] == stored['runtime'] == lookup['runtime'] == menu['runtime'] == styles['runtime'], 'exact native runtime')
    require(names['all36_individual_five_gates_pass_in_scoped_context'] and len(names['records']) == conf['scoped_name_count'] == 36, 'all36 scoped name reviews')
    validate_natural_dialogue_batch(names)
    require(native['runtime']['captain'] == conf['captain'] == 3, 'current Maria context')
    require(native['pages'] == stored['complete_stored_pages'] == visual['final_body_pages'] == conf['native_pages'] == 303, 'all303 final pages')
    require(stored['reconstruction_sha256'] == sha(Path(conf['reconstruction']).read_bytes())
        and lookup['stored_sha256'] == sha(Path(conf['stored_native']).read_bytes()), 'final storage identities')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
        and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['fresh_relocated_native_relative_cases'] == conf['relative_cases'] == 635, 'complete stored display and branch guards')
    require(lookup['all299_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'], 'all299 effective bodies')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases']) == (303,606,0)
        and loaders['all_native_executed_instructions_current_ROM_exact']
        and loaders['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact'], 'whole SC3 loader and parent guards')
    bodies = stored['records']+stored['style_records']; planes = {r['id']:r for r in native['records']}
    require((len(stored['records']),len(stored['style_records']),len(planes)) == (292,7,299), 'ordinary and style membership')
    require(sum(bytes.fromhex(r['stored_hex'])[0] == 254 for r in stored['records']) == conf['FE_count'] == 0, 'no FE approval inferred')
    require(len(styles['objects']) == 1 and styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8
        and styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives']) == 9, 'complete style object and rejections')
    require(len(menu['menus']) == conf['menu_count'] == 1 and stored['typed_labels_checked'] == conf['typed_choice_count'] == 2
        and menu['offline_visual_approved'] and not menu['direct_view_pending'], 'complete menu scope')
    for obj in menu['menus']:
        path = Path(obj['original_receipt']); require(sha(path.read_bytes()) == obj['original_receipt_sha256'], 'native menu dependency')
        proof = load(path)
        require(proof['runtime'] == native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            and proof['native_choice_object_hex'] == obj['target_object_hex'] and len(proof['compiler_negatives_rejected']) == 7, 'exact native menu provider and planes')
    require(set(planes) == {r['id'] for r in bodies} == {r['id'] for r in lookup['records']}, 'complete body identity set')
    for row in bodies:
        for page in planes[row['id']]['complete_native_English_display']['pages']:
            require(sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256'], 'exact approved plane')
    require((actual['frames'],actual['initialized_runs'],actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances'])
        == (conf['actual_frames'],3,92,96,207) and conf['actual_frames'] == 42683, 'honest representative and offline scope')
    require(actual['all_final_selected_body_planes_match_final_compiled_native_planes']
        and actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed']
        and actual['all_four_two_page_transitions_observed'] and actual['corrected_B14_I_glyph_observed']
        and actual['reclaimed_one_page_Havana_paragraph_observed']
        and actual['ordinary_default_menu_return_to_next_fixture_speech_observed']
        and actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing'], 'required gameplay display and returns')
    require(not any(actual[k] for k in ['natural_activation','earned_chronology','full_route','hardware']), 'no broader gameplay claim')
    require(actual['menu']['block'] == 29 and actual['menu']['source_command_offset'] == 304
        and actual['ordinary_default_A_return_frame'] == 17680, 'exact source-bound menu return')
    for path,digest in actual['evidence'].items():require(sha(Path(path).read_bytes()) == digest, 'gameplay dependency: '+path)
    require(len(actual['reviewed_body_sheets']) == 12 and visual['every_final_page_directly_viewed_in_readable_sheets']
        and visual['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked'], 'complete visual review')
    for sheet in actual['reviewed_body_sheets']:
        require(sha(Path(sheet['path']).read_bytes()) == sheet['sha256'], 'exact directly viewed sheet')
    require(visual['all_native_glyph_consumption_bounds_andpagination_guards_pass'], 'selected native page receipts')
    for path,digest in visual['evidence'].items():require(sha(Path(path).read_bytes()) == digest, 'offline display dependency: '+path)
    layout = load(conf['plan'])
    require(not any(r.get('qa_waivers') for r in doc['records']) and not layout['failures']
        and all(not any(i['severity'] in ['warning','error'] for i in r['base_QA']['issues']) for r in layout['records']), 'unwaived formatting checks')
    dependency = previous.env['NdsImage'].open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes()) == conf['final_dependency_ROM_sha256']
        and sha(dependency.read_file('/__arm9__.bin')) == native['runtime']['ARM9_sha256'] == conf['final_runtime_ARM9_sha256']
        and sha(dependency.read_file('/GRP/KANJI.FNT')) == native['font_sha256'], 'current renderer and font dependency')
    rebuilt = load(conf['reconstruction'])
    require(max(g['target_bytes'] for g in rebuilt['groups']) <= 9216, 'original native script allocation bound')
    for run in actual['runs']:
        path = Path(run['run_plan']); require(conf['dependencies'].get(str(path)) == sha(path.read_bytes()), 'frozen run plan')
        plan = load(path); fixture = load(plan['fixture'])
        require(sha(Path(plan['fixture']).read_bytes()) == plan['fixture_sha256']
            and fixture['padded_QA_block_bytes'] <= 9216 and fixture['QA_block_inside_original_stack_buffer'], 'bounded initialized fixture')
    exit_fixture = load(actual['qualified_exit_run']['fixture'])
    require(exit_fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        and len(exit_fixture['original_initializers'])+len(exit_fixture['source_bound_QA_host_opening_exit']) == 47, 'source-complete qualified QA exit')


source = checked_text(previous.prior.source, {
    "'dk4-reviewed-hodram-residual-release-v1'": "'dk4-reviewed-maria301-release-v1'",
    "len(styles['objects']) == 7": "len(styles['objects']) == 1",
    "path == '/data/SC1.DK4'": "path == '/data/SC3.DK4'",
    'len(clean_blocks) == 325': 'len(clean_blocks) == 303',
    'native_loads=325': 'native_loads=303',
})
env = {**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-source-current-transaction-and-inverses-explicit-SC3','exec'),env)
plan_release = env['plan_release']
