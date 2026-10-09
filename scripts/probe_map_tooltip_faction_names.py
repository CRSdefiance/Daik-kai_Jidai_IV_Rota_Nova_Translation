"""Execute native faction construction/name lookup and fixed-name tooltip rasters."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, format_copy, machine_for
from scripts.inventory_map_tooltip_classes import execute_class
from scripts.probe_map_entity_tooltip_raster import verify_raster

TABLE, COUNT, SOURCE_STRIDE, RUNTIME_STRIDE = 0x11BC70, 20, 68, 76
VTABLE, NAME_GETTER = 0x137240, 0x3CF9C
ROUTE_FACTIONS = (0, 2, 1, 3)
LOCKS = ((0xCD488, 0xCD550), (0x3CF9C, 0x3D060), (0xCB160, 0xCB16C),
         (0xCB184, 0xCB190), (0x397D8, 0x3980C), (0x115260, 0x115270),
         (VTABLE, VTABLE + 32), (0x24740, 0x24750))


def execute_name(source, index, route, player_name=b'Player Fleet'):
    if not 0 <= index < COUNT or not 0 <= route < len(ROUTE_FACTIONS):
        raise ValueError('Faction/route index outside mapped source bounds')
    if not player_name or b'\0' in player_name or len(player_name) > 18:
        raise ValueError('Player faction name exceeds native eighteen-byte editor capacity')
    if struct.unpack_from('<I', source, VTABLE + 8)[0] != BASE + NAME_GETTER:
        raise ValueError('Native faction name vtable differs')
    if struct.unpack_from('<4I', source, 0x115260) != ROUTE_FACTIONS:
        raise ValueError('Native route-to-faction mapping differs')
    machine = machine_for(source)
    base = struct.unpack_from('<I', source, 0xCB168)[0]
    owner = base + 4 + index * RUNTIME_STRIDE
    player_base = struct.unpack_from('<I', source, 0xCB18C)[0]
    player_pointer = player_base + struct.unpack_from('<I', source, 0x3CFC4)[0]
    global_state = struct.unpack_from('<I', source, 0x39808)[0]
    machine.mem_write(global_state + 0x48, struct.pack('<I', route))
    machine.mem_write(player_pointer, player_name + b'\0')
    machine.mem_write(owner - 4, b'\xA5' * (RUNTIME_STRIDE + 8))
    machine.mem_write(owner, struct.pack('<I', BASE + VTABLE))
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Faction lookup executes outside native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((owner <= address and address + size <= owner + RUNTIME_STRIDE)
                or (STACK - 0x1000 <= address and address + size <= STACK)):
            raise ValueError('Faction lookup writes outside native owner/stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.reg_write(UC_ARM_REG_R0, owner)
    machine.emu_start(BASE + 0xCD488, STOP, count=10000)
    field = TABLE + index * SOURCE_STRIDE
    fixed_pointer = struct.unpack_from('<I', source, field)[0]
    if struct.unpack('<I', machine.mem_read(owner + 4, 4))[0] != fixed_pointer:
        raise ValueError('Faction initializer differs from complete source name pointer')
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_R0, owner)
    machine.emu_start(BASE + NAME_GETTER, STOP, count=10000)
    pointer = machine.reg_read(UC_ARM_REG_R0)
    player_selected = index == ROUTE_FACTIONS[route]
    expected_pointer = player_pointer if player_selected else fixed_pointer
    if pointer != expected_pointer:
        raise ValueError('Native faction name selection differs')
    if player_selected:
        expected = player_name
    else:
        off = fixed_pointer - BASE
        if not 0 <= off < len(source):
            raise ValueError('Fixed faction name pointer outside source')
        expected = source[off:source.index(0, off)]
    actual = bytes(machine.mem_read(pointer, len(expected) + 1))
    if actual != expected + b'\0':
        raise ValueError('Native faction name loses complete text/NUL')
    required = {0xCD488, 0xCD53C, 0x3D030, 0xCB160, NAME_GETTER, 0x3CFC8, 0x397D8}
    if player_selected:
        required.add(0xCB184)
    if not required <= executed:
        raise ValueError('Native faction constructor/index/route/name bodies not executed')
    if machine.reg_read(UC_ARM_REG_SP) != STACK or machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Native faction lookup damages stack/return')
    if any(bytes(machine.mem_read(p, 4)) != b'\xA5' * 4 for p in (owner - 4, owner + RUNTIME_STRIDE)):
        raise ValueError('Native faction constructor damages adjacent owner')
    return {'index': index, 'route': route, 'player_selected': player_selected,
            'pointer': pointer, 'pointer_field': field, 'full_text_hex': actual.hex(),
            'text': expected.decode('cp932'), 'native_constructor_and_name_getter_executed': True,
            'stack_return_and_adjacent_owner_guards_preserved': True}


def probe(clean, current, proposed, allocation):
    if sha(current) != allocation['source_arm9_sha256'] or sha(proposed) != allocation['target_arm9_sha256']:
        raise ValueError('Complete allocation source/target differs')
    for lo, hi in LOCKS:
        if clean[lo:hi] != current[lo:hi] or current[lo:hi] != proposed[lo:hi]:
            raise ValueError('Native faction source code/literal/vtable differs')
    if struct.unpack_from('<I', clean, 0x24748)[0] != 0xE3570014:
        raise ValueError('Native ordinary faction bound differs')
    selections = [execute_name(proposed, index, route) for index in range(COUNT) for route in range(4)]
    fixed = [next(row for row in selections if row['index'] == index and not row['player_selected'])
             for index in range(COUNT)]
    for row in fixed:
        field = row['pointer_field']
        pointer = struct.unpack_from('<I', current, field)[0] - BASE
        if struct.unpack_from('<I', proposed, field)[0] != BASE + pointer:
            raise ValueError('Inherited faction name pointer changes')
        if current[pointer:current.index(0, pointer) + 1] != bytes.fromhex(row['full_text_hex']):
            raise ValueError('Inherited complete faction name changes')
    classes = [execute_class(proposed, index) for index in range(39)]
    rasters = []
    for faction in fixed:
        name = faction['text'].encode('ascii')
        for ship in classes:
            ship_class = ship['text'].encode('ascii')
            expected = name + b'\n  ' + ship_class + b' class'
            copied = format_copy(proposed, 0x705F0, [name, ship_class], expected)
            text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('ascii')
            for mode in (4, 16):
                rasters.append({'faction_index': faction['index'], 'class_index': ship['index'],
                                **verify_raster(proposed, text, mode)})
    return {'status': 'pass-native-fixed-faction-names-and-all-static-class-combinations',
            'source_arm9_sha256': sha(current), 'target_arm9_sha256': sha(proposed),
            'ordinary_faction_count': COUNT, 'source_stride': SOURCE_STRIDE,
            'runtime_stride': RUNTIME_STRIDE, 'route_factions': ROUTE_FACTIONS,
            'native_name_selections': selections, 'fixed_name_raster_count': len(rasters),
            'fixed_name_rasters': rasters,
            'player_name_source': {'getter': NAME_GETTER, 'base_getter': 0xCB184,
                                   'offset': 0x1A39, 'capacity_proven': False},
            'limitations': ['Player-name input fixture verifies selection only; writer/editor/save capacity remains unresolved.',
                           'Older faction-name English fidelity remains a separate review.',
                           'Full-width numeric pixel painting and physical palette/composition remain pending.',
                           'No ROM integration or formatting approval.']}


def main():
    root = Path('work/analysis/map_creature_complete_v139')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin')
    proposed = (root / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((root / 'report.json').read_text(encoding='utf-8'))
    report = probe(clean, current, proposed, allocation)
    (root / 'native_faction_name_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"80 native faction/route name selections; {report['fixed_name_raster_count']} fixed faction/class rasters pass.")


if __name__ == '__main__':
    main()
