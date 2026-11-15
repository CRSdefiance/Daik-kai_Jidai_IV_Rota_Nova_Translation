"""Derive complete source/English B52 entry fixtures with both original end commands retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_fixture_tools_v8648');assert not root.exists()
    result=derive('scripts/create_Hodram_B49_fixtures_v8406.py','scripts/create_Hodram_B52_fixtures_v8648.py',{
        'Hodram_B49_fixtures_v8406':'Hodram_B52_fixtures_v8648','Hodram_B49_reference_v8403':'Hodram_B52_reference_v8645','Hodram_B49_relocation_v8398':'Hodram_B52_relocation_v8642','Hodram_B49_references_v8405b':'Hodram_B52_references_v8647',
        'all36_commands14_full_preambles8_relatives2_choices_query_picture_hide_effects_andterminal_bound':'all14_commands3_full_preambles4_relatives_zeroqueries_twochoices4_opaque_controls_andboth_terminals_bound',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B52_current_v8631/current_effective.json',
        "sum(c['word']==0 for c in parsed)==1":"sum(c['word']==0 for c in parsed)==2",
        'v8406_RESEARCH_ONLY':'v8648_RESEARCH_ONLY',
        "sum(len(f['all_original_exchange_commands']) for f in fixtures)==72":"sum(len(f['all_original_exchange_commands']) for f in fixtures)==28",
        'Hodram complete clean/revised B49':'Hodram complete clean/revised B52',
        'all36_commands14_speeches8_relative_sites_two_typed_labels_preserved_perversion':'all14_commands3_speeches4_relative_sites_two_typed_labels_both_distinct_endwords_preserved_perversion',
        'registered_current_V8377_mainV4701_unchanged':'registered_current_V8609_mainV4701_unchanged',
        'Pinned two complete B49 fixtures:original8 initializers34bytes;all36commands14speeches8relatives2typedlabels perversion.':'Pinned two complete B52 fixtures:original8initializers34bytes;all14commands3speeches4relatives2typedlabels2distinctends perversion.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,original_eight_initializers_all_fourteen_commands_four_relative_operands_andboth_end_words_preserved=True,constant34byte_shift_only_no_commands_omitted=True,all_other_ROM_files_components_andopening_archive_inverse_required=True,no_RAM_eventflag_role_roster_funds_RNG_condition_orresult_forcing=True,research_only_no_natural_activation_location_hardware_orcredit_claim=True,new_credit=0,full_goal_complete=False))
