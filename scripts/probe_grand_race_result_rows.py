"""Audit complete printf result rows and a caller-scoped wider-frame proposal."""

import argparse
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_copy import execute as execute_name_copy
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    BASE,
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_wireless_return import check_branch, resolve_pc_load, word


def assemble_row(place, number, name):
    """Conditional model: name is a complete, terminated 16-byte-or-shorter field."""
    if any(not value or any(ord(c) < 32 or ord(c) > 126 for c in value)
           for value in (place, number)):
        raise ValueError('Label must be printable ASCII')
    if not name or len(name) > 16 or b'\0' in name:
        raise ValueError('Complete name must contain 1 through 16 bytes without NUL')
    decoded = name.decode('cp932')
    if any(ord(c) < 32 for c in decoded):
        raise ValueError('Name contains a control character')
    raw = place.encode('ascii') + b' ' + number.encode('ascii') + b' ' + name
    if len(raw) + 1 > 32:
        raise ValueError('Complete printf output exceeds the native 32-byte buffer')
    # D1604 advances 6 px for ASCII and 12 px for double-byte CP932 characters.
    width = sum(6 if len(c.encode('cp932')) == 1 else 12 for c in raw.decode('cp932'))
    return raw + b'\0', width


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned ROM differs')
    inputs = [NdsImage.open(path).read_file('/__arm9__.bin')
              for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    source = inputs[0]
    if hashlib.sha256(source).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese ARM9 differs')
    locks = []
    for lo, hi in ((0xF7950, 0xF8058), (0xFB324, 0xFB4C0), (0xFB004, 0xFB038),
                   (0xD7720, 0xD77BC), (0xD1604, 0xD1850),
                   (0x12ED04, 0x12ED0C), (0x12EDEC, 0x12EDFC),
                   (0x12EE6C, 0x12EE7C), (0x16B8E0, 0x16B8EC),
                   (0x16BAA0, 0x16BAAC), (0xFA5B0, 0xFA63C),
                   (0xF8B88, 0xF8BA8), (0xF9BD8, 0xF9BF8),
                   (0xFB780, 0xFB830), (0xFC1D4, 0xFC218),
                   (0xFC654, 0xFC698), (0x10BC3C, 0x10BD0C),
                   (0x10C4E8, 0x10C590), (0x16BBA0, 0x16BBA8),
                   (0xF8EC4, 0xF8F00), (0xF9C34, 0xF9C70),
                   (0xCB184, 0xCB190), (0xCBF18, 0xCBF2C),
                   (0xCC3EC, 0xCC3F0), (0x148E94, 0x148EB8),
                   (0x1371C, 0x13724), (0x830A0, 0x830D8),
                   (0x82FA8, 0x82FE0), (0x469DC, 0x46A1C),
                   (0x46BE0, 0x46C20), (0xD010C, 0xD016C),
                   (0xD01AC, 0xD0264), (0xCD6CC, 0xCD6EC), (0xCED98, 0xCEDC8)):
        if any(data[lo:hi] != source[lo:hi] for data in inputs[1:]):
            raise ValueError(f'Result caller/renderer differs at {lo:#x}')
        locks.append({'start': lo, 'end': hi,
                      'sha256': hashlib.sha256(source[lo:hi]).hexdigest()})
    for at, reg, literal, target in (
        (0xF7C0C, 0, 0xF8010, 0x125978),
        (0xF7C10, 6, 0xF8024, 0x12ED04),
        (0xF7DC8, 1, 0xF8034, 0x16B8E0),
        (0xF7DA4, 3, 0xF8030, 0x12EE6C),
        (0xF7DD4, 3, 0xF8038, 0x12EDEC),
        (0xF7C6C, 1, 0xF802C, 0x16BAA0),
    ):
        resolve_pc_load(source, at, reg, literal)
        if word(source, literal) != BASE + target:
            raise ValueError('Result source table/format differs')
    for at, target in ((0xF7DE0, 0xD7720), (0xF7E18, 0xFB004),
                       (0xFB494, 0xD1604), (0xD7740, 0xD7754)):
        check_branch(source, at, target)
    if source[0x16B8E0:0x16B8E9] != b'%s %s %s\0':
        raise ValueError('Printf format differs')
    if tuple(word(source, 0x16BAA0 + i * 4) - BASE for i in range(3)) != (
            0xFB324, 0xFB004, 0xFAFFC):
        raise ValueError('Framed widget methods differ')
    required = {0xF7D44: 0xE28D1FC5,  # SP+0x314, four 32-byte output buffers.
                0xF7D48: 0xE0815280, 0xF7D3C: 0xE0010190,
                0xF7D40: 0xE281B020, 0xF7E3C: 0xE28BB01C,
                0xF7E6C: 0xE2877011, 0xF7DD0: 0xE7932102,
                0xF7DDC: 0xE7933109, 0xF7DCC: 0xE58D0000}
    if any(word(source, at) != value for at, value in required.items()):
        raise ValueError('Printf indexing, name stride or row positions differ')
    geometry_refs = [i for i in range(0, len(source) - 3, 4)
                     if word(source, i) == BASE + 0x12ED04]
    if geometry_refs != [0xF8024]:
        raise ValueError('Wider-frame proposal has an additional aligned consumer')
    if struct.unpack_from('<2I', source, 0x12ED04) != (156, 12):
        raise ValueError('Original framed-row dimensions differ')
    # FA5B0 copies all 17 packet bytes. It does not synthesize a terminator:
    # byte 17 is loaded from the packet and stored after the 16-byte loop.
    copy_required = {0xFA5BC: 0xE3A03011, 0xFA5DC: 0xE3A0E008,
                     0xFA5E0: 0xE4D4C001, 0xFA5E4: 0xE4D43001,
                     0xFA5EC: 0xE4C5C001, 0xFA5F0: 0xE4C53001,
                     0xFA604: 0xE5D40000, 0xFA610: 0xE5C50000}
    if any(word(source, at) != value for at, value in copy_required.items()):
        raise ValueError('Native packet-name copy differs')
    for at, target in ((0xF8BA4, 0xFB780), (0xF9BF4, 0xFB780),
                       (0xFB598, 0x10C524), (0x10C584, 0x10C4E8),
                       (0xFC664, 0x10BC3C)):
        check_branch(source, at, target)
    resolve_pc_load(source, 0xFB788, 4, 0xFB81C)
    resolve_pc_load(source, 0xFC658, 2, 0xFC694)
    if (word(source, 0xFB81C) != 0x0237B560
            or word(source, 0xFC694) != 0x0237B560
            or struct.unpack_from('<2I', source, 0x16BBA0) != (0x0237B560, 16)):
        raise ValueError('Connection metadata name field differs')
    sender_required = {0xFB790: 0xE3A03008, 0xFB794: 0xE4D12001,
                       0xFB798: 0xE4D10001, 0xFB7A0: 0xE4C42001,
                       0xFB7A4: 0xE4C40001, 0x10BCC4: 0xE3A02018}
    if any(word(source, at) != value for at, value in sender_required.items()):
        raise ValueError('Connection name initialization differs')
    resolve_pc_load(source, 0xF8EC8, 1, 0xF9154)
    resolve_pc_load(source, 0xF9C38, 1, 0xFA0F4)
    resolve_pc_load(source, 0xCBF1C, 2, 0xCC3EC)
    if (word(source, 0xF9154) != 0x19E4 or word(source, 0xFA0F4) != 0x19E4
            or word(source, 0xCB18C) != 0x022D4340
            or word(source, 0xCC3EC) != BASE + 0x148E94
            or word(source, 0x148EB4) != BASE + 0x1371C
            or word(source, 0x1371C) != 0xE2800020
            or word(source, 0x13720) != 0xE12FFF1E):
        raise ValueError('Concrete name accessor differs')
    for start in (0xF8ED8, 0xF9C48):
        expected = (0xE28A4E17, 0xE3A03008, 0xE4D02001, 0xE4D01001,
                    0xE2533001, 0xE4C42001, 0xE4C41001, 0x1AFFFFF9,
                    0xE5D00000, 0xE5C40000)
        if tuple(word(source, start + i * 4) for i in range(10)) != expected:
            raise ValueError('Game-payload complete name copy differs')
    check_branch(source, 0xCD6E8, 0xCED98)
    name_copy_executions = [execute_name_copy(inputs[2], name) for name in
                            (b'', b'ABCDEFGHIJKLMNOP', '一二三四五六七八'.encode('cp932'))]
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {r['id'].removeprefix('GRAND_RACE_UI_'): r for r in
            json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    for prefix, table in (('PLACE_', 0x12EE6C), ('NUMBER_', 0x12EDEC)):
        for n in range(4):
            part = rows[prefix + str(n + 1)]['source_parts_in_reading_order'][0]
            raw = bytes.fromhex(part['source_hex'])
            start = part['offset']
            if word(source, table + n * 4) != BASE + start or source[start:start + len(raw)] != raw:
                raise ValueError('Placement/player source order differs')
    cases = []
    for rank in range(1, 5):
        for player in range(1, 5):
            raw, width = assemble_row(rows[f'PLACE_{rank}']['english'],
                                      rows[f'NUMBER_{player}']['english'], b'ABCDEFGHIJKLMNOP')
            cases.append({'rank': rank, 'player': player,
                          'text': raw[:-1].decode('ascii'), 'bytes_with_nul': len(raw),
                          'width_px': width, 'original_frame_overflow_px': max(0, width - 156),
                          'proposed_frame_spare_px': 180 - width})
    output = Path('work/qa/grand_race_result_rows')
    output.mkdir(parents=True, exist_ok=True)
    font = GameAsciiFont.from_arm9(inputs[2])
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native ASCII font differs')
    sheet = Image.new('RGB', (1024, 412), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, width in enumerate((156, 180)):
        panel = Image.new('RGB', (256, 192), '#eef1f5')
        rect = ImageDraw.Draw(panel)
        x = (256 - width) // 2
        for n in range(4):
            y = 32 + n * 28
            rect.rectangle((x, y, x + width - 1, y + 11), outline='#ab3040' if index == 0 else '#407a50')
            text = cases[n * 4 + n]['text']
            for pos, char in enumerate(text):
                panel.paste('#183047', (x + pos * 6, y), font.decode(char))
        label = 'Original 156 px: complete English exceeds frame' if index == 0 else 'Proposed caller-only 180 px: complete English fits'
        draw.text((index * 512 + 4, 4), label, fill='black')
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (index * 512, 28))
    sheet.save(output / 'sheet.png')
    report = {'candidate_sha256': CANDIDATE_SHA,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'consumer_locks': locks, 'geometry_aligned_references': geometry_refs,
              'conditional_name_limit_bytes': 16, 'name_producer_limit_verified': False,
              'native_packet_name_copy': {'function': 0xFA5B0, 'copied_bytes': 17,
                                          'synthesizes_terminator': False,
                                          'packet_writer_requires_proof': True},
              'connection_name_initialization': {
                  'join_call': 0xF8BA4, 'host_call': 0xF9BF4,
                  'source': 'CB184 owner +0x19e4 interface; vtable 0x148e94 +0x20 invokes 0x1371c',
                  'copier': 0xFB780, 'destination': 0x0237B560,
                  'copied_bytes': 16, 'synthesizes_terminator': False,
                  'host_metadata_table': 0x16BBA0, 'host_declared_name_bytes': 16,
                  'join_registration_copy_bytes': 24,
                  'scope': 'Connection metadata only; not proof of the game payload name producer.',
              },
              'game_payload_getter': {'caller': 0xFB598, 'getter': 0x10C524,
                                      'address_calculation': 0x10C4E8,
                                      'scope': 'Computes packet pointer; does not impose a name terminator.'},
              'game_payload_name_writers': {
                  'join_copy': 0xF8ED8, 'host_copy': 0xF9C48,
                  'destination': 'UI owner +0x170 (game payload +0x10)',
                  'copied_bytes': 17, 'synthesizes_terminator': False,
                  'source_owner': 0x022D4340, 'interface_offset': 0x19E4,
                  'name_accessor': 0x1371C, 'field_offset': 0x20,
                  'load_method': 0x82FA8, 'load_bytes': 17,
                  'save_method': 0x830A0, 'save_bytes': 17,
                  'population_method': 0xCD6CC, 'population_copier': 0xCED98,
                  'scope': 'Concrete stored field resolved; its termination invariant remains pending.',
              },
              'native_name_copy_executions': name_copy_executions,
              'printf_format': '%s %s %s', 'output_buffer_bytes': 32,
              'cases': cases, 'proposed_width': 180, 'proposed_text_x': 38,
              'row_y': [32, 60, 88, 116], 'preview_reviewed': args.reviewed,
              'rom_written': False,
              'limitations': ['Name producer termination/limit requires proof; 17-byte stride is insufficient.',
                              'Unaligned/dynamic geometry consumers remain unproven.',
                              'Preview outlines show text areas, not native frame graphics.',
                              'No native printf execution, full-screen composition or gameplay acceptance.',
                              'No geometry edit has been integrated.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'cases': len(cases), 'width_px': cases[0]['width_px'],
                      'preview': str(output / 'sheet.png'), 'rom_written': False}))


if __name__ == '__main__':
    main()
