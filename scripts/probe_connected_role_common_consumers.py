"""Connect actual duty lookup to both native shared-message table consumers.

Assignment and current-route values are controlled inputs, not global bounds.
"""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
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

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_interface_release import TARGET
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, common_message_entries
from scripts.prepare_item_crew_owner import prepare as prepare_crew
from scripts.prepare_item_role_state import prepare as prepare_role
from scripts.probe_common_copy_arm946_alignment import arm946_machine

BASE, STACK, STOP = 0x02000000, 0x027F0000, 0x027E0000
SPECS = ((0x12720, 0x1278C, 0x130BDC, 0x623,
          '9bae2c6fc3a175a9dcee2eb3a269102e95546ab167c92bcda261f9c4726d332b'),
         (0x128B4, 0x12920, 0x130B88, 0x551,
          '7c480e7b445651cbccf6073340f20102edb5af5919fa289db905434908c227b7'))


def connected(source, common, caller, route, attribute, state='matching'):
    lo, hi, array, special, digest = SPECS[caller]
    if sha(source[lo:hi]) != digest:
        raise ValueError('Exact connected COMMON caller required')
    if source[0x132C0:0x132CC] != struct.pack('<3I', 0xE0800001, 0xE5D0001E, 0xE12FFF1E):
        raise ValueError('Actual ship role virtual differs')
    if not 0 <= route < 4 or not 0 <= attribute < 21 or state not in ('matching', 'unassigned', 'null-ship'):
        raise ValueError('Mapped route/duty state required')
    crew = 170
    table = struct.unpack_from('<I', source, array + attribute * 4)[0]
    if state != 'matching':
        expected_id = None
    elif attribute in (12, 16):
        expected_id = crew + special
    else:
        if not table:
            raise ValueError('Null role table cannot be classified as a valid live assignment')
        slots = struct.unpack_from('<4I', source, table - BASE)
        expected_id = slots[route]
        if expected_id == 0xFFFFFFFF:
            expected_id = next(v for v in slots if v != 0xFFFFFFFF)
    machine = arm946_machine(source)
    machine.mem_map(0x01FF0000, 0x10000)
    # Loaded sections are explicit initialization inputs here. Full native
    # startup/cache execution is separately verified on this exact release.
    for section in MainCodeFile(source, BASE).sections:
        machine.mem_write(section.ramAddress, bytes(section.data))
    owner = prepare_crew(source, machine, 74, crew, role_state='matching')
    setup = prepare_role(source, machine, owner['actor_pointer'], crew, route, attribute,
                         'unassigned' if state == 'unassigned' else 'matching')
    if state == 'null-ship':
        # 155 is the native ship-table null sentinel.
        machine.mem_write(setup['faction_root'] + 4 + route * 132 + 0xC + 4, bytes((155,)))
    common_owner = struct.unpack_from('<I', source, 0x552A0)[0]
    output = common_owner + 0x2030
    expected = b''
    if expected_id is not None:
        entries = common_message_entries(common, source, clean=False)
        expected = entries[expected_id].text
        directory = [struct.unpack_from('<HH', source, DIRECTORY_OFFSET + i * 4) for i in range(41)]
        block = max(i for i, (first, _) in enumerate(directory) if first <= expected_id)
        machine.mem_write(common_owner + 0x2C, bytes((block, 255, 0, 1)))
        machine.mem_write(common_owner + 0x30, IlnkContainer.parse(common).blocks[block])
    machine.mem_write(output - 16, b'\xA5' * (16 + 512 + 16))
    executed, selected = set(), []

    def trace(uc, address, size, _):
        executed.add(address - BASE)
        if address == BASE + 0x5528C:
            selected.append(uc.reg_read(UC_ARM_REG_R0))

    handle = machine.hook_add(UC_HOOK_CODE, trace)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_R0, crew)
    saved = {register: 0xA5A5A5A5 + index for index, register in enumerate(
        (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    for register, value in saved.items():
        machine.reg_write(register, value)
    try:
        machine.emu_start(BASE + lo, STOP, count=100000)
    finally:
        machine.hook_del(handle)
    required = {lo, 0xCB1A8, 0x81F54, 0x820DC}
    if state != 'unassigned':
        required |= {0x82E04, 0x36C94}
    if state == 'matching':
        required |= {0x132C0, 0x5528C, 0x534F4, 0x53628, 0x535E0, 0xCEC74}
        if attribute not in (12, 16):
            required |= {0x53C6C, 0x7F244}
    if (not required <= executed or selected != ([] if expected_id is None else [expected_id])
            or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or any(machine.reg_read(register) != value for register, value in saved.items())
            or machine.reg_read(UC_ARM_REG_R0) != (0 if expected_id is None else output)):
        raise ValueError('Connected role lookup/COMMON caller, selection or ABI differs')
    if expected_id is not None and bytes(machine.mem_read(output, len(expected) + 1)) != expected + b'\0':
        raise ValueError('Connected role consumer drops complete COMMON text')
    if (bytes(machine.mem_read(output - 16, 16)) != b'\xA5' * 16
            or bytes(machine.mem_read(output + 512, 16)) != b'\xA5' * 16
            or expected_id is None and bytes(machine.mem_read(output, 512)) != b'\xA5' * 512):
        raise ValueError('Connected role COMMON output guards or no-assignment path differ')
    return {'caller': BASE + lo, 'route_input': route, 'role_attribute_input': attribute, 'state': state,
            'selected_id': expected_id, 'complete_text_hex': expected.hex(),
            'native_executed_offsets': sorted(executed),
            'actual_duty_search_ship_virtual_table_selector_COMMON_copy_and_ABI_pass': True,
            'remaining_245_id_overlap': expected_id is not None and
            (3289 <= expected_id <= 3319 or 3393 <= expected_id <= 3606)}


def main():
    image = NdsImage.open('out/all_routes_combined_v159_candidate.nds')
    source, common = image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')
    if sha(source) != TARGET:
        raise ValueError('Exact V159 item ARM9 required')
    attributes = [i for i in range(21) if i not in (9, 10, 11)]
    cases = [connected(source, common, caller, route, attribute)
             for caller in range(2) for route in range(4) for attribute in attributes]
    cases += [connected(source, common, caller, route, 5, state)
              for caller in range(2) for route in range(4) for state in ('unassigned', 'null-ship')]
    if len(cases) != 160 or any(c['remaining_245_id_overlap'] for c in cases):
        raise ValueError('Connected duty COMMON inventory differs')
    report = {'status': 'pass-connected-native-duty-to-COMMON-consumers-controlled-inputs',
              'source_rom_sha256': sha(Path('out/all_routes_combined_v159_candidate.nds').read_bytes()),
              'source_arm9_sha256': sha(source), 'source_common_sha256': sha(common), 'cases': cases,
              'ship_role_virtual': {'address': BASE + 0x132C0, 'reads': 'byte at ship+0x1E+matched duty index'},
              'unclassified_null_role_indices': [9, 10, 11],
              'limitations': ['Complete native callers execute; no role, selector, ownership or COMMON lookup callbacks.',
                              'Native crew/faction constructors and ship initializer execute; state, tables, loaded sections and warm cache are inputs.',
                              'Role attributes and current routes are controlled inputs, not live/global producer bounds.',
                              'Null tables at roles 9-11 remain excluded from valid fixtures and their live exclusion remains unproved.',
                              'These mapped paths do not select the remaining 245 IDs; that does not prove those IDs unused.',
                              'Outer display/layout and physical gameplay remain unverified; no ROM or translation changes.']}
    Path('work/analysis/connected_role_common_v159_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Pass: 160 complete native duty/ship-role/table/COMMON caller cases. No remaining-245 overlap in this scope.')


if __name__ == '__main__':
    main()
