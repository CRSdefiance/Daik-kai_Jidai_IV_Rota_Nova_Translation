"""Source-lock whole B49 entry fixtures and identical ordinary-input capture runners."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_scene_tools_v8406');assert not root.exists();tools=[]
    fixture='work/analysis/Hodram_B49_fixtures_v8406/two_whole_scripts.json'
    tools.append(derive('scripts/create_Hodram_outcome_fixtures_v8332.py','scripts/create_Hodram_B49_fixtures_v8406.py',{
        'Hodram_outcome_fixtures_v8332':'Hodram_B49_fixtures_v8406',
        'work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json':'work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json',
        'work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json':'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json',
        'work/analysis/Hodram_outcome_reference_census_v8331/all15_commands_zero_relative_sites6_records_two_EV1_entries_shipped_callers.json':'work/analysis/Hodram_B49_references_v8405b/references.json',
        "callers['all15_source_current_target_commands_zero_relative_sites6_complete_preambles_bound']":"callers['all36_commands14_full_preambles8_relatives2_choices_query_picture_hide_effects_andterminal_bound']",
        "    for group in mapping['groups']:\n        number=group['block']; records=group['text_records']":"    current=read('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')\n    assert current['current_ROM_sha256']==reference['parent_sha256']\n    for group in mapping['groups']:\n        group=dict(group,all_source_commands=current['groups'][0]['all_source_commands'])\n        number=group['block']; records=group['text_records']",
        '_v8332_RESEARCH_ONLY.nds':'_v8406_RESEARCH_ONLY.nds',
        'len(planned)==4':'len(planned)==2',
        "sum(len(f['all_original_exchange_commands']) for f in fixtures)==30":"sum(len(f['all_original_exchange_commands']) for f in fixtures)==72",
        'updated[:-4]':'updated[:-2]',
        'B47/B48':'B49',
        'four_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json':'two_whole_scripts.json',
        'all15_commands6_speeches_zero_relative_sites_preserved_perversion':'all36_commands14_speeches8_relative_sites_two_typed_labels_preserved_perversion',
        'registered_current_V8300_mainV4701_unchanged':'registered_current_V8377_mainV4701_unchanged',
        'new_ROMs=4':'new_ROMs=2',
        "    print('Pinned six Hodram whole-exchange fixtures: original8 initializers34bytes; all60commands28speeches8relatives perversion. No runtime forcing, credit or registered release.')":"    print('Pinned two complete B49 fixtures:original8 initializers34bytes;all36commands14speeches8relatives2typedlabels perversion.No runtime forcing,credit orregistered release.')",
    }))
    tools.append(derive('scripts/run_Hodram_outcomes_v8333.py','scripts/run_Hodram_B49_v8407.py',{
        'Hodram_outcome_scene_runs_v8333':'Hodram_B49_scene_runs_v8407',
        'work/analysis/Hodram_outcome_fixtures_v8332/four_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json':fixture,
        'choices=[47,48]':'choices=[49]',
        'frames={47:10001,48:10001}[block]':'frames={49:10001}[block]',
        '_v8333':'_v8407',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_native_high_integer_constants_andmultiplicity_preserved=True,whole36_commands14_speeches8_relatives_two_choices_query_pictures_effects_andend_retained=True,identical_ordinary_Hodram_inputs_no_runtime_state_forcing=True,no_natural_optional_activation_location_orunvisited_conditional_coverage_claim=True,new_credit=0,full_goal_complete=False))
