from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE_FILE = "/data/SC2.DK4"


def inventory(profile_name: str) -> dict[str, object]:
    stack = json.loads((ROOT / "translations/release_stack.json").read_text(encoding="utf-8"))
    profile = stack["profiles"][profile_name]
    batch_names = [layer["batch"] for layer in stack["accepted_layers"]]
    batch_names.extend(profile["batches"])
    translated: set[str] = set()
    excluded: dict[str, str] = {}
    for batch_name in batch_names:
        path = ROOT / batch_name
        batch = json.loads(path.read_text(encoding="utf-8"))
        if batch.get("file_path") != ROUTE_FILE:
            continue
        translated.update(str(record["id"]) for record in batch.get("records", []))
        excluded.update(
            (str(row_id), str(reason))
            for row_id, reason in batch.get("excluded_records", {}).items()
        )
    excluded = {row_id: reason for row_id, reason in excluded.items() if row_id not in translated}

    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    source_ids = {row["id"] for row in rows}
    stale = sorted(translated - source_ids)
    if stale:
        raise ValueError(f"Translated IDs missing from clean source: {stale[:10]}")
    blocks: dict[int, dict[str, object]] = {}
    for row in rows:
        row_id = row["id"]
        block_number = int(row_id.split("_B", 1)[1].split("_R", 1)[0])
        block = blocks.setdefault(
            block_number,
            {"total": 0, "translated": 0, "excluded": 0, "remaining": []},
        )
        block["total"] = int(block["total"]) + 1
        if row_id in translated:
            block["translated"] = int(block["translated"]) + 1
        elif row_id in excluded:
            block["excluded"] = int(block["excluded"]) + 1
        else:
            block["remaining"].append(
                {
                    "id": row_id,
                    "source_length": int(row["source_length"]),
                    "lead_hex": row["source_hex"][:2],
                    "japanese": row["japanese"],
                }
            )
    return {
        "profile": profile_name,
        "route_file": ROUTE_FILE,
        "source_record_count": len(rows),
        "translated_record_count": len(translated),
        "excluded_record_count": len(excluded),
        "remaining_record_count": sum(len(block["remaining"]) for block in blocks.values()),
        "blocks": {str(number): block for number, block in sorted(blocks.items())},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory Lil's untranslated SC2 source records.")
    parser.add_argument("--profile", default="lil-deep-route-v23")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = inventory(args.profile)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"{report['profile']}: {report['translated_record_count']}/"
        f"{report['source_record_count']} translated; "
        f"{report['remaining_record_count']} remaining; "
        f"{report['excluded_record_count']} explicitly excluded"
    )
    for number, block in report["blocks"].items():
        if block["remaining"]:
            print(
                f"B{int(number):03d}: {block['translated']}/{block['total']} translated, "
                f"{len(block['remaining'])} remaining, {block['excluded']} excluded"
            )


if __name__ == "__main__":
    main()
