"""Construct native faction/ship interfaces with controlled crew-duty state."""

import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

BASE, STOP = 0x02000000, 0x027FFF00
STATES = ('matching', 'mismatching', 'unassigned', 'outside-faction', 'other-fleet-leader',
          'secondary-fleet-leader', 'captain')


def prepare(source, machine, actor, crew, current, attribute, state):
    if state not in STATES or not 0 <= attribute < 21:
        raise ValueError('Mapped item attribute and explicit native eligibility state required')
    if (state == 'captain') != (crew == current):
        raise ValueError('Captain state must select the actual current-captain interface')
    factions = struct.unpack_from('<I', source, 0xCB1B0)[0]
    ships = struct.unpack_from('<I', source, 0xCB150)[0]
    global_state = struct.unpack_from('<I', source, 0x39808)[0]
    if not 0 <= current < 4:
        raise ValueError('Role-dependent crew state requires a real current-captain index 0..3')
    fleet = current
    group = struct.unpack_from('<I', source, 0x115260 + fleet * 4)[0]
    machine.mem_write(global_state + 0x48, struct.pack('<I', fleet))
    machine.mem_write(actor + 5, bytes((group if state != 'outside-faction' else (group + 1) % 4,)))
    # The copied native global constructor installs this final faction vtable.
    if struct.unpack_from('<I', source, 0xCC53C)[0] != 0x02134EE0:
        raise ValueError('Actual faction constructor final vtable differs')
    stack, executed = machine.reg_read(UC_ARM_REG_SP), set()
    owned = [(factions + 4, factions + 4 + 63 * 132), (ships + 4, ships + 4 + 140)]

    def code(uc, address, size, _):
        if not BASE <= address < BASE + len(source):
            raise ValueError('Faction/ship initialization escapes native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not any(lo <= address < address + size <= hi for lo, hi in owned + [(stack - 1024, stack)]):
            raise ValueError('Faction/ship initialization escapes owned objects/stack')

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    try:
        for index in range(63):
            pointer = factions + 4 + index * 132
            machine.mem_write(pointer, bytes(132))
            machine.reg_write(UC_ARM_REG_R0, pointer)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            machine.emu_start(BASE + 0xCC4CC, STOP, count=10000)
            if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != stack
                    or struct.unpack('<I', machine.mem_read(pointer, 4))[0] != 0x02134EE0):
                raise ValueError('Actual faction constructor does not return with its final native vtable')
            # Only the player's faction is active; native active virtual reads bit0.
            machine.mem_write(pointer + 0x50, bytes((0 if index == fleet else 1,)))
            machine.mem_write(pointer + 8, bytes((current if index == fleet else 208,)))
        ship = ships + 4
        machine.mem_write(ship, struct.pack('<I', 0x0215EE94) + bytes(136))
        machine.reg_write(UC_ARM_REG_R0, ship)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0xCD27C, STOP, count=10000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != stack:
            raise ValueError('Actual mutable ship initializer does not return')
    finally:
        for handle in handles:
            machine.hook_del(handle)
    primary = factions + 4 + fleet * 132 + 0xC
    machine.mem_write(primary + 4, bytes((0,)))
    machine.mem_write(ship + 0x1E, bytes((24,)) * 31)
    machine.mem_write(ship + 0x48, bytes((current,)))
    duties = factions + struct.unpack_from('<I', source, 0x49A80)[0]
    machine.mem_write(duties + 6, b'\xFF' * 31)
    if state in ('matching', 'mismatching'):
        machine.mem_write(duties + 6 + 30, bytes((crew,)))
        machine.mem_write(ship + 0x1E + 30, bytes((attribute if state == 'matching' else (attribute + 1) % 21,)))
    elif state == 'other-fleet-leader':
        other = factions + 4 + 132
        machine.mem_write(other + 0x50, b'\0')
        machine.mem_write(other + 8, bytes((crew,)))
    elif state == 'secondary-fleet-leader':
        machine.mem_write(primary + 8 + 4, b'\0')
        machine.mem_write(ship + 0x48, bytes((crew,)))
    return {'state': state, 'expected_eligible': state not in ('mismatching', 'unassigned'),
            'crew': crew, 'current_captain': current, 'attribute': attribute,
            'native_faction_constructors': 63, 'native_mutable_ship_initializer': True,
            'faction_root': factions, 'ship': ship, 'duties': duties,
            'initialization_executed_offsets': sorted(executed),
            'active_faction_crew_membership_duty_assignment_and_ship_captain_are_inputs': True,
            'ship_vtable_and_outer_container_initialization_are_contracts': True}
