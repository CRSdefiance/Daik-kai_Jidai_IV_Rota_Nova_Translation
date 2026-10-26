"""Prepare B170-specific atomic rejection cases and cumulative registration."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_registration_tools_v4302')
NEW = Path('scripts/register_lil_B170_v4302.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    old = Path('scripts/register_lil_B169_v4250b.py')
    text = old.read_text(encoding='utf-8')
    def section(start, stop, value):
        global text
        a, b = text.index(start), text.index(stop, text.index(start))
        text = text[:a] + value + text[b:]
    section('    mutations = [', '    for macro in', '''    mutations = [
        ('missing_gate', 'manuscript', lambda value: value['records'][0]['review'].update(source=False)),
        ('missing_speech', 'manuscript', lambda value: value['records'].pop()),
        ('wrong_source', 'manuscript', lambda value: value['records'][0]['source_reference'].update(offset=1)),
        ('wrong_current', 'manuscript', lambda value: value['records'][0]['current_reference'].update(offset=1)),
        ('wrong_selector', 'manuscript', lambda value: value['records'][0].update(english='{SPEAKER:19}Hello.')),
        ('Yifa_selector_as_text', 'manuscript', lambda value: value['records'][1].update(english='Yifa says hello.')),
        ('manual_break', 'manuscript', lambda value: value['records'][0].update(english=value['records'][0]['english'] + '{LB}')),
        ('manual_padding', 'manuscript', lambda value: value['records'][0].update(english=value['records'][0]['english'] + '{PAD}')),
        ('invented_relative', 'reference_map', lambda value: value['blocks'][0]['relative_skip_fixups'].append({})),
        ('missing_pause', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'].pop()),
        ('wrong_pause_resume', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'][0].update(target_resume=36)),
        ('missing_end', 'reference_map', lambda value: value['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong_end', 'reference_map', lambda value: value['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=0)),
        ('wrong_entry', 'reference_map', lambda value: value.update(entry_point_offset=10)),
        ('invented_choice', 'reference_map', lambda value: value['blocks'][0]['choice_commands'].append({})),
        ('wrong_command', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_A000_raw_word', 'reference_map', lambda value: value.update(source_A000_raw_hex_words=['0029', '0001'])),
        ('missing_native_plane', 'native_font_proof', lambda value: value['cases'].pop()),
        ('lost_internal_glyph', 'native_font_proof', lambda value: value['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost_native_bounds', 'native_font_proof', lambda value: value['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('lost_macro_negative', 'native_font_proof', lambda value: value['source_macro_preservation_negatives'].pop()),
        ('lost_stored_plane', 'final_padding_proof', lambda value: value['final_target_parity_cases'].pop()),
        ('lost_dispatch', 'relocated_control_proof', lambda value: value['relocated_dispatch_cases'].pop()),
        ('invented_predicate', 'relocated_control_proof', lambda value: value['relocated_predicate_pairs'].append({})),
        ('lost_C200', 'relocated_control_proof', lambda value: value['relocated_C200_pairs'].pop()),
        ('wrong_C200_ownership', 'relocated_control_proof', lambda value: value.update(original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor=False)),
        ('wrong_resource_reuse', 'relocated_control_proof', lambda value: value.update(source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime=False)),
        ('lost_opaque_leaf', 'relocated_control_proof', lambda value: value['all12_source_current_target_nonrelative_nonspeech_leaves'].pop()),
        ('lost_name_path', 'source_nameplate_consumer_proof', lambda value: value['native_four_consumer_cases']['rows'].pop()),
        ('lost_owned_scratch', 'source_nameplate_consumer_proof', lambda value: value['native_four_consumer_cases']['rows'][0].update(original_scratch_rings=[])),
        ('lost_end_decode', 'termination_decode_proof', lambda value: value['cases'].pop()),
        ('post_payload_read', 'termination_decode_proof', lambda value: value.update(all4_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('false_actual_second_end', 'representative_proof', lambda value: value.update(first_end1852_actual_second1856_native_decoder_only=False)),
        ('omitted_effect', 'representative_proof', lambda value: value.update(no_B170_source_command_omitted=False)),
        ('invented_earned_effect', 'representative_proof', lambda value: value.update(source_A000_packed_semantics_or_earned_recruitment_not_inferred=False)),
        ('lost_later_difference_scope', 'representative_proof', lambda value: value.update(later67_SeaView_differences_preserved_with_explicit_inference_and_state_scope=False)),
        ('lost_repeat_actor_state', 'focused_repeat_proof', lambda value: value.update(paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal=False)),
        ('lost_repeat_component_state', 'focused_repeat_proof', lambda value: value['paired_native_persistent_state_and_PRNG_samples'][2]['component_equality'].update(models=False)),
        ('lost_timing_distinction', 'focused_repeat_proof', lambda value: value['cross_language_speech_timing_differences'].pop()),
    ]
''')
    section('    def changed_actual', "    mutations.extend(('map_'", '''    def changed_actual(value, label):
        old = next(path for path in value['evidence'] if path.endswith('actual_all33_pause_resources_A000_C200_and_first_end.json'))
        actual = read(old)
        if label == 'wrong_actual_effect':
            actual['versions'][0]['actual_source_A000_hex1019_2001']['result_words'] = [3, 1]
        elif label == 'wrong_actual_end':
            actual['versions'][0]['source_first_end_offset'] = 1856
        elif label == 'wrong_actual_C200':
            actual['versions'][0]['actual_C200']['result_words'] = [3, 1]
        elif label == 'wrong_actual_pause':
            actual['versions'][0]['actual_pause_and_resume'][0]['returned'] = 3333
        else:
            actual['versions'].pop()
        destination = ROOT / label / 'actual_all33_pause_resources_A000_C200_and_first_end.json'
        destination.parent.mkdir()
        save(destination, actual)
        value['evidence'].pop(old)
        value['evidence'][str(destination)] = sha(destination.read_bytes())
    mutations.extend((label, 'representative_proof', lambda value, label=label: changed_actual(value, label))
                     for label in ['wrong_actual_effect', 'wrong_actual_end', 'wrong_actual_C200', 'wrong_actual_pause', 'missing_actual_version'])
''')
    description = next(line for line in text.splitlines() if line.startswith("        description='Full V4204"))
    replacement = "        description='Full V4251 cumulative stack plus33 complete B170 Yifa collision/apology/Taoist-training/resolve/passage reviews:21 revisions/12 retentions,33 progressive speeches,45 commands,twelve leaves,pause,resources,later A000 hex1019/2001,C200 and both ends. Two complete-content boots cover all33 panels,first end and normal return;two focused repeats bind original state and later PRNG/timing scope. No natural eligibility,earned flag,full-route orhardware claim.', note='B170 source/native/reference/representative approved;registered build,exact patch and fresh startup pending.')"
    changes = {
        'lil_B169_editorial_v2': 'lil_B170_editorial_v1',
        'lil_B169_registration_v4250b': 'lil_B170_registration_v4302',
        "PROFILE = 'all-routes-unified-v4251'": "PROFILE = 'all-routes-unified-v4303'",
        'B169': 'B170', 'lil_B169': 'lil_B170',
        'all_routes_combined_v4204': 'all_routes_combined_v4251',
        'editorial_manuscript_v5': 'editorial_manuscript_v6',
        'reference_checkpoint_v4247': 'reference_checkpoint_v4299',
        'all-routes-unified-v4204': 'all-routes-unified-v4251',
        'reference_approval_v4246': 'reference_approval_v4298',
        'loader_v4237': 'loader_v4285',
        "deps.add(doc['source_effect_operand_notation_amendment'])": "deps.add(doc['focused_repeat_proof'])",
        'transition_review_v4245/all6_sheets_source_effect_and_paired_return_review': 'transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review',
        "len(proof['changed_records']) == 36": "len(proof['changed_records']) == 33",
        'the complete V4204 stack': 'the complete V4251 stack',
        'after_full_V4204_before_literal_percent_safety': 'after_full_V4251_before_literal_percent_safety',
        'build_integrated_release_v4250b.tmp': 'build_integrated_release_v4302.tmp',
        'expected_manifest_batches=545': 'expected_manifest_batches=546',
        'positive_records=36': 'positive_records=33', 'expected_batches=545': 'expected_batches=546',
        description: replacement,
    }
    for key in changes:
        assert key in text, key
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)), lambda m: changes[m.group()], text)
    # Bind diagnostic view/repeat evidence as dependencies as well as main views.
    anchor = "    deps.update(row['path'] for row in visual['English_full_screen_views'] + visual['Japanese_full_screen_views'])\n"
    assert anchor in text
    text = text.replace(anchor, anchor + "    deps.update(row['path'] for row in visual['later_diagnostic_full_screen_views'])\n")
    assert 'B169' not in text and 'lil_B169' not in text and 'source_effect_operand_notation_amendment' not in text
    compile(text, str(NEW), 'exec')
    NEW.write_text(text, encoding='utf-8', newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(previous=str(old), previous_sha256=sha(old.read_bytes()), successor=str(NEW), successor_sha256=sha(NEW.read_bytes()),
        compiler='dk4tool/patch/lil_B170_editorial_v1.py', current_main_remains='all-routes-unified-v4251', target_profile='all-routes-unified-v4303',
        no_relative_or_predicate_or_offline_remark_inherited=True, source_pause_C200_both_ends_and_later_state_scope_negatives_added=True,
        positive_negative_and_registration_execution_pending=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Prepared B170 atomic negatives and cumulative registration after full V4251;main remains V4251.')
