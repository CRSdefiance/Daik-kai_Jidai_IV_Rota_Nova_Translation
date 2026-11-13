"""Preserve the existing CRLF format of changed JSON without changing any value."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "work/analysis/promotion_v4186"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    plan_path = AUDIT / "mutation_plan.json"
    original = plan_path.read_bytes()
    preserved = AUDIT / "mutation_plan.original_LF.json"
    assert not preserved.exists()
    plan = json.loads(original)
    corrections = []
    for index, entry in enumerate(plan):
        target = Path(entry["target"])
        before = (AUDIT / (str(index) + ".before")).read_bytes()
        if target.suffix != ".json" or before.count(b"\r\n") != before.count(b"\n"):
            continue
        current = target.read_bytes()
        assert sha(current) == entry["planned_sha256"]
        corrected = current.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        assert json.loads(corrected) == json.loads(current)
        destination = AUDIT / "staged" / (str(index) + ".preserved_CRLF")
        destination.write_bytes(corrected)
        corrections.append({"target": str(target), "before_sha256": sha(current),
                            "planned": str(destination), "planned_sha256": sha(corrected)})
        entry["planned"] = str(destination)
        entry["planned_sha256"] = sha(corrected)
    assert len(corrections) == 4
    preserved.write_bytes(original)
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    (AUDIT / "newline_correction_plan.json").write_text(json.dumps(corrections, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"existing_JSON_CRLF_format_preserved": len(corrections), "semantic_changes": 0}))


if __name__ == "__main__":
    main()
