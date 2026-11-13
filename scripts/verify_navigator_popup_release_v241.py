"""Verify complete inheritance, two bounded string changes and exact patch."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.navigator_selection_menu import SPECS, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/navigator_popup_v241")
PRIOR = Path("out/all_routes_combined_v218_candidate.nds")
ROM = Path("out/all_routes_combined_v241_candidate.nds")


def main():
    before_raw, after_raw = PRIOR.read_bytes(), ROM.read_bytes()
    assert sha(before_raw) == "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"
    assert (ROOT / "v218_builder_reproduction.nds").read_bytes() == before_raw
    before, after = NdsImage.open(PRIOR), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in before.iter_files()} == {p: bytes(d) for _, p, d in after.iter_files()}
    assert before.rom.arm7 == after.rom.arm7
    assert before.rom.arm9OverlayTable == after.rom.arm9OverlayTable
    assert before.rom.arm7OverlayTable == after.rom.arm7OverlayTable
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    expected, report = apply_release(before.read_file("/__arm9__.bin"), canonical.read_file("/__arm9__.bin"),
                                     "translations/navigator_selection_menu_release_v1.json")
    assert after.read_file("/__arm9__.bin") == expected
    arm9_file_offset = struct.unpack_from("<I", before_raw, 0x20)[0]
    allowed = {arm9_file_offset + off + n for _, off, _, _, size in SPECS for n in range(size)}
    assert len(before_raw) == len(after_raw)
    diff = [n for n, (a, b) in enumerate(zip(before_raw, after_raw, strict=True)) if a != b]
    assert diff and set(diff) <= allowed
    manifest = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert manifest["profile"] == "all-routes-unified-v241"
    assert manifest["batches"] == old["batches"] and len(manifest["batches"]) == 467
    assert manifest["required_batches"] == old["required_batches"]
    assert manifest["base_sha256"] == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert manifest["candidate_sha256"] == sha(after_raw)
    assert manifest["release_stack_sha256"] == sha(Path(manifest["release_stack"]).read_bytes())
    for path, records in old["changed_records"].items():
        assert set(records) <= set(manifest["changed_records"][path])
    for key, _, _, _, _ in SPECS:
        assert key in manifest["changed_records"]["/__arm9__.bin"]
    clean, patch, rebuilt = Path("work/clean.nds"), ROM.with_suffix(".xdelta"), ROOT / "exact_patch_reconstruction.nds"
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == after_raw
    proof = {"format": "dk4-navigator-popup-release-proof-v241", "candidate": str(ROM),
             "candidate_sha256": sha(after_raw), "patch": str(patch), "patch_sha256": sha(patch.read_bytes()),
             "manifest_sha256": sha(ROM.with_suffix(".manifest.json").read_bytes()),
             "profile": manifest["profile"], "canonical_base_sha256": manifest["base_sha256"],
             "all_467_inherited_batches_required_layers_and_changed_records_preserved": True,
             "V218_builder_reproduction_exact": True, "complete_ROM_bytes_changed": len(diff),
             "ROM_byte_changes_only_inside_two_original_string_slots": True,
             "all_internal_files_ARM7_overlays_and_runtime_code_unchanged": True,
             "patch_reconstruction_exact": True, "plan": report,
             "cold_boot_display_pending": True, "experimental_user_acceptance_pending": True,
             "full_goal_complete": False}
    (ROOT / "saved_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": proof["candidate_sha256"], "patch_sha256": proof["patch_sha256"],
                      "ROM_bytes_changed": len(diff), "full_inheritance_and_exact_patch_pass": True}))


if __name__ == "__main__":
    main()
