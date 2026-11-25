"""Prove the native .000 portrait atlas through its reader and real framebuffer."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import bgr555
from dk4tool.rom.nds import NdsImage

CANDIDATE = Path("out/all_routes_combined_v190_candidate.nds")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")
ROOT = Path("work/qa/native_portrait_atlas_v195")
REPORT = Path("work/analysis/native_portrait_atlas_v195.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def native5(image):
    return bytes((value * 31 + 127) // 255 for value in image.convert("RGB").tobytes())


def main():
    assert sha(CANDIDATE.read_bytes()) == "9ccff57aec0326722b89b85877fb5be23e63dc466022b1f7c2e0a984ccdd9424"
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    rom, base = NdsImage.open(CANDIDATE), NdsImage.open(BASE)
    raw = rom.read_file("/GRP/CMMNIMG.000")
    assert raw == base.read_file("/GRP/CMMNIMG.000")
    assert len(raw) == 512 + 178 * 56 * 64
    palette = raw[:512]
    colors = [bgr555(value) for value, in struct.iter_unpack("<H", palette)]
    image = Image.new("RGBA", (56, 178 * 64))
    image.putdata([colors[value] for value in raw[512:]])
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROOT / "full_atlas.png")
    rows = []
    for begin in range(0, 178, 40):
        count = min(40, 178 - begin)
        sheet = Image.new("RGB", (1200, ((count + 9) // 10) * 156), "#333333")
        draw = ImageDraw.Draw(sheet)
        for slot in range(count):
            index = begin + slot
            cell = image.crop((0, index * 64, 56, (index + 1) * 64))
            x, y = slot % 10 * 120, slot // 10 * 156
            draw.text((x + 4, y + 3), str(index), fill="white")
            sheet.paste(cell.resize((112, 128), Image.Resampling.NEAREST).convert("RGB"), (x + 4, y + 24))
        path = ROOT / f"review_{begin // 40}.png"
        sheet.save(path)
        rows.append({"path": str(path), "sha256": sha(path.read_bytes()), "first": begin, "last": begin + count - 1, "visual_review": "pending"})
    capture_report = json.loads(Path("work/emulation_v193/v190_lil_scene/capture_report.json").read_text())
    assert capture_report["ROM_sha256"] == sha(CANDIDATE.read_bytes())
    capture = next(row for row in capture_report["frames_captured"] if row["frame"] == 6300)
    assert sha(Path(capture["path"]).read_bytes()) == capture["PNG_sha256"]
    frame = Image.open(capture["path"]).convert("RGB")
    lil = image.crop((0, 2 * 64, 56, 3 * 64))
    assert native5(lil) == native5(frame.crop((8, 200, 64, 264)))
    arm, original = rom.read_file("/__arm9__.bin"), base.read_file("/__arm9__.bin")
    assert arm[0x47A28:0x47AC4] == original[0x47A28:0x47AC4]
    assert struct.unpack_from("<I", arm, 0x47AD4)[0] == 0x02115E50
    assert arm[0x115E50:0x115E60].split(b"\0", 1)[0] == b"/GRP/CMMNIMG.000"
    for offset, expected in ((0x47A40, 0xE3A03C0E), (0x47A50, 0xE2811C02), (0x47A94, 0xE3A00038), (0x47A9C, 0xE3A00040)):
        assert struct.unpack_from("<I", arm, offset)[0] == expected
    result = {
        "status": "pass-native-portrait-atlas-reader-geometry-and-live-pixels",
        "candidate_sha256": sha(CANDIDATE.read_bytes()),
        "path": "/GRP/CMMNIMG.000", "source_file_sha256": sha(raw),
        "palette_bytes": 512, "palette_sha256": sha(palette),
        "indices_sha256": sha(raw[512:]), "portrait_dimensions": [56, 64], "portrait_count": 178,
        "candidate_file_unchanged_from_canonical": True,
        "native_reader_range": [0x02047A28, 0x02047AC4],
        "native_reader_code_sha256": sha(arm[0x47A28:0x47AC4]),
        "native_reader_offset_formula": "512 + portrait_id * 3584", "native_read_bytes_per_portrait": 3584,
        "live_complete_portrait_match": {"atlas_index": 2, "capture": capture["path"], "frame": 6300, "destination_box": [8, 200, 64, 264], "matching_method": "complete native five-bit RGB equality; no exclusions or tolerance"},
        "review_sheets": rows,
        "legacy_CMMNIMG_block0_equivalence_claimed": False,
        "physical_hardware_or_all_portrait_usage_verified": False,
        "limits": ["Native reader constants and one complete emulator-rendered portrait establish this .000 atlas's geometry and palette interpretation.", "All other portrait consumers, alpha/crops and broader gameplay are not cleared by one sample.", "The similarly shaped legacy ILNK block uses different palette/pixels; its direct native use remains unproved."],
        "rom_changed": False,
    }
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Proved native .000 atlas: 178 portraits, 56x64 reader geometry and complete Lil framebuffer equality.")


if __name__ == "__main__":
    main()
