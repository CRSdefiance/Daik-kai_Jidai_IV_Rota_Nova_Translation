"""Derive changing-input B51 policy tests; retain all frozen dependency guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_policy_test_tools_v8584')
    assert not root.exists()
    result = derive('scripts/validate_Hodram_B50_policy_v8515b.py', 'scripts/validate_Hodram_B51_policy_v8584.py', {
        'hodram_B50_profile_v2': 'hodram_B51_profile_v1',
        'hodram_B50_layout_v2': 'hodram_B51_layout_v1',
        'hodram_B50_names_v2': 'hodram_B51_names_v1',
        'Hodram_B50_policy_validation_v8515b': 'Hodram_B51_policy_validation_v8584',
        'translations/hodram_B50_editorial_manuscript_v5.json': 'translations/hodram_B51_editorial_manuscript_v5.json',
        'translations/hodram_B50_speaker_name_review_v2.json': 'translations/hodram_B51_speaker_name_review_v2.json',
        'translations/hodram_B50_native_contract_v2.json': 'translations/hodram_B51_native_contract_v1.json',
        "('hodram_B50_'+suffix+'_v2.py')": "('hodram_B51_'+suffix+'_v1.py')",
        'Frozen Hodram-B50 contract changed': 'Frozen Hodram-B51 contract changed',
        'block=bank[50]': 'block=bank[51]',
        "'qa_waivers':['weak-line-ending']": "'actual_B51_source_andEnglish_body_header_covered':not row['actual_B51_source_andEnglish_body_header_covered'],'actual_B51_conditional_not_visited':not row['actual_B51_conditional_not_visited'],'qa_waivers':['weak-line-ending']",
        "changed['records'][index]['current']='Unapproved Name'": "changed['records'][index]['speaker']='Unapproved Name'",
        "changed['no_FE_personal_actor_name']=False": "changed['no_new_name_asset_orall207_name_review_credit']=False",
        "reject('names:FE-membership'": "reject('names:scope-credit'",
        "assert len(positives)==3 and sum(len(p['qa']['issues']) for p in positives)==3":
            "assert len(positives)==5 and sum(len(p['qa']['issues']) for p in positives)==2 and len(negatives)==322",
        'positive_batch_andone_scoped_name=True': 'positive_batch_andfour_scoped_names=True',
        'positive_editorial_units=3': 'positive_editorial_units=5',
        'three_original_infos_zero_warnings_waivers_preserved': 'two_original_infos_zero_warnings_waivers_preserved',
        'complete_original_B50_prose_controls_andcoherent_gift_phrase_boundary_frozen': 'complete_original_B51_prose_controls_qualified_names_andactual_versus_offline_scope_frozen',
        'B50 policy:3 speech compiler positives/no typedmenu/allfivegates/one scopedname pass;':
            'B51 policy:5 speech compiler positives/no typedmenu/allfivegates/four scopednames pass;',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, five_positive_compilers_and322_meaningful_changing_input_rejections_required=True,
        original_prose_preamble_refs_profiles_QA_runtime_locale_controls_andnames_rejections_preserved=True,
        per_record_actual_vs_unvisited_scope_mutations_added=True, all_frozen_guards_enabled_no_protected_file_mutation=True,
        no_test_orcredit_by_preparer=True))
