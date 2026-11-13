"""Atomic cumulative data layer for one source-reviewed and native-validated speaker label."""
import json
from pathlib import Path
from dk4tool.patch.shady_man_label_data_v1 import SOURCE,EXPECTED,transform,require
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
PATH='/__arm9__.bin';CONFIG='translations/shady_man_label_release_v1.json';FORMAT='dk4-shady-man-label-release-v1'
def load(path):return json.loads(Path(path).read_bytes())
def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']==FORMAT,'unknown registered format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'review dependency changed:'+p)
    arm=image.read_file(PATH);require(sha(arm)==SOURCE==conf['source_ARM9_sha256'],'exact cumulative ARM9 required')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['source_files'],'complete cumulative files differ')
    require({p:sha(v) for p,v in image.iter_components()}==conf['source_components'],'complete cumulative components differ')
    require(sha(baseline.read_file(PATH))==conf['canonical_ARM9_sha256'],'canonical ARM9 differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'==conf['clean_ROM_sha256'],'clean input differs')
    clean=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(clean)==conf['clean_ARM9_sha256'],'clean ARM9 differs')
    doc,seal,names,actual,display=[load(conf[k]) for k in ['manuscript','approval','names','actual','display']]
    require(doc['format']=='dk4-shady-man-label-localization-manuscript-v1' and doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','complete v2 en-US manuscript required')
    require(doc['all_five_per_record_gates_approved_registered_release_pending'] and not doc['full_goal_complete'] and doc['all207_name_review_scope_remains_open'] and doc['no_duplicate_dialogue_or_prior_name_review_credit'],'full editorial scope and no duplicate credit required')
    require(len(doc['records'])==1 and doc['records'][0]['id']=='ACTOR_173_PRIMARY_SPEAKER_LABEL','one exact reviewed identity required')
    row=doc['records'][0]
    require(row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=True),'five record gates required')
    require(all(row[k] for k in ['source_meaning','context','speaker','localization_note','formatting_reason']),'whole-context notes required')
    require(not row['target_native_getter_substitution_glyph_display_and_registered_release_pending'] and row['native_getter_substitution_glyph_and_representative_display_approved_registered_release_pending'],'native/display approval required')
    require(row['new_dialogue_completion_credit']==row['new_name_completion_credit']==0,'no duplicate review credit')
    require(seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'sealed manuscript differs')
    for key in ['all_five_gates_complete_for_one_source_owned_label','all621_parent_and621_target_fields_pass','all414_parent_and414_target_name_consumers_pass','only_actor173_primary_changes_all206_other_names_and_voices_exact','original96_macro_alignments_and_complete_font_plane_pass','actual18_nameplates10_target_headers_two_sheets_and_native_plane_viewed','no_catalogue_UI_natural_activation_original_location_full_effects_routes_earned_progress_or_hardware_claim','timing_and_RNG_differences_explicitly_preserved','full207_name_and_wider_editorial_goal_remains_open']:
        require(seal[key] is True,'sealed requirement missing:'+key)
    require(names['all414_parent_and414_target_name_consumers_pass'] and names['all621_parent_and621_target_fields_pass'] and names['all206_unaffected_actors_both_name_consumers_exact'] and names['all207_voice_classes_and_original_name_ownership_paths_exact'] and names['only_actor173_primary_changes_secondary_middle_and_all_pointers_exact'],'all original name consumers required')
    require(names['changed_catalog_actor_IDs']==[173] and len(names['changed_consumer_cases'])==2 and len(names['changed_field_consumers'])==1,'sole reviewed primary change required')
    require(actual['complete_speech_observations']==actual['complete_nameplate_observations']==18 and actual['actual_target_nameplate_cases']==10 and actual['new_cold_boots']==1 and actual['new_frames']==16001,'representative complete source path required')
    require(actual['complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact'] and actual['source_and_target_command_offsets_words_results_lengths_and_UI_words_exact'] and actual['no_whole_state_or_broad_simulation_equivalence_claim'],'complete glyphs and honest trace comparison required')
    require(actual['exit_frame']==7896 and actual['following_B120_end_frame']==12693,'complete source path return required')
    require(display['parent_target_macro_and_literal_outputs_exact'] and display['native_macro_alignment_cases']==96 and display['all_unowned4MiB_models_RNG_inputs_outputs_ABI_canaries_and_source_owned_name_ring_restoration_exact'],'complete original macro ownership required')
    require(display['complete_original_font_native_plane']['complete_first_final_glyphs_order_bounds_canaries_and_single_row_native_plane_exact'] and len(seal['viewed_sheets'])==2 and seal['viewed_native_plane']['viewed_after_image_return'],'complete native and actual visual review required')
    diff=load(seal['timing_difference_proof']);require(sha(Path(seal['timing_difference_proof']).read_bytes())==seal['timing_difference_proof_sha256'] and len(diff['command_differences'])==16 and diff['no_timing_RNG_whole_state_or_broad_simulation_equivalence_claim'],'unmasked measured timing/RNG differences required')
    target,plan=transform(arm,clean,doc['records'])
    require(plan==doc['data_plan']==seal['source_owned_data_plan'] and sha(target)==doc['target_ARM9_sha256']==conf['target_ARM9_sha256']==seal['target_ARM9_sha256'],'exact reviewed target required')
    require(target==Path(doc['target_ARM9']).read_bytes(),'research data differs')
    report=dict(format=FORMAT,manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),changed_records=[dict(id=row['id'],actor_ID=173,before=row['current_English'],after=row['english'])],data_plan=plan,all_source_context_five_gates_native_names_macros_glyphs_and_representative_checks_pass=True,all621_fields206_other_names_fonts_code_pointers_allocations_scene_words_and_unread_tail_preserved=True,actual_catalogue_UI_and_broad_simulation_equivalence_not_claimed=True,no_duplicate_dialogue_credit=True,full_goal_complete=False)
    image.replace_file(PATH,target)
    return report
