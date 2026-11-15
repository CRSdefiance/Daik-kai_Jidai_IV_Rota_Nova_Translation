import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_autoload import execute
from scripts.probe_common_display_name_hook import prepare


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


def test_real_copier_loads_extended_resident_section(source):
    before = execute(source)
    after = execute(prepare(source)[0])
    assert after['sections'][0]['bytes'] == before['sections'][0]['bytes'] + 168
    assert after['sections'][1] == before['sections'][1]
    assert after['overlay_destination_untouched']
    assert after['native_memory_writes'] == before['native_memory_writes'] + 42


def test_missing_native_store_is_rejected(source):
    modified = bytearray(source)
    struct.pack_into('<I', modified, 0xA10, 0xE1A00000)
    with pytest.raises(ValueError, match='Startup section copier did not return'):
        execute(bytes(modified))
