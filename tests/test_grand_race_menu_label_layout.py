import pytest

from scripts.probe_grand_race_menu_label_layout import label_geometry


def test_odd_difference_is_centered_by_pixels_without_added_spaces():
    geometry = label_geometry('Basic Rules', 14)
    assert geometry['x'] == 9  # three spare cells, split into two nine-pixel margins
    assert geometry['width'] == 84 and geometry['height'] == 20
    assert geometry['y'] == 4 and geometry['text_width'] == 66


@pytest.mark.parametrize('text', ['Text\ntext', 'Text\rtext', 'Text\0text', 'A' * 49])
def test_controls_and_labels_exceeding_native_copy_capacity_are_rejected(text):
    with pytest.raises(ValueError, match='complete printable'):
        label_geometry(text, 60)


def test_too_small_context_requires_larger_allocation_not_truncated_english():
    with pytest.raises(ValueError, match='Full English overflows'):
        label_geometry('Read the Rules', 8)
