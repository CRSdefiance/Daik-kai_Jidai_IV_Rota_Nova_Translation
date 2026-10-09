"""Format and preview complete race-help pages using the traced native context."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.dialogue.grand_race_help import format_page
from dk4tool.rom.nds import NdsImage


def main():
    manuscript_path = Path('translations/grand_race_rules_manuscript_v2.json')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    arm9 = NdsImage.open('out/all_routes_combined_v133_candidate.nds').read_file('/__arm9__.bin')
    proof = json.loads(Path('work/analysis/grand_race_help_consumer_proof.json').read_text())
    if proof['candidate_arm9_sha256'] != hashlib.sha256(arm9).hexdigest():
        raise ValueError('Consumer proof does not describe current candidate')
    if (proof['font_metrics']['ascii_width'], proof['font_metrics']['line_height'],
        proof['widget_bounds']['width'], proof['widget_bounds']['height']) != (6, 12, 252, 108):
        raise ValueError('Mapped font or widget dimensions differ from formatter')
    font = GameAsciiFont.from_arm9(arm9)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native ASCII font changed')
    out = Path('work/qa/grand_race_help')
    out.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1040, 1400), 'white')
    sheet_draw = ImageDraw.Draw(sheet)
    rows = []
    for index, row in enumerate(manuscript['records']):
        markup, raw, lines, draws = format_page(row['english'])
        panel = Image.new('RGB', (252, 108), '#eff1f4')
        for char, x, y in draws:
            panel.paste('#15273d', (x, y), font.decode(char))
        title = row['draft_english_title']
        for n, char in enumerate(title):
            panel.paste('#794524', (n * 6, 0), font.decode(char))
        panel.resize((504, 216), Image.Resampling.NEAREST).save(out / f"{row['id']}.png")
        x, y = index % 2 * 520, index // 2 * 280
        sheet_draw.text((x + 4, y + 4), title, fill='black')
        sheet.paste(panel.resize((504, 216), Image.Resampling.NEAREST), (x + 4, y + 24))
        rows.append({'id': row['id'], 'english': row['english'], 'formatted_markup': markup,
                     'encoded_hex': raw.hex().upper(), 'bytes_including_nul': len(raw) + 1,
                     'visible_lines': lines, 'line_count': len(lines),
                     'widths_px': [len(line) * 6 for line in lines],
                     'first_last_characters_and_all_native_pair_positions_exact': True})
    sheet.save(out / 'sheet.png')
    report = {'status': 'formatted-research-awaiting-preview-review-and-integration',
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'consumer_proof_sha256': hashlib.sha256(Path('work/analysis/grand_race_help_consumer_proof.json').read_bytes()).hexdigest(),
              'width': 252, 'height': 108, 'ascii_advance': 6, 'line_height': 12,
              'body_y': 12, 'max_body_lines': 8, 'entries': rows,
              'limitations': ['Exact-font panels and the native pair model are not gameplay screenshots.',
                              'Draft titles are shown for review but not inserted.',
                              'Integrated allocation and live page/navigation behavior still require verification.',
                              'No ROM/profile created and manuscript formatting gates remain pending.']}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'formatted_pages': len(rows), 'maximum_lines': max(r['line_count'] for r in rows),
                      'complete_prose_and_pair_positions_exact': True}))


if __name__ == '__main__':
    main()
