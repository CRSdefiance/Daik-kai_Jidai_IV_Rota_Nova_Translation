"""Maria Mode and player thanks, preserving the painted creator credits."""

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
from scripts.closing_gallery_v179 import BASE
from scripts.closing_gallery_v179 import BATCH as OLD
from scripts.fleet_row_graphics_v162 import save

PATH = "/GRP/SLACKIMG.DK4"
PRIOR = Path("out/all_routes_combined_v179_candidate.nds")
PRIOR_SHA = "9187eae3b0fe2c0187d84d678611ae03014244a0f0ed9f22c2b4a6a3b13f76ad"
PROFILE = "all-routes-unified-v180"
CANDIDATE = Path("out/all_routes_combined_v180_candidate.nds")
BATCH = Path("translations/gallery_closing_maria_raw_art_v2.json")
OUT = Path("work/qa/maria_gallery_v180")
PROOF = Path("work/analysis/maria_gallery_v180_saved_proof.json")
DECISIONS = Path("translations/gallery_maria_creator_marks_v180.json")
REPRO = Path("work/analysis/v179_maria_builder_reproduction.json")
SPECS = [
    {"id": "DK4_GALLERY_MARIA_MODE_V1", "box": [269, 36, 307, 199],
     "source_text": "まりあもーど", "english": "Maria Mode", "size": 17,
     "background": 30686, "ink_word": 0, "rotation": -90,
     "context": "Decorative vertical Maria Mode label beside a Maria portrait and painted creator credit.",
     "source_meaning": "Maria Mode heading.",
     "localization_note": "Established Maria spelling; the complete English title rotates clockwise within the original vertical strip, preserving the adjacent creator mark."},
    {"id": "DK4_GALLERY_PLAYING_THANKS_V1", "box": [0, 214, 280, 240],
     "source_text": "さいごまでプレイしてくれて、ありがとうございます…",
     "english": "Thanks for playing all the way through...", "size": 10,
     "background": 0, "ink_word": 32767,
     "context": "Painted closing message thanking the player for playing to the end; creator credit follows at the right.",
     "source_meaning": "Thanks the player for playing to the end.",
     "localization_note": "Natural American English gratitude; preserve the trailing pause and the original painted attribution."},
]
CREATOR_REGIONS = [[239, 91, 267, 199], [280, 211, 320, 240]]


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError("Exact canonical/V179 required")
    base, prior = [NdsImage.open(p) for p in (BASE, PRIOR)]
    source = base.read_file(PATH)
    a, b = [IlnkContainer.parse(r.read_file(PATH)).blocks[19] for r in (base, prior)]
    if sha(a) != BLOCK_SHA or a[13 * FRAME_BYTES:14 * FRAME_BYTES] != b[13 * FRAME_BYTES:14 * FRAME_BYTES]:
        raise ValueError("Unchanged original Maria image required")
    old_art, _ = apply_raw_bgr555_art(OLD, source)
    if IlnkContainer.parse(old_art).blocks[19] != b:
        raise ValueError("Earlier closing artwork is not exact")
    return base, prior, source, a


def region_bytes(frame, box):
    x0, y0, x1, y1 = box
    return b"".join(frame[(y * 320 + x0) * 2:(y * 320 + x1) * 2] for y in range(y0, y1))


def authored():
    _, _, _, block = sources()
    old = json.loads(OLD.read_text(encoding="utf-8"))
    records = copy.deepcopy(old["records"])
    cases = []
    frame = block[13 * FRAME_BYTES:14 * FRAME_BYTES]
    for spec in SPECS:
        source_region = region_bytes(frame, spec["box"])
        row = dict(spec, background_rule="background-aware-connected-art-v2")
        target_region, evidence = render_region_payload(row, source_region, old)
        records.append(dict(row, block_index=19, image_index=13, dimensions=[320, 240],
                            source_block_sha256=BLOCK_SHA, source_frame_sha256=sha(frame),
                            source_region_sha256=sha(source_region), words_zlib_hex=zlib.compress(target_region).hex(),
                            words_sha256=sha(target_region), speaker="static-portrait-closing-art",
                            review={k: True for k in ("source", "context", "localization", "naturalness", "formatting")}
                            | {"visual": False, "physical_gameplay": False}))
        cases.append(dict(evidence, id=spec["id"]))
    return records, cases


