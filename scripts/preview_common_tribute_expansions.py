"""Diagnostic shared-window previews of complete native tribute substitutions."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.codec import tokens_to_markup
from dk4tool.dialogue.layout import token_width, wrap_tokens
from dk4tool.dialogue.model import DialogueToken
from dk4tool.dialogue.preview import render_dialogue_preview, visible_lines
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_printf import execute


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    profile = get_dialogue_profile('shared')
    records = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))['records']
    destination = Path('work/qa/common_tribute_expanded')
    destination.mkdir(parents=True, exist_ok=True)
    rows, panels = [], []
    for record in records:
        text = record['english'].removesuffix('{PAD}')
        names = (None,) if record['message_id'] != 83 else (b'A', b'ABCDEFGHIJKLMNOPQR', 'あ'.encode('cp932') * 9)
        amounts = (1, 9, 10, 99, 100, 999999, 42949672) if record['message_id'] != 83 else (1, 9, 10, 884629)
        for name in names:
            for amount in amounts:
                result = execute(source, text, amount, name)
                expanded = result['expanded_text']
                # Arguments are already-produced runtime bytes, not authored macro
                # commands. Treat them as literal text without reinterpreting F/I.
                tokens = wrap_tokens([DialogueToken('text', expanded, expanded.encode('cp932'))], profile)
                lines = visible_lines(tokens)
                if ''.join(lines).replace(' ', '') != expanded.replace(' ', ''):
                    raise ValueError('Diagnostic wrapping drops expanded glyphs')
                widths = [0]
                for token in tokens:
                    if token.kind == 'line_break':
                        widths.append(profile.glyph_width(' '))
                    else:
                        widths[-1] += token_width(token, profile)
                if len(lines) > profile.max_lines or max(widths) > profile.window_width_px:
                    raise ValueError('Expanded text exceeds shared diagnostic window')
                key = f"{record['message_id']}_{amount}_{0 if name is None else len(name)}_{'sjis' if name and name[0] >= 128 else 'ascii'}"
                path = destination / f'{key}.png'
                render_dialogue_preview(tokens_to_markup(tokens), profile, path, arm9=source, kanji_font=font)
                rows.append({'message_id': record['message_id'], **result,
                             'lines': lines, 'widths_px': widths, 'preview': str(path),
                             'short_final_line': len(lines) > 1 and len(lines[-1]) <= 8})
                if amount == amounts[-1]:
                    panels.append((key, path))
    sheet = Image.new('RGB', (1400, 340 * ((len(panels) + 1) // 2)), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, (label, path) in enumerate(panels):
        x, y = (index % 2) * 700, (index // 2) * 340
        draw.text((x + 8, y + 8), label, fill='black')
        with Image.open(path) as panel:
            sheet.paste(panel, (x, y + 30))
    sheet.save(destination / 'boundary_sheet.png')
    report = {'status': 'diagnostic-model-fit-native-substitutions-pass', 'cases': rows,
              'short_final_line_cases': sum(row['short_final_line'] for row in rows),
              'limitations': 'Profile word wrapping and native glyph previews; does not execute COMMON window rendering, pair batching or physical composition. Formatting gates remain unapproved.'}
    (destination / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rows)} complete expanded previews fit the shared diagnostic model; {report["short_final_line_cases"]} short final lines remain for review.')


if __name__ == '__main__':
    main()
