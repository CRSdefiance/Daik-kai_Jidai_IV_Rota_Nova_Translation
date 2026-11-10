"""Bind actual coldboot captures to stored native bodies, names and controller menus."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Hodram_B171_B190_actual_pixels_20261104')
NATIVE = Path('work/analysis/Hodram_B171_B190_storage_inputs_20261104/all433_native_pages.json')
STORED = Path('work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json')
NAMES = Path('work/analysis/Hodram_B171_B190_scoped_name_planes_20261104/native_name_planes.json')
MENU = Path('work/analysis/Hodram_B171_B190_menu_20261104/B171_C154/menu_provider_and_planes.json')
FIXTURES = Path('work/analysis/Hodram_B171_B190_actual_fixtures_20261104')
RUNS = dict(sail='sail_lesson', pirate='pirate_transition', town='town_exchanges', refusal='sail_refusal')


def main():
    assert not ROOT.exists() or not any(ROOT.iterdir())
    native, stored, names, menu = map(load, [NATIVE, STORED, NAMES, MENU])
    native_by = {r['id']: r for r in native['records']}
    stored_by = {r['id']: r for r in stored['records']}
    consumers = {r['actor_ID']: r['text'] for r in names['consumer_bindings'] if r['consumer'] == 'progressive-nameplate'}
    name_planes = {r['text']: r for r in names['planes']}
    native_pages = {}
    suffixes = {}
    for row in native['records']:
        width = 228 if row['kind'] == 'system-FE' else 216
        display = row['complete_native_English_display']
        pages = [display] if width == 228 else display['pages']
        expanded = bytes.fromhex(stored_by[row['id']]['expanded_hex'])
        for number, page in enumerate(pages, 1):
            path = Path(page['native_plane'])
            raw = path.read_bytes()
            assert sha(raw) == page['native_plane_sha256'] and len(raw) == width * 64
            identity = row['id'], number
            native_pages[identity] = dict(id=row['id'], page=number, kind=row['kind'], width=width,
                native_plane=str(path), native_plane_sha256=sha(raw), pixel_mask_sha256=sha(bytes(bool(v) for v in raw)))
            start = page.get('start', 0)
            suffixes.setdefault(expanded[start:].hex(), []).append(identity)
    ROOT.mkdir(exist_ok=True)
    bodies, headers, runs, reports, observations, intervals = [], [], [], {}, {}, {}
    header_seen = set()
    findings = []
    for key, fixture_name in RUNS.items():
        terminal_path = Path(f'work/analysis/Hodram_B171_B190_{key}_run_20261104/terminal.json')
        terminal = load(terminal_path)
        fixture_path = FIXTURES / (fixture_name + '_fixture.json')
        fixture = load(fixture_path)
        assert terminal['terminal'] and terminal['frames'] == fixture['frames']
        report_path, observer_path = Path(terminal['report']), Path(terminal['observer'])
        assert sha(report_path.read_bytes()) == terminal['report_sha256']
        assert sha(observer_path.read_bytes()) == terminal['observer_sha256']
        report, observer = map(load, [report_path, observer_path])
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
        assert not report['callback_errors'] and not observer['errors'] and not observer['mismatches']
        assert observer['all_host_slots_restored_and_core_file_exact']
        assert report['ROM_sha256'] == fixture['research_ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
        ids = {r['id'] for r in fixture['selected_records']}
        allowed = {raw: [i for i in choices if i[0] in ids] for raw, choices in suffixes.items()}
        allowed = {raw: choices for raw, choices in allowed.items() if choices}
        paints = [r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] >= 2800]
        start_index = next(i for i, row in enumerate(paints) if row['text_hex'] in allowed)
        end_index = next((i for i in range(start_index, len(paints)) if paints[i]['text_hex'] not in allowed), len(paints))
        target_paints = paints[start_index:end_index]
        start = target_paints[0]['frame']
        end = paints[end_index]['frame'] if end_index < len(paints) else report['frames'] + 1
        intervals[key] = dict(first_target_frame=start, first_following_nonfixture_modal_frame=end,
            target_modal_paints=len(target_paints), following_text=paints[end_index]['text_CP932'] if end_index < len(paints) else None)
        if key in ['town', 'pirate']:
            assert [r['text_hex'] for r in target_paints] == [r['expected_expanded_body_hex'] for r in fixture['selected_records']], key
        observations[key] = target_paints
        reports[key] = report
        runs.append(dict(key=key, terminal=str(terminal_path), terminal_sha256=sha(terminal_path.read_bytes()),
            report=str(report_path), report_sha256=sha(report_path.read_bytes()),
            observer=str(observer_path), observer_sha256=sha(observer_path.read_bytes()),
            fixture=str(fixture_path), fixture_sha256=sha(fixture_path.read_bytes()), frames=report['frames']))
        for capture in report['frames_captured']:
            frame = capture['frame']
            if not start <= frame < end:
                continue
            active = next((r for r in reversed(target_paints) if r['frame'] <= frame), None)
            assert active is not None
            candidates = allowed[active['text_hex']]
            image_path = Path(capture['path'])
            assert sha(image_path.read_bytes()) == capture['PNG_sha256']
            image = Image.open(image_path).convert('RGB')
            found = []
            for identity in candidates:
                page = native_pages[identity]
                crop = image.crop((16, 296, 16 + page['width'], 360))
                digest = sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata()))
                if digest == page['pixel_mask_sha256']:
                    found.append(page)
            if not found:
                continue  # Typing, menu/transition and partial-page frames receive no complete-plane credit.
            bodies.append(dict(run=key, frame=frame, capture=capture, origin=[16, 296],
                native_equivalent_candidates=found, ambiguous_occurrence=len(found) != 1,
                live_modal_frame=active['frame'], live_modal_body_hex=active['text_hex'],
                complete_native_glyph_plane_andblank_guards_equal=True,
                bounded_framebuffer_comparison_no_backing_RAM_VRAM_orregister_ownership_claim=True))
            # Name attribution is source-bound only for a unique body/fixture candidate.
            if len(found) == 1:
                binding = next(r for r in fixture['selected_records'] if r['id'] == found[0]['id'])
                actor = binding['selector']
                if actor != 254 and (key, actor) not in header_seen:
                    text = consumers[actor]
                    plane = name_planes[text]
                    try:
                        origin = match(image, mask(plane['native_plane'], plane['native_plane_sha256'], 216), (98, 97, 98), [16], [276])
                    except AssertionError as exc:
                        findings.append(dict(kind='header-plane-mismatch', run=key, frame=frame, actor=actor, text=text, diagnostic=str(exc)))
                    else:
                        header_seen.add((key, actor))
                        headers.append(dict(run=key, frame=frame, text=text, actor_ID=actor, capture=capture, origin=origin,
                            complete_name_glyphs_andblank_guards_exact=True))
    observed = {(candidate['id'], candidate['page']) for row in bodies for candidate in row['native_equivalent_candidates']}
    required = [('DK4_MES_B171_R0068', 1), ('DK4_MES_B171_R0101', 1), ('DK4_MES_B179_R0047', 1)]
    required += [(f'DK4_MES_B171_R00{index}', page) for index in [75, 95, 98] for page in [1, 2]]
    missing = [identity for identity in required if identity not in observed]
    menu_samples = []
    vm = menu['versions'][-1]['cases'][0]['native_VM']
    width, rect = vm['minimum_width_units'] * 6, vm['native_menu_rectangle']
    dense_terminal = Path('work/analysis/Hodram_B171_menu_highlight_run_20261104/terminal.json')
    dense = load(dense_terminal)
    assert dense['terminal'] and dense['frames'] == 5001
    dense_report = load(dense['report'])
    dense_observer = load(dense['observer'])
    assert sha(Path(dense['report']).read_bytes()) == dense['report_sha256']
    assert sha(Path(dense['observer']).read_bytes()) == dense['observer_sha256']
    assert dense_report['cold_boot'] and not dense_report['savestate_loaded'] and not dense_report['callback_errors']
    assert not dense_observer['errors'] and not dense_observer['mismatches'] and dense_observer['all_host_slots_restored_and_core_file_exact']
    assert dense_report['ROM_sha256'] == reports['sail']['ROM_sha256']
    runs.append(dict(key='highlight', terminal=str(dense_terminal), terminal_sha256=sha(dense_terminal.read_bytes()),
        report=dense['report'], report_sha256=dense['report_sha256'], observer=dense['observer'],
        observer_sha256=dense['observer_sha256'], frames=5001,
        purpose='Only denser read-only sampling of the existing menu cursor phases; no ROM or input change.'))
    for key, wanted, frame in [('sail', 0, 4498), ('refusal', 1, 4680)]:
        capture_report = dense_report if key == 'sail' else reports[key]
        capture = next(c for c in capture_report['frames_captured'] if c['frame'] == frame)
        assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
        image = Image.open(capture['path']).convert('RGB')
        labels = []
        for index in range(2):
            plane = next(p for p in menu['records'] if p['version'] == 'reviewed-English' and p['option'] == index and p['style'] == 1)
            ink = mask(plane['path'], plane['sha256'], width)
            x, y = rect[0] + 16, 192 + rect[1] + 16 + 20 * index
            assert match(image, ink, (8, 8, 8), [x], [y]) == [x, y]
            blank = {(xx, yy) for yy in range(y - 4, y + 16) for xx in range(x, x + width)} - {(x + xx, y + yy) for xx, yy in ink}
            expected = (0, 165, 172) if index == wanted else (205, 198, 180)
            assert all(image.getpixel(point) == expected for point in blank)
            labels.append(dict(index=index, text=vm['labels'][index], origin=[x, y], selected=index == wanted))
        menu_samples.append(dict(run='highlight' if key == 'sail' else key, frame=frame, capture=capture, labels=labels, selected_option=wanted,
            all_two_complete_caption_glyphs_andblank_guards_exact=True, all_highlight_background_RGB_exact=True))
    branches = []
    for key, wanted in [('sail', 0), ('refusal', 1)]:
        row = next(r for r in observations[key] if r['frame'] >= 4720)
        branches.append(dict(run=key, selected_index=wanted, frame=row['frame'], text=row['text_CP932']))
    assert branches[0]['text'] != branches[1]['text']
    selected = []
    seen = set()
    def include(capture, label):
        identity = capture['path']
        if identity not in seen:
            seen.add(identity)
            selected.append(dict(capture=capture, label=label))
    # Inspect all distinct sailed pages and pirate bodies, plus first/last town utterances.
    for key in ['sail', 'pirate', 'refusal']:
        identities = set()
        for row in bodies:
            if row['run'] != key:
                continue
            signature = tuple((c['id'], c['page']) for c in row['native_equivalent_candidates'])
            if signature not in identities:
                identities.add(signature)
                include(row['capture'], key + ':' + ','.join(i.replace('DK4_MES_', '') + 'p' + str(p) for i, p in signature))
    for block in range(180, 191):
        samples = [r for r in bodies if r['run'] == 'town' and any(c['id'].startswith('DK4_MES_B' + str(block) + '_') for c in r['native_equivalent_candidates'])]
        if samples:
            include(samples[0]['capture'], f'town B{block} opening')
            include(samples[-1]['capture'], f'town B{block} ending')
    for row in menu_samples:
        include(row['capture'], row['run'] + ' menu index ' + str(row['selected_option']))
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
    sheets = []
    for at in range(0, len(selected), 12):
        part = selected[at:at + 12]
        sheet = Image.new('RGB', (768, math.ceil(len(part) / 3) * 216), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for index, item in enumerate(part):
            x, y = index % 3 * 256, index // 3 * 216
            image = Image.open(item['capture']['path']).convert('RGB')
            sheet.paste(image.crop((0, 192, 256, 384)), (x, y + 24))
            draw.text((x + 2, y + 2), item['label'][:35] + '@' + str(item['capture']['frame']), fill='black', font=font)
        path = ROOT / f'actual_QA_{at // 12 + 1:02d}.png'
        sheet.resize((1536, sheet.height * 2), Image.Resampling.NEAREST).save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes()), captures=part))
    save(ROOT / 'focused_actual_pixels.json', dict(runs=runs, body_pages=bodies, name_headers=headers, menu_samples=menu_samples,
        review_sheets=sheets, branch_responses=branches, target_capture_intervals=intervals,
        observed_record_page_equivalence=sorted(observed), required_distinct_display_cases=required,
        missing_required_cases=missing, header_findings=findings,
        all_required_distinct_display_cases_match=not missing and not findings,
        both_two_choice_highlights_andbranches_observed=True,
        full_pirate30_andtown130_native_body_sequence_matches_copied_source_commands=True,
        actual_frames=sum(r['frames'] for r in runs), actual_gameplay=True, disclosed_initialized_fixtures=True,
        natural_activation=False, hardware_verification=False, guide_photos=False,
        other_story_conditions_andfull_catalogue_item_city_widgets_unvisited=True,
        direct_visual_review_pending=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [NATIVE, STORED, NAMES, MENU, Path(__file__)]}))
    print(dict(body_capture_planes=len(bodies), observed_record_pages=len(observed), headers=len(headers),
        menus=len(menu_samples), sheets=len(sheets), missing=missing, header_findings=len(findings)))


if __name__ == '__main__':
    main()
