"""Source-locked complete damaged-save prose with generated native wrapping."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '9c0b2992d7b2a731869b590af1455fb84ed5c4b87b296112f3793ea4a651a8db'
OFFSET, CAPACITY = 0x12EB4C, 52
ENGLISH = ': This save is corrupted and could not be loaded.'


def formatted_suffix():
    words = ENGLISH.split(' ')
    choices = []
    for cut in range(1, len(words)):
        first, second = ' '.join(words[:cut]), ' '.join(words[cut:])
        lengths = (6 + len(first), 2 + len(second))
        if max(lengths) <= 38:
            choices.append(((max(lengths), sum(n * n for n in lengths), cut), first, second))
    if not choices:
        raise ValueError('Full damaged-save prose cannot fit native rows')
    _, first, second = min(choices)
    result = first + '\n  ' + second
    if ' '.join(result.split()) != ENGLISH:
        raise ValueError('Generated layout changes complete damaged-save meaning')
    return result


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-damaged-save-release-v1' or sha(source) != SOURCE:
        raise ValueError('Damaged-save release requires exact complete V144')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Damaged-save review dependency changed')
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    if len(document['records']) != 1:
        raise ValueError('Exactly one complete damaged-save suffix is required')
    row = document['records'][0]
    if row['offset'] != OFFSET or row['capacity'] != CAPACITY or row['english'] != ENGLISH + '{PAD}':
        raise ValueError('Reviewed damaged-save meaning/allocation differs')
    clean_path = Path('work/clean.nds')
    canonical_path = Path('out/raphael_natural_v2_accepted_base.nds')
    if (sha(clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
            or sha(canonical_path.read_bytes()) != '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'):
        raise ValueError('Damaged-save clean/canonical source differs')
    for path in (clean_path, canonical_path):
        raw = NdsImage.open(path).read_file('/__arm9__.bin')
        if raw[OFFSET:OFFSET + CAPACITY] != bytes.fromhex(row['source_hex']) or raw[OFFSET:OFFSET + CAPACITY] != source[OFFSET:OFFSET + CAPACITY]:
            raise ValueError('Damaged-save complete original allocation differs')
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    if (review['status'] != 'reviewed-native-damaged-save-layout-gameplay-pending'
            or review['source_sha256'] != SOURCE or len(review['preparation_cases']) != 256
            or len(review['pixel_cases']) != 12 or not review['visual_review_complete']
            or any(case['split_words'] for case in review['pixel_cases'])):
        raise ValueError('Complete native damaged-save review required')
    for lock in review['consumer_locks']:
        if sha(source[lock['start']:lock['end']]) != lock['sha256']:
            raise ValueError('Damaged-save native copy/consumer changed')
    needle = struct.pack('<I', 0x02000000 + OFFSET)
    positions, cursor = [], 0
    while (cursor := source.find(needle, cursor)) >= 0:
        positions.append(cursor)
        cursor += 1
    if positions != [0xEE7D0]:
        raise ValueError('Damaged-save literal consumers differ')
    raw = formatted_suffix().encode('ascii') + b'\0'
    if len(raw) > CAPACITY:
        raise ValueError('Complete generated suffix exceeds owned capacity')
    saved = bytearray(source)
    saved[OFFSET:OFFSET + CAPACITY] = raw.ljust(CAPACITY, b'\0')
    saved = bytes(saved)
    if sha(saved) != config['target_arm9_sha256'] or sha(saved) != review['research_sha256']:
        raise ValueError('Generated damaged-save output differs from reviewed native bytes')
    return saved, {'status': 'pass-native-damaged-save-layout-gameplay-pending',
                   'authored_offsets': [OFFSET], 'arm9_sha256': sha(saved),
                   'all_other_arm9_bytes_preserved': True, 'runtime_verified': False}
