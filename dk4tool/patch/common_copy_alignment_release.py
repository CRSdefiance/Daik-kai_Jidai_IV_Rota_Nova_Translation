"""Guard shared native copies against ARM946 unaligned load/store behavior."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = '75fac17b97382fb4428ce0823ae5a8ca2b698537fcc8e0f00e213247c4adcd57'
BASE, ENTRY, GUARD, BYTE_LOOP = 0x02000000, 0xCEC74, 0xCECA0, 0xCECCC
ORIGINAL_GUARD = (0xE2123001, 0x1A000008, 0xE1B020A2, 0xE2422001,
                  0x012FFF1E, 0xE0D130B2, 0xE3520000, 0xE2422001,
                  0xE0C030B2, 0x1AFFFFFA, 0xE12FFF1E)


def branch(at, target, condition=14):
    delta = target - at - 8
    if delta % 4 or not -(1 << 25) <= delta < 1 << 25:
        raise ValueError('Alignment guard branch is outside ARM bounds')
    return condition << 28 | 0x0A000000 | ((delta // 4) & 0xFFFFFF)


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Alignment repair requires the exact complete V151 ARM9')
    if struct.unpack_from('<I', source, ENTRY)[0] != 0xE2123003:
        raise ValueError('Native copy entry differs')
    if struct.unpack_from('<11I', source, GUARD) != ORIGINAL_GUARD:
        raise ValueError('Native halfword dispatch/body differs')
    # The obsolete halfword path provides an owned inline guard. Only aligned
    # pointers AND a whole-word count reach the unchanged word path. Every other
    # case uses the unchanged byte loop, including zero and single-byte counts.
    words = (0xE1803001, 0xE1833002, 0xE3130003,
             branch(BASE + GUARD + 12, BASE + ENTRY + 8, condition=0),
             branch(BASE + GUARD + 16, BASE + BYTE_LOOP),
             *([0xE1A00000] * 6))
    result = bytearray(source)
    struct.pack_into('<I', result, ENTRY, branch(BASE + ENTRY, BASE + GUARD))
    struct.pack_into('<11I', result, GUARD, *words)
    restored = bytearray(result)
    restored[ENTRY:ENTRY + 4] = source[ENTRY:ENTRY + 4]
    restored[GUARD:BYTE_LOOP] = source[GUARD:BYTE_LOOP]
    if restored != source:
        raise ValueError('Alignment repair changes unrelated bytes')
    return bytes(result)


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if (config.get('format') != 'dk4-common-copy-alignment-release-v1'
            or config['source_arm9_sha256'] != SOURCE):
        raise ValueError('Shared copy alignment configuration differs')
    saved = transform(source)
    if sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Shared copy alignment target differs')
    proof_path = Path(config['native_proof'])
    if sha(proof_path.read_bytes()) != config['native_proof_sha256']:
        raise ValueError('Alignment proof changed')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    if (proof['source_arm9_sha256'] != SOURCE or proof['repair_arm9_sha256'] != sha(saved)
            or proof['all_common_messages_preserved_warm_and_cold'] != list(range(3668))
            or proof['copy_alignment_matrix_cases'] != 704):
        raise ValueError('Alignment proof does not cover complete COMMON and copy alignment')
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'patched_entry': BASE + ENTRY, 'guard_span': [BASE + GUARD, BASE + BYTE_LOOP],
                   'word_copy_requires_aligned_source_destination_and_count': True,
                   'other_inputs_use_original_byte_loop': True, 'runtime_verified': False}
