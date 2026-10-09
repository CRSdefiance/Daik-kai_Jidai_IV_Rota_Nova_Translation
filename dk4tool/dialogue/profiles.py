from __future__ import annotations

from dataclasses import dataclass, field, replace


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
    balanced_wrapping: bool = False
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
        # prefixes the dock worker. SC0 B51 uses 0x18 for Serah. Printable
        # states used by later scenes live in a separate profile so accepted
        # English beginning with those ASCII bytes cannot be misclassified.
        leading_speaker_bytes=frozenset({0x18, 0x4B, 0x71}),
        metrics_source=(
            "cold-boot 2026-08-10: bare 0A exposes the following glyph before "
            "the line transition; 0A 20 protects it; default Raphael route "
            "macro widths are 7/6/10 fixed-width ASCII cells"
        ),
    ),
    "raphael-story-late-live": DialogueProfile(
        name="raphael-story-late-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x14, 0x18, 0x25, 0x27, 0x4B, 0x50, 0x54, 0x71, 0x72, 0x74}
        ),
        metrics_source=(
            "Raphael live story metrics plus source-correlated late-story NPC "
            "presentation states; isolated from accepted relocated English"
        ),
    ),
    "raphael-story-deep-route-live": DialogueProfile(
        name="raphael-story-deep-route-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x14, 0x18, 0x1F, 0x22, 0x25, 0x27, 0x30, 0x4B, 0x50, 0x53, 0x54, 0x68, 0x6A, 0x71, 0x72, 0x74, 0xFE}
        ),
        metrics_source=(
            "Accepted Raphael progressive-story metrics plus source-correlated "
            "Claudio, Arcadius, Charlotte, and Charlotte celebration presentation "
            "states through SC0 block 69, plus Maria Li, East Asian townspeople, "
            "Eirene jealousy, the Seville battle lead-in, and Simon Linares and "
            "Valdes's confrontation through block 75"
        ),
    ),
    "raphael-story-deep-route-v4-live": DialogueProfile(
        name="raphael-story-deep-route-v4-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x14, 0x18, 0x1F, 0x22, 0x25, 0x27, 0x30, 0x4B, 0x50, 0x53, 0x54, 0x68, 0x6A, 0x71, 0x72, 0x74, 0x8B, 0x97, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 76-80, where 0x8B "
            "is the Alexandria priest and 0x97 is the crew cheer presentation state; "
            "these bytes remain excluded from earlier batches where they begin Shift-JIS glyphs"
        ),
    ),
    "raphael-story-deep-route-v5-live": DialogueProfile(
        name="raphael-story-deep-route-v5-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x14, 0x18, 0x1F, 0x22, 0x25, 0x27, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x71, 0x72, 0x74, 0x93, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 81-82, adding "
            "Mivor and bullfight-spectator presentation states without treating "
            "the same printable bytes as controls in earlier Shift-JIS records"
        ),
    ),
    "raphael-story-deep-route-v6-live": DialogueProfile(
        name="raphael-story-deep-route-v6-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x14, 0x18, 0x1F, 0x22, 0x25, 0x27, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x71, 0x72, 0x74, 0x93, 0xA2, 0xA7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 83, adding the "
            "drowning boy and his mother's presentation states to the V5 set"
        ),
    ),
    "raphael-story-deep-route-v7-live": DialogueProfile(
        name="raphael-story-deep-route-v7-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x14, 0x18, 0x1F, 0x22, 0x25, 0x27, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x71, 0x72, 0x74, 0xA2, 0xA7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 84, where 0x10 "
            "is Gerhard's presentation state and 0x93 begins ordinary Shift-JIS "
            "choice text rather than a bullfight spectator state"
        ),
    ),
    "raphael-story-deep-route-v8-live": DialogueProfile(
        name="raphael-story-deep-route-v8-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x18, 0x1F, 0x22, 0x25, 0x27, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6D, 0x71, 0x72, 0x74, 0x97, 0xA2, 0xA7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 85-86, adding "
            "Charles, the Caribbean townsman, and returning-crew presentation states"
        ),
    ),
    "raphael-story-deep-route-v9-live": DialogueProfile(
        name="raphael-story-deep-route-v9-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6D, 0x71, 0x72, 0x74, 0x97, 0x9E, 0xA2, 0xA7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 87-88, adding "
            "Julian, Kurushima, and Kurushima-henchman presentation states"
        ),
    ),
    "raphael-story-deep-route-v10-live": DialogueProfile(
        name="raphael-story-deep-route-v10-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x97, 0x9E, 0xA2, 0xA7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 90-92, adding "
            "the tomato grower's presentation state"
        ),
    ),
    "raphael-story-deep-route-v12-live": DialogueProfile(
        name="raphael-story-deep-route-v12-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x97, 0x9E, 0xA2, 0xA7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 100-105, adding "
            "the treasure-rumor crewmate presentation state 0x16"
        ),
    ),
    "raphael-story-deep-route-v13-live": DialogueProfile(
        name="raphael-story-deep-route-v13-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x8B, 0x97, 0x9E, 0xA2, 0xA7, 0xBC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 108-110, adding "
            "the priest and churchwoman presentation states 0x8B and 0xBC"
        ),
    ),
    "raphael-story-deep-route-v14-live": DialogueProfile(
        name="raphael-story-deep-route-v14-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x8B, 0x97, 0x9E, 0xA2, 0xA7, 0xBC, 0xBF, 0xD0, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 111-113, adding "
            "the cathedral guide and formal crew presentation states 0xBF and 0xD0"
        ),
    ),
    "raphael-story-deep-route-v15-live": DialogueProfile(
        name="raphael-story-deep-route-v15-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x8B, 0x97, 0x9E, 0xA2, 0xA7, 0xB1, 0xB2, 0xBC, 0xBF, 0xCF, 0xD0, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 114-115, adding "
            "the Sphinx-failure and megalith-cult presentation states 0xCF, 0xB1, and 0xB2"
        ),
    ),
    "raphael-story-deep-route-v16-live": DialogueProfile(
        name="raphael-story-deep-route-v16-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA7, 0xB1, 0xB2, 0xBC, 0xBF, 0xCF, 0xD0, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 116-117, adding "
            "the Angkor guardian and hidden Christian presentation states 0x87 and 0xA0"
        ),
    ),
    "raphael-story-deep-route-v18a-live": DialogueProfile(
        name="raphael-story-deep-route-v18a-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xBC, 0xBF, 0xCF, 0xD0, 0xD6, 0xD7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 119 and 121; "
            "0x89 remains a Shift-JIS choice lead in the urn puzzle"
        ),
    ),
    "raphael-story-deep-route-v18-live": DialogueProfile(
        name="raphael-story-deep-route-v18-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x89, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xBC, 0xBF, 0xCF, 0xD0, 0xD6, 0xD7, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 119-121, adding "
            "the Yuan elder, sandbar grandfather, child, and alternate-rescuer states"
        ),
    ),
    "raphael-story-deep-route-v19-live": DialogueProfile(
        name="raphael-story-deep-route-v19-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x89, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 122 and 124-126, "
            "adding jade scholar, gift guide, figurehead observer, and tribal guide states"
        ),
    ),
    "raphael-story-deep-route-v20-live": DialogueProfile(
        name="raphael-story-deep-route-v20-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x89, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 123, adding "
            "the African bandit presentation state 0xB4"
        ),
    ),
    "raphael-story-deep-route-v22-live": DialogueProfile(
        name="raphael-story-deep-route-v22-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x31, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x89, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 blocks 132-134, adding "
            "battle ally and Spanish fleet presentation states 0x19, 0x31, and 0x3B"
        ),
    ),
    "raphael-story-deep-route-v24-live": DialogueProfile(
        name="raphael-story-deep-route-v24-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1F, 0x22, 0x25, 0x27, 0x29, 0x30, 0x31, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x87, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 136; 0x89 "
            "is a Shift-JIS lead in Raphael's Staff of Guidance question"
        ),
    ),
    "raphael-story-deep-route-v26-live": DialogueProfile(
        name="raphael-story-deep-route-v26-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x30, 0x31, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x8B, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 143, adding "
            "palace guard, Charlie, Albuquerque, and Silveira states plus the "
            "FU full-name runtime command; 0x89 remains an ordinary Shift-JIS lead"
        ),
    ),
    "raphael-story-deep-route-v30-live": DialogueProfile(
        name="raphael-story-deep-route-v30-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x30, 0x31, 0x36, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 147, adding "
            "Uddin's Basra guild attendant state 0x36 while preserving FU support; "
            "0x8B is a Shift-JIS lead in Raphael's pact response"
        ),
    ),
    "raphael-story-deep-route-v31-live": DialogueProfile(
        name="raphael-story-deep-route-v31-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x30, 0x31, 0x36, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics validated through SC0 block 148, "
            "preserving Uddin and attendant states plus all four identity commands"
        ),
    ),
    "raphael-story-deep-route-v33-live": DialogueProfile(
        name="raphael-story-deep-route-v33-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x30, 0x31, 0x36, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x8E, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 150, adding the "
            "relic scholar state 0x8E while preserving four identity commands"
        ),
    ),
    "raphael-story-deep-route-v37-live": DialogueProfile(
        name="raphael-story-deep-route-v37-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x30, 0x31, 0x36, 0x3B, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x8E, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 154, adding "
            "the New World local-resident state 0x5C"
        ),
    ),
    "raphael-story-deep-route-v38-live": DialogueProfile(
        name="raphael-story-deep-route-v38-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x8E, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 155, adding "
            "Escante agent state 0x3C"
        ),
    ),
    "raphael-story-deep-route-v39-live": DialogueProfile(
        name="raphael-story-deep-route-v39-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x87, 0x8E, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated for SC0 block 156, adding "
            "Maldonado state 0x2A"
        ),
    ),
    "raphael-story-deep-route-v42-live": DialogueProfile(
        name="raphael-story-deep-route-v42-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x12, 0x13, 0x14, 0x16, 0x18, 0x19, 0x1A, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael deep-route metrics isolated through SC0 block 165, adding "
            "the Portuguese king state 0x7D"
        ),
    ),
    "raphael-story-deep-route-v44-live": DialogueProfile(
        name="raphael-story-deep-route-v44-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x11, 0x12, 0x13, 0x14, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael ending metrics isolated for SC0 block 166, adding "
            "crew states 0x11, 0x17, and 0x1B"
        ),
    ),
    "raphael-story-deep-route-v46-live": DialogueProfile(
        name="raphael-story-deep-route-v46-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x10, 0x11, 0x12, 0x13, 0x14, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x73, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x94, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael post-ending optional-event metrics through SC0 block 167, "
            "adding Al's employer and attendant states 0x94 and 0x73"
        ),
    ),
    "raphael-story-deep-route-v47-live": DialogueProfile(
        name="raphael-story-deep-route-v47-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x60, 0x68, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x73, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x94, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael optional recruitment metrics through SC0 blocks 168-169, "
            "adding Angelo, Ian, and thug states 0x0F, 0x15, and 0x60"
        ),
    ),
    "raphael-story-deep-route-v48-live": DialogueProfile(
        name="raphael-story-deep-route-v48-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x60, 0x68, 0x69, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x73, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x94, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael optional recruitment metrics through SC0 block 170, "
            "adding Adil's merchant state 0x69"
        ),
    ),
    "raphael-story-deep-route-v50-live": DialogueProfile(
        name="raphael-story-deep-route-v50-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x0B, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x60, 0x68, 0x69, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x73, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x94, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael optional recruitment metrics through SC0 block 176, "
            "adding Jam Jack Ludwyan state 0x0B"
        ),
    ),
    "raphael-story-deep-route-v51-live": DialogueProfile(
        name="raphael-story-deep-route-v51-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 42, "FA": 36, "FO": 60, "FU": 84, "I": 12},
        macro_ascii_lengths={"FI": 7, "FA": 6, "FO": 10, "FU": 14},
        leading_speaker_bytes=frozenset(
            {0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x0B, 0x0D, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x22, 0x23, 0x25, 0x27, 0x29, 0x2A, 0x30, 0x31, 0x36, 0x3B, 0x3C, 0x4B, 0x4F, 0x50, 0x52, 0x53, 0x54, 0x5C, 0x5F, 0x60, 0x68, 0x69, 0x6A, 0x6C, 0x6D, 0x71, 0x72, 0x73, 0x74, 0x78, 0x7D, 0x87, 0x8E, 0x94, 0x97, 0x9E, 0xA0, 0xA2, 0xA3, 0xA7, 0xAA, 0xB1, 0xB2, 0xB3, 0xB4, 0xBC, 0xBF, 0xC6, 0xCF, 0xD0, 0xD1, 0xD6, 0xD7, 0xDC, 0xFE}
        ),
        metrics_source=(
            "Raphael optional recruitment and tutorial metrics through SC0 block 177, "
            "adding Cesare Tohni state 0x0D"
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
    "hodram-story-live": DialogueProfile(
        name="hodram-story-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        # FI/FA/FO expand to the selected captain's first name, surname, and
        # organization.  The accepted ARM9 name table fixes Hodram's defaults
        # to Hodram/Bergstrom/Bergstrom Fleet.
        macro_widths={"FI": 36, "FA": 54, "FO": 90, "I": 12},
        macro_ascii_lengths={"FI": 6, "FA": 9, "FO": 15},
        # SC1 B45-B148 source/context correlation.  Values
        # below 0x10 are recognized globally; these are the additional
        # printable/high-byte portrait, narrator, and NPC presentation states.
        leading_speaker_bytes=frozenset(
            {
                0x10,
                0x11,
                0x12,
                0x13,
                0x14,
                0x16,
                0x17,
                0x18,
                0x1A,
                0x22,
                0x24,
                0x29,
                0x26,
                0x2B,
                0x4F,
                0x52,
                0x54,
                0x3A,
                0x5C,
                0x5F,
                0x68,
                0x6C,
                0x69,
                0x71,
                0x72,
                0x73,
                0x74,
                0x77,
                0x89,
                0x8B,
                0x8D,
                0x93,
                0x97,
                0x9A,
                0x9C,
                0x9E,
                0xA0,
                0xA2,
                0xA3,
                0xA7,
                0xAA,
                0xB3,
                0xB4,
                0xB1,
                0xB2,
                0xBC,
                0xBF,
                0xC6,
                0xCF,
                0xD0,
                0xD1,
                0xD6,
                0xD7,
                0xDC,
                0xFE,
            }
        ),
        metrics_source=(
            "Accepted Hodram progressive-story renderer metrics plus complete "
            "SC1 B45-B148 source-state correlation and accepted "
            "ARM9 Hodram/Bergstrom/Bergstrom Fleet strings"
        ),
    ),
    "hodram-story-proof-live": DialogueProfile(
        name="hodram-story-proof-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 36, "FA": 54, "FO": 90, "I": 12},
        macro_ascii_lengths={"FI": 6, "FA": 9, "FO": 15},
        # Blocks 114-119 share the accepted Hodram renderer but use 0x89 and
        # 0x8D as Shift-JIS lead bytes in ordinary menu text.  Keeping those
        # two values out of this scene-specific state set prevents Push/Right/
        # Left from being mistaken for portrait controls.
        leading_speaker_bytes=frozenset(
            {
                0x10,
                0x11,
                0x12,
                0x14,
                0x16,
                0x17,
                0x18,
                0x1A,
                0x22,
                0x24,
                0x26,
                0x29,
                0x2B,
                0x4F,
                0x52,
                0x54,
                0x5F,
                0x68,
                0x69,
                0x6C,
                0x71,
                0x72,
                0x73,
                0x74,
                0x77,
                0x8B,
                0x93,
                0x97,
                0x9A,
                0x9C,
                0x9E,
                0xA0,
                0xA2,
                0xA7,
                0xB1,
                0xB2,
                0xBC,
                0xBF,
                0xCF,
                0xD0,
                0xFE,
            }
        ),
        metrics_source=(
            "Accepted Hodram story metrics with SC1 B114-B119 scene-specific "
            "state disambiguation for Shift-JIS lead bytes 0x89 and 0x8D"
        ),
    ),
    "lil-story-b23-probe": DialogueProfile(
        name="lil-story-b23-probe",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        # FI/FA/FO select the route protagonist's default first name,
        # surname, and company. Raphael's proven 7/6/10 lengths correspond
        # exactly to Raphael/Castor/Castor Co.; Lil/Argot/Argot Co. therefore
        # supply the route-specific 3/5/9 probe lengths below.
        macro_widths={"FI": 18, "FA": 30, "FO": 54, "I": 12},
        macro_ascii_lengths={"FI": 3, "FA": 5, "FO": 9},
        leading_speaker_bytes=frozenset({0x02, 0x09, 0x14, 0xFE}),
        metrics_source=(
            "SC2 B23 source correlation: 02=Lil, 09=Kamil, 14=Fernando, "
            "FE=tutorial panel; default Lil route macro strings are "
            "Lil/Argot/Argot Co. Runtime confirmation remains required."
        ),
    ),
    "lil-story-b22-first-screen-probe": DialogueProfile(
        name="lil-story-b22-first-screen-probe",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 18, "FA": 30, "FO": 54, "I": 12},
        macro_ascii_lengths={"FI": 3, "FA": 5, "FO": 9},
        leading_speaker_bytes=frozenset({0x02}),
        metrics_source=(
            "SC2 B22 R0019 single-record opening probe; 02=Lil from repeated "
            "B22/B23 source correlation. Uses the accepted progressive-story "
            "216 px width, guarded breaks, and pair-phase behavior."
        ),
    ),
    "lil-story-b22-intro-probe": DialogueProfile(
        name="lil-story-b22-intro-probe",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 18, "FA": 30, "FO": 54, "I": 12},
        macro_ascii_lengths={"FI": 3, "FA": 5, "FO": 9},
        leading_speaker_bytes=frozenset({0x02, 0x09, 0x0E, 0x14}),
        metrics_source=(
            "SC2 B22 source/context correlation: 02=Lil, 09=Kamil, "
            "0E=Emilio, 14=Fernando. Uses the accepted progressive-story "
            "216 px width, guarded breaks, and pair-phase behavior."
        ),
    ),
    "lil-story-deep-route-live": DialogueProfile(
        name="lil-story-deep-route-live",
        window_width_px=216,
        max_lines=4,
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
        macro_widths={"FI": 18, "FA": 30, "FO": 54, "I": 12},
        macro_ascii_lengths={"FI": 3, "FA": 5, "FO": 9},
        leading_speaker_bytes=frozenset(
            {
                0x01,
                0x02,
                0x06,
                0x07,
                0x09,
                0x0B,
                0x0D,
                0x0C,
                0x0E,
                0x0F,
                0x10,
                0x11,
                0x12,
                0x13,
                0x14,
                0x15,
                0x16,
                0x17,
                0x19,
                0x1A,
                0x1B,
                0x1C,
                0x1F,
                0x22,
                0x24,
                0x28,
                0x29,
                0x2B,
                0x38,
                0x40,
                0x41,
                0x43,
                0x44,
                0x46,
                0x4C,
                0x4F,
                0x54,
                0x6C,
                0x6D,
                0x71,
                0x72,
                0x97,
                0x99,
                0x9E,
                0xA2,
                0xA7,
                0xAB,
                0xB7,
                0xB8,
                0xB9,
                0xFE,
            }
        ),
        metrics_source=(
            "Accepted Lil story metrics plus SC2 B0-B37 Muramasa, Barbarossa, "
            "Aziza, bounty, Escante, Deck tutorial, harbor encounter, Clifford alliance, "
            "Valdes campaign, regional warnings, Espinosa and Sofala arcs, defeat, victory, "
            "Manuel-poem correlation, Kamil's sea-governance discussion, and Lelystad "
            "polder-founder scenes, raw-goods tutorials, Mediterranean returns, "
            "Batavia alliance scenes, Kamil's departure, Kuhn's private revelation, "
            "Li-family warnings and assassination, Maria's challenge, Kuhn's murder plot "
            "and war declaration, Li rewards, Clifford's summons, and Escante planning "
            "through SC2 B60, plus Clifford's proof theft, every stolen-item alert, "
            "Escante's defeat rewards, the New World proof-map ritual, and both branches "
            "of Kuhn's defeat, Kamil's Marinus identity and childhood, his return with "
            "Hodram, family reconciliation, Clifford's reward branches, Lil and Kamil's "
            "Amsterdam homecoming, confession, wedding, Kuhn's blessing, and the completed "
            "Lelystad polder through SC2 B70, plus the Ian jealousy scene and Christina's "
            "London recruitment and Mivor's harbor rescue through B73, plus Gerhard "
            "Adernkatz's recruitment and naval-combat tutorial in B74, Janus Pasha and "
            "Charles Jean Rochefort's recruitment events in B75-B76, and Yukihisa's "
            "recruitment, the Silla Gold Crown rivalry, and Julian's family history "
            "through B79, plus the B83 tomato-grower presentation state and "
            "B81-B96 treasure and character scenes, Cesare's B164 ship tutorial, "
            "Manuel's B166 room tutorial, and the B167 sail and wind lesson"
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

_PROFILES["lil-story-deep-route-v25-live"] = replace(
    _PROFILES["lil-story-deep-route-live"],
    name="lil-story-deep-route-v25-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-live"].leading_speaker_bytes
        | frozenset({0x8B, 0xBC, 0xBF, 0xD0})
    ),
    metrics_source=(
        "Accepted Lil renderer metrics plus source-identical SC0/SC1/SC3 evidence "
        "for B100-B104 churchwoman, priest, cathedral guide, and crew states; "
        "runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v26-live"] = replace(
    _PROFILES["lil-story-deep-route-v25-live"],
    name="lil-story-deep-route-v26-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v25-live"].leading_speaker_bytes
        | frozenset({0xCF})
    ),
    metrics_source=(
        "Lil V25 metrics plus source-identical SC0/SC1/SC3 B105 Sphinx-riddle "
        "evidence for CF party-reaction state; 8E/82/92 choice starts are text. "
        "Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v27-live"] = replace(
    _PROFILES["lil-story-deep-route-v26-live"],
    name="lil-story-deep-route-v27-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v26-live"].leading_speaker_bytes
        | frozenset({0xA0, 0xB1, 0xB2})
    ),
    metrics_source=(
        "Lil V26 metrics plus source-identical SC0/SC1 evidence for B106 "
        "megalith cult B1/B2 and B108 hidden believer A0; B106 A0 is the "
        "village speaker. 82/89/92 beginnings remain Shift-JIS text. "
        "Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v30-live"] = replace(
    _PROFILES["lil-story-deep-route-v27-live"],
    name="lil-story-deep-route-v30-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v27-live"].leading_speaker_bytes
        | frozenset({0x89})
    ),
    metrics_source=(
        "Lil V27 metrics plus B111 clean-source byte mapping for the monk's 89 "
        "presentation state. The same byte begins ordinary Shift-JIS text in "
        "other blocks; this mapping applies only to batches selecting V30. "
        "Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v31-live"] = replace(
    _PROFILES["lil-story-deep-route-v30-live"],
    name="lil-story-deep-route-v31-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v30-live"].leading_speaker_bytes
        | frozenset({0xA3, 0xAA, 0xD6, 0xD7})
    ),
    metrics_source=(
        "Lil V30 metrics plus clean-source and source-identical SC0/SC1/SC3 "
        "B112 rescue-scene mapping for A3 child, AA grandfather, D6 lookout, "
        "and D7 rescuer. The 81/82/8E/94 starts are ordinary Shift-JIS text. "
        "Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v32-live"] = replace(
    _PROFILES["lil-story-deep-route-v31-live"],
    name="lil-story-deep-route-v32-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v31-live"].leading_speaker_bytes
        | frozenset({0x68})
    ),
    metrics_source=(
        "Lil V31 metrics plus clean B114 cacao-follow-up source mapping for "
        "the townsman's 68 presentation state. B113 82/92 starts remain "
        "ordinary text, and its 13 scholar state is already mapped. "
        "Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v33-live"] = replace(
    _PROFILES["lil-story-deep-route-v32-live"],
    name="lil-story-deep-route-v33-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v32-live"].leading_speaker_bytes
        | frozenset({0x03, 0x04, 0xB4})
    ),
    metrics_source=(
        "Lil V32 metrics plus source-identical SC0/SC1/SC3 B115 evidence for "
        "03 Maria, 04 Janus, and B4 raider. B115 R0089 starts with staging LF, "
        "not a speaker; 82/92 starts are ordinary text. FO retains Lil's "
        "route-level expansion parity. Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v34-live"] = replace(
    _PROFILES["lil-story-deep-route-v33-live"],
    name="lil-story-deep-route-v34-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v33-live"].leading_speaker_bytes
        | frozenset({0xC6, 0xD1, 0xDC, 0xB3})
    ),
    metrics_source=(
        "Lil V33 metrics plus source-identical SC0/SC1/SC3 evidence for "
        "B116 C6 gift recipient, B117 DC figurehead observer, and B118 B3 "
        "tribal representative, and D1 selected companion; "
        "82/91 starts are ordinary text. Runtime confirmation remains pending"
    ),
)

