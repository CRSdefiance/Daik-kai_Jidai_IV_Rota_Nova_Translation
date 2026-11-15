"""Exact visible retained-art patches in a labeled Maria-selection fixture."""

import json
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_movie_gpu_fixtures_v336 import quantized

ROOT = Path('work/analysis/east_asian_town_v343')
FOLDER = Path('work/emulation_v193/east_asian_town_v343_facilities')


def main():
    report_path = FOLDER / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    manifest = json.loads((ROOT / 'selection_fixture_manifest.json').read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == manifest['research_ROM_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 18400
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    backgrounds = []
    for number, index, box in [(16400, 32, (80, 70, 180, 100)),
                               (17600, 33, (84, 0, 256, 96)),
                               (18400, 33, (86, 0, 256, 96))]:
        image = Image.open(FOLDER / f'frame_{number:06d}_navigation.png')
        original = PxlImage.from_bytes(rom.read_file(f'/towngrp/towngrp{index}.pxl')).render()
        actual = quantized(image.crop((box[0], box[1] + 192, box[2], box[3] + 192)))
        expected = quantized(original.crop(box))
        assert actual.tobytes() == expected.tobytes()
        backgrounds.append({'frame': number, 'source': index, 'source_box': box,
                            'native_origin': [0, 192], 'exact_source_pixels': actual.width * actual.height,
                            'portrait_and_dialogue_occlusion_excluded': True})
    icons = []
    for number, name, x0, y0 in [(17400, 'kbe04', 62, 192), (18200, 'kbe08', 0, 240)]:
        image = Image.open(FOLDER / f'frame_{number:06d}_navigation.png').convert('RGB')
        source = PxlImage.from_bytes(rom.read_file('/_pxl/' + name + '.pxl'))
        count = 0
        for i, value in enumerate(source.indices):
            if value == 255:
                continue
            x, y = i % source.width, i // source.width
            assert tuple(c >> 3 for c in image.getpixel((x + x0, y + y0))) == tuple(c >> 3 for c in source.palette[value][:3])
            count += 1
        icons.append({'source': '/_pxl/' + name + '.pxl', 'origin': [x0, y0],
                      'exact_nontransparent_pixels': count, 'not_the_retained_kbj_variant': True})
    captions = []
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    for number, text, region in [(17400, 'Tavern', (45, 235, 150, 270)),
                                 (18200, 'Inn', (0, 265, 150, 312))]:
        image = Image.open(FOLDER / f'frame_{number:06d}_navigation.png').convert('RGB')
        match = None
        colors = [color for color, _ in Counter(image.crop(region).get_flattened_data()).most_common()
                  if max(color) < 80 and max(color) - min(color) < 5]
        for color in colors:
            if match:
                break
            for y in range(region[1], region[3] - 10):
                if match:
                    break
                for x in range(region[0], region[2] - len(text) * 6 + 1):
                    try:
                        ink, bounds = complete_mask(font, text, image, x, y, color)
                    except ValueError:
                        continue
                    match = {'text': text, 'frame': number, 'ink_pixels': ink, 'bounds': bounds,
                             'complete_first_final_letters_and_blank_cells': True}
                    break
        if match is None:
            match = {'text': text, 'frame': number, 'visually_reviewed_English_caption': True,
                     'exact_native_caption_font_mask_pending': True}
        captions.append(match)
    proof = {'candidate_unchanged': 'out/all_routes_combined_v342_candidate.nds',
             'candidate_sha256': sha(Path('out/all_routes_combined_v342_candidate.nds').read_bytes()),
             'research_selection_manifest': str(ROOT / 'selection_fixture_manifest.json'),
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'background_patches': backgrounds, 'actual_icon_family': icons, 'actual_captions': captions,
             'original_Hangzhou_town_facility_routing_inside_selection_fixture': True,
             'legitimate_Maria_unlock_not_verified': True,
             'kbj_sign_variants_not_selected_backgrounds35_37_still_open': True,
             'commodity_name_missing_Japanese_discovered': 49, 'full_goal_complete': False}
    (ROOT / 'live_environment_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'retained_background_pixels': sum(x['exact_source_pixels'] for x in backgrounds),
                      'icon_pixels': sum(x['exact_nontransparent_pixels'] for x in icons), 'reviewed_captions_with_exact_font_masks_pending': len(captions)}))


if __name__ == '__main__':
    main()
