"""Inspect Switch DK4 dialogue and choice records and retain unclassified bytes."""

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
import struct
import sys


SPEECH = bytes.fromhex("00 40 ff ff")
CHOICES = {0x2100: 2, 0x2200: 3}
TOKEN = re.compile(r"FI|FA|FO|FU|FN|IC|%[-+ #0]*\d*(?:\.\d+)?[a-zA-Z%]|[\x00-\x1f\x7f]|I")


@dataclass(frozen=True)
class Block:
    index: int
    offset: int
    data: bytes


def read_bank(data):
    if len(data) < 4:
        raise ValueError("Missing block count.")
    count = struct.unpack_from("<I", data)[0]
    table_end = 4 + 8 * count
    if not count or table_end > len(data):
        raise ValueError("Invalid block table.")
    blocks = []
    cursor = table_end
    for index, (offset, size) in enumerate(struct.iter_unpack("<II", data[4:table_end])):
        if offset % 4 or offset < cursor or not size or offset + size > len(data):
            raise ValueError(f"Invalid or overlapping block {index} at {offset:#x}.")
        blocks.append(Block(index, offset, data[offset:offset + size]))
        cursor = offset + size
    return blocks


def _decode(raw):
    try:
        return raw.decode("cp932"), True
    except UnicodeDecodeError:
        return raw.decode("cp932", errors="replace"), False


def text_details(raw, start, dialogue):
    text, valid = _decode(raw)
    tokens = []
    if valid:
        for match in TOKEN.finditer(text):
            value = match[0]
            if value == "\n":
                kind = "line_break"
            elif value.startswith("%"):
                kind = "format_candidate"
            elif ord(value[0]) < 32 or value == "\x7f":
                kind = "unclassified_control_byte"
            elif not dialogue:
                continue
            elif value == "IC":
                kind = "pronoun_token_candidate"
            elif value == "I":
                kind = "possible_pronoun_collision"
            else:
                kind = "name_token"
            prefix_size = len(text[:match.start()].encode("cp932"))
            tokens.append({"kind": kind, "offset": start + prefix_size, "value": value})
        # Include percent signs that don't match printf syntax, including literal %.
        for match in re.finditer("%", text):
            offset = start + len(text[:match.start()].encode("cp932"))
            if not any(t["kind"] == "format_candidate" and
                       t["offset"] <= offset < t["offset"] + len(t["value"]) for t in tokens):
                tokens.append({"kind": "unclassified_percent", "offset": offset, "value": "%"})
    return {
        "text": text, "byte_length": len(raw), "text_offset": start,
        "terminator_offset": start + len(raw), "valid_cp932": valid,
        "explicit_line_count": text.count("\n") + 1,
        "explicit_line_bytes": [len(line) for line in raw.split(b"\n")],
        "tokens": sorted(tokens, key=lambda t: t["offset"]),
    }


def _speech(data, at, limit):
    if at + 6 >= limit or data[at:at + 4] != SPEECH:
        return None
    end = data.find(b"\0", at + 6, limit)
    if end <= at + 6:
        return None
    after = (end + 2) & ~1
    if after > limit or any(data[end:after]):
        return None
    return {
        "kind": "speech", "offset": at, "end": after, "opcode": "0x4000",
        "preamble_hex": data[at:at + 6].hex(" "),
        "presentation_byte": data[at + 4], "speaker_selector": data[at + 5],
        **text_details(data[at + 6:end], at + 6, dialogue=True),
    }


def _choice(data, at, limit):
    opcode = int.from_bytes(data[at:at + 2], "little")
    count = CHOICES.get(opcode)
    if count is None:
        return None
    base = at + 2 + 2 * count
    if base >= limit:
        return None
    indices = struct.unpack_from(f"<{count}H", data, at + 2)
    if indices[0] != 0 or sorted(set(indices)) != list(indices) or any(i % 2 for i in indices):
        return None
    values = []
    for i, index in enumerate(indices):
        start = base + index
        ceiling = base + indices[i + 1] if i + 1 < count else limit
        if start >= ceiling or ceiling > limit:
            return None
        end = data.find(b"\0", start, ceiling)
        if end <= start:
            return None
        after = (end + 2) & ~1
        if after > ceiling or any(data[end:after]) or (i + 1 < count and after != ceiling):
            return None
        label = text_details(data[start:end], start, dialogue=False)
        if not label["valid_cp932"] or any(
            not char.isprintable() and char != "\u3000" for char in label["text"]
        ):
            return None
        values.append({"index": i, "index_table_value": index, **label})
    return {"kind": "choice", "offset": at, "end": after,
            "opcode": f"{opcode:#06x}", "labels": values}


def _styles(data, at, limit, *, complete=False, voice_slots=10):
    if data[at:at + 2] != b"\x00\x41" or at + 24 >= limit:
        return None
    base = at + 24
    if complete:
        # A voice slot can point to its own line or share another slot's text.
        if voice_slots == 9 and data[at + 20:at + 22] != b"\0\0":
            return None
        slots = struct.unpack_from(f"<{voice_slots}H", data, at + 2)
        last = max(slots)
        if base + last >= limit:
            return None
        terminal = data.find(b"\0", base + last, limit)
        if terminal <= base + last:
            return None
        length = ((terminal + 2) & ~1) - base
    else:
        # Historical eight-slot view for reproducing previously released builds.
        slots = struct.unpack_from("<8H", data, at + 2)
        length = struct.unpack_from("<I", data, at + 18)[0]
    offsets = sorted(set(slots))
    if (offsets[0] != 0 or any(offset % 2 for offset in offsets)
            or length % 2 or offsets[-1] >= length or base + length > limit):
        return None
    values = []
    for offset, stop in zip(offsets, offsets[1:] + [length], strict=True):
        start, ceiling = base + offset, base + stop
        end = data.find(b"\0", start, ceiling)
        if end <= start or ((end + 2) & ~1) != ceiling or any(data[end:ceiling]):
            return None
        text = text_details(data[start:end], start, dialogue=True)
        if complete and (not text["valid_cp932"] or not text["text"].strip() or any(
            not char.isprintable() and char not in "\n\u3000" for char in text["text"]
        )):
            return None
        values.append({"style_slots": [i for i, slot in enumerate(slots) if slot == offset], **text})
    return {"kind": "style_alternatives", "offset": at, "end": base + length,
            "opcode": "0x4100", "index_table": list(slots), "text_area_bytes": length,
            "presentation_byte": data[at + 22], "speaker_selector": data[at + 23],
            "alternatives": values}


