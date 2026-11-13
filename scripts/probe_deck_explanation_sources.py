"""Map four untranslated Deck explanations and preserve full English drafts."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.inventory_arm9_text import components

SOURCE = '092f5a7f365286c8683728843df8774b26a7ba4ca507f4e6b5d368be82e07e34'
ROWS = [
    (0, 0x133024, 0x169F0, 'LOOKOUT',
     'A lookout makes it easier to discover towns and other locations at sea.',
     'Having a lookout makes towns and other locations easier to discover while at sea.'),
    (4, 0x13305C, 0x169F4, 'CAPTAIN',
     'A captain slows the rise in sailor fatigue.',
     'Having a captain makes sailor fatigue increase more slowly.'),
    (5, 0x133090, 0x169F8, 'ADJUTANT',
     'An adjutant lets you send negotiation documents from the guild.',
     'Having an adjutant enables sending negotiation documents at the guild.'),
    (10, 0x1330C8, 0x169FC, 'OARS',
     'This is where sailors row the oars. Navigators cannot be assigned here.',
     'This room is where sailors row the oars; navigators cannot be assigned to it.'),
]


def execute(source, room, state, at):
    machine = machine_for(source)
    resident = MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    machine.reg_write(UC_ARM_REG_R0, room)
    machine.reg_write(UC_ARM_REG_R1, state)
    machine.emu_start(BASE + 0x16868, STOP, count=1000)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or machine.reg_read(UC_ARM_REG_R0) != BASE + at):
        raise ValueError('Native Deck selector loses pointer/stack or depends on secondary state')
    raw = source[at:source.index(b'\0', at) + 1]
    machine.mem_write(STACK, b'\xA5' * 0x440)
    machine.reg_write(UC_ARM_REG_R6, room)
    machine.reg_write(UC_ARM_REG_R5, state)
    machine.emu_start(BASE + 0x19E70, BASE + 0x19E8C, count=100000)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x19E8C or machine.reg_read(UC_ARM_REG_SP) != STACK
            or bytes(machine.mem_read(STACK, 0x440)) != b'\xA5' * 16 + raw + b'\xA5' * (0x430 - len(raw))):
        raise ValueError('Actual Deck caller/macro copy changes complete source or 1024-byte buffer guards')
    return {'room': room, 'secondary_state': state, 'selected_offset': at,
            'complete_source_and_native_macro_copy_preserved': True}


def pool_plan(clean, current, reference_components):
    # This is an ownership/allocation lead, not permission to move every
    # neighboring label. All consumer grammars need independent classification.
    start, end = 0x133024, 0x133240
    owners, at = [], start
    drafted = {offset: english for _, offset, _, _, english, _ in ROWS}
    while at < end:
        nul = clean.index(b'\0', at)
        next_at = (nul + 4) & ~3
        if next_at > end or any(clean[nul + 1:next_at]):
            raise ValueError('Deck source ownership/alignment lead contains nonzero padding')
        current_nul = current.index(b'\0', at)
        if current_nul >= next_at:
            raise ValueError('Inherited Deck label exceeds its source owner')
        text = drafted.get(at, current[at:current_nul].decode('cp932'))
        owners.append({'offset': at, 'source_capacity': next_at - at,
                       'current_bytes_hex': current[at:next_at].hex().upper(),
                       'current_text': current[at:current_nul].decode('cp932'),
                       'proposed_complete_text': text, 'bytes_including_nul': len(text.encode('cp932')) + 1})
        at = next_at
    needed = sum(owner['bytes_including_nul'] for owner in owners)
    references = []
    literal_loads = {}
    for position in range(0, len(current) - 3, 4):
        instruction = struct.unpack_from('<I', current, position)[0]
        if instruction & 0x0F7F0000 == 0x051F0000:
            field = position + 8 + (1 if instruction & (1 << 23) else -1) * (instruction & 0xFFF)
            literal_loads.setdefault(field, []).append(position)
    for name, _, raw in reference_components:
        for position in range(len(raw) - 3):
            target = struct.unpack_from('<I', raw, position)[0] - BASE
            if start <= target < end:
                owner = next(owner for owner in owners if owner['offset'] <= target < owner['offset'] + owner['source_capacity'])
                references.append({'component': name, 'field_offset': position,
                                   'field_aligned': position % 4 == 0, 'target_offset': target,
                                   'owner_offset': owner['offset'], 'interior_byte_offset': target - owner['offset'],
                                   'pc_relative_load_instructions': literal_loads.get(position, []) if name == 'arm9' else [],
                                   'consumer_classification': ('native-pc-relative-literal-load-downstream-review-pending'
                                                             if name == 'arm9' and position in literal_loads
                                                             else 'native-equipment-pointer-table-index-bounds-pending'
                                                             if name == 'arm9' and 0x114E4C <= position <= 0x114E6C
                                                             else 'unresolved-address-word-candidate')})
    equipment = []
    if struct.unpack_from('<I', current, 0x1CA0C)[0] != BASE + 0x114E4C:
        raise ValueError('Deck equipment-label pointer table base differs')
    for index in range(9):
        machine = machine_for(current)
        machine.reg_write(UC_ARM_REG_R0, index)
        machine.emu_start(BASE + 0x1CA00, STOP, count=100)
        pointer = struct.unpack_from('<I', current, 0x114E4C + index * 4)[0]
        if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
                or machine.reg_read(UC_ARM_REG_R0) != pointer):
            raise ValueError('Native Deck equipment-label lookup changes pointer/stack')
        equipment.append({'index': index, 'pointer': pointer, 'selected_complete_text': current[pointer - BASE:current.index(b'\0', pointer - BASE)].decode('cp932')})
    return {'source_span': [start, end], 'source_capacity': end - start,
            'complete_unwrapped_bytes_including_nuls': needed,
            'unwrapped_spare_bytes': end - start - needed, 'owners': owners,
            'all_byte_position_address_candidates': references,
            'native_equipment_label_lookup_cases': equipment,
            'allocation_or_release_approved': False,
            'limits': 'Preserves all inherited neighboring wording as a storage lead. Native pointer/interior/fixed-copy consumers, shared controls, alignment, generated line guards and widget layout still require proof.'}


def main():
    image = NdsImage.open('out/all_routes_combined_v145_candidate.nds')
    current = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    if sha(current) != SOURCE or sha(clean) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731':
        raise ValueError('Pinned Deck source/current ARM9 differs')
    spans = [(0x16868, 0x16A0C), (0x19E68, 0x19ECC)]
    for lo, hi in spans:
        if current[lo:hi] != clean[lo:hi] or clean[lo:hi] != canonical[lo:hi]:
            raise ValueError('Deck selector/caller differs from original')
    records, cases = [], []
    for room, at, literal, name, english, meaning in ROWS:
        following = {0x133024: 0x13305C, 0x13305C: 0x133090,
                     0x133090: 0x1330C8, 0x1330C8: 0x1330FC}[at]
        if (current[at:following] != clean[at:following]
                or struct.unpack_from('<I', current, literal)[0] != BASE + at):
            raise ValueError('Deck complete source allocation/literal differs')
        cases.extend(execute(current, room, state, at) for state in range(256))
        records.append({'id': 'DECK_EXPLANATION_' + name, 'offset': at, 'capacity': following - at,
                        'source_hex': clean[at:following].hex().upper(),
                        'japanese': clean[at:following].split(b'\0', 1)[0].decode('cp932'),
                        'english': english + '{PAD}', 'speaker': 'Deck information panel',
                        'context': f'Native selector 16868 returns original pointer for room {room}; caller 19E78 passes it through macro copy 53914 into a 1024-byte buffer before the D5160/D5404 panel path.',
                        'source_meaning': meaning,
                        'localization_note': 'Full source-faithful natural English written independently of original line fragments. No abbreviations or authored wrapping. Layout and relocation remain pending.',
                        'review': {'source': True, 'context': True, 'localization': True,
                                   'naturalness': True, 'formatting': False}})
    manuscript = {'format': 'dk4-arm9-prompt-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                  'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
                  'review_gates': list(records[0]['review']), 'records': records}
    Path('translations/deck_explanations_manuscript_v1.json').write_text(
        json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = {'status': 'pass-original-native-deck-source-selection-copy-draft-layout-pending',
              'source_arm9_sha256': sha(clean), 'current_arm9_sha256': sha(current),
              'cases': cases, 'consumer_locks': [{'start': a, 'end': b, 'sha256': sha(clean[a:b])} for a, b in spans],
              'four_source_owner_bytes': sum(r['capacity'] for r in records),
              'full_english_unwrapped_bytes': sum(len(r['english'].removesuffix('{PAD}')) + 1 for r in records),
              'adjacent_complete_owned_pool_lead': pool_plan(clean, current, components(image)),
              'candidate_changed': False, 'runtime_verified': False,
              'limits': ['Native probes execute original Japanese selection/copy, not proposed English rendering.',
                         'Secondary states cover every byte as stress inputs, not a proven gameplay state range.',
                         'Parent bitmap geometry, final text wrapping/pixels, allocation and release/gameplay remain pending.']}
    Path('work/analysis/deck_explanations_source_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('status', 'four_source_owner_bytes', 'full_english_unwrapped_bytes')}))
    print(f'{len(cases)} native Deck source selections and complete caller/macro copies pass.')


if __name__ == '__main__':
    main()
