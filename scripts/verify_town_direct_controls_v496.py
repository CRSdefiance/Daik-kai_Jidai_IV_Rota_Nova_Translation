"""Record native-positive, live-negative town controls without release credit."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/town_dispatch_trace_v496')
PARENT = Path('out/all_routes_combined_v484_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def captured(folder, digest, frames):
    path = Path('work/emulation_v193') / folder / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == digest and report['frames'] == frames
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('synthetic_inventory_fixtures')
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    return path, report


def comparison(current, reference):
    old = {s['frame']: s for s in reference['frames_captured']}
    new = {s['frame']: s for s in current['frames_captured']}
    assert new.keys() <= old.keys()
    differences = []
    for frame, shot in new.items():
        if shot['PNG_sha256'] == old[frame]['PNG_sha256']:
            continue
        a, b = Image.open(old[frame]['path']).convert('RGB'), Image.open(shot['path']).convert('RGB')
        delta = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
        differences.append({'frame': frame, 'pixels': len(delta),
                            'bounds': [min(x for x, y in delta), min(y for x, y in delta),
                                       max(x for x, y in delta), max(y for x, y in delta)],
                            'only_stock_column': all(160 <= x < 256 and 88 <= y < 164 for x, y in delta)})
    return {'sampled_frames': len(new), 'exact_whole_frames': len(new) - len(differences),
            'different_frames': differences}


def main():
    parent = NdsImage.open(PARENT)
    source_files = files(parent)
    digest = sha(PARENT.read_bytes())
    assert digest == 'f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c'
    _, town_reference = captured('square_cells_v484', digest, 5900)
    _, fresh_reference = captured('square_cells_fresh_v484', digest, 21200)
    movie_bytes = parent.read_file('/FLS/M28.fls')
    texture = FlsArchive(movie_bytes).texture(46)
    points = [(12 + i % texture.width, 167 + i // texture.width, tuple(v >> 3 for v in texture.palette[n][:3]))
              for i, n in enumerate(texture.indices) if n]
    assert len(points) == 3047
    cases = []
    for version in (493, 494, 495):
        root = Path(f'work/analysis/town_direct_labels_v{version}')
        normal, movie = read(root / 'normal_manifest.json'), read(root / 'm28_manifest.json')
        target = files(NdsImage.open(normal['research_ROM']))
        assert source_files.keys() == target.keys()
        assert [key for key in source_files if source_files[key] != target[key]] == ['/__arm9__.bin']
        native = read(root / 'native_proof.json')
        assert len(native['all124_complete_native_masks']) == 124
        results = {}
        for label, frames, manifest in (('town', 5900, normal), ('fresh', 21200, normal), ('movie', 6000, movie)):
            path, report = captured(f'town_direct_labels_v{version}_{label}', manifest['research_ROM_sha256'], frames)
            arm = NdsImage.open(manifest['research_ROM']).read_file('/__arm9__.bin')
            assert sha(arm) == native['target_arm9_sha256']
            if label == 'movie':
                assert NdsImage.open(manifest['research_ROM']).read_file('/FLS/M20.fls') == movie_bytes
                shot = next(s for s in report['frames_captured'] if s['frame'] == 3700)
                image = Image.open(shot['path']).convert('RGB').point(lambda value: value >> 3)
                matches = sum(image.getpixel((x, y)) == rgb for x, y, rgb in points)
                assert matches == 3047
                result = {'matching_name_pixels': matches, 'normal_ending_or_unlock_not_proven': True}
            else:
                reference = town_reference if label == 'town' else fresh_reference
                assert report['core_options'] == reference['core_options']
                assert report['scripted_input_schedule'] == reference['scripted_input_schedule']
                result = comparison(report, reference)
            result.update({'report': str(path), 'report_sha256': sha(path.read_bytes())})
            results[label] = result
        assert results['town']['different_frames']
        cases.append({'version': version, 'results': results, 'live_stock_labels_missing': True,
                      'not_a_release_fix': True, 'all_non_ARM9_ROM_components_exact': True})
    manifest = read(ROOT / 'manifest.json')
    path, report = captured('town_dispatch_trace_v496', manifest['research_ROM_sha256'], 5900)
    result = comparison(report, town_reference)
    assert not result['different_frames']
    assert report['scripted_input_schedule'] == town_reference['scripted_input_schedule']
    assert report['core_options'] == town_reference['core_options']
    folder = path.parent
    itcm = (folder / 'native_state/arm9_itcm.bin').read_bytes()
    trace = itcm[0x45AC:0x4600]
    assert len(trace) == 84 and trace == bytes(84)
    arm = NdsImage.open(manifest['research_ROM']).read_file('/__arm9__.bin')
    section = MainCodeFile(arm, 0x02000000).sections[4]
    assert itcm[0x4504:0x4504 + manifest['helper_bytes']] == section.data[0x504:0x504 + manifest['helper_bytes']]
    proof = {'candidate': str(PARENT), 'candidate_sha256': digest, 'production_ROM_unchanged': True,
             'rejected_stack_prototypes': cases,
             'draw_dispatch_trace': {'report': str(path), 'report_sha256': sha(path.read_bytes()),
                                     'matching_96x12_commands': 0, 'terminal_helper_code_intact': True,
                                     'whole_frame_comparison': result,
                                     'zero_matches_does_not_prove_dispatcher_was_never_called': True},
             'actual_stock_draw_consumer_remains_unresolved': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'full_goal_complete': False}
    (ROOT / 'control_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Three stack prototypes rejected; diagnostic preserves all town frames, no matching rectangle recorded.')


if __name__ == '__main__':
    main()
