from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts.analyze_sc3_reuse import canonical_english, canonical_japanese
from scripts.inventory_lil_route import inventory

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROFILES = {
    "/data/SC0.DK4": "raphael-deep-route-v93",
    "/data/SC1.DK4": "hodram-deep-route-v32",
    "/data/SC3.DK4": "maria-deep-route-v111",
}


def _rows(file_path: str) -> dict[str, dict[str, str]]:
    route = file_path.split("/")[-1].split(".")[0].lower()
    with (ROOT / "work" / route / "script.csv").open(encoding="utf-8-sig", newline="") as stream:
        return {row["id"]: row for row in csv.DictReader(stream)}


def analyze() -> dict[str, object]:
    stack = json.loads((ROOT / "translations/release_stack.json").read_text(encoding="utf-8"))
    target_profile = max(
        (name for name in stack["profiles"] if name.startswith("lil-deep-route-v")),
        key=lambda name: int(name.rsplit("v", 1)[1]),
    )
    source_rows = {file_path: _rows(file_path) for file_path in SOURCE_PROFILES}
    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for file_path, profile_name in SOURCE_PROFILES.items():
        for batch_name in stack["profiles"][profile_name]["batches"]:
            batch = json.loads((ROOT / batch_name).read_text(encoding="utf-8"))
            if batch.get("file_path") != file_path:
                continue
            for record in batch.get("records", []):
                row_id = str(record["id"])
                row = source_rows[file_path].get(row_id)
                if not row:
                    continue
                source_key = canonical_japanese(row["japanese"])
                if not source_key:
                    continue
                by_source[source_key].append(
                    {
                        "file": file_path,
                        "id": row_id,
                        "batch": batch_name,
                        "speaker": str(record.get("speaker", "")),
                        "english": canonical_english(str(record.get("english", ""))),
                    }
                )

    remaining = inventory(target_profile)["blocks"]
    matches: list[dict[str, object]] = []
    by_block: Counter[int] = Counter()
    for number, block in remaining.items():
        for row in block["remaining"]:
            key = canonical_japanese(row["japanese"])
            sources = by_source.get(key, [])
            if not sources:
                continue
            block_number = int(number)
            by_block[block_number] += 1
            matches.append(
                {
                    "id": row["id"],
                    "block": block_number,
                    "japanese": row["japanese"],
                    "source_key": key,
                    "sources": sources,
                    "distinct_english": sorted({source["english"] for source in sources}),
                }
            )
    return {
        "format": "dk4-sc2-cross-route-reuse-audit-v1",
        "target_profile": target_profile,
        "source_profiles": list(SOURCE_PROFILES.values()),
        "remaining_record_count": sum(len(block["remaining"]) for block in remaining.values()),
        "matched_record_count": len(matches),
        "matched_blocks": {str(number): count for number, count in sorted(by_block.items())},
        "matches": matches,
    }


def main() -> None:
    report = analyze()
    output = ROOT / "work/analysis/sc2_cross_route_reuse.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Matched {report['matched_record_count']} of {report['remaining_record_count']} "
        f"remaining Lil records against source-identical translated records."
    )
    for number, count in sorted(
        report["matched_blocks"].items(), key=lambda item: (-item[1], int(item[0]))
    )[:25]:
        print(f"B{int(number):03d}: {count} matched")


if __name__ == "__main__":
    main()
