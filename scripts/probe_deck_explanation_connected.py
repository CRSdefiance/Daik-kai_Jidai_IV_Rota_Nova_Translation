"""Connect relocated Deck selectors, macro copying and actual bitmap painting."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE, arm_const
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import ACTOR, BASE, STACK, machine_for
from scripts.probe_deck_explanation_sources import ROWS
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def pointer_consumers(source, pool):
    moves = {m['old_offset']: m for m in pool['moves']}
    cases = []
    for ref in pool['references']:
        move = moves[ref['owner_offset']]
        pointer = BASE + move['new_offset']
        if struct.unpack_from('<I', source, ref['field_offset'])[0] != pointer:
            raise ValueError('Relocated Deck literal/table points to wrong owner')
        for instruction in ref['pc_relative_load_instructions']:
            word = struct.unpack_from('<I', source, instruction)[0]
            register = getattr(arm_const, 'UC_ARM_REG_R' + str((word >> 12) & 15))
            passed = False
            for flags in range(16):
                machine = machine_for(source)
                cpsr = machine.reg_read(arm_const.UC_ARM_REG_CPSR)
                machine.reg_write(arm_const.UC_ARM_REG_CPSR, (cpsr & 0x0FFFFFFF) | (flags << 28))
                machine.reg_write(register, 0)
                machine.emu_start(BASE + instruction, BASE + instruction + 4, count=1)
                if machine.reg_read(register) == pointer:
                    passed = True
                    cases.append({'kind': 'native-literal-load', 'instruction': instruction,
                                  'field': ref['field_offset'], 'relocated_pointer': pointer,
                                  'condition_flags_fixture': flags})
                    break
            if not passed:
                raise ValueError('Actual native Deck PC-relative consumer does not select relocated owner')
        raw = source[move['new_offset']:source.index(b'\0', move['new_offset'])].decode('cp932')
        if raw != move['complete_text']:
            raise ValueError('Relocated Deck consumer loses complete owner text/NUL')
    for index in range(9):
        machine = machine_for(source)
        machine.reg_write(arm_const.UC_ARM_REG_R0, index)
        machine.emu_start(BASE + 0x1CA00, 0x027E0000, count=100)
        expected = struct.unpack_from('<I', source, 0x114E4C + index * 4)[0]
        if machine.reg_read(arm_const.UC_ARM_REG_R0) != expected or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Native relocated equipment-label getter changes pointer/stack')
        cases.append({'kind': 'native-equipment-label-getter', 'index': index, 'relocated_pointer': expected})
    if len(cases) != 31:
        raise ValueError('Complete native Deck literal/table consumer set differs')
    return cases


def execute(source, room, state, move):
    machine = machine_for(source)
    resident = MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    # Default bitmap construction and successful parent allocation are fixture
    # contracts. Resource setup, native origin getter and actual painters execute.
    machine.mem_write(ACTOR + 0x10, source[0xD3C00:0xD3C04])
    machine.reg_write(UC_ARM_REG_R4, 1)
    machine.reg_write(UC_ARM_REG_R5, ACTOR)
    machine.emu_start(BASE + 0x19F90, BASE + 0x19FE8, count=10000)
    if struct.unpack('<2I', machine.mem_read(ACTOR + 0x38, 8)) != (168, 84):
        raise ValueError('Connected Deck bitmap dimensions differ')
    bitmap_bytes = 42 * 2 * 84
    machine.mem_write(ACTOR + 0xA8, b'\x99' * bitmap_bytes)
    machine.mem_write(ACTOR + 0xA8 + bitmap_bytes + 20, b'\xA5' * 32)
    machine.mem_write(STACK, b'\xA5' * 0x500)
    font = struct.unpack_from('<I', source, 0xD5088)[0]
    machine.mem_write(font + 4, struct.pack('<2I', 6, 12))
    machine.reg_write(UC_ARM_REG_R6, room)
    machine.reg_write(UC_ARM_REG_R5, state)
    machine.reg_write(UC_ARM_REG_R8, ACTOR)
    events, executed = [], set()

    def code(uc, address, size, _):
        executed.add(address)
        if address == BASE + 0xD16B4:
            sp = uc.reg_read(UC_ARM_REG_SP)
            glyph, style = struct.unpack('<2I', uc.mem_read(sp, 8))
            events.append({'kind': 'ascii', 'code': glyph, 'style': style,
                           'x': uc.reg_read(UC_ARM_REG_R2), 'y': uc.reg_read(UC_ARM_REG_R3)})

    machine.hook_add(UC_HOOK_CODE, code)
    machine.emu_start(BASE + 0x19E70, BASE + 0x19EB4, count=1000000)
    text = move['complete_text']
    raw = text.encode('ascii') + b'\0'
    content = [e for e in events if e['code'] != 32]
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x19EB4 or machine.reg_read(UC_ARM_REG_SP) != STACK
            or bytes(machine.mem_read(STACK + 0x10, 1024)) != raw + b'\xA5' * (1024 - len(raw))
            or [e['code'] for e in content] != [ord(c) for c in text if c not in (' ', '\n')]):
        raise ValueError('Connected Deck native caller loses full text, glyphs or buffer guards')
    if any(e['x'] < 0 or e['x'] + 6 > 168 or e['y'] < 0 or e['y'] + 12 > 36 for e in content):
        raise ValueError('Connected Deck text overlaps following label or bitmap edge')
    actual = bytes(machine.mem_read(ACTOR + 0xA8, bitmap_bytes))
    padded = bytearray(b'\x99' * (128 * 192))
    for y in range(84):
        padded[y * 128:y * 128 + 84] = actual[y * 84:(y + 1) * 84]
    if bytes(padded) != expected_pixels(source, b'', events, 4, background=9):
        raise ValueError('Connected native Deck pixels differ from independent font decode')
    if bytes(machine.mem_read(ACTOR + 0xA8 + bitmap_bytes + 20, 32)) != b'\xA5' * 32:
        raise ValueError('Connected Deck bitmap resource guard changed')
    required = {0x16868, 0x53914, 0xD5160, 0xD5404, 0xD16B4, 0xE2A5C}
    if not {BASE + at for at in required} <= executed:
        raise ValueError('Connected Deck selector/copy/raster/glyph-copy bodies did not execute')
    return {'room': room, 'state': state, 'relocated_offset': move['new_offset'],
            'complete_text': text, 'pixels_sha256': sha(actual),
            'actual_selector_macro_copy_context_and_pixels_connected': True,
            'glyph_count': len(content), 'full_pixels_independently_verified': True}


def main():
    source = Path('work/analysis/deck_explanations_pool_arm9.bin').read_bytes()
    pool_path = Path('work/analysis/deck_explanations_pool_proof.json')
    pool = json.loads(pool_path.read_text(encoding='utf-8'))
    if sha(source) != pool['research_arm9_sha256']:
        raise ValueError('Connected Deck research bytes differ')
    moves = {m['old_offset']: m for m in pool['moves']}
    cases = [execute(source, room, state, moves[offset]) for room, offset, *_ in ROWS for state in (0, 255)]
    result = {'status': 'pass-connected-native-deck-relocated-text-and-pixels',
              'research_arm9_sha256': sha(source), 'pool_proof_sha256': sha(pool_path.read_bytes()),
              'cases': cases, 'runtime_verified': False,
              'native_pointer_consumer_cases': pointer_consumers(source, pool),
              'limits': 'Bitmap default vtable, successful parent allocation, background clearing and font metrics are fixture contracts. Native resource setup, real bitmap origin, selector, macro copy, text context, glyph copies and raster execute in one machine. Physical composition/input/gameplay remain pending.'}
    Path('work/analysis/deck_explanations_connected_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} connected relocated Deck caller/bitmap executions match complete independent pixels.')


if __name__ == '__main__':
    main()
