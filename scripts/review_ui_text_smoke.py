"""Verify candidate-bound captures, complete glyph masks and runtime helpers.

An explicit checks JSON binds expected text to reviewed screens. Contact sheets
are review aids; emitting them never sets visual/hardware acceptance to true.
"""
import argparse
import hashlib
import json
import struct
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / '.deps'), str(REPO / '.runtime_deps')]
from ndspy.code import MainCodeFile
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def verify_runtime_helpers(section, observed, ram):
    """Allow only the two declared cache words; validate initialized ownership."""
    assert len(section) == len(observed) == 4096 and len(ram) == 0x400000
    actual = bytearray(observed)
    footer = struct.unpack_from('<I', actual, 0x2D8)[0]
    assert footer == 0 or 0x02000000 <= footer <= 0x02400000 - 1792
    actual[0x2D8:0x2DC] = section[0x2D8:0x2DC]
    market = struct.unpack_from('<I', actual, 0x680)[0]
    if market:
        assert struct.unpack_from('<I', section, 0x194)[0] == 0x01FFC680
        assert 0x02000000 <= market <= 0x02400000 - 4096
        header = struct.unpack_from('<5I', ram, market - 0x02000000)
        assert header[:3] == (4, 46, 36) and header[4] == 32
        assert (market + header[3]) & 0xFFFFFFFF == 0x02125A20
    actual[0x680:0x684] = section[0x680:0x684]
    assert actual == section, 'Immutable runtime helper bytes changed'
    return dict(immutable_helper_bytes_verified=4088, mutable_cache_bytes=8,
                footer_cache=footer, market_cache=market,
                market_cache_header_validated=bool(market))


