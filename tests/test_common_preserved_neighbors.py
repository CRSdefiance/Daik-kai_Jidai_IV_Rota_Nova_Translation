import json
import struct
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from dk4tool.script.common_native_reblocking import plan
from dk4tool.script.common_reblocking_release import read_preserved_neighbors


@pytest.fixture(scope='module')
def mixed_owner():
    parent = NdsImage.open('out/all_routes_combined_v119_candidate.nds')
    common, arm9 = parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin')
    before = common_message_entries(common, arm9, clean=False)
    manuscript = json.loads(Path('translations/common_bgm_complete_titles_v2.json').read_text(encoding='utf-8'))
    authored = {r['message_id']: r['english'].removesuffix('{PAD}').encode('ascii')
                for r in manuscript['records']}
    preserved = {i: before[i].text for i in (3289, 3290)}
    return common, arm9, before, authored, preserved


def test_complete_mixed_owner_preserves_all_neighbor_bytes_and_global_ids(mixed_owner):
    common, arm9, before, authored, preserved = mixed_owner
    rebuilt, mapped, report = plan(common, arm9, authored,
                                   compact_existing_english_padding=True, preserved=preserved)
    assert report['preserved_untranslated_ids'] == [3289, 3290]
    assert report['authored_ids'] == list(range(3251, 3289))
    blocks = IlnkContainer.parse(rebuilt).blocks
    directory = [struct.unpack_from('<HH', mapped, DIRECTORY_OFFSET + b * 4) for b in range(41)]
    offsets = struct.unpack_from('<3669H', mapped, TABLE_OFFSET)
    for e in before:
        i = e.message_id
        block = max(b for b, (first, _) in enumerate(directory) if first <= i)
        start, following = offsets[i:i + 2]
        limit = following if following >= start else directory[block][1]
        actual = blocks[block][start:limit].split(b'\0', 1)[0]
        assert actual.rstrip(b' ') == authored.get(i, e.text).rstrip(b' ')
        if i in preserved:
            assert actual == preserved[i]
    assert report['max_native_copy_bytes'] < 512


def test_missing_promotional_neighbor_remains_a_whole_owner_error(mixed_owner):
    common, arm9, _, authored, preserved = mixed_owner
    with pytest.raises(ValueError, match='Every authored packed neighbor'):
        plan(common, arm9, authored, preserved={3289: preserved[3289]})


def test_changed_preserved_first_byte_is_rejected(mixed_owner):
    common, arm9, _, authored, preserved = mixed_owner
    bad = {**preserved, 3290: preserved[3290][1:]}
    with pytest.raises(ValueError, match='complete current span'):
        plan(common, arm9, authored, preserved=bad)


def test_preserved_declaration_cannot_overlap_authored_or_unrelated_owner(mixed_owner):
    common, arm9, before, authored, preserved = mixed_owner
    with pytest.raises(ValueError, match='distinct verified native IDs'):
        plan(common, arm9, authored, preserved={**preserved, 3251: before[3251].text})
    with pytest.raises(ValueError, match='complete current span'):
        plan(common, arm9, authored, preserved={**preserved, 3291: before[3291].text})


def test_preserved_source_lock_cannot_be_replaced_with_current_bytes(mixed_owner):
    _, _, before, authored, _ = mixed_owner
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    declaration = {'message_id': 3290, 'source_hex': source[3290].text.hex(),
                   'current_hex': before[3290].text.hex(),
                   'status': 'untranslated-renderer-classification-pending',
                   'reason': 'Classify the promotional renderer; preserve the full native span.'}
    assert read_preserved_neighbors([declaration], source, before, authored) == {3290: before[3290].text}
    with pytest.raises(ValueError, match='source/current lock differs'):
        read_preserved_neighbors([{**declaration, 'source_hex': source[3290].text[1:].hex()}],
                                 source, before, authored)
    with pytest.raises(ValueError, match='Invalid, duplicate'):
        read_preserved_neighbors([declaration, declaration], source, before, authored)
