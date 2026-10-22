"""Current ordinary route movies: source RGB diagnostics with all failures kept."""

from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/route_opening_movies_v647')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    pre, configs = read(ROOT / 'preflight.json'), read(ROOT / 'run_configs.json')
    rom = NdsImage.open(pre['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    exporter_sha = sha((ROOT / 'executed_committed_exporter_source.py').read_bytes())
    results = {}
    for label, config in configs.items():
        folder = CAP / ('route_opening_movies_v647_' + label)
        report = read(folder / 'capture_report.json')
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == config['frames']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == read(config['inputs'])
        assert not report.get('battery_save_preloaded') and not any(k.startswith('synthetic_') for k in report)
        assert {r['frame'] for r in report['read_only_capture_GPU_states']} == set(config['gpu_export_frames'])
        source = rom.read_file(config['movie'])
        movie, cases, failures, seen = FlsArchive(source), [], [], set()
        shots = {s['frame']: s for s in report['frames_captured']}
        for number, state in enumerate(report['read_only_capture_GPU_states'], 1):
            frame = state['frame']
            committed = checked_export(state, exporter_sha)
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            u = machine(arm)
            u.mem_write(BASE, raw)
            call(u, 0x7F244, ())
            assert u.reg_read(UC_ARM_REG_R0) == config['captain']
            try:
                live = find_live(raw, source)
                assert live is not None, 'Expected original route movie controller absent'
                bindings, resources = vram_bindings(committed, movie)
                ordered, order = render_order(committed)
                expected, draws = compose(ordered, movie, bindings)
                shot = shots[frame + 1]
                assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
                actual = list(Image.open(shot['path']).convert('RGB').crop((0, 0, 256, 192)).get_flattened_data())
                diff = sum(a != b for a, b in zip(expected, actual, strict=True))
                if diff:
                    failures.append({'frame': frame, 'RGB_differences': diff})
                for resource in resources:
                    seen.update(resource['source_equivalence_candidates'])
                cases.append({'source_frame': frame, 'display_frame': frame + 1,
                    'movie_controller': live, 'whole_upper_RGB_differences': diff,
                    'source_VRAM_resources': resources, 'draws': draws, 'render_order': order,
                    'committed_path': committed['path'], 'committed_sha256': committed['sha256']})
            except (AssertionError, ValueError, KeyError) as error:
                failures.append({'frame': frame, 'model_error': repr(error)})
                print(label, 'unresolved', frame, repr(error), flush=True)
            if number % 12 == 0:
                print(label, number, 'cases', len(cases), 'failures', len(failures), flush=True)
        results[label] = {'movie': config['movie'], 'source_texture_count': movie.count,
            'source_candidates_seen': sorted(seen), 'missing_source_candidates': sorted(set(range(movie.count)) - seen),
            'cases': cases, 'failures': failures}
        save(ROOT / 'composition_diagnostic.json', {'routes': results, 'not_yet_final_verification': True})
        print(label, 'finished', len(cases), 'failures', len(failures), 'source views', len(seen), '/', movie.count, flush=True)


if __name__ == '__main__':
    main()
