"""Seed bounded equipment state; execute native crew constructors and searches."""

import struct

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

BASE, STOP = 0x02000000, 0x027FFF00


def prepare(source, machine, item_index, crew_index, player_name=None, role_state=None, equipment_slot=None):
    if not 0 <= crew_index < 207 or not 0 <= item_index < 188:
        raise ValueError('Mapped ordinary crew and static equipment indices required')
    resource = source[0x11E210 + item_index * 24:0x11E210 + (item_index + 1) * 24]
    if (resource[16] not in (2, 3, 4) or resource[20] != 115 or resource[21] & 20
            or resource[18] != 24 and (resource[16] != 4 or role_state is None)):
        raise ValueError('Native crew ownership requires mapped equipment and an explicit state for role-dependent items')
    slot = resource[16] - 2 if equipment_slot is None else equipment_slot
    if slot not in ((2, 3, 4) if resource[16] == 4 else (resource[16] - 2,)):
        raise ValueError('Equipment slot does not match the native item search')
    if player_name is not None and (not player_name or len(player_name) > 18
                                    or any(not 32 <= c <= 126 for c in player_name)):
        raise ValueError('Mutable captain name must fit the mapped eighteen-byte editor capacity')
    root = struct.unpack_from('<I', source, 0xCB18C)[0]
    current = crew_index if player_name is not None else (1 if crew_index == 0 else 0)
    state = struct.unpack_from('<I', source, 0x7F250)[0]
    machine.mem_write(state + 0x48, struct.pack('<I', current))
    context = machine.context_save()
    stack = machine.reg_read(UC_ARM_REG_SP)
    for index in range(207):
        actor = root + 4 + index * 32
        machine.mem_write(actor, bytes(32))
        machine.reg_write(UC_ARM_REG_R0, actor)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0x7EB3C, STOP, count=10)
        if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != stack
                or struct.unpack('<I', machine.mem_read(actor, 4))[0] != BASE + 0x148414):
            raise ValueError('Actual ordinary crew constructor does not initialize the native vtable')
        machine.mem_write(actor + 0x1B, b'\xFF' * 5)
    # The current captain is a distinct interface object. Its vtable/name storage
    # seed is a contract; the name virtual and native current-captain branch execute.
    player = root + struct.unpack_from('<I', source, 0x4D870)[0]
    machine.mem_write(player, struct.pack('<I', BASE + 0x148E94))
    machine.mem_write(player + 0x1B, b'\xFF' * 5)
    machine.mem_write(player + 0x20, (player_name if player_name is not None else b'Player') + b'\0')
    actor = player if player_name is not None else root + 4 + crew_index * 32
    machine.mem_write(actor + 0x1B + slot, bytes((item_index,)))
    role_initialization = None
    if role_state is not None:
        from scripts.prepare_item_role_state import prepare as prepare_role
        role_initialization = prepare_role(source, machine, actor, crew_index, current, resource[18], role_state)
    machine.context_restore(context)
    return {'crew_index': crew_index, 'current_captain_index': current, 'item_index': item_index,
            'crew_table': root, 'actor_pointer': actor, 'native_ordinary_constructors': 207,
            'runtime_equipment_and_current_captain_state_are_inputs': True,
            'captain_interface_vtable_and_mutable_name_seed_are_contracts': True,
            'equipment_slot': slot, 'role_initialization': role_initialization,
            'mutable_player_name': player_name.decode('ascii') if player_name is not None else None}
