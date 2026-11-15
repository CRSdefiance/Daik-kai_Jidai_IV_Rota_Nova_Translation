"""Research-only full ship plaque restoration, including overlapping erase regions."""
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.source_plaque_bevels import source_point
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/plaque_families_v556')
ROM = Path('out/all_routes_combined_v555_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    batch = json.loads(Path('translations/ships_submenu_graphics_v2.json').read_text(encoding='utf-8'))
    path = batch['file_path']
    old, original = [PxlImage.from_bytes(r.read_file(path)) for r in (current, clean)]
    result = PxlImage.from_bytes(old.source)
    donor = PxlImage.from_bytes(clean.read_file('/_pxl/towninfo.pxl'))
    font = GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    mapping = {rgb: min((n for n in range(len(old.palette)) if n != 1),
                       key=lambda n: sum((old.palette[n][k] - rgb[k]) ** 2 for k in range(3)))
               for rgb in donor.palette}
    columns = list(range(2, 43)) + list(range(85, 124))
    allowed = set()
    rows = []
    # Restore outside plaque faces from the original atlas. Old erase rectangles
    # overlap neighbouring plaques; finish all faces after every erase pass.
    for row in batch['records']:
        l, t, r, b = row['box']
        for y in range(t, b):
            for x in range(l, r):
                at = y * old.width + x
                result.indices[at] = original.indices[at]
                allowed.add(at)
    for row in batch['records']:
        l, top, r, _ = row['box']
        t, b = top + 7, top + 23
        width, height = r - l, b - t
        assert 4 < width <= 84 and height == 16
        for y in range(height):
            for x in range(width):
                if 2 <= x < width - 2 and 2 <= y < height - 2:
                    sx, sy = columns[x - 2], 62 + y - 2
                else:
                    sx, sy = source_point(x, y, width, height)
                rgb = donor.palette[donor.indices[sy * donor.width + sx]]
                result.indices[(t + y) * old.width + l + x] = mapping[rgb]
        dl, dt, dr, db = row.get('draw_box', row['box'])
        # Retain every prior accepted glyph position and term.
        tx, ty = dl + (dr - dl - len(row['text']) * 5) // 2, dt + (db - dt - 11) // 2
        expected = set()
        for n, ch in enumerate(row['text']):
            glyph = font.decode(ch)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        xx, yy = tx + n * 5 + x, ty + y
                        assert l <= xx < r and t <= yy < b
                        result.indices[yy * old.width + xx] = 1
                        expected.add((xx, yy))
        rows.append({'id': row['id'], 'english': row['text'], 'box': row['box'],
                     'draw_box': row.get('draw_box', row['box']), 'plaque_box': [l, t, r, b],
                     'font_band': [ty, ty + 11],
                     'expected_ink': sorted([list(p) for p in expected]),
                     'complete_first_final_and_all_glyph_pixels': len(expected),
                     'fully_completed': False})
    for row in rows:
        l, _, r, _ = row['box']
        t, b = row['font_band']
        points = {(x, y) for y in range(t, b) for x in range(l, r)
                  if result.indices[y * old.width + x] == 1}
        expected = {tuple(p) for p in row['expected_ink']}
        # An erase region can include the bottom edge of the preceding plaque;
        # compare actual glyphs against the inherited texture in that same region.
        prior = {(x, y) for y in range(t, b) for x in range(l, r)
                 if old.indices[y * old.width + x] == 1}
        structural = set()
        if row['english'] == 'Hull':
            # Original panel divider crosses the blank first font row. Verify
            # every owned divider pixel separately; do not call it glyph ink.
            assert t == 143 and not any(y == 143 for _, y in expected)
            assert all(result.indices[143 * old.width + x] == original.indices[143 * old.width + x]
                       for x in range(l, r))
            structural = {(x, 143) for x in range(l, r) if original.indices[143 * old.width + x] == 1}
            row['source_divider_row_verified'] = 143
        assert points == expected | structural and expected == prior, row['english']
    assert all(a == b for n, (a, b) in enumerate(zip(old.indices, result.indices, strict=True))
               if n not in allowed)
    output = result.to_bytes()
    assert output[:result.pixels_offset] == old.source[:old.pixels_offset]
    (ROOT / 'ship_RESEARCH_ONLY.pxl').write_bytes(output)
    sheet = Image.new('RGB', (1050, len(rows) * 95 + 30), (40, 45, 50))
    draw = ImageDraw.Draw(sheet)
    for col, label in enumerate(('Original source', 'Current V555', 'Source grain/frame prototype')):
        draw.text((col * 350 + 5, 5), label, fill='white')
    for n, row in enumerate(rows):
        draw.text((5, 30 + n * 95), row['english'], fill='white')
        for col, atlas in enumerate((original, old, result)):
            crop = atlas.render().crop(row['box']).convert('RGB')
            sheet.paste(crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST),
                        (col * 350 + 5, 47 + n * 95))
    sheet.save(ROOT / 'ship_texture_prototype_review.png')
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'file_path': path, 'source_sha256': sha(old.source), 'clean_sha256': sha(original.source),
             'target_sha256': sha(output), 'records': rows,
             'changed_pixels': sum(a != b for a, b in zip(old.indices, result.indices, strict=True)),
             'all11_prior_English_terms_positions_and_complete_masks_retained': True,
             'header_palette_geometry_and_unowned_pixels_retained': True,
             'overlapping_erase_rectangles_finished_before_all_plaque_faces': True,
             'texture_donor': '/_pxl/towninfo.pxl', 'grain_bounds': [[2, 62, 43, 74], [85, 62, 124, 74]],
             'bevel_donor_bounds': [8, 20, 48, 36], 'concealed_material_is_reconstruction': True,
             'native_crop_and_gameplay_verification_pending': True,
             'production_ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'ship_texture_prototype_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Ship texture research:11 complete English masks retained; original wallpaper outside faces restored; fine source grain and bevels applied.')


if __name__ == '__main__':
    main()
