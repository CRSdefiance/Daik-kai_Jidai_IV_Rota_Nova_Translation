from __future__ import annotations

import json
from pathlib import Path

from dk4tool.rom.hashing import hash_bytes
from dk4tool.script.mesfile import export_mesfile_rows


def materialize_translation_batch(
    batch: dict[str, object], source_data: bytes
) -> list[dict[str, object]]:
    if batch.get("format") != "dk4-ilnk-translation-batch-v1":
        raise ValueError("unsupported translation batch format")
    file_path = str(batch.get("file_path", ""))
    if not file_path.startswith("/"):
        raise ValueError("translation batch file_path must be an internal absolute path")
    expected_hash = str(batch.get("source_file_sha256", "")).lower()
    actual_hash = hash_bytes(source_data)["sha256"]
    if expected_hash != actual_hash:
        raise ValueError(
            f"{file_path}: source file SHA-256 mismatch "
            f"(expected {expected_hash}, got {actual_hash})"
        )

    exported = export_mesfile_rows(source_data, file_path)
    by_id = {str(row["id"]): row for row in exported}
    materialized: list[dict[str, object]] = []
    seen: set[str] = set()
    records = batch.get("records")
    if not isinstance(records, list):
        raise TypeError("translation batch records must be a list")
    for record in records:
        if not isinstance(record, dict):
            raise TypeError("translation batch record must be an object")
        row_id = str(record.get("id", ""))
        if row_id in seen:
            raise ValueError(f"{row_id}: duplicate translation batch record")
        seen.add(row_id)
        try:
            row = dict(by_id[row_id])
        except KeyError as error:
            raise ValueError(f"{row_id}: record not found in {file_path}") from error
        row["english"] = str(record.get("english", ""))
        row["status"] = str(record.get("status", "draft"))
        for field in ("speaker", "notes", "context"):
            if field in record:
                row[field] = str(record[field])
        materialized.append(row)
    return materialized


def read_translation_batch(path: str | Path, source_data: bytes) -> list[dict[str, object]]:
    with Path(path).open("r", encoding="utf-8") as stream:
        batch = json.load(stream)
    if not isinstance(batch, dict):
        raise TypeError("translation batch root must be an object")
    return materialize_translation_batch(batch, source_data)
