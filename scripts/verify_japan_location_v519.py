"""Verify labeled Osaka/Naha gameplay fixtures against unchanged production art."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_location_fixture_v519 import relocate
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_movie_gpu_fixtures_v336 import quantized
from scripts.verify_seoul_v516 import background, icon

ROM = Path('out/all_routes_combined_v518_candidate.nds')
OUT = Path('work/analysis/japan_location_v519')


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    digest = sha(ROM.read_bytes())
    assert digest == 'c451a11bb696c71970d7224a5194e28ec57fa406995862f9cc8e0b67711173b7'
    clean = NdsImage.open('work/clean.nds')
    font = GameAsciiFont.from_arm9(arm)
    reports, captions, backgrounds = [], [], []
    for name, town in [('osaka', 59), ('naha', 60)]:
        folder = Path('work/emulation_v193') / f'{name}_location_v519'
        report_path = folder / 'capture_report.json'
        report = json.loads(report_path.read_text())
        assert report['ROM_sha256'] == digest
        assert report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors']
        donor = report['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert donor['source_sha256'] == 'fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e'
        for frame in report['frames_captured']:
            assert sha(Path(frame['path']).read_bytes()) == frame['PNG_sha256']
        fixtures = report['synthetic_location_fixtures']
        assert len(fixtures) == 1 and not report['normal_travel_verified']
        raw = (folder / 'frame_005000_arm9_ram.bin').read_bytes()
        after, replay = relocate(arm, raw, town)
        assert fixtures[0] == dict(replay, frame=5000)
        offset = replay['active_ship'] + 0x10 - 0x02000000
        assert raw[:offset] == after[:offset] and raw[offset + 8:] == after[offset + 8:]
        reports.append({'path': str(report_path), 'sha256': sha(report_path.read_bytes()),
                        'donor_save_unchanged': True, 'fixture': fixtures[0]})
        for frame, text, origin, resource, sprite_origin in [
            (6200, 'Tavern', (56, 238), 'kbj04', (50, 192)),
            (7100, 'Inn', (63, 260), 'kbj08', (0, 240)),
        ]:
            path = folder / f'frame_{frame:06d}_navigation.png'
            image = Image.open(path).convert('RGB')
            ink, bounds = complete_mask(font, text, image, *origin, (0, 8, 0))
            resource_path = '/_pxl/' + resource + '.pxl'
            data = rom.read_file(resource_path)
            assert data == clean.read_file(resource_path)
            count = icon(image, PxlImage.from_bytes(data), *sprite_origin)
            captions.append({'town': name, 'image': str(path), 'English': text,
                             'full_glyph_and_blank_cell_mask_pixels': ink, 'bounds': bounds,
                             'complete_source_sprite_pixels': count, 'source': resource_path})
        if name == 'osaka':
            resource = '/towngrp/towngrp37.pxl'
            data = rom.read_file(resource)
            assert data == clean.read_file(resource)
            expected = quantized(PxlImage.from_bytes(data).render()).convert('RGB')
            for frame in (7400, 7800, 8800):
                path = folder / f'frame_{frame:06d}_navigation.png'
                image = Image.open(path).convert('RGB')
                actual = quantized(image.crop((0, 0, 256, 192))).convert('RGB')
                assert actual.tobytes() == expected.tobytes()
                backgrounds.append({'town': name, 'image': str(path), 'source': resource,
                                    'source_pixels_exact': 49152, 'native_origin': [0, 0],
                                    'original_story_scene_after_fixture_docking': True})
        else:
            resource = '/towngrp/towngrp47.pxl'
            data = rom.read_file(resource)
            assert data == clean.read_file(resource)
            expected = PxlImage.from_bytes(data).render()
            for frame in (6500, 7400):
                path = folder / f'frame_{frame:06d}_navigation.png'
                image = Image.open(path).convert('RGB')
                count = background(image, expected)
                backgrounds.append({'town': name, 'image': str(path), 'source': resource,
                                    'unoccluded_source_pixels_exact': count, 'native_origin': [0, 192],
                                    'portrait_nameplate_dialog_occlusions_excluded': True})
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'user_authorized_isolated_location_fixtures': True,
             'normal_travel_or_earned_unlock_not_claimed': True,
             'production_ROM_patch_and_original_donor_save_unchanged': True,
             'only_eight_active_ship_coordinate_bytes_per_fixture_permitted': True,
             'reports': reports, 'complete_alternate_signs_and_English_captions': captions,
             'actual_background_cases': backgrounds,
             'all22_original_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'location_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Osaka/Naha: four complete signs/captions, three full Osaka backgrounds and two Naha background regions pass; donor and ROM unchanged.')


if __name__ == '__main__':
    main()
