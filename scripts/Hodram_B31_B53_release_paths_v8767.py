"""Source-qualified two-block production paths and bounded actual/offline scope."""
from pathlib import Path
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS as ACTUAL_PROOFS

PARENT=Path('out/all_routes_combined_v8704_candidate.nds')
ROM=Path('out/Hodram_B31_B53_reference_v8736_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v3.json')
SEAL=Path('work/analysis/Hodram_B31_B53_release_seal_v8769/reference_seal.json')
CONFIG=Path('translations/hodram_B31_B53_editorial_release_v1.json')
PROOFS={**ACTUAL_PROOFS,
    'manuscript':str(DOC),'names':str(NAMES),
    'native_contract':'translations/hodram_B31_B53_native_contract_v1.json',
    'result_flow':'work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    'actual_review':'work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json',
    'format_approval':'work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json',
    'metadata':'work/analysis/Hodram_B31_B53_metadata_v8748/explicit_route_binding.json',
    'policy_validation':'work/analysis/Hodram_B31_B53_policy_validation_v8750/policy_validation.json',
    'independent_reconstruction':'work/analysis/Hodram_B31_B53_reconstruction_validation_v8752/independent_reconstruction_validation.json',
    'independent_native':'work/analysis/Hodram_B31_B53_native_validation_v8754/independent_native_validation.json',
    'independent_references':'work/analysis/Hodram_B31_B53_reference_validation_v8756/independent_reference_validation.json',
    'independent_controls':'work/analysis/Hodram_B31_B53_controls_validation_v8757/independent_controls_validation.json',
    'independent_loaders':'work/analysis/Hodram_B31_B53_loader_validation_v8761/independent_loader_validation.json',
    'independent_actual':'work/analysis/Hodram_B31_B53_actual_validation_v8764/independent_actual_validation.json',
    'independent_comparison':'work/analysis/Hodram_B31_B53_comparison_validation_v8766/independent_comparison_validation.json',
    'predecessor_release':'work/analysis/Hodram_B52_release_v8705/registered_release_verification.json',
    'own_input':'work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json',
    'own_startup':'work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
    'Gerhard_reference':'work/analysis/Gerhard_reference_v8215/research_image_receipt.json',
}

def proofs():
    return {key:str(Path(value)) for key,value in PROOFS.items()}

def observed_scope(data):
    groups=[(number,g) for number,key in [(31,'B31_actual'),(53,'B53_actual')] for g in data[key]['groups']]
    comparisons=data['comparison']['groups']
    return dict(editorial_units=3,speeches=3,typed_choices=0,revisions=3,justified_retentions=0,
        blocks=[31,53],scoped_static_actors=[34,113],source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=0,
        native_source_andEnglish_pages=6,actual_scene_runs=4,total_actual_frames=24004,
        complete_page_occurrences=sum(len(g['speeches']) for _,g in groups),
        complete_body_name_holds=sum(len(s['complete_holds']) for _,g in groups for s in g['speeches']),
        actual_unique_speech_IDs=sorted({s['id'] for _,g in groups for s in g['speeches']}),
        unvisited_conditional_text_IDs=sorted({ident for _,g in groups for ident in g['unvisited_conditional_text_IDs']}),
        original_returns=[dict(block=number,version=g['version'],**g['normal_return']) for number,g in groups],
        measured_comparisons=[{key:g[key] for key in ['block','case','duration_differences','UI_request_differences','command_comparison_differences','script_returns','later_RGB_difference_count','final_PRNG_seeds','five_native_component_equality','whole_actors_equal','raw_calendars_uninterpreted','following_commands_equal']} for g in comparisons],
        later_RGB_pairs=[len(g['later_RGB_comparisons']) for g in comparisons],
        own_registered_V8704_captain1_context_no_historical_RAM_overlay=True,
        initialized_whole_script_fixtures_not_original_optional_activation_location_or_earned_progress=True,
        short_B31_R0013_complete_native_offline_only_actual_long_variant_same_consumer=True,
        normal_end_preserves_existing_parser_resultword_independently_of_interpreter_mode=True,
        source52_31_53_dependencies_not_continuous_exchange_chronology_B52choice_effect_orunnamed_man_identity=True,
        actual_progressive_names34_113_not_fullcatalogue_UI_all207_orcustomnames_approval=True,
        source_fullname_getter19thglyph_wrap_qualified_allcharacters_complete_no_geometry_change=True,
        no_everyframe_causality_future_simulation_fullroute_hardware_oropaque_effect_semantics_claim=True)
