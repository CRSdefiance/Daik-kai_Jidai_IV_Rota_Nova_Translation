"""Verify the bounded collection survey without crediting failed site screens."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

OUT = Path('work/analysis/collection_gallery_v526')
ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v525_candidate.nds')
NAMES = ('Pumpkin Seeds', 'Silkworms', 'Valiant Bec de Corbin',
         "Kublai's Greatsword", "Timur's Chainmail", 'Tireless Hawser',
         "Poseidon's Roar", 'Stylish Boots', 'Maiden Figurehead', 'Venus de Milo',
         'Aksum Gold Seal', 'Sahara Map', 'Ceremonial Knife', 'Twisted Horn')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def mask(font, image, text, x, y, advance=5):
    expected = {(x + n * advance + gx, y + gy) for n, ch in enumerate(text)
                for gy in range(11) for gx in range(6) if font.decode(ch).getpixel((gx, gy))}
    actual = {(xx, yy) for yy in range(y, y + 11) for xx in range(x, x + len(text) * advance + 2)
              if min(image.getpixel((xx, yy))) > 200
              and max(image.getpixel((xx, yy))) - min(image.getpixel((xx, yy))) < 5}
    assert actual == expected, (text, len(actual), len(expected))
    return {'English': text, 'origin': [x, y], 'advance': advance, 'complete_ink_pixels': len(expected),
            'first_and_final_letters_and_blank_cells_exact': True}


def report(path, digest):
    data = read(path)
    assert data['ROM_sha256'] == digest and data['cold_boot'] and not data['savestate_loaded']
    assert not data['callback_errors'] and data['synthetic_gallery_fixtures']
    assert not data['earned_unlock_verified']
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    donor = data['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    return data


def main():
    digest = sha(ROM.read_bytes())
    assert digest == 'c84d292ac756cd91c817637c1bdf9257c4f4a16512eadedba698e7d10024a605'
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl'))
    palette = [tuple(c // 8 for c in value[:3]) for value in atlas.palette]
    pages_root = ROOT / 'items_pages_v526'
    pages = report(pages_root / 'capture_report.json', digest)
    assert pages['scripted_input_schedule'] == read(OUT / 'items_pages_inputs.json')
    assert 'Undefined instruction' not in (OUT / 'items_pages_run.log').read_text(encoding='utf-8')
    cases = []
    for page, text in enumerate(NAMES):
        path = pages_root / f'frame_{2800 + page * 200:06d}_cold_boot.png'
        image = Image.open(path).convert('RGB')
        masks = [mask(font, image, text, 56, 24), mask(font, image, 'Items', 116, 2)]
        item_id = page * 15
        indices = atlas.indices[item_id * 1024:(item_id + 1) * 1024]
        opaque = [(n % 32, n // 32, palette[value]) for n, value in enumerate(indices) if value]
        assert all(tuple(c // 8 for c in image.getpixel((16 + x, 24 + y))) == color
                   for x, y, color in opaque), item_id
        cases.append({'page': page + 1, 'selected_item_id': item_id, 'image': str(path),
                      'complete_masks': masks, 'exact_selected_icon_opaque_pixels': len(opaque)})
    first, wrapped = [Image.open(pages_root / f'frame_{n:06d}_cold_boot.png').convert('RGB')
                      for n in (2800, 5600)]
    assert first.crop((0, 0, 256, 192)).tobytes() == wrapped.crop((0, 0, 256, 192)).tobytes()
    mask(font, wrapped, NAMES[0], 56, 24)
    sites = read(OUT / 'single_site_captures.json')
    assert len(sites) == 21 and [r['site_id'] for r in sites] == list(range(21))
    assert [r['site_id'] for r in sites if r['native_CPU_fault_observed']] == [1, 4]
    for row in sites:
        report(Path(row['capture_report']), digest)
        assert sha(Path(row['image']).read_bytes()) == row['image_sha256']
        if row['actual_site_display_credit']:
            image = Image.open(row['image']).convert('RGB')
            mask(font, image, 'Historic Sites', 86, 2, 6)
    clean_digest = sha(Path('work/clean.nds').read_bytes())
    clean = report(ROOT / 'collection_site_01_clean_v526' / 'capture_report.json', clean_digest)
    assert 'Undefined instruction: 0x26322A11 PC=0xE5881234' in (OUT / 'site_01/clean_capture.log').read_text(encoding='utf-8')
    assert clean['read_only_native_state']['ARM9_instruction_address'] == 0xE5881238
    review = read(OUT / 'historic_site_name_review.json')
    assert len(review['records']) == 21
    assert [r['site_id'] for r in review['records'] if not r['fits_current_slot']] == [1, 2, 4, 16, 17, 18, 19, 20]
    campaign = read('translations/graphics_completion_campaign_v1.json')
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'production_ROM_modified': False,
             'all14_Items_pages_and_original_wrap_verified': True,
             'all28_complete_item_heading_and_selected_name_masks': cases,
             'all198_individual_item_descriptions_tooltips_grid_icon_masks_not_claimed': True,
             'all21_separate_site_fixture_outcomes_recorded': sites,
             'successful_site_list_screens': 19, 'faulting_site_ids_without_display_credit': [1, 4],
             'site_01_fault_also_reproduced_in_unmodified_Japanese_ROM': True,
             'fault_cause_not_proven': True, 'natural_travel_or_discovery_not_claimed': True,
             'all21_site_names_reviewed_not_yet_applied': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'collection_survey_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Collection survey:14 Items pages,28 complete masks,14 exact opaque icons,wrap,19 site lists; two site faults remain uncredited.')


if __name__ == '__main__':
    main()
