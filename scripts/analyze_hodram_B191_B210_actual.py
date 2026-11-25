"""Compare focused coldboot pixels against reviewed native bodies, names and menus."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_hodram_B91_B110_actual_pixels import mask, match

ROOT = Path('work/analysis/Hodram_B191_B210_actual_pixels_20261104')
INPUT = Path('work/analysis/Hodram_B191_B210_storage_inputs_20261104')
STORED = Path('work/analysis/Hodram_B191_B210_stored_20261104/stored_native_verification.json')
NAMES = Path('work/analysis/Hodram_B191_B210_scoped_name_planes_20261104/native_name_planes.json')
MENUS = Path('work/analysis/Hodram_B191_B210_menus_20261104/complete_choice_objects.json')
FIXTURES = Path('work/analysis/Hodram_B191_B210_actual_fixtures_20261104')
RUNS = ['town_exchanges', 'book_offer', 'book_delegate', 'castle_letter', 'parrot', 'earrings']
# These native item-award effects are retained commands, not SC1 speech objects.
# They delimit neither a new editorial record nor the end of the copied scene.
INTERSTITIALS = dict(book_offer='Shakuntala acquired!        ', book_delegate='Shakuntala acquired!        ',
    castle_letter='Shachihoko acquired!        ', parrot='Rainbow Parrot acquired!        ',
    earrings='Ceramic Earrings acquired!        ')


def checked_run(key):
    terminal_path = Path(f'work/analysis/Hodram_B191_B210_{key}_run_20261104/terminal.json')
    fixture_path = FIXTURES / (key + '_fixture.json')
    terminal, fixture = map(load, [terminal_path, fixture_path])
    assert terminal['terminal'] and terminal['frames'] == fixture['frames']
    report_path, observer_path = Path(terminal['report']), Path(terminal['observer'])
    assert sha(report_path.read_bytes()) == terminal['report_sha256']
    assert sha(observer_path.read_bytes()) == terminal['observer_sha256']
    report, observer = map(load, [report_path, observer_path])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert not report['callback_errors'] and not observer['errors'] and not observer['mismatches']
    assert observer['all_host_slots_restored_and_core_file_exact']
    assert report['ROM_sha256'] == fixture['research_ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
    assert sha(Path(fixture['inputs']).read_bytes()) == fixture['inputs_sha256']
    receipt = dict(key=key, frames=report['frames'], terminal=str(terminal_path), terminal_sha256=sha(terminal_path.read_bytes()),
        report=str(report_path), report_sha256=sha(report_path.read_bytes()), observer=str(observer_path), observer_sha256=sha(observer_path.read_bytes()),
        fixture=str(fixture_path), fixture_sha256=sha(fixture_path.read_bytes()))
    return fixture, report, observer, receipt


def main():
    assert not ROOT.exists()
    native, stored, names, menus = map(load, [INPUT / 'all352_native_pages.json', STORED, NAMES, MENUS])
    stored_by = {r['id']: r for r in stored['records']}
    consumers = {r['actor_ID']: r['text'] for r in names['consumer_bindings'] if r['consumer'] == 'progressive-nameplate'}
    name_planes = {r['text']: r for r in names['planes']}
    pages_by_id, native_pages, suffixes = {}, {}, {}
    for row in native['records']:
        width = 228 if row['kind'] == 'system-FE' else 216
        display = row['complete_native_English_display']
        pages = [display] if width == 228 else display['pages']
        expanded = bytes.fromhex(stored_by[row['id']]['expanded_hex'])
        pages_by_id[row['id']] = []
        for number, page in enumerate(pages, 1):
            path = Path(page['native_plane'])
            raw = path.read_bytes()
            assert sha(raw) == page['native_plane_sha256'] and len(raw) == width * 64
            identity = row['id'], number
            native_pages[identity] = dict(id=row['id'], page=number, kind=row['kind'], width=width,
                native_plane=str(path), native_plane_sha256=sha(raw), pixel_mask_sha256=sha(bytes(bool(v) for v in raw)))
            body = expanded[page.get('start', 0):].hex()
            pages_by_id[row['id']].append((body, identity))
            suffixes.setdefault(body, []).append(identity)
    runs, bodies, headers, intervals, observations, reports, findings = [], [], [], {}, {}, {}, []
    sequence_proofs, header_seen, menu_samples = {}, set(), []
    # Whole native menu objects remain source-bound; repeated town price objects reuse them.
    menu_planes = []
    for obj in menus['objects']:
        if obj['exact_complete_object_andcode_dependencies_reused']:
            continue
        p = Path(obj['receipt']); assert sha(p.read_bytes()) == obj['receipt_sha256']
        proof = load(p)
        vm = (proof['versions'] if obj['count'] == 2 else proof['menus'][0]['versions'])[-1]['cases'][0]['native_VM']
        width, rect = vm['minimum_width_units'] * 6, vm['native_menu_rectangle']
        planes = [next(r for r in proof['records'] if r['version'] == 'reviewed-English' and r['option'] == i and r['style'] == 1)
            for i in range(obj['count'])]
        menu_planes.append(dict(block=obj['block'], source_command_offset=obj['source_command_offset'], vm=vm, width=width,
            rect=rect, planes=planes, masks=[mask(p['path'], p['sha256'], width) for p in planes]))
    for key in RUNS:
        fixture, report, observer, receipt = checked_run(key)
        runs.append(receipt); reports[key] = report
        ids = {r['id'] for r in fixture['selected_records']}
        allowed = {raw: [i for i in choices if i[0] in ids] for raw, choices in suffixes.items()}
        allowed = {raw: choices for raw, choices in allowed.items() if choices}
        effect_bodies = {INTERSTITIALS[key].encode('ascii').hex()} if key in INTERSTITIALS else set()
        if effect_bodies:
            assert any(c['word'] == 0xa000 for c in fixture['copied_commands'])
        paints = [r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] >= 2800]
        first = next(i for i, row in enumerate(paints) if row['text_hex'] in allowed)
        stop = next((i for i in range(first, len(paints)) if paints[i]['text_hex'] not in allowed and paints[i]['text_hex'] not in effect_bodies), len(paints))
        target = paints[first:stop]
        start, end = target[0]['frame'], paints[stop]['frame'] if stop < len(paints) else report['frames'] + 1
        observations[key] = target
        intervals[key] = dict(first_target_frame=start, first_following_nonfixture_modal_frame=end, target_modal_paints=len(target),
            following_text=paints[stop]['text_CP932'] if stop < len(paints) else None,
            source_item_effect_modal_calls=[dict(frame=r['frame'], text=r['text_CP932'], not_editorial_speech_credit=True)
                for r in target if r['text_hex'] in effect_bodies])
        ordered_ids = {}
        if key in ['town_exchanges', 'castle_letter', 'parrot']:
            expected = [item for r in fixture['selected_records'] for item in pages_by_id[r['id']]]
            speech_calls = [r for r in target if r['text_hex'] not in effect_bodies]
            assert [r['text_hex'] for r in speech_calls] == [raw for raw, _ in expected], (key, len(speech_calls), len(expected))
            assert len({r['frame'] for r in speech_calls}) == len(speech_calls)
            ordered_ids = {paint['frame']: identity for paint, (_, identity) in zip(speech_calls, expected, strict=True)}
            sequence_proofs[key] = dict(calls=len(expected), complete_ordered_calls_match_all_copied_source_speeches=True)
        for capture in report['frames_captured']:
            frame = capture['frame']
            if not start <= frame < end:
                continue
            active = next(r for r in reversed(target) if r['frame'] <= frame)
            if active['text_hex'] in effect_bodies:
                continue
            candidates = allowed[active['text_hex']]
            if ordered_ids:
                candidates = [identity for identity in candidates if identity == ordered_ids[active['frame']]]
                assert candidates
            image_path = Path(capture['path'])
            assert sha(image_path.read_bytes()) == capture['PNG_sha256']
            im = Image.open(image_path).convert('RGB')
            found = []
            for identity in candidates:
                page = native_pages[identity]
                crop = im.crop((16, 296, 16 + page['width'], 360))
                if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) == page['pixel_mask_sha256']:
                    found.append(page)
            if found:
                bodies.append(dict(run=key, frame=frame, capture=capture, origin=[16, 296], native_equivalent_candidates=found,
                    ambiguous_occurrence=len(found) != 1, live_modal_frame=active['frame'], live_modal_body_hex=active['text_hex'],
                    ordered_fixture_record_id=ordered_ids.get(active['frame']),
                    occurrence_evidence='complete ordered copied scene commands and native body calls' if ordered_ids else 'native body and pixel equivalence within declared fixture',
                    complete_native_glyph_plane_andblank_guards_equal=True,
                    bounded_framebuffer_comparison_no_backing_RAM_VRAM_orregister_ownership_claim=True))
                if len(found) == 1:
                    binding = next(r for r in fixture['selected_records'] if r['id'] == found[0]['id'])
                    actor = binding['selector']
                    if actor != 254 and (key, actor) not in header_seen:
                        text = consumers[actor]; plane = name_planes[text]
                        try:
                            origin = match(im, mask(plane['native_plane'], plane['native_plane_sha256'], 216), (98, 97, 98), [16], [276])
                        except AssertionError as exc:
                            findings.append(dict(kind='header-plane-mismatch', run=key, frame=frame, actor=actor, text=text, diagnostic=str(exc)))
                        else:
                            header_seen.add((key, actor))
                            headers.append(dict(run=key, frame=frame, text=text, actor_ID=actor, capture=capture, origin=origin,
                                complete_name_glyphs_andblank_guards_exact=True))
            for obj in menu_planes:
                if obj['block'] not in fixture['selected_source_blocks']:
                    continue
                labels, selected = [], []
                try:
                    for index, ink in enumerate(obj['masks']):
                        x, y = obj['rect'][0] + 16, 192 + obj['rect'][1] + 16 + 20 * index
                        match(im, ink, (8, 8, 8), [x], [y])
                        blank = {(xx, yy) for yy in range(y - 4, y + 16) for xx in range(x, x + obj['width'])} - {(x + xx, y + yy) for xx, yy in ink}
                        colors = {im.getpixel(point) for point in blank}
                        if colors == {(0, 165, 172)}: selected.append(index)
                        else: assert colors == {(205, 198, 180)}
                        labels.append(dict(index=index, text=obj['vm']['labels'][index], origin=[x, y]))
                    if len(selected) == 1:
                        menu_samples.append(dict(run=key, frame=frame, capture=capture, block=obj['block'],
                            source_command_offset=obj['source_command_offset'], labels=labels, selected_option=selected[0],
                            all_complete_caption_glyphs_blank_guards_andhighlight_RGB_exact=True))
                except AssertionError:
                    pass  # Partial typing/cursor phases are observations, never complete-caption credit.
    observed = {(c['id'], c['page']) for row in bodies for c in row['native_equivalent_candidates']}
    required = [(f'DK4_MES_B210_R{index:04d}', page) for index in [37, 70] for page in [1, 2]]
    required += [('DK4_MES_B208_R0065', 1)]
    missing = [identity for identity in required if identity not in observed]
    branches = [dict(run=key, responses=[dict(frame=r['frame'], text=r['text_CP932']) for r in observations[key] if 5440 <= r['frame'] < 7000])
        for key in ['book_offer', 'book_delegate']]
    assert branches[0]['responses'] != branches[1]['responses']
    selected, seen = [], set()
    def include(capture, label):
        if capture['path'] not in seen:
            seen.add(capture['path']); selected.append(dict(capture=capture, label=label))
    for key in RUNS[1:]:
        signatures = set()
        for row in bodies:
            if row['run'] != key: continue
            signature = tuple((c['id'], c['page']) for c in row['native_equivalent_candidates'])
            if signature not in signatures:
                signatures.add(signature)
                include(row['capture'], key + ':' + ','.join(i.replace('DK4_MES_', '') + 'p' + str(p) for i, p in signature))
    for block in range(191, 200):
        samples = [r for r in bodies if r['run'] == 'town_exchanges' and any(c['id'].startswith('DK4_MES_B' + str(block) + '_') for c in r['native_equivalent_candidates'])]
        assert samples, block
        include(samples[0]['capture'], f'town B{block} opening'); include(samples[-1]['capture'], f'town B{block} ending')
    seen_menus = set()
    for row in menu_samples:
        signature = row['run'], row['source_command_offset'], row['selected_option']
        if signature not in seen_menus:
            seen_menus.add(signature); include(row['capture'], row['run'] + ' menu ' + str(row['source_command_offset']) + ' index ' + str(row['selected_option']))
    ROOT.mkdir()
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12); sheets = []
    for at in range(0, len(selected), 12):
        part = selected[at:at + 12]; sheet = Image.new('RGB', (768, math.ceil(len(part) / 3) * 216), '#eeeeee'); draw = ImageDraw.Draw(sheet)
        for index, item in enumerate(part):
            x, y = index % 3 * 256, index // 3 * 216
            im = Image.open(item['capture']['path']).convert('RGB')
            sheet.paste(im.crop((0, 192, 256, 384)), (x, y + 24))
            draw.text((x + 2, y + 2), item['label'][:34] + '@' + str(item['capture']['frame']), fill='black', font=font)
        path = ROOT / f'actual_QA_{at // 12 + 1:02d}.png'; sheet.resize((1536, sheet.height * 2), Image.Resampling.NEAREST).save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes()), captures=part))
    save(ROOT / 'focused_actual_pixels.json', dict(runs=runs, body_pages=bodies, name_headers=headers, menu_samples=menu_samples,
        review_sheets=sheets, branch_responses=branches, target_capture_intervals=intervals, ordered_linear_scene_sequences=sequence_proofs,
        observed_record_page_equivalence=sorted(observed), required_distinct_display_cases=required, missing_required_cases=missing,
        header_findings=findings, all_required_distinct_display_cases_match=not missing and not findings,
        actual_frames=sum(r['frames'] for r in runs), actual_gameplay=True, disclosed_initialized_fixtures=True,
        natural_activation=False, hardware_verification=False, guide_photos=False,
        other_story_conditions_full_catalogue_item_city_widgets_andoriginal_town_layout_unvisited=True,
        direct_visual_review_pending=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [INPUT / 'all352_native_pages.json', STORED, NAMES, MENUS, Path(__file__)]}))
    print(dict(body_capture_planes=len(bodies), observed_record_pages=len(observed), headers=len(headers), menus=len(menu_samples),
        menu_cases=sorted(seen_menus), sheets=len(sheets), missing=missing, header_findings=len(findings)))


if __name__ == '__main__':
    main()
