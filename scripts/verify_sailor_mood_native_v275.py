"""Source battle context and complete status glyphs through the native renderer."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.sailor_mood_caption import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_modal_cursor_native_v272 import raster
from scripts.verify_sailor_status_tables_v274 import verify_selectors

ROOT = Path("work/analysis/sailor_mood_v275")


def main():
    original_rom = NdsImage.open("work/clean.nds")
    clean = original_rom.read_file("/__arm9__.bin")
    prior = NdsImage.open("out/all_routes_combined_v272_candidate.nds").read_file("/__arm9__.bin")
    target, plan = transform(prior, clean)
    assert target == (ROOT / "research_arm9.bin").read_bytes()
    assert verify_selectors(clean) == verify_selectors(target)
    # Original positive battle-message groups are literal operands of the
    # effect routine that writes Mood0 or Mood1. Preserve them as source evidence.
    entries = common_message_entries(original_rom.read_file("/COMMON/MESFILE.DK4"), clean)
    messages = []
    for state, descriptor in [(0, 0x117F40), (1, 0x117F80)]:
        ids = struct.unpack_from("<8I", clean, descriptor)
        messages.append({"Mood_state": state, "descriptor": hex(0x02000000 + descriptor),
                         "messages": [{"id": n, "Japanese": entries[n].text.decode("cp932")} for n in ids]})
    assert struct.unpack_from("<I", clean, 0x659C4)[0] == 0xE3A01000  # mov r1,#0
    assert struct.unpack_from("<I", clean, 0x659E0)[0] == 0xE3A01001  # mov r1,#1
    assert struct.unpack_from("<I", clean, 0x659F8)[0] == 0x02117F40
    assert struct.unpack_from("<I", clean, 0x659FC)[0] == 0x02117F80
    assert prior[0x65968:0x65A00] == target[0x65968:0x65A00] == clean[0x65968:0x65A00]
    font = GameAsciiFont.from_arm9(target)
    cases = []
    for name, table, count in [("Mood", 0x1483B0, 6), ("Health", 0x1483C8, 7)]:
        for state in range(count):
            pointer = struct.unpack_from("<I", target, table + 4 * state)[0]
            raw = target[pointer - 0x02000000:].split(b"\0", 1)[0]
            actual, events, returned = raster(target, raw, width=48, height=16, wrapping=0)
            assert returned == len(raw)
            visible = [e for e in events if e["code"] != 32]
            assert [e["code"] for e in visible] == list(raw)
            assert [(e["x"], e["y"]) for e in visible] == [(6 * i, 0) for i in range(len(raw))]
            expected = bytearray(48 * 16)
            for n, c in enumerate(raw):
                glyph = font.decode(chr(c))
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[y * 48 + n * 6 + x] = 1
            assert actual == expected, (name, state)
            changed = name == "Mood" and state == 0
            if not changed:
                assert raster(prior, raw, width=48, height=16, wrapping=0) == (actual, events, returned)
            cases.append({"field": name, "state": state, "English": raw.decode("ascii"),
                          "ink_pixels": sum(expected), "all_glyph_cells_and_complete_pixels": True,
                          "first_and_final_glyph_complete": True,
                          "other_status_pixels_positions_and_return_unchanged": not changed})
    proof = {"format": "dk4-sailor-mood-native-v275", "plan": plan,
             "original_battle_context": messages,
             "source_effect_code_and_message_operands_exact": True,
             "all512_target_native_selector_values_match_original_pointers_and_ABI": True,
             "Sailor_Info_native_getter_and_renderer_call_sites": ["020807AC", "020807B8", "020807D0", "020807DC"],
             "all13_status_glyph_cases": cases, "other12_native_status_rasters_exact_to_V272": True,
             "Excited_complete_ink_pixels": cases[0]["ink_pixels"],
             "loaded_bitmap_and_context_are_controlled_native_inputs": True,
             "native_bitmap_input_header_and_saved_register_stack_guards_pass": True,
             "actual_excited_gameplay_display_pending": True,
             "all18_plaque_hint_entries_remain_incomplete": True, "full_goal_complete": False}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"states": len(cases), "Excited_ink": cases[0]["ink_pixels"], "other12_rasters_exact": True}))


if __name__ == "__main__":
    main()
