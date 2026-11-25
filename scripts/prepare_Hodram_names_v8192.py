"""Bind six current Hodram source-speaker identities only after complete clean glosses andowncontext."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_names_tools_v8192')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/prove_Rafael_B49_names_v8078.py','scripts/prove_Hodram_names_v8192.py',{
        'Rafael_B49_names_v8078':'Hodram_B137_B45_B46_names_v8192',
        'Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json':'Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json',
        'Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json':'Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json',
        'current_V8066_Rafael_native_v8069':'current_V8172_Hodram_native_v8187',
        'Rafael_B48_context_binding_v8069/own_Rafael_startup_andstrict_captain0_context.json':'Hodram_current_binding_v8187/own_Hodram_startup_andstrict_captain1_context.json',
        "gloss['current_English_never_exposed_for_this_batch']":"gloss['source_only_no_current_body_orname_comparison_no_localized_manuscript']",
        "r['current_English_body_unread']":"r['current_English_body_not_yet_consulted']",'[0,2,4,5,6,8,9]':'[1,2,9,16,18,113]',
        'actor = root+0x19E4 if ident==0 else root+4+32*ident':'actor = root+0x19E4 if ident==1 else root+4+32*ident',
        'all_fourteen_original_consumers':'all_twelve_original_consumers','seven-static-speakers':'six-static-speakers',
        "{'assert captain==2':'assert captain==0'}":"{'assert captain==2':'assert captain==1'}",'captain0-voices':'captain1-voices',
        "len(native['rows'])==14":"len(native['rows'])==12",
        "'captain==3':'captain==0'":"'captain==3':'captain==1'",
        "b'Rafael Castor Castor Co.'":"b'Hodram Bergstrom Bergstrom Fleet'", "b'Rafael'":"b'Hodram'", "b'Castor'":"b'Bergstrom'", "b'Castor Co.'":"b'Bergstrom Fleet'",
        'measured-own-Rafael-defaults':'measured-own-Hodram-defaults',
        "start['actual_original_captain_ID']==0 and start['all_whole_RGB_actor_andcaptain_controls_equal']":"start['actual_original_captain_ID']==1 and start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass'] and start['no_historical_snapshot_orinitialized_RAM_overlay']",
        'seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json':'six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json',
        'native_fourteen_progressive_andfull_getters':'native_twelve_progressive_andfull_getters',
        'measured_default_macro_lengths=dict(FI=6,FA=6,FO=10)':'measured_default_macro_lengths=dict(FI=6,FA=9,FO=15)',
        'synthetic_defaults_all_seven_actors':'synthetic_defaults_all_six_actors','all28_default_macro_alignments':'all24_default_macro_alignments',
        'source_two_FI_R311_R388_other_default_probes_synthetic_not_new_source_macros':'source_zero_FI_FA_FO_all_default_probes_synthetic_not_new_source_macros',
        'Bind nine clean identities and18 current native getters before B49 English body comparison.':'Bind six clean identities and12 current native getters before Hodram B137/B45/B46 English body comparison.',
        'current_English_B49_bodies_still_unread':'current_English_Hodram_B137_B45_B46_bodies_still_unread',
        'Native names/voices/defaults pass;English B49 bodies remain unread.':'Native six names/voices/defaults pass;Hodram B137/B45/B46 English bodies remainunread.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared six-speaker12-getter/6-voice/24synthetic-default checks inownHodram captain1 context.')
