"""Whole Maria opening evidence; retain the observed percent defect as a failure."""

from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_maria_intro_v684 import CAP, ROM, ROOT
from scripts.verify_dialogue_palette_v628 import raster
from scripts.verify_fixed_name_glyphs_v279 import expand
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_village_wrap_v608 import read, save


def mask(font, lines):
    return {(16 + x, 296 + i * 16 + y) for i, text in enumerate(lines) for x, y in glyphs(font, text)}


def main():
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom = NdsImage.open(ROM)
    arm, source = rom.read_file('/__arm9__.bin'), rom.read_file('/data/SC3.DK4')
    chapter = IlnkContainer.parse(source).blocks[33]
    fields = chapter.split(b'\0')
    font = GameAsciiFont.from_arm9(arm)
    candidates = []
    for index, field in enumerate(fields):
        if not field or field[0] not in (3, 10, 11, 12, 13, 21, 74):
            continue
        body = field[1:].rstrip(b' ')
        try:
            decoded = body.decode('cp932')
        except UnicodeDecodeError:
            continue
        if not decoded or not all(c == '\n' or 32 <= ord(c) < 127 or c == '\u2026' for c in decoded):
            continue
        lines = [line.strip() for line in decoded.replace('FI', 'Maria').split('\n')]
        if max(map(len, lines)) <= 37 and len(lines) <= 5:
            if '\u2026' in decoded:
                pixels, _ = raster(arm, rom.read_file('/GRP/KANJI.FNT'), '\n'.join(lines).encode('cp932'))
                expected = {(16 + i % 228, 296 + i // 228) for i, p in enumerate(pixels) if p == 15}
            else:
                expected = mask(font, lines)
            candidates.append((index, lines, expected))
    reports, frames, snapshots, refs = {}, {}, {}, []
    for case in ('pilot_interactive', 'observed', 'baseline'):
        folder = CAP / ('maria_intro_v684_' + case)
        path = folder / 'capture_report.json'
        report = read(path)
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert report['frames'] == 31000 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and report['scripted_input_schedule'] == read(config['inputs'])
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_gallery_fixtures'}
        contract = read(folder / 'run_contract.json')
        assert contract['runner_sha256'] == sha(Path('scripts/run_maria_intro_v684.py').read_bytes())
        values = {}
        for row in report['frames_captured']:
            image_path = Path(row['path'])
            assert sha(image_path.read_bytes()) == row['PNG_sha256']
            im = Image.open(image_path).convert('RGB')
            if row['frame'] in values:
                assert im.tobytes() == values[row['frame']].tobytes()
            values[row['frame']] = im
        reports[case], frames[case] = report, values
        refs.append({'case': case, 'path': str(path), 'sha256': sha(path.read_bytes())})
        snapshot_rows = report.get('read_only_capture_RAM_snapshots', []) + report.get('read_only_pause_RAM_snapshots', [])
        snapshots[case] = {s['frame']: s for s in snapshot_rows}
    assert frames['observed'].keys() == frames['baseline'].keys() == frames['pilot_interactive'].keys()
    assert len(frames['observed']) == 49
    for frame, im in frames['observed'].items():
        assert im.tobytes() == frames['baseline'][frame].tobytes() == frames['pilot_interactive'][frame].tobytes()
    assert (CAP / 'maria_intro_v684_observed/final_arm9_ram.bin').read_bytes() == (
        CAP / 'maria_intro_v684_baseline/final_arm9_ram.bin').read_bytes() == (
        CAP / 'maria_intro_v684_pilot_interactive/final_arm9_ram.bin').read_bytes()
    meta_path = CAP / 'maria_intro_v684_observed/observer/SDK_entries.json'
    meta = read(meta_path)
    assert not meta['errors'] and not meta['mismatches'] and meta['all_opcode_slots_restored_and_core_file_unchanged']
    assert meta['trace_source_sha256'] == sha(Path('scripts/trace_file_ids_v683.py').read_bytes())
    names = [r for r in meta['rows'] if r['kind'] == 'filename']
    assert [r['filename'] for r in names if 'SC3.DK4' in r['filename']] == ['\\DATA\\SC3.DK4']
    art, caption_cases, resident, excluded = [], [], [], []
    for frame in range(4000, 31001, 600):
        im = frames['observed'][frame]
        entry = snapshots['observed'][frame]
        raw = Path(entry['path']).read_bytes()
        assert sha(raw) == entry['sha256'] and len(raw) == 0x400000
        pilot_entry = snapshots['pilot_interactive'][frame]
        assert Path(pilot_entry['path']).read_bytes() == raw
        u = machine(arm)
        u.mem_write(BASE, raw)
        call(u, 0x7F244, ())
        assert u.reg_read(UC_ARM_REG_R0) == 3
        assert expand(u, b'FI') == b'Maria'
        if frame <= 30400:
            offset = raw.find(chapter)
            assert offset >= 0 and raw.find(chapter, offset + 1) == -1
            resident.append({'frame': frame, 'matching_entire_original2528_byte_chapter33_address': BASE + offset,
                             'native_captain_getter': 3})
            request = [r for r in names if r['frame'] < frame and '/evstill/' in r['filename']][-1]
            path = request['filename']
            pxl = PxlImage.from_bytes(rom.read_file(path))
            expected = pxl.render().convert('RGB')
            assert expected.size == (256, 192)
            assert all(native5(a) == native5(b) for a, b in zip(
                im.crop((0, 0, 256, 192)).get_flattened_data(), expected.get_flattened_data(), strict=True)), (frame, path)
            art.append({'frame': frame, 'source': path, 'request_frame': request['frame'],
                        'whole_PXL_sha256': sha(rom.read_file(path)), 'all49152_upper_RGB5_source_pixels_exact': True})
        if frame in (4000, 5800, 21400, 28600, 29200, 29800, 30400, 31000):
            excluded.append({'frame': frame, 'scope': 'blank scene hold, native joined-name notification, or Town; no chapter-dialogue font claim',
                             'blank_scene_hold_ordinary_source_timing_not_resolved_here': frame in (4000, 5800, 21400)})
            continue
        actual = {(x, y) for y in range(296, 376) for x in range(16, 240) if im.getpixel((x, y)) == (0, 8, 0)}
        matched = [{'record': i, 'complete_visible_lines': lines} for i, lines, expected in candidates if actual == expected]
        if frame == 24400:
            assert not matched
            source_lines = [line.strip() for line in fields[137][1:].decode('ascii').rstrip().split('\n')]
            assert actual != mask(font, source_lines)
            caption_cases.append({'frame': frame, 'record': 137, 'status': 'confirmed_runtime_format_defect',
                'expected_ROM_lines': source_lines, 'raw_3_percent_followed_by_space_o_is_native_octal_conversion': True,
                'not_counted_as_passing_caption_or_waived_pixels': True})
        else:
            assert matched, frame
            caption_cases.append({'frame': frame, 'status': 'complete_native_font_mask_pass',
                'source_record_candidates': matched, 'all_edge_letters_spaces_and_remaining_rows_exact': True})
    sheet = Image.new('RGB', (1024, 820), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, frame in enumerate((4600, 7600, 11800, 17200, 20200, 24400, 30400, 31000)):
        x, y = i % 4 * 256, i // 4 * 410
        draw.text((x + 4, y + 4), f'V678 Maria {frame}', fill='white')
        sheet.paste(frames['observed'][frame], (x, y + 24))
    review = ROOT / 'full_opening_and_confirmed_percent_defect.png'
    sheet.save(review)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'], 'reports': refs,
        'two_fresh31000_frame_runs49_whole_baseline_pairs_and49_pilot_pairs_and_terminal_RAM_exact': True,
        'normal_New_Game_inputs_to_Hangzhou_existing_unlock_save_no_story_or_location_fixture': True,
        'actual_source_art_cases': art, 'complete_resident_chapter_cases': resident,
        'caption_cases': caption_cases, 'explicit_no_chapter_font_credit_cases': excluded,
        'one_confirmed_percent_corruption_not_waived_and_repair_required': True,
        'full_opening_navigation_complete_but_display_acceptance_blocked_by_known_record': True,
        'observer_trace': str(meta_path), 'observer_trace_sha256': sha(meta_path.read_bytes()),
        'review_sheet': str(review), 'review_sheet_sha256': sha(review.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'current_goal_turn_classification': 'progress',
        'all18_plaques_incomplete22_original_requirements_and_broader_gates_open': True, 'full_goal_complete': False})
    print('V684 complete Maria navigation to Hangzhou; source art and complete text checks retained; one real percent defect requires repair.', flush=True)


if __name__ == '__main__':
    main()
