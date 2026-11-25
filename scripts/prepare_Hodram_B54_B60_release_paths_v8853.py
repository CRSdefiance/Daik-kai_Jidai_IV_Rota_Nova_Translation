"""Declare the complete current-prefix evidence and all measured main/focused scope for release sealing."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_release_path_tools_v8853');assert not root.exists()
    old=Path('scripts/Hodram_B31_B53_release_paths_v8767.py').read_text(encoding='utf-8')
    scope=old[old.index('def observed_scope(data):'):]
    new_scope="""def observed_scope(data):
    groups=[(number,'main',g) for number in [54,56,57,58,59,60] for g in data['B'+str(number)+'_actual']['groups']]
    groups += [(60,'focus',g) for g in data['focus_actual']['groups']]
    comparisons=[('main',g) for g in data['comparison']['groups']]+[('focus',g) for g in data['focus_comparison']['groups']]
    reviewed=data['actual_review']
    return dict(editorial_units=82,speeches=82,typed_choices=0,revisions=46,justified_retentions=36,
        blocks=[54,55,56,57,58,59,60],scoped_static_actors=[1,20,23,24,36,84,113,114,119,141],
        actual_progressive_actor_IDs=reviewed['actual_progressive_actor_IDs'],offline_progressive_actor_IDs=[20,113],
        source_macro_counts=dict(FI=3,FA=4,FO=0),source_FE_panels=1,native_source_andEnglish_pages=167,
        actual_scene_runs=14,total_actual_frames=130014,main_runs=12,main_frames=116012,focused_runs=2,focused_frames=14002,
        complete_page_occurrences=sum(s['pages'] for _,_,g in groups for s in g['speeches']),
        complete_body_name_holds=sum(len(s['complete_holds']) for _,_,g in groups for s in g['speeches']),
        main_page_occurrences=129,main_complete_holds=580,
        actual_unique_speech_IDs=sorted({s['id'] for _,_,g in groups for s in g['speeches']}),
        offline_only_text_IDs=reviewed['offline_only_text_IDs'],
        unvisited_conditional_text_IDs=sorted({ident for _,_,g in groups for ident in g['unvisited_conditional_text_IDs']}),
        original_returns=[dict(block=number,evidence_scope=case,version=g['version'],**g['normal_return']) for number,case,g in groups],
        measured_comparisons=[dict(evidence_scope=case,**{key:g[key] for key in ['block','case','duration_differences','UI_request_differences','command_comparison_differences','script_returns','later_RGB_difference_count','final_PRNG_seeds','five_native_component_equality','whole_actors_equal','raw_calendars_uninterpreted','following_commands_equal']}) for case,g in comparisons],
        later_RGB_pairs=[len(g['later_RGB_comparisons']) for _,g in comparisons],
        manuscript_measured_limits=data['manuscript']['measured_limits'],
        own_registered_V8778_captain1_context_no_historical_RAM_overlay=True,
        initialized_whole_script_fixtures_not_original_optional_activation_location_or_earned_progress=True,
        B55_and18_B58_conditional_utterances_offline_only_with_complete_source_native_models=True,
        normal_end_preserves_existing_parser_resultword_independently_of_interpreter_mode=True,
        FE_distinct228x48_stride288_6x12_physical16pitch_palette_bitmap_VRAM_andabsentheader=True,
        three_English_two_page_records_each_page_has_complete_actual_body_name_holds=True,
        long_B60_actor_divergence_remains_focused7001_component_equality_is_bounded=True,
        all_timing_RNG_RGB_followingcommand_differences_retained_without_causal_orfuture_equivalence_claim=True,
        no_immediate_return_mainRAM_snapshot_claim=True,
        scoped_progressive_names_not_fullcatalogue_UI_all207_orcustomnames_approval=True,
        Geronimo_Alonso_shared_de_field_ownership_deployment_andfullconsumers_still_open=True,
        no_everyframe_causality_future_simulation_fullroute_hardware_oropaque_effect_semantics_claim=True)
