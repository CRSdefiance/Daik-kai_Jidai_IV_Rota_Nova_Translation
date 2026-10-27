"""Private item getter ABI, full tables, unsigned fallback and stack guards."""

import struct

from ndspy.code import MainCodeFile
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

from dk4tool.patch.item_interface_research import BASE, POOL
from scripts.execute_map_entity_tooltip_copy import STACK, STOP, machine_for


def verify(source, plan):
    machine = machine_for(source)
    payload = bytes(MainCodeFile(source, BASE).sections[3].data[:-48])
    machine.mem_write(POOL, payload)
    helpers = {row['kind']: row for row in plan['main_pool_helpers']}
    projected = {row['kind']: row for row in plan['item_only_projection']}
    fallback = struct.unpack_from('<I', source, 0x4A764)[0]
    supplied_pointer = 0x02460000
    calls, cases = [], []

    def code(uc, address, size, _):
        if address == BASE + 0x5528C:
            calls.append(uc.reg_read(UC_ARM_REG_R0))
            uc.reg_write(UC_ARM_REG_R0, supplied_pointer)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif not any(row['start'] <= address < row['start'] + row['bytes'] for row in helpers.values()):
            raise ValueError('Private item lookup escaped exact helper extents')

    def write(uc, access, address, size, value, _):
        if not STACK - 32 <= address < address + size <= STACK:
            raise ValueError('Private item lookup writes outside its caller stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    saved = {reg: 0x11110000 + index for index, reg in enumerate((
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    advice_count = len(plan['item_advice_projection'])
    inputs = {'role_lookup': [*range(16), -1, 16, 255],
              'type_lookup': [*range(13), -1, 13, 255],
              'advice_lookup': [*range(0xAFF, 0xAFF + advice_count), 0, 0xAFE, 0xAFF + advice_count, -1]}
    for kind, values in inputs.items():
        for value in values:
            for reg, seed in saved.items():
                machine.reg_write(reg, seed)
            machine.mem_write(STACK - 64, b'\xA5' * 64)
            machine.reg_write(UC_ARM_REG_SP, STACK)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            machine.reg_write(UC_ARM_REG_R0, value & 0xFFFFFFFF)
            machine.emu_start(helpers[kind]['start'], STOP, count=1000)
            if kind == 'role_lookup':
                expected = projected['ROLE']['target_table'] + value * 4 if 0 <= value < 16 else 0
            elif kind == 'type_lookup':
                expected = projected['CATEGORY']['compiled_pointers'][value] if 0 <= value < 13 else fallback
            else:
                expected = plan['item_advice_projection'][value - 0xAFF]['pointer'] if 0xAFF <= value < 0xAFF + advice_count else supplied_pointer
            result = machine.reg_read(UC_ARM_REG_R0)
            if (result != expected or machine.reg_read(UC_ARM_REG_PC) != STOP
                    or machine.reg_read(UC_ARM_REG_SP) != STACK
                    or any(machine.reg_read(reg) != seed for reg, seed in saved.items())
                    or bytes(machine.mem_read(STACK - 64, 32)) != b'\xA5' * 32):
                raise ValueError('Private item lookup loses ABI, boundary fallback or stack guard')
            cases.append({'kind': kind, 'input': value, 'returned_pointer': result})
    if calls != [value & 0xFFFFFFFF for value in inputs['advice_lookup']]:
        raise ValueError('Private advice lookup bypasses original COMMON selection')
    return {'cases': cases, 'all_pointers_registers_stack_guards_pass': True,
            'COMMON_selection_success_pointer_is_boundary_contract': True}
