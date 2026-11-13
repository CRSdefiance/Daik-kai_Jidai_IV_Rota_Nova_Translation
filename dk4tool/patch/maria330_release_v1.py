"""Pure SC3 mixed-consumer transaction, preserving both source-owned FE owners."""
from pathlib import Path
from dk4tool.patch import maria328_release_v1 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text

load,sha=previous.load,previous.sha
BLOCKS=[96,98,99,100,101,102,103,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124]

def require(value,message):
    if not value:raise ValueError('Maria330 release: '+message)

def qualify_evidence(conf,doc,reconstruction,stored):
    require(tuple(conf[k] for k in ['record_count','speech_count','ordinary_count','style_count','typed_choice_count','native_pages','relative_cases','FE_count'])
        ==(330,328,293,35,2,338,380,8),'exact source/native consumer scope')
    require(conf['captain']==3 and conf['FE_owner_IDs']==['DK4_MES_B116_R0041','DK4_MES_B116_R0051'],'exact current route and continuation owners')
    ready=load(conf['research_completion']);sealed=load(conf['sealed_inputs'])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending'] and
        (ready['records'],ready['revisions'],ready['retentions'])==(330,249,81),'sealed whole-exchange decisions')
    require(ready['manuscript']==conf['manuscript'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'exact final review')
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()),'sealed research identity')
    for p,h in ready['evidence'].items():require(sha(Path(p).read_bytes())==h,'research dependency: '+p)
    keys=['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native','typed_menu','native_styles','actual','visual_review','scoped_names']
    for key in keys:require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())),'sealed input: '+key)
    native,lookup,loaders,menu,styles,actual,visual,names=[load(conf[k]) for k in ['compiled_native','stored_lookup','loaders','typed_menu','native_styles','actual','visual_review','scoped_names']]
    require(native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==names['runtime']==doc['runtime'],'same qualified runtime')
    require(native['runtime']['captain']==3 and native['runtime']['candidate_sha256']==conf['parent_ROM_sha256'] and
        native['runtime']['ARM9_sha256']==conf['pre_runtime_ARM9_sha256'],'exact current parent and renderer')
    require(native['pages']==stored['complete_stored_pages']==visual['body_pages']==338 and visual['all338_final_pages_directly_viewed'] and
        visual['all_names_andtwo_captions_directly_viewed'],'complete body/caption/name visual coverage')
    require(native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact'] and
        native['selected_alignment_cases']==1320,'complete native page/code/alignment guards')
    require(stored['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes()) and
        stored['native_sha256']==sha(Path(conf['compiled_native']).read_bytes()) and lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()),'exact final storage identities')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
        stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and
        (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(156,182,380),'complete stored/parity/branch guards')
    require(lookup['all330_physical_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'complete original catalogue lookup')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(303,606,0) and
        loaders['all_native_executed_instructions_current_ROM_exact'] and loaders['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact'],'whole SC3 loads and handoffs')
    physical={r['id']:r for r in native['records']};entries=stored['records']+stored['style_records']
    require(set(physical)=={r['id'] for r in entries}=={r['id'] for r in lookup['records']} and
        (len(physical),len(stored['records']),len(stored['style_records']),stored['typed_labels_checked'])==(330,295,35,2),'complete physical membership')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==10,'eight source FE panels plus two continuations')
    require((len(styles['objects']),styles['physical_alternatives'],styles['native_target_slot_cases'])==(6,35,48) and styles['source_alias_equivalence_exact'] and
        sum(len(r['rejected']) for r in styles['compiler_negatives'])==54,'complete style slots and rejection cases')
    original_menu=load(menu['original_receipt'])
    require(sha(Path(menu['original_receipt']).read_bytes())==menu['original_receipt_sha256'] and
        menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus'])==1,'exact complete native menu bridge')
    require(original_menu['runtime']==native['runtime'] and original_menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and
        (original_menu['native_provider_alignments'],original_menu['bridged_modal_returns'],original_menu['complete_English_caption_style_planes'])==(6,18,8) and
        len(original_menu['compiler_negatives_rejected'])==len(set(original_menu['compiler_negatives_rejected']))==7,'all menu provider/planes/selection/cancel/negative checks')
    require(menu['menus']==load(reconstruction['menu'])['menus'],'exact storage-qualified menu adapter')
    for row in native['records']:
        display=row['complete_native_English_display'];pages=[display] if row['kind']=='system-FE' else display['pages']
        for page in pages:require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'exact viewed native plane')
    require((actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_native_body_candidates'],actual['distinct_body_pages'],
        actual['offline_only_source_body_objects'],actual['actual_caption_strings'],actual['actual_menus'])==(34402,2,53,55,58,275,2,1),'honest representative/offline scope')
    require(actual['all58_selected_pages_two_captions_andboth_host_transitions_directly_viewed'] and
        actual['all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass'] and
        actual['both_source_owned_FE_continuation_A_andfollowing_returns_observed'] and actual['no_extra_blank_FE_panel_observed'] and
        actual['complete_source_QA_hosts_return_to_resupply_andordinary_sailing'],'necessary actual display and transition proofs')
    require(actual['all_three_mixed_font_Latin_repairs_andformer_Japanese_grant_observed'] and actual['complete_dynamic_style_objects_observed']==5,'concrete glyph/dynamic-style behavior')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and
        actual['numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited'],'unvisited gameplay disclosed')
    for p,h in actual['evidence'].items():require(sha(Path(p).read_bytes())==h,'actual dependency: '+p)
    for sheet in actual['review_sheets']:require(sheet['directly_viewed'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'directly viewed actual sheet')
    require(reconstruction['source_editorial_objects']==330 and reconstruction['source_speeches']==293 and
        reconstruction['speech_count']==295 and reconstruction['total_rendered_speech_count']==330 and reconstruction['compound_objects']==7,'source and native counts')
    require(reconstruction['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and reconstruction['source_owned_exact_FE_controls_repeated_once_per_owner'] and
        reconstruction['FE_inserted_commands']==2 and len(reconstruction['per_owner_FE_pagination_rejections'])==2 and
        all(len(r['rejected'])==7 for r in reconstruction['per_owner_FE_pagination_rejections']),'complete original scopes and continuation inverses')
    validate_natural_dialogue_batch(names)
    require(names['all26_individual_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==26,'all scoped name gates')
    require(max(g['target_bytes'] for g in reconstruction['groups'])<=9216 and not any(r.get('qa_waivers') for r in doc['records']),'native allocation bound and no QA waivers')
    require(load(conf['plan'])['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'exact reviewed source plan')
    parent=previous.previous.NdsImage.open(conf['parent_ROM']); require(sha(parent.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'unchanged current font')

source=checked_text(previous.source,{
    "'dk4-reviewed-maria328-release-v1'":"'dk4-reviewed-maria330-release-v1'",
    "conf['record_count']==328":"conf['record_count']==330",
    'len(speech)==len(plans)==313 and len(choices)==15':'len(speech)==len(plans)==328 and len(choices)==2',
    "BLOCKS,'21 complete source exchanges'":"BLOCKS,'26 complete source exchanges'",
    "{'DK4_MES_B87_R0139'},'exact single qualified FE owner'":"{'DK4_MES_B116_R0041','DK4_MES_B116_R0051'},'exact two qualified FE owners'",
    'native_pages=321,native_commands=290,physical_body_candidates=314,style_slots=32,typed_labels=15':'native_pages=338,native_commands=295,physical_body_candidates=330,style_slots=48,typed_labels=2',
    'source_editorial_objects=328,fresh_relative_cases=315,native_loads=303,actual_frames=22001':'source_editorial_objects=330,fresh_relative_cases=380,native_loads=303,actual_frames=34402',
})
env={**previous.env,'BLOCKS':BLOCKS,'qualify_evidence':qualify_evidence,'require':require,'__file__':__file__}
exec(compile(source,__file__+'::same-pure-mixed-transaction-two-qualified-FE-owners','exec'),env)
plan_release=env['plan_release']
