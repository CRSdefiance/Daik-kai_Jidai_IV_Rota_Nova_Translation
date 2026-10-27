"""Preview protected names after actual COMMON display preparation."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.codec import tokens_to_markup
from dk4tool.dialogue.layout import token_width, wrap_tokens
from dk4tool.dialogue.model import DialogueToken
from dk4tool.dialogue.preview import render_dialogue_preview, visible_lines
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def main():
    proof_path = Path('work/analysis/common_display_name_escape_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    if sha(source) != proof['arm9_sha256']:
        raise ValueError('Display preparation proof belongs to another ARM9')
    destination = Path('work/qa/common_display_names')
    destination.mkdir(parents=True, exist_ok=True)
    profile, rows = get_dialogue_profile('shared'), []
    sheet = Image.new('RGB', (1400, 340 * ((len(proof['cases']) + 1) // 2)), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, case in enumerate(proof['cases']):
        expanded = case['native_preprocessing']['expanded']
        tokens = wrap_tokens([DialogueToken('text', expanded, expanded.encode('cp932'))], profile)
        lines, widths = visible_lines(tokens), [0]
        for token in tokens:
            if token.kind == 'line_break':
                widths.append(profile.glyph_width(' '))
            else:
                widths[-1] += token_width(token, profile)
        if (len(lines) > profile.max_lines or max(widths) > profile.window_width_px
                or ''.join(lines).replace(' ', '') != expanded.replace(' ', '')):
            raise ValueError('Protected name loses glyphs or exceeds diagnostic geometry')
        path = destination / f'name_{index:02d}.png'
        render_dialogue_preview(tokens_to_markup(tokens), profile, path, arm9=source, kanji_font=font)
        x, y = (index % 2) * 700, (index // 2) * 340
        draw.text((x + 8, y + 8), case['stored_name_hex'], fill='black')
        with Image.open(path) as panel:
            sheet.paste(panel, (x, y + 30))
        rows.append({'stored_name_hex': case['stored_name_hex'], 'lines': lines,
                     'widths_px': widths, 'preview': str(path), 'sha256': sha(path.read_bytes())})
    sheet.save(destination / 'boundary_sheet.png')
    report = {'status': 'pass-diagnostic-protected-name-fit', 'cases': rows,
              'source_proof_sha256': sha(proof_path.read_bytes()),
              'limitations': 'Actual preparation output, modeled shared wrapping and exact native font assets. Progressive window execution and physical placement remain unproven.'}
    (destination / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rows)} protected-name previews fit; maximum {max(len(row["lines"]) for row in rows)} rows.')


if __name__ == '__main__':
    main()
