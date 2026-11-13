"""Seal the two source-bound revisions after current native,actual menu and growth checks."""
from pathlib import Path
from copy import deepcopy
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_approval_v6106')
OLD=Path('translations/shachihoko_item116_editorial_manuscript_v1.json')
DOC=Path('translations/shachihoko_item116_editorial_manuscript_v2.json')
NATIVE=Path('work/analysis/shachihoko_native_v6098/all218_live_descriptions_and218_item_names_rebound_to_actual_target.json')
BOOT=Path('work/analysis/shachihoko_boot_v6099/source_bound_growth_boot_input_and_native_allocation_verification.json')
FONTS=Path('work/analysis/shachihoko_detail_fonts_v6101/both_detail_consumers_three_items_two_modes_complete_native_planes.json')
ACTUAL=Path('work/analysis/shachihoko_actual_menu_v6105/actual_menu_two_holds_eight_complete_native_text_fields_and_return.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,native,boot,fonts,actual=map(read,[OLD,NATIVE,BOOT,FONTS,ACTUAL]);receipt=read('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json')
    assert native['all217_other_compiled_paragraphs_pointers_and_all218_previous_target_name_outputs_exact'] and native['all_actual123264_deployed_payload_bytes_and_executed_target_instructions_exact']
    assert boot['all31_actual_same_input_whole_RGB_frames_equal_V6050'] and len(boot['all_six_postinit_whole_actor_and_captain_model_comparisons'])==6 and boot['complete_actual123264_payload_native_copy_reservation_and_cacheline_extents_verified']
    assert fonts['all24_native_field_word_glyph_pixel_bounds_and_parent_crop_cases_pass'] and fonts['all16_unselected_neighbor_item_planes_exact']
    assert actual['all_changed_title_and134_character_description_exact_native_independent_glyphs_and_original_parent_positions'] and len(actual['eight_complete_actual_title_description_field_matches'])==8
    sheets=[]
    for proof in [boot,fonts,actual]:
        path=Path(proof['sheet']);assert sha(path.read_bytes())==proof['sheet_sha256'];sheets.append(dict(path=str(path),sha256=proof['sheet_sha256'],viewed=True))
    new=deepcopy(old);new.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all_English_words_authored_before_storage_choice=True,native_formatting_and_combined_release_pending=False,
        all_five_per_record_gates_complete_registered_release_pending=True,native_reference_ROM=receipt['research_ROM'],native_reference_ROM_sha256=receipt['research_ROM_sha256'],
        native_data_plan=receipt['data_plan'],target_ARM9='work/analysis/shachihoko_item116_research_v6094/target_ARM9.bin',target_COMMON='work/analysis/shachihoko_item116_research_v6094/target_COMMON.bin',
        source_current_ROM_and_all_wider_editorial_history_preserved=True,source_bound_actual_growth_checks_complete=True,
        actual_menu_with_ordinary_inputs_and_source_A000_inside_disclosed_B22_fixture=True,
        no_natural_event204_original_location_earned_progress_or_full_effects_claim=True,no_duplicate_name_dialogue_or_generic_notice_credit=True)
    for row in new['records']:
        row['review']['formatting']=True
        if row['item_ID']==116 and row.get('message_id')==2931:
            row['formatting_reason']='One134-character logical paragraph;source-preserving native47-column formatter yields3 complete rows. Both main/standalone240x96 consumers in4/16-bit modes match every word,first/final/interior glyph,bounds,pixels and original parent crops. Two actual menu holds match all3 entire description fields at native parent positions. No authored wraps,clipping,orphan,blank page,macro or substitution waiver.'
            row['coverage_key']=dict(file_path='/COMMON/MESFILE.DK4',id='COMMON_MESSAGE_2931')
        else:
            row['native_glyph_bounds_first_final_characters_consumers_gameplay_and_release_pending']=False
            row['formatting_reason']='The complete10-character title fits its owned original slot without a pointer/code/font change. All218 virtual/static getters and436 source callers bind the intended label;both native detail consumers and two actual menu holds preserve every title glyph and original parent placement. Earlier separately retained card/acquisition name-consumer evidence remains scoped and unchanged. No source nickname or other name is globally replaced.'
    validate_natural_dialogue_batch(new);ROOT.mkdir(parents=True);save(DOC,new)
    save(ROOT/'coordinated_title_description_source_native_actual_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),parent_ROM=old['current_ROM'],parent_ROM_sha256=old['current_ROM_sha256'],
        native_reference_ROM=receipt['research_ROM'],native_reference_ROM_sha256=receipt['research_ROM_sha256'],data_plan=receipt['data_plan'],
        all_two_records_have_five_source_context_localization_naturalness_formatting_gates=True,
        all218_current_description_and_item_name_getters_plus436_callers_pass=True,all217_other_descriptions_and_names_exact=True,
        all24_detail_font_modes_fields_complete_glyphs_pixels_bounds_and_original_parent_crops_pass=True,
        eight_actual_complete_title_description_field_matches_two_holds_and_normal_return=True,
        expanded224_byte_payload_actual31_screens_six_actor_controls_and_native_copy_cache_arena_verified=True,
        source_V609_growth_failure_and_all_failed_probe_successors_preserved=True,
        no_natural_event_original_location_earned_inventory_full_route_or_hardware_claim=True,
        ordinary_actual_menu_and_native_CPU_coverage_explicitly_distinct=True,
        source_clean_message2931_not_already_in_current_contextual_coverage_keys=True,
        static_item_title_and_generic_acquisition_notice_receive_no_duplicate_dialogue_credit=True,
        all207_names_nicknames_all_storylines_and_remaining_editorial_scope_preserved=True,
        viewed_sheets=sheets,registered_build_patch_and_release_regressions_pending=True,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,DOC,NATIVE,BOOT,FONTS,ACTUAL,Path(__file__)]}))
    print('Two coordinated revisions sealed with5gates;24 native planes/8 actual fields/31 screens/6 actor controls reviewed. Source and native scope preserved;registered build/patch/regressions pending;no credit yet.')
