"""Strict V143-scoped narrow-English Options prompt replacement."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '1b5e9c5bec1418770c138256ecdd7d2c74d0f0db67fda6330a10f70ae68a82ec'
SLOTS = {0x13880C: (56, 0x3FD4C, 'Sailing Help is %s. Change to %s?'),
         0x138844: (52, 0x3FDD0, 'Reports are %s. Change to %s?')}


def apply_release(arm9, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-options-narrow-release-v1' or sha(arm9) != SOURCE or config.get('source_arm9_sha256') != SOURCE:
        raise ValueError('Options narrow release requires exact complete V143')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Options narrow manuscript/native review dependency changed')
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    if review.get('status') != 'reviewed-native-options-layout-gameplay-pending' or review.get('research_sha256') != config['target_arm9_sha256']:
        raise ValueError('Options narrow native output/layout review differs')
    clean_path = Path('work/clean.nds')
    canonical_path = Path('out/raphael_natural_v2_accepted_base.nds')
    if (sha(clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
            or sha(canonical_path.read_bytes()) != '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'):
        raise ValueError('Options clean/canonical source differs')
    clean = NdsImage.open(clean_path).read_file('/__arm9__.bin')
    canonical = NdsImage.open(canonical_path).read_file('/__arm9__.bin')
    rows = document['records']
    if len(rows) != 2 or {row['offset'] for row in rows} != set(SLOTS):
        raise ValueError('Both complete Options prompts are required')
    saved = bytearray(arm9)
    for row in rows:
        at = row['offset']
        capacity, literal, english = SLOTS[at]
        if (row['capacity'] != capacity or bytes.fromhex(row['source_hex']) != clean[at:at + capacity]
                or bytes.fromhex(row['canonical_source_hex']) != canonical[at:at + capacity]
                or bytes.fromhex(row['parent_hex']) != arm9[at:at + capacity]
                or row['english'] != english + '{PAD}'):
            raise ValueError('Options complete source allocation or reviewed prose differs')
        needle = struct.pack('<I', 0x02000000 + at)
        positions, cursor = [], 0
        while (cursor := arm9.find(needle, cursor)) >= 0:
            positions.append(cursor)
            cursor += 1
        if positions != [literal]:
            raise ValueError('Options prompt literal consumers differ')
        raw = english.encode('ascii') + b'\0'
        if len(raw) > capacity or english.count('%s') != 2:
            raise ValueError('Options narrow substitutions/allocation differ')
        saved[at:at + capacity] = raw.ljust(capacity, b'\0')
    result = bytes(saved)
    if sha(result) != config['target_arm9_sha256']:
        raise ValueError('Options narrow output differs from reviewed native bytes')
    return result, {'status': 'pass-native-options-narrow-layout-gameplay-pending',
                    'authored_offsets': sorted(SLOTS), 'source_arm9_sha256': SOURCE,
                    'expected_arm9_sha256': sha(result), 'all_other_arm9_bytes_preserved': True,
                    'original_current_proposed_argument_order_preserved': True,
                    'runtime_verified': False}