_PROFILES["lil-story-deep-route-v41-live"] = replace(
    _PROFILES["lil-story-deep-route-v34-live"],
    name="lil-story-deep-route-v41-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v34-live"].leading_speaker_bytes
        | frozenset({0x1D, 0x5C, 0x5F})
    ),
    metrics_source=(
        "Lil B127 source-correlated 5F losing gambler and 5C barkeep; "
        "B128 source-correlated 1D Martin Speyer. Existing 97 selector "
        "marks an admiral-addressing crew voice in B128."
    ),
)

_PROFILES["lil-story-deep-route-v45-live"] = replace(
    _PROFILES["lil-story-deep-route-v41-live"],
    name="lil-story-deep-route-v45-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v41-live"].leading_speaker_bytes
        - frozenset({0x46})
    ),
    metrics_source=(
        "Lil B133 R0022 begins with the FO faction macro (bytes 46 4F), "
        "then the FI name macro. Source 46 is not a speaker state in this batch; "
        "82/83/8E/8F/96 starts are visible text."
    ),
)

_PROFILES["lil-story-deep-route-v46-live"] = replace(
    _PROFILES["lil-story-deep-route-v45-live"],
    name="lil-story-deep-route-v46-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v45-live"].leading_speaker_bytes
        | frozenset({0x23, 0x2F, 0x60})
    ),
    metrics_source=(
        "Lil B134 source-correlated 23 Silveira presentation state; "
        "B135 source-correlated 60 desperate buyer and 2F Espinosa guard. "
        "24 is the inherited Espinosa state; 95/8F B134 choice starts are text."
    ),
)

_PROFILES["lil-story-deep-route-v48-live"] = replace(
    _PROFILES["lil-story-deep-route-v46-live"],
    name="lil-story-deep-route-v48-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v46-live"].leading_speaker_bytes
        | frozenset({0x26})
    ),
    metrics_source=(
        "Lil B137 source-correlated 26 Nagalpur presentation state. "
        "Inherited 02/09/0E/10/11/14/16/17/5C/C6 states cover Lil, "
        "crew, barkeep and waitress; FI name macros remain intact."
    ),
)

_PROFILES["lil-story-deep-route-v59-live"] = replace(
    _PROFILES["lil-story-deep-route-v48-live"],
    name="lil-story-deep-route-v59-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v48-live"].leading_speaker_bytes
        | frozenset({0x2A})
    ),
    metrics_source=(
        "Lil B151 source-correlated 2A Maldonado presentation state. "
        "The inherited 5C barkeep and crew states remain unchanged; "
        "FI, FA, and FO are name and faction macros."
    ),
)

_PROFILES["lil-story-deep-route-v61-live"] = replace(
    _PROFILES["lil-story-deep-route-v59-live"],
    name="lil-story-deep-route-v61-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v59-live"].leading_speaker_bytes
        | frozenset({0x73, 0x94})
    ),
    metrics_source=(
        "Lil B154 source-correlated 94 employer and 73 attendant presentation states "
        "in Al's recruitment scene; the 95 ten-byte event payload stays excluded."
    ),
)

_PROFILES["lil-story-deep-route-v63-live"] = replace(
    _PROFILES["lil-story-deep-route-v61-live"],
    name="lil-story-deep-route-v63-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v61-live"].leading_speaker_bytes
        | frozenset({0xA4, 0xA5})
    ),
    metrics_source=(
        "Lil B156 source-correlated A4 male and A5 female tavern patron "
        "presentation states in Ian Dukov's recruitment scene."
    ),
)

_PROFILES["lil-story-deep-route-v64-live"] = replace(
    _PROFILES["lil-story-deep-route-v63-live"],
    name="lil-story-deep-route-v64-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v63-live"].leading_speaker_bytes
        | frozenset({0x69, 0x8E})
    ),
    metrics_source=(
        "Lil B157 source-correlated 69 merchant Adil and 8E his wife in "
        "Carlo Sinato's recruitment scene; FE is inherited narration."
    ),
)

_PROFILES["lil-story-deep-route-v67-live"] = replace(
    _PROFILES["lil-story-deep-route-v64-live"],
    name="lil-story-deep-route-v67-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v64-live"].leading_speaker_bytes
        | frozenset({0x74})
    ),
    metrics_source=(
        "Lil B160-B162 source-correlated 74 dockworker in the stolen-ship scene. "
        "The 97 crew messenger state is inherited."
    ),
)

_PROFILES["lil-story-deep-route-v69-live"] = replace(
    _PROFILES["lil-story-deep-route-v67-live"],
    name="lil-story-deep-route-v69-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v67-live"].leading_speaker_bytes
        | frozenset({0x57, 0xA6})
    ),
    metrics_source=(
        "Lil B168 source-correlated 57 townsman and A6 young listener in "
        "Mikhail's recruitment scene. The A5 state is inherited."
    ),
)

_PROFILES["lil-story-deep-route-v72-live"] = replace(
    _PROFILES["lil-story-deep-route-v69-live"],
    name="lil-story-deep-route-v72-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v69-live"].leading_speaker_bytes
        | frozenset({0x51})
    ),
    metrics_source=(
        "Lil B171 source-correlated 51 Sanghyeon dream presentation state. "
        "Lil and Yifa states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v73-live"] = replace(
    _PROFILES["lil-story-deep-route-v72-live"],
    name="lil-story-deep-route-v73-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v72-live"].leading_speaker_bytes
        | frozenset({0xC9})
    ),
    metrics_source=(
        "Lil B172 source-correlated C9 Mihwa presentation state in the "
        "Golden Crown of Silla lead. Julian and Lil states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v74-live"] = replace(
    _PROFILES["lil-story-deep-route-v73-live"],
    name="lil-story-deep-route-v74-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v73-live"].leading_speaker_bytes
        | frozenset({0xCA})
    ),
    metrics_source=(
        "Lil B173 source-correlated CA Seoul tavernkeeper in the Golden "
        "Crown of Silla search. Other B173-B174 states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v75-live"] = replace(
    _PROFILES["lil-story-deep-route-v74-live"],
    name="lil-story-deep-route-v75-live",
    metrics_source=(
        "Lil B175 Aziza pirate confrontation: 02 Lil, 09 Kamil, FE Aziza, "
        "and B7-B9 pirate crew presentation states. Opaque 96 46 CA 80 "
        "event payload is excluded unchanged."
    ),
)

_PROFILES["lil-story-deep-route-v76-live"] = replace(
    _PROFILES["lil-story-deep-route-v75-live"],
    name="lil-story-deep-route-v76-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v75-live"].leading_speaker_bytes
        | frozenset({0xAE, 0xAF})
    ),
    metrics_source=(
        "Lil B176 source-correlated AE merchant patron and AF attendant "
        "in the Seville banana boom; FE market notice is inherited."
    ),
)

