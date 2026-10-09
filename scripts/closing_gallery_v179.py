"""Complete closing appreciation/title in native-size raw gallery artwork."""

import argparse
import copy
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.graphics.raw_bgr555_art import (
    BLOCK_SHA,
    FORMAT,
    FRAME_BYTES,
    apply_raw_bgr555_art,
    render_region_payload,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
PRIOR = Path("out/all_routes_combined_v178_candidate.nds")
PRIOR_SHA = "e03c0c0aee3787ff0b0813e270faadd3c7fdb6fc5ac7d62582b3fdb5e4b0778d"
PATH = "/GRP/SLACKIMG.DK4"
PROFILE = "all-routes-unified-v179"
BATCH = Path("translations/gallery_closing_raw_art_v1.json")
CANDIDATE = Path("out/all_routes_combined_v179_candidate.nds")
OUT = Path("work/qa/gallery_closing_v179")
FONT = Path("C:/Windows/Fonts/arialbd.ttf")
SPECS = [
    {"id": "DK4_GALLERY_CLOSING_APPRECIATION_V1", "box": [101, 119, 195, 141],
     "source_text": "おつかれさまでした。", "english": "Well done!", "size": 15,
     "background": 32767, "context": "Closing group portrait with warm appreciation after completion.",
     "source_meaning": "Warm appreciation for the recipient's efforts at completion.",
     "localization_note": "Natural congratulatory closing; no new claim about story facts or relationships."},
    {"id": "DK4_GALLERY_CLOSING_GAME_TITLE_V1", "box": [273, 172, 305, 188],
     "source_text": "大航海時代IV", "english": "Uncharted Waters IV", "size": 6,
     "background": 1057, "context": "Small game-title plaque within the original gold border.",
     "source_meaning": "The game's title and installment number IV.",
     "localization_note": "Established English title; automatic word wrapping within the original plaque interior."},
]


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError("Exact canonical/V178 required")
    base, prior = [NdsImage.open(p) for p in (BASE, PRIOR)]
    raw = base.read_file(PATH)
    block = IlnkContainer.parse(raw).blocks[19]
    if sha(block) != BLOCK_SHA or IlnkContainer.parse(prior.read_file(PATH)).blocks[19] != block:
        raise ValueError("Original gallery block differs")
    return base, prior, raw, block


def authored():
    _, _, _, block = sources()
    frame = block[16 * FRAME_BYTES:17 * FRAME_BYTES]
    words = struct.unpack("<76800H", frame)
    rows, cases = [], []
    for spec in SPECS:
        x0, y0, x1, y1 = spec["box"]
        source_words = [words[y * 320 + x] for y in range(y0, y1) for x in range(x0, x1)]
        raw_source = struct.pack(f"<{len(source_words)}H", *source_words)
        descriptor = dict(spec, background_rule="neutral-ink-erasure-protect-connected-art-v1")
        raw_target, evidence = render_region_payload(descriptor, raw_source,
            {"font_file_path": str(FONT), "font_sha256": sha(FONT.read_bytes())})
        rows.append(dict(descriptor, block_index=19, image_index=16, dimensions=[320, 240],
                         source_block_sha256=BLOCK_SHA, source_frame_sha256=sha(frame),
                         source_region_sha256=sha(raw_source), words_zlib_hex=zlib.compress(raw_target).hex(),
                         words_sha256=sha(raw_target), speaker="static-closing-art",
                         review={k: True for k in ("source", "context", "localization", "naturalness", "formatting")}
                         | {"visual": False, "physical_gameplay": False}))
        cases.append(dict(evidence, id=spec["id"]))
    return rows, cases


def materialize():
    _, _, source, block = sources()
    records, cases = authored()
    save(BATCH, {"format": FORMAT, "file_path": PATH, "source_file_sha256": sha(source),
                 "editorial_policy": "natural-dialogue-v2", "target_locale": "en-US",
                 "storage_layout": "reviewed-slackimg19-21x320x240-bgr555",
                 "font_file_path": str(FONT), "font_sha256": sha(FONT.read_bytes()), "records": records,
                 "limits": "Storage partition reviewed; actual native loader/geometry/palette/alpha/display/gameplay unproved."})
    # Draft visualization uses the same strict applier with temporary visual gates.
    draft = json.loads(BATCH.read_text(encoding="utf-8"))
    for row in draft["records"]:
        row["review"]["visual"] = True
    OUT.mkdir(parents=True, exist_ok=True)
    scratch = OUT / "reviewed-format-draft.json"
    save(scratch, draft)
    target, _ = apply_raw_bgr555_art(scratch, source)
    after = IlnkContainer.parse(target).blocks[19]
    canvas = Image.new("RGB", (1296, 518), "#303030")
    draw = ImageDraw.Draw(canvas)
    for col, raw in enumerate((block, after)):
        frame = raw[16 * FRAME_BYTES:17 * FRAME_BYTES]
        image = Image.new("RGB", (320, 240))
        image.putdata([bgr555(v)[:3] for v, in struct.iter_unpack("<H", frame)])
        image.save(OUT / ("original.png" if col == 0 else "english.png"))
        draw.text((col * 648 + 8, 6), "Original" if col == 0 else "English; native display pending", fill="white")
        canvas.paste(image.resize((640, 480), Image.Resampling.NEAREST), (col * 648 + 4, 28))
    canvas.save(OUT / "review.png")
    save(OUT / "evidence.json", {"cases": cases, "source_block_sha256": BLOCK_SHA,
                               "draft_target_sha256": sha(target), "visual_review": False})
    print("Prepared complete closing phrase and game-title plaque; inspect full preview.")


def register():
    if json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))["visual_review"] is not True:
        raise ValueError("Full preview review required")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    for row in batch["records"]:
        row["review"]["visual"] = True
    save(BATCH, batch)
    stack = load_release_stack()
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v178"])
    profile["batches"].append(BATCH.as_posix())
    profile.update(description="All 462 V178 batches/stages plus source-locked raw gallery closing artwork; 463 batches.",
                   note="Raw block-19 frame16 only; original framing/portraits and earlier atlas syncs retained. Native loader/display/gameplay pending; experimental.")
    stack["profiles"][PROFILE] = profile
    save(RELEASE_STACK_PATH, stack)


