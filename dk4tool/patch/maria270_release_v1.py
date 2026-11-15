"""Source-bound Maria270 append retaining the exact registered market-corrected ARM9."""
import inspect
from pathlib import Path
from dk4tool.patch import maria301_release_v2 as previous
from dk4tool.patch.market_goods_info_terminator_v1 import transform
from scripts.source_locked_derivation_v5118 import checked_text

load,sha,require=previous.env['load'],previous.env['sha'],previous.env['require']

def market_dependencies(conf,native,stored,lookup):
    path=conf['market_parent_qualification'];proof=load(path)
    require(proof==stored['exact_registered_market_parent_reuse']==lookup['exact_registered_market_parent_reuse'], 'exact qualified market parent')
    require(proof['native_runtime']==native['runtime'], 'actual old native context identity retained')
    require(stored['market_pointer_read_andexecution_dependency_guards_pass'] and lookup['market_pointer_read_andexecution_dependency_guards_pass'], 'no market dependency in native storage calls')
    image=previous.env['NdsImage'].open(conf['final_dependency_ROM'])
    original=previous.env['NdsImage'].open(native['runtime']['candidate'])
    require(sha(Path(native['runtime']['candidate']).read_bytes())==native['runtime']['candidate_sha256'], 'frozen original native candidate')
    arm,receipt=transform(original.read_file('/__arm9__.bin'))
    require(receipt==proof['exact_registered_market_transform'] and image.read_file('/__arm9__.bin')==arm, 'exact market-only ARM9 transform')
    require(sha(Path(conf['final_dependency_ROM']).read_bytes())==conf['final_dependency_ROM_sha256']==proof['target_candidate_sha256'], 'current registered market parent')
    require(sha(arm)==conf['final_runtime_ARM9_sha256']==proof['target_ARM9_sha256'], 'retained corrected ARM9')
    require(all(image.read_file(p)==original.read_file(p) for _,p,_ in original.iter_files()), 'all old native files preserved')
    require(sha(image.read_file('/GRP/KANJI.FNT'))==native['font_sha256'], 'exact native font')

evidence_source=checked_text(inspect.getsource(previous.previous.qualify_evidence),{
    '(301,178,123)':'(270,161,109)', '301 sealed individual reviews':'270 sealed individual reviews',
    "names['all36_individual_five_gates_pass_in_scoped_context']":"names['all28_individual_five_gates_pass_in_scoped_context']",
    "conf['scoped_name_count'] == 36":"conf['scoped_name_count'] == 28", 'all36 scoped name reviews':'all28 scoped name reviews',
    "conf['native_pages'] == 303":"conf['native_pages'] == 272", 'all303 final pages':'all272 final pages',
    "conf['relative_cases'] == 635":"conf['relative_cases'] == 480",
    "lookup['all299_ordinary_and_style_bodies_checked']":"lookup['all266_ordinary_and_style_bodies_checked']",'all299 effective bodies':'all266 effective bodies',
    '(292,7,299)':'(266,0,266)',
    "conf['FE_count'] == 0, 'no FE approval inferred'":"conf['FE_count'] == 1, 'exact one approved FE body'",
    "require(len(styles['objects']) == 1 and styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8\n        and styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives']) == 9, 'complete style object and rejections')":
        "require(not styles['objects'] and styles['physical_alternatives']==styles['native_target_slot_cases']==0 and not stored['style_records'], 'exact empty style scope')",
    "conf['menu_count'] == 1":"conf['menu_count'] == 2", "conf['typed_choice_count'] == 2":"conf['typed_choice_count'] == 4",
    "        for page in planes[row['id']]['complete_native_English_display']['pages']:":
        "        display=planes[row['id']]['complete_native_English_display']\n        for page in ([display] if bytes.fromhex(row['stored_hex'])[0]==254 else display['pages']):",
    '(conf[\'actual_frames\'],3,92,96,207)':'(conf[\'actual_frames\'],4,63,69,203)', "conf['actual_frames'] == 42683":"conf['actual_frames'] == 41924",
    "actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed']":"actual['all_selected_pages_directly_viewed']",
    "actual['all_four_two_page_transitions_observed'] and actual['corrected_B14_I_glyph_observed']":"actual['all_six_two_page_transitions_observed'] and actual['FE_to_named_speaker_transition_observed']",
    "actual['reclaimed_one_page_Havana_paragraph_observed']":"actual['both_reclaimed_B49_single_pages_andcomplete_question_tag_observed']",
    "actual['ordinary_default_menu_return_to_next_fixture_speech_observed']":"actual['ordinary_default_menu_returns_to_next_fixture_speech_observed']",
    "actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']":"actual['complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing']",
    "require(actual['menu']['block'] == 29 and actual['menu']['source_command_offset'] == 304\n        and actual['ordinary_default_A_return_frame'] == 17680, 'exact source-bound menu return')":
        "require([(m['block'],m['source_command_offset'],m['ordinary_A_frame']) for m in actual['menus']]==[(38,616,6160),(49,2416,7840)], 'exact source-bound menu returns')",
    "len(actual['reviewed_body_sheets']) == 12 and visual['every_final_page_directly_viewed_in_readable_sheets']":"len(actual['reviewed_body_sheets']) == 16 and visual['all272_selected_body_pages_directly_viewed']",
    "visual['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']":"visual['all42_name_strings_andboth_menu_sheets_directly_viewed']",
    "visual['all_native_glyph_consumption_bounds_andpagination_guards_pass']":"visual['all_formatted_body_macro_alignments_checked'] and native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']",
    "    dependency = previous.env['NdsImage'].open(conf['final_dependency_ROM'])\n    require(sha(Path(conf['final_dependency_ROM']).read_bytes()) == conf['final_dependency_ROM_sha256']\n        and sha(dependency.read_file('/__arm9__.bin')) == native['runtime']['ARM9_sha256'] == conf['final_runtime_ARM9_sha256']\n        and sha(dependency.read_file('/GRP/KANJI.FNT')) == native['font_sha256'], 'current renderer and font dependency')":
        "    market_dependencies(conf,native,stored,lookup)",
})
evidence_env={**previous.previous.qualify_evidence.__globals__,'market_dependencies':market_dependencies}
exec(compile(evidence_source,__file__+'::same-complete-evidence-contract-exact-Maria270-scope','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
source=checked_text(previous.previous.source,{
    "'dk4-reviewed-maria301-release-v1'":"'dk4-reviewed-maria270-release-v1'",
    "len(styles['objects']) == 1":"len(styles['objects']) == 0",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::unchanged-source-current-SC3-transaction-inverses-complete-caption-references','exec'),env)
plan_release=env['plan_release']
