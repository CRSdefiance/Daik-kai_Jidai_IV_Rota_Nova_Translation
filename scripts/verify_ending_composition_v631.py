"""Verify original Hodram photos, measured pipeline delay and alpha overlap."""

from copy import deepcopy
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_ending_blend_v631 import BINDINGS, CAP, ROOT, compose, plane
from scripts.research_photo_sampler_v630 import geometry
from scripts.verify_ending_gpu_v630 import load_run, pixel_check
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v627_candidate.nds')
PREVIOUS = Path('work/analysis/ending_gpu_state_v630/native_gpu_photo_proof.json')


def photo(polys):
    matches = [p for p in polys if BINDINGS[p['texture_parameter'], p['palette']] == 5]
    assert len(matches) == 1
    return matches[0]


def negative_controls(polys, movie, actual):
    expected, _ = compose(polys, movie)
    assert expected == actual
    p = photo(polys)
    tex = movie.texture(5)
    photo_plane = plane(p, tex)
    stars = [s for s in polys if BINDINGS[s['texture_parameter'], s['palette']] == 4]
    star_plane = plane(stars[0], movie.texture(4)) if stars else [None] * len(photo_plane)
    # Choose an unoccluded source texel from geometry, not a pixel fitted to the
    # screenshot. Alter it to the most different existing source palette color.
    at = next(i for i, source in enumerate(photo_plane) if source is not None
              and (star_plane[i] is None or movie.texture(4).indices[star_plane[i]] == 0))
    source = photo_plane[at]
    before = tex.indices[source]
    alternate = max(range(len(tex.palette)),
                    key=lambda i: sum(abs(a - b) for a, b in zip(tex.palette[i][:3], tex.palette[before][:3], strict=True)))
    tex.indices[source] = alternate
    mutated, _ = compose(polys, movie)
    tex.indices[source] = before
    assert mutated != actual
    shifted = deepcopy(polys)
    for vertex in photo(shifted)['vertices']:
        vertex[0] += 1 / 128
    moved, _ = compose(shifted, movie)
    assert moved != actual
    assert [(0, 0, 0)] * len(actual) != actual
    controls = {'source_texel_blank_and_one_pixel_photo_geometry_shift_rejected': True}
    if stars:
        without_star = [s for s in polys if BINDINGS[s['texture_parameter'], s['palette']] != 4]
        without_scenery = [s for s in polys if BINDINGS[s['texture_parameter'], s['palette']] not in (1, 2, 3)]
        assert compose(without_star, movie)[0] != actual
        assert compose(without_scenery, movie)[0] != actual
        wrong_alpha = deepcopy(polys)
        wrong = photo(wrong_alpha)
        wrong['attributes'] = (wrong['attributes'] & ~(31 << 16)) | (31 << 16)
        assert compose(wrong_alpha, movie)[0] != actual
        controls['missing_star_missing_scenery_and_wrong_alpha_rejected'] = True
    return controls


