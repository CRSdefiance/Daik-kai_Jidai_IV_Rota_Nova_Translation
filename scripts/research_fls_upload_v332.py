"""Native FLS decode/upload service with explicit immediate DMA and LCDC RAM.

This verifies CPU-side transfers, not bank aliases seen by a GPU or final pixels.
"""

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
from scripts.research_fls_stream_v310 import SNAPSHOT, case

ROOT = Path('work/analysis/fls_upload_v332')
ROM = Path('out/all_routes_combined_v326_candidate.nds')
IO, VRAM, VRAM_SIZE = 0x04000000, 0x06800000, 0xA4000


def inspect_payload(rom, path, index, kind):
    raw = rom.read_file(path)
    table, count, payload = struct.unpack_from('<3I', raw, 4)
    assert index < count and struct.unpack_from('<I', raw)[0] & 0x80
    record = struct.unpack_from('<6I', raw, table + index * 24)
    offset = record[2] if kind == 'palette' else record[4]
    expected = decompress_lz10(raw[payload + offset:])

    def inspect(u, obj):
        u.mem_map(IO, 0x2000)
        u.mem_map(VRAM, VRAM_SIZE)
        u.mem_write(VRAM, b'\xA5' * VRAM_SIZE)
        pending, transfers, requests = [], [], []

        def dma_write(uc, access, address, size, value, _):
            if 0x040000B0 <= address < 0x040000E0 and (address - 0x040000B0) % 12 == 8:
                if size != 4:
                    raise ValueError('Unmapped DMA control-write width')
                if value & 0x80000000:
                    pending.append((address, value))

        def code(uc, address, size, _):
            while pending:
                control_address, control = pending.pop(0)
                # Original SDK requests incrementing, immediate32-bit copies.
                if control & 0x3FE00000 != 0x04000000:
                    raise ValueError(f'Unmapped DMA mode {control:08X}')
                count = control & 0x1FFFFF
                if count == 0:
                    raise ValueError('Unbounded zero-count DMA not permitted')
                length = count * 4
                source, destination = struct.unpack('<2I', uc.mem_read(control_address - 8, 8))
                assert source % 4 == destination % 4 == 0
                assert BASE <= source < source + length <= BASE + 0x800000
                assert VRAM <= destination < destination + length <= VRAM + VRAM_SIZE
                contents = bytes(uc.mem_read(source, length))
                uc.mem_write(destination, contents)
                uc.mem_write(control_address, struct.pack('<I', control & ~0x80000000))
                transfers.append({'channel': (control_address - 0x040000B8) // 12,
                                  'control': control, 'source': source, 'destination': destination,
                                  'bytes': length, 'source_sha256': sha(contents),
                                  'immediate_DMA_model_not_physical_transfer': True})
            if address in (BASE + 0xE21B8, BASE + 0xE208C):
                requests.append({'SDK_entry': address, 'source': uc.reg_read(UC_ARM_REG_R0),
                                 'logical_VRAM_offset': uc.reg_read(UC_ARM_REG_R1),
                                 'bytes': uc.reg_read(UC_ARM_REG_R2)})

        code_hook = u.hook_add(UC_HOOK_CODE, code)
        write_hook = u.hook_add(UC_HOOK_MEM_WRITE, dma_write, begin=IO, end=IO + 0x1FFF)

        def invoke(offset, *args, limit=2000000):
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
                u.reg_write(register, value)
            u.emu_start(BASE + offset, STOP, count=limit)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK

        try:
            arm = rom.read_file('/__arm9__.bin')
            heap = struct.unpack_from('<I', arm, 0xD2D38)[0]
            invoke(0xFE71C, heap, 0x40000)
            invoke(0xFFB7C if kind == 'palette' else 0xFFC48,
                   obj + 0x1B4, 0, payload + offset, len(expected))
            completed = struct.unpack_from('<I', arm, 0xFE20C)[0]
            chunks = []
            for _ in range((len(expected) + 0x83FF) // 0x8400 + 2):
                invoke(0xFE218)
                entries = struct.unpack('<h', u.mem_read(0x0237E904, 2))[0]
                assert entries == 1
                type_id, target, source, work, length = struct.unpack('<5I', u.mem_read(completed, 20))
                assert type_id == (1 if kind == 'palette' else 0)
                assert 0 <= target < target + length <= len(expected)
                # Native partial requests include provisional overlapping bytes.
                # Compare final destination after every original queue piece.
                chunks.append({'logical_target': target, 'source': source, 'work': work, 'bytes': length})
                invoke(0xFE138)
                assert struct.unpack('<h', u.mem_read(0x0237E904, 2))[0] == 0
                if struct.unpack('<i', u.mem_read(0x0237E924, 4))[0] == -1 and struct.unpack('<h', u.mem_read(0x0237E908, 2))[0] == -1:
                    break
            else:
                raise ValueError('Original decode/upload queue did not become idle')
            assert transfers or requests
            assert transfers and transfers[0]['bytes'] > 0
            base = transfers[0]['destination']
            actual = bytes(u.mem_read(base, len(expected)))
            assert actual == expected, f'Complete final VRAM payload differs for {path}/{index}/{kind}'
            assert bytes(u.mem_read(base - 16, 16)) == b'\xA5' * 16 if base > VRAM else True
            assert bytes(u.mem_read(base + len(expected), 16)) == b'\xA5' * 16
            touched = set()
            for transfer in transfers:
                start = transfer['destination'] - VRAM
                touched.update(range(start, start + transfer['bytes']))
            final = bytes(u.mem_read(VRAM, VRAM_SIZE))
            assert all(value == 0xA5 for offset, value in enumerate(final) if offset not in touched)
            return {'native_decode_and_upload_service_returned': True, 'SDK_upload_requests': requests,
                    'DMA_transfers': transfers, 'native_completed_chunks': chunks,
                    'modeled_LCDC_RAM_sha256': sha(bytes(u.mem_read(VRAM, VRAM_SIZE))),
                    'expected_payload_bytes': len(expected), 'expected_payload_sha256': sha(expected),
                    'native_physical_destination_base': base,
                    'complete_final_modeled_VRAM_bytes_match_independent_decode': True,
                    'all_modeled_VRAM_outside_DMA_ranges_preserved': True,
                    'GPU_bank_aliases_and_final_pixels_not_verified': True}
        finally:
            u.hook_del(code_hook)
            u.hook_del(write_hook)

    return inspect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--largest', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm, ram = rom.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    cases = []
    selections = [('/FLS/logo.fls', 3)]
    if args.all:
        selections = [(path, index) for _, path, raw in rom.iter_files()
                      if path.casefold().endswith('.fls') and struct.unpack_from('<I', raw)[0] & 0x80
                      for index in range(struct.unpack_from('<I', raw, 8)[0])]
        assert len(selections) == 260
    elif args.largest:
        selections = [('/FLS/M22.fls', 0)]
    for path, index in selections:
        for kind in (('pixels',) if args.largest else ('palette', 'pixels')):
            result = case(rom, arm, ram, path, inspect=inspect_payload(rom, path, index, kind))
            inspection = result.get('additional_scoped_inspection', result)
            cases.append({'path': path, 'texture': index, 'kind': kind, 'inspection': inspection})
            if args.all and len(cases) % 20 == 0:
                (ROOT / 'progress.json').write_text(json.dumps({'completed': len(cases), 'total': 520,
                                                               'failed': sum(not r['inspection'].get('native_decode_and_upload_service_returned') for r in cases)}) + '\n', encoding='utf-8')
                print(f'Native upload cases {len(cases)}/520', flush=True)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'cases': cases,
             'controlled_logical_upload_offset_zero_and_immediate_DMA_LCDC_memory_are_contracts': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / ('all_upload_proof.json' if args.all else 'largest.json' if args.largest else 'exploration.json')).write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps([{'kind': r['kind'], 'pass': r['inspection'].get('native_decode_and_upload_service_returned'),
                       'error': r['inspection'].get('error'), 'PC': r['inspection'].get('stop_PC'),
                       'DMA_requests': len(r['inspection'].get('DMA_transfers', []))} for r in cases]))


if __name__ == '__main__':
    main()
