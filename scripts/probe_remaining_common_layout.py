"""Disposable packing/native-copy research for all remaining COMMON drafts.

Does not approve renderer layout, register a release or create a playable ROM.
"""

import argparse
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
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.residual_character_name_release import TARGET
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from dk4tool.script.common_native_reblocking import plan
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for

MANUSCRIPTS = ['translations/common_online_promotional_manuscript_v2.json',
               'translations/common_scene_labels_manuscript_v1.json']


def warm_copy(source, common, message_id, expected, *, cold_cache=False):
    blocks = IlnkContainer.parse(common).blocks
    directory = [struct.unpack_from('<HH', source, DIRECTORY_OFFSET + block * 4) for block in range(41)]
    block = max(i for i, (first, _) in enumerate(directory) if first <= message_id)
    start, following = struct.unpack_from('<2H', source, TABLE_OFFSET + message_id * 2)
    finish = following if following >= start else directory[block][1]
    if not 0 <= start < finish <= len(blocks[block]) <= 4096 or finish - start >= 512:
        raise ValueError('Research native copy extent exceeds source/cache/output')
    machine = machine_for(source)
    owner = struct.unpack_from('<I', source, 0x552A0)[0]
    output = owner + 0x2030
    machine.mem_write(owner + 0x2C, bytes((255 if cold_cache else block, 255, 0, 1)))
    if cold_cache:
        machine.mem_write(owner, source[0xD20B4:0xD20B8])
    else:
        machine.mem_write(owner + 0x30, blocks[block])
    machine.mem_write(output - 16, b'\xA5' * (16 + 512 + 16))
    executed, writes, opens, reads = set(), [], [], []

    def code(uc, address, size, _):
        executed.add(address - BASE)
        if cold_cache and address == BASE + 0xD0398:
            pointer = uc.reg_read(UC_ARM_REG_R1)
            path = bytes(uc.mem_read(pointer, 64)).split(b'\0', 1)[0]
            if (uc.reg_read(UC_ARM_REG_R0) != owner or uc.reg_read(UC_ARM_REG_R2) != 0
                    or b'MESFILE.DK4' not in path.upper()):
                raise ValueError('COMMON cold-cache host open arguments differ')
            opens.append(path.decode('ascii'))
            uc.mem_write(owner + 8, struct.pack('<I', 1))
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif cold_cache and address == BASE + 0xD0170:
            actor, offset, destination, count = [uc.reg_read(r) for r in
                                                (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
            if actor != owner or not 0 <= offset < offset + count <= len(common):
                raise ValueError('COMMON cold-cache host read escapes source')
            if not (owner <= destination < destination + count <= owner + 0x2030
                    or STACK - 0x1000 <= destination < destination + count <= STACK):
                raise ValueError(f'COMMON cold-cache read escapes header/cache/stack ownership: {destination:#x}, {count}')
            uc.mem_write(destination, common[offset:offset + count])
            reads.append({'offset': offset, 'count': count, 'destination': destination})
            uc.reg_write(UC_ARM_REG_R0, count)
            for r in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
                uc.reg_write(r, 0x02400000 + r)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def write(uc, access, address, size, value, _):
        if not ((output <= address < address + size <= output + 512)
                or ((owner if cold_cache else owner + 0x2C) <= address < address + size
                    <= (owner + 0x2030 if cold_cache else owner + 0x30))
                or (STACK - 0x1000 <= address < address + size <= STACK)):
            raise ValueError('Native COMMON warm copy writes outside output/LRU/stack')
        writes.append({'address': address, 'size': size})

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.reg_write(UC_ARM_REG_R0, owner)
    machine.reg_write(UC_ARM_REG_R1, message_id)
    machine.emu_start(BASE + 0x534F4, STOP, count=100000)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or machine.reg_read(UC_ARM_REG_R0) != output
            or bytes(machine.mem_read(output, len(expected) + 1)) != expected + b'\0'
            or (not cold_cache and bytes(machine.mem_read(output - 16, 16)) != b'\xA5' * 16)
            or bytes(machine.mem_read(output + 512, 16)) != b'\xA5' * 16
            or not {0x534F4, 0x53628, 0x535E0, 0xCEC74} <= executed):
        raise ValueError('Actual native COMMON copy loses complete text/guards/stack')
    if cold_cache and (len(opens) != 1 or len(reads) != 3
                       or not {0xD2018, 0xD1EF0, 0xD1F50, 0xD1EE0} <= executed):
        raise ValueError('Actual native COMMON cold-cache header/block path did not execute')
    return {'message_id': message_id, 'block': block, 'copied_bytes': finish - start,
            'english': expected.decode('cp932'), 'output_buffer_bytes': 512,
            'native_copy_first_final_nul_and_guards_verified': True,
            'cache_initialization_fixture': not cold_cache, 'write_count': len(writes),
            'cold_cache': cold_cache, 'host_file_contract_opens': opens, 'host_file_contract_reads': reads}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-v154', action='store_true', help='Rebase research onto repaired V154 and model ARM946 alignment explicitly.')
    args = parser.parse_args()
    candidate = 'out/all_routes_combined_v154_candidate.nds' if args.current_v154 else 'out/all_routes_combined_v150_candidate.nds'
    image = NdsImage.open(candidate)
    common, arm9 = [image.read_file(p) for p in ('/COMMON/MESFILE.DK4', '/__arm9__.bin')]
    expected_arm9 = '6730a45c7b1b74d3125c885f41425bb63442748aec22a1f7844808abfab70764' if args.current_v154 else TARGET
    if sha(arm9) != expected_arm9 or sha(common) != 'e916f6356187d935d18d9fb629be33f2b3db70ee4c4b5b2c913d0e68ceeb53b8':
        raise ValueError('Exact complete selected source required')
    if args.current_v154:
        from scripts.probe_common_copy_arm946_alignment import arm946_machine

        global machine_for
        machine_for = arm946_machine
    clean = NdsImage.open('work/clean.nds')
    original = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    current = common_message_entries(common, arm9, clean=False)
    authored = {}
    for path in MANUSCRIPTS:
        document = json.loads(Path(path).read_text(encoding='utf-8'))
        for row in document['records']:
            mid = row['message_id']
            if mid in authored or bytes.fromhex(row['source_hex']) != original[mid].text:
                raise ValueError('Duplicate ID or altered clean source manuscript')
            if current[mid].text != original[mid].text:
                raise ValueError('Remaining COMMON text already changed')
            authored[mid] = row['english'].removesuffix('{PAD}').encode('cp932')
    if set(authored) != set(range(3289, 3320)) | set(range(3393, 3607)):
        raise ValueError('Every one of the remaining 245 selections required')
    owners = {(current[i].block, current[i].record_index) for i in authored}
    preserved = {e.message_id: e.text for e in current
                 if (e.block, e.record_index) in owners and e.message_id not in authored}
    first = min(block for block, _ in owners)
    new_common, new_arm9, report = plan(common, arm9, authored, first_block=first, preserved=preserved)
    cases = [warm_copy(new_arm9, new_common, mid, raw) for mid, raw in sorted(authored.items())]
    cold = [warm_copy(new_arm9, new_common, mid, raw, cold_cache=True) for mid, raw in sorted(authored.items())]
    neighbors = [e for e in current if e.block >= first and e.message_id not in authored]
    neighbor_warm = [warm_copy(new_arm9, new_common, e.message_id, e.text) for e in neighbors]
    neighbor_cold = [warm_copy(new_arm9, new_common, e.message_id, e.text, cold_cache=True) for e in neighbors]
    report.update({'status': 'pass-research-all-remaining-common-packing-native-copy-layout-pending',
                   'source_arm9_sha256': expected_arm9, 'source_common_sha256': sha(common),
                   'source_candidate': candidate, 'ARM946_alignment_explicitly_modeled': args.current_v154,
                   'research_arm9_sha256': sha(new_arm9), 'research_common_sha256': sha(new_common),
                   'manuscript_hashes': {p: sha(Path(p).read_bytes()) for p in MANUSCRIPTS},
                   'native_warm_copy_cases': cases, 'native_cold_copy_cases': cold, 'candidate_changed': False,
                   'affected_unchanged_neighbor_warm_cases': neighbor_warm,
                   'affected_unchanged_neighbor_cold_cases': neighbor_cold,
                   'formatting_approved': False, 'physical_gameplay_verified': False,
                   'limits': ['Every original selection is compared by the packing planner; guarded native warm copies execute for the 245 drafts.',
                              'Warm cache contents/header are fixtures; cold-cache native ILNK header/block reads execute with a successful host open/read boundary contract, not physical I/O.',
                              'Preserved nonauthored packed neighbors do not count as new translations.',
                              'Actual COMMON consumers, resource identifiers, draw geometry, wrapping and glyph rendering remain unresolved.',
                              'Research only; no native directory registration, release profile or playable ROM.']})
    prefix = 'remaining_common_v154' if args.current_v154 else 'remaining_common'
    Path(f'work/analysis/{prefix}_research_common.bin').write_bytes(new_common)
    Path(f'work/analysis/{prefix}_research_arm9.bin').write_bytes(new_arm9)
    Path(f'work/analysis/{prefix}_layout_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'All {len(authored)} remaining drafts and {len(neighbors)} unchanged pool neighbors pass guarded native warm/cold copies; all {report["all_native_messages_compared"]} selections compared. Renderer mapping/integration pending.')


if __name__ == '__main__':
    main()
