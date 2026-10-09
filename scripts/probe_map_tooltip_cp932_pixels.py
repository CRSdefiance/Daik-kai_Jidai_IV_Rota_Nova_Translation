"""Compare actual ITCM glyph painting with independent font/pixel decoding."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import REFERENCE_KANJI_FONT_SHA256, GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import format_copy
from scripts.execute_scene_caption_raster import execute
from scripts.probe_map_tooltip_numeric_values import execute_pair, verify_mixed


def expected_pixels(source, font, events, mode, *, background=0):
    ascii_font = GameAsciiFont.from_arm9(source)
    mapping = struct.unpack_from('<3340H', source, 0x125EC4)
    palette = struct.unpack_from('<16H', source, 0x125A20)
    canvas = [[background] * 256 for _ in range(192)]
    for glyph in events:
        x, y, code, style = (glyph[k] for k in ('x', 'y', 'code', 'style'))
        if glyph['kind'] == 'ascii':
            bitmap = ascii_font.decode(chr(code))
            for row in range(11):
                for column in range(6):
                    if bitmap.getpixel((column, row)):
                        canvas[y + row][x + column] = palette[style] if mode == 16 else style
                    elif mode == 4:
                        canvas[y + row][x + column] = 0
            continue
        if code not in mapping:
            raise ValueError('CP932 glyph has no source font-map entry')
        index = mapping.index(code)
        cell = font[index * 22:(index + 1) * 22]
        ink = [(column, row) for row in range(11) for column in range(11)
               if cell[row * 2 + column // 8] & (0x80 >> (column % 8))]
        # Original D1964: style 15 shades with 14, styles 7..14 with zero,
        # and other styles with 15. A nonzero font flag disables the shadow.
        shadow = 14 if style == 15 else 0 if 7 <= style <= 14 else 15
        shadow_enabled = glyph.get('font_flags', 0) == 0
        if mode == 16:
            # Native painter visits rows top-to-bottom; future foreground replaces
            # a shadow pixel at that position. Decode both layers independently.
            if shadow_enabled:
                for column, row in ink:
                    canvas[y + row + 1][x + column + 1] = shadow
            for column, row in ink:
                canvas[y + row][x + column] = palette[style]
        else:
            # Native paletted painter clears a complete 12x12 cell, paints the
            # 11x11 mask, then shades lower-right empty cells bottom-to-top.
            for row in range(12):
                for column in range(12):
                    canvas[y + row][x + column] = 0
            for column, row in ink:
                canvas[y + row][x + column] = style
            if shadow_enabled:
                for row in range(11, 0, -1):
                    for column in range(11):
                        if canvas[y + row - 1][x + column] and not canvas[y + row][x + column + 1]:
                            canvas[y + row][x + column + 1] = shadow
    output = bytearray((256 if mode == 16 else 64) * 192 * 2)
    for y, row in enumerate(canvas):
        for x, color in enumerate(row):
            if mode == 16:
                struct.pack_into('<H', output, (y * 256 + x) * 2, color)
            else:
                output[(y * 256 + x) // 2] |= color << ((x % 2) * 4)
    return bytes(output)


def verify(source, font, name, percentage, armament, mode):
    if sha(font) != REFERENCE_KANJI_FONT_SHA256:
        raise ValueError('Exact clean ROM Kanji font asset required')
    # This earlier proof independently establishes every nonblank ASCII/CP932
    # request and its position from the actual numeric getters/converter/copy.
    requests = verify_mixed(source, name, percentage, armament, mode)
    numbers = execute_pair(source, percentage, armament)
    percent, rating = (bytes.fromhex(numbers[key]) for key in ('percent_hex', 'armament_hex'))
    expected = name.encode('ascii') + b'  ' + percent.rjust(6) + b'%\n  Armament ' + rating.rjust(8)
    copied = format_copy(source, 0x705F4, [name.encode('ascii'), percent, rating], expected)
    text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('cp932')
    native = execute(source, text, tooltip=True, mode=mode, kanji_font=font)
    if native['cp932_glyphs'] != requests['cp932_glyph_requests']:
        raise ValueError('Actual ITCM painter changes native numeric requests')
    if native['cp932_pixel_painter_is_contract'] or not {0x01FF83AC, 0x01FF83D4} <= set(native['itcm_executed_addresses']):
        raise ValueError('Actual ITCM glyph painter not executed')
    if not {0xD198C, 0xD19BC} <= set(native['executed_offsets']):
        raise ValueError('Native font-map lookup not executed')
    if any(native['cp932_font_flags']):
        raise ValueError('Unexpected tooltip font shadow setting')
    oracle = expected_pixels(source, font, native['glyph_events'], mode)
    if oracle != native['pixels']:
        offsets = [i for i, (a, b) in enumerate(zip(oracle, native['pixels'])) if a != b]
        raise ValueError(f'Independent full-buffer CP932 pixels differ at {offsets[:12]}')
    return {'name': name, 'percentage': percentage, 'armament': armament, 'mode': mode,
            'pixels_sha256': sha(native['pixels']), 'width': requests['width'],
            'cp932_glyphs': native['cp932_glyphs'], 'font_flags': native['cp932_font_flags'],
            'native_itcm_and_font_lookup_executed': True, 'independent_full_buffer_pixels_match': True,
            'stack_registers_and_buffer_guards_preserved': native['stack_and_registers_preserved']}


def verify_name(source, font, name, ship_class, mode):
    if sha(font) != REFERENCE_KANJI_FONT_SHA256:
        raise ValueError('Exact clean ROM Kanji font asset required')
    raw_name, raw_class = name.encode('cp932'), ship_class.encode('ascii')
    if not 1 <= len(raw_name) <= 18:
        raise ValueError('Player faction name outside actual eighteen-byte limit')
    expected = raw_name + b'\n  ' + raw_class + b' class'
    copied = format_copy(source, 0x705F0, [raw_name, raw_class], expected)
    text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('cp932')
    native = execute(source, text, tooltip=True, mode=mode, kanji_font=font)
    codes = [int.from_bytes(character.encode('cp932'), 'big') for character in text
             if character not in (' ', '\n')]
    events = [glyph for glyph in native['glyph_events'] if glyph['code'] != 32]
    if [glyph['code'] for glyph in events] != codes:
        raise ValueError('Mixed player-name/class glyph sequence loses complete characters')
    first_class = next(g for g in events if g['y'] == 12)
    if first_class['x'] != 6 or first_class['code'] != ord(ship_class[0]):
        raise ValueError('Mixed player-name tooltip drops/misplaces leading class character')
    if native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode):
        raise ValueError('Independent full-buffer CP932 name pixels differ')
    width = max(len(line.encode('cp932')) for line in text.split('\n')) * 6
    if width > 256 or native['tooltip_composites'][0]['width'] != width:
        raise ValueError('Complete player-name tooltip exceeds or differs from native width')
    return {'name_hex': raw_name.hex(), 'ship_class': ship_class, 'mode': mode, 'width': width,
            'pixels_sha256': sha(native['pixels']), 'leading_class_x': first_class['x'],
            'complete_ordered_glyph_sequence_and_independent_pixels_match': True}


def main():
    root = Path('work/analysis/map_creature_complete_v139')
    source = (root / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((root / 'report.json').read_text())
    if sha(source) != allocation['target_arm9_sha256']:
        raise ValueError('Complete proposed ARM9 differs')
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    font = clean_rom.read_file('/GRP/KANJI.FNT')
    current_rom = NdsImage.open('out/all_routes_combined_v139_candidate.nds')
    if current_rom.read_file('/GRP/KANJI.FNT') != font:
        raise ValueError('Current candidate Kanji font asset differs from clean')
    for lo, hi in ((0xD1898, 0xD1A50), (0x125A20, 0x125A60),
                   (0x125EC4, 0x125EC4 + 3340 * 2)):
        if source[lo:hi] != clean[lo:hi]:
            raise ValueError('Native CP932 palette/map/lookup code differs')
    for image in (clean, source):
        sections = [s for s in MainCodeFile(image, 0x02000000).sections if s.ramAddress == 0x01FF8000]
        if len(sections) != 1:
            raise ValueError('Unmapped ITCM autoload')
        if image is clean:
            itcm = bytes(sections[0].data)
        elif bytes(sections[0].data[0x3AC:0x5C8]) != itcm[0x3AC:0x5C8]:
            raise ValueError('Inherited ITCM painter changed')
    cases = [verify(source, font, name, pct, arm, mode)
             for name in ('Fleet', 'FleetX', 'A' * 18)
             for pct, arm in [(digit, digit) for digit in range(10)] + [(255, 65535)]
             for mode in (4, 16)]
    name_cases = [verify_name(source, font, name, ship_class, mode)
                  for name in ['ア' * size for size in range(1, 10)]
                  + ['A' + 'ア' * size for size in range(1, 9)]
                  for ship_class in ('Monster Fish', 'Giant Squid') for mode in (4, 16)]
    report = {'status': 'pass-real-itcm-full-width-numeric-pixels', 'target_arm9_sha256': sha(source),
              'font_sha256': sha(font), 'clean_itcm_sha256': sha(itcm),
              'unchanged_painter_span_sha256': sha(itcm[0x3AC:0x5C8]),
              'case_count': len(cases), 'cases': cases, 'name_case_count': len(name_cases), 'name_cases': name_cases,
              'limitations': ['Font loading is initialized from exact clean ROM asset; disk loader not executed.',
                             'Bitmap origin/clear/physical compositor retain existing contracts.',
                             'Physical palette/routing and gameplay remain pending.',
                             'No ROM integration or formatting approval.']}
    (root / 'native_cp932_pixel_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(cases)} real ITCM numeric and {len(name_cases)} CP932 player-name full-buffer pixel comparisons pass.')


if __name__ == '__main__':
    main()
