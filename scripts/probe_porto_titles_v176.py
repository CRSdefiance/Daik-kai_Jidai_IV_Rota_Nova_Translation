"""Controlled PXL headers and supplied crop descriptors; no live-loader claim."""

import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.fleet_row_graphics_v162 import save
from scripts.porto_title_copies_v176 import CANDIDATE, OUT, SPECS, asset
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_name_treasure_graphics_v161 import sizing


def main():
    rom = NdsImage.open(CANDIDATE)
    arm9 = rom.read_file("/__arm9__.bin")
    rows = []
    for spec in SPECS:
        raw = rom.read_file(spec["path"])
        width, height, _, _ = asset(spec, raw)
        row = {"path": spec["path"], "original_storage_dimensions": [width, height]}
        if "block" not in spec:
            row["controlled_PXL_header"] = sizing(arm9, raw, 20, 0x024A0000, supplied_table=True)
        else:
            row["embedded_loader_verified"] = False
        crops = []
        for kind in ("main", "caption"):
            x0, y0, x1, y1 = spec[kind]
            if not 0 <= x0 < x1 <= width or not 0 <= y0 < y1 <= height:
                raise ValueError("Supplied cell exceeds original storage image")
            uc = machine(arm9)
            view, owner = 0x02480000, 0x02490000
            uc.mem_write(view - 16, b"\xa5" * 80)
            uc.mem_write(view, bytes(48))
            uc.mem_write(STACK, struct.pack("<4I", x1 - x0, y1 - y0, 0, 0))
            executed = call(uc, 0xD3B34, (view, owner, x0, y0))
            if (
                struct.unpack("<I", uc.mem_read(view + 12, 4))[0] != owner
                or struct.unpack("<2I", uc.mem_read(view + 28, 8)) != (x0, y0)
                or struct.unpack("<2I", uc.mem_read(view + 40, 8)) != (x1 - x0, y1 - y0)
                or not {0x020D3B34, 0x020D3ED0, 0x020D41A4} <= executed
                or bytes(uc.mem_read(view - 16, 16)) != b"\xa5" * 16
                or bytes(uc.mem_read(view + 48, 16)) != b"\xa5" * 16
            ):
                raise ValueError("Supplied native crop origin/extent/owner/ABI/canary differs")
            crops.append({"kind": kind, "supplied_original_cell": spec[kind], "ABI_canaries": True})
        row["supplied_crop_constructors"] = crops
        rows.append(row)
    save(
        OUT / "native.json",
        {
            "status": "pass-two-controlled-PXL-headers-and-six-supplied-crop-contracts",
            "candidate_sha256": sha(CANDIDATE.read_bytes()),
            "arm9_sha256": sha(arm9),
            "cases": rows,
            "limits": [
                "Source owner/table/crop inputs are supplied; actual PC title/embedded loader and parent usage are unknown.",
                "Embedded ILNK bytes are never treated as a loose PXL header. Its 320x240 storage dimensions are independently preserved.",
                "Actual live crops, palette/alpha, GPU composition and physical input/gameplay remain pending.",
            ],
        },
    )
    print(
        "Pass: two controlled PXL headers and six supplied crop descriptors; actual native display pending."
    )


if __name__ == "__main__":
    main()
