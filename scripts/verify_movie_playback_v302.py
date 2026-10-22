"""Full opaque subtitle texture pixels in unskipped production movie captures."""

import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/movie_playback_v302')
ROM = Path('out/all_routes_combined_v299_candidate.nds')
DIGEST = '9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f'
CARDS = [('/FLS/M20.fls', 27, 'rafael', ['What is it, Clau?', 'What did you want to show?']),
         ('/FLS/M22.fls', 1, 'lil', ["Hey, don't!", "It's too dangerous!"]),
         ('/FLS/M22.fls', 2, 'lil', ["It's fine, it's fine.", 'Leave it to me!']),
         ('/FLS/M24.fls', 3, 'hodram_confirmed', ["The ship's here!", 'Report to the captain!']),
         ('/FLS/M24.fls', 4, 'hodram_confirmed', ['A foreign merchant ship!', 'Admiral, your orders?'])]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def locations(texture, pixels):
    points = [(i % texture.width, i // texture.width, texture.palette[n][:3])
              for i, n in enumerate(texture.indices) if n]
    anchor = next(p for p in points if p[2] == (255, 255, 255))
    minimum_x, maximum_x = min(x for x, _, _ in points), max(x for x, _, _ in points)
    minimum_y, maximum_y = min(y for _, y, _ in points), max(y for _, y, _ in points)
    results = []
    for y in range(anchor[1] - minimum_y, 192 - maximum_y + anchor[1]):
        for x in range(anchor[0] - minimum_x, 256 - maximum_x + anchor[0]):
            if pixels[x, y] != anchor[2]:
                continue
            ox, oy = x - anchor[0], y - anchor[1]
            # Several distinctive anchors cheaply reject ordinary bright scenery.
            samples = points[::max(1, len(points) // 32)]
            if not all(pixels[sx + ox, sy + oy] == color for sx, sy, color in samples):
                continue
            if all(pixels[sx + ox, sy + oy] == color for sx, sy, color in points):
                results.append((ox, oy))
    return results


def main(*, rom=ROM, root=ROOT, digest=DIGEST, capture_prefix='movie_playback_v302', cards=CARDS):
    assert sha(rom.read_bytes()) == digest
    current, clean = NdsImage.open(rom), NdsImage.open('work/clean.nds')
    reports, frames, dependencies = {}, {}, {}
    for name, limit, inputs in [('rafael', 6000, 'rafael_start_inputs.json'),
                               ('lil', 6000, 'lil_start_inputs.json'),
                               ('hodram_confirmed', 7000, 'hodram_confirmed_inputs.json')]:
        path = Path(f'work/emulation_v193/{capture_prefix}_{name}/capture_report.json')
        report = read(path)
        assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and report['frames'] == limit
        assert report['scripted_input_schedule'] == read(root / inputs)
        assert all(e['start'] <= (2500 if name == 'hodram_confirmed' else 2200) for e in report['scripted_input_schedule'])
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            if 2200 <= row['frame'] <= 5000 and 'cold_boot' in row['path']:
                frames.setdefault(name, []).append((row, Image.open(row['path']).convert('RGB')))
        reports[name], dependencies[str(path)] = report, sha(path.read_bytes())
    matches, missing, pictures = [], [], []
    for path, index, name, english in cards:
        archive = FlsArchive(current.read_file(path))
        texture = archive.texture(index)
        source = FlsArchive(clean.read_file(path)).texture(index)
        assert (texture.flags, texture.width, texture.height, texture.palette) == (source.flags, source.width, source.height, source.palette)
        count = Counter(texture.indices)
        assert set(count) == {0, 1, 2} and texture.palette[1][:3] == (255, 255, 255) and texture.palette[2][:3] == (0, 0, 0)
        found = []
        for row, image in frames[name]:
            for ox, oy in locations(texture, image.load()):
                visible = archive.records[index][0] >> 16
                active = [(i % texture.width, i // texture.width) for i, value in enumerate(texture.indices) if value]
                assert all(x < visible for x, _ in active)
                transparent_nonblack = sum(image.getpixel((ox + x, oy + y)) != (0, 0, 0)
                                           for y in range(texture.height) for x in range(visible)
                                           if texture.indices[y * texture.width + x] == 0 and 0 <= ox + x < 256 and 0 <= oy + y < 192)
                assert transparent_nonblack > 500
                found.append({'frame': row['frame'], 'capture': row['path'], 'capture_sha256': row['PNG_sha256'],
                              'source_texture_origin': [ox, oy], 'complete_white_fill_pixels': count[1],
                              'complete_opaque_black_outline_pixels': count[2],
                              'transparent_source_positions_showing_nonblack_artwork': transparent_nonblack,
                              'every_opaque_first_internal_final_letter_and_outline_pixel_exact': True})
                if len(found) == 1:
                    pictures.append((path + ' #' + str(index), image))
        case = {'file_path': path, 'texture_index': index, 'English': english, 'matches': found,
                'source_dimensions_palette_flags_preserved': True,
                'source_texture_sha256': sha(bytes(texture.indices)), 'source_opaque_pixels': count[1] + count[2]}
        matches.append(case)
        if not found:
            missing.append([path, index])
    # Inspect all exact subtitle copies, including the large introductory movie.
    sources = {(p, i): FlsArchive(clean.read_file(p)).texture(i) for p, i, _, _ in cards}
    copy_cases, textures = [], 0
    for _, path, raw in clean.iter_files():
        if not path.lower().endswith('.fls'):
            continue
        before, after = FlsArchive(raw), FlsArchive(current.read_file(path))
        assert before.count == after.count
        for index in range(before.count):
            t = before.texture(index)
            textures += 1
            for owner, s in sources.items():
                if (t.width, t.height, t.palette, bytes(t.indices)) == (s.width, s.height, s.palette, bytes(s.indices)):
                    now = after.texture(index)
                    assert bytes(now.indices) != bytes(t.indices)
                    copy_cases.append({'source_card': list(owner), 'path': path, 'texture': index,
                                       'exact_Japanese_source_copy_is_localized': True})
    preview = Image.new('RGB', (256 * 3, 408 * 2), '#333333')
    draw = ImageDraw.Draw(preview)
    for n, (label, image) in enumerate(pictures):
        x, y = n % 3 * 256, n // 3 * 408
        draw.text((x + 3, y + 3), label, fill='white')
        preview.paste(image, (x, y + 24))
    preview.save(root / 'movie_subtitle_review.png')
    proof = {'format': 'dk4-current-actual-movie-subtitle-playback-v302', 'candidate': str(rom), 'candidate_sha256': digest,
             'cards': matches, 'missing_actual_cards': missing, 'all_five_actual_subtitles_full_pixels_verified': not missing,
             'capture_report_dependencies': dependencies, 'complete_clean_FLS_textures_scanned_for_exact_subtitle_copies': textures,
             'source_subtitle_copy_cases': copy_cases,
             'rotated_scaled_compressed_or_approximate_copy_equivalence_not_claimed': True,
             'three_production_cold_boots_ordinary_start_inputs_no_skips_savestates_or_RAM_injection': True,
             'first_Hodram_run_stayed_at_confirmation_not_playback_evidence': 'work/emulation_v193/movie_playback_v302_hodram/capture_report.json',
             'native_movie_command_source_candidates': [{'path': '/data/SC0.DK4', 'block': 44, 'offset': 26, 'word': '4900', 'FLS_index': 20},
                                                        {'path': '/data/SC2.DK4', 'block': 22, 'offset': 18, 'word': '4902', 'FLS_index': 22},
                                                        {'path': '/data/SC1.DK4', 'block': 42, 'offset': 36, 'word': '4904', 'FLS_index': 24}],
             'all11_legacy_native_layout_and_raw_comic_display_gates_remain_open': True,
             'all18_plaque_hint_entries_remain_incomplete': True, 'ROM_modified': False, 'full_goal_complete': False}
    (root / 'proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{sum(bool(r["matches"]) for r in matches)}/5 actual cards; {textures} FLS textures checked; missing {missing}.', flush=True)
    assert not missing


if __name__ == '__main__':
    main()
