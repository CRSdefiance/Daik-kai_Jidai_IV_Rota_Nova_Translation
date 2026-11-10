"""Bind current names only after complete clean B49 and prerequisite-source glosses."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/prove_Rafael_B48_names_v8023.py','scripts/prove_Rafael_B49_names_v8078.py',{
        'B48':'B49','Rafael_B48_names_v8023':'Rafael_B49_names_v8078',
        'Rafael_B48_clean_gloss_v8022/91_fresh_clean_glosses_nine_source_identities_before_current_English.json':'Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json',
        'Rafael_B48_clean_names_v8021/nine_clean_static_identity_fields_before_current_English.json':'Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json',
        'current_V8013_Rafael_native_v8016':'current_V8066_Rafael_native_v8069',
        'Rafael_B47_context_binding_v8016':'Rafael_B48_context_binding_v8069',
        'all91_glosses_fresh_before_current_English_exposure':'current_English_never_exposed_for_this_batch',
        '[0,4,5,6,7,8,13,75,113]':'[0,2,4,5,6,8,9]',
        'len(excluded)==4':'len(excluded)==0',"len(native['rows'])==18":"len(native['rows'])==14",
        'all_eighteen_original_consumers':'all_fourteen_original_consumers','nine-static-speakers':'seven-static-speakers',
        'nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments':'seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments',
        'native_eighteen_progressive_andfull_getters':'native_fourteen_progressive_andfull_getters',
        'synthetic_defaults_all_nine_actors':'synthetic_defaults_all_seven_actors',
        'all36_default_macro_alignments':'all28_default_macro_alignments',
        'source_FI_atR370_only_other_default_probes_synthetic_not_new_source_macros':'source_two_FI_R311_R388_other_default_probes_synthetic_not_new_source_macros',
        'source_FE_four_records_excluded_from_static_name_getters_not_assumed_progressive':'no_source_FE_objects_no_FE_consumer_assumed',
        'printable4B_and71_are_source_speaker_state_not_prose':'source_actors_remain_executable_speaker_state_not_prose',
    }))
