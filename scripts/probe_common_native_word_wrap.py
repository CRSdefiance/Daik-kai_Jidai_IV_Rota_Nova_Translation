"""Execute a bounded ARM word wrapper; native renderer verification follows."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP, machine_for
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded
from scripts.probe_common_tribute_modal_pixels import verify

CODE, INPUT, OUTPUT = 0x0242A000, 0x0242B020, 0x0242C020


def helper_bytes():
    words, labels, branches = [], {}, []

    def emit(word):
        words.append(word)

    def label(name):
        labels[name] = len(words)

    def branch(name, condition=14):
        branches.append((len(words), name, condition))
        emit(0)

    def mov(rd, rm):
        emit(0xE1A00000 | rd << 12 | rm)

    def imm(op, rd, rn, value, condition=14):
        emit(condition << 28 | op | rn << 16 | rd << 12 | value)

    def reg(op, rd, rn, rm):
        emit(0xE0000000 | op | rn << 16 | rd << 12 | rm)

    emit(0xE92D4FF0)  # push r4-r11,lr; leaf makes no nested calls
    mov(4, 0)
    mov(5, 1)
    mov(8, 1)
    imm(0x03A00000, 6, 0, 0)
    imm(0x03A00000, 7, 0, 39)
    imm(0x03A00000, 3, 0, 1)
    label('next')
    imm(0x03A00000, 9, 0, 0)
    label('spaces')
    emit(0xE5D40000)
    imm(0x03500000, 0, 0, 32)
    branch('word', 1)
    imm(0x02800000, 4, 4, 1)
    imm(0x02800000, 9, 9, 1)
    branch('spaces')
    label('word')
    mov(10, 4)
    imm(0x03A00000, 11, 0, 0)
    label('scan')
    emit(0xE7DA000B)  # ldrb r0,[r10,r11]
    imm(0x03500000, 0, 0, 0)
    branch('ready', 0)
    imm(0x03500000, 0, 0, 32)
    branch('ready', 0)
    imm(0x02800000, 11, 11, 1)
    branch('scan')
    label('ready')
    imm(0x03500000, 0, 11, 0)
    branch('finish', 0)
    imm(0x03500000, 0, 11, 38)
    branch('fail', 8)
    reg(0x00400000, 2, 5, 8)
    reg(0x00800000, 2, 2, 9)
    reg(0x00800000, 2, 2, 11)
    imm(0x03500000, 0, 2, 236)
    branch('fail', 8)
    reg(0x00800000, 2, 6, 9)
    reg(0x00800000, 2, 2, 11)
    reg(0x01500000, 0, 2, 7)
    branch('copy_spaces', 9)
    imm(0x03A00000, 0, 0, 10)
    emit(0xE4C50001)
    imm(0x03A00000, 0, 0, 32)
    emit(0xE4C50001)
    emit(0xE4C50001)
    imm(0x03500000, 0, 9, 0)
    imm(0x02400000, 9, 9, 1, 1)
    imm(0x03A00000, 6, 0, 0)
    imm(0x03A00000, 7, 0, 38)
    imm(0x02800000, 3, 3, 1)
    imm(0x03500000, 0, 3, 4)
    branch('fail', 8)
    reg(0x00800000, 2, 9, 11)
    imm(0x03500000, 0, 2, 38)
    branch('fail', 8)
    label('copy_spaces')
    imm(0x03500000, 0, 9, 0)
    branch('copy_word', 0)
    imm(0x03A00000, 0, 0, 32)
    label('space_copy')
    emit(0xE4C50001)
    imm(0x02800000, 6, 6, 1)
    imm(0x02500000, 9, 9, 1)
    branch('space_copy', 1)
    label('copy_word')
    mov(4, 10)
    label('word_copy')
    emit(0xE4D40001)
    emit(0xE4C50001)
    imm(0x02800000, 6, 6, 1)
    imm(0x02500000, 11, 11, 1)
    branch('word_copy', 1)
    branch('next')
    label('finish')
    imm(0x03A00000, 0, 0, 0)
    emit(0xE5C50000)
    reg(0x00400000, 0, 5, 8)
    branch('return')
    label('fail')
    imm(0x03A00000, 0, 0, 0)
    label('return')
    emit(0xE8BD8FF0)
    for at, name, condition in branches:
        words[at] = condition << 28 | 0x0A000000 | ((labels[name] - at - 2) & 0xFFFFFF)
    return struct.pack(f'<{len(words)}I', *words)


def execute(source, text):
    expected = wrap_expanded(text).encode('cp932')
    raw = text.encode('cp932')
    if len(raw) > 224:
        raise ValueError('Expanded notice exceeds bounded input')
    machine = machine_for(source)
    machine.mem_write(CODE, helper_bytes())
    machine.mem_write(INPUT - 32, b'\xa5' * (len(raw) + 65))
    machine.mem_write(INPUT, raw + b'\0')
    original = bytes(machine.mem_read(INPUT - 32, len(raw) + 65))
    machine.mem_write(OUTPUT - 32, b'\xa5' * 304)
    machine.reg_write(UC_ARM_REG_R0, INPUT)
    machine.reg_write(UC_ARM_REG_R1, OUTPUT)
    preserved = {UC_ARM_REG_R4 + index: 0x12340000 + index for index in range(8)}
    for register, value in preserved.items():
        machine.reg_write(register, value)

    def write(uc, access, address, size, value, _):
        if not ((OUTPUT <= address and address + size <= OUTPUT + 240)
                or (STACK - 0x1000 <= address and address + size <= STACK)):
            raise ValueError('ARM wrapper writes outside buffer/stack bounds')

    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(CODE, STOP, count=20000)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or machine.reg_read(UC_ARM_REG_R0) != len(expected)
            or any(machine.reg_read(register) != value for register, value in preserved.items())):
        raise ValueError('ARM wrapper return length, stack or live registers differ')
    if bytes(machine.mem_read(OUTPUT - 32, 304)) != b'\xa5' * 32 + expected + b'\0' + b'\xa5' * (271 - len(expected)):
        raise ValueError('ARM wrapper differs from word reference or corrupts guards')
    if bytes(machine.mem_read(INPUT - 32, len(raw) + 65)) != original:
        raise ValueError('ARM wrapper changes complete input paragraph')
    return expected.decode('cp932')


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    previous = json.loads(Path('work/analysis/common_tribute_loaded_copy_proof.json').read_text(encoding='utf-8'))
    texts = list(dict.fromkeys(case['complete_prepared_text'] for case in previous['cases']))
    texts += ["Towns under Ｆleet  Group's exclusive contracts paid ８８４６２９ gold coins in tribute."]
    cases = []
    for text in texts:
        generated = execute(source, text)
        if generated.replace('\n  ', ' ') != text:
            raise ValueError('Runtime wrapper loses prose or repeated name spaces')
        for mode in (4, 16):
            native = verify(source, font, generated, mode, guarded=True)
            events = [event for event in native['glyph_events'] if event['code'] != 32]
            cursor = 0
            for word in text.split():
                if len({event['y'] for event in events[cursor:cursor + len(word)]}) != 1:
                    raise ValueError('Native ARM-wrapped output splits a word or money amount')
                cursor += len(word)
            cases.append({'original': text, 'generated': generated, 'mode': mode,
                          'pixels_sha256': sha(native['pixels']), 'native_arm_wrapper_and_renderer_pass': True})
    report = {'status': 'pass-arm-word-wrapper-native-modal-pixels-not-installed',
              'helper_hex': helper_bytes().hex(), 'helper_sha256': sha(helper_bytes()),
              'helper_bytes': len(helper_bytes()), 'cases': cases,
              'limitations': 'ARM leaf executes in diagnostic RAM then unchanged modal renderer executes separately. Production macro-pass hook, startup placement, full loader integration and monthly portrait windows remain pending.'}
    Path('work/analysis/common_native_word_wrap_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} ARM wrapper/native pixel cases pass; helper is {len(helper_bytes())} bytes, not installed.')


if __name__ == '__main__':
    main()
