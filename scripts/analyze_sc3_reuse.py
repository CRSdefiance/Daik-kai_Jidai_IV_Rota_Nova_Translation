from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
TRANSLATIONS = ROOT / "translations"
RELEASE_STACK = TRANSLATIONS / "release_stack.json"
SOURCE_PROFILES = (
    "raphael-deep-route-v93",
    "hodram-deep-route-v32",
    "lil-deep-route-v21",
)
ROUTE_PATHS = ("/data/SC0.DK4", "/data/SC1.DK4", "/data/SC2.DK4")
SC3_PATH = "/data/SC3.DK4"
ROUTE_CSV = {
    "/data/SC0.DK4": WORK / "sc0" / "script.csv",
    "/data/SC1.DK4": WORK / "sc1" / "script.csv",
    "/data/SC2.DK4": WORK / "sc2" / "script.csv",
    SC3_PATH: WORK / "sc3" / "script.csv",
}
SPEAKER_RE = re.compile(r"^\{SPEAKER:[0-9A-Fa-f]{2}\}")
MARKUP_RE = re.compile(r"\{(?:LB|PAD)\}")
MACRO_PREFIX_RE = re.compile(r"^(?:FI|FA|FO|I)(?=[^A-Za-z]|$)")


def read_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return {row["id"]: row for row in csv.DictReader(stream)}


def is_japanese(character: str) -> bool:
    codepoint = ord(character)
    return (
        0x3040 <= codepoint <= 0x30FF
        or 0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or 0xFF66 <= codepoint <= 0xFF9F
    )


def canonical_japanese(value: str) -> str:
    """Return a conservative speaker-independent source key.

    MESFILE exports retain the one-byte presentation state as the first decoded
    character.  It can appear as a C0 control, printable ASCII, or half-width
    katakana.  Remove exactly one such byte only when the remainder begins with
    Japanese prose, a route macro, a line-break token, or Japanese punctuation.
    The rest of the source is normalized only for authored line breaks and spaces.
    """

    text = value.strip()
    if not text:
        return text
    if len(text) > 1:
        remainder = text[1:]
        first = text[0]
        remainder_is_text = (
            is_japanese(remainder[0])
            or remainder.startswith("{LB}")
            or bool(MACRO_PREFIX_RE.match(remainder))
            or remainder[0] in "『「（…！？＜・"
        )
        first_is_state = (
            ord(first) < 0x20
            or (ord(first) < 0x80 and not first.isdigit())
            or 0xFF66 <= ord(first) <= 0xFF9F
            or unicodedata.category(first).startswith("C")
        )
        if first_is_state and remainder_is_text:
            text = remainder
    text = text.replace("{LB}", " ")
    return re.sub(r"\s+", " ", text).strip()


def canonical_english(value: str) -> str:
    text = SPEAKER_RE.sub("", value.strip(), count=1)
    text = MARKUP_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def translated_sources() -> list[dict[str, object]]:
    source_rows = {path: read_csv(csv_path) for path, csv_path in ROUTE_CSV.items()}
    stack = json.loads(RELEASE_STACK.read_text(encoding="utf-8"))
    profile_batches = {
        ROOT / batch
        for profile_name in SOURCE_PROFILES
        for batch in stack["profiles"][profile_name]["batches"]
    }
    records: list[dict[str, object]] = []
    for batch_path in sorted(profile_batches):
        try:
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        file_path = batch.get("file_path")
        if file_path not in ROUTE_PATHS or not isinstance(batch.get("records"), list):
            continue
        for record in batch["records"]:
            row_id = str(record.get("id", ""))
            english = str(record.get("english", ""))
            row = source_rows[file_path].get(row_id)
            if not row or not english:
                continue
            source_key = canonical_japanese(row["japanese"])
            english_key = canonical_english(english)
            if not source_key or not english_key:
                continue
            records.append(
                {
                    "source_file": file_path,
                    "source_id": row_id,
                    "source_batch": batch_path.name,
                    "japanese": row["japanese"],
                    "source_key": source_key,
                    "english": english,
                    "english_key": english_key,
                    "speaker": record.get("speaker", ""),
                    "source_meaning": record.get("source_meaning", ""),
                    "localization_note": record.get("localization_note", ""),
                }
            )
    return records


def main() -> None:
    sc3_rows = read_csv(ROUTE_CSV[SC3_PATH])
    translated = translated_sources()
    by_source: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in translated:
        by_source[str(record["source_key"])].append(record)

    reusable: list[dict[str, object]] = []
    conflicts: list[dict[str, object]] = []
    unmatched: list[dict[str, object]] = []
    block_counts: Counter[int] = Counter()
    block_reused: Counter[int] = Counter()
    for row_id, row in sc3_rows.items():
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[block] += 1
        key = canonical_japanese(row["japanese"])
        candidates = by_source.get(key, [])
        if not candidates:
            unmatched.append({"id": row_id, "block": block, "japanese": row["japanese"], "source_key": key})
            continue
        variants: dict[str, list[dict[str, object]]] = defaultdict(list)
        for candidate in candidates:
            variants[str(candidate["english_key"])].append(candidate)
        item = {
            "id": row_id,
            "block": block,
            "japanese": row["japanese"],
            "source_key": key,
            "variants": [
                {
                    "english": english,
                    "sources": [
                        {
                            "file": source["source_file"],
                            "id": source["source_id"],
                            "batch": source["source_batch"],
                            "speaker": source["speaker"],
                        }
                        for source in sources
                    ],
                }
                for english, sources in sorted(variants.items())
            ],
        }
        if len(variants) == 1:
            reusable.append(item)
            block_reused[block] += 1
        else:
            conflicts.append(item)

    report = {
        "format": "dk4-sc3-cross-route-reuse-audit-v1",
        "sc3_record_count": len(sc3_rows),
        "translated_source_record_count": len(translated),
        "source_profiles": list(SOURCE_PROFILES),
        "unique_reusable_count": len(reusable),
        "conflicting_translation_count": len(conflicts),
        "unmatched_count": len(unmatched),
        "blocks": [
            {
                "block": block,
                "records": block_counts[block],
                "unique_reusable": block_reused[block],
                "coverage_percent": round(100.0 * block_reused[block] / block_counts[block], 1),
            }
            for block in sorted(block_counts)
        ],
        "reusable": reusable,
        "conflicts": conflicts,
        "unmatched": unmatched,
    }
    output = WORK / "analysis" / "sc3_cross_route_reuse.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "sc3_record_count": report["sc3_record_count"],
                "translated_source_record_count": report["translated_source_record_count"],
                "unique_reusable_count": report["unique_reusable_count"],
                "conflicting_translation_count": report["conflicting_translation_count"],
                "unmatched_count": report["unmatched_count"],
                "best_blocks": sorted(
                    report["blocks"], key=lambda item: (-item["unique_reusable"], item["block"])
                )[:25],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
