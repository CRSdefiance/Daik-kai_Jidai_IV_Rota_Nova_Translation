"""Exact inherited build and the actual missing-D tutorial's complete pixels."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.modal_cursor_guard import ROOT, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_modal_cursor_native_v271 import raster

ROM = Path("out/all_routes_combined_v271_candidate.nds")
CAPTURE = Path("work/emulation_v193/modal_cursor_v271")
PRIOR = Path("work/emulation_v193/direct_equipment_v270")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    old_path = Path("out/all_routes_combined_v270_candidate.nds")
    assert (ROOT / "v270_reproduction.nds").read_bytes() == old_path.read_bytes()
    a, b = NdsImage.open(old_path), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    original, arm = a.read_file("/__arm9__.bin"), b.read_file("/__arm9__.bin")
    target, plan = transform(original)
    assert arm == target == (ROOT / "research_arm9.bin").read_bytes()
    m, old_m = load(ROM.with_suffix(".manifest.json")), load(old_path.with_suffix(".manifest.json"))
    norm = lambda rows: [p.replace("\\", "/") for p in rows]
    assert norm(m["batches"]) == norm(old_m["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == old_m["required_batches"]
    for path, records in old_m["changed_records"].items():
        assert set(records) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest and m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report, old_report = load(CAPTURE / "capture_report.json"), load(PRIOR / "capture_report.json")
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == old_report["frames"] == 28400 and not report["callback_errors"]
    assert report["scripted_input_schedule"] == old_report["scripted_input_schedule"]
    lookup = {r["frame"]: r for r in old_report["frames_captured"] if "cold_boot" in r["path"]}
    unchanged, changed = [], []
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if "cold_boot" not in row["path"] or row["frame"] not in lookup:
            continue
        now = Image.open(row["path"]).convert("RGB")
        before = Image.open(lookup[row["frame"]]["path"]).convert("RGB")
        delta = [(x, y) for y in range(384) for x in range(256) if now.getpixel((x, y)) != before.getpixel((x, y))]
        if delta:
            assert all(16 <= x < 240 and 296 <= y < 376 for x, y in delta), row["frame"]
            changed.append(row["frame"])
        else:
            unchanged.append(row["frame"])
    assert 22000 in changed
    text = IlnkContainer.parse(b.read_file("/data/SC0.DK4")).blocks[43].split(b"\0")[45][1:].rstrip(b" ")
    pixels, events, returned = raster(arm, text)
    assert returned == len(text)
    expected = {(16 + x, 296 + y) for y in range(96) for x in range(240) if pixels[y * 240 + x]}
    image = Image.open(CAPTURE / "frame_022000_cold_boot.png").convert("RGB")
    colors = {image.getpixel(point) for point in expected}
    assert len(colors) == 1, colors
    color = next(iter(colors))
    assert max(color) < 20
    actual = {(x, y) for y in range(296, 356) for x in range(16, 220) if image.getpixel((x, y)) == color}
    assert actual == expected and len(expected) == 916
    assert len({(e["x"], e["y"]) for e in events if e["code"] != 32}) == len([e for e in events if e["code"] != 32])
    assert Image.open(CAPTURE / "frame_028400_cold_boot.png").tobytes() == Image.open(PRIOR / "frame_028400_cold_boot.png").tobytes()
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = load(file)["plaque_style_v247"]
        assert len(audit["ongoing_plaque_inventory"]) == 18 and not audit["full_plaque_audit_complete"]
        assert all(not row["fully_completed"] for row in audit["ongoing_plaque_inventory"])
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    proof = {"format": "dk4-modal-cursor-live-v271", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "code_plan": plan, "all916_actual_tutorial_ink_pixels_exact": True,
             "leading_D_and_n_and_all_other_letters_complete": True,
             "changed_text_frames": changed, "unchanged_whole_frames": unchanged,
             "occupied_item_2080_pixel_paper_composite_and_all223_glyphs_preserved": True,
             "all467_batches_records_files_routes_art_ARM7_overlays_and_prior_stages_retained": True,
             "exact_full_V270_reproduction_and_clean_patch_reconstruction": True,
             "all_stored_FE_selectors_controls_macro_bytes_prose_record_allocations_unchanged": True,
             "only_source_locked40_byte_cursor_code_block_changed": True,
             "not_all325_records_live_gameplay_verified": True,
             "all18_plaques_and_variants_incomplete": True, "experimental_user_acceptance_pending": True,
             "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"],
                      "actual_tutorial_ink_pixels": len(expected), "changed_frames": changed, "unchanged_frames": len(unchanged)}))


if __name__ == "__main__":
    main()
