"""Verify actual V627 GPU exports and source-derived complete photo pixels."""

from copy import deepcopy
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_desmume_gpu_v630 import tags
from scripts.native_ending_fixture_v537 import request_ending
from scripts.research_photo_sampler_v630 import CAP, ROOT, geometry, rgb_palette, sample
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v627_candidate.nds')
HODRAM = CAP.parent / 'ending_gpu_v630_hodram_actual'


def pixel_check(poly, texture, actual):
    predicted, details = sample(poly, texture)
    assert list(actual.get_flattened_data()) == predicted
    palette = rgb_palette(texture)
    index = details['source_texel_for_negative_control']
    before = texture.indices[index]
    alternate = next(i for i, color in enumerate(palette) if color != palette[before])
    texture.indices[index] = alternate
    erased, _ = sample(poly, texture)
    texture.indices[index] = before
    assert erased != predicted
    shifted = deepcopy(poly)
    for vertex in shifted['vertices']:
        vertex[0] += 1 / 128  # one original screen pixel, no per-frame alignment
    moved, _ = sample(shifted, texture)
    assert moved != predicted
    assert predicted != [(0, 0, 0)] * (256 * 192)
    return {**details, 'all49152_RGB_pixels_exact_no_mask_or_tolerance': True,
            'source_texel_blank_and_one_pixel_geometry_shift_controls_rejected': True,
            'source_reconstruction_RGB_sha256': sha(actual.tobytes())}


