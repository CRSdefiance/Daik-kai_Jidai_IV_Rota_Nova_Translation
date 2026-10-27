"""Research correct price-caption ownership and restore an overwritten illustration."""
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/marker_materials_v568')
FILE = '/_pxl/__marker.pxl'
CELLS = ((48, '売り値', 'Sell'), (60, '買い値', 'Buy'))


def repair(original, current, arm):
    result = PxlImage.from_bytes(current.source)
    # All three historical price/action boxes are restored before localizing
    # the two genuine source captions. The lower box contains artwork, not Sell.
    owned = {y*256+x for y in range(48, 96) for x in range(112, 145)}
    for n in owned:
        result.indices[n] = original.indices[n]
    masks = []
    for top, _, _ in CELLS:
        white = {(x, y) for y in range(12) for x in range(32)
                 if original.indices[(top+y)*256+112+x] == 15}
        shadow = {(x+1, y+1) for x, y in white if x < 31 and y < 11
                  and original.indices[(top+y+1)*256+113+x] <= 3}
        masks.append(white | shadow)
    rows = []
    for cell, (top, jp, text) in enumerate(CELLS):
        hidden = masks[cell]
        inferred, other_row_donors = 0, 0
        for x, y in sorted(hidden, key=lambda p: (p[1], p[0])):
            context = {(dx, dy) for dy in range(-5, 6) for dx in range(-5, 6)
                       if 0 <= x+dx < 32 and 0 <= y+dy < 12 and (x+dx, y+dy) not in hidden}
            options = []
            for other, (other_top, _, _) in enumerate(CELLS):
                for donor_y in range(12):
                    for donor_x in range(1, 31):
                        if (donor_x, donor_y) in masks[other]:
                            continue
                        if original.indices[(other_top+donor_y)*256+112+donor_x] <= 3:
                            continue
                        pairs = [(original.indices[(top+y+dy)*256+112+x+dx],
                                  original.indices[(other_top+donor_y+dy)*256+112+donor_x+dx])
                                 for dx, dy in context if 0 <= donor_x+dx < 32 and 0 <= donor_y+dy < 12
                                 and (donor_x+dx, donor_y+dy) not in masks[other]]
                        if not pairs:
                            continue
                        distance = sum(sum(abs(a-b) for a, b in zip(original.palette[p][:3],
                                                                    original.palette[q][:3], strict=True)) for p, q in pairs)
                        options.append((distance/len(pairs), -len(pairs), abs(donor_y-y)*2+abs(donor_x-x),
                                        other, donor_x, donor_y))
            if not options:
                raise ValueError(f'No reviewed unlettered price-row donor at {cell,x,y}')
            _, _, _, other, donor_x, donor_y = min(options)
            donor_top = CELLS[other][0]
            result.indices[(top+y)*256+112+x] = original.indices[(donor_top+donor_y)*256+112+donor_x]
            inferred += 1
            other_row_donors += donor_y != y
        font = GameAsciiFont.from_arm9(arm)
        left, text_top = 112+(32-len(text)*5)//2, top+1
        ink = set()
        for n, ch in enumerate(text):
            glyph = font.decode(ch)
            for gy in range(2, 11):
                for gx in range(5):
                    if glyph.getpixel((gx, gy)):
                        point = (left+n*5+gx, text_top+gy-2)
                        ink.add(point)
                        result.indices[point[1]*256+point[0]] = 15
        actual = {(x, y) for y in range(top, top+12) for x in range(112, 144)
                  if result.indices[y*256+x] == 15}
        assert actual == ink
        preserved = sum(result.indices[(top+y)*256+112+x] == original.indices[(top+y)*256+112+x]
                        for y in range(12) for x in range(32)
                        if (x, y) not in hidden and (112+x, top+y) not in ink)
        rows.append({'Japanese': jp, 'English': text, 'actual_source_cell': [112, top, 144, top+12],
                     'complete_English_ink': len(ink), 'source_stroke_shadow_reconstructed_points': inferred,
                     'visible_original_material_points_exact': preserved,
                     'donors': 'Unlettered original pixels from these two source price cells; 2D visible-context color matching.',
                     'inferred_points_using_other_source_rows': other_row_donors,
                     'concealed_texture_is_inferred': True})
    assert all(result.indices[n] == current.indices[n] for n in range(65536) if n not in owned)
    bag = {y*256+x for y in range(72, 112) for x in range(112, 152)}
    assert all(result.indices[n] == original.indices[n] for n in bag)
    return result, {'price_cells': rows, 'entire_original_bag_40x40_exact': True,
                    'bag_pixels_restored_from_incorrect_Buy_Sell_overwrites': sum(current.indices[n] != result.indices[n] for n in bag),
                    'only_owned_33x48_region_changed': True,
                    'changed_pixels': sum(a != b for a, b in zip(current.indices, result.indices, strict=True))}


def main():
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open('out/all_routes_combined_v566_candidate.nds')
    original, before = (PxlImage.from_bytes(r.read_file(FILE)) for r in (clean, current))
    after, proof = repair(original, before, current.read_file('/__arm9__.bin'))
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT/'marker_price_ownership_RESEARCH_ONLY.pxl').write_bytes(after.to_bytes())
    canvas = Image.new('RGB', (696, 320), '#263238')
    draw = ImageDraw.Draw(canvas)
    for row, (title, image) in enumerate((('Original Japanese', original),
                                         ('V566: wrong ownership', before),
                                         ('Research: Sell / Buy / bag', after))):
        draw.text((8+row*232, 4), title, fill='white')
        crop = image.render().crop((110, 46, 154, 114)).convert('RGB')
        canvas.paste(crop.resize((176, 272), Image.Resampling.NEAREST), (8+row*232, 28))
    canvas.save(ROOT/'price_ownership_review.png')
    proof.update(source_file=FILE, clean_sha256=sha(original.source), inherited_sha256=sha(before.source),
                 target_sha256=sha(after.to_bytes()), research_only=True, production_ROM_changed=False)
    (ROOT/'price_ownership_prototype.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(proof, ensure_ascii=False))


if __name__ == '__main__':
    main()
