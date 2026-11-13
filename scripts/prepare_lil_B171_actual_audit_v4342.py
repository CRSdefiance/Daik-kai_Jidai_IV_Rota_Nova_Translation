"""Derive full-plane B171 audit with explicit dream/morning, C200 and end contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_actual_tools_v4342')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/audit_lil_B170_actual_v4293.py').read_text(encoding='utf-8')
    start=old.index('        selected = [row for row in pairs')
    stop=old.index('        for pending in trace',start)
    old_flow=old[start:stop]
    new_flow='''        selected = [row for row in pairs if row['block'] == 22]
        assert len(intervals) == len({row['id'] for row in intervals}) == 37
        assert not any(row['word'] in [0x8000, 0x100, 0x200, 0x300, 0x400, 0x2000] for row in selected)
        native = {row['offset']: row for row in fixture['all54_stored_fixture_commands']}
        cursor, expected = 8, []
        while True:
            command = native[cursor]
            expected.append(cursor)
            if command['word'] == 0:
                break
            cursor += command['native_extent']
        assert len(expected) == 53 and [row['offset'] for row in selected] == expected
        assert selected[-1]['word'] == 0 and selected[-1]['original_source_offset'] == 2112
        assert sum(row['word'] == 0xA000 for row in selected) == 4
        assert not any(row['word'] == 0xA000 and row.get('original_source_block') == 171 for row in selected)
        c200 = [row for row in selected if row['word'] == 0xC200]
        assert len(c200) == 1 and c200[0]['original_source_offset'] == 2110
        resources = [row for row in selected if row.get('original_source_block') == 171 and row['word'] & 0xFF00 == 0x6300]
        assert [row['word'] for row in resources] == [0x6325]
        presentations = [row for row in selected if row.get('original_source_block') == 171 and row['word'] in [0x6000, 0x4500, 0x4621, 0x61FF]]
        assert [row['word'] for row in presentations] == [0x6000, 0x4500, 0x4621, 0x61FF]
        assert [row['original_source_offset'] for row in presentations] == [8, 10, 1252, 1256]
        assert sum(row['prefix'] == 254 for row in intervals) == 0
        final_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B171_R0140')
        dream_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B171_R0074')
        wake_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B171_R0077')
        morning_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B171_R0080')
        assert dream_speech['returned'] <= presentations[2]['start'] <= presentations[2]['returned'] <= presentations[3]['start'] <= presentations[3]['returned'] <= wake_speech['start']
        assert wake_speech['returned'] <= resources[0]['start'] <= resources[0]['returned'] <= morning_speech['start']
        assert final_speech['returned'] <= c200[0]['start'] <= c200[0]['returned'] <= selected[-1]['start']
'''
    start=old.index('        versions.append(dict(')
    stop=old.index('        photosets[case]',start)
    old_version=old[start:stop]
    new_version='''        versions.append(dict(case=case, source_block=171, ROM_sha256=report['ROM_sha256'], frames=20001,
            input_schedule=rp['original_inputs'], input_schedule_sha256=rp['inputs_sha256'],
            capture_report=str(paths[2]), observer_report=str(paths[3]), selected_B22_command_pairs=selected,
            selected_intervals=intervals, actual_C200=c200[0], actual_resources=resources,
            actual_presentation_commands=presentations,
            dream_to_waking_interval=[dream_speech, presentations[2], presentations[3], wake_speech],
            waking_to_morning_interval=[wake_speech, resources[0], morning_speech],
            fixture_exit_frame=selected[-1]['returned'], source_first_end_offset=2112,
            second_source_end2116_stored_and_decoded_offline_not_actually_reached=True,
            following_observed_blocks=sorted({row['block'] for row in pairs if row['block'] != 22}),
            all_retained_linear_control_flow_matches_original_commands=True,
            all37_speeches_presentations_resource_C200_and_first_end_observed=True))
'''
    start=old.index("    save(ROOT / 'actual_all33_pause_resources_A000_C200_and_first_end.json'")
    old_output=old[start:]
    new_output='''    save(ROOT / 'actual_all37_dream_morning_presentations_resource_C200_and_first_end.json', dict(versions=versions,
        actual_panels=actual, fresh_actual_unique_speech_panels=len(actual), complete_matching_observations=sum(bool(row['holds']) for row in actual),
        offline_only_display_IDs=offline, failures=failures, paired_region_differences=region_differences,
        review_sheets=sheets, visual_review_pending=True, actual_new_cold_boot_runs=2,
        selected_command_counts={format(word, '04X'): count for word, count in counts.items()},
        all45_source_commands_and_both_stored_ends_preserved=True,
        all37_linear_progressive_speeches_observed=True,
        original4500_4621_61FF_6325_transitions_and_final_C200_executed=True,
        source_presentation_resource_results_recorded_without_semantic_inference=True,
        actual_source_event171_not_selected=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_and_all_B171_commands_preserved=True,
        first_source_end2112_actually_reached_and_decoded_second2116_offline_only=True,
        evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    assert not failures, failures
    print(dict(actual_panels=len(actual), matching=sum(bool(row['holds']) for row in actual), offline_only=offline,
        exits=[(version['case'], version['fixture_exit_frame']) for version in versions],
        command_pairs=[len(version['selected_B22_command_pairs']) for version in versions],
        sheets=len(sheets), visual_review_pending=True))
'''
    tool=derive('scripts/audit_lil_B170_actual_v4293.py','scripts/audit_lil_B171_actual_v4342.py',{
        old_flow:new_flow,old_version:new_version,old_output:new_output,
        'B170':'B171','lil_B170':'lil_B171','actual_v4293':'actual_v4342',
        'display_fixture_v4291':'display_fixture_v4340',
        'native_approval_v4278/all33_native_progressive_and_source_reconciliation':'native_approval_v4328/all37_native_progressive_and_source_reconciliation',
        'display_run_v4292':'display_run_v4341','display_v4292':'display_v4341',
        'source_event170_not_selected':'source_event171_not_selected',
        'all_source_commands_and_later_A000_retained':'all_source_commands_presentations_resource_and_C200_retained',
        "assert source['block'] != 170":"assert source['block'] != 171",
        'original_source_block=170':'original_source_block=171',
        'len(actual) + len(offline) == 33':'len(actual) + len(offline) == 37',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_speeches=37,source_commands=45,
        stored_fixture_commands=54,expected_observed_until_first_end=53,no_predicates_or_relative_sites=True,
        source_A000=0,source_pause=0,source_end_offsets=[2112,2116],
        no_natural_eligibility_earned_flag_or_full_route_claim=True,full_goal_complete=False))
    print('Prepared B171 full-plane audit:37 speeches,original dream/morning transitions,resource,C200 and first end.')
