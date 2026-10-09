"""Verify the complete registered stack and exact clean-ROM patch reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sailing_no_target import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/no_target_v218")
CANDIDATE = Path("out/all_routes_combined_v218_candidate.nds")


def main():
    previous_path = Path("out/all_routes_combined_v217_candidate.nds")
    previous, candidate = NdsImage.open(previous_path), NdsImage.open(CANDIDATE)
    previous_sha = "124588d04ad361b505e1eccb1b05aa422ad5e919771d1faf4be256cd734b713e"
    assert sha(previous_path.read_bytes()) == previous_sha
    assert sha((Path("work/analysis/no_target_v218/v217_builder_reproduction.nds")).read_bytes()) == previous_sha
    before = {p: bytes(v) for _, p, v in previous.iter_files()}
    after = {p: bytes(v) for _, p, v in candidate.iter_files()}
    assert before == after and previous.rom.arm7 == candidate.rom.arm7
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    expected, plan = apply_release(previous.read_file("/__arm9__.bin"), canonical.read_file("/__arm9__.bin"),
                                   "translations/sailing_no_target_release_v1.json")
    assert candidate.read_file("/__arm9__.bin") == expected
    manifest = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    older = json.loads(previous_path.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert manifest["profile"] == "all-routes-unified-v218"
    assert manifest["base_sha256"] == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert manifest["batches"] == older["batches"] and len(manifest["batches"]) == 467
    assert manifest["required_batches"] == older["required_batches"]
    assert manifest["release_stack_sha256"] == sha(Path(manifest["release_stack"]).read_bytes())
    terminal = manifest["relocations"]["/__arm9__.bin"]["sailing_no_target"]
    assert terminal["release_config_sha256"] == sha(Path(terminal["release_config"]).read_bytes())
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = CANDIDATE.with_suffix(".xdelta")
    rebuilt = ROOT / "exact_clean_patch_reconstruction.nds"
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == CANDIDATE.read_bytes()
    proof = {"format": "dk4-sailing-no-target-registered-release-proof-v1",
             "candidate": CANDIDATE.as_posix(), "candidate_sha256": sha(CANDIDATE.read_bytes()),
             "profile": manifest["profile"], "base_sha256": manifest["base_sha256"],
             "all_467_inherited_batches_and_required_layers_retained": True,
             "full_V217_reproduction_after_shared_builder_change_exact": True,
             "only_changed_component_vs_V217": "/__arm9__.bin",
             "all_existing_internal_files_ARM7_and_original_overlay_identical": True,
             "plan": plan, "patch": patch.as_posix(), "patch_sha256": sha(patch.read_bytes()),
             "clean_source_sha256": sha(clean.read_bytes()), "patch_reconstruction_exact": True,
             "cold_boot_pixel_proof": "work/analysis/no_target_v218/live_pixels.json",
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": proof["candidate_sha256"], "patch_sha256": proof["patch_sha256"],
                      "inherited_batches": 467, "all_files_and_ARM7_preserved": True, "patch_reconstruction_exact": True}))


if __name__ == "__main__":
    main()
