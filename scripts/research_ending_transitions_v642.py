"""Source/native binding and full RGB diagnostics for Rafael/Lil transitions."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_ending_blend_v631 import plane, sixbit_palette
from scripts.research_photo_sampler_v630 import geometry
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_ending_photo_pixels_v629 import drawing, prepare
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ending_transitions_v642')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v640_candidate.nds')


def native_bindings(arm, clean_arm, raw, source):
    live = find_live(raw, source)
    if live is None:
        return {}, {'no_live_FLS_controller': True}
    obj = live['object']
    u, original = prepare(arm, raw), machine(clean_arm)
    state = raw[obj - BASE:obj - BASE + 0x1B18]
    buffer = struct.unpack_from('<h', state, 0x1A08)[0] ^ 1
    bindings, rows, executed = {}, [], set()
    handle = u.hook_add(UC_HOOK_CODE, lambda cpu, address, size, unused: executed.add(address))
    try:
        for slot in range(1, 32):
            at = 0x204 + buffer * 0xC00 + slot * 0x60
            if not struct.unpack_from('<h', state, at)[0] or struct.unpack_from('<h', state, at + 0x34)[0]:
                continue
            texture_input = struct.unpack_from('<h', state, at + 2)[0]
            call(u, 0x100390, (obj, texture_input & 0xFFFFFFFF))
            selected = u.reg_read(UC_ARM_REG_R0)
            result = drawing(u, obj, slot)
            if not result['GPU_writes']:
                continue
            args = {address: [w['value'] for w in result['GPU_writes'] if w['address'] == address]
                    for address in (0x040004A8, 0x040004AC)}
            assert all(len(values) == 1 for values in args.values())
            key = (args[0x040004A8][0], args[0x040004AC][0])
            assert key not in bindings or bindings[key] == selected
            bindings[key] = selected
            rows.append({'slot': slot, 'texture_input': texture_input, 'original_selector_result': selected,
                         'actual_native_texture_parameter': key[0], 'actual_native_palette': key[1],
                         'full_original_draw': result})
    finally:
        u.hook_del(handle)
    assert all(bytes(u.mem_read(a, 4)) == bytes(original.mem_read(a, 4)) for a in executed)
    assert not ({0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed)
    return bindings, {'live_controller': live, 'draws': rows,
                      'all_native_selector_and_draw_calls_full_ABI_clean_instruction_words': True,
                      'no_file_getter_or_drawing_bridge': True, 'isolated_captured_RAM_copy_only': True,
                      'executed_instruction_addresses': sorted(executed)}


def compose(polys, movie, bindings):
    result, depth = [(0, 0, 0)] * (256 * 192), [float('inf')] * (256 * 192)
    counts = []
    for poly in polys:
        binding = (poly['texture_parameter'], poly['palette'])
        assert binding in bindings, ('No native binding', binding)
        texture_id = bindings[binding]
        tex = movie.texture(texture_id)
        assert poly['vertex_colors_RGB6'] == [[63, 63, 63]] * len(poly['vertices'])
        assert poly['attributes'] >> 4 & 3 == 0
        alpha = poly['attributes'] >> 16 & 31
        assert alpha
        z = poly['vertices'][0][2]
        assert all(v[2] == z for v in poly['vertices'])
        transparent_zero = bool(poly['texture_parameter'] & (1 << 29))
        palette = sixbit_palette(tex)
        locations = plane(poly, tex)
        drawn = 0
        for position, source in enumerate(locations):
            if source is None or z > depth[position]:
                continue
            index = tex.indices[source]
            if transparent_zero and index == 0:
                continue
            color = palette[index]
            if alpha == 31:
                result[position] = color
                depth[position] = z
            else:
                a = alpha + 1
                result[position] = tuple((a * s + (32 - a) * d) >> 5
                                         for s, d in zip(color, result[position], strict=True))
            drawn += 1
        counts.append({'texture': texture_id, 'alpha': alpha, 'drawn_pixels': drawn})
    rgb = []
    for r6, g6, b6 in result:
        r, g, b = r6 >> 1, g6 >> 1, b6 >> 1
        g_out = (g << 1) | (g >> 4)
        rgb.append((r * 255 // 31, g_out * 255 // 63, b * 255 // 31))
    return rgb, counts


def main():
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, clean_arm = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    configs = read(ROOT / 'run_configs.json')
    for config in configs:
        captain, label = config['captain'], config['label']
        folder = CAP / f'ending_transitions_v642_{label}'
        report = read(folder / 'capture_report.json')
        assert report['frames'] == config['frames'] and report['ROM_sha256'] == sha(ROM.read_bytes())
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == read(config['inputs'])
        shots = {r['frame']: r for r in report['frames_captured']}
        states = {r['frame']: r for r in report['read_only_capture_GPU_states']}
        assert states.keys() == set(config['gpu_export_frames'])
        source = rom.read_file(f'/FLS/M{29 + captain}.fls')
        movie = FlsArchive(source)
        polys, bindings, native, images = {}, {}, {}, {}
        for frame, state in states.items():
            assert sha(Path(state['path']).read_bytes()) == state['sha256']
            for item in state['files'].values():
                assert sha(Path(item['path']).read_bytes()) == item['sha256']
            assert state['read_only_export'] and not state['state_loaded'] and state['main_RAM_unchanged_by_export']
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            assert sha(raw) == state['main_RAM_sha256']
            bindings[frame], native[frame] = native_bindings(arm, clean_arm, raw, source)
            polys[frame] = geometry(Path(state['files']['gpu_geometry_chunk91.bin']['path']).read_bytes())
            assert sha(Path(shots[frame]['path']).read_bytes()) == shots[frame]['PNG_sha256']
            images[frame] = Image.open(shots[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
        save(ROOT / f'{label}_native_bindings.json', native)
        tests = []
        for lag in (0, 1, 2, 3):
            for frame in sorted(states):
                if frame - lag not in states:
                    continue
                sf = frame - lag
                try:
                    expected, draws = compose(polys[sf], movie, bindings[sf])
                    actual = list(images[frame].get_flattened_data())
                    differences = sum(a != b for a, b in zip(expected, actual, strict=True))
                    tests.append({'source_geometry_frame': sf, 'display_frame': frame, 'lag': lag,
                                  'whole_upper_RGB_differences': differences, 'draws': draws})
                except (AssertionError, ValueError, KeyError) as error:
                    tests.append({'source_geometry_frame': sf, 'display_frame': frame, 'lag': lag,
                                  'model_error': repr(error)})
        save(ROOT / f'{label}_transition_diagnostic.json', {'comparisons': tests,
            'captured_states': len(states), 'not_yet_a_passing_verification': True})
        for lag in (0, 1, 2, 3):
            rows = [r for r in tests if r['lag'] == lag]
            print(label, 'lag', lag, 'cases', len(rows), 'exact', sum(r.get('whole_upper_RGB_differences') == 0 for r in rows),
                  'errors', sum('model_error' in r for r in rows),
                  'differences', [(r['display_frame'], r.get('whole_upper_RGB_differences', r.get('model_error'))) for r in rows if r.get('whole_upper_RGB_differences') != 0][:8])


if __name__ == '__main__':
    main()
