"""Research ARM helper protecting display-only F/I; no ROM hook is installed."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP, machine_for
from scripts.probe_common_tribute_preprocessing import execute as preprocess

CODE, INPUT, OUTPUT = 0x02426000, 0x02427020, 0x02428020


def expected_display_name(name):
    # Preserve original CP932 byte spellings, including extension aliases.
    # Decode/re-encode would canonicalize some valid two-byte characters.
    name.decode('cp932')
    result = bytearray()
    index = 0
    while index < len(name):
        value = name[index]
        if 0x81 <= value <= 0x9F or 0xE0 <= value <= 0xFC:
            result.extend(name[index:index + 2])
            index += 2
        else:
            result.extend(b'\x82\x65' if value == 0x46 else b'\x82\x68' if value == 0x49 else bytes([value]))
            index += 1
    return bytes(result)


def helper_bytes():
    # ARM instructions are checked by execution below. r0=input, r1=37-byte
    # output; r0 returns output. r2/r3/ip scratch, all callee registers unchanged.
    words, labels, branches = [], {}, []

    def emit(word):
        words.append(word)

    def label(name):
        labels[name] = len(words)

    def branch(name, condition=14):
        branches.append((len(words), name, condition))
        emit(0)

    emit(0xE1A0C001)  # mov ip,r1
    label('loop')
    emit(0xE4D02001)  # ldrb r2,[r0],#1
    emit(0xE3520000)
    branch('finish', 0)
    emit(0xE3520081)
    branch('ascii', 3)
    emit(0xE352009F)
    branch('pair', 9)
    emit(0xE35200E0)
    branch('ascii', 3)
    emit(0xE35200FC)
    branch('pair', 9)
    label('ascii')
    emit(0xE3520046)
    branch('wide_f', 0)
    emit(0xE3520049)
    branch('wide_i', 0)
    emit(0xE4C12001)  # strb r2,[r1],#1
    branch('loop')
    label('pair')
    emit(0xE4C12001)
    emit(0xE4D02001)
    emit(0xE4C12001)
    branch('loop')
    label('wide_f')
    emit(0xE3A03065)  # CP932 full-width F = 82 65
    branch('wide')
    label('wide_i')
    emit(0xE3A03068)  # CP932 full-width I = 82 68
    label('wide')
    emit(0xE3A02082)
    emit(0xE4C12001)
    emit(0xE4C13001)
    branch('loop')
    label('finish')
    emit(0xE4C12001)  # terminating zero
    emit(0xE1A0000C)
    emit(0xE12FFF1E)
    for at, name, condition in branches:
        words[at] = (condition << 28) | 0x0A000000 | ((labels[name] - at - 2) & 0xFFFFFF)
    return struct.pack(f'<{len(words)}I', *words)


def escape(source, name):
    if not name or len(name) > 18 or b'\0' in name:
        raise ValueError('Requires a complete native eighteen-byte name')
    expected = expected_display_name(name)
    machine = machine_for(source)
    code = helper_bytes()
    machine.mem_write(CODE, code)
    machine.mem_write(INPUT - 32, b'\xa5' * 83)
    machine.mem_write(INPUT, name + b'\0')
    before = bytes(machine.mem_read(INPUT - 32, 83))
    machine.mem_write(OUTPUT - 32, b'\xa5' * 101)
    machine.reg_write(UC_ARM_REG_R0, INPUT)
    machine.reg_write(UC_ARM_REG_R1, OUTPUT)

    def write(uc, access, address, size, value, _):
        if not OUTPUT <= address < address + size <= OUTPUT + 37:
            raise ValueError('Display escape writes outside its bounded output')

    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(CODE, STOP, count=1000)
    actual = bytes(machine.mem_read(OUTPUT - 32, 101))
    if actual != b'\xa5' * 32 + expected + b'\0' + b'\xa5' * (68 - len(expected)):
        raise ValueError('Display escape loses glyphs/NUL or changes guards')
    if bytes(machine.mem_read(INPUT - 32, 83)) != before:
        raise ValueError('Display escape changes the original stored name')
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_R0) != OUTPUT
            or machine.reg_read(UC_ARM_REG_SP) != STACK):
        raise ValueError('Display escape changes return pointer/stack')
    return expected


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    text = next(row['english'].removesuffix('{PAD}') for row in manuscript['records'] if row['message_id'] == 83)
    names = [b'A', b'Fleet', b'Indigo', b'FI', b'IC', b'FO', b'FU', b'FA',
             b'ABCDEFGHIJKLMNOPQR', b'F' * 18, b'I' * 18, 'あ'.encode('cp932') * 9]
    # CP932 trail bytes 46/49 must stay intact, rather than being escaped as ASCII.
    for trail in (0x46, 0x49):
        for lead in range(0x81, 0xFD):
            raw = bytes((lead, trail))
            try:
                decoded = raw.decode('cp932')
            except UnicodeDecodeError:
                continue
            if len(decoded) == 1:
                names.append(raw * 9)
                break
    cases = []
    for name in names:
        safe = escape(source, name)
        # The output can grow to 36 bytes; the separate display buffer is not
        # subjected to the stored-name eighteen-byte validation in this call.
        result = preprocess(source, text, safe, display_name_capacity=36)
        if not result['name_preserved_after_macros']:
            raise ValueError('Protected display name still collides with macros')
        cases.append({'stored_name_hex': name.hex(), 'display_name_hex': safe.hex(),
                      'stored_name_unchanged': True, 'native_preprocessing': result})
    report = {'status': 'pass-research-helper-not-installed', 'arm9_sha256': sha(source),
              'helper_hex': helper_bytes().hex(), 'helper_sha256': sha(helper_bytes()),
              'cases': cases, 'limitations': 'New ARM helper executes in diagnostic RAM. No production code location, caller hook, ring lifetime or display geometry is approved. F/I display glyphs become full width, increasing layout width; stored names stay exact.'}
    Path('work/analysis/common_display_name_escape_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} ARM display-escape and actual COMMON preprocessing cases pass; no ROM hook installed.')


if __name__ == '__main__':
    main()
