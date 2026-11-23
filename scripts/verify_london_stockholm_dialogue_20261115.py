"""Verify the changed pages and preserved ordinary town transitions."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from scripts import observe_london_riga_towns_20261115 as baseline
from scripts import stage_london_stockholm_dialogue_20261115 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.verify_captain_biographies_v1 import captured, shots


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'gameplay_comparison.png'
BODY = (16, 294, 244, 366)
HELD = {
    'london': {5051: (858, ('３０３',)), 6251: (874, ())},
    'riga': {8921: (1154, ('Bergstrom',)), 11321: (1154, ('Bergstrom',)), 12921: (1154, ('Bergstrom',))},
}


def run(folder, digest, case):
    inputs, _, end, _, donor = baseline.schedule(case)
    terminal_path, trace_path, report_path = (folder / p for p in (
        'terminal.json', 'requests.json', 'capture/capture_report.json'))
    terminal, trace, report = map(base.load, (terminal_path, trace_path, report_path))
    assert terminal['ROM_sha256'] == report['ROM_sha256'] == digest
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == inputs and report['frames'] == end
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    preload = report['battery_save_preloaded']
    assert preload['copied_byte_exact_before_cold_boot'] and preload['source_sha256'] == donor['source_sha256']
    assert base.digest(preload['source']) == donor['source_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert trace['source_requests'] == terminal['target_COMMON_calls']
    assert all(base.digest(p) == sha for p, sha in terminal['evidence'].items())
    return shots(report), trace['source_requests'], {str(terminal_path): base.digest(terminal_path)} | terminal['evidence']


def native_hold(image, plane):
    expected = {(16 + i % 228, 296 + i // 228) for i, pixel in enumerate(plane) if pixel == 1}
    visible = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
               if image.getpixel((x, y)) == (0, 8, 0)}
    assert expected == visible, (len(expected - visible), len(visible - expected))
    return len(expected)


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    stored, manuscript = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    assert base.digest(stage.MANUSCRIPT) == stored['manuscript_sha256']
    assert base.digest(stage.ROM) == stored['candidate_sha256']
    current = base.NdsImage.open(stage.ROM)
    arm, kanji = (current.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = font_tools(current)
    cases, evidence, gallery = [], {}, []
    variants = {(r['id'], tuple(r['arguments'])): r for r in manuscript['focused_native_cases']}
    for city, matching in HELD.items():
        prior, source_calls, old_e = run(baseline.ROOT / city, stored['previous_sha256'], city)
        after, current_calls, new_e = run(ROOT / city, stored['candidate_sha256'], city)
        assert source_calls == current_calls and prior.keys() == after.keys()
        assert not set(r['message_ID'] for r in current_calls) & set(
            base.load(base.LEDGER)['pending_shared_consumer_checkpoint_20261114']['remaining_legacy_keys'])
        evidence.update(old_e | new_e)
        current_frames, previous_frames = {}, {}
        equal, changed = [], []
        for frame in after:
            a, b = captured(prior[frame]), captured(after[frame])
            previous_frames[frame], current_frames[frame] = a, b
            diff = ImageChops.difference(a, b)
            evidence.update({r['path']: r['PNG_sha256'] for r in (prior[frame], after[frame])})
            if diff.getbbox() is None:
                equal.append(frame)
                continue
            left, top, right, bottom = diff.getbbox()
            assert BODY[0] <= left < right <= BODY[2] and BODY[1] <= top < bottom <= BODY[3], (city, frame, diff.getbbox())
            preceding = [r for r in current_calls if 0 <= frame - r['frame'] <= 260]
            assert preceding and preceding[-1]['message_ID'] in stage.CHOICES, (city, frame, preceding)
            changed.append(frame)
        holds = []
        for frame, (ident, args) in matching.items():
            native = variants[ident, args]
            pixels, _ = render_portrait(raster, arm, kanji, bytes.fromhex(native['formatted_hex']))
            assert stage.digest(pixels) == native['native_ink_sha256'] and frame in changed
            result = native_hold(current_frames[frame], pixels)
            holds.append(dict(frame=frame, record=ident, lines=native['lines'], complete_foreground_ink=result,
                              previous=prior[frame], revised=after[frame]))
            if city == 'london' or frame == min(matching):
                gallery.append((f'{city if city == "london" else "Stockholm"} / {ident}', previous_frames[frame], current_frames[frame]))
        cases.append(dict(route='London' if city == 'london' else 'Riga to Stockholm',
            equivalent_unmodified_input_trace=current_calls, exact_full_frames=equal,
            changed_dialogue_only_frames=changed, complete_changed_message_holds=holds))

    sheet = Image.new('RGB', (1024, 286 * len(gallery)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, (caption, a, b) in enumerate(gallery):
        for column, image in enumerate((a,b)):
            x, y = column*512, row*286
            draw.text((x+8,y+5), f'{caption} / {"Before" if column == 0 else "After"}', fill='white')
            panel = image.crop((0, 251, 256, 384)).resize((512, 266), Image.Resampling.NEAREST)
            sheet.paste(panel,(x,y+20))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=stored['candidate_sha256'], ordinary_cold_boots=True, cases=cases,
        native_sheet_seen_separately=stored['sheets'], sheet=str(SHEET), sheet_sha256=base.digest(SHEET), evidence=evidence,
        matched_source_NATIVE_requests=True, no_ROM_or_RAM_fixtures_beyond_copied_battery=True, hardware=False))
    print(sum(len(row['complete_changed_message_holds']) for row in cases), 'complete changed-message holds,',
          sum(len(row['exact_full_frames']) for row in cases), 'identical frames.')


if __name__ == '__main__':
    main()
