"""Pure complete-block SC0 integration with scoped native and representative display proofs."""
import inspect
from pathlib import Path
from dk4tool.patch import rafael_B51_B60_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_evidence(conf, doc, stored):
    load, require, sha = previous.load, previous.require, previous.sha
    native, visual, actual, names, lookup, loaders, menu, pixels, menu_body, menu_pixels = [load(conf[k]) for k in
        ['compiled_native','visual_review','actual','scoped_names','stored_lookup','loaders','typed_menu','focused_pixels','menu_body_pixels','menu_pixels']]
    previous.validate_natural_dialogue_batch(names)
    require(native['runtime'] == stored['runtime'] == lookup['runtime'] and native['runtime']['captain'] == 0, 'explicit current own Rafael context')
    require(names['all_five_gates_pass_in_scoped_context'] and len(names['records']) == conf['scoped_name_count'], 'individual scoped names androles')
    require(native['pages'] == stored['complete_stored_pages'] == visual['body_pages'] == conf['native_pages'], 'all native/stored/viewed body pages')
    require(visual['all256_final_pages_directly_viewed_or_exact_native_plane_reuse'] and visual['all6_labels_and24_current_reviewed_caption_style_planes_checked']
        and visual['all18_scoped_nameplanes_viewed'], 'complete body/menu/name visual coverage')
    require(stored['native_sha256'] == sha(Path(conf['compiled_native']).read_bytes()) and stored['reconstruction_sha256'] == sha(Path(conf['reconstruction']).read_bytes()), 'exact native/storage identities')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['fresh_relocated_native_relative_cases'] == conf['relative_cases'], 'complete stored glyphs andnative branch guards')
    speech = [r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    entries, compiled = [{r['id']:r for r in proof['records']} for proof in [stored,native]]
    require(set(entries) == set(compiled) == {r['id'] for r in speech} and len(entries) == conf['speech_count'], 'complete individual speech membership')
    for row in speech:
        entry, plane, ref = entries[row['id']], compiled[row['id']], row['planned_integrated_reference']
        require((ref['offset'],ref['record_index'],ref['exact_stored_hex']) == (entry['new_offset'],entry['new_record_index'],entry['stored_hex']), 'tested complete stored reference')
        require(all(plane[k] == row[k] for k in ['source_reference','current_reference']) and plane['logical_English'] == row['english'], 'exact source/current/prose binding')
        display = plane['complete_native_English_display']
        if row['kind'] == 'system-FE':
            require(row['source_selector'] == 254 and display['planned_native_row_comparison']['complete_glyph_row_membership_exact'], 'FE selector andfull native row membership')
        for page in ([display] if row['kind']=='system-FE' else display['pages']):
            require(sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256'], 'complete viewed plane unchanged')
    require(sum(r['kind']=='system-FE' for r in speech) == conf['FE_count'], 'complete FE membership')
    require(len(lookup['records']) == conf['speech_count'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'], 'original catalogue cannot restore old wording')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases']) ==
        (343,2*len(conf['blocks']),686-2*len(conf['blocks'])) and loaders['prior_executed_parent_instructions_match_current_runtime'], 'all native loads andparent modes')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and menu['typed_labels'] == conf['typed_choice_count'] and len(menu['menus']) == conf['menu_count'], 'all complete original native menu objects')
    for obj in menu['menus']:
        path = Path(obj['native_proof']); proof = load(path)
        require(sha(path.read_bytes()) == obj['native_proof_sha256'], 'native menu proof identity')
        require(proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and proof['source_index_andcount_preserved']
            and len(proof['compiler_negatives_rejected']) == 7, 'complete native captions/indices andnegative cases')
        require((proof['native_provider_alignments'],proof['bridged_modal_returns'],proof['complete_English_caption_style_planes']) == (6,18,8), 'native alignments/styles/returns')
    require(actual['total_frames'] == conf['actual_frames'] and actual['initialized_fixture_runs'] == conf['actual_runs'], 'terminal initialized tests')
    require((actual['source_speeches_observed'],actual['native_body_pages_observed'],actual['actual_choice_labels'],actual['offline_only_source_speeches']) ==
        tuple(conf[k] for k in ['actual_speeches','actual_body_pages','typed_choice_count','offline_speeches']), 'honest source/page/menu coverage')
    require(actual['source_speeches_observed']+actual['offline_only_source_speeches'] == conf['speech_count'], 'no omitted orduplicated source credit')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        and actual['original_story_branches_numeric_return_registers_stat_effects_andcancellation_unvisited'], 'unvisited story outcomes remain explicit')
    require(actual['all12_newly_scoped_identities_andthree_distinct_Sailor_portraits_observed'] and actual['all_three_native_menus_both_cursor_states_andA_to_following_dialogue_observed']
        and actual['full_Janus_ten_speech_conversation_payer_exchange_andtwo_page_sentence_transition_observed'], 'required distinct rendering andtransition risks')
    require(visual['actual_four_compact_body_sheets_one_full_context_sheet_one_menu_body_sheet_andone_cursor_sheet_directly_viewed'], 'actual manual visual review')
    for proof in [pixels,menu_body]:
        require(proof['all_selected_pages_observed_in_exact_fixture_order'] and proof['all_complete_native_body_andheader_planes_andblank_guards_match'], 'complete actual pixels andcall order')
    ids = {r['id'] for p in [pixels,menu_body] for r in p['body_pages']}
    pages = {(r['id'],r['page']) for p in [pixels,menu_body] for r in p['body_pages']}
    require(len(ids) == conf['actual_speeches'] and len(pages) == conf['actual_body_pages'] and sorted(ids) == actual['source_IDs_observed'], 'individual current-wording actual membership')
    require(menu_pixels['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches'] and
        {(r['source_command_offset'],tuple(r['observed_selected_options'])) for r in menu_pixels['menus']} ==
        {(r['source_command_offset'],(0,1)) for r in menu['menus']}, 'all complete menu captions andboth actual cursor states')
    dependency = load(conf['dependency_qualification'])
    require(dependency['current_runtime'] == native['runtime'] and dependency['exact_ARM9_COMMON_font_andcomplete_actor_array'] and dependency['owned_source_blocks_exact'], 'qualified renderer/name/macro reuse')
    renderer = previous.NdsImage.open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes()) == conf['final_dependency_ROM_sha256'], 'verified final renderer reference')
    require(sha(renderer.read_file('/__arm9__.bin')) == native['runtime']['ARM9_sha256'] == conf['final_runtime_ARM9_sha256'], 'exact final registered renderer')
    require(sha(renderer.read_file('/GRP/KANJI.FNT')) == native['font_sha256'], 'unchanged native font')


