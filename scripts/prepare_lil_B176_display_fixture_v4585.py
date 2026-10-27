"""Derive complete B176 fixtures without omitting its leading source effect."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B176_display_preparation_v4585')
assert not root.exists()
tool=derive('scripts/research_lil_B175_display_fixture_v4531.py','scripts/research_lil_B176_display_fixture_v4585.py',{
    'B175':'B176','lil_B175':'lil_B176','display_fixture_v4531':'display_fixture_v4585',
    'all_routes_combined_v4496':'all_routes_combined_v4541',
    'relocation_v4521':'relocation_v4575','display_v4531':'display_v4585',
    'bank[175]':'bank[176]','source_block=175':'source_block=176',
    'len(commands)==39':'len(commands)==13',
    '==[0x6000,0x6344,0x4696,0x4635,0xC200,0,0]':'==[0xA000,0xC200,0]',
    'len(walk)==48 and len(speeches)==32':'len(walk)==22 and len(speeches)==10',
    "sum(c['word']==0 for c in walk)==2":"sum(c['word']==0 for c in walk)==1",
    "sum(c['word']==0xA000 for c in walk)==4":"sum(c['word']==0xA000 for c in walk)==5",
    "sum(r['source_selector']==254 for r in texts)==9":"sum(r['source_selector']==254 for r in texts)==1",
    'all48_stored_fixture_commands':'all22_stored_fixture_commands',
    'all32_speeches23_progressive9_FE_one_resource_three_presentations_C200_both_ends_retained':
        'all10_speeches9_progressive1_impersonal_FE_one_source_A000_C200_single_end_retained',
    'source_port_not_stated_initialized_fixture_town_is_Amsterdam':
        'closing_notice_names_Seville_without_proving_earlier_scene_location_initialized_fixture_town_is_Amsterdam',
    'source_event175_not_selected_or_eligibility_earned':'source_event176_not_selected_or_eligibility_earned',
    'source_all39_commands_preserved_without_omission_or_flattening':'source_all13_commands_preserved_without_omission_or_flattening',
    'no_source_predicate_relative_A000_pause_or_typed_objects':'no_source_predicate_relative_pause_resources_presentations_or_typed_objects',
    'source_FE_woman_and_CA80_7D80_presentation_operands_not_assigned_guessed_actor_identity':
        'source_FE_notice_remains_impersonal_and_leading_A000_packed_operand_semantics_not_inferred',
    'stored_speech_objects=32,actual_transitions_and_two_end_reachability_to_be_observed':
        'stored_speech_objects=10,actual_transition_A000_and_single_end_reachability_to_be_observed',
    'all39 commands+9 original init commands,23 progressive/nine FE panels,C200 and both ends.':
        'all13 commands+9 original init commands,nine progressive/one impersonal FE,one source A000,C200 and single end.',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,source_commands=13,fixture_commands=22,
    source_A000=1,original_prelude_A000=4,source_FE=1,source_speeches=10,
    no_ROM_registry_ledger_orcredit_change_yet=True,full_goal_complete=False))
