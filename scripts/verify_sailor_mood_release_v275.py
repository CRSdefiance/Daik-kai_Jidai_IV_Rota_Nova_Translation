"""Full V272 reproduction, inherited V275 ROM, town replay and exact patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/sailor_mood_v275")
ROM = Path("out/all_routes_combined_v275_candidate.nds")
PRIOR = Path("out/all_routes_combined_v272_candidate.nds")
CAPTURE = Path("work/emulation_v193/sailor_mood_v275")
PRIOR_CAPTURE = Path("work/emulation_v193/plaque_states_v274")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    assert (ROOT / "v272_reproduction.nds").read_bytes() == PRIOR.read_bytes()
    old, rom = NdsImage.open(PRIOR), NdsImage.open(ROM)
    before, after = old.read_file("/__arm9__.bin"), rom.read_file("/__arm9__.bin")
    assert after == (ROOT / "research_arm9.bin").read_bytes()
    assert len(before) == len(after)
    assert before[:0x1482F4] == after[:0x1482F4]
    assert before[0x1482FC:] == after[0x1482FC:]
    assert after[0x1482F4:0x1482FC] == b"Excited\0"
    assert {p: bytes(d) for _, p, d in old.iter_files()} == {p: bytes(d) for _, p, d in rom.iter_files()}
    assert old.rom.arm7 == rom.rom.arm7 and old.rom.arm9OverlayTable == rom.rom.arm9OverlayTable
    m, earlier = load(ROM.with_suffix(".manifest.json")), load(PRIOR.with_suffix(".manifest.json"))
    assert m["batches"] == earlier["batches"] and len(m["batches"]) == 467
    assert m["required_batches"] == earlier["required_batches"]
    for path, ids in earlier["changed_records"].items():
        assert set(ids) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest
    assert m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    stage = m["relocations"]["/__arm9__.bin"]["sailor_mood_caption"]
    assert stage["release_config_sha256"] == sha(Path(stage["release_config"]).read_bytes())
    old_report, report = load(PRIOR_CAPTURE / "capture_report.json"), load(CAPTURE / "capture_report.json")
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and report["frames"] == old_report["frames"] == 32200
    assert report["scripted_input_schedule"] == old_report["scripted_input_schedule"]
    lookup = {r["frame"]: r for r in report["frames_captured"]}
    compared = set()
    for row in old_report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        current = lookup[row["frame"]]
        assert sha(Path(current["path"]).read_bytes()) == current["PNG_sha256"]
        assert Image.open(row["path"]).tobytes() == Image.open(current["path"]).tobytes(), row["frame"]
        compared.add(row["frame"])
    for file in ["graphics_completion_campaign_v1.json", "graphics_visual_audit_v150.json"]:
        audit = load(Path("translations") / file)
        plaque = audit["plaque_style_v247"]
        assert len(plaque["ongoing_plaque_inventory"]) == 18 and not plaque["full_plaque_audit_complete"]
        assert all(not row["fully_completed"] for row in plaque["ongoing_plaque_inventory"])
        assert audit["user_scope_exceptions"]["low_resolution_online_images"]["translation_required"] is False
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    native = load(ROOT / "native_proof.json")
    assert native["plan"]["target_arm9_sha256"] == sha(after)
    proof = {"format": "dk4-sailor-mood-release-v275", "candidate": str(ROM),
             "candidate_sha256": digest, "patch_sha256": sha(patch.read_bytes()),
             "profile": m["profile"], "base_sha256": m["base_sha256"],
             "all467_batches_required_layers_prior_records_and_files_preserved": True,
             "all_native_code_and_other_strings_unchanged_only_original8byte_label_slot_changed": True,
             "exact_full_V272_reproduction_and_clean_patch_reconstruction": True,
             "cold_boot_frames": 32200, "unchanged_whole_frames": sorted(compared),
             "all13_native_status_glyphs_and_other12_rasters_verified": True,
             "actual_excited_gameplay_display_pending": True,
             "all18_plaque_hint_entries_and_variants_remain_incomplete": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_release_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"],
                      "unchanged_whole_frames": len(compared), "Excited_ink_pixels": native["Excited_complete_ink_pixels"]}))


if __name__ == "__main__":
    main()
