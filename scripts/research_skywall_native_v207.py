"""Partition all sky records through the actual loader; display layout stays open."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import audit_standard_font
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/skywall_native_v207")
ROM = Path("out/all_routes_combined_v205_candidate.nds")
BUFFER = 0x02480020
OPEN, SEEK, READ, CLOSE = 0x020DED50, 0x020DEB70, 0x020DEBDC, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    arm, original = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    assert arm[0x7BA3C:0x7BB80] == original[0x7BA3C:0x7BB80]
    raw = rom.read_file("/GRP/SKYWALL.DK4")
    assert raw == clean.read_file("/GRP/SKYWALL.DK4")
    assert len(raw) == 13 * 0x2200 + 0x4200
    u = machine(arm)
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (OPEN, SEEK, READ, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 80)).split(b"\0")[0]
            path = name.decode("ascii").replace("\\", "/")
            assert path == "/GRP/SKYWALL.DK4" and not handles
            handles[obj] = 0
            value = 1
            events.append({"operation": "open", "path": path})
        elif address == SEEK:
            position = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= position < len(raw)
            handles[obj] = position
            events.append({"operation": "seek", "offset": position})
            value = 1
        elif address == READ:
            destination, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            position = handles[obj]
            assert position + count <= len(raw) and destination == BUFFER
            uc.mem_write(destination, raw[position:position + count])
            handles[obj] += count
            events.append({"operation": "read", "offset": position, "bytes": count})
            value = count
        else:
            handles.pop(obj)
            events.append({"operation": "close"})
            value = 1
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    records = []
    sheet = Image.new("RGB", (4 * 148, 4 * 160), (230, 230, 230))
    draw = ImageDraw.Draw(sheet)
    try:
        for index in range(14):
            size = 0x4200 if index == 13 else 0x2200
            offset = index * 0x2200
            u.mem_write(BUFFER - 16, b"\xa5" * (0x4200 + 32))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_R4, index)
            u.reg_write(UC_ARM_REG_R5, 0x2200)
            u.reg_write(UC_ARM_REG_R8, BUFFER)
            start = len(events)
            u.emu_start(0x0207BA3C, 0x0207BA7C, count=10000)
            assert u.reg_read(UC_ARM_REG_PC) == 0x0207BA7C
            assert u.reg_read(UC_ARM_REG_SP) == STACK and not handles
            assert u.reg_read(UC_ARM_REG_R4) == index
            assert u.reg_read(UC_ARM_REG_R5) == size and u.reg_read(UC_ARM_REG_R8) == BUFFER
            loaded = bytes(u.mem_read(BUFFER, size))
            assert loaded == raw[offset:offset + size]
            assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(BUFFER + size, 16)) == b"\xa5" * 16
            pixels, palette = loaded[:-512], loaded[-512:]
            # Diagnostic 8-bit tile atlas only. Native screen assembly is not inferred.
            colors = [((v & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31,
                       ((v >> 10) & 31) * 255 // 31) for v in struct.unpack("<256H", palette)]
            atlas = Image.new("RGB", (128, len(pixels) // 128))
            for tile in range(len(pixels) // 64):
                tx, ty = tile % 16 * 8, tile // 16 * 8
                for p in range(64):
                    atlas.putpixel((tx + p % 8, ty + p // 8), colors[pixels[tile * 64 + p]])
            path = ROOT / f"record_{index:02d}_diagnostic_8bit_tiles.png"
            atlas.save(path)
            x, y = index % 4 * 148, index // 4 * 160
            sheet.paste(atlas, (x, y + 20))
            draw.text((x, y), f"{index}: {len(pixels)}+512", fill=(0, 0, 0))
            records.append({"index": index, "offset": offset, "bytes": size,
                            "complete_native_read_sha256": sha(loaded), "pixel_transfer_bytes": len(pixels),
                            "trailing_palette_bytes": 512, "events": events[start:],
                            "guards_and_fragment_registers_exact": True,
                            "diagnostic_atlas": path.as_posix(), "atlas_sha256": sha(path.read_bytes())})
    finally:
        u.hook_del(hook)
    assert sum(r["bytes"] for r in records) == len(raw)
    sheet.save(ROOT / "all_records_diagnostic.png")
    font = rom.read_file("/GRP/KANJI.FNT")
    assert font == clean.read_file("/GRP/KANJI.FNT")
    font_audit = audit_standard_font(arm, font)
    assert font_audit["all_renderer_signatures_match"]
    assert font_audit["shift_jis"]["map_sorted"] and font_audit["shift_jis"]["font_size_matches_map"]
    assert font_audit["shift_jis"]["matches_clean_reference"]
    proof = {"format": "dk4-raw-sky-partition-native-proof-v1", "ROM": ROM.as_posix(),
             "ROM_sha256": sha(ROM.read_bytes()), "source_file": "/GRP/SKYWALL.DK4",
             "source_sha256": sha(raw), "complete_file_bytes": len(raw), "records": records,
             "native_fragment": ["0207BA3C", "0207BA7C"],
             "native_transfer_split_evidence": "0207BA80..0207BAA8 passes size-512 pixel bytes and trailing 512 palette bytes to native BG transfer functions; those hardware routines are not executed here.",
             "index_and_preceding_buffer_context_supplied": True,
             "only_SDK_filesystem_bridged": True, "GPU_tile_depth_layout_city_assignment_pending": True,
             "atlas_scope": "Diagnostic 8-bit tile interpretation, not a proven displayed sky or translation-clearance image.",
             "diagnostic_visual_review": "pending", "KANJI_FNT": font_audit,
             "KANJI_decision": "Retain original character font, not composed Japanese UI artwork. Individual source glyphs must remain available to render source names and user input.",
             "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_sky_record_reads": len(records), "complete_file_bytes": len(raw),
                      "font_records": font_audit["shift_jis"]["glyph_count"], "display_classification_still_open": True}))


if __name__ == "__main__":
    main()
