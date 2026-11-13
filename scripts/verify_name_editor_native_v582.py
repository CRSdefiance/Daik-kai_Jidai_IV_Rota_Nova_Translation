"""Ordinary New Game editor: source Latin glyphs, insertion/delete and completion."""

import json
import shutil
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import (
    SJIS_GLYPH_COUNT,
    SJIS_MAP_OFFSET,
    GameAsciiFont,
    decode_glyph,
)
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path("out/all_routes_combined_v581_candidate.nds")
ROOT = Path("work/analysis/confirm_consumers_v582")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/name_editor_v582")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V581 Name editor")
BASE, PARENT, OWNER = 0x02000000, 0x0218EEC8, 0x023139C0


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def full_sprite_matches(image, sprite):
    palette = struct.unpack_from("<16H", sprite.source, 20)
    opaque = [(x, y, native5(sprite.palette[sprite.indices[y * 48 + x]]))
              for y in range(20) for x in range(48)
              if palette[sprite.indices[y * 48 + x]] & 0x8000]
    assert len(opaque) == 881
    anchors = [opaque[n] for n in (0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 880)]
    pixels = image.load()
    found = []
    for top in range(365):
        for left in range(209):
            if (all(native5(pixels[left + x, top + y]) == color for x, y, color in anchors)
                    and all(native5(pixels[left + x, top + y]) == color for x, y, color in opaque)):
                found.append([left, top])
    return found


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert digest == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    manifest = read(ROM.with_suffix(".manifest.json"))
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v581"
    run = read(CAPTURE / "capture_report.json")
    assert run["ROM_sha256"] == digest and run["cold_boot"] and not run["savestate_loaded"]
    assert not run["callback_errors"] and run["frames"] == 6500
    assert run.get("battery_save_preloaded") is None
    assert not any(value for key, value in run.items() if key.startswith("synthetic_") and key.endswith("fixtures"))
    frames = {}
    for row in run["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        frames[row["frame"]] = row
    snapshots = {}
    for row in run["read_only_pause_RAM_snapshots"]:
        assert row["read_only_export"] and sha(Path(row["path"]).read_bytes()) == row["sha256"]
        snapshots[row["frame"]] = Path(row["path"]).read_bytes()
    arm = rom.read_file("/__arm9__.bin")
    kanji = rom.read_file("/GRP/KANJI.FNT")
    clean = NdsImage.open("work/clean.nds")
    assert kanji == clean.read_file("/GRP/KANJI.FNT")
    mapping = struct.unpack_from(f"<{SJIS_GLYPH_COUNT}H", arm, SJIS_MAP_OFFSET)
    assert arm[SJIS_MAP_OFFSET:SJIS_MAP_OFFSET + SJIS_GLYPH_COUNT * 2] == clean.read_file(
        "/__arm9__.bin")[SJIS_MAP_OFFSET:SJIS_MAP_OFFSET + SJIS_GLYPH_COUNT * 2]
    images = {frame: Image.open(row["path"]).convert("RGB") for frame, row in frames.items()}
    latin = images[5500]
    glyphs, union = [], set()
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for index, char in enumerate(letters):
        full = chr(ord(char) + 0xFEE0)
        code = int.from_bytes(full.encode("cp932"), "big")
        slot = mapping.index(code)
        mask = decode_glyph(kanji, slot)
        assert not any(mask.getpixel((x, y)) for x in range(12, 16) for y in range(11))
        left, top = 56 + index % 10 * 14, 216 + index // 10 * 14
        points = 0
        for y in range(11):
            for x in range(12):
                ink = bool(mask.getpixel((x, y)))
                assert (latin.getpixel((left + x, top + y)) == (230, 230, 230)) == ink
                if ink:
                    points += 1
                    union.add((left + x, top + y))
        glyphs.append({"letter": char, "source_character": full, "code_hex": full.encode("cp932").hex(),
                       "glyph_index": slot, "bounds": [left, top, left + 12, top + 11],
                       "complete_ink_pixels": points})
    for y in range(216, 300):
        for x in range(56, 196):
            assert (latin.getpixel((x, y)) == (230, 230, 230)) == ((x, y) in union)
    font = GameAsciiFont.from_arm9(arm)
    english = []
    for frame, text, x, y, color in [(4400, "Name: Edit", 16, 198, (230, 230, 230)),
                                    (4800, "Name", 48, 224, (213, 214, 213)),
                                    (4800, "Rafael", 60, 244, (230, 230, 230)),
                                    (5900, "Rafael", 60, 244, (230, 230, 230)),
                                    (2000, "Rafael", 89, 220, (230, 230, 230)),
                                    (6100, "Rafael", 89, 220, (230, 230, 230)),
                                    (6100, "Name: Edit", 16, 198, (230, 230, 230))]:
        ink, bounds = complete_mask(font, text, images[frame], x, y, color)
        english.append({"frame": frame, "text": text, "bounds": bounds, "complete_ink_pixels": ink})
    buffer = PARENT + 0xB4 - BASE
    expected_buffers = {4800: b"Rafael\0", 5200: b"Rafael\0", 5500: b"Rafael\0",
                        5700: b"Rafael\x82\x81\0", 5900: b"Rafael\0"}
    states = []
    for frame, expected in expected_buffers.items():
        raw = snapshots[frame]
        assert raw[buffer:buffer + len(expected)] == expected
        words = [struct.unpack_from("<I", raw, PARENT - BASE + offset)[0]
                 for offset in (0, 4, 0x38, 0xD8)]
        assert words == [0x021558CC, 0x0215591C, 0x02155D44, 16]
        states.append({"frame": frame, "editor_parent": PARENT, "buffer": PARENT + 0xB4,
                       "bytes_with_NUL_hex": expected.hex(), "name_capacity": 16,
                       "native_parent_provider_and_child_vtables": words[:3]})
    u = machine(arm)
    u.mem_write(BASE, snapshots[5500])
    label = 0x02470000
    u.mem_write(label, "英".encode("cp932") + b"\0")
    call(u, 0xD1E3C, (PARENT + 4, label))
    assert u.reg_read(UC_ARM_REG_R0) == 50
    keys = 0x02470100
    u.mem_write(0x027F0000, struct.pack("<I", 0xFFFFFFFF))
    call(u, 0xD1BBC, (PARENT + 4, 50, keys, 0))
    count = u.reg_read(UC_ARM_REG_R0)
    table = bytes(u.mem_read(keys, count * 2))
    assert count == 52 and table.decode("cp932") == "".join(chr(ord(c) + 0xFEE0) for c in letters)
    # B returns to editing; it does not leave that state for the biography.
    assert images[4400].tobytes() == images[6500].tobytes()
    confirmation_differences = []
    for y in range(384):
        for x in range(256):
            if images[2000].getpixel((x, y)) != images[6100].getpixel((x, y)):
                assert 16 <= x < 100 and 198 <= y < 209
                confirmation_differences.append([x, y])
    assert len(confirmation_differences) == 182
    confirm = PxlImage.from_bytes(rom.read_file("/_pxl/kakutei.pxl"))
    confirm_matches = {str(frame): full_sprite_matches(images[frame], confirm)
                       for frame in (2000, 4400, 4800, 5500, 5700, 5900, 6100, 6500)}
    assert not any(confirm_matches.values())
    sections = [(s.ramAddress, bytes(s.data)) for s in MainCodeFile(arm, BASE).sections]
    sections += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).values()]
    references = []
    for base, data in sections:
        for at in range(0, len(data) - 3, 4):
            instruction = struct.unpack_from("<I", data, at)[0]
            if instruction & 0x0F7F0000 != 0x051F0000:
                continue
            literal = at + 8 + (instruction & 4095) * (1 if instruction & 0x800000 else -1)
            if 0 <= literal <= len(data) - 4 and struct.unpack_from("<I", data, literal)[0] == OWNER:
                references.append({"instruction": base + at, "literal": base + literal, "owner": OWNER})
    assert [row["instruction"] for row in references] == [0x0210EBDC, 0x0210EBE8]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    archived = []
    for frame in (2400, 4000, 4400, 4800, 5500, 5700, 5900, 6100, 6500):
        source = Path(frames[frame]["path"])
        dest = ARCHIVE / source.name
        shutil.copyfile(source, dest)
        archived.append({"path": str(dest), "sha256": sha(dest.read_bytes()),
                         "unmodified_native_frame": True, "ordinary_controller_and_stylus_only": True})
    (ROOT / "final_recorded_inputs.json").write_text(json.dumps(run["scripted_input_schedule"], indent=2) + "\n", encoding="utf-8")
    result = {"candidate": str(ROM), "candidate_sha256": digest, "production_changed": False,
              "capture_report": str(CAPTURE / "capture_report.json"),
              "capture_report_sha256": sha((CAPTURE / "capture_report.json").read_bytes()),
              "ordinary_new_game_Y_Edit_then_A_opens_keyboard": True,
              "Latin_toggle_requires_selection_then_A": True,
              "all52_original_Latin_keyboard_glyphs": glyphs, "complete_Latin_popup_mask_pixels": 11760,
              "complete_Latin_ink_pixels": len(union), "complete_English_headers_and_names": english,
              "native_editor_states": states, "native_live_provider_Latin_index": 50,
              "native_generated_Latin_table_hex": table.hex(),
              "fullwidth_a_inserted_then_deleted_and_unchanged_Rafael_finished": True,
              "whole_name_edit_frame_exact_before_after": True,
              "confirmation_exact_outside_182_state_header_differences": True,
              "confirmation_header_remains_Name_Edit_during_edit_state": True,
              "no_existing_save_loaded_and_no_gameplay_save_action": True, "no_synthetic_fixtures": True,
              "Confirm_exact_sprite_search": confirm_matches, "Confirm_owner_PC_relative_loads": references,
              "linear_disassembly_zero_reference_diagnostic_superseded": True,
              "indirect_computed_aliases_and_other_Confirm_parents_not_excluded": True,
              "five_miniature_normal_consumers_and_Confirm_parent_remain_open": True,
              "all18_plaques_remain_incomplete_and22_historical_objects_retained": True,
              "guide_candidates_publication_approved": False, "archive": str(ARCHIVE),
              "screenshots": archived, "full_goal_complete": False, "hardware_device_verification": False}
    proof = ROOT / "native_name_editor_proof.json"
    proof.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for path in (proof, ROOT / "final_recorded_inputs.json", CAPTURE / "capture_report.json"):
        shutil.copyfile(path, ARCHIVE / path.name)
    print(f"V582: ordinary Y Edit entry, all52 Latin glyphs/{len(union)} ink points, native insertion/delete and complete unchanged-name return pass; Confirm context remains open.")


if __name__ == "__main__":
    main()
