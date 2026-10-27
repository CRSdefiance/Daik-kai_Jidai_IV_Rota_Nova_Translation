"""Bounded whole-source/native M28 composition diagnostics; failures retained."""

from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_ending_transitions_v642 import compose, native_bindings
from scripts.research_photo_sampler_v630 import geometry
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opening_composition_v646')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/opening_composition_v646_actual')
ROM = Path('out/all_routes_combined_v640_candidate.nds')


def main():
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    source = rom.read_file('/FLS/M28.fls')
    assert sha(source) == pre['opening_movie_sha256']
    arm, clean_arm = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    report = read(CAP / 'capture_report.json')
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == config['frames']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['scripted_input_schedule'] and not report.get('battery_save_preloaded')
    assert not any(k.startswith('synthetic_') for k in report)
    exports = {r['frame']: r for r in report['read_only_capture_GPU_states']}
    assert set(exports) == set(config['gpu_export_frames'])
    shots = {s['frame']: s for s in report['frames_captured']}
    movie, rows, seen = FlsArchive(source), [], set()
    native_path = ROOT / 'native_bindings.json'
    natives = read(native_path) if native_path.exists() else {}
    for number, (frame, export) in enumerate(sorted(exports.items()), 1):
        assert sha(Path(export['path']).read_bytes()) == export['sha256']
        for item in export['files'].values():
            assert sha(Path(item['path']).read_bytes()) == item['sha256']
        assert export['read_only_export'] and not export['state_loaded'] and export['main_RAM_unchanged_by_export']
        raw = Path(export['files']['arm9_main_ram.bin']['path']).read_bytes()
        assert sha(raw) == export['main_RAM_sha256']
        if str(frame) not in natives:
            binding, native = native_bindings(arm, clean_arm, raw, source)
            natives[str(frame)] = {'bindings': [[a, b, i] for (a, b), i in binding.items()], 'native': native,
                                   'source_RAM_sha256': sha(raw), 'script_sha256': sha(Path(__file__).read_bytes())}
            save(native_path, natives)
        item = natives[str(frame)]
        assert item['source_RAM_sha256'] == sha(raw)
        binding = {(a, b): i for a, b, i in item['bindings']}
        seen.update(binding.values())
        polys = geometry(Path(export['files']['gpu_geometry_chunk91.bin']['path']).read_bytes())
        row = {'source_geometry_frame': frame, 'display_frame': frame + 2,
               'selected_textures': sorted(set(binding.values())), 'polygon_count': len(polys)}
        shot = shots.get(frame + 2)
        if shot is None:
            row['model_error'] = 'No independently captured display at fixed lag2'
        else:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            actual = list(Image.open(shot['path']).convert('RGB').crop((0, 0, 256, 192)).get_flattened_data())
            try:
                expected, counts = compose(polys, movie, binding)
                diff = [i for i, (a, b) in enumerate(zip(expected, actual, strict=True)) if a != b]
                row.update({'whole_upper_RGB_differences': len(diff), 'draws': counts,
                    'first_differences': [[p % 256, p // 256, expected[p], actual[p]] for p in diff[:8]]})
            except (AssertionError, ValueError, KeyError) as error:
                row['model_error'] = repr(error)
                row['polygon_attributes'] = [{'attrs': p['attributes'], 'param': p['texture_parameter'],
                    'colors': p['vertex_colors_RGB6'], 'vertices': p['vertices']} for p in polys]
        rows.append(row)
        if number % 24 == 0:
            print(number, '/', len(exports), 'native textures', len(seen), 'exact',
                  sum(r.get('whole_upper_RGB_differences') == 0 for r in rows), flush=True)
    save(ROOT / 'composition_diagnostic.json', {'cases': rows, 'native_textures_seen': sorted(seen),
        'missing_texture_bindings': sorted(set(range(movie.count)) - seen),
        'all_source_textures_count': movie.count, 'not_yet_a_passing_verification': True,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('diagnostic cases', len(rows), 'exact', sum(r.get('whole_upper_RGB_differences') == 0 for r in rows),
          'errors', sum('model_error' in r for r in rows), 'native textures', len(seen), flush=True)


if __name__ == '__main__':
    main()
