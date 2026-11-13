import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_preprocessing import execute


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


TEXT = "Towns under %s's exclusive contracts paid %s gold coins in tribute."


@pytest.mark.parametrize('name', [b'A', 'あ'.encode('cp932') * 9])
def test_baseline_safe_names(source, name):
    result = execute(source, TEXT, name)
    assert result['name_preserved_after_macros']
    assert result['expanded'] == result['formatted']


@pytest.mark.parametrize('name, damaged', [(b'Fleet', 'leet'), (b'Indigo', '僕digo')])
def test_v142_macro_collision_is_reproduced(source, name, damaged):
    # Evidence test for the pinned defective baseline, not a release approval.
    result = execute(source, TEXT, name)
    assert name.decode('ascii') in result['formatted']
    assert not result['name_preserved_after_macros']
    assert f"{damaged}'s" in result['expanded']


def test_oversized_name_rejected(source):
    with pytest.raises(ValueError, match='bounded name'):
        execute(source, TEXT, b'A' * 19)
