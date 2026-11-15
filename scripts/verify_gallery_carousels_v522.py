"""Verify every original Gallery carousel image and complete live text field."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_gallery_hodram_v521 import compact_caption
from scripts.verify_movie_gpu_fixtures_v336 import quantized

ROM = Path('out/all_routes_combined_v518_candidate.nds')
OUT = Path('work/analysis/gallery_v522')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/gallery_all_v522')
BASE = 0x02000000


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rom', type=Path, default=ROM)
    parser.add_argument('--capture', type=Path, default=CAPTURE)
    parser.add_argument('--output', type=Path, default=OUT / 'all_carousels_proof.json')
    parser.add_argument('--fixture-manifest', type=Path, default=Path('work/analysis/gallery_v521/save_fixture_manifest.json'))
    args = parser.parse_args()
    plan = read(OUT / 'run_plan.json')
    digest = sha(args.rom.read_bytes())
    assert read(args.rom.with_suffix('.manifest.json'))['candidate_sha256'] == digest
    current, clean = NdsImage.open(args.rom), NdsImage.open('work/clean.nds')
    arm, source = [r.read_file('/__arm9__.bin') for r in (current, clean)]
    restored = bytearray(arm)
    for offset, a, b in [(0x42FDC, 0xE3A0C006, 0xE3A0C005), (0x42FF0, 0xE58D6004, 0xE58D5004)]:
        assert struct.unpack_from('<I', source, offset)[0] == a
        assert struct.unpack_from('<I', arm, offset)[0] == b
        restored[offset:offset + 4] = source[offset:offset + 4]
    assert restored[0x42E5C:0x4300C] == source[0x42E5C:0x4300C]
    report_path = args.capture / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == plan['final_frame'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == read(OUT / 'inputs.json')
    assert len(report['synthetic_gallery_fixtures']) == 1 and not report['earned_unlock_verified']
    fixture = read(args.fixture_manifest)
    assert fixture['production_ROM_sha256'] == digest
    assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
    assert sha(Path(fixture['fixture_save']).read_bytes()) == fixture['fixture_save_sha256']
    assert report['battery_save_preloaded']['source_sha256'] == fixture['fixture_save_sha256']
    captures = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        captures[row['frame']] = row
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']:
        assert row['read_only_export'] and row['bytes'] == 0x400000
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        snapshots[row['frame']] = row
    assert set(snapshots) == set(plan['capture_frames'])
    font, original_u = GameAsciiFont.from_arm9(arm), machine(source)
    popup = Image.open(captures[2400]['path']).convert('RGB')
    menu = []
    for text, x, y in [('Items', 113, 252), ('Ruins', 113, 272),
                       ('Characters', 98, 292), ('Event Scenes', 92, 312)]:
        ink, bounds = complete_mask(font, text, popup, x, y, (8, 8, 8))
        menu.append({'English': text, 'complete_ink_pixels': ink, 'bounds': bounds})
    expected_images = {}
    routes = []
    description_table = struct.unpack_from('<I', arm, 0x43304)[0]
    for route, literal in zip(plan['routes'], (0x432DC, 0x432E4, 0x432EC, 0x432F4), strict=True):
        image_table, caption_table = struct.unpack_from('<2I', arm, literal)
        count = route['count']
        indices = struct.unpack_from(f'<{count}I', arm, image_table - BASE)
        assert arm[image_table - BASE:image_table - BASE + count * 4] == source[
            image_table - BASE:image_table - BASE + count * 4]
        # Maria was already selected in the parent menu: this capture sequence
        # begins at1 and still traverses all38 positions, ending at0.
        start_position = 1 if route['route'] == 3 else 0
        visited = set()
        cases = []
        for capture_number, frame in enumerate(route['frames']):
            position = (capture_number + start_position) % count
            visited.add(position)
            index = indices[position]
            image_path = Path(captures[frame]['path'])
            image = Image.open(image_path).convert('RGB')
            raw = Path(snapshots[frame]['path']).read_bytes()
            assert struct.unpack_from('<H', raw, 0x27985C)[0] & 15 == 15
            resource = f'/evstill/evstill{index:03d}.pxl'
            if resource not in expected_images:
                expected_images[resource] = quantized(PxlImage.from_bytes(current.read_file(resource)).render()).convert('RGB').tobytes()
            assert quantized(image.crop((0, 0, 256, 192))).convert('RGB').tobytes() == expected_images[resource], (route['captain'], position, resource)
            pointer = struct.unpack_from('<I', arm, caption_table - BASE + position * 4)[0]
            assert struct.unpack_from('<I', raw, caption_table - BASE + position * 4)[0] == pointer
            assert BASE <= pointer < BASE + len(raw) - 256
            text = raw[pointer - BASE:pointer - BASE + 256].split(b'\0')[0].decode('ascii')
            source_pointer = struct.unpack_from('<I', source, caption_table - BASE + position * 4)[0]
            japanese = bytes(original_u.mem_read(source_pointer, 256)).split(b'\0')[0].decode('cp932')
            caption = compact_caption(font, text, image)
            heading_ink, heading_bounds = complete_mask(font, 'Event Scenes', image, 92, 194, (230, 230, 230))
            description_pointer = struct.unpack_from('<I', raw, description_table - BASE + route['route'] * 4)[0]
            assert BASE <= description_pointer < BASE + len(raw) - 128
            description = raw[description_pointer - BASE:description_pointer - BASE + 128].split(b'\0')[0].decode('ascii')
            assert description.strip() == f"Memorable scenes from {route['captain']}'s story."
            description_ink, description_bounds = complete_mask(font, description, image, 8, 212, (230, 230, 230))
            cases.append({'position': position, 'image': str(image_path), 'source': resource,
                          'all49152_native_screen_pixels_exact': True,
                          'caption': dict(caption, Japanese=japanese, native_pointer=pointer),
                          'heading': {'complete_ink_pixels': heading_ink, 'bounds': heading_bounds},
                          'description': {'English': description, 'complete_ink_pixels': description_ink,
                                          'bounds': description_bounds, 'runtime_pointer': description_pointer}})
        assert visited == set(range(count))
        wrapped = Image.open(captures[route['wrap_frame']]['path']).convert('RGB')
        first = Image.open(captures[route['frames'][0]]['path']).convert('RGB')
        assert first.crop((0, 0, 256, 192)).tobytes() == wrapped.crop((0, 0, 256, 192)).tobytes()
        compact_caption(font, cases[0]['caption']['English'], wrapped)
        for y in range(384):
            for x in range(256):
                if 256 <= y < 278 and (16 <= x < 32 or 224 <= x < 240):
                    continue
                assert first.getpixel((x, y)) == wrapped.getpixel((x, y)), (route['captain'], x, y)
        routes.append({'captain': route['captain'], 'route': route['route'], 'count': count,
                       'actual_start_position': start_position,
                       'all_original_table_positions_visited_once': True,
                       'cases': cases, 'wrap_frame': route['wrap_frame'],
                       'wrapped_image_caption_and_surroundings_exact_except_original_arrow_visibility': True})
    assert sum(r['count'] for r in routes) == 164
    requirements = read('translations/graphics_completion_requirements_v313.json')
    campaign = read('translations/graphics_completion_campaign_v1.json')
    assert len(requirements['historical_pending_items_retained']) == 22
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
    proof = {'candidate': str(args.rom), 'candidate_sha256': digest,
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'plan': str(OUT / 'run_plan.json'), 'complete_Gallery_popup_labels': menu,
             'all164_original_Gallery_positions_and_four_wraps': routes,
             'distinct_source_images': len(expected_images), 'full_source_pixel_comparisons': 164 * 49152,
             'all164_captions_headings_and_route_descriptions_complete': True,
             'captions_verified_from_each_actual_capture_RAM_snapshot': True,
             'captured_production_ROM_and_original_donor_save_unchanged_during_testing': True,
             'authorized_isolated_Gallery_save_fixture': True,
             'earned_unlock_normal_ending_movie_playback_and_Characters_gallery_not_claimed': True,
             'other_original_graphics_restoration_and_native_consumer_gates_remain': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All164 Gallery images, captions, headings and descriptions plus four wraps pass; per-frame runtime pointers and donor preserved.')


if __name__ == '__main__':
    main()
