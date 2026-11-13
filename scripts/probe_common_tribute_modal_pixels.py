"""Connect corrected native preparation to actual modal CP932 glyph painting."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def verify(source, font, text, mode, *, guarded=False, portrait=False):
    native = execute(source, text, modal=True, mode=mode, kanji_font=font,
                     modal_guarded=guarded, portrait=portrait)
    codes = [int.from_bytes(character.encode('cp932'), 'big') for character in text if character not in (' ', '\n')]
    events = [event for event in native['glyph_events'] if event['code'] != 32]
    if [event['code'] for event in events] != codes:
        raise ValueError('Native modal text loses leading, interior or final glyphs')
    if any(event['x'] < 0 or event['y'] < 0
           or event['x'] + (12 if event['kind'] == 'cp932' else 6) > 256
           or event['y'] + 12 > 96 for event in events):
        raise ValueError('Native modal glyph exceeds actual mode-zero bounds')
    if native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=9):
        raise ValueError('Native modal full-buffer pixels differ from independent font decoding')
    required = {0x548A8, 0xD5160, 0xD5A10, 0xD5A18, 0xD5A2C, 0xD5404, 0xD16B4, 0xD5140}
    if not required <= set(native['executed_offsets']) or native['cp932_pixel_painter_is_contract']:
        raise ValueError('Actual modal pipeline and CP932 painter did not execute')
    return native


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    proof_path = Path('work/analysis/common_tribute_loaded_copy_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    unique = {case['name_hex']: case['complete_prepared_text'] for case in proof['cases']}
    destination = Path('work/qa/common_tribute_native_modal')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1044, len(unique) * 230), 'white')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for index, (name, text) in enumerate(unique.items()):
        for mode in (4, 16):
            native = verify(source, font, text, mode)
            rows = sorted({event['y'] for event in native['glyph_events']})
            content_events = [event for event in native['glyph_events'] if event['code'] != 32]
            cursor, broken_words = 0, []
            for word in text.split():
                glyph_rows = sorted({event['y'] for event in content_events[cursor:cursor + len(word)]})
                if len(glyph_rows) > 1:
                    broken_words.append({'word': word, 'row_origins': glyph_rows})
                cursor += len(word)
            cases.append({'stored_name_hex': name, 'mode': mode, 'prepared_text': text,
                          'row_origins': rows, 'glyph_count': len(native['glyph_events']),
                          'pixels_sha256': sha(native['pixels']),
                          'complete_nonblank_glyphs_and_independent_pixels_match': True,
                          'split_words': broken_words, 'formatting_approved': False})
            if mode == 16:
                colors = struct.unpack('<49152H', native['pixels'])
                panel = Image.new('RGB', (256, 192))
                # Diagnostic ink view; raw native pixel hashes remain unchanged.
                panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14
                               else (0, 0, 0) for c in colors])
                panel = panel.crop((0, 0, 256, 96)).resize((1024, 192), Image.Resampling.NEAREST)
                path = destination / f'name_{index:02d}.png'
                panel.save(path)
                draw.text((10, index * 230 + 8), name, fill='black')
                sheet.paste(panel, (10, index * 230 + 30))
    sheet.save(destination / 'native_sheet.png')
    report = {'status': 'native-modal-glyphs-pixels-pass-word-wrapping-unresolved',
              'renderer_arm9_sha256': sha(source), 'prepared_proof_sha256': sha(proof_path.read_bytes()),
              'font_sha256': sha(font), 'cases': cases,
              'limitations': 'Connected separate invocations: research hooked loader/preparation then unchanged V142 modal pipeline. Parent bitmap origin/physical routing and input dismissal are contracts; cold-cache disk I/O and full hardware boot are unproven. These modal results do not approve the portrait-bearing monthly actor windows.'}
    (destination / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} actual native town modal cases preserve glyph order and match independently decoded full pixels.')


if __name__ == '__main__':
    main()
