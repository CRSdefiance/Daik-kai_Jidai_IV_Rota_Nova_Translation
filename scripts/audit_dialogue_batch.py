from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import (
    audit_fixed_dialogue_record,
    audit_relocatable_dialogue_record,
)
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows
from dk4tool.script.translation_batch import materialize_translation_batch


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit every record in a natural-dialogue batch and render previews."
    )
    parser.add_argument(
        "--rom", type=Path, required=True, help="Source-locked canonical baseline ROM"
    )
    parser.add_argument(
        "--japanese-rom",
        type=Path,
        help="Optional clean Japanese ROM used only for source/context reporting",
    )
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="Do not fail the command for unwaived editorial warnings",
    )
    args = parser.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    if not isinstance(batch, dict):
        raise TypeError("translation batch root must be an object")
    validate_natural_dialogue_batch(batch)
    image = NdsImage.open(args.rom)
    file_path = str(batch.get("file_path", ""))
    source_data = image.read_file(file_path)
    arm9 = image.read_file("/__arm9__.bin")
    profile = get_dialogue_profile(str(batch.get("dialogue_profile", "story")))
    rows = materialize_translation_batch(batch, source_data)
    japanese_by_id: dict[str, str] = {}
    if args.japanese_rom:
        japanese_image = NdsImage.open(args.japanese_rom)
        japanese_by_id = {
            str(row["id"]): str(row["japanese"])
            for row in export_mesfile_rows(
                japanese_image.read_file(file_path), file_path, include_non_japanese=True
            )
        }
    source_records = {
        str(record["id"]): record
        for record in batch.get("records", [])
        if isinstance(record, dict)
    }

    args.out.mkdir(parents=True, exist_ok=True)
    preview_dir = args.out / "previews"
    records: list[dict[str, object]] = []
    blocking = 0
    for row in rows:
        row_id = str(row["id"])
        authored = source_records[row_id]
        audit_function = (
            audit_relocatable_dialogue_record
            if batch.get("encoder") == "dialogue-relocatable-v1"
            else audit_fixed_dialogue_record
        )
        audit = audit_function(
            bytes.fromhex(str(row["source_hex"])),
            str(row["english"]),
            profile,
        )
        waivers = {
            str(value) for value in authored.get("qa_waivers", [])
        } if isinstance(authored.get("qa_waivers", []), list) else set()
        unwaived = [
            issue
            for issue in audit["issues"]
            if issue["severity"] == "error"
            or (issue["severity"] == "warning" and issue["code"] not in waivers)
        ]
        blocking += len(unwaived)
        preview_path = preview_dir / f"{row_id}.png"
        if audit["formatted_markup"]:
            render_dialogue_preview(
                str(audit["formatted_markup"]), profile, preview_path, arm9=arm9
            )
        records.append(
            {
                "id": row_id,
                "japanese": japanese_by_id.get(row_id, row["japanese"]),
                "speaker": authored.get("speaker", ""),
                "context": authored.get("context", ""),
                "target_markup": row["english"],
                "qa_waivers": sorted(waivers),
                "preview": preview_path.relative_to(args.out).as_posix()
                if preview_path.exists()
                else None,
                **audit,
            }
        )

    report = {
        "format": "dk4-dialogue-qa-report-v1",
        "batch": args.batch.as_posix(),
        "profile": profile.name,
        "metrics_source": profile.metrics_source,
        "record_count": len(records),
        "blocking_issue_count": blocking,
        "records": records,
    }
    (args.out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    markdown = [
        f"# Dialogue QA: {args.batch.name}",
        "",
        f"- Profile: `{profile.name}`",
        f"- Records: {len(records)}",
        f"- Blocking issues: {blocking}",
        f"- Native continuation indent: {profile.glyph_width(' ') if profile.guard_linebreaks else 0}px",
        "",
        "| Record | Speaker | Formatted lines | Padding | Issues | Preview |",
        "|---|---|---|---:|---|---|",
    ]
    for record in records:
        issue_text = "; ".join(
            f"{issue['severity']}:{issue['code']}" for issue in record["issues"]
        ) or "none"
        lines = " / ".join(str(value) for value in record["visible_lines"])
        preview = f"[PNG]({record['preview']})" if record["preview"] else "n/a"
        markdown.append(
            "| "
            + " | ".join(
                _markdown_cell(value)
                for value in (
                    record["id"],
                    record["speaker"],
                    lines,
                    record["padding_bytes"],
                    issue_text,
                    preview,
                )
            )
            + " |"
        )
    (args.out / "summary.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")

    if blocking and not args.allow_warnings:
        raise SystemExit(
            f"dialogue QA failed with {blocking} unwaived error/warning issue(s); "
            f"see {args.out / 'summary.md'}"
        )


if __name__ == "__main__":
    main()
