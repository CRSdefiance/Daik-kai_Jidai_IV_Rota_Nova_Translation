"""Pure303-record SC3 append, retaining complete mixed-object and source inverse guards."""
import inspect
from pathlib import Path
from dk4tool.patch import maria301_release_v2 as previous
from dk4tool.script.maria303_source_alignment_v1 import rebuild_block
from scripts.source_locked_derivation_v5118 import checked_text

load, sha, require = previous.env['load'], previous.env['sha'], previous.env['require']
evidence_source = checked_text(inspect.getsource(previous.previous.qualify_evidence), {
    '(301,178,123)': '(303,181,122)', '301 sealed individual reviews': '303 sealed individual reviews',
    "names['all36_individual_five_gates_pass_in_scoped_context']": "names['all20_individual_five_gates_pass_in_scoped_context']",
    "conf['scoped_name_count'] == 36": "conf['scoped_name_count'] == 20", 'all36 scoped name reviews': 'all20 scoped name reviews',
    "conf['native_pages'] == 303": "conf['native_pages'] == 299", 'all303 final pages': 'all299 final pages',
    "conf['relative_cases'] == 635": "conf['relative_cases'] == 120",
    '(292,7,299)': '(299,0,299)',
    "conf['FE_count'] == 0, 'no FE approval inferred'": "conf['FE_count'] == 12, 'exact12 original FE panels'",
    "require(len(styles['objects']) == 1 and styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8\n        and styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives']) == 9, 'complete style object and rejections')":
        "require(not styles['objects'] and styles['physical_alternatives'] == styles['native_target_slot_cases'] == 0 and styles['source_has_no_4100_style_objects'] and not stored['style_records'], 'exact empty style scope')",
    "conf['menu_count'] == 1": "conf['menu_count'] == 2",
    "conf['typed_choice_count'] == 2": "conf['typed_choice_count'] == 4",
    "        for page in planes[row['id']]['complete_native_English_display']['pages']:":
        "        display=planes[row['id']]['complete_native_English_display']\n        for page in ([display] if bytes.fromhex(row['stored_hex'])[0] == 254 else display['pages']):",
    '(conf[\'actual_frames\'],3,92,96,207)': '(conf[\'actual_frames\'],2,116,116,183)',
    "conf['actual_frames'] == 42683": "conf['actual_frames'] == 48322",
    "actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed']": "actual['all116_selected_pages_directly_viewed']",
    "actual['all_four_two_page_transitions_observed'] and actual['corrected_B14_I_glyph_observed']":
        "actual['both_reclaimed_single_page_paragraphs_andnext_source_returns_observed'] and actual['corrected_B59_ASCII_I_andB61_normal_F_glyphs_observed']",
    "actual['reclaimed_one_page_Havana_paragraph_observed']": "actual['inline_FE_boy_andnamed_portrait_return_observed']",
    "actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']": "actual['complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing']",
    "require(actual['menu']['block'] == 29 and actual['menu']['source_command_offset'] == 304\n        and actual['ordinary_default_A_return_frame'] == 17680, 'exact source-bound menu return')":
        "require({(m['block'],m['source_command_offset']) for m in actual['menus']} == {(60,428),(64,104)} and all(m['observed_selected_options'] == [0] for m in actual['menus']) and actual['numeric_modal_return_register_other_menu_indices_andcancellation_unvisited'], 'exact source-bound menu display and honest returns')",
    "len(actual['reviewed_body_sheets']) == 12 and visual['every_final_page_directly_viewed_in_readable_sheets']":
        "len(actual['reviewed_body_sheets']) == 10 and visual['all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse']",
    "visual['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']": "visual['all24_names_andfour_captions_directly_viewed']",
    "visual['all_native_glyph_consumption_bounds_andpagination_guards_pass']":
        "native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact'] and native['all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse'] and native['selected_alignment_cases'] == 1196",
})
evidence_env = dict(previous.previous.qualify_evidence.__globals__)
exec(compile(evidence_source, __file__+'::same-five-gates-storage-native-pixels-loaders-gameplay303', 'exec'), evidence_env)


def qualify_evidence(conf, doc, stored):
    evidence_env['qualify_evidence'](conf, doc, stored)
    path = Path(conf['source_alignment_qualification'])
    require(conf['dependencies'].get(str(path)) == sha(path.read_bytes()), 'exact source alignment qualification')
    alignment = load(path)
    require(alignment['owner'] == 'DK4_MES_B62_R0053'
        and alignment['complete_native_command_extent_unchanged'] == 38
        and alignment['source_meaning_body_andcontrols_unchanged']
        and alignment['ownership_negative_cases_rejected'] == ['wrong owner', 'shifted source', 'source terminator changed', 'current terminator changed'], 'one exact old source/current terminator shift')


source = checked_text(previous.previous.source, {
    "'dk4-reviewed-maria301-release-v1'": "'dk4-reviewed-maria303-release-v1'",
    "len(styles['objects']) == 1": "len(styles['objects']) == 0",
})
env = {**previous.env, 'qualify_evidence': qualify_evidence, 'rebuild_block': rebuild_block, '__file__': __file__}
exec(compile(source, __file__+'::unchanged-complete-transaction-with-exact-qualified-source-span', 'exec'), env)
plan_release = env['plan_release']
