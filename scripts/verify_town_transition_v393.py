"""Resolve the bounded V349 reveal discrepancy and verify current town loading."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_commodity_layout_v346 import mask

ROOT = Path('work/analysis/town_transition_v393')
EMULATION = Path('work/emulation_v193')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def captures(folder):
    path = folder / 'capture_report.json'
    report = read(path)
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    result = {}
    for row in report['frames_captured']:
        image_path = Path(row['path'])
        assert sha(image_path.read_bytes()) == row['PNG_sha256']
        assert Image.open(image_path).size == (256, 384)
        if 'cold_boot' in image_path.name:
            result[row['frame']] = image_path
    return path, report, result


def main():
    old_path, old_report, old = captures(EMULATION / 'commodity_v349_fade_parent')
    new_path, new_report, new = captures(EMULATION / 'commodity_v349_fade_target')
    # Independent, unmodified parent captures: completed upper scenery and
    # pre-dialogue lower paper, before the later A prompt appears.
    scene_path = old_path.parent / 'frame_011600_final.png'
    paper_path = old[11396]
    scene = Image.open(scene_path).convert('RGB')
    paper = Image.open(paper_path).convert('RGB')
    phase_pixels = {f: Image.open(p).convert('RGB').tobytes() for f, p in old.items()}
    cases = []
    for frame in range(11396, 11407):
        image = Image.open(new[frame]).convert('RGB')
        unexpected = []
        for y in range(384):
            source = scene if y < 192 else paper
            for x in range(256):
                pixel = image.getpixel((x, y))
                if pixel not in ((0, 0, 0), source.getpixel((x, y))):
                    unexpected.append((x, y))
        assert not unexpected
        matches = [f for f, pixels in phase_pixels.items() if image.tobytes() == pixels]
        cases.append({'frame': frame, 'all98304_pixels_correct_source_or_black_reveal': True,
                      'exact_parent_phase_matches': matches})
    disputed = Image.open(new[11399]).convert('RGB')
    original_phase = Image.open(old[11399]).convert('RGB')
    old_delta = [(x, y) for y in range(384) for x in range(256)
             if disputed.getpixel((x, y)) != original_phase.getpixel((x, y))]
    assert len(old_delta) == 89
    assert all(144 <= x < 176 and 175 <= y < 192 for x, y in old_delta)
    assert all(disputed.getpixel(point) == scene.getpixel(point) for point in old_delta)

    a_path, a, a_frames = captures(EMULATION / 'town_transition_v393_v360')
    b_path, b, b_frames = captures(EMULATION / 'town_transition_v393_v388')
    assert a['frames'] == b['frames'] == 3400
    assert a['scripted_input_schedule'] == b['scripted_input_schedule']
    assert a['battery_save_preloaded']['source_sha256'] == b['battery_save_preloaded']['source_sha256']
    assert a['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert b['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert b['ROM_sha256'] == read(Path(b['ROM']).with_suffix('.manifest.json'))['candidate_sha256']
    assert a_frames.keys() == b_frames.keys()
    exact = []
    different = []
    for frame in a_frames:
        if a_frames[frame].read_bytes() == b_frames[frame].read_bytes():
            exact.append(frame)
        else:
            different.append(frame)
    assert different == [2851]
    earlier = Image.open(a_frames[2850]).convert('RGB')
    later = Image.open(a_frames[2852]).convert('RGB')
    mixed = Image.open(b_frames[2851]).convert('RGB')
    prior_mixed = Image.open(a_frames[2851]).convert('RGB')
    row_sources = []
    delta = []
    for y in range(384):
        current_row = [mixed.getpixel((x, y)) for x in range(256)]
        sources = [label for label, source in [('earlier', earlier), ('later', later)]
                   if current_row == [source.getpixel((x, y)) for x in range(256)]]
        assert sources, f'Unexpected transition pixel in row {y}'
        row_sources.append({'row': y, 'exact_adjacent_original_frame_sources': sources})
        delta.extend((x, y) for x in range(256)
                     if mixed.getpixel((x, y)) != prior_mixed.getpixel((x, y)))
    assert len(delta) == 1024 and {y for x, y in delta} == {87, 88, 233, 234}
    assert all(frame in b_frames for frame in range(2800, 3221))
    final_path = b_path.parent / 'frame_003400_final.png'
    final = Image.open(final_path).convert('RGB')
    arm = NdsImage.open(b['ROM']).read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    labels = [mask(final, font, text, y) for text, y in
              [('Salt', 88), ('Olive Oil', 104), ('Saffron', 120), ('Almond', 136), ('Guns', 152)]]
    assert arm[0x15BFAF:0x15BFB6] == b'Almond\0'
    proof = {'candidate': b['ROM'], 'candidate_sha256': b['ROM_sha256'],
             'old_reveal_reports': [str(old_path), str(new_path)],
             'old_reveal_report_sha256': [sha(old_path.read_bytes()), sha(new_path.read_bytes())],
             'old_fixture_ROM_sha256': [old_report['ROM_sha256'], new_report['ROM_sha256']],
             'source_scene_capture': str(scene_path), 'source_scene_sha256': sha(scene_path.read_bytes()),
             'source_paper_capture': str(paper_path), 'source_paper_sha256': sha(paper_path.read_bytes()),
             'old_dense_source_or_reveal_cases': cases,
             'disputed_frame': {'frame': 11399, 'different_pixels': len(old_delta),
                               'bounds': [144, 175, 176, 192],
                               'all_differences_are_correct_original_scene_pixels': True,
                               'native_scanline_timing_mechanism_not_proven': True},
             'current_genuine_town_reports': [str(a_path), str(b_path)],
             'current_genuine_report_sha256': [sha(a_path.read_bytes()), sha(b_path.read_bytes())],
             'current_genuine_battery_sha256': b['battery_save_preloaded']['source_sha256'],
             'current_420_dense_frames_exact_prior_integrated_release': True,
             'current_frame2851': {'changed_pixels': len(delta),
                                  'changed_rows': [87, 88, 233, 234],
                                  'all384_rows_exact_adjacent_original_frame': row_sources,
                                  'all_source_pixels_correct': True,
                                  'native_scanline_timing_mechanism_not_proven': True},
             'current_dense_frame_count': 421, 'all_current_capture_frames': sorted(b_frames),
             'exact_matching_current_capture_frames': exact,
             'final_capture': str(final_path), 'final_capture_sha256': sha(final_path.read_bytes()),
             'all_five_complete_specialty_labels': labels,
             'old_Maria_visibility_fixture_not_legitimate_unlock': True,
             'specific_old_corrupt_artwork_suspicion_resolved': True,
             'all_other_scene_transition_contexts_not_claimed': True,
             'all18_plaques_incomplete': True, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'11 old reveal frames contain only original pixels or black; disputed89 are exact scenery. '
          f'Current420 dense frames match V360; remaining frame has only adjacent original rows. '
          f'{len(exact)} total captures match exactly.')


if __name__ == '__main__':
    main()
