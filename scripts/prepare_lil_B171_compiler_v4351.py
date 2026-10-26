"""Derive atomic B171 compilation with source-owned transition and no-pause contracts."""
import ast
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_compiler_tools_v4351')
OLD=Path('dk4tool/patch/lil_B170_editorial_v1.py')
NEW=Path('dk4tool/patch/lil_B171_editorial_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    def section(start,stop,value):
        global text
        a=text.index(start);b=text.index(stop,a)
        text=text[:a]+value+text[b:]
    section('SELECTORS = ','\n\ndef load', '''SELECTORS = {2, 25, 81}
FLAGS = ['all45_commands_zero_relative_sites_zero_predicates_verified', 'all37_active_speech_targets_preserved',
         'all8_leaves_four_presentations_one_resource_C200_and_both_ends_exact',
         'both_consecutive_declared_endwords_preserved', 'no_FE_consumers_and_FI1_FO0_preserved',
         'no_source2100_4100_or_dynamic_objects', 'no_source_A000_or2000_pause', 'representative_shared_rules_approved']
OFFLINE = []
''')
    section("    require(mapping['source_A000_hex']", "    require(len(native['cases'])", '''    timing = repeat['cross_language_command_timing_differences']
    require(Counter(case['source']['word'] for case in timing) == {0x4000: 17, 0x4621: 1, 0x61FF: 1, 0x6325: 1, 0xC200: 1, 0: 1},
            'exact17 speech/five control-end timing distinction required')
    require(repeat['paired_town11770_whole1A04_actor_models_and_captain2_equal']
            and repeat['cross_language_command_order_results_and_first_end_word_equal']
            and repeat['cross_language_exit_frames'] == [11737, 11735]
            and repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
            and all(all(case['component_equality'].values()) for case in repeat['paired_native_persistent_state_and_PRNG_samples'] if case['frame'] <= 16450),
            'explicit post-scene state and later PRNG scope required')
''')
    section("    require(len(controls['relocated_dispatch_cases'])", "    require(sample['actual_two_disclosed", '''    require(len(controls['relocated_dispatch_cases']) == 37 and not controls['relocated_predicate_pairs']
            and len(controls['all8_source_current_target_nonrelative_nonspeech_leaves']) == 8
            and controls['all37_progressive_consumers_FI1_FO0_exact']
            and len(controls['relocated_C200_pairs']) == 1 and controls['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
            and controls['source_resource10_boundary_cases_reused_only_by_exact_word_and_runtime']
            and controls['source_four_presentation_structural_results_reused_only_by_exact_whole_commands_and_runtime']
            and controls['both_consecutive_endwords_and_no_source_pause_or_A000_preserved']
            and controls['no_source_relative_sites_or_membership_predicates']
            and controls['later_older_record0D_reaudit_stays_open'], 'complete relocated source controls required')
    require(ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4
            and ends['B171_first_end_precedes_second_end_and_declared_logical_end']
            and ends['second_B171_declared_word_decoder_probe_not_actual_reachability_claim']
            and ends['no_relative_destination_at_or_beyond_logical_end'], 'four guarded end decodes required')
    require(names['source_19_selector_is_Yifa25_not_text_to_strip'] and names['source_printed_Ifa_maps_to_approved_Yifa_spelling']
            and names['surname_not_added_to_source_spoken_introduction']
            and names['source_anideshi_and_sibling_simile_do_not_establish_biological_kinship']
            and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names'] == {'2': 'Lil', '25': 'Yifa', '81': 'Sanghyeon'}
            and names['progressive_nameplate_values'] == names['full_catalogue_values'] == {'2': 'Lil Argot', '25': 'Yifa Sol', '81': 'Sanghyeon Kan'}, 'source-owned identities required')
    name_cases = names['native_six_consumer_cases']['rows']
    require(len(name_cases) == 6 and {case['actor_ID'] for case in name_cases} == SELECTORS
            and all(case['all_actor_models_and_unowned4MiB_exact'] and case['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for case in name_cases), 'complete original name paths required')
    require(all(case['original_scratch_rings'] and case['original_getter_writes'] for case in name_cases), 'all six owned scratch paths required')
''')
    section("    require(sample['actual_two_disclosed", "    require(len(native['review_sheets'])", '''    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['two_additional_focused_repeats_postscene_state_and_PRNG_checked']
            and sample['new_emulator_runs'] == 4
            and sample['actual37_progressive_panels_dream_morning_resource_C200_first_end_and_normal_town_return_pass']
            and sample['no_open_translation_specific_display_or_control_finding']
            and sample['original45_commands_and_both_declared_endwords_preserved'] and sample['no_B171_source_command_omitted']
            and sample['first_end2112_actual_second2116_native_decoder_only']
            and sample['original_B22_four_A000_initialization_commands_retained'] and sample['no_source_A000_or_pause_invented']
            and sample['later59_sailing_differences_preserved_with_explicit_inference_and_state_scope']
            and sample['no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim']
            and sample['actual_selected_B171_source_events'] == [] and sample['offline_only_display_IDs'] == [], 'representative actual approval required')
    actual_paths = [path for path in sample['evidence'] if path.endswith('actual_all37_dream_morning_presentations_resource_C200_and_first_end.json')]
    require(len(actual_paths) == 1, 'one exact actual proof required')
    actual = load(actual_paths[0])
    require(sha(Path(actual_paths[0]).read_bytes()) == sample['evidence'][actual_paths[0]] and not actual['failures']
            and not actual['paired_region_differences'] and len(actual['versions']) == 2
            and {version['case'] for version in actual['versions']} == {'clean_Japanese', 'reviewed_English'}
            and actual['complete_matching_observations'] == actual['fresh_actual_unique_speech_panels'] == 37, 'two complete actual paths required')
    require([version['fixture_exit_frame'] for version in actual['versions']] == [11737, 11735], 'source/English exits differ from observed pair')
    require(all(version['frames'] == 20001 and version['source_first_end_offset'] == 2112
                and len(version['selected_B22_command_pairs']) == 53 and version['selected_B22_command_pairs'][-1]['result_words'] == [0, 0]
                and version['actual_C200']['original_source_offset'] == 2110 and version['actual_C200']['result_words'] == [3, 0]
                and [r['word'] for r in version['actual_presentation_commands']] == [0x6000, 0x4500, 0x4621, 0x61FF]
                and [r['word'] for r in version['actual_resources']] == [0x6325]
                and version['second_source_end2116_stored_and_decoded_offline_not_actually_reached'] for version in actual['versions']), 'actual presentation/resource/C200/termination results differ')
''')
    section("    require(sum(command['word'] == 0xA000", "    restored = bytearray(logical)", '''    leaves = [command for command in commands if command['word'] != 0x4000]
    require([command['word'] for command in leaves] == [0x6000, 0x4500, 0x4621, 0x61FF, 0x6325, 0xC200, 0, 0]
            and [command['old_offset'] for command in leaves] == [8, 10, 1252, 1256, 1306, 2110, 2112, 2116]
            and all(command['word'] not in [0xA000, 0x2000, 0x8000] for command in commands), 'presentation/resource/C200/no-pause scope differs')
    require([(command['old_offset'], block[command['old_offset']:command['old_offset'] + command['old_native_extent']].hex()) for command in leaves]
            == [(8, '0060'), (10, '004500000021'), (1252, '21467e80'), (1256, 'ff61'), (1306, '2563'), (2110, '00c2'), (2112, '00000000'), (2116, '00000000')], 'eight complete source leaves differ')
''')
    changes={
        'B170':'B171','lil_B170':'lil_B171','lil_B170_layout_v2':'lil_B171_layout_v1',
        'all33_five_review_gates_true':'all37_five_review_gates_true',
        "len(native['cases']) == 33":"len(native['cases']) == 37",
        "native['current_original_macro_alignment_calls'] == 264":"native['current_original_macro_alignment_calls'] == 296",
        'all33_current_native_speech_planes_pass':'all37_current_native_speech_planes_pass',
        "native['progressive_planes'] == 33":"native['progressive_planes'] == 37",
        "('source_consumer_negative_controls', 13)":"('source_consumer_negative_controls', 15)",
        "('source_macro_preservation_negatives', 2)":"('source_macro_preservation_negatives', 1)",
        "len(stored['final_target_parity_cases']) == 33":"len(stored['final_target_parity_cases']) == 37",
        "stored['current_final_stored_macro_alignment_cases'] == 132":"stored['current_final_stored_macro_alignment_cases'] == 148",
        'all33_final_targets_complete_native_planes_equal_reviewed_planes':'all37_final_targets_complete_native_planes_equal_reviewed_planes',
        "len(sample['viewed_actual_sheets']) == 6":"len(sample['viewed_actual_sheets']) == 7",
        "== 33 and {row['source_selector']":"== 37 and {row['source_selector']",
        "{'progressive': 33}":"{'progressive': 37}",
        "{'revise': 21, 'retain-wording': 12}":"{'revise': 24, 'retain-wording': 13}",
        '33 exact speech records required':'37 exact speech records required',
        "len(sample['represented_reviewed_display_IDs']) == 33":"len(sample['represented_reviewed_display_IDs']) == 37",
        '== 170':'== 171','[170]':'[171]','block=170':'block=171',
        "len({case['id'] for case in controls['relocated_dispatch_cases']}) == 33":"len({case['id'] for case in controls['relocated_dispatch_cases']}) == 37",
        "{b'FI': 1, b'FO': 1}":"{b'FI': 1}",
        "and spec['original2000_pause_and_resume_maps'] == [dict(old_offset=36, new_offset=32, source_resume=38, target_resume=34, source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]":"and not spec['original2000_pause_and_resume_maps']",
        "for command in commands) == 33":"for command in commands) == 37",
        '[1852, 1856]':'[2112, 2116]',
        'all33_progressive_speeches_macros_pause_resources_A000_C200_and12_leaves_preserved':'all37_progressive_speeches_macros_presentations_resource_C200_and8_leaves_preserved',
        "        require(mapped(a) == b":"        require(command['word'] == struct.unpack_from('<H', block, a)[0] == struct.unpack_from('<H', target, b)[0], 'mapped opcode differs')\n        require(mapped(a) == b",
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    assert 'B170' not in text and 'lil_B170' not in text
    assert not [n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Tuple)]
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        scope=dict(speeches=37,commands=45,relative_sites=0,predicates=0,leaves=8,pause=0,A000=0,C200=1,declared_ends=2,FI=1,FO=0),
        timing_split17_speeches_five_control_end_commands=True,positive_and_negative_execution_pending=True,
        no_registry_ROM_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Atomic B171 compiler prepared:37 speeches,45 commands,eight exact leaves,no pause/A000,C200 and both ends;17/5 timing split bound.')
