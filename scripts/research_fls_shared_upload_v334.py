"""Observed concurrent bindings plus original uploads into modeled LCDC memory."""

import argparse
import json
import struct
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
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.research_fls_concurrent_v333 import POSES, eligible, fixture, read
from scripts.research_fls_stream_v310 import SNAPSHOT, case
from scripts.research_fls_upload_v332 import ROM, VRAM, VRAM_SIZE

ROOT = Path('work/analysis/fls_shared_upload_v334')


def inspect_state(rom, path, state):
    raw = rom.read_file(path)
    table, _, payload = struct.unpack_from('<3I', raw, 4)

    def inspect(u, obj):
        def invoke(offset, *args):
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
                u.reg_write(reg, value)
            u.emu_start(BASE + offset, STOP, count=2000000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK

        heap = struct.unpack_from('<I', rom.read_file('/__arm9__.bin'), 0xD2D38)[0]
        invoke(0xFE71C, heap, 0x40000)
        bindings = fixture(state)(u, obj)
        u.mem_map(VRAM, VRAM_SIZE)
        u.mem_write(VRAM, b'\xA5' * VRAM_SIZE)
        pending, segments, requests = [], [], []
        active = None

        def add_segment(uc, source, destination, length, method):
            assert active is not None
            delta = source - active['source']
            assert 0 <= delta < delta + length <= active['bytes']
            assert VRAM <= destination < destination + length <= VRAM + VRAM_SIZE
            segments.append({'kind': active['kind'], 'logical': active['logical'] + delta,
                             'physical': destination, 'bytes': length, 'method': method})

        def writes(uc, access, address, size, value, _):
            if 0x040000B0 <= address < 0x040000E0 and (address - 0x040000B0) % 12 == 8:
                assert size == 4
                if value & 0x80000000:
                    pending.append((address, value))

        def code(uc, address, size, _):
            nonlocal active
            while pending:
                control_address, control = pending.pop(0)
                assert control & 0x3FE00000 == 0x04000000
                count = control & 0x1FFFFF
                assert count
                length = count * 4
                source, destination = struct.unpack('<2I', uc.mem_read(control_address - 8, 8))
                assert source % 4 == destination % 4 == 0
                assert BASE <= source < source + length <= BASE + 0x800000
                add_segment(uc, source, destination, length, 'immediate-modeled-DMA')
                uc.mem_write(destination, bytes(uc.mem_read(source, length)))
                uc.mem_write(control_address, struct.pack('<I', control & ~0x80000000))
            if address in (BASE + 0xE21B8, BASE + 0xE208C):
                active = {'kind': 'pixels' if address == BASE + 0xE21B8 else 'palette',
                          'source': uc.reg_read(UC_ARM_REG_R0), 'logical': uc.reg_read(UC_ARM_REG_R1),
                          'bytes': uc.reg_read(UC_ARM_REG_R2)}
                requests.append(active)
            elif address == BASE + 0xE2910:
                add_segment(uc, uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1),
                            uc.reg_read(UC_ARM_REG_R2), 'original-CPU-copy')

        code_hook = u.hook_add(UC_HOOK_CODE, code)
        write_hook = u.hook_add(UC_HOOK_MEM_WRITE, writes, begin=0x04000000, end=0x04000FFF)
        try:
            iterations = 0
            for iterations in range(1, 1001):
                if struct.unpack('<i', u.mem_read(0x0237E924, 4))[0] == -1 and struct.unpack('<h', u.mem_read(0x0237E908, 2))[0] == -1:
                    break
                invoke(0xFE218)
                count = struct.unpack('<h', u.mem_read(0x0237E904, 2))[0]
                assert 0 <= count <= 32
                if count:
                    invoke(0xFE138)
                    assert struct.unpack('<h', u.mem_read(0x0237E904, 2))[0] == 0
            else:
                raise ValueError('Shared native decoder/upload queue did not become idle')

            def retrieve(kind, logical, length):
                result = bytearray(length)
                covered = bytearray(length)
                for part in segments:
                    if part['kind'] != kind:
                        continue
                    left, right = max(logical, part['logical']), min(logical + length, part['logical'] + part['bytes'])
                    if left < right:
                        source = part['physical'] + left - part['logical']
                        result[left - logical:right - logical] = u.mem_read(source, right - left)
                        covered[left - logical:right - logical] = b'\x01' * (right - left)
                assert all(covered), f'Unmapped final {kind} span {logical:X}+{length:X}'
                return bytes(result)

            checks = []
            allocation = struct.unpack('<I', u.mem_read(obj + 4, 4))[0]
            for bound in bindings['native_allocations']:
                index = (bound['owner_relative_to_prefix'] - table) // 24
                assert index in {p['native_texture_index'] for p in eligible(state)}
                record = struct.unpack_from('<6I', raw, table + index * 24)
                width, height, kind = record[0] >> 16, record[1] & 0xFFFF, record[0] & 0xFFFF
                storage_width = 1 << max(3, (width - 1).bit_length())
                pixels = decompress_lz10(raw[payload + record[4]:])
                used = storage_width * height * (4, 8, 16)[kind] // 8
                pixel_start = bound['texture_interval'][0]
                assert retrieve('pixels', pixel_start, used) == pixels[:used], f'Visible pixel span differs: {path}/{index}'
                pal = decompress_lz10(raw[payload + record[2]:])
                assert retrieve('palette', bound['palette_interval'][0], record[3]) == pal
                checks.append({'texture': index, 'native_visible_dimensions': [width, height],
                               'visible_row_bytes_checked': used, 'palette_bytes_checked': record[3],
                               'visible_pixels_sha256': sha(pixels[:used]), 'palette_sha256': sha(pal),
                               'all_simultaneously_visible_rows_and_palette_bytes_exact': True})
            assert allocation
            return {'bindings': bindings, 'native_queue_iterations': iterations, 'SDK_requests': requests,
                    'physical_copy_segments': segments, 'complete_shared_visible_texture_checks': checks,
                    'all_native_queues_idle': True, 'timing_GPU_aliases_clipping_blending_pixels_not_modeled': True}
        finally:
            u.hook_del(code_hook)
            u.hook_del(write_hook)
    return inspect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    poses = read(POSES)
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, ram = current.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    rows = []
    movies = poses['cases'] if args.all else [next(r for r in poses['cases'] if r['path'] == '/FLS/M22.fls')]
    for movie in movies:
        states = [max(movie['frames']['states'], key=lambda s: len(eligible(s)))]
        if args.all:
            unique = {}
            for state in movie['frames']['states']:
                key = tuple((p['slot'], p['native_texture_index']) for p in eligible(state))
                if key and key not in unique:
                    unique[key] = state
            states = list(unique.values())
        for state in states:
            if not eligible(state):
                continue
            pair = [case(rom, arm, ram, movie['path'], inspect=inspect_state(rom, movie['path'], state))
                    for rom in (current, clean)]
            inspected = [r.get('additional_scoped_inspection') for r in pair]
            if not all(inspected):
                failure = {'path': movie['path'], 'tick': state['tick'], 'results': pair}
                (ROOT / 'failure.json').write_text(json.dumps(failure, indent=2) + '\n', encoding='utf-8')
                raise ValueError(f'Shared upload failed at {movie["path"]}/{state["tick"]}')
            assert inspected[0]['bindings'] == inspected[1]['bindings']
            rows.append({'path': movie['path'], 'tick': state['tick'], 'current': inspected[0],
                         'clean': inspected[1], 'current_clean_bindings_and_material_commands_exact': True})
            (ROOT / 'progress.json').write_text(json.dumps({'completed': len(rows), 'path': movie['path'],
                                                           'tick': state['tick']}) + '\n', encoding='utf-8')
            if args.all and len(rows) % 10 == 0:
                print(f'Shared upload combinations {len(rows)}/270', flush=True)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'cases': rows,
             'captured_globals_observed_poses_immediate_DMA_LCDC_memory_are_explicit_contracts': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / ('all_shared_upload_proof.json' if args.all else 'exploration.json')).write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'combinations': len(rows), 'current_clean_binding_commands_exact': True,
                      'each_ROM_shared_visible_pixel_and_palette_spans_exact': True, 'GPU_pixels_verified': False}))


if __name__ == '__main__':
    main()
