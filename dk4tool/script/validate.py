from __future__ import annotations

from dataclasses import asdict, dataclass

from dk4tool.formats.control_codes import missing_tokens

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
            encoded = english.encode(normalize_encoding(row.get("encoding", "cp932")))
        except (LookupError, UnicodeEncodeError) as error:
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
        if wrap_width and any(len(line) > wrap_width for line in english.splitlines()):
            issues.append(ValidationIssue(row_id, "warning", f"line exceeds {wrap_width} characters"))
    return issues

