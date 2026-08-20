from __future__ import annotations

from dataclasses import asdict, dataclass

from .codec import parse_markup
from .encoder import (
    DialogueEncodingError,
    encode_fixed_dialogue,
    encode_relocatable_dialogue,
)
from .layout import token_width
from .preview import visible_lines
from .profiles import DialogueProfile

WEAK_LINE_ENDINGS = {
    "a",
    "an",
    "as",
    "at",
    "for",
    "from",
    "in",
    "of",
    "the",
    "to",
    "with",
}


@dataclass(frozen=True)
class DialogueQaIssue:
    severity: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _line_widths(markup: str, profile: DialogueProfile) -> list[int]:
    widths = [0]
    for token in parse_markup(markup):
        if token.kind == "line_break":
            widths.append(profile.glyph_width(" ") if profile.guard_linebreaks else 0)
        else:
            widths[-1] += token_width(token, profile)
    return widths


def audit_fixed_dialogue_record(
    source_raw: bytes,
    target_markup: str,
    profile: DialogueProfile,
) -> dict[str, object]:
    """Produce exhaustive layout/encoding evidence for one fixed dialogue record."""

    issues: list[DialogueQaIssue] = []
    try:
        encoding = encode_fixed_dialogue(source_raw, target_markup, profile)
    except DialogueEncodingError as error:
        return {
            "formatted_markup": "",
            "visible_lines": [],
            "line_widths_px": [],
            "padding_bytes": None,
            "manual_break_count": target_markup.count("{LB}"),
            "automatic_break_count": None,
            "issues": [
                DialogueQaIssue("error", "encoding", str(error)).to_dict()
            ],
        }

    formatted = encoding.formatted_markup
    lines = visible_lines(parse_markup(formatted))
    # Speaker controls are zero-width and share a line with dialogue. Strip their
    # diagnostic label before applying prose heuristics.
    display_lines = [
        line.split(">", 1)[1] if line.startswith("<SPEAKER") and ">" in line else line
        for line in lines
    ]
    manual_breaks = target_markup.count("{LB}")
    formatted_breaks = formatted.count("{LB}")
    if manual_breaks:
        issues.append(
            DialogueQaIssue(
                "warning",
                "manual-break",
                f"record contains {manual_breaks} author-supplied line break(s)",
            )
        )
    for index, line in enumerate(display_lines[:-1], start=1):
        words = line.strip().split()
        if words and words[-1].strip(".,!?;:\"'").casefold() in WEAK_LINE_ENDINGS:
            issues.append(
                DialogueQaIssue(
                    "warning",
                    "weak-line-ending",
                    f"line {index} ends with weak wrap word {words[-1]!r}",
                )
            )
    if len(display_lines) > 1:
        final = display_lines[-1].strip()
        if 0 < len(final) <= 8:
            issues.append(
                DialogueQaIssue(
                    "warning",
                    "orphan-final-line",
                    f"final line is unusually short: {final!r}",
                )
            )
    if any(line.startswith((" ", "\t")) for line in display_lines):
        issues.append(
            DialogueQaIssue(
                "error",
                "authored-leading-space",
                "a visible line begins with authored whitespace",
            )
        )
    issues.extend(
        DialogueQaIssue(
            "info" if issue.code == "line-break-count" else issue.severity,
            issue.code,
            issue.message,
        )
        for issue in encoding.diagnostics
    )
    return {
        "formatted_markup": formatted,
        "visible_lines": display_lines,
        "line_widths_px": _line_widths(formatted, profile),
        "padding_bytes": encoding.padding_bytes,
        "manual_break_count": manual_breaks,
        "automatic_break_count": formatted_breaks - manual_breaks,
        "guard_indent_px": profile.glyph_width(" ") if profile.guard_linebreaks else 0,
        "issues": [issue.to_dict() for issue in issues],
    }


def audit_relocatable_dialogue_record(
    source_raw: bytes,
    target_markup: str,
    profile: DialogueProfile,
) -> dict[str, object]:
    """Audit a mapped record without applying its obsolete source byte budget."""

    issues: list[DialogueQaIssue] = []
    try:
        encoding = encode_relocatable_dialogue(source_raw, target_markup, profile)
    except DialogueEncodingError as error:
        return {
            "formatted_markup": "",
            "visible_lines": [],
            "line_widths_px": [],
            "padding_bytes": None,
            "manual_break_count": target_markup.count("{LB}"),
            "automatic_break_count": None,
            "issues": [DialogueQaIssue("error", "encoding", str(error)).to_dict()],
        }

    formatted = encoding.formatted_markup
    lines = visible_lines(parse_markup(formatted))
    display_lines = [
        line.split(">", 1)[1] if line.startswith("<SPEAKER") and ">" in line else line
        for line in lines
    ]
    manual_breaks = target_markup.count("{LB}")
    formatted_breaks = formatted.count("{LB}")
    if manual_breaks:
        issues.append(
            DialogueQaIssue(
                "warning",
                "manual-break",
                f"record contains {manual_breaks} author-supplied line break(s)",
            )
        )
    for index, line in enumerate(display_lines[:-1], start=1):
        words = line.strip().split()
        if words and words[-1].strip(".,!?;:\"'").casefold() in WEAK_LINE_ENDINGS:
            issues.append(
                DialogueQaIssue(
                    "warning",
                    "weak-line-ending",
                    f"line {index} ends with weak wrap word {words[-1]!r}",
                )
            )
    if len(display_lines) > 1:
        final = display_lines[-1].strip()
        if 0 < len(final) <= 8:
            issues.append(
                DialogueQaIssue(
                    "warning",
                    "orphan-final-line",
                    f"final line is unusually short: {final!r}",
                )
            )
    if any(line.startswith((" ", "\t")) for line in display_lines):
        issues.append(
            DialogueQaIssue(
                "error",
                "authored-leading-space",
                "a visible line begins with authored whitespace",
            )
        )
    issues.extend(
        DialogueQaIssue(
            "info" if issue.code == "line-break-count" else issue.severity,
            issue.code,
            issue.message,
        )
        for issue in encoding.diagnostics
    )
    return {
        "formatted_markup": formatted,
        "visible_lines": display_lines,
        "line_widths_px": _line_widths(formatted, profile),
        "padding_bytes": 0,
        "manual_break_count": manual_breaks,
        "automatic_break_count": formatted_breaks - manual_breaks,
        "guard_indent_px": profile.glyph_width(" ") if profile.guard_linebreaks else 0,
        "issues": [issue.to_dict() for issue in issues],
    }
