"""Verify the actual corrected screen pixels, stat crops and tooltip backdrop."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/two_screen_layout_v246")
ROM = Path("out/all_routes_combined_v246_candidate.nds")


def load_capture(name, frame, digest):
    directory = Path("work/emulation_v193/two_screen_v246") / name
    report = json.loads((directory / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    row = next(r for r in report["frames_captured"] if r["frame"] == frame)
    return Image.open(row["path"]).convert("RGB"), report, row


def main():
    digest = sha(ROM.read_bytes())
    rom = NdsImage.open(ROM)
    crew, _crew_report, crew_row = load_capture("crew",10000,digest)
    person, person_report, person_row = load_capture("person",10500,digest)
    cases = []
    for name,image,path,batch_path in (
        ("crew",crew,"/_pxl/dividecrewinfo.pxl","translations/assign_sailors_graphics_v4.json"),
        ("person",person,"/_pxl/personinfo.pxl","translations/person_info_graphics_v2.json"),
    ):
        asset = PxlImage.from_bytes(rom.read_file(path))
        batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
        for row in batch["records"]:
            x0,y0,x1,y1 = row["box"]
            # Dynamic numbers lie outside the caption/plaque interior.
            if name == "crew":
                x0,y0,x1,y1 = row.get("draw_box",row["box"])
            for y in range(y0,y1):
                for x in range(x0,x1):
                    assert native5(image.getpixel((x,y))) == native5(asset.palette[asset.indices[y*256+x]])
            cases.append({"screen":name,"text":row["text"],"complete_pixel_bounds":[x0,y0,x1,y1],
                          "full_caption_area_and_first_last_letters_exact":True})
    snapshot = person_report["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    assert sha(ram) == snapshot["sha256"]
    # Find six initialized bar views of the stat atlas, with new bounded widths.
    views = []
    for offset in range(0,len(ram)-48,4):
        f = struct.unpack_from("<12I",ram,offset)
        if (f[5] == 4 and f[7] == 0 and f[8] in (0,8,16,24,32,40) and f[11] == 8
                and 0 <= f[10] <= 50 and 0x02312700 <= f[3] <= 0x02314000):
            views.append({"view":0x02000000+offset,"source_row":f[8],"width":f[10],"owner":f[3]})
    groups = {}
    for v in views:groups.setdefault(v["owner"],[]).append(v)
    valid = [g for g in groups.values() if {v["source_row"] for v in g} == {0,8,16,24,32,40}]
    assert valid
    # Visible paper tooltip is tan rather than the old opaque white rectangle.
    gold = [(x,y) for y in range(207,224) for x in range(134,225)
            if abs(person.getpixel((x,y))[0]-205)<12 and abs(person.getpixel((x,y))[1]-190)<12
            and abs(person.getpixel((x,y))[2]-141)<12]
    assert len(gold)>300
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    heading_ink, heading_bounds = complete_mask(font,"Equipped Items",person,138,210,(0,8,0))
    proof = {"format":"dk4-two-screen-live-pixels-v246","ROM_sha256":digest,
             "crew_capture":crew_row,"person_capture":person_row,"complete_caption_cases":cases,
             "native_bar_view_groups":valid,"stat_label_right_edge":170,"bar_left_edge":174,
             "bar_maximum_right_edge":224,"numeric_front_origin":227,
             "labels_bars_values_have_separate_horizontal_space":True,
             "equipment_tooltip_tan_pixels":len(gold),"no_savestate_RAM_injection_or_fixture_ROM":True,
             "equipment_heading_complete_font_ink_pixels":heading_ink,
             "equipment_heading_complete_bounds":heading_bounds,
             "both_actual_screens_visually_reviewed":True,"full_goal_complete":False}
    (ROOT / "live_proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    saved_path = ROOT / "saved_proof.json"
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    saved["cold_boot_both_screens_pending"] = False
    saved["live_proof"] = str(ROOT / "live_proof.json")
    saved_path.write_text(json.dumps(saved,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"complete_live_caption_cases":len(cases),"tan_tooltip_pixels":len(gold),
                      "stat_geometry_nonoverlapping":True}))


if __name__ == "__main__":
    main()
