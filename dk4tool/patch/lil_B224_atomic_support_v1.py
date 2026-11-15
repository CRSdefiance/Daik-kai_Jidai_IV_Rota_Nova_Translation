"""Immutable B224 approval, actual-display and scoped comparison obligations."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha

def audit_sealed_scope(doc,mapping,seal,load,require):
    for key,value in doc.items():
        if key.endswith('_sha256') and isinstance(doc.get(key[:-7]),str) and Path(doc[key[:-7]]).is_file():
            require(sha(Path(doc[key[:-7]]).read_bytes())==value,'manuscript bound file:'+key)
    approval=load(doc['native_approval'])
    require(approval['manuscript_sha256']==doc['native_approved_manuscript_sha256'] and approval['all15_five_gates_approved'],'native approval')
    for key,expected in dict(revision_count=10,retention_count=5,native_pages=15,logical_compiled_alignments=120,stored_alignments=60,zero_ink_parity_tails=9,name_alignments=20,layout_rejections=62,actual_objects=15,actual_native_pages=15,complete_body_holds=59,complete_name_holds=59,offline_only_objects=0).items():
        require(approval[key]==expected,'approval count:'+key)
    for key in ['actual15_objects15_pages59_body59_headers_explicit','retained_R11_ellipsis_source_palette_and_full_RGB_bound','all_observed_equality_scopes_no_broad_simulation_or_causal_claim','original_event224_no_explicit_dependencies_not_natural_activation_or_original_location','two_contextual_names_no_asset_or_duplicate_credit_Basra_metadata_not_surname']:
        require(seal[key] is True,'reference seal:'+key)
    require(doc['all207_name_alias_and_full_four_storyline_editorial_objective_open'] and doc['two_contextual_names_no_asset_or_duplicate_credit'] and doc['no_relationship_rank_occupation_religion_actual_magic_or_confirmed_shield_find_invented'],'full scope/meaning')
    controls=load(doc['relocated_control_proof']);a,b=controls['source_C200'],controls['relocated_C200']
    require(a['offset']==952 and b['offset']==1034 and a['source_command_hex']==b['source_command_hex']=='00c2' and a['native_result']==b['native_result']==[3,0,0,0,0,0],'C200 source-owned result')
    require(a['source_owned_UI_request_words']==b['source_owned_UI_request_words']==[1,2,13,0,0,0,1] and a['source_owned_UI_writes']==b['source_owned_UI_writes'] and b['all_other4MiB_actor_roster_event_RNG_and_models_exact'] and b['native_presentation_resource_bodies_not_executed'],'C200 exact owned request and resource limit')
    names=load(doc['speaker_name_review']);require({r['actor_ID']:r['english'] for r in names['records']}=={26:'Julian Lopes',197:'Safia'} and names['secondary_Basra_preserved_not_appended_as_surname'] and names['both_actual_English_names_complete'] and names['all207_names_roles_aliases_and_earlier_consumers_remain_open'],'contextual names without metadata surname')
    actual=load(doc['actual_English_proof']);later=load(doc['later_scope_proof'])
    require(actual['actual_unique_speeches']==15 and actual['actual_complete_body_holds']==actual['actual_complete_name_holds']==59 and actual['incomplete_sampled_body_holds']==0 and len(actual['command_pairs'])==27 and not actual['command_comparison_differences'] and actual['source_English_all_measured_command_results_UI_timing_RNG_equal'],'actual counts and command scope')
    require(len(actual['semantic_upper_portrait_pairs'])==15 and all(r['upper_scene_RGB_equal'] and r['portrait_RGB_equal'] for r in actual['semantic_upper_portrait_pairs']),'matched scene/portrait scope')
    require(len(actual['later_sampled_whole_frame_comparisons'])==159 and all(r['whole_RGB_equal'] for r in actual['later_sampled_whole_frame_comparisons']) and later['total_later_sampled_frames']==159 and not later['later_sampled_RGB_differences'],'159 sampled later frames only')
    require(actual['exit_frame']==actual['source_exit_frame']==6455 and actual['normal_port_sample_frame']==6550 and later['captain_IDs']==[2,2] and later['final_PRNG_seeds']==[3169181745,3169181745] and later['whole_actor_and_captain_equal'] and all(later['five_native_component_equality'].values()),'queried final scope')
    require(all(r['B120_end_frames']==[11256] for r in later['following_B120']) and actual['all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank'] and not actual['unreturned_following_dialogues_at_capture_end'],'following route-aware scope')
    require(actual['initialized_B22_not_natural_event224_original_location_earned_progress_full_effects_route_or_hardware'] and actual['no_roles_roster_funds_conditions_RNG_results_RAM_code_battery_or_savestate_forced'] and actual['no_full_RAM_every_intermediate_frame_future_sequence_broad_simulation_or_causal_claim'] and later['no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim'],'coverage limits')
    rows={r['id']:r for r in doc['records']};palette=load(doc['ellipsis_palette_proof']);ident='DK4_MES_B224_R0011';row=rows[ident]
    require(row['source_hex']==row['current_hex']==row['compiled_hex']==palette['complete_source_current_compiled_hex']=='1a8163' and row['english']=='{SPEAKER:1A}…','original exact CP932 ellipsis')
    require(palette['record_ID']==ident and palette['black_RGB']==[0,8,0] and palette['retained_CP932_shadow_RGB']==[197,198,197] and palette['other_English_ASCII_shadow_RGB']==[98,97,98] and palette['black_pixels']==palette['shadow_pixels']==6 and palette['source_and_English_native_planes_byte_exact'] and palette['sole_existing_ellipsis_palette_scope_not_global_Japanese_renderer_approval'] and palette['no_capture_glyph_font_metric_renderer_guard_or_source_byte_change'],'source-bound palette scope')
    require(actual['retained_R11_complete_original_CP932_ink_lighter_gray_and_whole_body_RGB_verified'] and actual['ASCII_dark_gray_masks_and_all_name_masks_unchanged'],'actual palette proof')
    source_cases=palette['source_actual_cases'];panels={p['id']:p for p in actual['actual_panels']};p=panels[ident]
    require([h['frame'] for h in p['complete_body_holds']]==[3370,3430,3490,3550] and len(source_cases)==4,'all four ellipsis holds')
    for h in source_cases:
        require(sha(Path(h['capture']).read_bytes())==h['capture_sha256'] and h['all6_black_and6_lighter_gray_pixels_exact'] and h['body_RGB_sha256']==palette['source_body_RGB_sha256'],'source ellipsis capture')
    for panel in actual['actual_panels']:
        expected=[197,198,197] if panel['id']==ident else [98,97,98]
        require(panel['body_shadow_RGB']==expected,'individual body palette')
        for hold in panel['complete_body_holds']:
            require(hold['body_shadow_RGB']==expected and hold['complete_independent_native_body_black_gray_all_glyphs_equal'],'all original grayscale masks')
            if panel['id']==ident:
                require(hold['retained_R11_full_body_RGB_equals_original'],'full source RGB comparison')
                # Original body viewport: actual pixels, not a recreated screenshot.
                with Image.open(hold['capture']) as im:
                    body=im.convert('RGB').crop((16,296,232,360))
                require(sha(body.tobytes())==palette['source_body_RGB_sha256'],'exact original body RGB hash')
                source=next(s for s in source_cases if s['frame']==hold['frame'])
                with Image.open(source['capture']) as si,Image.open(hold['capture']) as ei:
                    require(si.convert('RGB').crop((16,296,232,360)).tobytes()==body.tobytes()==ei.convert('RGB').crop((16,296,232,360)).tobytes(),'actual retained body RGB equality')
        value=bytes.fromhex(rows[panel['id']]['compiled_hex'])[1:]
        if panel['id']!=ident:require(all(c<128 for c in value),'no unreviewed CP932 glyph')
        else:require(value==bytes.fromhex('8163') and value.decode('cp932')=='…','sole original CP932 glyph')
    require(sum(bool(r['row_count_reason']) for r in rows.values())==5 and sum(bool(r['exact_reviewed_base_warnings']) for r in rows.values())==3,'five row reasons/three exact warnings')
    require(mapping['blocks'][0]['source_tail_bytes']==2 and mapping['blocks'][0]['target_tail_bytes']==0,'source tail2 and target no tail')
