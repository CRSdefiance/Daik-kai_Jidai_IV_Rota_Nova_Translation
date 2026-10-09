"""Research loaded ITCM extension and tribute hook; no playable ROM is written."""

import json
import struct
from pathlib import Path

import ndspy.code
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R9,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.probe_common_display_name_escape import INPUT, expected_display_name, helper_bytes

HELPER, HOOK, OVERLAY = 0x01FF9B20, 0xB2590, 0x01FFA000
ARENA_LO_LITERAL = 0xE45E4


def branch_link(at, target):
    delta = target - at - 8
    if delta % 4 or not -(1 << 25) <= delta < (1 << 25):
        raise ValueError('ARM branch target outside aligned signed range')
    return 0xEB000000 | ((delta >> 2) & 0xFFFFFF)


def prepare(source):
    if sha(source) != '863776d944118cc12418a91ed32e24cac1755aeac70ace682fdfa0897818b7eb':
        raise ValueError('Exact V142 source required for research hook')
    code = ndspy.code.MainCodeFile(source, BASE)
    if struct.unpack_from('<I', code.sections[0].data, ARENA_LO_LITERAL)[0] != HELPER:
        raise ValueError('Native ITCM arena lower boundary differs')
    resident = code.sections[1]
    if resident.ramAddress != 0x01FF8000 or len(resident.data) != 0x1B20 or resident.bssSize:
        raise ValueError('Resident ITCM load extent differs')
    if struct.unpack_from('<I', code.sections[0].data, HOOK)[0] != 0xE1A0A000:
        raise ValueError('Tribute name assignment differs')
    helper = helper_bytes()
    wrapper = HELPER + len(helper)
    root = struct.unpack_from('<I', source, 0xABFC0)[0]
    words = [0xE92D4010, 0xE1A04000, 0xE59F0014,
             branch_link(wrapper + 12, BASE + 0xAC000),
             0xE1A01000, 0xE1A00004, branch_link(wrapper + 24, HELPER),
             0xE1A0A000, 0xE8BD8010, root]
    payload = helper + struct.pack('<10I', *words)
    if HELPER + len(payload) > OVERLAY:
        raise ValueError('Extended resident section overlaps overlay load address')
    before = [bytes(section.data) for section in code.sections]
    resident.data.extend(payload)
    arena_low = (resident.ramAddress + len(resident.data) + 31) & ~31
    struct.pack_into('<I', code.sections[0].data, ARENA_LO_LITERAL, arena_low)
    struct.pack_into('<I', code.sections[0].data, HOOK, branch_link(BASE + HOOK, wrapper))
    saved = bytes(code.save())
    loaded = ndspy.code.MainCodeFile(saved, BASE)
    if (len(loaded.sections) != len(code.sections)
            or bytes(loaded.sections[1].data) != before[1] + payload
            or bytes(loaded.sections[2].data) != before[2]):
        raise ValueError('ARM9 serialization changes existing resident/DTCM content')
    expected_static = bytearray(before[0])
    struct.pack_into('<I', expected_static, ARENA_LO_LITERAL, arena_low)
    struct.pack_into('<I', expected_static, HOOK, branch_link(BASE + HOOK, wrapper))
    settings = code.codeSettingsOffs
    # Only the autoload table start/end move when resident payload grows.
    for offset in (settings, settings + 4):
        struct.pack_into('<I', expected_static, offset,
                         struct.unpack_from('<I', before[0], offset)[0] + len(payload))
    if bytes(loaded.sections[0].data) != expected_static:
        raise ValueError('Unexpected static code or code-settings change')
    return saved, payload


def execute(saved, name, index):
    if not name or len(name) > 18 or b'\0' in name or not 0 <= index < 32:
        raise ValueError('Bounded name and ring index required')
    expected = expected_display_name(name)
    loaded = ndspy.code.MainCodeFile(saved, BASE)
    machine = machine_for(saved)
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(loaded.sections[1].ramAddress, bytes(loaded.sections[1].data))
    root = struct.unpack_from('<I', saved, 0xABFC0)[0]
    machine.mem_write(root + 8, struct.pack('<I', index))
    machine.mem_write(INPUT, name + b'\0')
    for register, value in ((UC_ARM_REG_R0, INPUT), (UC_ARM_REG_R5, 884629),
                            (UC_ARM_REG_R9, 83), (UC_ARM_REG_R4, 0x12345678)):
        machine.reg_write(register, value)
    machine.emu_start(BASE + HOOK, BASE + 0xB25A8, count=10000)
    name_pointer = machine.reg_read(UC_ARM_REG_R1)
    digits_pointer = machine.reg_read(UC_ARM_REG_R2)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0xB25A8
            or machine.reg_read(UC_ARM_REG_R0) != 83
            or machine.reg_read(UC_ARM_REG_R5) != 884629
            or machine.reg_read(UC_ARM_REG_R4) != 0x12345678
            or machine.reg_read(UC_ARM_REG_SP) != STACK):
        raise ValueError('Hook changes message ID, live money/registers or caller stack')
    if bytes(machine.mem_read(name_pointer, len(expected) + 1)) != expected + b'\0':
        raise ValueError('Actual hook loses protected display name')
    digits = '８８４６２９'.encode('cp932') + b'\0'
    if bytes(machine.mem_read(digits_pointer, len(digits))) != digits:
        raise ValueError('Actual caller loses complete amount')
    if bytes(machine.mem_read(INPUT, len(name) + 1)) != name + b'\0':
        raise ValueError('Hook changes stored name')
    return {'index': index, 'name_hex': name.hex(), 'display_hex': expected.hex(),
            'native_arguments': [83, name_pointer, digits_pointer], 'live_registers_preserved': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, payload = prepare(source)
    cases = [execute(saved, name, index) for index in range(32)
             for name in (b'Fleet', b'Indigo', b'F' * 18, b'I' * 18, 'あ'.encode('cp932') * 9)]
    report = {'status': 'pass-serialized-arm9-research-hook-not-playable-release',
              'source_arm9_sha256': sha(source), 'research_arm9_sha256': sha(saved),
              'helper_address': HELPER, 'payload_bytes': len(payload),
              'overlay_start': OVERLAY, 'resident_content_preserved': True,
              'dtcm_content_preserved': True, 'cases': cases,
              'limitations': 'Saved/reparsed ARM9 sections and actual hooked argument preparation execute. Static reference audit, boot loader/overlay loading, intervening message-loader lifetime and progressive window execution remain pending. No ROM/profile is changed.'}
    Path('work/analysis/common_display_name_hook_arm9.bin').write_bytes(saved)
    Path('work/analysis/common_display_name_hook_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} serialized ARM9 hook cases pass; {len(payload)} bytes extend resident ITCM without overlay overlap.')


if __name__ == '__main__':
    main()
