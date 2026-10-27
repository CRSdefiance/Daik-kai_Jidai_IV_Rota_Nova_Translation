"""Original movie projection commands with explicit instantaneous math hardware.

Division/square-root results follow the pinned core; timing and GPU processing
are not modeled. Game/SDK instructions execute without instruction bridges.
"""

import argparse
import hashlib
import json
import math
import struct
from fractions import Fraction
from pathlib import Path

from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.research_fls_stream_v310 import SNAPSHOT, case

ROOT = Path('work/analysis/fls_projection_v331')
ROM = Path('out/all_routes_combined_v326_candidate.nds')
IO = 0x04000000


def signed(value, bits):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def math_hardware(u):
    events = []

    def read(uc, access, address, size, value, _):
        if IO + 0x280 <= address < IO + 0x2B0:
            control = struct.unpack('<H', uc.mem_read(IO + 0x280, 2))[0]
            mode = control & 3
            numerator = int.from_bytes(uc.mem_read(IO + 0x290, 8), 'little')
            denominator = int.from_bytes(uc.mem_read(IO + 0x298, 8), 'little')
            num = signed(numerator, 32 if mode == 0 else 64)
            den = signed(denominator, 64 if mode == 2 else 32)
            if den:
                if num == -(1 << 63) and den == -1:
                    raise ValueError('Undefined pinned C++ overflow case not modeled')
                quotient = abs(num) // abs(den)
                if (num < 0) != (den < 0):
                    quotient = -quotient
                remainder = num - quotient * den
            else:
                quotient, remainder = (1 if num < 0 else -1), num
            status = mode | (0x4000 if denominator == 0 else 0)
            uc.mem_write(IO + 0x280, struct.pack('<H', status))
            uc.mem_write(IO + 0x2A0, struct.pack('<2Q', quotient & ((1 << 64) - 1), remainder & ((1 << 64) - 1)))
            events.append({'operation': 'divide', 'mode': mode, 'numerator': num, 'denominator': den,
                           'quotient': quotient, 'remainder': remainder, 'status': status})
        elif IO + 0x2B0 <= address < IO + 0x2C0:
            mode = struct.unpack('<H', uc.mem_read(IO + 0x2B0, 2))[0] & 1
            operand = int.from_bytes(uc.mem_read(IO + 0x2B8, 8 if mode else 4), 'little')
            result = math.isqrt(operand)
            uc.mem_write(IO + 0x2B0, struct.pack('<H', mode))
            uc.mem_write(IO + 0x2B4, struct.pack('<I', result))
            events.append({'operation': 'sqrt', 'mode': mode, 'operand': operand, 'result': result})

    hook = u.hook_add(UC_HOOK_MEM_READ, read, begin=IO + 0x280, end=IO + 0x2BF)
    return hook, events


