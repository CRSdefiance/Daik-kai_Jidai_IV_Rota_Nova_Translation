"""Build source/current plaque crops and keep every audit entry open."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/plaque_review_v342/review_packet')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rom', default='out/all_routes_combined_v342_candidate.nds')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open(args.rom)
    clean = NdsImage.open('work/clean.nds')
    prior = NdsImage.open('out/all_routes_combined_v341_candidate.nds')
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 22)
    small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
    jp_font = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 22)
    rows = []
    for filename, group in [('assign_sailors_graphics_v5.json', 'Assign Sailors'),
                            ('person_info_graphics_v3.json', 'Sailor Info')]:
        batch = read(Path('translations') / filename)
        path = batch['file_path']
        assert current.read_file(path) == prior.read_file(path)
        before = PxlImage.from_bytes(clean.read_file(path)).render().convert('RGB')
        after = PxlImage.from_bytes(current.read_file(path)).render().convert('RGB')
        for record in batch['records']:
            number = len(rows) + 1
            box = record['box']
            source_path = ROOT / f'{number:02d}_source.png'
            target_path = ROOT / f'{number:02d}_English.png'
            a, b = before.crop(box), after.crop(box)
            a.save(source_path)
            b.save(target_path)
            assert Image.open(target_path).convert('RGB').tobytes() == b.tobytes()
            rows.append({'number': number, 'id': record['id'], 'screen': group,
                         'Japanese': record['source_japanese'], 'English': record['text'],
                         'meaning': record['source_meaning'], 'source_asset': path,
                         'edit_region': box, 'plaque_bounds': record['plaque_box'],
                         'source_crop': str(source_path), 'English_crop': str(target_path),
                         'source_crop_sha256': sha(source_path.read_bytes()),
                         'English_crop_sha256': sha(target_path.read_bytes()),
                         'fully_completed': False, 'status': 'pending-continued-audit-and-user-review'})
    assert len(rows) == 17
    hint_shot = Path('work/emulation_v193/roster_role_crop_v341/frame_017600_cold_boot.png')
    shot = Image.open(hint_shot).convert('RGB')
    box = (136, 208, 224, 224)
    hint_path = ROOT / '18_Equipped_Items_actual.png'
    shot.crop(box).save(hint_path)
    variants = []
    for text, frame, bounds in [('Armor', 11400, (64, 208, 98, 224)),
                                ('Weapon', 11700, (16, 208, 56, 224))]:
        report = read('work/emulation_v193/plaque_audit_v300_person/capture_report.json')
        capture = next(x for x in report['frames_captured'] if x['frame'] == frame and 'cold_boot' in x['path'])
        assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
        image = Image.open(capture['path']).convert('RGB').crop(bounds)
        path = ROOT / f'18_{text}_historical_actual.png'
        image.save(path)
        variants.append({'English': text, 'crop': str(path), 'capture_ROM_sha256': report['ROM_sha256'],
                         'historical_V299_capture_not_new_current_gameplay': True, 'fully_completed': False})
    rows.append({'number': 18, 'id': 'runtime-equipped-items', 'screen': 'Sailor Info',
                 'Japanese': '装備アイテム', 'English': 'Equipped Items',
                 'meaning': 'Items currently equipped; Weapon and Armor are variants of this same entry.',
                 'English_crop': str(hint_path), 'actual_capture': str(hint_shot),
                 'actual_capture_ROM_sha256': read('work/emulation_v193/roster_role_crop_v341/capture_report.json')['ROM_sha256'],
                 'not_a_source_Japanese_runtime_screenshot': True, 'variants': variants,
                 'fully_completed': False, 'status': 'pending-continued-audit-and-user-review'})

    for group, subset, filename in [('Assign Sailors', rows[:7], 'assign_sailors_review.png'),
                                    ('Sailor Info', rows[7:], 'sailor_info_review.png')]:
        count = (len(subset) + 1) // 2
        sheet = Image.new('RGB', (1160, 130 + count * 180 + 64), '#192026')
        draw = ImageDraw.Draw(sheet)
        draw.text((24, 18), group + ' plaque audit', font=font, fill='#f1e8cd')
        draw.text((24, 55), 'Native asset crops at 3x nearest-neighbor; no smoothing. Source wording shown above.', font=small, fill='#cbd3d8')
        draw.text((24, 80), 'Stat-source crops omit runtime text. Hint captures retain their explicit V341 / V299 provenance.', font=small, fill='#cbd3d8')
        for index, row in enumerate(subset):
            x, y = 18 + index % 2 * 572, 130 + index // 2 * 180
            draw.rounded_rectangle((x, y, x + 552, y + 168), radius=7, fill='#28323a')
            draw.text((x + 12, y + 8), f"{row['number']:02d}  {row['English']}", font=font, fill='#ffffff')
            draw.text((x + 280, y + 12), row['Japanese'], font=jp_font, fill='#d9d0b6')
            if row['number'] != 18:
                draw.text((x + 12, y + 43), ('Original artwork; runtime label' if 12 <= row['number'] <= 17 else 'Original source region'), font=small, fill='#aab9c5')
                draw.text((x + 286, y + 43), 'Current English region', font=small, fill='#aab9c5')
                for image_path, left in [(row['source_crop'], x + 12), (row['English_crop'], x + 286)]:
                    image = Image.open(image_path)
                    sheet.paste(image.resize((image.width * 3, image.height * 3), Image.Resampling.NEAREST), (left, y + 67))
                draw.text((x + 12, y + 145), 'In ongoing audit', font=small, fill='#e5c78e')
            else:
                image = Image.open(row['English_crop'])
                sheet.paste(image.resize((image.width * 3, image.height * 3), Image.Resampling.NEAREST), (x + 12, y + 47))
                draw.text((x + 300, y + 58), 'Actual V341 header', font=small, fill='#aab9c5')
                for offset, variant in zip((12, 200), row['variants']):
                    image = Image.open(variant['crop'])
                    sheet.paste(image.resize((image.width * 3, image.height * 3), Image.Resampling.NEAREST), (x + offset, y + 105))
                draw.text((x + 350, y + 120), 'V299 empty-slot variants', font=small, fill='#aab9c5')
        draw.text((24, sheet.height - 43), '18 total audit entries across both sheets. Occupied weapons/armor and alternate states remain pending.', font=small, fill='#e5c78e')
        sheet.save(ROOT / filename)
    proof = {'ROM': args.rom, 'ROM_sha256': sha(Path(args.rom).read_bytes()),
             'all17_sprite_assets_exact_V341': True, 'all18_audit_entries': rows,
             'source_reference_ROM': 'work/clean.nds',
             'native_source_asset_crops_not_a_claim_of_new_gameplay': True,
             'all18_fully_completed_false': True, 'full_goal_complete': False}
    (ROOT / 'review_inventory.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'entries': len(rows), 'sheets': 2, 'all_remain_in_audit': True}))


if __name__ == '__main__':
    main()
