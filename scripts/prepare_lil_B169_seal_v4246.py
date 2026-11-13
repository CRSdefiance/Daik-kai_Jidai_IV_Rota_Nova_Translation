"""Derive the B169 reference approval with explicit actual/offline and operand scope."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_seal_tools_v4246')
if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/seal_lil_B168_references_v4202.py','scripts/seal_lil_B169_references_v4246.py',{
        'Seal all54 reviews with exact relocation and scoped progressive/FE/effect coverage.':'Seal all36 reviews with exact relocation and scoped progressive/effect coverage.',
        'prepare_lil_B168_research_v4192':'prepare_lil_B169_research_v4235',
        'lil_B168_reference_approval_v4202':'lil_B169_reference_approval_v4246',
        'lil_B168_editorial_manuscript_v7':'lil_B169_editorial_manuscript_v4',
        'lil_B168_editorial_manuscript_v8':'lil_B169_editorial_manuscript_v5',
        'lil_B168_editorial_relocation_map':'lil_B169_editorial_relocation_map',
        'lil_B168_reference_census_v4195/all82':'lil_B169_reference_census_v4238/all53',
        'lil_B168_relocated_controls_v4197/all54_progressive_FE_dispatches_three_predicates_and16_leaves':'lil_B169_relocated_controls_v4240/all36_progressive_dispatches_three_predicates_and5_leaves',
        'lil_B168_stored_v4191/all54_final_stored_targets216':'lil_B169_stored_v4234/all36_final_stored_targets144',
        'lil_B168_ends_v4196/four_declared_end_decodes':'lil_B169_ends_v4239/two_declared_end_decodes',
        'lil_B168_actual_v4200/actual_progressive_FE_three_predicates_full_effect_and_return':'lil_B169_actual_v4244/actual_progressive_three_predicates_full_effect_and_return',
        'lil_B168_display_fixture_v4198':'lil_B169_display_fixture_v4241',
        'lil_B168_transition_review_v4201/all9_sheets_contact_FE_source_effect_and_paired_return_review':'lil_B169_transition_review_v4245/all6_sheets_source_effect_and_paired_return_review',
        'all82_clean_current_target_commands_and12_relative_sites_reexecuted':'all53_clean_current_target_commands_and12_relative_sites_reexecuted',
        "len(control['relocated_dispatch_cases']) == 54":"len(control['relocated_dispatch_cases']) == 36",
        "len(control['all16_source_current_target_nonrelative_nonspeech_leaves']) == 16":"len(control['all5_source_current_target_nonrelative_nonspeech_leaves']) == 5",
        "stored['current_final_stored_macro_alignment_cases'] == 216 and len(stored['final_target_parity_cases']) == 54":"stored['current_final_stored_macro_alignment_cases'] == 144 and len(stored['final_target_parity_cases']) == 36",
        'all54_final_targets_complete_native_planes_equal_reviewed_planes':'all36_final_targets_complete_native_planes_equal_reviewed_planes',
        "ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4":"ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 2",
        "== 51 and not actual['failures']":"== 33 and not actual['failures']",
        "len(visual['all9_actual_sheets_viewed']) == 9 and len(visual['English_full_screen_views']) == 5":"len(visual['all6_actual_sheets_viewed']) == 6 and len(visual['English_full_screen_views']) == 3",
        'source_B168_later_A000_and_all_resources_presentations_and_FE_notices_preserved':'source_B169_later_numeric29_0001_A000_and_no_invented_resources_presentations_FE',
        "native['all54_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 432":"native['all36_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 288",
        "['DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135']":"['DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097']",
        "paths = [INPUT, PLAN, CENSUS, CONTROL, STORED, ENDS, ACTUAL, FIXTURE, VISUAL, Path(__file__)]":"amendment = Path(visual['source_effect_operand_notation_amendment'])\n    assert sha(amendment.read_bytes()) == visual['source_effect_operand_notation_amendment_sha256']\n    assert read(amendment)['operand_hex_values'] == ['0029','0001'] and read(amendment)['operand_decimal_values'] == [41,1]\n    paths = [INPUT, PLAN, CENSUS, CONTROL, STORED, ENDS, ACTUAL, FIXTURE, VISUAL, amendment, Path(__file__)]",
        "visual['all9_actual_sheets_viewed']":"visual['all6_actual_sheets_viewed']",
        'actual_selected_B168_source_events':'actual_selected_B169_source_events',
        'actual51_panels_three_FE_and_normal_return_pass':'actual33_progressive_panels_and_normal_return_pass',
        'no_B168_source_command_omitted':'no_B169_source_command_omitted',
        "== checked['block'] == 168":"== checked['block'] == 169",
        "len(block['command_map']) == 82":"len(block['command_map']) == 53",
        "len(block['text_records']) == 54":"len(block['text_records']) == 36",
        '[2906, 2910]':'[2558]',
        'dk4-lil-B168-source-relocation-map-v1':'dk4-lil-B169-source-relocation-map-v1',
        'all82_commands12_relative_sites60_target_skips_verified':'all53_commands12_relative_sites60_target_skips_verified',
        'all54_active_speech_targets_preserved':'all36_active_speech_targets_preserved',
        'all16_leaves_three_predicates_four_resources_six_presentations_one_effect_and_two_ends_exact':'all5_leaves_three_predicates_one_effect_and_one_end_exact',
        'two_consecutive_declared_endwords_preserved':'single_declared_tail_endword_preserved',
        'three_FE_null_actor_consumers_and_FI7_FA1_FO1_preserved':'no_FE_consumers_and_FI5_FO2_preserved',
        "    save(MAP, mapping)":"    mapping.update(source_effect_operand_hex_values=['0029','0001'],source_effect_operand_decimal_values=[41,1],source_effect_operand_notation_amendment=str(amendment),source_effect_operand_notation_amendment_sha256=sha(amendment.read_bytes()))\n    save(MAP, mapping)",
        "('termination_decode_proof', ENDS)":"('termination_decode_proof', ENDS), ('source_effect_operand_notation_amendment', amendment)",
        'all54_source_native_reference_and_representative_rules_approved':'all36_source_native_reference_and_representative_rules_approved',
        '54 approvals sealed:51 actual/three offline remarks,three FE,82commands/12spans/60skips/216storedcases.':'36 approvals sealed:33 actual/three offline remarks,no FE,53commands/12spans/60skips/144storedcases.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,no_prose_or_credit_change=True,full_goal_complete=False))
    print('B169 source-reference seal producer prepared;all53 commands and corrected hex0029/0001 operand reference required.')
