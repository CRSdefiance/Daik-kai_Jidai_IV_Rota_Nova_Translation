"""Restore an uninterpreted source mark; never infer a number from clipped art."""

import argparse
import copy
import json
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_portrait13_v177 import BASE
from scripts.audit_portrait13_v177 import CANDIDATE as PRIOR
from scripts.audit_portrait13_v177 import CANDIDATE_SHA as PRIOR_SHA
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_pxl_native_label_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for, sizing

PATH = "/evstill/evstill207.pxl"
OLD = Path("translations/village_caption_evstill207_graphics_v1.json")
BATCH = Path("translations/village_caption_evstill207_graphics_v2.json")
PROFILE = "all-routes-unified-v178"
CANDIDATE = Path("out/all_routes_combined_v178_candidate.nds")
OUT = Path("work/qa/image207_mark_v178")
PROOF = Path("work/analysis/image207_mark_v178_saved_proof.json")
PRESERVED_ROWS = 20


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError("Exact canonical and V177 required")
    base, prior = [NdsImage.open(p) for p in (BASE, PRIOR)]
    raw = base.read_file(PATH)
    if sha(raw) != "10bb77241596b7928c01ae63b4a4d27cdb76499ad5304fbbff4d3c70da9b45c4":
        raise ValueError("Wrong original image207")
    original_english, _ = apply_pxl_native_label_batch(OLD, raw, base.read_file("/__arm9__.bin"))
    if prior.read_file(PATH) != original_english:
        raise ValueError("Prior English differs from canonical-source authoring")
    return base, prior


def materialize():
    base, prior = sources()
    source = PxlImage.from_bytes(base.read_file(PATH))
    background = bytearray([255] * (256 * 192))
    background[:256 * PRESERVED_ROWS] = source.indices[:256 * PRESERVED_ROWS]
    batch = json.loads(OLD.read_text(encoding="utf-8"))
    batch.update(scope="Complete readable English caption plus exact preservation of unidentified top-edge source stroke.")
    row = batch["records"][0]
    row.update({"background_indices_zlib_hex": zlib.compress(background).hex(),
                "localization_note": row["localization_note"] + " Preserve every original pixel in rows 0 through 19. The clipped stroke is uninterpreted: no numeral, character or extra English meaning is asserted.",
                "preserved_source_region": [0, 0, 256, PRESERVED_ROWS]})
    row["review"]["visual"] = False
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(PATH), base.read_file("/__arm9__.bin"))
    evidence = preservation(target)
    OUT.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1584, 424), "#303030")
    draw = ImageDraw.Draw(canvas)
    for column, (label, raw) in enumerate((("Original", base.read_file(PATH)), ("V177", prior.read_file(PATH)), ("Preserved mark + unchanged English", target))):
        raster = PxlImage.from_bytes(raw).render().convert("RGB")
        raster.save(OUT / f"image_{column}.png")
        draw.text((column * 528 + 8, 8), label, fill="white")
        canvas.paste(raster.resize((512, 384), Image.Resampling.NEAREST), (column * 528 + 8, 30))
    canvas.save(OUT / "review.png")
    save(OUT / "evidence.json", dict(evidence, visual_review=False))
    print("Source-locked mark restored; review preview before registration.")


def preservation(target):
    base, prior = sources()
    a, b, c = [PxlImage.from_bytes(raw) for raw in (base.read_file(PATH), prior.read_file(PATH), target)]
    extent = 256 * PRESERVED_ROWS
    if (len(target) != len(a.source) or target[:a.pixels_offset] != a.source[:a.pixels_offset]
            or (c.width, c.height, c.bits_per_pixel) != (256, 192, 8)
            or c.indices[:extent] != a.indices[:extent]
            or c.indices[extent:] != b.indices[extent:]):
        raise ValueError("Clipped mark or unchanged complete English/header/palette differs")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    row = batch["records"][0]
    old = json.loads(OLD.read_text(encoding="utf-8"))
    if (row["id"] != old["records"][0]["id"] or row["text"] != old["records"][0]["text"]
            or row["box"] != old["records"][0]["box"]):
        raise ValueError("Caption meaning, identity or placement changed")
    arm9 = base.read_file("/__arm9__.bin")
    mask, _ = mask_for(arm9, batch, row)
    # Independent full native-glyph mask; the separate preserved stroke is above it.
    for y in range(PRESERVED_ROWS, 192):
        for x in range(256):
            if (c.indices[y * 256 + x] == batch["color_index"]) != bool(mask.getpixel((x, y + 2))):
                raise ValueError("Complete English glyph raster differs")
    restored = sum(v != 255 for v in a.indices[:extent])
    if not restored:
        raise ValueError("Missing original clipped source mark")
    return {"path": PATH, "preserved_source_region": [0, 0, 256, PRESERVED_ROWS],
            "preserved_nonwhite_indices": restored, "source_mark_indices_sha256": sha(bytes(a.indices[:extent])),
            "complete_english_unchanged_below_region": True, "original_header_palette_extent_exact": True,
            "interpretation": "Unknown clipped stroke retained verbatim; no number/character interpretation claimed.",
            "native_display_verified": False}


