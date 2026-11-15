"""Source-preserving raw16 versus opaque-bit control in a borrowed native widget.

Research files are not playable releases or proof of the comic's real consumer.
"""

import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/raw_direct_color_v587")
PARENT = Path("out/all_routes_combined_v581_candidate.nds")
FILE, STRING_OFFSET = "/_pxl/logo.pxl", 0x134BC8
ORIGINAL = b"/evstill/evstill%03u.pxl\0"


def contents(rom):
    return {p: raw for _, p, raw in rom.iter_files()} | dict(rom.iter_components())


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    digest = sha(PARENT.read_bytes())
    assert digest == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    parent = NdsImage.open(PARENT)
    before = contents(parent)
    arm = before["/__arm9__.bin"]
    assert arm[STRING_OFFSET:STRING_OFFSET + len(ORIGINAL)] == ORIGINAL
    block = IlnkContainer.parse(before["/GRP/SLACKIMG.DK4"]).blocks[19]
    assert len(block) == 21 * 320 * 240 * 2
    words = struct.unpack(f"<{len(block) // 2}H", block)
    assert not any(v & 0x8000 for v in words)
    frame = block[6 * 153600:7 * 153600]
    assert len(frame) == 153600
    packet = (FILE.encode("ascii") + b"\0").ljust(len(ORIGINAL), b"\0")
    fixture_arm = arm[:STRING_OFFSET] + packet + arm[STRING_OFFSET + len(ORIGINAL):]
    rows = []
    viewport = b"".join(frame[(y * 320 + 32) * 2:(y * 320 + 288) * 2] for y in range(32, 160))
    caption = b"".join(frame[(y * 320 + 40) * 2:(y * 320 + 112) * 2] for y in range(96, 128))
    specs = [("source_highbits", frame, 320, 240, False),
             ("opaque_bit_control", frame, 320, 240, True),
             ("viewport_source_highbits", viewport, 256, 128, False),
             ("viewport_opaque_control", viewport, 256, 128, True),
             ("caption_source_highbits", caption, 72, 32, False),
             ("caption_opaque_control", caption, 72, 32, True)]
    for mode, selected_pixels, width, height, opaque in specs:
        count = width * height
        header = struct.pack("<5I", 16, width, height, 20, 20)
        pixels = struct.pack(f"<{count}H", *(v | 0x8000 for v in struct.unpack(f"<{count}H", selected_pixels))) if opaque else selected_pixels
        fixture = NdsImage.open(PARENT)
        fixture.replace_file("/__arm9__.bin", fixture_arm)
        fixture.replace_file(FILE, header + pixels)
        target = ROOT / f"comic06_{mode}_RESEARCH_ONLY.nds"
        if target.exists():
            saved = NdsImage.open(target)
            assert contents(saved) == contents(fixture)
        else:
            fixture.save(target)
        after = contents(NdsImage.open(target))
        assert before.keys() == after.keys()
        assert sorted(p for p in before if before[p] != after[p]) == sorted(["/__arm9__.bin", FILE])
        assert after["/__arm9__.bin"] == fixture_arm
        assert after[FILE] == header + pixels
        assert after["/GRP/SLACKIMG.DK4"] == before["/GRP/SLACKIMG.DK4"]
        assert all((a & 0x7FFF) == (b & 0x7FFF) for a, b in zip(
            struct.unpack(f"<{count}H", selected_pixels), struct.unpack(f"<{count}H", pixels), strict=True))
        record = {"research_only": True, "not_registered_playable_candidate": True,
                  "parent": str(PARENT), "parent_sha256": digest,
                  "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
                  "mode": mode, "source_archive": "/GRP/SLACKIMG.DK4", "source_block": 19,
                  "source_frame": 6, "source_frame_sha256": sha(frame), "source_block_sha256": sha(block),
                  "explicit_source_viewport": [0, 0, 320, 240] if width == 320 else [32, 32, 288, 160] if width == 256 else [40, 96, 112, 128],
                  "selected_source_pixel_bytes_sha256": sha(selected_pixels),
                  "source_all21_frames_high_bits_clear": True,
                  "supplied_direct16_PXL_header_words": list(struct.unpack("<5I", header)),
                  "replacement_file": FILE, "replacement_sha256": sha(header + pixels),
                  "pixel_bytes_exact_raw_frame": mode == "source_highbits",
                  "pixel_bytes_exact_selected_source_window": not opaque,
                  "only_high_bit_changed_in_control": opaque,
                  "all_original_low15_color_words_exact": True,
                  "only_other_change_filename_literal_span": [STRING_OFFSET, len(ORIGINAL)],
                  "all_ARM_instructions_original_routes_and_archive_bytes_preserved": True,
                  "borrowed_event_still_widget_not_original_comic_scene_or_descriptor": True,
                  "production_ROM_and_patch_changed": False}
        target.with_suffix(".fixture.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        rows.append(record)
    # Positive control: the exact current indexed logo, with only the same
    # filename substitution. A missing raw image is not an opacity result.
    control = NdsImage.open(PARENT)
    control.replace_file("/__arm9__.bin", fixture_arm)
    target = ROOT / "indexed8_positive_RESEARCH_ONLY.nds"
    if target.exists():
        assert contents(NdsImage.open(target)) == contents(control)
    else:
        control.save(target)
    control_contents = contents(NdsImage.open(target))
    assert [p for p in before if before[p] != control_contents[p]] == ["/__arm9__.bin"]
    positive = {"research_only": True, "not_registered_playable_candidate": True,
                "parent": str(PARENT), "parent_sha256": digest,
                "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
                "mode": "indexed8_positive", "source_file": FILE,
                "all_original_artwork_and_routes_exact": True,
                "only_change_filename_literal_span": [STRING_OFFSET, len(ORIGINAL)],
                "production_ROM_and_patch_changed": False}
    target.with_suffix(".fixture.json").write_text(json.dumps(positive, indent=2) + "\n", encoding="utf-8")
    rows.append(positive)
    # Lossless indexed comparison of exactly the same tiny caption. No color
    # quantization or resizing: every original low15 source word maps exactly.
    caption_words = struct.unpack("<2304H", caption)
    colors = sorted(set(caption_words))
    assert 1 < len(colors) <= 256
    indices = {value: n for n, value in enumerate(colors)}
    palette = struct.pack("<256H", *([v | 0x8000 for v in colors] + [0x8000] * (256 - len(colors))))
    indexed = struct.pack("<5I", 0x108, 36, 32, 20, 532) + palette + bytes(indices[v] for v in caption_words)
    control = NdsImage.open(PARENT)
    control.replace_file("/__arm9__.bin", fixture_arm)
    control.replace_file(FILE, indexed)
    target = ROOT / "caption_indexed8_lossless_RESEARCH_ONLY.nds"
    if target.exists():
        assert contents(NdsImage.open(target)) == contents(control)
    else:
        control.save(target)
    saved = contents(NdsImage.open(target))
    assert sorted(p for p in before if before[p] != saved[p]) == sorted(["/__arm9__.bin", FILE])
    indexed_record = {"research_only": True, "not_registered_playable_candidate": True,
                      "parent": str(PARENT), "parent_sha256": digest,
                      "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
                      "mode": "caption_indexed8_lossless", "source_frame": 6,
                      "explicit_source_viewport": [40, 96, 112, 128],
                      "selected_source_pixel_bytes_sha256": sha(caption),
                      "lossless_palette_colors": len(colors), "source_low15_colors_exact": True,
                      "replacement_file": FILE, "replacement_sha256": sha(indexed),
                      "source_archive_and_all_routes_and_ARM_instructions_exact": True,
                      "supplied_format_control_not_original_comic_loader": True,
                      "production_ROM_and_patch_changed": False}
    target.with_suffix(".fixture.json").write_text(json.dumps(indexed_record, indent=2) + "\n", encoding="utf-8")
    rows.append(indexed_record)
    inputs = Path("work/analysis/standalone_resource_compatibility_v550/fixtures/opening_inputs.json").read_bytes()
    (ROOT / "opening_inputs.json").write_bytes(inputs)
    (ROOT / "fixture_manifest.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    assert sha(PARENT.read_bytes()) == digest
    print("Eight source/format research controls prepared;21 original high-bit-clear frames;production unchanged.")


if __name__ == "__main__":
    main()