_PROFILES["lil-story-deep-route-v77-live"] = replace(
    _PROFILES["lil-story-deep-route-v76-live"],
    name="lil-story-deep-route-v77-live",
    metrics_source=(
        "Lil B177 Genoa tomato boom; AE patron, AF attendant, and FE market "
        "notice presentation states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v78-live"] = replace(
    _PROFILES["lil-story-deep-route-v77-live"],
    name="lil-story-deep-route-v78-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v77-live"].leading_speaker_bytes
        | frozenset({0xA8})
    ),
    metrics_source=(
        "Lil B178 source-correlated A8 third neighbor in the Amsterdam "
        "wheat boom; A6, A7, and FE presentation states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v79-live"] = replace(
    _PROFILES["lil-story-deep-route-v78-live"],
    name="lil-story-deep-route-v79-live",
    metrics_source=(
        "Lil B179 San Jorge wine boom; 60 drinker, 5C barkeep, and FE "
        "market notice presentation states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v80-live"] = replace(
    _PROFILES["lil-story-deep-route-v79-live"],
    name="lil-story-deep-route-v80-live",
    metrics_source=(
        "Lil B180-B182 Lisbon spices, Athens rubies, and London gems "
        "market rumors; A6-A8 women and FE market notice states inherited."
    ),
)

_PROFILES["lil-story-deep-route-v81-live"] = replace(
    _PROFILES["lil-story-deep-route-v80-live"],
    name="lil-story-deep-route-v81-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v80-live"].leading_speaker_bytes
        | frozenset({0x55, 0x6E, 0x84})
    ),
    metrics_source=(
        "Lil B183 Basra painting craze: source-correlated 55 shopkeeper, "
        "6E and 84 collectors. The 99, 94, and FE states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v82-live"] = replace(
    _PROFILES["lil-story-deep-route-v81-live"],
    name="lil-story-deep-route-v82-live",
    metrics_source=(
        "Lil B184-B186 Sofala tea, Stockholm furs, and Alexandria sweets "
        "market scenes; A4, A5, AE, AF, and FE states are inherited."
    ),
)

_PROFILES["lil-story-deep-route-v83-live"] = replace(
    _PROFILES["lil-story-deep-route-v82-live"],
    name="lil-story-deep-route-v83-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v82-live"].leading_speaker_bytes
        | frozenset({0x9B})
    ),
    metrics_source=(
        "Lil B187 Malacca almond-medicine rumor: source-correlated 9B coughing "
        "man, with inherited 57 friend and FE market notice states."
    ),
)

_PROFILES["lil-story-deep-route-v84-live"] = replace(
    _PROFILES["lil-story-deep-route-v83-live"],
    name="lil-story-deep-route-v84-live",
    metrics_source=(
        "Lil B188 Osaka giyaman-glass rumor: source-leading 82 and 96 "
        "are Shift-JIS dialogue text, not presentation states. FE market "
        "notice state is inherited."
    ),
)

_PROFILES["lil-story-deep-route-v85-live"] = replace(
    _PROFILES["lil-story-deep-route-v84-live"],
    name="lil-story-deep-route-v85-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v84-live"].leading_speaker_bytes
        | frozenset({0x52, 0x93})
    ),
    metrics_source=(
        "Lil B189 Hamburg ceramics boom: source-correlated 93/52 collectors "
        "and inherited 68/71 swindlers and FE market notice states."
    ),
)

_PROFILES["lil-story-deep-route-v86-live"] = replace(
    _PROFILES["lil-story-deep-route-v85-live"],
    name="lil-story-deep-route-v86-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v85-live"].leading_speaker_bytes
        | frozenset({0x77, 0x9F})
    ),
    metrics_source=(
        "Lil B190 Havana medicine rumor: source-correlated 9F townsman and "
        "77 friend, with inherited FE market notice state."
    ),
)

_PROFILES["lil-story-deep-route-v87-live"] = replace(
    _PROFILES["lil-story-deep-route-v86-live"],
    name="lil-story-deep-route-v87-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v86-live"].leading_speaker_bytes
        | frozenset({0x56, 0x9A})
    ),
    metrics_source=(
        "Lil B191 Calicut dye rumor: source-correlated 56 father and 9A son, "
        "with inherited FE market notice state."
    ),
)

_PROFILES["lil-story-deep-route-v88-live"] = replace(
    _PROFILES["lil-story-deep-route-v87-live"],
    name="lil-story-deep-route-v88-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v87-live"].leading_speaker_bytes
        | frozenset({0x75, 0x9C})
    ),
    metrics_source=(
        "Lil B192-B194 Istanbul tobacco, Seoul chilies, and Hangzhou sake: "
        "75/9C Hangzhou townsmen added; 99/73, A6/A7/A8, 06 and FE inherited. "
        "B194 companion name macro FI remains live."
    ),
)

_PROFILES["lil-story-deep-route-v89-live"] = replace(
    _PROFILES["lil-story-deep-route-v88-live"],
    name="lil-story-deep-route-v89-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v88-live"].leading_speaker_bytes
        | frozenset({0x67})
    ),
    metrics_source=(
        "Lil B195 Veracruz cheese dish: source-correlated 67 second patron "
        "added; 77 first patron, 5C barkeep, and FE market notice inherited."
    ),
)

_PROFILES["lil-story-deep-route-v90-live"] = replace(
    _PROFILES["lil-story-deep-route-v89-live"],
    name="lil-story-deep-route-v90-live",
    leading_speaker_bytes=(
        (_PROFILES["lil-story-deep-route-v89-live"].leading_speaker_bytes
         - frozenset({0x94}))
        | frozenset({0xAD})
    ),
    metrics_source=(
        "Lil B196 six-stage haggling: AD seller added; 14/13/06/19 crew "
        "and FE notice inherited. Source-leading 94 is Shift-JIS Buy/Pass "
        "choice text here, so it is removed as a presentation state."
    ),
)

_PROFILES["lil-story-deep-route-v91-live"] = replace(
    _PROFILES["lil-story-deep-route-v90-live"],
    name="lil-story-deep-route-v91-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v90-live"].leading_speaker_bytes
        | frozenset({0xA9})
    ),
    metrics_source=(
        "Lil B197 celestial-maiden book: A9 mysterious woman added; 15 Ian "
        "and FE system notice inherited. Choice-leading 94 remains Shift-JIS "
        "text, and the four-byte 21 48 8C A8 event payload is nontext."
    ),
)

_PROFILES["lil-story-deep-route-v94-live"] = replace(
    _PROFILES["lil-story-deep-route-v91-live"],
    name="lil-story-deep-route-v94-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v91-live"].leading_speaker_bytes
        | frozenset({0xAC})
    ),
    metrics_source=(
        "Lil B200 Carlo and collapsed traveler: AC traveler added; "
        "13 Carlo and FE sound/reward notices inherited."
    ),
)

_PROFILES["lil-story-deep-route-v96-live"] = replace(
    _PROFILES["lil-story-deep-route-v94-live"],
    name="lil-story-deep-route-v96-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v94-live"].leading_speaker_bytes
        | frozenset({0x9D})
    ),
    metrics_source=(
        "Lil B202 fleeing stranger and Glassmaking Guide: 9D stranger added; "
        "93 pursuer, 02 Lil, and 12 Charles inherited."
    ),
)

_PROFILES["lil-story-deep-route-v98-live"] = replace(
    _PROFILES["lil-story-deep-route-v96-live"],
    name="lil-story-deep-route-v98-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v96-live"].leading_speaker_bytes
        | frozenset({0x91, 0x7C, 0x82})
    ),
    metrics_source=(
        "Lil B204 shachihoko/figurehead incident: 91 woman, 7C retainer, "
        "and 82 Japanese lord added; 0B Jam, 02 Lil, and FE letter inherited."
    ),
)

_PROFILES["lil-story-deep-route-v100-live"] = replace(
    _PROFILES["lil-story-deep-route-v98-live"],
    name="lil-story-deep-route-v100-live",
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v98-live"].leading_speaker_bytes
        - frozenset({0x82, 0x94, 0x8D})
    ),
    metrics_source=(
        "Lil B206 ceramic-earrings merchant: AD seller, 02 Lil, and 07 Cristina "
        "are presentation states; 82/94/8D begin four bare Shift-JIS choices."
    ),
)

_PROFILES["lil-story-deep-route-v101-live"] = replace(
    _PROFILES["lil-story-deep-route-v100-live"],
    name="lil-story-deep-route-v101-live",
    leading_speaker_bytes=(
        (_PROFILES["lil-story-deep-route-v100-live"].leading_speaker_bytes
         - frozenset({0x82, 0x92, 0x93, 0x8A, 0x8F, 0xE6}))
        | frozenset({0x95})
    ),
    metrics_source=(
        "Lil B207-B214: 95 Three Kingdoms enthusiast added. Alternate letter "
        "reports and five choices begin with Japanese text, including 82/92/93."
    ),
)

_PROFILES["lil-story-deep-route-v102-live"] = replace(
    _PROFILES["lil-story-deep-route-v101-live"],
    name="lil-story-deep-route-v102-live",
    balanced_wrapping=True,
    leading_speaker_bytes=(
        _PROFILES["lil-story-deep-route-v101-live"].leading_speaker_bytes
        | frozenset({0x78, 0xC5, 0xC7})
    ),
    metrics_source=(
        "Lil B215-B226: 78 Solomon legend keeper, C5 Safia, and C7 Lucia added. "
        "Eight choices and alternate letter entries retain bare text starts."
    ),
)

_PROFILES["raphael-story-deep-route-v55-live"] = replace(
    _PROFILES["raphael-story-deep-route-v51-live"],
    name="raphael-story-deep-route-v55-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v51-live"].leading_speaker_bytes
         - frozenset({0x8E, 0x94}))
        | frozenset({0x51, 0xAE, 0xAF, 0xB7, 0xB8, 0xC9, 0xCA})
    ),
    metrics_source=(
        "Raphael optional-event metrics through SC0 block 188, adding "
        "Sanghyeon, Mihwa, tavernkeeper, pirate, and trade-boom states; "
        "ambiguous Shift-JIS 0x8E/0x94 leads remain text in this range"
    ),
)

_PROFILES["raphael-story-deep-route-v56-live"] = replace(
    _PROFILES["raphael-story-deep-route-v55-live"],
    name="raphael-story-deep-route-v56-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v55-live"].leading_speaker_bytes
        | frozenset({0x55, 0x5C, 0x60, 0x6E, 0x84, 0x94, 0x99, 0xA6, 0xA7, 0xA8})
    ),
    metrics_source=(
        "Raphael trade-boom metrics through SC0 block 195, adding verified "
        "merchant, customer, tavern patron, dealer, and companion states"
    ),
)

_PROFILES["raphael-story-deep-route-v57-live"] = replace(
    _PROFILES["raphael-story-deep-route-v56-live"],
    name="raphael-story-deep-route-v57-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v56-live"].leading_speaker_bytes
        | frozenset({0x57, 0x9B, 0xA4, 0xA5})
    ),
    metrics_source=(
        "Raphael trade-boom metrics through SC0 block 199, adding verified "
        "tea, fur, and almond-rumor speaker states"
    ),
)

_PROFILES["raphael-story-deep-route-v58-live"] = replace(
    _PROFILES["raphael-story-deep-route-v57-live"],
    name="raphael-story-deep-route-v58-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v57-live"].leading_speaker_bytes
        | frozenset({0x56, 0x67, 0x75, 0x77, 0x82, 0x93, 0x96, 0x9A, 0x9C, 0x9F})
    ),
    metrics_source=(
        "Raphael trade-boom metrics through SC0 block 207, adding verified "
        "lord, retainer, dyer, townsman, and tavern-patron states"
    ),
)

_PROFILES["raphael-story-deep-route-v59-live"] = replace(
    _PROFILES["raphael-story-deep-route-v58-live"],
    name="raphael-story-deep-route-v59-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v58-live"].leading_speaker_bytes
         - frozenset({0x82, 0x94, 0x96}))
        | frozenset({0x69, 0x8C, 0x9D, 0xA9, 0xAC, 0xAD})
    ),
    metrics_source=(
        "Raphael treasure and stat-event metrics through SC0 block 214; "
        "ambiguous Shift-JIS 0x82/0x94/0x96 leads remain text in this range"
    ),
)

_PROFILES["raphael-story-deep-route-v60-live"] = replace(
    _PROFILES["raphael-story-deep-route-v59-live"],
    name="raphael-story-deep-route-v60-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v59-live"].leading_speaker_bytes
        | frozenset({0x7C, 0x91, 0xAA})
    ),
    metrics_source=(
        "Raphael optional-item metrics through SC0 block 217, adding verified "
        "herbalist, castle-retainer, and towns-woman states"
    ),
)

_PROFILES["raphael-story-deep-route-v61-live"] = replace(
    _PROFILES["raphael-story-deep-route-v60-live"],
    name="raphael-story-deep-route-v61-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v60-live"].leading_speaker_bytes
         - frozenset({0x93}))
        | frozenset({0x95})
    ),
    metrics_source=(
        "Raphael legendary-weapon and correspondence metrics through SC0 "
        "block 227, adding the verified Three Kingdoms enthusiast state and "
        "leaving ambiguous Shift-JIS 0x93 leads as text in the Yukihisa letter"
    ),
)

_PROFILES["raphael-story-deep-route-v62-live"] = replace(
    _PROFILES["raphael-story-deep-route-v61-live"],
    name="raphael-story-deep-route-v62-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v61-live"].leading_speaker_bytes
         - frozenset({0x91, 0x95}))
        | frozenset({0xC5, 0xC7})
    ),
    metrics_source=(
        "Raphael legendary-equipment metrics through SC0 block 243, adding "
        "Lucia and Safia while preserving ambiguous Shift-JIS 0x91/0x95 leads"
    ),
)

_PROFILES["raphael-story-deep-route-v63-live"] = replace(
    _PROFILES["raphael-story-deep-route-v62-live"],
    name="raphael-story-deep-route-v63-live",
    metrics_source=(
        "Raphael legendary-equipment and relic metrics through SC0 block 250"
    ),
)

_PROFILES["raphael-story-deep-route-v64-live"] = replace(
    _PROFILES["raphael-story-deep-route-v63-live"],
    name="raphael-story-deep-route-v64-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v63-live"].leading_speaker_bytes
         - frozenset({0x8C}))
        | frozenset({0x43, 0x8B, 0xBA})
    ),
    metrics_source=(
        "Raphael frozen-rose and supernatural-figurehead metrics through SC0 "
        "block 254, adding the conman, priest, and Francisca states while "
        "preserving ambiguous Shift-JIS 0x8C leads"
    ),
)

_PROFILES["raphael-story-deep-route-v65-live"] = replace(
    _PROFILES["raphael-story-deep-route-v64-live"],
    name="raphael-story-deep-route-v65-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v64-live"].leading_speaker_bytes
         - frozenset({0x97}))
        | frozenset({0xBD, 0xBE, 0xC1, 0xC3, 0xC4, 0xC8})
    ),
    metrics_source=(
        "Raphael local-discovery and supernatural-figurehead metrics through "
        "SC0 block 264, adding verified town-woman states while preserving an "
        "ambiguous Shift-JIS 0x97 lead"
    ),
)

_PROFILES["raphael-story-deep-route-v66-live"] = replace(
    _PROFILES["raphael-story-deep-route-v65-live"],
    name="raphael-story-deep-route-v66-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v65-live"].leading_speaker_bytes
        | frozenset({0x42, 0x44, 0x93, 0x94})
    ),
    metrics_source=(
        "Raphael guild-smuggler contract metrics through SC0 block 270, "
        "adding verified Jean, Jacob, and guildmaster speaker states"
    ),
)

_PROFILES["raphael-story-deep-route-v67-live"] = replace(
    _PROFILES["raphael-story-deep-route-v66-live"],
    name="raphael-story-deep-route-v67-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v66-live"].leading_speaker_bytes
        | frozenset({0x3E, 0x3F, 0x41, 0x45, 0x71, 0x95})
    ),
    metrics_source=(
        "Raphael guild-bounty metrics through SC0 block 285, adding verified "
        "Jacks, Julian, Prett, Peralonso, guild, and messenger states"
    ),
)

_PROFILES["raphael-story-deep-route-v68-live"] = replace(
    _PROFILES["raphael-story-deep-route-v67-live"],
    name="raphael-story-deep-route-v68-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v67-live"].leading_speaker_bytes
        | frozenset({0x46, 0x47})
    ),
    metrics_source=(
        "Raphael late guild-bounty metrics through SC0 block 292, adding "
        "verified Zaganos Bey and William Clive states"
    ),
)

