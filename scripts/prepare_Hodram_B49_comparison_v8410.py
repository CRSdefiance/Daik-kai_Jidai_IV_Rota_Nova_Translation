"""Measure the selected B49 path anditem148 layout2 with no controller/state retiming."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_comparison_tools_v8410');assert not root.exists()
    result=derive('scripts/compare_Hodram_actual_v8283.py','scripts/compare_Hodram_B49_actual_v8410.py',{
        'Hodram_actual_comparison_v8283':'Hodram_B49_comparison_v8410',
        'for number in [137,45,46]:':'for number in [49]:',
        'work/analysis/Hodram_actual_v8282':'work/analysis/Hodram_B49_actual_v8409',
        "assert all(g['normal_return'] and not g['unvisited_conditional_text_IDs'] for g in [old,new])":"assert all(g['normal_return'] for g in [old,new])\n        assert old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs'] and len(old['unvisited_conditional_text_IDs'])==8\n        assert len(old['speeches'])==len(new['speeches'])==6",
        'if number==46:':'if number==49:',
        "c['word']==0x4800":"c['word']==0x4820",
        "command['whole_command_hex']=='0048b5a8' and command['canonical_clean_offset']==140":"command['whole_command_hex']=='204894a8' and command['canonical_clean_offset']==32",
        'original_4800_calls=display':'original_4820_calls=display',
        'descriptor=[0,181,1,5],layout=[0,0,0],original_Red_Dye_item181_source_control_not_Rafael4821=True':'descriptor=[0,148,1,5],layout=[2,0,0],original_Ullr_Bow_item148_source_4820_layout2=True',
        'descriptor_layout_from_exact_original_operand_and8190b_native_consumer_not_dialogue_UI_request_words':'descriptor_layout_from_exact_original_operand_and8384_native_consumer_not_dialogue_UI_request_words',
        'original4800_4700_actual=resource':'original4820_4700_actual=resource,unvisited_conditional_text_IDs=old[\'unvisited_conditional_text_IDs\']',
        'three_paired_whole_exchanges_controls_scenes_returns_bounded_later_state.json':'paired_selected_path_comparison.json',
        'total_actual_frames=100006':'total_actual_frames=20002',
        'current_registered_V8259_andmainV4701_unchanged':'current_registered_V8377_andmainV4701_unchanged',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_measured_command_timing_UI_PRNG_actor_native_component_calendar_andRGB_differences_retained=True,exact_source_item148_layout2_andhide_sequence_bound=True,six_observed_speeches_eight_unvisited_conditional_speeches_explicit=True,no_emulator_replay_input_retiming_orstate_forcing=True,new_credit=0,full_goal_complete=False))
