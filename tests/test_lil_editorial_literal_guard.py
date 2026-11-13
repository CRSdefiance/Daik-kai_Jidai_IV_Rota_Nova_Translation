from dataclasses import replace
from pathlib import Path

import pytest

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.layout import format_markup, lint_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile


def profile():
    return get_dialogue_profile("lil-opening-editorial-native-v1")


def test_historical_profiles_still_reject_literal_i_and_f():
    old = get_dialogue_profile("lil-story-b22-intro-probe")
    assert old.literal_prefix_policy == "forbid" and not old.balanced_wrapping
    with pytest.raises(ValueError, match="unsafe-literal-macro"):
        encode_relocatable_dialogue(b"\x02", "{SPEAKER:02}I'm Fernando.", old)


@pytest.mark.parametrize("text", ["I", "I'm ready.", "I will go.", "Fernando?", "It's fine."])
def test_native_guard_profile_preserves_ordinary_english(text):
    result = encode_relocatable_dialogue(b"\x02", "{SPEAKER:02}" + text, profile())
    assert result.encoded == b"\x02" + text.encode("ascii")


@pytest.mark.parametrize("text", ["FIRE", "FAME", "FOG", "FUEL", "ICARUS", "I！"])
def test_native_macro_collisions_still_fail(text):
    with pytest.raises(ValueError, match="unsafe-literal-macro"):
        encode_relocatable_dialogue(b"\x02", "{SPEAKER:02}" + text, profile())


def test_genuine_macro_is_preserved_and_missing_macro_is_rejected():
    result = encode_relocatable_dialogue(b"\x02FI", "{SPEAKER:02}{MACRO:FI}! I'm ready.", profile())
    assert result.encoded == b"\x02FI! I'm ready."
    with pytest.raises(ValueError, match="missing-macro"):
        encode_relocatable_dialogue(b"\x02FI", "{SPEAKER:02}Lil! I'm ready.", profile())


def test_explicit_i_before_newline_is_unsafe_even_with_native_guard():
    issues = lint_dialogue(b"\x02", "{SPEAKER:02}I{LB}will go.", profile())
    assert any(i.code == "unsafe-literal-macro" and i.severity == "error" for i in issues)


def test_automatic_wrap_preserves_literal_i_without_exposing_i_lf():
    narrow = replace(profile(), window_width_px=72, max_lines=8)
    text = "One day I will return with a fortune."
    markup = format_markup("{SPEAKER:02}" + text, narrow)
    assert "I{LB}" not in markup and markup.replace("{SPEAKER:02}", "").replace("{LB}", " ") == text
    result = encode_relocatable_dialogue(b"\x02", "{SPEAKER:02}" + text, narrow)
    assert b"I\n" not in result.encoded


def test_direct_playable_batch_cannot_opt_in_without_runtime_bound_post_layer():
    from scripts.build_integrated_release import validate_playable_dialogue_header

    header = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
              "encoder": "dialogue-relocatable-v1", "dialogue_profile": profile().name}
    with pytest.raises(ValueError, match="proven runtime hash"):
        validate_playable_dialogue_header(Path("unbound.json"), header)
