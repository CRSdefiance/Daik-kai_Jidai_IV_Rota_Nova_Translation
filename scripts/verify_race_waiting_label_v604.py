"""Verify the inherited missing final letter and the complete native card repair."""

import copy
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.race_waiting_label import AFTER, BEFORE, OFFSET, apply_release
from dk4tool.rom.nds import NdsImage
from scripts.prepare_blitter_trace_v603 import CONTROL, FIELDS, RECORDS, STRIDE
from scripts.verify_blitter_trace_v603 import target
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path("work/analysis/race_controls_v604")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ROM = Path("out/all_routes_combined_v604_candidate.nds")
PARENT = Path("out/all_routes_combined_v599_candidate.nds")
DIGEST = "fb8de61d20e94e742574bded2d8e4251305f2b56265ff8624dd766eaa6cf9158"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def report(name, digest, frames):
    path = CAPTURE / name / "capture_report.json"
    d = read(path)
    assert d["ROM_sha256"] == digest and d["frames"] == frames
    assert d["cold_boot"] and not d["savestate_loaded"] and not d["callback_errors"]
    shots = {}
    for row in d["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        shots[row["frame"]] = Image.open(row["path"]).convert("RGB")
    ram = {}
    for row in d.get("read_only_capture_RAM_snapshots", []):
        assert row["read_only_export"]
        data = Path(row["path"]).read_bytes()
        assert sha(data) == row["sha256"] and len(data) == 0x400000
        ram[row["frame"]] = data
    return d, shots, ram, {"path": str(path), "sha256": sha(path.read_bytes())}


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    current, parent = NdsImage.open(ROM), NdsImage.open(PARENT)
    parent_sha = sha(PARENT.read_bytes())
    before = {p: b for _, p, b in parent.iter_files()} | dict(parent.iter_components())
    after = {p: b for _, p, b in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys()
    changed = sorted(p for p in before if before[p] != after[p])
    assert changed == ["/__arm9__.bin"]
    arm, original_arm = after[changed[0]], before[changed[0]]
    expected, transform = apply_release(original_arm, "translations/race_waiting_label_v1.json")
    assert arm == expected
    byte_diff = [i for i, pair in enumerate(zip(arm, original_arm, strict=True)) if pair[0] != pair[1]]
    assert byte_diff and all(OFFSET <= i < OFFSET + len(BEFORE) for i in byte_diff)
    manifest, previous = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    registry = read("translations/release_stack.json")
    assert manifest["profile"] == "all-routes-unified-v604" and manifest["candidate_sha256"] == DIGEST
    assert manifest["base_sha256"] == registry["canonical_baseline"]["sha256"]
    assert sha(Path(manifest["base_rom"]).read_bytes()) == manifest["base_sha256"]
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["batches"] == previous["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == previous["required_batches"] and len(registry["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    assert manifest["relocations"]["/__arm9__.bin"]["race_waiting_label"]["target_arm9_sha256"] == sha(arm)
    assert sha((ROOT / "v604_reconstructed_RESEARCH_ONLY.nds").read_bytes()) == DIGEST
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == "5fa980cd6995606989375b69e6be7083cfcb6fbe90c122e96e2a30d7bc20cc7a"
    font = GameAsciiFont.from_arm9(arm)
    assert font.glyphs == GameAsciiFont.from_arm9(original_arm).glyphs
    host, host_images, host_ram, host_binding = report("race_controls_v604_host_candidate", DIGEST, 5600)
    old_host, old_images, old_ram, old_host_binding = report("race_controls_v604_host_return_baseline", parent_sha, 5600)
    assert host["scripted_input_schedule"] == old_host["scripted_input_schedule"]
    for d in (host, old_host):
        assert d["battery_save_preloaded"]["source_sha256"] == "295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949"
        assert len(d["synthetic_gallery_fixtures"]) == 1 and not d["synthetic_gallery_fixtures"][0]["earned_unlock_verified"]
    labels, old_missing, whole_host, host_changes = [], [], [], []
    for frame in sorted(host_images):
        image, old = host_images[frame], old_images[frame]
        if frame not in (4400, 4800, 5200):
            assert image.tobytes() == old.tobytes()
            whole_host.append(frame)
            continue
        q, old_q = image.point(lambda n: n >> 3), old.point(lambda n: n >> 3)
        for y in (240, 280, 318):
            text = AFTER[:-1].decode("ascii")
            count, bounds = complete_mask(font, text, q, 74, y, (28, 28, 28))
            assert count == 168 and bounds == [74, y, 164, y + 11]
            # Every blank cell through the old120px extent is checked as well;
            # old trailing letters may not remain outside the shorter label.
            complete_mask(font, text + " " * 5, q, 74, y, (28, 28, 28))
            labels.append({"frame": frame, "text": text, "bounds": bounds, "complete_ink_points": count,
                           "whole_old_120px_foreground_region_including_blank_tail_exact": True})
            missing = [(74 + i * 6 + x, y + dy) for i, c in enumerate(BEFORE[:-1].decode("ascii"))
                       for dy in range(11) for x in range(6)
                       if font.decode(c).getpixel((x, dy)) and old_q.getpixel((74 + i * 6 + x, y + dy)) != (28, 28, 28)]
            assert len(missing) == (8 if y == 280 else 0)
            if missing:
                assert all(x >= 74 + 19 * 6 for x, _ in missing)
                old_missing.append({"frame": frame, "source_row": y, "missing_final_r_points": missing})
        masked, old_masked = image.copy(), old.copy()
        for y in (240, 280, 318):
            masked.paste((0, 0, 0), (74, y, 194, y + 11))
            old_masked.paste((0, 0, 0), (74, y, 194, y + 11))
        assert masked.tobytes() == old_masked.tobytes()
        changes = sum(a != b for a, b in zip(image.get_flattened_data(), old.get_flattened_data(), strict=True))
        host_changes.append({"frame": frame, "changed_pixels": changes,
                             "all_other_whole_frame_pixels_exact": True})
        assert host_ram[frame][OFFSET:OFFSET + len(BEFORE)] == AFTER.ljust(len(BEFORE), b"\0")
        assert old_ram[frame][OFFSET:OFFSET + len(BEFORE)] == BEFORE
    join, join_images, _, join_binding = report("race_controls_v604_join_candidate", DIGEST, 5600)
    old_join, old_join_images, _, old_join_binding = report("race_controls_v604_join_baseline", parent_sha, 5600)
    assert join["scripted_input_schedule"] == old_join["scripted_input_schedule"]
    assert join_images.keys() == old_join_images.keys()
    assert all(image.tobytes() == old_join_images[n].tobytes() for n, image in join_images.items())
    market, market_images, _, market_binding = report("race_controls_v604_market_candidate", DIGEST, 24100)
    old_market, old_market_images, _, old_market_binding = report("keyboard_v599_market_regression", parent_sha, 24100)
    assert market["scripted_input_schedule"] == old_market["scripted_input_schedule"]
    assert market.get("battery_save_preloaded") is None
    assert market_images.keys() == old_market_images.keys()
    assert all(image.tobytes() == old_market_images[n].tobytes() for n, image in market_images.items())
    trace, trace_images, _, trace_binding = report("race_controls_v604_host_navigation",
        "" + read("work/analysis/blitter_trace_v603/fixture_manifest.json")["research_ROM_sha256"], 5200)
    assert trace_images[4400].tobytes() == old_images[4400].tobytes()
    native = trace["read_only_native_state"]
    assert native["read_only_export"] and not native["state_loaded"] and native["main_RAM_unchanged_by_export"]
    assert sha(Path(native["path"]).read_bytes()) == native["sha256"]
    region = native["regions"]["ITCM"]
    data = Path(region["path"]).read_bytes()
    assert sha(data) == region["sha256"]
    calls, selected, used, overflow, controls, magic = struct.unpack_from("<6I", data, CONTROL & 0x7FFF)
    rows = [dict(zip(FIELDS, struct.unpack_from("<20I", data, (RECORDS & 0x7FFF) + i * STRIDE), strict=True))
            for i in range(used)]
    assert calls == 27582 and selected == used == 2 and overflow == 0 and controls == 3 and magic == 0x603B117
    assert {r["kind"] for r in rows} == {0, 1} and not any(target(r) for r in rows)
    parent_proof_path = Path("work/analysis/keyboard_labels_v599/preservation_proof.json")
    preservation = copy.deepcopy(read(parent_proof_path))
    assert preservation["candidate_sha256"] == parent_sha
    preservation.update(candidate=str(ROM), candidate_sha256=DIGEST, parent_proof=str(parent_proof_path),
        parent_proof_sha256=sha(parent_proof_path.read_bytes()), only_changed_component_from_V599="/__arm9__.bin",
        all_graphics_files_and_embedded_containers_exact_V599=True, race_waiting_label_transform=transform,
        all_other_ARM9_bytes_exact_V599=True)
    save(ROOT / "preservation_proof.json", preservation)
    save(ROOT / "release_proof.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
        "parent": str(PARENT), "parent_sha256": parent_sha, "changed_components": changed,
        "profile": manifest["profile"], "canonical_baseline": registry["canonical_baseline"],
        "manifest_sha256": sha(ROM.with_suffix(".manifest.json").read_bytes()),
        "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()), "exact_clean_patch_reconstruction": True,
        "470_batches_114_accepted_layers_retained": True, "transform": transform, "changed_ARM9_bytes": byte_diff,
        "all_graphics_and_embedded_files_exact_V599": True, "complete_native_label_masks": labels,
        "old_clipped_final_letter_evidence": old_missing, "native_host_changes": host_changes,
        "whole_host_return_and_preceding_frames_exact": whole_host, "whole_Join_frames_exact": sorted(join_images),
        "whole_Market_frames_exact": sorted(market_images), "Host_and_Join_Back_verified": True,
        "trace_drawing_calls": calls, "trace_no_target_records_zero_overflow_both_positive_controls": True,
        "ordinary_Confirm_and_miniature_parents_still_open": True,
        "reports": {"host": host_binding, "host_baseline": old_host_binding, "join": join_binding,
                    "join_baseline": old_join_binding, "market": market_binding, "market_baseline": old_market_binding,
                    "research_trace": trace_binding},
        "synthetic_system_unlock_not_earned": True, "wireless_peer_or_completed_race_not_verified": True,
        "script_sha256": sha(Path(__file__).read_bytes()), "status": "experimental", "full_goal_complete": False})
    print(f"V604: {len(labels)} full native labels/{sum(r['complete_ink_points'] for r in labels)} ink points; inherited final-r loss confirmed; outside text exact; Join/Market/Back exact; patch exact;18/22 open.")


if __name__ == "__main__":
    main()
