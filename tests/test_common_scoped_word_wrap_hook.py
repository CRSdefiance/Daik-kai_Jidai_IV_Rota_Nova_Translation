import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_scoped_word_wrap_hook import check_scope, prepare


@pytest.fixture(scope='module')
def source():
    return prepare(NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin'))[0]


@pytest.mark.parametrize('parent,message,active', [(0x020546E8, 83, True),
                                                 (0x020546E8, 82, False),
                                                 (0x0205469C, 83, False),
                                                 (0x02054720, 83, False)])
def test_modal_scope_and_original_pronoun_expansion(source, parent, message, active):
    result = check_scope(source, parent, message, 'I? says hello.')
    assert result['word_wrapper_invoked'] is active
    assert result['original_macro_expander_executed']
    assert result['original_expansion'] == '僕 says hello.'


def test_serialized_payload_fits_resident_overlay_gap():
    original = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    _, placement = prepare(original)
    assert placement['total_payload_bytes'] == 548
    assert placement['wrapper_address'] < 0x01FFA000