def inspect(u, obj, *, with_math=True):
    u.mem_map(IO, 0x1000)
    hook, arithmetic = math_hardware(u) if with_math else (None, [])
    writes = []

    def observe(uc, access, address, size, value, _):
        writes.append({'address': address, 'size': size, 'value': value, 'PC': uc.reg_read(UC_ARM_REG_PC)})

    observer = u.hook_add(UC_HOOK_MEM_WRITE, observe, begin=IO + 0x400, end=IO + 0x5FF)
    u.mem_write(obj + 0x1A90, struct.pack('<I', 0xA5A5A5A5))
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    u.reg_write(UC_ARM_REG_R0, obj)
    try:
        u.emu_start(BASE + 0xFD178, BASE + 0xFD28C, count=500000)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0xFD28C
        assert struct.unpack('<I', u.mem_read(obj + 0x1A90, 4))[0] == 0
        assert writes and (arithmetic or not with_math)
        return {'original_projection_prefix_reaches_draw_loop': True,
                'original_parent_resets_mask_count_to_zero': True,
                'native_GPU_register_commands': writes, 'hardware_arithmetic_requests': arithmetic,
                'instantaneous_math_completion_no_cycle_or_GPU_pixel_model': True,
                'stopped_before_slot_selection_and_full_parent_return': True}
    finally:
        if hook is not None:
            u.hook_del(hook)
        u.hook_del(observer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    source = json.loads((ROOT / 'source.json').read_text(encoding='utf-8'))
    raw = (ROOT / 'MMU.cpp').read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == source['blob']
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, ram = current.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    assert arm[0xFD178:0xFD338] == clean.read_file('/__arm9__.bin')[0xFD178:0xFD338] == ram[0xFD178:0xFD338]
    for left, right in ((0xE13F4, 0xE1B18), (0xFD4F8, 0xFDC60), (0xFE840, 0xFFA04)):
        assert arm[left:right] == clean.read_file('/__arm9__.bin')[left:right] == ram[left:right]
    paths = sorted(path for _, path, _ in current.iter_files() if path.casefold().endswith('.fls')) if args.all else ['/FLS/M22.fls']
    results = []
    for path in paths:
        pair = [case(rom, arm, ram, path, inspect=inspect) for rom in (current, clean)]
        projected = [r.get('additional_scoped_inspection') for r in pair]
        assert all(projected), pair
        assert projected[0] == projected[1]
        results.append({'path': path, 'projection': projected[0],
                        'clean_current_native_commands_and_arithmetic_exact': True})
    timelines = json.loads(Path('work/analysis/fls_frames_v312/all_files_proof.json').read_text(encoding='utf-8'))
    previous = NdsImage.open(timelines['candidate'])
    assert timelines['candidate_sha256'] == sha(Path(timelines['candidate']).read_bytes())
    mask_audit = []
    for movie in timelines['cases']:
        assert current.read_file(movie['path']) == previous.read_file(movie['path'])
        assert movie['clean_source_native_states_and_geometry_exact'] and movie['frames']['error'] is None
        assert movie['frames']['states'][-1]['return'] == 5
        active_masks = [{'tick': state['tick'], 'slot': slot['slot'], 'kind': slot['draw_kind']}
                        for state in movie['frames']['states'] for slot in state['slots']
                        if slot['draw_kind'] != 0]
        assert not active_masks
        mask_audit.append({'path': movie['path'], 'native_updates': movie['frames']['native_update_calls'],
                           'recorded_distinct_states': len(movie['frames']['states']),
                           'active_mask_slots': active_masks,
                           'limited_to_recorded_constructor_timeline_path_not_global_unused': True})
    # Independent exact-rational reference for original Ortho inputs:
    # top/left0, bottom/right1, near1, far400, scale1. FX12 rounds to
    # nearest; these non-tie values avoid a platform rounding assumption.
    fixed = lambda value: math.floor(Fraction(value) * 4096 + Fraction(1, 2))
    expected_projection = [fixed(2), 0, 0, 0, 0, fixed(-2), 0, 0,
                           0, 0, fixed(Fraction(-2, 399)), 0,
                           fixed(-1), fixed(1), fixed(Fraction(-401, 399)), fixed(1)]
    expected_camera = [4096, 0, 0, 0, 4096, 0, 0, 0, 4096, 0, 0, -4096]
    for record in results:
        commands = record['projection']['native_GPU_register_commands']
        projection = [signed(c['value'], 32) for c in commands if c['address'] == IO + 0x458]
        camera = [signed(c['value'], 32) for c in commands if c['address'] == IO + 0x45C]
        assert projection == expected_projection and camera == expected_camera
        record['exact_expected_FX12_projection_matrix'] = projection
        record['exact_expected_FX12_camera_matrix'] = camera
    negative = case(current, arm, ram, '/FLS/M22.fls', inspect=lambda u, obj: inspect(u, obj, with_math=False))
    rejected = negative['additional_scoped_inspection']
    bad_projection = [signed(c['value'], 32) for c in rejected['native_GPU_register_commands'] if c['address'] == IO + 0x458]
    assert bad_projection != expected_projection
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'source': source,
             'cases': results, 'mask_slot_audit': mask_audit,
             'source_timeline_proof_sha256': sha(Path('work/analysis/fls_frames_v312/all_files_proof.json').read_bytes()),
             'source_draw_parent_resets_mask_count_and_checks_slot_draw_kind': True,
             'independent_exact_projection_and_camera_matrix_reference_checks': len(results),
             'projection_reference_original_inputs': {'top': 0, 'bottom': 1, 'left': 0, 'right': 1,
                                                      'near': 1, 'far': 400, 'scale': 1},
             'bare_zero_IO_negative_control_projection': bad_projection,
             'bare_zero_IO_does_not_pass_projection_reference': True,
             'actual_contextual_masks_not_present_in_these_timelines_screen_GPU_clipping_still_open': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / ('all_projection_proof.json' if args.all else 'exploration.json')).write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_projection_pairs': len(results),
                      'commands_each_version': sum(len(r['projection']['native_GPU_register_commands']) for r in results),
                      'math_requests_each_version': sum(len(r['projection']['hardware_arithmetic_requests']) for r in results),
                      'active_timeline_mask_slots': 0, 'GPU_pixels_verified': False}))


if __name__ == '__main__':
    main()
