"""Bind one early menu-return header animation and two complete stable holds."""
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    out = ROOT/'name_header_transition_v1.json'
    assert not out.exists()
    fixturepath = ROOT/'display_fixtures_v1/Maria321_Jam_figurehead_refusal_menu1_fixture.json'
    terminalpath = ROOT/'display_run_menu2_v1/terminal.json'
    namespath = ROOT/'name_planes_v1/native_name_planes.json'
    nativepath = ROOT/'final_native_v1.json'
    fixture, terminal, names, native = map(load, [fixturepath, terminalpath, namespath, nativepath])
    reportpath, observerpath = map(Path, [terminal['report'], terminal['observer']])
    assert digest(reportpath) == terminal['report_sha256'] and digest(observerpath) == terminal['observer_sha256']
    report, observer = map(load, [reportpath, observerpath])
    assert terminal['terminal'] and terminal['frames'] == report['frames'] == 17441
    assert report['ROM_sha256'] == fixture['research_ROM_sha256'] == digest(fixture['research_ROM'])
    key = 'DK4_MES_B215_R0174'
    binding = next(r for r in fixture['selected_records'] if r['id'] == key)
    assert binding['selector'] == 139 and binding['logical_English'] == 'A wise decision.'
    call = next(r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] == 10736)
    assert call['text_CP932'].strip() == 'A wise decision.'
    assert not any(r['kind'] == 'modal_paint' and 10736 < r['frame'] <= 10920 for r in observer['rows'])
    body = next(r for r in native['records'] if r['id'] == key)['complete_native_English_display']['pages'][0]
    assert digest(body['native_plane']) == body['native_plane_sha256']
    expected_body = bytes(bool(v) for v in Path(body['native_plane']).read_bytes())
    plane = next(p for p in names['planes'] if p['text'] == 'Priest')
    ink = mask(plane['native_plane'], plane['native_plane_sha256'], 216)
    right, bottom = max(x for x,y in ink)+4, max(y for x,y in ink)+2
    captures = []
    for frame in [10740,10800,10920]:
        cap = next(c for c in report['frames_captured'] if c['frame'] == frame)
        assert digest(cap['path']) == cap['PNG_sha256']
        with Image.open(cap['path']) as image:
            image = image.convert('RGB')
            crop = image.crop((16,296,232,360))
            assert bytes(rgb == (0,8,0) for rgb in crop.getdata()) == expected_body
            found = {(x-16,y-276) for y in range(276,276+bottom) for x in range(14,16+right) if image.getpixel((x,y)) == (98,97,98)}
            missing, extra = sorted(ink-found), sorted(found-ink)
            if frame == 10740:
                assert missing == [(0,1),(0,2),(1,1),(2,1),(3,2),(14,1),(14,2),(32,1),(32,2)] and not extra
            else:
                assert not missing and not extra
                assert match(image,ink,(98,97,98),[16],[276]) == [16,276]
        captures.append(dict(capture=cap, missing_header_pixels=missing, extra_header_pixels=extra,
            complete_body_plane_exact=True, complete_header_approved=frame != 10740))
    save(out, dict(fixture=str(fixturepath), fixture_sha256=digest(fixturepath), terminal=str(terminalpath), terminal_sha256=digest(terminalpath),
        report=str(reportpath), report_sha256=digest(reportpath), observer=str(observerpath), observer_sha256=digest(observerpath),
        runtime=native['runtime'], id=key, source_selector=139, expected_name='Priest', native_call_frame=10736,
        nonapproved_transition_frame=10740, frames_after_call=4, stable_frames=[10800,10920],
        captured_header_transition_not_a_complete_name_approval=True, all_later_stable_header_pixels_complete_andexact=True,
        early_capture_added_for_menu_cursor_QA_not_regular_hold=True,
        no_ROM_font_control_input_ororiginal_capture_changes=True, captures=captures, new_credit=0,
        evidence={str(p):digest(p) for p in [fixturepath,terminalpath,reportpath,observerpath,namespath,nativepath,Path(__file__)]}))
    print('Bound the nine missing early header pixels at+4 frames; both complete regular holds pass without changing ROM or captures.')


if __name__ == '__main__':
    main()
