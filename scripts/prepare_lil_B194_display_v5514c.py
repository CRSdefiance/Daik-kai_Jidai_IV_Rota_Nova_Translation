"""Preserve all21 commands in paired default-state content fixtures; observe availability normally."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B194_display_tools_v5514')
if __name__ == '__main__':
    assert not ROOT.exists()
    rows = [derive('scripts/research_lil_B191_display_fixture_v5386.py', 'scripts/research_lil_B194_display_fixture_v5514.py', {
        'B191': 'B194', 'display_fixture_v5386': 'display_fixture_v5514', 'display_v5386': 'display_v5514',
        'combined_v5346': 'combined_v5478', 'relocation_v5377b': 'relocation_v5506b',
        'manuscript_v4': 'manuscript_v3', 'bank[191]': 'bank[194]', 'source_block=191': 'source_block=194',
        'len(commands)==38': 'len(commands)==21', 'len(walk)==47 and len(speeches)==13': 'len(walk)==30 and len(speeches)==11',
        "sum(c['word']==0xC200 for c in walk)==1": "sum(c['word']==0xC200 for c in walk)==2",
        "sum(c['word']==0xA000 for c in walk)==8": "sum(c['word']==0xA000 for c in walk)==5",
        "sum(c['word']==0x8000 for c in walk)==3": "sum(c['word']==0x8000 for c in walk)==1",
        "sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==16": "sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==4",
        'all47_stored_fixture_commands': 'all30_stored_fixture_commands',
        'all13_speeches12_progressive1_FE_three_predicates16_branches_four_alternative_A000_or_no_effect_C200_end_retained':
        'all11_stored_speeches10_progressive1_FE_one_unforced_availability4_branches_one_FI_resource42_two_C200_end_retained',
        'closing_notice_names_Calicut': 'closing_notice_names_Hangzhou', 'source_event191_not_selected': 'source_event194_not_selected',
        'source_all38_commands': 'source_all21_commands',
        'three_original_mixed_predicates16_relative_sites_preserved': 'one_original_availability_predicate_four_relative_sites_and_one_FI_preserved',
        'no_source_pause_resources_presentations_or_typed_objects': 'no_source_pause_presentations_or_typed_objects_resource42_preserved',
        'alternative_A000_packed_operand_semantics': 'leading_A000_packed_operand_semantics',
        'stored_speech_objects=13': 'stored_speech_objects=11',
        'actual_predicate_RNG_effect_C200_and_single_end_to_be_observed': 'actual_unforced_availability_selected_speeches_effect_C200_and_single_end_to_be_observed',
        'B191 fixtures retain all38 commands+9 original init commands,twelve progressive/one impersonal FE,three mixed predicates,16relative sites,four alternative A000s and no-effect paths,C200 and end.':
        'Paired B194 fixtures retain21 source commands,one unforced actor6 availability predicate,four relative sites,11 stored speeches,one FI,resource42 and two C200 sites.',
    })]
    rows.append(derive('scripts/run_lil_B191_display_fixture_v5388.py', 'scripts/run_lil_B194_display_fixture_v5515.py', {
        'B191': 'B194', 'display_fixture_v5386': 'display_fixture_v5514',
        'display_run_v5388': 'display_run_v5515', 'display_v5388': 'display_v5515',
        'source_event191_not_selected': 'source_event194_not_selected', "'displayed_original_source_block':191": "'displayed_original_source_block':194",
        'all_source38_commands_12_progressive1_FE_three_predicates16_branches_four_A000_or_no_effect_C200_end_retained':
        'all_source21_commands_10_progressive1_FE_one_availability4_branches_one_FI_resource42_two_C200_end_retained',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'prepared_tools.json', dict(tools=rows, source_commands=21, original_B22_initializers=9,
        stored_fixture_commands=30, stored_speech_objects=11, availability_unforced=True,
        actual_speech_selection_and_return_to_be_observed=True, no_natural_event194_or_earned_state_claim=True,
        source_all_commands_FI_relative_predicate_resource_and_two_UI_preserved=True,
        new_emulator_runs=0, new_review_credit=0, full_goal_complete=False))
