"""Native map tooltip pixel proof with independent newline/paired-glyph oracle."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import format_copy
from scripts.execute_scene_caption_raster import execute


def expected_glyphs(text):
    first, second = text.split('\n')
    if not second.startswith('  ') or not text.isascii():
        raise ValueError('Machine newline guard and complete ASCII required')
    odd = len(first) % 2
    if odd:
        first += ' '
    content = second[2:]
    result = [{'code': ord(c), 'style': 15, 'x': i * 6, 'y': 0} for i, c in enumerate(first)]
    result.append({'code': 32, 'style': 15, 'x': 0, 'y': 12})
    if not odd:
        result.append({'code': 32, 'style': 15, 'x': 6, 'y': 12})
    result.extend({'code': ord(c), 'style': 15, 'x': (i + 1) * 6, 'y': 12}
                  for i, c in enumerate(content))
    if (len(content) + (1 if odd else 2)) % 2:
        result.append({'code': 32, 'style': 15, 'x': (len(content) + 1) * 6, 'y': 12})
    return result


def expected_pixels(source, glyphs, mode, width, height):
    font = GameAsciiFont.from_arm9(source)
    palette = struct.unpack_from('<I', source, 0xD181C)[0] - 0x02000000
    color = struct.unpack_from('<H', source, palette + 30)[0]
    output = bytearray((256 if mode == 16 else 64) * 192 * 2)
    for glyph in glyphs:
        bitmap = font.decode(chr(glyph['code']))
        for row in range(11):
            for column in range(6):
                px, py = glyph['x'] + column, glyph['y'] + row
                if px >= width or py >= height or not bitmap.getpixel((column, row)):
                    continue
                if mode == 16:
                    struct.pack_into('<H', output, (py * 256 + px) * 2, color)
                else:
                    offset, shift = (py * 256 + px) // 2, (px % 2) * 4
                    output[offset] |= 15 << shift
    return bytes(output)


def verify_raster(source, text, mode):
    expected = expected_glyphs(text)
    width = max(map(len, text.split('\n'))) * 6
    if width > 256:
        raise ValueError('Complete tooltip exceeds physical screen width')
    result = execute(source, text, tooltip=True, mode=mode)
    if result['glyphs'] != expected or result['cp932_glyphs']:
        raise ValueError('Tooltip native glyph order/row placement/leading character differs')
    if result['tooltip_composites'][0]['width'] != width or result['tooltip_composites'][0]['height'] != 24:
        raise ValueError('Native tooltip measurement differs')
    if result['pixels'] != expected_pixels(source, expected, mode, width, 24):
        raise ValueError('Tooltip native full-buffer pixels differ')
    if result['actual_tracking'] != 0 or not {0x763C, 0xCF220, 0xCF348, 0xD5404, 0xD16B4, 0xD5140} <= set(result['executed_offsets']):
        raise ValueError('Original tooltip measurement/render/cleanup not executed')
    return {'formatted_text': text, 'mode': mode, 'width': width, 'height': 24,
            'glyph_count': len(expected), 'second_row_first_glyph_x': 6,
            'pixels_sha256': sha(result['pixels']), 'stack_registers_guard_and_cleanup_preserved': True}


def main():
    root = Path('work/analysis/map_entity_tooltips_v139')
    source = (root / 'proposed_arm9.bin').read_bytes()
    prior = json.loads((root / 'report.json').read_text())
    if sha(source) != prior['target_arm9_sha256']:
        raise ValueError('Tooltip proposal differs')
    cases = []
    for name in (b'Pirates', b'Monster', b'???', b'Fleet', b'FleetX', b'Albuquerque', b'Nagarpur Co.'):
        for ship_class in (b'Carrack', b'Armed Retonda'):
            expected = name + b'\n  ' + ship_class + b' class'
            copied = format_copy(source, 0x705F0, [name, ship_class], expected)
            text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('ascii')
            for mode in (4, 16):
                cases.append(verify_raster(source, text, mode))
    for name, percent, armament in ((b'Fleet', b'100', b'250'), (b'Monster', b'0', b'1'),
                                    (b'Ship', b'1234567', b'123456789')):
        expected = name + b'  ' + percent.rjust(6) + b'%\n  Armament ' + armament.rjust(8)
        copied = format_copy(source, 0x705F4, [name, percent, armament], expected)
        text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('ascii')
        for mode in (4, 16):
            cases.append(verify_raster(source, text, mode))
    report = {'status': 'pass-native-guarded-map-tooltip-pixels-dynamic-coverage-pending',
              'source_arm9_sha256': sha(source), 'cases': cases,
              'limitations': ['Dynamic name/class/percentage bounds are representative, not exhaustive.',
                              'Parent bitmap validity, UI state update, bitmap clear and physical composition are contracts.',
                              'Glyph copy and bitmap origin retain existing bounded contracts.',
                              'Native newline guards produce the same six-pixel continuation indent for both first-row ASCII parities.']}
    (root / 'native_raster_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} complete guarded tooltip native pixel cases pass; dynamic coverage pending.')


if __name__ == '__main__':
    main()
