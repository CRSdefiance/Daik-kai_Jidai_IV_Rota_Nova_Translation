from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BASE_SHA256 = "d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf"
COMMON_SHA256 = "943ce540c99bca4cd5f2be16fba071e082b588619ac05f4c1fecd49528976ffc"

RECORDS = {
    "DK4_MES_B00_R0008": {
        "entries": [(2, "Need help?"), (14, "Thanks! Come again.")],
        "context": "Trader greeting and farewell with two proven interior entry points.",
        "source_meaning": "The trader asks what the player needs, or thanks the player and invites future business.",
    },
    "DK4_MES_B09_R0042": {
        "entries": [(2, "Excellent choice. How much will you invest?")],
        "context": "Trader response when an existing shareholder chooses to invest.",
        "source_meaning": "The trader welcomes the investment, compliments the player, and asks for an amount.",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_record(source: bytes, entries: list[tuple[int, str]]) -> bytes:
    rebuilt = bytearray(b" " * len(source))
    for index, (offset, text) in enumerate(entries):
        end = entries[index + 1][0] if index + 1 < len(entries) else len(source)
        encoded = text.encode("ascii")
        if len(encoded) > end - offset:
            raise ValueError(f"{text!r} does not fit interior slot {offset}:{end}")
        rebuilt[offset : offset + len(encoded)] = encoded
    return bytes(rebuilt)


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize the second Trader dialogue polish pass.")
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument(
        "--out", type=Path, default=Path("translations/trading_dialogue_polish_v2.json")
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    common = NdsImage.open(args.rom).read_file("/COMMON/MESFILE.DK4")
    if sha256(common) != COMMON_SHA256:
        raise SystemExit("wrong canonical accepted COMMON component")
    blocks = IlnkContainer.parse(common).blocks

    rows: list[dict[str, object]] = []
    for record_id, spec in RECORDS.items():
        block_index = int(record_id.split("_B", 1)[1].split("_", 1)[0])
        record_index = int(record_id.rsplit("R", 1)[1])
        source = blocks[block_index].split(b"\0")[record_index]
        entries = list(spec["entries"])
        replacement = build_record(source, entries)
        rows.append(
            {
                "id": record_id,
                "english": " | ".join(text for _, text in entries),
                "source_hex": source.hex().upper(),
                "replacement_hex": replacement.hex().upper(),
                "interior_entries": [
                    {"offset": offset, "english": text} for offset, text in entries
                ],
                "context": spec["context"],
                "source_meaning": spec["source_meaning"],
                "localization_note": (
                    "Preserves every proven interior entry offset. The greeting avoids standalone "
                    "uppercase I, which this renderer interprets as the Japanese pronoun glyph."
                    if record_id.endswith("R0008")
                    else "Natural American English replaces the earlier literal phrasing without moving the runtime entry point."
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "ilnk-interior-fixed-text-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": COMMON_SHA256,
        "target_locale": "en-US",
        "scope": "Trader greeting phase repair and natural investment response",
        "records": rows,
    }
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(rows)} polished Trader records")


if __name__ == "__main__":
    main()
