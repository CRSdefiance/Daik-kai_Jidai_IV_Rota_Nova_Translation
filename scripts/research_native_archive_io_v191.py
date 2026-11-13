"""Execute the game's ILNK reader, bridging only SDK file I/O to the saved ROM."""

import hashlib
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
    UC_ARM_REG_R4,
    UC_ARM_REG_R6,
    UC_ARM_REG_R9,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")
OUT = Path("work/analysis/native_archive_io_v191.json")
OBJECT, NAME, BUFFER = 0x02460000, 0x02461000, 0x02480000
CHUNK = 65536
SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sha(CANDIDATE.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    rom, original = NdsImage.open(CANDIDATE), NdsImage.open(BASE)
    arm, source = rom.read_file("/__arm9__.bin"), original.read_file("/__arm9__.bin")
    ranges = [(0x4704C, 0x470B4), (0x9EDD8, 0x9EE18), (0xD0170, 0xD051C), (0xD0590, 0xD060C), (0xD1EE0, 0xD2128), (0x10E190, 0x11155C)]
    assert all(arm[lo:hi] == source[lo:hi] for lo, hi in ranges)
    uc = machine(arm)
    handles, events, executed = {}, [], set()

    def bridge(u, address, size, user):
        executed.add(address)
        if address not in (SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE):
            return
        obj = u.reg_read(UC_ARM_REG_R0)
        if address == SDK_OPEN:
            pointer = u.reg_read(UC_ARM_REG_R1)
            name = bytearray()
            for index in range(1024):
                value = u.mem_read(pointer + index, 1)[0]
                if not value:
                    break
                name.append(value)
            else:
                raise ValueError("Unterminated native filename")
            path = name.decode("ascii").replace("\\", "/")
            assert path in rom.path_map() and obj not in handles
            raw = rom.read_file(path)
            handles[obj] = {"path": path, "raw": raw, "position": 0}
            u.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            events.append({"operation": "open", "path": path, "file_id": rom.path_map()[path], "bytes": len(raw), "sha256": sha(raw)})
            result = 1
        elif address == SDK_SEEK:
            state = handles[obj]
            offset, origin = u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)
            assert origin == 0 and 0 <= offset <= len(state["raw"])
            state["position"] = offset
            events.append({"operation": "seek", "path": state["path"], "offset": offset})
            result = 1
        elif address == SDK_READ:
            state = handles[obj]
            destination, count = u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)
            start, end = state["position"], state["position"] + count
            assert 0 <= start <= end <= len(state["raw"])
            if count:
                u.mem_write(destination, state["raw"][start:end])
            state["position"] = end
            events.append({"operation": "read", "path": state["path"], "offset": start, "bytes": count, "destination": destination})
            result = count
        else:
            state = handles.pop(obj)
            events.append({"operation": "close", "path": state["path"]})
            result = 1
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = uc.hook_add(UC_HOOK_CODE, bridge)
    portrait_rows, block_rows = [], []
    try:
        registration_trace = resource_call(uc, 0x10E190, ())
        # Actual call site 0209EDD8..0209EE14 uses blocks 14..17 and buffer 02233040.
        slack = IlnkContainer.parse(rom.read_file("/GRP/SLACKIMG.DK4"))
        actual_buffer = struct.unpack_from("<I", arm, 0x9F0B4)[0]
        assert actual_buffer == 0x02233040
        for block in range(14, 18):
            raw = slack.blocks[block]
            assert len(raw) == 104 * 136
            uc.mem_write(actual_buffer - 16, b"\xa5" * (len(raw) + 32))
            start = len(events)
            # Execute the actual parent block selection, archive helper and image
            # view construction. Parent context values come from its preceding
            # MOV/STR instructions; the complete UI constructor is not executed.
            uc.reg_write(UC_ARM_REG_SP, STACK)
            uc.reg_write(UC_ARM_REG_R4, 104)
            uc.reg_write(UC_ARM_REG_R6, 136)
            uc.reg_write(UC_ARM_REG_R9, block - 14)
            uc.reg_write(UC_ARM_REG_R11, 0)
            uc.mem_write(STACK + 0x14, struct.pack("<I", 0))
            uc.mem_write(STACK + 0xCC, b"\xa5" * 80)
            before = set(executed)
            uc.emu_start(0x0209EDD8, 0x0209EE18, count=100000)
            assert uc.reg_read(UC_ARM_REG_PC) == 0x0209EE18
            assert uc.reg_read(UC_ARM_REG_SP) == STACK
            assert uc.reg_read(UC_ARM_REG_R4) == 104 and uc.reg_read(UC_ARM_REG_R6) == 136
            assert uc.reg_read(UC_ARM_REG_R9) == block - 14 and uc.reg_read(UC_ARM_REG_R11) == 0
            trace = executed - before
            assert bytes(uc.mem_read(actual_buffer, len(raw))) == raw
            assert bytes(uc.mem_read(actual_buffer - 16, 16)) == b"\xa5" * 16
            assert bytes(uc.mem_read(actual_buffer + len(raw), 16)) == b"\xa5" * 16
            assert not handles and {0x020D2018, 0x020D1EF0, 0x020D1F50, 0x020D3D30} <= executed
            view = list(struct.unpack("<12I", uc.mem_read(STACK + 0xDC, 48)))
            owner = struct.unpack_from("<I", arm, 0x119E24 + (block - 14) * 4)[0]
            assert view[3] == owner and view[10:12] == [104, 136]
            filename_pointer = struct.unpack("<I", uc.mem_read(owner + 12, 4))[0]
            filename = bytes(uc.mem_read(filename_pointer, 128)).split(b"\0", 1)[0].decode("ascii")
            assert filename.replace("\\", "/").lstrip("/").startswith("_pxl/personbustup")
            assert bytes(uc.mem_read(STACK + 0xCC, 16)) == b"\xa5" * 16
            assert bytes(uc.mem_read(STACK + 0x10C, 16)) == b"\xa5" * 16
            portrait_rows.append({"block_index": block, "buffer_from_actual_caller_literal": actual_buffer, "bytes": len(raw), "sha256": sha(raw), "native_parent_segment_completed": True, "native_helper_returns_to_actual_parent_and_canaries": True, "new_distinct_instructions": len(trace), "actual_initialized_owner": owner, "actual_owner_filename": filename, "native_view": view, "actual_view_extent": [104, 136], "events": events[start:]})
        for _, path, data in rom.iter_files():
            if not path.startswith("/GRP/") or not data.startswith(b"ILNK"):
                continue
            archive = IlnkContainer.parse(data)
            assert archive.to_bytes() == data
            uc.mem_write(NAME, path.encode("ascii") + b"\0")
            uc.mem_write(OBJECT - 16, b"\xa5" * 80)
            call(uc, 0xD2100, (OBJECT,))
            call(uc, 0xD2018, (OBJECT, NAME))
            assert uc.reg_read(UC_ARM_REG_R0) == 1
            assert struct.unpack("<I", uc.mem_read(OBJECT + 0x28, 4))[0] == len(archive.blocks)
            for block_index, raw in enumerate(archive.blocks):
                reconstructed, chunks = bytearray(), []
                for offset in range(0, len(raw), CHUNK):
                    count = min(CHUNK, len(raw) - offset)
                    uc.mem_write(BUFFER - 16, b"\xa5" * (count + 32))
                    uc.mem_write(STACK, struct.pack("<I", count))
                    trace = call(uc, 0xD1EF0, (OBJECT, BUFFER, block_index, offset))
                    received = bytes(uc.mem_read(BUFFER, count))
                    assert received == raw[offset : offset + count]
                    assert uc.reg_read(UC_ARM_REG_R0) == count
                    assert bytes(uc.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
                    assert bytes(uc.mem_read(BUFFER + count, 16)) == b"\xa5" * 16
                    assert 0x020D1F50 in trace and 0x020D0170 in trace
                    reconstructed.extend(received)
                    chunks.append({"offset": offset, "bytes": count})
                assert bytes(reconstructed) == raw
                block_rows.append({"path": path, "block_index": block_index, "bytes": len(raw), "complete_sha256": sha(reconstructed), "chunks": chunks, "complete_native_return_ABI_and_canaries": True})
            call(uc, 0xD2004, (OBJECT,))
            call(uc, 0xD20E0, (OBJECT,))
            assert bytes(uc.mem_read(OBJECT - 16, 16)) == b"\xa5" * 16
            assert bytes(uc.mem_read(OBJECT + 44, 16)) == b"\xa5" * 16
            assert not handles
    finally:
        uc.hook_del(hook)
    result = {
        "status": "pass-native-ILNK-directory-and-offset-reader-SDK-bridge",
        "candidate": str(CANDIDATE),
        "candidate_sha256": sha(CANDIDATE.read_bytes()),
        "candidate_ARM9_sha256": sha(arm),
        "native_code_ranges_identical_to_canonical": [{"start_offset": lo, "end_exclusive": hi, "sha256": sha(arm[lo:hi])} for lo, hi in ranges],
        "actual_portrait_helper_calls": portrait_rows,
        "native_archive_blocks": block_rows,
        "block_count": len(block_rows),
        "bytes_verified": sum(row["bytes"] for row in block_rows),
        "native_read_chunks": sum(len(row["chunks"]) for row in block_rows),
        "distinct_native_instructions": len(executed),
        "actual_resource_registration_instructions": len(registration_trace),
        "SDK_bridge_addresses": [SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE],
        "SDK_events": events,
        "all_handles_closed": not handles,
        "hardware_filesystem_GPU_input_gameplay_verified": False,
        "limitations": [
            "SDK open/read/absolute-seek/close are explicitly bridged to the exact saved candidate filesystem.",
            "Native constructors, filename selection, archive count/directory offsets, partial reads, buffer copies and close logic execute unchanged ARM code.",
            "The actual portrait parent segment and helper use their real buffer literal and registered owners; preceding parent register/stack context is supplied, and the full UI constructor is not executed.",
            "The parent reads the raw bytes and constructs a view on a loose PXL owner; this does not prove that the raw buffer supplies the displayed pixels or palette.",
            "Generic archive reads use controlled chunk buffers and valid source-derived indices/ranges; no invalid-input or allocation safety claim is made.",
            "Pixel encoding, palette/alpha, parent resource binding, hardware OS/filesystem, GPU, input and gameplay remain unverified.",
        ],
        "rom_changed": False,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Pass: four actual portrait helper calls and {len(block_rows)} complete native-read archive blocks; SDK I/O bridged.")


if __name__ == "__main__":
    main()
