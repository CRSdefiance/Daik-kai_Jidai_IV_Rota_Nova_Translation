"""Continuous original update/load/decode/upload/cleanup with explicit DMA model.

Geometry drawing, hardware timing and GPU pixels are outside this lifecycle test.
"""

import argparse
import json
import struct
from itertools import pairwise
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP
from scripts.research_fls_stream_v310 import SNAPSHOT, case
from scripts.research_fls_upload_v332 import ROM, VRAM, VRAM_SIZE

ROOT = Path('work/analysis/fls_lifetime_v335')


def inspect_lifetime(rom):
    def inspect(u, obj):
        u.mem_map(0x04000000, 0x1000)
        u.mem_map(VRAM, VRAM_SIZE)
        u.mem_write(VRAM, b'\xA5' * VRAM_SIZE)
        pending, live, events = [], {'texture': {}, 'palette': {}}, []
        freed_keys, reused = {'texture': set(), 'palette': set()}, 0
        maximum, dma_count, cpu_count, frame = 0, 0, 0, 0
        texture_free = struct.unpack('<I', u.mem_read(0x021702E8, 4))[0]
        palette_free = struct.unpack('<I', u.mem_read(0x021702F0, 4))[0]

        def write(uc, access, address, size, value, _):
            if 0x040000B0 <= address < 0x040000E0 and (address - 0x040000B0) % 12 == 8:
                assert size == 4
                if value & 0x80000000:
                    pending.append((address, value))

        def code(uc, address, size, _):
            nonlocal maximum, dma_count, cpu_count, reused
            while pending:
                control_address, control = pending.pop(0)
                assert control & 0x3FE00000 == 0x04000000
                count = control & 0x1FFFFF
                assert count
                length = count * 4
                source, destination = struct.unpack('<2I', uc.mem_read(control_address - 8, 8))
                assert source % 4 == destination % 4 == 0
                assert BASE <= source < source + length <= BASE + 0x800000
                assert VRAM <= destination < destination + length <= VRAM + VRAM_SIZE
                uc.mem_write(destination, bytes(uc.mem_read(source, length)))
                uc.mem_write(control_address, struct.pack('<I', control & ~0x80000000))
                dma_count += 1
            if address in (BASE + 0xFFF5C, BASE + 0xFFFC4):
                kind = 'palette' if address == BASE + 0xFFF5C else 'texture'
                key = uc.reg_read(UC_ARM_REG_R0)
                assert key and key not in live[kind], f'Invalid/repeated live allocation {kind}/{key:X}'
                start = (key & 0xFFFF) * 8
                length = ((key >> 16) & (0x7FFF if kind == 'texture' else 0xFFFF)) * (16 if kind == 'texture' else 8)
                assert length > 0
                live[kind][key] = [start, start + length]
                ordered = sorted(live[kind].values())
                assert all(a[1] <= b[0] for a, b in pairwise(ordered))
                recycled = key in freed_keys[kind]
                reused += recycled
                events.append({'frame': frame, 'operation': 'allocate', 'kind': kind, 'key': key,
                               'interval': live[kind][key], 'previously_freed_key_reused': recycled})
                maximum = max(maximum, len(live['texture']))
            elif address in (texture_free, palette_free):
                kind = 'texture' if address == texture_free else 'palette'
                key = uc.reg_read(UC_ARM_REG_R0)
                assert key in live[kind], f'Free of untracked {kind}/{key:X}'
                interval = live[kind].pop(key)
                freed_keys[kind].add(key)
                events.append({'frame': frame, 'operation': 'free', 'kind': kind, 'key': key, 'interval': interval})
            elif address == BASE + 0xE2910:
                destination = uc.reg_read(UC_ARM_REG_R1)
                length = uc.reg_read(UC_ARM_REG_R2)
                if VRAM <= destination < VRAM + VRAM_SIZE:
                    assert destination + length <= VRAM + VRAM_SIZE
                    cpu_count += 1

        hook = u.hook_add(UC_HOOK_CODE, code)
        observer = u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0x04000000, end=0x04000FFF)

        def invoke(offset, *args):
            saved = {r: u.reg_read(r) for r in SAVED}
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
                u.reg_write(register, value)
            u.emu_start(BASE + offset, STOP, count=2000000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
            assert all(u.reg_read(r) == v for r, v in saved.items())
            return u.reg_read(UC_ARM_REG_R0)

        try:
            heap = struct.unpack_from('<I', rom.read_file('/__arm9__.bin'), 0xD2D38)[0]
            invoke(0xFE71C, heap, 0x40000)
            pending_at_end = None
            for frame in range(1, 20001):
                returned = invoke(0xFD478, obj)
                if returned == 3:
                    pending_at_end = {'active': struct.unpack('<i', u.mem_read(0x0237E924, 4))[0],
                                      'head': struct.unpack('<h', u.mem_read(0x0237E908, 2))[0]}
                    break
                assert returned in (1, 2)
                invoke(0xFE218)
                invoke(0xFE138)
                assert struct.unpack('<h', u.mem_read(0x0237E904, 2))[0] == 0
            else:
                raise ValueError('Continuous native update did not finish within20000 calls')
            invoke(0xFDF00, obj)
            assert not live['texture'] and not live['palette']
            assert struct.unpack('<i', u.mem_read(0x0237E924, 4))[0] == -1
            assert struct.unpack('<h', u.mem_read(0x0237E908, 2))[0] == -1
            return {'continuous_native_update_calls': frame, 'native_terminal_state': 3,
                    'allocation_free_events': events, 'freed_keys_reused_count': reused,
                    'maximum_live_texture_allocations': maximum,
                    'modeled_immediate_DMA_copies': dma_count, 'original_CPU_copy_calls': cpu_count,
                    'pending_jobs_at_timeline_end_before_original_cleanup': pending_at_end,
                    'original_cleanup_leaves_no_tracked_live_keys_or_pending_jobs': True,
                    'all_live_native_allocation_intervals_nonoverlapping': True,
                    'all_update_service_cleanup_returns_saved_registers_stack_pass': True,
                    'geometry_VBlank_hardware_timing_GPU_aliases_and_pixels_not_modeled': True}
        finally:
            u.hook_del(hook)
            u.hook_del(observer)
    return inspect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, ram = current.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    paths = sorted(path for _, path, _ in current.iter_files() if path.casefold().endswith('.fls')) if args.all else ['/FLS/M22.fls']
    rows = []
    for path in paths:
        pair = [case(rom, arm, ram, path, inspect=inspect_lifetime(rom)) for rom in (current, clean)]
        inspections = [r.get('additional_scoped_inspection') for r in pair]
        if not all(inspections):
            (ROOT / 'failure.json').write_text(json.dumps({'path': path, 'results': pair}, indent=2) + '\n', encoding='utf-8')
            raise ValueError('Native lifetime failure: ' + path)
        same_lifetime = [{k: v for k, v in r.items() if k not in ('modeled_immediate_DMA_copies', 'original_CPU_copy_calls')}
                         for r in inspections]
        assert same_lifetime[0] == same_lifetime[1]
        rows.append({'path': path, 'current': inspections[0], 'clean': inspections[1],
                     'current_clean_native_allocation_lifetimes_exact': True})
        (ROOT / 'progress.json').write_text(json.dumps({'files': len(rows), 'total': len(paths), 'path': path}) + '\n', encoding='utf-8')
        print(f'Native lifetime files {len(rows)}/{len(paths)}: {path}', flush=True)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'cases': rows,
             'continuous_native_lifecycle_with_explicit_immediate_DMA_and_no_geometry_VBlank_GPU': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / ('all_lifetimes_proof.json' if args.all else 'exploration.json')).write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
