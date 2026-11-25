import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_escape import escape
from scripts.probe_common_tribute_preprocessing import execute


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('letter', ['F', 'I'])
@pytest.mark.parametrize('position', range(18))
def test_each_ascii_name_position_survives(source, letter, position):
    name = ('a' * position + letter + 'a' * (17 - position)).encode('ascii')
    safe = escape(source, name)
    assert safe.decode('cp932') == name.decode('ascii').replace(letter, chr(ord(letter) + 0xFEE0))
    result = execute(source, '%s received %s.', safe, display_name_capacity=36)
    assert result['name_preserved_after_macros']


@pytest.mark.parametrize('letter', ['F', 'I'])
def test_maximum_expanded_display_capacity(source, letter):
    safe = escape(source, letter.encode('ascii') * 18)
    assert len(safe) == 36
    assert execute(source, '%s received %s.', safe, display_name_capacity=36)['name_preserved_after_macros']


@pytest.mark.parametrize('name', [b'', b'A' * 19, b'F\0I'])
def test_invalid_stored_name_rejected(source, name):
    with pytest.raises(ValueError, match='eighteen-byte'):
        escape(source, name)


def test_cp932_extension_alias_bytes_remain_exact(source):
    name = b'\xfa\x40' * 9
    assert name.decode('cp932').encode('cp932') != name
    assert escape(source, name) == name