_PROFILES["raphael-story-deep-route-v69-live"] = replace(
    _PROFILES["raphael-story-deep-route-v68-live"],
    name="raphael-story-deep-route-v69-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v68-live"].leading_speaker_bytes
         - frozenset({0x8B, 0x93}))
        | frozenset({0x0E, 0xD3, 0xD8})
    ),
    metrics_source=(
        "Raphael forest-ruin and megalith-cult metrics through SC0 block 293, "
        "adding verified companion states while preserving ambiguous Shift-JIS "
        "0x8B/0x93 leads"
    ),
)

_PROFILES["raphael-story-deep-route-v70-live"] = replace(
    _PROFILES["raphael-story-deep-route-v69-live"],
    name="raphael-story-deep-route-v70-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v69-live"].leading_speaker_bytes
         - frozenset({0x94}))
        | frozenset({0x93})
    ),
    metrics_source=(
        "Raphael Stone Circle investigation and equinox-riddle metrics through "
        "SC0 block 296, restoring the verified guildmaster state while "
        "preserving an ambiguous Shift-JIS 0x94 lead"
    ),
)

_PROFILES["raphael-story-deep-route-v71-live"] = replace(
    _PROFILES["raphael-story-deep-route-v70-live"],
    name="raphael-story-deep-route-v71-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v70-live"].leading_speaker_bytes
        | frozenset({0xBB})
    ),
    metrics_source=(
        "Raphael Stone Circle discovery and London guild-resolution metrics "
        "through SC0 block 300, adding the verified informant state"
    ),
)

_PROFILES["raphael-story-deep-route-v72-live"] = replace(
    _PROFILES["raphael-story-deep-route-v71-live"],
    name="raphael-story-deep-route-v72-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v71-live"].leading_speaker_bytes
        - frozenset({0x93})
    ),
    metrics_source=(
        "Raphael jungle-cave and tiger encounter metrics through SC0 block 301, "
        "preserving an ambiguous Shift-JIS 0x93 lead"
    ),
)

_PROFILES["raphael-story-deep-route-v73-live"] = replace(
    _PROFILES["raphael-story-deep-route-v72-live"],
    name="raphael-story-deep-route-v73-live",
    metrics_source=(
        "Raphael jungle-rumor, Veda clue, and guardian handoff metrics through "
        "SC0 block 304"
    ),
)

_PROFILES["raphael-story-deep-route-v74-live"] = replace(
    _PROFILES["raphael-story-deep-route-v73-live"],
    name="raphael-story-deep-route-v74-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v73-live"].leading_speaker_bytes
        | frozenset({0x94, 0x97, 0xDE})
    ),
    metrics_source="Raphael hidden-village expedition metrics through SC0 block 305",
)

_PROFILES["raphael-story-deep-route-v75-live"] = replace(
    _PROFILES["raphael-story-deep-route-v74-live"],
    name="raphael-story-deep-route-v75-live",
    metrics_source="Raphael hidden-village medicine quest metrics through SC0 block 306",
)

_PROFILES["raphael-story-deep-route-v76-live"] = replace(
    _PROFILES["raphael-story-deep-route-v75-live"],
    name="raphael-story-deep-route-v76-live",
    metrics_source=(
        "Raphael medicine delivery, ruins guide, cliff route, and forest hazard "
        "metrics through SC0 block 310"
    ),
)

_PROFILES["raphael-story-deep-route-v77-live"] = replace(
    _PROFILES["raphael-story-deep-route-v76-live"],
    name="raphael-story-deep-route-v77-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v76-live"].leading_speaker_bytes
        | frozenset({0xC0})
    ),
    metrics_source="Raphael Colosseum lead and desert expedition metrics through SC0 block 312",
)

_PROFILES["raphael-story-deep-route-v78-live"] = replace(
    _PROFILES["raphael-story-deep-route-v77-live"],
    name="raphael-story-deep-route-v78-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v77-live"].leading_speaker_bytes
        | frozenset({0x61})
    ),
    metrics_source=(
        "Raphael dancer-earring payoff and mosque explorer-rescue setup metrics "
        "through SC0 block 315"
    ),
)

_PROFILES["raphael-story-deep-route-v79-live"] = replace(
    _PROFILES["raphael-story-deep-route-v78-live"],
    name="raphael-story-deep-route-v79-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v78-live"].leading_speaker_bytes
         - frozenset({0x95}))
        | frozenset({0xB6})
    ),
    metrics_source=(
        "Raphael cursed-explorer rescue and Arabian Nights ritual metrics "
        "through SC0 block 319; 0x95 is restored as a Shift-JIS lead in this range"
    ),
)

_PROFILES["raphael-story-deep-route-v80-live"] = replace(
    _PROFILES["raphael-story-deep-route-v79-live"],
    name="raphael-story-deep-route-v80-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v79-live"].leading_speaker_bytes
         - frozenset({0x94}))
        | frozenset({0xCB})
    ),
    metrics_source=(
        "Raphael guided-route and shortcut expedition metrics through SC0 block 320; "
        "0x94 is restored as a Shift-JIS lead in this range"
    ),
)

_PROFILES["raphael-story-deep-route-v81-live"] = replace(
    _PROFILES["raphael-story-deep-route-v80-live"],
    name="raphael-story-deep-route-v81-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v80-live"].leading_speaker_bytes
        | frozenset({0x5E, 0x66})
    ),
    metrics_source=(
        "Raphael foreign-story, chintz, wine, Kyoto lead, and Proof-map guardian "
        "reminder metrics through SC0 block 324"
    ),
)

_PROFILES["raphael-story-deep-route-v82-live"] = replace(
    _PROFILES["raphael-story-deep-route-v81-live"],
    name="raphael-story-deep-route-v82-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v81-live"].leading_speaker_bytes
        | frozenset({0xDA})
    ),
    metrics_source=(
        "Raphael forest navigation, wolf encounter, injury, treatment, and village "
        "arrival metrics through SC0 block 325"
    ),
)

_PROFILES["raphael-story-deep-route-v83-live"] = replace(
    _PROFILES["raphael-story-deep-route-v82-live"],
    name="raphael-story-deep-route-v83-live",
    leading_speaker_bytes=(
        (_PROFILES["raphael-story-deep-route-v82-live"].leading_speaker_bytes
         - frozenset({0x9F}))
        | frozenset({0xC9, 0xCD})
    ),
    metrics_source=(
        "Raphael secluded-city gate tip, dark-forest and vampire-bat expedition, "
        "and ancient-map rumor metrics through SC0 block 328; 0x9F is restored "
        "as a Shift-JIS lead in this range"
    ),
)

_PROFILES["raphael-story-deep-route-v84-live"] = replace(
    _PROFILES["raphael-story-deep-route-v83-live"],
    name="raphael-story-deep-route-v84-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v83-live"].leading_speaker_bytes
        | frozenset({0xCC})
    ),
    metrics_source=(
        "Raphael scorpion-desert expedition, Goryeo incense-burner rumor, pirate "
        "warning, and fortune-teller ruins lead metrics through SC0 block 331"
    ),
)

_PROFILES["raphael-story-deep-route-v85-live"] = replace(
    _PROFILES["raphael-story-deep-route-v84-live"],
    name="raphael-story-deep-route-v85-live",
    metrics_source=(
        "Raphael fog, dead-end, cliff-choice, injury, fatigue, and ruins-arrival "
        "expedition metrics through SC0 block 332"
    ),
)

_PROFILES["raphael-story-deep-route-v86-live"] = replace(
    _PROFILES["raphael-story-deep-route-v85-live"],
    name="raphael-story-deep-route-v86-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v85-live"].leading_speaker_bytes
        | frozenset({0xCE})
    ),
    metrics_source=(
        "Raphael jungle, cave/fire choice, bat fatigue, ancient-city transfer, "
        "ruins arrival, and missing-monk rumor metrics through SC0 block 335"
    ),
)

_PROFILES["raphael-story-deep-route-v87-live"] = replace(
    _PROFILES["raphael-story-deep-route-v86-live"],
    name="raphael-story-deep-route-v87-live",
    metrics_source=(
        "Raphael warrior trial, Tlaloc's Knife training, Ancient City Map lead, "
        "sextant trade, guarded treasure, and Book of Alchemy quest metrics "
        "through SC0 block 342"
    ),
)

_PROFILES["raphael-story-deep-route-v88-live"] = replace(
    _PROFILES["raphael-story-deep-route-v87-live"],
    name="raphael-story-deep-route-v88-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v87-live"].leading_speaker_bytes
        | frozenset({0x0C, 0x24, 0x28})
    ),
    metrics_source=(
        "Raphael Ruler's Proof progression and major regional-fleet battle "
        "metrics across early SC0 blocks 0-11"
    ),
)

_PROFILES["raphael-story-deep-route-v89-live"] = replace(
    _PROFILES["raphael-story-deep-route-v88-live"],
    name="raphael-story-deep-route-v89-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v88-live"].leading_speaker_bytes
        | frozenset({0x3D, 0xB0, 0xB9})
    ),
    metrics_source=(
        "Raphael pirate, bounty, regional-fleet, Valdes-victory, Gerhard-Vels, "
        "and Manuel sea-elegy metrics across SC0 blocks 12-25"
    ),
)

_PROFILES["raphael-story-deep-route-v90-live"] = replace(
    _PROFILES["raphael-story-deep-route-v89-live"],
    name="raphael-story-deep-route-v90-live",
    metrics_source=(
        "Raphael Aziza mutiny, rescue, backstory, recruitment, repeat encounter, "
        "and pirate-bounty capture metrics across SC0 blocks 26-34"
    ),
)

_PROFILES["raphael-story-deep-route-v91-live"] = replace(
    _PROFILES["raphael-story-deep-route-v90-live"],
    name="raphael-story-deep-route-v91-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v90-live"].leading_speaker_bytes
        - frozenset({0x46})
        | frozenset({0x33})
    ),
    metrics_source=(
        "Raphael first Hayreddin encounter, negotiation, Mediterranean-passage "
        "pact, and conditional anti-Spain protection metrics in SC0 blocks 36-37"
    ),
)

_PROFILES["raphael-story-deep-route-v92-live"] = replace(
    _PROFILES["raphael-story-deep-route-v91-live"],
    name="raphael-story-deep-route-v92-live",
    metrics_source=(
        "Raphael Hayreddin rescue, Amsterdam signal, Ruler's Proof lore, supply, "
        "departure, recruitment, and trade tutorial metrics in SC0 blocks 38-42"
    ),
)

_PROFILES["raphael-story-deep-route-v93-live"] = replace(
    _PROFILES["raphael-story-deep-route-v92-live"],
    name="raphael-story-deep-route-v93-live",
    metrics_source=(
        "Final Raphael Hans notices, royal summons, Silveira betrayal, Proof "
        "handoff, funding, and merchant residual metrics"
    ),
)

# The late Hodram ending/recruitment range introduces printable/high bytes that
# are also valid data bytes in earlier Shift-JIS records. Keep them scoped to
# V9 rather than changing how already accepted route batches are decoded.
_PROFILES["hodram-story-ending-live"] = replace(
    _PROFILES["hodram-story-live"],
    name="hodram-story-ending-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-live"].leading_speaker_bytes
        | frozenset({0x19, 0x4E, 0x78, 0x79, 0x7D, 0x84, 0x94})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B149-B157 "
        "late-route speaker-state correlation"
    ),
)

_PROFILES["hodram-story-recruit-live"] = replace(
    _PROFILES["hodram-story-ending-live"],
    name="hodram-story-recruit-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-ending-live"].leading_speaker_bytes
        | frozenset({0x15, 0x60, 0x8E, 0xA4, 0xA5})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B158-B162 "
        "optional-recruitment speaker-state correlation"
    ),
)

_PROFILES["hodram-story-cesare-live"] = replace(
    _PROFILES["hodram-story-recruit-live"],
    name="hodram-story-cesare-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-recruit-live"].leading_speaker_bytes
        - frozenset({0x89})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus SC1 B163-B168 "
        "Cesare/Elysion correlation with ambiguous Shift-JIS 0x89 retained as text"
    ),
)

_PROFILES["hodram-story-mikhail-live"] = replace(
    _PROFILES["hodram-story-cesare-live"],
    name="hodram-story-mikhail-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-cesare-live"].leading_speaker_bytes | frozenset({0x4C, 0x57, 0x6D, 0xA6}))
        - frozenset({0x8E})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus SC1 B169-B173 "
        "Fernando/Julio/Mikhail speaker-state correlation; 0x8E is retained "
        "as Shift-JIS choice text in this range"
    ),
)

_PROFILES["hodram-story-ifa-live"] = replace(
    _PROFILES["hodram-story-mikhail-live"],
    name="hodram-story-ifa-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-mikhail-live"].leading_speaker_bytes
        | frozenset({0x51, 0x99, 0xB7, 0xC9, 0xCA})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus SC1 B174-B179 "
        "Ifa/Sanghyeon/Julian/Mihwa/pirate speaker-state correlation"
    ),
)

_PROFILES["hodram-story-boom-live"] = replace(
    _PROFILES["hodram-story-ifa-live"],
    name="hodram-story-boom-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-ifa-live"].leading_speaker_bytes
        | frozenset({0x55, 0x56, 0x67, 0x6E, 0x75, 0x82, 0x96, 0x9B, 0x9F, 0xA8, 0xAE, 0xAF})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B180-B199 "
        "trade-boom speaker-state correlation"
    ),
)

_PROFILES["hodram-story-treasure-live"] = replace(
    _PROFILES["hodram-story-boom-live"],
    name="hodram-story-treasure-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-boom-live"].leading_speaker_bytes - frozenset({0x94}))
        | frozenset({0x7C, 0x91, 0x9D, 0xA9, 0xAC, 0xAD})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B200-B209 "
        "treasure/stat-event speaker-state correlation; 0x94 is retained as "
        "Shift-JIS choice text in this range"
    ),
)

_PROFILES["hodram-story-weapon-live"] = replace(
    _PROFILES["hodram-story-treasure-live"],
    name="hodram-story-weapon-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-treasure-live"].leading_speaker_bytes
         - frozenset({0x82, 0x8D, 0x93, 0x94}))
        | frozenset({0x95})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B210-B219 "
        "weapon-rumor and correspondence correlation; 0x82/0x8D/0x93/0x94 "
        "are retained as Shift-JIS text leads in this range"
    ),
)

_PROFILES["hodram-story-legend-live"] = replace(
    _PROFILES["hodram-story-weapon-live"],
    name="hodram-story-legend-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-weapon-live"].leading_speaker_bytes
        | frozenset({0xC5, 0xC7})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B220-B229 "
        "legendary-armor, correspondence, Lucia, and Safia state correlation"
    ),
)

_PROFILES["hodram-story-relic-live"] = replace(
    _PROFILES["hodram-story-legend-live"],
    name="hodram-story-relic-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-legend-live"].leading_speaker_bytes
        | frozenset({0x93, 0xBA, 0xC1, 0xC3, 0xC4})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B240-B249 "
        "relic, church, tavern-hint, and guild-request speaker-state correlation; "
        "0x82 remains a Shift-JIS choice-text lead in this range"
    ),
)

_PROFILES["hodram-story-quest-live"] = replace(
    _PROFILES["hodram-story-relic-live"],
    name="hodram-story-quest-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-relic-live"].leading_speaker_bytes
        | frozenset({0x40, 0xBD, 0xBE, 0xC8})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B250-B251 "
        "and B253-B259 local-hint and guild-quest speaker-state correlation"
    ),
)

_PROFILES["hodram-story-puzzle-live"] = replace(
    _PROFILES["hodram-story-legend-live"],
    name="hodram-story-puzzle-live",
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B252 ruin-puzzle "
        "correlation; 0x82/0x89/0x8A/0x8D/0x90/0x92/0x93 remain Shift-JIS text leads"
    ),
)

_PROFILES["hodram-story-guild-live"] = replace(
    _PROFILES["hodram-story-quest-live"],
    name="hodram-story-guild-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-quest-live"].leading_speaker_bytes
        | frozenset({0x3F, 0x43})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B260-B269 "
        "Gabriel and Julian guild-bounty speaker-state correlation"
    ),
)

