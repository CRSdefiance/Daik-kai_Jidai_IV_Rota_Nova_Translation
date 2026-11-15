"""Audit reviewed prose against immutable allocation and confirmed-name profiles."""

import argparse
import json
import re
from dataclasses import asdict, replace
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record, audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/name_editorial_v232")
OUT = Path("work/qa/name_editorial_v232")
MANUSCRIPT = Path("translations/confirmed_name_route_editorial_v232.json")
DEFAULTS = {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co.", "FU": "Rafael Castor"}


def safe_literal_markup(english):
    # Existing engine-compatible full-width glyphs represent literal I/F.
    # Preserve author prose and every control/macro token. This is a research
    # serialization step, not an instruction to make the English unnatural.
    return "".join(part if part.startswith("{") else part.replace("I", "Ｉ").replace("F", "Ｆ")
                   for part in re.split(r"(\{[^}]+\})", english))


def main():
    global ROOT, OUT, MANUSCRIPT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, default=MANUSCRIPT)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    ROOT, OUT, MANUSCRIPT = args.root, args.out, args.manuscript
    ROOT.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    reviewed = json.loads(MANUSCRIPT.read_text(encoding="utf-8"))
    prepared = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    drafts = {(r["file_path"], r["id"]): r for r in prepared["records"]}
    current = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    arm, font = current.read_file("/__arm9__.bin"), current.read_file("/GRP/KANJI.FNT")
    checks, pictures = [], []
    for row in reviewed["records"]:
        original = drafts.get((row["file_path"], row["id"]))
        if original is None:
            if not row.get("related_scene_dependency"):
                raise ValueError("Unknown source owner lacks explicit related-scene provenance")
            canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
            from dk4tool.formats.ilnk import IlnkContainer
            blocks = IlnkContainer.parse(canonical.read_file(row["file_path"])).blocks
            block_id = int(row["id"].split("_B")[1].split("_")[0])
            record_id = int(row["id"].split("_R")[1])
            canonical_source = blocks[block_id].split(b"\0")[record_id]
            if canonical_source != bytes.fromhex(row["expected_source_hex"]):
                raise ValueError("Related-scene canonical source lock differs")
            original = {"source_hex": row["expected_source_hex"], "proposed_profile": row["proposed_profile_hint"]}
        if row["expected_source_hex"] != original["source_hex"]:
            raise ValueError("Reviewed canonical allocation lock differs")
        payload = dict(prepared["proposed_profiles_not_registered"][original["proposed_profile"]])
        payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
        profile = replace(DialogueProfile(**payload), balanced_wrapping=True,
                          name=payload["name"] + "-editorial-v232")
        safe = safe_literal_markup(row["english"])
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["expected_source_hex"]), safe, profile)
        blockers = [issue for issue in audit["issues"] if issue["severity"] in {"error", "warning"}]
        result = {"id": row["id"], "source_hex": row["expected_source_hex"], "english": row["english"],
                  "profile": asdict(profile), "encoded_literal_safe_markup": safe,
                  "audit": audit, "blockers": blockers,
                  "new_English_not_shortened_to_improve_allocation": True}
        result["profile"]["leading_speaker_bytes"] = sorted(profile.leading_speaker_bytes)
        preview_audit = audit
        if blockers and all(issue["severity"] == "error" and "byte-overflow" in issue["message"] for issue in blockers):
            private = safe.removesuffix("{PAD}")
            preview_audit = audit_relocatable_dialogue_record(bytes.fromhex(row["expected_source_hex"]), private, profile)
            private_blockers = [issue for issue in preview_audit["issues"] if issue["severity"] in {"error", "warning"}]
            result["private_catalog_allocation_audit"] = preview_audit
            result["private_catalog_allocation_blockers"] = private_blockers
            if not private_blockers:
                encoded = encode_relocatable_dialogue(bytes.fromhex(row["expected_source_hex"]), private, profile)
                result["private_message_catalog_payload_hex"] = encoded.encoded.hex().upper()
                result["private_pool_allocation_required"] = True
        if not blockers or (result.get("private_pool_allocation_required") and not result["private_catalog_allocation_blockers"]):
            def expand(match, profile=profile):
                name = match[1]
                text = DEFAULTS[name]
                if len(text) != profile.macro_ascii_lengths[name] or len(text) * 6 != profile.macro_width(name):
                    raise ValueError("Confirmed default-name bytes/width differ from the profile")
                return text

            expanded = re.sub(r"\{MACRO:(FI|FA|FO|FU)\}", expand, preview_audit["formatted_markup"])
            path = OUT / (row["id"] + ".png")
            render_dialogue_preview(expanded, profile, path, arm9=arm, kanji_font=font)
            result.update({"preview": path.as_posix(), "preview_sha256": sha(path.read_bytes()),
                           "declared_default_expansions": DEFAULTS, "visual_review_complete": False})
            pictures.append(result)
        checks.append(result)
    sheets = []
    for start in range(0, len(pictures), 8):
        group = pictures[start:start + 8]
        opened = [Image.open(row["preview"]).convert("RGB") for row in group]
        cell_width = max(preview.width for preview in opened) + 8
        cell_height = max(preview.height for preview in opened) + 24
        image = Image.new("RGB", (cell_width * 2, cell_height * 4), "#eeeeee")
        draw = ImageDraw.Draw(image)
        for index, (row, preview) in enumerate(zip(group, opened, strict=True)):
            x, y = index % 2 * cell_width, index // 2 * cell_height
            draw.text((x + 2, y + 2), row["id"], fill="black")
            image.paste(preview, (x + 2, y + 20))
        path = OUT / f"sheet_{start // 8}.png"
        image.save(path)
        sheets.append({"path": path.as_posix(), "sha256": sha(path.read_bytes()),
                       "records": [row["id"] for row in group], "visual_review_complete": False})
    result = {"format": "dk4-confirmed-name-editorial-formatting-v232", "manuscript_sha256": sha(MANUSCRIPT.read_bytes()),
              "checks": checks, "source_reviewed_records": len(checks),
              "fixed_allocation_zero_blocker_records": sum(not row["blockers"] for row in checks),
              "fixed_or_private_allocation_zero_blocker_previews": len(pictures),
              "records_requiring_allocation_or_formatting_work": [row["id"] for row in checks if row["blockers"]],
              "review_sheets": sheets, "not_a_release_batch": True,
              "native_expansion_scene_flow_and_physical_display_pending": True, "ROM_modified": False}
    (ROOT / "formatting_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_reviewed": len(checks), "zero_blocker_previews": len(pictures),
                      "private_catalog_allocations_needed": sum(row.get("private_pool_allocation_required", False) for row in checks),
                      "blocked_records": [{"id": row["id"], "issues": row["blockers"]} for row in checks if row["blockers"]],
                      "sheets": len(sheets), "ROM_modified": False}))


if __name__ == "__main__":
    main()
