"""Both real conditional item descriptors and complete native footer rasters."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_scene_caption_raster import execute
from scripts.probe_scene_caption_raster import expected_pixels

TARGET = 'edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663'
CONFIGURATIONS = [('gallery', flag, True) for flag in (False, True)] + [
    ('regular', flag, select) for flag in (False, True) for select in (False, True)]


def verify(source, configuration, mode):
    native = execute(source, 'fixture', item_menu=configuration, mode=mode)
    menu, advice, select = configuration
    labels = (['Prev', 'Next', 'Advice' if advice else None, None, 'Back', None]
              if menu == 'gallery' else [None, None, 'Advice' if advice else None, None, 'Back', 'Select' if select else None])
    rendered = [label for label in reversed(labels) if label]
    if [r['text'] for r in native['footer_draws']] != rendered:
        raise ValueError('Actual item footer loses a complete label or conditional state')
    descriptor = native['item_menu_descriptor']
    if native['footer_labels'] != descriptor['words']:
        raise ValueError('Native footer does not transfer the actual item descriptor')
    consumed = ''.join(rendered)
    expected_glyphs = [{'code': ord(c), 'style': 1, 'x': i * 6, 'y': 0} for i, c in enumerate(consumed)]
    if (native['glyphs'] != expected_glyphs
            or native['pixels'] != expected_pixels(source, consumed, 0, 0, mode, advance=6)):
        raise ValueError('Actual item footer drops leading/interior/final glyphs or pixels')
    placements = []
    for slot, label in enumerate(labels):
        left, width, source_x = native['footer_metadata'][slot * 3:slot * 3 + 3]
        if label is None:
            if left != -1:
                raise ValueError('Disabled item command remains visible')
            continue
        if (width != len(label) * 6 or not 0 <= left <= left + width <= 256
                or not 0 <= source_x <= source_x + width <= len(consumed) * 6):
            raise ValueError('Item footer width/placement clips a complete command')
        placements.append({'slot': slot, 'text': label, 'left': left, 'width': width, 'source_x': source_x})
    ordered = sorted(placements, key=lambda row: row['left'])
    if any(a['left'] + a['width'] > b['left'] for a, b in pairwise(ordered)):
        raise ValueError('Complete native item footer labels overlap')
    if not {0xCA890, 0xCA780, 0xCA9F0, 0xD5160, 0xD5404, 0xD16B4, 0xD5140} <= set(native['executed_offsets']):
        raise ValueError('Item menu bypassed native footer transfer/measurement/render/cleanup')
    native['verified_placements'] = placements
    return native


def main():
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    if sha(source) != TARGET:
        raise ValueError('Exact cache-maintained item target required')
    destination = Path('work/qa/item_advice_menus_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1552, 330), 'white')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for number, configuration in enumerate(CONFIGURATIONS):
        for mode in (4, 16):
            native = verify(source, configuration, mode)
            cases.append({'configuration': configuration, 'mode': mode,
                          'descriptor': native['item_menu_descriptor'], 'placements': native['verified_placements'],
                          'draws': native['footer_draws'], 'pixels_sha256': sha(native['pixels']),
                          'complete_glyphs_pixels_nonoverlap_bounds_and_state_transfer_pass': True})
            if mode == 16:
                raster = Image.new('RGB', (256, 192))
                raster.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14 else (0, 0, 0)
                                for c in struct.unpack('<49152H', native['pixels'])])
                panel = Image.new('RGB', (256, 24), 'white')
                for row in native['verified_placements']:
                    panel.paste(raster.crop((row['source_x'], 0, row['source_x'] + row['width'], 12)), (row['left'], 6))
                panel = panel.resize((768, 72), Image.Resampling.NEAREST)
                x, y = 8 + number % 2 * 776, number // 2 * 110
                draw.text((x, y + 2), f'{configuration}; native footer positions; text-only composition', fill='black')
                sheet.paste(panel, (x, y + 24))
                panel.save(destination / f'panel_{number}.png')
    sheet.save(destination / 'native_sheet.png')
    proof = {'status': 'pass-both-native-item-advice-descriptors-and-complete-footer-text',
             'target_arm9_sha256': sha(source), 'cases': cases,
             'visual_review': {'complete': False, 'sheet': str(destination / 'native_sheet.png')},
             'limitations': ['Option bit4 state and regular Select availability are caller input contracts; native query/setup execute.',
                             'Descriptor constructor segments pause before artwork/parent binding; CPU frame restored explicitly.',
                             'Native descriptor transfer, widths, placement, full glyphs/pixels and font cleanup execute.',
                             'Surface view/origin and physical parent/controller-button composition/input remain pending.',
                             'No new ROM or release integration.']}
    Path('work/analysis/item_advice_menus_native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Pass: 12 native item-menu states/formats, real conditional descriptors, complete footer labels and pixels/placement.')


if __name__ == '__main__':
    main()
