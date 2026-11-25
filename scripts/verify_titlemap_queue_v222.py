"""Verify the real map-placement arguments and native deferred drawable queue."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path("work/analysis/titlemap_v222")
BASE = 0x02000000
HEADER, SOURCE, POINT = 0x02441000, 0x02441100, 0x02441400
BUFFER = 0x02233040


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    arm = rom.read_file("/__arm9__.bin")
    raw = rom.read_file("/GRP/TITLEMAP.DK4")
    u = machine(arm)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])[0]
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    control, scenes = struct.unpack_from("<2I", arm, 0xD3514)
    # The real call uses the point literal at 4BC88 and an integer priority at
    # 4BC8C. The earlier probe treated priority as a source-position pointer.
    point_pointer, priority = struct.unpack_from("<2I", arm, 0x4BC88)
    point = struct.unpack("<2I", u.mem_read(point_pointer, 8))
    assert point == (52, 36) and priority == 401
    u.mem_write(POINT, struct.pack("<2I", *point))
    u.mem_write(control + 4, struct.pack("<I", 1))
    rows = []
    for index in range(56):
        record = raw[index * 0x4940:(index + 1) * 0x4940]
        u.mem_write(BUFFER, record)
        colors = struct.pack("<256H", *(v | 0x8000 for v in struct.unpack("<256H", record[-512:])))
        u.mem_write(BUFFER + 0x4740, colors)
        u.mem_write(HEADER, struct.pack("<5I", 0x108, 76, 120,
                                       (BUFFER + 0x4740 - HEADER) & 0xFFFFFFFF,
                                       (BUFFER - HEADER) & 0xFFFFFFFF))
        u.mem_write(SOURCE - 16, b"\xa5" * 160)
        call(u, 0xD4524, (SOURCE,))
        u.mem_write(STACK, struct.pack("<4I", 152, 120, 0, 0))
        call(u, 0xD3AFC, (SOURCE, HEADER, 0, 0))
        u.mem_write(scenes + 12, bytes(12))
        vtable = struct.unpack("<I", u.mem_read(SOURCE, 4))[0]
        adjustment = struct.unpack("<I", u.mem_read(vtable - 12, 4))[0]
        assert adjustment == 0x30
        u.mem_write(STACK, struct.pack("<I", 0))
        # Parent-widget NULL is an explicit empty-scene fixture, not a destination
        # bitmap. No scene render, physical framebuffer or input result is claimed.
        call(u, 0xD4988, (SOURCE + adjustment, 0, POINT, priority))
        drawable = SOURCE + 0x44
        state = struct.unpack("<12I", u.mem_read(drawable, 48))
        assert state[3] == priority
        assert state[5] == scenes + 12 and state[6] == 0 and state[7] == 1
        assert state[8:12] == (52, 36, 204, 156)
        assert bytes(u.mem_read(SOURCE - 16, 16)) == b"\xa5" * 16
        assert bytes(u.mem_read(SOURCE + 0x80, 16)) == b"\xa5" * 16
        assert bytes(u.mem_read(BUFFER, 0x4940)) == record[:-512] + colors
        rows.append({"index": index, "original_source_sha256": sha(record),
                     "native_destination_bounds": list(state[8:12]), "priority": state[3],
                     "actual_copy_interface_adjustment": adjustment,
                     "actual_native_queue_owner": state[5], "parent_widget_fixture": state[6],
                     "native_return_saved_registers_stack_and_object_guards_exact": True})
    report = {"format": "dk4-titlemap-native-deferred-queue-proof-v1", "ROM_sha256": sha(rom.source.read_bytes()),
              "cases": rows, "native_point_literal": point_pointer, "native_priority_literal_value": priority,
              "all_56_destination_bounds_fit_256x192": True,
              "earlier_argument_order_and_destination_bitmap_assumption_corrected": True,
              "active_scene_one_and_parent_NULL_are_explicit_fixtures": True,
              "C9904_is_UI_hierarchy_processing_not_a_direct_bitmap_blit": True,
              "actual_scene_render_framebuffer_GPU_and_gameplay_selection_pending": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_queue_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_queued_maps": len(rows), "exact_destination_bounds": [52, 36, 204, 156],
                      "drawing_priority": priority, "object_guards_and_ABI_pass": True}))


if __name__ == "__main__":
    main()
