"""Pure registered six-exchange SC0 integration with measured FU and scoped display proof."""
import inspect
from dk4tool.patch import reviewed_scene_batch_v1 as previous
from dk4tool.script.rafael_story_rebuild_with_fu_v1 import rebuild_block
from scripts.source_locked_derivation_v5118 import checked_text

require=previous.require
load=previous.load

def qualify_display(conf,doc,stored):
    native,visual,names,headers,reconstruction=[load(conf[k]) for k in ['compiled_native','visual_review','scoped_names','name_visual','reconstruction']]
    previous.validate_natural_dialogue_batch(names)
    require(len(names['records'])==11 and names['no_name_data_change'] and names['progressive_consumers_only'],'all eleven scoped unchanged progressive identities')
    require({r['actor_ID'] for r in names['records']}=={0,4,5,6,8,31,34,51,75,151,153},'exact scoped actors')
    require(native['runtime']==stored['runtime'] and stored['runtime']['captain']==0,'own Rafael source context')
    require(reconstruction['unchanged_complete_ARM9_COMMON_font_actor_bytes_andall_six_source_blocks'],'exact current dependencies for reused stored proof')
    require(reconstruction['old_stored_native_sha256']==previous.sha(previous.Path(conf['stored_native']).read_bytes()),'exact stored dependency receipt')
    require(native['all177_final_pages_directly_viewed'] and visual['pages']==177 and visual['all_final_pages_directly_viewed_or_exact_plane_reuse'],'all177 final pages viewed')
    require(stored['all_stored_planes_equal_directly_viewed_compiled_planes'],'every stored plane equals viewed plane')
    require(headers['all11_actors_observed'] and headers['complete_header_plane_comparisons']==40 and headers['all_complete_first_internal_final_name_glyphs_andblank_guards_exact'],'all scoped complete actual headers')
    require(headers['six_new_native_name_previews_directly_viewed'] and headers['four_original_native_name_previews_exact_reuse'],'all native names viewed or exact reuse')
    require(not any(r['source_selector']==254 for r in doc['records']),'no unqualified FE object')
    entries={r['id']:r for r in stored['records']};compiled={r['id']:r for r in native['records']}
    require(set(entries)==set(compiled)=={r['id'] for r in doc['records']},'complete stored/native membership')
    for row in doc['records']:
        entry,plane,ref=entries[row['id']],compiled[row['id']],row['planned_integrated_reference']
        require(ref['offset']==entry['new_offset'] and ref['record_index']==entry['new_record_index'] and ref['exact_stored_hex']==entry['stored_hex'],'individual exact target reference')
        require(plane['source_reference']==row['source_reference'] and plane['current_reference']==row['current_reference'] and plane['logical_English']==row['english'],'individual source/current/prose binding')
    lookup=load(conf['stored_lookup'])
    require(len(lookup['records'])==175 and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'all new stored bodies bypass former aliases unchanged')

def qualify_actual(conf,actual):
    pixels=load(conf['focused_pixels']);headers=load(conf['name_visual'])
    require(actual['total_frames']==10001 and actual['initialized_fixture_runs']==1,'bounded initialized coldboot')
    require(actual['all_three_QA_sheets_directly_viewed'] and actual['all_required_distinct_wrap_glyph_macro_pagination_cases_pass'],'all concrete cases andvisual review')
    require((actual['actual_utterances'],actual['actual_pages'],actual['offline_only_utterances'])==(16,18,159),'honest per-utterance gameplay scope')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']),'no broader activation orhardware claim')
    require(pixels['frames']==10001 and pixels['all_selected_pages_observed_in_exact_fixture_order'] and pixels['all_selected_complete_native_body_planes_andblank_guards_match'],'all selected source calls andcomplete pixels')
    require(len(pixels['body_pages'])==40 and len(headers['headers'])==40,'complete body/header comparisons')
    require({h['actor_ID'] for h in headers['headers']}==set(actual['observed_actor_IDs']),'actual scoped header membership')
    observed={(r['id'],r['page']) for r in pixels['body_pages']}
    required={('DK4_MES_B36_R0046',1),('DK4_MES_B37_R0099',1),('DK4_MES_B37_R0254',1),('DK4_MES_B37_R0254',2),
        ('DK4_MES_B37_R0267',1),('DK4_MES_B39_R0024',1),('DK4_MES_B41_R0131',1),('DK4_MES_B41_R0131',2)}
    require(required<=observed and pixels['two_page_boundaries_andFU_andtwo_ASCII_I_andfour_wrap_cases_covered'],'every concrete changed display risk observed')

source=checked_text(inspect.getsource(previous.plan_release),{
    "'dk4-reviewed-scene-release-v1'":"'dk4-rafael-B36-B41-release-v1'",
    "conf['record_count'] == 224":"conf['record_count'] == 175",
    'set(range(61, 71))':'set(range(36,42))',
    "native['complete_stored_pages'] == 229":"native['complete_stored_pages'] == 177",
    "native['fresh_relocated_native_relative_cases'] == 300":"native['fresh_relocated_native_relative_cases'] == 400",
    "    require(native['unchanged_directly_viewed_planes_reused_exactly'] == 227 and\n            native['changed_stored_planes_match_two_new_directly_viewed_pages'], 'visual review inheritance')":
        '    qualify_display(conf,approved,native)',
    "loaders['fresh_whole_archive_loads_andcache_hits'] == 325":"loaders['fresh_whole_archive_loads_andcache_hits'] == 343",
    "loaders['fresh_parent_cases'] == 20 and loaders['exact_reused_parent_cases'] == 630":
        "loaders['fresh_parent_cases'] == 12 and loaders['exact_reused_parent_cases'] == 674",
    "    require(actual['total_frames'] == 43003 and len(actual['runs']) == 3 and\n            len(actual['all15_contact_sheets_directly_viewed']) == 15 and\n            actual['both_changed_glyph_records_observed_with_normal_I_andcomplete_text'] and\n            actual['scene_ends_andfollowing_town_UI_visually_observed'], 'representative gameplay')\n    require(len(actual['five_two_page_utterances_observed']) == 5 and\n            actual['not_natural_optional_event_activation_ororiginal_location_chronology'] and\n            actual['no_world_state_equivalence_orhardware_full_route_claim'], 'pagination and honest coverage')":
        '    qualify_actual(conf,actual)',
    "'/data/SC1.DK4'":"'/data/SC0.DK4'",'len(clean_blocks) == 325':'len(clean_blocks) == 343',
    'all224_source_controls_and392_commands60_relatives_preserved=True,':'all175_source_controls_complete_commands_and80_relatives_preserved=True,',
    'native_pages=229, fresh_relative_cases=300, native_loads=325,':'native_pages=177, fresh_relative_cases=400, native_loads=343,',
    'parent_modes=dict(fresh=20, exact_reused=630), actual_frames=43003,':'parent_modes=dict(fresh=12, exact_reused=674), actual_frames=10001,',
})
env={**previous.plan_release.__globals__,'rebuild_block':rebuild_block,'qualify_display':qualify_display,'qualify_actual':qualify_actual}
exec(compile(source,__file__+'::same-complete-pure-SC0-inverse-with-measured-FU','exec'),env)
plan_release=env['plan_release']
