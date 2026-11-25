from itertools import combinations

import pytest

from dk4tool.dialogue.common_portrait_reflow import WEAK_ENDINGS, compile_paragraph


def legal_partitions(text):
    words = text.split()
    for rows in range(1, 5):
        for cuts in combinations(range(1, len(words)), rows - 1):
            points = (0, *cuts, len(words))
            lines = [' '.join(words[a:b]) for a, b in zip(points, points[1:])]
            if any(len(s) > (35 if i == rows - 1 else 34) for i, s in enumerate(lines)):
                continue
            if any(s.split()[-1].strip('.,!?;:').lower() in WEAK_ENDINGS for s in lines[:-1]):
                continue
            if rows > 1 and len(lines[-1]) <= 8:
                continue
            yield lines


@pytest.mark.parametrize('text', [
    "You're a sailor, aren't you? For bulk trade, try the trade house.",
    "Oh, I know! I'll write you a letter of introduction to thank you for selling us those popular goods.",
    "The economy's been so bad lately, doing business is a real struggle.",
    'Any excess water will be dumped. Is that okay?',
    'A little advice.',
])
def test_full_width_plan_matches_independent_partition_search(text):
    raw, lines = compile_paragraph(text + '{PAD}')
    score = lambda ls: (len(ls), tuple(34 - len(s) for s in ls[:-1]))
    assert score(lines) == min(map(score, legal_partitions(text)))
    assert b' '.join(raw.split()).decode('ascii') == text
    assert raw.startswith(b'  ')
    # Every nonfinal row consumes an even ASCII count before the LF; guards
    # start the following row at the same native pair phase.
    assert all(len(s) % 2 == 0 for s in raw.split(b'\n')[:-1])


def test_shopkeeper_question_remains_whole_without_widening_native_budget():
    _, lines = compile_paragraph("You're a sailor, aren't you? For bulk trade, try the trade house.")
    assert lines == ["You're a sailor, aren't you?", 'For bulk trade, try', 'the trade house.']
    assert not any(len(s) > 35 for s in lines)


@pytest.mark.parametrize('text', [
    '', ' leading', 'two  spaces', 'Authored\nbreak', 'Macro {MACRO:FI}',
    'Width %s', 'Literal FI pair', 'Non-ASCII café', 'x' * 36,
    ' '.join(['unbreakableword'] * 12),
])
def test_unknown_controls_and_unfit_text_fail_closed(text):
    with pytest.raises(ValueError):
        compile_paragraph(text)
