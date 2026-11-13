"""Repeat complete fleet-name selection and pixels on the repaired V148 stack."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.persistent_name_release import TARGET
from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import components
from scripts.probe_fleet_name_display_callers import execute


def prepare():
    image = NdsImage.open('out/all_routes_combined_v148_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    if sha(source) != TARGET:
        raise ValueError('Exact complete V148 required')
    old, spare = 0x135260, 0x138878
    if (source[old:old + 16] != '所属不明艦隊'.encode('cp932').ljust(16, b'\0')
            or any(source[spare:spare + 28])
            or struct.unpack_from('<2I', source, 0x36B54) != (0x02135260, 0x02135258)):
        raise ValueError('Original fleet owners and reviewed companion spare differ')
    references = []
    for name, _, raw in components(image):
        for field in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, field)[0] - 0x02000000
            if old <= pointer < old + 16 or spare <= pointer < spare + 28:
                references.append((name, field, pointer))
    if references != [('arm9', 0x36B54, old)]:
        raise ValueError('Fleet storage has unclassified address references')
    saved = bytearray(source)
    saved[old:old + 16] = b'Pirate %s\0'.ljust(16, b'\0')
    saved[spare:spare + 28] = b'Unidentified fleet\0'.ljust(28, b'\0')
    struct.pack_into('<2I', saved, 0x36B54, 0x02000000 + spare, 0x02000000 + old)
    restored = bytearray(saved)
    for a, b in ((old, old + 16), (spare, spare + 28), (0x36B54, 0x36B5C)):
        restored[a:b] = source[a:b]
    if restored != source:
        raise ValueError('Fleet research changes unrelated V148 bytes')
    return bytes(saved), references


def main():
    source, references = prepare()
    font = NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    cases, panels = [], []
    for kind in ('fixed', 'centered'):
        selections = [(index, 1 if index == 0 else 0, '') for index in range(207)]
        selections += [(route, route, name) for route in range(4)
                       for name in ('A', 'A' * 15, 'A' * 16, '海' * 8, 'Indigo海')]
        selections += [(208, 0, '')]
        for index, route, name in selections:
            result, pixels = execute(source, kind, name, raster=True, kanji_font=font,
                                     captain_index=index, current_character=route)
            cases.append(result)
            if (index == 82 or index == 61 or index == 208
                    or (index == route == 0 and name in ('A' * 16, '海' * 8))):
                panel = Image.new('RGB', (192, 72))
                panel.putdata([(255, 255, 255) if ((pixels[(y * 192 + x) // 2] >> ((x % 2) * 4)) & 15) == 1
                               else (170, 170, 170) if ((pixels[(y * 192 + x) // 2] >> ((x % 2) * 4)) & 15) == 15
                               else (0, 0, 0) for y in range(72) for x in range(192)])
                labeled = Image.new('RGB', (576, 248), 'white')
                labeled.paste(panel.resize((576, 216), Image.Resampling.NEAREST), (0, 32))
                ImageDraw.Draw(labeled).text((8, 8), f'{kind}: captain {index}, route {route}, bytes {len(result["name_fixture"].encode("cp932")) if result["name_fixture"] else 0}', fill='black')
                panels.append(labeled)
    destination = Path('work/qa/fleet_names_v148_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1152, 248 * 5), 'white')
    for index, panel in enumerate(panels):
        sheet.paste(panel, ((index // 5) * 576, (index % 5) * 248))
    sheet_path = destination / 'native_sheet.png'
    sheet.save(sheet_path)
    Path('work/analysis/fleet_names_v148_research_arm9.bin').write_bytes(source)
    proof = {'status': 'pass-native-captain-name-selection-and-fleet-pixels-review-pending',
             'source_arm9_sha256': TARGET, 'research_arm9_sha256': sha(source),
             'address_candidates_in_reused_allocations': references, 'cases': cases,
             'ordinary_name_cases': 414, 'stored_player_name_cases': 40, 'sentinel_cases': 2,
             'native_sheet': str(sheet_path), 'native_sheet_sha256': sha(sheet_path.read_bytes()),
             'candidate_changed': False, 'physical_gameplay_verified': False,
             'limits': ['Captain byte/current-character route and no-affiliation branch are fixtures; live setters/eligibility are not bounded.',
                        'Ordinary actors execute their constructor; player interface vtable and valid stored names are initialization fixtures.',
                        'Native captain selector, root/current-character getters, real virtual name dispatch, formatter and glyph bodies execute.',
                        'Player names test valid sixteen-byte saved fields; physical saves and malformed-field handling are not executed.',
                        'Outer parent composition, bitmap clear/default vtable and font loading remain contracts; other virtual display consumers are open.',
                        'Research only; strict registration and saved-ROM/patch verification remain pending.']}
    Path('work/analysis/fleet_names_v148_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} connected native captain/name/fleet rasters pass; complete glyph order, bounds and independent pixels verified.')


if __name__ == '__main__':
    main()
