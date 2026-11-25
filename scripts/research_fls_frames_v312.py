"""Original FLS timeline update and draw-state snapshots before texture/GPU work."""

import argparse
import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.research_fls_stream_v310 import ROM, SNAPSHOT, case

ROOT = Path('work/analysis/fls_frames_v312')


def quad(u, obj, slot):
    context = u.context_save()
    stack_bytes = bytes(u.mem_read(STACK - 4096, 4128))
    hook = u.hook_add(UC_HOOK_CODE, lambda uc, address, size, data: uc.emu_stop() if address == STOP else None)
    try:
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R0, obj)
        u.reg_write(UC_ARM_REG_R1, slot)
        u.emu_start(BASE + 0xFEB28, BASE + 0xFEFCC, count=100000)
        if u.reg_read(UC_ARM_REG_PC) == STOP:
            return None  # original alpha/inactive guard
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0xFEFCC
        sp = u.reg_read(UC_ARM_REG_SP)
        return [list(struct.unpack('<2i', u.mem_read(sp + offset, 8))) for offset in (0x40, 0x4C, 0x58, 0x64)]
    except UcError as error:
        raise ValueError(f'Native quad PC {u.reg_read(UC_ARM_REG_PC):08X}: {error}') from error
    finally:
        u.hook_del(hook)
        u.mem_write(STACK - 4096, stack_bytes)
        u.context_restore(context)


def inspect_frames(u, obj):
    states = []
    trace = set()
    hook = u.hook_add(UC_HOOK_CODE, lambda uc, address, size, data: trace.add(address))
    error, last = None, None
    try:
        for tick in range(1, 20001):
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, obj)
            u.emu_start(BASE + 0xFD4F8, STOP, count=500000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
            returned = u.reg_read(UC_ARM_REG_R0)
            pointer = struct.unpack('<I', u.mem_read(obj + 0x1A04, 4))[0]
            slots = []
            for index in range(32):
                raw = bytes(u.mem_read(pointer + index * 0x60, 0x60))
                active, texture = struct.unpack_from('<2h', raw)
                if active:
                    context = u.context_save()
                    u.reg_write(UC_ARM_REG_LR, STOP)
                    u.reg_write(UC_ARM_REG_R0, obj)
                    u.reg_write(UC_ARM_REG_R1, texture & 0xFFFFFFFF)
                    u.emu_start(BASE + 0x100390, STOP, count=10000)
                    assert u.reg_read(UC_ARM_REG_PC) == STOP
                    selected = u.reg_read(UC_ARM_REG_R0)
                    u.context_restore(context)
                    table = struct.unpack('<I', u.mem_read(obj + 8, 4))[0]
                    count = struct.unpack('<I', u.mem_read(struct.unpack('<I', u.mem_read(obj + 4, 4))[0] + 8, 4))[0]
                    bounds = None
                    if selected < count:
                        record = struct.unpack('<6I', u.mem_read(table + selected * 24, 24))
                        bounds = [record[0] >> 16, record[1] & 0xFFFF]
                    slots.append({'slot': index, 'texture_input': texture, 'native_texture_index': selected,
                                  'native_texture_bounds': bounds,
                                  'six_fixed_words': list(struct.unpack_from('<6i', raw, 8)),
                                  'eight_control_shorts': list(struct.unpack_from('<8h', raw, 0x20)),
                                  'draw_kind': struct.unpack_from('<h', raw, 0x34)[0], 'state_hex': raw.hex()})
            value = {'return': returned, 'slots': slots,
                     'global_camera_colour_alpha_and_canvas_hex': bytes(u.mem_read(obj + 0x1A94, 0x24)).hex(),
                     'depth_spacing': struct.unpack('<I', u.mem_read(obj + 0x10, 4))[0]}
            if value != last:
                drawing = []
                buffer = struct.unpack('<h', u.mem_read(obj + 0x1A08, 2))[0] ^ 1
                draw_pointer = obj + 0x204 + buffer * 0xC00
                for slot in range(1, 32):
                    raw = bytes(u.mem_read(draw_pointer + slot * 0x60, 0x60))
                    if struct.unpack_from('<h', raw)[0] and struct.unpack_from('<h', raw, 0x34)[0] == 0:
                        corners = quad(u, obj, slot)
                        if corners is not None:
                            drawing.append({'slot': slot, 'texture_input': struct.unpack_from('<h', raw, 2)[0],
                                            'native_corners_fx12_before_clipping_or_GPU': corners})
                states.append({'tick': tick, 'native_frame_counter': struct.unpack('<h', u.mem_read(obj + 0x1A0A, 2))[0],
                               **value, 'previous_buffer_geometry': drawing})
                last = value
            if returned == 5:
                break
        else:
            error = 'Timeline did not finish within20000 native update calls'
    except (AssertionError, UcError, ValueError) as exc:
        error = f'{exc}; PC {u.reg_read(UC_ARM_REG_PC):08X}'
    finally:
        u.hook_del(hook)
    return {'states': states, 'native_update_calls': tick, 'error': error,
            'executed_addresses': sorted(trace), 'texture_decode_and_GPU_not_executed': True,
            'controlled_native_timeline_input_not_actual_playback': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm, ram = rom.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    clean = NdsImage.open('work/clean.nds')
    rows = []
    paths = ('/FLS/logo.fls', '/FLS/M20.fls', '/FLS/M22.fls', '/FLS/M24.fls', '/m02_03.fls')
    if args.all:
        paths = sorted(path for _, path, _ in rom.iter_files() if path.casefold().endswith('.fls'))
    for path in paths:
        result = case(rom, arm, ram, path, inspect=inspect_frames)
        frames = result.get('additional_scoped_inspection', result)
        source = case(clean, arm, ram, path, inspect=inspect_frames)
        original = source.get('additional_scoped_inspection', source)
        equal = frames == original
        rows.append({'path': path, 'frames': frames, 'clean_source_native_states_and_geometry_exact': equal,
                     'original_comparison_error': original.get('error')})
        (ROOT / 'progress.json').write_text(json.dumps({'files': len(rows), 'total': len(paths),
                                                       'path': path, 'exact_clean': equal, 'error': frames.get('error')}) + '\n', encoding='utf-8')
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'cases': rows,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / ('all_files_proof.json' if args.all else 'exploration.json')).write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps([{'path': r['path'], 'states': len(r['frames'].get('states', [])),
                       'ticks': r['frames'].get('native_update_calls'), 'error': r['frames'].get('error'),
                       'exact_clean': r['clean_source_native_states_and_geometry_exact']}
                      for r in rows], indent=2))


if __name__ == '__main__':
    main()
