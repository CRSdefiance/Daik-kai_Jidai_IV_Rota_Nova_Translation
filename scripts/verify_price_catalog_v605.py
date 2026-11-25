"""Complete Price Info names: real parent/canvas,113 normal entries,124 CPU cases."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ROOT = Path("work/analysis/marker_consumers_v605")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/marker_consumers_v605_price_navigation")
ROM = Path("out/all_routes_combined_v604_candidate.nds")
PARENT, BITMAP, VT = 0x02188344, 0x02188C1C, 0x021581F0


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canvas(raw):
    assert struct.unpack_from("<I", raw, PARENT - BASE)[0] == VT
    words = struct.unpack_from("<12I", raw, BITMAP - BASE)
    assert BITMAP == PARENT + 0x8D8 and words[0] == 0x02160360
    assert words[7:12] == (0, 0, 0, 144, 24)
    header = words[4] - BASE
    flags, width_words, height, palette, pixels = struct.unpack_from("<5I", raw, header)
    assert (flags, width_words, height) == (4, 64, 128)
    palette = header + (palette if palette < 0x80000000 else palette - 0x100000000)
    pixels += header
    assert 0 <= palette <= len(raw) - 32 and 0 <= pixels <= len(raw) - 16384
    color = struct.unpack_from("<H", raw, palette + 2)[0]
    assert color & 0x8000 and tuple((color >> shift) & 31 for shift in (0, 5, 10)) == (28, 28, 28)
    data = raw[pixels:pixels + 16384]
    indices = bytes(value for b in data for value in (b & 15, b >> 4))
    name = b"".join(indices[y * 256 + 48:y * 256 + 144] for y in range(12, 24))
    return {"header": header + BASE, "palette": palette + BASE, "pixels": pixels + BASE,
            "packed": data, "indices": indices, "name": name, "descriptor": words}


def main():
    report_path = CAPTURE / "capture_report.json"
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert digest == "fb8de61d20e94e742574bded2d8e4251305f2b56265ff8624dd766eaa6cf9158"
    assert report["ROM_sha256"] == digest and report["frames"] == 47580
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded")
    assert all(not value for key, value in report.items() if key.startswith("synthetic_"))
    input_path = Path("work/analysis/blitter_trace_v603/market_inputs.json")
    initial = read(input_path)
    assert report["scripted_input_schedule"][:len(initial)] == initial
    save(ROOT / "final_recorded_inputs.json", report["scripted_input_schedule"])
    shots = {}
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        shots[row["frame"]] = row
    snapshots = {}
    for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots"):
        for row in report.get(key, []):
            assert row["read_only_export"]
            snapshots[row["frame"]] = row
    rom = NdsImage.open(ROM)
    arm = rom.read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0xBEF70:0xBF0AC] == clean[0xBEF70:0xBF0AC]
    # Original item iterator: test byte14 bit0, then byte12 category.
    assert arm[0xBEF84:0xBEFA0] == bytes.fromhex("0e00d1e5010010e23c00000a0c10d1e50c009de5010050e13800001a")
    updater = bytearray(arm[0xBF338:0xBF3F0])
    updater[0xBF3DC - 0xBF338:0xBF3E0 - 0xBF338] = clean[0xBF3DC:0xBF3E0]
    assert bytes(updater) == clean[0xBF338:0xBF3F0]
    type_info = struct.unpack_from("<I", arm, VT - BASE - 4)[0]
    name_pointer = struct.unpack_from("<I", arm, type_info - BASE + 4)[0]
    assert arm[name_pointer - BASE:arm.index(0, name_pointer - BASE)] == b"21CPriceInformationView"
    font = GameAsciiFont.from_arm9(arm)
    manuscript = Path("translations/commodity_name_manuscript_v343.json")
    rows = read(manuscript)["records"]
    assert len(rows) == 124
    masks, by_mask = {}, {}
    for row in rows:
        mask = bytearray(96 * 12)
        for index, char in enumerate(row["English"]):
            glyph = font.decode(char)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        assert index * 5 + x < 96
                        mask[y * 96 + index * 5 + x] = 1
        masks[row["index"]] = bytes(mask)
        assert bytes(mask) not in by_mask
        by_mask[bytes(mask)] = row["index"]
    seed_info = snapshots[29700]
    seed = Path(seed_info["path"]).read_bytes()
    assert sha(seed) == seed_info["sha256"]
    actual_canvas = canvas(seed)
    assert actual_canvas["name"] == masks[0]
    u = machine(arm)
    u.mem_write(BASE, seed)
    for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).values():
        u.mem_write(overlay.ramAddress, bytes(overlay.data))
    call(u, 0xCB124, ())
    table = u.reg_read(UC_ARM_REG_R0) + 4
    catalog = []
    for row in rows:
        index = row["index"]
        obj = table + index * 16
        entry = bytes(u.mem_read(obj, 16))
        vtable = struct.unpack_from("<I", entry)[0]
        getter = struct.unpack("<I", u.mem_read(vtable + 4, 4))[0]
        call(u, getter - BASE, (obj,))
        assert u.reg_read(UC_ARM_REG_R0) == index
        catalog.append({"index": index, "English": row["English"], "category": entry[12],
                        "listed_by_original_Price_Info_filter": bool(entry[14] & 1),
                        "complete_entry_sha256": sha(entry)})
    eligible = {r["index"] for r in catalog if r["listed_by_original_Price_Info_filter"]}
    excluded = [r for r in catalog if r["index"] not in eligible]
    assert len(eligible) == 113 and len(excluded) == 11 and {r["category"] for r in catalog} == set(range(18))
    replay = []
    for row in rows:
        index = row["index"]
        before = bytes(u.mem_read(actual_canvas["pixels"], 16384))
        header = bytes(u.mem_read(actual_canvas["header"], 20))
        palette = bytes(u.mem_read(actual_canvas["palette"], 32))
        expected = bytearray(value for b in before for value in (b & 15, b >> 4))
        for y in range(12):
            expected[(y + 12) * 256 + 48:(y + 12) * 256 + 144] = masks[index][y * 96:y * 96 + 96]
        packed = bytes(expected[i] | expected[i + 1] << 4 for i in range(0, len(expected), 2))
        executed = call(u, 0xBF338, (PARENT, index), instruction_limit=1000000)
        assert {0x020BF338, 0x01FFC800, 0x020D3718, 0x020D5160, 0x020D5140} <= executed
        assert bytes(u.mem_read(actual_canvas["pixels"], 16384)) == packed
        assert bytes(u.mem_read(actual_canvas["header"], 20)) == header
        assert bytes(u.mem_read(actual_canvas["palette"], 32)) == palette
        replay.append({"index": index, "English": row["English"], "whole16384_byte_actual_canvas_exact": True,
                       "source_name_box": [48, 12, 144, 24], "not_new_native_screenshot_or_availability_credit": True})
    appearances, first = [], {}
    for frame, snapshot in sorted(snapshots.items()):
        if not 29700 <= frame <= 46380:
            continue
        raw = Path(snapshot["path"]).read_bytes()
        assert sha(raw) == snapshot["sha256"] and len(raw) == 0x400000
        current = canvas(raw)
        index = by_mask.get(current["name"])
        if index is None:
            assert not any(current["name"]), f"Unknown nonempty name at frame{frame}"
            continue
        assert index in eligible
        assert struct.unpack_from("<I", raw, PARENT - BASE + 0x5FC)[0] == catalog[index]["category"]
        image = Image.open(shots[frame]["path"]).convert("RGB").point(lambda n: n >> 3)
        mask = masks[index]
        count = 0
        for y in range(12):
            for x in range(96):
                ink = image.getpixel((160 + x, 208 + y)) == (28, 28, 28)
                assert ink == bool(mask[y * 96 + x]), (frame, index, x, y)
                count += ink
        appearance = {"frame": frame, "index": index, "English": rows[index]["English"],
            "category": catalog[index]["category"], "parent": PARENT, "bitmap": BITMAP,
            "dynamic_header": current["header"], "actual_canvas_name_box": [48, 12, 144, 24],
            "native_name_box": [160, 208, 256, 220], "complete_ink_points": count,
            "whole_source_and_native96x12_foreground_masks_exact": True,
            "snapshot_sha256": snapshot["sha256"], "screenshot": shots[frame]["path"],
            "screenshot_sha256": shots[frame]["PNG_sha256"]}
        appearances.append(appearance)
        first.setdefault(index, appearance)
    assert set(first) == eligible
    for frame in (28100, 28500, 28900, 46780, 47180, 47580):
        assert frame in shots and frame in snapshots
    baseline = read("E:/Rota Nova translations/Generated/work/emulation_v193/race_controls_v604_market_candidate/capture_report.json")
    old_shot = next(s for s in baseline["frames_captured"] if s["frame"] == 24100)
    assert Image.open(old_shot["path"]).tobytes() == Image.open(shots[24100]["path"]).tobytes()
    assert Image.open(shots[24100]["path"]).tobytes() == Image.open(shots[24500]["path"]).tobytes()
    census_path = ROOT / "crop_argument_census.json"
    census = read(census_path)
    assert census["candidate_sha256"] == digest
    assert census["script_sha256"] == sha(Path("scripts/trace_marker_consumers_v605.py").read_bytes())
    proof = {"candidate": str(ROM), "candidate_sha256": digest, "production_ROM_patch_registry_and_art_changed": False,
        "report": str(report_path), "report_sha256": sha(report_path.read_bytes()), "frames": 47580,
        "ordinary_New_Game_navigation_no_battery_save_savestate_or_synthetic_fixture": True,
        "menu_path": "Market > Market Info > Lisbon report0coins > Price Info >18 categories",
        "actual_parent": PARENT, "parent_vtable": VT, "parent_RTTI": "21CPriceInformationView",
        "actual_name_bitmap": BITMAP, "actual_name_bitmap_offset": 0x8D8,
        "actual_source_canvas": [256, 128], "actual_name_box": [48, 12, 144, 24], "native_name_box": [160, 208, 256, 220],
        "old_V357_anchor_was_explicitly_supplied_not_actual_parent_and_used_different_canvas": True,
        "old_controlled_font_evidence_retained_no_historical_native_parent_credit_inferred": True,
        "original_availability_filter": [0x020BEF70, 0x020BEFA0], "filter_code_exact_clean": True,
        "all124_actual_parent_CPU_replay": replay, "whole_canvas_replay_bytes": 124 * 16384,
        "all113_originally_listed_names_observed": sorted(first), "all18_categories_observed": sorted({r["category"] for r in first.values()}),
        "native_unique_name_cases": [first[k] for k in sorted(first)], "native_name_appearances": len(appearances),
        "native_appearances": appearances, "unique_complete_ink_points": sum(r["complete_ink_points"] for r in first.values()),
        "unique_full_native_name_positions": 113 * 96 * 12, "excluded_by_original_view_filter": excluded,
        "excluded_entries_global_nonuse_not_inferred": True, "existing_abbreviations_and_semantics_not_rewritten": True,
        "rejected_leads": ["Small footer was misread as Y Price; native enlarged crop proves Y Sell. Y left the frame unchanged.",
                           "Raw-data plan included11 filtered records; plan expectations were not used as passing evidence.",
                           "Sold/Local/Cargo source rows are not the Buy/Sell price cells."],
        "old_transactions_preserved_at24100": True, "source_and_actual_Back_return_states_captured": True,
        "marker_census": str(census_path), "marker_census_sha256": sha(census_path.read_bytes()),
        "five_marker_header_ordinary_parents_still_open": True,
        "unclassified_legacy_graphics_and_other_goal_gates_still_open": True,
        "manuscript_sha256": sha(manuscript.read_bytes()), "script_sha256": sha(Path(__file__).read_bytes()),
        "hardware_device_verification": False, "publication_approved": False, "full_goal_complete": False}
    save(ROOT / "native_price_catalog_proof.json", proof)
    print(f"V605:113 ordinary names/18 categories/{len(appearances)} appearances;124 real-parent CPU cases;130176 native positions;all lettering complete;five marker contexts open;V604 unchanged.")


if __name__ == "__main__":
    main()
