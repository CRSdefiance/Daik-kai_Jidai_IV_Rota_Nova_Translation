"""Original queued palette/pixel stream decode before any GPU upload."""

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
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP
from scripts.research_fls_stream_v310 import ROM, SNAPSHOT, case

ROOT = Path('work/analysis/fls_payload_v311')


def inspect_payload(rom, path, index, kind):
    raw = rom.read_file(path)
    table, count, payload = struct.unpack_from('<3I', raw, 4)
    assert index < count
    record = struct.unpack_from('<6I', raw, table + index * 24)
    offset, stored_bytes = record[2:4] if kind == 'palette' else record[4:6]
    compressed = bool(struct.unpack_from('<I', raw)[0] & 0x80)
    expected = decompress_lz10(raw[payload + offset:]) if compressed else raw[payload + offset:payload + offset + stored_bytes]
    width, height, pixel_type = record[0] >> 16, record[1] & 0xFFFF, record[0] & 0xFFFF
    storage_width = 1 << max(3, (width - 1).bit_length())
    storage_height = 1 << max(3, (height - 1).bit_length())
    output_bytes = record[3] if kind == 'palette' else storage_width * storage_height * (4, 8, 16)[pixel_type] // 8
    assert len(expected) == output_bytes

    def inspect(u, obj):
        trace = set()
        saved = {register: u.reg_read(register) for register in SAVED}
        debug = []

        def observe(uc, addr, size, data):
            trace.add(addr)
            if output_bytes == 131072 and addr in (BASE + 0xFE250, BASE + 0xFE2CC, BASE + 0xFE360):
                from unicorn.arm_const import UC_ARM_REG_R8

                pointer = uc.reg_read(UC_ARM_REG_R8)
                debug.append({'PC': addr, 'R8': pointer,
                              'job': list(struct.unpack('<5I', uc.mem_read(pointer, 20))),
                              'context': list(struct.unpack('<8I', uc.mem_read(0x0237E90C, 32)))})

        hook = u.hook_add(UC_HOOK_CODE, observe)
        try:
            # Recreate the exact movie allocator initialization from D2BD4.
            # The town snapshot's old movie heap has been reused by gameplay.
            arm = rom.read_file('/__arm9__.bin')
            heap = struct.unpack_from('<I', arm, 0xD2D38)[0]
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, heap)
            u.reg_write(UC_ARM_REG_R1, 0x40000)
            u.emu_start(BASE + 0xFE71C, STOP, count=100000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, obj + 0x1B4)
            u.reg_write(UC_ARM_REG_R1, 0x02468000)  # declared inert future-upload destination
            u.reg_write(UC_ARM_REG_R2, payload + offset)
            # Original FFFEC derives pixel output size from padded dimensions
            # and format; record+14 is the stored compressed slot size.
            u.reg_write(UC_ARM_REG_R3, output_bytes)
            u.emu_start(BASE + (0xFFB7C if kind == 'palette' else 0xFFC48), STOP, count=100000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP
            completed = struct.unpack_from('<I', arm, 0xFE20C)[0]
            actual, chunks = bytearray(output_bytes), []
            for _ in range((output_bytes + 0x83FF) // 0x8400 + 2):
                u.reg_write(UC_ARM_REG_LR, STOP)
                u.emu_start(BASE + 0xFE218, STOP, count=2000000)
                assert u.reg_read(UC_ARM_REG_PC) == STOP, 'CPU decoder did not return within bound'
                entries = struct.unpack('<h', u.mem_read(0x0237E904, 2))[0]
                assert entries == 1, f'Expected one completed CPU upload job, got {entries}'
                kind_value, target, source, work, length = struct.unpack('<5I', u.mem_read(completed, 20))
                assert kind_value == (1 if kind == 'palette' else 0)
                relative = target - 0x02468000
                assert 0 <= relative < output_bytes and 0 < length <= output_bytes - relative
                # Partial native requests overlap future output. Later requests
                # overwrite those spans; stop when the original queue is idle,
                # not when summed request lengths reach the output size.
                actual[relative:relative + length] = u.mem_read(source, length)
                chunks.append({'type': kind_value, 'destination': target, 'source': source, 'work': work, 'bytes': length})
                active = struct.unpack('<i', u.mem_read(0x0237E924, 4))[0]
                pending = struct.unpack('<h', u.mem_read(0x0237E908, 2))[0]
                if active == -1 and pending == -1:
                    break
            else:
                raise ValueError('Native payload queue did not reach idle')
            if len(actual) != len(expected) or actual != expected:
                token = path.replace('/', '_') + f'_{index}_{kind}'
                (ROOT / (token + '_actual.bin')).write_bytes(actual)
                (ROOT / (token + '_expected.bin')).write_bytes(expected)
                (ROOT / (token + '_chunks.json')).write_text(json.dumps(chunks, indent=2) + '\n', encoding='utf-8')
                (ROOT / (token + '_context.json')).write_text(json.dumps(debug, indent=2) + '\n', encoding='utf-8')
                raise ValueError(f'Complete decoded bytes differ at {next((n for n in range(min(len(actual),len(expected))) if actual[n] != expected[n]), None)}')
            assert u.reg_read(UC_ARM_REG_SP) == STACK
            assert all(u.reg_read(register) == value for register, value in saved.items())
            assert bytes(u.mem_read(STACK - 8192, 32)) == bytes(u.mem_read(STACK, 32)) == b'\xA5' * 32
            return {'length': len(actual), 'chunks': chunks,
                    'pass': True, 'decoded_bytes_sha256': sha(actual),
                    'native_original_movie_heap_reinitialized': [heap, 0x40000],
                    'native_saved_register_stack_and_outer_guards_preserved': True,
                    'executed_native_addresses': sorted(trace), 'expected_bytes': len(expected)}
        except (AssertionError, UcError, ValueError) as error:
            return {'pass': False, 'error': str(error), 'PC': u.reg_read(UC_ARM_REG_PC),
                    'expected_bytes': len(expected), 'executed_native_addresses': sorted(trace)}
        finally:
            u.hook_del(hook)

    return inspect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='All260 compressed textures; raw-root exploration remains separate.')
    parser.add_argument('--largest', action='store_true', help='Only the131072-byte M22 background pixel case.')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm, ram = rom.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    cases = []
    selections = [('/FLS/logo.fls', 3), ('/FLS/M22.fls', 1), ('/m02_03.fls', 0)]
    if args.all:
        selections = []
        for _, path, raw in rom.iter_files():
            if path.casefold().endswith('.fls') and struct.unpack_from('<I', raw)[0] & 0x80:
                selections.extend((path, index) for index in range(struct.unpack_from('<I', raw, 8)[0]))
        assert len(selections) == 260
    elif args.largest:
        selections = [('/FLS/M22.fls', 0)]
    for path, index in selections:
        for kind in (('pixels',) if args.largest else ('palette', 'pixels')):
            result = case(rom, arm, ram, path, inspect=inspect_payload(rom, path, index, kind))
            cases.append({'path': path, 'texture': index, 'kind': kind,
                          'inspection': result.get('additional_scoped_inspection', result)})
            if args.largest:
                cases[-1]['native_file_events'] = result.get('events', [])
            if args.all and len(cases) % 20 == 0:
                (ROOT / 'all_compressed_progress.json').write_text(json.dumps({
                    'completed_cases': len(cases), 'total_cases': 520,
                    'failures': sum(not r['inspection'].get('pass') for r in cases),
                }) + '\n', encoding='utf-8')
                print(f'Native decoded cases: {len(cases)}/520; failures {sum(not r["inspection"].get("pass") for r in cases)}', flush=True)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'cases': cases,
             'controlled_payload_queue_parameters_and_upload_destination': True,
             'GPU_upload_not_executed': True, 'ROM_modified': False, 'full_goal_complete': False}
    filename = 'all_compressed_proof.json' if args.all else ('largest_case.json' if args.largest else 'exploration.json')
    (ROOT / filename).write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    if args.all:
        print(json.dumps({'cases': len(cases), 'passing': sum(bool(r['inspection'].get('pass')) for r in cases),
                          'failures': [{k: v for k, v in row.items() if k != 'executed_native_addresses'}
                                       for row in cases if not row['inspection'].get('pass')]}))
    else:
        print(json.dumps([{**r, 'inspection': {k: v for k, v in r['inspection'].items() if k != 'executed_native_addresses'}}
                          for r in cases], indent=2))


if __name__ == '__main__':
    main()
