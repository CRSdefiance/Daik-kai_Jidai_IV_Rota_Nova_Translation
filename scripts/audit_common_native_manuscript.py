"""Render source-locked native paragraphs without assuming record coordinates."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageDraw

from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.manuscript.read_text(encoding='utf-8'))
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                    clean.read_file('/__arm9__.bin'))
    base = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    arm9, font = base.read_file('/__arm9__.bin'), base.read_file('/GRP/KANJI.FNT')
    rows = []
    ids = set()
    for row in payload['records']:
        i = row['message_id']
        if i in ids or bytes.fromhex(row['source_hex']) != source[i].text:
            raise ValueError('Duplicate ID or changed clean source')
        ids.add(i)
        text = row['english'].removesuffix('{PAD}')
        if re.findall(r'%[sdi]', text) != re.findall(r'%[sdi]', source[i].text.decode('cp932')):
            raise ValueError('Source argument shape differs')
        audit = audit_native_common_entry(b' ' * len(text.encode('cp932')), row['english'])
        preview = args.out / 'previews' / f'{i}.png'
        render_dialogue_preview(audit['formatted_markup'], get_dialogue_profile('shared'),
                                preview, arm9=arm9, kanji_font=font)
        rows.append({'message_id': i, 'source': source[i].text.decode('cp932'),
                     'english': text, 'preview': preview.as_posix(), **audit})
    blockers = sum(v['severity'] in {'warning', 'error'} for row in rows for v in row['issues'])
    args.out.mkdir(parents=True, exist_ok=True)
    report = {'manuscript': args.manuscript.as_posix(), 'blockers': blockers, 'entries': rows,
              'limitation': 'Literal printf previews do not prove actual runtime substitution widths.'}
    (args.out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                         encoding='utf-8')
    for start in range(0, len(rows), 8):
        sheet = Image.new('RGB', (576, 880), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for j, row in enumerate(rows[start:start + 8]):
            with Image.open(row['preview']) as raw:
                preview = raw.convert('RGB')
            preview.thumbnail((280, 196))
            x, y = (j % 2) * 288, (j // 2) * 220
            draw.text((x + 4, y + 2), str(row['message_id']), fill='black')
            sheet.paste(preview, (x + 4, y + 20))
        sheet.save(args.out / f'sheet_{start // 8}.png')
    print(f'{len(rows)} exact-font previews; {blockers} blockers; {args.out}')
    if blockers:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
