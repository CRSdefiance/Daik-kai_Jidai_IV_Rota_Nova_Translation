"""Independent original M26 source/native composition; retain every failed case."""

from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_wedding_fixture_v677 import ROOT
from scripts.probe_button_prompt_native import call
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_transitions_v642 import compose, native_bindings
from scripts.run_village_visits_v664 import CAP
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_ending_photo_pixels_v629 import drawing, prepare
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    folder = CAP / 'wedding_playback_v677_observed'
    report = read(folder / 'capture_report.json')
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    source = rom.read_file('/FLS/M26.fls')
    assert source == clean.read_file('/FLS/M26.fls')
    movie = FlsArchive(source)
    shots = {s['frame']: s for s in report['frames_captured']}
    exporter = sha(Path('scripts/inspect_committed_gpu_v646.py').read_bytes())
    rows, failures, prior_native = [], [], {}
    for index, state in enumerate(report['read_only_capture_GPU_states']):
        frame = state['frame']
        try:
            committed = checked_export(state, exporter)
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            assert sha(raw) == state['main_RAM_sha256']
            native, native_proof = native_bindings(arm, original, raw, source)
            bound, views = vram_bindings(committed, movie)
            retained = []
            for key, selected in bound.items():
                if key in native:
                    assert native[key] == selected
                    continue
                # Current CPU state may already have zero opacity while the
                # committed GPU list retains the final fading command. Bind its
                # complete geometry/UV/alpha to an earlier actual original draw;
                # do not inject a drawable alpha into the current source state.
                witness_frame, witness = prior_native[key]
                assert witness['original_selector_result'] == selected
                draw = witness['full_original_draw']
                attrs = [w['value'] for w in draw['GPU_writes'] if w['address'] == 0x040004A4]
                assert len(attrs) == 1
                polys = [p for p in committed['polygons'] if (p['texture_parameter'], p['palette']) == key]
                assert len(polys) == 1
                poly = polys[0]
                assert (poly['attributes'] & 0xFFFFFF) == (attrs[0] & 0xFFFFFF)
                expected_xy = [(2 * x / 4096 - 1, 1 - 2 * y / 4096) for x, y in draw['GPU_XY16']]
                expected_uv = [(u / 16, v / 16) for u, v in draw['texture_coordinates_12_4']]
                assert [(v[0], v[1]) for v in poly['vertices']] == expected_xy
                assert [(v[4], v[5]) for v in poly['vertices']] == expected_uv
                live = find_live(raw, source)
                assert live is not None
                u = prepare(arm, raw)
                call(u, 0x100390, (live['object'], witness['texture_input']))
                assert u.reg_read(UC_ARM_REG_R0) == selected
                current_draw = drawing(u, live['object'], witness['slot'])
                assert not current_draw['GPU_writes']
                retained.append({'committed_key': list(key), 'source_texture': selected,
                    'prior_actual_native_source_frame': witness_frame,
                    'full_prior_native_draw': draw,
                    'committed_XY_UV_alpha_mode_and_source_key_exact_prior_original_draw': True,
                    'isolated_draw_and_committed_polygon_ID_values_retained_separately': [attrs[0] >> 24, poly['attributes'] >> 24],
                    'current_original_selector_result': selected, 'current_original_draw': current_draw,
                    'current_native_counter': live['native_counter'],
                    'VRAM_complete_original_palette_and_indices_verified_independently': True,
                    'no_source_state_alpha_change_no_pixel_waiver_or_frame_delay_fit': True})
            for witness in native_proof.get('draws', []):
                prior_native[witness['actual_native_texture_parameter'], witness['actual_native_palette']] = (frame, witness)
            ordered, order = render_order(committed)
            expected, draws = compose(ordered, movie, bound)
            checks = []
            for lag in range(4):
                shot = shots[frame + lag]
                assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
                actual = list(Image.open(shot['path']).convert('RGB').crop((0, 0, 256, 192)).get_flattened_data())
                checks.append({'lag': lag, 'RGB_differences': sum(a != b for a, b in zip(expected, actual, strict=True))})
            row = {'frame': frame, 'native': native_proof, 'source_views': views, 'draws': draws,
                   'separate_retained_committed_commands': retained,
                   'render_order': order, 'comparisons': checks,
                   'committed': {'path': committed['path'], 'sha256': committed['sha256']}}
            rows.append(row)
        except (AssertionError, ValueError, KeyError) as exc:
            failures.append({'frame': frame, 'error': repr(exc)})
            print('V677 unresolved', frame, repr(exc), flush=True)
        save(ROOT / 'composition_research.json', {'rows': rows, 'failures': failures,
            'not_final_verification': True, 'script_sha256': sha(Path(__file__).read_bytes())})
        if index % 16 == 0:
            print('V677 compositions', index + 1, 'rows', len(rows), 'failures', len(failures), flush=True)
    passing_lags = [lag for lag in range(4) if all(next(c['RGB_differences'] for c in r['comparisons'] if c['lag'] == lag) == 0 for r in rows)]
    print('V677 complete source compositions', len(rows), 'failures', len(failures), 'global passing lags', passing_lags, flush=True)


if __name__ == '__main__':
    main()
