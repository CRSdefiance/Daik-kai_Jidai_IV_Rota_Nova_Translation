"""Qualify the complete reviewed SC1 transaction over registered Rafael5186."""
from pathlib import Path
from dk4tool.patch import rafael_story_b321_b342_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.env['load'];sha=previous.env['sha'];require=previous.env['require']

def qualify_evidence(conf,doc,stored):
    ready=load(conf['research_completion'])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
        and (ready['records'],ready['revisions'],ready['retentions'])==(277,170,107),'all sealed individual editorial gates')
    for path,checksum in ready['evidence'].items():
        require(sha(Path(path).read_bytes())==checksum,'sealed research dependency: '+path)
    for key in ('manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','scoped_names'):
        require(ready['evidence'].get(conf[key])==sha(Path(conf[key]).read_bytes()),'exact qualified input: '+key)
    native,lookup,loaders,visual,actual,names,menu,styles=[load(conf[k]) for k in
        ('compiled_native','stored_lookup','loaders','visual_review','actual','scoped_names','typed_menu','native_styles')]
    require(native['runtime']==stored['runtime']==lookup['runtime']==names['runtime']==menu['runtime']==styles['runtime'],'same registered runtime')
    require(names['all_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==23,'all scoped name decisions')
    previous.env['validate_natural_dialogue_batch'](names)
    require(native['pages']==visual['body_pages']==stored['complete_stored_pages']==conf['native_pages']==284,'all final pages')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
        and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        and stored['fresh_relocated_native_relative_cases']==conf['relative_cases']==150,'all stored glyphs and relocated branch cases')
    require(lookup['all270_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'all stored catalogue bodies')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(325,38,612)
        and loaders['prior_executed_parent_instructions_match_current_runtime'],'whole archive and exact loader modes')
    bodies=stored['records']+stored['style_records'];planes={r['id']:r for r in native['records']}
    require((len(stored['records']),len(stored['style_records']),len(bodies))==(241,29,conf['speech_count'])
        and len(planes)==270,'exact ordinary and voice bodies')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==conf['FE_count']==4,'all four distinct FE panels')
    require(len(styles['objects'])==4 and styles['native_target_slot_cases']==32 and styles['physical_alternatives']==29
        and styles['source_alias_equivalence_exact'] and sum(len(r['rejected']) for r in styles['compiler_negatives'])==36,'complete native personality contracts')
    require(len(menu['menus'])==3 and sum(len(r['record_IDs']) for r in menu['menus'])==conf['typed_choice_count']==7
        and menu['offline_visual_approved'] and not menu['direct_view_pending'],'all typed caption contracts')
    for item in menu['menus']:
        proofpath=Path(item['original_receipt']);require(sha(proofpath.read_bytes())==item['original_receipt_sha256'],'native menu proof')
        proof=load(proofpath)
        require(proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'],'complete native menu consumer')
        versions=proof['versions'] if len(item['record_IDs'])==2 else next(m['versions'] for m in proof['menus']
            if (m['block'],m['source_command_offset'],m['record_IDs'])==(item['block'],item['source_command_offset'],item['record_IDs']))
        require(versions[-1]['object_hex']==item['target_object_hex'],'exact menu target')
    require(stored['typed_labels_checked']==7 and len(stored['typed_objects'])==3,'all stored menu identities')
    require({r['id'] for r in bodies}==planes.keys()=={r['id'] for r in lookup['records']},'complete body membership')
    for row in bodies:
        plane=planes[row['id']]
        pages=[plane['complete_native_English_display']] if plane['kind']=='system-FE' else plane['complete_native_English_display']['pages']
        for page in pages:require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'complete reviewed pixel plane')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['source_speech_variants_observed'],actual['native_body_pages_observed'],actual['offline_only_speech_variants'])
        ==(23441,1,65,74,205),'honest observed/offline scope')
    require(actual['all_four_FE_panels_FI_expansion_four_voice_objects_andrepresentative_pagination_observed']
        and not any(actual[k] for k in ('natural_activation','original_location','earned_chronology','full_route','hardware')),'representative initialized gameplay only')
    require({(m['block'],m['source_command_offset'],tuple(m['options'])) for m in actual['source_menu_occurrences_complete_pixel_approved']}
        =={(216,64,(0,)),(216,230,(0,))},'two distinct source-bound menu behaviors')
    require(not actual['repeated_B224_yes_no_menu']['complete_occurrence_highlight_background_credit']
        and actual['repeated_B224_yes_no_menu']['stored_source_bytes_andnative_providers_exact'],'no duplicate-pixel occurrence overclaim')
    require(visual['all_body_caption_andname_planes_approved'] and visual['all_actual_generated_pages_andrepresentative_menus_directly_viewed']
        and visual['actual_sheets_directly_viewed']==14,'complete required visual review')
    for p in visual['reviewed_actual_sheets']:require(sha(Path(p['path']).read_bytes())==p['sha256'],'exact viewed actual sheet')
    # One grammatical soft-wrap preference is explicitly approved; no safety rule is waived.
    layout=load(conf['plan']);approved={r['id']:r for r in doc['records']}
    exceptions=[r for r in layout['records'] if 'unmodified_base_QA' in r]
    require(len(exceptions)==1 and exceptions[0]['id']=='DK4_MES_B229_R0036','exact heuristic retention scope')
    record=approved[exceptions[0]['id']];retention=visual['exact_QA_line_ending_retention']['QA_line_ending_retention']
    require(record['qa_waivers']==['weak-line-ending'] and record['qa_waiver_reason']==retention['reason']
        and record['exact_QA_line_ending_retention']==retention,'documented record-local QA retention')
    require(exceptions[0]['base_QA']['visible_lines'][0]==retention['exact_line']=='The Huns were nomadic horsemen of'
        and retention['line_index']==0,'exact approved ordinary word boundary')
    require([i['code'] for i in exceptions[0]['unmodified_base_QA']['issues'] if i['severity']=='warning']==['weak-line-ending'],'original diagnostic preserved')
    require(all(not r.get('qa_waivers') for r in doc['records'] if r['id']!=record['id']),'no other unqualified heuristic exceptions')
    renderer=previous.env['NdsImage'].open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes())==conf['final_dependency_ROM_sha256']
        and sha(renderer.read_file('/__arm9__.bin'))==native['runtime']['ARM9_sha256']==conf['final_runtime_ARM9_sha256']
        and sha(renderer.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'exact registered renderer and font')

source=checked_text(previous.source,{
    "'dk4-reviewed-rafael-compound-fu-scene-release-v1'":"'dk4-reviewed-hodram-b211-b230-release-v1'",
    "len(styles['objects']) == 48":"len(styles['objects']) == 4",
    "path == '/data/SC0.DK4'":"path == '/data/SC1.DK4'",
    "len(clean_blocks) == 343":"len(clean_blocks) == 325",
    'native_loads=343':'native_loads=325',
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-source-current-archive-transaction-SC1-scope','exec'),env)
plan_release=env['plan_release']
