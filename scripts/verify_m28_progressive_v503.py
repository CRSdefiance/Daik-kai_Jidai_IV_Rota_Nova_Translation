"""Distinguish progressive name images rather than matching every prefix to a full name."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_m28_planes_v503 import PARENT, ROOT
from scripts.verify_fleet_release_v375 import files


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def points(texture):
    return [(i % texture.width, i // texture.width, tuple(value >> 3 for value in texture.palette[n][:3]))
            for i, n in enumerate(texture.indices) if n]


def full_match(image, pixels, origin):
    data = image.load()
    ox, oy = origin
    return all(data[x + ox, y + oy] == rgb for x, y, rgb in pixels)


def main():
    manifest = read(ROOT / 'fixture_manifest.json')
    fixture = Path(manifest['research_ROM'])
    parent = NdsImage.open(PARENT)
    current = NdsImage.open(fixture)
    assert sha(PARENT.read_bytes()) == manifest['parent_sha256']
    assert sha(fixture.read_bytes()) == manifest['research_ROM_sha256']
    before, after = files(parent), files(current)
    assert before.keys() == after.keys()
    assert [key for key in before if before[key] != after[key]] == ['/FLS/M20.fls']
    movie = parent.read_file('/FLS/M28.fls')
    assert current.read_file('/FLS/M20.fls') == movie
    archive = FlsArchive(movie)
    source = FlsArchive(NdsImage.open('work/clean.nds').read_file('/FLS/M28.fls'))
    edited = [i for i in range(len(archive.records)) if
              archive.texture(i).indices != source.texture(i).indices or archive.texture(i).palette != source.texture(i).palette]
    assert edited == [4, 5, *range(27, 47)]
    report_path = Path('work/emulation_v193/m28_planes_v503/capture_report.json')
    report = read(report_path)
    assert report['ROM_sha256'] == manifest['research_ROM_sha256']
    assert report['frames'] == 9000 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
    assert report['every_frame_capture_window'] == [3540, 3700]
    captures = {}
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        captures[shot['frame']] = shot
    images = {frame: Image.open(shot['path']).crop((0, 0, 256, 192)).convert('RGB').point(lambda v: v >> 3)
              for frame, shot in captures.items()}
    caption_cases = []
    for index, origin in ((4, (0, 48)), (5, (0, 82))):
        pixels = points(archive.texture(index))
        matches = [frame for frame, image in images.items() if full_match(image, pixels, origin)]
        assert matches, ('Unverified caption', index)
        caption_cases.append({'texture': index, 'origin': list(origin), 'nonzero_pixels': len(pixels),
                              'exact_complete_frames': matches, 'capture': captures[matches[0]]})
    groups = []
    for index in range(27, 47):
        texture = archive.texture(index)
        pixels = points(texture)
        assert all(0 <= x + 12 < 256 and 0 <= y + 167 < 192 for x, y, rgb in pixels)
        same = next((g for g in groups if g['pixels'] == pixels), None)
        if same:
            same['textures'].append(index)
        else:
            groups.append({'textures': [index], 'pixels': pixels})
    assert len(groups) == 19 and [g['textures'] for g in groups if len(g['textures']) > 1] == [[30, 31]]
    groups.sort(key=lambda g: len(g['pixels']))
    states = []
    for frame in range(3540, 3701):
        image = images[frame]
        complete = [i for i, group in enumerate(groups) if full_match(image, group['pixels'], (12, 167))]
        if complete:
            # A full name necessarily contains its earlier prefixes. Credit
            # only the largest complete distinct image observed at this frame.
            index = max(complete)
            states.append({'frame': frame, 'visual_state': index,
                           'textures_with_equivalent_pixels': groups[index]['textures'],
                           'complete_nonzero_pixels': len(groups[index]['pixels'])})
    rows, missing = [], []
    for index, group in enumerate(groups):
        frames = [s['frame'] for s in states if s['visual_state'] == index]
        row = {'textures_with_equivalent_pixels': group['textures'],
               'full_ink_and_shadow_pixels': len(group['pixels']),
               'distinct_state_frames': frames, 'origin': [12, 167],
               'not_credited_from_a_later_full_name': True}
        if frames:
            row['capture'] = captures[frames[0]]
        else:
            missing.append(group['textures'])
        rows.append(row)
    observed_order = []
    for state in states:
        if not observed_order or observed_order[-1] != state['visual_state']:
            observed_order.append(state['visual_state'])
    assert observed_order == list(range(19)), ('Unexpected reveal order', observed_order)
    proof = {'candidate': str(PARENT), 'candidate_sha256': manifest['parent_sha256'],
             'fixture_manifest': str(ROOT / 'fixture_manifest.json'),
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'edited_textures': edited, 'two_complete_caption_cases': caption_cases,
             'progressive_visual_states': rows, 'per_frame_largest_complete_state': states,
             'all19_distinct_visual_states_observed_in_original_order': True,
             'missing_distinct_visual_states': missing,
             'identical_texture30_31_pixels_do_not_identify_which_texture_was_bound': True,
             'pixel_evidence_not_direct_texture_binding_trace': True,
             'controlled_substitution_not_normal_ending_or_unlock': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'production_ROM_unchanged': True, 'full_goal_complete': False}
    (ROOT / 'progressive_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps({'complete_captions': len(caption_cases), 'distinct_progressive_states': len(rows) - len(missing),
                      'missing_states': missing, 'dense_frames': 161}))
    assert not missing, 'Remaining visual states require another targeted capture window'


if __name__ == '__main__':
    main()
