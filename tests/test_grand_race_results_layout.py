import pytest

from scripts.probe_grand_race_results_layout import fit_lines


def test_complete_continue_prompt_fits_original_two_rows():
    english = 'Touch the lower screen or press the A Button.'
    assert fit_lines(english, 2, 48, 160) == [
        'Touch the lower screen', 'or press the A Button.']


@pytest.mark.parametrize('money', ['5,000', '2,000', '1,000', '500'])
def test_complete_prize_sentence_fits_original_position(money):
    english = f'You won {money} in prize money.'
    assert fit_lines(english, 1, 80, 160) == [english]


@pytest.mark.parametrize('english,count,x,y', [
    ('A' * 35, 1, 48, 144),  # Within generic 40 cells, outside this widget.
    ('Touch the lower screen or press the A Button.', 2, 48, 166),
    ('Text', 1, -1, 16),
])
def test_actual_native_bounds_fail_instead_of_clipping(english, count, x, y):
    with pytest.raises(ValueError, match='native widget bounds'):
        fit_lines(english, count, x, y)
