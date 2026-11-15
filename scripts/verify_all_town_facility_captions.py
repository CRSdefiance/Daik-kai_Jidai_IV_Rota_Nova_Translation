"""All 12 source town types through both original native caption layouts.

Uses an explicitly captured, initialized Lisbon UI as an isolated CPU fixture;
does not claim earned access, natural visits or facility effects in every town.
"""
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_glyph_right_bounds import propose
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine, call

ROOT = Path('../tmp/lisbon_office_fix')
TYPES = ['Square', 'Market', 'Yard', 'Port', 'Tavern', 'Guild', 'Palace', 'Govt',
         'Inn', 'Ruins', 'Church', 'Gate']


def main():
    source = NdsImage.open('out/all_routes_combined_v8865_candidate.nds').read_file('/__arm9__.bin')
    target, patches = propose(source)
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ram = (ROOT / 'observed_hover2/observer/Guild_before_ram.bin').read_bytes()
    native = ROOT / 'native_trace/capture_native_state_004700'
    itcm = (native / 'arm9_itcm.bin').read_bytes()
    dtcm = (native / 'arm9_dtcm.bin').read_bytes()
    state = json.loads((native / 'native_state.json').read_text(encoding='utf-8'))
    section = MainCodeFile(target, 0x02000000).sections[4]
    fixed_itcm = bytearray(itcm)
    fixed_itcm[0x4000:0x5000] = section.data
    fixed_itcm[0x42D8:0x42DC] = itcm[0x42D8:0x42DC]  # Existing footer cache only.
    ui, caption = 0x021922A4, 0x02192AC0
    font = GameAsciiFont.from_arm9(target)
    cpu = machine(target)
    events = []

    def glyph(uc, address, size, data):
        code, style = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
        events.append(dict(code=code, style=style, x=uc.reg_read(UC_ARM_REG_R2), y=uc.reg_read(UC_ARM_REG_R3)))

    cpu.hook_add(UC_HOOK_CODE, glyph, begin=0x020D16B4, end=0x020D16B4)
    results, pictures = [], []
    old_failures = []
    old_cpu = machine(source)
    for variant in [0, 1]:
        for index, label in enumerate(TYPES):
            old_cpu.mem_write(0x02000000, ram)
            old_cpu.mem_write(0x01FF8000, itcm)
            old_cpu.mem_write(state['DTCM_region'], dtcm)
            old_cpu.mem_write(ui + 0x894, struct.pack('<I', variant))
            header = struct.unpack('<I', old_cpu.mem_read(caption + 16, 4))[0]
            before_header = bytes(old_cpu.mem_read(header, 20))
            call(old_cpu, 0xB8014, (ui, index), instruction_limit=500000)
            after_header = bytes(old_cpu.mem_read(header, 20))
            if after_header != before_header:
                old_failures.append(dict(facility_ID=index, English=label, alternate_layout=bool(variant),
                    header_before=before_header.hex(), header_after=after_header.hex()))
    assert [(r['alternate_layout'], r['facility_ID']) for r in old_failures] == [(False, 5), (False, 9), (True, 5), (True, 9)]
    from PIL import Image, ImageDraw
    for variant in [0, 1]:
        for index, label in enumerate(TYPES):
            cpu.mem_write(0x02000000, ram)
            cpu.mem_write(0x01FF8000, bytes(fixed_itcm))
            cpu.mem_write(state['DTCM_region'], dtcm)
            for p in patches['patches']:
                if p['offset'] in [0xD1738, 0xD17F4]:
                    cpu.mem_write(0x02000000 + p['offset'], bytes.fromhex(p['after_hex']))
            cpu.mem_write(ui + 0x894, struct.pack('<I', variant))
            header = struct.unpack('<I', cpu.mem_read(caption + 16, 4))[0]
            before_header = bytes(cpu.mem_read(header, 20))
            mode, pitch, height, palette_offset, pixel_offset = struct.unpack('<5I', before_header)
            assert (mode, pitch, height) == (4, 9, 12)
            pixels = (header + pixel_offset) & 0xFFFFFFFF
            events.clear()
            call(cpu, 0xB8014, (ui, index), instruction_limit=500000)
            assert bytes(cpu.mem_read(header, 20)) == before_header, (variant, label, 'image header')
            pointer = struct.unpack('<I', cpu.mem_read(caption + 48, 4))[0]
            actual_label = bytes(cpu.mem_read(pointer, 32)).split(b'\0')[0].decode('ascii')
            assert actual_label == label
            clean_pointer = struct.unpack_from('<I', original, 0x11A8F0 + index * 4)[0]
            japanese = original[clean_pointer-0x02000000:].split(b'\0')[0].decode('cp932')
            codes = ''.join(chr(e['code']) for e in events)
            assert codes.rstrip(' ') == label, (label, codes)
            expected = bytearray(216)
            for e in events:
                assert e['style'] == 15 and e['y'] == 0
                char = font.decode(chr(e['code']))
                for y in range(11):
                    for x in range(max(0, min(6, 36-e['x']))):
                        px, py = e['x'] + x, y + 1
                        if char.getpixel((x, y)):
                            at, shift = py * 18 + px // 2, px % 2 * 4
                            expected[at] |= 15 << shift
                if e['code'] != 32:
                    assert 0 <= e['x'] and e['x'] + 6 <= 36, 'Only synthetic blank may be clipped'
            actual = bytes(cpu.mem_read(pixels, 216))
            assert actual == expected, (variant, label, 'complete pixels')
            assert bytes(cpu.mem_read(0x01FFC300, 96)) == bytes(section.data[0x300:0x360])
            picture = Image.new('RGB', (36, 12), '#76c8d2')
            picture.putdata([(0, 8, 0) if n else (118, 200, 210) for b in actual for n in (b & 15, b >> 4)])
            pictures.append(picture.resize((216, 72), Image.Resampling.NEAREST))
            results.append(dict(facility_ID=index, English=label, Japanese=japanese, alternate_layout=bool(variant),
                original_caption_getter_layout_clear_font_and_return_executed=True,
                complete_bitmap_matches_independent_font=True, header_intact=True, glyphs=events.copy(),
                no_visible_letter_clipped=True, immutable_clip_helper_intact=True))
    sheet = Image.new('RGB', (640, 24 * 94 + 20), '#182b36')
    draw = ImageDraw.Draw(sheet)
    for n, (row, picture) in enumerate(zip(results, pictures)):
        draw.text((12, 12+n*94), f"ID {row['facility_ID']} {row['English']} / {'alternate' if row['alternate_layout'] else 'standard'}", fill='white')
        sheet.paste(picture, (300, 8+n*94))
    sheet.save(ROOT / 'all_24_facility_captions.png')
    result = dict(source_table_facility_count=12, complete_native_cases=24, predecessor_native_cases=24,
        predecessor_header_overwrites=old_failures, facilities=results,
        fixture='Captured initialized Lisbon UI; facility ID and original layout branch supplied in isolated CPU copies.',
        every_town_natural_visit_or_effect_or_GPU_coverage=False)
    (ROOT / 'all_town_facility_captions.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('All12 town types, both original native layouts, complete glyph pixels/headers/ABI pass.')


if __name__ == '__main__':
    main()
