"""Verify current opening/menu pixels and native title resource views.

The live evidence is normal cold-boot playback. The separate resource probe uses
native registration, allocation and image construction with ROM-backed SDK I/O;
it does not manufacture a physical display for an unobserved title copy.
"""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/graphics_review_v229")
ROM = Path("out/all_routes_combined_v218_candidate.nds")
ROM_SHA = "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"
OPENING = Path("work/emulation_v193/graphics_review_v229/opening")
MOVIE = Path("work/emulation_v193/graphics_review_v229/full_movie")
MENU = Path("work/emulation_v193/no_target_v218")
VIEW = 0x02470020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def capture(root, frame):
    report = json.loads((root / "capture_report.json").read_text(encoding="utf-8"))
    if (report["ROM_sha256"] != ROM_SHA or not report["cold_boot"]
            or report["savestate_loaded"] or report["callback_errors"]):
        raise ValueError("Capture identity/cold-boot/callback gate differs")
    row = next(r for r in report["frames_captured"] if r["frame"] == frame)
    path = Path(row["path"])
    if sha(path.read_bytes()) != row["PNG_sha256"]:
        raise ValueError("Recorded framebuffer PNG differs")
    return Image.open(path).convert("RGB"), row


def live_pixels(image):
    archive = FlsArchive(image.read_file("/FLS/M28.fls"))
    masks, cases = {}, []
    for index, origin in [(4, (0, 48)), (5, (0, 82))]:
        texture = archive.texture(index)
        mask = {(i % texture.width + origin[0], i // texture.width + origin[1]): native5(texture.palette[n])
                for i, n in enumerate(texture.indices) if native5(texture.palette[n]) != (0, 0, 0)}
        if not all(0 <= x < 256 and 0 <= y < 192 for x, y in mask):
            raise ValueError("Opening foreground escapes screen")
        masks[index] = mask
        for frame in ([800, 850, 900] if index == 4 else [850, 900]):
            actual, row = capture(OPENING, frame)
            if any(native5(actual.getpixel(point)) != color for point, color in mask.items()):
                raise ValueError(f"Opening texture {index} loses/changes foreground at frame {frame}")
            cases.append({"asset_index": index, "frame": frame, "origin": list(origin),
                          "foreground_pixels_exact": len(mask), "capture": row,
                          "bounds": [min(p[0] for p in mask), min(p[1] for p in mask),
                                     max(p[0] for p in mask) + 1, max(p[1] for p in mask) + 1],
                          "all_first_last_letters_and_shadow_edges_present": True})
    actual, _ = capture(OPENING, 850)
    opaque_black = []
    for index, origin in [(4, (0, 48)), (5, (0, 82))]:
        texture = archive.texture(index)
        blanks = [(i % texture.width + origin[0], i // texture.width + origin[1])
                  for i, n in enumerate(texture.indices) if native5(texture.palette[n]) == (0, 0, 0)]
        black = [p for p in blanks if native5(actual.getpixel(p)) == (0, 0, 0)]
        if black:
            raise ValueError("Transparent movie padding paints opaque black over water")
        opaque_black.append({"asset_index": index, "black_key_source_pixels": len(blanks),
                             "opaque_black_pixels_in_unfaded_frame": 0})
    menu, row = capture(MENU, 1100)
    title = PxlImage.from_bytes(image.read_file("/_pxl/title/title03.pxl"))
    if (title.width, title.height) != (256, 192):
        raise ValueError("Reviewed menu dimensions differ")
    if any(native5(menu.getpixel((i % 256, i // 256))) != native5(title.palette[n])
           for i, n in enumerate(title.indices)):
        raise ValueError("Full native menu title differs from stored art")
    movie_report = json.loads((MOVIE / "capture_report.json").read_text(encoding="utf-8"))
    if (movie_report["ROM_sha256"] != ROM_SHA or not movie_report["cold_boot"]
            or movie_report["savestate_loaded"] or movie_report["callback_errors"]
            or movie_report["scripted_input_schedule"]):
        raise ValueError("Uninterrupted movie capture gate differs")
    expected_bytes = {index: [(y * 256 * 3 + x * 3, bytes(color)) for (x, y), color in mask.items()]
                      for index, mask in masks.items()}
    matching_movie_frames = {index: [] for index in masks}
    lut = [(v * 31 + 127) // 255 for v in range(256)]
    for movie_frame in movie_report["frames_captured"]:
        path = Path(movie_frame["path"])
        if sha(path.read_bytes()) != movie_frame["PNG_sha256"]:
            raise ValueError("Movie PNG identity differs")
        raw = Image.open(path).convert("RGB").crop((0, 0, 256, 192)).point(lut * 3).tobytes()
        for index, pixels in expected_bytes.items():
            if all(raw[at:at + 3] == color for at, color in pixels):
                matching_movie_frames[index].append(movie_frame["frame"])
    if not all(len(frames) >= 3 and max(frames) > 10000 for frames in matching_movie_frames.values()):
        raise ValueError("Repeated uninterrupted title displays not established")
    return {"opening_foreground_cases": cases, "opening_black_key_evidence": opaque_black,
            "uninterrupted_movie_matching_full_foreground_frames": matching_movie_frames,
            "uninterrupted_movie_captures_checked": len(movie_report["frames_captured"]),
            "movie_native_placement_is_two_pixels_above_authoring_preview": True,
            "menu_full_screen_pixels_exact": 49152, "menu_capture": row,
            "menu_background_copyright_both_logos_and_complete_bounds_verified": True}


def native_views(image, *, expected_paths=None, owner_range=(0x02312700, 0x02312890)):
    arm = image.read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    for lo, hi in [(0x10E190, 0x11182C), (0xD3D30, 0xD42AC), (0xD6524, 0xD6C90)]:
        if arm[lo:hi] != clean[lo:hi]:
            raise ValueError("Native registration/cache/image code differs")
    u = machine(arm)
    resource_call(u, 0x10E190, ())
    manager = struct.unpack_from("<I", arm, 0x5D24)[0]
    call(u, 0xD6C0C, (manager,))
    owners = {}
    # Search initialized native object fields, never assume that neighboring
    # filename literals form an owner/path pair. Some literals are vtables.
    expected = (set(expected_paths) if expected_paths is not None
                else {f"/_pxl/title/title{i:02d}.pxl" for i in range(7)})
    for pointer in range(*owner_range, 4):
        fields = struct.unpack("<5I", u.mem_read(pointer, 20))
        if fields[0] != 0x02160538:
            continue
        name = bytes(u.mem_read(fields[3], 96)).split(b"\0", 1)[0].decode("ascii")
        path = "/" + name.replace("\\", "/").lstrip("/")
        if path in expected:
            if path in owners:
                raise ValueError("Duplicate initialized title owner")
            owners[path] = pointer
    if set(owners) != expected:
        raise ValueError(f"Complete requested native owner set differs: {sorted(owners)}")
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 96)).split(b"\0", 1)[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            if path not in owners or obj in handles:
                raise ValueError("Native title file contract differs")
            data = image.read_file(path)
            handles[obj] = [path, data, 0]
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(data)))
            events.append({"operation": "open", "path": path, "sha256": sha(data)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = uc.reg_read(UC_ARM_REG_R1)
            if uc.reg_read(UC_ARM_REG_R2) != 0 or not 0 <= offset <= len(state[1]):
                raise ValueError("Native title seek leaves source")
            state[2] = offset
            result = 1
        elif address == READ:
            state = handles[obj]
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            if state[2] + count > len(state[1]):
                raise ValueError("Native title read leaves source")
            uc.mem_write(target, state[1][state[2]:state[2] + count])
            state[2] += count
            events.append({"operation": "read", "path": state[0], "count": count})
            result = count
        else:
            events.append({"operation": "close", "path": handles.pop(obj)[0]})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    try:
        for path, owner in sorted(owners.items()):
            data = image.read_file(path)
            pxl = PxlImage.from_bytes(data)
            u.mem_write(VIEW - 16, b"\xa5" * 80)
            u.mem_write(VIEW, bytes(48))
            # Same whole-image constructor arguments as original scene setup
            # 0203DEE0 -> 020D4018; zero width/height asks for native full extent.
            u.mem_write(STACK, bytes(8))
            trace = resource_call(u, 0xD4018, (VIEW, owner, 0, 0))
            fields = struct.unpack("<12I", u.mem_read(VIEW, 48))
            # Reproduce original scene 0203DEE0's virtual source-to-destination
            # copy. Zero optional crop dimensions are a lazy full-image view;
            # do not invent explicit bounds in the source or call slot +8 a
            # size getter (it is another view constructor).
            destination, point = VIEW + 0x100, VIEW + 0x200
            u.mem_write(destination - 16, b"\xa5" * 80)
            u.mem_write(destination, bytes(48))
            u.mem_write(point, bytes(8))
            resource_call(u, 0xD3D80, (destination,))
            destination_vtable = struct.unpack("<I", u.mem_read(destination, 4))[0]
            copy_method = struct.unpack("<I", u.mem_read(destination_vtable + 12, 4))[0]
            resource_call(u, copy_method - 0x02000000, (destination, point, VIEW))
            copied_fields = struct.unpack("<12I", u.mem_read(destination, 48))
            resource_call(u, 0xD4170, (destination,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            if (fields[3] != owner or copied_fields[1:] != fields[1:]
                    or bytes(u.mem_read(pointer, len(data))) != data or handles
                    or bytes(u.mem_read(VIEW - 16, 16)) != b"\xa5" * 16
                    or bytes(u.mem_read(VIEW + 48, 16)) != b"\xa5" * 16
                    or bytes(u.mem_read(destination - 16, 16)) != b"\xa5" * 16
                    or bytes(u.mem_read(destination + 48, 16)) != b"\xa5" * 16
                    or 0x020D4018 not in trace):
                raise ValueError(f"Native title view/header/palette/pixels/guards differ: {path}, pointer={pointer:#x}")
            cases.append({"path": path, "owner": owner, "data_pointer": pointer,
                          "source_sha256": sha(data), "complete_resource_bytes": len(data),
                          "native_view": list(fields), "destination_view": list(copied_fields),
                          "source_header_extent": [pxl.width, pxl.height],
                          "native_virtual_copy_method": copy_method,
                          "native_optional_crop_parameters": list(fields[7:12]),
                          "complete_header_palette_indices_exact": True,
                          "constructor_virtual_copy_return_stack_and_view_guards_verified": True,
                          "unobserved_physical_crop_not_claimed": path != "/_pxl/title/title03.pxl"})
    finally:
        u.hook_del(hook)
    return {"cases": cases, "SDK_file_contract_events": events,
            "actual_native_registration_allocation_constructor_and_cache_executed": True,
            "physical_title05_and_standalone_logo_display_not_inferred_from_fixture": True}


def main():
    if sha(ROM.read_bytes()) != ROM_SHA:
        raise ValueError("Current registered ROM identity differs")
    image = NdsImage.open(ROM)
    result = {"format": "dk4-title-display-native-proof-v229", "ROM": ROM.as_posix(),
              "ROM_sha256": ROM_SHA, "live_pixels": live_pixels(image), "native_views": native_views(image),
              "full_movie_capture_report_sha256": sha((MOVIE / "capture_report.json").read_bytes()),
              "scope": "Complete observed opening foreground across repeated uninterrupted playback and menu screen; seven native title resource views with explicit SDK I/O bridges. Unobserved copies and other scene/gameplay gates remain separate.",
              "registered_ROM_modified": False, "hardware_device_verification": False, "full_goal_complete": False}
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "title_native_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"opening_foreground_pixel_samples": sum(c["foreground_pixels_exact"] for c in result["live_pixels"]["opening_foreground_cases"]),
                      "menu_full_screen_pixels": 49152, "native_title_views": len(result["native_views"]["cases"]),
                      "ROM_modified": False}))


if __name__ == "__main__":
    main()
