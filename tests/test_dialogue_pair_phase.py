from __future__ import annotations

import pytest

from dk4tool.dialogue.codec import PairPhaseError, parse_markup, tokens_to_bytes
from dk4tool.dialogue.encoder import (
    DialogueEncodingError,
    encode_fixed_dialogue,
    encode_relocatable_dialogue,
)
from dk4tool.dialogue.profiles import DialogueProfile, get_dialogue_profile


def phase_profile(*, macro_lengths: dict[str, int] | None = None) -> DialogueProfile:
    return DialogueProfile(
        name="pair-phase-test",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_ascii_lengths=macro_lengths or {},
    )


def encode(markup: str, *, profile: DialogueProfile | None = None) -> bytes:
    selected = profile or phase_profile()
    return tokens_to_bytes(
        parse_markup(markup),
        guard_linebreaks=selected.guard_linebreaks,
        pair_phase_safe_breaks=selected.pair_phase_safe_breaks,
        macro_ascii_lengths=selected.macro_ascii_lengths,
    )


def test_odd_ascii_phase_does_not_get_pre_lf_space() -> None:
    assert encode("A{LB}B") == b"A\x0A B"


def test_even_ascii_phase_gets_internal_pre_lf_space() -> None:
    assert encode("AA{LB}B") == b"AA \x0A B"


def test_multiple_breaks_track_progressive_pair_phase_across_record() -> None:
    assert encode("A{LB}BC{LB}D") == b"A\x0A BC \x0A D"


def test_controls_and_multibyte_text_do_not_change_ascii_phase() -> None:
    markup = "{SPEAKER:05}{HEX:02}A\u8a71{LB}B"
    assert encode(markup) == b"\x05\x02A" + "\u8a71".encode("cp932") + b"\x0A B"


def test_known_runtime_macro_expansion_parity_is_counted() -> None:
    profile = phase_profile(macro_lengths={"FI": 7, "FA": 6})
    assert encode("{MACRO:FI}{LB}A", profile=profile) == b"FI\x0A A"
    assert encode("{MACRO:FA}{LB}A", profile=profile) == b"FA \x0A A"


def test_unknown_runtime_macro_parity_fails_closed_at_break() -> None:
    with pytest.raises(PairPhaseError, match="unknown expansion parity"):
        encode("{MACRO:I}{LB}A")


def test_pair_phase_mode_requires_protected_breaks() -> None:
    with pytest.raises(PairPhaseError, match="require protected"):
        tokens_to_bytes(
            parse_markup("A{LB}B"),
            pair_phase_safe_breaks=True,
        )


def test_positioned_break_fails_closed_in_pair_phase_mode() -> None:
    with pytest.raises(PairPhaseError, match="positioned"):
        encode("A{LB@5}B")


def test_b44_r0071_formats_to_the_cold_booted_pair_safe_bytes() -> None:
    source = bytes.fromhex(
        "05834B8389834E835E93AF915282CC9470914482F088F882AB8EE682C182C4"
        "0A89B482C6835783468369835882C58F43979D82B582BD82F182BE82BA"
    )
    result = encode_fixed_dialogue(
        source,
        "{SPEAKER:05}She was a wreck when we got her. "
        "Janus helped repair her.{PAD}",
        get_dialogue_profile("raphael-story-live"),
    )

    assert result.formatted_markup == (
        "{SPEAKER:05}She was a wreck when we got her.{LB}"
        "Janus helped repair her.{PAD}"
    )
    assert result.encoded == (
        b"\x05She was a wreck when we got her. \x0A Janus helped repair her."
    )
    assert result.padding_bytes == 0


def test_phase_repair_consumes_allocation_and_reports_capacity_failure() -> None:
    with pytest.raises(DialogueEncodingError, match="byte-overflow"):
        encode_fixed_dialogue(
            b"AA\x0A B",
            "AA{LB}B{PAD}",
            phase_profile(),
        )


def test_phase_space_is_not_exposed_in_translator_markup() -> None:
    result = encode_fixed_dialogue(
        b"AA \x0A B",
        "AA{LB}B{PAD}",
        phase_profile(),
    )
    assert result.formatted_markup == "AA{LB}B{PAD}"
    assert result.encoded == b"AA \x0A B"


def test_full_first_line_before_pair_phase_break_fails_closed() -> None:
    source = b" " * 80
    with pytest.raises(DialogueEncodingError, match="pair-phase-auto-wrap"):
        encode_fixed_dialogue(
            source,
            "A" * 36 + " next{PAD}",
            phase_profile(),
        )


def test_relocatable_dialogue_can_exceed_source_allocation() -> None:
    profile = get_dialogue_profile("raphael-story-live")
    source = b"\x05short"
    target = "{SPEAKER:05}This is a complete, naturally written sentence."

    encoded = encode_relocatable_dialogue(source, target, profile)

    assert len(encoded.encoded) > len(source)
    assert encoded.encoded.replace(b"\n ", b" ").endswith(
        b"This is a complete, naturally written sentence."
    )


def test_relocatable_dialogue_rejects_fixed_padding() -> None:
    profile = get_dialogue_profile("raphael-story-live")
    with pytest.raises(DialogueEncodingError, match="must not request"):
        encode_relocatable_dialogue(
            b"\x05short", "{SPEAKER:05}Longer text.{PAD}", profile
        )
