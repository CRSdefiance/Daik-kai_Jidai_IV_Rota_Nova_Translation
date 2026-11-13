"""Derive an atomic B170 compiler with its own linear/pause/C200/two-end contract."""
import ast
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_compiler_tools_v4301')
OLD = Path('dk4tool/patch/lil_B169_editorial_v2.py')
NEW = Path('dk4tool/patch/lil_B170_editorial_v1.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    text = OLD.read_text(encoding='utf-8')
    def section(start, stop, value):
        global text
        a, b = text.index(start), text.index(stop, text.index(start))
        text = text[:a] + value + text[b:]
    section('SELECTORS = ', '\n\ndef load', '''SELECTORS = {2, 25}
FLAGS = ['all45_commands_zero_relative_sites_zero_predicates_verified', 'all33_active_speech_targets_preserved',
         'all12_leaves_two_resources_pause_A000_C200_and_both_ends_exact',
         'both_consecutive_declared_endwords_preserved', 'no_FE_consumers_and_FI1_FO1_preserved',
         'no_source2100_4100_or_dynamic_objects', 'representative_shared_rules_approved', 'source_packed_semantics_not_inferred']
OFFLINE = []
''')
    section("    amendment = load(doc['source_effect_operand_notation_amendment'])", "    require(len(native['cases'])", '''    repeat = load(doc['focused_repeat_proof'])
    require(mapping['source_A000_hex'] == '00a0ffff19100120' and mapping['source_A000_raw_hex_words'] == ['1019', '2001']
            and mapping['source_packed_semantics_not_inferred'], 'source A000 raw command required')
    require(repeat['paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal']
            and repeat['cross_language_command_order_results_and_first_end_equal']
            and len(repeat['cross_language_speech_timing_differences']) == 22
            and not any(repeat['same_ROM_later_differing_frames'].values())
            and all(all(case['component_equality'].values()) for case in repeat['paired_native_persistent_state_and_PRNG_samples'] if case['frame'] <= 16090),
            'explicit post-scene state and later PRNG scope required')
''')
    section("    require(len(controls['relocated_dispatch_cases'])", "    require(sample['actual_two_disclosed", '''    require(len(controls['relocated_dispatch_cases']) == 33 and not controls['relocated_predicate_pairs']
            and len(controls['all12_source_current_target_nonrelative_nonspeech_leaves']) == 12
            and controls['all33_progressive_consumers_FI1_FO1_exact']
            and len(controls['relocated_C200_pairs']) == 1 and controls['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
            and controls['source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime']
            and controls['source_other_presentation_structural_results_reused_only_by_exact_whole_commands_and_runtime']
            and controls['source_A000_hex'] == '00a0ffff19100120'
            and controls['both_consecutive_endwords_and_one_pause_preserved']
            and controls['no_source_relative_sites_or_membership_predicates']
            and controls['later_older_record0D_reaudit_stays_open'], 'complete relocated source controls required')
    require(ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4
            and ends['B170_first_end_precedes_second_end_and_declared_logical_end']
            and ends['second_B170_declared_word_decoder_probe_not_actual_reachability_claim']
            and ends['no_relative_destination_at_or_beyond_logical_end'], 'four guarded end decodes required')
    require(names['source_19_selector_is_Yifa25_not_text_to_strip'] and names['source_printed_Ifa_maps_to_approved_Yifa_spelling']
            and names['surname_not_added_to_source_spoken_introduction'] and names['source_onesan_address_does_not_establish_kinship']
            and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names'] == {'2': 'Lil', '25': 'Yifa'}
            and names['progressive_nameplate_values'] == names['full_catalogue_values'] == {'2': 'Lil Argot', '25': 'Yifa Sol'}, 'source-owned identities required')
    name_cases = names['native_four_consumer_cases']['rows']
    require(len(name_cases) == 4 and {case['actor_ID'] for case in name_cases} == SELECTORS
            and all(case['all_actor_models_and_unowned4MiB_exact'] and case['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for case in name_cases), 'complete original name paths required')
    require(all(case['original_scratch_rings'] and case['original_getter_writes'] for case in name_cases), 'all four owned scratch paths required')
''')
    section("    require(sample['actual_two_disclosed", "    require(len(native['review_sheets'])", '''    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['two_additional_focused_repeats_postscene_state_and_PRNG_checked']
            and sample['new_emulator_runs'] == 4
            and sample['actual33_progressive_panels_figure_pause_resources_A000_C200_first_end_and_normal_town_return_pass']
            and sample['no_open_translation_specific_display_or_control_finding']
            and sample['original45_commands_and_both_declared_endwords_preserved'] and sample['no_B170_source_command_omitted']
            and sample['first_end1852_actual_second1856_native_decoder_only']
            and sample['original_B22_four_A000_initialization_commands_retained']
            and sample['later67_SeaView_differences_preserved_with_explicit_inference_and_state_scope']
            and sample['source_A000_packed_semantics_or_earned_recruitment_not_inferred']
            and sample['actual_selected_B170_source_events'] == [] and sample['offline_only_display_IDs'] == [], 'representative actual approval required')
    actual_paths = [path for path in sample['evidence'] if path.endswith('actual_all33_pause_resources_A000_C200_and_first_end.json')]
    require(len(actual_paths) == 1, 'one exact actual proof required')
    actual = load(actual_paths[0])
    require(sha(Path(actual_paths[0]).read_bytes()) == sample['evidence'][actual_paths[0]] and not actual['failures']
            and not actual['paired_region_differences'] and len(actual['versions']) == 2
            and {version['case'] for version in actual['versions']} == {'clean_Japanese', 'reviewed_English'}
            and actual['complete_matching_observations'] == actual['fresh_actual_unique_speech_panels'] == 33, 'two complete actual paths required')
    require(all(version['frames'] == 20001 and version['source_first_end_offset'] == 1852 and version['fixture_exit_frame'] == 11257
                and len(version['selected_B22_command_pairs']) == 53 and version['selected_B22_command_pairs'][-1]['result_words'] == [0, 0]
                and version['actual_source_A000_hex1019_2001']['original_source_offset'] == 1842
                and version['actual_source_A000_hex1019_2001']['result_words'] == [3, 0]
                and version['actual_C200']['original_source_offset'] == 1850 and version['actual_C200']['result_words'] == [3, 0]
                and [(p['start'], p['returned']) for p in version['actual_pause_and_resume']] == [(3200, 3332), (3332, 3576)]
                and version['second_source_end1856_stored_and_decoded_offline_not_actually_reached'] for version in actual['versions']), 'actual pause/control/effect/termination results differ')
''')
    section("    require([command['old_offset'] for command in stops]", "    restored = bytearray(logical)", '''    require([command['old_offset'] for command in stops] == [1852, 1856] and len(stops) == 2
            and stops[0]['new_offset'] + 4 == stops[1]['new_offset'] and stops[-1]['new_offset'] + 4 == len(logical)
            and all(target[command['new_offset']:command['new_offset'] + 4] == bytes(4) for command in stops), 'both source ends differ')
    require([(command['old_offset'], command['new_offset'], 4) for command in stops]
            == [(item['source_offset'], item['target_offset'], item['extent']) for item in spec['original_declared_end_word_maps']], 'end map differs')
    require(sum(command['word'] == 0xA000 for command in commands) == 1
            and next(command['old_offset'] for command in commands if command['word'] == 0xA000) == 1842
            and block[1842:1850] == target[mapped(1842):mapped(1850)] == bytes.fromhex('00a0ffff19100120')
            and sum(command['word'] == 0xC200 for command in commands) == 1
            and next(command['old_offset'] for command in commands if command['word'] == 0xC200) == 1850
            and sum(command['word'] == 0x2000 for command in commands) == 1
            and block[36:38] == target[mapped(36):mapped(38)] == bytes.fromhex('0020')
            and mapped(36) == 32 and mapped(38) == 34
            and sum(command['word'] == 0x8000 for command in commands) == 0
            and [command['word'] for command in commands if command['word'] & 0xFF00 == 0x6300] == [0x6342, 0x632D], 'effect/pause/C200/predicates/resource scope differs')
''')
    changes = {
        'B169': 'B170', 'lil_B169': 'lil_B170',
        'all36_five_review_gates_true': 'all33_five_review_gates_true',
        "'source_effect_operand_notation_amendment']": "'focused_repeat_proof']",
        "len(native['cases']) == 36": "len(native['cases']) == 33",
        "native['current_original_macro_alignment_calls'] == 288": "native['current_original_macro_alignment_calls'] == 264",
        'all36_current_native_speech_planes_pass': 'all33_current_native_speech_planes_pass',
        "native['progressive_planes'] == 36": "native['progressive_planes'] == 33",
        "('source_consumer_negative_controls', 21)": "('source_consumer_negative_controls', 13)",
        "len(stored['final_target_parity_cases']) == 36": "len(stored['final_target_parity_cases']) == 33",
        "stored['current_final_stored_macro_alignment_cases'] == 144": "stored['current_final_stored_macro_alignment_cases'] == 132",
        'all36_final_targets_complete_native_planes_equal_reviewed_planes': 'all33_final_targets_complete_native_planes_equal_reviewed_planes',
        "== 36 and {row['source_selector']": "== 33 and {row['source_selector']",
        "{'progressive': 36}": "{'progressive': 33}",
        "{'revise': 19, 'retain-wording': 17}": "{'revise': 21, 'retain-wording': 12}",
        '36 exact speech records required': '33 exact speech records required',
        "len(sample['represented_reviewed_display_IDs']) == 36": "len(sample['represented_reviewed_display_IDs']) == 33",
        '== 169': '== 170', '[169]': '[170]', 'block=169': 'block=170',
        "len({case['id'] for case in controls['relocated_dispatch_cases']}) == 36": "len({case['id'] for case in controls['relocated_dispatch_cases']}) == 33",
        "{b'FI': 5, b'FO': 2}": "{b'FI': 1, b'FO': 1}",
        "and not spec['original2000_pause_and_resume_maps']": "and spec['original2000_pause_and_resume_maps'] == [dict(old_offset=36, new_offset=32, source_resume=38, target_resume=34, source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]",
        "len(edges) == 12 and len(spec['target_native_skip_cases']) == 60": "not edges and not spec['target_native_skip_cases']",
        'len(commands) == 53': 'len(commands) == 45',
        "for command in commands) == 36": "for command in commands) == 33",
        'relative_operands=12, source_commands=53': 'relative_operands=0, source_commands=45',
        'all36_progressive_speeches_macros_twelve_spans_and5_leaves_preserved': 'all33_progressive_speeches_macros_pause_resources_A000_C200_and12_leaves_preserved',
        'actual_two_retained_B22_fixtures_not_natural_source_activation': 'actual_two_retained_B22_fixtures_plus_two_state_repeats_not_natural_source_activation',
    }
    for key in changes:
        assert key in text, key
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)), lambda m: changes[m.group()], text)
    assert 'B169' not in text and 'lil_B169' not in text
    assert 'source_effect_operand_notation_amendment' not in text
    assert not [node for node in ast.walk(ast.parse(text)) if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Tuple)]
    compile(text, str(NEW), 'exec')
    NEW.write_text(text, encoding='utf-8', newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(previous=str(OLD), previous_sha256=sha(OLD.read_bytes()), successor=str(NEW), successor_sha256=sha(NEW.read_bytes()),
        scope=dict(speeches=33, commands=45, relative_sites=0, predicates=0, leaves=12, pause=1, A000=1, C200=1, declared_ends=2, FI=1, FO=1),
        positive_and_negative_execution_pending=True, no_tuple_subscript_keys=True, no_registry_ROM_orcredit_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Atomic B170 compiler prepared;33 speeches,45 commands,pause/resources/A000/C200/both ends and focused state scope required.')
