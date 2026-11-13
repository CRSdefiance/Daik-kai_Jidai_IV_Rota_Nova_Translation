"""Map source fleet-name getter branches; English layout/relocation remain open."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.inventory_arm9_text import components

SOURCE = '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75'
OWNERS = [(0x13523C, 12), (0x135248, 8), (0x135250, 8),
          (0x135258, 8), (0x135260, 16)]


def getter(source, name=None, *, unidentified='所属不明艦隊', pirate='海賊', ring_index=0):
    machine = machine_for(source)
    frame = STACK - 16
    machine.reg_write(UC_ARM_REG_SP, frame)
    machine.mem_write(frame + 4, struct.pack('<3I', 0x1234, 0x5678, STOP))
    if name is None:
        machine.reg_write(UC_ARM_REG_R0, 0)
        machine.emu_start(BASE + 0x36B0C, STOP, count=100)
        selected = machine.reg_read(UC_ARM_REG_R0)
        target = struct.unpack_from('<I', source, 0x36B54)[0]
        if selected != target:
            raise ValueError('Actual no-affiliation/no-captain branch selects unexpected text')
        raw = bytes(machine.mem_read(selected, 128)).split(b'\0')[0]
        if raw.decode('cp932') != unidentified:
            raise ValueError('Complete unidentified-fleet wording differs')
    else:
        pointer = 0x02410000
        machine.mem_write(pointer, name.encode('cp932') + b'\0')
        machine.reg_write(UC_ARM_REG_R0, pointer)
        owner = struct.unpack_from('<I', source, 0x36B48)[0]
        buffer = owner + 12 + ring_index * 128
        expected = (pirate + name).encode('cp932') + b'\0'
        # ABFCC calls AC000: +8 ring index, 32 slots, each 128 bytes at +12.
        machine.mem_write(owner - 32, b'\xA5' * (32 + 12 + 4096 + 32))
        machine.mem_write(owner, b'\0' * 12)
        machine.mem_write(owner + 8, struct.pack('<I', ring_index))
        machine.emu_start(BASE + 0x36B30, STOP, count=100000)
        selected = machine.reg_read(UC_ARM_REG_R0)
        if selected != buffer or bytes(machine.mem_read(owner - 32, 4172)) != (
                b'\xA5' * 32 + b'\0' * 8 + struct.pack('<I', (ring_index + 1) % 32)
                + b'\xA5' * (ring_index * 128) + expected
                + b'\xA5' * (4128 - ring_index * 128 - len(expected))):
            raise ValueError('Actual pirate-name native formatter changes text/observed guards')
        raw = expected[:-1]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native fleet getter fails to restore return frame')
    return {'name_fixture': name, 'complete_source_output': raw.decode('cp932'), 'ring_index': ring_index,
            'selected_pointer': selected, 'actual_formatter_or_literal_return_verified': True,
            'native_stack_restored': True}


def main():
    image = NdsImage.open('out/all_routes_combined_v147_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if (sha(source) != SOURCE or source[0x36A6C:0x36B4C] != clean[0x36A6C:0x36B4C]
            or source[0x36B50:0x36B5C] != clean[0x36B50:0x36B5C]):
        raise ValueError('Exact V147/original fleet getter required')
    inherited = struct.unpack_from('<I', source, 0x36B4C)[0] - BASE
    inherited_text = source[inherited:].split(b'\0', 1)[0].decode('cp932')
    start, end = 0x13523C, 0x135270
    refs = []
    for name, _, raw in components(image):
        for p in range(len(raw) - 3):
            target = struct.unpack_from('<I', raw, p)[0] - BASE
            if start <= target < end:
                refs.append({'component': name, 'field_offset': p, 'target_offset': target})
    owners = [{'offset': at, 'capacity': capacity,
               'source_hex': clean[at:at + capacity].hex(),
               'current_hex': source[at:at + capacity].hex(),
               'source_text': clean[at:at + capacity].split(b'\0')[0].decode('cp932')}
              for at, capacity in OWNERS]
    if any(o['source_hex'] != o['current_hex'] for o in owners):
        raise ValueError('Fleet-name family differs from clean Japanese')
    rows = []
    for at, capacity, japanese, english, meaning in (
            (0x135258, 8, '海賊%s', 'Pirate %s', 'Pirate followed by the captain name.'),
            (0x135260, 16, '所属不明艦隊', 'Unidentified fleet', 'A fleet whose affiliation is unknown.')):
        rows.append({'id': f'FLEET_NAME_{at:X}', 'offset': at, 'capacity': capacity,
                     'source_hex': clean[at:at + capacity].hex().upper(),
                     'japanese': japanese, 'english': english + '{PAD}',
                     'speaker': 'Fleet name getter',
                     'context': 'Native 36A6C fleet-name getter: no ordinary affiliation and no captain returns unidentified label; captain branch formats pirate prefix with captain name.',
                     'source_meaning': meaning,
                     'localization_note': 'Natural American English preserves affiliation uncertainty and pirate identity. Complete names and %s substitution must survive. Storage relocation, dynamic name bounds and display consumers remain unproved.',
                     'review': {'source': True, 'context': True, 'localization': True,
                                'naturalness': True, 'formatting': False}})
    manuscript = {'format': 'dk4-arm9-prompt-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'encoder': 'dialogue-fixed-v1',
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': rows}
    Path('translations/fleet_name_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    cases = [getter(source)] + [getter(source, name) for name in ('', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    proof = {'status': 'pass-source-fleet-getter-english-layout-pending',
             'source_arm9_sha256': sha(source), 'source_span': [start, end],
             'owners': owners, 'all_byte_position_address_candidates': refs,
             'native_source_cases': cases, 'candidate_changed': False,
             'inherited_ordinary_fleet_format': {'literal_offset': 0x36B4C,
                                                'target_offset': inherited, 'complete_text': inherited_text},
             'consumer_lock': {'start': 0x36A6C, 'end': 0x36B5C,
                               'sha256': sha(source[0x36A6C:0x36B5C])},
             'limits': ['Entry begins after upstream affiliation/captain getters; inputs are fixtures.',
                        'Actual AC000 ring allocator uses 32 slots of 128 bytes. Valid captain-name lengths are not established; formatter writes are not bounded by the allocator.',
                        'The ordinary %s fleet format at 135248 is already redirected by inherited literal 36B4C. Other possible consumers of its old bytes and the numbered-fleet format remain unresolved.',
                        'Complete English pirate/unidentified strings require 32 aligned bytes versus their 24 owned bytes.',
                        'Display consumers, rendering, relocation and physical gameplay remain pending.']}
    Path('work/analysis/fleet_name_source_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Five original fleet-name owners mapped; seven actual native source getter/formatter cases pass. English layout remains open.')


if __name__ == '__main__':
    main()
