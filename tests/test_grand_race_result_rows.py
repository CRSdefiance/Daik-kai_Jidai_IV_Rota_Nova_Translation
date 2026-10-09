import pytest

from scripts.probe_grand_race_result_rows import assemble_row


def test_complete_long_ascii_name_retains_all_bytes_but_exceeds_old_frame():
    raw, width = assemble_row('1st Place', '1P', b'ABCDEFGHIJKLMNOP')
    assert raw == b'1st Place 1P ABCDEFGHIJKLMNOP\0'
    assert len(raw) == 30 and width == 174
    assert width > 156 and width <= 180


def test_full_eight_character_japanese_name_has_same_width_budget():
    name = '一二三四五六七八'.encode('cp932')
    raw, width = assemble_row('4th Place', '4P', name)
    assert raw.endswith(name + b'\0')
    assert len(raw) == 30 and width == 174


@pytest.mark.parametrize('name', [b'', b'A' * 17, b'ABC\0DEF', b'A\nB'])
def test_incomplete_or_over_limit_name_is_rejected(name):
    with pytest.raises(ValueError):
        assemble_row('1st Place', '1P', name)


def test_incomplete_cp932_pair_is_rejected():
    with pytest.raises(UnicodeDecodeError):
        assemble_row('1st Place', '1P', b'\x88')


def test_complete_printf_buffer_limit_is_checked_separately_from_name_limit():
    with pytest.raises(ValueError, match='32-byte buffer'):
        assemble_row('First Place', 'Player 1', b'ABCDEFGHIJKLMNOP')
