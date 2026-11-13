"""Registered two-file commit for the source/native/actual-approved cultural item correction."""
import json
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shachihoko_item116_research_v1 import transform
CONFIG='translations/shachihoko_item116_editorial_release_v1.json'
FORMAT='dk4-shachihoko-item116-editorial-release-v1'
ARM,COMMON='/__arm9__.bin','/COMMON/MESFILE.DK4'

def load(path):return json.loads(Path(path).read_bytes())
def require(value,message):
    if not value:raise ValueError('Item116 coordinated release: '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']==FORMAT,'wrong release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'changed proof dependency:'+p)
    arm,common=image.read_file(ARM),image.read_file(COMMON)
    require(sha(arm)==conf['source_ARM9_sha256'] and sha(common)==conf['source_COMMON_sha256'],'exact cumulative inputs required')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['source_files'],'cumulative file ancestry differs')
    require({p:sha(v) for p,v in image.iter_components()}==conf['source_components'],'cumulative component ancestry differs')
    require(sha(baseline.read_file(ARM))==conf['canonical_ARM9_sha256'],'canonical baseline differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','clean input differs')
    clean=NdsImage.open(conf['clean_ROM']);require(sha(clean.read_file(ARM))==conf['clean_ARM9_sha256'],'clean ARM9 differs')
    doc,seal,binding,native,boot,fonts,actual,names=[load(conf[k]) for k in ['manuscript','approval','bindings','native','boot','fonts','actual','actual_names']]
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','v2 American localization required')
    validate_natural_dialogue_batch(doc)
    require(doc['format']=='dk4-coordinated-cultural-item-editorial-v1' and len(doc['records'])==2,'exact two source identities required')
    require([r['id'] for r in doc['records']]==['ITEM_116_CULTURAL_NAME','COMMON_ITEM_116_CULTURAL_DESCRIPTION'],'wrong title or description identity')
    require(doc['all_five_per_record_gates_complete_registered_release_pending'] and not doc['full_goal_complete'] and doc['all207_names_all_storylines_and_full_editorial_goal_preserved'],'complete review gates and full objective required')
    require(doc['no_duplicate_name_dialogue_or_generic_notice_credit'] and doc['no_natural_event204_original_location_earned_progress_or_full_effects_claim'],'honest scope required')
    for row in doc['records']:
        require(row['item_ID']==116 and row['editorial_decision']=='revise' and row['formatting_reason'],'source-owned revisions and format reasons required')
        require(not any(c in row['english'] for c in ['\n','\r','{','%']) and row['english'].encode('ascii').decode('ascii')==row['english'],'plain unbroken safe prose required')
    description=doc['records'][1];japanese=common_message_entries(clean.read_file(COMMON),clean.read_file(ARM))[2931]
    require(description['message_id']==2931 and description['source_hex']==japanese.text.hex() and description['source_Japanese']==japanese.text.decode('cp932'),'exact clean description required')
    require(seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'sealed prose differs')
    for flag in ['all_two_records_have_five_source_context_localization_naturalness_formatting_gates','all218_current_description_and_item_name_getters_plus436_callers_pass',
        'all217_other_descriptions_and_names_exact','all24_detail_font_modes_fields_complete_glyphs_pixels_bounds_and_original_parent_crops_pass',
        'eight_actual_complete_title_description_field_matches_two_holds_and_normal_return','expanded224_byte_payload_actual31_screens_six_actor_controls_and_native_copy_cache_arena_verified',
        'no_natural_event_original_location_earned_inventory_full_route_or_hardware_claim','ordinary_actual_menu_and_native_CPU_coverage_explicitly_distinct',
        'all207_names_nicknames_all_storylines_and_remaining_editorial_scope_preserved']:
        require(seal[flag] is True,'approval requirement missing:'+flag)
    require(len(binding['native']['cases'])==218 and len(native['all218_native_COMMON_then_private_description_lookups']['cases'])==218,'all source/target description lookups required')
    require(len(native['only_item116_description_changes'])==1 and native['only_item116_description_changes'][0]['after']['item_ID']==116,'only item116 description may change')
    require(native['all217_other_compiled_paragraphs_pointers_and_all218_previous_target_name_outputs_exact'] and native['all_actual123264_deployed_payload_bytes_and_executed_target_instructions_exact'],'exact deployed target and unaffected names required')
    require(boot['all31_actual_same_input_whole_RGB_frames_equal_V6050'] and len(boot['frame_comparisons'])==31 and len(boot['all_six_postinit_whole_actor_and_captain_model_comparisons'])==6,'fresh source-bound growth boot/input regressions required')
    require(boot['complete_actual123264_payload_native_copy_reservation_and_cacheline_extents_verified'] and boot['original_and_disposable_town_battery_hashes_exact'],'native growth allocation/cache and battery preservation required')
    require(fonts['all24_native_field_word_glyph_pixel_bounds_and_parent_crop_cases_pass'] and len(fonts['cases'])==24 and fonts['all16_unselected_neighbor_item_planes_exact'],'both native consumers and modes required')
    require(actual['all_changed_title_and134_character_description_exact_native_independent_glyphs_and_original_parent_positions'] and len(actual['eight_complete_actual_title_description_field_matches'])==8,'complete actual title and paragraph fields required')
    require(actual['ordinary_X_Up_Up_A_then_B_B_menu_inputs_only_after_source_scene'] and actual['no_RAM_inventory_money_roster_condition_or_RNG_fixture'] and actual['actual_return_to_port_UI_frame']==8420,'ordinary menu visit and return required')
    require(names['all_two_current_native_independent_and_actual_field_masks_exact'] and names['no_glyph_or_source_substitution_loss'] and len(names['cases'])==2,'current card and acquisition name consumers required')
    require(len(seal['viewed_sheets'])==3 and all(r['viewed'] for r in seal['viewed_sheets']),'viewed complete native/actual sheets required')
    for r in seal['viewed_sheets']:require(sha(Path(r['path']).read_bytes())==r['sha256'],'reviewed sheet changed')
    target,newcommon,plan=transform(arm,common,clean.read_file(ARM),doc,binding)
    require(json.loads(json.dumps(plan))==doc['native_data_plan']==seal['data_plan'],'approved source-owned transform differs')
    require(sha(target)==conf['target_ARM9_sha256'] and sha(newcommon)==conf['target_COMMON_sha256'],'approved target hashes differ')
    require(target==Path(doc['target_ARM9']).read_bytes() and newcommon==Path(doc['target_COMMON']).read_bytes(),'independent reference data differs')
    report=dict(format=FORMAT,manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),
        source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),source_COMMON_sha256=sha(common),target_COMMON_sha256=sha(newcommon),
        changed_records=[dict(file_path=ARM,id=doc['records'][0]['id'],item_ID=116),dict(file_path=COMMON,id=doc['records'][1]['id'],message_ID=2931)],
        source_owned_data_plan=plan,proposal_research_flags_retained_as_historical_transform_metadata=True,
        all_source_context_five_gates_native_actual_growth_checks_verified_before_two_file_commit=True,
        all_other_records_names_graphics_fonts_components_and_original_native_display_controls_preserved=True,
        no_duplicate_dialogue_or_generic_notice_review_credit=True,full_editorial_objective_remains_active=True,full_goal_complete=False)
    # Both replacements happen only after every input,source,prose,native and actual guard.
    image.replace_file(ARM,target)
    image.replace_file(COMMON,newcommon)
    return report
