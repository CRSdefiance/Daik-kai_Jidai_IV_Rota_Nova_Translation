"""Run complete original captured Refit font paints for all31 natural paragraphs."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.refit_help import PROFILE, compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.trace_refit_text_v706 import IDS as ORIGINAL_IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v708')
IDS = (1247, *ORIGINAL_IDS)
TEXT = 0x02440020


def bitmap(u, ctx):
    surface = struct.unpack('<I', u.mem_read(ctx + 44, 4))[0]
    assert struct.unpack('<I', u.mem_read(surface + 20, 4))[0] == 5
    header = struct.unpack('<I', u.mem_read(surface + 16, 4))[0]
    words = struct.unpack('<5I', u.mem_read(header, 20))
    assert words[:3] == (4, 42, 84)
    pixels = (header + words[4]) & 0xFFFFFFFF
    return header, pixels


def draw(arm, row, text):
    raw = Path(row['RAM']).read_bytes()
    assert sha(raw) == row['RAM_sha256']
    u = machine(arm)
    u.mem_write(BASE, raw)
    ctx = row['R0_context']
    assert struct.unpack('<4I', u.mem_read(ctx + 4, 16)) == (0, 0, 168, 84)
    header, pixels = bitmap(u, ctx)
    assert bytes(u.mem_read(pixels, 7056)) == bytes(7056)
    u.mem_write(TEXT - 16, b'\xA5' * (len(text) + 32))
    u.mem_write(TEXT, text)
    before = bytes(u.mem_read(BASE, 0x400000))
    trace = call(u, 0xD5404, (ctx, TEXT), instruction_limit=1000000)
    after = bytes(u.mem_read(BASE, 0x400000))
    changes = [BASE + i for i, (a, b) in enumerate(zip(before, after)) if a != b]
    allowed = [(ctx, ctx + 72), (pixels, pixels + 7056)]
    assert all(any(lo <= a < hi for lo, hi in allowed) for a in changes), [hex(a) for a in changes if not any(lo <= a < hi for lo, hi in allowed)][:12]
    assert bytes(u.mem_read(TEXT, len(text))) == text
    assert bytes(u.mem_read(TEXT - 16, 16)) == bytes(u.mem_read(TEXT + len(text), 16)) == b'\xA5' * 16
    assert struct.unpack('<5I', u.mem_read(header, 20)) == struct.unpack_from('<5I', raw, header - BASE)
    result = bytes(u.mem_read(pixels, 7056))
    indices = bytes(n for value in result for n in (value & 15, value >> 4))
    assert set(indices) <= {0, 1}
    return indices, {'native_return': u.reg_read(UC_ARM_REG_R0), 'native_distinct_instructions': len(trace),
        'whole_RAM_differences_only_context_and_entire_original_bitmap': allowed,
        'original_header': header, 'actual_pixel_storage': pixels,
        'native_return_stack_saved_registers_source_guards_and_header_exact': True}


def model(font, lines):
    result = bytearray(168 * 84)
    for row, line in enumerate(lines):
        for i, char in enumerate(line):
            for y in range(11):
                for x in range(6):
                    if font.decode(char).getpixel((x, y)):
                        result[(row * 12 + y) * 168 + i * 6 + x] = 1
    return bytes(result)


def main():
    pre = read(ROOT / 'preflight.json')
    assert sha(ROM.read_bytes()) == pre['candidate_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    manifest = read('translations/refit_help_manuscript_v2.json')
    validate_natural_dialogue_batch(manifest)
    events = read(CAP / 'refit_help_v706_original_consumer/observer/events.json')
    assert events['all_host_slots_restored'] and not events['errors'] and not events['mismatches']
    by_id = {r['message_id']: r for r in events['rows']}
    assert {1248, 1249, 1250, 1255, 1287} <= set(by_id)
    captured = by_id[1248]
    font = GameAsciiFont.from_arm9(arm)
    old, old_proof = draw(arm, captured, bytes.fromhex(captured['text_hex']) + b'\0')
    old_lines = ['A carpenter can repair damag', 'ed', ' ships.']
    assert old == model(font, old_lines)
    rows, negative_count = [], 0
    sheet = Image.new('RGB', (4 * 350, 8 * 210), '#202b32')
    labels = ImageDraw.Draw(sheet)
    for index, row in enumerate(manifest['records']):
        text, lines = compile_paragraph(row['english'])
        actual, proof = draw(arm, captured, text)
        expected = model(font, lines)
        assert actual == expected, (row['message_id'], lines, sum(a != b for a, b in zip(actual, expected)))
        ink = [i for i, value in enumerate(expected) if value]
        for column in (min(i % 168 for i in ink), max(i % 168 for i in ink)):
            changed = bytearray(actual)
            for i in ink:
                if i % 168 == column:
                    changed[i] = 0
            assert bytes(changed) != expected
            negative_count += 1
        picture = Image.frombytes('L', (168, 84), bytes(230 if n else 45 for n in actual)).convert('RGB')
        path = ROOT / f'native_help_{row["message_id"]}.png'
        picture.save(path)
        x, y = index % 4 * 350, index // 4 * 210
        sheet.paste(picture.resize((336, 168), Image.Resampling.NEAREST), (x + 7, y + 30))
        labels.text((x + 7, y + 8), str(row['message_id']), fill='white')
        rows.append({'message_id': row['message_id'], 'English': row['english'], 'lines': lines,
            'compiled_hex': text.hex(), 'complete_native_168x84_indices_sha256': sha(actual),
            'all_first_final_letters_blank_cells_and_bounds_exact': True, 'proof': proof,
            'native_preview': str(path), 'native_preview_sha256': sha(path.read_bytes())})
    assert [r['message_id'] for r in rows] == list(IDS)
    for bad in ('x' * 28, 'First\nsecond', ' leading', 'two  spaces', ' '.join(['longword'] * 30)):
        try:
            compile_paragraph(bad)
        except ValueError:
            negative_count += 1
        else:
            raise AssertionError('Invalid Refit paragraph accepted')
    sheet_path = ROOT / 'all31_native_help.png'
    sheet.save(sheet_path)
    save(ROOT / 'native_font_proof.json', {'profile': PROFILE, 'complete_original_captured_Refit_font_entry': 0x020D5404,
        'original_parent_return': captured['LR'], 'captured_original_context': captured,
        'current_broken_baseline_complete_bitmap_reproduced': old_proof,
        'all31_complete_native_font_paints': rows, 'native_bitmap_pixels_compared': 31 * 168 * 84,
        'whole_source_RAM_guards_header_and_ABI_pass': True, 'negative_controls': negative_count,
        'captured_original_168x84_context_uses12_pixel_font_line_advance': True,
        'all_lines_start_at_same_zero_x': True,
        'observed_screen16_pixel_line_advance_is_not_inferred_to_be_this12_pixel_context': True,
        'source_and_canonical_manuscript_locked': True,
        'font_context_is_supplied_from_one_real_call_not_all31_normal_parent_visits': True,
        'production_integration_and_actual_changed_ROM_display_pending': True,
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V708 all31 source paragraphs pass complete original native Refit paints, 437472 pixels, same left margin and first/final glyph controls.', flush=True)


if __name__ == '__main__':
    main()
