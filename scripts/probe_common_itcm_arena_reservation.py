"""Execute native SDK arena bounds for the research resident extension."""

import json
import struct
from pathlib import Path

import ndspy.code
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_common_display_name_hook import prepare as name_hook
from scripts.probe_common_scoped_word_wrap_hook import prepare as scoped_hook


def initialize(source):
    machine = machine_for(source)
    flag = struct.unpack_from('<I', source, 0xE48DC)[0]
    machine.mem_write(flag, b'\0' * 4)
    machine.mem_write(0x027FFDA0, b'\xa5' * 72)
    machine.emu_start(BASE + 0xE47C8, STOP, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native arena initializer fails to return with intact stack')
    table = bytes(machine.mem_read(0x027FFDA0, 72))
    if bytes(machine.mem_read(flag, 4)) != b'\x01\0\0\0':
        raise ValueError('Native arena initializer fails to set its initialization flag')
    machine.emu_start(BASE + 0xE47C8, STOP, count=10000)
    if bytes(machine.mem_read(0x027FFDA0, 72)) != table:
        raise ValueError('Repeated native initialization changes established arena bounds')
    return {'low': list(struct.unpack('<9I', table[:36])),
            'high': list(struct.unpack('<9I', table[36:])),
            'native_initializer_executed': True, 'repeat_preserves_bounds': True}


def bounds(source):
    values = []
    for offset in (0xE450C, 0xE45F4):
        machine = machine_for(source)
        machine.reg_write(UC_ARM_REG_R0, 3)
        machine.emu_start(BASE + offset, STOP, count=1000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Native arena getter fails to return with intact stack')
        values.append(machine.reg_read(UC_ARM_REG_R0))
    return values


def verify(source, expected_low):
    low, high = bounds(source)
    resident = ndspy.code.MainCodeFile(source, BASE).sections[1]
    end = resident.ramAddress + len(resident.data) + resident.bssSize
    if low != expected_low or high != BASE or low != (end + 31) & ~31:
        raise ValueError('Native arena bounds fail to reserve the complete aligned resident extent')
    if end > 0x01FFA000 or low > 0x01FFA000:
        raise ValueError('Reserved resident extent overlaps native overlay destination')
    return {'native_arena_low': low, 'native_arena_high': high,
            'resident_end': end, 'padding_bytes': low - end,
            'alignment': 32, 'native_getters_executed': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    named, _ = name_hook(source)
    scoped, _ = scoped_hook(source)
    original_runtime, named_runtime, scoped_runtime = [initialize(raw) for raw in (source, named, scoped)]
    for runtime, low in ((original_runtime, 0x01FF9B20),
                         (named_runtime, 0x01FF9BE0), (scoped_runtime, 0x01FF9D60)):
        if runtime['low'][3] != low or runtime['high'][3] != BASE:
            raise ValueError('Native initialization stores incorrect reserved arena bounds')
        if runtime['high'] != original_runtime['high'] or any(
                runtime['low'][i] != original_runtime['low'][i] for i in range(9) if i != 3):
            raise ValueError('Research reservation changes unrelated arena bounds')
    report = {'status': 'pass-native-initial-arena-bounds-research-only',
              'original': verify(source, 0x01FF9B20),
              'name_hook': verify(named, 0x01FF9BE0),
              'scoped_hook': verify(scoped, 0x01FF9D60),
              'runtime_initialization': {'original': original_runtime,
                                         'name_hook': named_runtime, 'scoped_hook': scoped_runtime},
              'source_sha256': sha(source), 'research_sha256': sha(scoped),
              'limitations': 'Executes native initial getters and full arena-bound initialization at 020E47C8, including native setters and repeat-call guard. Hardware environment/global inputs are diagnostic RAM. Heap allocation, later computed writes, physical cache behavior and cold boot remain unproven. No playable ROM is changed.'}
    Path('work/analysis/common_itcm_arena_reservation_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Native arena bounds reserve both research extensions with 32-byte alignment.')


if __name__ == '__main__':
    main()
