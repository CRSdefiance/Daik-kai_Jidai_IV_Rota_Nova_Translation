"""Execute source-bounded tooltip getters and full-width numeric conversions."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import (
    ACTOR,
    BASE,
    STACK,
    STOP,
    format_copy,
    machine_for,
)
from scripts.execute_scene_caption_raster import execute as raster


def digits(value):
    return ''.join(chr(0xFF10 + int(c)) for c in str(value)).encode('cp932')


def execute_pair(source, percentage, armament, *, entry=0, ring_index=31):
    if not 0 <= percentage <= 255 or not 0 <= armament <= 65535 or entry not in (None, 0, 1, 2) or not 0 <= ring_index < 32:
        raise ValueError('Values exceed source byte/halfword/ring bounds')
    machine = machine_for(source)
    pool = struct.unpack_from('<I', source, 0xABFC0)[0]
    machine.mem_write(pool + 8, struct.pack('<I', ring_index))
    machine.mem_write(pool + 12, b'\xA5' * (32 * 128))
    pairs = bytearray([0x15, 0, 0x15, 0, 0x15, 0])
    if entry is not None:
        pairs[entry * 2:entry * 2 + 2] = bytes([7, percentage])
    machine.mem_write(ACTOR + 0x10, bytes(pairs))
    machine.mem_write(ACTOR + 0x18, struct.pack('<H', armament))
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Numeric getter/converter executes outside native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x1000 <= address and address + size <= STACK)
                or (pool + 8 <= address and address + size <= pool + 12)
                or (pool + 12 <= address and address + size <= pool + 12 + 32 * 128)):
            raise ValueError('Native numeric conversion writes outside ring/stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)

    def call(offset, value, argument=None):
        machine.reg_write(UC_ARM_REG_R0, value)
        if argument is not None:
            machine.reg_write(UC_ARM_REG_R1, argument)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + offset, STOP, count=10000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Native numeric call fails to return with intact stack')
        return machine.reg_read(UC_ARM_REG_R0)

    selected = call(0xB4AA8, ACTOR, 7)
    expected_percentage = percentage if entry is not None else 0
    if selected != expected_percentage:
        raise ValueError('Native percentage selection differs')
    percent_pointer = call(0xABF50, selected)
    selected_armament = call(0xB3FD4, ACTOR, 1)
    if selected_armament != armament:
        raise ValueError('Native unsigned armament selection differs')
    armament_pointer = call(0xABF50, selected_armament)
    values = []
    for pointer, value, index in ((percent_pointer, expected_percentage, ring_index),
                                 (armament_pointer, armament, (ring_index + 1) % 32)):
        expected = digits(value) + b'\0'
        slot = pool + 12 + index * 128
        if pointer != slot + 128 - len(expected) or bytes(machine.mem_read(pointer, len(expected))) != expected:
            raise ValueError('Native full-width digits lose first/last bytes/NUL or alias a ring slot')
        if bytes(machine.mem_read(slot, 128 - len(expected))) != b'\xA5' * (128 - len(expected)):
            raise ValueError('Numeric conversion damages earlier slot bytes')
        values.append(expected[:-1])
    if not {0xB4AA8, 0xB3FD4, 0xABF50, 0xAC000} <= executed:
        raise ValueError('Native getter/converter/ring bodies were not executed')
    used = {ring_index, (ring_index + 1) % 32}
    for index in set(range(32)) - used:
        if bytes(machine.mem_read(pool + 12 + index * 128, 128)) != b'\xA5' * 128:
            raise ValueError('Native numeric conversion damages another ring slot')
    final_index = struct.unpack('<I', machine.mem_read(pool + 8, 4))[0]
    if final_index != (ring_index + 2) % 32:
        raise ValueError('Native numeric ring advancement/wrap differs')
    return {'percentage': selected, 'armament': armament, 'matching_entry': entry,
            'ring_index': ring_index, 'percent_pointer': percent_pointer, 'armament_pointer': armament_pointer,
            'percent_hex': values[0].hex(), 'armament_hex': values[1].hex(),
            'final_ring_index': final_index, 'all_other_ring_slots_preserved': True,
            'complete_digits_nul_stack_and_distinct_ring_slots_preserved': True}


def verify_mixed(source, name, percentage, armament, mode):
    native = execute_pair(source, percentage, armament)
    percent, rating = bytes.fromhex(native['percent_hex']), bytes.fromhex(native['armament_hex'])
    raw = name.encode('ascii') + b'  ' + percent.rjust(6) + b'%\n  Armament ' + rating.rjust(8)
    copied = format_copy(source, 0x705F4, [name.encode('ascii'), percent, rating], raw)
    text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('cp932')
    result = raster(source, text, tooltip=True, mode=mode)
    visible = [g for g in result['glyphs'] if g['code'] != 32]
    percent_x = (len(name) + 2 + max(6 - len(percent), 0)) * 6
    expected_ascii = ([{'code': ord(c), 'style': 15, 'x': i * 6, 'y': 0}
                       for i, c in enumerate(name) if c != ' ']
                      + [{'code': ord('%'), 'style': 15, 'x': percent_x + len(percent) * 6, 'y': 0}]
                      + [{'code': ord(c), 'style': 15, 'x': (i + 1) * 6, 'y': 12}
                         for i, c in enumerate('Armament')])
    expected_cp = []
    for raw_digits, x, y in ((percent, percent_x, 0), (rating, 60 + max(8 - len(rating), 0) * 6, 12)):
        expected_cp.extend({'code': int.from_bytes(raw_digits[i:i + 2], 'big'),
                            'style': 15, 'x': x + i * 6, 'y': y} for i in range(0, len(raw_digits), 2))
    if visible != expected_ascii or result['cp932_glyphs'] != expected_cp:
        raise ValueError('Mixed native ASCII/full-width numeric glyph bytes/rows/leading character differ')
    width = max(len(line.encode('cp932')) for line in text.split('\n')) * 6
    if width > 256 or result['tooltip_composites'][0]['width'] != width:
        raise ValueError('Mixed numeric tooltip width differs or exceeds screen')
    return {'name': name, 'percentage': percentage, 'armament': armament, 'mode': mode,
            'width': width, 'ascii_glyphs': visible, 'cp932_glyph_requests': result['cp932_glyphs'],
            'ascii_bytes_positions_and_native_cp932_requests_preserved': True,
            'cp932_pixel_painter_is_contract': True}


def main():
    root = Path('work/analysis/map_creature_complete_v139')
    source = (root / 'proposed_arm9.bin').read_bytes()
    report = json.loads((root / 'report.json').read_text(encoding='utf-8'))
    if sha(source) != report['target_arm9_sha256']:
        raise ValueError('Complete allocation differs')
    percentage_cases = [execute_pair(source, value, 65535, entry=entry) for entry in range(3) for value in range(256)]
    boundary_cases = [execute_pair(source, 255, value, entry=None if value == 0 else 0, ring_index=index)
                      for index in (0, 31) for value in (0, 9, 10, 99, 100, 999, 1000, 9999, 10000, 65535)]
    mixed = [verify_mixed(source, name, percent, armament, mode)
             for name in ('Fleet', 'FleetX', 'Albuquerque', 'Nagarpur Co.')
             for percent, armament in ((0, 0), (9, 9), (10, 100), (99, 9999), (255, 65535))
             for mode in (4, 16)]
    output = {'status': 'pass-source-bounded-numeric-getters-conversion-and-mixed-glyph-requests',
              'target_arm9_sha256': sha(source), 'percentage_cases': percentage_cases,
              'boundary_cases': boundary_cases, 'mixed_cases': mixed,
              'source_bounds': {'percentage': [0, 255], 'armament': [0, 65535],
                                'ring_slots': 32, 'slot_capacity': 128},
              'limitations': ['Native CP932 glyph requests execute; ITCM number pixels remain a painter contract.',
                             'Dynamic faction/name bounds and physical routing remain pending.']}
    (root / 'native_numeric_proof.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print('768 native percentage cases, 20 numeric/ring boundaries and 40 mixed-glyph cases pass; CP932 pixels/name bounds pending.')


if __name__ == '__main__':
    main()
