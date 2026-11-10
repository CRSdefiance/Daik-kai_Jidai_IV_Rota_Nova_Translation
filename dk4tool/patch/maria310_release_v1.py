"""Pure seven-exchange SC3 append with the exact qualified FE storage amendment."""
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria301_release_v2 as previous
from dk4tool.script.reviewed_FE_storage_padding_v1 import remove_FE_text_parity_space
from scripts.source_locked_derivation_v5118 import checked_text

load,sha,require=previous.env['load'],previous.env['sha'],previous.env['require']

def amend_storage(arm,target,proof,group,inventory):
    if 'owned_FE_storage_amendment' not in group:return target,proof
    receipt_path=Path(group['owned_FE_storage_amendment']);expected=load(receipt_path)
    require(sha(receipt_path.read_bytes())==group['owned_FE_storage_amendment_sha256'],'exact FE storage receipt')
    owner=expected['owner']
    require(group['block']==54 and owner['id']=='DK4_MES_B54_R0507' and owner['source_reference']['offset']==4509,'exclusive clean FE owner')
    target,amendment=remove_FE_text_parity_space(arm,target,owner,inventory)
    require(all(v==expected[k] for k,v in amendment.items()),'fresh complete FE storage inverse and native command maps')
    require(expected['semantic_negatives_rejected']==['control','compiled','offset','stored'],'FE ownership rejections')
    result=deepcopy(proof);mapping={c['old_offset']:c['new_offset'] for c in amendment['command_map']}
    commands={c['offset']:c for c in amendment['all_target_commands']}
    for row in result['text_records']:
        row['new_offset']=mapping[row['new_offset']-5]+5
        if row['id']==owner['id']:
            require(row['compiled_hex']==owner['compiled_hex'] and row['parity_space_added'],'exact compiled full panel')
            row.update(stored_hex=row['compiled_hex'],parity_space_added=False,owned_FE_storage_alignment=True)
        at=row['new_offset'];raw=bytes.fromhex(row['stored_hex'])
        require(target[at:at+len(raw)+1]==raw+b'\0','complete amended body and terminator')
        row['new_record_index']=target[:at].count(b'\0')
    for row in result['command_map']:
        row['new_offset']=mapping[row['new_offset']];row['new_extent']=commands[row['new_offset']]['native_extent']
    fixes={f['old_offset']:f for f in amendment['relative_fixups']}
    for row in result['relative_fixups']:
        fix=fixes[row['new_offset']]
        require(row['new_span']==fix['old_span'] and row['new_target']==fix['old_target'],'composed exact relative origin')
        row.update(new_offset=fix['new_offset'],new_span=fix['new_span'],new_target=fix['new_target'])
    result.update(all_target_commands=amendment['all_target_commands'],new_logical_end=amendment['new_logical_end'],
        new_tail_hex=target[amendment['new_logical_end']:].hex())
    return target,result

evidence_source=checked_text(inspect.getsource(previous.previous.qualify_evidence),{
    '(301,178,123)':'(310,184,126)','301 sealed individual reviews':'310 sealed individual reviews',
    "names['all36_individual_five_gates_pass_in_scoped_context']":"names['all26_individual_five_gates_pass_in_scoped_context']",
    "conf['scoped_name_count'] == 36":"conf['scoped_name_count'] == 26",'all36 scoped name reviews':'all26 scoped name reviews',
    "conf['native_pages'] == 303":"conf['native_pages'] == 318",'all303 final pages':'all318 final pages',
    "conf['relative_cases'] == 635":"conf['relative_cases'] == 660",
    "lookup['all299_ordinary_and_style_bodies_checked']":"lookup['all310_ordinary_bodies_checked']",'all299 effective bodies':'all310 effective bodies',
    '(292,7,299)':'(310,0,310)',
    "conf['FE_count'] == 0, 'no FE approval inferred'":"conf['FE_count'] == 31, 'exact31 original FE bodies'",
    "require(len(styles['objects']) == 1 and styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8\n        and styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives']) == 9, 'complete style object and rejections')":
        "require(not styles['objects'] and styles['physical_alternatives']==styles['native_target_slot_cases']==0 and styles['source_has_no_4100_style_objects'] and not stored['style_records'], 'exact empty style scope')",
    "conf['menu_count'] == 1":"conf['menu_count'] == 0", "conf['typed_choice_count'] == 2":"conf['typed_choice_count'] == 0",
    "        for page in planes[row['id']]['complete_native_English_display']['pages']:":
        "        display=planes[row['id']]['complete_native_English_display']\n        for page in ([display] if bytes.fromhex(row['stored_hex'])[0]==254 else display['pages']):",
    "(conf['actual_frames'],3,92,96,207)":"(conf['actual_frames'],2,64,70,246)","conf['actual_frames'] == 42683":"conf['actual_frames'] == 36802",
    "actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed']":"actual['all70_selected_pages_directly_viewed']",
    "actual['all_four_two_page_transitions_observed'] and actual['corrected_B14_I_glyph_observed']":
        "actual['all_six_distinct_two_page_transitions_observed'] and actual['corrected_B56_B57_ASCII_I_F_glyphs_observed']",
    "actual['reclaimed_one_page_Havana_paragraph_observed']":"actual['all_five_repaired_FE_panels_andstorage_alignment_observed']",
    "actual['ordinary_default_menu_return_to_next_fixture_speech_observed']":"actual['no_typed_menus_in_source_scope']",
    "actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']":"actual['complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing']",
    "require(actual['menu']['block'] == 29 and actual['menu']['source_command_offset'] == 304\n        and actual['ordinary_default_A_return_frame'] == 17680, 'exact source-bound menu return')":
        "require(actual['no_extra_blank_FE_panel_between_R507_andR511'] and actual['ordinary_16frame_A_return_observed'], 'exact FE A return without blank page')",
    "len(actual['reviewed_body_sheets']) == 12 and visual['every_final_page_directly_viewed_in_readable_sheets']":
        "len(actual['reviewed_body_sheets']) == 6 and visual['all318_final_pages_directly_viewed_or_exact_visual_reuse']",
    "visual['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']":"visual['all31_name_strings_directly_viewed']",
    "visual['all_native_glyph_consumption_bounds_andpagination_guards_pass']":
        "native['all_records_native_checked_once_or_exact_compiled_dependency_reuse'] and native['all318_final_pages_directly_viewed_or_exact_visual_dependency_reuse'] and native['selected_alignment_cases']==1240",
})
evidence_env=dict(previous.previous.qualify_evidence.__globals__)
exec(compile(evidence_source,__file__+'::same-five-gates-native-storage-pixels-loaders-andgameplay-exact310-scope','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
source=checked_text(previous.previous.source,{
    "'dk4-reviewed-maria301-release-v1'":"'dk4-reviewed-maria310-release-v1'",
    "len(styles['objects']) == 1":"len(styles['objects']) == 0",
    '        require(sha(target) == group[\'target_sha256\']':
        "        target,proof=amend_storage(arm,target,proof,group,inventory)\n        require(sha(target) == group['target_sha256']",
    'one_complete_NDS_object_commit_after_all_gates=True,':
        'one_complete_NDS_object_commit_after_all_gates=True,source_bound_FE_storage_alignment_preserves_all318_compiled_pages=True,',
})
env={**previous.env,'qualify_evidence':qualify_evidence,'amend_storage':amend_storage,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-source-current-transaction-guards-with-qualified-FE-storage-amendment','exec'),env)
plan_release=env['plan_release']
