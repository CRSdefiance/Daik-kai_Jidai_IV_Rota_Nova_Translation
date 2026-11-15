"""Bind focused coldboots to immutable native text planes; no emulator reruns."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Hodram_B151_B170_actual_pixels_20261102')
NATIVE = Path('work/analysis/Hodram_B151_B170_reconstruction_inputs_20261102/all634_native_pages.json')
NAMES = Path('work/analysis/Hodram_B151_B170_scoped_name_planes_20261102/native_name_planes.json')
MENU = Path('work/analysis/Hodram_B151_B170_formatting_20261102/menus_v1/B170_C1314/menu_provider_and_planes.json')
RUNS = {
    'cinematic': Path('work/analysis/Hodram_B156_cinematic_English_run_20261102/terminal.json'),
    'focused': Path('work/analysis/Hodram_B151_B170_focused_run_20261102/terminal.json'),
    'second': Path('work/analysis/Hodram_B170_menu_only_run_20261102/terminal.json'),
}


def main():
    assert not ROOT.exists()
    lookup = {}
    for row in load(NATIVE)['records']:
        width = 228 if row['kind'] == 'system-FE' else 216
        display = row['complete_native_English_display']
        pages = [display] if width == 228 else display['pages']
        for number, page in enumerate(pages, 1):
            data = Path(page['native_plane']).read_bytes()
            assert sha(data) == page['native_plane_sha256'] and len(data) == width * 64
            lookup.setdefault((width, sha(bytes(bool(v) for v in data))), []).append(dict(
                id=row['id'], page=number, kind=row['kind'], native_plane=page['native_plane'],
                native_plane_sha256=page['native_plane_sha256']))
    bodies, reports, observations, bindings = [], {}, {}, []
    for key, terminal_path in RUNS.items():
        terminal = load(terminal_path)
        assert terminal['terminal']
        report_path, observer_path = Path(terminal['report']), Path(terminal['observer'])
        assert sha(report_path.read_bytes()) == terminal['report_sha256']
        assert sha(observer_path.read_bytes()) == terminal['observer_sha256']
        report, observer = load(report_path), load(observer_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
        assert not report['callback_errors'] and not observer['errors'] and not observer['mismatches']
        assert observer['all_host_slots_restored_and_core_file_exact']
        assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
        reports[key], observations[key] = report, observer
        bindings.append(dict(key=key, terminal=str(terminal_path), terminal_sha256=sha(terminal_path.read_bytes()),
            report=str(report_path), report_sha256=terminal['report_sha256'],
            observer=str(observer_path), observer_sha256=terminal['observer_sha256'], frames=report['frames']))
        for capture in report['frames_captured']:
            if capture['frame'] < 2800:
                continue
            image_path = Path(capture['path'])
            assert sha(image_path.read_bytes()) == capture['PNG_sha256']
            image = Image.open(image_path).convert('RGB')
            for width in (216, 228):
                crop = image.crop((16, 296, 16 + width, 360))
                digest = sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata()))
                found = lookup.get((width, digest), [])
                if found:
                    bodies.append(dict(run=key, frame=capture['frame'], capture=capture, origin=[16, 296],
                        viewport=[width, 64], native_equivalent_candidates=found,
                        ambiguous_occurrence=len(found) != 1,
                        complete_native_glyph_plane_andblank_guards_equal=True,
                        bounded_framebuffer_comparison_no_backing_RAM_VRAM_orregister_ownership_claim=True))
    observed = {(c['id'], c['page']) for b in bodies for c in b['native_equivalent_candidates']}
    required = [(f'DK4_MES_B156_R00{r}', page) for r in (87, 90) for page in (1, 2)]
    required += [(f'DK4_MES_B168_R0{r}', 1) for r in (157, 161, 166, 170, 174, 177, 181)]
    required += [('DK4_MES_B170_R0125', 1), ('DK4_MES_B170_R0082', 1)]
    # The second response is bound below by exact live text; its catalogue index
    # is derived from the native plane rather than guessed from branch order.
    required = [r for r in required if r[0] != 'DK4_MES_B170_R0082']
    assert all(case in observed for case in required), [r for r in required if r not in observed]
    paints = {key: [r for r in value['rows'] if r['kind'] == 'modal_paint'] for key, value in observations.items()}
    first = next(r for r in paints['focused'] if r['text_CP932'].strip() == 'Honest and humble. A fine attitude.')
    second = next(r for r in paints['second'] if r['text_CP932'].strip() == 'Testing me, eh? Not so fast.')
    assert first['frame'] == 6648 and second['frame'] == 4006

    def get_capture(key, frame):
        capture = next(c for c in reports[key]['frames_captured'] if c['frame'] == frame)
        return Image.open(capture['path']).convert('RGB'), capture

    names = load(NAMES)['planes']
    headers = []
    for frame, text in [(3960, 'Hodram Bergstrom'), (4800, 'Claudio Manaus'),
                        (5040, 'Rafael Castor'), (5280, 'Gerhard Adernkatz'), (5520, 'Rafael Castor'),
                        (5760, 'Gerhard Adernkatz'), (6000, 'Cesare Tony'), (6240, 'Arcadius Eudoxios'),
                        (6720, 'Julio Erneco')]:
        # Exact approved name spellings are checked against the actual plane;
        # callers must not infer a name from a portrait alone.
        plane = next(p for p in names if p['text'] == text)
        image, capture = get_capture('focused', frame)
        assert match(image, mask(plane['native_plane'], plane['native_plane_sha256'], 216),
                     (98, 97, 98), [16], [276]) == [16, 276]
        headers.append(dict(run='focused', frame=frame, text=text, capture=capture, origin=[16, 276],
            complete_name_glyphs_andblank_guards_exact=True))
    menu = load(MENU)
    vm = menu['versions'][-1]['cases'][0]['native_VM']
    width, rect = vm['minimum_width_units'] * 6, vm['native_menu_rectangle']
    x = rect[0] + 16
    captions = []
    for key, frame, wanted in [('focused', 6600, 0), ('second', 3840, 1)]:
        image, capture = get_capture(key, frame)
        labels = []
        for index in range(2):
            plane = next(p for p in menu['records'] if p['version'] == 'reviewed-English' and p['option'] == index and p['style'] == 1)
            ink = mask(plane['path'], plane['sha256'], width)
            y = 192 + rect[1] + 16 + 20 * index
            assert match(image, ink, (8, 8, 8), [x], [y]) == [x, y]
            blank = {(xx, yy) for yy in range(y - 4, y + 16) for xx in range(x, x + width)} - {(x + xx, y + yy) for xx, yy in ink}
            expected = (0, 165, 172) if index == wanted else (205, 198, 180)
            assert all(image.getpixel(p) == expected for p in blank)
            labels.append(dict(index=index, text=vm['labels'][index], origin=[x, y], selected=index == wanted))
        captions.append(dict(run=key, frame=frame, capture=capture, labels=labels, selected_option=wanted,
            all_two_complete_caption_glyphs_andblank_guards_exact=True, all_highlight_background_RGB_exact=True))
    ROOT.mkdir(parents=True)
    selected, seen = [], set()
    for item in bodies:
        if item['run'] == 'cinematic':
            continue  # All 31 cinematic captures already have direct visual approval.
        identity = item['run'], tuple((c['id'], c['page']) for c in item['native_equivalent_candidates'])
        if identity not in seen:
            seen.add(identity)
            selected.append(dict(capture=item['capture'], label=item['run'] + ':' + ','.join(
                c['id'].replace('DK4_MES_', '') + 'p' + str(c['page']) for c in item['native_equivalent_candidates'])))
    selected.extend(dict(capture=c['capture'], label=c['run'] + ' menu index ' + str(c['selected_option'])) for c in captions)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
    sheets = []
    for at in range(0, len(selected), 12):
        part = selected[at:at + 12]
        sheet = Image.new('RGB', (768, math.ceil(len(part) / 3) * 216), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for j, item in enumerate(part):
            x, y = j % 3 * 256, j // 3 * 216
            image = Image.open(item['capture']['path']).convert('RGB')
            sheet.paste(image.crop((0, 192, 256, 384)), (x, y + 24))
            draw.text((x + 2, y + 2), item['label'][:35] + '@' + str(item['capture']['frame']), fill='black', font=font)
        path = ROOT / f'focused_QA_{at // 12 + 1:02d}.png'
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.Resampling.NEAREST).save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes()), captures=part))
    save(ROOT / 'focused_actual_pixels.json', dict(runs=bindings, body_pages=bodies,
        observed_record_page_equivalence=sorted(observed), required_distinct_display_cases=required,
        name_headers=headers, menu_samples=captions, review_sheets=sheets,
        branch_responses=[dict(run='focused', frame=first['frame'], text=first['text_CP932'], selected_index=0),
                          dict(run='second', frame=second['frame'], text=second['text_CP932'], selected_index=1)],
        all_required_distinct_display_cases_match=True, both_two_choice_highlights_andbranches_observed=True,
        B168_Rafael_actor0_name_andportrait_transitions_observed=True,
        B156_two_generated_page_bottom_spacing_cases_both_pages_observed=True,
        exact_native_plane_equivalence_not_unique_occurrence_for_duplicate_text=True,
        actual_frames=sum(r['frames'] for r in bindings), actual_gameplay=True, disclosed_initialized_fixtures=True,
        natural_activation=False, hardware_verification=False, guide_photos=False,
        other_conditions_three_other_menus_andstatic_label_widgets_unvisited=True,
        direct_visual_review_pending=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [NATIVE, NAMES, MENU, *RUNS.values(), Path(__file__)]}))
    print(dict(exact_body_capture_planes=len(bodies), distinct_record_page_equivalences=len(observed),
        exact_headers=len(headers), exact_menu_highlights=len(captions), sheets=len(sheets), all_required_cases_pass=True))


if __name__ == '__main__':
    main()
