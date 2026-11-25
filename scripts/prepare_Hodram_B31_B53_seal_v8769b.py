"""Prepare the exact established registered-prefix seal for the two-block batch."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_seal_tools_v8769b');assert not root.exists()
    source=Path('scripts/seal_Hodram_B52_release_v8693.py').read_text('utf-8')
    start=source.index("    assert data['independent_actual']['summary']");end=source.index('    parent,reference=',start)
    qualified="""    assert data['independent_actual']['actual_summary']['complete_actual_holds']==76
    assert data['independent_actual']['actual_summary']['unique_speech_IDs']==2
    assert data['independent_comparison']['comparison_summary']['later_full_RGB_pairs_recomputed']==68
    assert [data['independent_controls']['native_control_summary'][k] for k in ['independent_final_dispatches','native_relative_cases','normal_seeded_ends','original_result_channel_cases']]==[3,20,50,50]
    assert data['independent_controls']['native_control_summary']['original_current_native_context']['candidate_sha256']==data['predecessor_release']['candidate_sha256']
"""
    # Inspect the qualified context's literal schema before deriving this producer.
    from scripts.verify_village_wrap_v608 import read
    context=read('work/analysis/Hodram_B31_B53_controls_validation_v8757/independent_controls_validation.json')['native_control_summary']['original_current_native_context']
    assert 'candidate_sha256' in context
    old="""    approval=data['format_approval'];assert approval['all5_five_gates_true'] and approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())"""
    new="""    approval=data['format_approval'];assert approval['all3_five_gates_true'] and data['metadata']['predecessor_sha256']==approval['manuscript_sha256'] and data['metadata']['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())"""
    receipt=derive('scripts/seal_Hodram_B52_release_v8693.py','scripts/seal_Hodram_B31_B53_release_v8769.py',{
        'Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'hodram_B52_editorial_v2':'hodram_B31_B53_editorial_v2',
        'dk4tool.dialogue.hodram_B52_':'dk4tool.dialogue.hodram_B31_B53_',
        "len(doc['records'])==3 and len(doc['typed_choice_records'])==2 and (doc['revised'],doc['retained'])==(2,3)":"len(doc['records'])==3 and not doc['typed_choice_records'] and (doc['revised'],doc['retained'])==(3,0)",
        "data['policy_validation']['negative_count']==243":"data['policy_validation']['negative_count']==236",
        "counts={'independent_reconstruction':26,'independent_references':20,'independent_native':10,'independent_menu':12,\n            'independent_controls':9,'independent_loaders':7,'independent_actual':7,'independent_comparison':6}":"counts={'independent_reconstruction':51,'independent_references':20,'independent_native':12,\n            'independent_controls':12,'independent_loaders':8,'independent_actual':13,'independent_comparison':12}",
        source[start:end]:qualified,
        "data['reference']['only_changed_blocks']==[52] and data['reference']['all324_otherSC1_blocks_andall_other_files_components_exact']":"data['reference']['only_changed_blocks']==[31,53] and data['reference']['all323_otherSC1_blocks_andall_other_files_components_exact']",
        old:new,
        "==(12,138,50406)":"==(4,76,24004)",
        "'hodram_outcomes_editorial_release_v7.json'":"'hodram_outcomes_editorial_release_v8.json'",
        "'hodram_B49_editorial_release_v5.json','hodram_B50_editorial_release_v2.json','hodram_B51_editorial_release_v1.json'":"'hodram_B49_editorial_release_v6.json','hodram_B50_editorial_release_v3.json','hodram_B51_editorial_release_v2.json','hodram_B52_editorial_release_v3.json'",
        "profile='all-routes-unified-v8609'":"profile='all-routes-unified-v8704'",
        "doc['records']+doc['typed_choice_records']":"doc['records']",
        'all5_disjoint_source_current_final_references_andwhole_image_inverses_verified':'all3_disjoint_source_current_final_references_andwhole_image_inverses_verified',
        'all_independent_production_readers_and340_real_changedinput_rejections_pass':'all_independent_production_readers_and364_real_changedinput_rejections_pass',
        'historical_source_context_andunequal_whole_snapshots_qualified_without_RAM_overlay':'own_registered_V8704_captain1_context_without_historical_RAM_overlay',
        'complete_registered_V8609_andall_prior_dependencies_preserved':'complete_registered_V8704_andall_prior_dependencies_preserved',
        "previous=read('translations/hodram_B52_editorial_release_v1.json')":"previous=read('translations/hodram_B52_editorial_release_v3.json')",
        "Path('translations/hodram_B52_editorial_release_v1.json')":"Path('translations/hodram_B52_editorial_release_v3.json')",
        "Path('scripts/Hodram_B52_release_paths_v8693.py')":"Path('scripts/Hodram_B31_B53_release_paths_v8767.py')",
        "Path('translations/hodram_B52_native_contract_v1.json')":"Path('translations/hodram_B31_B53_native_contract_v1.json')",
        "format='dk4-Hodram-B52-editorial-release-v1'":"format='dk4-Hodram-B31_B53-editorial-release-v1'",
        'frozen_B52_dependency_count':'frozen_B31_B53_dependency_count',
        'every_frozen_B52_andoriginal855_B51_dependency_entry_retained_exact':'every_frozen_B31_B53_andentire_previous_B52_release_dependency_entry_retained_exact',
        "print('Sealed B52:5 approvals/all independent readers/whole registeredV8609;'":"print('Sealed B31/B53:3 approvals/all independent readers/whole registeredV8704;'",
        "'dependencies including all471 frozen and855 predecessor entries. Atomic tests/registered integration pending; no ROM/credit.'":"'dependencies including all734 frozen andevery previous B52 release entry. Atomic tests/registered integration pending; no ROM/credit.'",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_original_ancestry_frozen_andprior_dependency_merge_guards_preserved=True,
        source_locked_three_speech_two_block_nochoice_ownV8704_context_andall364_semantic_rejections_bound=True,
        no_seal_configuration_orROM_written_by_preparer=True,new_credit=0,full_goal_complete=False))
