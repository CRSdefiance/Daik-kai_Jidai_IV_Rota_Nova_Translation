import pytest

from scripts.probe_grand_race_wireless_return import balanced_lines


def test_original_two_widgets_cannot_fit_complete_host_selection_prompt():
    english = 'The host is choosing the race area. Please wait until the selection is confirmed.'
    with pytest.raises(ValueError, match='does not fit 2'):
        balanced_lines(english, 2)
    # A third line preserves all the text and fits the actual 40-cell width.
    lines = balanced_lines(english, 3)
    assert ' '.join(lines) == english
    assert all(16 + len(line) * 6 <= 256 for line in lines)


def test_return_prompt_preserves_all_controls_and_complete_menu_destination():
    english = 'Touch the lower screen or press the A Button to return to the menu.'
    lines = balanced_lines(english, 3)
    assert ' '.join(lines) == english
    assert lines[0].startswith('Touch') and lines[-1].endswith('menu.')
    assert sum(len(line.encode('ascii')) + 1 for line in lines) == 68
    assert not any('\n' in line or '\r' in line for line in lines)


@pytest.mark.parametrize('english', ['', ' Text', 'Text ', 'Text  text', 'Text\ntext', 'Text\x1bA'])
def test_authored_spacing_controls_and_empty_native_lines_fail_closed(english):
    with pytest.raises(ValueError, match='one printable ASCII paragraph'):
        balanced_lines(english, 3)
