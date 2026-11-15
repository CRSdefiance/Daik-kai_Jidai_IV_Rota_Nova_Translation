"""Research rebasing stale entity-name pointers to actual SDK-loaded DTCM bytes."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import BASE, STOP, machine_for


def main():
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    if sha(source) != '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75':
        raise ValueError('Exact complete V147 source required')
    document = json.loads(Path('translations/entity_ship_names_arm9_v2.json').read_text(encoding='utf-8'))
    pool = next(row for row in document['records'] if row['id'] == 'DK4_ENTITY_NAME_RELOCATION_POOL')
    old_code, code = [MainCodeFile(raw, BASE) for raw in (canonical, source)]
    old_start = sum(len(section.data) for section in old_code.sections[:2])
    new_start = sum(len(section.data) for section in code.sections[:2])
    old_data, data = old_code.sections[2], code.sections[2]
    if (old_data.ramAddress, data.ramAddress, len(data.data)) != (0x027E0000, 0x027E0000, 1632):
        raise ValueError('Original/current DTCM section ownership differs')
    relative = pool['offset'] - old_start
    expected_pool = bytes.fromhex(pool['replacement_hex'])
    if relative < 0 or relative + len(expected_pool) > len(data.data):
        raise ValueError('Full entity-name pool does not belong to source DTCM data')
    if bytes(data.data[relative:relative + len(expected_pool)]) != expected_pool:
        raise ValueError('Complete inherited entity-name pool changed')
    saved, moves = bytearray(source), []
    for row in document['records']:
        if 'POINTER' not in row['id']:
            continue
        at = row['offset']
        original = bytes.fromhex(row['replacement_hex'])
        if len(original) != 4 or source[at:at + 4] != original:
            raise ValueError('Inherited entity-name pointer field changed')
        target = struct.unpack('<I', original)[0]
        delta = target - BASE - pool['offset']
        if not 0 <= delta < len(expected_pool) or (delta and expected_pool[delta - 1] != 0):
            raise ValueError('Entity pointer is not a complete text owner start')
        text = expected_pool[delta:].split(b'\0', 1)[0].decode('cp932')
        if text != row['english']:
            raise ValueError('Original entity-pointer wording differs from owned pool')
        runtime = data.ramAddress + relative + delta
        struct.pack_into('<I', saved, at, runtime)
        moves.append({'field': at, 'original_pointer': target, 'runtime_pointer': runtime,
                      'complete_text': text})
    saved = bytes(saved)
    restored = bytearray(saved)
    for move in moves:
        at = move['field']
        restored[at:at + 4] = source[at:at + 4]
    if restored != source:
        raise ValueError('Entity runtime rebase changes bytes beyond pointer fields')
    machine = machine_for(saved)
    machine.mem_map(0x01FF0000, 0x10000)
    machine.mem_write(data.ramAddress, b'\xA5' * 0x4000)
    hardware = []

    def startup(uc, address, size, _):
        if not BASE + 0x9E0 <= address < BASE + 0xA5C:
            raise ValueError('Startup copier escapes native body')
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            hardware.append(address)
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    handle = machine.hook_add(UC_HOOK_CODE, startup)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    machine.hook_del(handle)
    if bytes(machine.mem_read(data.ramAddress, len(data.data))) != bytes(data.data):
        raise ValueError('Actual SDK copier loses DTCM data')
    bss_start, bss_end = struct.unpack_from('<2I', source, code.codeSettingsOffs + 12)
    machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x8AC
            or bytes(machine.mem_read(bss_start, bss_end - bss_start)) != bytes(bss_end - bss_start)
            or bytes(machine.mem_read(data.ramAddress, len(data.data))) != bytes(data.data)):
        raise ValueError('Native startup BSS clearing loses loaded entity-name storage')
    for move in moves:
        loaded = bytes(machine.mem_read(move['runtime_pointer'], 128)).split(b'\0', 1)[0].decode('cp932')
        if loaded != move['complete_text']:
            raise ValueError('Actual SDK load loses complete relocated text')
    cases = []
    table = struct.unpack_from('<I', source, 0xCDAC0)[0] - BASE
    for index in range(207):
        selected = ordinary_getter(saved, index, machine)
        if selected != struct.unpack_from('<I', saved, table + index * 32)[0]:
            raise ValueError('Native ordinary getter loses rebased pointer')
        text = bytes(machine.mem_read(selected, 128)).split(b'\0', 1)[0].decode('cp932')
        if not all(c.isprintable() for c in text):
            raise ValueError('Native runtime name remains nonprintable')
        cases.append({'index': index, 'selected_pointer': selected, 'complete_text': text})
    if bytes(machine.mem_read(data.ramAddress, len(data.data))) != bytes(data.data):
        raise ValueError('Native given-name consumers overwrite loaded name storage')
    japanese = [row['index'] for row in cases if any('\u3040' <= c <= '\u30ff' or '\u3400' <= c <= '\u9fff'
                                                   for c in row['complete_text'])]
    result = {'status': 'pass-research-sdk-loaded-entity-name-pointer-repair',
              'source_arm9_sha256': sha(source), 'research_arm9_sha256': sha(saved),
              'pool_old_file_offset': pool['offset'], 'pool_current_file_offset': new_start + relative,
              'pool_runtime_address': data.ramAddress + relative,
              'file_displacement': new_start - old_start, 'complete_pool_bytes': len(expected_pool),
              'pointers_rebased': len(moves), 'moves': moves, 'native_given_name_cases': cases,
              'remaining_japanese_given_name_indices': japanese,
              'actual_sdk_autoload_complete_dtcm_bytes_verified': True,
              'actual_startup_bss_clear_range': [bss_start, bss_end],
              'actual_startup_bss_clear_preserves_loaded_name_storage': True,
              'cache_operations_deferred': len(hardware), 'all_other_arm9_bytes_preserved': True,
              'candidate_changed': False,
              'limits': ['Actual SDK copier runs; cache maintenance remains a hardware contract.',
                         'Ordinary zero-type objects are fixtures; valid captain/class bounds and special player interface remain open.',
                         'This restores inherited complete entity English; older prose fidelity and remaining Japanese still need review.',
                         'Full startup/hardware ownership, downstream display, physical gameplay and strict integration remain pending.']}
    Path('work/analysis/entity_name_runtime_rebased_arm9.bin').write_bytes(saved)
    Path('work/analysis/entity_name_runtime_rebase_proof.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(moves)} entity pointers rebased to actual SDK-loaded storage; all 207 native ordinary getters return complete printable names.')


if __name__ == '__main__':
    main()
