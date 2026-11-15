"""Pure390-object transaction with the exact odd-length FE padding owner and full inverses."""
from pathlib import Path
from dk4tool.patch import maria337_release_v1 as previous
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block as original_rebuild
from dk4tool.script.reviewed_FE_storage_padding_v2 import replace_FE_text_parity_space_with_NUL
from scripts.source_locked_derivation_v5118 import checked_text

load,sha=previous.load,previous.sha
BLOCKS=list(range(152,176))


def require(value,message):
    if not value:raise ValueError('Maria390 release: '+message)


def rebuild_block(arm,clean,current,rows,plans,inventory,objects):
    target,proof=original_rebuild(arm,clean,current,rows,plans,inventory,objects)
    owned=[r for r in rows if r['id']=='DK4_MES_B164_R0099']
    if not owned:return target,proof
    require(len(owned)==1,'single FE owner')
    record=owned[0]
    receiptpath=Path('work/Maria_B152_B175_clean_20261109/reconstruction_v2/FE_storage_alignment.json')
    accepted=load(receiptpath);owner=accepted['owner']
    require(accepted['one_text_alignment_space_replaced_with_NUL'] and accepted['exact_changed_byte']==660,'qualified exact padding byte')
    require(all(record[k]==owner[k] for k in ['source_hex','current_hex','source_reference','current_reference','source_complete_preamble_hex']),'exact source/current FE owner')
    text=next(r for r in proof['text_records'] if r['id']==record['id'])
    require(text['compiled_hex']==owner['compiled_hex'] and text['parity_space_added'],'original compiled owner')
    command=next(c for c in proof['all_target_commands'] if c['offset']==text['new_offset']-5)
    require(command['whole_command_hex']==owner['stored_command_hex'] and command['offset']==owner['command_offset'],'fresh exact44-byte command')
    target,amended=replace_FE_text_parity_space_with_NUL(arm,target,owner,inventory)
    require(amended['full_block_inverse_exact'],'owned byte inverse')
    for row in proof['text_records']:
        if row['id']==record['id']:row.update(stored_hex=row['compiled_hex'],parity_space_added=False,owned_FE_storage_alignment=True)
        at=row['new_offset'];raw=bytes.fromhex(row['stored_hex'])
        require(target[at:at+len(raw)+1]==raw+b'\0','complete amended stored body')
        row['new_record_index']=target[:at].count(b'\0')
    proof.update(all_target_commands=amended['all_target_commands'],new_logical_end=amended['new_logical_end'],
        new_tail_hex=target[amended['new_logical_end']:].hex())
    return target,proof


