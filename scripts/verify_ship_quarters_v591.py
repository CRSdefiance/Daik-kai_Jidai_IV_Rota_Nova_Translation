"""Verify the exact registered repair and matched ordinary sailing captures."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_quarters_label import FACE, FILE, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/ship_quarters_v591")
ROM = Path("out/all_routes_combined_v591_candidate.nds")
PARENT = Path("out/all_routes_combined_v581_candidate.nds")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
OWNER, VTABLE = 0x02313C90, 0x0216017C


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def report(folder, digest):
    path = folder / "capture_report.json"
    r = read(path)
    assert r["ROM_sha256"] == digest and r["frames"] == 5840
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert r["scripted_input_schedule"] == read(ROOT / "replay_inputs.json")
    assert not any(value for key, value in r.items() if key.startswith("synthetic_"))
    save = r["battery_save_preloaded"]
    assert save["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
    assert sha(Path(save["source"]).read_bytes()) == save["source_sha256"]
    for shot in r["frames_captured"]:
        assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
    for snap in r["read_only_capture_RAM_snapshots"]:
        assert sha(Path(snap["path"]).read_bytes()) == snap["sha256"]
    return r, {"path": str(path), "sha256": sha(path.read_bytes())}


def main():
    current, parent, clean = [NdsImage.open(p) for p in (ROM, PARENT, Path("work/clean.nds"))]
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    assert parent_digest == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    manifest, old_manifest = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    stack = read("translations/release_stack.json")
    assert manifest["profile"] == "all-routes-unified-v591" and manifest["candidate_sha256"] == digest
    assert manifest["base_sha256"] == stack["canonical_baseline"]["sha256"]
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["batches"] == old_manifest["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == old_manifest["required_batches"] and len(stack["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    before = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    after = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == [FILE]
    _, expected, patch_report = apply_release(parent, clean, "translations/ship_quarters_label_v1.json")
    assert expected == after[FILE]
    plan = read(ROOT / "plan.json")
    original, revised = [PxlImage.from_bytes(d[FILE]) for d in (before, after)]
    assert original.source[:original.pixels_offset] == revised.source[:revised.pixels_offset]
    changed = {(n % original.width, n // original.width) for n, (a, b) in enumerate(zip(original.indices, revised.indices, strict=True)) if a != b}
    assert len(changed) == plan["changed_pixels"] == 144
    assert changed <= {tuple(p) for p in plan["old_ink"] + plan["new_ink"]}
    preservation_path = Path("work/analysis/equipment_material_v580/v581_preservation_proof.json")
    preservation = read(preservation_path)
    assert preservation["candidate_sha256"] == parent_digest
    assert len(preservation["entries"]) == 921 and preservation["all57_embedded_block_extents_exact"]
    assert all(before[row["path"]] == after[row["path"]] for row in preservation["entries"] if row["path"] != FILE)
    make_xdelta(Path("work/clean.nds"), ROM, ROM.with_suffix(".xdelta"))
    reconstructed = ROOT / "reconstructed_exact.nds"
    apply_xdelta(Path("work/clean.nds"), ROM.with_suffix(".xdelta"), reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    control, control_binding = report(CAPTURE / "ship_quarters_v591_control", parent_digest)
    actual, actual_binding = report(CAPTURE / "ship_quarters_v591_actual", digest)
    assert actual["core_options"] == control["core_options"]
    a, b = [{s["frame"]: s for s in r["frames_captured"]} for r in (control, actual)]
    assert a.keys() == b.keys()
    cases, native_views, counts = [], [], []
    font = GameAsciiFont.from_arm9(after["/__arm9__.bin"])
    u = machine(after["/__arm9__.bin"])
    for frame in sorted(a):
        old, new = [Image.open(s[frame]["path"]).convert("RGB") for s in (a, b)]
        assert old.size == new.size == (256, 384)
        ship_view = frame in (5320, 5340, 5360)
        differences = {(x, y) for y in range(384) for x in range(256) if native5(old.getpixel((x, y))) != native5(new.getpixel((x, y)))}
        assert differences == (changed if ship_view else set()), (frame, len(differences))
        if ship_view:
            for x, y in changed:
                assert native5(old.getpixel((x, y))) == native5(original.palette[original.indices[y * 256 + x]])
                assert native5(new.getpixel((x, y))) == native5(revised.palette[revised.indices[y * 256 + x]])
            left, top, right, bottom = FACE
            assert all(native5(new.getpixel((x, y))) == native5(revised.palette[revised.indices[y * 256 + x]])
                       for y in range(top, bottom) for x in range(left, right))
            # Complete original-font reconstruction, including both word ends.
            full_mask = {(16 + n * 5 + xx, 103 + yy) for n, ch in enumerate("Quarters")
                         for yy in range(11) for xx in range(6) if font.decode(ch).getpixel((xx, yy))}
            assert full_mask == {tuple(p) for p in plan["new_ink"]} and len(full_mask) == 100
            assert all(native5(new.getpixel(p)) == native5(revised.palette[1]) for p in full_mask)
            raw_path = CAPTURE / f"ship_quarters_v591_actual/frame_{frame:06d}_arm9_ram.bin"
            raw = raw_path.read_bytes()
            assert len(raw) == 0x400000
            matches = []
            for offset in range(0, len(raw) - 48, 4):
                values = struct.unpack_from("<12I", raw, offset)
                if values[3] == OWNER and values[7:12] == (0, 0, 0, 256, 192):
                    matches.append((BASE + offset, values))
            assert len(matches) == 1
            view, values = matches[0]
            assert values[0] == VTABLE
            u.mem_write(BASE, raw)
            executed = call(u, 0xD4170, (view,))
            assert not {0x020DED50, 0x020DEBDC} & executed
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(after[FILE]))) == after[FILE]
            filename = bytes(u.mem_read(int.from_bytes(u.mem_read(OWNER + 12, 4), "little"), 80)).split(b"\0")[0]
            assert filename == b"_pxl/shipinfo.pxl"
            native_views.append({"frame": frame, "view": view, "fields": list(values),
                                 "resident_pointer": pointer, "complete_resident_file_exact": True,
                                 "original_resolver_no_FS_bridge_or_supplied_binding": True,
                                 "whole_1008_pixel_face_exact": True, "complete_Quarters_ink": 100})
        cases.append({"frame": frame, "whole_two_screen_pixels_checked": 98304,
                      "changed_pixels": len(differences), "only_complete_expected_Quarters_pixels_changed": ship_view,
                      "unchanged_other_menu_or_startup_frame": not ship_view})
    for frame, region in ((5360, (64, 96, 88, 124)), (5840, (64, 104, 88, 130))):
        counts.append({"frame": frame, **find_mask(font, "1", Image.open(b[frame]["path"]).convert("RGB"), region)})
    final_ship = Image.open(b[5360]["path"]).convert("RGB")
    left, top, right, bottom = FACE
    observed_face = {(x, y): native5(final_ship.getpixel((x, y)))
                     for y in range(top, bottom) for x in range(left, right)}
    expected_face = {(x, y): native5(revised.palette[revised.indices[y * 256 + x]])
                     for y in range(top, bottom) for x in range(left, right)}

    def full_face_matches(pixels):
        return pixels == expected_face

    assert full_face_matches(observed_face)
    blank = observed_face[left, top]
    assert blank != native5(revised.palette[1])
    negatives = []
    for n in (0, 7):
        points = {(16 + n * 5 + xx, 103 + yy) for yy in range(11) for xx in range(6)
                  if font.decode("Quarters"[n]).getpixel((xx, yy))}
        assert points and points <= full_mask
        negative = dict(observed_face)
        for point in points:
            negative[point] = blank
        assert not full_face_matches(negative)
        negatives.append({"character": "Quarters"[n], "index": n, "erased_ink_points": len(points),
                          "complete_mask_rejects_missing_first_or_last_letter": True})
    result = {"candidate": str(ROM), "candidate_sha256": digest,
              "parent": str(PARENT), "parent_sha256": parent_digest,
              "canonical_base": manifest["base_rom"], "canonical_base_sha256": manifest["base_sha256"],
              "profile": manifest["profile"], "manifest_sha256": sha(ROM.with_suffix(".manifest.json").read_bytes()),
              "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()), "exact_clean_patch_reconstruction": True,
              "only_shipinfo_changes_from_V581": True, "all_code_route_data_and_other_graphics_exact": True,
              "inherited_470_batches_114_layers_921_entries_57_embedded_blocks_retained": True,
              "parent_preservation_proof": str(preservation_path), "parent_preservation_proof_sha256": sha(preservation_path.read_bytes()),
              "label_change": patch_report, "control_report": control_binding, "actual_report": actual_binding,
              "same_ordinary_schedule_save_and_core_options": True, "captured_frame_cases": cases,
              "native_view_bindings": native_views, "actual_same_ship_quarters_counts": counts,
              "first_final_letter_negative_controls": negatives, "all_other_native_frame_pixels_exact": True,
              "source_save_unchanged_no_synthetic_fixtures_or_save_acceptance": True,
              "ordinary_miniature_Confirm_Admiral_and_other_contexts_remain_open": True,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "experimental_not_human_accepted": True, "full_goal_complete": False}
    (ROOT / "release_proof.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"V591 verified:144 glyph-only changes;3 complete native Quarters faces;{len(cases)} complete paired frames;exact clean patch and unchanged inherited stack.")


if __name__ == "__main__":
    main()
