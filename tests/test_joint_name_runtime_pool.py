import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_joint_name_runtime_pool import prepare


@pytest.fixture(scope='module')
def repair():
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    return source, clean, prepare(source, clean)


def test_every_complete_name_and_aligned_start(repair):
    source, _, (saved, start, used, moves, owners) = repair
    assert used == 1480
    assert len(owners) == 117
    assert len(moves) == 239
    assert next(m for m in moves if m['field'] == 0x705E8)['text'] == 'Monster'
    assert sum(m['batch'] == 'all_item_names_arm9_v1' for m in moves) == 45
    assert sum(m.get('source_reviewed_role_revision', False) for m in moves) == 8
    assert all(m['text'] == 'Square Shopkeeper' for m in moves
               if m.get('source_reviewed_role_revision'))
    for move in moves:
        pointer = struct.unpack_from('<I', saved, move['field'])[0]
        delta = pointer - 0x027E0000
        assert delta % 4 == 0
        assert saved[start + delta:].split(b'\0', 1)[0].decode('cp932') == move['text']
    assert saved[start + 1540:start + 1632] == source[start + 1540:start + 1632]


def test_preserves_itcm_and_all_unowned_bytes(repair):
    source, _, (saved, start, _, moves, _) = repair
    restored = bytearray(saved)
    restored[start:start + 1540] = source[start:start + 1540]
    for move in moves:
        at = move['field']
        restored[at:at + 4] = source[at:at + 4]
    assert restored == source


def test_rejects_modified_parent(repair):
    source, clean, _ = repair
    damaged = bytearray(source)
    damaged[0x11E468] ^= 1
    with pytest.raises(ValueError, match='Exact V147'):
        prepare(bytes(damaged), clean)


def test_rejects_unowned_original_storage(repair):
    source, clean, _ = repair
    damaged = bytearray(clean)
    damaged[0x171E60] = 1
    with pytest.raises(ValueError, match='not empty'):
        prepare(source, bytes(damaged))


def test_rejects_sdk_table_mismatch(repair):
    source, clean, _ = repair
    damaged = bytearray(clean)
    damaged[0x171E60 + 1540] ^= 1
    with pytest.raises(ValueError, match='SDK trailing'):
        prepare(source, bytes(damaged))