def qualify_evidence(conf,doc,stored):
    require(tuple(conf[k] for k in ['record_count','speech_count','ordinary_count','style_count','typed_choice_count','native_pages','relative_cases','FE_count'])
        ==(390,373,373,0,17,373,610,32),'exact source/native scope')
    require(doc['blocks']==conf['reviewed_blocks']==conf['blocks']==BLOCKS and conf['captain']==3 and conf['FE_owner_IDs']==[],'24 complete exchanges/no new controls')
    ready,sealed=map(load,[conf['research_completion'],conf['sealed_inputs']])
    require(ready['all_individual_five_gates_pass'] and ready['registered_integration_pending'] and
        (ready['records'],ready['revisions'],ready['retentions'])==(390,154,236),'sealed decisions')
    require(ready['manuscript']==conf['manuscript'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'final review identity')
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()),'sealed research')
    for p,h in ready['evidence'].items():require(sha(Path(p).read_bytes())==h,'research dependency: '+p)
    keys=['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native','typed_menu','native_styles','actual','visual_review','scoped_names']
    for key in keys:require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())),'sealed '+key)
    native,lookup,loader,menu,styles,actual,visual,names,rebuilt=[load(conf[k]) for k in
        ['compiled_native','stored_lookup','loaders','typed_menu','native_styles','actual','visual_review','scoped_names','reconstruction']]
    require(all(v['runtime']==doc['runtime']==native['runtime'] for v in [stored,lookup,menu,styles,names]),'same native runtime')
    require(native['runtime']['captain']==3 and native['runtime']['candidate_sha256']==conf['parent_ROM_sha256'] and
        native['runtime']['ARM9_sha256']==conf['pre_runtime_ARM9_sha256'],'current parent/renderer')
    require(native['pages']==stored['complete_stored_pages']==visual['body_pages']==373 and visual['all373_final_pages_directly_viewed'] and
        visual['all_names_and17_captions_directly_viewed'],'all body/caption/name views')
    require(native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact'] and
        native['selected_alignment_cases']==1492,'complete glyph/alignment checks')
    require(stored['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes()) and stored['native_sha256']==sha(Path(conf['compiled_native']).read_bytes()) and
        lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()),'exact final stored identities')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and
        (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'],stored['total_qualified_native_relative_cases'],
        stored['exact_previous_stored_records_reused'],stored['fresh_changed_block_records'])==(7,366,0,610,359,14),'fresh changed block/exact compatible reuse')
    require(lookup['all373_physical_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'all effective bodies')
    require((loader['fresh_whole_archive_loads_andcache_hits'],loader['fresh_parent_cases'],loader['exact_reused_parent_cases'])==(303,606,0) and
        loader['all_native_executed_instructions_current_ROM_exact'] and loader['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact'],'complete current archive/cache/handoffs')
    require({r['id'] for r in native['records']}=={r['id'] for r in stored['records']}=={r['id'] for r in lookup['records']} and
        len(stored['records'])==373 and not stored['style_records'] and stored['typed_labels_checked']==17,'complete membership')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==32,'32 original FE panels')
    require(not styles['objects'] and styles['physical_alternatives']==styles['native_target_slot_cases']==0 and not styles['compiler_negatives'] and
        styles['source_alias_equivalence_exact'] and styles['no_source_orcurrent_style_objects_in_this_scope'],'exact empty style scope')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus'])==conf['menu_count']==8 and
        menu['menus']==load(rebuilt['menu'])['menus'],'eight exact storage-qualified menus')
    group=load(menu['original_receipt'])
    require(sha(Path(menu['original_receipt']).read_bytes())==menu['original_receipt_sha256'] and group['runtime']==native['runtime'],'original menu bridge')
    require((group['menus'],group['captions'],group['native_provider_alignments'],group['bridged_modal_returns'],group['current_andtarget_normal_highlight_planes'],
        group['target_normal_highlight_planes'],group['compiler_negatives'])==(8,17,48,150,68,34,57),'all provider/glyph/selection/cancel/rejection cases')
    for m in menu['menus']:
        require(sha(Path(m['proof']).read_bytes())==m['proof_sha256'],'menu dependency')
        proof=load(m['proof']);count=m['caption_count']
        require(proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and count in [2,3],'menu native guards')
        versions=proof.get('versions',proof.get('menus',[{}])[0].get('versions'))
        require(versions[-1]['object_hex']==m['target_object_hex'] and len(versions[-1]['cases'][0]['native_VM']['labels'])==count,'source indices/target object')
    for row in native['records']:
        display=row['complete_native_English_display']
        for page in ([display] if row['kind']=='system-FE' else display['pages']):require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'exact viewed plane')
    require((actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages'],actual['offline_only_source_body_objects'],
        actual['actual_caption_strings'],actual['actual_menus'])==(63284,4,83,83,290,5,2),'honest actual/offline scope')
    require(actual['all83_current_pages_five_captions_andfour_host_transitions_directly_viewed'] and actual['all_selected_current_pages_match_current_compiled_native_planes'] and
        actual['corrected_wine_question_andanswer_with_both16_frame_A_transitions_observed'] and actual['both_two_choice_options_all_three_indices_andordinary_A_returns_observed'] and
        actual['all17_town_forecasts_and27_FE_panels_observed'] and actual['Calicut_padding_repair_complete_single_row_andnormal_A_return_observed'] and
        actual['reclaimed_bargaining_aside_single_page_andfollowing_A_observed'] and actual['Wits_fullwidth50000_Namahage_andGlassmakingGuide_repairs_observed'] and
        actual['complete_source_QA_hosts_return_to_resupply_andordinary_sailing'],'required representative risks/returns')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and
        actual['numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited'],'unvisited scope disclosed')
    for p,h in actual['evidence'].items():require(sha(Path(p).read_bytes())==h,'actual dependency: '+p)
    for sheet in actual['review_sheets']:require(sheet['directly_viewed'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'actual direct view')
    require((rebuilt['source_editorial_objects'],rebuilt['source_speeches'],rebuilt['speech_count'],rebuilt['total_rendered_speech_count'],rebuilt['compound_objects'])==(390,373,373,373,8),'source/native counts')
    require(rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['composed_block_archive_andserialized_parent_inverses_exact'] and
        rebuilt['FE_inserted_commands']==rebuilt['FE_continuation_owners']==0,'complete inverses/no new FE controls')
    padding=load(conf['owned_FE_padding_qualification'])
    require(sha(Path(rebuilt['owned_FE_storage_amendment']).read_bytes())==rebuilt['owned_FE_storage_amendment_sha256'] and padding['one_text_alignment_space_replaced_with_NUL'] and
        padding['exact_changed_byte']==660 and padding['full_block_inverse_exact'] and len(padding['semantic_negatives_rejected'])==4,'exact qualified odd-length padding owner')
    validate_natural_dialogue_batch(names)
    require(names['all47_individual_five_gates_pass_in_scoped_context'] and len(names['records'])==conf['scoped_name_count']==47,'all scoped name gates')
    require(max(g['target_bytes'] for g in rebuilt['groups'])<=9216 and not any(r.get('qa_waivers') for r in doc['records']),'allocation/no waivers')
    require(load(conf['plan'])['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'final source plan')
    parent=previous.env['NdsImage'].open(conf['parent_ROM'])
    require(sha(parent.read_file('/GRP/KANJI.FNT'))==native['font_sha256'],'current font')


source=checked_text(previous.source,{"'dk4-reviewed-maria337-release-v1'":"'dk4-reviewed-maria390-release-v1'"})
env={**previous.env,'qualify_evidence':qualify_evidence,'rebuild_block':rebuild_block,'require':require,'__file__':__file__}
exec(compile(source,__file__+'::same-pure-whole-source-current-transaction-exact-owned-padding-byte','exec'),env)
plan_release=env['plan_release']
