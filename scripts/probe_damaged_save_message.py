"""Localize and execute complete native damaged-save message preparation."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.damaged_save_release import CAPACITY, ENGLISH, OFFSET, SOURCE, formatted_suffix
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.probe_map_tooltip_numeric_values import digits


def prepare(source):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V144 ARM9 required')
    raw = formatted_suffix().encode('ascii') + b'\0'
    if len(raw) > CAPACITY:
        raise ValueError('Complete damaged-save message exceeds owned copy')
    result = bytearray(source)
    result[OFFSET:OFFSET + CAPACITY] = raw.ljust(CAPACITY, b'\0')
    return bytes(result)


def execute(source, slot):
    # The actual caller loads an unsigned byte at EE090; exercise its entire
    # representable range without claiming every value is a valid save slot.
    if not 0 <= slot <= 255:
        raise ValueError('Native incoming slot exceeds unsigned byte')
    machine = machine_for(source)
    machine.mem_write(STACK - 0x200, b'\xA5' * 0x200)
    pool = struct.unpack_from('<I', source, 0xABFC0)[0]
    machine.mem_write(pool + 8, struct.pack('<I', 31))
    machine.mem_write(pool + 12, b'\xA5' * (32 * 128))
    machine.reg_write(UC_ARM_REG_R0, slot)
    machine.emu_start(BASE + 0xEE67C, BASE + 0xEE6BC, count=1000)
    frame = STACK - 36 - 0x74
    if machine.reg_read(UC_ARM_REG_SP) != frame:
        raise ValueError('Native damaged-save frame differs')
    if bytes(machine.mem_read(frame + 0x3C, CAPACITY)) != source[OFFSET:OFFSET + CAPACITY]:
        raise ValueError('Actual 26-pair source copy loses complete suffix')
    machine.emu_start(BASE + 0xEE75C, BASE + 0xEE780, count=10000)
    expected = digits(slot + 1) + formatted_suffix().encode('ascii') + b'\0'
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0xEE780
            or machine.reg_read(UC_ARM_REG_SP) != frame
            or machine.reg_read(UC_ARM_REG_R0) != frame
            or bytes(machine.mem_read(frame, 0x3C)) != expected + b'\xA5' * (0x3C - len(expected))
            or bytes(machine.mem_read(frame + 0x3C, CAPACITY)) != source[OFFSET:OFFSET + CAPACITY]):
        raise ValueError('Native number/copy/concatenation damages message, frame or suffix')
    resident = MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    buffers = struct.unpack_from('<2I', source, 0x54890)
    for buffer in buffers:
        machine.mem_write(buffer - 32, b'\xA5' * 320)
    machine.emu_start(BASE + 0xEE780, BASE + 0x5479C, count=100000)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5479C
            or machine.reg_read(UC_ARM_REG_SP) != frame - 24 - 200):
        raise ValueError('Damaged-save native modal formatting fails to reach construction')
    for buffer in buffers:
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xA5' * 32 + expected + b'\xA5' * (288 - len(expected)):
            raise ValueError('Native modal formatter/macros lose number, prose, guards or generated break')
    return {'incoming_slot_byte': slot, 'display_number': slot + 1,
            'complete_text': expected[:-1].decode('cp932'),
            'bytes_including_nul': len(expected), 'destination_capacity': 0x3C,
            'native_digits_copy_concat_and_guards_preserved': True,
            'actual_modal_formatter_and_macros_preserve_complete_text': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v144_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    spans = [(0xEE67C, 0xEE7E0), (0xEE090, 0xEE0A8),
             (0xD9AF4, 0xD9B28), (0xD9B88, 0xD9C70)]
    for lo, hi in spans:
        if source[lo:hi] != clean[lo:hi] or clean[lo:hi] != canonical[lo:hi]:
            raise ValueError('Native damaged-save consumer differs from original')
    if (source[OFFSET:OFFSET + CAPACITY] != clean[OFFSET:OFFSET + CAPACITY]
            or struct.unpack_from('<I', source, 0xEE7D0)[0] != BASE + OFFSET):
        raise ValueError('Damaged-save original allocation/consumer differs')
    research = prepare(source)
    cases = [execute(research, slot) for slot in range(256)]
    report = {'status': 'pass-research-native-damaged-save-preparation-rendering-pending',
              'source_sha256': sha(source), 'research_sha256': sha(research),
              'consumer_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])} for lo, hi in spans],
              'cases': cases, 'runtime_verified': False,
              'generated_suffix': formatted_suffix(),
              'limits': ['Native failed-checksum branch begins at EE75C; disk read/checksum and screen widgets are not executed.',
                         'All unsigned-byte inputs are tested, not claimed valid save slots.',
                         'Mixed CP932 number/ASCII modal painting, visual review and release integration remain separate gates.']}
    row = {'id': 'DAMAGED_SAVE_MESSAGE_SUFFIX', 'offset': OFFSET, 'capacity': CAPACITY,
           'source_hex': clean[OFFSET:OFFSET + CAPACITY].hex().upper(),
           'japanese': clean[OFFSET:OFFSET + CAPACITY].split(b'\0', 1)[0].decode('cp932'),
           'english': ENGLISH + '{PAD}', 'speaker': 'Load error dialog',
           'context': 'EE67C checksum mismatch branch converts incoming unsigned-byte slot plus one to full-width digits, copies that number, then concatenates this suffix into the 60-byte frame before modal 5473C.',
           'source_meaning': 'The save data in the numbered slot is corrupted; it could not be loaded.',
           'localization_note': 'A colon after the native slot number introduces a complete natural-English error sentence. Preserves corruption and failed loading without abbreviating. Native suffix copy, numeric conversion and concatenation are verified for every incoming byte; modal layout remains pending.',
           'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}}
    manuscript = {'format': 'dk4-arm9-prompt-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                  'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
                  'review_gates': list(row['review']), 'records': [row]}
    Path('translations/damaged_save_message_manuscript_v1.json').write_text(
        json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('work/analysis/damaged_save_message_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    Path('work/analysis/damaged_save_message_arm9.bin').write_bytes(research)
    print(f'Complete damaged-save preparation passes {len(cases)} native inputs; modal layout pending.')


if __name__ == '__main__':
    main()
