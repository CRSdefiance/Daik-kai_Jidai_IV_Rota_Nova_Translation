"""Derive a complete B169 actual-plane/flow audit, retaining all source effects."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_actual_tools_v4244')

if __name__ == '__main__':
    assert not ROOT.exists()
    old = Path('scripts/audit_lil_B168_actual_v4200.py').read_text(encoding='utf-8')
    start = old.index("        touch = next(row for row in intervals")
    stop = old.index('        for pending in trace',start)
    original_contact = old[start:stop]
    final_speech = "        final_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B169_R0167')\n        assert final_speech['returned'] <= effects[0]['start'] <= effects[0]['returned'] <= selected[-1]['start']\n        assert bytes.fromhex(commands[effects[0]['offset']]['whole_command_hex']).hex() == '00a0ffff29000100'\n"
    tool = derive('scripts/audit_lil_B168_actual_v4200.py','scripts/audit_lil_B169_actual_v4244.py',{
        original_contact:final_speech,
        '168':'169','lil_B168_actual_v4200':'lil_B169_actual_v4244',
        'lil_B168_display_fixture_v4198':'lil_B169_display_fixture_v4241',
        'lil_B168_native_approval_v4187/all54_native_progressive_FE_and_source_reconciliation':'lil_B169_native_approval_v4230/all36_native_progressive_and_source_reconciliation',
        'lil_B168_display_run_v4199':'lil_B169_display_run_v4242',
        'lil_B168_display_v4199':'lil_B169_display_v4242',
        'progressive/FE plane':'progressive plane',
        '51 <= len(intervals) <= 54':'33 <= len(intervals) <= 36',
        '== 2906':'== 2558','source_end_offset=2906':'source_end_offset=2558',
        '== 2582':'== 2550',
        'resources == [0x6342, 0x630B, 0x6300, 0x6301]':'resources == []',
        'all91_stored_fixture_commands':'all62_stored_fixture_commands',
        'DK4_MES_B168_R0020':'DK4_MES_B169_R0067',
        'DK4_MES_B168_R0048':'DK4_MES_B169_R0082',
        'DK4_MES_B168_R0135':'DK4_MES_B169_R0097',
        "sum(row['prefix'] == 254 for row in intervals) == 3":"sum(row['prefix'] == 254 for row in intervals) == 0",
        "sum(row['prefix'] == 254 for row in actual) == 3":"sum(row['prefix'] == 254 for row in actual) == 0",
        'actual_source_recruitment_effect':'actual_source_hex0029_0001_effect',
        'all_selected_speeches_presentations_resources_effects_and_FE_return_normally':'all_selected_progressive_speeches_and_source_effect_return_normally',
        'preview.width in [216, 228]':'preview.width == 216',
        'len(actual) + len(offline) == 54':'len(actual) + len(offline) == 36',
        'actual_progressive_FE_three_predicates_full_effect_and_return':'actual_progressive_three_predicates_full_effect_and_return',
        'all_source_relative_containers_three_queries_resources_presentations_A000_and_both_stored_ends_preserved':'all_source_relative_containers_three_queries_A000_and_single_stored_end_preserved',
        'all_three_FE_notices_and_final_Mikhail_speech_observed':'no_FE_objects_and_final_give_and_take_speech_observed',
        'source_effect_returns_after_touch_protest_sigh_and_before_FE_help':'source_hex0029_0001_effect_returns_after_final_give_and_take_and_before_end',
        'second_consecutive_endword_decoder_proven_offline_not_actually_reached':'single_source_tail_endword_actually_reached_and_decoded',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,
        source_A000_notation_amendment='work/analysis/lil_B169_operand_notation_v4243/source_A000_hex0029_0001_decimal41_1_metadata_correction.json',
        no_natural_eligibility_earned_flag_or_full_route_claim=True,full_goal_complete=False))
    print('B169 complete actual glyph/portrait/flow audit prepared;effect hex0029/0001 after final speech remains intact.')
