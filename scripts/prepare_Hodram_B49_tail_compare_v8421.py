"""Measure both bounded-tail choice runs,retaining all timing/state/PRNG/RGB differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_tail_compare_tools_v8421');assert not root.exists()
    result=derive('scripts/compare_Hodram_actual_v8283.py','scripts/compare_Hodram_B49_tail_v8421.py',{
        'Hodram_actual_comparison_v8283':'Hodram_B49_tail_comparison_v8421',
        'for number in [137,45,46]:':'for choice in [\'accept\',\'decline\']:\n        number=49',
        "Path(f'work/analysis/Hodram_actual_v8282/B{number}/paired_actual_dialogue_headers_flow_returns.json')":"Path('work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json')",
        "proof['all_observed_complete_body_name_holds_andnative_flow_pass']":"proof['all_observed_complete_glyph_masks_singlepages_names_native_flow_andreturns_pass']",
        "old,new=proof['groups'];":"old,new=[g for g in proof['groups'] if g['choice']==choice];",
        "assert all(g['normal_return'] and not g['unvisited_conditional_text_IDs'] for g in [old,new])":"assert all(g['normal_return'] for g in [old,new]) and old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']\n        assert len(old['speeches'])==len(new['speeches'])==(4 if choice=='accept' else 7)",
        'if number==46:':'if number==49:',
        "command['whole_command_hex']=='0048b5a8' and command['canonical_clean_offset']==140":"command['whole_command_hex']=='004894a8' and command['canonical_clean_offset']==962",
        "min(c['start'] for c in hide)-4":"min(c['returned'] for c in hide)-4",
        'descriptor=[0,181,1,5],layout=[0,0,0],original_Red_Dye_item181_source_control_not_Rafael4821=True':'descriptor=[0,148,1,5],layout=[0,0,0],original_Ullr_Bow_item148_source_4800_layout0=True,item_card_observed_during_original_hide_command_wait_not_assumed_instant_hide=True',
        'descriptor_layout_from_exact_original_operand_and8190b_native_consumer_not_dialogue_UI_request_words':'descriptor_layout_from_exact_original_operand_and8384_native_consumer_not_dialogue_UI_request_words',
        "f'B{number}_full_scene_transition_pairs.png'":"f'B{number}_{choice}_full_scene_transition_pairs.png'",
        'groups.append(dict(block=number,scene_pairs=scenes':'groups.append(dict(block=number,choice=choice,scene_pairs=scenes',
        'three_paired_whole_exchanges_controls_scenes_returns_bounded_later_state.json':'both_bounded_tail_comparisons.json',
        'total_actual_frames=100006':'total_actual_frames=40004',
        'initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths':'initialized_bounded_possession_dialogue_tail_not_whole_B49_inventory_eligibility_original_location_oroptional_event_activation',
        'current_registered_V8259_andmainV4701_unchanged':'current_registered_V8377_andmainV4701_unchanged',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_native_high_integer_constants_andmultiplicity_preserved=True,source_English_each_choice_compared_without_input_orstate_retiming=True,item148_layout0_andhide_wait_bound_to_original_commands=True,all_timing_UI_PRNG_actor_component_calendar_andRGB_differences_retained=True,no_broad_simulation_orlegitimate_inventory_trade_claim=True,new_credit=0,full_goal_complete=False))
