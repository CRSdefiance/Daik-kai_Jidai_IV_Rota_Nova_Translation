"""Expose current English only after complete clean contextual,identity andbranch review."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/map_Rafael_B48_current_v8028.py','scripts/map_Rafael_B49_current_v8086.py',{
        'B48':'B49','Rafael_B48_current_v8028':'Rafael_B49_current_v8086',
        'Rafael_next_clean_v8020':'Rafael_next_clean_v8073',
        'Rafael_B48_branch_gloss_v8027/91_fresh_glosses32_paths_B128_B37_context_before_current_English.json':'Rafael_B49_branch_gloss_v8085/61_refined_glosses256_paths_B39_B41_context_before_current_English.json',
        'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json':'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json',
        'all91_source_glosses_complete_exchange_nine_identities_and32_paths_bound_before_current_English':'all61_source_glosses_complete_exchange_seven_identities_and256_paths_bound_before_current_English',
        'Rafael_B48_source_controls_v8024/source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends.json':'Rafael_B49_source_controls_v8081/source_EV0_56_relative_sites280_cases13_raw_predicates1_query25_seeded_ends.json',
        'len(rows)==91':'len(rows)==61','all91_complete_source_current_refs':'all61_complete_source_current_refs',
        'all91_clean_whole_context_glosses':'all61_clean_whole_context_glosses',
        'source_explicit_completion_dependencies=[],source_completion_queries=[128,37]':'source_explicit_completion_dependencies=[39],source_explicit_exclusions=[151],source_completion_queries=[41]',
        'current_English_body_unread=False,current_effective_body_dispatch_andcatalogue_pending=True':'current_English_body_unread=False,current_English_dialogue_body_still_unread=False,current_English_dialogue_body_now_exposed=True,current_effective_body_dispatch_andcatalogue_pending=True',
        'after91 clean glosses,B128/B37 callbacks,names and32 native source paths':'after61clean glosses,B39/B41context,names and256native source paths',
    }))
    print(derive('scripts/prove_Rafael_B48_effective_v8029.py','scripts/prove_Rafael_B49_effective_v8087.py',{
        'B48':'B49','Rafael_B48_effective_v8029':'Rafael_B49_effective_v8087',
        'Rafael_B48_current_v8028/all91_complete_source_current_refs':'Rafael_B49_current_v8086/all61_complete_source_current_refs',
        'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json':'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json',
        'all91_clean_whole_context_glosses':'all61_clean_whole_context_glosses',
        'len(cases)==182 and len(rows)==91':'len(cases)==122 and len(rows)==61',
        "for r in rows)==4":"for r in rows)==0",
        'all91_effective_English_templates182_original_dispatches4_FE':'all61_effective_English_templates122_original_dispatches_no_FE',
        'all87_progressive_speakers_andvoices_match':'all61_progressive_speakers_andvoices_match',
        'four_FE_original_null_actor_calls_preserve_zero_source_FE_macros':'no_FE_objects_no_FE_dispatch_or_display_coverage_claim',
        'FE_incidental_r1_not_geometry_orstatic_actor':'all_seven_static_source_speakers_not_invented_from_incidental_r1',
        'all91_actual_body_name_bounds':'all61_actual_body_name_bounds',
        '182 original dispatches/91 effective templates':'122 original dispatches/61 effective templates',
        'Bind91 clean/current B48 speeches through original captain0 dispatch;four FE panels remain distinct.':'Bind61clean/current B49speeches through original captain0dispatch;noFEobjects.',
    }))
