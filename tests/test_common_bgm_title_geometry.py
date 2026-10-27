import pytest

from scripts.audit_common_bgm_titles import title_geometry


def test_complete_village_title_exposes_both_panel_overflows():
    result = title_geometry('Southeast Asian Village')
    assert result['width_pixels'] == 138
    assert result['left'] == -5 and result['right'] == 133
    assert not result['fits_panel']


def test_last_fitting_byte_count_and_first_overflow_are_distinct():
    assert title_geometry('A' * 21)['fits_panel']
    assert not title_geometry('A' * 22)['fits_panel']


@pytest.mark.parametrize('title', ['Ｆeelings', 'Title\nnext', 'Title\x00', ''])
def test_unmapped_double_byte_glyphs_and_layout_bytes_are_rejected(title):
    with pytest.raises((ValueError, UnicodeEncodeError)):
        title_geometry(title)
