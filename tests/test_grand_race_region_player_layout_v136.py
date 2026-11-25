import pytest

from scripts.probe_grand_race_region_player_layout_v136 import check_fit, geometry


def test_longest_region_fits_lower_left_native_label():
    position, frame = geometry('region', 2)
    assert position == (8, 92)
    assert frame == (8, 92, 108, 12)
    assert check_fit('Southeast Asia', position, frame) == 84


def test_player_status_remains_complete_on_one_line():
    position, frame = geometry('player', 3)
    assert position == (80, 160)
    assert frame is None
    assert check_fit('You are Player 4.', position, frame) == 102


def test_role_text_is_inside_the_inset_frame():
    position, frame = geometry('role', 1)
    assert position == (32, 64)
    assert frame == (24, 56, 124, 28)
    assert check_fit('Join', position, frame) == 24


def test_native_region_frame_overflow_cannot_pass_screen_only_check():
    with pytest.raises(ValueError, match='native frame'):
        check_fit('A' * 19, *geometry('region', 0))


def test_native_player_status_screen_overflow_rejects():
    with pytest.raises(ValueError, match='screen bounds'):
        check_fit('A' * 30, *geometry('player', 0))


@pytest.mark.parametrize('kind,index', [('region', 4), ('role', 2), ('player', -1)])
def test_invalid_table_index_rejects(kind, index):
    with pytest.raises(ValueError, match='group/index'):
        geometry(kind, index)
