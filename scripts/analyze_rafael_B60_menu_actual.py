"""Check live captions, cursor movement and both modal continuations without claiming story branches."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Rafael_B60_menu_actual_pixels_20261104')
FIXTURE = Path('work/analysis/Rafael_B60_menu_actual_fixture_20261104/menu_fixture.json')
TERMINAL = Path('work/analysis/Rafael_B60_menu_actual_run_20261104/terminal.json')
NATIVE = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/compatible_native_pages.json')
MENUS = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/compatible_menu_objects.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    fixture, terminal, native, menus = map(load, [FIXTURE, TERMINAL, NATIVE, MENUS])
    assert terminal['terminal'] and terminal['frames'] == fixture['frames'] == 6501
    report_path, observer_path = Path(terminal['report']), Path(terminal['observer'])
    assert sha(report_path.read_bytes()) == terminal['report_sha256'] and sha(observer_path.read_bytes()) == terminal['observer_sha256']
    report, observer = map(load, [report_path, observer_path])
    assert report['ROM_sha256'] == fixture['research_ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    rows = {r['id']: r for r in native['records']}
    expected = []
    for row in fixture['selected_records']:
        pages = rows[row['id']]['complete_native_English_display']['pages']
        assert len(pages) == 1
        page = pages[0]
        raw = Path(page['native_plane']).read_bytes()
        assert sha(raw) == page['native_plane_sha256'] and len(raw) == 216 * 64
        expected.append(dict(id=row['id'], text_hex=row['expected_expanded_body_hex'],
            native_plane=page['native_plane'], native_plane_sha256=page['native_plane_sha256'],
            pixel_mask_sha256=sha(bytes(bool(v) for v in raw))))
    allowed = {r['text_hex'] for r in expected}
    paints = [r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] >= 2800]
    target = [r for r in paints if r['text_hex'] in allowed]
    assert len(expected) == 5 and [r['text_hex'] for r in target] == [r['text_hex'] for r in expected]
    assert target[2]['frame'] == 4728 and target[4]['frame'] == 5687
    captures = report['frames_captured']
    samples = []
    for i, (paint, page) in enumerate(zip(target, expected, strict=True)):
        # Menus replace the preceding speech; only exact complete body masks earn credit.
        end = target[i+1]['frame'] if i+1 < len(target) else 6000
        for cap in captures:
            if not paint['frame'] <= cap['frame'] < end:
                continue
            path = Path(cap['path'])
            assert sha(path.read_bytes()) == cap['PNG_sha256']
            image = Image.open(path).convert('RGB')
            crop = image.crop((16, 296, 232, 360))
            if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) == page['pixel_mask_sha256']:
                samples.append(dict(**page, capture=cap, frame=cap['frame'], complete_body_plane_andblank_guards_exact=True))
    assert {r['id'] for r in samples} == {r['id'] for r in expected}
    menu_samples = []
    for item, start, end in [(menus['menus'][0], 4240, 4720), (menus['menus'][1], 5200, 5680)]:
        path = Path(item['source_native_receipt'])
        assert sha(path.read_bytes()) == item['source_native_receipt_sha256']
        proof = load(path)
        vm = proof['versions'][-1]['cases'][0]['native_VM']
        width, rect = vm['minimum_width_units'] * 6, vm['native_menu_rectangle']
        planes = [next(p for p in proof['records'] if p['version'] == 'reviewed-English' and p['option'] == option and p['style'] == 1) for option in range(2)]
        for cap in captures:
            if not start + 30 <= cap['frame'] < end:
                continue
            image_path = Path(cap['path'])
            assert sha(image_path.read_bytes()) == cap['PNG_sha256']
            image = Image.open(image_path).convert('RGB')
            labels, selected = [], []
            for option, plane in enumerate(planes):
                ink = mask(plane['path'], plane['sha256'], width)
                x, y = rect[0] + 16, 192 + rect[1] + 16 + option * 20
                assert match(image, ink, (8, 8, 8), [x], [y]) == [x, y]
                blank = {(xx, yy) for yy in range(y-4, y+16) for xx in range(x, x+width)} - {(x+xx, y+yy) for xx, yy in ink}
                cyan = {point for point in blank if image.getpixel(point) == (0, 165, 172)}
                assert not cyan or cyan == blank
                if cyan:
                    selected.append(option)
                else:
                    assert all(image.getpixel(point) == (205, 198, 180) for point in blank)
                labels.append(dict(index=option, text=vm['labels'][option], origin=[x, y], native_plane=plane['path'], native_plane_sha256=plane['sha256']))
            assert len(selected) <= 1
            menu_samples.append(dict(source_command_offset=item['source_command_offset'], frame=cap['frame'], capture=cap,
                labels=labels, visible_selected_option=selected[0] if selected else None,
                both_complete_caption_glyphs_centering_blank_guards_andbackgrounds_exact=True,
                highlight_off_phase=not selected))
    first = [s for s in menu_samples if s['source_command_offset'] == 768]
    second = [s for s in menu_samples if s['source_command_offset'] == 1852]
    assert any(s['visible_selected_option'] == 0 and s['frame'] < 4460 for s in first)
    assert any(s['visible_selected_option'] == 1 and 4460 < s['frame'] < 4580 for s in first)
    assert any(s['visible_selected_option'] == 0 and 4580 < s['frame'] < 4720 for s in first)
    # The callback labelled 5400 still shows option zero at the scheduled DOWN
    # boundary; the later 5520 callback proves the resulting option-one state.
    assert any(s['visible_selected_option'] == 0 and s['frame'] <= 5400 for s in second)
    assert any(s['visible_selected_option'] == 1 and 5400 < s['frame'] < 5680 for s in second)
    ROOT.mkdir()
    chosen = []
    for condition in [lambda s: s['source_command_offset'] == 768 and s['visible_selected_option'] == 0,
                      lambda s: s['source_command_offset'] == 768 and s['visible_selected_option'] == 1,
                      lambda s: s['source_command_offset'] == 1852 and s['visible_selected_option'] == 0,
                      lambda s: s['source_command_offset'] == 1852 and s['visible_selected_option'] == 1]:
        chosen.append(next(s for s in menu_samples if condition(s)))
    chosen += [next(s for s in samples if s['id'] == row['id']) for row in [expected[2], expected[4]]]
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
    sheet = Image.new('RGB', (1536, 1600), '#eee')
    draw = ImageDraw.Draw(sheet)
    for i, sample in enumerate(chosen):
        x, y = i % 3 * 512, i // 3 * 800
        label = 'C'+str(sample['source_command_offset'])+' selected '+str(sample['visible_selected_option']) if 'source_command_offset' in sample else sample['id'].replace('DK4_MES_', '')+' continuation'
        draw.text((x+4, y+4), label, font=font, fill='black')
        sheet.paste(Image.open(sample['capture']['path']).convert('RGB').resize((512, 768), Image.Resampling.NEAREST), (x, y+28))
    png = ROOT / 'menus_and_continuations_QA.png'
    sheet.save(png)
    save(ROOT / 'menu_actual_pixels.json', dict(frames=6501, body_pages=samples, menu_samples=menu_samples,
        all_five_ordered_speech_calls_andcomplete_body_planes_match=True,
        both_two_option_menu_caption_planes_centering_first_internal_final_glyphs_andblank_guards_match=True,
        first_menu_cursor_down_up_andsecond_menu_cursor_down_observed=True,
        A_acceptance_followed_by_original_next_fixture_speech_observed=True,
        continuation_frames=[4728, 5687], numeric_modal_return_register_not_observed=True,
        native_bridged_return_values_0_1_minus1_andoriginal_relative_sites_proved_separately_offline=True,
        original_story_response_branches_conditions_andcancellation_unvisited=True,
        review_sheet=dict(path=str(png), sha256=sha(png.read_bytes())), direct_visual_review_pending=True,
        actual_gameplay=True, disclosed_initialized_fixture=True, natural_activation=False, hardware=False,
        new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [FIXTURE, TERMINAL, NATIVE, MENUS, report_path, observer_path, Path(__file__)]}))
    print(f'Two menus/four captions: {len(menu_samples)} full samples; DOWN/UP/DOWN andboth A continuations pass. One QA sheet pending direct review.')
