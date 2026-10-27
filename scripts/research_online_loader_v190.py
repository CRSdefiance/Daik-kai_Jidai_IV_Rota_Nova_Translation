"""Execute native resource loading with an explicit ROM-backed SDK I/O bridge.

The bridge supplies filesystem open/read/close. Registration, cache allocation,
eviction, image construction and resolution execute the game's actual ARM code.
This is a scoped native integration probe, not a hardware filesystem/GPU test.
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
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.online_headers_v189 import CANDIDATE, PROOF, save
from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP, call, machine

PAGE_PROOF = Path("work/analysis/online_resource_pages_v189.json")
OUT = Path("work/analysis/online_loader_v190_research.json")
VIEW = 0x02480000


def resource_call(uc, offset, args):
    """Allow native pool compaction copies to finish with strict caller ABI checks."""
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
        uc.reg_write(reg, value)
    saved = {reg: 0xA5A51000 + index for index, reg in enumerate(SAVED)}
    for reg, value in saved.items():
        uc.reg_write(reg, value)
    executed = set()
    handle = uc.hook_add(UC_HOOK_CODE, lambda u, a, s, d: executed.add(a))
    try:
        uc.emu_start(BASE + offset, STOP, count=4_000_000)
    finally:
        uc.hook_del(handle)
    if (
        uc.reg_read(UC_ARM_REG_PC) != STOP
        or uc.reg_read(UC_ARM_REG_SP) != STACK
        or any(uc.reg_read(reg) != value for reg, value in saved.items())
    ):
        raise ValueError("Complete native resource routine or saved-register ABI failed")
    return executed


def main():
    saved = json.loads(PROOF.read_text(encoding="utf-8"))
    pages = json.loads(PAGE_PROOF.read_text(encoding="utf-8"))
    if (
        saved["candidate_sha256"] != sha(CANDIDATE.read_bytes())
        or pages["candidate_sha256"] != saved["candidate_sha256"]
    ):
        raise ValueError("Exact V189 and actual-page proof required")
    rom = NdsImage.open(CANDIDATE)
    arm9 = rom.read_file("/__arm9__.bin")
    source = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    ranges = (
        (0x10E190, 0x11182C),
        (0x111A90, 0x1123D0),
        (0xD6524, 0xD6C90),
        (0xD3D30, 0xD3D7C),
        (0xD4064, 0xD42AC),
        (0xDF0A0, 0xDF0C8),
        (0xD7650, 0xD7670),
    )
    for lo, hi in ranges:
        if arm9[lo:hi] != source[lo:hi]:
            raise ValueError("Relevant native registration/cache/image code changed")
    uc = machine(arm9)
    init_trace = call(uc, 0x10E190, ())
    online_trace = call(uc, 0x111A90, ())
    cache_manager = struct.unpack_from("<I", arm9, 0x5D24)[0]
    if cache_manager != 0x0231272C:
        raise ValueError("Actual startup pool manager differs")
    pool_trace = call(uc, 0xD6C0C, (cache_manager,))
    pool_start, pool_end = struct.unpack("<2I", uc.mem_read(cache_manager, 8))
    if (pool_start, pool_end) != (0x02313FF0, 0x02373FF0):
        raise ValueError("Actual native resource pool differs")
    handles, io = {}, []
    current_trace = set()

    def read_name(pointer):
        return bytes(uc.mem_read(pointer, 96)).split(b"\0", 1)[0].decode("ascii")

    def bridge(u, address, size, _data):
        current_trace.add(address)
        obj = u.reg_read(UC_ARM_REG_R0)
        if address == 0x020DED50:
            path = "/" + read_name(u.reg_read(UC_ARM_REG_R1))
            raw = rom.read_file(path)
            handles[obj] = path
            # SDK FSFile.start/end; caller computes the exact file byte length.
            u.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            io.append(
                {
                    "operation": "open",
                    "path": path,
                    "bytes": len(raw),
                    "ROM_file_id": rom.path_map()[path],
                    "sha256": sha(raw),
                }
            )
            result = 1
        elif address == 0x020DEBDC:
            path = handles[obj]
            raw = rom.read_file(path)
            destination, count = u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)
            if (
                count != len(raw)
                or not pool_start + 16 <= destination < destination + count <= pool_end
            ):
                raise ValueError("Native allocation/read length escaped actual cache pool")
            u.mem_write(destination, raw)
            io.append(
                {"operation": "read", "path": path, "bytes": count, "destination": destination}
            )
            result = count
        elif address == 0x020DED08:
            io.append({"operation": "close", "path": handles.pop(obj)})
            result = 1
        elif address == 0x020E5650:
            raise ValueError("Native resource loader reached its fatal assertion")
        else:
            return
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = uc.hook_add(UC_HOOK_CODE, bridge)
    owners = {
        image["path"]: image["owner_address"] for p in pages["pages"] for image in p["screenshots"]
    }
    if len(owners) != pages["screenshot_selection_count"]:
        raise ValueError("Expected unique actual screenshot registrations")
    rows = []
    try:
        # Selected screenshots are resolved twice while hot, then all screenshots
        # exceed the real pool and exercise the native cache's eviction path.
        sequence = list(pages["remaining_screenshot_actual_selections"]) + list(owners)
        for path in sequence:
            owner = owners[path]
            raw = rom.read_file(path)
            current_trace.clear()
            before_io = len(io)
            uc.mem_write(VIEW - 16, b"\xa5" * 80)
            uc.mem_write(VIEW, bytes(48))
            uc.mem_write(STACK, struct.pack("<4I", 256, 192, 0, 0))
            call(uc, 0xD3D30, (VIEW, owner, 0, 0))
            try:
                first = resource_call(uc, 0xD4170, (VIEW,))
            except ValueError:
                print(
                    "Resolver stopped:",
                    path,
                    hex(uc.reg_read(UC_ARM_REG_PC)),
                    "I/O",
                    io[before_io:],
                )
                print(
                    "Executed key loader entries:",
                    [hex(x) for x in sorted(current_trace) if 0x020D6524 <= x < 0x020D6C90][:20],
                )
                raise
            pointer = uc.reg_read(UC_ARM_REG_R0)
            loaded = bytes(uc.mem_read(pointer, len(raw)))
            if loaded != raw:
                raise ValueError(
                    "Complete native-resolved image differs from actual candidate file"
                )
            if (
                struct.unpack("<I", uc.mem_read(VIEW + 12, 4))[0] != owner
                or struct.unpack("<2I", uc.mem_read(VIEW + 40, 8)) != (256, 192)
                or bytes(uc.mem_read(VIEW - 16, 16)) != b"\xa5" * 16
                or bytes(uc.mem_read(VIEW + 48, 16)) != b"\xa5" * 16
            ):
                raise ValueError("Actual native image view, extent or canaries differ")
            native_id = struct.unpack("<I", uc.mem_read(owner + 16, 4))[0]
            if native_id == 0xFFFFFFFF or not {0x020D4170, 0x020D6558, 0x020D68F0} <= first:
                raise ValueError("Native resource did not resolve through its actual owner/cache")
            hot_start = len(io)
            second = resource_call(uc, 0xD4170, (VIEW,))
            if (
                len(io) != hot_start
                or uc.reg_read(UC_ARM_REG_R0) != pointer
                or bytes(uc.mem_read(pointer, len(raw))) != raw
            ):
                raise ValueError("Hot native cache lookup repeated I/O or changed the image")
            resident_checks = []
            # Compaction moves other live images. Validate all registered owners
            # still resident, without changing their LRU order or supplying pointers.
            for resident_path, resident_owner in owners.items():
                resident_id = struct.unpack("<I", uc.mem_read(resident_owner + 16, 4))[0]
                if resident_id == 0xFFFFFFFF:
                    continue
                resource_call(uc, 0xD68F0, (cache_manager, resident_id))
                resident_pointer = uc.reg_read(UC_ARM_REG_R0)
                resident_raw = rom.read_file(resident_path)
                if (
                    not resident_pointer
                    or bytes(uc.mem_read(resident_pointer, len(resident_raw))) != resident_raw
                ):
                    raise ValueError("Compaction corrupted another resident screenshot")
                resident_checks.append(
                    {
                        "path": resident_path,
                        "cache_id": resident_id,
                        "complete_image_sha256": sha(resident_raw),
                    }
                )
            rows.append(
                {
                    "path": path,
                    "owner": owner,
                    "cache_id": native_id,
                    "resolved_pointer": pointer,
                    "complete_image_sha256": sha(loaded),
                    "bytes": len(raw),
                    "cold_operations": io[before_io:hot_start],
                    "hot_IO_operations": 0,
                    "complete_view_canaries": True,
                    "executed_cache_eviction": 0x020D6524 in first,
                    "native_first_lookup_instruction_count": len(first),
                    "native_hot_lookup_instruction_count": len(second),
                    "other_resident_image_checks": resident_checks,
                }
            )
    finally:
        uc.hook_del(hook)
    if handles:
        raise ValueError("SDK bridge handle leaked")
    if not any(row["executed_cache_eviction"] for row in rows):
        raise ValueError("Actual native pool was not exercised through eviction")
    save(
        OUT,
        {
            "status": "pass-scoped-native-loader-cache-with-explicit-ROM-SDK-bridge",
            "candidate": str(CANDIDATE),
            "candidate_sha256": saved["candidate_sha256"],
            "source_ARM9_sha256": sha(source),
            "candidate_ARM9_sha256": sha(arm9),
            "code_ranges": [
                {"start": lo, "end_exclusive": hi, "sha256": sha(arm9[lo:hi])} for lo, hi in ranges
            ],
            "native_initializers_executed": {
                "all_resource_registry_instructions": len(init_trace),
                "Online_registry_instructions": len(online_trace),
                "pool_initialization_instructions": len(pool_trace),
            },
            "actual_cache_pool": [pool_start, pool_end],
            "actual_page_screenshot_count": len(owners),
            "resident_image_checks": sum(len(r["other_resident_image_checks"]) for r in rows),
            "lookups": rows,
            "SDK_bridge_events": io,
            "SDK_bridge_addresses": [0x020DED50, 0x020DEBDC, 0x020DED08],
            "native_filesystem_hardware_verified": False,
            "native_GPU_display_verified": False,
            "limits": [
                "Only SDK open/read/close are bridged to exact actual candidate ROM filesystem resources.",
                "Resource registration, actual filenames/owners, native pool allocation/cache IDs/eviction and image-view resolution execute native ARM code.",
                "NitroFS hardware, OS scheduling, graphics rendering/layers/palette/alpha, physical input and live readability remain unverified.",
            ],
        },
    )
    print(
        f"Pass: {len(rows)} actual-owner image resolutions, {len(owners)} screenshots, hot cache and native eviction; SDK I/O bridged."
    )


if __name__ == "__main__":
    main()
