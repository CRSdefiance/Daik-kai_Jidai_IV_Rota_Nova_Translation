"""Derive a B170 full-plane audit with explicit linear/pause/C200/end contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_actual_tools_v4293')

if __name__ == '__main__':
    assert not ROOT.exists()
    old = Path('scripts/audit_lil_B169_actual_v4244.py').read_text(encoding='utf-8')
    start = old.index('        selected = [row for row in pairs')
    stop = old.index('        for pending in trace', start)
    old_flow = old[start:stop]
    new_flow = '''        selected = [row for row in pairs if row['block'] == 22]
        assert len(intervals) == len({row['id'] for row in intervals}) == 33
        assert not any(row['word'] in [0x8000, 0x100, 0x200, 0x300, 0x400] for row in selected)
        native = {row['offset']: row for row in fixture['all54_stored_fixture_commands']}
        cursor, expected = 8, []
        while True:
            command = native[cursor]
            expected.append(cursor)
            if command['word'] == 0:
                break
            cursor += command['native_extent']
        assert len(expected) == 53 and [row['offset'] for row in selected] == expected
        assert selected[-1]['word'] == 0 and selected[-1]['original_source_offset'] == 1852
        assert sum(row['word'] == 0xA000 for row in selected) == 5
        effects = [row for row in selected if row.get('original_source_block') == 170 and row['word'] == 0xA000]
        assert len(effects) == 1 and effects[0]['original_source_offset'] == 1842
        assert commands[effects[0]['offset']]['whole_command_hex'] == '00a0ffff19100120'
        c200 = [row for row in selected if row['word'] == 0xC200]
        assert len(c200) == 1 and c200[0]['original_source_offset'] == 1850
        pauses = [row for row in selected if row['word'] == 0x2000]
        assert len(pauses) == 1 and pauses[0]['original_source_offset'] == 36 and pauses[0]['extent'] == 2
        pause_index = selected.index(pauses[0])
        assert selected[pause_index + 1]['original_source_offset'] == 38
        assert selected[pause_index + 1]['start'] >= pauses[0]['returned']
        resources = [row['word'] for row in selected if row.get('original_source_block') == 170 and row['word'] & 0xFF00 == 0x6300]
        assert resources == [0x6342, 0x632D]
        presentations = [row for row in selected if row.get('original_source_block') == 170 and row['word'] in [0x6000, 0x4621, 0x0505, 0x050A, 0x6242]]
        assert [row['word'] for row in presentations] == [0x6000, 0x4621, 0x0505, 0x050A, 0x6242]
        assert sum(row['prefix'] == 254 for row in intervals) == 0
        final_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B170_R0125')
        assert final_speech['returned'] <= effects[0]['start'] <= effects[0]['returned'] <= c200[0]['start'] <= c200[0]['returned'] <= selected[-1]['start']
'''
    start = old.index('        versions.append(dict(')
    stop = old.index('        photosets[case]', start)
    old_version = old[start:stop]
    new_version = '''        versions.append(dict(case=case, source_block=170, ROM_sha256=report['ROM_sha256'], frames=20001,
            input_schedule=rp['original_inputs'], input_schedule_sha256=rp['inputs_sha256'],
            capture_report=str(paths[2]), observer_report=str(paths[3]), selected_B22_command_pairs=selected,
            selected_intervals=intervals, actual_source_A000_hex1019_2001=effects[0],
            actual_C200=c200[0], actual_pause_and_resume=[pauses[0], selected[pause_index + 1]],
            actual_resources=resources, actual_presentation_commands=presentations,
            fixture_exit_frame=selected[-1]['returned'], source_first_end_offset=1852,
            second_source_end1856_stored_and_decoded_offline_not_actually_reached=True,
            following_observed_blocks=sorted({row['block'] for row in pairs if row['block'] != 22}),
            all_retained_linear_control_flow_matches_original_commands=True,
            all33_speeches_resources_presentations_pause_effect_C200_and_first_end_observed=True))
'''
    start = old.index("    save(ROOT / 'actual_progressive_three_predicates_full_effect_and_return.json'")
    old_output = old[start:]
    new_output = '''    save(ROOT / 'actual_all33_pause_resources_A000_C200_and_first_end.json', dict(versions=versions,
        actual_panels=actual, fresh_actual_unique_speech_panels=len(actual), complete_matching_observations=sum(bool(row['holds']) for row in actual),
        offline_only_display_IDs=offline, failures=failures, paired_region_differences=region_differences,
        review_sheets=sheets, visual_review_pending=True, actual_new_cold_boot_runs=2,
        selected_command_counts={format(word, '04X'): count for word, count in counts.items()},
        all45_source_commands_and_both_stored_ends_preserved=True,
        all33_linear_progressive_speeches_observed=True,
        source_A000_hex1019_2001_after_final_encouragement_before_C200_and_first_end=True,
        source_A000_raw_words_recorded_without_packed_semantic_inference=True,
        actual_source_event170_not_selected=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_and_all_B170_commands_preserved=True,
        first_source_end1852_actually_reached_and_decoded_second1856_offline_only=True,
        evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    assert not failures, failures
    print(dict(actual_panels=len(actual), matching=sum(bool(row['holds']) for row in actual), offline_only=offline,
        exits=[(version['case'], version['fixture_exit_frame']) for version in versions],
        command_pairs=[len(version['selected_B22_command_pairs']) for version in versions],
        sheets=len(sheets), visual_review_pending=True))
'''
    tool = derive('scripts/audit_lil_B169_actual_v4244.py', 'scripts/audit_lil_B170_actual_v4293.py', {
        old_flow: new_flow, old_version: new_version, old_output: new_output,
        'B169': 'B170', 'lil_B169': 'lil_B170', 'actual_v4244': 'actual_v4293',
        'display_fixture_v4241': 'display_fixture_v4291',
        'native_approval_v4230/all36_native_progressive_and_source_reconciliation': 'native_approval_v4278/all33_native_progressive_and_source_reconciliation',
        'display_run_v4242': 'display_run_v4292', 'display_v4242': 'display_v4292',
        "source_event169_not_selected": "source_event170_not_selected",
        "assert source['block'] != 169": "assert source['block'] != 170",
        'original_source_block=169': 'original_source_block=170',
        'len(actual) + len(offline) == 36': 'len(actual) + len(offline) == 33',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool, source_speeches=33,
        source_commands=45, stored_fixture_commands=54, expected_observed_until_first_end=53,
        no_predicates_or_relative_sites=True, original_later_A000_hex='00a0ffff19100120',
        no_natural_eligibility_earned_flag_or_full_route_claim=True, full_goal_complete=False))
    print('Prepared B170 actual-plane audit:33 speeches,original pause/resources/effect/C200 and first declared end.')
