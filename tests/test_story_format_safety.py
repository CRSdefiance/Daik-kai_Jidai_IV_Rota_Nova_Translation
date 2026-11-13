import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety import story_percent_findings


def archive(text):
    return IlnkContainer([text.encode('cp932') + b'\0']).to_bytes()


@pytest.mark.parametrize('target,command', [
    ('They agreed to 3% of sales.', '% o'),
    ('A 1% share buys little.', '% s'),
    ('We are 50% done.', '% d'),
    ('We are 100% sure.', '% s'),
])
def test_valid_printf_syntax_can_still_introduce_an_unprovided_argument(target, command):
    findings = story_percent_findings(archive('売上の３％です'), archive(target))
    assert len(findings) == 1
    assert findings[0]['current_percent_commands'] == [command]
    assert findings[0]['source_percent_commands'] == []
    assert not findings[0]['invalid_offsets']


def test_actual_source_format_arguments_remain_supported():
    assert not story_percent_findings(archive('%sは%d隻です'), archive('%s owns %d ships.'))


def test_argument_type_and_order_cannot_be_changed():
    assert story_percent_findings(archive('%sは%d隻です'), archive('%d ships belong to %s.'))


def test_word_percent_does_not_create_a_native_command():
    assert not story_percent_findings(archive('売上の３％です'), archive('They agreed to 3 percent of sales.'))


def test_source_leading_percent_is_a_preserved_state_only_at_byte_zero():
    assert not story_percent_findings(archive('%こんにちは'), archive('%Greetings, Admiral.'))
    findings = story_percent_findings(archive('%こんにちは'), archive('%Take 3% of sales.'))
    assert len(findings) == 1 and findings[0]['source_leading25_preserved']
    assert findings[0]['current_percent_commands'] == ['% o']


def test_a_new_leading_percent_is_not_a_speaker_exception():
    assert story_percent_findings(archive('こんにちは'), archive('%Greetings, Admiral.'))


def test_dangling_percent_and_unsupported_commands_are_blocked():
    assert story_percent_findings(archive('比率です'), archive('The ratio is 50%'))
    assert story_percent_findings(archive('こんにちは'), archive('Take %q of it.'))
