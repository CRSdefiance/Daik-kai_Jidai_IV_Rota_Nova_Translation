"""Bind every B51 reference to original loaders and the shipped caller census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_reference_tools_v8572')
    assert not root.exists()
    insert = '''    b=deepcopy(b)
    manuscript=read('translations/hodram_B51_editorial_manuscript_v2.json')
    for ref in b['text_records']:
        row=next(r for r in manuscript['records'] if r['id']==ref['id'])
        for key in ['source_reference','current_reference','source_selector','source_complete_preamble_hex']:
            assert ref.get(key,row[key])==row[key]
            ref[key]=deepcopy(row[key])
    b['all_source_commands']=a['all_source_commands']
    qualified={**mapping,'groups':[b],'external_references_complete':True,'source_current_final_references_complete':True}
    qualified_path=ROOT/'source_current_final_map.json';save(qualified_path,qualified)
'''
    result = derive('scripts/verify_Hodram_B49_references_v8405b.py', 'scripts/verify_Hodram_B51_references_v8572.py', {
        'Hodram_B49_references_v8405b': 'Hodram_B51_references_v8572',
        'Hodram_B49_reference_v8403': 'Hodram_B51_reference_v8570b',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json': 'work/analysis/Hodram_B51_current_v8559/current_effective.json',
        'Hodram_B49_relocation_v8398': 'Hodram_B51_relocation_v8565',
        'Hodram_B49_loaders_v8404': 'Hodram_B51_loaders_v8571',
        'work/analysis/Hodram_B49_controls_v8401d/stored_controls.json': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
        'block=bank[49]': 'block=bank[51]',
        'len(maps)==36': 'len(maps)==20',
        "r['native_selected_block']==49": "r['native_selected_block']==51",
        '[(49,49,[48])]': '[(51,51,[])]',
        "len(controls['final_dispatches'])==14": "len(controls['stored_dispatches'])==5",
        "ROOT.mkdir(parents=True);save(ROOT/'references.json'": "ROOT.mkdir(parents=True)\n" + insert + "    save(ROOT/'references.json'",
        'block=49': 'block=51',
        'all14_text_records': 'all5_text_records',
        "typed_choice_records=b['choice_commands']": "typed_choice_records=[]",
        'all36_commands14_full_preambles8_relatives2_choices_query_picture_hide_effects_andterminal_bound':
            'all20_commands5_full_preambles8_relatives2_queries4_opaque_controls_andterminal_bound',
        'event49_requires48_not_natural_eligibility_location_orfull_chronology_proof': 'event51_no_listed_prerequisite_not_natural_eligibility_location_orchronology_proof',
        'actual_B49_backing_controller_transitions_policy_atomic_registered_release_pending': 'actual_B51_branch_headers_transitions_policy_atomic_registered_release_pending',
        'B49:36 command maps/8 relative sites40cases/14 speeches2choices,originalEV1entry,325load-cache/650modes andfresh shipped-code census pass.Actual UI/policy/release pending.':
            'B51:20 command maps/8 relative sites40cases/5 speeches2queries,originalEV1entry,325load-cache/650modes andshipped-code census pass.Actual/policy/release pending.',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, complete_five_speech_source_current_final_andall_twenty_command_references_required=True,
        all_eight_nested_relative_targets_original_EV1_entry_andall_native_load_cache_parent_guards_preserved=True,
        qualified_reference_corrects_only_historical_block_label_not_ROM_bytes=True, no_ROM_write_orcredit_by_preparer=True))
