"""Atomic registered layer for three context-reviewed, native-validated speaker labels."""
import json
from pathlib import Path
from dk4tool.patch.generic_speaker_label_data_v1 import SOURCE,EXPECTED,transform,require
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
PATH='/__arm9__.bin'
CONFIG='translations/generic_speaker_labels_release_v1.json'
FORMAT='dk4-generic-speaker-labels-release-v1'

def load(path):return json.loads(Path(path).read_bytes())

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']==FORMAT,'unknown registered format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'review dependency changed:'+p)
    arm=image.read_file(PATH);require(sha(arm)==SOURCE==conf['source_ARM9_sha256'],'exact cumulative ARM9 required')
    require({p:sha(data) for _,p,data in image.iter_files()}==conf['source_files'],'complete cumulative files differ')
    require({p:sha(data) for p,data in image.iter_components()}==conf['source_components'],'complete cumulative components differ')
    require(sha(baseline.read_file(PATH))==conf['canonical_ARM9_sha256'],'canonical ARM9 differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'==conf['clean_ROM_sha256'],'clean input differs')
    clean=NdsImage.open(conf['clean_ROM']).read_file(PATH)
    require(sha(clean)==conf['clean_ARM9_sha256'],'clean ARM9 differs')
    doc,seal,names,actual,display=[load(conf[k]) for k in ['manuscript','approval','names','actual','display']]
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','v2 en-US policy required')
    require(doc['format']=='dk4-generic-speaker-label-localization-manuscript-v1' and doc['all_five_per_record_gates_approved_registered_release_pending'],'complete contextual name manuscript required')
    require(not doc['full_goal_complete'] and doc['all207_name_review_scope_remains_open'] and doc['no_duplicate_dialogue_or_prior_name_review_credit'],'full review scope and no duplicate credit required')
    require(len(doc['records'])==3 and [r['id'] for r in doc['records']]==[f'ACTOR_{i:03d}_PRIMARY_SPEAKER_LABEL' for i in EXPECTED],'exact three source identities required')
    for row in doc['records']:
        require(row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=True),'five record gates required')
        require(row['source_meaning'] and row['context'] and row['speaker'] and row['localization_note'] and row['formatting_reason'],'whole-context notes required')
        require(not row['target_native_getter_substitution_glyph_display_and_registered_release_pending'] and row['native_getter_substitution_glyph_and_representative_display_approved_registered_release_pending'],'native/display approval required')
        require(row['new_dialogue_completion_credit']==row['new_name_completion_credit']==0,'no duplicate source credit')
    require(seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'sealed manuscript differs')
    for flag in ['all621_parent_and621_target_primary_secondary_middle_consumers_pass','only_three_primary_outputs_change','all_five_gates_complete_for_three_source_owned_labels',
        'all414_target_progressive_catalogue_name_consumers_64_macro_alignments_three_native_planes_and16_actual_target_headers_pass',
        'complete_two_existing_exchanges28_speeches25_nameplates_observed_five_sheets_viewed',
        'no_full_catalogue_UI_natural_event_activation_original_location_full_route_or_hardware_claim',
        'all207_review_queue_not_complete_and_all_other_editorial_scope_preserved']:
        require(seal[flag] is True,'sealed requirement missing:'+flag)
    require(names['all414_target_getters_and414_parent_getters_executed'] and names['all204_unaffected_actors_both_name_consumers_exact']
        and names['all207_voice_classes_and_original_name_ownership_paths_exact'] and names['six_changed_getters_are_same_readonly_pointers_no_scratch_or_RAM_writes'],'all original name consumers required')
    require(names['changed_catalog_actor_IDs']==[164,165,172] and len(names['changed_consumer_cases'])==6,'exact changed actor consumers required')
    require(actual['complete_speech_observations']==28 and actual['complete_nameplate_observations']==25 and actual['actual_target_nameplate_cases']==16
        and actual['changed_actor_speech_observations']=={'164':4,'165':4,'172':8},'complete actual target observations required')
    require(actual['complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact'] and actual['new_cold_boots']==2 and actual['new_frames']==16002,'first/final glyph and fixture checks required')
    require(display['parent_target_macro_and_literal_outputs_exact'] and display['native_macro_alignment_cases']==64
        and display['actual_nameplate_independent_masks_and_five_complete_context_sheets_viewed']
        and display['original_current_ascii_y_plus_one_oracle_reused_only_name_data_changed']
        and display['odd_ASCII_pairs_emit_one_blank_space_without_losing_first_or_final_glyph'],'current native macro/font behavior required')
    require(display['all_unowned4MiB_models_RNG_inputs_outputs_ABI_canaries_and_source_owned_name_ring_restoration_exact'],'original full-name scratch ownership required')
    require(len(display['three_complete_original_font_native_planes'])==3 and len(display['viewed_sheets'])==5,'three planes/five reviewed sheets required')
    target,plan=transform(arm,clean,doc['records'])
    require(plan==doc['data_plan']==seal['source_owned_data_plan'] and sha(target)==conf['target_ARM9_sha256']==seal['target_ARM9_sha256'],'exact approved target required')
    require(target==Path(doc['target_ARM9']).read_bytes() and sha(target)==doc['target_ARM9_sha256'],'research data differs')
    report=dict(format=FORMAT,manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),
        source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),changed_records=[dict(id=r['id'],actor_ID=r['actor_ID'],before=r['current_English'],after=r['english']) for r in doc['records']],
        data_plan=plan,all_source_context_five_gates_native_name_macros_glyphs_and_representative_checks_pass=True,
        all_621_fields_204_other_names_fonts_code_pointers_allocations_and_scene_words_preserved=True,
        actual_catalogue_UI_not_claimed=True,no_duplicate_dialogue_credit=True,full_goal_complete=False)
    # The sole image mutation occurs after every source,prose,native and dependency check.
    image.replace_file(PATH,target)
    return report
