from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.scan.sjis_scan import contains_japanese


@dataclass(frozen=True)
class MesfileRecord:
    block_index: int
    segment_index: int
    source_offset: int
    raw_bytes: bytes
    text: str

    @property
    def row_id(self) -> str:
        return f"DK4_MES_B{self.block_index:02d}_R{self.segment_index:04d}"

    @property
    def pointer_group(self) -> str:
        return f"ILNK:{self.block_index}:{self.segment_index}"


def decode_mesfile_text(raw: bytes) -> str:
    return raw.decode("cp932").replace("\n", "{LB}")


def encode_mesfile_text(text: str) -> bytes:
    output = bytearray()
    cursor = 0
    while cursor < len(text):
        aligned_linebreak = re.match(r"\{LB@([0-9]+)\}", text[cursor:])
        if aligned_linebreak:
            target_offset = int(aligned_linebreak.group(1))
            if len(output) > target_offset:
                raise ValueError(
                    f"cannot align line break to byte {target_offset}; "
                    f"translation already occupies {len(output)} bytes"
                )
            output.extend(b" " * (target_offset - len(output)))
            output.append(0x0A)
            cursor += len(aligned_linebreak.group(0))
        elif text.startswith("{PAD}", cursor):
            cursor += 5
        elif text.startswith("{LB}", cursor):
            output.append(0x0A)
            cursor += 4
        elif text.startswith("{END}", cursor):
            output.append(0x00)
            cursor += 5
        elif text.startswith("{HEX:", cursor) and cursor + 8 <= len(text):
            token = text[cursor : cursor + 8]
            if token[-1] == "}":
                output.append(int(token[5:7], 16))
                cursor += 8
            else:
                output.extend(text[cursor].encode("cp932"))
                cursor += 1
        else:
            output.extend(text[cursor].encode("cp932"))
            cursor += 1
    return bytes(output)


def iter_mesfile_records(data: bytes) -> list[MesfileRecord]:
    container = IlnkContainer.parse(data)
    header_size = 8 + (len(container.blocks) + 1) * 4
    records: list[MesfileRecord] = []
    block_offset = header_size
    for block_index, block in enumerate(container.blocks):
        cursor = 0
        for segment_index, raw in enumerate(block.split(b"\0")):
            if raw:
                try:
                    text = decode_mesfile_text(raw)
                except UnicodeDecodeError:
                    cursor += len(raw) + 1
                    continue
                if contains_japanese(text):
                    records.append(
                        MesfileRecord(
                            block_index,
                            segment_index,
                            block_offset + cursor,
                            raw,
                            text,
                        )
                    )
            cursor += len(raw) + 1
        block_offset += len(block)
    return records


def analyze_mesfile(data: bytes) -> dict[str, object]:
    container = IlnkContainer.parse(data)
    all_records = [raw for block in container.blocks for raw in block.split(b"\0") if raw]
    controls = Counter(byte for raw in all_records for byte in raw if byte < 0x20)
    decode_failures = 0
    for raw in all_records:
        try:
            decode_mesfile_text(raw)
        except UnicodeDecodeError:
            decode_failures += 1
    return {
        "format": "ILNK",
        "block_count": len(container.blocks),
        "offset_entry_count": len(container.blocks) + 1,
        "nonempty_record_count": len(all_records),
        "japanese_record_count": len(iter_mesfile_records(data)),
        "undecodable_record_count": decode_failures,
        "blocks_ending_with_null": sum(block.endswith(b"\0") for block in container.blocks),
        "records_with_linebreaks": sum(b"\n" in raw for raw in all_records),
        "control_byte_counts": {f"{byte:02X}": count for byte, count in sorted(controls.items())},
        "insertion_policy": "exact-length-only",
    }


def export_mesfile_rows(data: bytes, file_path: str) -> list[dict[str, object]]:
    rows = []
    for record in iter_mesfile_records(data):
        rows.append(
            {
                "id": record.row_id,
                "file_path": file_path,
                "container_path": f"{file_path}#block={record.block_index}",
                "encoding": "shift_jis",
                "source_offset": record.source_offset,
                "source_length": len(record.raw_bytes),
                "source_hex": record.raw_bytes.hex().upper(),
                "japanese": record.text,
                "english": "",
                "status": "untranslated",
                "context": f"ILNK block {record.block_index}, record {record.segment_index}",
                "speaker": "",
                "notes": "",
                "max_bytes": len(record.raw_bytes),
                "allow_expand": "false",
                "pointer_group": record.pointer_group,
                "control_profile": "mesfile",
                "wrap_width": 38,
            }
        )
    return rows


def rebuild_mesfile(data: bytes, rows: list[dict[str, str]]) -> bytes:
    container = IlnkContainer.parse(data)
    segments = [block.split(b"\0") for block in container.blocks]
    seen: set[tuple[int, int]] = set()
    for row in rows:
        if not row.get("english"):
            continue
        parts = row.get("pointer_group", "").split(":")
        if len(parts) != 3 or parts[0] != "ILNK":
            raise ValueError(f"{row.get('id')}: invalid ILNK pointer_group")
        block_index, segment_index = int(parts[1]), int(parts[2])
        key = (block_index, segment_index)
        if key in seen:
            raise ValueError(f"{row.get('id')}: duplicate ILNK record")
        seen.add(key)
        try:
            original = segments[block_index][segment_index]
        except IndexError as error:
            raise ValueError(f"{row.get('id')}: ILNK record is out of range") from error
        expected = bytes.fromhex(row["source_hex"])
        if original != expected:
            raise ValueError(f"{row.get('id')}: ILNK source bytes do not match")
        english = row["english"]
        pad_to_length = english.endswith("{PAD}")
        replacement = encode_mesfile_text(english)
        if pad_to_length:
            if len(replacement) > len(original):
                raise ValueError(
                    f"{row.get('id')}: ILNK replacement is {len(replacement)} bytes; "
                    f"cannot pad it to the shorter {len(original)}-byte source record"
                )
            replacement = replacement.ljust(len(original), b" ")
        allow_expand = row.get("allow_expand", "").lower() in {"1", "true", "yes"}
        if len(replacement) != len(original) and not allow_expand:
            raise ValueError(
                f"{row.get('id')}: ILNK replacement is {len(replacement)} bytes; "
                f"exactly {len(original)} bytes are required until inner pointers are mapped"
            )
        segments[block_index][segment_index] = replacement
    container.blocks = [b"\0".join(block) for block in segments]
    return container.to_bytes()
