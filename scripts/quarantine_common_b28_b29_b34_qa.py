from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "translations/common_natural_v2_b28_b29_b34_safe.json"
REPORT = ROOT / "work/qa/common_natural_v2_b28_b29_b34_safe/report.json"
SAFE_OUT = ROOT / "translations/common_natural_v2_b28_b29_b34_safe_qa.json"
BLOCKED_OUT = ROOT / "translations/common_natural_v2_b28_b29_b34_qa_blocked.json"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    source_records = {record["id"]: record for record in source["records"]}
    blocked: dict[str, list[dict[str, str]]] = {}
    for row in report["records"]:
        waivers = set(row.get("qa_waivers", []))
        issues = [
            issue
            for issue in row.get("issues", [])
            if issue.get("severity") in {"error", "warning"}
            and issue.get("code") not in waivers
        ]
        if issues:
            blocked[row["id"]] = issues

    unknown = set(blocked) - set(source_records)
    if unknown:
        raise SystemExit(f"QA report contains unknown records: {sorted(unknown)}")
    safe_records = [
        record for record in source["records"] if record["id"] not in blocked
    ]
    blocked_records = []
    for row_id in sorted(blocked):
        record = dict(source_records[row_id])
        record["blocker"] = "Quarantined by exhaustive dialogue QA; not buildable safely in its fixed allocation."
        record["qa_issues"] = blocked[row_id]
        record["formatting_review"] = False
        blocked_records.append(record)

    safe = dict(source)
    safe["format"] = "dk4-ilnk-translation-batch-v1"
    safe["scope"] = (
        "QA-clean subset of COMMON blocks 28, 29, and 34; overflow, command-byte, "
        "pair-phase, and unstable-wrap drafts are quarantined."
    )
    safe["blocked_records"] = [record["id"] for record in blocked_records]
    safe["records"] = safe_records
    blocked_batch = {
        "format": "dk4-ilnk-editorial-draft-v1",
        "file_path": source["file_path"],
        "source_file_sha256": source["source_file_sha256"],
        "blocks": [28, 29, 34],
        "buildable": False,
        "reason": "These otherwise translated drafts fail the fixed-allocation renderer audit and remain excluded from the ROM.",
        "records": blocked_records,
    }
    if len(safe_records) + len(blocked_records) != len(source_records):
        raise SystemExit("QA quarantine did not partition the source batch exactly")
    SAFE_OUT.write_text(json.dumps(safe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source["format"] = "dk4-ilnk-editorial-draft-v1"
    source["buildable"] = False
    source["reason"] = "Superseded by the QA-filtered safe batch and its quarantine companion."
    SOURCE.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BLOCKED_OUT.write_text(
        json.dumps(blocked_batch, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {SAFE_OUT}: {len(safe_records)} safe, {len(blocked_records)} quarantined")


if __name__ == "__main__":
    main()