_PROFILES["hodram-story-bounty-live"] = replace(
    _PROFILES["hodram-story-guild-live"],
    name="hodram-story-bounty-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-guild-live"].leading_speaker_bytes
        | frozenset({0x41, 0x42, 0x44, 0x94})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B270-B279 "
        "Prett, Ramusio, Portunto, and Berio bounty speaker-state correlation"
    ),
)

_PROFILES["hodram-story-commission-live"] = replace(
    _PROFILES["hodram-story-bounty-live"],
    name="hodram-story-commission-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-bounty-live"].leading_speaker_bytes
        | frozenset({0x47, 0x48})
    ),
    metrics_source=(
        "Accepted Hodram progressive-story metrics plus isolated SC1 B280-B289 "
        "Berio, Swedish royal commission, William, and ancient-city quest correlation"
    ),
)

_PROFILES["hodram-story-jungle-live"] = replace(
    _PROFILES["hodram-story-commission-live"],
    name="hodram-story-jungle-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-commission-live"].leading_speaker_bytes
         - frozenset({0x89, 0x8B, 0x8D, 0x93, 0x97, 0x9F}))
        | frozenset({0xD3, 0xD8})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B290 jungle-expedition correlation; "
        "0x89/0x8B/0x8D/0x93/0x97/0x9F remain Shift-JIS text leads"
    ),
)

_PROFILES["hodram-story-cave-live"] = replace(
    _PROFILES["hodram-story-jungle-live"],
    name="hodram-story-cave-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-jungle-live"].leading_speaker_bytes
        | frozenset({0x97})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B291 cave-expedition correlation; "
        "0x89/0x8B/0x8D/0x93 remain Shift-JIS text leads while 0x97 is a "
        "source-correlated presentation state in this block"
    ),
)

_PROFILES["hodram-story-ruins-live"] = replace(
    _PROFILES["hodram-story-commission-live"],
    name="hodram-story-ruins-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-commission-live"].leading_speaker_bytes
        | frozenset({0xC2, 0xD3})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B292-B299 sea-monster, "
        "hidden-village, ruins, and gunpowder-quest speaker correlation"
    ),
)

_PROFILES["hodram-story-snake-live"] = replace(
    _PROFILES["hodram-story-cave-live"],
    name="hodram-story-snake-live",
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B300 giant-snake and swamp "
        "correlation; 0x93 remains a Shift-JIS choice lead and 0x97 remains "
        "a source-correlated party presentation state"
    ),
)

_PROFILES["hodram-story-colosseum-live"] = replace(
    _PROFILES["hodram-story-commission-live"],
    name="hodram-story-colosseum-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-commission-live"].leading_speaker_bytes
        | frozenset({0xC0})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B301 Colosseum-rumor speaker correlation"
    ),
)

_PROFILES["hodram-story-desert-live"] = replace(
    _PROFILES["hodram-story-cave-live"],
    name="hodram-story-desert-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-cave-live"].leading_speaker_bytes
         - frozenset({0x81, 0x82, 0x8D, 0x8E, 0x8F, 0x90, 0x92, 0x97}))
        | frozenset({0xD0, 0xD3, 0xD6})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B302 desert-expedition correlation; "
        "0x81/0x82/0x8D/0x8E/0x8F/0x90/0x92 are Shift-JIS text leads while "
        "0xD0/0xD3/0xD6 are source-correlated presentation states"
    ),
)

_PROFILES["hodram-story-mosque-live"] = replace(
    _PROFILES["hodram-story-commission-live"],
    name="hodram-story-mosque-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-commission-live"].leading_speaker_bytes
        | frozenset({0xC5})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B303 mosque-treasure speaker correlation"
    ),
)

_PROFILES["hodram-story-proof-live"] = replace(
    _PROFILES["hodram-story-commission-live"],
    name="hodram-story-proof-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-commission-live"].leading_speaker_bytes
         - frozenset({0x91}))
        | frozenset({0xCB})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B304-B308 swamp, Golden Pavilion, "
        "Yuan-relic, and Proof-map speaker correlation; 0x91 remains a Shift-JIS text lead"
    ),
)

_PROFILES["hodram-story-wolf-live"] = replace(
    _PROFILES["hodram-story-cave-live"],
    name="hodram-story-wolf-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-cave-live"].leading_speaker_bytes
         - frozenset({0x91}))
        | frozenset({0xD6, 0xD7, 0xDA})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B309 wolf and forest expedition "
        "correlation; 0x91 remains a Shift-JIS text lead while "
        "0x97/0xD0/0xD3/0xD6/0xD7/0xDA are isolated presentation states"
    ),
)

_PROFILES["hodram-story-eastasia-live"] = replace(
    _PROFILES["hodram-story-wolf-live"],
    name="hodram-story-eastasia-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-wolf-live"].leading_speaker_bytes
         - frozenset({0x96}))
        | frozenset({0xC9, 0xCC, 0xCD, 0xD1})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B310-B314 East Asia city-gate, "
        "forest, ruins, desert, and celadon-rumor speaker correlation; "
        "0x96 remains a Shift-JIS text lead"
    ),
)

_PROFILES["hodram-story-final-expeditions-live"] = replace(
    _PROFILES["hodram-story-eastasia-live"],
    name="hodram-story-final-expeditions-live",
    leading_speaker_bytes=(
        (_PROFILES["hodram-story-eastasia-live"].leading_speaker_bytes
         - frozenset({0x94}))
        | frozenset({0x16, 0xB3, 0xCE, 0xCF})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B315-B319 prophecy, fog, jungle, "
        "ancient-city, and missionary-rumor speaker correlation; "
        "0x94 remains a Shift-JIS text lead"
    ),
)

_PROFILES["hodram-story-final-treasures-live"] = replace(
    _PROFILES["hodram-story-final-expeditions-live"],
    name="hodram-story-final-treasures-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-final-expeditions-live"].leading_speaker_bytes
        | frozenset({0xA1})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B320-B324 sextant exchange, "
        "survey dispatch, treasure handoff, and alchemy-book speaker correlation"
    ),
)

_PROFILES["hodram-story-opening-battles-live"] = replace(
    _PROFILES["hodram-story-final-treasures-live"],
    name="hodram-story-opening-battles-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-final-treasures-live"].leading_speaker_bytes
        | frozenset({0x1B, 0x49, 0xB8, 0xB9})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B0-B12 relic, Aziza fleet, and "
        "early-bounty speaker correlation"
    ),
)

_PROFILES["hodram-story-caribbean-battles-live"] = replace(
    _PROFILES["hodram-story-opening-battles-live"],
    name="hodram-story-caribbean-battles-live",
    leading_speaker_bytes=(
        _PROFILES["hodram-story-opening-battles-live"].leading_speaker_bytes
        | frozenset({0x1D, 0x21, 0x25, 0x28, 0x2A, 0x34, 0x35, 0x37, 0x38, 0x39, 0x3C, 0xD5})
    ),
    metrics_source=(
        "Accepted Hodram story metrics plus SC1 B20-B41 bounty, naval tutorial, "
        "Barbarossa, Maldonado, slave-ship, Lil decoy, Pasha, and sea-monster "
        "speaker correlation"
    ),
)

_PROFILES["raphael-story-deep-route-v39-plain-live"] = replace(
    _PROFILES["raphael-story-deep-route-v39-live"],
    name="raphael-story-deep-route-v39-plain-live",
    leading_speaker_bytes=(
        _PROFILES["raphael-story-deep-route-v39-live"].leading_speaker_bytes
        - frozenset({0x97})
    ),
    metrics_source=(
        "SC0 block 156 plain-text companion profile: 0x97 is the Shift-JIS lead "
        "of 来 in Raphael's final response, not Maldonado's officer state"
    ),
)

_PROFILES["maria-story-shared-events-live"] = DialogueProfile(
    name="maria-story-shared-events-live",
    window_width_px=216,
    max_lines=4,
    guard_linebreaks=True,
    pair_phase_safe_breaks=True,
    macro_widths={"FI": 30, "FA": 18, "FO": 42, "I": 12},
    macro_ascii_lengths={"FI": 5, "FA": 3, "FO": 7},
    leading_speaker_bytes=frozenset(
        {
            0x03,
            0x06,
            0x0E,
            0x13,
            0x14,
            0x15,
            0x16,
            0x19,
            0x1A,
            0xA9,
            0xAD,
            0xC7,
            0xD0,
            0xD3,
            0xD7,
            0xD8,
            0xFE,
        }
    ),
    metrics_source=(
        "SC3 clean-source correlation for Maria Lee's shared optional events: "
        "03=Maria, 06=Xien, 0E/13/14/15/16/19/1A/D0/D3/D7/D8=party-member "
        "variants, A9/AD/C7=event participants, and FE=system narration. Runtime "
        "macros use the accepted "
        "Maria/Lee/Li Clan ARM9 values and the accepted progressive-story renderer."
    ),
)

_PROFILES["maria-story-wolf-event-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-wolf-event-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x97, 0x9C, 0xD6, 0xDA})
    ),
    metrics_source=(
        "SC3 block 281 wolf-event correlation adds route-local party presentation "
        "states 97/9C/D6/DA. They remain isolated from other SC3 blocks because "
        "0x97 is also the valid Shift-JIS lead byte of 勇 in block 252."
    ),
)

_PROFILES["maria-story-jungle-ruins-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-jungle-ruins-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0xB3, 0xCF, 0xD6})
    ),
    metrics_source=(
        "SC3 blocks 292-293 jungle and island-ruins correlation adds route-local "
        "presentation states B3/CF/D6 for the expedition guide and party variants. "
        "These remain isolated from unrelated SC3 blocks to avoid treating valid "
        "Shift-JIS lead bytes as presentation state."
    ),
)

_PROFILES["maria-story-alchemy-event-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-alchemy-event-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x02, 0x12, 0xA1, 0xB3, 0xCF})
    ),
    metrics_source=(
        "SC3 blocks 300-302 sextant, inheritance, and alchemy-book correlation "
        "adds route-local presentation states 02/12/A1/B3/CF. They remain isolated "
        "from unrelated SC3 blocks to protect valid Shift-JIS lead bytes."
    ),
)

_PROFILES["maria-story-tiger-cave-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-tiger-cave-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x97})
    ),
    metrics_source=(
        "SC3 block 259 jungle and tiger-cave correlation adds route-local party "
        "presentation state 97. The source-leading 0A bytes in three records are "
        "newlines rather than speaker states; keeping them out of this set prevents "
        "blank first rows and offset text. The 97 state remains isolated because it "
        "can also be a valid Shift-JIS lead byte in unrelated SC3 text."
    ),
)

_PROFILES["maria-story-dark-forest-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-dark-forest-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0xD6})
    ),
    metrics_source=(
        "SC3 block 283 dark-forest correlation adds the route-local D6 party "
        "presentation state. Binary choice/event controls remain excluded."
    ),
)

_PROFILES["maria-story-art-market-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-art-market-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x55, 0x6E, 0x84, 0x94, 0x99})
    ),
    metrics_source=(
        "SC3 block 156 art-market correlation adds verified dealer, buyer, critic, "
        "and companion presentation states 55/6E/84/94/99. These potentially "
        "ambiguous Shift-JIS bytes remain isolated to the correlated event block."
    ),
)

_PROFILES["maria-story-earrings-event-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-earrings-event-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x07})
    ),
    metrics_source=(
        "SC3 block 179 ceramic-earrings event correlation adds Cristina's 07 "
        "presentation state. Source-leading 82/8D/94 bytes remain Shift-JIS text "
        "leads for choices, preventing first-character loss."
    ),
)

_PROFILES["maria-story-pirate-sword-rumor-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-pirate-sword-rumor-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x07, 0xAA})
    ),
    metrics_source=(
        "SC3 block 181 pirate-sword rumor correlation adds Cristina's 07 and the "
        "old sailor's AA presentation states, isolated from unrelated Shift-JIS."
    ),
)

_PROFILES["maria-story-church-figurehead-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-church-figurehead-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x8B})
    ),
    metrics_source=(
        "SC3 block 215 church-figurehead correlation adds the priest's 8B state. "
        "Choice-leading 82 remains Shift-JIS text, and the isolated 94 event control "
        "is excluded, preventing leading-character loss."
    ),
)

_PROFILES["maria-story-tavern-fraud-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-tavern-fraud-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x43, 0x5C})
    ),
    metrics_source=(
        "SC3 block 213 tavern-fraud correlation adds the conman's 43 and "
        "tavernkeeper's 5C presentation states. The source-leading 0A on Xien's "
        "appraisal remains a line-break byte, not a speaker state."
    ),
)

_PROFILES["maria-story-mikhail-recruitment-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-mikhail-recruitment-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x4C, 0x57, 0xA5, 0xA6})
    ),
    metrics_source=(
        "SC3 block 139 Mikhail recruitment correlation adds Mikhail's 4C, the "
        "townsman's 57, and the two girls' A5/A6 presentation states. Source-leading "
        "0A bytes remain line breaks and are never treated as speaker states."
    ),
)

_PROFILES["maria-story-cheese-boom-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-cheese-boom-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x5C, 0x67, 0x77})
    ),
    metrics_source=(
        "SC3 block 168 Veracruz cheese-boom correlation adds the tavernkeeper's "
        "5C, patron's 67, and townsman's 77 presentation states."
    ),
)

_PROFILES["maria-story-muramasa-letter-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-muramasa-letter-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x0B, 0x0C, 0xD0})
    ),
    metrics_source=(
        "SC3 block 182 Yukihisa correspondence adds Jam's 0B, the letter's 0C, "
        "and the reporting crewmate's D0 presentation states. Source-leading "
        "82/92/93 bytes belong to Shift-JIS alternate companion text and are not states."
    ),
)

_PROFILES["maria-story-ceramics-boom-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-ceramics-boom-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x52, 0x68, 0x71})
    ),
    metrics_source=(
        "SC3 block 162 Hamburg ceramics-boom correlation adds the collector's 52 "
        "and the merchants' 68/71 presentation states. Source-leading 93 bytes are "
        "Shift-JIS text leads and are never treated as presentation states."
    ),
)

_PROFILES["maria-story-shared-rumors-v21-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-shared-rumors-v21-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x0C, 0x0F, 0x52, 0x57, 0x68, 0x71, 0x77, 0xA6, 0xA7, 0xA8})
    ),
    metrics_source=(
        "SC3 blocks 160/163/166/171 correlate market-rumor and namahage states. "
        "Source-leading 93/9B/9F bytes are Shift-JIS text leads, never speaker states."
    ),
)

_PROFILES["maria-story-shared-events-v22-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-shared-events-v22-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset(
            {
                0x56,
                0x75,
                0x82,
                0x96,
                0x9A,
                0x9C,
                0xA4,
                0xA5,
                0xA6,
                0xA7,
                0xA8,
                0xAE,
                0xAF,
            }
        )
    ),
    metrics_source=(
        "SC3 blocks 151/153/154/157/159/161/164/167 correlate eight complete "
        "commodity-rumor events against identical SC0/SC1 records. This confirms "
        "56/75/82/96/9A/9C/A4/A5/A6/A7/A8/AE/AF as block-local presentation "
        "states; 06 and FE remain inherited verified states. The ambiguous high "
        "bytes are deliberately isolated to these blocks so valid Shift-JIS leads "
        "remain visible elsewhere."
    ),
)

_PROFILES["maria-story-shared-events-v23-live"] = replace(
    _PROFILES["maria-story-shared-events-v22-live"],
    name="maria-story-shared-events-v23-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v22-live"].leading_speaker_bytes
        | frozenset({0x44, 0x5C, 0x60, 0x94, 0xC5})
    ),
    metrics_source=(
        "SC3 blocks 150/152/155/158/197/241 correlate complete commodity rumors, "
        "Julian and Safia's Medusa-shield conversation, and the Calicut cargo-thief "
        "reward. Cross-route source equality confirms 44/5C/60/94/C5 as local "
        "presentation states in addition to the V22 set."
    ),
)

