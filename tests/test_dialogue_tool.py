from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from dk4tool.cli import parser
from dk4tool.dialogue.codec import (
    parse_markup,
    tokenize_raw,
    tokens_to_bytes,
    tokens_to_markup,
)
from dk4tool.dialogue.encoder import DialogueEncodingError, encode_fixed_dialogue
from dk4tool.dialogue.layout import format_markup, lint_dialogue
from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import DialogueProfile, get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.dialogue.report import inspect_ilnk_dialogue
from dk4tool.formats.ilnk import IlnkContainer


def narrow_profile(*, max_lines: int = 4) -> DialogueProfile:
    return DialogueProfile(
        name="test",
        window_width_px=22,
        max_lines=max_lines,
        default_ascii_width=6,
        glyph_widths={" ": 4},
        macro_widths={"FI": 12, "I": 6},
    )


def test_raw_tokenization_is_byte_exact_with_macros_and_unknown_controls():
    raw = "船".encode("cp932") + b"\x0AFI I\x02"
    tokens = tokenize_raw(raw)
    markup = tokens_to_markup(tokens)

    assert markup == "船{LB}{MACRO:FI} {MACRO:I}{HEX:02}"
    assert tokens_to_bytes(tokens) == raw
    assert tokens_to_bytes(parse_markup(markup)) == raw


def test_leading_speaker_slot_is_explicit_and_legacy_hex_is_compatible():
    raw = b"\x05" + "話".encode("cp932")
    markup = tokens_to_markup(tokenize_raw(raw))
    assert markup == "{SPEAKER:05}話"
    assert tokens_to_bytes(parse_markup(markup)) == raw
    assert tokens_to_bytes(parse_markup("{HEX:05}話")) == raw


def test_leading_linebreak_is_not_misclassified_as_a_speaker_slot():
    assert tokens_to_markup(tokenize_raw(b"\x0A\x0Aship")) == "{LB}{LB}ship"


def test_route_profile_can_map_printable_leading_speaker_state():
    assert tokens_to_markup(tokenize_raw(b"KHans")) == "KHans"
    assert (
        tokens_to_markup(
            tokenize_raw(b"KHans", leading_speaker_bytes=frozenset({0x4B}))
        )
        == "{SPEAKER:4B}Hans"
    )


def test_raphael_profile_preserves_hans_leading_state():
    result = encode_fixed_dialogue(
        b"KHans speaks",
        "{SPEAKER:4B}Hans speaks{PAD}",
        get_dialogue_profile("raphael-story-live"),
    )

    assert result.encoded == b"KHans speaks"


def test_guarded_aligned_linebreak_matches_native_compatibility_rule():
    tokens = parse_markup("A{LB@5}B{END}{PAD}")
    assert tokens_to_bytes(tokens, guard_linebreaks=True) == b"A   \x0A B\x00"


def test_consecutive_linebreaks_use_one_guard_before_visible_text():
    tokens = parse_markup("{LB}{LB}A ship{PAD}")
    wide = DialogueProfile(name="wide", window_width_px=216, max_lines=4)
    assert format_markup("{LB}{LB}A ship{PAD}", wide) == "{LB}{LB}A ship{PAD}"
    assert tokens_to_bytes(tokens, guard_linebreaks=True) == b"\x0A\x0A A ship"


def test_unknown_markup_is_rejected():
    with pytest.raises(ValueError, match="unknown dialogue token"):
        parse_markup("Hello {WAIT:2}")


def test_pixel_wrapper_breaks_at_words_without_trailing_space():
    assert format_markup("one two", narrow_profile()) == "one{LB}two"


def test_linter_blocks_unknown_source_control_and_missing_linebreak():
    issues = lint_dialogue(b"A\x02\x0AB", "a{HEX:02}b", narrow_profile())
    codes = {issue.code for issue in issues}
    assert "unknown-control" in codes
    assert "line-break-count" in codes


def test_linter_requires_explicit_macro_and_flags_literal_macro_bytes():
    issues = lint_dialogue(b"FI", "First", narrow_profile())
    codes = {issue.code for issue in issues}
    assert "missing-macro" in codes
    assert "unsafe-literal-macro" in codes


def test_linter_rejects_an_added_runtime_command():
    issues = lint_dialogue(b"hello", "hello{MACRO:FA}", narrow_profile())
    assert "unexpected-macro" in {issue.code for issue in issues}


def test_fixed_encoder_preserves_commands_and_exact_allocation():
    source = b"\x05hello there       "
    result = encode_fixed_dialogue(
        source,
        "{SPEAKER:05}hello{PAD}",
        DialogueProfile(name="wide", window_width_px=216, max_lines=4),
    )

    assert result.encoded == b"\x05hello".ljust(len(source), b" ")
    assert len(result.encoded) == len(source)
    assert result.padding_bytes == len(source) - len(b"\x05hello")


def test_fixed_encoder_requires_padding_and_rejects_unsafe_literal_macro():
    profile = DialogueProfile(name="wide", window_width_px=216, max_lines=4)
    with pytest.raises(DialogueEncodingError, match=r"include \{PAD\}"):
        encode_fixed_dialogue(b"hello", "hello", profile)
    with pytest.raises(DialogueEncodingError, match="unsafe-literal-macro"):
        encode_fixed_dialogue(b"abcdef", "Fine{PAD}", profile)


