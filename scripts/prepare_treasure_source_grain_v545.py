"""Review and register original visible grain for the Treasure Name header."""

import copy
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.treasure_source_grain import BOX, PATH, transform
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/treasure_texture_v545")


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open("out/all_routes_combined_v544_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    source, original = current.read_file(PATH), clean.read_file(PATH)
    result, plan = transform(source, original)
    old, new, jp = [PxlImage.from_bytes(d) for d in (source, result, original)]
    font = GameAsciiFont.from_arm9(current.read_file("/__arm9__.bin"))
    expected = {(90 + n * 6 + x, 2 + y) for n, char in enumerate("Treasure Name")
                for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
    actual = {(x, y) for y in range(15) for x in range(84, 174)
              if new.indices[y * new.width + x] == 7}
    assert actual == expected
    assert all(a == b for i, (a, b) in enumerate(zip(old.indices, new.indices))
               if not (BOX[0] <= i % old.width < BOX[2] and BOX[1] <= i // old.width < BOX[3]))
    config = {"format": "dk4-treasure-source-grain-release-v1", **{k: plan[k] for k in
              ("source_sha256", "japanese_source_sha256", "target_sha256")}, "status": "experimental"}
    write("translations/treasure_source_grain_v1.json", config)
    write(ROOT / "source_frame_proof.json", {**plan, "first_and_final_letters_complete": True,
          "all_other_header_pixels_list_rows_palette_dimensions_preserved": True,
          "production_integration_and_native_crops_pending": True})
    (ROOT / "RESEARCH_ONLY.pxl").write_bytes(result)
    sheet = Image.new("RGB", (1100, 115), (40, 45, 50))
    draw = ImageDraw.Draw(sheet)
    for n, (label, asset) in enumerate([("Japanese source", jp), ("V544", old), ("Source grain restored", new)]):
        draw.text((n * 365 + 5, 8), label, fill="white")
        sheet.paste(asset.render().crop(BOX).convert("RGB").resize((360, 60), Image.Resampling.NEAREST),
                    (n * 365 + 5, 35))
    sheet.save(ROOT / "header_source_grain_review.png")
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v544"])
    profile["treasure_source_grain"] = "translations/treasure_source_grain_v1.json"
    profile["description"] = profile["note"] = "Complete V544 stack plus original visible treasure-header grain; all graphics audits remain open."
    stack["profiles"]["all-routes-unified-v545"] = profile
    write(stack_path, stack)
    save = Path("work/emulation_v193/guild_diplomacy_v340/saves/all_routes_combined_v340_candidate.dsv")
    dest = ROOT / "ancient-map-texture-test-only.dsv"
    # Copy the verified isolated historical donor; never launch the original.
    assert sha(save.read_bytes()) == "28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e"
    shutil.copyfile(save, dest)
    assert save.read_bytes() == dest.read_bytes()
    write(ROOT / "save_copy_manifest.json", {"source": str(save), "source_sha256": sha(save.read_bytes()),
                                            "test_copy": str(dest), "test_copy_sha256": sha(dest.read_bytes())})
    inputs = [{"start": f, "duration": 8, "buttons": ["START" if f == 1601 else "A"]}
              for f in (1601, 2001, 2401, 2801)]
    inputs += [{"start": 3201, "duration": 8, "buttons": ["X"]},
               {"start": 3601, "duration": 8, "touch": [108, 43]},
               {"start": 4001, "duration": 8, "buttons": ["A"]},
               {"start": 4401, "duration": 8, "touch": [125, 137]}]
    write(ROOT / "list_inputs.json", inputs)
    print(f"Registered V545: {plan['visible_source_pixels_preserved']} visible pixels retained, complete Treasure Name mask.")


if __name__ == "__main__":
    main()
