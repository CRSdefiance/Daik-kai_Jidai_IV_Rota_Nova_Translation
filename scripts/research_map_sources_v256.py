"""Restore the proven map interpretation and test native atlas loading/views.

Native map page origins, extents and palette bank IDs are supplied contracts;
this is not proof of a particular game's map-menu parent or GPU bank choice.
"""

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

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

ROOT = Path("work/analysis/common_paper_v256")
ROM = Path("out/all_routes_combined_v255_candidate.nds")
VIEW = 0x02470020


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == "9d8553cb2d1566a6754eb21269515e1af1677b51a4cce11450d4cdb92068ddc4"
    current, base = NdsImage.open(ROM), NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    legacy = IlnkContainer.parse(base.read_file("/GRP/CMMNIMG.DK4")).blocks[3]
    assert legacy == IlnkContainer.parse(current.read_file("/GRP/CMMNIMG.DK4")).blocks[3]
    prior = json.loads(Path("work/analysis/common_raw_v194.json").read_text(encoding="utf-8"))
    recovered = next(r for r in prior["blocks"] if r["block_index"] == 3)
    assert sha(legacy) == recovered["source_block_sha256"]
    assert recovered["cell_dimensions_interpretation"] == [304, 200] and recovered["cell_count_interpretation"] == 8
    indices = bytes(n for value in legacy[32:] for n in (value & 15, value >> 4))
    assert len(indices) == 304 * 200 * 8
    assert legacy[:32] + bytes(indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2)) == legacy
    cells = []
    for page in range(8):
        data = indices[page * 60800:(page + 1) * 60800]
        assert sha(data) == recovered["cells"][page]["indices_sha256"]
        cells.append({"page": page, "indices_sha256": sha(data), "all_source_pixels": 60800,
                      "separate_Japanese_caption_or_instruction_observed": False,
                      "retain_original_unlabeled_map_painting": True, "native_legacy_consumer_pending": True})
    path = "/_pxl/seamap.pxl"
    blob = current.read_file(path)
    assert blob == base.read_file(path)
    image = PxlImage.from_bytes(blob)
    assert (image.width, image.height, image.bits_per_pixel, image.pixels_offset) == (244, 1280, 4, 276)
    assert len(blob[20:276]) == 8 * 32
    arm = current.read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    for lo, hi in [(0x10E190, 0x11182C), (0xD3D30, 0xD3D80), (0xD4064, 0xD42AC), (0xD6524, 0xD6C90)]:
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    resource_call(u, 0x10E190, ())
    manager = struct.unpack_from("<I", arm, 0x5D24)[0]
    call(u, 0xD6C0C, (manager,))
    owner = struct.unpack_from("<I", arm, 0x10F328)[0]
    filename = struct.unpack_from("<I", arm, 0x10F324)[0]
    assert bytes(u.mem_read(filename, 16)) == b"_pxl/seamap.pxl\0"
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address == 0x020E5650:
            raise ValueError("Native assertion reached")
        if address not in (0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == 0x020DED50:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 128)).split(b"\0")[0].decode("ascii")
            assert "/" + name.replace("\\", "/").lstrip("/") == path and obj not in handles
            handles[obj] = 0
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(blob)))
            events.append({"operation": "open", "path": path})
            result = 1
        elif address == 0x020DEB70:
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(blob)
            handles[obj] = offset
            events.append({"operation": "seek", "offset": offset})
            result = 1
        elif address == 0x020DEBDC:
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            start = handles[obj]
            assert start + count <= len(blob)
            uc.mem_write(target, blob[start:start + count])
            handles[obj] += count
            events.append({"operation": "read", "offset": start, "bytes": count})
            result = count
        else:
            handles.pop(obj)
            events.append({"operation": "close"})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    for page in range(8):
        for bank in range(8):
            u.mem_write(VIEW - 16, b"\xA5" * 80)
            u.mem_write(STACK, struct.pack("<4I", 244, 160, bank, 0))
            resource_call(u, 0xD3D30, (VIEW, owner, 0, page * 160))
            fields = struct.unpack("<12I", u.mem_read(VIEW, 48))
            assert fields[3] == owner and fields[7:9] == (0, page * 160)
            assert fields[10:12] == (244, 160) and fields[9] & 0xFFFF == bank
            resource_call(u, 0xD4170, (VIEW,))
            loaded = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(loaded, len(blob))) == blob and not handles
            assert bytes(u.mem_read(VIEW - 16, 16)) == bytes(u.mem_read(VIEW + 48, 16)) == b"\xA5" * 16
            assert (page + 1) * 160 <= image.height
            cases.append({"page": page, "bank": bank, "native_view": fields,
                          "complete_atlas_header_all8_palettes_pixels_and_guarded_ABI_exact": True,
                          "origin_extent_and_bank_supplied_not_game_parent_inferred": True})
    legacy_palette = [bgr555(v)[:3] for v, in struct.iter_unpack("<H", legacy[:32])]
    sheet = Image.new("RGB", (4 * 312, 2 * 416), "#333333")
    draw = ImageDraw.Draw(sheet)
    native = image.render().convert("RGB")
    for page in range(8):
        x = page % 4 * 312
        y = page // 4 * 416
        draw.text((x + 4, y + 2), f"Map {page}: legacy 304x200", fill="white")
        cell = Image.new("RGB", (304, 200))
        cell.putdata([legacy_palette[n] for n in indices[page * 60800:(page + 1) * 60800]])
        sheet.paste(cell, (x + 4, y + 20))
        draw.text((x + 4, y + 224), "Native seamap 244x160; comparison only", fill="white")
        native_cell = native.crop((0, page * 160, 244, (page + 1) * 160))
        sheet.paste(native_cell, (x + 4, y + 244))
        assert sheet.crop((x + 4, y + 20, x + 308, y + 220)).tobytes() == cell.tobytes()
        assert sheet.crop((x + 4, y + 244, x + 248, y + 404)).tobytes() == native_cell.tobytes()
    sheet.save(ROOT / "legacy_and_native_maps_review.png")
    palette_sheets = []
    for bank in range(8):
        colors = [bgr555(v)[:3] for v, in struct.iter_unpack("<H", blob[20 + bank * 32:52 + bank * 32])]
        bank_sheet = Image.new("RGB", (4 * 252, 2 * 188), "#333333")
        labels = ImageDraw.Draw(bank_sheet)
        for page in range(8):
            data = image.indices[page * 39040:(page + 1) * 39040]
            cell = Image.new("RGB", (244, 160))
            cell.putdata([colors[n] for n in data])
            x, y = page % 4 * 252, page // 4 * 188
            labels.text((x + 4, y + 4), f"Bank {bank}, page {page}", fill="white")
            bank_sheet.paste(cell, (x + 4, y + 24))
            assert bank_sheet.crop((x + 4, y + 24, x + 248, y + 184)).tobytes() == cell.tobytes()
        destination = ROOT / f"native_bank{bank}_all8_source_pages.png"
        bank_sheet.save(destination)
        palette_sheets.append({"bank": bank, "path": str(destination), "sha256": sha(destination.read_bytes()),
                               "all_source_pixels_visible_at_original_scale": True,
                               "GPU_alpha_and_actual_bank_selection_not_claimed": True})
    proof = {"format": "dk4-map-source-native-v256", "candidate": str(ROM), "candidate_sha256": sha(ROM.read_bytes()),
             "legacy_path": "/GRP/CMMNIMG.DK4", "legacy_block": 3, "legacy_sha256": sha(legacy),
             "whole_243232_source_bytes_accounted_and_roundtrip_exact": True,
             "all8_V194_source_map_pixel_hashes_reconfirmed_in_V255": True, "source_map_cells": cells,
             "V250_wrong_width_source_clearance_regression_superseded": True,
             "native_path": path, "native_sha256": sha(blob), "actual_registration_owner": owner,
             "native_source_header_dimensions": [244, 1280], "native_palette_banks_preserved": 8,
             "native_cache_view_cases": cases, "SDK_filesystem_bridge_events": events,
             "all64_native_cases_pass": True, "legacy_native_copy_equivalence_not_claimed": True,
             "complete_native_palette_source_review_sheets": palette_sheets,
             "native_parent_bank_choice_UV_GPU_and_legacy_usage_pending": True,
             "unresolved_native_storage_block_count_remains11": True,
             "all18_plaque_entries_remain_incomplete": True, "ROM_modified": False, "full_goal_complete": False}
    review_path = ROOT / "native_source_visual_review.json"
    if review_path.exists():
        review = json.loads(review_path.read_text(encoding="utf-8"))
        assert review["legacy_source_sha256"] == sha(legacy) and review["native_source_sha256"] == sha(blob)
        assert review["source_charts"] == [{k: s[k] for k in ("bank", "path", "sha256")} for s in palette_sheets]
        proof["visual_review_evidence"] = str(review_path)
        proof["visual_review_evidence_sha256"] = sha(review_path.read_bytes())
        proof["completed_source_visual_review_preserved_with_exact_source_and_chart_hashes"] = True
    (ROOT / "proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("Eight exact legacy source maps restored;64 native cache/view/bank cases pass; no ROM changed.")


if __name__ == "__main__":
    main()
