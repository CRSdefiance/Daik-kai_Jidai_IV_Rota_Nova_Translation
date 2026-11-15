"""Source-lock four whole-outcome scene fixtures and identical ordinary-input captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_scene_tools_v8332');assert not root.exists();tools=[]
    fixture='work/analysis/Hodram_outcome_fixtures_v8332/four_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json'
    tools.append(derive('scripts/create_Hodram_scene_fixtures_v8279.py','scripts/create_Hodram_outcome_fixtures_v8332.py',{
        'Hodram_scene_fixtures_v8279':'Hodram_outcome_fixtures_v8332',
        'work/analysis/Hodram_reference_v8276/research_image_receipt.json':'work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json',
        'work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json':'work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json',
        'work/analysis/Hodram_reference_census_v8278/all60_commands8_relative_sites28_records_three_EV1_entries_shipped_callers.json':'work/analysis/Hodram_outcome_reference_census_v8331/all15_commands_zero_relative_sites6_records_two_EV1_entries_shipped_callers.json',
        'all60_source_current_target_commands8_relative_sites28_complete_preambles_bound':'all15_source_current_target_commands_zero_relative_sites6_complete_preambles_bound',
        'len(planned)==6':'len(planned)==4',"sum(len(f['all_original_exchange_commands']) for f in fixtures)==120":"sum(len(f['all_original_exchange_commands']) for f in fixtures)==30",
        '_v8279_RESEARCH_ONLY.nds':'_v8332_RESEARCH_ONLY.nds','updated[:-6]':'updated[:-4]',
        'B137/B45/B46':'B47/B48','six_complete_clean_revised_SC1_scripts':'four_complete_clean_revised_SC1_scripts',
        'all60_commands28_speeches8_relative_sites_preserved_perversion':'all15_commands6_speeches_zero_relative_sites_preserved_perversion',
        'actual_selected_path_body_name_pagination_4800_layout0_hide4700_transitions_returns_pending':'actual_selected_path_body_name_pagination_FE_scene_controls_transitions_returns_pending',
        'registered_current_V8259_mainV4701_unchanged':'registered_current_V8300_mainV4701_unchanged','new_ROMs=6':'new_ROMs=4',
    }))
    tools.append(derive('scripts/run_Hodram_scenes_v8280.py','scripts/run_Hodram_outcomes_v8333.py',{
        'Hodram_scene_runs_v8280':'Hodram_outcome_scene_runs_v8333',
        'work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json':fixture,
        'choices=[137,45,46]':'choices=[47,48]',
        'frames={137:24001,45:10001,46:16001}[block]':'frames={47:10001,48:10001}[block]',
        '_v8280':'_v8333',
    }))
    root.mkdir(parents=True);save(root/'source_locked_whole_fixture_andreadonly_capture_derivations.json',dict(tools=tools,all_native_numeric_constants_andmultiplicity_preserved=True,
        paired_scripts_keep_all_original_controls_effects_preambles_andcomplete_ends=True,same_ordinary_inputs_no_savestate_orRAM_conditions_roster_roles_funds_RNG_orresults_forced=True,new_credit=0,full_goal_complete=False))
