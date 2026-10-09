import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import HELPER, HOOK, branch_link, execute, prepare


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


@pytest.fixture(scope='module')
def saved(source):
    return prepare(source)[0]


@pytest.mark.parametrize('name', [b'Fleet', b'Indigo', b'F' * 18, b'I' * 18])
@pytest.mark.parametrize('index', [0, 30, 31])
def test_actual_hook_preserves_call_arguments_and_live_registers(saved, name, index):
    result = execute(saved, name, index)
    assert result['native_arguments'][0] == 83
    assert result['live_registers_preserved']


def test_original_arm9_required(source):
    modified = bytearray(source)
    modified[HOOK] ^= 1
    with pytest.raises(ValueError, match='Exact V142'):
        prepare(bytes(modified))


def test_serialized_hook_instruction_and_payload_size(source):
    saved, payload = prepare(source)
    assert len(payload) == 168
    assert struct.unpack_from('<I', saved, HOOK)[0] == branch_link(0x02000000 + HOOK, HELPER + 128)


@pytest.mark.parametrize('address', [0x10000001, 0x08000000])
def test_invalid_arm_branch_rejected(address):
    with pytest.raises(ValueError, match='branch target'):
        branch_link(HELPER, address)
