"""Reserve a separate SDK-loaded name section outside BSS, heap and DTCM scratch."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
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
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_common_itcm_arena_reservation import initialize


def prepare():
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    combined = Path('work/analysis/joint_square_shopkeeper_research_arm9.bin').read_bytes()
    joint = json.loads(Path('work/analysis/joint_name_runtime_pool_proof.json').read_text(encoding='utf-8'))
    shop = json.loads(Path('work/analysis/joint_square_shopkeeper_native_proof.json').read_text(encoding='utf-8'))
    if (sha(source) != '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75'
            or sha(combined) != shop['research_arm9_sha256']):
        raise ValueError('Exact V147 and source-reviewed composed research required')
    before, code, original = [MainCodeFile(raw, BASE) for raw in (source, combined, clean)]
    if len(code.sections) != 3 or code.codeSettingsOffs is None:
        raise ValueError('Original three-section ownership differs')
    settings = code.codeSettingsOffs
    bss_start, pool_base = struct.unpack_from('<2I', source, settings + 12)
    if pool_base != 0x02387A20 or struct.unpack_from('<I', source, 0xE45DC)[0] != pool_base:
        raise ValueError('Native main BSS end / initial heap lower boundary differs')
    used = joint['used_aligned_bytes']
    payload = bytes(code.sections[2].data[:used])
    if used != 1480 or code.sections[2].ramAddress != 0x027E0000:
        raise ValueError('Reviewed complete payload differs')
    extent = (used + 31) & ~31
    heap_low = pool_base + extent
    moves = joint['pointer_moves']
    for move in moves:
        delta = move['runtime_pointer'] - 0x027E0000
        if (not 0 <= delta < used or payload[delta:].split(b'\0', 1)[0].decode('cp932') != move['text']
                or struct.unpack_from('<I', combined, move['field'])[0] != move['runtime_pointer']):
            raise ValueError('Complete inherited owner/field differs')
        struct.pack_into('<I', code.sections[0].data, move['field'], pool_base + delta)
    # Restore native scratch and SDK data. The last 92 original SDK bytes must
    # already be preserved; translated names were never legitimate scratch state.
    if bytes(before.sections[2].data[1540:]) != bytes(original.sections[2].data[1540:]):
        raise ValueError('Original SDK trailing state differs')
    code.sections[2].data = bytearray(original.sections[2].data)
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, heap_low)
    code.sections.append(MainCodeFile.Section(payload + bytes(extent - used), pool_base, 0))
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    if (len(loaded.sections) != 4 or bytes(loaded.sections[1].data) != bytes(before.sections[1].data)
            or bytes(loaded.sections[2].data) != bytes(original.sections[2].data)
            or bytes(loaded.sections[3].data) != payload + bytes(extent - used)):
        raise ValueError('Serialization changes unrelated resident/SDK or complete new section')
    expected_main = bytearray(code.sections[0].data)
    for offset in (settings, settings + 4):
        expected_main[offset:offset + 4] = saved[offset:offset + 4]
    if bytes(loaded.sections[0].data) != expected_main:
        raise ValueError('Serialization changes unexpected static code/settings')
    if saved[settings + 12:settings + 20] != source[settings + 12:settings + 20]:
        raise ValueError('New persistent data changes original BSS clearing boundaries')
    return saved, {'base': pool_base, 'used_bytes': used, 'reserved_bytes': extent,
                   'heap_low': heap_low, 'bss_start': bss_start, 'moves': moves,
                   'source_sha256': sha(source)}, shop


def main():
    saved, placement, shop = prepare()
    machine = machine_for(saved)
    machine.mem_map(0x01FF0000, 0x10000)
    pool_base, extent = placement['base'], placement['reserved_bytes']
    machine.mem_write(pool_base, b'\xA5' * extent)

    def cache(uc, address, size, _):
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    hook = machine.hook_add(UC_HOOK_CODE, cache)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    machine.hook_del(hook)
    machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
    expected_pool = bytes(MainCodeFile(saved, BASE).sections[3].data)
    if bytes(machine.mem_read(pool_base, extent)) != expected_pool:
        raise ValueError('Actual SDK copy/BSS clearing loses persistent names')
    runtime_before = initialize(NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin'))
    runtime_after = initialize(saved)
    if (runtime_after['low'][0] != placement['heap_low']
            or runtime_after['high'] != runtime_before['high']
            or any(runtime_after['low'][i] != runtime_before['low'][i] for i in range(1, 9))):
        raise ValueError('Native SDK arena reservation changes unrelated bounds')
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    arena_table_before = struct.unpack('<18I', machine.mem_read(0x027FFDA0, 72))
    machine.emu_start(BASE + 0xE47C8, STOP, count=10000)
    actual_arenas = struct.unpack('<18I', machine.mem_read(0x027FFDA0, 72))
    active = (0, 2, 3, 4, 5, 6)
    unused = (1, 7, 8)
    if (any(actual_arenas[i] != runtime_after['low'][i]
            or actual_arenas[i + 9] != runtime_after['high'][i] for i in active)
            or any(actual_arenas[i] != arena_table_before[i]
                   or actual_arenas[i + 9] != arena_table_before[i + 9] for i in unused)
            or bytes(machine.mem_read(pool_base, extent)) != expected_pool):
        raise ValueError(f'Startup-loaded arenas differ: actual={actual_arenas}, expected_low={runtime_after["low"]}, expected_high={runtime_after["high"]}, pool_preserved={bytes(machine.mem_read(pool_base, extent)) == expected_pool}')
    names = []
    previous = {r['index']: r['complete_text'] for r in shop['native_given_name_cases']}
    for index in range(207):
        pointer = ordinary_getter(saved, index, machine)
        text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
        if text != previous[index]:
            raise ValueError('Persistent name section changes reviewed ordinary name')
        names.append({'index': index, 'pointer': pointer, 'text': text})
    scratch, text_ptr, output, bounds, cursor = (0x02450000, 0x02451000, 0x02452000, 0x02453000, 0x02454000)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_R0, scratch)
    machine.emu_start(BASE + 0xCAA4C, STOP, count=10000)
    font = struct.unpack_from('<I', saved, 0xD5088)[0]
    machine.mem_write(font + 4, struct.pack('<2I', 6, 12))
    machine.mem_write(text_ptr, b'AB\0')
    machine.mem_write(bounds, struct.pack('<I', 0xFD))
    machine.mem_write(cursor, struct.pack('<I', 0))
    machine.mem_write(STACK, struct.pack('<I', cursor))
    for reg, value in ((UC_ARM_REG_R0, scratch), (UC_ARM_REG_R1, text_ptr),
                       (UC_ARM_REG_R2, output), (UC_ARM_REG_R3, bounds)):
        machine.reg_write(reg, value)
    scratch_writes = []

    def write(uc, access, address, size, value, _):
        if pool_base <= address < pool_base + extent:
            raise ValueError('Native scratch path writes persistent names')
        if 0x027E0000 <= address < 0x027E0600:
            scratch_writes.append(address)

    hook = machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xCA780, BASE + 0xCA810, count=100000)
    machine.hook_del(hook)
    if not scratch_writes or bytes(machine.mem_read(pool_base, extent)) != expected_pool:
        raise ValueError('Native scratch render fails persistence check')
    for move in placement['moves']:
        pointer = struct.unpack_from('<I', saved, move['field'])[0]
        selected = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
        if selected != move['text']:
            raise ValueError('Scratch rendering loses persistent complete text')
    report = {'status': 'pass-research-reserved-autoload-names-startup-arena-scratch',
              'research_sha256': sha(saved), 'placement': placement,
              'native_given_names': names, 'native_arenas_before': runtime_before,
              'native_arenas_after': runtime_after, 'scratch_write_count': len(scratch_writes),
              'scratch_preserves_complete_pool': True, 'candidate_changed': False,
              'same_machine_sdk_arena_initialization_preserves_names': True,
              'same_machine_active_arena_indices_verified': list(active),
              'same_machine_unused_arena_indices_preserved': list(unused),
              'limits': ['SDK cache maintenance is contracted; physical boot/gameplay remain pending.',
                         'Repeated item/name caller and raster checks, broader pointer producers and strict integration remain pending.']}
    Path('work/analysis/persistent_name_section_arm9.bin').write_bytes(saved)
    Path('work/analysis/persistent_name_section_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(placement["moves"])} names in separately reserved section {pool_base:08X}..{placement["heap_low"]:08X}; startup, native arenas and scratch persistence pass.')


if __name__ == '__main__':
    main()
