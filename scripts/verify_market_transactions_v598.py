"""Verify ordinary Market transactions and complete native heading graphics."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ROOT = Path("work/analysis/trade_consumers_v598")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/trade_consumers_v598")
ROM = Path("out/all_routes_combined_v593_candidate.nds")
FIELDS = {
    19700: (30000, 0, 1144, 28856), 20000: (30000, 0, 1144, 28856),
    20300: (30000, 0, 1144, 28856), 20600: (30000, 0, 1144, 28856),
    20900: (30000, 0, 572, 29428), 22000: (29428, 0, 0, 29428),
    22300: (29428, 288, 0, 29716), 22900: (29428, 288, 0, 29716),
    24100: (29716, 0, 0, 29716),
}
HEADINGS = (("Sold", 0, 328, 0x8D4), ("Local", 16, 286, 0x860), ("Cargo", 32, 232, 0x7EC))


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def exact_text(font, image, text, area):
    mask = Image.new("1", (len(text) * 6, 11))
    for index, character in enumerate(text):
        mask.paste(font.decode(character), (index * 6, 0))
    points = [(x, y) for y in range(11) for x in range(mask.width) if mask.getpixel((x, y))]
    color = (230, 230, 230)
    matches = []
    left, top, right, bottom = area
    for y in range(top, bottom):
        for x in range(left, right):
            if not all(image.getpixel((x + dx, y + dy)) == color for dx, dy in points):
                continue
            if all((image.getpixel((x + dx, y + dy)) == color) == bool(mask.getpixel((dx, dy)))
                   for dy in range(11) for dx in range(mask.width)):
                matches.append((x, y))
    assert len(matches) == 1, (text, area, matches)
    x, y = matches[0]
    return {"text": text, "origin": [x, y], "full_cell_bounds": [x, y, x + mask.width, y + 11],
            "complete_ink_points": len(points), "first_last_and_all_blank_cells_exact": True}


def main():
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    assert digest == "d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642"
    arm = rom.read_file("/__arm9__.bin")
    font = GameAsciiFont.from_arm9(arm)
    report_path = CAPTURE / "capture_report.json"
    r = read(report_path)
    assert r["frames"] == 24100 and r["ROM_sha256"] == digest
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert not r.get("battery_save_preloaded")
    assert all(not value for key, value in r.items() if key.startswith("synthetic_"))
    snapshots = {s["frame"]: s for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots")
                 for s in r.get(key, [])}
    for snapshot in snapshots.values():
        assert sha(Path(snapshot["path"]).read_bytes()) == snapshot["sha256"]
    shots = {s["frame"]: s for s in r["frames_captured"] if "navigation" in Path(s["path"]).name}
    for shot in r["frames_captured"]:
        assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
    atlas = PxlImage.from_bytes(rom.read_file("/_pxl/__marker.pxl"))
    originals = PxlImage.from_bytes(clean.read_file("/_pxl/__marker.pxl"))
    assert atlas.source[:atlas.pixels_offset] == originals.source[:originals.pixels_offset]
    batch = read("translations/interface_marker_graphics_v1.json")
    words = []
    for record in batch["records"]:
        if record["id"] not in ("DK4_MARKER_FOR_SALE", "DK4_MARKER_SPECIALTY", "DK4_MARKER_CARGO"):
            continue
        blank = PxlImage.from_bytes(atlas.source)
        blank.indices[:] = bytes(len(blank.indices))
        blank.draw_text(tuple(record["box"]), record["text"], 15, maximum_size=record["maximum_size"])
        left, top, right, bottom = record["box"]
        expected = {(x, y) for y in range(top, bottom) for x in range(left, right) if blank.indices[y * 256 + x] == 15}
        actual = {(x, y) for y in range(top, bottom) for x in range(left, right) if atlas.indices[y * 256 + x] == 15}
        assert expected == actual and expected and max(x for x, y in expected) < 144
        words.append({"text": record["text"], "complete_original_layout_ink_points": len(actual),
                      "entire_word_inside_actual32_pixel_native_source_width": True})
    assert sum(w["complete_original_layout_ink_points"] for w in words) == 188
    frames = []
    view = 0x0218F25C
    native_code_ranges = [(0xBCADC, 0xBCB00), (0x48098, 0x480DC), (0xC20B8, 0xC21E0)]
    assert all(arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi] for lo, hi in native_code_ranges)
    for frame, values in FIELDS.items():
        funds, income, spent, total = values
        assert funds + income - spent == total
        image = Image.open(shots[frame]["path"]).convert("RGB")
        raw = Path(snapshots[frame]["path"]).read_bytes()
        u = machine(arm)
        u.mem_write(BASE, raw)
        assert struct.unpack("<I", u.mem_read(view, 4))[0] == 0x02158698
        type_info = struct.unpack("<I", u.mem_read(0x02158698 - 4, 4))[0]
        name_pointer = struct.unpack("<I", u.mem_read(type_info + 4, 4))[0]
        assert bytes(u.mem_read(name_pointer, 32)).split(b"\0")[0] == b"12CTradingView"
        model = struct.unpack("<I", u.mem_read(view + 0x5F8, 4))[0]
        assert model == 0x021918C0
        before = bytes(u.mem_read(model, 0x610))
        stock = []
        for index in range(5):
            getters = []
            for method in (0xBCAF4, 0xBCAE8, 0xBCADC):
                call(u, method, (model, index))
                getters.append(u.reg_read(UC_ARM_REG_R0))
            stock.append({"goods_id": getters[0], "grade": getters[1], "quantity": getters[2]})
        assert [x["goods_id"] for x in stock] == [13, 14, 27, 78, 86]
        assert [x["quantity"] for x in stock] == [3 if frame <= 20600 else 4, 5, 8, 7, 5]
        assert bytes(u.mem_read(model, 0x610)) == before
        heading_cases = []
        for text, source_y, dest_y, relative in HEADINGS:
            address = view + relative
            state = struct.unpack("<12I", u.mem_read(address, 48))
            assert state[3] == 0x02313F74 and state[7:9] == (112, source_y)
            assert state[10:12] == (32, 16) and state[6] == 0 and state[9] & 255 == 0
            call(u, 0xD4170, (address,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(atlas.source))) == atlas.source
            for y in range(16):
                for x in range(32):
                    rgba = atlas.palette[atlas.indices[(source_y + y) * 256 + 112 + x]]
                    assert rgba[3]
                    assert tuple(c >> 3 for c in image.getpixel((32 + x, dest_y + y))) == tuple(c >> 3 for c in rgba[:3])
            heading_cases.append({"text": text, "view": address, "source_XYWH": [112, source_y, 32, 16],
                                  "destination": [32, dest_y], "resident_pointer": pointer,
                                  "whole512_pixel_native_crop_exact": True})
        text_cases = []
        for label, value in zip(("Funds", "Income", "Spent", "Sum"), values, strict=True):
            label_case = exact_text(font, image, label, (0, 25, 60, 94))
            y = label_case["origin"][1]
            number_case = exact_text(font, image, str(value), (64, y, 114, y + 1))
            text_cases += [label_case, number_case]
        frames.append({"frame": frame, "displayed_net_fields": dict(zip(("Funds", "Income", "Spent", "Sum"), values, strict=True)),
                       "current_native_stock_getters": stock, "actual_model_unchanged_by_queries": True,
                       "complete_header_graphics": heading_cases, "complete_HUD_text_masks": text_cases})
    same = Image.open(shots[22300]["path"]).convert("RGB").tobytes() == Image.open(shots[22900]["path"]).convert("RGB").tobytes()
    assert same
    final_inputs = ROOT / "final_recorded_inputs.json"
    final_inputs.write_text(json.dumps(r["scripted_input_schedule"], indent=2) + "\n", encoding="utf-8")
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        d = read(Path("translations") / filename)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    proof = {"format": "dk4-ordinary-market-transactions-v598", "candidate": str(ROM), "candidate_sha256": digest,
             "report": str(report_path), "report_sha256": sha(report_path.read_bytes()),
             "actual_recorded_inputs": str(final_inputs), "input_sha256": sha(final_inputs.read_bytes()),
             "cold_boot_without_save_or_synthetic_fixtures": True, "source_exact_native_code_ranges": native_code_ranges,
             "complete_heading_source_word_checks": words, "ordinary_trade_screen_cases": frames,
             "all27_complete_heading_crops_13824_pixels_exact": True,
             "all72_HUD_word_number_masks_exact": True, "sale_confirmation_No_returns_entire98304_pixel_frame": same,
             "ordinary_purchase572_and_sale288_committed_final_funds29716": True,
             "Sold_section_contains_goods_sold_to_port_after_trade_and_reentry": True,
             "Buy_Sell_price_atlas_cells_not_identified_as_these_three_heading_sources": True,
             "price_cell_ordinary_parent_and_global_material_audit_remain_open": True,
             "three_source_backgrounds_not_assumed_identical_for_reconstruction": True,
             "source_texture_review": str(ROOT / "trade_heading_source_current_review.png"),
             "production_ROM_or_patch_changed": False, "all18_plaques_remain_incomplete": True,
             "all22_historical_objects_retained": True, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "ordinary_trade_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("V598: ordinary purchase/sale committed;27 whole heading crops/13824 pixels;72 complete HUD masks;full No-return frame exact;no ROM change.")


if __name__ == "__main__":
    main()
