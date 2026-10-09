"""Connect native captain selection to ordinary and stored player-name getters."""

import struct

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_SP

from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP


def setup(source, machine, fleet, index, current_character, player_name='A'):
    if not (0 <= index < 207 or index == 208) or not 0 <= current_character < 4:
        raise ValueError('Captain fixture outside initialized ordinary/current-character range')
    for section in MainCodeFile(source, BASE).sections:
        if section.ramAddress >= BASE:
            machine.mem_write(section.ramAddress, bytes(section.data))
    root = struct.unpack_from('<I', source, 0xCB18C)[0]
    state = struct.unpack_from('<I', source, 0x7F250)[0]
    machine.mem_write(state + 0x48, struct.pack('<I', current_character))
    machine.mem_write(fleet + 8, bytes([index]))
    if index == 208:
        return None
    if index == current_character:
        encoded = player_name.encode('cp932')
        if len(encoded) > 16 or b'\0' in encoded:
            raise ValueError('Stored player character name exceeds sixteen-byte field')
        actor = root + struct.unpack_from('<I', source, 0x369C4)[0]
        vtable = BASE + 0x148E94
        if struct.unpack_from('<I', source, 0x148EB4)[0] != BASE + 0x1371C:
            raise ValueError('Native stored-name virtual getter differs')
        # Interface and valid saved field are initialization fixtures. The
        # selector, virtual dispatch and real +0x20 getter execute downstream.
        machine.mem_write(actor, struct.pack('<I', vtable))
        machine.mem_write(actor + 0x20, encoded + b'\0')
        return player_name
    actor = root + 4 + index * 32
    machine.reg_write(UC_ARM_REG_R0, actor)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.emu_start(BASE + 0x7EB3C, STOP, count=10)
    field = 0x120B80 + index * 32
    pointer = struct.unpack_from('<I', source, field)[0]
    return bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
