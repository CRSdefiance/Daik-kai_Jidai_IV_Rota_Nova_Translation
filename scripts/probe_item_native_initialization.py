"""Native metadata initialization for every static/default promotional item."""

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
from scripts.execute_map_entity_tooltip_copy import BASE, machine_for
from scripts.probe_promotional_item_defaults import OWNER
from scripts.probe_promotional_item_defaults import verify as promotional_defaults

STOP = 0x027FFF00


def initialize_item_object(source, machine, index):
    if not 0 <= index < 218:
        raise ValueError('Only mapped static/default/generated promotional item indices are supported')
    table = struct.unpack_from('<I', source, 0xCB198)[0]
    owner = table + 4 + index * 20
    resource = BASE + 0x11E210 + index * 24 if index < 188 else OWNER + 0x3E4 + (index - 188) * 24
    metadata = bytes(machine.mem_read(resource, 24))
    machine.mem_write(owner, struct.pack('<I', BASE + 0x13C38C) + b'\xA5' * 16)
    expected = struct.pack('<I', BASE + 0x13C38C) + b'\xA5' * 4 + metadata[8:16] + metadata[20:22] + b'\xA5' * 2
    context = machine.context_save()
    stack = machine.reg_read(UC_ARM_REG_SP)
    preserved = {reg: machine.reg_read(reg) for reg in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                                                       UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
                                                       UC_ARM_REG_R10, UC_ARM_REG_R11)}
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address < BASE + len(source):
            raise ValueError('Native item initialization escaped source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((owner + 8 <= address < address + size <= owner + 18)
                or (stack - 256 <= address < address + size <= stack)):
            raise ValueError('Native item initialization escaped metadata/stack')

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    try:
        machine.reg_write(UC_ARM_REG_R0, owner)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0xCDAC4, STOP, count=1000)
        if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != stack
                or bytes(machine.mem_read(owner, 20)) != expected
                or any(machine.reg_read(reg) != value for reg, value in preserved.items())
                or not {0xCDAC4, 0x4A55C, 0xCB190, 0xCDAFC} <= executed
                or index >= 188 and 0x102BB0 not in executed):
            raise ValueError('Native item object metadata initialization/return differs')
    finally:
        for handle in handles:
            machine.hook_del(handle)
        machine.context_restore(context)
    return {'index': index, 'object_pointer': owner, 'metadata_pointer': resource,
            'object_hex': expected.hex(), 'executed_offsets': sorted(executed),
            'native_metadata_initialization_and_return_pass': True,
            'item_vtable_seed_and_outer_table_initialization_are_contracts': True}


def main():
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    machine = machine_for(source)
    context = machine.context_save()
    promotional = promotional_defaults(source, machine)
    machine.context_restore(context)
    rows = [initialize_item_object(source, machine, index) for index in range(198)]
    Path('work/analysis/item_native_initialization_proof.json').write_text(json.dumps({
        'status': 'pass-198-native-item-metadata-initializers', 'target_arm9_sha256': sha(source),
        'promotional_defaults': promotional, 'cases': rows,
        'full_outer_table_constructor_random_downloaded_states_and_physical_gameplay_verified': False,
    }, indent=2) + '\n', encoding='utf-8')
    print('Pass: all 198 native item object metadata initializers, real index getters, return/stack and bounded writes.')


if __name__ == '__main__':
    main()
