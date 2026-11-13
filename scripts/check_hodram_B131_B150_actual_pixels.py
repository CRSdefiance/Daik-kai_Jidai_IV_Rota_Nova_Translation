"""Match focused actual framebuffer text to complete already-qualified native planes."""
from pathlib import Path
from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Hodram_B131_B150_actual_pixels_20261102')
NATIVE = Path('work/analysis/Hodram_B131_B150_editorial_20261102/native_v3/compiled_native_pages.json')
SHEETS = [Path('work/analysis/Hodram_B131_B150_actual_20261102/capture_sheets.json'),
          Path('work/analysis/Hodram_B131_B150_actual_second_choice_20261102/capture_sheets.json')]
NAMES = Path('work/analysis/Hodram_B131_B150_retained_name_native_20261102/native_name_fields_verification_reviewed.json')
MENU = Path('work/analysis/Hodram_B131_B150_editorial_20261102/menus_v1/B136_C130/menu_provider_and_planes.json')


def ink_digest(data):
    return sha(bytes(bool(v) for v in data))


def main():
    assert not ROOT.exists()
    native = load(NATIVE)
    lookup = {}
    for row in native['records']:
        width = 228 if row['kind'] == 'system-FE' else 216
        rendered = row['complete_native_English_display']
        pages = [rendered] if row['kind'] == 'system-FE' else rendered['pages']
        for number, page in enumerate(pages, 1):
            path = Path(page['native_plane'])
            data = path.read_bytes()
            assert sha(data) == page['native_plane_sha256'] and len(data) == width * 64
            key = row['block'], width, ink_digest(data)
            lookup.setdefault(key, []).append(dict(id=row['id'], page=number, kind=row['kind'],
                native_plane=str(path), native_plane_sha256=page['native_plane_sha256']))
    runs = [r for path in SHEETS for r in load(path)['runs']]
    bodies = []
    captures = {}
    for run in runs:
        report_path = Path(run['capture_report'])
        assert sha(report_path.read_bytes()) == run['capture_report_sha256']
        report = load(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
        block = load(Path(report_path).with_name('run_plan.json'))['block']
        captures[str(report_path)] = report
        for capture in report['frames_captured']:
            if capture['frame'] < 3980:
                continue
            image_path = Path(capture['path'])
            assert sha(image_path.read_bytes()) == capture['PNG_sha256']
            image = Image.open(image_path).convert('RGB')
            for width in [216, 228]:
                crop = image.crop((16, 296, 16 + width, 360))
                digest = sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata()))
                found = lookup.get((block, width, digest), [])
                if found:
                    bodies.append(dict(block=block, frame=capture['frame'], capture_report=str(report_path),
                        capture_report_sha256=run['capture_report_sha256'], capture=capture,
                        native_equivalent_candidates=found, ambiguous_occurrence=len(found) != 1,
                        origin=[16, 296], viewport=[width, 64], complete_native_glyph_plane_andblank_guards_equal=True,
                        bounded_framebuffer_comparison_no_backing_RAM_VRAM_orregister_ownership_claim=True))
    observed = {(c['id'], c['page']) for b in bodies for c in b['native_equivalent_candidates']}
    required = [('SC1_B133_STYLE_10_4', 1), ('DK4_MES_B136_R0027', 1), ('DK4_MES_B136_R0044', 1),
                ('DK4_MES_B142_R0008', 1), ('DK4_MES_B142_R0008', 2), ('DK4_MES_B142_R0213', 1),
                ('DK4_MES_B143_R0033', 1), ('DK4_MES_B143_R0084', 1), ('DK4_MES_B143_R0087', 1)]
    assert all(case in observed for case in required), [case for case in required if case not in observed]
    name = load(NAMES)
    headers = []
    report_path = Path('work/emulation_v193/Hodram_B131_B150_English_20261102_B143/capture_report.json')
    report = load(report_path)
    for frame, text in [(4460, 'Barkeep'), (8300, 'Sera Shahrbaraz')]:
        plane = next(p for p in name['planes'] if p['text'] == text and p['style'] == 11)
        ink = mask(plane['plane'], plane['plane_sha256'], 216)
        capture = next(c for c in report['frames_captured'] if c['frame'] == frame)
        image = Image.open(capture['path']).convert('RGB')
        origin = match(image, ink, (98, 97, 98), [16], [276])
        headers.append(dict(frame=frame, text=text, capture_report=str(report_path),
            capture_report_sha256=sha(report_path.read_bytes()), capture=capture, origin=origin,
            complete_name_glyphs_andblank_guards_exact=True))
    menu = load(MENU)
    vm = menu['versions'][-1]['cases'][0]['native_VM']
    width = vm['minimum_width_units'] * 6
    rect = vm['native_menu_rectangle']
    x = rect[0] + 16
    captions = []
    for folder, frame, wanted in [('Hodram_B131_B150_English_20261102_B136', 4460, 0),
                                  ('Hodram_B136_second_choice_20261102', 4440, 1)]:
        report_path = Path('work/emulation_v193') / folder / 'capture_report.json'
        report = load(report_path)
        capture = next(c for c in report['frames_captured'] if c['frame'] == frame)
        image = Image.open(capture['path']).convert('RGB')
        labels = []
        for index in range(2):
            plane = next(p for p in menu['records'] if p['version'] == 'reviewed-English' and p['option'] == index and p['style'] == 1)
            ink = mask(plane['path'], plane['sha256'], width)
            y = 192 + rect[1] + 16 + 20 * index
            assert match(image, ink, (8, 8, 8), [x], [y]) == [x, y]
            blank = {(xx, yy) for yy in range(y - 4, y + 16) for xx in range(x, x + width)} - {(x + xx, y + yy) for xx, yy in ink}
            expected_rgb = (0, 165, 172) if index == wanted else (205, 198, 180)
            assert all(image.getpixel(p) == expected_rgb for p in blank)
            labels.append(dict(index=index, text=vm['labels'][index], origin=[x, y], selected=index == wanted,
                               complete_caption_andhighlight_rectangle_exact=True))
        captions.append(dict(frame=frame, capture_report=str(report_path), capture_report_sha256=sha(report_path.read_bytes()),
            capture=capture, labels=labels, selected_option=wanted, all_two_complete_caption_glyphs_andblank_guards_exact=True,
            all_highlight_background_RGB_exact=True))
    ROOT.mkdir(parents=True)
    save(ROOT / 'focused_actual_pixels.json', dict(body_pages=bodies, observed_record_page_equivalence=sorted(observed),
        required_distinct_display_cases=required, name_headers=headers, menu_samples=captions,
        all_required_distinct_display_cases_match=True, both_two_choice_highlights_anddecline_branch_observed=True,
        B143_Rafael_actor0_portrait_name_andsmile_visually_observed=True,
        B142_source_embedded_Foreign_Girl_heading_andFI_expansion_observed=True,
        other_conditional_paths_andseven_other_personalities_not_individually_activated=True,
        all_three_changed_full_catalogue_UIs_unvisited=True, actual_gameplay=True,
        disclosed_initialized_fixtures=True, natural_activation=False, hardware_verification=False,
        B133_post_dialogue_battle_fixture_limitation_separately_source_controlled=True,
        unbound_identical_text_not_relabelled_as_exact_source_occurrence=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [NATIVE, *SHEETS, NAMES, MENU, Path(__file__)]}))
    print(dict(exact_body_capture_planes=len(bodies), distinct_record_page_equivalences=len(observed),
               exact_headers=len(headers), complete_two_choice_highlights=len(captions), all_required_cases_pass=True))


if __name__ == '__main__':
    main()