source = checked_text(inspect.getsource(previous.plan_release), {
    "'dk4-rafael-B51-B60-release-v1'": "'dk4-reviewed-rafael-plain-scene-release-v1'",
    "== conf['record_count'] == 249": "== conf['record_count']",
    "len(speech) == 245 and len(choices) == 4": "len(speech) == conf['speech_count'] and len(choices) == conf['typed_choice_count']",
    "len(layout['records']) == 245": "len(layout['records']) == conf['speech_count']",
    "require(doc['blocks'] == conf['blocks'] == reconstruction['changed_blocks'] == list(range(51,61)), 'all ten complete scenes')":
        """require(doc['blocks'] == conf['reviewed_blocks'] == reconstruction['reviewed_blocks'], 'complete reviewed scope')
    require(conf['blocks'] == reconstruction['changed_blocks'] and set(doc['blocks'])-set(conf['blocks']) == set(reconstruction['unchanged_control_only_blocks']), 'changed versus control-only blocks')""",
    "[g['block'] for g in reconstruction['groups']] == conf['blocks']": "[g['block'] for g in reconstruction['groups']] == conf['reviewed_blocks']",
    'native_pages=253,fresh_relative_cases=380,native_loads=343,typed_labels=4,actual_frames=18662,':
        "native_pages=conf['native_pages'],fresh_relative_cases=conf['relative_cases'],native_loads=343,typed_labels=conf['typed_choice_count'],actual_frames=conf['actual_frames'],",
})
env = {**previous.plan_release.__globals__, 'qualify_evidence':qualify_evidence}
exec(compile(source, __file__+'::same-full-source-current-rebuild-pure-transaction-scoped-plain-SC0', 'exec'), env)
plan_release = env['plan_release']
