"""Actual emulator GPU source-pixel checks in labeled substituted-movie fixtures."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_movie_gpu_fixture_v336 import PARENT, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def quantized(image):
    return image.convert('RGB').point(lambda value: value >> 3)


def plane_locations(texture, image):
    points = [(i % texture.width, i // texture.width,
               tuple(value >> 3 for value in texture.palette[index][:3]))
              for i, index in enumerate(texture.indices) if index]
    anchor = next(p for p in points if max(p[2]) == max(max(v[2]) for v in points))
    minimum_x, maximum_x = min(p[0] for p in points), max(p[0] for p in points)
    minimum_y, maximum_y = min(p[1] for p in points), max(p[1] for p in points)
    pixels = image.load()
    samples = points[::max(1, len(points) // 32)]
    for y in range(anchor[1] - minimum_y, 192 - maximum_y + anchor[1]):
        for x in range(anchor[0] - minimum_x, 256 - maximum_x + anchor[0]):
            if pixels[x, y] != anchor[2]:
                continue
            ox, oy = x - anchor[0], y - anchor[1]
            if (all(pixels[px + ox, py + oy] == value for px, py, value in samples)
                    and all(pixels[px + ox, py + oy] == value for px, py, value in points)):
                yield {'origin': [ox, oy], 'full_nonzero_source_pixels': len(points),
                       'leading_internal_trailing_ink_and_source_shadows_included': True}


def main():
    parent = NdsImage.open(PARENT)
    digest = sha(PARENT.read_bytes())
    rows = []
    for number in (28, 29, 30, 31, 32):
        label = f'm{number}'
        manifest = read(ROOT / f'{label}_fixture_manifest.json')
        folder = Path(f'work/emulation_v193/movie_gpu_fixture_v336_{label}')
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        assert manifest['parent_sha256'] == digest
        assert manifest['research_only'] and manifest['not_registered_playable_or_distribution_candidate']
        assert sha(Path(manifest['research_ROM']).read_bytes()) == report['ROM_sha256'] == manifest['research_ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == (11000 if number == 28 else 12500)
        assert report['scripted_input_schedule'] == read(ROOT / 'opening_inputs.json')
        assert all(e['start'] <= 2200 for e in report['scripted_input_schedule'])
        archive = FlsArchive(parent.read_file(f'/FLS/M{number}.fls'))
        frames = []
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            if 2400 <= shot['frame'] <= 10500:
                frames.append((shot, quantized(Image.open(shot['path']).crop((0, 0, 256, 192)))))
        matches = []
        if number != 28:
            references = {i: quantized(archive.texture(i).render().crop((0, 0, 256, 192))).tobytes()
                          for i in range(1, len(archive.records))
                          if archive.texture(i).width >= 256 and archive.texture(i).height >= 192}
            for shot, image in frames:
                actual = image.tobytes()
                for index, expected in references.items():
                    if actual == expected:
                        matches.append({'frame': shot['frame'], 'texture': index, 'whole_upper_screen_source_exact_pixels': 49152})
            assert matches, f'No full opaque scene match for {label}'
        else:
            texture = archive.texture(46)
            for shot, image in frames:
                for matched in plane_locations(texture, image):
                    matches.append({'frame': shot['frame'], 'texture': 46,
                                    'English': 'Hodram Joakim Bergstrom', **matched})
            assert matches, 'No complete GPU Hodram name plane match'
        rows.append({'movie': f'/FLS/M{number}.fls', 'capture_report': str(report_path),
                     'capture_report_sha256': sha(report_path.read_bytes()), 'fixture_manifest': str(ROOT / f'{label}_fixture_manifest.json'),
                     'actual_original_emulator_GPU_matches': matches,
                     'substituted_opening_input_path_not_legitimate_ending_unlock_or_caller_proof': True})
    proof = {'production_candidate_unchanged': str(PARENT), 'candidate_sha256': digest,
             'research_only_exact_movie_file_substitutions': 5, 'cases': rows,
             'actual_emulator_GPU_used_not_custom_pixel_renderer': True,
             'source_quantized_photos_and_full_name_ink_shadows_match': True,
             'normal_caller_unlock_story_endings_complete_movie_pixel_alpha_timing_hardware_still_open': True,
             'all18_plaques_and_variants_still_incomplete': True,
             'Online_low_resolution_images_exempt': True, 'ROM_modified': False,
             'full_goal_complete': False, 'documentation': 'docs/movie_gpu_fixture_v336.md'}
    path = ROOT / 'GPU_pixel_proof.json'
    path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / filename
        audit = read(target)
        assert audit['latest_candidate_sha256'] == digest
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['actual_controlled_movie_GPU_v336'] = {**proof, 'proof': str(path)}
        audit['current_goal_turn_classification'] = 'progress-actual-GPU-substituted-movie-captures-and-complete-source-pixel-matches'
        target.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'movies': len(rows), 'source_pixel_matches': [len(r['actual_original_emulator_GPU_matches']) for r in rows],
                      'production_ROM_unchanged': True, 'legitimate_ending_gameplay_verified': False}))


if __name__ == '__main__':
    main()
