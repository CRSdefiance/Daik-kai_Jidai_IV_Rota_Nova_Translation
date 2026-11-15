"""All fixed ship names and mutable-name bounds through real figurehead search."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_item_advice_menus import TARGET
from scripts.verify_item_interface_research import verify_page


def main():
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    if sha(source) != TARGET:
        raise ValueError('Exact cache-maintained item target required')
    image_path = Path('out/all_routes_combined_v158_candidate.nds')
    if sha(image_path.read_bytes()) != '9a197373ba448718f3c0d887fdd27f01ce19b75dae11bb22515fed36981a7f5f':
        raise ValueError('Immutable V158 resources differ')
    image = NdsImage.open(image_path)
    font, common = image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4')
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    destination = Path('work/qa/item_ship_owners_native')
    destination.mkdir(parents=True, exist_ok=True)
    configurations = [(ship, None) for ship in range(50, 154)]
    configurations += [(slot, b'ABCDEFGHIJKLMNOPQR'[:length]) for slot in (0, 49) for length in range(1, 19)]
    cases, panels = [], []
    for ship, name in configurations:
        for mode in (4, 16):
            native = verify_page(source, plan, 'main', (0, 3), font, mode, item_index=118,
                                 common=common, ship_index=ship, ship_name=name)
            if native['item_provider_contracts'] != ['item_art_provider_not_rendered']:
                raise ValueError('Actual ship ownership retained a lookup/name/COMMON callback')
            owner = next(r for r in native['item_draws'] if r['x'] == 88 and r['y'] == 24)
            cases.append({'ship_index': ship, 'mutable_name': name.decode('ascii') if name else None,
                          'mode': mode, 'owner_draw': owner, 'draws': native['item_draws'],
                          'classification': native['item_actual_owner_classifications'],
                          'ship_initialization': native['item_ship_owner_initialization'],
                          'pixels_sha256': sha(native['pixels']),
                          'native_ship_init_search_name_all_glyphs_pixels_bounds_nonoverlap_pass': True})
            if mode == 16 and ((name is None and ship in (50, 99, 107, 131, 153))
                               or name is not None and len(name) in (1, 18)):
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                               for c in struct.unpack('<49152H', native['pixels'])])
                panels.append((ship, name, panel.crop((0, 0, 240, 96)).resize((720, 288), Image.Resampling.NEAREST)))
        if len(cases) % 64 == 0:
            print(f'{len(cases)} native ship ownership/name cases pass', flush=True)
            Path('work/analysis/item_ship_owners_native_phase.json').write_text(json.dumps({
                'target_arm9_sha256': sha(source), 'status': 'partial-native-ship-ownership-phase',
                'cases': cases}, indent=2) + '\n', encoding='utf-8')
    sheet = Image.new('RGB', (1456, ((len(panels) + 1) // 2) * 316), 'white')
    drawing = ImageDraw.Draw(sheet)
    for number, (ship, name, panel) in enumerate(panels):
        x, y = 8 + number % 2 * 728, number // 2 * 316
        drawing.text((x, y + 2), f'Ship {ship}; mutable {name!r}; native initializer/search/name; artwork fixture', fill='black')
        sheet.paste(panel, (x, y + 22))
        panel.save(destination / f'panel_{number}.png')
    sheet.save(destination / 'native_sheet.png')
    report = {'status': 'pass-all-fixed-ship-item-owner-names-and-mutable-name-bounds',
              'target_arm9_sha256': sha(source), 'cases': cases,
              'fixed_name_count': 104, 'native_ship_initializer_count': 154,
              'mutable_name_lengths': list(range(1, 19)), 'mutable_slot_boundaries': [0, 49],
              'visual_review': {'complete': False, 'panel_count': len(panels), 'sheet': str(destination / 'native_sheet.png')},
              'limitations': ['All 154 native default ship initializers execute per case; 104 full fixed names match source and fit nineteen-byte fields.',
                              'Native figurehead conversion, ship search/active status/equipment getters, owner classification and name virtual execute.',
                              'Ship vtable/outer table initialization, figurehead equipment and active mutable-slot name/class are controlled runtime inputs.',
                              'Item metadata, original warm COMMON selection/copy and complete renderer glyphs/pixels are native.',
                              'Artwork, local bitmap/font origin, warm cache initialization and physical composition remain contracts.',
                              'Equipment-role eligibility, random/download states, counter/parent and physical gameplay remain pending.',
                              'Existing fixed-name wording is preserved; older shorthand/source-context fidelity still needs its separate review.',
                              'Research only; no new ROM or promotion.']}
    Path('work/analysis/item_ship_owners_native_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Pass: {len(cases)} native ship ownership rasters, 104 fixed names, all editor lengths 1..18 at slots 0/49.')


if __name__ == '__main__':
    main()
