"""Verify cold-boot menu captions and resolve the six actual cached views."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.research_online_loader_v190 import resource_call
from scripts.verify_crew_menu_live_v243 import CASES

ROM = Path("out/all_routes_combined_v245_candidate.nds")
CAPTURE = Path("work/emulation_v193/radial_marker_v245")
PREVIOUS = Path("work/emulation_v193/crew_buttons_v243/navigation")
ROOT = Path("work/analysis/radial_marker_v245")


def read_report(path, digest):
    report = json.loads((path / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    assert report["core_DLL_sha256"] == "42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b"
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    return report


def get_frame(report, n):
    row = next(r for r in report["frames_captured"] if r["frame"] == n)
    return Image.open(row["path"]).convert("RGB"), row


def main():
    digest = sha(ROM.read_bytes())
    report = read_report(CAPTURE, digest)
    previous = read_report(PREVIOUS, "d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027")
    assert report["scripted_input_schedule"] == previous["scripted_input_schedule"]
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    cases = []
    for frame, text, x, y, advance, color in CASES:
        actual, row = get_frame(report, frame)
        mask = Image.new("1", ((len(text) - 1) * advance + 6, 11))
        for n, ch in enumerate(text):
            layer = Image.new("1", mask.size)
            layer.paste(font.decode(ch), (n * advance, 0))
            mask = ImageChops.lighter(mask, layer)
        for dy in range(11):
            for dx in range(mask.width):
                assert (actual.getpixel((x + dx, y + dy)) == color) == bool(mask.getpixel((dx, dy)))
        old, _ = get_frame(previous, frame)
        bounds = ImageChops.difference(actual, old).getbbox()
        cases.append({"text": text, "frame": frame, "capture": row,
                      "complete_native_font_mask_and_first_last_letters_exact": True,
                      "changed_framebuffer_bounds_vs_V241": list(bounds) if bounds else None})
    earlier_frames = []
    for n in (1, 60, 180, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000):
        actual, _ = get_frame(report, n)
        old, _ = get_frame(previous, n)
        assert actual.tobytes() == old.tobytes()
        earlier_frames.append(n)
    snapshot = report["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    assert len(ram) == 0x400000 and sha(ram) == snapshot["sha256"]
    owner, resource = 0x02313F74, rom.read_file("/_pxl/__marker.pxl")
    u = machine(rom.read_file("/__arm9__.bin"))
    u.mem_write(0x02000000, ram)
    views = []
    needle, start = struct.pack("<I", owner), 0
    while (offset := ram.find(needle, start)) >= 0:
        start = offset + 1
        if offset < 12 or offset % 4 or offset + 36 > len(ram):
            continue
        fields = struct.unpack_from("<12I", ram, offset - 12)
        if fields[0] != 0x0214B190 or fields[7] != 0 or fields[10:12] != (64, 24):
            continue
        assert fields[8] in (0, 24, 48, 72, 96, 120)
        assert fields[9] & 0xFF == 10  # Higher padding bytes are not a palette index.
        pointer = 0x02000000 + offset - 12
        before_view = bytes(u.mem_read(pointer, 48))
        resource_call(u, 0xD4170, (pointer,))
        loaded = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(loaded, len(resource))) == resource
        assert bytes(u.mem_read(pointer, 48)) == before_view
        views.append({"actual_live_view": pointer, "source_origin": list(fields[7:9]),
                      "crop_extent": [64, 24], "palette_parameter_byte": fields[9] & 0xFF,
                      "loaded_resource_pointer": loaded, "complete_resource_bytes_exact": len(resource),
                      "native_resolver_stack_saved_register_and_view_preservation_pass": True})
    assert len(views) == 6 and {v["source_origin"][1] for v in views} == {0, 24, 48, 72, 96, 120}
    proof = {"format": "dk4-radial-marker-live-proof-v245", "ROM_sha256": digest,
             "live_caption_cases": cases, "earlier_complete_frame_matches": earlier_frames,
             "actual_live_marker_views_and_original_warm_cache_resolution": views,
             "actual_view_resource_bytes_verified": 6 * len(resource),
             "all_native_source_crops_within_256_by256_marker": True,
             "warm_snapshot_resolution_is_CPU_replay_not_additional_physical_render": True,
             "virtual_slot_16_not_used_or_claimed_as_image_getter": True,
             "full_pixel_panel_palette_alpha_composition_not_inferred_from_caption_masks": True,
             "ROM_already_compiled_registered_and_exact_patch_verified": True,
             "full_goal_complete": False}
    (ROOT / "live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    saved_path = ROOT / "saved_proof.json"
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    saved["cold_boot_display_pending"] = False
    saved["live_proof"] = str(ROOT / "live_proof.json")
    saved["live_proof_sha256"] = sha((ROOT / "live_proof.json").read_bytes())
    saved_path.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_live_caption_cases": len(cases), "earlier_complete_frame_matches": len(earlier_frames),
                      "actual_native_cached_views": len(views), "cached_resource_bytes_verified": 6 * len(resource)}))


if __name__ == "__main__":
    main()
