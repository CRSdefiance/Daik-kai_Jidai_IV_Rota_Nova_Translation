"""Complete ordinary name bounds through real item ownership/name consumers."""

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
    destination = Path('work/qa/item_crew_owners_native')
    destination.mkdir(parents=True, exist_ok=True)
    cases, panels = [], []
    configurations = [(24, crew, None) for crew in range(207)]
    configurations += [(49, crew, None) for crew in (0, 103, 206)]
    configurations += [(24, 206, b'ABCDEFGHIJKLMNOPQR'[:length]) for length in range(1, 19)]
    for item, crew, mutable in configurations:
        for mode in (4, 16):
            native = verify_page(source, plan, 'main', (0, 2), font, mode, item_index=item,
                                 common=common, crew_index=crew, player_name=mutable)
            owner = next(r for r in native['item_draws'] if r['x'] == 88 and r['y'] == 24)
            if native['item_provider_contracts'] != ['item_art_provider_not_rendered']:
                raise ValueError('Actual crew ownership case retained a lookup/name/COMMON mock')
            cases.append({'item_index': item, 'crew_index': crew, 'mode': mode,
                          'mutable_name': mutable.decode('ascii') if mutable else None,
                          'owner_draw': owner, 'classification': native['item_actual_owner_classifications'],
                          'initialization': native['item_crew_owner_initialization'],
                          'draws': native['item_draws'], 'pixels_sha256': sha(native['pixels']),
                          'native_search_classification_name_all_glyphs_pixels_bounds_nonoverlap_pass': True})
            if mode == 16 and ((mutable is None and item == 24 and crew in (0, 68, 103, 201, 202, 206))
                               or mutable is not None and len(mutable) in (1, 18)):
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                               for c in struct.unpack('<49152H', native['pixels'])])
                panels.append((crew, mutable, panel.crop((0, 0, 240, 96)).resize((720, 288), Image.Resampling.NEAREST)))
        if len(cases) % 64 == 0:
            print(f'{len(cases)} native ownership/name raster cases pass', flush=True)
            Path('work/analysis/item_crew_owners_native_phase.json').write_text(json.dumps({
                'target_arm9_sha256': sha(source), 'status': 'partial-native-ownership-phase',
                'cases': cases}, indent=2) + '\n', encoding='utf-8')
    sheet = Image.new('RGB', (1456, ((len(panels) + 1) // 2) * 316), 'white')
    drawing = ImageDraw.Draw(sheet)
    for number, (crew, mutable, panel) in enumerate(panels):
        x, y = 8 + number % 2 * 728, number // 2 * 316
        drawing.text((x, y + 2), f'Crew {crew}; mutable {mutable!r}; native names/search; artwork fixture', fill='black')
        sheet.paste(panel, (x, y + 22))
        panel.save(destination / f'panel_{number}.png')
    sheet.save(destination / 'native_sheet.png')
    report = {'status': 'pass-native-207-ordinary-item-owner-names-and-mutable-captain-bounds',
              'target_arm9_sha256': sha(source), 'cases': cases,
              'ordinary_crew_name_count': 207, 'mutable_name_lengths': list(range(1, 19)),
              'visual_review': {'complete': False, 'panel_count': len(panels), 'sheet': str(destination / 'native_sheet.png')},
              'limitations': ['Native ownership classification/search, current-captain lookup, eligibility and name virtual execute.',
                              'Ordinary crew constructors execute; equipment state and current captain are explicit runtime inputs.',
                              'Mutable captain interface vtable/name storage and containing tables are initialization contracts.',
                              'All ordinary names rendered for native weapon search; armor first/middle/last and mutable-name boundaries also execute.',
                              'These bounds checks do not establish narrative name fidelity or every crew member being recruitable.',
                              'Equipment-role eligibility variants, ship owners, artwork/full parent composition and physical gameplay remain pending.',
                              'Warm COMMON cache and local bitmap/font origin initialization remain contracts; source getters/copy are native.',
                              'Research only; no ROM integration.']}
    Path('work/analysis/item_crew_owners_native_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Pass: {len(cases)} actual ownership/name rasters; all 207 ordinary names, armor boundaries, all mutable lengths 1..18.')


if __name__ == '__main__':
    main()
