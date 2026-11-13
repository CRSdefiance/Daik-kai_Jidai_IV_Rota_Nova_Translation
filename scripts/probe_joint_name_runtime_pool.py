"""REJECTED storage research: native scratch rendering overwrites this DTCM pool.

Retained for source/pointer/getter reproduction only; never integrate its output.
See probe_name_pool_scratch_conflict.py for the actual overwrite proof.
"""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for, select

ROLE_REVISIONS = {
    'Shopkeeper': ('広場の店主', 'Square Shopkeeper'),
}


def prepare(source, clean):
    if sha(source) != '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75':
        raise ValueError('Exact V147 required')
    original, current = [MainCodeFile(raw, BASE) for raw in (clean, source)]
    section = current.sections[2]
    if (section.ramAddress, len(section.data)) != (0x027E0000, 1632):
        raise ValueError('DTCM ownership changed')
    if bytes(original.sections[2].data[:1540]) != bytes(1540):
        raise ValueError('Original shared allocation is not empty')
    if bytes(section.data[1540:]) != bytes(original.sections[2].data[1540:]):
        raise ValueError('SDK trailing pointer table changed')
    start = sum(len(s.data) for s in current.sections[:2])
    packed, moves, fields, owners = bytearray(), [], set(), []
    for name in ('all_item_names_arm9_v1', 'entity_ship_names_arm9_v2'):
        document = json.loads(Path(f'translations/{name}.json').read_text(encoding='utf-8'))
        pool = next(r for r in document['records'] if 'RELOCATION_POOL' in r['id'])
        payload = bytes.fromhex(pool['replacement_hex'])
        locations = {}
        for row in document['records']:
            if 'POINTER' not in row['id']:
                continue
            word = bytes.fromhex(row['replacement_hex'])
            if len(word) != 4:
                raise ValueError('Pointer field is not a word')
            old_pointer = struct.unpack('<I', word)[0]
            delta = old_pointer - BASE - pool['offset']
            if not 0 <= delta < len(payload):
                continue
            field = row['offset']
            if field in fields or source[field:field + 4] != word:
                raise ValueError('Duplicate or changed inherited pointer field')
            fields.add(field)
            text = payload[delta:].split(b'\0', 1)[0]
            if (delta and payload[delta - 1] != 0) or text.decode('cp932') != row['english']:
                raise ValueError('Pointer does not own the complete reviewed text')
            revision = ROLE_REVISIONS.get(row['english']) if name == 'entity_ship_names_arm9_v2' else None
            if revision:
                original_pointer = struct.unpack_from('<I', clean, field)[0] - BASE
                original_text = clean[original_pointer:].split(b'\0', 1)[0].decode('cp932')
                if original_text != revision[0]:
                    raise ValueError('Reviewed full role name does not match original Japanese owner')
                text = revision[1].encode('ascii')
            english = text.decode('cp932')
            if delta not in locations:
                while len(packed) % 4:
                    packed.append(0)
                locations[delta] = len(packed)
                packed.extend(text + b'\0')
                owners.append({'batch': name, 'old_pointer': old_pointer,
                               'runtime_pointer': section.ramAddress + locations[delta],
                               'text': english, 'inherited_text': row['english']})
            moves.append({'id': row['id'], 'batch': name, 'field': field,
                          'old_pointer': old_pointer,
                          'runtime_pointer': section.ramAddress + locations[delta],
                          'text': english,
                          'source_reviewed_role_revision': revision is not None})
    while len(packed) % 4:
        packed.append(0)
    if len(packed) > 1540 or len(moves) != 238:
        raise ValueError('Full joint allocation/count differs')
    monster = next(o for o in owners if o['batch'] == 'entity_ship_names_arm9_v2'
                   and o['text'] == 'Monster')
    if struct.unpack_from('<I', source, 0x705E8)[0] != monster['old_pointer']:
        raise ValueError('Inherited native map Monster alias changed')
    moves.append({'id': 'NATIVE_MAP_MONSTER_ALIAS', 'batch': 'native-map-label',
                  'field': 0x705E8, 'old_pointer': monster['old_pointer'],
                  'runtime_pointer': monster['runtime_pointer'], 'text': 'Monster'})
    saved = bytearray(source)
    saved[start:start + 1540] = packed + bytes(1540 - len(packed))
    for move in moves:
        struct.pack_into('<I', saved, move['field'], move['runtime_pointer'])
    restored = bytearray(saved)
    restored[start:start + 1540] = source[start:start + 1540]
    for move in moves:
        at = move['field']
        restored[at:at + 4] = source[at:at + 4]
    if restored != source:
        raise ValueError('Changes escape shared allocation and pointer fields')
    return bytes(saved), start, len(packed), moves, owners


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--persistent', action='store_true', help='Run consumer checks on the separately reserved section.')
    args = parser.parse_args()
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    saved, start, used, moves, owners = prepare(source, clean)
    if args.persistent:
        saved = Path('work/analysis/persistent_name_section_arm9.bin').read_bytes()
        persistent = json.loads(Path('work/analysis/persistent_name_section_proof.json').read_text(encoding='utf-8'))
        if sha(saved) != persistent['research_sha256']:
            raise ValueError('Exact separately reserved section research required')
        updated = {}
        for move in moves:
            move['runtime_pointer'] = struct.unpack_from('<I', saved, move['field'])[0]
            updated[move['old_pointer']] = move['runtime_pointer']
        for owner in owners:
            owner['runtime_pointer'] = updated[owner['old_pointer']]
    for begin, end in ((0x4A53C, 0x4A58C), (0xCDAFC, 0xCDB48), (0x102AD0, 0x102BC4),
                       (0xCBE68, 0xCBED4), (0xCC3C0, 0xCC3D4), (0x13C38C, 0x13C3A0)):
        if saved[begin:end] != clean[begin:end]:
            raise ValueError('Native item initializer/getter/resolver differs from source')
    code = MainCodeFile(saved, BASE)
    section = code.sections[2]
    machine = machine_for(saved)
    machine.mem_map(0x01FF0000, 0x10000)
    machine.mem_write(section.ramAddress, b'\xA5' * 0x4000)

    def startup(uc, address, size, _):
        if not BASE + 0x9E0 <= address < BASE + 0xA5C:
            raise ValueError('SDK copier escapes native body')
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    hook = machine.hook_add(UC_HOOK_CODE, startup)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    machine.hook_del(hook)
    bss_start, bss_end = struct.unpack_from('<2I', saved, code.codeSettingsOffs + 12)
    machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x8AC
            or bytes(machine.mem_read(bss_start, bss_end - bss_start)) != bytes(bss_end - bss_start)):
        raise ValueError('Actual BSS clearing did not finish')
    for move in moves:
        pointer = struct.unpack_from('<I', saved, move['field'])[0]
        text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
        if text != move['text']:
            raise ValueError('SDK-loaded complete name differs')
    # The last 30 names are mutable buffers, not direct static-catalogue names.
    # Only the serialized input boundary is a fixture; the native initializer
    # builds every runtime pointer and copies the first ten metadata pairs.
    runtime_root = struct.unpack_from('<I', saved, 0xCDB44)[0]
    runtime_catalogue = runtime_root + 0x3E4
    serialized = bytearray(0x6B4)
    mutable_names = []
    for index in range(30):
        text = (f'Custom Item {index + 1}' if index % 2 == 0 else f'船{index + 1}')
        encoded = text.encode('cp932') + b'\0'
        serialized[0x22 + index * 32:0x22 + index * 32 + len(encoded)] = encoded
        struct.pack_into('<2I', serialized, 0x3E4 + index * 24 + 8, index + 100, index + 200)
        mutable_names.append(text)
    load_calls = []
    init_writes = []
    native_item_storage = struct.unpack_from('<I', saved, 0x102B80)[0]
    metadata_fields = {native_item_storage + (188 + i) * 20 + 0x34E4 + extra
                       for i in range(10) for extra in (0, 4)}

    def load_input(uc, address, size, _):
        if address == BASE + 0x46858:
            if uc.reg_read(UC_ARM_REG_R1) != runtime_root:
                raise ValueError('Native initializer loads the wrong runtime object')
            uc.mem_write(runtime_root, bytes(serialized))
            load_calls.append(address)
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def init_write(uc, access, address, size, value, _):
        if not ((STACK - 0x10000 <= address and address + size <= STACK)
                or (size == 4 and address in metadata_fields)
                or (size == 4 and runtime_catalogue <= address < runtime_catalogue + 30 * 24
                    and (address - runtime_catalogue) % 24 == 0)):
            raise ValueError('Native mutable-item initialization writes outside owned fields')
        init_writes.append({'address': address, 'size': size, 'value': value})

    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_R0, runtime_root)
    machine.reg_write(UC_ARM_REG_R1, 0x02430000)
    hook = machine.hook_add(UC_HOOK_CODE, load_input)
    write_hook = machine.hook_add(UC_HOOK_MEM_WRITE, init_write)
    machine.emu_start(BASE + 0x102AD0, STOP, count=3000)
    machine.hook_del(hook)
    machine.hook_del(write_hook)
    if len(load_calls) != 1 or machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Native late-item initializer did not finish')
    for index in range(30):
        pointer = struct.unpack('<I', machine.mem_read(runtime_catalogue + index * 24, 4))[0]
        if pointer != runtime_root + 0x22 + index * 32:
            raise ValueError('Native initializer loses mutable name buffer')
        if index < 10:
            target = native_item_storage + (188 + index) * 20 + 0x34E4
            if struct.unpack('<2I', machine.mem_read(target, 8)) != (index + 100, index + 200):
                raise ValueError('Native initializer loses late-item metadata')
    item_root = struct.unpack_from('<I', saved, 0xCB198)[0]
    # The actual global initialization loop owns 218 objects of 20 bytes.
    machine.reg_write(UC_ARM_REG_R4, item_root - 0x34D8)
    machine.emu_start(BASE + 0xCBE68, BASE + 0xCBED4, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0xCBED4:
        raise ValueError('Native global item-object initialization did not finish')
    item_cases = []
    caller_cases = []
    for index in range(218):
        actor = item_root + 4 + index * 20
        vtable = struct.unpack('<I', machine.mem_read(actor, 4))[0]
        if vtable != BASE + 0x13C38C:
            raise ValueError('Native item object owns an unexpected interface')
        getter = struct.unpack('<I', machine.mem_read(vtable + 8, 4))[0]
        if getter != BASE + 0x4A53C:
            raise ValueError('Native item interface selects a different name getter')
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.reg_write(UC_ARM_REG_R0, actor)
        machine.emu_start(getter, STOP, count=1000)
        pointer = machine.reg_read(UC_ARM_REG_R0)
        expected_pointer = (struct.unpack_from('<I', saved, 0x11E210 + index * 24)[0]
                            if index < 188 else runtime_root + 0x22 + (index - 188) * 32)
        if (machine.reg_read(UC_ARM_REG_PC) != STOP
                or machine.reg_read(UC_ARM_REG_SP) != STACK or pointer != expected_pointer):
            raise ValueError('Actual item index/name getter loses complete pointer')
        text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
        if not all(c.isprintable() for c in text):
            raise ValueError('Native item name remains corrupted')
        if index >= 188 and text != mutable_names[index - 188]:
            raise ValueError('Mutable item name differs from complete input')
        item_cases.append({'index': index, 'pointer': pointer, 'text': text,
                           'native_initialized_object': actor, 'vtable': vtable, 'name_getter': getter,
                           'native_initialized_mutable_name': index >= 188})
        for entry, end, index_register, result_register in (
                (0x1C7CC, 0x1C7EC, UC_ARM_REG_R4, UC_ARM_REG_R4),
                (0x1C91C, 0x1C93C, UC_ARM_REG_R6, UC_ARM_REG_R7)):
            if saved[entry:end] != clean[entry:end]:
                raise ValueError('Actual virtual item-name caller changed')
            machine.reg_write(UC_ARM_REG_SP, STACK)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            machine.reg_write(index_register, index)
            machine.emu_start(BASE + entry, BASE + end, count=1000)
            if (machine.reg_read(UC_ARM_REG_PC) != BASE + end
                    or machine.reg_read(UC_ARM_REG_SP) != STACK
                    or machine.reg_read(result_register) != pointer):
                raise ValueError('Actual root/index/vtable/name caller loses pointer or stack')
            selected = bytes(machine.mem_read(machine.reg_read(result_register), 128)).split(b'\0', 1)[0].decode('cp932')
            if selected != text:
                raise ValueError('Native virtual name caller loses complete text')
            caller_cases.append({'entry': entry, 'end': end, 'index': index,
                                 'selected_pointer': pointer, 'text': selected})
    static_cases = []
    for index in range(218):
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.reg_write(UC_ARM_REG_R0, index)
        machine.reg_write(UC_ARM_REG_R1, 0)
        machine.emu_start(BASE + 0xCDAFC, STOP, count=1000)
        entry = machine.reg_read(UC_ARM_REG_R0)
        if entry != BASE + 0x11E210 + index * 24:
            raise ValueError('Static item catalogue selector differs')
        pointer = struct.unpack('<I', machine.mem_read(entry, 4))[0]
        text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
        static_cases.append({'index': index, 'pointer': pointer, 'text': text})
    table = struct.unpack_from('<I', saved, 0xCDAC0)[0] - BASE
    cases = []
    for index in range(207):
        pointer = ordinary_getter(saved, index, machine)
        if pointer != struct.unpack_from('<I', saved, table + index * 32)[0]:
            raise ValueError('Native ordinary getter differs')
        text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
        if not all(c.isprintable() for c in text):
            raise ValueError('Native given name remains corrupted')
        cases.append({'index': index, 'text': text, 'pointer': pointer})
    map_cases = [select(saved, case, machine) for case in ('pirates', 'monster', 'unknown', 'named')]
    if bytes(machine.mem_read(section.ramAddress, 1632)) != bytes(section.data):
        raise ValueError('Loaded DTCM storage changed')
    name_section = code.sections[3] if args.persistent else section
    if bytes(machine.mem_read(name_section.ramAddress, len(name_section.data))) != bytes(name_section.data):
        raise ValueError('Native item/name/map consumers overwrite persistent storage')
    result = {'status': ('pass-native-item-name-map-consumers-persistent-section' if args.persistent
                         else 'isolated-checks-pass-storage-rejected-native-scratch-alias'),
              'separately_reserved_persistent_names': args.persistent,
              'storage_approved_for_integration': False,
              'native_scratch_conflict_proof': 'work/analysis/name_pool_scratch_conflict_proof.json',
              'source_sha256': sha(source), 'research_sha256': sha(saved),
              'serialized_dtcm_start': start, 'runtime_base': name_section.ramAddress,
              'allocation_bytes': len(name_section.data) if args.persistent else 1540, 'used_aligned_bytes': used,
              'complete_string_owners': owners, 'pointer_moves': moves,
              'native_ordinary_given_names': cases,
              'native_item_name_getter_cases': item_cases,
              'native_item_virtual_caller_cases': caller_cases,
              'native_item_object_initializer': {'start': 0xCBE68, 'end': 0xCBED4,
                                                 'object_count': 218, 'object_stride': 20,
                                                 'vtable': BASE + 0x13C38C, 'name_slot_offset': 8},
              'native_static_item_catalogue_cases': static_cases,
              'native_mutable_item_initializer': {'entry': 0x102AD0, 'serialized_input_contract': 0x46858,
                                                  'runtime_root': runtime_root, 'pointer_count': 30,
                                                  'metadata_pairs_verified': 10, 'guarded_writes': init_writes},
              'native_map_label_selection_cases': map_cases,
              'sdk_copy_and_bss_clear_preserve_all_names': True,
              'sdk_trailing_92_bytes_preserved': True,
              'itcm_and_all_other_bytes_preserved': True, 'candidate_changed': False,
              'limits': ['All 30 mutable pointers are natively initialized, but serialized input is a fixture at the file-load boundary; actual save/new-game data producers remain open.',
                         'Reference inventory, runtime writes, display bounds and full gameplay remain pending.',
                         'Cache instructions are hardware contracts; this is not full boot evidence.',
                         'Inherited wording is preserved; untranslated names and older fidelity review remain open.']}
    if not args.persistent:
        Path('work/analysis/joint_name_runtime_pool_arm9.bin').write_bytes(saved)
    report_path = 'persistent_name_consumers_proof.json' if args.persistent else 'joint_name_runtime_pool_proof.json'
    Path('work/analysis', report_path).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    reviewed_roles = []
    for move in moves:
        if not move.get('source_reviewed_role_revision'):
            continue
        original_pointer = struct.unpack_from('<I', clean, move['field'])[0]
        reviewed_roles.append({
            'id': move['id'], 'pointer_field': move['field'], 'source_pointer': original_pointer,
            'japanese': '広場の店主', 'english': 'Square Shopkeeper{PAD}',
            'speaker': 'Square shopkeeper nameplate',
            'context': 'Ordinary native given-name table entries 84–91. Each clean pointer selects the same explicit location and role.',
            'source_meaning': 'The shopkeeper in the square.',
            'localization_note': 'Retains the source location and role in complete natural English; shared aligned relocation replaces the shortened inherited label. Display layout remains pending.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False}})
    Path('translations/shared_square_shopkeeper_name_review_v1.json').write_text(json.dumps({
        'format': 'dk4-name-review-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'target_locale': 'en-US', 'clean_arm9_sha256': sha(clean), 'records': reviewed_roles,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(moves)} pointers, {len(owners)} owners, {used}/{len(name_section.data) if args.persistent else 1540} bytes; 218 item getters, 218 static selectors, 436 virtual callers, 207 ordinary getters and four map selections pass.')


if __name__ == '__main__':
    main()