def verify():
    base, prior, source, original_block = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    stack = load_release_stack()
    repro = json.loads(Path("work/analysis/v178_raw_art_builder_reproduction.json").read_text(encoding="utf-8"))
    if (manifest["candidate_sha256"] != sha(CANDIDATE.read_bytes()) or manifest["base_sha256"] != CANONICAL_BASELINE_SHA256
            or manifest["profile"] != PROFILE or manifest["release_stack_sha256"] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest["batches"] != old["batches"] + [str(BATCH)] or len(manifest["batches"]) != 463
            or manifest["batches"] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest["required_batches"] != [str(p) for p in accepted_batch_paths(stack)]
            or manifest["relocations"] != old["relocations"] or not all(manifest["checks"].values())
            or repro["reproduction_sha256"] != PRIOR_SHA or sha(Path(repro["reproduction"]).read_bytes()) != PRIOR_SHA
            or repro["builder_sha256"] != sha(Path("scripts/build_integrated_release.py").read_bytes())):
        raise ValueError("Saved identity/full inheritance/reproduction differs")
    if repro["raw_art_module_sha256"] != sha(Path("dk4tool/graphics/raw_bgr555_art.py").read_bytes()):
        raise ValueError("Raw art support differs from full prior reproduction")
    before, after = [rom_files(r) for r in (prior, new)]
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != [PATH] or manifest["changed_paths"] != old["changed_paths"]:
        raise ValueError("Unexpected file delta")
    for path, ids in old["changed_records"].items():
        if manifest["changed_records"][path][:len(ids)] != ids:
            raise ValueError("Prior record IDs lost")
    expected, ids = apply_raw_bgr555_art(BATCH, source)
    wanted = IlnkContainer.parse(expected).blocks[19]
    previous_blocks, saved_blocks = [IlnkContainer.parse(r.read_file(PATH)).blocks for r in (prior, new)]
    if (saved_blocks[19] != wanted or any(a != b for i, (a, b) in enumerate(zip(previous_blocks, saved_blocks, strict=True)) if i != 19)
            or manifest["changed_records"][PATH] != old["changed_records"][PATH] + ids):
        raise ValueError("Saved artwork or earlier atlas syncs differ")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    rows, _ = authored()
    if any(row["words_sha256"] != expected_row["words_sha256"] for row, expected_row in zip(batch["records"], rows, strict=True)):
        raise ValueError("Saved complete glyph payload differs from independent authoring")
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    if sha(clean.read_bytes()) != "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d":
        raise ValueError("Wrong clean patch base")
    patch = CANDIDATE.with_suffix(".xdelta")
    reconstruction = Path("work/analysis/gallery_closing_v179_patch_reconstruction.nds")
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("Patch reconstruction differs")
    save(Path("work/analysis/gallery_closing_v179_saved_proof.json"), {
        "status": "pass-saved-v179-closing-art-and-complete-atlas-inheritance", "candidate": str(CANDIDATE),
        "candidate_sha256": sha(CANDIDATE.read_bytes()), "canonical_base_sha256": CANONICAL_BASELINE_SHA256,
        "previous_sha256": PRIOR_SHA, "profile": PROFILE, "profile_status": "experimental", "batch_count": 463,
        "candidate_arm9_sha256": sha(new.read_file("/__arm9__.bin")), "builder_sha256": repro["builder_sha256"],
        "raw_art_module_sha256": repro["raw_art_module_sha256"],
        "registry_sha256": manifest["release_stack_sha256"], "changed_paths_vs_v178": changed,
        "changed_paths_vs_canonical": manifest["changed_paths"], "source_block_sha256": sha(original_block),
        "saved_block_sha256": sha(saved_blocks[19]), "earlier_atlas_syncs_byte_exact": True,
        "patch": str(patch), "patch_bytes": patch.stat().st_size, "patch_sha256": sha(patch.read_bytes()),
        "clean_patch_base_sha256": sha(clean.read_bytes()), "patch_reconstruction_exact": True,
        "actual_native_loader_geometry_display_gameplay_verified": False})
    print("Saved exact V179 closing artwork, inherited atlas syncs and reconstructable patch.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "register", "verify"])
    globals()[parser.parse_args().action]()
