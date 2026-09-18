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
            "through B79"
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


def profile_names() -> tuple[str, ...]:
    return tuple(sorted(_PROFILES))


def get_dialogue_profile(name: str) -> DialogueProfile:
    try:
        return _PROFILES[name]
    except KeyError as error:
        raise ValueError(f"unknown dialogue profile: {name}") from error
