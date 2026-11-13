"""Native ship metadata/name initialization and bounded figurehead state inputs."""

import struct

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

BASE, STOP, VTABLE = 0x02000000, 0x027FFF00, 0x0215EE94


def prepare(source, machine, item_index, ship_index, mutable_name=None):
    if not 0 <= ship_index < 154 or not 114 <= item_index <= 123:
        raise ValueError('Mapped native ship/figurehead indices required')
    resource = source[0x11E210 + item_index * 24:0x11E210 + (item_index + 1) * 24]
    if resource[16] != 5 or resource[20] != 115 or resource[21] & 20:
        raise ValueError('Figurehead must have its ordinary native owner/flags')
    if ship_index < 50:
        if (not mutable_name or len(mutable_name) > 18 or any(not 32 <= c <= 126 for c in mutable_name)):
            raise ValueError('Mutable ship name must fit the mapped eighteen-byte editor capacity')
    elif mutable_name is not None:
        raise ValueError('Fixed source ship metadata requires its native source name')
    if struct.unpack_from('<9I', source, VTABLE - BASE) != (
            BASE + 0x181A0, BASE + 0x1A4E0, BASE + 0x11DB0, BASE + 0xA4908,
            BASE + 0x62D68, BASE + 0xAB0C4, BASE + 0x132C0, BASE + 0x1856C, BASE + 0x353D4):
        raise ValueError('Native ship name/status/figurehead vtable differs')
    root = struct.unpack_from('<I', source, 0xCB150)[0]
    table = struct.unpack_from('<I', source, 0xCD3CC)[0]
    context = machine.context_save()
    stack = machine.reg_read(UC_ARM_REG_SP)
    preserved = {reg: machine.reg_read(reg) for reg in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                                                       UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
                                                       UC_ARM_REG_R10, UC_ARM_REG_R11)}
    executed = set()
    current = None

    def code(uc, address, size, _):
        if not BASE <= address < BASE + len(source):
            raise ValueError('Native ship initializer escaped source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((current <= address < address + size <= current + 0x8C)
                or (stack - 0x1000 <= address < address + size <= stack)):
            raise ValueError('Native ship initialization escaped object/stack')

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    try:
        for index in range(154):
            current = root + 4 + index * 0x8C
            machine.mem_write(current - 4, b'\xA5' * 4 + struct.pack('<I', VTABLE) + bytes(0x88) + b'\xA5' * 4)
            machine.reg_write(UC_ARM_REG_R0, current)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            machine.emu_start(BASE + 0xCD27C, STOP, count=10000)
            if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != stack
                    or any(machine.reg_read(reg) != value for reg, value in preserved.items())
                    or bytes(machine.mem_read(current - 4, 4)) != b'\xA5' * 4
                    or bytes(machine.mem_read(current + 0x8C, 4)) != b'\xA5' * 4):
                raise ValueError('Native ship initializer return/guards differ')
            if index >= 50:
                metadata = bytes(machine.mem_read(table + (index - 50) * 44, 44))
                name_pointer = struct.unpack_from('<I', metadata)[0]
                expected = bytes(machine.mem_read(name_pointer, 128)).split(b'\0', 1)[0]
                if len(expected) > 18 or bytes(machine.mem_read(current + 8, len(expected) + 1)) != expected + b'\0':
                    raise ValueError('Native fixed ship name overflows its nineteen-byte field or loses bytes')
    finally:
        for handle in handles:
            machine.hook_del(handle)
        machine.context_restore(context)
    actor = root + 4 + ship_index * 0x8C
    if ship_index < 50:
        # Native default initialization leaves player slots inactive. Supply the
        # caller's active class and editor-bounded mutable name as runtime inputs.
        machine.mem_write(actor + 0x49, b'\0')
        machine.mem_write(actor + 8, mutable_name + b'\0')
    if bytes(machine.mem_read(actor + 0x49, 1)) == b'\x28':
        raise ValueError('Selected fixed source ship is inactive')
    machine.mem_write(actor + 0x4B, bytes((item_index - 114,)))
    if not {0xCD27C, 0xA4BF0, 0xCB148, 0xCD3B8, 0xCED98} <= executed:
        raise ValueError('Native ship index/source/name initializer did not execute')
    return {'ship_index': ship_index, 'item_index': item_index, 'actor_pointer': actor,
            'name_pointer': actor + 8, 'name': bytes(machine.mem_read(actor + 8, 19)).split(b'\0', 1)[0].decode('cp932'),
            'native_default_ship_initializers': 154, 'native_fixed_source_names_checked': 104,
            'initialized_ship_table_sha256': sha(bytes(machine.mem_read(root + 4, 154 * 0x8C))),
            'vtable_seed_figurehead_equipment_and_mutable_slot_state_are_contracts': True,
            'mutable_name': mutable_name.decode('ascii') if mutable_name is not None else None}
