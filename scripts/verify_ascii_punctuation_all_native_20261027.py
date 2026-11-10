"""Original native painter and footer constructor: complete pixels and memory guards."""

import json
import struct
import string
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC
from ndspy.code import MainCodeFile

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_draw_offset_20261027_v2 import BASE
from dk4tool.patch.ascii_punctuation_all_20261027 import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine, STACK
from scripts.research_online_loader_v190 import resource_call as call
from scripts.verify_name_catalog_glyphs_v278 import raster, expected_pixels

ROOT = Path('work/font_punctuation_all_20261027')
CONFIG = Path('translations/ascii_punctuation_all_20261027_v1.json')


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def glyph_bounds(arm):
    cpu = machine(arm)
    font = GameAsciiFont.from_arm9(arm)
    rows = []
    header = 0x02450000
    palette = struct.unpack_from('<I', arm, 0xD181C)[0] - BASE
    color = struct.unpack_from('<H', arm, palette + 2)[0]
    for mode in [4, 16]:
        width, pitch = 32, 8 if mode == 4 else 32
        stride = 16 if mode == 4 else 64
        for height in [0, 2, 10, 11, 12, 13, 14, 16]:
            for char in 'gjpqy' + string.punctuation:
                size = stride * height
                raw = struct.pack('<5I', mode, pitch, height, 0x2000, 20)
                cpu.mem_write(header - 16, b'\xA5' * (20 + size + 32))
                initial = b'\x99' * size
                cpu.mem_write(header, raw + initial)
                cpu.mem_write(STACK, struct.pack('<2I', ord(char), 1))
                call(cpu, 0xD16B4, (0, header, 8, 0))
                expected = bytearray(initial)
                glyph = font.decode(char)
                for y in range(max(0, min(11, height - 1))):
                    for x in range(6):
                        ink = bool(glyph.getpixel((x, y)))
                        px, py = x + 8, y + 1
                        if mode == 16:
                            if ink:
                                struct.pack_into('<H', expected, py * stride + px * 2, color)
                        else:
                            at, shift = py * stride + px // 2, px % 2 * 4
                            expected[at] = (expected[at] & ~(15 << shift)) | ((1 if ink else 0) << shift)
                assert bytes(cpu.mem_read(header + 20, size)) == expected, (mode, height, char)
                assert bytes(cpu.mem_read(header, 20)) == raw
                assert bytes(cpu.mem_read(header - 16, 16)) == b'\xA5' * 16
                assert bytes(cpu.mem_read(header + 20 + size, 16)) == b'\xA5' * 16, (mode, height, char)
                rows.append(dict(mode=mode, height=height, character=char,
                    complete_available_pixels_and_memory_guards=True, full_tail=height >= 12))
    return rows


