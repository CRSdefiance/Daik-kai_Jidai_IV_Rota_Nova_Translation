from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

SOURCE_CSV = Path("work/sc2/script.csv")
SOURCE_ROM = Path("work/clean.nds")
OUTPUT = Path("translations/hodram_sc2_control_map_probe_v1.json")
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"

# Every diagnostic payload is exactly as long as the Japanese payload it replaces.
# The original leading byte is copied verbatim and is never interpreted by this tool.
PROBES = {
    "DK4_MES_B27_R0012": (0x01, "HODRAM [01]..."),
    "DK4_MES_B27_R0044": (0x02, "LIL state [02] OK..."),
    "DK4_MES_B27_R0161": (0x09, "KAMIL [09]...."),
    "DK4_MES_B27_R0127": (0x10, "GERHARD [10].."),
    "DK4_MES_B27_R0035": (0x14, "FERNANDO [14] OK..."),
    "DK4_MES_B27_R0041": (0x09, "Macro FI should show Lil........."),
}


def main() -> None:
    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}

    records: list[dict[str, str]] = []
    for row_id, (expected_lead, payload_text) in PROBES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        payload = payload_text.encode("ascii")
        if source[0] != expected_lead:
            raise SystemExit(f"{row_id}: expected lead {expected_lead:02X}, got {source[0]:02X}")
        source[1:].decode("cp932")
        if len(payload) != len(source) - 1:
            raise SystemExit(
                f"{row_id}: diagnostic payload is {len(payload)} bytes; "
                f"source payload is {len(source) - 1}"
            )
        replacement = source[:1] + payload
        records.append(
            {
                "id": row_id,
                "english": payload_text,
                "source_lead_hex": f"{source[0]:02X}",
                "source_hex_guard": source.hex(),
                "replacement_hex": replacement.hex(),
                "status": "research-control-map-probe",
                "notes": "Exact-length diagnostic; original one-byte lead preserved verbatim.",
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "content_type": "sc2-control-map-research-probe-v1",
        "research_only": True,
        "source_rom_sha256": hashlib.sha256(SOURCE_ROM.read_bytes()).hexdigest(),
        "profile_note": "Diagnostic-only Hodram block-27 probe. It preserves each exact source lead and allocation; it is not translated dialogue and must never be promoted.",
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} exact-length diagnostic records")


if __name__ == "__main__":
    main()
