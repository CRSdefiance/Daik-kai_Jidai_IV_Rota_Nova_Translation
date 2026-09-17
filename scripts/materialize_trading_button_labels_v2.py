from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BASE_SHA256 = "d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf"
ARM9_SHA256 = "249860ab1d29ecfa8e149fd04b5cbff3c3414fb192f81459cfaf469d6c83fa52"
RECORDS = (
    (
        "DK4_TRADE_CONFIRM_BUTTON_A",
        0x11B51C,
        8,
        "Select",
        "Trading-post A-button: select the highlighted good or quantity.",
    ),
    (
        "DK4_TRADE_FINISH_BUTTON_X",
        0x11B554,
        8,
        "Finish",
        "Trading-post X-button: finish the complete multi-ship transaction.",
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize distinct trade-screen confirmation labels.")
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("translations/trading_button_labels_v2.json"),
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    arm9 = NdsImage.open(args.rom).read_file("/__arm9__.bin")
    if sha256(arm9) != ARM9_SHA256:
        raise SystemExit("wrong canonical accepted ARM9 component")

    records = []
    for record_id, offset, size, english, context in RECORDS:
        encoded = english.encode("ascii")
        if len(encoded) >= size:
            raise SystemExit(f"{record_id}: replacement must leave a null terminator")
        source = arm9[offset : offset + size]
        if source != b"Done\0\0\0\0":
            raise SystemExit(f"{record_id}: expected baked Done slot, found {source.hex()}")
        records.append(
            {
                "id": record_id,
                "offset": offset,
                "source_hex": source.hex().upper(),
                "english": english,
                "context": context,
                "notes": "Distinct action label; explicitly null-terminated inside the original eight-byte slot.",
            }
        )

    batch = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": "/__arm9__.bin",
        "source_file_sha256": ARM9_SHA256,
        "records": records,
    }
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(records)} trade button labels")


if __name__ == "__main__":
    main()