def native():
    base, prior = sources()
    arm9 = prior.read_file("/__arm9__.bin")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(PATH), arm9)
    preservation(target)
    glyph = glyph_case(arm9, dict(batch, color_index=15), batch["records"][0])
    header = sizing(arm9, target, 20, 0x024A0000, supplied_table=True)
    save(OUT / "native.json", {"status": "pass-controlled-complete-caption-glyph-and-PXL-header",
                               "arm9_source": str(PRIOR), "arm9_sha256": sha(arm9),
                               "glyph": glyph, "controlled_header": header,
                               "limits": ["Supplied resource/table and scratch glyph probes do not prove scene reachability, loading/cropping, GPU/palette/alpha or physical gameplay.",
                                          "The clipped source mark remains unidentified."]})
    print("Controlled glyph/header checks pass; actual scene usage remains open.")


def register():
    evidence = json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))
    if evidence["visual_review"] is not True or not (OUT / "native.json").exists():
        raise ValueError("Reviewed preview and controlled native evidence required")
    stack = load_release_stack()
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v177"])
    if profile["batches"].count(OLD.as_posix()) != 1:
        raise ValueError("Expected exactly one superseded source batch")
    profile["batches"] = [BATCH.as_posix() if p == OLD.as_posix() else p for p in profile["batches"]]
    profile.update(description="All V177 layers/stages retained, with image207 v1 superseded by v2 preserving its unknown clipped mark; 462 batches.",
                   note="Only source mark restoration; complete English caption unchanged. Native scene usage/display and mark meaning pending; experimental.")
    stack["profiles"][PROFILE] = profile
    save(RELEASE_STACK_PATH, stack)
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    batch["records"][0]["review"]["visual"] = True
    save(BATCH, batch)


def verify():
    base, prior = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    previous = json.loads(Path("work/analysis/online27_bubbles_v177_saved_proof.json").read_text(encoding="utf-8"))
    native_evidence = json.loads((OUT / "native.json").read_text(encoding="utf-8"))
    stack = load_release_stack()
    expected_batches = [str(BATCH) if Path(p) == OLD else p for p in old["batches"]]
    if (manifest["base_sha256"] != CANONICAL_BASELINE_SHA256 or manifest["candidate_sha256"] != sha(CANDIDATE.read_bytes())
            or manifest["profile"] != PROFILE or manifest["release_stack_sha256"] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest["batches"] != expected_batches or len(expected_batches) != 462
            or manifest["batches"] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest["required_batches"] != [str(p) for p in accepted_batch_paths(stack)]
            or manifest["changed_records"] != old["changed_records"] or manifest["relocations"] != old["relocations"]
            or not all(manifest["checks"].values())
            or sha(Path("scripts/build_integrated_release.py").read_bytes()) != previous["builder_sha256"]):
        raise ValueError("Saved identity, supersession, stages or builder differs")
    if native_evidence["arm9_sha256"] != sha(new.read_file("/__arm9__.bin")):
        raise ValueError("Controlled native code differs from candidate")
    before, after, canonical = [rom_files(r) for r in (prior, new, base)]
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if changed != [PATH] or canonical_changed != old["changed_paths"] or manifest["changed_paths"] != canonical_changed:
        raise ValueError("Unexpected previous/canonical file delta")
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(PATH), new.read_file("/__arm9__.bin"))
    if target != new.read_file(PATH):
        raise ValueError("Saved artwork differs from canonical-source batch")
    evidence = preservation(target)
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    if sha(clean.read_bytes()) != "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d":
        raise ValueError("Wrong clean base")
    patch = CANDIDATE.with_suffix(".xdelta")
    reconstruction = Path("work/analysis/image207_v178_patch_reconstruction.nds")
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("Patch reconstruction differs")
    save(PROOF, {"status": "pass-saved-v178-source-mark-preservation-and-exact-patch", "case": evidence,
                 "candidate": str(CANDIDATE), "candidate_sha256": sha(CANDIDATE.read_bytes()),
                 "canonical_base": str(BASE), "canonical_base_sha256": CANONICAL_BASELINE_SHA256,
                 "previous_sha256": PRIOR_SHA, "profile": PROFILE, "profile_status": "experimental", "batch_count": 462,
                 "superseded_batch": str(OLD), "replacement_batch": str(BATCH),
                 "candidate_arm9_sha256": sha(new.read_file("/__arm9__.bin")), "registry_sha256": manifest["release_stack_sha256"],
                 "builder_sha256": previous["builder_sha256"], "builder_unchanged": True,
                 "changed_paths_vs_v177": changed, "changed_paths_vs_canonical": canonical_changed,
                 "patch": str(patch), "patch_bytes": patch.stat().st_size, "patch_sha256": sha(patch.read_bytes()),
                 "clean_patch_base_sha256": sha(clean.read_bytes()), "patch_reconstruction_exact": True,
                 "actual_native_scene_loading_gameplay_verified": False})
    print("Saved V178 complete inheritance, one mark-only file delta and exact patch proof.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "native", "register", "verify"])
    globals()[parser.parse_args().action]()
