from __future__ import annotations

from dataclasses import dataclass

from .codec import PairPhaseError, parse_markup, tokens_to_bytes
from .layout import DialogueDiagnostic, format_markup, lint_dialogue, token_width
from .profiles import DialogueProfile


class DialogueEncodingError(ValueError):
    """Raised when editable dialogue cannot be encoded without changing semantics."""


@dataclass(frozen=True)
class FixedDialogueEncoding:
    formatted_markup: str
    encoded: bytes
    diagnostics: tuple[DialogueDiagnostic, ...]
    padding_bytes: int


@dataclass(frozen=True)
class RelocatableDialogueEncoding:
    formatted_markup: str
    encoded: bytes
    diagnostics: tuple[DialogueDiagnostic, ...]


def encode_fixed_dialogue(
    source_raw: bytes,
    target_markup: str,
    profile: DialogueProfile,
) -> FixedDialogueEncoding:
    """Format and encode one record without moving any following bytes.

    This is deliberately conservative. The target must opt into trailing-space
    padding with ``{PAD}``, preserve every source command exactly, fit the
    calibrated window, and fit the original record's byte allocation.
    """

    if "{PAD}" not in target_markup:
        raise DialogueEncodingError(
            "fixed-size dialogue must include {PAD} so trailing allocation is explicit"
        )
    target_tokens = parse_markup(target_markup)
    if any(token.kind == "end" for token in target_tokens):
        raise DialogueEncodingError(
            "{END} is not valid inside a fixed ILNK record; the container owns separators"
        )

    formatted = format_markup(target_markup, profile)
    diagnostics = tuple(
        lint_dialogue(source_raw, formatted, profile, max_bytes=len(source_raw))
    )
    errors = [diagnostic for diagnostic in diagnostics if diagnostic.severity == "error"]
    if errors:
        details = "; ".join(f"{issue.code}: {issue.message}" for issue in errors)
        raise DialogueEncodingError(details)

    formatted_tokens = parse_markup(formatted)
    try:
        encoded = tokens_to_bytes(
            formatted_tokens,
            guard_linebreaks=profile.guard_linebreaks,
            pair_phase_safe_breaks=profile.pair_phase_safe_breaks,
            macro_ascii_lengths=profile.macro_ascii_lengths,
        )
    except PairPhaseError as error:
        raise DialogueEncodingError(f"pair-phase-unsafe: {error}") from error
    padding = len(source_raw) - len(encoded)
    if padding < 0:
        # The linter normally catches this. Keep the invariant local to this
        # function in case a custom linter/profile is introduced later.
        raise DialogueEncodingError(
            f"encoded dialogue is {len(encoded)} bytes; allocation is {len(source_raw)}"
        )
    # Fixed records are padded with ordinary spaces. They are not zero-width to
    # the native renderer: enough padding after a full page advances into an
    # empty page and produces a blank text box before the next record.
    line_count = 1
    final_line_width = 0
    for token in formatted_tokens:
        if token.kind == "line_break":
            line_count += 1
            final_line_width = (
                profile.glyph_width(" ") if profile.guard_linebreaks else 0
            )
        else:
            final_line_width += token_width(token, profile)
    padding_width = padding * profile.glyph_width(" ")
    padding_lines = (final_line_width + padding_width) // profile.window_width_px
    if line_count + padding_lines > profile.max_lines:
        raise DialogueEncodingError(
            "padding-page-overflow: trailing fixed-size padding would advance "
            "into a blank dialogue page"
        )
    encoded += b" " * padding
    return FixedDialogueEncoding(formatted, encoded, diagnostics, padding)


def encode_relocatable_dialogue(
    source_raw: bytes,
    target_markup: str,
    profile: DialogueProfile,
) -> RelocatableDialogueEncoding:
    """Format a mapped dialogue record without inheriting its Japanese byte limit."""

    if "{PAD}" in target_markup:
        raise DialogueEncodingError(
            "relocatable dialogue must not request fixed-allocation padding"
        )
    target_tokens = parse_markup(target_markup)
    if any(token.kind == "end" for token in target_tokens):
        raise DialogueEncodingError(
            "{END} is not valid inside a relocated ILNK record; the container owns separators"
        )

    formatted = format_markup(target_markup, profile)
    diagnostics = tuple(lint_dialogue(source_raw, formatted, profile))
    errors = [diagnostic for diagnostic in diagnostics if diagnostic.severity == "error"]
    if errors:
        details = "; ".join(f"{issue.code}: {issue.message}" for issue in errors)
        raise DialogueEncodingError(details)

    try:
        encoded = tokens_to_bytes(
            parse_markup(formatted),
            guard_linebreaks=profile.guard_linebreaks,
            pair_phase_safe_breaks=profile.pair_phase_safe_breaks,
            macro_ascii_lengths=profile.macro_ascii_lengths,
        )
    except PairPhaseError as error:
        raise DialogueEncodingError(f"pair-phase-unsafe: {error}") from error
    if b"\0" in encoded:
        raise DialogueEncodingError("relocated dialogue contains an ILNK record terminator")
    return RelocatableDialogueEncoding(formatted, encoded, diagnostics)
