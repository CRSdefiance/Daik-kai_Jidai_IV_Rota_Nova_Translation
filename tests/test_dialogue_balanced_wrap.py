from dataclasses import replace

import pytest

from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.layout import format_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record


@pytest.mark.parametrize("text", [
    "No idea. A Minotaur once lived here. That's all the rumor says.",
    "You remind me of a woman pirate from long ago. She was a fearsome fighter.",
    "Gerhard? Watching the sunset? What's wrong?",
])
def test_planned_wrap_keeps_prose_and_guard_space(text: str) -> None:
    profile = get_dialogue_profile("lil-story-deep-route-v102-live")
    source = b"\x02" + "話".encode("cp932") * 50
    markup = f"{{SPEAKER:02}}{text}{{PAD}}"
    result = encode_fixed_dialogue(source, markup, profile)
    qa = audit_fixed_dialogue_record(source, markup, profile)
    assert not [i for i in qa["issues"] if i["severity"] in {"error", "warning"}]
    assert result.encoded[0] == 2 and result.encoded[1] == ord(text[0])
    assert len(result.encoded) == len(source)
    assert all(w <= profile.window_width_px - 6 for w in qa["line_widths_px"][:-1])
    assert " ".join(qa["visible_lines"]) == text


def test_planned_wrap_preserves_macro_command_and_explicit_layout() -> None:
    profile = get_dialogue_profile("lil-story-deep-route-v102-live")
    source = b"\x02FI" + "話".encode("cp932") * 50
    target = "{SPEAKER:02}{MACRO:FI}, consider this tale of old heroes. A curious story reached us today.{PAD}"
    result = encode_fixed_dialogue(source, target, profile)
    assert result.encoded[:3] == b"\x02FI"
    assert result.encoded.count(b"FI") == 1
    assert [(t.kind, t.value) for t in parse_markup(result.formatted_markup) if t.kind in {"speaker", "macro"}] == [("speaker", "02"), ("macro", "FI")]
    explicit = "{SPEAKER:02}Yes.{LB}No.{PAD}"
    assert format_markup(explicit, profile) == format_markup(explicit, replace(profile, balanced_wrapping=False))
    assert not get_dialogue_profile("lil-story-deep-route-v101-live").balanced_wrapping
