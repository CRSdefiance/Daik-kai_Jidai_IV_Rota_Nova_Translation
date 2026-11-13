"""Trace the eighteen-byte faction editor and nineteen-byte serialized field."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, format_copy, machine_for
from scripts.inventory_map_tooltip_classes import execute_class
from scripts.probe_map_entity_tooltip_raster import verify_raster

RECORD, OWNER, IO = 0x02414000, 0x02415000, 0x02416000
FIELD, CAPACITY, STORAGE = 0x55, 18, 19
LOCKS = ((0x46F50, 0x46F78), (0x46FF0, 0x46FF4), (0xCD53C, 0xCD550),
         (0xCD704, 0xCD710), (0xCED98, 0xCEDC8), (0x9DF54, 0x9DFB0),
         (0x83050, 0x83078), (0x83148, 0x83170), (0x469DC, 0x46A1C),
         (0x46BE0, 0x46C20))


def native_copy(source, name):
    if not name or len(name) > CAPACITY or b'\0' in name:
        raise ValueError('Faction name outside eighteen-byte editor capacity')
    name.decode('cp932')
    machine = machine_for(source)
    machine.mem_write(RECORD + 0x3B, name + b'\0')
    machine.mem_write(OWNER + FIELD - 4, b'\xA5' * (STORAGE + 8))
    machine.reg_write(UC_ARM_REG_R4, RECORD)
    machine.reg_write(UC_ARM_REG_R5, OWNER)
    executed = set()

    def code(uc, address, size, _):
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not OWNER + FIELD <= address < address + size <= OWNER + FIELD + len(name) + 1:
            raise ValueError('Faction setter writes outside complete name/NUL')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xCD704, BASE + 0xCD710, count=10000)
    expected = name + b'\0' + b'\xA5' * (STORAGE - len(name) - 1)
    if bytes(machine.mem_read(OWNER + FIELD, STORAGE)) != expected or 0xCED98 not in executed:
        raise ValueError('Native faction setter loses complete name/NUL')
    if machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native faction setter damages stack')
    if any(bytes(machine.mem_read(p, 4)) != b'\xA5' * 4
           for p in (OWNER + FIELD - 4, OWNER + FIELD + STORAGE)):
        raise ValueError('Native faction setter damages adjacent fields')
    return expected


def serialize(source, field, *, restore=False):
    if len(field) != STORAGE:
        raise ValueError('Exactly nineteen serialized faction bytes required')
    machine = machine_for(source)
    machine.mem_write(OWNER + FIELD - 4, b'\xA5' * (STORAGE + 8))
    if not restore:
        machine.mem_write(OWNER + FIELD, field)
    machine.reg_write(UC_ARM_REG_R4, IO)
    machine.reg_write(UC_ARM_REG_R5, OWNER)
    executed, calls, saved = set(), [], bytearray()
    backend = 0xD010C if restore else 0xD01AC
    start, stop = (0x83148, 0x83170) if restore else (0x83050, 0x83078)

    def code(uc, address, size, _):
        executed.add(address - BASE)
        if address == BASE + backend:
            position = len(calls)
            if (uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)) != (
                    IO, OWNER + FIELD + position, 1) or position >= STORAGE:
                raise ValueError('Serialized faction byte backend arguments differ')
            calls.append(position)
            if restore:
                uc.mem_write(OWNER + FIELD + position, field[position:position + 1])
            else:
                saved.extend(uc.mem_read(OWNER + FIELD + position, 1))
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif not BASE <= address < BASE + len(source):
            raise ValueError('Serialization executes outside native source')

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x1000 <= address and address + size <= STACK)
                or (address == IO + 0x28 and size == 4)):
            raise ValueError('Serialization writes outside native stack/byte counter')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + start, BASE + stop, count=10000)
    if len(calls) != STORAGE or struct.unpack('<I', machine.mem_read(IO + 0x28, 4))[0] != STORAGE:
        raise ValueError('Native serialization loses nineteen-byte extent')
    if (0x46BE0 if restore else 0x469DC) not in executed:
        raise ValueError('Actual native byte serialization helper not executed')
    result = bytes(machine.mem_read(OWNER + FIELD, STORAGE)) if restore else bytes(saved)
    if result != field or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native serialization loses bytes or stack')
    if any(bytes(machine.mem_read(p, 4)) != b'\xA5' * 4
           for p in (OWNER + FIELD - 4, OWNER + FIELD + STORAGE)):
        raise ValueError('Native serialization damages neighboring fields')
    return {'restore': restore, 'complete_field_hex': result.hex(), 'byte_calls': len(calls),
            'native_loop_and_byte_helper_executed': True, 'physical_io_backend_is_contract': True}


def default_name(source, route):
    if not 0 <= route < 4:
        raise ValueError('Unmapped default route')
    machine = machine_for(source)
    machine.mem_write(RECORD, b'\xA5' * 0x70)
    machine.mem_write(RECORD + 4, struct.pack('<I', route))
    machine.reg_write(UC_ARM_REG_R4, RECORD)
    machine.emu_start(BASE + 0x46F50, BASE + 0x46F78, count=10000)
    route_table = struct.unpack_from('<I', source, 0x46FF0)[0] - BASE
    index = struct.unpack_from('<I', source, route_table + route * 4)[0]
    pointer = struct.unpack_from('<I', source, 0x11BC70 + index * 68)[0] - BASE
    expected = source[pointer:source.index(0, pointer)]
    if len(expected) > CAPACITY or bytes(machine.mem_read(RECORD + 0x3B, len(expected) + 1)) != expected + b'\0':
        raise ValueError('Native default faction-name producer loses complete name')
    if machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Default name producer damages stack')
    return {'route': route, 'faction_index': index, 'name_hex': expected.hex(), 'text': expected.decode('cp932')}


def edit_dispatch(source, name):
    native_copy(source, name)  # Require a valid full string before keyboard contract.
    machine = machine_for(source)
    editor = IO
    machine.mem_write(editor + 0x54, struct.pack('<I', RECORD))
    machine.mem_write(RECORD + 0x3B, b'Original\0')
    machine.reg_write(UC_ARM_REG_R4, editor)
    calls = []

    def code(uc, address, size, _):
        if address == BASE + 0xAEB98:
            if uc.reg_read(UC_ARM_REG_R1) != CAPACITY or uc.reg_read(UC_ARM_REG_R0) != STACK + 4:
                raise ValueError('Faction-name keyboard limit/address differs')
            calls.append(CAPACITY)
            uc.mem_write(STACK + 4, name + b'\0')
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    machine.hook_add(UC_HOOK_CODE, code)
    machine.emu_start(BASE + 0x9DF54, BASE + 0x9DFB0, count=10000)
    if calls != [CAPACITY] or bytes(machine.mem_read(RECORD + 0x3B, len(name) + 1)) != name + b'\0':
        raise ValueError('Native edit dispatch loses complete accepted faction name')
    if machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native edit dispatch damages stack')
    return {'limit': CAPACITY, 'name_hex': name.hex(), 'native_dispatch_strlen_and_copy_executed': True,
            'keyboard_ui_is_contract': True}


def main():
    root = Path('work/analysis/map_creature_complete_v139')
    source = (root / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((root / 'report.json').read_text())
    if sha(source) != allocation['target_arm9_sha256']:
        raise ValueError('Complete proposal hash differs')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if any(clean[lo:hi] != source[lo:hi] for lo, hi in LOCKS):
        raise ValueError('Native faction-name producer/editor/serialization source differs')
    names = [b'A' * size for size in range(1, CAPACITY + 1)] + ['ア'.encode('cp932') * size for size in range(1, 10)]
    defaults = [default_name(source, route) for route in range(4)]
    cases = []
    for name in names:
        field = native_copy(source, name)
        cases.append({'name_hex': name.hex(), 'editor': edit_dispatch(source, name),
                      'save': serialize(source, field), 'load': serialize(source, field, restore=True)})
    classes = [execute_class(source, index) for index in range(39)]
    rasters = []
    for name in (b'A' * 17, b'A' * 18):
        for ship in classes:
            ship_class = ship['text'].encode('ascii')
            expected = name + b'\n  ' + ship_class + b' class'
            copied = format_copy(source, 0x705F0, [name, ship_class], expected)
            for mode in (4, 16):
                rasters.append({'name_bytes': len(name), 'class_index': ship['index'],
                                **verify_raster(source, bytes.fromhex(copied['full_text_hex'])[:-1].decode('ascii'), mode)})
    report = {'status': 'pass-native-eighteen-byte-editor-and-nineteen-byte-serialization',
              'target_arm9_sha256': sha(source), 'editor_capacity_bytes': CAPACITY,
              'serialized_storage_bytes': STORAGE, 'special_owner_offset': 0x19E4,
              'name_offset_in_special_owner': FIELD, 'shared_name_offset': 0x1A39,
              'defaults': defaults, 'cases': cases, 'maximum_ascii_raster_cases': rasters,
              'limitations': ['Keyboard UI and physical I/O backend remain contracts.',
                             'Serialized load preserves nineteen bytes; it does not synthesize/validate a NUL for malformed saves.',
                             'Full-width CP932 pixels and physical routing remain pending.',
                             'No ROM integration or formatting approval.']}
    (root / 'native_player_faction_name_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Four native defaults, 27 complete editor/copy/save/load cases and 156 maximum ASCII tooltip rasters pass.')


if __name__ == '__main__':
    main()
