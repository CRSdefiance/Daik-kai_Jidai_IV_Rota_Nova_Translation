"""Audit complete retained B171 control flow and every actually selected progressive plane."""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_actual_v4342')
PLAN = Path('work/analysis/lil_B171_display_fixture_v4340/complete_effect_preserving_B22_fixtures.json')
FONT = Path('work/analysis/lil_B171_native_approval_v4328/all37_native_progressive_and_source_reconciliation.json')
CAPBASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


if __name__ == '__main__':
    assert not ROOT.exists()
    plan, font = read(PLAN), read(FONT)
    versions, photosets = [], {}
    evidence = {str(path): sha(path.read_bytes()) for path in [PLAN, FONT, Path(__file__)]}
    for fixture in plan['fixtures']:
        assert read(Path('work/analysis/lil_B171_display_run_v4341_' + fixture['case']) / 'terminal.json')['terminal']
    for fixture in plan['fixtures']:
        case = fixture['case']
        run = Path('work/analysis/lil_B171_display_run_v4341_' + case)
        cap = CAPBASE / ('lil_B171_display_v4341_' + case)
        paths = [run / 'terminal.json', run / 'run_plan.json', cap / 'capture_report.json', cap / 'observer/commands.json']
        terminal, rp, report, trace = map(read, paths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances'] == 1
        assert report['frames'] == 20001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(fixture['research_ROM']).read_bytes()) == fixture['research_ROM_sha256'] == report['ROM_sha256'] == rp['research_ROM_sha256']
        assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event171_not_selected'] and rp['all_source_commands_presentations_resource_and_C200_retained']
        assert sha(Path(rp['fixture_manifest']).read_bytes()) == rp['fixture_manifest_sha256'] == sha(PLAN.read_bytes())
        assert not trace['errors'] and trace['mismatches'] == 0 and trace['all_host_slots_restored_and_core_file_exact']
        assert all(not value for key, value in report.items() if key.startswith('synthetic_'))
        assert sha(Path(rp['original_inputs']).read_bytes()) == rp['inputs_sha256']
        blocks = IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks
        block = blocks[22]
        assert sha(block) == fixture['fixture_block_sha256']
        photos = {}
        for photo in report['frames_captured']:
            path = Path(photo['path'])
            assert sha(path.read_bytes()) == photo['PNG_sha256']
            picture = Image.open(path).convert('RGB')
            assert picture.size == (256, 384)
            photos[photo['frame']] = (photo, picture)
        snapshot = report['read_only_RAM_snapshot']
        assert snapshot['read_only_export'] and snapshot['bytes'] == 4194304
        assert sha(Path(snapshot['path']).read_bytes()) == snapshot['sha256']
        rows, pairs, intervals = trace['rows'], [], []
        by_at = {row['fixture_command_offset']: row for row in fixture['original_text_records']}
        commands = {row['fixture_offset']: row for row in fixture['selected_original_objects']}
        for row in rows:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            source = row['source']
            assert source['classification'] == 'original_SC_cache' and source['route'] == 2
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256'] == sha(blocks[source['block']])
            assert source['block'] != 171
            if row['kind'] != 'after_command':
                continue
            entry = rows[row['entry_row']]
            source = entry['source']
            at = source['instruction_offset']
            word = int.from_bytes(blocks[source['block']][at:at + 2], 'little')
            pair = dict(block=source['block'], offset=at, word=word, start=entry['frame'], returned=row['frame'],
                        extent=row['decoded_length'], result_words=row['result_words'])
            pairs.append(pair)
            if source['block'] != 22:
                continue
            if at in commands:
                assert word == commands[at]['source_word']
                pair.update(original_source_block=171, original_source_offset=commands[at]['source_offset'])
            if word == 0x4000:
                record = by_at[at]
                assert block[at:at + record['native_extent']].hex() == record['whole_command_hex']
                intervals.append(dict(id=record['id'], start=entry['frame'], returned=row['frame'], offset=at, prefix=record['source_selector']))
        selected = [row for row in pairs if row['block'] == 22]
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
        for pending in trace['unreturned_at_capture_end']:
            assert rows[pending['entry_row']]['source']['block'] != 22
        versions.append(dict(case=case, source_block=171, ROM_sha256=report['ROM_sha256'], frames=20001,
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
        photosets[case] = photos
        evidence.update({str(path): sha(path.read_bytes()) for path in paths})
    shape = lambda version: [(row.get('original_source_offset'), row['word'], row['result_words']) for row in version['selected_B22_command_pairs']]
    assert shape(versions[0]) == shape(versions[1])
    assert versions[0]['input_schedule_sha256'] == versions[1]['input_schedule_sha256']
    by_id = {row['id']: row for row in font['cases']}
    source_intervals = {row['id']: row for row in versions[0]['selected_intervals']}
    actual, panels, failures, region_differences = [], [], [], []
    for interval in versions[1]['selected_intervals']:
        case = by_id[interval['id']]
        preview = Image.open(case['preview']).convert('RGB')
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        assert preview.height == 64 and preview.width == 216
        ink0 = {(x, y) for y in range(64) for x in range(preview.width) if preview.getpixel((x, y)) == (0, 8, 0)}
        gray0 = {(x, y) for y in range(64) for x in range(preview.width) if preview.getpixel((x, y)) == (98, 97, 98)}
        source_interval = source_intervals[interval['id']]
        holds = []
        for frame, (photo, picture) in photosets['reviewed_English'].items():
            if not max(interval['start'], source_interval['start']) < frame < min(interval['returned'], source_interval['returned']):
                continue
            ink = {(x, y) for y in range(64) for x in range(preview.width) if picture.getpixel((16 + x, 296 + y)) == (0, 8, 0)}
            gray = {(x, y) for y in range(64) for x in range(preview.width) if picture.getpixel((16 + x, 296 + y)) == (98, 97, 98)}
            if ink != ink0 or gray != gray0:
                continue
            source_photo, source_picture = photosets['clean_Japanese'][frame]
            regions_equal = (picture.crop((0, 192, 256, 294)).tobytes() == source_picture.crop((0, 192, 256, 294)).tobytes()
                             and picture.crop((0, 0, 256, 192)).tobytes() == source_picture.crop((0, 0, 256, 192)).tobytes())
            if not regions_equal:
                region_differences.append(dict(id=interval['id'], frame=frame, native_text_plane_exact=True,
                    paired_source_upper_or_portrait_region_differs=True, not_masked_or_retimed=True))
                continue
            holds.append(dict(frame=frame, capture=photo['path'], capture_sha256=photo['PNG_sha256'],
                clean_capture=source_photo['path'], clean_capture_sha256=source_photo['PNG_sha256'],
                complete_ink_gray_masks_equal_native_plane=True, portrait_name_picture_and_upper_regions_equal_Japanese=True))
            evidence[photo['path']] = photo['PNG_sha256']
            evidence[source_photo['path']] = source_photo['PNG_sha256']
        if not holds:
            failures.append(dict(id=interval['id'], prefix=interval['prefix'], finding='No complete native plane and paired upper/portrait regions within shared holding interval.'))
        else:
            panels.append((interval['id'], interval['prefix'], Image.open(holds[0]['capture']).convert('RGB').crop((0, 192, 256, 384))))
        actual.append(dict(id=interval['id'], prefix=interval['prefix'], consumer='FE-paper' if interval['prefix'] == 254 else 'progressive',
            native_plane_sha256=case['whole_native_plane_sha256'], interval=interval, holds=holds,
            actually_displayed_in_disclosed_B22_fixture=True))
    offline = sorted(set(by_id) - {row['id'] for row in actual})
    assert set(offline) <= set(plan['expected_conditional_speech_IDs'])
    assert len(actual) + len(offline) == 37
    assert sum(row['prefix'] == 254 for row in actual) == 0
    ROOT.mkdir(parents=True)
    sheets = []
    for start in range(0, len(panels), 6):
        sheet = Image.new('RGB', (1560, 832), '#263238')
        draw = ImageDraw.Draw(sheet)
        for index, (ident, prefix, picture) in enumerate(panels[start:start + 6]):
            x, y = index % 3 * 520, index // 3 * 416
            draw.text((x + 4, y + 3), f'{ident} / {prefix:02X} / actual retained B171 content', fill='white')
            sheet.paste(picture.resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 24))
        path = ROOT / f'actual_consumer_sheet{start // 6 + 1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes())))
    counts = Counter(row['word'] for row in versions[1]['selected_B22_command_pairs'])
    save(ROOT / 'actual_all37_dream_morning_presentations_resource_C200_and_first_end.json', dict(versions=versions,
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
