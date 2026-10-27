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
from .profiles import DialogueProfile, get_dialogue_profile

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


def audit_native_common_entry(source_raw: bytes, target_markup: str) -> dict[str, object]:
    """Audit COMMON's native wrapper without storing the preview's line breaks.

    Native entry bounds come from the ARM9 table. Visual wrapping, command
    safety and prose heuristics share the existing dialogue QA, while byte
    allocation is measured against the actual unbroken native paragraph.
    This does not relocate the record or alter the native offset table.
    """
    text = target_markup.removesuffix("{PAD}")
    profile = get_dialogue_profile("shared")
    report = audit_relocatable_dialogue_record(source_raw, text, profile)
    try:
        if "{" in text or "\n" in text or "\r" in text:
            raise ValueError("native COMMON prose requires one plain paragraph")
        if any(ord(character) > 127 and character not in {"Ｆ", "Ｉ"} for character in text):
            raise ValueError("native English permits only ASCII and safe full-width reserved Latin glyphs")
        encoded = text.encode("cp932")
        if len(encoded) > len(source_raw):
            raise ValueError(f"native entry requires {len(encoded)} bytes in {len(source_raw)}")
        report["native_padding_bytes"] = len(source_raw) - len(encoded)
        report["native_encoded_hex"] = encoded.ljust(len(source_raw), b" ").hex().upper()
        widths = report.get("line_widths_px", [])
        if widths:
            padding_rows = (widths[-1] + report["native_padding_bytes"] * profile.glyph_width(" ")) // profile.window_width_px
            if len(widths) + padding_rows > profile.max_lines:
                raise ValueError("native padding would advance into a blank dialogue page")
    except (ValueError, UnicodeEncodeError) as error:
        report["issues"].append(DialogueQaIssue("error", "native-entry-encoding", str(error)).to_dict())
    return report


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
