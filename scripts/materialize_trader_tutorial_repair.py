from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"

PACKED_RECORDS = {
    "DK4_MES_B00_R0008": {
        "size": 55,
        "entries": [(2, "Can I help?"), (14, "Thanks! Come again.")],
        "context": "Trader greeting and farewell share one record with two interior entry points.",
        "source_meaning": "The trader asks what the player needs, or thanks the player and asks for future business.",
    },
    "DK4_MES_B00_R0010": {
        "size": 111,
        "entries": [
            (1, "Does this work?"),
            (25, "This okay?"),
            (37, "Is this okay?"),
            (57, "Good with this?"),
            (77, "Will this do?"),
            (97, "This good?"),
        ],
        "context": "Six officer-voice confirmation variants share fixed interior entry points.",
        "source_meaning": "Each voice asks the player to confirm the proposed trade or arrangement.",
    },
    "DK4_MES_B00_R0009": {
        "size": 36,
        "entries": [(2, "Okay. A little discount for you.")],
        "context": "The trader agrees to improve the deal; the caller enters after the two-byte source prefix.",
        "source_meaning": "The trader relents and says they will provide a little extra service.",
    },
    "DK4_MES_B00_R0011": {
        "size": 27,
        "entries": [(1, "Does this look all right?")],
        "context": "The trader asks for confirmation after the one-byte source prefix.",
        "source_meaning": "The trader asks whether the proposed terms are satisfactory.",
    },
    "DK4_MES_B00_R0012": {
        "size": 64,
        "entries": [(1, "Each report has a fee. Which city?")],
        "context": "The trader explains the recurring market-report fee and asks for a city.",
        "source_meaning": "A fee is charged each time the player views another city's market report.",
    },
    "DK4_MES_B09_R0029": {
        "size": 40,
        "entries": [(2, "Anything else?"), (26, "Just browsing?")],
        "context": "The trader checks whether the player has more business or was only browsing.",
        "source_meaning": "The trader asks whether the player needs anything else, then challenges an idle visitor.",
    },
    "DK4_MES_B09_R0030": {
        "size": 40,
        "entries": [(1, "Thanks. We'll put it to good use.")],
        "context": "The trader accepts an investment after the one-byte runtime entry prefix.",
        "source_meaning": "The trader expresses gratitude and promises to use the contribution effectively.",
    },
    "DK4_MES_B09_R0032": {
        "size": 47,
        "entries": [(2, "Cargo holds are full. Buy less.")],
        "context": "The trader blocks a purchase after the two-byte runtime entry prefix.",
        "source_meaning": "The cargo holds are full, so the player must reduce the purchase quantity.",
    },
    "DK4_MES_B09_R0033": {
        "size": 24,
        "entries": [(2, "Start over?")],
        "context": "The trader confirms restarting the transaction after the source prefix.",
        "source_meaning": "The trader asks whether the player truly wants to redo the transaction.",
    },
    "DK4_MES_B09_R0034": {
        "size": 11,
        "entries": [(1, "A pain.")],
        "context": "The trader grumbles after the one-byte source prefix.",
        "source_meaning": "The trader complains that restarting is troublesome.",
    },
    "DK4_MES_B09_R0035": {
        "size": 67,
        "entries": [
            (1, "I'm busy. Don't waste my time."),
            (37, "You don't have enough money."),
        ],
        "context": "Two trader rejection messages share one record.",
        "source_meaning": "The trader rejects joking around while busy, or says the player lacks enough money.",
    },
    "DK4_MES_B09_R0036": {
        "size": 127,
        "entries": [
            (1, "Paying double may let us buy extra stock this time."),
            (65, "If we pay double, they may sell us extra stock."),
        ],
        "context": "Two officer voices explain the temporary double-price stock offer.",
        "source_meaning": "An officer says paying twice the normal amount may make additional goods available.",
    },
    "DK4_MES_B09_R0037": {
        "size": 56,
        "entries": [(1, "Paying double may get us extra stock.")],
        "context": "A companion explains the temporary double-price stock offer after the source prefix.",
        "source_meaning": "Paying twice the normal amount may make additional goods available.",
    },
    "DK4_MES_B09_R0039": {
        "size": 126,
        "entries": [
            (0, "Paying double may get us extra stock this time."),
            (64, "Pay double and we may get extra stock!"),
        ],
        "context": "Two more officer voices explain the temporary double-price stock offer.",
        "source_meaning": "An officer says paying twice the normal amount may make additional goods available.",
    },
    "DK4_MES_B09_R0040": {
        "size": 102,
        "entries": [
            (1, "Paying double may get us extra stock this time."),
            (65, "Sorry. Sign a contract in %s first."),
        ],
        "context": "An officer's stock hint and the trader's missing-contract rejection share one record.",
        "source_meaning": "The officer explains the double-price offer; the trader says to return after contracting in the named city.",
    },
    "DK4_MES_B09_R0041": {
        "size": 107,
        "entries": [(2, "No local share, yet you still want to invest? That's unusual. How much?")],
        "context": "The trader reacts to investment without local share after the two-byte source prefix.",
        "source_meaning": "The trader notes that the player cannot trade without share, admires the unusual investment, and asks for an amount.",
    },
    "DK4_MES_B09_R0042": {
        "size": 105,
        "entries": [(2, "So you'll invest? You are different. How much?")],
        "context": "The trader welcomes investment from a shareholder after the two-byte source prefix.",
        "source_meaning": "The trader welcomes the investment, compliments the player, and asks for an amount.",
    },
    "DK4_MES_B09_R0043": {
        "size": 150,
        "entries": [
            (0, "Not enough money. Market reports aren't free."),
            (
                60,
                "Since you're investing, I'll boost your share a little. Don't worry, I'll handle it.",
            ),
        ],
        "context": "The market-report payment rejection and investment bonus response share one record.",
        "source_meaning": "The trader refuses a free market report, or promises a small share advantage after investment.",
    },
    "DK4_MES_B09_R0044": {
        "size": 21,
        "entries": [(1, "Come back anytime.")],
        "context": "The trader closes the interaction after the one-byte source prefix.",
        "source_meaning": "The trader invites the player to return for future business.",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_record(size: int, entries: list[tuple[int, str]]) -> bytes:
    result = bytearray(b" " * size)
    for index, (offset, text) in enumerate(entries):
        encoded = text.encode("ascii")
        end = entries[index + 1][0] if index + 1 < len(entries) else size
        if not 0 <= offset <= end <= size:
            raise ValueError(f"invalid interior range {offset}:{end} for {size}-byte record")
        if len(encoded) > end - offset:
            raise ValueError(
                f"{text!r} needs {len(encoded)} bytes in {end - offset}-byte interior slot"
            )
        result[offset : offset + len(encoded)] = encoded
    return bytes(result)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize source-locked packed Trader tutorial records."
    )
    parser.add_argument(
        "--rom",
        type=Path,
        default=Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("translations/trader_tutorial_interior_fixed_v1.json"),
    )
    parser.add_argument(
        "--natural-batch",
        type=Path,
        default=Path("translations/trader_tutorial_natural_v2.json"),
    )
    args = parser.parse_args()

    rom_data = args.rom.read_bytes()
    if sha256(rom_data) != BASE_SHA256:
        raise SystemExit("wrong canonical ROM for Trader tutorial materialization")
    common = NdsImage.open(args.rom).read_file("/COMMON/MESFILE.DK4")
    if sha256(common) != COMMON_SHA256:
        raise SystemExit("wrong canonical /COMMON/MESFILE.DK4")
    blocks = IlnkContainer.parse(common).blocks

    records: list[dict[str, object]] = []
    for row_id, spec in PACKED_RECORDS.items():
        block_index = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        record_index = int(row_id.rsplit("R", 1)[1])
        source = blocks[block_index].split(b"\0")[record_index]
        size = int(spec["size"])
        if len(source) != size:
            raise SystemExit(f"{row_id}: expected {size} source bytes, found {len(source)}")
        entries = list(spec["entries"])
        replacement = build_record(size, entries)
        records.append(
            {
                "id": row_id,
                "english": " | ".join(text for _, text in entries),
                "replacement_hex": replacement.hex().upper(),
                "interior_entries": [
                    {"offset": offset, "english": text} for offset, text in entries
                ],
                "context": spec["context"],
                "source_meaning": spec["source_meaning"],
                "localization_note": (
                    "Every original interior entry offset is preserved exactly; unused bytes "
                    "inside each independently bounded slot remain spaces."
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
        "records": records,
    }
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    natural = json.loads(args.natural_batch.read_text(encoding="utf-8"))
    natural["records"] = [
        record
        for record in natural["records"]
        if str(record.get("id", "")) not in PACKED_RECORDS
    ]
    args.natural_batch.write_text(
        json.dumps(natural, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"wrote {args.out}: {len(records)} runtime-fixed records; "
        f"retained {len(natural['records'])} ordinary natural records"
    )


if __name__ == "__main__":
    main()
