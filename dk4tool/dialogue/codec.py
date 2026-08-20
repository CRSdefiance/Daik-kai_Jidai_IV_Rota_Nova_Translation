from __future__ import annotations

import re

from .model import DialogueToken

MACROS = (b"FI", b"FA", b"FO")
MARKUP_RE = re.compile(
    r"\{(?:LB(?:@[0-9]+)?|ALIGN@[0-9]+|PAD|END|SPEAKER:[0-9A-Fa-f]{2}|"
    r"MACRO:(?:FI|FA|FO|I)|HEX:[0-9A-Fa-f]{2})\}"
)


def _append_text(tokens: list[DialogueToken], value: str, raw: bytes) -> None:
    if tokens and tokens[-1].kind == "text":
        previous = tokens[-1]
        tokens[-1] = DialogueToken("text", previous.value + value, previous.raw + raw)
    else:
        tokens.append(DialogueToken("text", value, raw))


def _cp932_character(raw: bytes, cursor: int) -> tuple[str | None, bytes]:
    first = raw[cursor]
    width = 2 if (0x81 <= first <= 0x9F) or (0xE0 <= first <= 0xFC) else 1
    candidate = raw[cursor : cursor + width]
    if len(candidate) != width:
        return None, raw[cursor : cursor + 1]
    try:
        return candidate.decode("cp932"), candidate
    except UnicodeDecodeError:
        return None, raw[cursor : cursor + 1]


def tokenize_raw(
    raw: bytes, *, leading_speaker_bytes: frozenset[int] = frozenset()
) -> list[DialogueToken]:
    """Tokenize a record without discarding or normalizing any source byte."""

    tokens: list[DialogueToken] = []
    cursor = 0
    while cursor < len(raw):
        byte = raw[cursor]
        if cursor == 0 and (
            (0x01 <= byte <= 0x0F and byte != 0x0A)
            or byte in leading_speaker_bytes
        ):
            tokens.append(DialogueToken("speaker", f"{byte:02X}", bytes([byte])))
            cursor += 1
            continue
        if byte == 0x0A:
            tokens.append(DialogueToken("line_break", "", b"\x0A"))
            cursor += 1
            continue
        if byte < 0x20:
            tokens.append(DialogueToken("raw_control", f"{byte:02X}", bytes([byte])))
            cursor += 1
            continue
        macro = next((value for value in MACROS if raw.startswith(value, cursor)), None)
        if macro is not None:
            tokens.append(DialogueToken("macro", macro.decode("ascii"), macro))
            cursor += len(macro)
            continue
        if byte == ord("I"):
            tokens.append(DialogueToken("macro", "I", b"I"))
            cursor += 1
            continue
        character, encoded = _cp932_character(raw, cursor)
        if character is None:
            tokens.append(DialogueToken("raw_control", encoded.hex().upper(), encoded))
        else:
            _append_text(tokens, character, encoded)
        cursor += len(encoded)
    return tokens


def tokens_to_markup(tokens: list[DialogueToken]) -> str:
    output: list[str] = []
    for token in tokens:
        if token.kind == "text":
            output.append(token.value)
        elif token.kind == "line_break":
            output.append("{LB}" if not token.value else f"{{LB@{token.value}}}")
        elif token.kind == "macro":
            output.append(f"{{MACRO:{token.value}}}")
        elif token.kind == "speaker":
            output.append(f"{{SPEAKER:{token.value}}}")
        elif token.kind == "raw_control":
            output.extend(f"{{HEX:{byte:02X}}}" for byte in token.raw)
        elif token.kind == "align":
            output.append(f"{{ALIGN@{token.value}}}")
        elif token.kind == "pad":
            output.append("{PAD}")
        elif token.kind == "end":
            output.append("{END}")
        else:
            raise ValueError(f"unsupported dialogue token kind: {token.kind}")
    return "".join(output)


