"""Record the native name-editor byte-boundary hazard without altering a ROM."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.name_editor_atomic_append import apply
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_append import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Candidate source differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x9DE24, 0x9DE80), (0xAEB98, 0xAEC04),
             (0xAFBB0, 0xAFC88), (0xAFD4C, 0xAFDB8),
             (0xAFE58, 0xAFE80), (0xB07FC, 0xB0808),
             (0xB08C8, 0xB0A18), (0xB0F38, 0xB0FCC), (0xCED28, 0xCED50))
    if any(source[lo:hi] != clean[lo:hi] for lo, hi in spans):
        raise ValueError('Native name-editor evidence differs from clean source')
    if struct.unpack_from('<I', source, 0xB08D4)[0] != 0x020CED28:
        raise ValueError('Native byte strlen target differs')
    cases = [execute(source, b'A' * size, inserted, capacity)
             for capacity in (32, 16) for size in (14, 15, 16)
             for inserted in (b'B', 'ア'.encode('cp932'))]
    hazard = execute(source, b'A' * 15, 'ア'.encode('cp932'), 16)
    if hazard['terminated_at'] != 16 or bytes.fromhex(hazard['result_hex'])[-1:] != b'\x83':
        raise ValueError('Expected source-derived insertion boundary changed')
    patched = apply(source)
    repaired_cases = []
    for size in range(17):
        for inserted in (b'B', 'ア'.encode('cp932')):
            case = execute(patched, b'A' * size, inserted, 16, full_return=True)
            expected = b'A' * size + inserted if size + len(inserted) <= 16 else b'A' * size
            if bytes.fromhex(case['result_hex']) != expected:
                raise ValueError('Whole-insertion repair changed complete text')
            repaired_cases.append(case)
    report = {
        'status': 'confirmed-split-character-and-in-memory-atomic-repair',
        'candidate_sha256': CANDIDATE_SHA, 'rom_written': False, 'runtime_verified': False,
        'source_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])}
                         for lo, hi in spans],
        'caller_limit': 16, 'insertion_capacity': 16, 'constructor_default_capacity': 32,
        'capacity_source': 'Editor +D8 equals subobject +38 +A0. AFE60 overwrites constructor capacity with caller limit 16.',
        'length_guard': 'AFD68 reads byte strlen via B08C8; AFD70 rejects only existing lengths >=16.',
        'cases': cases, 'hazard': hazard, 'repaired_cases': repaired_cases,
        'repair_scope': 'Forty in-place instruction bytes at B091C:B0944; no ROM/batch/profile written.',
        'limitations': [
            'End-insertion with initialized cursor and byte string only; keyboard table conversion not executed.',
            'Earlier seventeen-byte name hazard diagnosis was incorrect: parent and subobject fields alias.',
            'Actual name capacity 16 splits a two-byte insert after a 15-byte name, while retaining a terminator.',
            'In-memory repair preflights full byte strlen and rejects an insertion that cannot fit intact.',
            'Native strlen body and insertion function frame/return executed; callee registers and stack preserved.',
            'External cursor/drawing helpers modeled with strict object arguments and caller-register poisoning.',
            'Middle insertion, saves, packet consumers and gameplay remain pending; no integration credit.'
        ]}
    Path('work/analysis/grand_race_name_append_v136_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Actual 16-byte name capacity splits CP932; 34 atomic repair boundary cases pass in memory.')


if __name__ == '__main__':
    main()
