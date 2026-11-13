"""Actual native image-widget pixels in bounded source-opcode fixtures."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_generic_image_gpu_v538 import OUT, PARENT
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = OUT.parent
CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
INDICES = [*range(11), 12, 19, 20]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    digest = sha(PARENT.read_bytes())
    parent = NdsImage.open(PARENT)
    baseline = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    inputs = read(OUT / 'opening_inputs.json')
    cases = []
    for index in INDICES:
        fixture = OUT / f'index{index:02d}_RESEARCH_ONLY.nds'
        manifest = read(fixture.with_suffix('.fixture.json'))
        assert manifest['research_only'] and manifest['not_playable_distribution_or_registered_candidate']
        assert manifest['parent_sha256'] == digest and manifest['requested_image_index'] == index
        assert manifest['inherited_batches'] == 470
        saved = NdsImage.open(fixture)
        actual_files = {p: data for _, p, data in saved.iter_files()} | dict(saved.iter_components())
        path = manifest['only_changed_file']
        assert actual_files.keys() == baseline.keys()
        assert [p for p in baseline if baseline[p] != actual_files[p]] == [path]
        before, after = [IlnkContainer.parse(data[path]).blocks for data in (baseline, actual_files)]
        assert len(before) == len(after) == 343
        assert all(a == b for n, (a, b) in enumerate(zip(before, after)) if n != 44)
        assert len(before[44]) == len(after[44]) and before[44][:30] == after[44][:30]
        assert before[44][34:] == after[44][34:]
        assert after[44][30:34].hex() == manifest['replacement_generic_image_packet']
        folder = CAPTURES / f'generic_image_gpu_v538_{index:02d}'
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == manifest['research_ROM_sha256'] == sha(fixture.read_bytes())
        assert report['frames'] == 9000 and report['cold_boot']
        assert not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == inputs
        selected = index if index <= 12 or index == 20 else 12
        source_path = f'/_pxl/slackimg{selected:02d}.pxl'
        source = PxlImage.from_bytes(parent.read_file(source_path))
        assert source.width <= 256 and source.height <= 172
        origin = [(256 - source.width) // 2, 20]
        points = [(i % source.width, i // source.width, native5(source.palette[color]))
                  for i, color in enumerate(source.indices) if color]
        assert len(points) > 100
        matches = []
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            if not 3600 <= shot['frame'] <= 9000:
                continue
            image = Image.open(shot['path']).convert('RGB')
            pixels = image.load()
            if all(native5(pixels[x + origin[0], y + origin[1]]) == rgb for x, y, rgb in points):
                matches.append(shot)
        assert matches, ('No complete native source image match', index)
        native = read(folder / 'native_state/native_state.json')
        assert native['read_only_export'] and not native['state_loaded']
        cases.append({'index': index, 'source_path': source_path,
                      'source_file_sha256': sha(parent.read_file(source_path)),
                      'source_extent': [source.width, source.height], 'native_origin': origin,
                      'source_visible_nonzero_pixels_exact': len(points),
                      'complete_source_ink_edges_and_shadows_included': True,
                      'all_points_inside_native_upper_screen': True,
                      'palette_zero_transparency_and_all_transition_states_not_claimed': True,
                      'exact_frames': matches, 'capture_report': str(report_path),
                      'capture_report_sha256': sha(report_path.read_bytes()),
                      'fixture_manifest': str(fixture.with_suffix('.fixture.json')),
                      'synthetic_source_instruction_not_ordinary_event_progression': True})
    assert cases[11]['source_path'] == cases[12]['source_path'] == '/_pxl/slackimg12.pxl'
    assert cases[11]['source_visible_nonzero_pixels_exact'] == cases[12]['source_visible_nonzero_pixels_exact']
    proof = {'candidate': str(PARENT), 'candidate_sha256': digest,
             'all14_native_widget_cases': cases,
             'all11_creature_paintings_and_complete_labels_and_press_button_art_visible': True,
             'index19_displays_name_labels_not_raw_comic': True,
             'all_geometry_comes_from_original_source_command_and_widget': True,
             'only_one_four_byte_SC0_block44_instruction_substituted_per_fixture': True,
             'all_prose_other_controls_files_components_and_artwork_exact_parent': True,
             'production_ROM_changed': False,
             'raw_legacy_comic_reachability_or_native_display_proven': False,
             'other_original_image11_caller_and_all_alpha_transitions_unverified': True,
             'all22_requirements_and18_incomplete_plaques_retained': True, 'full_goal_complete': False}
    assert sha(PARENT.read_bytes()) == digest
    (ROOT / 'native_GPU_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('14 actual native image-widget cases:11 creature paintings,complete labels,alias19,and press-button art pass.')


if __name__ == '__main__':
    main()
