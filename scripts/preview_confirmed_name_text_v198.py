"""Render passing migration layouts with explicit default-name preview expansions."""

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/confirmed_names_v198")
OUT = Path("work/qa/confirmed_names_v198")
DEFAULTS = {
    "/data/SC0.DK4": {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co.", "FU": "Rafael Castor"},
    "/data/SC1.DK4": {"FI": "Hodram", "FA": "Bergstrom", "FO": "Bergstrom Fleet"},
    "/data/SC2.DK4": {"FI": "Lil", "FA": "Argot", "FO": "Argot Co."},
    "/data/SC3.DK4": {"FI": "Maria", "FA": "Li", "FO": "Li Clan"},
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    preparation = json.loads((ROOT / "confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    report = json.loads((ROOT / "text_preparation_report.json").read_text(encoding="utf-8"))
    checks = {(r["file_path"], r["id"]): r for r in report["checks"]}
    arm9 = NdsImage.open("out/all_routes_combined_v190_candidate.nds").read_file("/__arm9__.bin")
    images = []
    for row in preparation["records"]:
        check = checks[row["file_path"], row["id"]]
        if "audit" not in check or check["encoding_errors"]:
            continue
        payload = dict(preparation["proposed_profiles_not_registered"][row["proposed_profile"]])
        payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
        profile = DialogueProfile(**payload)
        markup = check["audit"]["formatted_markup"]
        used = {}

        def expand(match, defaults=DEFAULTS[row["file_path"]], profile=profile, used=used):
            name = match[1]
            text = defaults[name]
            if len(text) != profile.macro_ascii_lengths[name] or profile.macro_width(name) != len(text) * 6:
                raise ValueError("Declared default macro text does not match the formatting calibration")
            used[name] = text
            return text

        expanded = re.sub(r"\{MACRO:(FI|FA|FO|FU)\}", expand, markup)
        path = OUT / (row["file_path"].split("/")[-1].replace(".", "_") + "_" + row["id"] + ".png")
        render_dialogue_preview(expanded, profile, path, arm9=arm9)
        images.append({"file_path": row["file_path"], "id": row["id"], "path": path.as_posix(),
                       "sha256": sha(path.read_bytes()), "declared_default_expansions": used,
                       "phase_recovery": check.get("phase_auto_wrap_recovered_by_formatter", False)})
    # Risk-focused first sheet, followed by the complete remaining collection.
    images.sort(key=lambda row: (not row["phase_recovery"], row["file_path"], row["id"]))
    sheets = []
    for start in range(0, len(images), 12):
        group = images[start:start + 12]
        opened = [Image.open(row["path"]).convert("RGB") for row in group]
        width = max(i.width for i in opened)
        height = max(i.height for i in opened) + 24
        sheet = Image.new("RGB", (width * 3, height * 4), "#303030")
        draw = ImageDraw.Draw(sheet)
        for index, (row, im) in enumerate(zip(group, opened, strict=True)):
            x, y = index % 3 * width, index // 3 * height
            draw.text((x + 3, y + 3), row["file_path"].split("/")[-1] + " " + row["id"], fill="white")
            sheet.paste(im, (x, y + 24))
        path = OUT / f"review_{start // 12:02d}.png"
        sheet.save(path)
        sheets.append({"path": path.as_posix(), "sha256": sha(path.read_bytes()),
                       "records": [{"file_path": r["file_path"], "id": r["id"]} for r in group],
                       "visually_reviewed": False})
    result = {"format": "dk4-confirmed-name-preview-inventory-v1", "images": images, "sheets": sheets,
              "record_count": len(images), "all_visual_reviews_complete": False,
              "scope": "Offline layout/native ASCII glyph previews with declared default macro text; not live expansion, GPU or timing proof.",
              "editorial_review_gates_still_false": True, "playable_ROM_modified": False}
    (ROOT / "preview_inventory.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"previews": len(images), "sheets": len(sheets), "visual_review_pending": True}))


if __name__ == "__main__":
    main()
