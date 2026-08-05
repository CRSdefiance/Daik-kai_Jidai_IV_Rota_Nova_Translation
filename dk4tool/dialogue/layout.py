from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass

from .codec import parse_markup, tokenize_raw, tokens_to_bytes, tokens_to_markup
from .model import DialogueToken
from .profiles import DialogueProfile


@dataclass(frozen=True)
class DialogueDiagnostic:
    severity: str
    code: str
    message: str
    line: int | None = None
    pixel_width: int | None = None

    def to_dict(self) -> dict[str, str | int | None]:
        return asdict(self)


def token_width(token: DialogueToken, profile: DialogueProfile) -> int:
    if token.kind == "text":
        return sum(profile.glyph_width(character) for character in token.value)
    if token.kind == "macro":
        return profile.macro_width(token.value)
    return 0


def _text_units(token: DialogueToken) -> list[DialogueToken]:
    return [
        DialogueToken("text", value, value.encode("cp932"))
        for value in re.findall(r"\s+|[^\s]+", token.value)
    ]


def _split_long_text(token: DialogueToken, profile: DialogueProfile) -> list[DialogueToken]:
    pieces: list[DialogueToken] = []
    current = ""
    current_width = 0
    for character in token.value:
        width = profile.glyph_width(character)
        if current and current_width + width > profile.window_width_px:
            pieces.append(DialogueToken("text", current, current.encode("cp932")))
            current = ""
            current_width = 0
        current += character
        current_width += width
    if current:
        pieces.append(DialogueToken("text", current, current.encode("cp932")))
    return pieces


def wrap_tokens(tokens: list[DialogueToken], profile: DialogueProfile) -> list[DialogueToken]:
    output: list[DialogueToken] = []
    line_width = 0
    pending_space: DialogueToken | None = None

    def line_break() -> None:
        nonlocal line_width, pending_space
        if not output or output[-1].kind != "line_break":
            output.append(DialogueToken("line_break", "", b"\x0A"))
        line_width = 0
        pending_space = None

    def append_visible(unit: DialogueToken) -> None:
        nonlocal line_width, pending_space
        width = token_width(unit, profile)
        space_width = token_width(pending_space, profile) if pending_space else 0
        if line_width and line_width + space_width + width > profile.window_width_px:
            line_break()
        elif pending_space is not None:
            output.append(pending_space)
            line_width += space_width
            pending_space = None
        output.append(unit)
        line_width += width

    for token in tokens:
        if token.kind == "line_break":
            line_break()
            if token.value:
                output[-1] = token
            continue
        if token.kind in {"align", "pad", "end", "speaker", "raw_control"}:
            output.append(token)
            continue
        units = _text_units(token) if token.kind == "text" else [token]
        for unit in units:
            if unit.kind == "text" and unit.value.isspace():
                if line_width:
                    pending_space = unit
                elif output and output[-1].kind == "line_break":
                    # Whitespace after an automatic wrap is not useful layout.
                    pending_space = None
                else:
                    output.append(unit)
                    line_width += token_width(unit, profile)
                continue
            width = token_width(unit, profile)
            if width > profile.window_width_px and unit.kind == "text":
                parts = _split_long_text(unit, profile)
            else:
                parts = [unit]
            for index, part in enumerate(parts):
                append_visible(part)
                if line_width >= profile.window_width_px and index < len(parts) - 1:
                    line_break()
    return output


def format_markup(text: str, profile: DialogueProfile) -> str:
    return tokens_to_markup(wrap_tokens(parse_markup(text), profile))


def _token_counts(tokens: list[DialogueToken], kind: str) -> Counter[str]:
    return Counter(token.value for token in tokens if token.kind == kind)


def lint_dialogue(
    source_raw: bytes,
    target_markup: str,
    profile: DialogueProfile,
    *,
    max_bytes: int | None = None,
) -> list[DialogueDiagnostic]:
    diagnostics: list[DialogueDiagnostic] = []
    source = tokenize_raw(source_raw)
    target = parse_markup(target_markup)

    unknown = [token for token in source if token.kind == "raw_control"]
    if unknown:
        values = ", ".join(token.raw.hex().upper() for token in unknown)
        diagnostics.append(
            DialogueDiagnostic("error", "unknown-control", f"unmapped source bytes: {values}")
        )

    for kind, code in (
        ("macro", "missing-macro"),
        ("speaker", "missing-speaker"),
        ("raw_control", "missing-control"),
    ):
        missing = _token_counts(source, kind) - _token_counts(target, kind)
        if missing:
            values = ", ".join(f"{name} x{count}" for name, count in sorted(missing.items()))
            diagnostics.append(DialogueDiagnostic("error", code, f"required tokens missing: {values}"))

    source_commands = [
        (token.kind, token.value)
        for token in source
        if token.kind in {"macro", "speaker", "raw_control"}
    ]
    target_commands = [
        (token.kind, token.value)
        for token in target
        if token.kind in {"macro", "speaker", "raw_control"}
    ]
    if Counter(source_commands) == Counter(target_commands) and source_commands != target_commands:
        diagnostics.append(
            DialogueDiagnostic(
                "error", "control-order", "runtime macros or controls changed order"
            )
        )

    source_breaks = sum(token.kind == "line_break" for token in source)
    target_breaks = sum(token.kind == "line_break" for token in target)
    if source_breaks != target_breaks:
        diagnostics.append(
            DialogueDiagnostic(
                "warning",
                "line-break-count",
                f"source has {source_breaks} line breaks; target has {target_breaks}",
            )
        )

    literal = "".join(token.value for token in target if token.kind == "text")
    unsafe = sorted({character for character in literal if character in "FI"})
    if unsafe:
        diagnostics.append(
            DialogueDiagnostic(
                "error",
                "unsafe-literal-macro",
                "literal uppercase macro bytes are unsafe: " + ", ".join(unsafe),
            )
        )

    lines: list[int] = [0]
    for token in target:
        if token.kind == "line_break":
            lines.append(0)
        else:
            lines[-1] += token_width(token, profile)
    for index, width in enumerate(lines, start=1):
        if width > profile.window_width_px:
            diagnostics.append(
                DialogueDiagnostic(
                    "error",
                    "line-overflow",
                    f"line is {width}px; maximum is {profile.window_width_px}px",
                    line=index,
                    pixel_width=width,
                )
            )
    if len(lines) > profile.max_lines:
        diagnostics.append(
            DialogueDiagnostic(
                "error",
                "page-overflow",
                f"dialogue uses {len(lines)} lines; profile permits {profile.max_lines}",
            )
        )

    encoded = tokens_to_bytes(target, guard_linebreaks=profile.guard_linebreaks)
    if max_bytes is not None and len(encoded) > max_bytes:
        diagnostics.append(
            DialogueDiagnostic(
                "error",
                "byte-overflow",
                f"encoded dialogue is {len(encoded)} bytes; maximum is {max_bytes}",
            )
        )
    return diagnostics
