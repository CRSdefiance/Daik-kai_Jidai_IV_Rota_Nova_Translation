"""Immutable six-outcome production evidence paths and measured, deliberately bounded scope."""
from pathlib import Path
from scripts.prepare_Hodram_outcome_checkpoint_v8341 import PROOFS as previous
PARENT=Path('out/all_routes_combined_v8300_candidate.nds')
ROM=Path('out/Hodram_B47_B48_reference_v8329_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v2.json')
MAP=Path('translations/hodram_outcomes_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Hodram_outcome_reference_seal_v8347/six_records15_commands_two_source_inverses_approved_reference.json')

def proofs():
    paths={**previous,'manuscript':DOC,'names':NAMES,
        'current':'work/analysis/Hodram_outcome_current_binding_v8343/six_exact_source_current_final_refs_registered_parent_anddisplay_binding.json',
        'source_final_binding':'work/analysis/Hodram_outcome_current_binding_v8343/source_current_final_reference_binding.json',
        'independent_rebuild':'work/analysis/Hodram_outcome_independent_rebuild_v8344/six_records15_commands_two_clean_source_inverses_entire_tested_ROM_equal.json',
        'native_contract':'translations/hodram_outcomes_native_contract_v1.json',
        'policy_validation':'work/analysis/Hodram_outcome_policy_validation_v8346/six_positives_source_facts_FE_FI_five_gates_profiles_andscope_rejections.json'}
    return {k:str(Path(v)) for k,v in paths.items()}

def observed_scope(data):
    actual=[g for key in ['actual47','actual48'] for g in data[key]['groups']];comparison=data['comparison']['groups'];later=data['later']['groups']
    return dict(complete_records=6,revisions=3,justified_retentions=3,source_macro_counts=dict(FI=1,FA=0,FO=0),source_FE_panels=1,scoped_static_actors=[2],default_macro_lengths=dict(FI=6,FA=9,FO=15),
        actual_whole_scene_runs=len(actual),actual_whole_scene_frames=sum(g['actual_frames'] for g in actual),focused_FE_frames=data['FE_geometry']['focused_actual_frames'],
        complete_source_andrevised_page_observations=sum(len(g['speeches']) for g in actual),complete_body_name_orFE_absent_header_holds=sum(len(s['complete_holds']) for g in actual for s in g['speeches']),
        normal_returns=[dict(block=g['block'],version=g['version'],**g['normal_return']) for g in actual],
        measured_later_comparisons=[dict(block=c['block'],command_field_differences=len(c['command_comparison_differences']),duration_differences=c['duration_differences'],UI_differences=c['UI_request_differences'],later_RGB_pairs=len(c['later_RGB_comparisons']),later_RGB_differences=c['later_RGB_difference_count'],final_PRNG_seeds=c['final_PRNG_seeds'],
            five_checked_final_components_equal=c['five_native_component_equality'],whole_actor_bytes_equal=c['whole_actors_equal'],final_captain_IDs=[n['captain_ID'] for n in c['final_native_values']],raw_calendars_uninterpreted=c['raw_calendars_uninterpreted'],
            all_observed_original_script_entry_andreturn_PRNG_pairs_equal=next(l for l in later if l['block']==c['block'])['all_observed_script_entry_andreturn_PRNG_pairs_equal']) for c in comparison],
        source_FE_original_typed_descriptors_palette_bankD_VRAM_andfour_complete_bitmap_holds=True,
        paint_context_is_temporary_stack_storage_persistent_view_bitmap_andpalette_distinct=True,
        whole_original_script_opening_fixtures_not_natural_optional_activation_original_location_eligibility_orearned_progress=True,
        no_everyframe_causal_proof_future_random_outcome_broad_simulation_fullroute_orhardware_equivalence=True,
        no_RNG_input_flags_roster_roles_funds_conditions_orresults_forced=True)