def main():
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    previous = read(PREVIOUS)
    assert sha(ROM.read_bytes()) == previous['candidate_sha256']
    preflight = read('work/analysis/ending_gpu_state_v630/preflight_proof.json')
    arm = rom.read_file('/__arm9__.bin')
    for row in preflight['original_code_ranges']:
        lo, hi = row['offset']
        assert arm[lo:hi] == clean.read_file('/__arm9__.bin')[lo:hi]
    source = rom.read_file('/FLS/M30.fls')
    assert source == clean.read_file('/FLS/M30.fls')
    movie = FlsArchive(source)
    _run, shots, states, binding = load_run(CAP, 1, 14080, preflight, arm)
    frames = {f for anchor in (13360, 13520, 13760, 14000) for f in range(anchor - 2, anchor + 3)}
    assert states.keys() == frames
    polygons, images = {}, {}
    for frame, state in states.items():
        polygons[frame] = geometry(Path(state['files']['gpu_geometry_chunk91.bin']['path']).read_bytes())
        assert all((p['texture_parameter'], p['palette']) in BINDINGS for p in polygons[frame])
        images[frame] = Image.open(shots[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
    results = []
    for anchor in (13360, 13520, 13760, 14000):
        for frame in range(anchor, anchor + 3):
            source_frame = frame - 2
            polys = polygons[source_frame]
            actual = list(images[frame].get_flattened_data())
            expected, counts = compose(polys, movie)
            assert expected == actual, (source_frame, frame)
            controls = negative_controls(polys, movie, actual)
            if anchor != 13360:
                # Independent earlier opaque sampler also passes with the same
                # globally measured source-to-display phase; no new opaque math.
                pixel_check(photo(polys), movie.texture(5), images[frame])
            target = ROOT / f'M30_{frame:06d}_SOURCE_COMPOSITION.png'
            im = Image.new('RGB', (256, 192))
            im.putdata(expected)
            im.save(target)
            images[frame].save(ROOT / f'M30_{frame:06d}_ACTUAL_UPPER.png')
            results.append({'source_geometry_frame': source_frame, 'display_frame': frame,
                            'source_PNG': shots[frame]['path'], 'PNG_sha256': shots[frame]['PNG_sha256'],
                            'GPU_state_proof': states[source_frame]['path'],
                            'GPU_state_proof_sha256': states[source_frame]['sha256'],
                            'all49152_RGB_pixels_exact': True, 'original_source_draws': counts,
                            'complete_reconstruction_RGB_sha256': sha(im.tobytes()), **controls})
    # Compare fixed offsets on every overlapping available frame. Offset2 is
    # shared by every case;0/1/3 each fail. Never choose a match per screenshot.
    lag_controls = []
    for lag in (0, 1, 2, 3):
        comparisons = []
        for frame in sorted(frames):
            if frame - lag not in frames:
                continue
            predicted, _ = compose(polygons[frame - lag], movie)
            actual = list(images[frame].get_flattened_data())
            count = sum(a != b for a, b in zip(actual, predicted, strict=True))
            comparisons.append({'source_geometry_frame': frame - lag, 'display_frame': frame,
                                'RGB_differences': count})
        assert comparisons
        assert all(c['RGB_differences'] == 0 for c in comparisons) if lag == 2 else any(c['RGB_differences'] for c in comparisons)
        lag_controls.append({'fixed_lag_frames': lag, 'comparisons': comparisons,
                             'all_whole_frame_comparisons_exact': all(c['RGB_differences'] == 0 for c in comparisons)})
    old_binding = previous['Hodram_actual_V627_run']
    old_report = read(old_binding['path'])
    assert sha(Path(old_binding['path']).read_bytes()) == old_binding['sha256']
    old_shots = {r['frame']: r for r in old_report['frames_captured']}
    for frame in (13360, 13520, 13760, 14000):
        old = Image.open(old_shots[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
        assert old.tobytes() == images[frame].tobytes()
    assert len(results) == 12
    save(ROOT / 'native_composition_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'new_run': binding,
        'original_M30_file_sha256': sha(source), 'all_original_M30_artwork_exact_clean': True,
        'original_source_code_ranges': preflight['original_code_ranges'],
        'all12_complete_native_upper_frame_compositions': results,
        'nine_opaque_and_three_translucent_full49152_RGB_planes_exact': True,
        'observed_uniform_geometry_submission_to_display_lag_frames': 2,
        'same_frame_and_wrong_uniform_phase_controls': lag_controls,
        'source_stage_evidence': {'file': 'work/analysis/ending_gpu_state_v630/gfx3d.cpp',
                                  'sha256': sha(Path('work/analysis/ending_gpu_state_v630/gfx3d.cpp').read_bytes()),
                                  'pending_list_swap': '397..405,2458..2480', 'serialized_pending_list': '2857..2868',
                                  'source_commit': '95b4d798731caa809125b6c3c11d17cc332ff6ef'},
        'source_six_bit_alpha_rule': '(alpha+1)*source + (31-alpha)*destination, shifted right5',
        'source_palette_five_to_six_rule': '0 maps0;nonzero c maps2*c+1',
        'three_translucent_star_visible_pixels': [46, 46, 19],
        'all_four_V630_Hodram_photo_findings_resolved_with_no_pixel_waiver': True,
        'historical_V630_proof_retained': str(PREVIOUS), 'historical_V630_proof_sha256': sha(PREVIOUS.read_bytes()),
        'no_ROM_patch_registry_or_artwork_changes': True,
        'bounded_axis_aligned_flat_white_single_translucent_photo_model_not_a_full_GPU': True,
        'not_all_movie_frames_routes_or_hardware_verified': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'sampler_sha256': sha(Path('scripts/research_ending_blend_v631.py').read_bytes()),
        'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V631:9 opaque/3 translucent complete RGB frames exact;fixed2-frame phase proven with0/1/3 negatives;four Hodram findings resolved.')


if __name__ == '__main__':
    main()
