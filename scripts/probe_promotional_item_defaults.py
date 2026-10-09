"""Execute default promotional name/metadata initialization before random items."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for

OWNER, END = 0x023800C8, 0x023800C8 + 0x6B4


def verify(source, machine=None):
    machine = machine if machine is not None else machine_for(source)
    machine.mem_write(OWNER - 32, b'\xA5' * (END - OWNER + 64))
    machine.reg_write(UC_ARM_REG_R0, OWNER)
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address < BASE + len(source):
            raise ValueError('Promotional default initializer escaped native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((OWNER + 0x22 <= address < address + size <= END)
                or (STACK - 0x1000 <= address < address + size <= STACK)):
            raise ValueError('Promotional default initializer escaped owned names/metadata/stack')

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    # Stop at the actual boundary before the random-item selection loop.
    machine.emu_start(BASE + 0x102C24, BASE + 0x102C7C, count=100000)
    for handle in handles:
        machine.hook_del(handle)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x102C7C
            or machine.reg_read(UC_ARM_REG_SP) != STACK - 56
            or not {0xD7650, 0xD9B88} <= executed
            or bytes(machine.mem_read(OWNER - 32, 32)) != b'\xA5' * 32
            or bytes(machine.mem_read(END, 32)) != b'\xA5' * 32):
        raise ValueError('Native promotional initialization boundary/guards differ')
    rows = []
    original = struct.unpack_from('<I', source, 0x102E40)[0] - BASE
    names = struct.unpack_from('<I', source, 0x102E44)[0] - BASE
    for index in range(10):
        record_pointer = OWNER + 0x3E4 + index * 24
        name_pointer = OWNER + 0x22 + index * 32
        record = bytes(machine.mem_read(record_pointer, 24))
        name_source = struct.unpack_from('<I', source, names + index * 8)[0] - BASE
        expected_name = source[name_source:source.index(0, name_source)]
        actual_name = bytes(machine.mem_read(name_pointer, 32)).split(b'\0', 1)[0]
        if (struct.unpack_from('<I', record)[0] != name_pointer
                or record[4:] != source[original + index * 24 + 4:original + (index + 1) * 24]
                or actual_name != expected_name):
            raise ValueError('Promotional default source metadata/name differs')
        rows.append({'index': index + 188, 'metadata_pointer': record_pointer,
                     'metadata_hex': record.hex(), 'name_pointer': name_pointer,
                     'name': actual_name.decode('cp932'), 'name_hex': actual_name.hex(),
                     'native_complete_name_metadata_and_guards_pass': True})
    return {'target_arm9_sha256': sha(source), 'default_promotional_items': rows,
            'native_initializer_segment': [BASE + 0x102C24, BASE + 0x102C7C],
            'saved_frame_bytes_at_segment_stop': 56,
            'full_initializer_return_random_additions_downloaded_states_and_rendering_verified': False,
            'runtime_owner_argument_is_initialized_boundary_contract': True}


def main():
    source = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    result = verify(source)
    Path('work/analysis/promotional_item_default_initialization_proof.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Ten default promotional item names/metadata pass actual initializer copy and guards; full initialization/download/rendering pending.')


if __name__ == '__main__':
    main()
