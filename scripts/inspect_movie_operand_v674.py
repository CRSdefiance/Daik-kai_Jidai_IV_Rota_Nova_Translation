"""Original packed movie-opcode arguments; byte hits are not decoded triggers."""

import struct
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.probe_button_prompt_native import STACK, machine
from scripts.verify_village_wrap_v608 import read, save

OWNER, STREAM, RESULT, LENGTH = 0x02460000, 0x02461000, 0x02462000, 0x02462020


def decode(arm):
    u, rows = machine(arm), []
    u.mem_write(OWNER, bytes(32))
    u.mem_write(OWNER + 4, struct.pack('<I', STREAM))
    for low in range(256):
        word = 0x4200 | low
        u.mem_write(STREAM - 16, b'\xA5' * 36)
        u.mem_write(STREAM, struct.pack('<H', word))
        u.mem_write(LENGTH, bytes(4))
        for reg, value in ((UC_ARM_REG_R0, RESULT), (UC_ARM_REG_R1, OWNER),
                           (UC_ARM_REG_R2, LENGTH), (UC_ARM_REG_SP, STACK)):
            u.reg_write(reg, value)
        u.emu_start(0x0202A510, 0x02029D34, count=128)
        assert u.reg_read(UC_ARM_REG_PC) == 0x02029D34
        assert u.reg_read(UC_ARM_REG_SP) == STACK - 120
        assert bytes(u.mem_read(LENGTH, 4)) == struct.pack('<I', 2)
        # Skip neither a decoder result nor a movie result: execute just the
        # original argument fragment, excluding preceding sound/UI side effects.
        u.emu_start(0x02029D54, 0x02029D74, count=16)
        args = [u.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        assert args == [(low & 127) + 1, low >> 7, 1, 0]
        assert bytes(u.mem_read(STREAM, 2)) == struct.pack('<H', word)
        assert bytes(u.mem_read(STREAM - 16, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(STREAM + 2, 18)) == b'\xA5' * 18
        rows.append({'packed_word': word, 'original_FLS_request_arguments': args})
    return rows


def scan(image):
    rows = []
    for _, path, blob in image.iter_files():
        if not path.startswith(('/data/', '/testdata/', '/COMMON/')):
            continue
        if blob.startswith(b'ILNK'):
            blocks = IlnkContainer.parse(blob).blocks
        elif blob.startswith(b'VE'):
            blocks = [blob]
        else:
            continue
        hits = []
        for block, data in enumerate(blocks):
            for at in range(len(data) - 1):
                word = struct.unpack_from('<H', data, at)[0]
                if word in (0x4219, 0x4299):
                    hits.append({'block': block, 'offset': at, 'word': word,
                        'aligned': at % 2 == 0, 'context_hex': data[max(0, at - 12):at + 16].hex(),
                        'not_an_instruction_boundary_or_reachability_claim': True})
        rows.append({'path': path, 'sha256': sha(blob), 'blocks': len(blocks),
            'M26_byte_candidates': hits})
    return rows


def main():
    pre = read(ROOT / 'preflight.json')
    current, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm, original = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert arm[0x29AA0:0x29DBC] == original[0x29AA0:0x29DBC]
    assert arm[0x2A510:0x2A5BC] == original[0x2A510:0x2A5BC]
    a, b = decode(arm), decode(original)
    assert a == b and len(a) == 256
    save(ROOT / 'movie_operand_proof.json', {'candidate_sha256': pre['candidate_sha256'],
        'all256_clean_and_current_argument_cases_exact': True, 'cases': a,
        'M26_packed_words': [0x4219, 0x4299], 'decoder_fragments_not_full_native_call_ABI_or_runtime_trigger': True,
        'scans': {'current': scan(current), 'clean': scan(clean)},
        'byte_candidates_not_decoded_events_and_absence_not_global_nonuse': True,
        'original_M26_story_consumer_still_open': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V674 original packed movie arguments:512 clean/current fragment cases exact; M26 trigger still unresolved.')


if __name__ == '__main__':
    main()
