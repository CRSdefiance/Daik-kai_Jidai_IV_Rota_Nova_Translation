"""Native whole-panel review grid covering every projected category/role label."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_item_interface_research import ROLE_ATTRIBUTES, verify_page


def main():
    source = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    if sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Item preview research identity differs')
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    font = image.read_file('/GRP/KANJI.FNT')
    destination = Path('work/qa/item_interface_native')
    rows = []
    for group in range(4):
        sheet = Image.new('RGB', (1456, 632), 'white')
        draw = ImageDraw.Draw(sheet)
        for cell in range(4):
            role = group * 4 + cell
            category = role % 13
            native = verify_page(source, plan, 'main', (255, 3, category, ROLE_ATTRIBUTES[role]), font, 16)
            panel = Image.new('RGB', (256, 192))
            panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                           for c in struct.unpack('<49152H', native['pixels'])])
            panel = panel.crop((0, 0, 240, 96)).resize((720, 288), Image.Resampling.NEAREST)
            origin = (8 + cell % 2 * 728, cell // 2 * 316)
            draw.text((origin[0], origin[1] + 2), f'Category {category}; role {role}; native item canvas, owner fixtures', fill='black')
            sheet.paste(panel, (origin[0], origin[1] + 22))
            rows.append({'category': category, 'role': role, 'native_pixels_sha256': sha(native['pixels'])})
        sheet.save(destination / f'label_grid_{group}.png')
    Path('work/analysis/item_label_grid_proof.json').write_text(json.dumps({
        'target_arm9_sha256': sha(source), 'cases': rows,
        'all_13_categories_and_16_roles_covered': True, 'visually_reviewed': False}, indent=2) + '\n', encoding='utf-8')
    print('Four native panel grids cover every item-only category and crew role; visual review pending.')


if __name__ == '__main__':
    main()