def parse_markup(text: str) -> list[DialogueToken]:
    """Parse editable dialogue markup while keeping literal text distinct from macros."""

    tokens: list[DialogueToken] = []
    cursor = 0
    for match in MARKUP_RE.finditer(text):
        if match.start() > cursor:
            literal = text[cursor : match.start()]
            if re.search(r"\{[^{}]*\}", literal):
                raise ValueError(f"unknown dialogue token in {literal!r}")
            _append_text(tokens, literal, literal.encode("cp932"))
        token = match.group(0)
        if token == "{LB}":
            tokens.append(DialogueToken("line_break", "", b"\x0A"))
        elif token.startswith("{LB@"):
            tokens.append(DialogueToken("line_break", token[4:-1], b"\x0A"))
        elif token.startswith("{ALIGN@"):
            tokens.append(DialogueToken("align", token[7:-1], b""))
        elif token == "{PAD}":
            tokens.append(DialogueToken("pad", "", b""))
        elif token == "{END}":
            tokens.append(DialogueToken("end", "", b"\x00"))
        elif token.startswith("{MACRO:"):
            value = token[7:-1]
            tokens.append(DialogueToken("macro", value, value.encode("ascii")))
        elif token.startswith("{SPEAKER:"):
            value = token[9:-1].upper()
            tokens.append(DialogueToken("speaker", value, bytes([int(value, 16)])))
        else:
            raw = bytes([int(token[5:7], 16)])
            if not tokens and 0x01 <= raw[0] <= 0x0F and raw[0] != 0x0A:
                # Backward compatibility for the project's existing {HEX:04}-style
                # speaker prefixes. New exports use the explicit SPEAKER token.
                tokens.append(DialogueToken("speaker", token[5:7].upper(), raw))
            else:
                tokens.append(DialogueToken("raw_control", token[5:7].upper(), raw))
        cursor = match.end()
    if cursor < len(text):
        literal = text[cursor:]
        if re.search(r"\{[^{}]*\}", literal):
            raise ValueError(f"unknown dialogue token in {literal!r}")
        _append_text(tokens, literal, literal.encode("cp932"))
    return tokens


class PairPhaseError(ValueError):
    """Raised when protected-break ASCII pair parity cannot be proven."""


def tokens_to_bytes(
    tokens: list[DialogueToken],
    *,
    guard_linebreaks: bool = False,
    pair_phase_safe_breaks: bool = False,
    macro_ascii_lengths: dict[str, int] | None = None,
) -> bytes:
    """Encode tokens, optionally repairing progressive ASCII pair phase.

    The live-tested zero-cursor renderer batches printable single-byte glyphs
    in pairs.  At the unsafe phase, a protected ``LF + guard`` causes the
    guard and first continuation glyph to share a draw batch; the next batch
    can overwrite that first glyph.  An internal pre-LF space flips the phase.
    It is emitted here rather than represented in editable markup.
    """

    if pair_phase_safe_breaks and not guard_linebreaks:
        raise PairPhaseError("pair-phase-safe breaks require protected line breaks")

    output = bytearray()
    ascii_phase = 0
    phase_known = True
    known_macro_lengths = macro_ascii_lengths or {}

    def append(raw: bytes, *, count_ascii: bool = False) -> None:
        nonlocal ascii_phase
        output.extend(raw)
        if count_ascii:
            ascii_phase ^= sum(0x20 <= byte < 0x80 for byte in raw) & 1

    for index, token in enumerate(tokens):
        if token.kind == "text":
            append(token.raw)
            ascii_phase ^= sum(ord(character) < 0x80 for character in token.value) & 1
        elif token.kind == "macro":
            append(token.raw)
            if pair_phase_safe_breaks:
                if token.value not in known_macro_lengths:
                    phase_known = False
                elif phase_known:
                    ascii_phase ^= known_macro_lengths[token.value] & 1
        elif token.kind in {"speaker", "raw_control", "end"}:
            append(token.raw)
        elif token.kind == "line_break":
            next_is_linebreak = (
                index + 1 < len(tokens) and tokens[index + 1].kind == "line_break"
            )
            needs_guard = guard_linebreaks and not next_is_linebreak
            if pair_phase_safe_breaks and needs_guard and token.value:
                raise PairPhaseError(
                    "pair-phase-safe breaks do not support positioned {LB@...}"
                )
            if pair_phase_safe_breaks and needs_guard and not phase_known:
                raise PairPhaseError(
                    "cannot prove ASCII pair phase after runtime macro with "
                    "unknown expansion parity"
                )
            if token.value:
                target = int(token.value)
                if len(output) > target:
                    raise ValueError(
                        f"cannot align line break to byte {target}; "
                        f"dialogue already occupies {len(output)} bytes"
                    )
                padding = target - len(output)
                append(
                    b" " * max(0, padding - (1 if needs_guard else 0)),
                    count_ascii=True,
                )
            # The cold-booted B44_R0071 fixture has 32 printable ASCII bytes
            # before LF and loses its first continuation glyph without this
            # repair.  Adding one byte flips that even phase to the safe one.
            if pair_phase_safe_breaks and needs_guard and not ascii_phase:
                append(b" ", count_ascii=True)
            append(b"\x0A")
            if needs_guard:
                append(b" ", count_ascii=pair_phase_safe_breaks)
        elif token.kind == "align":
            target = int(token.value)
            if len(output) > target:
                raise ValueError(
                    f"cannot align text to byte {target}; "
                    f"dialogue already occupies {len(output)} bytes"
                )
            append(b" " * (target - len(output)), count_ascii=True)
        elif token.kind == "pad":
            continue
        else:
            raise ValueError(f"unsupported dialogue token kind: {token.kind}")
    return bytes(output)