def _following_choice_branches(data, choice):
    # These relative commands are interpreted only in a complete choice dispatch table.
    start = choice["end"]
    count = len(choice["labels"])
    if start + count * 4 > len(data):
        return []
    jumps = []
    for i, (opcode, span) in enumerate(struct.iter_unpack("<HH", data[start:start + count * 4])):
        at = start + i * 4
        destination = at + 4 + span
        if opcode != (i + 2) * 0x100 or span % 2 or destination > len(data):
            return []
        jumps.append({"index": i, "opcode": f"{opcode:#06x}", "offset": at,
                      "relative_span": span, "target": destination})
    return jumps


def inspect_block(block, *, complete_styles=False, voice_slots=10):
    data = block.data
    if len(data) < 8 or data[:2] != b"DS" or struct.unpack_from("<I", data, 4)[0] != len(data) - 8:
        raise ValueError(f"Block {block.index} has an unsupported Switch scenario header.")
    records = []
    cursor = unknown_start = 8
    turn = 0
    while cursor + 1 < len(data):
        entry = (_speech(data, cursor, len(data)) or _choice(data, cursor, len(data))
                 or _styles(data, cursor, len(data), complete=complete_styles, voice_slots=voice_slots))
        if entry is None:
            cursor += 2
            continue
        if cursor > unknown_start:
            records.append({"kind": "unclassified", "offset": unknown_start, "end": cursor,
                            "hex": data[unknown_start:cursor].hex(" ")})
        if entry["kind"] == "speech":
            entry["turn"] = turn
            turn += 1
        records.append(entry)
        cursor = entry["end"]
        if entry["kind"] == "choice" and (branches := _following_choice_branches(data, entry)):
            end = cursor + 4 * len(branches)
            records.append({"kind": "choice_dispatch", "offset": cursor, "end": end,
                            "relative_commands": branches})
            cursor = end
        unknown_start = cursor
    if len(data) > unknown_start:
        records.append({"kind": "unclassified", "offset": unknown_start, "end": len(data),
                        "hex": data[unknown_start:].hex(" ")})
    return {"index": block.index, "file_offset": block.offset,
            "size": len(data), "header_hex": data[:8].hex(" "), "records": records}


def report(path, selection=None):
    blocks = read_bank(path.read_bytes())
    if selection is not None and not 0 <= selection < len(blocks):
        raise ValueError(f"Block {selection} is outside 0–{len(blocks) - 1}.")
    selected = blocks if selection is None else [blocks[selection]]
    rows = [inspect_block(block, complete_styles=True) for block in selected]
    counts = Counter(entry["kind"] for row in rows for entry in row["records"])
    return {"file": str(path), "block_count": len(blocks), "counts": dict(counts), "blocks": rows}


def print_text(result, summary):
    print(f"{result['file']} · {result['block_count']} blocks")
    print(", ".join(f"{count} {kind}" for kind, count in sorted(result["counts"].items())))
    if summary:
        return
    for block in result["blocks"]:
        base = block["file_offset"]
        print(f"\nBlock {block['index']}  file {base:#x}  {block['size']} bytes  header {block['header_hex']}")
        for entry in block["records"]:
            at = entry["offset"]
            where = f"+{at:04x} / file {base + at:#x}"
            if entry["kind"] == "unclassified":
                print(f"  {where}  unclassified  {entry['hex']}")
                continue
            if entry["kind"] == "choice_dispatch":
                print(f"  {where}  choice dispatch")
                for branch in entry["relative_commands"]:
                    print(f"    {branch['opcode']} at +{branch['offset']:04x} targets +{branch['target']:04x}")
                continue
            if entry["kind"] == "speech":
                print(f"  {where}  turn {entry['turn']}  {entry['preamble_hex']}  "
                      f"{entry['byte_length']} bytes  {entry['explicit_line_count']} explicit lines")
                values = [entry]
            elif entry["kind"] == "choice":
                print(f"  {where}  choice {entry['opcode']}")
                values = entry["labels"]
            else:
                print(f"  {where}  style alternatives {entry['opcode']}  "
                      f"selector {entry['speaker_selector']:#04x}")
                values = entry["alternatives"]
            for value in values:
                slots = value.get("style_slots")
                label = f"slots {slots} " if slots is not None else ""
                if "index" in value:
                    label = f"[{value['index']}] "
                print(f"    {label}{value['text']!r}")
                if not value["valid_cp932"]:
                    print("    invalid CP932")
                for token in value["tokens"]:
                    print(f"    +{token['offset']:04x}  {token['kind']}  {token['value']!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="An extracted Switch Sc*.dk4 scenario bank.")
    parser.add_argument("--block", type=int, help="Inspect one zero-based block.")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="Emit offset and token data as JSON.")
    output.add_argument("--summary", action="store_true", help="Print inventory counts only.")
    args = parser.parse_args()
    try:
        result = report(args.file, args.block)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(errors="backslashreplace")
        print_text(result, args.summary)


if __name__ == "__main__":
    main()
