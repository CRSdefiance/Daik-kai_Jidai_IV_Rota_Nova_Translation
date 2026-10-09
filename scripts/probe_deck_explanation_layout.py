"""Execute native Deck bitmap initialization and complete English explanation ink."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP

from dk4tool.patch.deck_explanation_release import format_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import ACTOR, BASE, STACK, machine_for
from scripts.execute_scene_caption_raster import execute
from scripts.probe_deck_explanation_sources import ROWS, SOURCE
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def geometry(source):
    machine = machine_for(source)
    machine.reg_write(UC_ARM_REG_R4, 1)
    machine.reg_write(UC_ARM_REG_R5, ACTOR)
    machine.emu_start(BASE + 0x19F90, BASE + 0x19FE8, count=10000)
    dims = list(struct.unpack('<2I', machine.mem_read(ACTOR + 0x38, 8)))
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x19FE8 or machine.reg_read(UC_ARM_REG_SP) != STACK or dims != [168, 84]:
        raise ValueError('Native Deck bitmap initialization differs')
    resource = list(struct.unpack('<5I', machine.mem_read(ACTOR + 0x1C38, 20)))
    if resource[:3] != [4, 42, 84]:
        raise ValueError('Native Deck packed resource differs')
    return {'dimensions': dims, 'resource_words': resource,
            'actual_resource_and_bitmap_initializer_executed': True,
            'scope': 'Successful AE220 parent-allocation result supplied; exact following resource setup and D3ABC/D3E44/D41E0 execute.'}


def main():
    source = NdsImage.open('out/all_routes_combined_v145_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if sha(source) != SOURCE:
        raise ValueError('Exact V145 required')
    spans = [(0x19F90, 0x1A000), (0xD3ABC, 0xD3AFC), (0xD3E44, 0xD3E88),
             (0xD41E0, 0xD42A0), (0x19E8C, 0x19F0C)]
    if any(source[a:b] != clean[a:b] for a, b in spans):
        raise ValueError('Deck bitmap/placement code differs from clean')
    destination = Path('work/qa/deck_explanations_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (672, 4 * 164), 'white')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for index, (room, offset, _, name, english, _) in enumerate(ROWS):
        formatted = format_paragraph(english)
        for mode in (4, 16):
            native = execute(source, formatted, tracking=0, x=0, y=0, mode=mode,
                             surface_size=(168, 84), deck=True)
            events = [e for e in native['glyph_events'] if e['code'] != 32]
            expected = [ord(c) for c in english if c != ' ']
            if [e['code'] for e in events] != expected:
                raise ValueError('Deck explanation loses leading/interior/final glyphs')
            if any(e['x'] < 0 or e['x'] + 6 > 168 or e['y'] < 0 or e['y'] + 12 > 36 for e in events):
                raise ValueError('Complete Deck prose overlaps following label at y36')
            if native['actual_tracking'] != 0 or native['pixels'] != expected_pixels(source, b'', native['glyph_events'], mode, background=9):
                raise ValueError('Native Deck tracking/pixels differ')
            cursor = 0
            for word in english.split():
                if len({e['y'] for e in events[cursor:cursor + len(word)]}) != 1:
                    raise ValueError('Deck native renderer splits a word')
                cursor += len(word)
            cases.append({'room': room, 'offset': offset, 'english': english,
                          'formatted_text': formatted, 'mode': mode,
                          'pixels_sha256': sha(native['pixels']), 'complete_words_and_glyphs_preserved': True,
                          'maximum_glyph_bottom': max(e['y'] + 12 for e in events),
                          'formatting_approved': False})
            if mode == 16:
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14
                               else (0, 0, 0) for c in struct.unpack('<49152H', native['pixels'])])
                panel = panel.crop((0, 0, 168, 36)).resize((672, 144), Image.Resampling.NEAREST)
                draw.text((8, index * 164 + 2), name, fill='black')
                sheet.paste(panel, (0, index * 164 + 20))
    path = destination / 'native_sheet.png'
    sheet.save(path)
    report = {'status': 'pass-native-deck-geometry-and-complete-ink-review-pending',
              'source_arm9_sha256': sha(source), 'geometry': geometry(source), 'cases': cases,
              'consumer_locks': [{'start': a, 'end': b, 'sha256': sha(source[a:b])} for a, b in spans],
              'native_sheet_sha256': sha(path.read_bytes()), 'candidate_changed': False,
              'limits': 'Separate native geometry/raster invocations; bitmap origin/font metrics and physical composition remain contracts. English allocation/relocation and actual caller-through-render remain pending.'}
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native Deck rasters preserve complete words and glyphs above y36.')


if __name__ == '__main__':
    main()