def preservation(target):
    _, prior, _, _ = sources()
    previous, current = [IlnkContainer.parse(r).blocks for r in (prior.read_file(PATH), target)]
    if len(target) != len(prior.read_file(PATH)) or any(a != b for i, (a, b) in enumerate(zip(previous, current, strict=True)) if i != 19):
        raise ValueError("Previous atlas blocks/allocation changed")
    a, b = [raw[13 * FRAME_BYTES:14 * FRAME_BYTES] for raw in (previous[19], current[19])]
    if previous[19][:13 * FRAME_BYTES] != current[19][:13 * FRAME_BYTES] or previous[19][14 * FRAME_BYTES:] != current[19][14 * FRAME_BYTES:]:
        raise ValueError("Other gallery frames changed")
    owned = set()
    for spec in SPECS:
        x0, y0, x1, y1 = spec["box"]
        owned.update((y * 320 + x) * 2 + c for y in range(y0, y1) for x in range(x0, x1) for c in (0, 1))
    if any(x != y for i, (x, y) in enumerate(zip(a, b, strict=True)) if i not in owned):
        raise ValueError("Unowned picture/creator pixels changed")
    for box in CREATOR_REGIONS:
        if region_bytes(a, box) != region_bytes(b, box):
            raise ValueError("Painted creator mark changed")
    return {"other_frames_and_prior_atlas_syncs_byte_exact": True,
            "creator_regions": [{"box": box, "source_region_sha256": sha(region_bytes(a, box)), "byte_exact": True} for box in CREATOR_REGIONS],
            "scope": "Maria heading and readable player-thanks sentence only; original creator marks retained without invented romanized identity.",
            "native_display_verified": False}


def materialize():
    _, prior, source, _ = sources()
    records, cases = authored()
    batch = json.loads(OLD.read_text(encoding="utf-8"))
    batch["records"] = records
    batch["limits"] = "Cumulative canonical-source gallery closing/Maria artwork. Native partition/loader/display/gameplay remain unproved."
    save(BATCH, batch)
    draft = copy.deepcopy(batch)
    for row in draft["records"]:
        row["review"]["visual"] = True
    OUT.mkdir(parents=True, exist_ok=True)
    scratch = OUT / "reviewed-format-draft.json"
    save(scratch, draft)
    raw_target, _ = apply_raw_bgr555_art(scratch, source)
    target = IlnkContainer.parse(prior.read_file(PATH))
    target.blocks[19] = IlnkContainer.parse(raw_target).blocks[19]
    evidence = preservation(target.to_bytes())
    canvas = Image.new("RGB", (1296, 518), "#303030")
    draw = ImageDraw.Draw(canvas)
    for col, block in enumerate((IlnkContainer.parse(source).blocks[19], target.blocks[19])):
        frame = block[13 * FRAME_BYTES:14 * FRAME_BYTES]
        raster = Image.new("RGB", (320, 240))
        raster.putdata([bgr555(v)[:3] for v, in struct.iter_unpack("<H", frame)])
        raster.save(OUT / ("original.png" if col == 0 else "english.png"))
        draw.text((col * 648 + 8, 6), "Original" if col == 0 else "English; native display pending", fill="white")
        canvas.paste(raster.resize((640, 480), Image.Resampling.NEAREST), (col * 648 + 4, 28))
    canvas.save(OUT / "review.png")
    save(OUT / "evidence.json", dict(evidence, cases=cases, visual_review=False))
    print("Prepared Maria heading and player-thanks message; inspect complete source/candidate comparison.")


def register():
    if json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))["visual_review"] is not True:
        raise ValueError("Complete preview review required")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    old = json.loads(OLD.read_text(encoding="utf-8"))
    if batch["records"][:len(old["records"])] != old["records"]:
        raise ValueError("Inherited closing records changed")
    for row in batch["records"]:
        row["review"]["visual"] = True
    save(BATCH, batch)
    stack = load_release_stack()
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v179"])
    if profile["batches"].count(OLD.as_posix()) != 1:
        raise ValueError("Expected one raw-art source batch")
    profile["batches"] = [BATCH.as_posix() if p == OLD.as_posix() else p for p in profile["batches"]]
    profile.update(description="All V179 layers/stages preserved; raw gallery v1 superseded by cumulative v2 with complete Maria heading/thanks. 463 batches.",
                   note="Frame16 exact; frame13 heading and player-thanks only. Creator marks/unowned art/earlier atlas syncs preserved. Actual native display/gameplay pending; experimental.")
    stack["profiles"][PROFILE] = profile
    save(RELEASE_STACK_PATH, stack)


