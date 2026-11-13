"""Test runtime word-wrap output against actual modal glyph/pixel drawing."""

import json
import re
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_modal_pixels import verify


def wrap_expanded(text):
    if not text or '\n' in text or '\r' in text or any(ord(c) < 32 for c in text):
        raise ValueError('One complete expanded paragraph required')
    if text.strip() != text:
        raise ValueError('Expanded notice requires no outer whitespace')
    rows, current, width = [], '', 0
    for spaces, word in re.findall(r'( *)([^ ]+)', text):
        word_width = len(word.encode('cp932')) * 6
        budget = 234 if not rows else 228
        if word_width > 228:
            raise ValueError('Complete word exceeds guarded modal content width')
        required = word_width + len(spaces) * 6
        if current and width + required > budget:
            rows.append(current)
            current, width = '', 0
            spaces = spaces[1:]
        current += spaces + word
        width += word_width + len(spaces) * 6
    rows.append(current)
    if len(rows) > 4:
        raise ValueError('Expanded paragraph exceeds reviewed four-row limit')
    return '\n  '.join(rows)


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    proof_path = Path('work/analysis/common_tribute_loaded_copy_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    unique = {case['name_hex']: case['complete_prepared_text'] for case in proof['cases']}
    destination = Path('work/qa/common_tribute_guarded_modal')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1044, len(unique) * 230), 'white')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for index, (name, original) in enumerate(unique.items()):
        guarded = wrap_expanded(original)
        if guarded.replace('\n  ', ' ') != original:
            raise ValueError('Generated runtime wrapping changes original prose')
        for mode in (4, 16):
            native = verify(source, font, guarded, mode, guarded=True)
            events = [event for event in native['glyph_events'] if event['code'] != 32]
            cursor = 0
            for word in original.split():
                locations = events[cursor:cursor + len(word)]
                if len({event['y'] for event in locations}) != 1:
                    raise ValueError('Guarded native output splits a complete word or money value')
                cursor += len(word)
            cases.append({'stored_name_hex': name, 'mode': mode, 'original': original,
                          'generated_runtime_text': guarded, 'pixels_sha256': sha(native['pixels']),
                          'whole_words_numbers_and_leading_glyphs_preserved': True})
            if mode == 16:
                panel = Image.new('RGB', (256, 192))
                colors = struct.unpack('<49152H', native['pixels'])
                panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14
                               else (0, 0, 0) for c in colors])
                panel = panel.crop((0, 0, 256, 96)).resize((1024, 192), Image.Resampling.NEAREST)
                panel.save(destination / f'name_{index:02d}.png')
                draw.text((10, index * 230 + 8), name, fill='black')
                sheet.paste(panel, (10, index * 230 + 30))
    sheet.save(destination / 'native_sheet.png')
    report = {'status': 'pass-generated-runtime-word-wrap-native-glyphs-pixels-not-installed',
              'renderer_arm9_sha256': sha(source), 'source_proof_sha256': sha(proof_path.read_bytes()),
              'cases': cases, 'limitations': 'Runtime expanded text is wrapped by a Python reference, then actual modal renderer/painter executes. No native wrapping helper or hook is installed; prose stays one paragraph in manuscripts. Parent routing/origin/input and monthly portrait windows remain unproven.'}
    (destination / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} guarded native modal cases keep all words, money values and continuation letters intact.')


if __name__ == '__main__':
    main()
