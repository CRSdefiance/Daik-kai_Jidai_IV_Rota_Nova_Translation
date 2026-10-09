"""Execute the real menu label copier; final graphics dispatch remains pending."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)

START, END = 0xACC64, 0xACC9C
NAMES = ('START', 'READ_RULES', 'ABOUT', 'BASIC_RULES', 'MAP_SUPPLIES', 'LIMITS')


def execute_copy(arm9, raw):
    """Bounded interpretation of the native byte copier, including signed loads."""
    if not raw.endswith(b'\0') or b'\0' in raw[:-1]:
        raise ValueError('Input must be one complete terminated string')
    registers = [0] * 16
    registers[0], registers[1] = 0x100, 0x1000
    memory = {0x1000 + index: byte for index, byte in enumerate(raw)}
    position, zero, greater_equal, steps = START, False, False, 0
    while True:
        steps += 1
        if steps > 500 or not START <= position < END:
            raise ValueError('Native copy escaped bounded code')
        instruction = struct.unpack_from('<I', arm9, position)[0]
        next_position = position + 4
        if instruction == 0xE2803068:
            registers[3] = registers[0] + 0x68
        elif instruction == 0xE3A02000:
            registers[2] = 0
        elif instruction in (0xEA000002, 0xAA000002, 0x1AFFFFF7):
            take = instruction >> 28 == 14 or (instruction >> 28 == 10 and greater_equal) or (instruction >> 28 == 1 and not zero)
            if take:
                displacement = instruction & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 1 << 24
                next_position = position + 8 + displacement * 4
        elif instruction in (0xE0D100D1, 0xE1D100D0):
            byte = memory[registers[1]]
            registers[0] = byte if byte < 128 else byte - 256
            if instruction == 0xE0D100D1:
                registers[1] += 1
        elif instruction == 0xE2822001:
            registers[2] += 1
        elif instruction in (0xE4C30001, 0xE5C30000):
            memory[registers[3]] = registers[0] & 255
            if instruction == 0xE4C30001:
                registers[3] += 1
        elif instruction == 0xE3520030:
            greater_equal = registers[2] >= 48
        elif instruction == 0xE3500000:
            zero = registers[0] == 0
        elif instruction == 0xE3A00000:
            registers[0] = 0
        elif instruction == 0xE12FFF1E:
            return bytes(memory[address] for address in range(0x168, registers[3] + 1))
        else:
            raise ValueError(f'Unknown copier opcode {instruction:08x}')
        position = next_position


def main():
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned input ROM differs')
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    if hashlib.sha256(sources[0]).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese source differs')
    spans = ((START, END), (0x52FD0, 0x53024), (0xADFDC, 0xAE0F0), (0xD4914, 0xD4988))
    locks = []
    for lo, hi in spans:
        if not sources[0][lo:hi] == sources[1][lo:hi] == sources[2][lo:hi]:
            raise ValueError('Source copier/draw code differs')
        locks.append({'start': lo, 'end': hi, 'sha256': hashlib.sha256(sources[0][lo:hi]).hexdigest()})
    path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {row['id'].removeprefix('GRAND_RACE_UI_'): row for row in json.loads(path.read_text(encoding='utf-8'))['records']}
    selections = []
    for name in NAMES:
        raw = rows[name]['english'].encode('ascii') + b'\0'
        if len(raw) > 49 or execute_copy(sources[2], raw) != raw:
            raise ValueError('Native menu copy truncates or drops a character')
        selections.append({'id': rows[name]['id'], 'english': rows[name]['english'], 'copied_hex': raw.hex()})
    # Exercise exact boundary and overlong input to prove the truncation ceiling.
    if execute_copy(sources[2], b'A' * 48 + b'\0') != b'A' * 48 + b'\0' or execute_copy(sources[2], b'A' * 49 + b'\0') != b'A' * 48 + b'\0':
        raise ValueError('Native capacity behavior differs')
    report = {'status': 'research-native-menu-copy-proven-final-renderer-pending', 'rom_written': False,
              'source_locks': locks, 'manuscript_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'selections': selections, 'copy_limit': 48,
              'draw_path': ['0x52FD0', '0xADFDC', '0xD4914', 'supplied graphics-context vtable[0]'],
              'limitations': ['Final supplied graphics-context implementation and geometry remain pending.',
                              'Font preview and runtime are not established by byte-copy execution.']}
    directory = Path('work/analysis/grand_race_menu_copy')
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Six complete native menu copies and 48/49-byte boundaries verified; final renderer pending; no ROM written')


if __name__ == '__main__':
    main()