def test_fixed_encoder_wraps_with_guarded_linebreaks():
    source = b"one two    "
    result = encode_fixed_dialogue(source, "one two{PAD}", narrow_profile())
    assert result.formatted_markup == "one{LB}two{PAD}"
    assert result.encoded.startswith(b"one\x0A two")


def test_guarded_continuation_line_reserves_sacrificial_space():
    profile = DialogueProfile(
        name="guarded",
        window_width_px=24,
        max_lines=4,
        default_ascii_width=6,
        guard_linebreaks=True,
    )

    # The first line can use four cells. A continuation line has only three
    # visible cells because the encoded guard space consumes the first cell.
    assert format_markup("aaaa bbbb", profile) == "aaaa{LB}bbb{LB}b"


def test_revoked_story_clean_profile_documents_failed_bare_newline_probe():
    profile = get_dialogue_profile("story-clean-revoked")
    result = encode_fixed_dialogue(
        b"one two" + b" " * 9,
        "one{LB}two{PAD}",
        profile,
    )

    assert result.encoded.startswith(b"one\x0Atwo")
    assert b"\x0A " not in result.encoded


def test_raphael_live_profile_guards_every_visible_continuation():
    profile = get_dialogue_profile("raphael-story-live")
    result = encode_fixed_dialogue(
        b"one two three" + b" " * 12,
        "one{LB}two{LB}three{PAD}",
        profile,
    )

    assert result.encoded.startswith(b"one\x0A two\x0A three")
    for index, byte in enumerate(result.encoded[:-1]):
        if byte == 0x0A:
            assert result.encoded[index + 1] == 0x20


def test_raphael_live_profile_uses_default_route_macro_widths():
    profile = get_dialogue_profile("raphael-story-live")

    assert profile.macro_width("FI") == 7 * 6
    assert profile.macro_width("FA") == 6 * 6
    assert profile.macro_width("FO") == 10 * 6


def test_fixed_encoder_rejects_padding_that_creates_blank_page():
    profile = DialogueProfile(name="tiny", window_width_px=12, max_lines=2)
    source = b"a\nb" + b" " * 7
    with pytest.raises(DialogueEncodingError, match="padding-page-overflow"):
        encode_fixed_dialogue(source, "a{LB}b{PAD}", profile)


def test_linter_reports_pixel_and_byte_overflow():
    issues = lint_dialogue(b"abc", "abcde", narrow_profile(), max_bytes=3)
    codes = {issue.code for issue in issues}
    assert "line-overflow" in codes
    assert "byte-overflow" in codes


def test_ilnk_inspection_includes_every_nonempty_record():
    data = IlnkContainer([b"abc\0FI\x0Adef\0", "日本".encode("cp932") + b"\0"]).to_bytes()
    report = inspect_ilnk_dialogue(data, "/COMMON/MESFILE.DK4")
    assert report["record_count"] == 3
    assert report["control_safe_record_count"] == 3
    assert report["macro_counts"] == {"FI": 1}
    assert report["records"][1]["markup"] == "{MACRO:FI}{LB}def"


def test_preview_writes_a_valid_png(tmp_path: Path):
    destination = tmp_path / "preview.png"
    render_dialogue_preview("one{LB}two", get_dialogue_profile("story"), destination)
    with Image.open(destination) as image:
        assert image.format == "PNG"
        assert image.width > 0
        assert image.height > 0


def test_preview_can_use_extracted_game_ascii_font(tmp_path: Path):
    from dk4tool.dialogue.font_audit import ASCII_FONT_OFFSET

    arm9 = bytearray(ASCII_FONT_OFFSET + 95 * 11)
    arm9[ASCII_FONT_OFFSET] = 0x80
    destination = tmp_path / "game-font-preview.png"
    render_dialogue_preview(
        "!", get_dialogue_profile("story"), destination, arm9=bytes(arm9)
    )
    assert destination.exists()


def test_story_profile_uses_live_calibrated_36_cell_width():
    profile = get_dialogue_profile("story")

    assert profile.window_width_px == 216
    assert format_markup("a" * 36, profile) == "a" * 36
    assert format_markup("a" * 37, profile) == "a" * 36 + "{LB}a"


def test_shared_profile_uses_live_calibrated_36_cell_width():
    profile = get_dialogue_profile("shared")

    assert profile.window_width_px == 216
    assert format_markup("a" * 36, profile) == "a" * 36
    assert format_markup("a" * 37, profile) == "a" * 36 + "{LB}a"


def test_formatter_reflows_the_reported_janus_choice_without_manual_breaks():
    text = "Will Julio show you the ropes, or will you prepare on your own?{PAD}"
    formatted = format_markup(text, get_dialogue_profile("story"))

    assert formatted == (
        "Will Julio show you the ropes, or{LB}will you prepare on your own?{PAD}"
    )


def test_dialogue_qa_flags_author_supplied_breaks_and_orphans():
    report = audit_fixed_dialogue_record(
        b"A" * 64,
        "A natural sentence.{LB}End.{PAD}",
        get_dialogue_profile("story"),
    )
    codes = {issue["code"] for issue in report["issues"]}

    assert "manual-break" in codes
    assert "orphan-final-line" in codes


def test_dialogue_cli_commands_are_registered(tmp_path: Path):
    parsed = parser().parse_args(
        ["preview-dialogue", "script.csv", "--record", "ROW", "--out", str(tmp_path / "x.png")]
    )
    assert parsed.command == "preview-dialogue"
    assert parsed.profile == "story"
