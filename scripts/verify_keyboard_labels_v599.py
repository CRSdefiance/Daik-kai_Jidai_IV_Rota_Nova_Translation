"""Verify display-only keyboard labels, native character pages and full regression frames."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import (
    SJIS_GLYPH_COUNT,
    SJIS_MAP_OFFSET,
    GameAsciiFont,
    decode_glyph,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.keyboard_page_labels import apply_release
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path("work/analysis/keyboard_labels_v599")
ROM = Path("out/all_routes_combined_v599_candidate.nds")
PARENT = Path("out/all_routes_combined_v593_candidate.nds")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
BASE, EDITOR = 0x02000000, 0x0218EEC8
DIGEST = "1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def report(folder, digest, frames):
    path = CAPTURE / folder / "capture_report.json"
    r = read(path)
    assert r["ROM_sha256"] == digest and r["frames"] == frames
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert r.get("battery_save_preloaded") is None
    assert not any(value for key, value in r.items() if key.startswith("synthetic_"))
    shots = {}
    for row in r["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        shots[row["frame"]] = Image.open(row["path"]).convert("RGB")
    snapshots = {}
    for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots"):
        for row in r.get(key, []):
            assert row["read_only_export"] and sha(Path(row["path"]).read_bytes()) == row["sha256"]
            snapshots[row["frame"]] = Path(row["path"]).read_bytes()
    return r, shots, snapshots, {"path": str(path), "sha256": sha(path.read_bytes())}


def complete_page(image, table, arm, kanji):
    mapping = struct.unpack_from(f"<{SJIS_GLYPH_COUNT}H", arm, SJIS_MAP_OFFSET)
    union, cases = set(), []
    for n in range(len(table) // 2):
        code = int.from_bytes(table[n * 2:n * 2 + 2], "big")
        slot = mapping.index(code)
        glyph = decode_glyph(kanji, slot)
        assert not any(glyph.getpixel((x, y)) for y in range(11) for x in range(12, 16))
        x, y = 56 + n % 10 * 14, 216 + n // 10 * 14
        points = {(x + xx, y + yy) for yy in range(11) for xx in range(12) if glyph.getpixel((xx, yy))}
        union |= points
        cases.append({"character": table[n * 2:n * 2 + 2].decode("cp932"), "source_glyph": slot,
                      "bounds": [x, y, x + 12, y + 11], "ink_pixels": len(points)})
    # Include every inter-cell gap and unused slot, not only expected ink.
    rows = (len(cases) + 9) // 10
    for y in range(216, 216 + rows * 14):
        for x in range(56, 196):
            assert (image.getpixel((x, y)) == (230, 230, 230)) == ((x, y) in union)
    return {"characters": cases, "ink_pixels": len(union), "whole_foreground_positions": 140 * rows * 14}


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    current, parent = NdsImage.open(ROM), NdsImage.open(PARENT)
    previous = sha(PARENT.read_bytes())
    assert previous == "d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642"
    before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    after = {p: data for _, p, data in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys()
    changed = sorted(p for p in before if before[p] != after[p])
    assert changed == ["/__arm9__.bin"]
    arm = after[changed[0]]
    transformed, transform = apply_release(before[changed[0]], "translations/keyboard_page_labels_v1.json")
    assert arm == transformed
    contracts = read(ROOT / "display_and_provider_contract.json")
    assert contracts["revised_ARM9_sha256"] == sha(arm)
    assert contracts["script_sha256"] == sha(Path("scripts/probe_keyboard_labels_v599.py").read_bytes())
    assert len(contracts["all49_display_routes"]) == 49
    assert contracts["current_and_revised_original_provider_contracts_exact"]
    manifest, prior = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    registry = read("translations/release_stack.json")
    assert manifest["candidate_sha256"] == DIGEST and manifest["profile"] == "all-routes-unified-v599"
    assert manifest["base_sha256"] == registry["canonical_baseline"]["sha256"]
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["batches"] == prior["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == prior["required_batches"] and len(registry["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    apply_xdelta(Path("work/clean.nds"), ROM.with_suffix(".xdelta"), ROOT / "v599_reconstructed.nds")
    assert sha((ROOT / "v599_reconstructed.nds").read_bytes()) == DIGEST
    keyboard, images, snapshots, binding = report("keyboard_labels_v599", DIGEST, 7900)
    historic, old_images, _, old_binding = report("name_editor_v582",
        "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68", 6500)
    assert keyboard["scripted_input_schedule"][:10] == historic["scripted_input_schedule"][:10]
    font = GameAsciiFont.from_arm9(arm)
    assert font.glyphs == GameAsciiFont.from_arm9(before["/__arm9__.bin"]).glyphs
    labels = []
    for frame in (4800, 5700, 5900, 6400, 7300, 7500):
        for text, x in (("EN", 158), ("#+", 172)):
            count, bounds = complete_mask(font, text, images[frame], x, 320, (230, 230, 230))
            assert bounds[2] <= x + 12 and bounds[3] <= 332
            labels.append({"frame": frame, "text": text, "bounds": bounds, "complete_ink_pixels": count})
    old_comparisons = []
    for frame in (4800, 5500, 5700, 5900):
        differences = [(x, y) for y in range(384) for x in range(256)
                       if images[frame].getpixel((x, y)) != old_images[frame].getpixel((x, y))]
        assert len(differences) == (0 if frame == 5500 else 178)
        assert all((158 <= x < 170 or 172 <= x < 184) and 320 <= y < 332 for x, y in differences)
        old_comparisons.append({"frame": frame, "whole_frame_positions": 98304,
                                "differences_only_inside_two12x12_control_cells": len(differences)})
    kanji = current.read_file("/GRP/KANJI.FNT")
    assert kanji == parent.read_file("/GRP/KANJI.FNT")
    queries = []
    for japanese, index, frame, expected_count in (("英", 50, 5500, 52), ("記", 51, 7000, 26)):
        uc = machine(arm)
        uc.mem_write(BASE, snapshots[frame])
        uc.mem_write(0x02470000, japanese.encode("cp932") + b"\0")
        call(uc, 0xD1E3C, (EDITOR + 4, 0x02470000))
        assert uc.reg_read(UC_ARM_REG_R0) == index
        uc.mem_write(STACK, struct.pack("<I", 0xFFFFFFFF))
        call(uc, 0xD1BBC, (EDITOR + 4, index, 0x02470100, 0))
        count = uc.reg_read(UC_ARM_REG_R0)
        assert count == expected_count
        table = bytes(uc.mem_read(0x02470100, count * 2))
        queries.append({"source_identifier": japanese, "page_index": index, "table_hex": table.hex(),
                        "native_glyph_page": complete_page(images[frame], table, arm, kanji)})
    states = []
    for frame, expected in ((4800, b"Rafael\0"), (5500, b"Rafael\0"), (5700, b"Rafael\x82\x81\0"),
                            (5900, b"Rafael\0"), (6400, b"Rafael\0"), (7000, b"Rafael\0"),
                            (7300, b"Rafael\x82\x4f\0"), (7500, b"Rafael\0")):
        raw = snapshots[frame]
        offset = EDITOR + 0xB4 - BASE
        assert raw[offset:offset + len(expected)] == expected
        words = [struct.unpack_from("<I", raw, EDITOR - BASE + at)[0] for at in (0, 4, 0x38, 0xD8)]
        assert words == [0x021558CC, 0x0215591C, 0x02155D44, 16]
        states.append({"frame": frame, "name_buffer_hex": expected.hex(), "original_vtables_and_capacity": words})
    assert images[4400].tobytes() == images[6100].tobytes() == images[7900].tobytes()
    complete_mask(font, "Rafael", images[7700], 89, 220, (230, 230, 230))
    confirmation_diff = [(x, y) for y in range(384) for x in range(256)
                         if images[2000].getpixel((x, y)) != images[7700].getpixel((x, y))]
    assert len(confirmation_diff) == 182
    assert all(16 <= x < 100 and 198 <= y < 209 for x, y in confirmation_diff)
    market, market_images, _, market_binding = report("keyboard_v599_market_regression", DIGEST, 24100)
    original, original_images, _, original_binding = report("trade_consumers_v598", previous, 24100)
    assert market["scripted_input_schedule"] == original["scripted_input_schedule"]
    regression = sorted(market_images.keys() & original_images.keys())
    assert len(regression) == 19
    assert all(market_images[n].tobytes() == original_images[n].tobytes() for n in regression)
    input_path = ROOT / "final_recorded_inputs.json"
    save(input_path, keyboard["scripted_input_schedule"])
    parent_proof = Path("work/analysis/ship_batteries_v593/preservation_proof.json")
    preservation = read(parent_proof)
    assert preservation["candidate_sha256"] == previous and len(preservation["entries"]) == 921
    assert len(preservation["embedded_block_extents"]) == 57
    preservation.update(candidate=str(ROM), candidate_sha256=DIGEST, parent_proof=str(parent_proof),
        parent_proof_sha256=sha(parent_proof.read_bytes()), only_different_graphics_file=None,
        all_graphics_files_and_embedded_containers_exact_V593=True,
        only_changed_component_from_V593="/__arm9__.bin",
        keyboard_display_transform=transform)
    # The prior room-text-only assertion belongs to V593, not this new ARM9 delta.
    preservation.pop("ARM9_only_two12_byte_room_text_slots_change_fonts_and_code_exact")
    preservation.pop("changed_atlas_complete_header_all_palette_banks_and_extent_exact")
    preservation["prior_V593_room_text_assertion_retained_in_parent_proof"] = True
    save(ROOT / "preservation_proof.json", preservation)
    save(ROOT / "release_proof.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
        "canonical_base": registry["canonical_baseline"], "profile": manifest["profile"],
        "parent": str(PARENT), "parent_sha256": previous, "changed_components_from_V593": changed,
        "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()), "exact_clean_patch_reconstruction": True,
        "manifest_sha256": sha(ROM.with_suffix(".manifest.json").read_bytes()),
        "all470_batches114_layers_retained": True, "display_transform": transform,
        "routing_contract_proof": str(ROOT / "display_and_provider_contract.json"),
        "routing_contract_proof_sha256": sha((ROOT / "display_and_provider_contract.json").read_bytes()),
        "reports": {"keyboard": binding, "historical_keyboard": old_binding,
                    "market": market_binding, "historical_market": original_binding},
        "complete_control_label_masks": labels, "whole_historical_keyboard_comparisons": old_comparisons,
        "native_provider_queries_and_complete_pages": queries, "actual_name_buffer_states": states,
        "Latin_and_Symbol_insertion_and_whole_character_deletion": True,
        "whole98304_pixel_edit_screen_returned_exact_twice": True,
        "confirmation_182_state_header_pixels_only": True,
        "whole_market_regression_frames_exact": regression,
        "whole_market_regression_pixel_positions": len(regression) * 98304,
        "ordinary_cold_boot_no_synthetic_fixture_or_existing_save": True,
        "input_schedule": str(input_path), "input_schedule_sha256": sha(input_path.read_bytes()),
        "script_sha256": sha(Path(__file__).read_bytes()), "status": "experimental",
        "hardware_device_verification": False, "full_goal_complete": False})
    print("V599:12 complete control-label masks;52 Latin/26 Symbol cells;actual insert/delete/Finish/Back;19 whole Market frames exact;921/57 preserved;patch exact.")


if __name__ == "__main__":
    main()
