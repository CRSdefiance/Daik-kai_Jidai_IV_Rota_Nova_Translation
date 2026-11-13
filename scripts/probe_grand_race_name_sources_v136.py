"""Verify source character names and the mapped native initialization chain."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_copy import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def inspect_names(source):
    expected = ('Raphael', 'Hodram', 'Lil', 'Maria')
    rows = []
    for index, name in enumerate(expected):
        field = 0x120B80 + index * 32
        offset = struct.unpack_from('<I', source, field)[0] - 0x02000000
        if not 0 <= offset < len(source):
            raise ValueError('Character-name pointer is outside ARM9')
        raw = source[offset:offset + 17]
        end = raw.find(b'\0')
        if end < 0 or raw[:end] != name.encode('ascii'):
            raise ValueError('Expected complete translated source name differs')
        copied = execute(source, raw[:end])
        rows.append({'index': index, 'pointer_field': field, 'offset': offset,
                     'name': name, 'bytes_before_nul': end, 'native_copy': copied})
    return rows


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Candidate differs from the reviewed source')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x3E368, 0x3E4D4), (0x46F00, 0x46F50),
             (0x47028, 0x4704C), (0x9DC5C, 0x9DCE4),
             (0x9F660, 0x9F6B8), (0x9EDA8, 0x9EDD8),
             (0x9F0B0, 0x9F0B4), (0xCD6CC, 0xCD750),
             (0xCDAB4, 0xCDAC4), (0xCED98, 0xCEDC8),
             (0x148E94, 0x148EB8), (0x120B80, 0x120C00))
    if any(source[lo:hi] != clean[lo:hi] for lo, hi in spans):
        raise ValueError('Native source-name initialization or table changed')
    if struct.unpack_from('<I', source, 0xCDAC0)[0] != 0x02120B80:
        raise ValueError('Native character table resolver differs')
    if struct.unpack_from('<I', source, 0x148EA8)[0] != 0x020CD6CC:
        raise ValueError('Stored-name virtual setter differs')
    report = {
        'status': 'pass-mapped-source-names-only', 'candidate_sha256': CANDIDATE_SHA,
        'rom_written': False, 'runtime_verified': False,
        'source_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])}
                         for lo, hi in spans],
        'names': inspect_names(source),
        'initialization_chain': [
            '3E3F4 calls 47028 with a character record index and stack record.',
            '47028 calls 46F00; CDAB4 resolves 120B80 + index * 32.',
            '46F20 copies the table main name into record + 8 using CED98.',
            '3E3FC calls 9DC5C with that record; 9DC84 calls constructor 9F660.',
            '9F6B4 retains the record pointer at object + 54.',
            '9DC8C calls 9EA38; 9EDBC loads the retained record.',
            '9EDD4 dispatches virtual slot + 14; current-player vtable targets CD6CC.',
            'CD6CC copies record + 8 into stored name + 20 using CED98.'
        ],
        'limitations': [
            'This proves the four current default source names fit and copy intact.',
            'It does not prove all edited names, character selection indices, saved names or received packets.',
            'Name editing in 9DCE4 and save/load writers still require boundary analysis.',
            'Result-row maximum remains conditional; no release integration credit.'
        ]
    }
    Path('work/analysis/grand_race_name_sources_v136_proof.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print('Four complete default names pass native copy; edited/save/network names remain pending.')


if __name__ == '__main__':
    main()
