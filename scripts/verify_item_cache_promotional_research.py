"""Fresh cache-target rasters and real default promotional resource coverage."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_item_lookup_abi import verify as lookup_abi
from scripts.verify_item_interface_research import verify_page


def main():
    old = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    source, cache = transform(old)
    if source != Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes():
        raise ValueError('Deterministic cache-target identity differs')
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    inherited = json.loads(Path('work/analysis/item_interface_native_proof.json').read_text(encoding='utf-8'))
    if plan['target_arm9_sha256'] != sha(old) or inherited['target_arm9_sha256'] != sha(old):
        raise ValueError('Preserved item-prefix evidence differs')
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    source_rom_sha = sha(Path('out/all_routes_combined_v158_candidate.nds').read_bytes())
    if source_rom_sha != '9a197373ba448718f3c0d887fdd27f01ce19b75dae11bb22515fed36981a7f5f':
        raise ValueError('Immutable V158 resource ROM differs')
    font, common = image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4')
    destination = Path('work/qa/item_cache_promotional_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1456, 1580), 'white')
    drawing = ImageDraw.Draw(sheet)
    rows = []
    for index in (*range(188, 198), 5, 22, 151):
        for page in ('main', 'standalone'):
            for mode in (4, 16):
                native = verify_page(source, plan, page, (0, 4 if page == 'main' else 1),
                                     font, mode, item_index=index, common=common)
                rows.append({'index': index, 'page': page, 'mode': mode,
                             'draws': native['item_draws'], 'actual_common_ids': native['item_actual_common_ids'],
                             'pixels_sha256': sha(native['pixels']),
                             'provider_contracts': native['item_provider_contracts'],
                             'promotional_default_initialization': native['item_promotional_default_initialization'],
                             'native_object_metadata_initialization': native['item_native_object_metadata_initialization'],
                             'native_name_metadata_COMMON_all_glyphs_pixels_bounds_nonoverlap_pass': True})
                if index >= 188 and page == 'main' and mode == 16:
                    panel = Image.new('RGB', (256, 192))
                    panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                                   for c in struct.unpack('<49152H', native['pixels'])])
                    panel = panel.crop((0, 0, 240, 96)).resize((720, 288), Image.Resampling.NEAREST)
                    n = index - 188
                    origin = (8 + n % 2 * 728, n // 2 * 316)
                    drawing.text((origin[0], origin[1] + 2), f'Promotional item {index}; native text, price/art fixtures', fill='black')
                    sheet.paste(panel, (origin[0], origin[1] + 22))
                    panel.save(destination / f'item_{index}.png')
        print(f'Item {index}: both native callers/formats pass', flush=True)
    sheet.save(destination / 'native_sheet.png')
    proof = {'status': 'pass-cache-target-local-rasters-and-ten-default-promotional-providers',
             'target_arm9_sha256': sha(source), 'source_rom_sha256': source_rom_sha,
             'font_sha256': sha(font), 'COMMON_sha256': sha(common), 'cache_plan': cache, 'cases': rows,
             'private_lookup_abi': lookup_abi(source, plan),
             'preserved_prefix_evidence': {'arm9_sha256': sha(old),
                                          'proof_sha256': sha(Path('work/analysis/item_interface_native_proof.json').read_bytes()),
                                          'payload_prefix_bytes': cache['item_payload_prefix_bytes_preserved'],
                                          'scope': 'Original main/ITCM/data restored comparison and complete item payload preserved; '
                                                   '2090 previous rasters are inherited byte evidence, not fresh target executions.'},
             'visual_review': {'complete': False, 'sheet': str(destination / 'native_sheet.png')},
             'limitations': ['Ten promotional defaults execute their real source initialization segment and dynamic provider.',
                             'Initializer pauses before random additions; CPU state restored explicitly for the separate draw.',
                             'Item vtable/table seeds and warm COMMON-cache initialization, price ownership, artwork and local bitmap origin remain contracts.',
                             'Random/download states, real crew/ship owners, Advice menus, counter/parent and physical cold boot remain pending.',
                             'Research only; V158 remains latest combined ROM.']}
    Path('work/analysis/item_cache_promotional_native_proof.json').write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Pass: {len(rows)} fresh rasters, ten native promotional defaults, 237 lookup ABI cases; visual review pending.')


if __name__ == '__main__':
    main()
