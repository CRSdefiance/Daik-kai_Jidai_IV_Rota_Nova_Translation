"""Portable source/current recognition packet; no fabricated gameplay scenes."""

import html
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode
from scripts.inventory_graphics_v150 import pxl_render
from scripts.run_small_controls_v701 import CASES
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/display_context_packet_v739')
PACKET = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V739 Display context lookup')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
CARDS = (168, 169, 170, 171, 206, 207, 208, 209)


def palette_preview(raw, bank):
    image = PxlImage.from_bytes(raw)
    size = 32 if image.bits_per_pixel == 4 else 512
    offset = struct.unpack_from('<I', raw, 12)[0] + size * bank
    assert offset + size <= image.pixels_offset
    colors = [bgr555(v)[:3] for v, in struct.iter_unpack('<H', raw[offset:offset + size])]
    picture = Image.new('RGB', (image.width, image.height))
    picture.putdata([colors[i] for i in image.indices])
    return picture


def save_picture(image, name):
    path = PACKET / 'images' / name
    image = image.convert('RGB')
    image.save(path)
    observed = Image.open(path).convert('RGB')
    assert observed.size == image.size and observed.tobytes() == image.tobytes()
    return {'path': str(path.relative_to(PACKET)).replace('\\', '/'),
            'PNG_sha256': sha(path.read_bytes()), 'RGB_sha256': sha(image.tobytes()),
            'dimensions': list(image.size)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists() and not (PACKET / 'index.html').exists()
    (PACKET / 'images').mkdir(parents=True, exist_ok=True)
    pre = read('work/analysis/village_request_sweep_v735/preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    entries = []

    def add(identifier, family, label, original, english, provenance, limit):
        entries.append({'id': identifier, 'family': family, 'label': label,
                        'original': save_picture(original, identifier + '_source.png'),
                        'English': save_picture(english, identifier + '_English.png'),
                        'source': provenance, 'interpretation_limit': limit,
                        'original_display_context_verified': False})

    blocks = [IlnkContainer.parse(r.read_file('/GRP/SLACKIMG.DK4')).blocks[19] for r in (clean, current)]
    assert all(len(b) == 21 * 153600 for b in blocks)
    for frame in range(21):
        images = []
        for block in blocks:
            raw = block[frame * 153600:(frame + 1) * 153600]
            rgb = bytes(c for word, in struct.iter_unpack('<H', raw) for c in bgr555(word)[:3])
            images.append(Image.frombytes('RGB', (320, 240), rgb))
        add(f'comic_{frame:02d}', 'comics', f'Comic/sketch frame {frame:02d}', *images,
            {'file': '/GRP/SLACKIMG.DK4', 'block': 19, 'frame': frame,
             'source_frame_sha256': sha(blocks[0][frame * 153600:(frame + 1) * 153600]),
             'current_frame_sha256': sha(blocks[1][frame * 153600:(frame + 1) * 153600])},
            'Stored BGR555 RGB decode,320x240. Alpha/import/viewer/readability in the original game are unverified.')
    for key, case in CASES.items():
        if key == 'baseline':
            continue
        path = case['path']
        x, y, width, height = case['rect']
        images = [palette_preview(r.read_file(path), case['bank']).crop((x, y, x + width, y + height))
                  for r in (clean, current)]
        add('control_' + key, 'controls', case['label'], *images,
            {'file': path, 'box': [x, y, x + width, y + height], 'preview_palette_bank': case['bank'],
             'source_whole_file_sha256': sha(clean.read_file(path)),
             'current_whole_file_sha256': sha(current.read_file(path))},
            'Stored-palette RGB crop. The bank is a documented diagnostic choice,not proof of the intended normal-screen palette or transparency.')
    for index in CARDS:
        path = f'/evstill/evstill{index:03d}.pxl'
        images = [pxl_render(r.read_file(path))[0].convert('RGB') for r in (clean, current)]
        add(f'village_{index}', 'cards', f'Village caption card {index}', *images,
            {'file': path, 'source_whole_file_sha256': sha(clean.read_file(path)),
             'current_whole_file_sha256': sha(current.read_file(path))},
            'Whole stored image. Original event-parent fixtures passed; ordinary trigger remains unidentified.')
    legacy = (
        ('/_pxl/logo.pxl', 'Standalone Rota Nova logo'),
        ('/_pxl/startmenu0.pxl', 'Porto Estado ocean title'),
        ('/_pxl/winframe00.pxl', 'Porto Estado sky title'),
        ('/_pxl/seamap.pxl', 'Separate sepia-map atlas'),
        ('/_pxl/copyright.pxl', 'Standalone copyright strip'),
        ('/_pxl/ship_eurL.pxl', 'Standalone European ship texture'),
        ('/_pxl/slackimg12.pxl', 'Separate name-entry labels'),
        ('/_pxl/slackimg20.pxl', 'Separate Press a button prompt'),
    )
    for path, label in legacy:
        images = [pxl_render(r.read_file(path))[0].convert('RGB') for r in (clean, current)]
        add('legacy_' + Path(path).stem, 'legacy', label, *images,
            {'file': path, 'preview_palette_bank': 0,
             'source_whole_file_sha256': sha(clean.read_file(path)),
             'current_whole_file_sha256': sha(current.read_file(path))},
            'Whole stored decode,bank0 where paletted. Separate native fixture evidence exists; original ordinary parent is unverified. Map/texture interpretation is not native geometry.')
    for index, block in enumerate(IlnkContainer.parse(clean.read_file('/GRP/WINFRAME.DK4')).blocks):
        before = decode(block)
        if before is None:
            continue
        now = IlnkContainer.parse(current.read_file('/GRP/WINFRAME.DK4')).blocks[index]
        after = decode(now)
        assert after is not None
        images = []
        for info in (before, after):
            size = 32 if info['depth'] == 4 else 512
            palette = [bgr555(word)[:3] for word, in struct.iter_unpack('<H', info['palette'][:size])]
            image = Image.new('RGB', (info['width'], info['height']))
            image.putdata([palette[i] for i in info['indices']])
            images.append(image)
        label = ('Embedded Porto Estado title', 'Porto Estado book cover', 'Book left-page backdrop',
                 'Book right-page backdrop', 'Embedded Koei publisher logo', 'Hoist the sails! banner')[index]
        add(f'legacy_WINFRAME_block{index}', 'legacy', f'{label} / block {index}', *images,
            {'file': '/GRP/WINFRAME.DK4', 'block': index, 'preview_palette_bank': 0,
             'source_block_sha256': sha(block), 'current_block_sha256': sha(now)},
            'Decoded embedded storage,not an original DS screenshot or demonstrated viewport.')
    assert len([r for r in entries if r['family'] == 'comics']) == 21
    assert len([r for r in entries if r['family'] == 'controls']) == 6
    assert len([r for r in entries if r['family'] == 'cards']) == 8
    assert len([r for r in entries if r['family'] == 'legacy']) == 14
    # Recognition overviews preserve complete images; full-size files remain
    # linked alongside them. Thumbnails cannot establish small-text readability.
    overview = Image.new('RGB', (960, 1152), '#263238')
    draw = ImageDraw.Draw(overview)
    draw.text((12, 8), 'Original stored comic/sketch art / recognition only / NOT emulator screenshots', fill='white')
    for n in range(21):
        x, y = n % 4 * 240, 36 + n // 4 * 186
        row = next(r for r in entries if r['id'] == f'comic_{n:02d}')
        image = Image.open(PACKET / row['original']['path']).convert('RGB')
        draw.text((x + 6, y), f'Frame {n:02d} / source 320x240', fill='white')
        overview.paste(image.resize((224, 168), Image.Resampling.NEAREST), (x + 8, y + 16))
    overview.save(PACKET / 'comic_recognition_overview.png')
    controls = Image.new('RGB', (848, 1200), '#263238')
    draw = ImageDraw.Draw(controls)
    draw.text((12, 10), 'Stored control crops / source left,English right / normal display contexts unknown', fill='white')
    for n, row in enumerate(r for r in entries if r['family'] == 'controls'):
        y = 42 + n * 190
        draw.text((12, y), row['label'] + ' / stored-palette preview', fill='white')
        for column, field in enumerate(('original', 'English')):
            image = Image.open(PACKET / row[field]['path']).convert('RGB')
            controls.paste(image.resize((image.width * 8, image.height * 8), Image.Resampling.NEAREST),
                           (12 + column * 424, y + 22))
    controls.save(PACKET / 'control_recognition_comparison.png')
    sections = []
    names = {'comics': 'Comic/sketch artwork', 'controls': 'Six controls',
             'cards': 'Eight village cards', 'legacy': 'Other legacy/standalone examples'}
    for family, title in names.items():
        cards = []
        for row in (r for r in entries if r['family'] == family):
            figures = ''.join(f'<figure><a href="{row[field]["path"]}"><img src="{row[field]["path"]}" '
                              f'alt="{html.escape(row["label"])} {field}" '
                              f'style="width:{row[field]["dimensions"][0] * (8 if family == "controls" else 1)}px"></a><figcaption>{field}: '
                              f'{row[field]["dimensions"][0]}x{row[field]["dimensions"][1]}</figcaption></figure>'
                              for field in ('original', 'English'))
            cards.append(f'<article id="{row["id"]}"><h3>{html.escape(row["label"])}</h3>'
                         f'<p>{html.escape(row["source"]["file"])}</p><div class="pair">{figures}</div>'
                         f'<p>{html.escape(row["interpretation_limit"])}</p></article>')
        sections.append(f'<section id="{family}"><h2>{title}</h2>{"".join(cards)}</section>')
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Rota Nova: display context lookup</title>'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><style>'
            'body{background:#1e282e;color:#eef2f5;font:16px system-ui;max-width:1100px;margin:32px auto;padding:0 20px}'
            'a{color:#7ed9e5}article{background:#2b383f;border:1px solid #50616a;border-radius:8px;padding:20px;margin:20px 0}'
            '.pair{display:flex;gap:24px;flex-wrap:wrap}figure{margin:0;max-width:48%}'
            'img{image-rendering:pixelated;max-width:100%;height:auto}'
            'figcaption{color:#bac8ce}p{line-height:1.55}nav{display:flex;gap:24px;flex-wrap:wrap}</style>'
            '<h1>Which original screens show these graphics?</h1>'
            '<p>These are exact stored-resource RGB decodes, not emulator screenshots. English artwork is already '
            'implemented and source-reviewed. The missing evidence is the original DS menu, event or viewer that '
            'uses each resource. A menu path, screenshot or save can supply a useful lead.</p>'
            '<p>This packet does not approve artwork, remove requirements, prove resources unused, or mark the '
            'graphics goal complete. Click any image for its complete stored dimensions. Thumbnails do not '
            'establish native readability. The four excluded low-resolution Online bodies are not reopened.</p><nav>'
            + ''.join(f'<a href="#{key}">{value}</a>' for key, value in names.items()) + '</nav>'
            + ''.join(sections) + '</html>')
    (PACKET / 'index.html').write_text(page, encoding='utf-8')
    manifest = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
                'source': 'work/clean.nds', 'source_sha256': sha(Path('work/clean.nds').read_bytes()),
                'entries': entries, 'full49_source_current_cases_98_RGB_decodes': True,
                'no_native_scene_readability_opacity_availability_or_user_acceptance_claim': True,
                'publication_approved': False, 'full_goal_complete': False}
    save(PACKET / 'manifest.json', manifest)
    files = {str(p.relative_to(PACKET)).replace('\\', '/'): sha(p.read_bytes())
             for p in PACKET.rglob('*') if p.is_file()}
    save(ROOT / 'proof.json', {'packet': str(PACKET), 'all_packet_file_hashes': files,
                              'entries': len(entries), 'decoded_images': len(entries) * 2,
                              'producer_sha256': sha(Path(__file__).read_bytes()),
                              'previous_goal_turn_classification': 'progress: V738 source-bound indexed lead resolved',
                              'release_hashes_unchanged': pre['release_hashes'],
                              'native_graphics_contexts_and_user_response_still_pending': True,
                              'full_goal_complete': False})
    print('V739 context packet:49 source/current cases,98 full RGB decodes,portable index and2 recognition sheets on E.', flush=True)


if __name__ == '__main__':
    main()
