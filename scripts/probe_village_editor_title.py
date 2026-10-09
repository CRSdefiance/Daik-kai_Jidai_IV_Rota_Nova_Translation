"""Verify actual editor-title bitmap arguments, printf context and native pixels."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R10

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.execute_scene_caption_raster import execute
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def main():
    source = Path('work/analysis/village_promised_words_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/village_promised_words_plan.json').read_text(encoding='utf-8'))
    if sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Village title research differs')
    row = next(r for r in plan['records'] if r['kind'] == 'MESSAGE' and r['index'] == 5)
    machine = machine_for(source)
    machine.reg_write(UC_ARM_REG_R10, 0x02431000)
    machine.emu_start(BASE + 0xB0250, BASE + 0xB0280, count=1000)
    args = list(struct.unpack('<4I', machine.mem_read(STACK, 16)))
    if args != [108, 12, 1, 0]:
        raise ValueError('Actual editor title bitmap dimensions/flags differ')
    font = NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    destination = Path('work/qa/village_promised_words_native')
    cases = []
    for mode in (4, 16):
        native = execute(source, row['english'], editor_title=True, surface_size=(108, 12),
                         x=0, y=0, mode=mode, kanji_font=font)
        events = [e for e in native['glyph_events'] if e['code'] != 32]
        if [e['code'] for e in events] != [ord(c) for c in row['english'] if c != ' ']:
            raise ValueError('Native editor title loses a leading/interior/final character')
        if any(e['x'] < 0 or e['x'] + 6 > 108 or e['y'] != 0 for e in events):
            raise ValueError('Actual editor title exceeds its 108-by-12 client')
        if native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=9):
            raise ValueError('Native editor title pixels differ from independent decoding')
        if not {0xAC378, 0xD51AC, 0xD5200, 0xCE898, 0xD5404, 0xAC358} <= set(native['executed_offsets']):
            raise ValueError('Native title constructor/printf/draw/cleanup did not execute')
        cases.append({'mode': mode, 'english': row['english'], 'pixels_sha256': sha(native['pixels']),
                      'glyph_events': native['glyph_events'], 'native_tracking': native['actual_tracking'],
                      'native_printf_template': '%-17s', 'complete_glyphs_bounds_and_independent_pixels': True})
        if mode == 16:
            panel = Image.new('RGB', (256, 192))
            colors = struct.unpack('<49152H', native['pixels'])
            panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14 else (0, 0, 0) for c in colors])
            panel.crop((0, 0, 108, 12)).resize((864, 96), Image.Resampling.NEAREST).save(destination / 'editor_title.png')
    input_cases = []
    answers = [r for r in plan['records'] if r['kind'] == 'ANSWER']
    sheet = Image.new('RGB', (1044, len(answers) * 90), 'white')
    draw = ImageDraw.Draw(sheet)
    for row in answers:
        for mode in (4, 16):
            native = execute(source, row['english'], editor_input=True, x=0, y=0,
                             mode=mode, kanji_font=font)
            content = [e for e in native['glyph_events'] if e['code'] != 32]
            if ([e['code'] for e in content] != [ord(c) for c in row['english'] if c != ' ']
                    or any(e['x'] < 0 or e['x'] + 6 > 108 or e['y'] != 0 for e in content)
                    or native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=0)
                    or not {0xB0C70, 0xD5160, 0xD5404, 0xD5140} <= set(native['executed_offsets'])):
                raise ValueError('Actual input redraw changes complete answer, pixels or bounds')
            input_cases.append({'index': row['index'], 'mode': mode, 'english': row['english'],
                                'pixels_sha256': sha(native['pixels']), 'final_x': native['final_x'],
                                'complete_glyphs_native_redraw_and_independent_pixels': True})
            if mode == 16:
                panel = Image.new('RGB', (256, 192))
                colors = struct.unpack('<49152H', native['pixels'])
                panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0) for c in colors])
                panel = panel.crop((0, 0, 128, 12)).resize((1024, 64), Image.Resampling.NEAREST)
                panel.save(destination / f'answer_{row["index"]:02d}.png')
                draw.text((10, row['index'] * 90 + 2), str(row['index']), fill='black')
                sheet.paste(panel, (10, row['index'] * 90 + 20))
    sheet.save(destination / 'answer_sheet.png')
    proof = {'status': 'pass-native-editor-title-geometry-printf-and-paired-pixels',
             'arm9_sha256': sha(source), 'actual_bitmap_stack_arguments': args, 'cases': cases,
             'actual_input_redraw_cases': input_cases,
             'visual_review': {'complete': False},
             'limitations': 'Connected separate native geometry/title printf and actual B0C70 input-redraw invocations. Parent bitmap origin/construction, whole-bitmap clear and physical/editor input composition remain contracts; complete answer ink is bounded to 108 pixels.'}
    Path('work/analysis/village_promised_words_title_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Two actual title pixel modes and 48 actual input-redraw cases pass; complete title/answers fit 108 pixels.')


if __name__ == '__main__':
    main()
