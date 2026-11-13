"""Execute whole raw-art record reads/uploads and prepare palette-complete views."""

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
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROOT = Path("work/analysis/raw_resource_v219")
ROM = Path("out/all_routes_combined_v218_candidate.nds")
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08
PIXELS, PALETTE = 0x020E21B8, 0x020E208C


def views(row, data):
    pixels, palette = data[:-512], data[-512:]
    indices = bytes(v for byte in pixels for v in (byte & 15, byte >> 4))
    words = struct.unpack("<256H", palette)
    results = []
    # The observed 2F000 texture presentations include a fixed 256-pixel width
    # and a dynamic width with 256 rows. Review both complete source arrangements;
    # record-to-parent selection remains a separate native contract.
    widths = [256]
    dynamic_width = len(indices) // 256
    if dynamic_width != 256:
        widths.append(dynamic_width)
    for width in widths:
        assert len(indices) % width == 0
        height = len(indices) // width
        scale = 2 if width < 64 else 1
        cell_width, cell_height = max(width * scale, 128), height * scale + 20
        sheet = Image.new("RGB", (cell_width * 4, cell_height * 4), (230, 230, 230))
        draw = ImageDraw.Draw(sheet)
        files = []
        for bank in range(16):
            colors = [tuple((c << 3) | (c >> 2) for c in (v & 31, v >> 5 & 31, v >> 10 & 31))
                      for v in words[bank * 16:(bank + 1) * 16]]
            im = Image.new("P", (width, height))
            im.putpalette([c for color in colors for c in color] + [0] * (768 - 48))
            im.putdata(indices)
            assert im.tobytes() == indices
            filename = ROOT / f"{row['family']}_{row['index']:02d}_{width}wide_palette{bank:02d}.png"
            im.save(filename)
            x, y = bank % 4 * cell_width, bank // 4 * cell_height
            draw.text((x, y), f"{row['family']} {row['index']} pal {bank}", fill="black")
            sheet.paste(im.convert("RGB").resize((width * scale, height * scale), Image.Resampling.NEAREST), (x, y + 20))
            files.append({"bank": bank, "path": filename.as_posix(), "sha256": sha(filename.read_bytes())})
        path = ROOT / f"{row['family']}_{row['index']:02d}_{width}wide_all16palettes.png"
        sheet.save(path)
        results.append({"source_arrangement": [width, height], "indices": len(indices),
                        "indices_sha256": sha(indices), "full_original_palette_sha256": sha(palette),
                        "sheet": path.as_posix(), "sheet_sha256": sha(path.read_bytes()), "palette_views": files,
                        "RGB_view_does_not_claim_native_alpha_or_parent_selection": True})
    return results


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    assert sha(ROM.read_bytes()) == "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"
    arm = rom.read_file("/__arm9__.bin")
    assert arm[0xCDE20:0xCE4D0] == clean.read_file("/__arm9__.bin")[0xCDE20:0xCE4D0]
    records = []
    for family, kind, table, count in (("GMONS", 1, 0x125908, 6), ("OCETC", 2, 0x125938, 8)):
        raw = rom.read_file(f"/GRP/{family}.DK4")
        assert raw == clean.read_file(f"/GRP/{family}.DK4")
        ranges = []
        for index in range(count):
            size, offset = struct.unpack_from("<2I", arm, table + index * 8)
            if kind == 1:
                size += 512
            offset += index * 512
            assert offset + size <= len(raw)
            expected = raw[offset:offset + size]
            ranges.append((offset, offset + size))
            u = machine(arm)
            handles, events, transfers = {}, [], []
            scratch = 0x022E1794
            u.mem_write(0x021703F8, struct.pack("<3I", kind, index, 0))
            u.mem_write(scratch - 16, b"\xa5" * (size + 32))

            def bridge(uc, address, width, _, *, family=family, kind=kind, handles=handles,
                       events=events, offset=offset, size=size, scratch=scratch,
                       expected=expected, transfers=transfers):
                if address in (OPEN, READ, SEEK, CLOSE):
                    obj = uc.reg_read(UC_ARM_REG_R0)
                    if address == OPEN:
                        name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 64)).split(b"\0")[0].decode("ascii").replace("\\", "/")
                        assert name == f"/GRP/{family}.DK4" and not handles
                        handles[obj] = 0
                        value = 1
                        events.append({"operation": "open", "file": name})
                    elif address == SEEK:
                        position = uc.reg_read(UC_ARM_REG_R1)
                        assert uc.reg_read(UC_ARM_REG_R2) == 0 and position == offset
                        handles[obj] = position
                        value = 1
                        events.append({"operation": "seek", "offset": position})
                    elif address == READ:
                        target, length = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
                        assert target == scratch and length == size and handles[obj] == offset
                        uc.mem_write(target, expected)
                        handles[obj] += length
                        value = length
                        events.append({"operation": "read", "bytes": length})
                    else:
                        handles.pop(obj)
                        value = 1
                        events.append({"operation": "close"})
                    uc.reg_write(UC_ARM_REG_R0, value)
                    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
                elif address in (0x020E231C, 0x020E2148, 0x020E2100, 0x020E2034, PIXELS, PALETTE):
                    if address in (PIXELS, PALETTE):
                        pointer, destination, length = [uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
                        at = 0 if address == PIXELS else size - 512
                        assert pointer == scratch + at
                        assert destination == (0x2F000 if address == PIXELS else 0x1000)
                        assert length == (size - 512 if address == PIXELS else 512 if kind == 1 else 384)
                        assert bytes(uc.mem_read(pointer, length)) == expected[at:at + length]
                        transfers.append({"kind": "pixels" if address == PIXELS else "palette", "destination": destination,
                                          "bytes": length, "complete_source_sha256": sha(expected[at:at + length])})
                    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

            h = u.hook_add(UC_HOOK_CODE, bridge)
            call(u, 0xCDE20, (0,))
            assert bytes(u.mem_read(scratch, size)) == expected and not handles
            assert bytes(u.mem_read(scratch - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(scratch + size, 16)) == b"\xa5" * 16
            call(u, 0xCE238, (0,))
            u.hook_del(h)
            assert len(transfers) == 2
            row = {"family": family, "kind": kind, "index": index, "offset": offset, "bytes": size,
                   "full_record_sha256": sha(expected), "events": events, "native_transfers": transfers,
                   "complete_native_read_upload_arguments_ABI_and_guards_exact": True,
                   "OCETC_final_128_palette_bytes_retained_but_not_uploaded_here": kind == 2}
            row["source_views"] = views(row, expected)
            records.append(row)
        cursor = 0
        for start, end in sorted(ranges):
            assert start == cursor
            cursor = end
        assert cursor == len(raw)
    result = {"format": "dk4-raw-art-native-record-research-v1", "ROM_sha256": sha(ROM.read_bytes()),
              "records": records, "complete_file_partitions": ["OCETC", "GMONS"],
              "source_bytes_covered": sum(row["bytes"] for row in records),
              "observed_texture_bank_byte_offset": 0x2F000, "observed_palette_bank_byte_offset": 0x1000,
              "source_arrangements_are_candidate_parent_geometries_not_final_crop_proof": True,
              "actual_GPU_parent_palette_bank_selection_and_alpha_pending": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_record_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_records": len(records), "complete_files": 2, "source_bytes_covered": result["source_bytes_covered"],
                      "complete_palette_variant_views": sum(len(row["source_views"]) * 16 for row in records)}))


if __name__ == "__main__":
    main()