"""
    extras={
      'source_controls':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json',
      'source_display':'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json',
      'source_names':'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json',
      'current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json',
      'pages':'work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json',
      'relocation':'work/analysis/Hodram_B54_B60_references_v8814/source_current_final_map.json',
      'independent_FE_actual':'work/analysis/Hodram_B56_FE_production_validation_v8851b/independent_FE_actual_validation.json',
      'policy_count_qualification':'work/analysis/Hodram_B54_B60_policy_count_v8834/terminal_failure_and_count_qualification.json',
      'FE_JSON_qualification':'work/analysis/Hodram_B56_FE_JSON_qualification_v8852/JSON_tuple_array_qualification.json',
    }
    module=derive('scripts/Hodram_B31_B53_release_paths_v8767.py','scripts/Hodram_B54_B60_release_paths_v8853.py',{
      'two-block':'seven-block','review_Hodram_B31_B53_actual_v8744':'review_Hodram_B54_B60_actual_v8825',
      'out/all_routes_combined_v8704_candidate.nds':'out/all_routes_combined_v8778_candidate.nds',
      'out/Hodram_B31_B53_reference_v8736_RESEARCH_ONLY.nds':'out/Hodram_B54_B60_reference_v8812_RESEARCH_ONLY.nds',
      'translations/hodram_B31_B53_editorial_manuscript_v5.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
      'translations/hodram_B31_B53_speaker_name_review_v3.json':'translations/hodram_B54_B60_speaker_name_review_v2.json',
      'Hodram_B31_B53_release_seal_v8769':'Hodram_B54_B60_release_seal_v8855',
      'translations/hodram_B31_B53_editorial_release_v1.json':'translations/hodram_B54_B60_editorial_release_v1.json',
      'translations/hodram_B31_B53_native_contract_v1.json':'translations/hodram_B54_B60_native_contract_v1.json',
      'Hodram_B31_B53_actual_review_v8744':'Hodram_B54_B60_actual_review_v8825',
      'Hodram_B31_B53_format_v8745b':'Hodram_B54_B60_format_v8826',
      'Hodram_B31_B53_metadata_v8748':'Hodram_B54_B60_metadata_v8829',
      'Hodram_B31_B53_policy_validation_v8750':'Hodram_B54_B60_policy_validation_v8831b',
      'Hodram_B31_B53_reconstruction_validation_v8752':'Hodram_B54_B60_reconstruction_validation_v8833',
      'Hodram_B31_B53_native_validation_v8754':'Hodram_B54_B60_native_validation_v8838',
      'Hodram_B31_B53_reference_validation_v8756':'Hodram_B54_B60_reference_validation_v8836',
      'Hodram_B31_B53_controls_validation_v8757':'Hodram_B54_B60_controls_validation_v8840',
      'Hodram_B31_B53_loader_validation_v8761':'Hodram_B54_B60_loader_validation_v8842',
      'Hodram_B31_B53_actual_validation_v8764':'Hodram_B54_B60_actual_validation_v8847',
      'Hodram_B31_B53_comparison_validation_v8766':'Hodram_B54_B60_comparison_validation_v8849',
      'Hodram_B52_release_v8705':'Hodram_B31_B53_release_v8779',
      'current_V8704_Hodram_native_v8707':'current_V8778_Hodram_native_v8781',
      'Hodram_B52_registered_startup_view_v8708':'Hodram_B31_B53_registered_startup_view_v8782',
      '\ndef proofs():':'\nPROOFS.update('+repr(extras)+')\n\ndef proofs():',
      scope:new_scope,
    })
    root.mkdir(parents=True);save(root/'source_locked_release_paths.json',dict(module=module,whole_current_registered_prefix_andall_measured_main_focused_offline_limits_explicit=True,all207_fullname_shared_de_customname_graphics_andolder_reaudit_scope_retained=True,reference_seal_andatomic_configuration_not_yet_written=True,new_credit=0,full_goal_complete=False))
