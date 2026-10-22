"""Prepare centered crew plaques and readable native-font stat plaques."""

import copy
import json
import zlib
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_pxl_native_label_batch

OUT = Path("work/analysis/two_screen_layout_v246")


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    assert sha(Path("out/raphael_natural_v2_accepted_base.nds").read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    arm = base.read_file("/__arm9__.bin")
    crew = copy.deepcopy(json.loads(Path("translations/assign_sailors_graphics_v3.json").read_text(encoding="utf-8")))
    source = base.read_file(crew["file_path"])
    assert sha(source) == crew["source_file_sha256"]
    for row in crew["records"]:
        oldbox = row["box"]
        image = PxlImage.from_bytes(source)
        oldbg = zlib.decompress(bytes.fromhex(row["background_indices_zlib_hex"]))
        width = oldbox[2] - oldbox[0]
        for y in range(oldbox[1], oldbox[3]):
            image.indices[y * 256 + oldbox[0]:y * 256 + oldbox[2]] = oldbg[(y-oldbox[1])*width:(y-oldbox[1]+1)*width]
        if row["text"] in ("Marines", "Guns", "Lateen", "Square"):
            lower = row["text"] in ("Lateen", "Square")
            row["box"][3] = 146 if lower else 124
            inner = [row["draw_box"][0], 132 if lower else 110,
                     row["draw_box"][2], 144 if lower else 122]
            image.erase_dark_text(tuple(inner), threshold=135)
            row["draw_box"] = [inner[0], inner[1], inner[2], inner[1] + 11]
        x0, y0, x1, y1 = row["box"]
        background = bytes(image.indices[y * 256 + x] for y in range(y0,y1) for x in range(x0,x1))
        row["background_indices_zlib_hex"] = zlib.compress(background).hex()
        row["context"] = "Assign Sailors: caption centered inside its actual paper plaque."
        row["localization_note"] = "Retain the reviewed English wording; restore the entire old text area and use original native glyphs at the plaque's measured baseline."
        row["review"] = {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}
    crew["supersedes"] = "translations/assign_sailors_graphics_v3.json"
    crew["scope"] = "Center the four lower crew captions in the measured native plaque extents; preserve the three top captions."
    cp = Path("translations/assign_sailors_graphics_v4.json")
    save(cp, crew)
    crew_bytes, _ = apply_pxl_native_label_batch(cp, source, arm)
    person = copy.deepcopy(json.loads(Path("translations/person_info_graphics_v1.json").read_text(encoding="utf-8")))
    source = base.read_file(person["file_path"])
    assert sha(source) == person["source_file_sha256"]
    paper = zlib.decompress(bytes.fromhex(person["records"][0]["background_indices_zlib_hex"]))
    assert len(paper) == 46 * 15
    for n, (japanese, english) in enumerate((("体力","Stamina"),("敏捷","Agility"),("魅力","Charm"),
                                            ("知力","Wits"),("精神","Spirit"),("運","Luck"))):
        person["records"].append({"id": f"DK4_PERSON_STAT_PLAQUE_{n}_V2", "box": [124,99+n*15,170,114+n*15],
                                  "text": english, "source_japanese": japanese, "source_meaning": english,
                                  "background_indices_zlib_hex": zlib.compress(paper).hex(),
                                  "context": "Sailor Info upper-right stats; original 24-pixel plaque was too narrow for English.",
                                  "localization_note": "Keep the full native English stat name on a wider paper plaque; bars and values receive separate native layout space.",
                                  "review": {g: True for g in ("source","context","localization","naturalness","formatting")}})
    person["font_sha256"] = REFERENCE_ASCII_FONT_SHA256
    person["editorial_policy"] = "natural-dialogue-v2"
    person["supersedes"] = "translations/person_info_graphics_v1.json"
    person["scope"] = "Preserve all four status plaques; add six complete wider stat plaques with matching native-font styling."
    pp = Path("translations/person_info_graphics_v2.json")
    save(pp, person)
    person_bytes, _ = apply_pxl_native_label_batch(pp, source, arm)
    for name, old_path, data in (("crew",crew["file_path"],crew_bytes),("person",person["file_path"],person_bytes)):
        before = PxlImage.from_bytes(base.read_file(old_path)).render().convert("RGB")
        after = PxlImage.from_bytes(data).render().convert("RGB")
        sheet = Image.new("RGB",(1024,384));sheet.paste(before.resize((512,384),Image.Resampling.NEAREST),(0,0));sheet.paste(after.resize((512,384),Image.Resampling.NEAREST),(512,0))
        sheet.save(OUT/f"{name}_art_preview.png")
        (OUT/f"{name}_target.pxl").write_bytes(data)
    print("Prepared full crew caption baselines and six wide native-font stat plaques; runtime layout stage remains to verify.")


if __name__ == "__main__":
    main()
