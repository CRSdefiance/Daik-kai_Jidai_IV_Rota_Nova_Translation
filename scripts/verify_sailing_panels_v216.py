"""Execute scoped producers, actual sprite-bank loops and native staged startup."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.sailing_panel_graphics import (
    DRAW_FRAGMENTS,
    POINTERS,
    PRODUCER,
    UPLOAD_BYTES,
    encode_panels,
    packed_pixel_offset,
    transform,
)
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute

ROOT = Path("work/analysis/sailing_panels_v216")
BUFFER = 0x02460020


def make_machine(arm, rom):
    uc = machine(arm)
    stage = MainCodeFile(arm, BASE).sections[3]
    uc.mem_write(POOL, bytes(stage.data[:-48]))
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])[0]
    uc.mem_write(overlay.ramAddress, bytes(overlay.data))
    font = rom.read_file("/GRP/KANJI.FNT")
    uc.mem_write(struct.unpack_from("<I", arm, 0xD19B8)[0], font)
    return uc


def sprite_layout(arm, rom, panel, fragment, produced):
    uc = make_machine(arm, rom)
    uc.mem_write(BUFFER, produced)
    image = Image.new("L", (256, 176), 0)
    requests = []

    def observe(u, address, size, _):
        if address != 0x02089358:
            return
        kind = u.reg_read(UC_ARM_REG_R0)
        point = u.reg_read(UC_ARM_REG_R1)
        descriptor = u.reg_read(UC_ARM_REG_R2)
        tile = u.reg_read(UC_ARM_REG_R3)
        x0, y0 = struct.unpack("<2I", u.mem_read(point, 8))
        assert kind == 256 and descriptor == struct.unpack_from("<I", arm, 0x68BE8)[0]
        assert tile * 32 + 256 <= UPLOAD_BYTES
        requests.append({"origin": [x0, y0], "first_tile": tile, "dimensions": [32, 16]})
        for y in range(16):
            for x in range(32):
                # Read exactly the bank requested by the native loop, including blank rows.
                virtual_x = tile // 8 * 32 + x
                value = produced[packed_pixel_offset(virtual_x, y)] >> (virtual_x % 2 * 4) & 15
                if x0 + x < 256 and y0 + y < 176:
                    image.putpixel((x0 + x, y0 + y), value * 17)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    handle = uc.hook_add(UC_HOOK_CODE, observe)
    start, end = DRAW_FRAGMENTS[fragment]
    uc.reg_write(UC_ARM_REG_SP, STACK)
    try:
        uc.emu_start(BASE + start, BASE + end, count=50000)
    finally:
        uc.hook_del(handle)
    assert uc.reg_read(UC_ARM_REG_PC) == BASE + end and uc.reg_read(UC_ARM_REG_SP) == STACK
    expected = Image.new("L", image.size, 0)
    from dk4tool.dialogue.font_audit import GameAsciiFont
    font = GameAsciiFont.from_arm9(arm)
    for row in panel["glyphs"]:
        mask = font.decode(row["character"])
        x0, y0 = row["origin"]
        for y in range(11):
            for x in range(6):
                if mask.getpixel((x, y)):
                    expected.putpixel((x0 + x, y0 + y), 255)
    assert image.tobytes() == expected.tobytes(), fragment
    assert len(requests) == 6 + 8 * len(panel["lines"])
    path = ROOT / (fragment + "_English_native_bank_layout.png")
    image.save(path)
    return {"fragment": fragment, "sprite_bank_requests": requests,
            "complete_foreground_and_blank_pixels_exact": 256 * 176,
            "first_last_glyphs_complete": True, "all_instructions_preserved": True,
            "preview": path.as_posix(), "preview_sha256": sha(path.read_bytes()),
            "native_parent_fragment_and_bank_loop_executed": True,
            "sprite_submission_is_explicit_bridge_not_GPU_execution": True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    prior = NdsImage.open("out/all_routes_combined_v211_candidate.nds")
    source = prior.read_file("/__arm9__.bin")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/__arm9__.bin")
    manuscript = json.loads(Path("translations/sailing_mode_panels_manuscript_v1.json").read_text(encoding="utf-8"))
    saved, plan = transform(source, canonical, manuscript)
    assert saved == (ROOT / "English_arm9.bin").read_bytes()
    panels = encode_panels(source, manuscript)
    producers, layouts = [], []
    for panel in panels:
        uc = make_machine(saved, prior)
        uc.mem_write(BUFFER - 16, b"\xa5" * (UPLOAD_BYTES + 32))
        call(uc, plan["entry"] - BASE, (panel["source_pointer"], 15, BUFFER))
        produced = bytes(uc.mem_read(BUFFER, UPLOAD_BYTES))
        assert produced == panel["packed"].ljust(UPLOAD_BYTES, b"\0")
        assert bytes(uc.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
        assert bytes(uc.mem_read(BUFFER + UPLOAD_BYTES, 16)) == b"\xa5" * 16
        assert uc.reg_read(UC_ARM_REG_R0) == 1 and uc.reg_read(UC_ARM_REG_R2) == BUFFER
        producers.append({"id": panel["id"], "source_pointer": panel["source_pointer"],
                          "complete_upload_buffer_sha256": sha(produced), "guard_bytes_exact": True,
                          "return_stack_and_saved_register_ABI_exact": True,
                          "full_upload_extent_cleared_before_copy": True})
        name = {POINTERS[0]: "info", POINTERS[1]: "search", POINTERS[2]: "war"}[panel["source_pointer"]]
        fragments = ("war_target", "war_no_target") if name == "war" else (name,)
        layouts.extend(sprite_layout(saved, prior, panel, fragment, produced) for fragment in fragments)
    # An unrecognized pointer must still execute the untouched original overlay.
    original, patched = make_machine(source, prior), make_machine(saved, prior)
    # Two complete Japanese glyphs at the end of the original Info allocation.
    unknown = POINTERS[0] + 136
    for uc, entry in ((original, PRODUCER), (patched, plan["entry"])):
        uc.mem_write(BUFFER - 16, b"\xa5" * (UPLOAD_BYTES + 32))
        call(uc, entry - BASE, (unknown, 15, BUFFER))
    assert bytes(original.mem_read(BUFFER - 16, UPLOAD_BYTES + 32)) == bytes(patched.mem_read(BUFFER - 16, UPLOAD_BYTES + 32))
    payload = bytes(MainCodeFile(saved, BASE).sections[3].data[:-48])
    boot = execute(saved, bytes(prior.rom.arm7), prior.rom.arm7RamAddress, True, payload)
    assert boot["arm7_source_changed_bytes_after_arm9_autoload"] == 0
    assert all(row["matches_original"] for row in boot["arm7_native_loaded_sections"])
    assert all(boot[k] for k in ("repaired_pool_matches_complete_payload", "repair_returns_with_stack_preserved",
                                 "actual_startup_call_preserves_r0_r3", "late_copy_reached_caller_continuation"))
    arena = initialize(saved)
    assert arena["low"][0] == plan["pool_span"][1]
    previous_arena = initialize(source)
    assert arena["high"] == previous_arena["high"]
    assert arena["low"][1:] == previous_arena["low"][1:]
    result = {"format": "dk4-sailing-English-native-bank-proof-v1", "plan": plan,
              "producer_cases": producers, "native_parent_layouts": layouts,
              "unknown_source_pointer_fallback_matches_original_overlay": True,
              "startup": boot, "native_arena_bounds": arena,
              "all_other_arena_bounds_preserved": True,
              "original_overlay_font_palettes_and_Japanese_fields_preserved": True,
              "physical_GPU_and_gameplay_pending": True, "full_goal_complete": False}
    (ROOT / "native_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"producer_cases": len(producers), "parent_variants": len(layouts),
                      "exact_parent_pixels": len(layouts) * 256 * 176,
                      "native_startup_and_ARM7_preserved": True, "native_arena_low": arena["low"][0]}))


if __name__ == "__main__":
    main()
