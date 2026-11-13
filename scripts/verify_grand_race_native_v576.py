"""Check actual Grand Race help/menu captures without changing production art.

The save carries an authorized synthetic system unlock. These are native UI
tests, not earned-unlock, wireless-race or guide-publication evidence.
"""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.grand_race_help import format_page
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path('work/analysis/miniature_consumers_v576')
CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193/grand_race_v576_complete')
ROM = Path('out/all_routes_combined_v573_candidate.nds')
ROM_SHA = 'f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77'
PAGE_FRAMES = {
    0x1152CC: 3400, 0x1152DC: 4400, 0x1152B4: 4800,
    0x1152D4: 5200, 0x1152EC: 5600, 0x1152C4: 7000,
    0x1152BC: 7400, 0x1152AC: 8400, 0x1152FC: 8800,
}
MINIATURES = {
    'Done': (240, 40, 256, 48), 'Rank': (184, 48, 208, 56),
    'Cancel': (208, 48, 256, 56), 'Pick Cargo': (208, 32, 256, 40),
    'Pick Ship': (208, 40, 240, 48),
}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def native_string(raw, address):
    start = address - 0x02000000
    assert 0 <= start < len(raw)
    return raw[start:raw.index(0, start)]


def find_mask(font, text, image, region, color):
    """Find full ink/blank masks; precompute masks instead of repeated decoding."""
    width = len(text) * 6
    mask = Image.new('1', (width, 11))
    for i, char in enumerate(text):
        mask.paste(font.decode(char), (i * 6, 0))
    expected = [bytes(bool(mask.getpixel((x, y))) for x in range(width)) for y in range(11)]
    pixels = image.load()
    observed = [bytes(pixels[x, y] == color for x in range(256)) for y in range(384)]
    ax, ay = next((x, y) for y in range(11) for x in range(width) if mask.getpixel((x, y)))
    left, top, right, bottom = region
    matches = []
    for y in range(top, bottom - 10):
        for x in range(left, right - width + 1):
            if pixels[x + ax, y + ay] != color:
                continue
            if all(observed[y + row][x:x + width] == expected[row] for row in range(11)):
                matches.append([x, y])
    assert len(matches) == 1, (text, matches)
    x, y = matches[0]
    count, bounds = complete_mask(font, text, image, x, y, color)
    return {'text': text, 'bounds': bounds, 'native_color_5bit': list(color),
            'complete_ink_pixels': count, 'all_ink_and_blank_cells_exact': True}


