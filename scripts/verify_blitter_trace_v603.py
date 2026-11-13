"""Bind native drawing-call logs to cold boots, exact captures and bounded scope."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image, ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_blitter_trace_v603 import (
    CAPACITY,
    CONTROL,
    CORNER,
    END,
    ENTRY,
    FIELDS,
    RECORDS,
    ROOT,
    SOURCE,
    STRIDE,
    TILE,
)

CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
SCENES = {"keyboard": (7900, "keyboard_labels_v599"),
          "deck": (4650, "blitter_trace_v603_deck_baseline"),
          "market": (24100, "keyboard_v599_market_regression")}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def target(row):
    if row["width_words"] == 12 and row["height"] == 20:
        return "Confirm-shape"
    if row["height"] == 8 and row["width_words"] in (4, 6, 8, 12):
        return "small-independent-canvas"
    if row["height"] == 256 and row["width_words"] in (64, 128):
        # Matches the runtime conservative zero-size bound: the original tiled
        # routine can paint a one-pixel source when its descriptor extent is 0.
        left = 440 if row["width_words"] == 128 else 184
        sx, sy, width, height = [signed(row[k]) for k in FIELDS[5:9]]
        if sx < left + 72 and sx + max(1, width) > left and sy < 56 and sy + max(1, height) > 32:
            return "miniature-atlas-intersection"
    return None


def signed(value):
    return value if value < 0x80000000 else value - 0x100000000


def main():
    manifest_path = ROOT / "fixture_manifest.json"
    manifest = read(manifest_path)
    assert manifest["script_sha256"] == sha(Path("scripts/prepare_blitter_trace_v603.py").read_bytes())
    abi_path = ROOT / "ABI_proof.json"
    abi = read(abi_path)
    assert abi["fixture_manifest_sha256"] == sha(manifest_path.read_bytes())
    assert abi["script_sha256"] == sha(Path("scripts/verify_blitter_trace_abi_v603.py").read_bytes())
    assert sha(SOURCE.read_bytes()) == manifest["production_ROM_sha256"]
    research_path = Path(manifest["research_ROM"])
    assert sha(research_path.read_bytes()) == manifest["research_ROM_sha256"]
    research = NdsImage.open(research_path)
    arm = research.read_file("/__arm9__.bin")
    sections = MainCodeFile(arm, 0x02000000).sections
    payload = next(bytes(s.data) for s in sections if s.ramAddress == ENTRY)
    low = next(s for s in sections if s.ramAddress <= CORNER < s.ramAddress + len(s.data))
    corner_branch = bytes(low.data[CORNER - low.ramAddress:CORNER - low.ramAddress + 4])
    overlay = loadOverlayTable(research.rom.arm9OverlayTable, lambda _id, fid: research.rom.files[fid])[0]
    tile_branch = bytes(overlay.data[TILE - overlay.ramAddress:TILE - overlay.ramAddress + 4])
    source_atlas = NdsImage.open(SOURCE).read_file("/_pxl/__frame.pxl")
    source_pixel_word = struct.unpack_from("<I", source_atlas, struct.unpack_from("<I", source_atlas, 16)[0])[0]
    runs, total_calls, total_pairs, total_unique = [], 0, 0, 0
    for scene, (frames, baseline_name) in SCENES.items():
        report_path = CAPTURE / f"blitter_trace_v603_{scene}/capture_report.json"
        baseline_path = CAPTURE / baseline_name / "capture_report.json"
        r, baseline = read(report_path), read(baseline_path)
        assert r["ROM_sha256"] == manifest["research_ROM_sha256"]
        assert baseline["ROM_sha256"] == manifest["production_ROM_sha256"]
        assert r["frames"] == baseline["frames"] == frames
        assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
        assert r["scripted_input_schedule"] == baseline["scripted_input_schedule"]
        native = r["read_only_native_state"]
        assert native["read_only_export"] and not native["state_loaded"]
        assert native["main_RAM_unchanged_by_export"] and native["serialized_RAM_matches_same_frame_direct_export"]
        assert sha(Path(native["path"]).read_bytes()) == native["sha256"]
        for region in native["regions"].values():
            assert sha(Path(region["path"]).read_bytes()) == region["sha256"]
        itcm = Path(native["regions"]["ITCM"]["path"]).read_bytes()
        assert len(itcm) == 0x8000
        assert itcm[ENTRY & 0x7FFF:CONTROL & 0x7FFF] == payload[:CONTROL - ENTRY]
        assert itcm[CORNER & 0x7FFF:(CORNER & 0x7FFF) + 4] == corner_branch
        assert itcm[TILE & 0x7FFF:(TILE & 0x7FFF) + 4] == tile_branch
        assert itcm[(RECORDS & 0x7FFF) + CAPACITY * STRIDE:END & 0x7FFF] == bytes(END - RECORDS - CAPACITY * STRIDE)
        total, selected, used, overflow, positive_mask, magic = struct.unpack_from("<6I", itcm, CONTROL & 0x7FFF)
        assert total > 10000 and used <= CAPACITY and overflow == 0 and positive_mask == 3 and magic == 0x603B117
        rows = [dict(zip(FIELDS, struct.unpack_from("<20I", itcm, (RECORDS & 0x7FFF) + i * STRIDE), strict=True))
                for i in range(used)]
        assert selected == sum(row["hits"] for row in rows)
        assert {row["kind"] for row in rows} == {0, 1}
        hits = [row for row in rows if target(row)]
        assert not hits
        # These are positive samples, not counts of every use of these ordinary
        # source regions. Their file identity is only bound at the final keyboard
        # snapshot; logged addresses have been reused by the other two scenes.
        assert len(rows) == 2
        assert all(row["first_pixel_word"] == source_pixel_word and row["bank"] == 48 for row in rows)
        raw_info = r["read_only_RAM_snapshot"]
        raw = Path(raw_info["path"]).read_bytes()
        assert sha(raw) == raw_info["sha256"] and len(raw) == 0x400000
        resident = raw.find(source_atlas)
        assert resident >= 0
        at_logged = []
        for row in rows:
            at = row["header"] - 0x02000000
            at_logged.append(raw[at:at + len(source_atlas)] == source_atlas)
        assert at_logged == ([True, True] if scene == "keyboard" else [False, False])
        old_shots = {s["frame"]: s for s in baseline["frames_captured"]}
        compared, unmatched, unique = [], [], set()
        for shot in r["frames_captured"]:
            assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
            if shot["frame"] not in old_shots:
                unmatched.append(shot["frame"])
                continue
            old = old_shots[shot["frame"]]
            assert sha(Path(old["path"]).read_bytes()) == old["PNG_sha256"]
            current_image = Image.open(shot["path"]).convert("RGB")
            old_image = Image.open(old["path"]).convert("RGB")
            assert current_image.size == old_image.size == (256, 384)
            assert ImageChops.difference(current_image, old_image).getbbox() is None
            compared.append(shot["frame"])
            unique.add(shot["frame"])
        assert unmatched == ([6900] if scene == "keyboard" else [])
        if scene == "deck":
            save = r["battery_save_preloaded"]
            assert save["source_sha256"] == baseline["battery_save_preloaded"]["source_sha256"]
            assert sha(Path(save["source"]).read_bytes()) == save["source_sha256"]
        else:
            assert r.get("battery_save_preloaded") is None
        runs.append({"scene": scene, "frames": frames, "report": str(report_path),
            "report_sha256": sha(report_path.read_bytes()), "baseline_report": str(baseline_path),
            "baseline_report_sha256": sha(baseline_path.read_bytes()), "native_state": native["path"],
            "native_state_sha256": native["sha256"], "drawing_calls": total, "filtered_calls": selected,
            "unique_records": used, "overflow": overflow, "both_original_drawing_entries_still_hooked_at_end": True,
            "helper_code_and_log_tail_unchanged": True, "records": rows, "target_records": hits,
            "whole_capture_comparisons_exact": compared, "unique_compared_frames": sorted(unique),
            "uncompared_frames": unmatched, "current_atlas_resident_address": resident + 0x02000000,
            "logged_addresses_still_match_whole_current_atlas_at_final_frame": at_logged,
            "logged_address_reuse_not_misidentified_as_current_owner": True})
        total_calls += total
        total_pairs += len(compared)
        total_unique += len(unique)
    proof = {"status": "pass-scoped-runtime-drawing-trace-no-target-in-three-input-paths",
        "script_sha256": sha(Path(__file__).read_bytes()), "fixture_manifest": str(manifest_path),
        "fixture_manifest_sha256": sha(manifest_path.read_bytes()), "ABI_proof": str(abi_path),
        "ABI_proof_sha256": sha(abi_path.read_bytes()), "headless_runner_sha256": sha(Path("scripts/headless_desmume_v193.py").read_bytes()),
        "production_ROM": str(SOURCE), "production_ROM_sha256": manifest["production_ROM_sha256"],
        "runs": runs, "total_native_frames": sum(v[0] for v in SCENES.values()), "total_drawing_calls": total_calls,
        "whole_capture_pairs_exact": total_pairs, "unique_frame_pairs_exact": total_unique,
        "unique_whole_frame_pixel_positions": total_unique * 98304,
        "target_records": 0, "all_runs_zero_overflow": True, "ordinary_Confirm_and_five_miniature_parents_still_open": True,
        "limits": ["Instrumented research ROM; no guide, earned-outcome or hardware credit.",
                   "Selection covers declared 4-bit shapes and 256/512-square miniature atlas intersections only.",
                   "Other GPU, direct-color, resized, partial/composed and unrelated input paths remain untested.",
                   "Whole-atlas identity at a later snapshot does not prove the content at an earlier logged call.",
                   "No global unused-asset conclusion and no fully completed plaque entries."],
        "production_ROM_patch_or_registry_changed": False, "goal_complete": False}
    (ROOT / "native_trace_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"V603: {total_calls} native drawing calls/{proof['total_native_frames']} frames; {total_pairs} exact captures/{total_unique} unique frames; zero target records/overflow; ordinary parents open.")


if __name__ == "__main__":
    main()
