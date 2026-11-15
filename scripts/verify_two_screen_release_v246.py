"""Verify the combined two-screen candidate preserves the complete prior stack."""

import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/two_screen_layout_v246")
ROM = Path("out/all_routes_combined_v246_candidate.nds")
PRIOR = Path("out/all_routes_combined_v245_candidate.nds")


def main():
    assert sha(PRIOR.read_bytes()) == "57b7f42f04f60c5e6f06d03ebe91eacbaff04204dde27967fd3e3b205634d3c4"
    assert (ROOT / "v245_reproduction.nds").read_bytes() == PRIOR.read_bytes()
    before, after = NdsImage.open(PRIOR), NdsImage.open(ROM)
    old = {p: bytes(d) for _,p,d in before.iter_files()}
    new = {p: bytes(d) for _,p,d in after.iter_files()}
    changed = sorted(p for p in old if old[p] != new[p])
    assert changed == ["/_pxl/dividecrewinfo.pxl", "/_pxl/personinfo.pxl"]
    assert after.read_file("/__arm9__.bin") == (ROOT / "research_arm9.bin").read_bytes()
    assert before.rom.arm7 == after.rom.arm7
    assert before.rom.arm9OverlayTable == after.rom.arm9OverlayTable
    for name,path in [("crew","/_pxl/dividecrewinfo.pxl"),("person","/_pxl/personinfo.pxl")]:
        p, q = PxlImage.from_bytes(old[path]), PxlImage.from_bytes(new[path])
        assert q.source == (ROOT / (name+"_target.pxl")).read_bytes()
        assert p.source[:p.pixels_offset] == q.source[:q.pixels_offset]
        assert len(p.source) == len(q.source)
    previous = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    manifest = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    swaps = {"translations/assign_sailors_graphics_v3.json":"translations/assign_sailors_graphics_v4.json",
             "translations/person_info_graphics_v1.json":"translations/person_info_graphics_v2.json"}
    norm = lambda s: s.replace("\\","/")
    expected = [swaps.get(norm(s),norm(s)) for s in previous["batches"]]
    assert [norm(s) for s in manifest["batches"]] == expected and len(expected) == 467
    assert manifest["required_batches"] == previous["required_batches"]
    for p, ids in previous["changed_records"].items():
        assert set(ids) <= set(manifest["changed_records"][p])
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["candidate_sha256"] == sha(ROM.read_bytes())
    patch = ROM.with_suffix(".xdelta")
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    rebuilt = ROOT / "exact_patch_reconstruction.nds"
    make_xdelta(clean,ROM,patch)
    apply_xdelta(clean,patch,rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    proof = {"format":"dk4-two-screen-combined-release-v246","candidate":str(ROM),
             "candidate_sha256":sha(ROM.read_bytes()),"patch":str(patch),"patch_sha256":sha(patch.read_bytes()),
             "manifest_sha256":sha(ROM.with_suffix(".manifest.json").read_bytes()),
             "profile":manifest["profile"],"canonical_base_sha256":manifest["base_sha256"],
             "changed_components_vs_V245":["/__arm9__.bin",*changed],
             "all_467_prior_batches_records_required_layers_and_terminal_stages_retained":True,
             "complete_V245_reproduction_after_builder_change_exact":True,
             "all_routes_other_graphics_ARM7_and_original_overlay_unchanged":True,
             "both_PXL_headers_palettes_dimensions_extents_preserved":True,
             "exact_clean_patch_reconstruction":True,"cold_boot_both_screens_pending":True,
             "experimental_user_acceptance_pending":True,"full_goal_complete":False}
    (ROOT / "saved_proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"candidate_sha256":proof["candidate_sha256"],"patch_sha256":proof["patch_sha256"],
                      "full_inheritance_and_exact_patch_pass":True}))


if __name__ == "__main__":
    main()
