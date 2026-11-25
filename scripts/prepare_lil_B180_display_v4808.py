"""Prepare all-source conditional B180 fixtures and read-only current observations."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_display_tools_v4808')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B179_display_fixture_v4739.py','scripts/research_lil_B180_display_fixture_v4808.py',{
        'B179':'B180','display_fixture_v4739':'display_fixture_v4808','display_v4739':'display_v4808',
        'all_routes_combined_v4701':'all_routes_combined_v4766','relocation_v4729':'relocation_v4798',
        'bank[179]':'bank[180]','source_block=179':'source_block=180',
        'len(commands)==16':'len(commands)==28',
        "assert [c['word'] for c in commands if c['word']!=0x4000]==[0xA000,0]":
        "assert [c['word'] for c in commands]==[c['word'] for c in group['all_clean_native_commands']]",
        'len(walk)==25 and len(speeches)==14':'len(walk)==37 and len(speeches)==11',
        "sum(c['word']==0xC200 for c in walk)==0":"sum(c['word']==0xC200 for c in walk)==1",
        "sum(c['word']==0xA000 for c in walk)==5":"sum(c['word']==0xA000 for c in walk)==7",
        "assert not any(c['word'] in [0x8000,0x100,0x200,0x300,0x400,0x2100,0x4100,0x2000] for c in walk)":
        "assert sum(c['word']==0x8000 for c in walk)==2 and sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==10\n        assert not any(c['word'] in [0x2100,0x4100,0x2000] for c in walk)",
        'all25_stored_fixture_commands':'all37_stored_fixture_commands',
        'all14_speeches13_progressive1_impersonal_FE_one_source_A000_single_end_no_C200_retained':
        'all11_speeches10_progressive1_FE_two_predicates_ten_branches_three_alternative_A000_C200_end_retained',
        'closing_notice_names_Sao_Jorge':'closing_notice_names_Lisbon','source_event179_not_selected':'source_event180_not_selected',
        'source_all16_commands_preserved_without_omission_or_flattening':'source_all28_commands_preserved_without_omission_or_flattening',
        'no_source_predicate_relative_pause_resources_presentations_or_typed_objects=True':
        'two_original_predicates_ten_relative_sites_preserved=True,no_source_pause_resources_presentations_or_typed_objects=True',
        'source_FE_notice_remains_impersonal_and_leading_A000_packed_operand_semantics_not_inferred':
        'source_FE_notice_remains_impersonal_and_alternative_A000_packed_operand_semantics_not_inferred',
        'stored_speech_objects=14':'stored_speech_objects=11',
        'actual_transition_A000_and_single_end_reachability_to_be_observed':'actual_predicate_RNG_effect_C200_and_single_end_to_be_observed',
        'B180 fixtures retain all16 commands+9 original init commands,thirteen progressive/one impersonal FE,one source A000,single end and no C200.':
        'B180 fixtures retain all28 commands+9 original init commands,ten progressive/one impersonal FE,two predicates,ten relative sites,three alternative A000s,C200 and end.'})]
    tools.append(derive('scripts/observe_script_sources_v733.py','scripts/observe_lil_B180_v4810.py',{
        "'player_descriptor16_hex': memory(player, 16).hex()}":
        "'player_descriptor16_hex': memory(player, 16).hex(),\n                    'original_RNG_seed':struct.unpack_from('<I',raw,0x168EB8)[0],\n                    'native_UI_request_words':list(struct.unpack_from('<7I',raw,0x2793C0)),\n                    'native_UI_pending_flag':struct.unpack_from('<I',raw,0x2793F8)[0]}"}))
    tools.append(derive('scripts/run_lil_B179_display_fixture_v4741.py','scripts/run_lil_B180_display_fixture_v4810.py',{
        'B179':'B180','display_fixture_v4739':'display_fixture_v4808',
        'display_run_v4741':'display_run_v4810','display_v4741':'display_v4810',
        'source_event179_not_selected':'source_event180_not_selected',
        "'displayed_original_source_block':179":"'displayed_original_source_block':180",
        'all_source16_commands_13_progressive1_impersonal_FE_A000_and_single_end_no_C200_retained':
        'all_source28_commands_10_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained',
        "changes = [":"changes = [(\"from scripts import observe_script_sources_v733 as original\",\"from scripts import observe_lil_B180_v4810 as original\"),"}))
    tools.append(derive('scripts/pin_lil_B179_display_v4740.py','scripts/pin_lil_B180_display_v4809.py',{
        'B179':'B180','display_tools_v4740':'display_tools_v4809','display_fixture_v4739':'display_fixture_v4808',
        'source_speeches=14,progressive=13':'source_speeches=11,progressive=10',
        'source_commands=16,stored_fixture_commands=25,source_A000=1':'source_commands=28,stored_fixture_commands=37,source_A000_alternatives=3',
        'All14-panel audit counts are source bound;no C200 probe.':'All11 source panels and conditional controls retained;actual observation pending.'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        source_speeches=11,source_commands=28,stored_fixture_commands=37,source_A000_alternatives=3,
        C200=1,source_predicates=2,relative_sites=10,source_end=572,frames_per_boot=9001,
        RNG_and_UI_fields_observed_readonly_at_each_command_boundary=True,no_ROM_or_emulator_run_yet=True,
        source_event180_not_naturally_selected_or_eligibility_earned=True,full_goal_complete=False))
    print('Prepared paired complete B180 content fixtures and read-only RNG/UI command-boundary observer.')
