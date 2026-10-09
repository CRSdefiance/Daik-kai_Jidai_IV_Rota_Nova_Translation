import pytest

from dk4tool.patch.name_editor_atomic_append import END, START, apply
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_append import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE


@pytest.fixture
def source():
    return NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')


@pytest.mark.parametrize('size', range(17))
@pytest.mark.parametrize('inserted', [b'B', 'ア'.encode('cp932')])
def test_atomic_complete_insertion(source, size, inserted):
    result = execute(apply(source), b'A' * size, inserted, 16, full_return=True)
    fits = size + len(inserted) <= 16
    assert bytes.fromhex(result['result_hex']) == b'A' * size + (inserted if fits else b'')
    assert result['rejected_whole_insert'] == (not fits)
    assert result['terminated_at'] <= 16
    assert result['stack_balanced'] is True
    assert [call['target'] for call in result['external_calls']] == (
        [0xB0B54, 0xB0C70] if fits else [0xB0C70])
    if not fits:
        assert result['writes'] == []


def test_only_owned_instructions_change(source):
    patched = apply(source)
    assert patched[:START] == source[:START]
    assert patched[END:] == source[END:]
    assert len(patched) == len(source)


def test_source_lock_rejects_different_loop(source):
    mutated = bytearray(source)
    mutated[START] ^= 1
    with pytest.raises(ValueError, match='source differs'):
        apply(mutated)
