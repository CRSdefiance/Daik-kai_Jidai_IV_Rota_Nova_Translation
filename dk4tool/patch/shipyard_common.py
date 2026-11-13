"""Complete native Shipyard paragraphs and whole-selection cache packing."""

import struct

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries

IDS = tuple(range(784, 805))
SLOTS = {786: 2, 789: 1, 798: 1, 799: 1, 800: 1, 802: 1, 803: 3, 804: 2}


def compile_text(row):
    text = row['english'].removesuffix('{PAD}')
    n = row['message_id']
    if (not text.isascii() or text != ' '.join(text.split()) or any(c in text for c in '{}')
            or text.count('%s') != SLOTS.get(n, 0) or '%' in text.replace('%s', '')
            or any(token in text for token in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('One faithful paragraph and exact source substitutions required')
    if any(ord(c) < 32 or ord(c) >= 127 for c in text) or len(text) >= 200:
        raise ValueError('COMMON paragraph exceeds bounded native input or contains controls')
    # A generated native prefix, not translator-authored alignment. All selected
    # consumers now use the proven post-printf literal/balancing formatter.
    return b' ' + text.encode('ascii')


def plan(common, arm, authored):
    before = common_message_entries(common, arm, clean=False)
    assert tuple(sorted(authored)) == IDS
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 2 <= e.block <= 18]
    assert [e.message_id for e in selected] == list(range(164, 1713))
    for e in selected:
        assert set(blocks[e.block][e.block_offset + len(e.text) + 1:e.copy_end]) <= {0, 32}
    for block in range(2, 19):
        first = next(e for e in selected if e.block == block)
        assert set(blocks[block][:first.block_offset]) <= {0, 32}
    groups, group, body = [], [], bytearray()
    for e in selected:
        text = authored.get(e.message_id, e.text) + b'\0'
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body)))
            group, body = [], bytearray()
        group.append((e.message_id, len(body), text))
        body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 17, [len(raw) for _, raw in groups]
    rebuilt, target = list(blocks), bytearray(arm)
    fields, mapping = [], []
    for block, (group, raw) in zip(range(2, 19), groups, strict=True):
        rebuilt[block] = raw
        field = DIRECTORY_OFFSET + 4 * block
        struct.pack_into('<HH', target, field, group[0][0], len(raw))
        fields.append((field, 4))
        for number, offset, text in group:
            field = TABLE_OFFSET + 2 * number
            struct.pack_into('<H', target, field, offset)
            fields.append((field, 2))
            mapping.append({'id': number, 'block': block, 'offset': offset, 'text_hex': text[:-1].hex()})
    return IlnkContainer(rebuilt).to_bytes(), bytes(target), fields, mapping
