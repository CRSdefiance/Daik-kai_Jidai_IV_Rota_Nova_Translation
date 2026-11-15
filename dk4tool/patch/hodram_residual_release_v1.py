"""Register the394 residual SC1 reviews through the original complete-scene transaction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_b311_b324_release_v1 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.load;sha=previous.sha;require=previous.require

def qualify_evidence(conf,doc,stored):
    ready=load(conf['research_completion']);sealed=load(conf['sealed_inputs'])
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()),'sealed research identity')
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
        and (ready['records'],ready['revisions'],ready['retentions'])==(394,221,173),'394 sealed individual reviews')
    for path,digest in ready['evidence'].items():require(sha(Path(path).read_bytes())==digest,'research dependency: '+path)
    for key in ['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','scoped_names','compiled_native','typed_menu','native_styles','actual','visual_review']:
        require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())),'sealed input: '+key)
    original=load(ready['manuscript']);require(sha(Path(ready['manuscript']).read_bytes())==ready['manuscript_sha256'],'original five-gate manuscript')
    projection=deepcopy(original)
    for row in projection['records']:row['finding']=row['editorial_finding']
    projection.update(registered_schema_aliases_only=True,source_review=ready['manuscript'],source_review_sha256=ready['manuscript_sha256'])
    require(projection==doc,'exact finding alias projection; no editorial or gate changes')
    native,lookup,loaders,names,menu,styles,actual,visual=[load(conf[k]) for k in
        ['compiled_native','stored_lookup','loaders','scoped_names','typed_menu','native_styles','actual','visual_review']]
    require(native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime'],'same exact native runtime')
    require(names['all42_individual_five_gates_pass'] and len(names['records'])==conf['scoped_name_count']==42,'all42 names reviewed')
    validate_natural_dialogue_batch(names)
    require(native['pages']==stored['complete_stored_pages']==visual['final_native_pages']==conf['native_pages']==389,'all389 final pages')
    require(stored['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes())
        and lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()),'exact final storage bindings')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
        and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['fresh_relocated_native_relative_cases']==conf['relative_cases']==685,'complete stored display andbranch guards')
    require(lookup['all388_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'complete native effective bodies')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(325,2,648)
        and loaders['prior_executed_parent_instructions_match_current_runtime'] and loaders['incremental_fresh_blocks']==[29],'qualified incremental loaders')
    bodies=stored['records']+stored['style_records'];planes={r['id']:r for r in native['records']}
    require((len(stored['records']),len(stored['style_records']),len(bodies),len(planes))==(341,47,388,388),'complete ordinary/style membership')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==conf['FE_count']==16,'all16 FE consumers')
    require(len(styles['objects'])==7 and styles['native_target_slot_cases']==56 and styles['physical_alternatives']==47
        and styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives'])==63,'complete seven style contracts')
    require(len(menu['menus'])==3 and sum(len(r['record_IDs']) for r in menu['menus'])==conf['typed_choice_count']==6
        and menu['offline_visual_approved'] and not menu['direct_view_pending'],'all six captions')
    for obj in menu['menus']:
        path=Path(obj['original_receipt']);require(sha(path.read_bytes())==obj['original_receipt_sha256'],'native menu dependency')
        proof=load(path)
        require(proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            and proof['versions'][-1]['object_hex']==obj['target_object_hex'],'exact complete native menu provider andplanes')
    require(stored['typed_labels_checked']==6 and len(stored['typed_objects'])==3,'all stored menus')
    require({r['id'] for r in bodies}==planes.keys()=={r['id'] for r in lookup['records']},'complete body identity set')
    for body in bodies:
        row=planes[body['id']];display=row['complete_native_English_display']
        pages=[display] if row['kind']=='system-FE' else display['pages']
        for page in pages:require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'exact approved native plane')
    require((actual['frames'],actual['initialized_runs'],actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances'])
        ==(57363,3,169,170,219),'honest representative/offline coverage')
    require(actual['all_final_selected_body_planes_match_final_compiled_native_planes']
        and actual['all170_broad_pages_three_corrected_headers_andfinal_wrap_directly_viewed']
        and actual['all_three_native_menus_default_selection_andordinary_A_returns_observed']
        and actual['all_three_final_resupply_returns_directly_viewed']
        and actual['all_three_changed_progressive_names_observed_complete']
        and not any(actual[k] for k in ['natural_activation','earned_chronology','hardware']),'complete required observed display cases andreturns')
    require({(m['block'],m['source_command_offset'],tuple(m['observed_selected_options'])) for m in actual['menus']}
        =={(30,1100,(0,)),(33,414,(0,)),(37,216,(0,))},'three exact menu occurrences')
    for path,digest in actual['evidence'].items():require(sha(Path(path).read_bytes())==digest,'gameplay dependency: '+path)
    require(len(actual['reviewed_body_sheets'])==17,'complete direct-view contact coverage')
    for sheet in actual['reviewed_body_sheets']+[actual['menu_sheet']]:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'directly viewed sheet')
    require(visual['final_all389_pages_directly_viewed_or_exact_reused'] and visual['additional_final_native_page_directly_viewed']
        and visual['three_menus_six_captions_directly_viewed'] and visual['all42_scoped_planned_names_native_andvisually_checked'],'all offline visual cases')
    require(load(conf['opaque_pixel_model'])['all8_mutations_rejected'],'two source-bound complete ink/shadow models with negative cases')
    layout=load(conf['plan'])
    require(all(not r.get('qa_waivers') for r in doc['records']) and all(not any(i['severity'] in ['warning','error'] for i in r['base_QA']['issues']) for r in layout['records']),'original QA without waivers')
    dependency=previous.env['NdsImage'].open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes())==conf['final_dependency_ROM_sha256']
        and sha(dependency.read_file('/__arm9__.bin'))==native['runtime']['ARM9_sha256']==conf['final_runtime_ARM9_sha256']
        and sha(dependency.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'retained native code andfont dependency')
    capacity=load(conf['capacity_proof']);rebuilt=load(conf['reconstruction'])
    require(capacity['registered_ARM9_sha256']==native['runtime']['ARM9_sha256'] and capacity['safe_QA_block_limit']==9216
        and capacity['source_current_consumer_code_exact'] and max(g['target_bytes'] for g in rebuilt['groups'])<=9216,'native source-qualified allocation bound')
    for run in actual['runs']:
        terminal=load(run['terminal']);plan=load(terminal['run_plan']);fixture=load(plan['fixture'])
        require(sha(Path(plan['fixture']).read_bytes())==plan['fixture_sha256'],'exact observed fixture')
        require(fixture['QA_block_inside_original_stack_buffer'] and fixture['padded_QA_block_bytes']<=9216
            and fixture['source_bound_QA_host_exit_hex']=='00c200000000','bounded initialized host with correct cleanup')

source=checked_text(previous.source,{
    "'dk4-reviewed-hodram-b311-b324-release-v1'":"'dk4-reviewed-hodram-residual-release-v1'",
    "len(styles['objects']) == 38":"len(styles['objects']) == 7",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::unchanged-complete-SC1-source-transaction-394-review-scope','exec'),env)
plan_release=env['plan_release']
