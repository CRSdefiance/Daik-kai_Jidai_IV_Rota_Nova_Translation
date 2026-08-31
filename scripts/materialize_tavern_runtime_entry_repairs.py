from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.materialize_trader_tutorial_repair import build_record

BASE_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"

RUNTIME_RECORDS = {
    "DK4_MES_B00_R0037": {
        "size": 31,
        "entries": [(1, "That'll be 10 coins."), (21, "5 coins.")],
        "context": "The barkeep's ten- and five-coin replies share fixed entry offsets.",
        "source_meaning": "The barkeep states the applicable drink price.",
    },
    "DK4_MES_B00_R0038": {
        "size": 26,
        "entries": [(1, "Please serve %s.")],
        "context": "The barkeep calls the hostess after the one-byte runtime entry prefix.",
        "source_meaning": "The keeper asks the named hostess to serve the guest.",
    },
    "DK4_MES_B00_R0039": {
        "size": 20,
        "entries": [(2, "Hey, %s!"), (14, "On it!")],
        "context": "The keeper's hostess call and her answer have separate fixed entry offsets.",
        "source_meaning": "The keeper calls the named hostess, and she answers promptly.",
    },
    "DK4_MES_B00_R0040": {
        "size": 19,
        "entries": [(1, "Welcome!")],
        "context": "The hostess greeting begins after the source's one-byte entry prefix.",
        "source_meaning": "The hostess welcomes the customer.",
    },
    "DK4_MES_B00_R0041": {
        "size": 30,
        "entries": [(1, "Welcome, %s!")],
        "context": "The personalized greeting begins after the source's one-byte entry prefix.",
        "source_meaning": "The hostess welcomes the named customer.",
    },
    "DK4_MES_B00_R0042": {
        "size": 28,
        "entries": [(2, "Here, have another drink.")],
        "context": "The drink offer begins after the two-byte runtime entry prefix.",
        "source_meaning": "The hostess offers the customer another drink.",
    },
    "DK4_MES_B00_R0043": {
        "size": 27,
        "entries": [(1, "That'll be 20 coins.")],
        "context": "The twenty-coin reply begins after the source prefix.",
        "source_meaning": "The hostess states the twenty-coin price.",
    },
    "DK4_MES_B00_R0044": {
        "size": 15,
        "entries": [(1, "Ten coins.")],
        "context": "The ten-coin reply begins after the source prefix.",
        "source_meaning": "The hostess states the ten-coin price.",
    },
    "DK4_MES_B10_R0039": {
        "size": 73,
        "entries": [(2, "Drinks aren't free."), (22, "%s serves %s as %s.")],
        "context": "A refusal and a local-officer rumor share fixed interior entry points.",
        "source_meaning": "The barkeep refuses a free drink or identifies a locally prominent officer.",
    },
    "DK4_MES_B10_R0041": {
        "size": 101,
        "entries": [(0, "Have you visited the nearby town of %s?"), (48, "Know %s? It's nearby.")],
        "context": "Two nearby-city rumors share fixed voice-specific entries.",
        "source_meaning": "The speaker asks whether the player knows or has visited a nearby city.",
    },
    "DK4_MES_B10_R0043": {
        "size": 73,
        "entries": [
            (0, "Hm?"),
            (4, "You're pretty weak."),
            (24, "Right..."),
            (32, "%s, right?"),
            (43, "A toast to our new friendship!"),
        ],
        "context": "Five hostess reactions share independently addressed fixed entries.",
        "source_meaning": "The hostess reacts, judges an opponent, confirms a name, and proposes a toast.",
    },
}

MOVED_FROM_NATURAL = {
    "DK4_MES_B00_R0038",
    "DK4_MES_B00_R0040",
    "DK4_MES_B00_R0041",
    "DK4_MES_B00_R0042",
    "DK4_MES_B00_R0043",
    "DK4_MES_B00_R0044",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize runtime-proven tavern entry repairs.")
    parser.add_argument(
        "--rom",
        type=Path,
        default=Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds"),
    )
    parser.add_argument(
        "--out", type=Path, default=Path("translations/stockholm_tavern_interior_fixed_v1.json")
    )
    parser.add_argument(
        "--natural-batch",
        type=Path,
        default=Path("translations/tutorial_tavern_recruit_natural_v2.json"),
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical ROM for tavern repair materialization")
    common = NdsImage.open(args.rom).read_file("/COMMON/MESFILE.DK4")
    if sha256(common) != COMMON_SHA256:
        raise SystemExit("wrong canonical shared-message archive")
    blocks = IlnkContainer.parse(common).blocks

    records = []
    for row_id, spec in RUNTIME_RECORDS.items():
        block_index = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        record_index = int(row_id.rsplit("R", 1)[1])
        source = blocks[block_index].split(b"\0")[record_index]
        size = int(spec["size"])
        entries = list(spec["entries"])
        if len(source) != size:
            raise SystemExit(f"{row_id}: expected {size} source bytes, found {len(source)}")
        replacement = build_record(size, entries)
        records.append(
            {
                "id": row_id,
                "english": " | ".join(text for _, text in entries),
                "replacement_hex": replacement.hex().upper(),
                "interior_entries": [
                    {"offset": offset, "english": text} for offset, text in entries
                ],
                "speaker": "Barkeep / Tavern Hostess",
                "context": spec["context"],
                "source_meaning": spec["source_meaning"],
                "localization_note": "Runtime-observed source entry offsets are preserved exactly; unused bytes remain spaces.",
                "runtime_evidence": "User cold-boot screenshots exposed dropped leading characters or the packed alternate entry.",
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
        "scope": "Runtime-proven shared tavern entries and packed alternate messages",
        "unchanged_records": ["DK4_MES_B00_R0040", "DK4_MES_B00_R0042"],
        "unchanged_record_reason": (
            "These runtime-offset-safe records are already byte-identical in the "
            "accepted canonical baseline; declaring them prevents the ordinary "
            "formatter from reintroducing the observed dropped-prefix defects."
        ),
        "records": records,
    }
    args.out.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    natural = json.loads(args.natural_batch.read_text(encoding="utf-8"))
    natural["records"] = [
        record
        for record in natural["records"]
        if str(record.get("id", "")) not in MOVED_FROM_NATURAL
    ]
    args.natural_batch.write_text(
        json.dumps(natural, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"wrote {args.out}: {len(records)} runtime-fixed records; "
        f"retained {len(natural['records'])} ordinary tavern/recruitment records"
    )


if __name__ == "__main__":
    main()
