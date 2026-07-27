from __future__ import annotations

CSV_COLUMNS = [
    "id",
    "file_path",
    "container_path",
    "encoding",
    "source_offset",
    "source_length",
    "source_hex",
    "japanese",
    "english",
    "status",
    "context",
    "speaker",
    "notes",
    "max_bytes",
    "allow_expand",
    "pointer_group",
    "control_profile",
    "wrap_width",
]

STATUSES = {
    "untranslated",
    "draft",
    "reviewed",
    "approved",
    "do_not_translate",
    "technical",
    "overflow",
    "inserted",
    "failed",
}

