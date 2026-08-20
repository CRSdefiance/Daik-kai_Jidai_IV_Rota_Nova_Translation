from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

from dk4tool.dialogue.codec import parse_markup, tokenize_raw, tokens_to_markup
from dk4tool.dialogue.layout import format_markup
from dk4tool.dialogue.preview import visible_lines
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_relocatable_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows

CANONICAL_ROM_SHA256 = (
    "fe7cdcaf7cfa24f18c1c48608ddddf58dc9a7555cb93c8131163037e814c8586"
)
SC0_PATH = "/data/SC0.DK4"
BLOCK_INDEX = 44
EXCLUDED_STATUSES = {
    "accepted-opening-verbatim",
    "non-prose-control-fragment",
    "translated-control-blocked",
}
FIXED_LAYOUT_RECORDS = {
    "DK4_MES_B44_R0454",
    "DK4_MES_B44_R0456",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: JSON root must be an object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Materialize the reviewed Raphael Lisbon manuscript as an experimental "
            "parity-preserving relocation batch against the accepted baseline."
        )
    )
    parser.add_argument(
        "--rom",
        type=Path,
        default=Path("out/raphael_natural_v2_pre_lisbon_accepted_rollback.nds"),
    )
    parser.add_argument(
        "--manuscript",
        type=Path,
        default=Path("translations/drafts/raphael_intro_lisbon_sol_v1.json"),
    )
    parser.add_argument(
        "--overrides",
        type=Path,
        default=Path(
            "translations/drafts/raphael_intro_lisbon_encoding_overrides_v1.json"
        ),
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path(
            "translations/drafts/raphael_natural_english_editorial_draft_v1.json"
        ),
    )
    parser.add_argument(
        "--batch-out",
        type=Path,
        default=Path("translations/raphael_intro_lisbon_natural_relocatable_v1.json"),
    )
    parser.add_argument(
        "--map-out",
        type=Path,
        default=Path("translations/sc0_b44_lisbon_parity_relocation_map.json"),
    )
    args = parser.parse_args()

    rom_data = args.rom.read_bytes()
    if sha256(rom_data) != CANONICAL_ROM_SHA256:
        raise SystemExit("refusing to materialize from a noncanonical ROM")
    manuscript = load_json(args.manuscript)
    overrides = load_json(args.overrides)
    metadata = load_json(args.metadata)
    override_by_id = {
        str(record["id"]): str(record["english"])
        for record in overrides.get("records", [])
        if isinstance(record, dict)
    }
    metadata_by_id = {
        str(record["id"]): record
        for record in metadata.get("records", [])
        if isinstance(record, dict)
    }

    image = NdsImage.open(args.rom)
    source_file = image.read_file(SC0_PATH)
    source_rows = export_mesfile_rows(
        source_file, SC0_PATH, include_non_japanese=True
    )
    source_by_id = {str(row["id"]): row for row in source_rows}
    container = IlnkContainer.parse(source_file)
    source_block = container.blocks[BLOCK_INDEX]
    if source_block[:4] != b"CS\0\x01":
        raise SystemExit("accepted block 44 is not a CS v1 script")
    source_body_size = struct.unpack_from("<H", source_block, 4)[0]
    logical_end = 8 + source_body_size
    if logical_end > len(source_block) or any(source_block[logical_end:]):
        raise SystemExit("accepted block 44 has invalid length or alignment padding")

    profile = get_dialogue_profile("raphael-story-live")
    records: list[dict[str, object]] = []
    segments: list[int] = []
    used_overrides: set[str] = set()
    issues: list[str] = []
    for record in manuscript.get("records", []):
        if not isinstance(record, dict):
            raise TypeError("manuscript record must be an object")
        row_id = str(record["id"])
        status = str(record["status"])
        if row_id in FIXED_LAYOUT_RECORDS:
            continue
        if status in EXCLUDED_STATUSES:
            continue
        if status != "translated":
            raise SystemExit(f"{row_id}: unsupported manuscript status {status!r}")
        source_row = source_by_id[row_id]
        parts = str(source_row["pointer_group"]).split(":")
        if len(parts) != 3 or int(parts[1]) != BLOCK_INDEX:
            raise SystemExit(f"{row_id}: record is outside block 44")
        segment_index = int(parts[2])
        source_raw = bytes.fromhex(str(source_row["source_hex"]))
        source_tokens = tokenize_raw(
            source_raw, leading_speaker_bytes=profile.leading_speaker_bytes
        )
        unknown = [token for token in source_tokens if token.kind == "raw_control"]
        if unknown:
            raise SystemExit(f"{row_id}: accepted source contains unmapped controls")
        speaker_prefix = tokens_to_markup(
            [token for token in source_tokens if token.kind == "speaker"]
        )
        prose = override_by_id.get(row_id, str(record["natural_english"]))
        if row_id in override_by_id:
            used_overrides.add(row_id)
        target = speaker_prefix + prose
        audit = audit_relocatable_dialogue_record(source_raw, target, profile)
        blocking = [
            item
            for item in audit["issues"]
            if item["severity"] in {"error", "warning"}
        ]
        if blocking:
            formatted_lines = audit["visible_lines"]
            if not formatted_lines:
                formatted_lines = visible_lines(
                    parse_markup(format_markup(target, profile))
                )
            issues.append(
                row_id
                + ": "
                + "; ".join(
                    f"{item['severity']}:{item['code']}:{item['message']}"
                    for item in blocking
                )
                + " | lines="
                + " / ".join(str(line) for line in formatted_lines)
            )
            continue
        meta = metadata_by_id[row_id]
        records.append(
            {
                "id": row_id,
                "english": target,
                "speaker": record["speaker"],
                "context": meta["scene_context"],
                "source_meaning": meta["source_meaning"],
                "localization_note": (
                    "Source-first Sol localization. Build-facing wording preserves "
                    "the full meaning while honoring the renderer's literal F/I macro "
                    "restriction; layout is automatic and parity is structural."
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )
        segments.append(segment_index)

    unused_overrides = set(override_by_id) - used_overrides
    if unused_overrides:
        issues.append("unused overrides: " + ", ".join(sorted(unused_overrides)))
    if issues:
        raise SystemExit("materialization blocked:\n" + "\n".join(issues))
    if len(records) != 106 or len(segments) != len(set(segments)):
        raise SystemExit(
            f"expected 106 unique relocatable translated records, got {len(records)}"
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": SC0_PATH,
        "source_file_sha256": sha256(source_file),
        "encoder": "dialogue-relocatable-v1",
        "dialogue_profile": "raphael-story-live",
        "relocation_map": args.map_out.as_posix(),
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "editorial_source": args.manuscript.as_posix(),
        "editorial_source_sha256": sha256(args.manuscript.read_bytes()),
        "encoding_overrides": args.overrides.as_posix(),
        "encoding_overrides_sha256": sha256(args.overrides.read_bytes()),
        "records": records,
    }
    relocation_map = {
        "format": "dk4-cs-relocation-map-v1",
        "file_path": SC0_PATH,
        "source_file_sha256": sha256(source_file),
        "block_index": BLOCK_INDEX,
        "source_block_sha256": sha256(source_block),
        "source_block_size": len(source_block),
        "source_cs_body_size": source_body_size,
        "movable_segments": segments,
        "required_segments": segments,
        "external_references_complete": True,
        "preserve_record_parity": True,
        "parity_mismatch_policy": "append-single-space",
        "status": "experimental-cold-boot-required",
        "proof_scope": (
            "Accepted block-44 source; 106 relocatable post-opening prose records; "
            "two fixed-offset choice records are handled by an exact-allocation batch; "
            "five accepted opening records and two unmapped control records unchanged."
        ),
        "proof_basis": [
            "The accepted five-record probe established that every resized CS dialogue record must preserve its original odd/even byte phase.",
            "The ROM-wide static scan found no persistent component/file pointer to an interior block-44 dialogue segment; the ILNK header is rebuilt mechanically.",
            "The aligned-value scan found no verified interior dialogue-entry pointer; candidate values target empty or command-adjacent segments and are retained byte-for-byte.",
            "Every non-target segment remains byte-identical and the builder records each structural parity byte.",
            "Cold-boot testing proved that choice records 454 and 456 use fixed interior offsets; they are forbidden from this relocation map.",
            "Runtime control flow remains experimental until the user cold-boots both tutorial-choice branches through the Lisbon handoff."
        ],
    }

    args.batch_out.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.map_out.write_text(
        json.dumps(relocation_map, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "batch": args.batch_out.as_posix(),
                "map": args.map_out.as_posix(),
                "records": len(records),
                "source_file_sha256": sha256(source_file),
                "source_block_sha256": sha256(source_block),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