def footer(arm):
    cpu = machine(arm)
    section = MainCodeFile(arm, BASE).sections[3]
    cpu.mem_write(0x02387A20, bytes(section.data[:-48]))
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    cpu.mem_write(metrics + 4, struct.pack('<2I', 6, 12))
    header, heap, descriptor, texts = 0x02450000, 0x02480000, 0x02490000, 0x02491000
    cpu.mem_write(heap - 32, b'\xA5' * (1792 + 64))
    allocations, glyphs, blits = [], [], []

    def hook(uc, address, size, _):
        if address == BASE + 0x51A0:
            allocations.append(uc.reg_read(UC_ARM_REG_R0))
            assert allocations == [1792], 'Only one owned allocation permitted'
            uc.reg_write(UC_ARM_REG_R0, heap)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0xD16B4:
            code, style = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
            glyphs.append(dict(code=code, style=style, x=uc.reg_read(UC_ARM_REG_R2), y=uc.reg_read(UC_ARM_REG_R3)))
        elif address == 0x01FF92D8:
            sp = uc.reg_read(UC_ARM_REG_SP)
            source = uc.reg_read(UC_ARM_REG_R1)
            if source == header:
                extent_ptr, destination_ptr = struct.unpack('<2I', uc.mem_read(sp, 8))
                blits.append(dict(extent=list(struct.unpack('<2I', uc.mem_read(extent_ptr, 8))),
                    destination=list(struct.unpack('<2I', uc.mem_read(destination_ptr, 8)))))
            # Final GPU/parent copy is an explicit boundary; actual emulator
            # captures independently verify composition. Its source rows execute.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0xCA474:
            # Button frame art is unchanged and outside this text-buffer proof.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, hook)
    call(cpu, 0xCAA4C, (header,))
    assert allocations == [], 'Static construction must not call an uninitialized allocator'
    assert struct.unpack('<I', cpu.mem_read(header + 8, 4))[0] == 14
    call(cpu, 0xCAA4C, (header,))
    assert allocations == []
    cases, pictures = [], []
    font = GameAsciiFont.from_arm9(arm)
    tables = [0x12EC28, 0x119134, 0x11914C, 0x119308]
    for table in tables + [None]:
        if table is None:
            labels = ['g;', 'j"', 'p.', 'q!', 'y~', '[gyp,?]']
            pointers = []
            cursor = texts
            for label in labels:
                pointers.append(cursor)
                cpu.mem_write(cursor, label.encode() + b'\0')
                cursor += len(label) + 1
            cpu.mem_write(descriptor, struct.pack('<6I', *pointers))
            pointer = descriptor
        else:
            pointer = BASE + table
        if allocations:
            cpu.mem_write(heap, bytes(1792))
        glyphs.clear()
        call(cpu, 0xCA890, (header, pointer))
        assert allocations == [1792]
        assert (header + struct.unpack('<I', cpu.mem_read(header + 16, 4))[0]) & 0xFFFFFFFF == heap
        pixels = bytes(cpu.mem_read(heap, 1792))
        expected = bytearray(1792)
        for e in glyphs:
            g = font.decode(chr(e['code']))
            assert 0 <= e['x'] and e['x'] + 6 <= 256
            for y in range(11):
                for x in range(6):
                    px, py = e['x'] + x, e['y'] + 1 + y
                    assert py < 14
                    at, shift = py * 128 + px // 2, px % 2 * 4
                    expected[at] = (expected[at] & ~(15 << shift)) | ((e['style'] if g.getpixel((x, y)) else 0) << shift)
        assert pixels == expected
        assert bytes(cpu.mem_read(heap - 32, 32)) == b'\xA5' * 32
        assert bytes(cpu.mem_read(heap + 1792, 32)) == b'\xA5' * 32
        metadata = struct.unpack('<18h', cpu.mem_read(header + 0x2C, 36))
        for slot in range(6):
            # CA53C draws icon and complete text; provide its owned icon globals.
            cpu.mem_write(0x0211B5CC, struct.pack('<2I', 12, 16))
            call(cpu, 0xCA53C, (header, header + 0x2C + slot * 6, 0))
        picture = Image.new('RGB', (256, 14), '#17284a')
        picture.putdata([(238, 238, 238) if v else (23, 40, 74)
                         for b in pixels for v in [b & 15, b >> 4]])
        pictures.append(picture.resize((768, 42), Image.Resampling.NEAREST))
        cases.append(dict(table=table, glyph_count=len(glyphs), full_14_rows_equal_independent_pixels=True,
            metadata=list(metadata), full_tail_row11_preserved=True, memory_guards_intact=True))
    assert blits and all(b['extent'][1] == 14 and b['destination'][1] == 178 for b in blits)
    sheet = Image.new('RGB', (800, len(pictures) * 82 + 20), '#17252b')
    draw = ImageDraw.Draw(sheet)
    for i, (picture, case) in enumerate(zip(pictures, cases)):
        draw.text((16, i * 82 + 8), 'Native footer source ' + (hex(case['table']) if case['table'] else 'constructed descender stress labels'), fill='white')
        sheet.paste(picture, (16, i * 82 + 28))
    sheet.save(ROOT / 'native_button_descenders.png')
    return dict(cases=cases, owned_allocation_calls=allocations, final_native_text_copy_rectangles=blits,
        original_initializer_view_constructor_width_placement_font_cleanup_and_label_pixels_executed=True,
        native_allocator_return_and_final_GPU_copy_are_declared_test_boundaries=True,
        warm_constructor_reuses_single_zeroed_1792_byte_buffer=True)


if __name__ == '__main__':
    cfg = json.loads(CONFIG.read_text())
    source = NdsImage.open(cfg['predecessor_rom']).read_file('/__arm9__.bin')
    arm, proof = apply_release(source, CONFIG)
    sample = '"Wait; sail on."{LB}Aye! Ready? ~ 10 days ~{LB}Quickly, bring my spyglass!{LB}Can you judge this cargo, Rafael?'
    raw = tokens_to_bytes(parse_markup(sample), guard_linebreaks=True, pair_phase_safe_breaks=True)
    pixels, events, kanji = raster(arm, raw)
    _, prior_events, prior_kanji = raster(source, raw)
    assert events == prior_events and kanji == prior_kanji
    assert set(';".!~') <= {chr(e['code']) for e in events if e['kind'] == 'ascii'}
    save(ROOT / 'cursor_verification.json', dict(same_bytes=raw.hex(),
        before_events=prior_events, after_events=events, all_glyph_positions_identical=True,
        quotation_marks_and_every_following_character_keep_original_advance=True))
    assert pixels == expected_pixels(arm, kanji, [dict(e, y=e['y'] + 1) for e in events])
    assert sorted({e['y'] for e in events}) == [0, 16, 32, 48]
    bounds = glyph_bounds(arm)
    save(ROOT / 'native_bounds.json', dict(cases=bounds, guarded_case_count=len(bounds)))
    footer_proof = footer(arm)
    save(ROOT / 'native_font_offset_proof.json', dict(proof=proof, four_row_native_plus1_pixels_complete=True,
        widths_cursor_line_spacing_and_string_bytes_unchanged=True, guarded_glyph_cases=len(bounds),
        footer=footer_proof, hardware_verification=False))
    print('Offset,', len(bounds), 'tight-surface glyph cases, and complete native footer tails pass.')
