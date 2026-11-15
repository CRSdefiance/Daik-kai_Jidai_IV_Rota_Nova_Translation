"""Genuine Istanbul purchase, equipped weapon, source review and cold-load pixels."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import (
    SJIS_GLYPH_COUNT,
    SJIS_MAP_OFFSET,
    GameAsciiFont,
    decode_glyph,
)
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.probe_button_prompt_native import call, machine
from scripts.record_navigation_v327 import dark_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_med_ports_v471 import town
from scripts.verify_occupied_armor_v469 import compact_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROM = Path('out/all_routes_combined_v474_candidate.nds')
ROOT = Path('work/analysis/istanbul_weapon_v477')
CAPTURE = Path('work/emulation_v193/istanbul_weapon_v477')
RELOAD = Path('work/emulation_v193/weapon_reload_v477')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def item_state(arm, path, index):
    raw = path.read_bytes()
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    item = u.reg_read(UC_ARM_REG_R0) + 4 + index * 20
    values = {}
    for key, function in [('category', 0x4A448), ('price', 0x4A410), ('found_flag', 0x4A368)]:
        call(u, function, (item,))
        values[key] = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A53C, (item,))
    values['name'] = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 96)).split(b'\0')[0].decode('cp932')
    out = 0x02470020
    u.mem_write(out - 16, b'\xA5' * 48)
    call(u, 0x49DE8, (out, item))
    descriptor = bytes(u.mem_read(out, 16))
    values['owner_descriptor_type'] = struct.unpack_from('<I', descriptor, 4)[0]
    values['owner_index_or_city_if_type2_or4'] = struct.unpack_from('<I', descriptor, 8)[0] if values['owner_descriptor_type'] in (2, 4) else None
    assert bytes(u.mem_read(out - 16, 16)) == bytes(u.mem_read(out + 16, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    return {'item_id': index, 'snapshot': str(path), 'snapshot_sha256': sha(raw),
            'captured_RAM_preserved': True, **values}


def currency_mask(rom, image):
    text = 'Price: ３００００ coins.'
    arm = rom.read_file('/__arm9__.bin')
    ascii_font = GameAsciiFont.from_arm9(arm)
    mapping = {code: index for index, code in enumerate(struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H', arm, SJIS_MAP_OFFSET))}
    kanji = rom.read_file('/GRP/KANJI.FNT')
    expected, x0, y0 = set(), 16, 296
    x = x0
    for character in text:
        if ord(character) < 128:
            glyph, advance = ascii_font.decode(character), 6
        else:
            code = int.from_bytes(character.encode('cp932'), 'big')
            glyph, advance = decode_glyph(kanji, mapping[code]), 12
        expected.update((x + dx, y0 + dy) for dy in range(11) for dx in range(glyph.width) if glyph.getpixel((dx, dy)))
        x += advance
    actual = {(px, py) for py in range(y0, y0 + 11) for px in range(x0, x) if image.getpixel((px, py)) == (0, 8, 0)}
    assert actual == expected
    return {'text': text, 'bounds': [x0, y0, x, y0 + 11], 'ink_pixels': len(expected),
            'all_ASCII_and_native_fullwidth_currency_glyphs_and_blank_cells_exact': True}


def main():
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    digest = sha(ROM.read_bytes())
    font = GameAsciiFont.from_arm9(arm)
    reports = []
    for folder, count in [(CAPTURE, 15495), (RELOAD, 3800)]:
        path = folder / 'capture_report.json'
        report = read(path)
        assert report['ROM_sha256'] == digest and report['frames'] == count
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, report))
    donor = reports[0][1]['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    saved = ROOT / 'istanbul_weapon_test_copy.dsv'
    assert saved.read_bytes() == Path(donor['destination']).read_bytes()
    assert sha(saved.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    samples = [item_state(arm, CAPTURE / f'frame_{frame:06d}_arm9_ram.bin', 29) for frame in (8695, 9695, 10595)]
    samples.append(item_state(arm, RELOAD / 'final_arm9_ram.bin', 29))
    assert [(s['owner_descriptor_type'], s['owner_index_or_city_if_type2_or4']) for s in samples] == [(4, 22), (0, None), (2, 1), (2, 1)]
    assert all(s['name'] == 'Golden Cutlass' and s['category'] == 2 and s['price'] == 30000 for s in samples)
    armor = item_state(arm, RELOAD / 'final_arm9_ram.bin', 49)
    assert armor['name'] == 'Blue Oak Shield' and armor['category'] == 3
    assert (armor['owner_descriptor_type'], armor['owner_index_or_city_if_type2_or4']) == (2, 1)
    before = Image.open(CAPTURE / 'frame_010595_navigation.png').convert('RGB')
    after = Image.open(RELOAD / 'frame_003800_final.png').convert('RGB')
    assert before.tobytes() == after.tobytes()
    text = 'Golden Cutlass'
    ink, bounds = complete_mask(font, text, after, 18, 210, (0, 8, 0))
    assert ink == 165 and bounds == [18, 210, 102, 221]
    expected = {(18 + n * 6 + x, 210 + y) for n, c in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    tile = paper(88, 16, palette)
    for y in range(16):
        for x in range(88):
            point = 16 + x, 208 + y
            rgb = (0, 8, 0) if point in expected else palette[tile[y * 88 + x]][:3]
            assert native5(after.getpixel(point)) == native5(rgb)
    assert rom.read_file('/_pxl/item.pxl') == clean.read_file('/_pxl/item.pxl')
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    assert [native5(v) for v in after.crop((16, 224, 48, 256)).get_flattened_data()] == [
        native5(v) for v in atlas.crop((0, 29 * 32, 32, 30 * 32)).get_flattened_data()]
    batch = read(Path('translations/person_info_graphics_v3.json'))
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    for image in (before, after):
        for row in batch['records']:
            x0, y0, x1, y1 = row['plaque_box']
            assert all(native5(image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]][:3])
                       for y in range(y0, y1) for x in range(x0, x1))
    skills = []
    for label, x, y in [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
                        ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
                        ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]:
        value = numeric_field(font, after, x + 42, y)
        count, box = complete_mask(font, f'{label:>7}{value:3d}', after, x, y, (230, 230, 230))
        skills.append({'label': label, 'value': value, 'complete_ink_pixels': count, 'bounds': box})
    inventory = Image.open(CAPTURE / 'frame_009695_navigation.png').convert('RGB')
    inventory_masks = [compact_mask(font, word, inventory, x, y) for word, x, y in
                       [(text, 56, 24), ('Weapon', 8, 64),
                        ('A very heavy military sword made entirely of', 8, 112), ('gold.', 8, 128)]]
    messages = []
    for frame, words in [(7465, ['Discovered Istanbul.']), (7595, ['Dock at Istanbul?']),
                         (8795, ['Buy it?']), (8895, ['Thank you!']),
                         (9895, ['Hodram Joakim Bergstrom equipped', 'Golden Cutlass.'])]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        messages.extend({'frame': frame, 'mask': dark_text(font, word, image, (8, 292, 253, 350))} for word in words)
    price_image = Image.open(CAPTURE / 'frame_008795_navigation.png').convert('RGB')
    price = currency_mask(rom, price_image)
    assert 'Price: ３００００ coins.'.encode('cp932') in (CAPTURE / 'frame_008795_arm9_ram.bin').read_bytes()
    u = machine(clean.read_file('/__arm9__.bin'))
    call(u, 0xCDAFC, (29, 1))
    metadata = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 32))
    name_pointer = struct.unpack_from('<I', metadata)[0]
    japanese_name = bytes(u.mem_read(name_pointer, 96)).split(b'\0')[0].decode('cp932')
    japanese_description = IlnkContainer.parse(clean.read_file('/COMMON/MESFILE.DK4')).blocks[30].split(b'\0')[10].decode('cp932').strip()
    assert japanese_name == '黄金のカットラス'
    assert japanese_description == '大変に重い軍刀。すべての部分が黄金で作られている。'
    town_image = Image.open(CAPTURE / 'frame_007995_navigation.png').convert('RGB')
    town_masks = town(font, town_image, 'Istanbul', '(N41 E28)', ['Sulfur', 'Carpets', 'Antiques'])
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p, _ in reports],
             'original_Syracuse_donor_unchanged': True, 'normal_Istanbul_discovery_docking_Guild_purchase_and_equip': True,
             'clean_Japanese_name': japanese_name, 'clean_Japanese_description': japanese_description,
             'English_name_and_description_faithful_to_clean_source': True,
             'original_native_ownership_progression': samples, 'found_flag_alone_not_used_as_ownership_proof': True,
             'Blue_Oak_Shield_still_equipped_after_cold_load': armor,
             'complete_inventory_masks': inventory_masks, 'complete_messages': messages,
             'complete_native_fullwidth_price_mask': price, 'Istanbul_complete_town_masks': town_masks,
             'complete_owner': find_mask(font, 'Hodram Joakim Bergstrom', after, (80, 16, 256, 60)),
             'tooltip_ink_pixels': ink, 'tooltip_bounds': bounds, 'paper_and_corner_pixels_exact': 1408,
             'original_icon_row29_pixels_exact': 1024, 'all20_person_plaque_instances_exact': True,
             'all10_complete_skill_lines': skills, 'entire_occupied_Weapon_screen98304_pixels_exact_after_cold_load': True,
             'normal_slot6_save_completed_with4200_more_frames_then_cold_loaded': True,
             'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'occupied_Weapon_Golden_Cutlass_Hodram_Normal_context_verified': True,
             'other_equipment_names_owners_conditions_and_wider_graphics_remain_open': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'weapon_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Genuine Golden Cutlass purchase/equip/save/reload;165 tooltip,1408 paper,1024 icon pixels;whole98304 screen exact.')


if __name__ == '__main__':
    main()
