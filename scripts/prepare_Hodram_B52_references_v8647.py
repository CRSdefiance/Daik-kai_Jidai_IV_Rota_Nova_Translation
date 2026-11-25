"""Bind B52 command/choice references and reuse an identical complete native-unit caller census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_reference_tools_v8647');assert not root.exists()
    reuse="""    from ndspy.code import MainCodeFile,loadOverlayTable
    from dk4tool.patch.main_pool_cache_visibility import BASE
    units=[('section'+str(n),s.ramAddress,bytes(s.data)) for n,s in enumerate(MainCodeFile(image.read_file('/__arm9__.bin'),BASE).sections)]
    units += [('overlay'+str(n),s.ramAddress,bytes(s.data)) for n,s in loadOverlayTable(image.rom.arm9OverlayTable,lambda _,f:image.rom.files[f]).items()]
    unit_hashes=[dict(name=n,base=b,bytes=len(d),sha256=sha(d)) for n,b,d in units]
    assert unit_hashes==prior['native_call_census']['units']
    bound_census=deepcopy(prior['native_call_census'])
"""
    result=derive('scripts/verify_Hodram_B51_references_v8572.py','scripts/verify_Hodram_B52_references_v8647.py',{
        'Hodram_B51_references_v8572':'Hodram_B52_references_v8647','Hodram_B51_reference_v8570b':'Hodram_B52_reference_v8645','Hodram_B51_current_v8559':'Hodram_B52_current_v8631','Hodram_B51_relocation_v8565':'Hodram_B52_relocation_v8642','Hodram_B51_loaders_v8571':'Hodram_B52_loaders_v8646','Hodram_B51_stored_v8566':'Hodram_B52_stored_v8643',
        'work/analysis/Hodram_outcome_reference_census_v8331/all15_commands_zero_relative_sites6_records_two_EV1_entries_shipped_callers.json':'work/analysis/Hodram_B51_references_v8572/references.json',
        '    fresh=census(image);assert fresh==prior[\'native_call_census\']\n':reuse,
        'block=bank[51]':'block=bank[52]','len(maps)==20':'len(maps)==14',"len(b['relative_fixups'])==8":"len(b['relative_fixups'])==4","for r in b['relocated_skip_cases'])==40":"for r in b['relocated_skip_cases'])==20",
        "r['native_selected_block']==51":"r['native_selected_block']==52",
        "[(e['event_ID'],e['script_block'],e['must_be_completed']) for e in events]==[(51,51,[])]":"[(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in events]==[(52,52,[30],[74])]",
        "len(controls['stored_dispatches'])==5 and len(controls['normal_seeded_ends'])==25":"len(controls['stored_dispatches'])==3 and len(controls['distinct_seeded_ends'])==50 and len(controls['typed_choice_records'])==2",
        'hodram_B51_editorial_manuscript_v2':'hodram_B52_editorial_manuscript_v3','block=51':'block=52',
        "all5_text_records=b['text_records'],typed_choice_records=[]":"all3_speech_records=b['text_records'],typed_choice_records=controls['typed_choice_records']",
        'native_call_census=fresh,fresh_caller_censuses=1':'native_call_census=bound_census,fresh_caller_censuses=0,exact_reused_caller_censuses=1,all_original_census_section_overlay_names_bases_lengths_andpayload_hashes_exact=True',
        'all20_commands5_full_preambles8_relatives2_queries4_opaque_controls_andterminal_bound':'all14_commands3_full_preambles4_relatives_zeroqueries_twochoices4_opaque_controls_andboth_terminals_bound',
        'event51_no_listed_prerequisite_not_natural_eligibility_location_orchronology_proof':'event52_requires30_excludes74_not_natural_eligibility_location_orchronology_proof',
        'actual_B51_branch_headers_transitions_policy_atomic_registered_release_pending':'actual_B52_changed_menu_bothend_branch_headers_transitions_policy_atomic_registered_release_pending',
        'Bind all B49 commands/entries and a fresh shipped-code caller census':'Bind all B52 commands/entries and an exactly reused complete shipped-code caller census',
        'B51:20 command maps/8 relative sites40cases/5 speeches2queries,originalEV1entry,325load-cache/650modes andshipped-code census pass.':'B52:14command maps/4relative sites20cases/3speeches2choices/2distinctends,originalEV1entry,325load-cache/650modes andexact all-native-unit census reuse pass.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,three_speech_two_choice_clean_current_final_refs_andboth_end_commands_bound=True,all_native_section_overlay_names_bases_lengths_hashes_must_equal_original_census_inputs=True,no_unchanged_caller_scan_orcompleted_native_probe_replay=True,no_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
