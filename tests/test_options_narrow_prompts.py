import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_options_narrow_prompts import execute, prepare, respond


@pytest.mark.parametrize('kind,flags,text', [
    ('sailing', 0, 'Sailing Help is Off. Change to On?'),
    ('sailing', 2, 'Sailing Help is On. Change to Off?'),
    ('reports', 0, 'Reports are Off. Change to On?'),
    ('reports', 1, 'Reports are On. Change to Off?'),
])
def test_actual_options_caller_preserves_complete_prose_and_state_order(kind, flags, text):
    source = NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin')
    assert execute(prepare(source), kind, flags)['complete_prepared_text'] == text


@pytest.mark.parametrize('accepted', [False, True])
def test_native_response_preserves_unrelated_settings(accepted):
    source = NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin')
    assert respond(source, 'sailing', 255, accepted)['result_flags'] == (253 if accepted else 255)


def test_changed_response_mask_is_detected():
    source = bytearray(NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin'))
    struct.pack_into('<I', source, 0x3FD20, 0xE3C11001)
    with pytest.raises(ValueError, match='wrong preference'):
        respond(bytes(source), 'sailing', 2, True)
