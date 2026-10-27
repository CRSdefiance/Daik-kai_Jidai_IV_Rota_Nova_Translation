"""Strict complete Deck explanation release with aligned source-owned relocation."""

import itertools
import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '092f5a7f365286c8683728843df8774b26a7ba4ca507f4e6b5d368be82e07e34'
PARAGRAPHS = {
    0x133024: 'A lookout makes it easier to discover towns and other locations at sea.',
    0x13305C: 'A captain slows the rise in sailor fatigue.',
    0x133090: 'An adjutant lets you send negotiation documents from the guild.',
    0x1330C8: 'This is where sailors row the oars. Navigators cannot be assigned here.',
}


def format_paragraph(english):
    words = english.split(' ')
    choices = []
    for count in range(1, 4):
        for cuts in itertools.combinations(range(1, len(words)), count - 1):
            bounds = (0, *cuts, len(words))
            lines = [' '.join(words[a:b]) for a, b in itertools.pairwise(bounds)]
            widths = [len(line) + (2 if n else 0) for n, line in enumerate(lines)]
            if max(widths) <= 28:
                choices.append(((count, max(widths), sum(n * n for n in widths), cuts), lines))
    if not choices:
        raise ValueError('Complete Deck explanation cannot fit its three rows')
    result = '\n  '.join(min(choices)[1])
    if ' '.join(result.split()) != english:
        raise ValueError('Deck generated layout changes prose')
    return result


def transform(source, pool):
    if sha(source) != SOURCE or pool['source_span'] != [0x133024, 0x133240]:
        raise ValueError('Deck release requires exact complete V145 source/pool')
    start, end = pool['source_span']
    owners, refs = pool['owners'], pool['all_byte_position_address_candidates']
    if len(owners) != 31 or len(refs) != 31 or any(r['component'] != 'arm9' for r in refs):
        raise ValueError('Complete Deck owners/reference grammar differs')
    actual = [(p, struct.unpack_from('<I', source, p)[0] - 0x02000000)
              for p in range(len(source) - 3)
              if start <= struct.unpack_from('<I', source, p)[0] - 0x02000000 < end]
    if actual != [(r['field_offset'], r['target_offset']) for r in refs]:
        raise ValueError('Complete Deck byte-position reference set differs')
    packed, moves, cursor = bytearray(), [], start
    for owner in owners:
        old, capacity = owner['offset'], owner['source_capacity']
        raw = bytes.fromhex(owner['current_bytes_hex'])
        if (old != cursor or raw != source[old:old + capacity]
                or raw.split(b'\0', 1)[0].decode('cp932') != owner['current_text']):
            raise ValueError('Deck neighboring owner bytes/wording differ')
        cursor += capacity
        text = format_paragraph(PARAGRAPHS[old]) if old in PARAGRAPHS else owner['current_text']
        encoded = text.encode('cp932') + b'\0'
        moves.append({'old_offset': old, 'new_offset': start + len(packed), 'complete_text': text})
        packed.extend(encoded)
        packed.extend(b'\0' * (-len(packed) % 4))
    if cursor != end or len(packed) != 536:
        raise ValueError('Complete aligned Deck allocation differs')
    saved = bytearray(source)
    saved[start:end] = packed.ljust(end - start, b'\0')
    by_old = {m['old_offset']: m for m in moves}
    for ref in refs:
        field = ref['field_offset']
        if ref['interior_byte_offset'] or start <= field < end:
            raise ValueError('Deck interior reference requires separate proof')
        struct.pack_into('<I', saved, field, 0x02000000 + by_old[ref['owner_offset']]['new_offset'])
    restored = bytearray(saved)
    restored[start:end] = source[start:end]
    for ref in refs:
        field = ref['field_offset']
        restored[field:field + 4] = source[field:field + 4]
    if bytes(restored) != source:
        raise ValueError('Deck release changes unrelated ARM9 bytes')
    return bytes(saved), moves


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-deck-explanation-release-v1' or sha(source) != SOURCE:
        raise ValueError('Deck release requires exact complete V145')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Deck source/manuscript/native evidence dependency changed')
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    rows = document['records']
    if len(rows) != 4 or {r['offset'] for r in rows} != set(PARAGRAPHS):
        raise ValueError('All four complete Deck explanations required')
    capacities = {0x133024: 56, 0x13305C: 52, 0x133090: 56, 0x1330C8: 52}
    if any(row['capacity'] != capacities[row['offset']] for row in rows):
        raise ValueError('Complete Deck source allocation sizes differ')
    paths = [(Path('work/clean.nds'), 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'),
             (Path('out/raphael_natural_v2_accepted_base.nds'), '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe')]
    for path, digest in paths:
        if sha(path.read_bytes()) != digest:
            raise ValueError('Deck clean/canonical source differs')
        original = NdsImage.open(path).read_file('/__arm9__.bin')
        for row in rows:
            at, capacity = row['offset'], row['capacity']
            if (row['english'] != PARAGRAPHS[at] + '{PAD}'
                    or original[at:at + capacity] != bytes.fromhex(row['source_hex'])
                    or source[at:at + capacity] != original[at:at + capacity]):
                raise ValueError('Deck source meaning/complete allocation differs')
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    if (review['status'] != 'reviewed-native-deck-layout-connected-consumers-gameplay-pending'
            or len(review['pixel_cases']) != 8 or len(review['connected_cases']) != 8
            or len(review['native_pointer_consumer_cases']) != 31
            or review['visual_review']['panels_reviewed'] != 4):
        raise ValueError('Complete native Deck ink/connected review required')
    for lock in review['consumer_locks']:
        if sha(source[lock['start']:lock['end']]) != lock['sha256']:
            raise ValueError('Deck native selector/geometry/caller changed')
    pool = json.loads(Path(config['pool']).read_text(encoding='utf-8'))
    saved, moves = transform(source, pool)
    if sha(saved) != config['target_arm9_sha256'] or sha(saved) != review['research_arm9_sha256']:
        raise ValueError('Deck release output differs from reviewed native bytes')
    return saved, {'status': 'pass-native-deck-explanations-gameplay-pending',
                   'arm9_sha256': sha(saved), 'source_span': pool['source_span'],
                   'used_aligned_bytes': 536, 'owned_bytes': 540, 'references_relocated': 31,
                   'authored_offsets': sorted(PARAGRAPHS), 'all_other_arm9_bytes_preserved': True,
                   'inherited_owners_preserved': 27, 'moves': moves, 'runtime_verified': False}
