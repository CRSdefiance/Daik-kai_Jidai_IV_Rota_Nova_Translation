"""Match observed tutorial calls and framebuffer pixels to the reviewed native pages."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Rafael_early_tutorial_B42_B43_actual_pixels_20261104')
FIXTURES = Path('work/analysis/Rafael_early_tutorial_B42_B43_actual_fixtures_20261104')
DISPLAY = Path('work/analysis/Rafael_early_tutorial_B42_B43_formatting_20261104/speech_display_approved_v2/all40_native_pages.json')
STORED = Path('work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/stored_native_v1/stored_native_verification.json')
NAMES = Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104/native_name_planes.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    native, stored, names = map(load, [DISPLAY, STORED, NAMES])
    assert native['runtime'] == stored['runtime'] == names['runtime']
    source = {r['id']: r for r in stored['records']}
    by_id = {r['id']: r for r in native['records']}
    consumers = {r['actor_ID']: r['text'] for r in names['consumer_bindings'] if r['consumer'] == 'progressive-nameplate'}
    name_planes = {r['text']: r for r in names['planes']}
    pages = {}
    for row in native['records']:
        width = 228 if row['kind'] == 'system-FE' else 216
        display = row['complete_native_English_display']
        expanded = bytes.fromhex(source[row['id']]['expanded_hex'])
        for number, page in enumerate([display] if width == 228 else display['pages'], 1):
            data = Path(page['native_plane']).read_bytes()
            assert sha(data) == page['native_plane_sha256'] and len(data) == width * 64
            pages[row['id'], number] = dict(id=row['id'], page=number, width=width,
                text_hex=expanded[page.get('start', 0):].hex(), native_plane=page['native_plane'],
                native_plane_sha256=page['native_plane_sha256'], pixel_mask_sha256=sha(bytes(bool(v) for v in data)))
    assert len(pages) == 42
    bodies, headers, runs, sequences, intervals, following = [], [], [], [], {}, []
    reports = {}
    for key in ['first_voyage', 'crew_duties']:
        terminal_path = Path(f'work/analysis/Rafael_early_tutorial_B42_B43_{key}_run_20261104/terminal.json')
        fixture_path = FIXTURES / (key + '_fixture.json')
        terminal, fixture = map(load, [terminal_path, fixture_path])
        assert terminal['terminal'] and terminal['frames'] == fixture['frames']
        report_path, observer_path = Path(terminal['report']), Path(terminal['observer'])
        assert sha(report_path.read_bytes()) == terminal['report_sha256'] and sha(observer_path.read_bytes()) == terminal['observer_sha256']
        report, observer = map(load, [report_path, observer_path])
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256'] == fixture['research_ROM_sha256']
        assert sha(Path(fixture['inputs']).read_bytes()) == fixture['inputs_sha256']
        expected = [p for row in fixture['selected_records'] for identity, p in pages.items() if identity[0] == row['id']]
        allowed = {p['text_hex'] for p in expected}
        paints = [r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] >= 2800]
        target = [r for r in paints if r['text_hex'] in allowed]
        assert [r['text_hex'] for r in target] == [p['text_hex'] for p in expected], (key, len(target), len(expected))
        assert len({r['frame'] for r in target}) == len(target)
        ordered = {r['frame']: p for r, p in zip(target, expected, strict=True)}
        start = target[0]['frame']
        end = next((r['frame'] for r in paints if r['frame'] > target[-1]['frame'] and r['text_hex'] not in allowed), report['frames'] + 1)
        intervals[key] = dict(first_target_frame=start, first_following_nonfixture_modal_frame=end)
        sequences.append(dict(run=key, calls=len(target), complete_ordered_calls_match_all_copied_source_speeches=True,
            calls_andpages=[dict(frame=r['frame'], id=p['id'], page=p['page']) for r, p in zip(target, expected, strict=True)]))
        seen_headers = set()
        for capture in report['frames_captured']:
            frame = capture['frame']
            if not start <= frame < end:
                continue
            active = next(r for r in reversed(target) if r['frame'] <= frame)
            page = ordered[active['frame']]
            path = Path(capture['path'])
            assert sha(path.read_bytes()) == capture['PNG_sha256']
            im = Image.open(path).convert('RGB')
            crop = im.crop((16, 296, 16 + page['width'], 360))
            if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) != page['pixel_mask_sha256']:
                continue  # Partial typing is not complete-page coverage.
            bodies.append(dict(run=key, frame=frame, capture=capture, id=page['id'], page=page['page'], origin=[16, 296],
                complete_native_glyph_plane_andblank_guards_equal=True, live_modal_frame=active['frame']))
            actor = next(r['selector'] for r in fixture['selected_records'] if r['id'] == page['id'])
            if actor != 254 and actor not in seen_headers:
                text = consumers[actor]
                plane = name_planes[text]
                origin = match(im, mask(plane['native_plane'], plane['native_plane_sha256'], 216), (98, 97, 98), [16], [276])
                headers.append(dict(run=key, frame=frame, actor_ID=actor, text=text, origin=origin, capture=capture,
                    complete_name_glyphs_andblank_guards_exact=True))
                seen_headers.add(actor)
        reports[key] = report
        following += [dict(run=key, frame=r['frame'], text=r['text_CP932'], outside_reviewed_batch=True) for r in paints if r['frame'] >= end]
        runs.append(dict(key=key, frames=report['frames'], terminal=str(terminal_path), terminal_sha256=sha(terminal_path.read_bytes()),
            report=str(report_path), report_sha256=sha(report_path.read_bytes()), observer=str(observer_path), observer_sha256=sha(observer_path.read_bytes()),
            fixture=str(fixture_path), fixture_sha256=sha(fixture_path.read_bytes())))
    observed = {(r['id'], r['page']) for r in bodies}
    required = {('DK4_MES_B42_R0019', 1), ('DK4_MES_B42_R0019', 2), ('DK4_MES_B42_R0026', 1),
        ('DK4_MES_B42_R0080', 1), ('DK4_MES_B43_R0017', 1), ('DK4_MES_B43_R0030', 1),
        ('DK4_MES_B43_R0030', 2), ('DK4_MES_B43_R0045', 1)}
    assert required <= observed and {r['actor_ID'] for r in headers} == {0, 4, 5, 6}
    selected = []
    seen = set()
    for row in bodies:
        identity = row['id'], row['page']
        if identity in required and identity not in seen:
            selected.append(dict(capture=row['capture'], label=row['id'].replace('DK4_MES_', '') + 'p' + str(row['page'])))
            seen.add(identity)
    for row in headers:
        selected.append(dict(capture=row['capture'], label=row['text'] + ' header'))
    for key, report in reports.items():
        end = intervals[key]['first_following_nonfixture_modal_frame']
        later = [r for r in report['frames_captured'] if r['frame'] >= end + 120]
        assert later
        selected.append(dict(capture=later[0], label=key + ' following transition'))
    ROOT.mkdir()
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
    sheets = []
    for at in range(0, len(selected), 9):
        part = selected[at:at+9]
        sheet = Image.new('RGB', (768, math.ceil(len(part)/3)*216), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for i, item in enumerate(part):
            x, y = i % 3 * 256, i // 3 * 216
            im = Image.open(item['capture']['path']).convert('RGB')
            sheet.paste(im.crop((0,192,256,384)), (x,y+24))
            draw.text((x+2,y+2), item['label'][:30]+'@'+str(item['capture']['frame']), fill='black', font=font)
        path = ROOT / f'focused_QA_{at//9+1}.png'
        sheet.resize((1536,sheet.height*2),Image.Resampling.NEAREST).save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),captures=part))
    save(ROOT/'focused_actual_pixels.json',dict(runs=runs,body_pages=bodies,name_headers=headers,review_sheets=sheets,
        ordered_linear_scene_sequences=sequences,observed_record_pages=sorted(observed),required_distinct_display_cases=sorted(required),
        target_intervals=intervals,following_outside_batch_text=following,actual_frames=sum(r['frames'] for r in runs),
        actual_gameplay=True,disclosed_initialized_fixtures=True,natural_activation=False,hardware_verification=False,
        complete_body_planes_andheaders_andtwo_page_transitions_pass=True, all_required_distinct_display_cases_match=True,
        source_event_eligibility_original_location_earned_progress_fullroute_unvisited=True,
        direct_visual_review_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DISPLAY,STORED,NAMES,Path(__file__)]}))
    print(dict(actual_frames=sum(r['frames'] for r in runs),body_planes=len(bodies),observed_record_pages=len(observed),headers=len(headers),sheets=len(sheets)))
