"""Execute the entire native promotional initializer and verify all thirty names."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_promotional_item_defaults import END, OWNER


def cstring(source, pointer):
    offset = pointer - BASE
    return source[offset:source.index(0, offset)]


def verify(source, seed, machine=None):
    if not 0 <= seed <= 0xFFFFFFFF:
        raise ValueError('Native RNG state must be an unsigned word')
    machine = machine if machine is not None else machine_for(source)
    rng = struct.unpack_from('<I', source, 0xD9858)[0]
    flag = struct.unpack_from('<I', source, 0x51A20)[0]
    machine.mem_write(rng, struct.pack('<I', seed))
    machine.mem_write(flag, bytes(4))
    machine.mem_write(OWNER - 32, b'\xA5' * (END - OWNER + 64))
    machine.reg_write(UC_ARM_REG_R0, OWNER)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    preserved = {r: machine.reg_read(r) for r in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                                                UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
                                                UC_ARM_REG_R10, UC_ARM_REG_R11)}
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address < BASE + len(source):
            raise ValueError(f'Full promotional initializer escaped native code: {address:08X}')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((OWNER + 4 <= address < address + size <= END)
                or STACK - 0x1000 <= address < address + size <= STACK
                or rng <= address < address + size <= rng + 4):
            raise ValueError(f'Full promotional initializer writes outside owned state: {address:08X}')

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    try:
        machine.emu_start(BASE + 0x102C24, STOP, count=200000)
    finally:
        for handle in handles:
            machine.hook_del(handle)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or any(machine.reg_read(r) != value for r, value in preserved.items())
            or not {0x519D4, 0xD9834, 0x2F04, 0xD7650, 0xD9B88, 0xD7720} <= executed
            or bytes(machine.mem_read(OWNER - 32, 32)) != b'\xA5' * 32
            or bytes(machine.mem_read(END, 32)) != b'\xA5' * 32):
        raise ValueError('Full native promotional return, RNG/formatting or guards differ')
    selected = list(struct.unpack('<5I', machine.mem_read(OWNER + 4, 20)))
    if len(set(selected)) != 5 or any(not 188 <= n < 198 for n in selected):
        raise ValueError('Native promotional selection must choose five distinct default items')
    names = struct.unpack_from('<I', source, 0x102E44)[0] - BASE
    formats = struct.unpack_from('<I', source, 0x102E4C)[0] - BASE
    defaults = [cstring(source, struct.unpack_from('<I', source, names + i * 8)[0]) for i in range(10)]
    templates = [cstring(source, struct.unpack_from('<I', source, formats + i * 4)[0]) for i in range(4)]
    expected = defaults + [template.replace(b'%s', defaults[item - 188]) for item in selected for template in templates]
    rows = []
    for index, value in enumerate(expected):
        pointer = OWNER + 0x22 + index * 32
        field = bytes(machine.mem_read(pointer, 32))
        record = bytes(machine.mem_read(OWNER + 0x3E4 + index * 24, 24))
        if len(value) >= 32 or field.split(b'\0', 1)[0] != value or struct.unpack_from('<I', record)[0] != pointer:
            raise ValueError('Native generated promotional name loses characters, termination or metadata ownership')
        rows.append({'index': index + 188, 'name': value.decode('cp932'), 'name_hex': value.hex(),
                     'name_byte_length': len(value), 'metadata_hex': record.hex(),
                     'complete_native_name_and_metadata_pointer_pass': True})
    return {'target_arm9_sha256': sha(source), 'seed': seed, 'selected_default_indices': selected,
            'names': rows, 'full_native_initializer_return_rng_copy_sprintf_and_guards_pass': True,
            'native_callee_saved_registers_and_stack_preserved': True,
            'rng_state_is_controlled_input': True,
            'native_rendering_download_states_and_physical_gameplay_verified': False}


def main():
    source = Path('work/analysis/item_parent_layout_research_arm9.bin').read_bytes()
    seeds = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF] + list(range(2, 34))
    cases = [verify(source, seed) for seed in seeds]
    seen = {n for case in cases for n in case['selected_default_indices']}
    if seen != set(range(188, 198)):
        raise ValueError('Native seed cases miss a promotional base name')
    report = {'status': 'pass-full-native-promotional-initialization', 'target_arm9_sha256': sha(source),
              'cases': cases, 'selected_default_name_coverage': sorted(seen),
              'name_cases': len(cases) * 30, 'max_name_bytes': max(r['name_byte_length'] for c in cases for r in c['names']),
              'limitations': ['Native complete RNG/selection/uniqueness/template/metadata/copy/sprintf loops execute without getter callbacks.',
                              'Seeds and owner storage are runtime inputs; this is not all possible random sequences.',
                              'Generated map rendering/COMMON consumers and downloaded-save states still require verification.',
                              'Research only; V158 remains the latest combined ROM.']}
    Path('work/analysis/promotional_item_full_initialization_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"Pass: {len(cases)} complete native initializers, {report['name_cases']} complete names; max {report['max_name_bytes']}/31 bytes.")


if __name__ == '__main__':
    main()
