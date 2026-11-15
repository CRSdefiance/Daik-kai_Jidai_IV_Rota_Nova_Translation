"""Attribute bounded live pages by exact ordered calls; compare complete bodies and headers."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Rafael_B51_B60_focused_pixels_20261104')
FIXTURE = Path('work/analysis/Rafael_B51_B60_focused_20261104/focused_fixture.json')
TERMINAL = Path('work/analysis/Rafael_B51_B60_focused_run_20261104/terminal.json')
NATIVE = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/compatible_native_pages.json')
NAMES = Path('work/analysis/Rafael_B51_B60_progressive_name_planes_20261104/native_name_planes.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    fixture, terminal, native, names = map(load, [FIXTURE, TERMINAL, NATIVE, NAMES])
    assert terminal['terminal'] and terminal['frames'] == fixture['frames'] == 12161
    report_path, observer_path = Path(terminal['report']), Path(terminal['observer'])
    assert sha(report_path.read_bytes()) == terminal['report_sha256']
    assert sha(observer_path.read_bytes()) == terminal['observer_sha256']
    report, observer = map(load, [report_path, observer_path])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert report['ROM_sha256'] == fixture['research_ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    byid = {r['id']: r for r in native['records']}
    decisions_path = Path(names['name_decisions'])
    assert sha(decisions_path.read_bytes()) == names['name_decisions_sha256']
    byactor = {r['actor_ID']: r['english'] for r in load(decisions_path)['records']}
    name_planes = {r['text']: r for r in names['planes']}
    expected = []
    for row in fixture['selected_records']:
        body = bytes.fromhex(row['expected_expanded_body_hex'])
        display = byid[row['id']]['complete_native_English_display']
        width = 228 if row['selector'] == 254 else 216
        pages = [display] if width == 228 else display['pages']
        for number, page in enumerate(pages, 1):
            plane = Path(page['native_plane']).read_bytes()
            assert sha(plane) == page['native_plane_sha256'] and len(plane) == width * 64
            expected.append(dict(id=row['id'], page=number, selector=row['selector'], width=width,
                native_plane=page['native_plane'], native_plane_sha256=page['native_plane_sha256'],
                text_hex=body[page.get('start', 0):].hex(), pixel_mask_sha256=sha(bytes(bool(v) for v in plane))))
    assert len(expected) == fixture['expected_pages'] == 30 and len(fixture['selected_records']) == 27
    allowed = {p['text_hex'] for p in expected}
    paints = [r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] >= 2800]
    target = [r for r in paints if r['text_hex'] in allowed]
    assert [r['text_hex'] for r in target] == [p['text_hex'] for p in expected], (len(target), len(expected))
    assert len({r['frame'] for r in target}) == len(target)
    ordered = {r['frame']: p for r, p in zip(target, expected, strict=True)}
    start = target[0]['frame']
    end = next((r['frame'] for r in paints if r['frame'] > target[-1]['frame']), report['frames'] + 1)
    assert not [r for r in paints if start <= r['frame'] < end and r['text_hex'] not in allowed]
    samples, headers = [], []
    for cap in report['frames_captured']:
        if not start <= cap['frame'] < end:
            continue
        active = next(r for r in reversed(target) if r['frame'] <= cap['frame'])
        page = ordered[active['frame']]
        path = Path(cap['path'])
        assert sha(path.read_bytes()) == cap['PNG_sha256']
        image = Image.open(path).convert('RGB')
        crop = image.crop((16, 296, 16 + page['width'], 360))
        if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) != page['pixel_mask_sha256']:
            continue
        samples.append(dict(**page, capture=cap, frame=cap['frame'], live_modal_frame=active['frame'],
            complete_native_body_plane_andblank_guards_equal=True,
            occurrence_evidence='complete ordered native calls and exact sequential source-command copies'))
        actor = page['selector']
        if actor != 254:
            text = byactor[actor]
            plane = name_planes[text]
            origin = match(image, mask(plane['native_plane'], plane['native_plane_sha256'], 216), (98, 97, 98), [16], [276])
            headers.append(dict(actor_ID=actor, text=text, frame=cap['frame'], capture=cap, origin=origin,
                native_plane=plane['native_plane'], native_plane_sha256=plane['native_plane_sha256'],
                complete_name_glyphs_andblank_guards_exact=True))
    unique = {}
    for sample in samples:
        unique.setdefault((sample['id'], sample['page']), sample)
    assert set(unique) == {(p['id'], p['page']) for p in expected}, ('missing', [(p['id'], p['page']) for p in expected if (p['id'], p['page']) not in unique])
    assert {h['actor_ID'] for h in headers} == set(fixture['ordinary_actor_IDs']) and len(fixture['ordinary_actor_IDs']) == 18
    ROOT.mkdir()
    sheets = []
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
    selected = [unique[p['id'], p['page']] for p in expected]
    for first in range(0, len(selected), 6):
        group = selected[first:first+6]
        sheet = Image.new('RGB', (1536, 1600), '#eee')
        draw = ImageDraw.Draw(sheet)
        for index, sample in enumerate(group):
            x, y = index % 3 * 512, index // 3 * 800
            draw.text((x+4, y+4), sample['id'].replace('DK4_MES_', '') + ' p' + str(sample['page']) + ' actor' + str(sample['selector']), font=font, fill='black')
            sheet.paste(Image.open(sample['capture']['path']).convert('RGB').resize((512, 768), Image.Resampling.NEAREST), (x, y+28))
        png = ROOT / f'focused_QA_{len(sheets)+1}.png'
        sheet.save(png)
        sheets.append(dict(path=str(png), sha256=sha(png.read_bytes()), pages=len(group)))
    save(ROOT / 'focused_actual_pixels.json', dict(frames=fixture['frames'], selected_utterances=27, selected_pages=30,
        complete_body_planes=len(samples), complete_header_planes=len(headers), body_pages=samples, headers=headers,
        ordered_selected_source_calls=[dict(frame=r['frame'], id=p['id'], page=p['page']) for r, p in zip(target, expected, strict=True)],
        all_selected_pages_observed_in_exact_fixture_order=True, all_complete_native_body_andheader_planes_andblank_guards_match=True,
        all18_actors_three_FE_three_I_Fernan_F_andthree_two_page_transitions_observed=True,
        review_sheets=sheets, direct_visual_review_pending=True, unvisited_utterances=218,
        all245_complete_conversations_reviewed_offline_not_naturally_played=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        following_nonfixture_modal_frame=end, actual_gameplay=True, disclosed_initialized_fixture=True,
        menu_controller_checks_separate_andpending=True, new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [FIXTURE, TERMINAL, NATIVE, NAMES, report_path, observer_path, Path(__file__)]}))
    print(f'27 utterances/30 ordered pages;{len(samples)} full body and{len(headers)} full header planes pass. Five QA sheets pending direct review.')
