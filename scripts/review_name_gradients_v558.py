"""Restore each original name plaque's own horizontal gradient; research only."""
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/name_gradients_v558')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open('out/all_routes_combined_v557_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    batch = json.loads(Path('translations/name_entry_plaques_graphics_v1.json').read_text(encoding='utf-8'))
    path = batch['file_path']
    original = PxlImage.from_bytes(clean.read_file(path))
    old = PxlImage.from_bytes(current.read_file(path))
    result = PxlImage.from_bytes(original.source)
    assert old.palette == original.palette
    font = GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    records = []
    ink = set()
    for row in batch['records']:
        l, t, r, b = row['box']
        gradients, restored, concealed = [], 0, 0
        for y in range(t + 1, t + 10):
            counts = Counter(original.indices[y * 44 + x] for x in range(4, 40)
                             if original.indices[y * 44 + x] != 15)
            ranking = counts.most_common()
            assert len(ranking) == 1 or ranking[0][1] > ranking[1][1]
            mode = ranking[0][0]
            gradients.append({'row': y, 'index': mode, 'source_votes': ranking[0][1],
                              'candidate_nonwhite_samples': sum(counts.values())})
            for x in range(4, 40):
                pos = y * 44 + x
                if original.indices[pos] == 15:
                    result.indices[pos] = mode
                    concealed += 1
        dl, dt, dr, _ = row['draw_box']
        tx = dl + (dr - dl - len(row['text']) * 5) // 2
        expected = set()
        for n, ch in enumerate(row['text']):
            glyph = font.decode(ch)
            assert not glyph.crop((0, 0, 6, 2)).getbbox()
            for y in range(2, 11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        pos = (dt + y - 2) * 44 + tx + n * 5 + x
                        result.indices[pos] = 15
                        expected.add(pos)
        ink.update(expected)
        source_preserved = 0
        for y in range(t, b):
            for x in range(l, r):
                pos = y * 44 + x
                if pos not in expected and original.indices[pos] != 15:
                    assert result.indices[pos] == original.indices[pos]
                    source_preserved += 1
                    restored += old.indices[pos] != original.indices[pos]
        records.append({'id': row['id'], 'english': row['text'], 'source_Japanese': row['source_japanese'],
                        'box': row['box'], 'draw_box': row['draw_box'], 'row_gradients': gradients,
                        'complete_English_ink_pixels': len(expected), 'source_material_pixels_preserved': source_preserved,
                        'source_material_pixels_restored': restored, 'concealed_Japanese_white_pixels_reconstructed': concealed,
                        'fully_completed': False})
    assert {n for n, v in enumerate(result.indices) if v == 15} == {n for n, v in enumerate(old.indices) if v == 15}
    assert all(result.indices[n] == old.indices[n] for n in ink)
    output = result.to_bytes()
    assert output[:result.pixels_offset] == old.source[:old.pixels_offset]
    (ROOT / 'name_RESEARCH_ONLY.pxl').write_bytes(output)
    sheet = Image.new('RGB', (570, 340), (40, 45, 50))
    draw = ImageDraw.Draw(sheet)
    for col, (atlas, label) in enumerate(zip((original, old, result), ('Original Japanese', 'Current V557', 'Own source gradients'), strict=True)):
        draw.text((col * 190 + 5, 5), label, fill='white')
        sheet.paste(atlas.render().convert('RGB').resize((176, 240), Image.Resampling.NEAREST), (col * 190 + 5, 30))
    sheet.save(ROOT / 'name_gradient_review.png')
    proof = {'file_path': path, 'source_sha256': sha(old.source), 'clean_sha256': sha(original.source),
             'target_sha256': sha(output), 'records': records,
             'all5_full_English_masks_and_positions_retained': True,
             'all_original_nonwhite_material_outside_English_ink_exact': True,
             'all_unchanged_original_frame_pixels_retained': True,
             'header_palette_dimensions_retained': True, 'production_ROM_changed': False,
             'embedded_sync_and_native_review_pending': True, 'full_goal_complete': False}
    (ROOT / 'prototype_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All5 original gradients restored; complete English masks/positions and source frames retained.')


if __name__ == '__main__':
    main()
