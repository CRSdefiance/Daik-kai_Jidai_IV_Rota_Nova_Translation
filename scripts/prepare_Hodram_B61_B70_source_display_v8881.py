"""Prepare complete original dispatch, macro, and native-page source checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B61_B70_display_preparation_v8881')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
        'scripts.Hodram_B31_B53_registered_route_context_v8781':'scripts.Hodram_B54_B60_registered_route_context_v8868',
        'work/analysis/Hodram_B54_B60_source_display_v8794':'work/analysis/Hodram_B61_B70_source_display_v8881',
        'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json':
            'work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json',
        'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json':'work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json',
        'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json':
            'work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json',
        'work/analysis/Hodram_B54_B60_clean_names_v8793/twenty_clean_full_andprogressive_compositions_current_binding.json':
            'work/analysis/Hodram_B61_B70_clean_names_v8880/thirtytwo_clean_full_andprogressive_compositions_current_binding.json',
        'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json':'work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json',
        'current_B54_B60_English_dialogue_bodies_still_unconsulted':'current_B61_B70_English_dialogue_bodies_still_unconsulted',
        'current_B54_B60_English_dialogue_bodies_unconsulted':'current_B61_B70_English_dialogue_bodies_unconsulted',
        'ten_source_selector_voices':'sixteen_source_selector_voices',
        'len(rows)==82':'len(rows)==224',
        "for r in rows)==328":"for r in rows)==896",
        '82_complete_source_dispatches_alignments_pages_andmacro_binding.json':'224_complete_source_dispatches_alignments_pages_andmacro_binding.json',
        'source_FE_count=1,FE_original_null_actor_and228x48_288stride_6x12_metrics_16physicalpitch_bound_offline=True':
            'source_FE_count=0,FE_no_source_occurrences_prior_calibration_only=True',
        'source_queries_branches_context_names_editorial_current_localization_actual_andrelease_still_pending':
            'source_controls_proved_context_name_editorial_current_localization_actual_andrelease_still_pending',
        'All82source dispatches/328alignments/':'All224source dispatches/896alignments/'
    }
    result=derive('scripts/prove_Hodram_B54_B60_source_display_v8794.py','scripts/prove_Hodram_B61_B70_source_display_v8881.py',changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        complete_original_dispatch_actor_voice_macro_four_alignments_consumption_glyphs_pixels_bounds_andpagination_guards_preserved=True,
        FE_source_occurrences_zero_no_new_FE_source_coverage_claim=True,
        current_story_English_unread=True,new_credit=0,full_goal_complete=False))
    print('Prepared 224 source dispatches/896 macro alignment cases/native pages; not executed yet.')
