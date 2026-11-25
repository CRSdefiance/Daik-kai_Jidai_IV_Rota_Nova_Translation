"""Connected original partial archive reads and raw16 software-copy contracts.

The descriptor/crop are supplied research inputs, not a discovered comic scene.
"""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine

ROOT = Path("work/analysis/raw_direct_color_v587")
HEADER, POINT, SIZE, DEST = 0x02420020, 0x02470000, 0x02470020, 0x02470040
FB = 0x022E1794
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    rom, clean = NdsImage.open("out/all_routes_combined_v581_candidate.nds"), NdsImage.open("work/clean.nds")
    arm, original_arm = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    u, original = machine(arm), machine(original_arm)
    regions = [(0x0204704C, 0x020470B4), (0x020D1EF0, 0x020D2138),
               (0x01FF92D8, 0x01FF97D0), (0x020E28E0, 0x020E28FC)]
    for lo, hi in regions:
        assert bytes(u.mem_read(lo, hi - lo)) == bytes(original.mem_read(lo, hi - lo))
    archive = rom.read_file("/GRP/SLACKIMG.DK4")
    block = IlnkContainer.parse(archive).blocks[19]
    assert len(block) == 21 * 153600 and not any(v & 0x8000 for v, in struct.iter_unpack("<H", block))
    handles, events = {}, []

    def bridge(uc, address, size, data):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            path = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 96)).split(b"\0")[0].decode("ascii")
            assert path.replace("\\", "/").casefold() == "/grp/slackimg.dk4"
            assert obj not in handles
            handles[obj] = 0
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(archive)))
            events.append({"operation": "open", "path": path})
            result = 1
        elif address == SEEK:
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(archive)
            handles[obj] = offset
            events.append({"operation": "seek", "offset": offset})
            result = 1
        elif address == READ:
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            offset = handles[obj]
            assert 0 <= offset <= offset + count <= len(archive)
            if target == HEADER + 20:
                assert count == 153600
            uc.mem_write(target, archive[offset:offset + count])
            handles[obj] += count
            events.append({"operation": "read", "offset": offset, "bytes": count, "target": target})
            result = count
        else:
            handles.pop(obj)
            events.append({"operation": "close"})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    fill = struct.pack("<H", 0x89AB) * (256 * 192 * 2)
    try:
        for frame in range(21):
            pixels = block[frame * 153600:(frame + 1) * 153600]
            u.mem_write(HEADER - 16, b"\xA5" * (153620 + 32))
            header = struct.pack("<5I", 16, 320, 240, 20, 20)
            u.mem_write(HEADER, header)
            start = len(events)
            # Wrapper arguments are block,destination,offset,requested length.
            # A zero requested length means whole block, not an empty read.
            executed = call(u, 0x4704C, (19, HEADER + 20, frame * 153600, len(pixels)), instruction_limit=500000)
            assert {0x020D2018, 0x020D1EF0} <= executed and not handles
            assert bytes(u.mem_read(HEADER, len(header) + len(pixels))) == header + pixels
            io = events[start:]
            assert len([r for r in io if r["operation"] == "read" and r["bytes"] == 153600]) == 1
            views = []
            for index, (sx, sy) in enumerate(((0, 0), (64, 0), (0, 48), (64, 48))):
                screen = index % 2
                u.mem_write(FB - 16, b"\xA5" * 16 + fill + b"\xA5" * 16)
                u.mem_write(0x022E1770, bytes(4))
                u.mem_write(0x022E176C, bytes(4))
                u.mem_write(POINT, struct.pack("<2I", sx, sy))
                u.mem_write(SIZE, struct.pack("<2I", 256, 192))
                u.mem_write(DEST, bytes(8))
                u.mem_write(STACK, struct.pack("<2I", SIZE, DEST))
                executed = call(u, 0x01FF92D8 - BASE, (screen, HEADER, 0, POINT), instruction_limit=1000000)
                assert 0x020E28E0 in executed
                wanted = bytearray(fill)
                for y in range(192):
                    source = ((sy + y) * 320 + sx) * 2
                    target = screen * 0x18000 + y * 512
                    wanted[target:target + 512] = pixels[source:source + 512]
                actual = bytes(u.mem_read(FB, len(fill)))
                assert actual == bytes(wanted)
                assert bytes(u.mem_read(FB - 16, 16)) == bytes(u.mem_read(FB + len(fill), 16)) == b"\xA5" * 16
                assert bytes(u.mem_read(HEADER, 153620)) == header + pixels
                assert bytes(u.mem_read(HEADER - 16, 16)) == bytes(u.mem_read(HEADER + 153620, 16)) == b"\xA5" * 16
                views.append({"source_XYWH": [sx, sy, 256, 192], "screen": screen,
                              "full_two_screen_framebuffer_sha256": sha(actual),
                              "all_bytes_guards_source_and_call_ABI_exact": True,
                              "raw_clear_high_bits_copied_without_opacity_conversion": True})
            cases.append({"frame": frame, "full_source_bytes": 153600, "source_sha256": sha(pixels),
                          "original_partial_block_read_IO": io, "controlled_software_views": views,
                          "union_of_four_views_covers_every320x240_source_word": True})
    finally:
        u.hook_del(hook)
    result = {"candidate_sha256": sha(rom.source.read_bytes()), "archive_sha256": sha(archive),
              "block19_sha256": sha(block), "source_bound_original_code_ranges": regions,
              "original_partial_frame_reads": 21, "native_direct16_software_copy_cases": 84,
              "complete_source_words_covered": 21 * 320 * 240,
              "complete_two_screen_framebuffer_bytes_compared": 84 * len(fill), "frames": cases,
              "only_SDK_filesystem_calls_bridged": True,
              "descriptor_source_rectangles_and_research_buffer_addresses_supplied": True,
              "not_actual_GPU_or_original_comic_parent_or_source_crop_proof": True,
              "no_high_bit_or_palette_fix_authorized_by_this_test": True,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "production_ROM_and_patch_changed": False, "full_goal_complete": False}
    (ROOT / "connected_raw_read_copy_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("V587:21 original partial comic reads and84 raw16 copy cases pass;all1,612,800 source words covered;not a GPU/ordinary-consumer proof.")


if __name__ == "__main__":
    main()
