"""Map actual Online page resources through the unchanged native initializer.

This executes resource registration and reads the game's real page tables. It
does not replace registration with supplied owners, or claim filesystem/GPU proof.
"""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.online_headers_v189 import CANDIDATE, PROOF, save
from scripts.probe_button_prompt_native import call, machine

RAM_BASE = 0x02000000
DESCRIPTORS = (0x12F88C, 0x12F898, 0x12F8A4, 0x12F8B0)
COUNTS = (4, 4, 2, 3)
CODE_RANGES = ((0x111A90, 0x1123D0), (0x1045B4, 0x1048C8), (0xD3D30, 0xD3D7C), (0xD4064, 0xD40AC))
OUTPUT = Path("work/analysis/online_resource_pages_v189.json")


def main():
    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    if sha(CANDIDATE.read_bytes()) != proof["candidate_sha256"]:
        raise ValueError("Exact saved candidate required")
    source, candidate = NdsImage.open("work/clean.nds"), NdsImage.open(CANDIDATE)
    clean = source.read_file("/__arm9__.bin")
    arm9 = candidate.read_file("/__arm9__.bin")
    code = []
    for lo, hi in CODE_RANGES:
        if arm9[lo:hi] != clean[lo:hi]:
            raise ValueError("Mapped registration/parent/constructor code changed")
        code.append({"start_offset": lo, "end_exclusive": hi, "sha256": sha(arm9[lo:hi])})
    uc = machine(arm9)
    executed = call(uc, 0x111A90, ())
    if len(executed) != 449 or min(executed) != 0x02111A90 or max(executed) != 0x02112190:
        raise ValueError("Complete native resource initializer trace differs")

    def owner_name(owner):
        # Native initializer creates 20-byte resource owners: vtable, two
        # initially self-referential list pointers, filename pointer, -1 ID.
        fields = struct.unpack("<5I", uc.mem_read(owner, 20))
        if fields[:3] != (0x02160538, owner + 4, owner + 4) or fields[4] != 0xFFFFFFFF:
            raise ValueError("Actual registered resource layout differs")
        name = bytes(uc.mem_read(fields[3], 96)).split(b"\0", 1)[0]
        if name != clean[fields[3] - RAM_BASE :].split(b"\0", 1)[0]:
            raise ValueError("Original filename changed")
        path = "/" + name.decode("ascii")
        if not path.startswith("/_pxl/online/Online") or path not in candidate.path_map():
            raise ValueError("Owner does not identify an actual Online ROM resource")
        p = PxlImage.from_bytes(candidate.read_file(path))
        return {
            "owner_address": owner,
            "filename_pointer": fields[3],
            "path": path,
            "file_id": candidate.path_map()[path],
            "dimensions": [p.width, p.height],
            "candidate_resource_sha256": sha(candidate.read_file(path)),
        }

    pages = []
    for category, (offset, count) in enumerate(zip(DESCRIPTORS, COUNTS, strict=True)):
        data, captions, actual_count = struct.unpack_from("<3I", arm9, offset)
        if actual_count != count or arm9[offset : offset + 12] != clean[offset : offset + 12]:
            raise ValueError("Native category descriptor changed")
        for index in range(count):
            start = data - RAM_BASE + index * 16
            background, image_table, caption_art, image_count = struct.unpack_from(
                "<4I", arm9, start
            )
            if (
                image_count not in (1, 2, 3)
                or arm9[start : start + 16] != clean[start : start + 16]
            ):
                raise ValueError("Native page descriptor changed")
            owners = struct.unpack_from(f"<{image_count}I", arm9, image_table - RAM_BASE)
            if (
                arm9[image_table - RAM_BASE : image_table - RAM_BASE + 4 * image_count]
                != clean[image_table - RAM_BASE : image_table - RAM_BASE + 4 * image_count]
            ):
                raise ValueError("Actual page screenshot-selection table changed")
            images = [owner_name(o) for o in owners]
            for image in images:
                if image["dimensions"] != [256, 192]:
                    raise ValueError("Screenshot exceeds actual full-page selection extent")
            pages.append(
                {
                    "category_index": category,
                    "page_index": index,
                    "descriptor_offset": offset,
                    "page_data_offset": start,
                    "screenshots": images,
                    "background": owner_name(background),
                    "caption_art": owner_name(caption_art),
                    "image_count": image_count,
                    "caption_table_pointer": captions,
                }
            )

    wanted = {
        "/_pxl/online/Online24.pxl": (0, 2, 1),
        "/_pxl/online/Online27.pxl": (1, 2, 0),
        "/_pxl/online/Online31.pxl": (2, 0, 1),
        "/_pxl/online/Online33.pxl": (2, 1, 0),
    }
    selected = {}
    for p in pages:
        for i, image in enumerate(p["screenshots"]):
            if image["path"] in wanted:
                actual = (p["category_index"], p["page_index"], i)
                if actual != wanted[image["path"]]:
                    raise ValueError(
                        "Remaining screenshot appears at an unexpected actual selection"
                    )
                selected[image["path"]] = dict(
                    category_index=actual[0],
                    page_index=actual[1],
                    screenshot_index=actual[2],
                    **image,
                )
    if set(selected) != set(wanted):
        raise ValueError("A remaining screenshot is absent from actual page data")
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    parent = [
        (i.address, i.mnemonic, i.op_str) for i in cs.disasm(arm9[0x104744:0x104780], 0x02104744)
    ]
    if parent != [
        (0x02104744, "mov", "r0, #0x100"),
        (0x02104748, "str", "r0, [sp]"),
        (0x0210474C, "mov", "r0, #0xc0"),
        (0x02104750, "str", "r0, [sp, #4]"),
        (0x02104754, "mov", "r2, #0"),
        (0x02104758, "str", "r2, [sp, #8]"),
        (0x0210475C, "str", "r2, [sp, #0xc]"),
        (0x02104760, "ldr", "r3, [sp, #0x2c]"),
        (0x02104764, "ldr", "r1, [sp, #0x30]"),
        (0x02104768, "add", "r3, sb, r3, lsl #4"),
        (0x0210476C, "ldr", "r4, [r3, #4]"),
        (0x02104770, "add", "r0, sp, #0x84"),
        (0x02104774, "ldr", "r1, [r4, r1, lsl #2]"),
        (0x02104778, "mov", "r3, r2"),
        (0x0210477C, "bl", "#0x20d3d30"),
    ]:
        raise ValueError("Actual screenshot origin/extent/table constructor sequence differs")
    save(
        OUTPUT,
        {
            "status": "pass-actual-static-registration-and-page-selection-map",
            "candidate": str(CANDIDATE),
            "candidate_sha256": proof["candidate_sha256"],
            "ARM9_sha256": sha(arm9),
            "clean_ARM9_sha256": sha(clean),
            "code_ranges": code,
            "native_initializer": {
                "entry_address": 0x02111A90,
                "distinct_instructions_executed": 449,
                "complete_return_and_saved_register_ABI": True,
            },
            "category_count": 4,
            "page_count": len(pages),
            "screenshot_selection_count": sum(p["image_count"] for p in pages),
            "pages": pages,
            "remaining_screenshot_actual_selections": selected,
            "actual_parent_constructor": {
                "call_address": 0x0210477C,
                "constructor": 0x020D3D30,
                "origin": [0, 0],
                "extent": [256, 192],
                "instructions": parent,
            },
            "native_filesystem_loading_verified": False,
            "native_GPU_display_verified": False,
            "limits": [
                "Native static initializer is executed; no placeholder resource-owner table is supplied.",
                "Real page tables select these ROM resources and pass full 256x192 bounds at origin zero.",
                "Filesystem loading, navigation/input, layer transforms, palette/GPU composition and live readability remain unverified.",
            ],
        },
    )
    print(
        "Mapped 13 actual pages and four remaining screenshot selections; live loading/display pending."
    )


if __name__ == "__main__":
    main()
