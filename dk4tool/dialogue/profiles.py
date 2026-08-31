from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DialogueProfile:
    name: str
    window_width_px: int
    max_lines: int
    default_ascii_width: int = 6
    default_multibyte_width: int = 12
    line_height_px: int = 16
    guard_linebreaks: bool = True
    pair_phase_safe_breaks: bool = False
    glyph_widths: dict[str, int] = field(default_factory=dict)
    macro_widths: dict[str, int] = field(default_factory=dict)
    # Runtime macro expansions participate in the progressive ASCII pair
    # renderer.  Width alone cannot prove byte parity, so profiles that enable
    # pair-phase repair must declare the exact expansion length explicitly.
    macro_ascii_lengths: dict[str, int] = field(default_factory=dict)
    # Some SC0 speakers use printable single-byte values as a leading runtime
    # state. Keep these route-specific so ordinary ASCII never becomes a
    # control globally.
    leading_speaker_bytes: frozenset[int] = field(default_factory=frozenset)
    metrics_source: str = "provisional screenshot-derived estimate"

    def glyph_width(self, character: str) -> int:
        if character in self.glyph_widths:
            return self.glyph_widths[character]
        return self.default_ascii_width if ord(character) < 0x80 else self.default_multibyte_width

    def macro_width(self, name: str) -> int:
        return self.macro_widths.get(name, 72)


_PROFILES = {
    "story": DialogueProfile(
        name="story",
        window_width_px=216,
        max_lines=4,
        macro_widths={"FI": 72, "FA": 72, "FO": 96, "I": 12},
        metrics_source=(
            "ARM9 renderer trace: 6 px ASCII, 12 px Shift-JIS; "
            "216 px story window from cold-boot 38/39-cell probe"
        ),
    ),
    "story-clean-revoked": DialogueProfile(
        name="story-clean-revoked",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=False,
        macro_widths={"FI": 72, "FA": 72, "FO": 96, "I": 12},
        metrics_source=(
            "ARM9 standard-dialogue parser trace: byte 0A calls the newline helper, "
            "advances only past 0A, and resumes at the first visible character; "
            "216 px story window from cold-boot 38/39-cell probe"
        ),
    ),
    "raphael-story-live": DialogueProfile(
        name="raphael-story-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        # Default route values rendered by FI/FA/FO. Route-aware widths avoid
        # the generic 12-cell worst-case estimate that caused premature wraps.
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        # SC0 B48: 0x4B consistently prefixes Hans; 0x71 consistently
        # prefixes the dock worker. Both precede CP932 prose and were already
        # preserved by the legacy fixed-size batch.
        leading_speaker_bytes=frozenset({0x4B, 0x71}),
        metrics_source=(
            "cold-boot 2026-08-10: bare 0A exposes the following glyph before "
            "the line transition; 0A 20 protects it; default Raphael route "
            "macro widths are 7/6/10 fixed-width ASCII cells"
        ),
    ),
    "hodram-story-probe": DialogueProfile(
        name="hodram-story-probe",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        # SC1's route-specific macro lengths remain deliberately absent. Any
        # future FI/FA/FO record therefore fails closed during pair-phase repair.
        macro_widths={},
        macro_ascii_lengths={},
        # Static source/context correlation identifies these as one-byte
        # presentation states in Hodram's opening. The profile remains a probe
        # until the user confirms their portrait/nameplate effects at runtime.
        leading_speaker_bytes=frozenset({0x10, 0x12, 0x17, 0xFE}),
        metrics_source=(
            "SC1 Hodram opening source correlation plus the accepted shared "
            "progressive-story protected-break and pair-phase behavior; "
            "portrait/nameplate effects await cold-boot confirmation"
        ),
    ),
    "help": DialogueProfile(
        name="help",
        window_width_px=232,
        max_lines=6,
        macro_widths={"FI": 72, "FA": 72, "FO": 96, "I": 12},
        metrics_source=(
            "ARM9 renderer trace: 6 px ASCII, 12 px Shift-JIS; "
            "232 px help-window estimate pending a dedicated live probe"
        ),
    ),
    "shared": DialogueProfile(
        name="shared",
        window_width_px=216,
        max_lines=4,
        macro_widths={"FI": 72, "FA": 72, "FO": 96, "I": 12},
        metrics_source=(
            "ARM9 renderer trace: 6 px ASCII, 12 px Shift-JIS; "
            "216 px shared window from live Market Info 38-cell probe"
        ),
    ),
    "shared-pair-live": DialogueProfile(
        name="shared-pair-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        metrics_source=(
            "Shared 216 px Market Info calibration plus the accepted progressive "
            "ASCII pair-phase renderer; used by source-locked Trader prompts"
        ),
    ),
}


def profile_names() -> tuple[str, ...]:
    return tuple(sorted(_PROFILES))


def get_dialogue_profile(name: str) -> DialogueProfile:
    try:
        return _PROFILES[name]
    except KeyError as error:
        raise ValueError(f"unknown dialogue profile: {name}") from error
