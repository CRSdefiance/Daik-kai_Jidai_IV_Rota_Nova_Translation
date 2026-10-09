import pytest

from dk4tool.dialogue.grand_race_help import format_page, model_native_ascii


def test_complete_paragraph_uses_safe_pairs_at_every_break():
    english = 'The first player must pass every checkpoint. The race continues until all players finish. ' * 2
    english = english.strip()
    _, raw, lines, _ = format_page(english)
    assert ' '.join(lines) == english
    phase = 0
    for index, byte in enumerate(raw):
        if byte == 10:
            assert phase == 1
            assert raw[index + 1] == 32
        else:
            phase ^= 1


def test_native_pair_model_exposes_unguarded_cross_line_character():
    draws = model_native_ascii(b'A\nBC')
    assert ('B', 6, 12) in draws
    assert ('B', 0, 24) not in draws


def test_native_pair_model_exposes_unsafe_guard_phase():
    draws = model_native_ascii(b'AB\n CD')
    assert ('C', 6, 24) in draws
    assert ('D', 6, 24) in draws


def test_safe_guard_flushes_previous_line_and_preserves_next_start():
    draws = model_native_ascii(b'ABC\n DE')
    assert ('C', 12, 12) in draws
    assert ('D', 0, 24) in draws
    assert ('E', 6, 24) in draws


def test_page_overflow_is_rejected_without_shortening():
    with pytest.raises(ValueError):
        format_page('Every checkpoint is required. ' * 25)


def test_authored_layout_is_rejected():
    with pytest.raises(ValueError, match='one paragraph'):
        format_page('Keep\nall instructions.')
