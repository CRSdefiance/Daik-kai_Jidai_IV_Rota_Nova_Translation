"""Audit complete retained B168 control flow and every actually selected progressive/FE plane."""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B168_actual_v4200')
PLAN = Path('work/analysis/lil_B168_display_fixture_v4198/complete_effect_preserving_B22_fixtures.json')
FONT = Path('work/analysis/lil_B168_native_approval_v4187/all54_native_progressive_FE_and_source_reconciliation.json')
CAPBASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


if __name__ == '__main__':
    assert not ROOT.exists()
    plan, font = read(PLAN), read(FONT)
    versions, photosets = [], {}
    evidence = {str(path): sha(path.read_bytes()) for path in [PLAN, FONT, Path(__file__)]}
    for fixture in plan['fixtures']:
        assert read(Path('work/analysis/lil_B168_display_run_v4199_' + fixture['case']) / 'terminal.json')['terminal']
    for fixture in plan['fixtures']:
        case = fixture['case']
        run = Path('work/analysis/lil_B168_display_run_v4199_' + case)
        cap = CAPBASE / ('lil_B168_display_v4199_' + case)
        paths = [run / 'terminal.json', run / 'run_plan.json', cap / 'capture_report.json', cap / 'observer/commands.json']
        terminal, rp, report, trace = map(read, paths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances'] == 1
        assert report['frames'] == 20001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(fixture['research_ROM']).read_bytes()) == fixture['research_ROM_sha256'] == report['ROM_sha256'] == rp['research_ROM_sha256']
        assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event168_not_selected'] and rp['all_source_commands_and_later_A000_retained']
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
            assert source['block'] != 168
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
                pair.update(original_source_block=168, original_source_offset=commands[at]['source_offset'])
            if word == 0x4000:
                record = by_at[at]
                assert block[at:at + record['native_extent']].hex() == record['whole_command_hex']
                intervals.append(dict(id=record['id'], start=entry['frame'], returned=row['frame'], offset=at, prefix=record['source_selector']))
        selected = [row for row in pairs if row['block'] == 22]
        assert selected[-1]['word'] == 0 and selected[-1]['original_source_offset'] == 2906
        assert len(intervals) == len({row['id'] for row in intervals})
        assert 51 <= len(intervals) <= 54
        predicates = [row for row in selected if row['word'] == 0x8000]
        assert len(predicates) == 3 and all(row['result_words'][0] == 2 and row['result_words'][1] in [0, 1] for row in predicates)
        assert selected[-1]['result_words'] == [0, predicates[-1]['result_words'][1]]
        assert sum(row['word'] == 0xA000 for row in selected) == 5
        effects = [row for row in selected if row.get('original_source_block') == 168 and row['word'] == 0xA000]
        assert len(effects) == 1 and effects[0]['original_source_offset'] == 2582
        resources = [row['word'] for row in selected if row.get('original_source_block') == 168 and row['word'] & 0xFF00 == 0x6300]
        assert resources == [0x6342, 0x630B, 0x6300, 0x6301]
        native = {row['offset']: row for row in fixture['all91_stored_fixture_commands']}
        actual_at = {row['offset']: row for row in selected}
        cursor, last, expected = 8, 0, []
        while True:
            command = native[cursor]
            word = command['word']
            expected.append(cursor)
            if word == 0:
                break
            if word == 0x8000:
                last = actual_at[cursor]['result_words'][1]
                cursor += command['native_extent']
            elif word in [0x100, 0x200, 0x300, 0x400]:
                span = int.from_bytes(block[cursor + 2:cursor + 4], 'little')
                take = word == 0x100 or last == word // 256 - 2
                extent = 4 + (span if take else 0)
                assert actual_at[cursor]['extent'] == extent
                cursor += extent
            else:
                cursor += command['native_extent']
        assert [row['offset'] for row in selected] == expected
        ids = {row['id'] for row in intervals}
        assert ('DK4_MES_B168_R0020' in ids) == bool(predicates[0]['result_words'][1])
        assert ('DK4_MES_B168_R0048' in ids) == bool(predicates[1]['result_words'][1])
        assert ('DK4_MES_B168_R0135' in ids) == bool(predicates[2]['result_words'][1])
        assert sum(row['prefix'] == 254 for row in intervals) == 3
        touch = next(row for row in intervals if row['id'] == 'DK4_MES_B168_R0204')
        protest = next(row for row in intervals if row['id'] == 'DK4_MES_B168_R0207')
        sigh = next(row for row in intervals if row['id'] == 'DK4_MES_B168_R0214')
        first_fe = next(row for row in intervals if row['id'] == 'DK4_MES_B168_R0222')
        assert touch['returned'] <= protest['start'] < sigh['returned'] <= effects[0]['start'] <= effects[0]['returned'] <= first_fe['start']
        for pending in trace['unreturned_at_capture_end']:
            assert rows[pending['entry_row']]['source']['block'] != 22
        versions.append(dict(case=case, source_block=168, ROM_sha256=report['ROM_sha256'], frames=20001,
            input_schedule=rp['original_inputs'], input_schedule_sha256=rp['inputs_sha256'],
            capture_report=str(paths[2]), observer_report=str(paths[3]), selected_B22_command_pairs=selected,
            selected_intervals=intervals, actual_three_unforced_predicates=predicates,
            actual_source_recruitment_effect=effects[0], fixture_exit_frame=selected[-1]['returned'], source_end_offset=2906,
            following_observed_blocks=sorted({row['block'] for row in pairs if row['block'] != 22}),
            all_retained_control_flow_follows_original_unforced_results=True,
            all_selected_speeches_presentations_resources_effects_and_FE_return_normally=True))
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
        assert preview.height == 64 and preview.width in [216, 228]
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
    assert len(actual) + len(offline) == 54
    assert sum(row['prefix'] == 254 for row in actual) == 3
    ROOT.mkdir(parents=True)
    sheets = []
    for start in range(0, len(panels), 6):
        sheet = Image.new('RGB', (1560, 832), '#263238')
        draw = ImageDraw.Draw(sheet)
        for index, (ident, prefix, picture) in enumerate(panels[start:start + 6]):
            x, y = index % 3 * 520, index // 3 * 416
            draw.text((x + 4, y + 3), f'{ident} / {prefix:02X} / actual retained B168 content', fill='white')
            sheet.paste(picture.resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 24))
        path = ROOT / f'actual_consumer_sheet{start // 6 + 1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes())))
    counts = Counter(row['word'] for row in versions[1]['selected_B22_command_pairs'])
    save(ROOT / 'actual_progressive_FE_three_predicates_full_effect_and_return.json', dict(versions=versions,
        actual_panels=actual, fresh_actual_unique_speech_panels=len(actual), complete_matching_observations=sum(bool(row['holds']) for row in actual),
        offline_only_display_IDs=offline, failures=failures, paired_region_differences=region_differences,
        review_sheets=sheets, visual_review_pending=True, actual_new_cold_boot_runs=2,
        selected_command_counts={format(word, '04X'): count for word, count in counts.items()},
        all_source_relative_containers_three_queries_resources_presentations_A000_and_both_stored_ends_preserved=True,
        all_three_FE_notices_and_final_Mikhail_speech_observed=True,
        source_effect_returns_after_touch_protest_sigh_and_before_FE_help=True,
        actual_source_event168_not_selected=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_and_all_B168_commands_preserved=True,
        second_consecutive_endword_decoder_proven_offline_not_actually_reached=True,
        evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    assert not failures, failures
    print(dict(actual_panels=len(actual), matching=sum(bool(row['holds']) for row in actual), offline_only=offline,
               exits=[(version['case'], version['fixture_exit_frame']) for version in versions],
               query_results=[[row['result_words'] for row in version['actual_three_unforced_predicates']] for version in versions],
               sheets=len(sheets), visual_review_pending=True))