_PROFILES["maria-story-shared-events-v24-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-shared-events-v24-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x12, 0x68, 0x69, 0xAC})
    ),
    metrics_source=(
        "SC3 blocks 173/174/207/208/209 correlate Carlo's inn and rope events, "
        "Filippo's Papal States rumor, and the Charles/Jam letters. This confirms "
        "12/68/69/AC as local presentation states. Source-leading 82/92/94 bytes in "
        "letter-delivery and Buy/Pass records remain Shift-JIS text leads."
    ),
)

_PROFILES["maria-story-shared-events-v25-live"] = replace(
    _PROFILES["maria-story-shared-events-live"],
    name="maria-story-shared-events-v25-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-live"].leading_speaker_bytes
        | frozenset({0x07, 0x4C, 0x7C, 0x82, 0x91, 0x95, 0xAA})
    ),
    metrics_source=(
        "SC3 blocks 176-178 and 184-186 correlate six shared optional events, "
        "confirming 07/4C/7C/82/91/95/AA as local presentation states. The "
        "four-byte 414893A8 and 214896A8 records are preserved nontext event payloads; "
        "choice-leading 8A/8F/92/E6 bytes remain Shift-JIS text leads."
    ),
)

_PROFILES["maria-story-shared-events-v26-live"] = replace(
    _PROFILES["maria-story-shared-events-v25-live"],
    name="maria-story-shared-events-v26-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v25-live"].leading_speaker_bytes
        | frozenset({0x0D, 0x10, 0x11, 0x17, 0x42, 0x55, 0x93, 0xBA})
    ),
    metrics_source=(
        "SC3 blocks 194, 198, 206, 210, 214, and 231 correlate six shared "
        "historical, treasure, and recovery events, confirming their local "
        "presentation-state bytes while preserving fixed ILNK allocations."
    ),
)

_PROFILES["maria-story-shared-events-v27-live"] = replace(
    _PROFILES["maria-story-shared-events-v26-live"],
    name="maria-story-shared-events-v27-live",
    leading_speaker_bytes=(
        (_PROFILES["maria-story-shared-events-v26-live"].leading_speaker_bytes
        - frozenset({0x82}))
        | frozenset({0x04, 0x15, 0x5C, 0x71, 0x9A})
    ),
    metrics_source=(
        "SC3 blocks 183, 191, 211, 212, 220, and 230 correlate six shared "
        "weapon, recovery, figurehead, and capture events, confirming their "
        "local presentation states; 82 is removed locally because it is a "
        "Shift-JIS choice-text lead in blocks 212 and 220. The leading 0A in "
        "two block-212 records is retained as a raw leading token followed by "
        "the renderer's mandatory one-byte space guard."
    ),
)

_PROFILES["maria-story-shared-events-v28-live"] = replace(
    _PROFILES["maria-story-shared-events-v27-live"],
    name="maria-story-shared-events-v28-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v27-live"].leading_speaker_bytes
        | frozenset({0x13, 0x16, 0x19, 0x78, 0xD0})
    ),
    metrics_source=(
        "SC3 blocks 187, 188, 195, 196, and 200-204 correlate letter, weapon, "
        "armor, and equipment-rumor events. D0 is a presentation byte in the "
        "first letter-delivery variants; 82/92 remain Shift-JIS text leads in "
        "the alternate delivery lines."
    ),
)

_PROFILES["maria-story-shared-events-v29-live"] = replace(
    _PROFILES["maria-story-shared-events-v28-live"],
    name="maria-story-shared-events-v29-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v28-live"].leading_speaker_bytes
        | frozenset({0x47, 0x48, 0x73, 0x79, 0x93, 0x94, 0x99,
                     0xBC, 0xBD, 0xC1, 0xC3, 0xC4, 0xC8, 0xCF})
    ),
    metrics_source=(
        "SC3 blocks 118, 165, 190, 216-219, 222, 224, 229, 240, 246-247, "
        "249-250, and 253 correlate local rumors, ruin leads, pirate bounties, "
        "rewards, and commodity-boom messages. Cross-route equality and portrait "
        "correlation confirm the added presentation-state bytes in these blocks."
    ),
)

_PROFILES["maria-story-shared-events-v30-live"] = replace(
    _PROFILES["maria-story-shared-events-v29-live"],
    name="maria-story-shared-events-v30-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v29-live"].leading_speaker_bytes
        | frozenset({0x87, 0xA1, 0xB3, 0xCE})
    ),
    metrics_source=(
        "SC3 blocks 294-299 cover late New World rumors, ghost-ship and warrior-ruin "
        "quests, Guam rescue, the New World proof handoff, and sextant trade. "
        "87/A1/B3/CE are block-local presentation states; five source-leading 0A "
        "records retain their intentional opening line break through explicit waivers."
    ),
)

_PROFILES["maria-story-shared-events-v31-live"] = replace(
    _PROFILES["maria-story-shared-events-v30-live"],
    name="maria-story-shared-events-v31-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v30-live"].leading_speaker_bytes
        | frozenset({0xCC})
    ),
    metrics_source=(
        "SC3 blocks 286-290 cover the celadon-burner rumor and the complete San "
        "Jorge anti-bandit supply chain. CC is the local-woman presentation state; "
        "82 and 96 remain valid Shift-JIS leads in two Maria responses."
    ),
)

_PROFILES["maria-story-shared-events-v32-live"] = replace(
    _PROFILES["maria-story-shared-events-v31-live"],
    name="maria-story-shared-events-v32-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v31-live"].leading_speaker_bytes
        | frozenset({0x66, 0xCB})
    ),
    metrics_source=(
        "SC3 block 275 begins the Macao smuggling conspiracy: an injured defector "
        "reveals that false Portuguese missionaries are coming to seek an imperial "
        "audience. Existing 03/66/CB presentation states are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v33-live"] = replace(
    _PROFILES["maria-story-shared-events-v32-live"],
    name="maria-story-shared-events-v33-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v32-live"].leading_speaker_bytes
        | frozenset({0x5D, 0x65})
    ),
    metrics_source=(
        "SC3 block 276 continues the Macao conspiracy at the tavern, where the "
        "defector buys the missionaries' arrival time and port from an informant."
    ),
)

_PROFILES["maria-story-shared-events-v34-live"] = replace(
    _PROFILES["maria-story-shared-events-v33-live"],
    name="maria-story-shared-events-v34-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v33-live"].leading_speaker_bytes
        | frozenset({0x8B})
    ),
    metrics_source=(
        "SC3 block 277 exposes the false Portuguese missionary delegation and "
        "Maria's analysis of the smugglers' scheme. 8B is the missionary state; "
        "three source-leading 0A records retain their intentional opening break."
    ),
)

_PROFILES["maria-story-shared-events-v35-live"] = replace(
    _PROFILES["maria-story-shared-events-v34-live"],
    name="maria-story-shared-events-v35-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v34-live"].leading_speaker_bytes
        | frozenset({0x0B, 0x0C, 0x44, 0x58, 0x7B, 0x81, 0x83})
    ),
    metrics_source=(
        "SC3 block 278 covers the staged governor's-office arrest and the defector "
        "joining Maria. 0B/0C/44/58/7B/81/83 are block-local presentation states; "
        "four source-leading 0A records preserve their opening transition."
    ),
)

_PROFILES["maria-story-shared-events-v36-live"] = replace(
    _PROFILES["maria-story-shared-events-v35-live"],
    name="maria-story-shared-events-v36-live",
    metrics_source=(
        "SC3 blocks 279-280 close the defector episode with the Kyoto map lead and "
        "provide all eight companion variants for the northeastern-China Proof-map reminder. "
        "92 and 82 remain Shift-JIS text leads, not presentation states."
    ),
)

_PROFILES["maria-story-shared-events-v37-live"] = replace(
    _PROFILES["maria-story-shared-events-v36-live"],
    name="maria-story-shared-events-v37-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v36-live"].leading_speaker_bytes
        - frozenset({0x95})
    ),
    metrics_source=(
        "SC3 block 274 covers the Kyoto-map maze, both navigation choices, all companion "
        "variants, and the successful exit. 82/8E/92/95 are block-local Shift-JIS text leads; one "
        "opaque six-byte event payload remains excluded as nontext."
    ),
)

_PROFILES["maria-story-shared-events-v38-live"] = replace(
    _PROFILES["maria-story-shared-events-v37-live"],
    name="maria-story-shared-events-v38-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v37-live"].leading_speaker_bytes
        | frozenset({0x12, 0x6E, 0xC5})
    ),
    metrics_source=(
        "SC3 blocks 270-273 cover the dancer's inland-mosque lead and the complete "
        "carronade-defense research quest, its specialist branches, and guild reward. "
        "12/6E/C5 are confirmed presentation states; 94 remains the guildmaster state."
    ),
)

_PROFILES["maria-story-shared-events-v39-live"] = replace(
    _PROFILES["maria-story-shared-events-v38-live"],
    name="maria-story-shared-events-v39-live",
    metrics_source=(
        "SC3 blocks 254-258 cover the complete London Lime Drops scurvy-cure loan, "
        "one-month reminder and return, monetary/share rewards, and the follow-up ruin lead. "
        "Existing 03/93/FE states and the source-leading 0A companion continuation are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v40-live"] = replace(
    _PROFILES["maria-story-shared-events-v39-live"],
    name="maria-story-shared-events-v40-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v39-live"].leading_speaker_bytes
        | frozenset({0x9C, 0xD6})
    ),
    metrics_source=(
        "SC3 blocks 260-263 cover the Malacca shark-fin commission, alternate delicacy "
        "resolution, rewards, jungle-kingdom rumor, and first ancient-coin discovery. "
        "9C/D6 are companion presentation states; 82/92 are Shift-JIS text leads, and "
        "the four-byte 20469480 scene-entry payload remains nontext."
    ),
)

_PROFILES["maria-story-shared-events-v41-live"] = replace(
    _PROFILES["maria-story-shared-events-v40-live"],
    name="maria-story-shared-events-v41-live",
    leading_speaker_bytes=(
        (_PROFILES["maria-story-shared-events-v40-live"].leading_speaker_bytes
        - frozenset({0x8B}))
        | frozenset({0x5F})
    ),
    metrics_source=(
        "SC3 blocks 264-266 cover the jungle-map traversal, all companion variants, "
        "the ancient-kingdom vista, and the Turkish guild's Ceuta speed-run contract. "
        "5F is the messenger state; 8B is a Shift-JIS choice lead here, while 82/92/94 "
        "remain block-correlated text/state as authored, "
        "and two short scene-control payloads remain excluded."
    ),
)

_PROFILES["maria-story-shared-events-v42-live"] = replace(
    _PROFILES["maria-story-shared-events-v41-live"],
    name="maria-story-shared-events-v42-live",
    leading_speaker_bytes=(
        (_PROFILES["maria-story-shared-events-v41-live"].leading_speaker_bytes
        - frozenset({0x93}))
        | frozenset({0x97, 0xC0})
    ),
    metrics_source=(
        "SC3 blocks 267-269 cover the complete jungle giant-snake and bog branches, "
        "the Colosseum rumor, and the desert/quicksand expedition with all companion variants. "
        "97/C0 are confirmed presentation states; 82/8E/90/92/93 remain Shift-JIS text leads, "
        "and one eight-byte scene-transition payload remains excluded as nontext."
    ),
)

_PROFILES["maria-story-shared-events-v43-live"] = replace(
    _PROFILES["maria-story-shared-events-v42-live"],
    name="maria-story-shared-events-v43-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v42-live"].leading_speaker_bytes
        | frozenset({0x43, 0x93, 0xC9, 0xCD})
    ),
    metrics_source=(
        "SC3 outstanding tail records cover Jacob, Gabriel, William, and Hernan bounty "
        "reminders/completion, the northern monk, imperial-palace, and ancient-map leads. "
        "43/93/C9/CD are confirmed presentation states; sixteen short opaque records are "
        "verified scene-control payloads and remain excluded as nontext."
    ),
)

_PROFILES["maria-story-shared-events-v44-live"] = replace(
    _PROFILES["maria-story-shared-events-v43-live"],
    name="maria-story-shared-events-v44-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v43-live"].leading_speaker_bytes
        | frozenset({0x01, 0x1B, 0x29, 0x2B, 0x40, 0xB7, 0xB8, 0xB9})
    ),
    metrics_source=(
        "SC3 blocks 0-10 cover the Proof discussion, Muramasa scenes, Kurushima and "
        "Escante confrontations, pirate-rival battles, and Yuris/Jacob/Gabriel encounters. "
        "01/1B/29/2B/40/B7/B8/B9 are confirmed presentation states; one six-byte "
        "opening scene-control payload remains excluded as nontext."
    ),
)

_PROFILES["maria-story-shared-events-v45-live"] = replace(
    _PROFILES["maria-story-shared-events-v44-live"],
    name="maria-story-shared-events-v45-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v44-live"].leading_speaker_bytes
        | frozenset({0x02, 0x09, 0x17})
    ),
    metrics_source=(
        "SC3 blocks 11-18 cover the Hernan battle, Lil rescue outcomes, Escante aftermath, "
        "and Manuel's sea elegy. 02/09/17 are confirmed Lil, Kamil, and Manuel states; "
        "all FI/FA macros and branch-specific continuations are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v46-live"] = replace(
    _PROFILES["maria-story-shared-events-v45-live"],
    name="maria-story-shared-events-v46-live",
    metrics_source=(
        "SC3 block 19 covers Aziza's crew mutiny, intervention and ransom branches, "
        "her father's Bloodstained Shamshir, renunciation of piracy, and recruitment. "
        "03/07/0A/0B/0C/11/1B/B7/B8/B9 are established presentation states, and all "
        "FI/FA/FO runtime name macros are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v47-live"] = replace(
    _PROFILES["maria-story-shared-events-v46-live"],
    name="maria-story-shared-events-v47-live",
    metrics_source=(
        "SC3 blocks 20-24 cover Aziza rematch outcomes and the Ulysse, Jacob, and "
        "Gabriel bounty captures. 03/1B/40/43/44 are established presentation states; "
        "source-authored leading line breaks and the FI runtime name macro are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v48-live"] = replace(
    _PROFILES["maria-story-shared-events-v47-live"],
    name="maria-story-shared-events-v48-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v47-live"].leading_speaker_bytes
        | frozenset({0x1C, 0x2C, 0x39, 0x4A})
    ),
    metrics_source=(
        "SC3 blocks 25-30 cover bounty finales, the ghost ship, an ironclad clash, "
        "both Lil-rescue choices, and Clifford's intervention. 1C/2C/39/4A are confirmed "
        "rival/crew presentation states; FI/FA macros and choice records are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v49-live"] = replace(
    _PROFILES["maria-story-shared-events-v48-live"],
    name="maria-story-shared-events-v49-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v48-live"].leading_speaker_bytes
        | frozenset({0x28, 0x9B})
    ),
    metrics_source=(
        "SC3 blocks 31-32 cover Kuen's false-flag assault, Hodram's rescue, Lil's "
        "reconciliation, and all anomalous-ship sighting variants. 28/9B are confirmed "
        "Kuen presentation states; FI/FO macros and source-leading breaks are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v50-live"] = replace(
    _PROFILES["maria-story-shared-events-v49-live"],
    name="maria-story-shared-events-v50-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v49-live"].leading_speaker_bytes
        | frozenset({0x74})
    ),
    metrics_source=(
        "SC3 blocks 33-34 cover the wako debrief, strategy reflection, coastal trade "
        "contracts, and local warning about Kuen and Pereira. 74 is the local-sailor "
        "presentation state; five short opaque scene-control payloads remain excluded."
    ),
)

