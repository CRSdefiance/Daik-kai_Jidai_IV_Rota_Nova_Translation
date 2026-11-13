"""Preserve every frozen and predecessor release dependency when preparing the cumulative seal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_seal_tools_v8855');assert not root.exists()
    producer=derive('scripts/seal_Hodram_B31_B53_release_v8769.py','scripts/seal_Hodram_B54_B60_release_v8855.py',{
        'Seal B52 approvals, all independent readers and complete registered V8609 ancestry.':'Seal82 Hodram approvals,all independent readers andcomplete registered V8778 ancestry.',
        'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_names_v1':'hodram_B54_B60_names_v1',
        'hodram_B31_B53_editorial_v2':'hodram_B54_B60_editorial_v1',
        'Hodram_B31_B53_release_paths_v8767':'Hodram_B54_B60_release_paths_v8853',
        "len(doc['records'])==3":"len(doc['records'])==82",
        "(doc['revised'],doc['retained'])==(3,0)":"(doc['revised'],doc['retained'])==(46,36)",
        "['negative_count']==236":"['negative_count']==625",
        "counts={'independent_reconstruction':51,'independent_references':20,'independent_native':12,\n            'independent_controls':12,'independent_loaders':8,'independent_actual':13,'independent_comparison':12}":"counts={'independent_reconstruction':161,'independent_references':25,'independent_native':12,\n            'independent_controls':12,'independent_loaders':11,'independent_actual':16,'independent_comparison':16,'independent_FE_actual':8}",
        "['complete_actual_holds']==76":"['complete_actual_holds']==676",
        "['unique_speech_IDs']==2":"['unique_speech_IDs']==63",
        "['later_full_RGB_pairs_recomputed']==68":"['later_full_RGB_pairs_recomputed']==335",
        '==[3,20,50,50]':'==[82,120,175,50]',
        "data['reference']['only_changed_blocks']==[31,53]":"data['reference']['only_changed_blocks']==[54,55,56,57,58,59,60]",
        'all323_otherSC1_blocks_andall_other_files_components_exact':'all318_otherSC1_blocks_andall_other_files_components_exact',
        "approval['all3_five_gates_true']":"approval['all82_five_gates_true']",
        '==(4,76,24004)':'==(150,676,130014)',
        "'hodram_B52_editorial_release_v3.json']]":"'hodram_B52_editorial_release_v3.json','hodram_B31_B53_editorial_release_v2.json']]",
        'all-routes-unified-v8704':'all-routes-unified-v8778',
        'all3_disjoint_source_current_final_references_andwhole_image_inverses_verified':'all82_disjoint_source_current_final_references_andwhole_image_inverses_verified',
        'all_independent_production_readers_and364_real_changedinput_rejections_pass':'all_independent_production_readers_and886_real_changedinput_rejections_pass',
        'own_registered_V8704':'own_registered_V8778','complete_registered_V8704':'complete_registered_V8778',
        "previous=read('translations/hodram_B52_editorial_release_v3.json')":"previous=read('translations/hodram_B31_B53_editorial_release_v2.json')",
        "Path('translations/hodram_B52_editorial_release_v3.json')":"Path('translations/hodram_B31_B53_editorial_release_v2.json')",
        'translations/hodram_B31_B53_native_contract_v1.json':'translations/hodram_B54_B60_native_contract_v1.json',
        'dk4-Hodram-B31_B53-editorial-release-v1':'dk4-Hodram-B54_B60-editorial-release-v1',
        'frozen_B31_B53_dependency_count':'frozen_B54_B60_dependency_count',
        'prior_complete_release_dependency_count':'prior_complete_B31_B53_release_dependency_count',
        'every_frozen_B31_B53_andentire_previous_B52_release_dependency_entry_retained_exact':'every_frozen_B54_B60_andentire_previous_B31_B53_release_dependency_entry_retained_exact',
        'Sealed B31/B53:3 approvals/all independent readers/whole registeredV8704;':'Sealed B54-B60:82 approvals/all independent readers/whole registeredV8778;',
        'dependencies including all734 frozen andevery previous B52 release entry.':'dependencies including all2468 frozen andevery previous B31/B53 release entry.',
    })
    root.mkdir(parents=True);save(root/'source_locked_seal_producer.json',dict(producer=producer,all_original_frozen_andcomplete_previous_release_dependency_entries_required_exact=True,all_predecessor_configuration_digests_andoriginal_builder_entries_preserved=True,all82_fivegate_and846_prior_plus40_saved_actual_FE_comparison_semantic_rejections_required=True,no_seal_config_ROM_orregistry_change_yet=True,new_credit=0,full_goal_complete=False))