def main():
    report_path = CAPTURES / 'capture_report.json'
    report = read_json(report_path)
    assert sha(ROM.read_bytes()) == report['ROM_sha256'] == ROM_SHA
    assert report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == 12200 and not report['callback_errors']
    fixtures = report['synthetic_gallery_fixtures']
    assert len(fixtures) == 1
    fixture = read_json(ROOT / 'current_save_fixture_manifest.json')
    assert not fixture['earned_unlock_verified'] and fixture['synthetic_gallery_fixture']
    assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
    assert sha(Path('work/analysis/gallery_v521/gallery-test-only.dsv').read_bytes()) == fixture['fixture_save_sha256']
    assert report['battery_save_preloaded']['source_sha256'] == fixture['fixture_save_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']

    shots = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        shots.setdefault(row['frame'], path)
    snapshots = {}
    # Explicit capture snapshots and interactive pause snapshots have separate
    # report fields. Assert both rather than assuming the filename proves origin.
    for key in ('read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots'):
        for row in report.get(key, []):
            assert row['read_only_export']
            snapshots[row['frame']] = row
    if not all(frame in snapshots for frame in PAGE_FRAMES.values()):
        raise ValueError(f'Missing report-bound RAM snapshots; report fields: {list(report)}')

    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    mapped = machine(arm)
    manuscript_path = Path('translations/grand_race_rules_manuscript_v2.json')
    manuscript = read_json(manuscript_path)
    pages = []
    for row in manuscript['records']:
        descriptor = row['descriptor_offset']
        frame = PAGE_FRAMES[descriptor]
        snapshot = snapshots[frame]
        raw = Path(snapshot['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == snapshot['sha256']
        descriptor_bytes = bytes(mapped.mem_read(0x02000000 + descriptor, 8))
        assert raw[descriptor:descriptor + 8] == descriptor_bytes
        title_pointer, body_pointer = struct.unpack('<2I', descriptor_bytes)
        title = native_string(raw, title_pointer).decode('ascii')
        _, body, lines, _ = format_page(row['english'])
        assert native_string(raw, body_pointer) == body
        assert bytes(mapped.mem_read(body_pointer, len(body) + 1)) == body + b'\0'
        image = Image.open(shots[frame]).convert('RGB').point(lambda n: n >> 3)
        title_count, title_bounds = complete_mask(font, title, image, 4, 192, (0, 31, 0))
        line_proofs = []
        expected_body = Image.new('1', (252, 128))
        for index, text in enumerate(lines):
            y = 216 + 16 * index
            count, bounds = complete_mask(font, text, image, 4, y, (28, 28, 28))
            assert bounds[2] <= 256 and bounds[3] < 364
            line_proofs.append({'text': text, 'bounds': bounds, 'complete_ink_pixels': count})
            for col, char in enumerate(text):
                expected_body.paste(font.decode(char), (col * 6, index * 16))
        for y in range(128):
            for x in range(252):
                assert (image.getpixel((x + 4, y + 216)) == (28, 28, 28)) == bool(expected_body.getpixel((x, y)))
        # Independently distinguish the observed pitch from the historical
        # 12-pixel research model without altering the release formatter.
        try:
            complete_mask(font, lines[1], image, 4, 228, (28, 28, 28))
        except ValueError:
            pass
        else:
            raise ValueError('The 12-pixel negative control unexpectedly matched')
        pages.append({'title': title, 'frame': frame, 'descriptor': 0x02000000 + descriptor,
                      'title_pointer': title_pointer, 'body_pointer': body_pointer,
                      'title_bounds': title_bounds, 'title_complete_ink_pixels': title_count,
                      'body_lines': line_proofs, 'body_row_pitch_pixels': 16,
                      'all_first_and_final_glyphs_and_blank_cells_exact': True,
                      'full_252_by_128_body_foreground_mask_exact': True,
                      'caption': str(shots[frame]), 'caption_sha256': sha(shots[frame].read_bytes()),
                      'snapshot_sha256': sha(raw)})

    menus = []
    for frame, texts, pointer_table in (
        (2400, ['Start Race', 'Read the Rules'], 0x02115354),
        (3000, ['About the Race', 'Basic Rules', 'Map & Supplies', 'Race Limits'], 0x021153A4),
    ):
        image = Image.open(shots[frame]).convert('RGB').point(lambda n: n >> 3)
        raw = Path(snapshots[frame]['path']).read_bytes()
        for index, text in enumerate(texts):
            entry = pointer_table + 16 * index
            pointer = int.from_bytes(raw[entry - 0x02000000:entry - 0x02000000 + 4], 'little')
            assert native_string(raw, pointer).decode('ascii') == text
            matches = []
            for color in ((1, 1, 1),):
                try:
                    match = find_mask(font, text, image, (75, 238, 182, 337), color)
                except AssertionError:
                    continue
                matches.append(match)
            assert len(matches) == 1, (text, matches)
            menus.append({**matches[0], 'frame': frame, 'native_string_pointer': pointer,
                          'native_menu_entry': entry})

    for original, returned, label in ((5200, 6000, 'Race Area'), (8400, 9200, 'Time Limit')):
        assert Image.open(shots[original]).tobytes() == Image.open(shots[returned]).tobytes(), label

    consumer_scans = []
    for frame in (2400, 3000, 10600, 11000, 11400, 11800):
        snapshot = snapshots[frame]
        raw = Path(snapshot['path']).read_bytes()
        assert sha(raw) == snapshot['sha256']
        views = []
        pos = 12
        needle = struct.pack('<I', 0x02313F60)
        while (pos := raw.find(needle, pos)) >= 0:
            start = pos - 12
            pos += 4
            if start < 0 or start % 4 or start + 48 > len(raw):
                continue
            words = struct.unpack_from('<12I', raw, start)
            x, y, width, height = words[7], words[8], words[10], words[11]
            if not (0 < width <= 256 and 0 < height <= 256 and x + width <= 256 and y + height <= 256):
                continue
            intersections = [name for name, (left, top, right, bottom) in MINIATURES.items()
                             if x < right and left < x + width and y < bottom and top < y + height]
            views.append({'address': 0x02000000 + start, 'source_rect': [x, y, width, height],
                          'palette_bank_low_byte': words[9] & 255, 'miniature_intersections': intersections})
        consumer_scans.append({'frame': frame, 'snapshot_sha256': sha(raw), 'frame_owner_views': views,
                               'intersecting_views': sum(bool(v['miniature_intersections']) for v in views)})

    proof = {'format': 'dk4-grand-race-native-UI-proof-v576', 'candidate': str(ROM),
             'candidate_sha256': ROM_SHA, 'ARM9_sha256': sha(arm),
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'manuscript': str(manuscript_path), 'manuscript_sha256': sha(manuscript_path.read_bytes()),
             'fixture_manifest': str(ROOT / 'current_save_fixture_manifest.json'),
             'synthetic_system_unlock_fixture': True, 'earned_unlock_verified': False,
             'cold_boot': True, 'savestate_loaded': False, 'frames': report['frames'],
             'pages': pages, 'six_menu_labels': menus, 'two_previous_page_returns_pixel_exact': True,
             'body_row_pitch_is_observed_16_not_historical_model_12': True,
             'original_release_formatter_unchanged': True, 'source_save_and_fixture_unchanged': True,
             'native_frame_view_scans': consumer_scans,
             'five_miniature_caption_consumers_remain_unresolved': True,
             'view_scan_excludes_neither_direct_blits_nor_other_consumers': True,
             'wireless_peers_or_completed_races_verified': False,
             'production_ROM_changed': False, 'all18_plaques_remain_incomplete': True,
             'full_goal_complete': False}
    (ROOT / 'native_help_and_consumer_proof.json').write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_help_pages': len(pages), 'native_body_lines': sum(len(p['body_lines']) for p in pages),
                      'menu_labels': len(menus), 'complete_body_ink_pixels': sum(
                          line['complete_ink_pixels'] for p in pages for line in p['body_lines']),
                      'miniature_intersecting_views_by_frame': {r['frame']: r['intersecting_views'] for r in consumer_scans},
                      'production_changed': False, 'full_goal_complete': False}))


if __name__ == '__main__':
    main()
