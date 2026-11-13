"""Decode source/current raw comic frames for a complete, source-labelled review."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.rom.nds import NdsImage


def main():
    out = Path('work/analysis/comic_current_v506')
    out.mkdir(parents=True, exist_ok=True)
    candidate = Path('out/all_routes_combined_v502_candidate.nds')
    source = Path('out/raphael_natural_v2_accepted_base.nds')
    blocks = [IlnkContainer.parse(NdsImage.open(p).read_file('/GRP/SLACKIMG.DK4')).blocks[19]
              for p in (source, candidate)]
    frame_bytes = 320 * 240 * 2
    assert all(len(block) == 21 * frame_bytes for block in blocks)
    batch = json.loads(Path('translations/gallery_chase_fringe_raw_art_v8.json').read_text(encoding='utf-8'))
    rows = []
    for first in range(0, 21, 4):
        sheet = Image.new('RGB', (640, min(4, 21-first) * 260), '#dddddd')
        draw = ImageDraw.Draw(sheet)
        for index in range(first, min(first+4, 21)):
            row = {'frame': index, 'current_batch_captions': [
                {'id': r['id'], 'source': r['source_text'], 'english': r['english'], 'box': r['box']}
                for r in batch['records'] if r['image_index'] == index]}
            for col, block in enumerate(blocks):
                raw = block[index*frame_bytes:(index+1)*frame_bytes]
                rgb = bytes(channel for word in struct.unpack('<76800H', raw)
                            for channel in bgr555(word)[:3])
                image = Image.frombytes('RGB', (320,240), rgb)
                # Direct source-byte decode; no resize, smoothing or artwork edits.
                sheet.paste(image, (col*320, (index-first)*260+20))
                draw.text((col*320+3, (index-first)*260+3),
                          f'Frame {index}: ' + ('accepted source' if col == 0 else 'current V502'), fill='black')
                row['source_sha256' if col == 0 else 'current_sha256'] = hashlib.sha256(raw).hexdigest()
            before = blocks[0][index*frame_bytes:(index+1)*frame_bytes]
            after = blocks[1][index*frame_bytes:(index+1)*frame_bytes]
            boxes = [r['box'] for r in row['current_batch_captions']]
            unowned_changes = []
            high_bit_changes = 0
            changed_words = 0
            for pos, (old, new) in enumerate(zip(struct.unpack('<76800H', before), struct.unpack('<76800H', after))):
                if old != new:
                    changed_words += 1
                    x, y = pos % 320, pos // 320
                    if not any(x0 <= x < x1 and y0 <= y < y1 for x0,y0,x1,y1 in boxes):
                        unowned_changes.append([x,y])
                high_bit_changes += bool((old ^ new) & 0x8000)
            assert not unowned_changes and high_bit_changes == 0
            row['changed_source_words'] = changed_words
            row['all_unowned_source_words_exact'] = True
            row['all_source_high_bits_exact'] = True
            row['untouched_frame_byte_exact'] = before == after if not boxes else None
            rows.append(row)
        sheet.save(out / f'source_current_frames_{first:02d}_{min(first+3,20):02d}.png')
    proof = {
        'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'source_block_sha256': hashlib.sha256(blocks[0]).hexdigest(),
        'frames': rows,
        'storage_interpretation': '21 x 320 x 240 BGR555',
        'decoded_source_previews_not_native_display_evidence': True,
        'production_ROM_unchanged': True,
        'all21_frames_unowned_source_words_and_high_bits_exact': True,
    }
    (out / 'all_frames_manifest.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Decoded all 21 source/current frames in six labelled sheets.')


if __name__ == '__main__':
    main()
