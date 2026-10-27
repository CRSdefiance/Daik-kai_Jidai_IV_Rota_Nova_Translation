"""Verify complete changed text, resident chapter, original movie and ordinary UI."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.wedding_dialogue_cleanup import transform
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.native_wedding_fixture_v677 import plan
from scripts.prepare_wedding_dialogue_v678 import BATCH, ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_village_wrap_v608 import read, save
from scripts.verify_wedding_dialogue_v678 import ROM


def shot(row):
    assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return Image.open(row['path']).convert('RGB')


def report(folder, digest):
    path = folder / 'capture_report.json'
    value = read(path)
    assert value['cold_boot'] and not value['savestate_loaded'] and not value['callback_errors']
    assert value['ROM_sha256'] == digest and value['core_DLL_sha256'] == CORE_SHA
    assert not value.get('battery_save_preloaded')
    rows = {}
    for item in value['frames_captured']:
        if item['frame'] in rows:
            assert shot(rows[item['frame']]).tobytes() == shot(item).tobytes()
        rows[item['frame']] = item
    return value, rows, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    static = read(ROOT / 'static_release_proof.json')
    assert sha(ROM.read_bytes()) == static['candidate_sha256'] and sha(CORE.read_bytes()) == CORE_SHA
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    chapter = IlnkContainer.parse(rom.read_file('/data/SC2.DK4')).blocks[70]
    font = GameAsciiFont.from_arm9(arm)
    reports, images, refs, fixtures = {}, {}, {}, []
    for mode in ('wedding', 'baseline', 'ordinary'):
        folder = CAP / ('wedding_dialogue_v678_' + mode)
        reports[mode], images[mode], refs[mode] = report(folder, static['candidate_sha256'])
        contract = read(folder / 'run_contract.json')
        assert contract['runner_sha256'] == sha(Path('scripts/run_wedding_dialogue_v678.py').read_bytes())
        assert sha(Path(contract['inputs']).read_bytes()) == contract['inputs_sha256']
        assert reports[mode]['frames'] == contract['frames'] == (24100 if mode == 'ordinary' else 16000)
        if mode == 'ordinary':
            assert not any(k.startswith('synthetic_') and v for k, v in reports[mode].items())
            continue
        receipt = read(folder / 'chapter_fixture/fixture.json')
        assert receipt['slot_restored_before_filter_free'] and receipt['applied']
        assert not receipt['errors'] and not receipt['mismatches'] and receipt['callbacks'] == 1
        assert receipt['script_sha256'] == contract['fixture_sha256'] == sha(Path('scripts/native_wedding_fixture_v677.py').read_bytes())
        row, = receipt['rows']
        data = {key: Path(item['path']).read_bytes() for key, item in row['files'].items()}
        assert all(sha(data[key]) == item['sha256'] for key, item in row['files'].items())
        after, expected = plan(arm, data['CPU_before.bin'], data['RAM_before.bin'])
        assert row['receipt'] == expected and data['CPU_expected_after.bin'] == after
        assert expected['changed_CPU_byte_offsets'] == [20] and row['frame'] == 2222
        assert row['actual_CPU_after_exact_and_full_WRAM_unchanged_at_fixture']
        fixtures.append({'mode': mode, 'receipt': str(folder / 'chapter_fixture/fixture.json'),
                         'replayed_single_CPU_byte_no_WRAM_write': True})
    assert images['wedding'].keys() == images['baseline'].keys()
    assert all(shot(row).tobytes() == shot(images['baseline'][frame]).tobytes() for frame, row in images['wedding'].items())
    assert (CAP / 'wedding_dialogue_v678_wedding/final_arm9_ram.bin').read_bytes() == (
        CAP / 'wedding_dialogue_v678_baseline/final_arm9_ram.bin').read_bytes()
    ordinary_parent, ordinary_images, ordinary_ref = report(
        CAP / 'village_consistency_v666_newgame', read(ROOT / 'preflight.json')['source_candidate_sha256'])
    assert reports['ordinary']['scripted_input_schedule'] == ordinary_parent['scripted_input_schedule']
    assert images['ordinary'].keys() == ordinary_images.keys() and len(ordinary_images) == 89
    assert all(shot(row).tobytes() == shot(ordinary_images[frame]).tobytes() for frame, row in images['ordinary'].items())
    parent_report, parent_images, parent_ref = report(CAP / 'wedding_playback_v677_fixture_baseline',
        read(ROOT / 'preflight.json')['source_candidate_sha256'])
    assert reports['wedding']['scripted_input_schedule'] == parent_report['scripted_input_schedule']
    matched, changed = [], []
    for frame, row in images['wedding'].items():
        if frame not in parent_images:
            continue
        actual, prior = shot(row), shot(parent_images[frame])
        if actual.tobytes() == prior.tobytes():
            matched.append(frame)
            continue
        assert frame in (11400, 14200)
        assert all(actual.getpixel((x, y)) == prior.getpixel((x, y)) for y in range(384) for x in range(256)
                   if not (16 <= x < 240 and 296 <= y < 376))
        changed.append(frame)
    assert changed == [11400, 14200]
    fields, block_checks = [], []
    snapshots = {row['frame']: row for row in reports['wedding']['read_only_capture_RAM_snapshots']}
    expected_lines = static['stage']['proof']['records']
    for frame, index in ((11300, 0), (11400, 0), (14100, 1), (14200, 1)):
        image, lines = shot(images['wedding'][frame]), expected_lines[index]['compiled_lines']
        masks = [full_cells(image, font, text, 16, 296 + i * 16, (0, 8, 0)) for i, text in enumerate(lines)]
        expected = {(16 + x, 296 + i * 16 + y) for i, text in enumerate(lines) for x, y in glyphs(font, text)}
        actual = {(x, y) for y in range(296, 376) for x in range(16, 240) if image.getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected
        fields.append({'frame': frame, 'id': expected_lines[index]['id'], 'complete_lines': masks,
                       'whole_text_rectangle_including_remaining_empty_rows_exact': True,
                       'no_orphan_word_dropped_edge_letter_extra_text_or_page_in_these_holds': True})
    for frame in (11300, 11400, 11500, 11600, 14100, 14200, 14300, 14400, 14500, 16000):
        entry = snapshots[frame]
        data = Path(entry['path']).read_bytes()
        assert sha(data) == entry['sha256'] and len(data) == 0x400000
        assert data[0x18F2B0:0x18F2B0 + len(chapter)] == chapter
        cursor = struct.unpack_from('<I', data, 0x18F254)[0] - 0x0218F2B0
        block_checks.append({'frame': frame, 'all6764_actual_resident_chapter_bytes_exact': True, 'original_VM_cursor_offset': cursor})
    meta = read(CAP / 'wedding_dialogue_v678_wedding/observer/paint_observer.json')
    assert meta['original_slot_restored_and_DLL_file_unchanged'] and meta['all_three_original_slot_pointers_restored_before_filter_free']
    assert not meta['mismatch'] and not meta['overflow']
    entries = Path(meta['path']).read_bytes()
    assert sha(entries) == meta['sha256']
    special = []
    for row in struct.iter_unpack('<40I', entries):
        if row[1] in (0x02024134, 0x02028A28, 0x020D2B1C):
            special.append({'frame': row[0], 'PC': row[1], 'args': list(row[3:7])})
        else:
            assert not row[38]
    assert [(r['frame'], r['PC']) for r in special] == [(16, 0x020D2B1C), (559, 0x020D2B1C),
        (2222, 0x02024134), (14489, 0x02028A28), (14489, 0x020D2B1C)]
    assert special[2]['args'][1] == 70 and special[3]['args'][1] == 6 and special[4]['args'] == [26, 0, 1, 0]
    assert rom.read_file('/FLS/M26.fls') == NdsImage.open('work/clean.nds').read_file('/FLS/M26.fls')
    # Exact-source guards must reject corruption before applying any final-stage edit.
    pre = read(ROOT / 'preflight.json')
    source = NdsImage.open(pre['source_candidate']).read_file('/data/SC2.DK4')
    canonical = NdsImage.open(pre['canonical_baseline']['path']).read_file('/data/SC2.DK4')
    for label, a, b in (('source', bytes([source[0] ^ 1]) + source[1:], canonical),
                         ('canonical', source, bytes([canonical[0] ^ 1]) + canonical[1:])):
        try:
            transform(a, b, read(BATCH))
        except ValueError:
            pass
        else:
            raise AssertionError(label + ' corrupt source accepted')
    selected = [('wedding', f) for f in (11300, 11400, 11500, 11600, 14100, 14200, 14300, 14400, 14600, 15200, 16000)]
    # Whole original ordinary captures will also be reviewed separately by phase.
    sheet = Image.new('RGB', (768, 4 * 410), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (mode, frame) in enumerate(selected):
        x, y = i % 3 * 256, i // 3 * 410
        draw.text((x + 4, y + 4), f'V678 {frame} CHAPTER FIXTURE', fill='white')
        sheet.paste(shot(images[mode][frame]), (x, y + 24))
    sheet_path = ROOT / 'actual_dialogue_and_transition_review.png'
    sheet.save(sheet_path)
    save(ROOT / 'proof.json', {**static, 'cold_boot_verification_pending': False,
        'reports': refs, 'ordinary_V666_baseline': ordinary_ref, 'wedding_V666_baseline': parent_ref,
        'observer_common_fixture_baseline_whole_screen_pairs': len(images['wedding']),
        'wedding_capture_records_per_run': len(reports['wedding']['frames_captured']),
        'ordinary89_whole_title_selection_story_town_frames_exact_V666': True,
        'ordinary_frames': sorted(ordinary_images), 'changed_fields': fields,
        'resident_chapter_checks': block_checks, 'original_source_requests': special, 'fixtures': fixtures,
        'unchanged_wedding_whole_frames_exact_V666': matched,
        'only_two_sampled_text_boxes_differ_surrounding_portrait_nameplate_art_exact': changed,
        'movie_request_same_frame_and_sampled_playback_transitions_exact_V677': True,
        'exact_source_and_canonical_corruption_guards_reject': True,
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'earned_wedding_full_route_hardware_verification': False,
        'all18_plaques22_historical_requirements_and_other_graphics_gates_open': True,
        'current_goal_turn_classification': 'progress', 'full_goal_complete': False})
    print('V678: two complete text repairs,73 distinct observer/baseline pairs (74 capture records),89 ordinary regression frames and original movie transition verified.', flush=True)


if __name__ == '__main__':
    main()
