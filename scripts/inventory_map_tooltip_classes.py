"""Trace all 39 native map class initializers and stage remaining creature names."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.prepare_map_entity_tooltips import SOURCE_SHA

TABLE, COUNT, SOURCE_STRIDE, RUNTIME_STRIDE = 0x11C7A8, 39, 56, 64
VTABLE = 0x15EE20
CREATURES = (
    (34, 0x15B7E8, 8, '化魚', 'Monster Fish', 'A fish transformed into a monster.'),
    (35, 0x15BC58, 8, '大イカ', 'Giant Squid', 'A giant squid.'),
    (36, 0x15B958, 8, 'サメ', 'Shark', 'A shark.'),
    (37, 0x15B76C, 4, '鯨', 'Whale', 'A whale.'),
)
LOCKS = ((0x30218, 0x30254), (0xCD3D0, 0xCD488), (0xABEC0, 0xABEE4),
         (0xCB154, 0xCB160), (0x1FD74, 0x1FD7C), (VTABLE, VTABLE + 64))


def execute_class(source, index):
    if not 0 <= index < COUNT:
        raise ValueError('Class index outside source-bounded table')
    machine = machine_for(source)
    runtime_base = struct.unpack_from('<I', source, 0xCB15C)[0]
    owner = runtime_base + 4 + index * RUNTIME_STRIDE
    machine.mem_write(owner - 4, b'\xA5' * 4 + bytes(RUNTIME_STRIDE) + b'\xA5' * 4)
    machine.mem_write(owner, struct.pack('<I', BASE + VTABLE))
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Class initializer executes outside native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((owner <= address and address + size <= owner + RUNTIME_STRIDE)
                or (STACK - 0x1000 <= address and address + size <= STACK)):
            raise ValueError('Class initializer writes outside owner/stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.reg_write(UC_ARM_REG_R0, owner)
    machine.emu_start(BASE + 0xCD3D0, STOP, count=10000)
    if machine.reg_read(UC_ARM_REG_SP) != STACK or machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Class initializer damages stack')
    name_getter = struct.unpack_from('<I', source, VTABLE + 4)[0]
    if name_getter != BASE + 0x1FD74:
        raise ValueError('Native class name vtable differs')
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_R0, owner)
    machine.emu_start(name_getter, STOP, count=100)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native name getter damages stack or does not return')
    pointer = machine.reg_read(UC_ARM_REG_R0)
    field = TABLE + index * SOURCE_STRIDE
    if pointer != struct.unpack_from('<I', source, field)[0]:
        raise ValueError('Native initializer/name accessor differs from source table')
    offset = pointer - BASE
    raw = source[offset:source.index(0, offset)]
    if not {0xABEC0, 0xCB154, 0xCD474, 0x1FD74} <= executed:
        raise ValueError('Native index/selection/name bodies were not executed')
    if bytes(machine.mem_read(owner - 4, 4)) != b'\xA5' * 4 or bytes(machine.mem_read(owner + RUNTIME_STRIDE, 4)) != b'\xA5' * 4:
        raise ValueError('Native class initializer damages adjacent owner')
    return {'index': index, 'pointer_field': field, 'source_offset': offset,
            'text': raw.decode('cp932'), 'full_text_hex': (raw + b'\0').hex(),
            'constructed_owner': owner, 'owner_state_hex': bytes(machine.mem_read(owner, RUNTIME_STRIDE)).hex(),
            'native_initializer_index_and_name_getter_executed': True,
            'stack_and_adjacent_owner_guards_preserved': True}


def inventory(clean, current):
    if sha(current) != SOURCE_SHA:
        raise ValueError('Exact V139 source required')
    for lo, hi in LOCKS:
        if clean[lo:hi] != current[lo:hi]:
            raise ValueError('Native class constructor/count/accessor differs')
    if struct.unpack_from('<I', clean, 0x3024C)[0] != 0xE3560027:
        raise ValueError('Source class-count bound differs')
    cases = [execute_class(current, i) for i in range(COUNT)]
    records = []
    for index, offset, capacity, japanese, english, meaning in CREATURES:
        source = japanese.encode('cp932') + b'\0'
        if any(image[offset:offset + capacity] != source.ljust(capacity, b'\0') for image in (clean, current)):
            raise ValueError('Creature source/padding differs')
        row = cases[index]
        if row['source_offset'] != offset or row['text'] != japanese:
            raise ValueError('Native creature name differs')
        records.append({'id': 'MAP_CREATURE_CLASS_' + str(index), 'class_index': index,
                        'source_offset': offset, 'source_capacity': capacity,
                        'pointer_field': row['pointer_field'], 'source_hex': source[:-1].hex(),
                        'japanese': japanese, 'english': english, 'speaker': 'Map creature class',
                        'source_meaning': meaning,
                        'context': 'Native class table 11C7A8, indices 34-37; CD3D0 initializes the name, vtable+4 returns it, and map class format 705F0 displays it.',
                        'localization_note': 'Full natural creature name, preserving the monster/giant qualifiers. No shortening to fit old slots; relocation and formatting pending.',
                        'review': {'source': True, 'context': True, 'localization': True,
                                   'naturalness': True, 'formatting': False}})
    required = sum(len(row['english'].encode('ascii')) + 1 for row in records)
    available = sum(row['source_capacity'] for row in records)
    return {'status': 'all-39-native-class-initializers-mapped-four-creature-names-pending',
            'source_arm9_sha256': sha(current), 'count': COUNT, 'source_stride': SOURCE_STRIDE,
            'runtime_stride': RUNTIME_STRIDE, 'table': TABLE, 'cases': cases,
            'source_code_locks': [{'start': lo, 'end': hi, 'sha256': sha(clean[lo:hi])} for lo, hi in LOCKS],
            'creature_storage': {'owned_bytes': available, 'complete_english_bytes': required,
                                 'shortfall_bytes': required - available,
                                 'largest_string_including_nul': max(len(row['english']) + 1 for row in records)},
            'limitations': ['Native class table coverage does not bound every dynamic faction/user name.',
                           'Creature names require complete relocation and native formatting before integration.']}, records


def main():
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin')
    report, records = inventory(clean, current)
    root = Path('work/analysis/map_entity_tooltips_v139')
    root.mkdir(parents=True, exist_ok=True)
    (root / 'all_class_initializer_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    document = {'format': 'dk4-map-creature-class-manuscript-v2',
                'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                'status': 'source-reviewed-full-relocation-and-formatting-pending',
                'source_arm9_sha256': sha(current), 'records': records}
    Path('translations/map_creature_class_manuscript_v2.json').write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All 39 native class initializers/name getters pass; four complete creature translations staged.')


if __name__ == '__main__':
    main()
