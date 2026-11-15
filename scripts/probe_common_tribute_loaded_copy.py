"""Run hooked tribute, warm COMMON cache lookup, real formatter and macros."""

import json
import struct
from pathlib import Path

import ndspy.code
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R9,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.execute_map_entity_tooltip_copy import BASE, machine_for
from scripts.probe_common_display_name_escape import INPUT, expected_display_name
from scripts.probe_common_display_name_hook import HOOK, prepare
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded


def execute(source, common, name, index, *, word_wrapped=False, cold_cache=False):
    expected_name = expected_display_name(name)
    loaded = ndspy.code.MainCodeFile(source, BASE)
    machine = machine_for(source)
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(loaded.sections[1].ramAddress, bytes(loaded.sections[1].data))
    owner = struct.unpack_from('<I', source, 0x552A0)[0]
    root = struct.unpack_from('<I', source, 0xABFC0)[0]
    entry = common_message_entries(common, source, clean=False)[83]
    block = IlnkContainer.parse(common).blocks[entry.block]
    if entry.block != 0 or len(block) > 4096 or not 0 <= index < 32:
        raise ValueError('Unexpected tribute cache block or ring index')
    machine.mem_write(owner + 0x2C, bytes((255 if cold_cache else 0, 255, 0, 1)))
    if cold_cache:
        # Actual source ILNK class methods return an uncached offset table.
        machine.mem_write(owner, source[0xD20B4:0xD20B8])
    else:
        machine.mem_write(owner + 0x30, block)
    machine.mem_write(root + 8, struct.pack('<I', index))
    machine.mem_write(INPUT, name + b'\0')
    for register, value in ((UC_ARM_REG_R0, INPUT), (UC_ARM_REG_R4, 0x12345678),
                            (UC_ARM_REG_R5, 884629), (UC_ARM_REG_R9, 83)):
        machine.reg_write(register, value)
    executed, allocations, file_reads, file_opens = set(), [], [], []

    def code(uc, address, size, _):
        executed.add(address)
        if address == BASE + 0xAC000:
            allocations.append(struct.unpack('<I', uc.mem_read(root + 8, 4))[0])
        if cold_cache and address == BASE + 0xD0398:
            if uc.reg_read(UC_ARM_REG_R0) != owner or uc.reg_read(UC_ARM_REG_R2) != 0:
                raise ValueError('Host open contract receives wrong native owner/mode')
            pointer = uc.reg_read(UC_ARM_REG_R1)
            path = bytes(uc.mem_read(pointer, 64)).split(b'\0', 1)[0]
            if b'MESFILE.DK4' not in path.upper():
                raise ValueError('Native cache miss opens an unrelated file')
            file_opens.append(path.decode('ascii'))
            uc.mem_write(owner + 8, struct.pack('<I', 1))
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif cold_cache and address == BASE + 0xD0170:
            actor, offset, destination, count = (uc.reg_read(register) for register in
                                                (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3))
            if actor != owner or offset + count > len(common):
                raise ValueError('Native ILNK read escapes exact source file')
            uc.mem_write(destination, common[offset:offset + count])
            file_reads.append({'offset': offset, 'count': count, 'destination': destination})
            uc.reg_write(UC_ARM_REG_R0, count)
            for register in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
                uc.reg_write(register, 0xBAD00000 + register)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif not cold_cache and address in (BASE + 0xD2018, BASE + 0xD1EF0):
            raise ValueError('Warm-cache proof unexpectedly enters filesystem loading')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.emu_start(BASE + HOOK, BASE + 0x5479C, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5479C:
        raise ValueError('Full preparation path did not reach native widget continuation')
    expected = entry.text.replace(b'%s', expected_name, 1).replace(b'%s', '８８４６２９'.encode('cp932'), 1) + b'\0'
    buffers = struct.unpack_from('<2I', source, 0x54890)
    generated = wrap_expanded(expected[:-1].decode('cp932')).encode('cp932') + b'\0' if word_wrapped else expected
    for pointer, value in zip(buffers, (expected, generated), strict=True):
        if bytes(machine.mem_read(pointer, len(value))) != value:
            raise ValueError('Actual loader/formatter/macros lose complete corrected notice')
    selected = owner + 0x2030
    if bytes(machine.mem_read(selected, len(entry.text) + 1)) != entry.text + b'\0':
        raise ValueError('Actual cache loader drops first/final source characters')
    if allocations != [index, (index + 1) % 32]:
        raise ValueError('Loader/display preparation changes escaped-name ring lifetime')
    required = {BASE + offset for offset in (0x546B8, 0x5528C, 0x534F4, 0x53628,
                                             0x535E0, 0xCEC74, 0xCE898, 0x53914)}
    if not required <= executed:
        raise ValueError('Complete native loader and preparation bodies did not execute')
    if word_wrapped and 0x01FF9BC8 not in executed:
        raise ValueError('Scoped ARM word helper did not execute')
    if cold_cache and (len(file_opens) != 1 or len(file_reads) != 3
                       or not {BASE + 0xD2018, BASE + 0xD1EF0, BASE + 0xD1F50,
                               BASE + 0xD1EE0} <= executed):
        raise ValueError('Actual ILNK cold-cache directory/block path did not execute')
    return {'name_hex': name.hex(), 'ring_index': index, 'ring_allocations': allocations,
            'cold_cache': cold_cache, 'host_file_contract_opens': file_opens,
            'host_file_contract_reads': file_reads,
            'complete_prepared_text': generated[:-1].decode('cp932'),
            'native_cache_lookup_formatting_macros': True}


def research_dataset(arm9=None):
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    common = rom.read_file('/COMMON/MESFILE.DK4')
    if arm9 is None:
        arm9, _ = prepare(rom.read_file('/__arm9__.bin'))
    clean = NdsImage.open('work/clean.nds')
    clean_common = clean.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(clean_common, clean.read_file('/__arm9__.bin'))
    blocks = IlnkContainer.parse(clean_common).blocks
    rows = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))['records']
    encoded, prefixes = {}, {}
    for row in rows:
        entry = entries[row['message_id']]
        if entry.text != bytes.fromhex(row['source_hex']):
            raise ValueError('Research manuscript differs from clean Japanese source')
        encoded[entry.message_id] = row['english'].removesuffix('{PAD}').encode('cp932')
        owner = entry.block, entry.record_index
        first = next(item for item in entries if (item.block, item.record_index) == owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    repacked = repack_native_records(common, arm9, encoded, prefixes)
    return repacked


def main():
    repacked = research_dataset()
    cases = [execute(repacked.arm9, repacked.common, name, index)
             for index in (0, 1, 30, 31)
             for name in (b'Fleet', b'Indigo', b'F' * 18, b'I' * 18, 'あ'.encode('cp932') * 9)]
    report = {'status': 'pass-research-corrected-tribute-native-warm-cache-preparation',
              'research_arm9_sha256': sha(repacked.arm9), 'research_common_sha256': sha(repacked.common),
              'cases': cases, 'limitations': 'Corrected prose repacked in memory; no playable ROM/profile built. Actual hook, warm native cache lookup, copy, varargs formatter and macros execute in one machine. Cold-cache filesystem I/O, widgets, progressive wrapping and physical composition remain unproven.'}
    Path('work/analysis/common_tribute_loaded_copy_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} actual hooked loader/formatter/macro cases preserve corrected tribute text and ring lifetime.')


if __name__ == '__main__':
    main()
