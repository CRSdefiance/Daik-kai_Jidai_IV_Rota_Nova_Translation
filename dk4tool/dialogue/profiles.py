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
    glyph_widths: dict[str, int] = field(default_factory=dict)
    macro_widths: dict[str, int] = field(default_factory=dict)
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
}


def profile_names() -> tuple[str, ...]:
    return tuple(sorted(_PROFILES))


def get_dialogue_profile(name: str) -> DialogueProfile:
    try:
        return _PROFILES[name]
    except KeyError as error:
        raise ValueError(f"unknown dialogue profile: {name}") from error
