"""Render the complete catalog targets with calibrated default name expansions."""

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.preview_confirmed_name_text_v198 import DEFAULTS

ROOT = Path("work/analysis/confirmed_names_v200")
OUT = Path("work/qa/confirmed_names_v200")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    plan = json.loads((args.root / "catalog_plan.json").read_text(encoding="utf-8"))
    preparation = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    drafts = {(r["file_path"], r["id"]): r for r in preparation["records"]}
    arm9 = NdsImage.open("out/all_routes_combined_v190_candidate.nds").read_file("/__arm9__.bin")
    images = []
    for row in plan["prepared_records"]:
        draft = drafts[row["file_path"], row["id"]]
        payload = dict(preparation["proposed_profiles_not_registered"][draft["proposed_profile"]])
        payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
        profile = DialogueProfile(**payload)
        result = encode_relocatable_dialogue(bytes.fromhex(row["canonical_source_hex"]), row["english"].removesuffix("{PAD}"), profile)
        assert result.encoded.hex() == row["encoded_translation_hex"]
        used = {}

        def expand(match, defaults=DEFAULTS[row["file_path"]], profile=profile, used=used):
            name = match[1]
            text = defaults[name]
            if len(text) != profile.macro_ascii_lengths[name] or profile.macro_width(name) != len(text) * 6:
                raise ValueError("Default preview expansion disagrees with calibrated length/width")
            used[name] = text
            return text

        expanded = re.sub(r"\{MACRO:(FI|FA|FO|FU)\}", expand, result.formatted_markup)
        path = args.out / (row["file_path"].split("/")[-1].replace(".", "_") + "_" + row["id"] + ".png")
        render_dialogue_preview(expanded, profile, path, arm9=arm9)
        images.append({"file_path": row["file_path"], "id": row["id"], "path": path.as_posix(),
                       "sha256": sha(path.read_bytes()), "source_slot_bytes": row["source_slot_bytes"],
                       "full_translation_bytes": len(result.encoded), "formatted_markup": result.formatted_markup,
                       "declared_default_expansions": used, "individual_visual_review_complete": False})
    sheets = []
    for start in range(0, len(images), 6):
        group = images[start:start + 6]
        opened = []
        for row in group:
            with Image.open(row["path"]) as im:
                opened.append(im.convert("RGB"))
        width = max(im.width for im in opened)
        height = max(im.height for im in opened) + 24
        sheet = Image.new("RGB", (width * 2, height * 3), "#303030")
        draw = ImageDraw.Draw(sheet)
        for index, (row, im) in enumerate(zip(group, opened, strict=True)):
            x, y = index % 2 * width, index // 2 * height
            draw.text((x + 3, y + 3), row["file_path"].split("/")[-1] + " " + row["id"], fill="white")
            sheet.paste(im, (x, y + 24))
        path = args.out / f"review_{start // 6:02d}.png"
        sheet.save(path)
        sheets.append({"path": path.as_posix(), "sha256": sha(path.read_bytes()),
                       "records": [{"file_path": r["file_path"], "id": r["id"]} for r in group],
                       "visually_reviewed": False})
    report = {"format": "dk4-confirmed-name-catalog-preview-inventory-v1", "images": images, "sheets": sheets,
              "record_count": len(images), "all_visual_reviews_complete": False,
              "scope": "Offline complete target layout/native font with calibrated default expansions; original deep-scene GPU/control verification remains pending.",
              "editorial_review_complete": False, "research_only": True, "playable_ROM_modified": False}
    (args.root / "preview_inventory.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_name_previews": len(images), "sheets": len(sheets)}))


if __name__ == "__main__":
    main()
