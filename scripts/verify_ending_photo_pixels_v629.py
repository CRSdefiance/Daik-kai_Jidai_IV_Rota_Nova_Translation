"""Original ending FIFO output, controller continuity and complete photo check.

Reuses disclosed V594 captures. No ROM mutation, graphics replacement or new
emulator run. Unmatched sampling hypotheses remain explicit research results.
"""

import math
import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_regional_ui_v616 import native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ending_photo_pixels_v629')
ROM = Path('out/all_routes_combined_v627_candidate.nds')
PRIOR = Path('work/analysis/ending_photo_markers_v594/native_photo_usage_proof.json')
FIFO = 0x0400048C


def prepare(arm, raw):
    u = machine(arm)
    u.mem_write(BASE, raw)
    u.mem_map(0x04000000, 0x100000)
    return u


def drawing(u, obj, slot):
    """Execute the whole original quad function through its actual GPU writes."""
    writes = []

    def observe(cpu, access, address, size, value, unused):
        writes.append({'pc': cpu.reg_read(UC_ARM_REG_PC), 'address': address,
                       'size': size, 'value': value})

    before = bytes(u.mem_read(obj, 0x1B18))
    handle = u.hook_add(UC_HOOK_MEM_WRITE, observe, begin=0x04000000, end=0x040FFFFF)
    try:
        executed = call(u, 0xFEB28, (obj, slot), instruction_limit=300000)
    finally:
        u.hook_del(handle)
    after = bytes(u.mem_read(obj, 0x1B18))
    differences = [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    assert set(differences) <= {1}
    assert not writes or after[1] == (before[1] + 1) & 63
    assert BASE + 0xFF9C0 in executed or not writes
    vertex_values = [r['value'] for r in writes if r['address'] == FIFO]
    coords = [r['value'] for r in writes if r['address'] == 0x04000488]
    if writes:
        assert len(vertex_values) == 8 and len(coords) == 4
    vertices = [list(struct.unpack('<2h', struct.pack('<I', v))) for v in vertex_values[::2]]
    uv = [list(struct.unpack('<2h', struct.pack('<I', v))) for v in coords]
    return {'GPU_writes': writes, 'GPU_XY16': vertices, 'texture_coordinates_12_4': uv,
            'vertex_Z16': vertex_values[1::2], 'only_controller_polygon_ID_byte_changed': True,
            'complete_original_draw_return_stack_and_saved_registers_pass': True}


def projected_pixels(texture, native_dimensions, vertices):
    """An explicit simple sampling hypothesis, not a general DS compositor.

    The original function normalizes X by256 and Y by192 before VTX16. Convert
    emitted normalized vertices back to screen coordinates, then floor source
    coordinates. Clamping is part of this declared hypothesis, not a waiver.
    """
    left, top = vertices[0][0] / 16, vertices[0][1] * 3 / 64
    right, bottom = vertices[2][0] / 16, vertices[2][1] * 3 / 64
    assert right > left and bottom > top
    assert vertices[0][0] == vertices[1][0] and vertices[2][0] == vertices[3][0]
    assert vertices[0][1] == vertices[3][1] and vertices[1][1] == vertices[2][1]
    width, height = native_dimensions
    xs = [max(0, min(width - 1, math.floor((x - left) * width / (right - left)))) for x in range(256)]
    ys = [max(0, min(height - 1, math.floor((y - top) * height / (bottom - top)))) for y in range(192)]
    colors = []
    for red, green, blue, alpha in texture.palette:
        r, g, b = ((v * 31 + 127) // 255 for v in (red, green, blue))
        g6 = g * 2 + (g >> 4)
        colors.append((r * 255 // 31, g6 * 255 // 63, b * 255 // 31))
    indices = [ys[y] * texture.width + xs[x] for y in range(192) for x in range(256)]
    return [colors[texture.indices[i]] for i in indices], indices


def continuity(arm, folder, source):
    first, last = 8320, 10240
    raw = (folder / f'frame_{first:06d}_arm9_ram.bin').read_bytes()
    live = find_live(raw, source)
    obj, offset = live['object'], live['object'] - BASE
    u = prepare(arm, raw)
    texture = FlsArchive(source).texture(4)
    shots = {r['frame']: r for r in read(folder / 'capture_report.json')['frames_captured']}
    anchors, full_draws, sampling = [], 0, []
    for frame in range(first, last + 1):
        if frame > first:
            call(u, 0xFD4F8, (obj,), instruction_limit=500000)
            data = bytes(u.mem_read(obj, 0x1B18))
            previous = struct.unpack_from('<h', data, 0x1A08)[0] ^ 1
            for slot in range(1, 32):
                at = 0x204 + previous * 0xC00 + slot * 0x60
                if struct.unpack_from('<h', data, at)[0] and not struct.unpack_from('<h', data, at + 0x34)[0]:
                    # Real original drawing includes its polygon-ID update.
                    if frame in shots and slot == 3:
                        texture_input = struct.unpack_from('<h', data, at + 2)[0]
                        call(u, 0x100390, (obj, texture_input))
                        assert u.reg_read(UC_ARM_REG_R0) == 4
                        result = drawing(u, obj, slot)
                        assert result['GPU_XY16']
                        shot = shots[frame]
                        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
                        actual = Image.open(shot['path']).convert('RGB').crop((0, 0, 256, 192))
                        predicted, source_indices = projected_pixels(texture, (256, 192), result['GPU_XY16'])
                        differences = sum(a != b for a, b in zip(actual.get_flattened_data(), predicted, strict=True))
                        sampling.append({'frame': frame, 'GPU_XY16': result['GPU_XY16'],
                                         'source_PNG': shot['path'], 'source_PNG_sha256': shot['PNG_sha256'],
                                         'all49152_RGB_pixels_compared': True,
                                         'simple_sampling_RGB_mismatches': differences,
                                         'complete_frame_exact': differences == 0,
                                         'unmatched_states_remain_open': differences != 0})
                        if not differences:
                            assert list(actual.get_flattened_data()) != [(0, 0, 0)] * (256 * 192)
                            assert list(actual.get_flattened_data()) != predicted[1:] + predicted[:1]
                            source_index = source_indices[len(source_indices) // 2]
                            before_index = texture.indices[source_index]
                            texture.indices[source_index] = (before_index + 1) % len(texture.palette)
                            changed, _ = projected_pixels(texture, (256, 192), result['GPU_XY16'])
                            texture.indices[source_index] = before_index
                            assert list(actual.get_flattened_data()) != changed
                            sampling[-1]['blank_shift_and_source_texel_negative_controls_rejected'] = True
                            actual.save(ROOT / f'M32_{frame:06d}_ACTUAL_UPPER.png')
                            reconstruction = Image.new('RGB', (256, 192))
                            reconstruction.putdata(predicted)
                            reconstruction.save(ROOT / f'M32_{frame:06d}_SOURCE_RECONSTRUCTION.png')
                    else:
                        call(u, 0xFEB28, (obj, slot), instruction_limit=300000)
                    full_draws += 1
        if frame in (8640, 8960, 9280, 9600, 9920, 10240):
            path = folder / f'frame_{frame:06d}_arm9_ram.bin'
            actual = path.read_bytes()
            assert find_live(actual, source)['object'] == obj
            assert bytes(u.mem_read(obj, 0x1B18)) == actual[offset:offset + 0x1B18], frame
            anchors.append({'frame': frame, 'all6936_controller_bytes_exact': True,
                            'source_RAM': str(path), 'source_RAM_sha256': sha(actual)})
    return {'initial_RAM_sha256': sha(raw), 'first_frame': first, 'last_frame': last,
            'original_update_calls': last - first, 'complete_original_draw_calls': full_draws,
            'actual_whole_controller_anchors': anchors, 'no_SDK_geometry_or_GPU_write_bridges': True,
            'all_captured_sampling_comparisons_in_replayed_interval': sampling,
            'original_control_screens_are_not_new_emulator_runs': True,
            'GPU_writes_observed_or_retained_in_dummy_IO_not_executed_by_a_GPU': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    prior = read(PRIOR)
    current = NdsImage.open(ROM)
    original, captured = NdsImage.open('work/clean.nds'), NdsImage.open(prior['candidate'])
    arm, old, clean = (r.read_file('/__arm9__.bin') for r in (current, captured, original))
    assert sha(ROM.read_bytes()) == '0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09'
    assert sha(Path(prior['candidate']).read_bytes()) == prior['candidate_sha256']
    ranges = []
    for lo, hi in ((0xFD4F8, 0xFDC60), (0xFEB28, 0xFF9C8), (0x100390, 0x1003CC), (0xDFA88, 0xDFD00)):
        assert arm[lo:hi] == old[lo:hi] == clean[lo:hi]
        ranges.append({'offsets': [lo, hi], 'sha256': sha(arm[lo:hi]), 'clean_V593_V627_exact': True})
    cases, exact = [], []
    for case in prior['cases']:
        source = current.read_file(case['file'])
        assert source == captured.read_file(case['file']) == original.read_file(case['file'])
        movie = FlsArchive(source)
        texture = movie.texture(case['texture'])
        texture.render().save(ROOT / (case['label'] + '_SOURCE.png'))
        report_path = Path(case['reports']['control']['path'])
        assert sha(report_path.read_bytes()) == case['reports']['control']['sha256']
        report = read(report_path)
        assert report['ROM_sha256'] == prior['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        shots = {r['frame']: r for r in report['frames_captured']}
        for row in case['native_snapshot_projection_cases']:
            if not row['original_photo_drawings']:
                continue
            frame = row['frame']
            path = report_path.parent / f'frame_{frame:06d}_arm9_ram.bin'
            raw = path.read_bytes()
            live = find_live(raw, source)
            assert live == row['live_source']
            u = prepare(arm, raw)
            source_draw = row['original_photo_drawings'][0]
            call(u, 0x100390, (live['object'], source_draw['texture_input']))
            assert u.reg_read(UC_ARM_REG_R0) == case['texture']
            result = drawing(u, live['object'], source_draw['slot'])
            assert len(result['GPU_XY16']) == 4
            shot = shots[frame]
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            image = Image.open(shot['path']).convert('RGB').crop((0, 0, 256, 192))
            actual = list(image.get_flattened_data())
            predicted, source_indices = projected_pixels(texture, case['native_dimensions'], result['GPU_XY16'])
            diff = [i for i, (a, b) in enumerate(zip(actual, predicted, strict=True)) if a != b]
            five = list(native5(image).get_flattened_data())
            predicted5 = [tuple((v * 31 + 127) // 255 for v in c) for c in predicted]
            d5 = sum(a != b for a, b in zip(five, predicted5, strict=True))
            record = {'label': case['label'], 'frame': frame, 'file': case['file'], 'texture': case['texture'],
                      'native_dimensions': case['native_dimensions'], 'live_binding': live,
                      'RAM': str(path), 'RAM_sha256': sha(raw), 'source_PNG': shot['path'],
                      'source_PNG_sha256': shot['PNG_sha256'], **result,
                      'simple_sampling_RGB_mismatches': len(diff), 'simple_sampling_native5_mismatches': d5,
                      'simple_sampling_model_not_accepted_for_unmatched_states': bool(diff)}
            if not diff:
                assert case['label'] == 'maria' and frame == 9280
                assert result['texture_coordinates_12_4'] == [[0, 0], [0, 3072], [4096, 3072], [4096, 0]]
                assert result['GPU_XY16'] == [[0, -295], [0, 4672], [4968, 4672], [4968, -295]]
                image.save(ROOT / 'M32_009280_ACTUAL_UPPER.png')
                expected_image = Image.new('RGB', (256, 192))
                expected_image.putdata(predicted)
                expected_image.save(ROOT / 'M32_009280_SOURCE_RECONSTRUCTION.png')
                # Wrong photo, missing source texels, and one-pixel source shifts
                # must all fail the complete independent captured framebuffer.
                black = [(0, 0, 0)] * len(predicted)
                shifted = predicted[1:] + predicted[:1]
                assert actual != black and actual != shifted
                altered = texture.indices[:]
                changed_at = source_indices[len(source_indices) // 2]
                texture.indices[changed_at] = (texture.indices[changed_at] + 1) % len(texture.palette)
                mutated, _ = projected_pixels(texture, case['native_dimensions'], result['GPU_XY16'])
                texture.indices[:] = altered
                assert actual != mutated
                record.update(all49152_native_pixels_and_RGB_colors_exact=True,
                              all_geometric_viewport_pixels_included_no_waivers=True,
                              blank_one_pixel_shift_and_source_texel_controls_rejected=True,
                              sampled_distinct_source_texels=len(set(source_indices)),
                              reconstructed_RGB_sha256=sha(expected_image.tobytes()))
                exact.append({'label': case['label'], 'frame': frame, 'full_native_pixels': 49152})
            cases.append(record)
    assert len(cases) == 11 and exact == [{'label': 'maria', 'frame': 9280, 'full_native_pixels': 49152}]
    maria = prior['cases'][1]
    continued = continuity(arm, Path(maria['reports']['control']['path']).parent,
                           current.read_file(maria['file']))
    all_exact = sorted({r['frame'] for r in continued['all_captured_sampling_comparisons_in_replayed_interval']
                        if r['complete_frame_exact']} | {9280})
    save(ROOT / 'native_photo_pixels_proof.json', {
        'current_candidate': str(ROM), 'current_candidate_sha256': sha(ROM.read_bytes()),
        'captured_candidate': prior['candidate'], 'captured_candidate_sha256': prior['candidate_sha256'],
        'source_code_ranges': ranges, 'cases': cases, 'M32_controller_continuity': continued,
        'complete_source_photo_frames': [{'label': 'maria', 'frame': f, 'full_native_pixels': 49152} for f in all_exact],
        'remaining_sampling_projection_clip_and_composition_states_open': True,
        'no_failed_model_is_classified_as_a_ROM_or_artwork_defect': True,
        'no_ROM_patch_registry_or_artwork_changes_no_new_emulator_run': True,
        'source_retention_no_Japanese_caption_decisions_retain_prior_visual_reviews': True,
        'prior_marker_proof': str(PRIOR), 'prior_marker_proof_sha256': sha(PRIOR.read_bytes()),
        'test_fixture_not_earned_completion_or_hardware_verification': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print(f'V629:11 original GPU streams;1920 updates/six6936-byte anchors exact;'
          f'{len(all_exact)} complete49152-pixel photos exact;other sampling states open.')


if __name__ == '__main__':
    main()
