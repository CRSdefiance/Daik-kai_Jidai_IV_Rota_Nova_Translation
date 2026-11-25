"""Pure registered integration of539 reviewed Rafael speeches and unchanged control-only68."""
import inspect
from dk4tool.patch import rafael_B51_B60_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def require(value,message):
    if not value:raise ValueError('Rafael B61-B80 release: '+message)


def qualify_evidence(conf,doc,stored):
    load=previous.load
    native,visual,names,actual,np,cg,menu,lookup,loaders=[load(conf[k]) for k in
        ['compiled_native','visual_review','scoped_names','actual','focused_pixels','CG_pixels','typed_menu','stored_lookup','loaders']]
    previous.validate_natural_dialogue_batch(names)
    actors={0,3,4,5,6,8,10,11,31,34,39,40,48,80,83,104,106,113,139,147,151,179}
    require(len(names['records'])==22 and names['no_new_dialogue_credit'],'22 scoped identities without dialogue credit')
    require({r['actor_ID'] for r in names['records']}==actors,'exact scoped actors')
    require(not names['actual_scene_headers_unvisited'],'actual scoped headers verified')
    require(native['runtime']==stored['runtime'] and stored['runtime']['captain']==0,'own Rafael context')
    require(visual['all_final_pages_directly_viewed'] and visual['body_pages']==stored['complete_stored_pages']==545,'all native/stored/viewed pages')
    require(stored['fresh_relocated_native_relative_cases']==485 and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'],'branches andcomplete glyphs')
    observed={r['id']:r for r in stored['records']};compiled={r['id']:r for r in native['records']}
    require(set(observed)==set(compiled)=={r['id'] for r in doc['records']} and len(observed)==539,'individual speech membership')
    for row in doc['records']:
        entry,plane,ref=observed[row['id']],compiled[row['id']],row['planned_integrated_reference']
        require(ref['offset']==entry['new_offset'] and ref['record_index']==entry['new_record_index']
            and ref['exact_stored_hex']==entry['stored_hex'],'individual stored target reference')
        require(plane['source_reference']==row['source_reference'] and plane['current_reference']==row['current_reference']
            and plane['logical_English']==row['english'],'source/current/prose binding')
        if row['kind']=='system-FE':
            require(row['source_selector']==254 and plane['complete_native_English_display']['planned_native_row_comparison']['complete_glyph_row_membership_exact'],'complete FE glyph row membership')
    require(sum(r['kind']=='system-FE' for r in doc['records'])==6,'five Charlotte FE speeches andone funds notice')
    require(len(lookup['records'])==539 and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'no old catalogue body restoration')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,2,684)
        and loaders['prior_executed_parent_instructions_match_current_runtime'],'all archive andparent modes')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and not menu['menus'],'absence ofnative menus')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['qualifying_final_revision_frames'],actual['qualifying_final_revision_runs'],
        actual['actual_utterances'],actual['actual_body_pages'],actual['offline_only_utterances'])==(102005,5,39002,2,95,101,444),'honest actual versus offline scope')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']),'no unvisited route orhardware claim')
    require(actual['all17_final_sheets_directly_viewed_or_exact_sheet_pixel_reuse']
        and actual['all_six_FE_speeches_all_six_two_page_cases_andall22_headers_observed']
        and actual['complete_original_B69_66_speeches_92_commands_CG_actions_andreturn_observed'],'distinct behavior andcomplete CG scene')
    for result,counts in [(np,(29,35,74,72)),(cg,(66,66,142,132))]:
        require(result['all_selected_pages_observed_in_exact_fixture_order']
            and result['all_complete_native_body_andheader_planes_andblank_guards_match'],'ordered native calls andcomplete actual pixels')
        require((result['selected_utterances'],result['selected_pages'],len(result['body_pages']),len(result['headers']))==counts,'individual actual membership')
        require(all(r['complete_native_body_plane_andblank_guards_equal'] for r in result['body_pages'])
            and all(r['complete_name_glyphs_andblank_guards_exact'] for r in result['headers']),'all body/header plane guards')
    require({r['actor_ID'] for r in np['headers']}==actors,'all22 actual headers')
    ids={r['id'] for result in [np,cg] for r in result['body_pages']}
    pages={(r['id'],r['page']) for result in [np,cg] for r in result['body_pages']}
    require(len(ids)==95 and len(pages)==101 and ids<set(observed),'95 observed versus444 offline-only')
    require(cg['complete_scene_commands_retained'],'all original CG actions andreturn retained')


SOURCE=checked_text(inspect.getsource(previous.plan_release),{
    'dk4-rafael-B51-B60-release-v1':'dk4-rafael-B61-B80-release-v1',
    "conf['record_count'] == 249":"conf['record_count'] == 539",
    'len(speech) == 245 and len(choices) == 4':'len(speech) == 539 and len(choices) == 0',
    "len(layout['records']) == 245":"len(layout['records']) == 539",
    "    require(doc['blocks'] == conf['blocks'] == reconstruction['changed_blocks'] == list(range(51,61)), 'all ten complete scenes')":
        """    require(doc['blocks']==conf['reviewed_blocks']==reconstruction['reviewed_blocks']==list(range(61,81)),'all20 inventoried scenes')
    require(conf['blocks']==reconstruction['changed_blocks']==[n for n in range(61,81) if n!=68]
        and reconstruction['unchanged_control_only_blocks']==[68],'19 changed scenes andunchanged control-only68')""",
    "[g['block'] for g in reconstruction['groups']] == conf['blocks']":"[g['block'] for g in reconstruction['groups']] == conf['reviewed_blocks']",
    'native_pages=253,fresh_relative_cases=380,native_loads=343,typed_labels=4,actual_frames=18662':
        'native_pages=545,fresh_relative_cases=485,native_loads=343,typed_labels=0,actual_frames=102005',
})
env={**previous.plan_release.__globals__,'require':require,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-complete-scene-inverses-539-with-control-only68','exec'),env)
plan_release=env['plan_release']
