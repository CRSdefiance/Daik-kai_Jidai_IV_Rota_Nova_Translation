from __future__ import annotations

from collections import Counter

from dk4tool.formats.ilnk import IlnkContainer

from .codec import tokenize_raw, tokens_to_markup


def inspect_ilnk_dialogue(data: bytes, file_path: str) -> dict[str, object]:
    """Inventory every non-empty ILNK record without decoding away unknown bytes."""

    container = IlnkContainer.parse(data)
    header_size = 8 + (len(container.blocks) + 1) * 4
    block_offset = header_size
    records: list[dict[str, object]] = []
    control_counts: Counter[str] = Counter()
    macro_counts: Counter[str] = Counter()
    speaker_counts: Counter[str] = Counter()

    for block_index, block in enumerate(container.blocks):
        cursor = 0
        for segment_index, raw in enumerate(block.split(b"\0")):
            if raw:
                tokens = tokenize_raw(raw)
                controls = [token.value for token in tokens if token.kind == "raw_control"]
                macros = [token.value for token in tokens if token.kind == "macro"]
                speakers = [token.value for token in tokens if token.kind == "speaker"]
                control_counts.update(controls)
                macro_counts.update(macros)
                speaker_counts.update(speakers)
                records.append(
                    {
                        "id": f"ILNK_B{block_index:02d}_R{segment_index:04d}",
                        "block_index": block_index,
                        "segment_index": segment_index,
                        "source_offset": block_offset + cursor,
                        "source_length": len(raw),
                        "source_hex": raw.hex().upper(),
                        "markup": tokens_to_markup(tokens),
                        "macros": macros,
                        "speakers": speakers,
                        "raw_controls": controls,
                        "line_break_count": sum(
                            token.kind == "line_break" for token in tokens
                        ),
                        "control_safe": not controls,
                    }
                )
            cursor += len(raw) + 1
        block_offset += len(block)

    return {
        "file_path": file_path,
        "format": "ILNK",
        "block_count": len(container.blocks),
        "record_count": len(records),
        "control_safe_record_count": sum(
            bool(record["control_safe"]) for record in records
        ),
        "raw_control_counts": dict(sorted(control_counts.items())),
        "macro_counts": dict(sorted(macro_counts.items())),
        "speaker_counts": dict(sorted(speaker_counts.items())),
        "records": records,
    }