def complete_mask(font, text, image, region, advance=6, color=None):
    width = (len(text) - 1) * advance + 6
    expected = Image.new('1', (width, 11))
    for index, character in enumerate(text):
        glyph = font.decode(character)
        for y in range(11):
            for x in range(6):
                if glyph.getpixel((x, y)):
                    expected.putpixel((index * advance + x, y), 1)
    inks = [(x, y) for y in range(11) for x in range(width) if expected.getpixel((x, y))]
    assert inks, 'Do not use an empty/all-blank text as a visible-text oracle'
    colors = [tuple(color)] if color else [c for c, _ in Counter(image.crop(region).get_flattened_data()).most_common(24)]
    pixels = image.load()
    for foreground in colors:
        for sy in range(region[1], region[3] - 10):
            for sx in range(region[0], region[2] - width + 1):
                if not all(pixels[sx + x, sy + y] == foreground for x, y in inks[::max(1, len(inks) // 10)]):
                    continue
                if all((pixels[sx + x, sy + y] == foreground) == bool(expected.getpixel((x, y)))
                       for y in range(11) for x in range(width)):
                    return dict(text=text, bounds=[sx, sy, sx + width, sy + 11], color=list(foreground),
                                advance=advance, ink_pixels=len(inks), complete_ink_and_blank_cells=True)
    raise AssertionError(('No complete glyph mask', text, region, advance))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom', type=Path, required=True)
    p.add_argument('--expect-sha256', required=True)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--checks', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    assert sha(args.rom) == args.expect_sha256
    if args.out.exists():
        p.error('Use a new review output folder')
    args.out.mkdir(parents=True)
    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    original_font = None
    if any(c.get('font') == 'original' for c in read(args.checks)['checks']):
        assert sha('work/clean.nds') == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
        original_font = GameAsciiFont.from_arm9(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    section = bytes(MainCodeFile(arm, 0x02000000).sections[4].data)
    spec = read(args.checks)
    reports, frames, runs = {}, {}, []
    for folder in spec['runs']:
        report_path = args.root / folder / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == args.expect_sha256
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
        captures = {}
        for row in report['frames_captured']:
            assert sha(row['path']) == row['PNG_sha256']
            assert Image.open(row['path']).size == (256, 384)
            captures[row['frame']] = row
        state = report['read_only_native_state']
        actual = Path(state['regions']['ITCM']['path']).read_bytes()[0x4000:0x5000]
        raw = Path(args.root / folder / 'final_arm9_ram.bin').read_bytes()
        # Existing Market name helper owns a second cached heap pointer. Its
        # declaration/allocation is in prepare_commodity_private_market_v353.py;
        # this is data, not an instruction or general-purpose writable region.
        helper_proof = verify_runtime_helpers(section, actual, raw)
        assert all(raw[at:at + 4] == arm[at:at + 4] for at in [0xD1738, 0xD17F4])
        battery = report.get('battery_save_preloaded')
        if battery:
            assert sha(battery['source']) == battery['source_sha256']
        fixtures = {k: v for k, v in report.items() if k.startswith('synthetic_') and v}
        if folder.startswith('results'):
            assert set(fixtures) == {'synthetic_battle_recovery_proximity_fixtures'}
            values = fixtures['synthetic_battle_recovery_proximity_fixtures']
            assert len(values) == 2 and all(v['action'] == 'approach' and len(v['owned_bytes']) == 8 for v in values)
        else:
            assert not fixtures, ('Unexpected gameplay fixture', folder)
        reports[folder], frames[folder] = report, captures
        runs.append(dict(folder=folder, frames=report['frames'], captured_frames=len(captures),
                         capture_report_sha256=sha(report_path),
                         **helper_proof,
                         runtime_column_branches_exact=True, source_battery_unchanged=bool(battery),
                         synthetic_fixture_kinds=list(fixtures)))
    masks, pictures, failures = [], {}, []
    for check in spec['checks']:
        folder, frame = check['run'], check['frame']
        path = frames[folder][frame]['path']
        image = Image.open(path).convert('RGB')
        pictures[folder, frame] = image
        try:
            selected_font = original_font if check.get('font') == 'original' else font
            assert check.get('font', 'candidate') in ('candidate', 'original')
            result = complete_mask(selected_font, check['text'], image, check['region'],
                                   check.get('advance', 6), check.get('color'))
            if 'expected_y' in check:
                assert result['bounds'][1] == check['expected_y'], 'Vertical placement changed'
            masks.append(dict(run=folder, frame=frame, font=check.get('font', 'candidate'), **result))
        except AssertionError as error:
            failures.append(dict(check=check, error=str(error)))
    comparisons = []
    blank_bands = []
    for check in spec.get('blank_bands', []):
        image = Image.open(frames[check['run']][check['frame']]['path']).convert('RGB')
        color = tuple(check['color'])
        passed = all(pixel != color for pixel in image.crop(check['region']).get_flattened_data())
        blank_bands.append(dict(check, passed=passed))
        if not passed:
            failures.append(dict(blank_band=check, error='Unexpected foreground below glyph rows'))
    for check in spec.get('comparisons', []):
        first = Image.open(frames[check['run']][check['frame']]['path']).convert('RGB')
        second = Image.open(frames[check['other_run']][check['other_frame']]['path']).convert('RGB')
        pictures[check['run'], check['frame']] = first
        pictures[check['other_run'], check['other_frame']] = second
        equal = first.crop(check['region']).tobytes() == second.crop(check['region']).tobytes()
        passed = equal == (check['expect'] == 'equal')
        comparisons.append(dict(check, passed=passed))
        if not passed:
            failures.append(dict(comparison=check, error='Region equality differs from expectation'))
    for folder in spec['runs']:
        selected = [(f, im) for (r, f), im in pictures.items() if r == folder]
        for first in range(0, len(selected), 12):
            chunk = selected[first:first + 12]
            sheet = Image.new('RGB', (4 * 256, ((len(chunk) + 3) // 4) * 408), '#182b36')
            draw = ImageDraw.Draw(sheet)
            for index, (frame, image) in enumerate(chunk):
                x, y = index % 4 * 256, index // 4 * 408
                draw.text((x + 4, y + 4), f'{folder} {frame}', fill='white')
                sheet.paste(image, (x, y + 24))
            sheet.save(args.out / f'{folder}_{first // 12 + 1}.png')
    proof = dict(ROM_sha256=args.expect_sha256, checks_source_sha256=sha(args.checks), runs=runs,
                 masks=masks, comparisons=comparisons, blank_bands=blank_bands,
                 failures=failures, status='failed' if failures else 'passed',
                 direct_visual_review_recorded_separately=True, hardware_verification=False,
                 complete_gameplay_or_all_UI_coverage=False)
    (args.out / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(len(masks), 'complete live masks;', len(failures), 'failures;', len(runs), 'candidate-bound runs')
    assert not failures, 'Pixel failures retained in proof.json'


if __name__ == '__main__':
    main()