def verify():
    base, prior, source, _ = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    repro = json.loads(REPRO.read_text(encoding="utf-8"))
    stack = load_release_stack()
    expected_batches = [str(BATCH) if Path(p) == OLD else p for p in old["batches"]]
    if (manifest["candidate_sha256"] != sha(CANDIDATE.read_bytes()) or manifest["base_sha256"] != CANONICAL_BASELINE_SHA256
            or manifest["profile"] != PROFILE or manifest["release_stack_sha256"] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest["batches"] != expected_batches or len(expected_batches) != 463
            or manifest["batches"] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest["required_batches"] != [str(p) for p in accepted_batch_paths(stack)]
            or manifest["relocations"] != old["relocations"] or not all(manifest["checks"].values())
            or repro["reproduction_sha256"] != PRIOR_SHA or sha(Path(repro["reproduction"]).read_bytes()) != PRIOR_SHA
            or repro["builder_sha256"] != sha(Path("scripts/build_integrated_release.py").read_bytes())
            or repro["raw_art_module_sha256"] != sha(Path("dk4tool/graphics/raw_bgr555_art.py").read_bytes())):
        raise ValueError("Saved identity/full stack/reproduction differs")
    before, after = [rom_files(r) for r in (prior, new)]
    if sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p)) != [PATH] or manifest["changed_paths"] != old["changed_paths"]:
        raise ValueError("Unexpected file delta")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    records, _ = authored()
    if any(a["words_sha256"] != b["words_sha256"] for a, b in zip(batch["records"], records, strict=True)):
        raise ValueError("Full English payload differs")
    expected, ids = apply_raw_bgr555_art(BATCH, source)
    if IlnkContainer.parse(new.read_file(PATH)).blocks[19] != IlnkContainer.parse(expected).blocks[19]:
        raise ValueError("Saved gallery artwork differs")
    for path, previous_ids in old["changed_records"].items():
        if manifest["changed_records"][path][:len(previous_ids)] != previous_ids:
            raise ValueError("Prior record IDs lost")
    if manifest["changed_records"][PATH] != old["changed_records"][PATH] + ids[2:]:
        raise ValueError("New record IDs differ")
    evidence = preservation(new.read_file(PATH))
    save(DECISIONS, {
        "format": "dk4-gallery-creator-mark-decisions-v1",
        "canonical_source_sha256": CANONICAL_BASELINE_SHA256,
        "source_path": PATH, "block_index": 19, "image_index": 13,
        "source_block_sha256": BLOCK_SHA, "source_partition_native_proved": False,
        "source_preview": str(OUT / "original.png"),
        "visual_review": "full-source-English-comparison-and-footer-boundary-enlargement-reviewed",
        "decision": "retain-original-painted-creator-credit-marks",
        "observation": "Both painted kana marks follow the explicit Latin by credit in the artwork.",
        "reason": "Preserve source creator attribution styling, consistent with neighboring signed paintings. Readable heading and player-thanks sentence are localized separately.",
        "interpretation_limit": "Do not invent a romanized name/identity from the painted kana; no story or menu text is retained by this decision.",
        "regions": evidence["creator_regions"],
        "candidate": str(CANDIDATE), "candidate_sha256": sha(CANDIDATE.read_bytes()),
        "actual_native_usage_verified": False,
    })
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    if sha(clean.read_bytes()) != "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d":
        raise ValueError("Wrong clean base")
    patch = CANDIDATE.with_suffix(".xdelta")
    reconstruction = Path("work/analysis/maria_v180_patch_reconstruction.nds")
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("Patch reconstruction differs")
    save(PROOF, dict(evidence, status="pass-saved-v180-Maria-heading-thanks-and-complete-inheritance",
                     candidate=str(CANDIDATE), candidate_sha256=sha(CANDIDATE.read_bytes()), canonical_base_sha256=CANONICAL_BASELINE_SHA256,
                     previous_sha256=PRIOR_SHA, profile=PROFILE, profile_status="experimental", batch_count=463,
                     candidate_arm9_sha256=sha(new.read_file("/__arm9__.bin")), registry_sha256=manifest["release_stack_sha256"],
                     builder_sha256=repro["builder_sha256"], raw_art_module_sha256=repro["raw_art_module_sha256"],
                     changed_paths_vs_v179=[PATH], changed_paths_vs_canonical=manifest["changed_paths"],
                     superseded_batch=str(OLD), replacement_batch=str(BATCH),
                     patch=str(patch), patch_bytes=patch.stat().st_size, patch_sha256=sha(patch.read_bytes()),
                     clean_patch_base_sha256=sha(clean.read_bytes()), patch_reconstruction_exact=True,
                     creator_decisions=str(DECISIONS),
                     actual_native_loading_gameplay_verified=False))
    print("Saved exact V180 heading/thanks, original creator marks, inherited atlas/frame16 and patch.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "register", "verify"])
    globals()[parser.parse_args().action]()
