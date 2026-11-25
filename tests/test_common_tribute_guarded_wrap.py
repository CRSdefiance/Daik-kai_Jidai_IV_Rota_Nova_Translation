import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded
from scripts.probe_common_tribute_modal_pixels import verify


@pytest.fixture(scope='module')
def assets():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    return rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')


@pytest.mark.parametrize('length', [13, 14])
@pytest.mark.parametrize('mode', [4, 16])
def test_native_guard_keeps_leading_continuation_at_both_parities(assets, length, mode):
    source, font = assets
    native = verify(source, font, 'A' * length + '\n  Leading glyph survives.', mode, guarded=True)
    continuation = [event for event in native['glyph_events'] if event['y'] == 12 and event['code'] != 32]
    assert continuation[0]['code'] == ord('L')
    assert continuation[0]['x'] == 6


def test_money_stays_one_complete_token():
    text = "Towns under " + 'Ｆ' * 18 + "'s exclusive contracts paid ８８４６２９ gold coins in tribute."
    generated = wrap_expanded(text)
    assert generated.replace('\n  ', ' ') == text
    assert len(generated.split('\n')) <= 4
    assert any('８８４６２９' in row for row in generated.split('\n'))


def test_authored_controls_and_oversized_words_rejected():
    with pytest.raises(ValueError, match='expanded paragraph'):
        wrap_expanded('Text\nNext')
    with pytest.raises(ValueError, match='Complete word'):
        wrap_expanded('Ｆ' * 20)


def test_unprotected_modal_line_rejected(assets):
    source, font = assets
    with pytest.raises(ValueError, match='two machine spaces'):
        verify(source, font, 'First\nLeading', 16, guarded=True)
