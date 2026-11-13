"""Register the fully reviewed 557-object SC0 extension and its exact evidence."""
from pathlib import Path
from dk4tool.patch import reviewed_rafael_plain_scene_release_v1 as previous
from dk4tool.script.reviewed_scene_rebuild_with_fu_andcompounds_v1 import rebuild_block
from scripts.source_locked_derivation_v5118 import checked_text

load,require,sha=previous.previous.load,previous.previous.require,previous.previous.sha
NdsImage=previous.previous.NdsImage
validate=previous.previous.validate_natural_dialogue_batch

def qualify_evidence(conf,doc,stored):
    native,names,visual,actual,lookup,loaders,menu,styles,ready=[load(conf[k]) for k in [
        'compiled_native','scoped_names','visual_review','actual','stored_lookup','loaders','typed_menu','native_styles','research_completion']]
    for path,digest in ready['evidence'].items():
        require(sha(Path(path).read_bytes())==digest,'exact research evidence: '+path)
    require(ready['all_individual_five_gates_pass'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())
        and ready['plan_sha256']==sha(Path(conf['plan']).read_bytes()),'exact sealed five-gate manuscript and plan')
    require(stored['reconstruction_sha256']==loaders['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes())
        and stored['native_sha256']==sha(Path(conf['compiled_native']).read_bytes())
        and lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()),'exact current stored and loader inputs')
    require(native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime'] and native['runtime']['captain']==0,
        'own Rafael consumer context')
    validate(names)
    require(names['all20_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==20,
        'exact scoped public names')
    require(native['pages']==stored['complete_stored_pages']==conf['native_pages']==558 and visual['all558_body_pages_8_captions_20_public_names_approved']
        and visual['all193_final_observed_pages_andfour_menus_directly_viewed'],'complete native, stored and viewed body/menu/name pages')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
        and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['total_relocated_native_relative_cases']==conf['relative_cases']==1190,'complete native stored/branch guards')
    speech=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    rows,compiled=[{r['id']:r for r in d['records']} for d in (stored,native)]
    require(set(rows)==set(compiled)=={r['id'] for r in speech} and len(rows)==conf['speech_count']==549,'complete individual speech membership')
    for r in speech:
        s,p,ref=rows[r['id']],compiled[r['id']],r['planned_integrated_reference']
        require((ref['offset'],ref['record_index'],ref['exact_stored_hex'])==(s['new_offset'],s['new_record_index'],s['stored_hex']),
            'tested complete stored reference')
        require(all(p[k]==r[k] for k in ['source_reference','current_reference']) and p['logical_English']==r['english'],
            'exact source/current/prose binding')
        display=p['complete_native_English_display'];fe=r['kind']=='system-FE'
        if fe:require(r['source_selector']==254 and display['planned_native_row_comparison']['complete_glyph_row_membership_exact'],'complete FE row placement')
        for page in ([display] if fe else display['pages']):
            require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'complete viewed native plane')
    require(sum(r['kind']=='system-FE' for r in speech)==conf['FE_count']==6,'complete FE membership')
    require(len(lookup['records'])==549 and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'all native catalogue bodies')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,2,684)
        and loaders['prior_executed_parent_instructions_match_current_runtime'],'complete archive loads and exact current handoff modes')
    require(stored['typed_labels_checked']==conf['typed_choice_count']==8 and len(stored['typed_objects'])==len(menu['menus'])==conf['menu_count']==4
        and not stored['style_records'] and not styles['objects'] and menu['offline_visual_approved'] and not menu['direct_view_pending'],
        'all four stored choice objects and no personality objects')
    for obj in menu['menus']:
        path=Path(obj['native_proof']);proof=load(path)
        require(sha(path.read_bytes())==obj['native_proof_sha256'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            and proof['source_index_andcount_preserved'] and len(proof['compiler_negatives_rejected'])==7,'complete caption proof, indices and negatives')
        require((proof['native_provider_alignments'],proof['bridged_modal_returns'],proof['complete_English_caption_style_planes'])==(6,18,8),
            'native menu alignments, styles and returns')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['source_speech_variants_observed'],actual['native_body_pages_observed'],
        actual['actual_choice_labels'],actual['offline_only_speech_variants'])==tuple(conf[k] for k in
        ['actual_frames','actual_runs','actual_speeches','actual_body_pages','typed_choice_count','offline_speeches']),'honest actual/offline scope')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        and actual['other_cursor_states_VM_returns_branches_andcancellation_offline_only']
        and actual['all_four_menus_default_cursor_andfollowing_fixture_speech_observed'],'bounded emulator coverage')
    observed={r['id'] for r in actual['exact_observed_pages']}
    require(sorted(observed)==actual['source_IDs_observed'] and set(actual['offline_only_source_IDs'])==set(rows)-observed
        and len({(r['id'],r['page']) for r in actual['exact_observed_pages']})==193,'exact per-record observed coverage')
    require({(m['block'],m['offset']) for m in actual['menus']}=={(m['block'],m['offset']) for m in stored['typed_objects']},
        'all observed menus bound to final stored commands')
    renderer=NdsImage.open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes())==conf['final_dependency_ROM_sha256']
        and sha(renderer.read_file('/__arm9__.bin'))==native['runtime']['ARM9_sha256']==conf['final_runtime_ARM9_sha256']
        and sha(renderer.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'unchanged verified runtime and font')

source=checked_text(previous.source,{
    "'dk4-reviewed-rafael-plain-scene-release-v1'":"'dk4-reviewed-rafael-compound-fu-scene-release-v1'",
    "        rows = [r for r in speech if r['block'] == number]":"""        rows = [deepcopy(r) for r in speech if r['block'] == number]
        for row in rows:
            index=row['current_reference']['record_index']
            require(row.get('current_record_index',index)==index,'exact current record index')
            row['current_record_index']=index""",
    "fresh_relative_cases=conf['relative_cases']":"qualified_relative_cases=conf['relative_cases']",
})
env={**previous.plan_release.__globals__,'qualify_evidence':qualify_evidence,'rebuild_block':rebuild_block}
exec(compile(source,__file__+'::same-complete-source-bound-transaction-with-qualified-FU','exec'),env)
plan_release=env['plan_release']
