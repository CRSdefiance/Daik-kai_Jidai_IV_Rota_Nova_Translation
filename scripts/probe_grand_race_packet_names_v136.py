"""Verify complete valid name fields reach every result slot and full row fits."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_packet_name import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA
from scripts.probe_grand_race_result_rows import assemble_row


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Current candidate differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if source[0xFA5B0:0xFA63C] != clean[0xFA5B0:0xFA63C]:
        raise ValueError('Original native packet copy changed')
    proposal = Path('work/analysis/grand_race_complete_ui_proposal_v136')
    proposed = (proposal / 'proposed_arm9.bin').read_bytes()
    proposal_report = json.loads((proposal / 'report.json').read_text())
    if proposal_report['proposed_arm9_sha256'] != sha(proposed):
        raise ValueError('Complete proposal changed')
    if proposed[0xFA5B0:0xFA63C] != source[0xFA5B0:0xFA63C]:
        raise ValueError('Combined proposal changed native name transfer')
    allocation_path = Path('work/analysis/grand_race_ui_allocation_v136/report.json')
    allocation = json.loads(allocation_path.read_text())
    labels = {}
    for row in allocation['selections']:
        if row['message'].startswith(('PLACE_', 'NUMBER_')):
            field = row['pointer_fields'][0]
            offset = struct.unpack_from('<I', proposed, field)[0] - 0x02000000
            label = proposed[offset:proposed.index(0, offset)].decode('ascii')
            if label != row['line']:
                raise ValueError('Complete compound row label differs')
            labels[row['message']] = label
    if len(labels) != 8 or struct.unpack_from('<2I', proposed, 0x12ED04) != (180, 12):
        raise ValueError('Complete labels and wider result frame required')
    names = [b'A' * size for size in range(1, 17)] + [
        'ア'.encode('cp932') * size for size in (1, 4, 7, 8)]
    transfers, rows = [], []
    for name in names:
        field = (name + b'\0').ljust(17, b'\xa5')
        for player in range(4):
            transfer = execute(proposed, field, player)
            if transfer['terminated_at'] != len(name):
                raise ValueError('Native transfer lost name termination')
            transfers.append(transfer)
            transferred = bytes.fromhex(transfer['saved_field_hex']).split(b'\0', 1)[0]
            for place in range(1, 5):
                saved, width = assemble_row(labels[f'PLACE_{place}'], labels[f'NUMBER_{player + 1}'], transferred)
                if width > 180 or len(saved) > 32:
                    raise ValueError('Full compound row exceeds its native area or buffer')
                rows.append({'player': player, 'place': place, 'name_hex': name.hex(),
                             'full_row_hex': saved.hex(), 'bytes_with_nul': len(saved), 'width': width})
    output = {
        'status': 'pass-native-transfer-of-valid-terminated-fields-and-compound-bounds',
        'candidate_sha256': CANDIDATE_SHA, 'proposed_arm9_sha256': sha(proposed),
        'allocation_sha256': sha(allocation_path.read_bytes()),
        'packet_copy_sha256': sha(source[0xFA5B0:0xFA63C]),
        'rom_written': False, 'runtime_verified': False,
        'transfer_count': len(transfers), 'compound_row_count': len(rows),
        'max_buffer_bytes_with_nul': max(row['bytes_with_nul'] for row in rows),
        'max_width_pixels': max(row['width'] for row in rows),
        'transfers': transfers, 'rows': rows,
        'limitations': ['Actual FA5B8:FA614 slot selection and copy executed for all four slots.',
                        'Incoming fields are initialized valid ASCII/full-width CP932 names of at most sixteen bytes plus NUL.',
                        'Transfer synthesizes no NUL; complete incoming producer/save/receive validation remains separate.',
                        'Compound row assembly uses mapped printf order and native advances; printf body/artwork/gameplay not executed.',
                        'Eight final formatting gates stay closed pending remaining producer and frame evidence.']}
    Path('work/analysis/grand_race_packet_names_v136_proof.json').write_text(json.dumps(output, indent=2) + '\n')
    print(f'{len(transfers)} native name transfers and {len(rows)} full compound rows pass; producer/frame gates remain explicit.')


if __name__ == '__main__':
    main()
