import json
from pathlib import Path

SOURCE = Path("translations/common_mesfile_spacing_v4.json")
OUTPUT = Path("translations/common_mesfile_spacing_v4_unified_base.json")
OVERRIDES = (
    Path("translations/common_global_layout_v1.json"),
    Path("translations/common_mystery_items_v1.json"),
    Path("translations/common_runtime_layout_v4.json"),
    Path("translations/common_shipyard_layout_v2.json"),
)


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    replaced = set()
    for path in OVERRIDES:
        batch = json.loads(path.read_text(encoding="utf-8"))
        if batch.get("file_path") != "/COMMON/MESFILE.DK4":
            continue
        replaced.update(record["id"] for record in batch.get("records", []))
    original_count = len(payload["records"])
    payload["records"] = [record for record in payload["records"] if record["id"] not in replaced]
    payload["scope"] = (
        "Unified-release base derived from common_mesfile_spacing_v4; records superseded "
        "by accepted runtime/global/mystery/shipyard layout layers are omitted."
    )
    payload["inventory"] = {
        "source_records": original_count,
        "superseded_records": original_count - len(payload["records"]),
        "retained_records": len(payload["records"]),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUTPUT}: {len(payload['records'])} retained, "
        f"{original_count - len(payload['records'])} superseded"
    )


if __name__ == "__main__":
    main()
