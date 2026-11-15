"""Seal one whole-context speaker label after current-native and actual image review."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_label_approval_v6266');INPUT=Path('translations/shady_man_label_manuscript_v1.json');OUTPUT=Path('translations/shady_man_label_manuscript_v2.json')
NAMES=Path('work/analysis/shady_man_names_v6263b/all207_distinct_names621_fields_eight_voices_and_one_changed_primary.json')
ACTUAL=Path('work/analysis/shady_man_scene_v6265d/complete_source_path_and_all_ten_changed_headers.json')
DISPLAY=Path('work/analysis/shady_man_macros_fonts_v6264/unchanged96_macro_alignments_and_complete_single_row_label.json')
DIFFERENCES=Path('work/analysis/shady_man_scene_v6265d/unmasked_source_target_timing_and_RNG_differences.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();names,actual,display,old=map(read,[NAMES,ACTUAL,DISPLAY,INPUT])
    assert names['all414_parent_and414_target_name_consumers_pass'] and names['all621_parent_and621_target_fields_pass'] and names['all206_unaffected_actors_both_name_consumers_exact']
    assert actual['complete_speech_observations']==18 and actual['actual_target_nameplate_cases']==10 and actual['complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact']
    assert display['parent_target_macro_and_literal_outputs_exact'] and display['native_macro_alignment_cases']==96
    assert len(actual['review_sheets'])==2
    viewed=[]
    for r in actual['review_sheets']:
        assert sha(Path(r['path']).read_bytes())==r['sha256'];viewed.append(dict(**r,viewed_after_image_return=True))
    plane=display['complete_original_font_native_plane'];assert sha(Path(plane['image']).read_bytes())==plane['image_sha256']
    diffs=read(DIFFERENCES);assert len(diffs['command_differences'])==16 and diffs['no_timing_RNG_whole_state_or_broad_simulation_equivalence_claim']
    new=deepcopy(old);row=new['records'][0];assert row['actor_ID']==173 and row['english']=='Shady Man';row['review']['formatting']=True
    row['target_native_getter_substitution_glyph_display_and_registered_release_pending']=False
    row['native_getter_substitution_glyph_and_representative_display_approved_registered_release_pending']=True
    row['formatting_reason']='Both original progressive/full-catalogue consumers and621 original name-field getters pass on each exact parent/target snapshot. The complete single-row native font plane preserves all nine characters plus the odd-pair blank. Ten actual Shady Man headers match independent full glyph masks and the entire previous-label width plus blank guards. Both context sheets and native plane were viewed.96 macro/literal alignment cases preserve original results and owned scratch behavior. No fit-driven shortening or manual breaks.'
    new.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),source_context_localization_naturalness_approved_native_format_and_release_pending=False,all_five_per_record_gates_approved_registered_release_pending=True,no_duplicate_dialogue_or_prior_name_review_credit=True,all206_other_actors_secondary_middle_fields_aliases_and_approved_names_preserved=True,actual_catalogue_UI_not_visited_native_getters_and_font_bounds_checked=True,source_target_timing_RNG_differences_preserved_no_broad_equivalence_claim=True,actual_observation_scope='One complete Japanese B206 purchase-path fixture in initialized Amsterdam,18 speech panels/10 changed headers. No natural event206 activation,original location,earned progression,full effects,full routes or hardware claim. Asking9000 gold is not proof of a completed9000 payment.',native_reference_ROM='out/shady_man_label_v6260_RESEARCH_ONLY.nds',native_reference_ROM_sha256=sha(Path('out/shady_man_label_v6260_RESEARCH_ONLY.nds').read_bytes()))
    save(OUTPUT,new);ROOT.mkdir(parents=True)
    save(ROOT/'one_label_source_native_display_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),target_ARM9_sha256=new['target_ARM9_sha256'],source_owned_data_plan=new['data_plan'],all_five_gates_complete_for_one_source_owned_label=True,all621_parent_and621_target_fields_pass=True,all414_parent_and414_target_name_consumers_pass=True,only_actor173_primary_changes_all206_other_names_and_voices_exact=True,original96_macro_alignments_and_complete_font_plane_pass=True,actual18_nameplates10_target_headers_two_sheets_and_native_plane_viewed=True,viewed_sheets=viewed,viewed_native_plane=dict(**plane,viewed_after_image_return=True),no_catalogue_UI_natural_activation_original_location_full_effects_routes_earned_progress_or_hardware_claim=True,timing_and_RNG_differences_explicitly_preserved=True,timing_difference_proof=str(DIFFERENCES),timing_difference_proof_sha256=sha(DIFFERENCES.read_bytes()),full207_name_and_wider_editorial_goal_remains_open=True,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,OUTPUT,NAMES,ACTUAL,DISPLAY,DIFFERENCES,Path(__file__)]}))
    print('Shady Man five-gate name review sealed:621 fields/414 names per version,96 macro alignments,complete plane and10 actual headers. Timing/RNG differences retained;registered release pending.')
