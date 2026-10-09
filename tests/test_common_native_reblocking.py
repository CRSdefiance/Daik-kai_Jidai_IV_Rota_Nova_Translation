import json
import re
import struct
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_entry_tables import ITEM_TABLES
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts.plan_common_native_reblocking import plan


@pytest.fixture(scope='module')
def inputs():
    rom = NdsImage.open('out/all_routes_combined_v119_candidate.nds')
    common, arm9 = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    rows = json.loads(Path('translations/common_b12_complete_manuscript_v1.json').read_text(encoding='utf-8'))['records']
    authored = {r['message_id']: r['english'].removesuffix('{PAD}').encode('cp932') for r in rows}
    return common, arm9, authored


def test_all_native_ids_are_selected_with_complete_source_argument_shapes(inputs):
    common, arm9, authored = inputs
    rebuilt, mapped_arm9, report = plan(common, arm9, authored)
    old_blocks, blocks = IlnkContainer.parse(common).blocks, IlnkContainer.parse(rebuilt).blocks
    assert blocks[:12] == old_blocks[:12]
    assert len(blocks) == 41 and all(len(b) <= 4096 for b in blocks)
    assert report['max_native_copy_bytes'] < 512
    assert arm9[:DIRECTORY_OFFSET] == mapped_arm9[:DIRECTORY_OFFSET]
    assert arm9[TABLE_OFFSET + 3669 * 2:] == mapped_arm9[TABLE_OFFSET + 3669 * 2:]
    parent = common_message_entries(common, arm9, clean=False)
    clean = NdsImage.open('work/clean.nds')
    sources = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    first_ids = [struct.unpack_from('<H', mapped_arm9, DIRECTORY_OFFSET + i * 4)[0] for i in range(41)]
    checked = 0
    for before, source in zip(parent, sources, strict=True):
        i = before.message_id
        block = next((b - 1 for b in range(1, 41) if i < first_ids[b]), 40)
        start, following = struct.unpack_from('<HH', mapped_arm9, TABLE_OFFSET + i * 2)
        end = following if following >= start else len(blocks[block])
        text = blocks[block][start:end].partition(b'\0')[0].rstrip(b' ')
        assert text == authored.get(i, before.text.rstrip(b' '))
        assert re.findall(rb'%[sdi]', text) == re.findall(rb'%[sdi]', source.text)
        checked += 1
    assert checked == 3668
    # Real message 1034 changes blocks; its unknown-fleet report must
    # survive both the selector change and its new pointer.
    assert any(1034 in r['message_ids'] and r['new_owner'][0] != 12 for r in report['relocations'])


def test_reblocking_rejects_an_incomplete_packed_owner(inputs):
    common, arm9, authored = inputs
    partial = dict(authored)
    del partial[975]
    with pytest.raises(ValueError, match='packed neighbor'):
        plan(common, arm9, partial)


@pytest.mark.parametrize('invalid', [b'', b'bad\0text', b'bad\ntext', b'bad\rtext'])
def test_reblocking_rejects_unsafe_authored_bytes(inputs, invalid):
    common, arm9, authored = inputs
    invalid_authored = dict(authored)
    invalid_authored[964] = invalid
    with pytest.raises(ValueError, match='nonempty CP932 paragraph'):
        plan(common, arm9, invalid_authored)


def test_reblocking_rejects_a_record_larger_than_the_live_cache(inputs):
    common, arm9, authored = inputs
    oversized = dict(authored)
    oversized[964] = b'A' * 4097
    with pytest.raises(ValueError, match='exceeds cache capacity'):
        plan(common, arm9, oversized)


def test_reblocking_rejects_a_changed_loader(inputs):
    common, arm9, authored = inputs
    corrupted = bytearray(arm9)
    corrupted[0x53558] ^= 1
    with pytest.raises(ValueError, match='loader/table evidence mismatch'):
        plan(common, bytes(corrupted), authored)


def test_padding_compaction_preserves_all_visible_text_and_unselected_bytes():
    rom = NdsImage.open('out/all_routes_combined_v122_candidate.nds')
    common, arm9 = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    rows = json.loads(Path('translations/common_japanese_b26_manuscript_v1.json').read_text(encoding='utf-8'))['records']
    authored = {r['message_id']: r['english'].removesuffix('{PAD}').encode('cp932') for r in rows}
    with pytest.raises(ValueError, match='needs 30 blocks'):
        plan(common, arm9, authored)
    rebuilt, mapped, report = plan(common, arm9, authored, compact_existing_english_padding=True)
    old = common_message_entries(common, arm9, clean=False)
    blocks = IlnkContainer.parse(rebuilt).blocks
    prior_blocks = IlnkContainer.parse(common).blocks
    assert len(blocks) == 41 and blocks[:12] == prior_blocks[:12]
    assert all(len(block) <= 4096 for block in blocks)
    assert report['removed_english_padding_bytes'] > 0
    assert report['max_native_copy_bytes'] < 512
    first_ids = [struct.unpack_from('<H', mapped, DIRECTORY_OFFSET + b * 4)[0] for b in range(41)]
    for e in old:
        b = max(b for b, first in enumerate(first_ids) if first <= e.message_id)
        start, following = struct.unpack_from('<HH', mapped, TABLE_OFFSET + e.message_id * 2)
        end = following if following >= start else len(blocks[b])
        text = blocks[b][start:end].partition(b'\0')[0].rstrip(b' ')
        assert text == authored.get(e.message_id, e.text.rstrip(b' '))
    for relocation in report['relocations']:
        owner = tuple(relocation['old_owner'])
        entries = [e for e in old if (e.block, e.record_index) == owner]
        if any(e.message_id in authored for e in entries):
            continue
        raw = prior_blocks[owner[0]].split(b'\0')[owner[1]]
        new_raw = bytes.fromhex(relocation['raw_hex'])
        item_ids = {(offset - TABLE_OFFSET) // 2 + i
                    for offset, count, *_ in ITEM_TABLES.values() for i in range(count)}
        if not entries or any(e.message_id in item_ids for e in entries):
            assert new_raw == raw
        else:
            assert new_raw[:entries[0].start] == raw[:entries[0].start]
            tail = raw[entries[-1].end:]
            assert not tail or new_raw.endswith(tail)
            for e in entries:
                if any((ord(c) < 32 or ord(c) >= 127) and c not in 'ＩＦ'
                       for c in e.text.decode('cp932')):
                    assert e.text in new_raw
