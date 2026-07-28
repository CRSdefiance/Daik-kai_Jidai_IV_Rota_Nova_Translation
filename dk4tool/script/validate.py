from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from dk4tool.formats.control_codes import missing_tokens
from dk4tool.script.mesfile import encode_mesfile_text

from .model import STATUSES


@dataclass(frozen=True)
class ValidationIssue:
    row_id: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def normalize_encoding(value: str) -> str:
    key = value.strip().lower().replace("_", "-")
    return {"shift-jis": "cp932", "shift_jis": "cp932", "utf-16le": "utf-16le"}.get(key, key)


def validate_rows(rows: list[dict[str, str]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for row in rows:
        row_id = row.get("id", "<missing>")
        status = row.get("status", "")
        if status not in STATUSES:
            issues.append(ValidationIssue(row_id, "error", f"unknown status: {status!r}"))
        english = row.get("english", "")
        if status == "approved" and not english:
            issues.append(ValidationIssue(row_id, "error", "approved row has blank English text"))
        if not english:
            continue
        missing = missing_tokens(row.get("japanese", ""), english)
        if missing:
            issues.append(
                ValidationIssue(row_id, "error", f"required control tokens missing: {missing}")
            )
        try:
            if row.get("control_profile") == "mesfile":
                encoded = encode_mesfile_text(english)
                source_hex = row.get("source_hex", "")
                if source_hex:
                    source = bytes.fromhex(source_hex)
                    source_indent = len(source) - len(source.lstrip(b" "))
                    encoded_indent = len(encoded) - len(encoded.lstrip(b" "))
                    if encoded_indent < source_indent:
                        encoded = b" " * (source_indent - encoded_indent) + encoded
                macro_scan = re.sub(r"\{[^{}]+\}", "", english)
                unsafe_f = any(
                    character == "F"
                    and (index + 1 == len(macro_scan) or macro_scan[index + 1] not in "IAO")
                    for index, character in enumerate(macro_scan)
                )
                unsafe_i = any(
                    character == "I" and (index == 0 or macro_scan[index - 1] != "F")
                    for index, character in enumerate(macro_scan)
                )
                if unsafe_f or unsafe_i:
                    issues.append(
                        ValidationIssue(
                            row_id,
                            "error",
                            "unsafe uppercase story macro letter; rewrite literal F/I text",
                        )
                    )
            else:
                encoded = english.encode(normalize_encoding(row.get("encoding", "cp932")))
        except (LookupError, UnicodeEncodeError, ValueError) as error:
            issues.append(ValidationIssue(row_id, "error", f"encoding failed: {error}"))
            continue
        try:
            maximum = int(row.get("max_bytes") or row.get("source_length") or 0)
        except ValueError:
            issues.append(ValidationIssue(row_id, "error", "max_bytes is not an integer"))
            continue
        allow_expand = row.get("allow_expand", "").lower() in {"1", "true", "yes"}
        if len(encoded) > maximum and not allow_expand:
            issues.append(
                ValidationIssue(
                    row_id, "error", f"encoded text is {len(encoded)} bytes; maximum is {maximum}"
                )
            )
        try:
            wrap_width = int(row.get("wrap_width") or 0)
        except ValueError:
            wrap_width = 0
            issues.append(ValidationIssue(row_id, "error", "wrap_width is not an integer"))
        visible_text = re.sub(r"\{LB@[0-9]+\}", "\n", english)
        visible_text = visible_text.replace("{LB}", "\n").replace("{END}", "").replace("{PAD}", "")
        visible_text = re.sub(r"\{HEX:[0-9A-Fa-f]{2}\}", "", visible_text)
        if wrap_width and any(len(line) > wrap_width for line in visible_text.splitlines()):
            issues.append(ValidationIssue(row_id, "warning", f"line exceeds {wrap_width} characters"))
    return issues
