import pytest

from dk4tool.rom.nds import NdsImage
from scripts import probe_common_native_word_wrap as probe


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('name', ['Ｆleet', 'Ｉndigo', 'Ｆ' * 18, 'Ｉ' * 18, 'Ｆleet  Group'])
def test_arm_wrap_preserves_complete_paragraph_and_name_spaces(source, name):
    original = f"Towns under {name}'s exclusive contracts paid ８８４６２９ gold coins in tribute."
    generated = probe.execute(source, original)
    assert generated.replace('\n  ', ' ') == original
    assert '８８４６２９' in generated
    assert len(generated.split('\n')) <= 4


def test_removed_newline_store_is_detected(source, monkeypatch):
    code = probe.helper_bytes()
    code = code.replace(bytes.fromhex('0100C5E4'), bytes.fromhex('0000A0E1'), 1)
    monkeypatch.setattr(probe, 'helper_bytes', lambda: code)
    original = "Towns under " + 'Ｆ' * 18 + "'s exclusive contracts paid ８８４６２９ gold coins in tribute."
    with pytest.raises(ValueError, match='return length'):
        probe.execute(source, original)
