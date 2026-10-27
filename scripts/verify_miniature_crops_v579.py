"""Check actual/blank native rendering of five complete miniature captions.

These disposable ROMs select a controlled crop in Cargo Setup. They establish
component loading/crop/palette behavior, not the five ordinary caller contexts.
"""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.compact_font import layout
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.prepare_miniature_crops_v579 import FILE, OWNER, PARENT, PARENT_SHA, RECTANGLE, ROOT
from scripts.probe_button_prompt_native import call, machine

CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def native_color(word):
    return word & 31, word >> 5 & 31, word >> 10 & 31


def main():
    manifest = read(ROOT / 'fixture_manifest.json')
    assert sha(PARENT.read_bytes()) == manifest['parent_sha256'] == PARENT_SHA
    assert sha(Path(manifest['source_save']).read_bytes()) == manifest['source_save_sha256']
    parent = NdsImage.open(PARENT)
    before = rom_files(parent)
    atlas = PxlImage.from_bytes(before[FILE])
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    rows = [row for row in batch['records'][15:] if row['text'] not in ('M', 'D')]
    assert len(rows) == 5
    expected = set()
    cells = []
    for row in rows:
        left, top, right, bottom = row['box']
        mask, _, _ = layout(row['text'], tuple(row['box']),
                            word_space_width=row.get('compact_word_space_width', 2), font_face=row['font_face'])
        points = {(left + x, top + y) for y in range(bottom - top) for x in range(right - left)
                  if mask.getpixel((x, y))}
        assert points == {(x, y) for y in range(top, bottom) for x in range(left, right)
                          if atlas.indices[y * 256 + x] == 9}
        expected |= points
        cells.append({'text': row['text'], 'source_Japanese': row['source_japanese'],
                      'source_box': row['box'], 'complete_font_ink_pixels': len(points),
                      'full_first_final_glyphs_and_spaces_included': True})
    assert len(expected) == 307 == len(manifest['all307_changed_source_points'])
    assert expected == set(map(tuple, manifest['all307_changed_source_points']))
    left, top, right, bottom = RECTANGLE
    destination = { (x - left, y - top + 261) for x, y in expected }
    reports, tables, fixtures = {}, {}, {}
    native_views = []
    for fixture in manifest['fixtures']:
        bank, kind = fixture['palette_bank'], fixture['kind']
        key = bank, kind
        fixtures[key] = fixture
        rom = NdsImage.open(fixture['ROM'])
        assert sha(Path(fixture['ROM']).read_bytes()) == fixture['ROM_sha256']
        after = rom_files(rom)
        assert sorted(path for path in before if before[path] != after[path]) == fixture['changed_internal_files']
        offsets = {offset for change in fixture['changes'] for offset in range(change['file_offset'], change['file_offset'] + 4)}
        assert len(fixture['changes']) == 10
        assert all(a == b for i, (a, b) in enumerate(zip(before['/__arm9__.bin'], after['/__arm9__.bin'], strict=True))
                   if i not in offsets)
        data = PxlImage.from_bytes(after[FILE])
        assert data.source[:data.pixels_offset] == atlas.source[:atlas.pixels_offset]
        differences = {i for i, (a, b) in enumerate(zip(data.indices, atlas.indices, strict=True)) if a != b}
        assert differences == ({y * 256 + x for x, y in expected} if kind == 'blank' else set())
        if kind == 'blank':
            assert all(data.indices[i] == 0 for i in differences)
        report_path = CAPTURES / f'miniature_crops_v579_bank{bank}_{kind}' / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == fixture['ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == 4600 and report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
        assert report['battery_save_preloaded']['source_sha256'] == manifest['source_save_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        shots = {}
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            shots.setdefault(shot['frame'], shot)
        snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}
        for frame in (4300, 4600):
            snapshot = snapshots[frame]
            raw = Path(snapshot['path']).read_bytes()
            assert len(raw) == 0x400000 and sha(raw) == snapshot['sha256']
            found = []
            needle, start = struct.pack('<I', OWNER), 12
            while (position := raw.find(needle, start)) >= 0:
                start = position + 4
                p = position - 12
                if p % 4 or p + 48 > len(raw):
                    continue
                words = struct.unpack_from('<12I', raw, p)
                if words[7:9] == (left, top) and words[10:12] == (right - left, bottom - top):
                    assert words[6] == 0 and words[9] & 255 == bank
                    found.append(p + 0x02000000)
            assert len(found) == 1, (key, frame, found)
            u = machine(after['/__arm9__.bin'])
            u.mem_write(0x02000000, raw)
            registered = int.from_bytes(u.mem_read(OWNER + 12, 4), 'little')
            assert bytes(u.mem_read(registered, 64)).split(b'\0')[0] == b'_pxl/__frame.pxl'
            call(u, 0xD4170, (found[0],))
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(data.source))) == data.source
            native_views.append({'bank': bank, 'kind': kind, 'frame': frame, 'view': found[0],
                                 'owner': OWNER, 'resident_PXL': pointer, 'whole_resident_PXL_sha256': sha(data.source),
                                 'source_rect': list(RECTANGLE), 'palette_and_flags_exact': True})
        reports[key] = {'path': str(report_path), 'sha256': sha(report_path.read_bytes()), 'report': report}
        tables[key] = shots

    pairs, appearances = [], []
    for bank in (0, 9):
        actual_key, blank_key = (bank, 'actual'), (bank, 'blank')
        assert reports[actual_key]['report']['core_options'] == reports[blank_key]['report']['core_options']
        for frame in (4300, 4600):
            actual, blank = [Image.open(tables[key][frame]['path']).convert('RGB').point(lambda value: value >> 3)
                             for key in (actual_key, blank_key)]
            ap, bp = actual.load(), blank.load()
            word0 = struct.unpack_from('<H', atlas.source, 20 + bank * 32)[0]
            word9 = struct.unpack_from('<H', atlas.source, 20 + bank * 32 + 18)[0]
            assert word9 & 0x8000 and bool(word0 & 0x8000) == (bank == 0)
            foreground, zero_color = native_color(word9), native_color(word0)
            actual_differences = set()
            for y in range(384):
                for x in range(256):
                    wanted = foreground if (x, y) in destination else bp[x, y]
                    assert ap[x, y] == wanted, (bank, frame, x, y)
                    if ap[x, y] != bp[x, y]:
                        actual_differences.add((x, y))
            assert actual_differences == destination
            for cell in cells:
                l, t, r, b = cell['source_box']
                source_mask = {(x, y) for y in range(t, b) for x in range(l, r) if (x, y) in expected}
                for y in range(t, b):
                    for x in range(l, r):
                        xx, yy = x - left, y - top + 261
                        if (x, y) in source_mask:
                            assert ap[xx, yy] == foreground and bp[xx, yy] != foreground
                        elif word0 & 0x8000:
                            assert ap[xx, yy] == zero_color
                        else:
                            assert ap[xx, yy] == bp[xx, yy]
                appearances.append({**cell, 'bank': bank, 'frame': frame,
                                    'destination_box': [l - left, t - top + 261, r - left, b - top + 261],
                                    'complete_native_cell_ink_and_background_exact': True})
            pairs.append({'bank': bank, 'frame': frame, 'actual_capture': tables[actual_key][frame],
                          'blank_capture': tables[blank_key][frame], 'native_foreground_RGB5': list(foreground),
                          'original_zero_index_is_opaque': bool(word0 & 0x8000),
                          'exact_changed_glyph_points': len(actual_differences),
                          'all98304_pair_screen_pixels_exact': True,
                          'blank_control_rejects_every_complete_caption': True})
    cross = []
    for frame in (4300, 4600):
        a, b = [Image.open(tables[bank, 'actual'][frame]['path']).convert('RGB').point(lambda value: value >> 3)
                for bank in (0, 9)]
        for y in range(384):
            for x in range(256):
                if not (0 <= x < 72 and 261 <= y < 285):
                    assert a.getpixel((x, y)) == b.getpixel((x, y)), (frame, x, y)
        cross.append({'frame': frame, 'outside72x24_native_crop_unchanged_between_banks': True})

    result = {'format': 'dk4-five-miniature-native-crop-proof-v579', 'production_candidate': str(PARENT),
              'production_candidate_sha256': PARENT_SHA, 'source_manifest': str(ROOT / 'fixture_manifest.json'),
              'source_manifest_sha256': sha((ROOT / 'fixture_manifest.json').read_bytes()),
              'reports': [{k: v for k, v in row.items() if k != 'report'} for row in reports.values()],
              'source_rectangle': list(RECTANGLE), 'native_destination': [0, 261, 72, 285],
              'native_resource_views': native_views, 'pairs': pairs, 'complete_caption_appearances': appearances,
              'complete_native_glyph_points': sum(row['complete_font_ink_pixels'] for row in appearances),
              'complete_cell_pixels': sum((row['source_box'][2] - row['source_box'][0]) * 8 for row in appearances),
              'whole_pair_screen_pixels': len(pairs) * 98304, 'cross_bank_scope': cross,
              'manual_crop_does_not_identify_normal_five_callers': True,
              'tested_banks0_and9_do_not_prove_all83_native_palette_uses': True,
              'ordinary_five_caption_contexts_and_Confirm_parent_remain_open': True,
              'all18_plaques_remain_incomplete': True, 'all22_historical_requirements_retained': True,
              'production_ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'native_five_caption_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_caption_appearances': len(appearances),
                      'complete_native_glyph_points': result['complete_native_glyph_points'],
                      'complete_cell_pixels': result['complete_cell_pixels'],
                      'whole_pair_screen_pixels': result['whole_pair_screen_pixels'],
                      'normal_five_consumers_still_unresolved': True, 'production_changed': False}))


if __name__ == '__main__':
    main()
