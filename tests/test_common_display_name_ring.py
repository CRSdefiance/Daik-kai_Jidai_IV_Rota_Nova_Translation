import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_ring import execute


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('index', range(32))
def test_name_and_amount_coexist_at_every_ring_index(source, index):
    result = execute(source, b'F' * 18, index)
    assert result['distinct_slots']
    assert result['all_other_ring_bytes_intact']
    assert result['next_index'] == (index + 2) % 32


@pytest.mark.parametrize('index', [-1, 32])
def test_unmapped_ring_indices_rejected(source, index):
    with pytest.raises(ValueError, match='ring index'):
        execute(source, b'Fleet', index)
