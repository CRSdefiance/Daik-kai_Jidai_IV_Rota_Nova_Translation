"""Verify native name caller loops, payload senders and receiving slots together."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_sender import execute as send
from scripts.execute_grand_race_packet_name import execute as receive
from scripts.execute_grand_race_saved_name import execute as storage
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Pinned candidate differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xF8EC4, 0xF8F00), (0xF9C34, 0xF9C70), (0xF9154, 0xF9158),
             (0xFA0F4, 0xFA0F8), (0x1371C, 0x13724), (0x148EB4, 0x148EB8),
             (0x830B0, 0x830D8), (0x82FB8, 0x82FE0), (0x469DC, 0x46A1C),
             (0x46BE0, 0x46C20), (0xD010C, 0xD016C), (0xD01AC, 0xD0264),
             (0xFA5B0, 0xFA63C))
    if any(source[lo:hi] != clean[lo:hi] for lo, hi in spans):
        raise ValueError('Native sender/getter/storage/receiver source changed')
    if (struct.unpack_from('<2I', source, 0x1371C) != (0xE2800020, 0xE12FFF1E)
            or struct.unpack_from('<I', source, 0x148EB4)[0] != 0x0201371C
            or any(struct.unpack_from('<I', source, at)[0] != 0x19E4 for at in (0xF9154, 0xFA0F4))):
        raise ValueError('Sender stored-name getter mapping differs')
    names = [b'A' * size for size in range(1, 17)] + ['ア'.encode('cp932') * size for size in (1, 4, 7, 8)]
    cases = []
    for name in names:
        field = (name + b'\0').ljust(17, b'\xa5')
        saved = storage(source, field, 'save')
        loaded = storage(source, bytes.fromhex(saved['output_hex']), 'load')
        for role in ('host', 'join'):
            sent = send(source, bytes.fromhex(loaded['output_hex']), role)
            receives = [receive(source, bytes.fromhex(sent['payload_field_hex']), player) for player in range(4)]
            if any(row['saved_field_hex'] != field.hex() or row['terminated_at'] != len(name) for row in receives):
                raise ValueError('Native name pipeline dropped a byte or NUL')
            cases.append({'name_hex': name.hex(), 'role': role, 'storage': [saved, loaded],
                          'send': sent, 'receives': receives})
    output = {'status': 'pass-valid-name-fields-native-caller-pipeline-with-explicit-io-contract',
              'candidate_sha256': CANDIDATE_SHA, 'rom_written': False, 'runtime_verified': False,
              'source_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])} for lo, hi in spans],
              'stored_name_count': len(names), 'sender_count': len(cases),
              'receiver_count': sum(len(case['receives']) for case in cases), 'cases': cases,
              'limitations': ['Native stored-name getter mapping source-verified; getter dispatch not executed.',
                              'Save/load caller loops executed; successful single-byte I/O contracts modeled, helper bodies/physical save files not executed.',
                              'Both native send loops and receiver slot copies executed; wireless network transport not executed.',
                              'Incoming names initialized valid and terminated; malformed/truncated saves/packets are not validated by these routines.',
                              'Full compound printf/frame painting and gameplay remain pending; eight final formatting gates unchanged.']}
    Path('work/analysis/grand_race_name_pipeline_v136_proof.json').write_text(json.dumps(output, indent=2) + '\n')
    print('20 complete fields: 40 host/join sends and 160 receives pass native caller pipeline; explicit successful save/load I/O scope.')


if __name__ == '__main__':
    main()
