"""Preview complete BGM names with the locked ASCII font and title geometry."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.patch.bgm_title_tracking import apply_probe, title_geometry
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_native_sound_selector import BASE, BASE_SHA, SELECTOR_CODE_RANGES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--renderer-probe', type=Path)
    args = parser.parse_args()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('Canonical baseline changed')
    base, clean = NdsImage.open(BASE), NdsImage.open('work/clean.nds')
    arm9, clean_arm9 = base.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for lo, hi in SELECTOR_CODE_RANGES:
        if arm9[lo:hi] != clean_arm9[lo:hi]:
            raise ValueError('The title renderer differs from the mapped clean code')
    advance = 6
    if args.renderer_probe:
        probe = args.renderer_probe.read_bytes()
        if probe != apply_probe(arm9):
            raise ValueError('Renderer probe differs from the exact scoped patch')
        arm9, advance = probe, 5
    font = GameAsciiFont.from_arm9(arm9)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('The mapped ASCII font differs')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean_arm9)
    payload = json.loads(args.manuscript.read_text(encoding='utf-8'))
    ids = [row['message_id'] for row in payload['records']]
    if ids != list(range(3251, 3289)):
        raise ValueError('Exactly all 38 BGM native IDs must be supplied in order')
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'previews').mkdir(exist_ok=True)
    rows = []
    for row in payload['records']:
        i = row['message_id']
        if bytes.fromhex(row['source_hex']) != source[i].text:
            raise ValueError(f'Clean native source changed at {i}')
        if row.get('presentation') != 'sound-bgm-title-ascii':
            raise ValueError(f'Unmapped title presentation at {i}')
        english = row['english'].removesuffix('{PAD}')
        geometry = title_geometry(english, advance)
        # Sixteen pixels outside each edge keep overflow visible. The gray
        # rectangle is the mapped 128-pixel panel, not a game screenshot.
        panel = Image.new('RGB', (160, 32), '#e6d9d9')
        draw = ImageDraw.Draw(panel)
        draw.rectangle((16, 0, 143, 31), fill='#eff1f4')
        draw.line((16, 0, 16, 31), fill='#c44a4a')
        draw.line((144, 0, 144, 31), fill='#c44a4a')
        for offset, char in enumerate(english):
            glyph = font.decode(char)
            panel.paste('#15273d', (16 + geometry['left'] + offset * advance, 10), glyph)
        preview = args.out / 'previews' / f'{i}.png'
        panel.resize((480, 96), Image.Resampling.NEAREST).save(preview)
        rows.append({'message_id': i, 'japanese': row['japanese'], 'english': english,
                     **geometry, 'preview': preview.as_posix()})
    for start in range(0, len(rows), 8):
        sheet = Image.new('RGB', (976, 544), '#ffffff')
        draw = ImageDraw.Draw(sheet)
        for j, row in enumerate(rows[start:start + 8]):
            x, y = (j % 2) * 488, (j // 2) * 136
            label = f"{row['message_id']}: {row['english']} ({row['width_pixels']}px)"
            draw.text((x + 4, y + 4), label, fill='black')
            with Image.open(row['preview']) as preview:
                sheet.paste(preview, (x + 4, y + 28))
        sheet.save(args.out / f'sheet_{start // 8}.png')
    owners = {(source[i].block, source[i].record_index) for i in ids}
    missing_neighbors = [e.message_id for e in source
                         if (e.block, e.record_index) in owners and e.message_id not in ids]
    overflow = [row['message_id'] for row in rows if not row['fits_panel']]
    following_heading = None
    if args.renderer_probe:
        heading_offset = struct.unpack_from('<I', arm9, 0x10930C)[0] - 0x02000000
        heading = arm9[heading_offset:].split(b'\0', 1)[0].decode('ascii')
        if heading != 'Vol':
            raise ValueError('The following accepted BGM heading differs')
        panel = Image.new('RGB', (128, 32), '#eff1f4')
        for index, char in enumerate(heading):
            panel.paste('#15273d', (24 + index * advance, 10), font.decode(char))
        panel.resize((384, 96), Image.Resampling.NEAREST).save(args.out / 'volume_heading.png')
        following_heading = {'text': heading, 'native_y': 98, 'left': 24,
                             'right': 24 + len(heading) * advance,
                             'preview': (args.out / 'volume_heading.png').as_posix()}
    report = {
        'status': 'draft-title-preview-with-integration-blockers',
        'manuscript_sha256': hashlib.sha256(args.manuscript.read_bytes()).hexdigest(),
        'source_locked_titles': 38,
        'ascii_font_sha256': hashlib.sha256(font.glyphs).hexdigest(),
        'renderer_code_matches_clean': args.renderer_probe is None,
        'exact_scoped_renderer_probe_verified': args.renderer_probe is not None,
        'panel_width': 128, 'ascii_advance': advance, 'title_center': 64,
        'overflow_ids': overflow, 'missing_packed_owner_neighbors': missing_neighbors,
        'entries': rows,
        'following_heading': following_heading,
        'limitations': ['Diagnostic panels are not gameplay screenshots.',
                        'Complete-owner integration and wider-title rendering are pending.',
                        'No live selection or playback has been verified.'],
    }
    (args.out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                        encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('source_locked_titles', 'overflow_ids',
                                           'missing_packed_owner_neighbors')}))


if __name__ == '__main__':
    main()
