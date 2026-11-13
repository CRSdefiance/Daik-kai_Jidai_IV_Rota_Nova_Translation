"""Verify complete repaired captions, all prior pixels and exact combined patch."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.frame_buttons_v165 import atlas_indices

ROOT = Path("work/analysis/radial_marker_v245")
ROM = Path("out/all_routes_combined_v245_candidate.nds")
PRIOR = Path("out/all_routes_combined_v241_candidate.nds")


def main():
    assert sha(PRIOR.read_bytes()) == "d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027"
    before, after = NdsImage.open(PRIOR), NdsImage.open(ROM)
    old_files = {p: bytes(d) for _, p, d in before.iter_files()}
    new_files = {p: bytes(d) for _, p, d in after.iter_files()}
    changed = sorted(p for p in old_files if old_files[p] != new_files[p])
    assert changed == ["/GRP/CMMNIMG.DK4", "/_pxl/__marker.pxl"]
    assert before.read_file("/__arm9__.bin") == after.read_file("/__arm9__.bin")
    assert before.rom.arm7 == after.rom.arm7
    marker = PxlImage.from_bytes(after.read_file("/_pxl/__marker.pxl"))
    old = PxlImage.from_bytes(before.read_file("/_pxl/__marker.pxl"))
    assert marker.source == (ROOT / "target_marker.pxl").read_bytes()
    assert marker.source[:marker.pixels_offset] == old.source[:old.pixels_offset]
    assert len(marker.source) == len(old.source)
    batch = json.loads(Path("translations/radial_marker_caption_repair_v1.json").read_text(encoding="utf-8"))
    font = GameAsciiFont.from_arm9(after.read_file("/__arm9__.bin"))
    owned, glyphs = set(), []
    for record in batch["records"]:
        left, top, right, bottom = record["box"]
        owned.update(y * 256 + x for y in range(top, bottom) for x in range(left, right))
        text = record["text"]
        x0 = left + (right - left - 5 * len(text)) // 2
        y0 = top + (bottom - top - 11) // 2
        ink = set()
        for n, ch in enumerate(text):
            g = font.decode(ch)
            for y in range(11):
                for x in range(6):
                    if g.getpixel((x, y)):
                        assert x < 5
                        ink.add((x0 + 5*n + x, y0 + y))
        for y in range(top, bottom):
            for x in range(left, right):
                assert (marker.indices[y * 256 + x] == 15) == ((x, y) in ink)
        glyphs.append({"text": text, "complete_native_font_ink_pixels": len(ink),
                       "complete_erase_box_has_only_reviewed_English_foreground": True,
                       "first_last_letters_internal_spaces_and_bounds_pass": True})
    assert all(marker.indices[n] == old.indices[n] for n in range(65536) if n not in owned)
    previous_archive = IlnkContainer.parse(before.read_file("/GRP/CMMNIMG.DK4"))
    archive = IlnkContainer.parse(after.read_file("/GRP/CMMNIMG.DK4"))
    assert len(previous_archive.blocks) == len(archive.blocks)
    assert len(before.read_file("/GRP/CMMNIMG.DK4")) == len(after.read_file("/GRP/CMMNIMG.DK4"))
    for n, (a, b) in enumerate(zip(previous_archive.blocks, archive.blocks, strict=True)):
        assert a[:20] == b[:20]
        if n != 5:
            assert a == b
    first, second = atlas_indices(before.read_file("/GRP/CMMNIMG.DK4")), atlas_indices(after.read_file("/GRP/CMMNIMG.DK4"))
    for y in range(256):
        assert second[y * 512:y * 512 + 256] == marker.indices[y * 256:(y + 1) * 256]
        assert second[y * 512 + 256:(y + 1) * 512] == first[y * 512 + 256:(y + 1) * 512]
    manifest = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    previous = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    replacements = {"translations/marker_gender_graphics_v1.json": "translations/marker_gender_and_radial_graphics_v2.json",
                    "translations/marker_cmmnimg_sync_v2.json": "translations/marker_cmmnimg_sync_v3.json"}
    normalize = lambda s: s.replace("\\", "/")
    expected = [replacements.get(normalize(s), normalize(s)) for s in previous["batches"]]
    assert [normalize(s) for s in manifest["batches"]] == expected and len(expected) == 467
    assert manifest["required_batches"] == previous["required_batches"]
    for path, records in previous["changed_records"].items():
        assert set(records) <= set(manifest["changed_records"][path])
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["candidate_sha256"] == sha(ROM.read_bytes())
    patch, rebuilt = ROM.with_suffix(".xdelta"), ROOT / "exact_patch_reconstruction.nds"
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    proof = {"format": "dk4-radial-marker-combined-release-proof-v245", "candidate": str(ROM),
             "candidate_sha256": sha(ROM.read_bytes()), "patch": str(patch), "patch_sha256": sha(patch.read_bytes()),
             "manifest_sha256": sha(ROM.with_suffix(".manifest.json").read_bytes()),
             "profile": manifest["profile"], "canonical_base_sha256": manifest["base_sha256"],
             "changed_internal_files_vs_V241": changed, "complete_caption_glyphs": glyphs,
             "no_original_Japanese_foreground_fragments_in_six_repaired_boxes": True,
             "all_other_marker_pixels_two_gender_cells_and83_palette_banks_exact": True,
             "embedded_copy_exact_frame_half_all_headers_palettes_other_blocks_preserved": True,
             "all_467_batches_prior_records_required_layers_and_terminal_stages_retained": True,
             "ARM9_ARM7_and_all_other_ROM_files_unchanged": True, "exact_patch_reconstruction": True,
             "one_hidden_background_pixel_per_plate_inferred_not_original_recovery": True,
             "cold_boot_display_pending": True, "experimental_user_acceptance_pending": True,
             "full_goal_complete": False}
    (ROOT / "saved_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": proof["candidate_sha256"], "patch_sha256": proof["patch_sha256"],
                      "complete_captions_verified": len(glyphs), "changed_paths": changed,
                      "prior_art_code_and_exact_patch_pass": True}))


if __name__ == "__main__":
    main()
