"""Audit original accept/refuse control flow and complete actual native glyph planes."""
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_menu_backing_surface_v4080 import paint
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B167_actual_v4151')
PLAN = Path('work/analysis/lil_B167_display_fixture_v4147/complete_choice_preserving_B22_fixtures.json')
FONT = Path('work/analysis/lil_B167_native_approval_v4135/all29_native_speech_choice_and_source_reconciliation.json')
MENU = Path('work/analysis/lil_B167_choices_v4133/B167_C152/original_choice_decoder_VM_geometry_and_native_pixels.json')
CAPBASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan, font, menu = map(read, [PLAN, FONT, MENU])
    versions, photosets = [], {}
    evidence = {str(p): sha(p.read_bytes()) for p in [PLAN, FONT, MENU, Path(__file__)]}
    for option in [0, 1]:
        for fixture in plan['fixtures']:
            run = Path(f'work/analysis/lil_B167_display_run_v4149_O{option}_' + fixture['case'])
            assert read(run / 'terminal.json')['terminal']
    for option in [0, 1]:
        for fixture in plan['fixtures']:
            case = fixture['case']
            fid = f'O{option}_{case}'
            run = Path('work/analysis/lil_B167_display_run_v4149_' + fid)
            cap = CAPBASE / ('lil_B167_display_v4149_' + fid)
            paths = [run / 'terminal.json', run / 'run_plan.json', cap / 'capture_report.json', cap / 'observer/commands.json']
            terminal, rp, report, trace = map(read, paths)
            assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances'] == 1
            assert report['frames'] == 14401 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
            assert sha(Path(fixture['research_ROM']).read_bytes()) == fixture['research_ROM_sha256'] == report['ROM_sha256'] == rp['research_ROM_sha256']
            assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event167_not_selected'] and rp['requested_sail_lesson_option'] == option
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
                assert picture.size == (256,384)
                photos[photo['frame']] = (photo, picture)
            snapshot = report['read_only_RAM_snapshot']
            assert snapshot['read_only_export'] and snapshot['bytes'] == 4194304
            assert sha(Path(snapshot['path']).read_bytes()) == snapshot['sha256']
            pairs, intervals = [], []
            rows = trace['rows']
            text_by_at = {r['fixture_command_offset']: r for r in fixture['original_text_records']}
            source_by_at = {r['fixture_offset']: r for r in fixture['selected_original_objects']}
            for row in rows:
                assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
                source = row['source']
                assert source['classification'] == 'original_SC_cache' and source['route'] == 2
                assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256'] == sha(blocks[source['block']])
                assert source['block'] != 167
                if row['kind'] != 'after_command':
                    continue
                entry = rows[row['entry_row']]
                src = entry['source']
                at = src['instruction_offset']
                word = int.from_bytes(blocks[src['block']][at:at+2], 'little')
                pair = dict(block=src['block'], offset=at, word=word, start=entry['frame'],
                            returned=row['frame'], extent=row['decoded_length'], result_words=row['result_words'])
                pairs.append(pair)
                if src['block'] != 22:
                    continue
                if at in source_by_at:
                    assert word == source_by_at[at]['source_word']
                    pair.update(original_source_block=167, original_source_offset=source_by_at[at]['source_offset'])
                if word == 0x4000:
                    record = text_by_at[at]
                    assert block[at:at+record['native_extent']].hex() == record['whole_command_hex']
                    intervals.append(dict(id=record['id'], start=entry['frame'], returned=row['frame'],
                        offset=at, prefix=record['source_selector']))
            selected = [p for p in pairs if p['block'] == 22]
            assert selected[-1]['word'] == 0
            menus = [p for p in selected if p['word'] == 0x2100]
            predicates = [p for p in selected if p['word'] == 0x8000]
            assert len(menus) == len(predicates) == 1 and menus[0]['result_words'] == [2, option]
            assert predicates[0]['result_words'][0] == 2 and predicates[0]['result_words'][1] in [0,1]
            assert selected[-1]['result_words'] == [0,predicates[0]['result_words'][1]] # the later query, not the menu, owns final state
            assert sum(p['word'] == 0xA000 for p in selected) == 4
            assert not any(p['word'] == 0xA000 and p.get('original_source_block') == 167 for p in selected)
            assert [p['word'] for p in selected if p.get('original_source_block') == 167 and p['word'] & 0xFF00 == 0x6300] == [0x6327,0x632B]
            native = {r['offset']: r for r in fixture['all55_stored_fixture_commands']}
            cursor, last_result, expected = 8, 0, []
            while True:
                command = native[cursor]
                word = command['word']
                expected.append(cursor)
                if word == 0:
                    break
                if word in [0x100,0x200,0x300,0x400]:
                    span = int.from_bytes(block[cursor+2:cursor+4], 'little')
                    take = word == 0x100 or last_result == word//256-2
                    cursor += 4 + (span if take else 0)
                else:
                    if word == 0x8000:
                        last_result = predicates[0]['result_words'][1]
                    elif word == 0x2100:
                        last_result = option
                    cursor += command['native_extent']
            assert [p['offset'] for p in selected] == expected
            expected_ids = {text_by_at[at]['id'] for at in expected if at in text_by_at}
            assert len(intervals) == len({r['id'] for r in intervals}) == len(expected_ids)
            assert {r['id'] for r in intervals} == expected_ids
            assert (('DK4_MES_B167_R0131' if option==0 else 'DK4_MES_B167_R0045') in expected_ids)==bool(predicates[0]['result_words'][1])
            assert (selected[-1]['original_source_offset']) == (2172 if option==0 else 430)
            for pending in trace['unreturned_at_capture_end']:
                assert rows[pending['entry_row']]['source']['block'] != 22
            versions.append(dict(case=case, option_index=option, source_block=167, ROM_sha256=report['ROM_sha256'],
                frames=report['frames'], input_schedule=rp['original_inputs'], input_schedule_sha256=rp['inputs_sha256'],
                capture_report=str(cap/'capture_report.json'), observer_report=str(cap/'observer/commands.json'),
                selected_B22_command_pairs=selected, selected_intervals=intervals, actual_choice_command_pair=menus[0],
                actual_unforced_Cesare_predicate=predicates[0], fixture_exit_frame=selected[-1]['returned'],
                source_end_offset=2172 if option==0 else 430, following_observed_blocks=sorted({p['block'] for p in pairs if p['block'] != 22}),
                all_retained_branch_commands_follow_native_source_outcome=True, all_selected_speeches_and_commands_return_normally=True))
            photosets[option, case] = photos
            evidence.update({str(p): sha(p.read_bytes()) for p in paths})
    byversion = {(v['option_index'],v['case']): v for v in versions}
    shape = lambda version: [(p.get('original_source_offset'),p['word'],p['result_words']) for p in version['selected_B22_command_pairs']]
    for option in [0,1]:
        assert shape(byversion[option,'clean_Japanese']) == shape(byversion[option,'reviewed_English'])
    byid = {r['id']: r for r in font['cases']}
    observations, unique, failures = [], {}, []
    for option in [0,1]:
        source_intervals = {r['id']: r for r in byversion[option,'clean_Japanese']['selected_intervals']}
        for interval in byversion[option,'reviewed_English']['selected_intervals']:
            case = byid[interval['id']]
            preview = Image.open(case['preview']).convert('RGB')
            assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
            ink0 = {(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y)) == (0,8,0)}
            gray0 = {(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y)) == (98,97,98)}
            src = source_intervals[interval['id']]
            holds = []
            for frame, (photo,picture) in photosets[option,'reviewed_English'].items():
                if not max(interval['start'],src['start']) < frame < min(interval['returned'],src['returned']):
                    continue
                ink = {(x,y) for y in range(64) for x in range(216) if picture.getpixel((16+x,296+y)) == (0,8,0)}
                gray = {(x,y) for y in range(64) for x in range(216) if picture.getpixel((16+x,296+y)) == (98,97,98)}
                if ink != ink0 or gray != gray0:
                    continue
                sourcephoto, sourcepicture = photosets[option,'clean_Japanese'][frame]
                assert picture.crop((0,192,256,294)).tobytes() == sourcepicture.crop((0,192,256,294)).tobytes()
                assert picture.crop((0,0,256,192)).tobytes() == sourcepicture.crop((0,0,256,192)).tobytes()
                holds.append(dict(frame=frame, capture=photo['path'], capture_sha256=photo['PNG_sha256'],
                    clean_capture=sourcephoto['path'], clean_capture_sha256=sourcephoto['PNG_sha256'],
                    complete_ink_gray_masks_equal_native_plane=True, portrait_name_picture_and_upper_regions_equal_Japanese=True))
                evidence[photo['path']] = photo['PNG_sha256']
                evidence[sourcephoto['path']] = sourcephoto['PNG_sha256']
            if not holds:
                failures.append(dict(id=interval['id'], option_index=option, finding='No complete native plane inside shared holding interval.'))
            record = dict(id=interval['id'], option_index=option, prefix=interval['prefix'], native_plane_sha256=case['whole_native_plane_sha256'],
                          interval=interval, holds=holds, actually_displayed_in_disclosed_B22_fixture=True)
            observations.append(record)
            if holds and interval['id'] not in unique:
                unique[interval['id']] = record
    arm = NdsImage.open(plan['parent']).read_file('/__arm9__.bin')
    masks = []
    for index, label in enumerate([b'Okay', b'No thanks']):
        pixels, proof = paint(arm,label,8,54,(0,index*12))
        masks.append({(x,y) for y in range(12) for x in range(54) if pixels[y*54+x] == 8})
    assert all(m for m in masks)
    def caption_style(picture,index):
        colors={picture.getpixel((101+x,272+20*index+y)) for y in range(12) for x in range(54)} & {(0,165,172),(205,198,180)}
        assert len(colors)==1
        return colors.pop()
    actualmenus = []
    for option in [0,1]:
        interval = byversion[option,'reviewed_English']['actual_choice_command_pair']
        holds = []
        for frame, (photo,picture) in photosets[option,'reviewed_English'].items():
            if not interval['start']+30 < frame < interval['returned']:
                continue
            sourcepicture = photosets[option,'clean_Japanese'][frame][1]
            for index, expected in enumerate(masks):
                x0, y0 = 101, 272 + 20*index
                actual = {(x,y) for y in range(12) for x in range(54) if picture.getpixel((x0+x,y0+y)) == (8,8,8)}
                assert actual == expected
                color,sourcecolor=caption_style(picture,index),caption_style(sourcepicture,index)
                allowed=[(0,165,172),(205,198,180)] if index==option else [(205,198,180)]
                assert color in allowed and sourcecolor in allowed
            holds.append(dict(frame=frame, path=photo['path'], sha256=photo['PNG_sha256'],
                all_complete_label_foreground_pixels_equal_complete_native_planes=True,
                correct_selected_highlight_visible=caption_style(picture,option)==(0,165,172),
                source_correct_selected_highlight_visible=caption_style(sourcepicture,option)==(0,165,172),
                English_caption_styles=[caption_style(picture,i) for i in [0,1]],
                Japanese_caption_styles=[caption_style(sourcepicture,i) for i in [0,1]],
                menu_relative_ages=[frame-interval['start'],frame-byversion[option,'clean_Japanese']['actual_choice_command_pair']['start']],
                original_permitted_blink_states_and_unselected_plain_style_pass=True))
        assert holds and any(h['correct_selected_highlight_visible'] for h in holds) and any(h['source_correct_selected_highlight_visible'] for h in holds)
        actualmenus.append(dict(option_index=option, native_result_words=interval['result_words'],
            text_canvas_origins=[[101,272],[101,292]], holds=holds))
    actual_ids = {r['id'] for v in versions if v['case'] == 'reviewed_English' for r in v['selected_intervals']}
    assert actual_ids == set(unique)
    offline = sorted(set(byid)-actual_ids)
    assert set(offline) <= {'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}
    assert {r['prefix'] for r in observations} == ({2,4,23,109} if len(offline)==2 else {2,4,13,23,109})
    ROOT.mkdir(parents=True)
    panels = [(ident,r['prefix'],Image.open(r['holds'][0]['capture']).convert('RGB').crop((0,192,256,384))) for ident,r in unique.items()]
    sheets = []
    for start in range(0,len(panels),6):
        sheet = Image.new('RGB',(1560,832),'#263238')
        draw = ImageDraw.Draw(sheet)
        for j,(ident,prefix,picture) in enumerate(panels[start:start+6]):
            x,y = j%3*520,j//3*416
            draw.text((x+4,y+3),f'{ident} / {prefix:02X} / actual retained-condition B22 fixture',fill='white')
            sheet.paste(picture.resize((512,384)),(x+4,y+24))
        path = ROOT / f'actual_consumer_sheet{start//6+1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT / 'actual_both_choices_conditional_panels_and_distinct_returns.json', dict(versions=versions,
        actual_panels=list(unique.values()), all_actual_speech_observations=observations, actual_menu_cases=actualmenus,
        fresh_actual_unique_speech_panels=len(unique), actual_English_speech_observations=len(observations),
        complete_matching_observations=sum(bool(r['holds']) for r in observations), offline_only_display_IDs=offline,
        failures=failures, review_sheets=sheets, visual_review_pending=True, actual_new_cold_boot_runs=4,
        all12_original_relative_commands_and_two_Cesare_queries_retained_not_flattened=True,
        both_real_choice_values_and_distinct_source_endwords_observed=True, actual_source_event167_not_selected=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_preserved_and_no_B167_command_omitted=True,
        source_and_English_type0_return_preserve_later_query_result_not_forced_menu_option=True,
        source_English_highlight_blink_phases_at_global_frames_are_recorded_without_false_RGB_equivalence=True, both_versions_visible_highlight_matches_returned_option_and_unselected_never_highlighted=True, historical_B166_audit_fixes_preserved={str(p):sha(p.read_bytes()) for p in [Path("scripts/audit_lil_B166_actual_v4104.py"),Path("scripts/audit_lil_B166_actual_v4104b.py"),Path("scripts/audit_lil_B166_actual_v4104c.py")]}, evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    assert not failures, failures
    print(dict(unique_panels=len(unique), observations=len(observations), offline_only=offline,
        actual_menu_values=[r['native_result_words'] for r in actualmenus],
        exits=[(v['option_index'],v['case'],v['fixture_exit_frame']) for v in versions], sheets=len(sheets), visual_review_pending=True))
