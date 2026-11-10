"""Qualify the complete residual speech-only transaction over Rafael4903."""
from pathlib import Path
from dk4tool.patch import rafael_story_b321_b342_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.env['load']; sha=previous.env['sha']; require=previous.env['require']


def qualify_evidence(conf,doc,stored):
    ready=load(conf['research_completion'])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
        and (ready['records'],ready['revisions'],ready['retentions'])==(283,162,121),'all sealed individual editorial gates')
    for path,checksum in ready['evidence'].items():
        require(sha(Path(path).read_bytes())==checksum,'sealed research dependency: '+path)
    for key in ('manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','visual_review','actual','scoped_names'):
        require(ready['evidence'].get(conf[key])==sha(Path(conf[key]).read_bytes()),'exact qualified input: '+key)
    native,lookup,loaders,visual,actual,names,menu,styles=[load(conf[k]) for k in
        ('compiled_native','stored_lookup','loaders','visual_review','actual','scoped_names','typed_menu','native_styles')]
    require(native['runtime']==stored['runtime']==lookup['runtime']==names['runtime']==menu['runtime']==styles['runtime'],'same registered runtime')
    require(names['all_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==39,'all scoped names')
    require(native['pages']==visual['body_pages']==stored['complete_stored_pages']==conf['native_pages']==284,'all final pages')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
        and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['fresh_relocated_native_relative_cases']==conf['relative_cases']==675,'all stored glyphs and relocated branch cases')
    require(lookup['all283_ordinary_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'all stored catalogue bodies')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,70,616)
        and loaders['prior_executed_parent_instructions_match_current_runtime'],'whole archive and exact loader modes')
    require(len(stored['records'])==len(native['records'])==len(lookup['records'])==conf['speech_count']==283,'complete speech membership')
    require(conf['style_count']==conf['menu_count']==conf['typed_choice_count']==conf['FE_count']==0
        and not styles['objects'] and not menu['menus'],'source-proven absence of compound and FE objects')
    stored_rows={r['id']:r for r in stored['records']}; planes={r['id']:r for r in native['records']}
    require(stored_rows.keys()==planes.keys()=={r['id'] for r in doc['records']},'exact body identities')
    for row in doc['records']:
        saved=stored_rows[row['id']]; plane=planes[row['id']]; ref=row['planned_integrated_reference']
        require((saved['new_offset'],saved['new_record_index'],saved['stored_hex'])==(ref['offset'],ref['record_index'],ref['exact_stored_hex']),'exact stored reference')
        require(all(row[k]==plane[k] for k in ('source_reference','current_reference')),'exact native source/current binding')
        for page in plane['complete_native_English_display']['pages']:
            require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'reviewed complete pixel plane')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['source_speech_variants_observed'],
        actual['native_body_pages_observed'],actual['offline_only_speech_variants'])==(28001,1,95,96,188),'honest observed/offline scope')
    require(actual['all39_progressive_name_headers_observed'] and not actual['menus']
        and actual['all_changed_full_catalogue_UIs_unvisited']
        and not any(actual[k] for k in ('natural_activation','original_location','earned_chronology','full_route','hardware')),'initialized display coverage only')
    require(visual['all_body_caption_andname_planes_approved'] and visual['all_actual_pages_and_menus_directly_viewed'],'complete visual review')
    renderer=previous.env['NdsImage'].open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes())==conf['final_dependency_ROM_sha256']
        and sha(renderer.read_file('/__arm9__.bin'))==native['runtime']['ARM9_sha256']==conf['final_runtime_ARM9_sha256']
        and sha(renderer.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'exact renderer and font dependencies')


source=checked_text(previous.source,{"len(styles['objects']) == 48":"len(styles['objects']) == 0"})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-archive-transaction','exec'),env)
plan_release=env['plan_release']