_PROFILES["maria-story-shared-events-v51-live"] = replace(
    _PROFILES["maria-story-shared-events-v50-live"],
    name="maria-story-shared-events-v51-live",
    metrics_source=(
        "SC3 blocks 35-36 cover Bergstrom's warning, Kamil's Argot connection, "
        "and Maria's first direct confrontation with Lil in Batavia. Existing "
        "01/02/03/09/0A presentation states and FI/FA/FO macros are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v52-live"] = replace(
    _PROFILES["maria-story-shared-events-v51-live"],
    name="maria-story-shared-events-v52-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v51-live"].leading_speaker_bytes
        | frozenset({0x25})
    ),
    metrics_source=(
        "SC3 blocks 37-38 cover the Lil-rescue aftermath and the Uddin Company "
        "proposal. 25 is the Uddin representative's presentation state; the FI/FA "
        "runtime-name macros and both alliance choices are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v53-live"] = replace(
    _PROFILES["maria-story-shared-events-v52-live"],
    name="maria-story-shared-events-v53-live",
    max_lines=5,
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v52-live"].leading_speaker_bytes
        | frozenset({0x19, 0x26})
    ),
    metrics_source=(
        "SC3 blocks 39-40 cover Nagalpur's collapse and Maria's Madagascar-inspired "
        "trade-port plan. 19/26 are confirmed companion/Nagalpur presentation states; "
        "the FI runtime-name macro and geographic exposition are preserved. The source-"
        "authored leading blank plus four-line East Africa explanation requires five "
        "renderer lines and is kept without a trailing blank page."
    ),
)

_PROFILES["maria-story-shared-events-v54-live"] = replace(
    _PROFILES["maria-story-shared-events-v53-live"],
    name="maria-story-shared-events-v54-live",
    metrics_source=(
        "SC3 blocks 41-44 cover Tamsui's founding, government negotiations, "
        "construction funding, English workers, wine delivery, and trading-post "
        "completion. Existing 03/0A/0B/4A states and FI/FA/FO macros are preserved."
    ),
)

_PROFILES["maria-story-shared-events-v55-live"] = replace(
    _PROFILES["maria-story-shared-events-v54-live"],
    name="maria-story-shared-events-v55-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v54-live"].leading_speaker_bytes
        | frozenset({0x2F})
    ),
    metrics_source=(
        "SC3 block 45 covers Maria's first African landfall, confrontation with an "
        "Espinosa plantation overseer, condemnation of enslavement, and declaration "
        "against the company. 2F is the overseer's presentation state."
    ),
)

_PROFILES["maria-story-shared-events-v56-live"] = replace(
    _PROFILES["maria-story-shared-events-v55-live"],
    name="maria-story-shared-events-v56-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v55-live"].leading_speaker_bytes
        | frozenset({0x24, 0x54, 0x72, 0x8D, 0xFE})
    ),
    metrics_source=(
        "SC3 blocks 46-47 cover the English colonial challenge after Espinosa's "
        "defeat, Espinosa's capture by his victims, the African regional-treasure "
        "lead, and Maria's public acclaim. 24/54/72/8D are Espinosa and local "
        "presentation states; FE is the anonymous young Englishman's voice state."
    ),
)

_PROFILES["maria-story-shared-events-v57-live"] = replace(
    _PROFILES["maria-story-shared-events-v56-live"],
    name="maria-story-shared-events-v57-live",
    leading_speaker_bytes=(
        (_PROFILES["maria-story-shared-events-v56-live"].leading_speaker_bytes - {0x81, 0x83, 0x8D})
        | frozenset({0x05, 0x2A})
    ),
    metrics_source=(
        "SC3 blocks 48-50 cover the Raphael/Crow meeting, fair-trade debate, "
        "Mediterranean intelligence, Maldonado alliance branches, and Richard's "
        "betrayal. 05 and 2A are Crow and Maldonado presentation states. 81/83/8D "
        "are removed here because they are Shift-JIS lead bytes of visible text in B48."
    ),
)

_PROFILES["maria-story-shared-events-v58-live"] = replace(
    _PROFILES["maria-story-shared-events-v57-live"],
    name="maria-story-shared-events-v58-live",
    metrics_source=(
        "SC3 blocks 51-53 cover Richard's failed betrayal, the return to Hangzhou, "
        "assembly of every Proof of the Conqueror, and the philosophical route "
        "epilogue about belief, legitimacy, peace, and responsibility."
    ),
)

_PROFILES["maria-story-shared-events-v59-live"] = replace(
    _PROFILES["maria-story-shared-events-v58-live"],
    name="maria-story-shared-events-v59-live",
    metrics_source=(
        "SC3 block 54 is the complete alternate Maria ending: repeated Proof "
        "discussion, Ming fleet review, companion comedy, and historical narration."
    ),
)

_PROFILES["maria-story-shared-events-v60-live"] = replace(
    _PROFILES["maria-story-shared-events-v59-live"],
    name="maria-story-shared-events-v60-live",
    metrics_source=(
        "SC3 block 55 is Angelo's complete fever dream and farewell to his late "
        "sister Bianca, including the recovery scene and new-family resolution."
    ),
)

_PROFILES["maria-story-shared-events-v61-live"] = replace(
    _PROFILES["maria-story-shared-events-v60-live"],
    name="maria-story-shared-events-v61-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v60-live"].leading_speaker_bytes
        | frozenset({0x52, 0x68})
    ),
    metrics_source=(
        "SC3 block 56 is the complete Seville bullfight spectacle and Emilio "
        "Ferrog recruitment event. 52 and 68 are additional crowd presentation states."
    ),
)

_PROFILES["maria-story-shared-events-v62-live"] = replace(
    _PROFILES["maria-story-shared-events-v61-live"],
    name="maria-story-shared-events-v62-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v61-live"].leading_speaker_bytes
        | frozenset({0x4F})
    ),
    metrics_source=(
        "SC3 block 57 is Cristina and Mivor's complete London recruitment event. "
        "4F is Mivor Gentz's presentation state."
    ),
)

_PROFILES["maria-story-shared-events-v63-live"] = replace(
    _PROFILES["maria-story-shared-events-v62-live"],
    name="maria-story-shared-events-v63-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v62-live"].leading_speaker_bytes
        | frozenset({0xA2, 0xA7})
    ),
    metrics_source=(
        "SC3 block 58 is the complete London harbor rescue and Cristina-Mivor "
        "romantic follow-up. A2 and A7 are the boy and his mother's presentation states."
    ),
)

_PROFILES["maria-story-shared-events-v64-live"] = replace(
    _PROFILES["maria-story-shared-events-v63-live"],
    name="maria-story-shared-events-v64-live",
    metrics_source=(
        "SC3 block 59 is Maria and Janus's complete recruitment of the retired "
        "master navigator Gerhard Adernkatz."
    ),
)

_PROFILES["maria-story-shared-events-v65-live"] = replace(
    _PROFILES["maria-story-shared-events-v64-live"],
    name="maria-story-shared-events-v65-live",
    metrics_source=(
        "SC3 block 60 is Janus Pasha's complete recruitment, ship reward, and vessel-naming tutorial."
    ),
)

_PROFILES["maria-story-shared-events-v66-live"] = replace(
    _PROFILES["maria-story-shared-events-v65-live"],
    name="maria-story-shared-events-v66-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v65-live"].leading_speaker_bytes
        | frozenset({0x6D})
    ),
    metrics_source=(
        "SC3 block 61 is Charles Jean Rochefort's complete science-and-explosions recruitment. "
        "6D is the local townsman's presentation state."
    ),
)

_PROFILES["maria-story-shared-events-v67-live"] = replace(
    _PROFILES["maria-story-shared-events-v66-live"],
    name="maria-story-shared-events-v67-live",
    metrics_source=(
        "SC3 block 62 is Maria's complete Golden Crown of Silla encounter with Julian."
    ),
)

_PROFILES["maria-story-shared-events-v68-live"] = replace(
    _PROFILES["maria-story-shared-events-v67-live"],
    name="maria-story-shared-events-v68-live",
    metrics_source=(
        "SC3 block 64 is the complete stranger trust choice, item gift, and luck/spirit outcomes."
    ),
)

_PROFILES["maria-story-shared-events-v69-live"] = replace(
    _PROFILES["maria-story-shared-events-v68-live"],
    name="maria-story-shared-events-v69-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v68-live"].leading_speaker_bytes
        | frozenset({0x6C})
    ),
    metrics_source=(
        "SC3 block 65 is Emilio's complete tomato-tasting and seedling gift event. "
        "6C is the tomato vendor's presentation state."
    ),
)

_PROFILES["maria-story-shared-events-v70-live"] = replace(
    _PROFILES["maria-story-shared-events-v69-live"],
    name="maria-story-shared-events-v70-live",
    metrics_source=(
        "SC3 block 66 is Emilio's complete banana-theft, monkey chase, and unfamiliar-seed event."
    ),
)

_PROFILES["maria-story-shared-events-v71-live"] = replace(
    _PROFILES["maria-story-shared-events-v70-live"],
    name="maria-story-shared-events-v71-live",
    metrics_source=(
        "SC3 block 68 is Gerhard Adernkatz's complete lost-Katzbalger reminiscence."
    ),
)

_PROFILES["maria-story-shared-events-v72-live"] = replace(
    _PROFILES["maria-story-shared-events-v71-live"],
    name="maria-story-shared-events-v72-live",
    metrics_source=(
        "SC3 block 70 is the complete rogue-ninja black-garb rumor event."
    ),
)

_PROFILES["maria-story-shared-events-v73-live"] = replace(
    _PROFILES["maria-story-shared-events-v72-live"],
    name="maria-story-shared-events-v73-live",
    metrics_source=(
        "SC3 block 73 is Charles's complete amber science discussion and glowing-island rumor."
    ),
)

_PROFILES["maria-story-shared-events-v74-live"] = replace(
    _PROFILES["maria-story-shared-events-v73-live"],
    name="maria-story-shared-events-v74-live",
    metrics_source=("SC3 block 74 is Julio's Christina concern and Shield of Minerva rumor."),
)

_PROFILES["maria-story-shared-events-v75-live"] = replace(
    _PROFILES["maria-story-shared-events-v74-live"],
    name="maria-story-shared-events-v75-live",
    metrics_source=("SC3 block 75 is Samwell's complete Peacock Mail rumor."),
)

_PROFILES["maria-story-shared-events-v76-live"] = replace(
    _PROFILES["maria-story-shared-events-v75-live"],
    name="maria-story-shared-events-v76-live",
    metrics_source=("SC3 block 76 is Samwell's complete Vest of the Jaguar God rumor."),
)

_PROFILES["maria-story-shared-events-v77-live"] = replace(
    _PROFILES["maria-story-shared-events-v76-live"],
    name="maria-story-shared-events-v77-live",
    metrics_source=("SC3 block 77 is the complete Telescope of Aristarchus rumor."),
)

_PROFILES["maria-story-shared-events-v78-live"] = replace(
    _PROFILES["maria-story-shared-events-v77-live"],
    name="maria-story-shared-events-v78-live",
    metrics_source=("SC3 block 78 is the complete Hestia's Cauldron rumor."),
)

_PROFILES["maria-story-shared-events-v79-live"] = replace(
    _PROFILES["maria-story-shared-events-v78-live"],
    name="maria-story-shared-events-v79-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v78-live"].leading_speaker_bytes
        | frozenset({0x8B, 0xBF})
    ),
    metrics_source=("SC3 blocks 81-86 cover the Muramasa, church, Proof, Santiago, cross, and temple-debate scenes."),
)

_PROFILES["maria-story-shared-events-v80-live"] = replace(
    _PROFILES["maria-story-shared-events-v79-live"],
    name="maria-story-shared-events-v80-live",
    metrics_source=("SC3 block 87 is the complete temple Sphinx and arithmetic riddle sequence."),
)

_PROFILES["maria-story-shared-events-v81-live"] = replace(
    _PROFILES["maria-story-shared-events-v80-live"],
    name="maria-story-shared-events-v81-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v80-live"].leading_speaker_bytes
        | frozenset({0xB1, 0xB2})
    ),
    metrics_source=("SC3 block 88 is the complete megalith-cult infiltration and staged-army confrontation."),
)

_PROFILES["maria-story-shared-events-v82-live"] = replace(
    _PROFILES["maria-story-shared-events-v81-live"],
    name="maria-story-shared-events-v82-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v81-live"].leading_speaker_bytes
        | frozenset({0xA0})
    ),
    metrics_source=("SC3 blocks 89-90 cover the hidden-believer lamp handoff and Ottoman deadline outcomes."),
)

_PROFILES["maria-story-shared-events-v83-live"] = replace(
    _PROFILES["maria-story-shared-events-v82-live"],
    name="maria-story-shared-events-v83-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v82-live"].leading_speaker_bytes
        | frozenset({0x94, 0x97, 0x99})
    ),
    metrics_source=("SC3 blocks 91-93 cover guild timing, the bean riddle, and the sacred-pot maze trap."),
)

_PROFILES["maria-story-shared-events-v84-live"] = replace(
    _PROFILES["maria-story-shared-events-v83-live"],
    name="maria-story-shared-events-v84-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v83-live"].leading_speaker_bytes
        | frozenset({0x89})
    ),
    metrics_source=("SC3 block 94 is the complete palace-sage Proof motive test and northeastern map-clan clue."),
)

_PROFILES["maria-story-shared-events-v85-live"] = replace(
    _PROFILES["maria-story-shared-events-v84-live"],
    name="maria-story-shared-events-v85-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v84-live"].leading_speaker_bytes
        | frozenset({0xA3, 0xAA, 0xD7})
    ),
    metrics_source=("SC3 blocks 95-96 cover the complete sandbar rescue and jade-ruin examination."),
)

_PROFILES["maria-story-shared-events-v86-live"] = replace(
    _PROFILES["maria-story-shared-events-v85-live"],
    name="maria-story-shared-events-v86-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v85-live"].leading_speaker_bytes
        | frozenset({0xB4})
    ),
    metrics_source=("SC3 block 97 is the complete Sao Jorge raider confrontation, recruitment, and tablet handoff."),
)

_PROFILES["maria-story-shared-events-v87-live"] = replace(
    _PROFILES["maria-story-shared-events-v86-live"],
    name="maria-story-shared-events-v87-live",
    leading_speaker_bytes=(
        (_PROFILES["maria-story-shared-events-v86-live"].leading_speaker_bytes
        | frozenset({0xB3, 0xC6, 0xD1, 0xDC}))
        - frozenset({0x91})
    ),
    metrics_source=("SC3 blocks 98-101 cover the Hindustan ruin lead, figurehead discovery, dagger reward, and Christina lead."),
)

_PROFILES["maria-story-shared-events-v88-live"] = replace(
    _PROFILES["maria-story-shared-events-v87-live"],
    name="maria-story-shared-events-v88-live",
    metrics_source=("SC3 block 102 is the complete Xien confidence dialogue and Staff of Guidance lead."),
)

_PROFILES["maria-story-shared-events-v89-live"] = replace(
    _PROFILES["maria-story-shared-events-v88-live"],
    name="maria-story-shared-events-v89-live",
    metrics_source=("SC3 block 103 contains all eight companion-specific shark warnings."),
)

_PROFILES["maria-story-shared-events-v90-live"] = replace(
    _PROFILES["maria-story-shared-events-v89-live"],
    name="maria-story-shared-events-v90-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v89-live"].leading_speaker_bytes
        | frozenset({0x90, 0x95})
    ),
    metrics_source=("SC3 blocks 104-107 cover the Ceuta deadline, Mao encounter, public-fear confession, Ming recognition, and East Asian Proof-map discovery."),
)

_PROFILES["maria-story-shared-events-v91-live"] = replace(
    _PROFILES["maria-story-shared-events-v90-live"],
    name="maria-story-shared-events-v91-live",
    metrics_source=("SC3 blocks 108-109 cover Kuen's defector, Argot deception, Maria's maritime mission, and companion pledges."),
)

_PROFILES["maria-story-shared-events-v92-live"] = replace(
    _PROFILES["maria-story-shared-events-v91-live"],
    name="maria-story-shared-events-v92-live",
    metrics_source=("SC3 blocks 110-112 cover the frightened townsman, Guam castaway, and Southeast Asian Proof-map reveal."),
)

_PROFILES["maria-story-shared-events-v93-live"] = replace(
    _PROFILES["maria-story-shared-events-v92-live"],
    name="maria-story-shared-events-v93-live",
    metrics_source=("SC3 blocks 113-115 cover Nagalpur rivalry, an admirer gift, and the Indian Ocean Proof-map reveal."),
)

