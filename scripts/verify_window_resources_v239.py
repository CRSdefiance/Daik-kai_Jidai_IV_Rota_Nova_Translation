"""Verify registered native window resources without inventing their scene usage."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_title_display_v229 import ROM, ROM_SHA, native_views

OUT = Path("work/analysis/window_resources_v239")
PATHS = {f"/_pxl/winframe{i:02d}.pxl" for i in (0, 1, 2, 3, 5)}


def main():
    assert sha(ROM.read_bytes()) == ROM_SHA
    image = NdsImage.open(ROM)
    proof = native_views(image, expected_paths=PATHS, owner_range=(0x023132F4, 0x02313358))
    proof.pop("physical_title05_and_standalone_logo_display_not_inferred_from_fixture")
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (768, 448), "#e4e4e4")
    draw = ImageDraw.Draw(sheet)
    for n, case in enumerate(proof["cases"]):
        path = case["path"]
        pxl = PxlImage.from_bytes(image.read_file(path))
        art = pxl.render().convert("RGB")
        assert art.width <= 256 and art.height <= 192
        preview = OUT / (Path(path).stem + ".png")
        art.save(preview)
        x, y = n % 3 * 256, n // 3 * 224
        draw.text((x + 4, y + 4), path, fill="black")
        sheet.paste(art, (x, y + 24))
        case["preview"] = str(preview)
        case["preview_sha256"] = sha(preview.read_bytes())
        case["physical_display_not_proved"] = True
        case["whole_view_inputs_are_research_invocations_not_scene_crops"] = True
    sheet.save(OUT / "full_source_sheet.png")
    proof.update({"format": "dk4-window-resource-native-proof-v239", "ROM_sha256": ROM_SHA,
                  "native_views_verified": len(proof["cases"]),
                  "native_registration_owner_range": [0x023132F4, 0x02313358],
                  "standalone_logo_and_startmenu_literal_reference_absence_not_unused_proof": True,
                  "actual_scene_crops_GPU_and_input_pending": True,
                  "ROM_modified": False, "full_goal_complete": False})
    (OUT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_registered_windows": len(proof["cases"]),
                      "full_resource_byte_copies": sum(c["complete_resource_bytes"] for c in proof["cases"]),
                      "physical_display_pending": True}))


if __name__ == "__main__":
    main()
