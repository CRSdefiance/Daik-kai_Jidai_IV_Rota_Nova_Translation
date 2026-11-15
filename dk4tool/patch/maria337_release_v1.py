"""Pure337-record SC3 transaction using the unchanged whole-block reconstruction."""
from pathlib import Path
from dk4tool.patch import maria301_release_v2 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text

load,sha=previous.env['load'],previous.env['sha']
BLOCKS=list(range(125,137))


def require(value,message):
    if not value:raise ValueError('Maria337 release: '+message)


def qualify_evidence(conf,doc,stored):
    require(tuple(conf[k] for k in ['record_count','speech_count','ordinary_count','style_count','typed_choice_count','native_pages','relative_cases','FE_count'])
        ==(337,335,335,0,2,339,430,6),'exact source/native consumer scope')
    require(doc['blocks']==conf['reviewed_blocks']==conf['blocks']==BLOCKS,'12 complete source exchanges')
    require(conf['captain']==3 and conf['FE_owner_IDs']==[],'exact current route and no continuation owners')
    ready,sealed=map(load,[conf['research_completion'],conf['sealed_inputs']])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending'] and
        (ready['records'],ready['revisions'],ready['retentions'])==(337,224,113),'sealed whole-exchange decisions')
    require(ready['manuscript']==conf['manuscript'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'exact final review')
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()),'sealed research identity')
    for p,h in ready['evidence'].items():require(sha(Path(p).read_bytes())==h,'research dependency: '+p)
    keys=['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native','typed_menu','native_styles','actual','visual_review','scoped_names']
    for key in keys:require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())),'sealed input: '+key)
    native,lookup,loaders,menu,styles,actual,visual,names,rebuilt=[load(conf[k]) for k in
        ['compiled_native','stored_lookup','loaders','typed_menu','native_styles','actual','visual_review','scoped_names','reconstruction']]
    require(native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==names['runtime']==doc['runtime'],'same qualified runtime')
    require(native['runtime']['captain']==3 and native['runtime']['candidate_sha256']==conf['parent_ROM_sha256'] and
        native['runtime']['ARM9_sha256']==conf['pre_runtime_ARM9_sha256'],'exact current parent and renderer')
    require(native['pages']==stored['complete_stored_pages']==visual['body_pages']==339 and visual['all339_final_pages_directly_viewed'] and
        visual['all_names_andtwo_captions_directly_viewed'],'complete body/caption/name visual coverage')
    require(native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact'] and
        native['selected_alignment_cases']==1340,'complete native page/code/alignment guards')
    require(stored['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes()) and
        stored['native_sha256']==sha(Path(conf['compiled_native']).read_bytes()) and lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()),'exact final storage identities')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
        stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and
        (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(176,163,430),'complete stored/parity/branch guards')
    require(lookup['all335_physical_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'complete original catalogue lookup')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(303,606,0) and
        loaders['all_native_executed_instructions_current_ROM_exact'] and loaders['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact'],'whole SC3 loads and handoffs')
    require({r['id'] for r in native['records']}=={r['id'] for r in stored['records']}=={r['id'] for r in lookup['records']} and
        len(native['records'])==len(stored['records'])==335 and not stored['style_records'] and stored['typed_labels_checked']==2,'complete physical membership')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==6,'six original FE panels')
    require(not styles['objects'] and styles['physical_alternatives']==styles['native_target_slot_cases']==0 and
        not styles['compiler_negatives'] and styles['source_alias_equivalence_exact'] and styles['no_source_orcurrent_style_objects_in_this_scope'],'exact empty style scope')
    original_menu=load(menu['original_receipt'])
    require(sha(Path(menu['original_receipt']).read_bytes())==menu['original_receipt_sha256'] and
        menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus'])==conf['menu_count']==1,'exact complete native menu bridge')
    require(original_menu['runtime']==native['runtime'] and original_menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and
        (original_menu['native_provider_alignments'],original_menu['bridged_modal_returns'],original_menu['complete_English_caption_style_planes'])==(6,18,4) and
        len(set(original_menu['compiler_negatives_rejected']))==7,'all menu provider/target planes/selection/cancel/negative checks')
    require(original_menu['current_font_comparison_not_approved'] and original_menu['reviewed_target_has_four_complete_ASCII_caption_style_planes'] and
        [r['text'].strip() for r in original_menu['exact_corrupt_current_provider_checked_butnot_ASCII_painted']]==['産es','札ecline'],'exact corrupt baseline disclosed without font approval')
    require(menu['menus']==load(rebuilt['menu'])['menus'],'exact storage-qualified menu adapter')
    for row in native['records']:
        display=row['complete_native_English_display']
        for p in ([display] if row['kind']=='system-FE' else display['pages']):require(sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256'],'exact viewed native plane')
    require((actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages'],actual['offline_only_source_body_objects'],
        actual['actual_caption_strings'],actual['actual_menus'])==(33202,2,48,52,287,2,1),'honest representative/offline scope')
    require(actual['all52_selected_pages_two_captions_andboth_host_transitions_directly_viewed'] and
        actual['all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass'] and
        actual['all_four_two_page_tutorial_A_andfollowing_returns_observed'] and actual['all_six_FE_panels_andnamed_returns_observed'] and
        actual['both_mixed_font_Latin_I_repairs_observed'] and actual['complete_source_QA_hosts_return_to_resupply_andordinary_sailing'],'necessary actual display and transition proofs')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and
        actual['numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited'],'unvisited gameplay disclosed')
    for p,h in actual['evidence'].items():require(sha(Path(p).read_bytes())==h,'actual dependency: '+p)
    for s in actual['review_sheets']:require(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'],'directly viewed actual sheet')
    require((rebuilt['source_editorial_objects'],rebuilt['source_speeches'],rebuilt['speech_count'],rebuilt['total_rendered_speech_count'],rebuilt['compound_objects'])==(337,335,335,335,1),'source and native counts')
    require(rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['FE_inserted_commands']==rebuilt['FE_continuation_owners']==0,'complete original scopes and inverses without insertions')
    validate_natural_dialogue_batch(names)
    require(names['all21_individual_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==21,'all scoped name gates')
    require(max(g['target_bytes'] for g in rebuilt['groups'])<=9216 and not any(r.get('qa_waivers') for r in doc['records']),'native allocation bound and no QA waivers')
    require(load(conf['plan'])['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'exact reviewed source plan')
    parent=previous.env['NdsImage'].open(conf['parent_ROM'])
    require(sha(parent.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'unchanged current font')


source=checked_text(previous.previous.source,{
    "'dk4-reviewed-maria301-release-v1'":"'dk4-reviewed-maria337-release-v1'",
    "len(styles['objects']) == 1":"len(styles['objects']) == 0",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'require':require,'__file__':__file__}
exec(compile(source,__file__+'::same-pure-complete-source-current-block-archive-NDS-inverses','exec'),env)
plan_release=env['plan_release']