_PROFILES["maria-story-shared-events-v94-live"] = replace(
    _PROFILES["maria-story-shared-events-v93-live"],
    name="maria-story-shared-events-v94-live",
    metrics_source=("SC3 blocks 116-120 cover the judgment anecdote and African and Mediterranean Proof-map reveals."),
)

_PROFILES["maria-story-shared-events-v95-live"] = replace(
    _PROFILES["maria-story-shared-events-v94-live"],
    name="maria-story-shared-events-v95-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v94-live"].leading_speaker_bytes
        | frozenset({0x83})
    ),
    metrics_source=("SC3 blocks 121-126 cover Bergstrom, Clifford's legacy, and North Sea and New World Proof-map reveals."),
)

_PROFILES["maria-story-shared-events-v96-live"] = replace(
    _PROFILES["maria-story-shared-events-v95-live"],
    name="maria-story-shared-events-v96-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v95-live"].leading_speaker_bytes
        | frozenset({0x0F})
    ),
    metrics_source=("SC3 blocks 127-129 cover Al and Angelo recruitment and Angelo's Bianca resolution."),
)

_PROFILES["maria-story-shared-events-v97-live"] = replace(
    _PROFILES["maria-story-shared-events-v96-live"],
    name="maria-story-shared-events-v97-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v96-live"].leading_speaker_bytes
        | frozenset({0x69, 0x8E})
    ),
    metrics_source=("SC3 blocks 130-131 cover Carlo's recruitment and Cristina's flamenco scene."),
)

_PROFILES["maria-story-shared-events-v98-live"] = replace(
    _PROFILES["maria-story-shared-events-v97-live"],
    name="maria-story-shared-events-v98-live",
    metrics_source=("SC3 blocks 132-133 cover Samwell's coin-trick recruitment and a following absence line."),
)

_PROFILES["maria-story-shared-events-v99-live"] = replace(
    _PROFILES["maria-story-shared-events-v98-live"],
    name="maria-story-shared-events-v99-live",
    metrics_source=("SC3 blocks 134 and 136 cover an absence hook and Dias's gambling recruitment."),
)

_PROFILES["maria-story-shared-events-v100-live"] = replace(
    _PROFILES["maria-story-shared-events-v99-live"],
    name="maria-story-shared-events-v100-live",
    metrics_source=("SC3 block 137 covers Julio Erneco's recruitment and his rivalry with Xien."),
)

_PROFILES["maria-story-shared-events-v101-live"] = replace(
    _PROFILES["maria-story-shared-events-v100-live"],
    name="maria-story-shared-events-v101-live",
    metrics_source=("SC3 block 138 covers Manuel's recruitment and ship-room tutorial."),
)

_PROFILES["maria-story-shared-events-v102-live"] = replace(
    _PROFILES["maria-story-shared-events-v101-live"],
    name="maria-story-shared-events-v102-live",
    metrics_source=("SC3 block 135 covers Cesare Tohni's rescue, recruitment, and ship-purchasing tutorial."),
)

_PROFILES["maria-story-shared-events-v103-live"] = replace(
    _PROFILES["maria-story-shared-events-v102-live"],
    name="maria-story-shared-events-v103-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v102-live"].leading_speaker_bytes
        | frozenset({0x51, 0xAE, 0xAF})
    ),
    metrics_source=("SC3 blocks 141, 142, and 149 cover Yifa's dream, the Silla crown lead, and the Seville banana boom."),
)

_PROFILES["maria-story-shared-events-v104-live"] = replace(
    _PROFILES["maria-story-shared-events-v103-live"],
    name="maria-story-shared-events-v104-live",
    metrics_source=("SC3 block 140 covers Yifa's pursuit, demonstration, and recruitment."),
)

_PROFILES["maria-story-shared-events-v105-live"] = replace(
    _PROFILES["maria-story-shared-events-v104-live"],
    name="maria-story-shared-events-v105-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v104-live"].leading_speaker_bytes
        | frozenset({0xCA})
    ),
    metrics_source=("SC3 block 143 covers Maria's Seoul tavern lead to the Golden Crown of Silla."),
)

_PROFILES["maria-story-shared-events-v106-live"] = replace(
    _PROFILES["maria-story-shared-events-v105-live"],
    name="maria-story-shared-events-v106-live",
    metrics_source=("SC3 blocks 147-148 cover optional companion reflections on India and Arab culture."),
)

_PROFILES["maria-story-shared-events-v107-live"] = replace(
    _PROFILES["maria-story-shared-events-v106-live"],
    name="maria-story-shared-events-v107-live",
    metrics_source=("SC3 blocks 144 and 146 cover Julian's recruitment and Yukihisa's independent sword search."),
)

_PROFILES["maria-story-shared-events-v108-live"] = replace(
    _PROFILES["maria-story-shared-events-v107-live"],
    name="maria-story-shared-events-v108-live",
    metrics_source=("SC3 block 145 covers Aziza's tavern confrontation and sword-interest setup."),
)

_PROFILES["maria-story-shared-events-v109-live"] = replace(
    _PROFILES["maria-story-shared-events-v108-live"],
    name="maria-story-shared-events-v109-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v108-live"].leading_speaker_bytes
        | frozenset({0x9D})
    ),
    metrics_source=("SC3 blocks 175, 180, 189, and 199 cover four optional book, weapon, and armor leads."),
)

_PROFILES["maria-story-shared-events-v110-live"] = replace(
    _PROFILES["maria-story-shared-events-v109-live"],
    name="maria-story-shared-events-v110-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v109-live"].leading_speaker_bytes
        | frozenset({0x8C})
    ),
    metrics_source=("SC3 block 172 covers the Rocco Alemkel portrait and navigator-book discovery."),
)

_PROFILES["maria-story-shared-events-v111-live"] = replace(
    _PROFILES["maria-story-shared-events-v110-live"],
    name="maria-story-shared-events-v111-live",
    leading_speaker_bytes=(
        _PROFILES["maria-story-shared-events-v110-live"].leading_speaker_bytes
        | frozenset({0x41, 0x45, 0xBE})
    ),
    metrics_source=("SC3 blocks 223-239 cover the final ruin greeting and bounty variants."),
)


_PROFILES["lil-story-deep-route-v103-live"] = replace(
    _PROFILES["lil-story-deep-route-v102-live"],
    name="lil-story-deep-route-v103-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v102-live"].leading_speaker_bytes | frozenset({0x68, 0x71}),
    metrics_source="Lil B227-B238: merchant 68 and sailor 71; twelve alternate letter reports retain bare starts.",
)


_PROFILES["lil-story-deep-route-v104-live"] = replace(
    _PROFILES["lil-story-deep-route-v103-live"],
    name="lil-story-deep-route-v104-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v103-live"].leading_speaker_bytes | frozenset({0x43, 0x8B, 0x93, 0xBA, 0xBC, 0xC1, 0xC3, 0xC4}),
    metrics_source="Lil B239-B249: swindler, priest, guild and tavern states; four choices have bare starts.",
)


_PROFILES["lil-story-deep-route-v105-live"] = replace(
    _PROFILES["lil-story-deep-route-v104-live"],
    name="lil-story-deep-route-v105-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v104-live"].leading_speaker_bytes | frozenset({0xBD, 0xBE, 0xC8})) - frozenset({0x82, 0x88, 0x89, 0x8A, 0x8D, 0x90, 0x92, 0x93}),
    metrics_source="Lil B250-B254: twenty-one bare choices/collapse variants, three tavern states, two figurehead events.",
)


_PROFILES["lil-story-deep-route-v106-live"] = replace(
    _PROFILES["lil-story-deep-route-v105-live"],
    name="lil-story-deep-route-v106-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v105-live"].leading_speaker_bytes | frozenset({0x3E, 0x3F, 0x40, 0x41, 0x44, 0x45, 0x46, 0x60, 0x93, 0x94, 0x95, 0xCF}),
    metrics_source="Lil B255-B282: guild quest, captured-person, tavern patron and companion presentation states; no bare records.",
)


_PROFILES["lil-story-deep-route-v107-live"] = replace(
    _PROFILES["lil-story-deep-route-v106-live"],
    name="lil-story-deep-route-v107-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v106-live"].leading_speaker_bytes | frozenset({0xD0, 0xD3, 0xD7, 0xD8})) - frozenset({0x81, 0x82, 0x88, 0x8A, 0x8C, 0x8E, 0x90, 0x92, 0x97, 0x9F}),
    metrics_source="Lil B283-B287: forest encounter, bare companion variants and choices, London delivery NPC states.",
)


_PROFILES["lil-story-deep-route-v108-live"] = replace(
    _PROFILES["lil-story-deep-route-v107-live"],
    name="lil-story-deep-route-v108-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v107-live"].leading_speaker_bytes | frozenset({0x97})) - frozenset({0x81, 0x82, 0x83, 0x89, 0x8A, 0x8B, 0x8D, 0x92, 0x93}),
    metrics_source="Lil B288: jungle/cave tiger encounter, bare variants and choices; Lil, Kamil, Mikhail and companion states.",
)


_PROFILES["lil-story-deep-route-v109-live"] = replace(
    _PROFILES["lil-story-deep-route-v108-live"],
    name="lil-story-deep-route-v109-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v108-live"].leading_speaker_bytes | frozenset({0xAA, 0xC7, 0x97}),
    metrics_source="Lil B289-B292 Angkor temple elder, hostess and platinum riddle; no bare records.",
)


_PROFILES["lil-story-deep-route-v110-live"] = replace(
    _PROFILES["lil-story-deep-route-v109-live"],
    name="lil-story-deep-route-v110-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v109-live"].leading_speaker_bytes | frozenset({0x94})) - frozenset({0x81, 0x82, 0x83, 0x8B, 0x91, 0x92, 0x96}),
    metrics_source="Lil B293-B294 cliff and fog: guide state 94, bare choices and companion variants.",
)


_PROFILES["lil-story-deep-route-v111-live"] = replace(
    _PROFILES["lil-story-deep-route-v110-live"],
    name="lil-story-deep-route-v111-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v110-live"].leading_speaker_bytes | frozenset({0x5F, 0x94}),
    metrics_source="Lil B295-B298 Heavenly Wristband guild quest; no bare records.",
)


_PROFILES["lil-story-deep-route-v112-live"] = replace(
    _PROFILES["lil-story-deep-route-v111-live"],
    name="lil-story-deep-route-v112-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v111-live"].leading_speaker_bytes | frozenset({0x97, 0xC0, 0xCF})) - frozenset({0x82, 0x83, 0x8A, 0x8B, 0x90, 0x91, 0x92, 0x93}),
    metrics_source="Lil B299-B300 giant snake and bog: bare variants/choices, state 97 and hostess C0.",
)


_PROFILES["lil-story-deep-route-v113-live"] = replace(
    _PROFILES["lil-story-deep-route-v112-live"],
    name="lil-story-deep-route-v113-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v112-live"].leading_speaker_bytes | frozenset({0x94, 0x97, 0xC5, 0xD6})) - frozenset({0x82, 0x83, 0x8F, 0x91, 0x92}),
    metrics_source="Lil B301-B305 desert bare variants and choices; state 97, hostess C5 and guild 94.",
)


_PROFILES["lil-story-deep-route-v114-live"] = replace(
    _PROFILES["lil-story-deep-route-v113-live"],
    name="lil-story-deep-route-v114-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v113-live"].leading_speaker_bytes | frozenset({0xCB, 0x97})) - frozenset({0x82, 0x83, 0x8B, 0x8D, 0x90, 0x92, 0x95}),
    metrics_source="Lil B306 river bare variants/choices, guide CB and real state 97; Japanese 97AC variant handled separately.",
)


_PROFILES["lil-story-deep-route-v115-live"] = replace(
    _PROFILES["lil-story-deep-route-v114-live"],
    name="lil-story-deep-route-v115-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v114-live"].leading_speaker_bytes | frozenset({0x89, 0xCB})) - frozenset({0x82, 0x92, 0x97}),
    metrics_source="Lil B307-B311 monk state 89, hostess CB and bare companion variants; B306R0081 Japanese 97AC is bare prose.",
)


_PROFILES["lil-story-deep-route-v116-live"] = replace(
    _PROFILES["lil-story-deep-route-v115-live"],
    name="lil-story-deep-route-v116-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v115-live"].leading_speaker_bytes | frozenset({0x97, 0xC9, 0xD7, 0xDA})) - frozenset({0x81, 0x82, 0x89, 0x8A, 0x8B, 0x90, 0x91, 0x92, 0x93}),
    metrics_source="Lil B312-B313 wolf choices and bare variants; states 97/D7/DA and hostess C9.",
)


_PROFILES["lil-story-deep-route-v117-live"] = replace(
    _PROFILES["lil-story-deep-route-v116-live"],
    name="lil-story-deep-route-v117-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v116-live"].leading_speaker_bytes | frozenset({0xCD, 0x97})) - frozenset({0x82, 0x89, 0x90, 0x91, 0x92, 0x96, 0x9F}),
    metrics_source="Lil B314-B315 dark forest bare variants/choices, real state 97 and hostess CD; 8949/9F54 are Japanese prose.",
)


_PROFILES["lil-story-deep-route-v118-live"] = replace(
    _PROFILES["lil-story-deep-route-v117-live"],
    name="lil-story-deep-route-v118-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v117-live"].leading_speaker_bytes - frozenset({0x81, 0x82, 0x8B, 0x8C, 0x8E, 0x8F, 0x91, 0x92, 0x93, 0x96}),
    metrics_source="Lil B316 scorpions: bare variants and Kill/Shoo/Run choices, real state 97 and treatment state DA.",
)


_PROFILES["lil-story-deep-route-v119-live"] = replace(
    _PROFILES["lil-story-deep-route-v118-live"],
    name="lil-story-deep-route-v119-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v118-live"].leading_speaker_bytes | frozenset({0x68, 0xCC})) - frozenset({0x82, 0x96}),
    metrics_source="Lil B317-B319 fortune teller CC and local man 68; bare response variants and FI/FO substitutions.",
)


_PROFILES["lil-story-deep-route-v120-live"] = replace(
    _PROFILES["lil-story-deep-route-v119-live"],
    name="lil-story-deep-route-v120-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v119-live"].leading_speaker_bytes - frozenset({0x82, 0x8C, 0x8D, 0x90, 0x92, 0x94, 0x96}),
    metrics_source="Lil B323 fog: bare companion variants and choices, real 02/D0/D3/FE states; packed events unchanged.",
)


_PROFILES["lil-story-deep-route-v121-live"] = replace(
    _PROFILES["lil-story-deep-route-v120-live"],
    name="lil-story-deep-route-v121-live",
    leading_speaker_bytes=_PROFILES["lil-story-deep-route-v120-live"].leading_speaker_bytes - frozenset({0x81, 0x82, 0x89, 0x8E, 0x90, 0x92, 0x96}),
    metrics_source="Lil B324 jungle: bare choices and companion variants, real 16/CF/D0/D3/D6/FE states; packed aftermath unchanged.",
)


_PROFILES["lil-story-deep-route-v122-live"] = replace(
    _PROFILES["lil-story-deep-route-v121-live"],
    name="lil-story-deep-route-v122-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v121-live"].leading_speaker_bytes | frozenset({0x93, 0xB3, 0xCE})) - frozenset({0x81, 0x82, 0x92}),
    metrics_source="Lil B325-B329: guide B3, hostess CE, guild 93, bare companions; sea crossing and tomato boom FI/FA.",
)


_PROFILES["lil-story-deep-route-v123-live"] = replace(
    _PROFILES["lil-story-deep-route-v122-live"],
    name="lil-story-deep-route-v123-live",
    leading_speaker_bytes=(_PROFILES["lil-story-deep-route-v122-live"].leading_speaker_bytes | frozenset({0xA1, 0x97})) - frozenset({0x92}),
    metrics_source="Lil B330-B335: guide B3, elder A1, survey 97, Charles 12, bare landing team; FA preserved.",
)


def profile_names() -> tuple[str, ...]:
    return tuple(sorted(_PROFILES))


def get_dialogue_profile(name: str) -> DialogueProfile:
    try:
        return _PROFILES[name]
    except KeyError as error:
        raise ValueError(f"unknown dialogue profile: {name}") from error
