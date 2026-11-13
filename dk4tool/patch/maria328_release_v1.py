"""Pure328-object mixed SC3 transaction with one source-owned FE continuation."""
import inspect
from pathlib import Path
from dk4tool.patch import rafael_story_b81_b84_release_v1 as previous
from dk4tool.patch import maria301_release_v2 as mixed
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text

load,sha=previous.load,previous.sha
BLOCKS=[73,74,75,76,77,78,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]

def require(value,message):
    if not value:raise ValueError('Maria328 release: '+message)

def qualify_evidence(conf,doc,reconstruction,stored):
    require((conf['record_count'],conf['speech_count'],conf['ordinary_count'],conf['style_count'],conf['typed_choice_count'],conf['native_pages'],conf['relative_cases'],conf['FE_count'])
        ==(328,313,289,24,15,321,315,27),'exact source/native consumer scope')
    require(conf['captain']==3 and conf['FE_owner_ID']=='DK4_MES_B87_R0139','exact current route and continuation owner')
    ready=load(conf['research_completion']);sealed=load(conf['sealed_inputs'])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending'] and
        (ready['records'],ready['revisions'],ready['retentions'])==(328,143,185),'sealed whole-exchange decisions')
    require(ready['manuscript']==conf['manuscript'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'exact final review')
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()),'sealed research identity')
    for p,h in ready['evidence'].items():require(sha(Path(p).read_bytes())==h,'research dependency: '+p)
    keys=['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native','typed_menu','native_styles','actual','visual_review','scoped_names']
    for key in keys:require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())),'sealed input: '+key)
    native,lookup,loaders,menu,styles,actual,visual,names=[load(conf[k]) for k in ['compiled_native','stored_lookup','loaders','typed_menu','native_styles','actual','visual_review','scoped_names']]
    require(native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==names['runtime']==doc['runtime'],'same qualified runtime')
    require(native['runtime']['captain']==3 and native['runtime']['candidate_sha256']==conf['parent_ROM_sha256'] and
        native['runtime']['ARM9_sha256']==conf['pre_runtime_ARM9_sha256'],'exact current parent and renderer')
    require(native['pages']==stored['complete_stored_pages']==visual['body_pages']==321 and visual['all321_final_pages_directly_viewed'] and
        visual['all_names_and15_captions_directly_viewed'],'complete body/caption/name visual coverage')
    require(native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact'] and
        native['selected_alignment_cases']==1256,'complete native page/code/alignment guards')
    require(stored['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes()) and
        stored['native_sha256']==sha(Path(conf['compiled_native']).read_bytes()) and lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()),'exact final storage identities')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
        stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and
        (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(148,173,315),'complete stored/parity/branch guards')
    require(lookup['all314_physical_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'complete original catalogue lookup')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(303,606,0) and
        loaders['all_native_executed_instructions_current_ROM_exact'] and loaders['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact'],'whole SC3 loads and handoffs')
    physical={r['id']:r for r in native['records']};entries=stored['records']+stored['style_records']
    require(set(physical)=={r['id'] for r in entries}=={r['id'] for r in lookup['records']} and
        (len(physical),len(stored['records']),len(stored['style_records']),stored['typed_labels_checked'])==(314,290,24,15),'complete physical membership')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==28,'27 source FE panels plus one continuation')
    require((len(styles['objects']),styles['physical_alternatives'],styles['native_target_slot_cases'])==(4,24,32) and styles['source_alias_equivalence_exact'] and
        sum(len(r['rejected']) for r in styles['compiler_negatives'])==36,'complete style slots and rejection cases')
    original_menu=load(menu['original_receipt'])
    require(sha(Path(menu['original_receipt']).read_bytes())==menu['original_receipt_sha256'] and menu['menus']==original_menu['menus'] and
        menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus'])==5,'exact complete native menu bridge')
    require(original_menu['runtime']==native['runtime'] and original_menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and
        (original_menu['native_provider_alignments'],original_menu['bridged_modal_returns'],original_menu['complete_English_caption_style_planes'])==(30,120,60) and
        sum(len(r['rejected']) for r in original_menu['compiler_negatives_rejected'])==40,'all menu provider/planes/selection/cancel/negative checks')
    for row in native['records']:
        display=row['complete_native_English_display'];pages=[display] if row['kind']=='system-FE' else display['pages']
        for page in pages:require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'exact viewed native plane')
    require((actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_native_body_candidates'],actual['distinct_body_pages'],
        actual['offline_only_source_body_objects'],actual['actual_caption_strings'],actual['actual_menus'])==(22001,1,43,44,48,270,6,2),'honest representative/offline scope')
    require(actual['all48_selected_pages_six_captions_andhost_transitions_directly_viewed'] and
        actual['all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass'] and
        actual['source_owned_FE_continuation_A_then_menu_then_named_return_observed'] and actual['no_extra_blank_FE_panel_observed'] and
        actual['repaired_bean_FE_rows_andfour_progressive_two_page_layouts_observed'] and
        actual['complete_source_QA_host_returns_to_resupply_andordinary_sailing'],'necessary actual display and transition proofs')
    require(actual['corrected_corrupt_style_observed']=='SC3_B95_STYLE_400_42' and actual['complete_dynamic_style_objects_observed']==3,'concrete glyph/dynamic-style behavior')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and
        actual['other_selections_cancellation_andoriginal_branch_outcomes_unvisited'],'unvisited gameplay disclosed')
    for p,h in actual['evidence'].items():require(sha(Path(p).read_bytes())==h,'actual dependency: '+p)
    for sheet in actual['review_sheets']:require(sheet['directly_viewed'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'directly viewed actual sheet')
    require(reconstruction['source_editorial_objects']==328 and reconstruction['source_speeches']==289 and
        reconstruction['speech_count']==290 and reconstruction['total_rendered_speech_count']==314 and reconstruction['compound_objects']==9,'source and native counts')
    require(reconstruction['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and reconstruction['source_owned_exact_FE_control_repeated_once'] and
        len(reconstruction['seven_FE_pagination_invalid_cases_rejected'])==7,'complete original scopes and continuation inverse')
    validate_natural_dialogue_batch(names)
    require(names['all24_individual_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==24,'all scoped name gates')
    require(max(g['target_bytes'] for g in reconstruction['groups'])<=9216 and not any(r.get('qa_waivers') for r in doc['records']),'native allocation bound and no QA waivers')
    layout=load(conf['plan']);require(layout['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'exact reviewed source plan')
    parent=previous.NdsImage.open(conf['parent_ROM']);require(sha(parent.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'unchanged current font')

source=checked_text(inspect.getsource(previous.plan_release),{
    "'dk4-rafael-B81-B84-release-v1'":"'dk4-reviewed-maria328-release-v1'",
    "doc,layout,reconstruction,stored,menu=[load(conf[k]) for k in ['manuscript','plan','reconstruction','stored_native','typed_menu']]":
        "doc,layout,reconstruction,stored,menu,styles=[load(conf[k]) for k in ['manuscript','plan','reconstruction','stored_native','typed_menu','native_styles']]",
    "len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==330":"len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==328",
    'len(speech)==len(plans)==325 and len(choices)==5':'len(speech)==len(plans)==313 and len(choices)==15',
    "[81,82,83,84],'four complete source exchanges'":"BLOCKS,'21 complete source exchanges'",
    "path=='/data/SC0.DK4'":"path=='/data/SC3.DK4'",'len(container.blocks)==len(original)==343':'len(container.blocks)==len(original)==303',
    "initial=group['first_page_reconstruction'];objects=compound_objects({**initial,'block':number},approved,plans,menu,{'objects':[]})":
        "initial=group.get('first_page_reconstruction',group);objects=compound_objects({**initial,'block':number},approved,plans,menu,styles)",
    "rows=[r for r in speech if r['block']==number]":
        "rows=[previous.deepcopy(r) for r in speech if r['block']==number and r.get('native_object_kind')!='4100-style-alternative']\n        for row in rows:row['current_record_index']=row['current_reference']['record_index']",
    "require(proof==initial,'complete original command order/scopes/relative maps andinverse')":
        "require(all(value==initial[key] for key,value in proof.items()) and ('first_page_reconstruction' not in group or proof==initial),'complete original command order/scopes/relative maps andinverse')",
    "if group['FE_pagination'] is not None:":"if group.get('FE_pagination') is not None:",
    "{'DK4_MES_B84_R0470','DK4_MES_B84_R0539'},'onlytwo qualified FE owners'":"{'DK4_MES_B87_R0139'},'exact single qualified FE owner'",
    'native_pages=336,native_commands=327,typed_labels=5':'native_pages=321,native_commands=290,physical_body_candidates=314,style_slots=32,typed_labels=15',
    'source_editorial_objects=330,fresh_relative_cases=140,native_loads=343,actual_frames=72406':'source_editorial_objects=328,fresh_relative_cases=315,native_loads=303,actual_frames=22001',
})
env={**previous.plan_release.__globals__,'previous':previous,'BLOCKS':BLOCKS,'compound_objects':mixed.compound_env['compound_objects'],
    'qualify_evidence':qualify_evidence,'require':require,'__file__':__file__}
exec(compile(source,__file__+'::same-pure-mixed-source-transaction-with-one-exact-FE-owner','exec'),env)
plan_release=env['plan_release']
