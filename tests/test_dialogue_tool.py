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
from dk4tool.dialogue.layout import format_markup, lint_dialogue
from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import DialogueProfile, get_dialogue_profile
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


def test_guarded_aligned_linebreak_matches_native_compatibility_rule():
    tokens = parse_markup("A{LB@5}B{END}{PAD}")
    assert tokens_to_bytes(tokens, guard_linebreaks=True) == b"A   \x0A B\x00"


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


def test_dialogue_cli_commands_are_registered(tmp_path: Path):
    parsed = parser().parse_args(
        ["preview-dialogue", "script.csv", "--record", "ROW", "--out", str(tmp_path / "x.png")]
    )
    assert parsed.command == "preview-dialogue"
    assert parsed.profile == "story"