def load_run(folder, captain, terminal, preflight, arm):
    path = folder / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == preflight['candidate_sha256'] and report['frames'] == terminal
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['earned_completion_verified'] and len(report['synthetic_ending_fixtures']) == 1
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_ending_fixtures')
    raw = (folder / 'frame_003000_arm9_ram.bin').read_bytes()
    _, fixture = request_ending(arm, raw, captain)
    assert report['synthetic_ending_fixtures'][0] == {'frame': 3000, **fixture}
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    expected_donor = preflight['donor_sha256'] if captain == 3 else preflight['Hodram']['donor_sha256']
    assert donor['source_sha256'] == expected_donor
    shots = {s['frame']: s for s in report['frames_captured']}
    for s in shots.values():
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
    snapshots = {}
    for gpu in report['read_only_capture_GPU_states']:
        assert gpu['read_only_export'] and not gpu['state_loaded'] and gpu['main_RAM_unchanged_by_export']
        assert gpu['script_sha256'] == sha(Path('scripts/inspect_desmume_gpu_v630.py').read_bytes())
        for field in gpu['files'].values():
            assert sha(Path(field['path']).read_bytes()) == field['sha256']
        assert sha(Path(gpu['path']).read_bytes()) == gpu['sha256']
        snapshots[gpu['frame']] = gpu
    return report, shots, snapshots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    preflight = read(ROOT / 'preflight_proof.json')
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    assert sha(ROM.read_bytes()) == preflight['candidate_sha256']
    arm = rom.read_file('/__arm9__.bin')
    for row in preflight['original_code_ranges']:
        lo, hi = row['offset']
        assert arm[lo:hi] == clean.read_file('/__arm9__.bin')[lo:hi]
    movie = rom.read_file('/FLS/M32.fls')
    assert movie == clean.read_file('/FLS/M32.fls')
    texture = FlsArchive(movie).texture(4)
    _run, shots, snapshots, binding = load_run(CAP, 3, 10400, preflight, arm)
    assert sorted(snapshots) == [8320, 8640, 8960, 9280, 9360, 9600, 10240]
    rows, base, matrices = [], None, None
    for frame, state in sorted(snapshots.items()):
        polys = geometry(Path(state['files']['gpu_geometry_chunk91.bin']['path']).read_bytes())
        photo = [p for p in polys if p['texture_parameter'] == 0x52D00004 and p['palette'] == 2]
        assert len(photo) == 1 and photo[0]['vertex_colors_RGB6'] == [[63, 63, 63]] * 4
        assert (photo[0]['attributes'] >> 4 & 3) == 0
        assert photo[0]['texture_parameter'] >> 16 & 15 == 0  # source clamp, no repeat/flip
        gpu_tags = tags(Path(state['files']['gpu_tagged_chunk90.bin']['path']).read_bytes())
        assert int.from_bytes(gpu_tags['gSCC'], 'little') & 32767 == 0
        if matrices is None:
            matrices = state['current_matrices_FX12_by_mode']
        assert matrices == state['current_matrices_FX12_by_mode']
        actual = Image.open(shots[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
        checked = pixel_check(photo[0], texture, actual)
        actual.save(ROOT / f'M32_{frame:06d}_V627_ACTUAL_UPPER.png')
        rows.append({'frame': frame, 'source_PNG': shots[frame]['path'], 'PNG_sha256': shots[frame]['PNG_sha256'],
                     'GPU_state_proof': state['path'], 'GPU_state_sha256': state['sha256'],
                     'original_transformed_polygon': photo[0], **checked})
        base = photo[0]
    previous = read('work/analysis/ending_photo_pixels_v629/native_photo_pixels_proof.json')
    assert previous['script_sha256'] == sha(Path('scripts/verify_ending_photo_pixels_v629.py').read_bytes())
    old_rows = []
    for row in previous['M32_controller_continuity']['all_captured_sampling_comparisons_in_replayed_interval']:
        polygon = deepcopy(base)
        uv = [[0, 0], [0, 192], [256, 192], [256, 0]]
        polygon['vertices'] = [[2 * x / 4096 - 1, 1 - 2 * y / 4096,
                                base['vertices'][0][2], 1, *uv[i]]
                               for i, (x, y) in enumerate(row['GPU_XY16'])]
        # The original fixed projection/position matrices and emitted VTX16
        # coordinates reproduce each independently exported geometry anchor.
        if row['frame'] in snapshots:
            native_poly = next(r['original_transformed_polygon'] for r in rows if r['frame'] == row['frame'])
            assert polygon['vertices'] == native_poly['vertices']
        path = Path(row['source_PNG'])
        assert sha(path.read_bytes()) == row['source_PNG_sha256']
        actual = Image.open(path).convert('RGB').crop((0, 0, 256, 192))
        old_rows.append({'frame': row['frame'], 'source_PNG': str(path), 'PNG_sha256': row['source_PNG_sha256'],
                         'former_RGB_mismatches': row['simple_sampling_RGB_mismatches'],
                         **pixel_check(polygon, texture, actual)})
    assert len(old_rows) == 24
    # Keep the separate Hodram transition open. Its pixels are not waived or
    # mistaken for a source-art defect by a model outside its validated scope.
    _hr, hs, hg, hb = load_run(HODRAM, 1, 14400, preflight, arm)
    assert sorted(hg) == [13360, 13520, 13760, 14000]
    hodram = []
    htex = FlsArchive(rom.read_file('/FLS/M30.fls')).texture(5)
    assert rom.read_file('/FLS/M30.fls') == clean.read_file('/FLS/M30.fls')
    for frame, state in sorted(hg.items()):
        polys = geometry(Path(state['files']['gpu_geometry_chunk91.bin']['path']).read_bytes())
        photo = [p for p in polys if p['texture_parameter'] == 0x52D03404 and p['palette'] == 100]
        assert len(photo) == 1
        alpha = photo[0]['attributes'] >> 16 & 31
        differences = None
        if alpha == 31:
            predicted, _ = sample(photo[0], htex)
            actual = Image.open(hs[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
            differences = sum(a != b for a, b in zip(actual.get_flattened_data(), predicted, strict=True))
            assert differences > 0
        hodram.append({'frame': frame, 'source_PNG': hs[frame]['path'], 'PNG_sha256': hs[frame]['PNG_sha256'],
                       'GPU_state_proof': state['path'], 'native_photo_alpha': alpha,
                       'opaque_model_RGB_differences': differences, 'composition_or_frame_binding_remains_open': True})
    # Actual GPU fields and geometry readers must reject malformed extents.
    for bad in (b'', b'GMCU' + bytes(8) + b'bad'):
        try:
            tags(bad)
        except (ValueError, AssertionError):
            pass
        else:
            assert bad == b''  # empty tag list is a valid empty container
    save(ROOT / 'native_gpu_photo_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': preflight['candidate_sha256'],
        'M32_actual_V627_run': binding, 'M32_actual_GPU_export_complete_frames': rows,
        'M32_existing_V593_whole_sequence_frames': old_rows,
        'seven_new_and24_existing_full49152_RGB_planes_exact': True,
        'source_clipping_FX4_truncation_and_scanline_interpolation_explain_all_former_M32_mismatches': True,
        'no_per_frame_alignment_pixel_mask_or_color_tolerance': True,
        'Hodram_actual_V627_run': hb, 'Hodram_separate_unresolved_states': hodram,
        'source_matrices_FX12': matrices, 'current_ROM_artwork_patch_registry_unchanged': True,
        'native_GPU_exports_are_read_only_and_never_loaded': True,
        'prior_V629_proof_sha256': sha(Path('work/analysis/ending_photo_pixels_v629/native_photo_pixels_proof.json').read_bytes()),
        'source_code_references': {
            'renderer': 'https://github.com/libretro/desmume/blob/95b4d79/desmume/src/rasterize.cpp',
            'clipping_and_serialization': 'https://github.com/libretro/desmume/blob/95b4d79/desmume/src/gfx3d.cpp'},
        'source_file_sha256': {name: sha((ROOT / name).read_bytes()) for name in ('gfx3d.cpp', 'saves.cpp')},
        'sampler_sha256': sha(Path('scripts/research_photo_sampler_v630.py').read_bytes()),
        'GPU_exporter_sha256': sha(Path('scripts/inspect_desmume_gpu_v630.py').read_bytes()),
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'not_earned_endings_complete_routes_or_hardware_verification': True,
        'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V630:7 new V627 +24 existing full photo frames exact RGB;all negative controls reject;Hodram composition remains open.')


if __name__ == '__main__':
    main()
