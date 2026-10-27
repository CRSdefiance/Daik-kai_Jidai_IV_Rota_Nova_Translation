"""Reference-only BGR555 hypothesis for all SLACKIMG block-19 source words."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_portrait13_v177 import BASE, CANDIDATE, CANDIDATE_SHA
from scripts.build_integrated_release import CANONICAL_BASELINE_SHA256

OUT = Path("work/qa/embedded_raw_v177/sketch19")
OBSERVATIONS = {
    4: "Japanese recruitment chapter title and creator credits.",
    5: "Japanese comic dialogue, vocal call and large exclamation.",
    6: "Question-mark balloon and small kana sound effects beside character.",
    7: "Large Japanese splash sound effect and small exclamations.",
    8: "Japanese identity question and creature's hiragana reply.",
    10: "Japanese end caption over dimmed scene.",
    11: "Chinese speech balloon plus Japanese Maria Mode title.",
    12: "Japanese Maria Mode title and large reveal sound effect.",
    13: "Japanese Maria Mode title, creator signature and playing-thanks sentence.",
    16: "Japanese closing appreciation and small game-title logo.",
    18: "Small handwritten kana artist signature; exact name unresolved.",
    19: "Small handwritten kana artist signature; exact name unresolved.",
}


def prepare():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError("Exact canonical and V177 required")
    base, current = [NdsImage.open(p) for p in (BASE, CANDIDATE)]
    source = IlnkContainer.parse(base.read_file("/GRP/SLACKIMG.DK4")).blocks[19]
    saved = IlnkContainer.parse(current.read_file("/GRP/SLACKIMG.DK4")).blocks[19]
    if source != saved or len(source) != 21 * 320 * 240 * 2:
        raise ValueError("Unexpected raw source extent/change")
    historical = json.loads(Path("work/analysis/embedded_graphics_v151/inventory.json").read_text(encoding="utf-8"))
    row = next(r for r in historical["blocks"] if r["path"] == "/GRP/SLACKIMG.DK4" and r["block_index"] == 19)
    if sha(source) != row["block_sha256"]:
        raise ValueError("Historical source block lock differs")
    OUT.mkdir(parents=True, exist_ok=True)
    rows, images = [], []
    reconstructed = bytearray()
    for index in range(21):
        offset = index * 153600
        raw = source[offset:offset + 153600]
        words = [v for v, in struct.iter_unpack("<H", raw)]
        if any(v & 0x8000 for v in words):
            raise ValueError("Unexpected high color bits")
        pixels = bytes(channel for v in words for channel in bgr555(v)[:3])
        image = Image.frombytes("RGB", (320, 240), pixels)
        path = OUT / f"sketch_{index:02d}.png"
        image.save(path)
        if Image.open(path).tobytes() != pixels:
            raise ValueError("Saved sketch preview differs")
        reconstructed.extend(struct.pack("<76800H", *words))
        images.append(image)
        rows.append({"index": index, "raw_offset": offset, "raw_bytes": len(raw),
                     "raw_sha256": sha(raw), "preview": str(path), "preview_sha256": sha(path.read_bytes()),
                     "visual_review": "pending", "native_geometry_proved": False})
    if bytes(reconstructed) != source:
        raise ValueError("Whole block word roundtrip differs")
    sheets = []
    for start in range(0, 21, 6):
        canvas = Image.new("RGB", (984, 536), "#303030")
        draw = ImageDraw.Draw(canvas)
        for slot, image in enumerate(images[start:start + 6]):
            x, y = (slot % 3) * 328 + 4, (slot // 3) * 268
            draw.text((x, y + 3), f"Raw19 sketch candidate {start + slot}", fill="white")
            canvas.paste(image, (x, y + 24))
        path = OUT / f"sheet_{start // 6}.png"
        canvas.save(path)
        sheets.append({"path": str(path), "sha256": sha(path.read_bytes()),
                       "indices": list(range(start, min(start + 6, 21))), "visual_review": "pending"})
    report = {"path": "/GRP/SLACKIMG.DK4", "block_index": 19,
              "canonical_source_sha256": CANONICAL_BASELINE_SHA256,
              "source_block_sha256": sha(source), "candidate": str(CANDIDATE), "candidate_sha256": CANDIDATE_SHA,
              "original_block_byte_exact_in_v177": True,
              "whole_block_words_consumed": True, "RGB555_roundtrip_exact": True,
              "hypothesis_dimensions": [320, 240], "records": rows, "sheets": sheets,
              "limits": ["Geometry/encoding are hypotheses until native metadata or a mapped loader proves them.",
                         "Source storage review does not prove native palette/alpha/crops, display or archive-wide clearance."]}
    (OUT / "inventory.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Prepared all 21 block-19 full-size reference previews; visual review pending.")


def record_review():
    report_path = OUT / "inventory.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report["candidate_sha256"] != CANDIDATE_SHA or len(report["records"]) != 21:
        raise ValueError("Prepared inventory differs")
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError("Reviewed candidate identity differs")
    source = IlnkContainer.parse(NdsImage.open(BASE).read_file("/GRP/SLACKIMG.DK4")).blocks[19]
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(source) != report["source_block_sha256"]:
        raise ValueError("Reviewed source identity differs")
    for index, row in enumerate(report["records"]):
        raw = source[index * 153600:(index + 1) * 153600]
        pixels = bytes(c for v, in struct.iter_unpack("<H", raw) for c in bgr555(v)[:3])
        if (row["index"] != index or sha(raw) != row["raw_sha256"]
                or sha(Path(row["preview"]).read_bytes()) != row["preview_sha256"]
                or Image.open(row["preview"]).convert("RGB").tobytes() != pixels):
            raise ValueError("Reviewed source/preview identity differs")
        row.update({"visual_review": "full-320x240-preview-reviewed-in-unscaled-six-image-sheet",
                    "observed_east_asian_text": index in OBSERVATIONS,
                    "observation": OBSERVATIONS.get(index, "Painting/sketch with no East Asian caption observed; Latin signatures retained."),
                    "translation_or_creator_credit_decision": "pending" if index in OBSERVATIONS else "no-caption-observed"})
    for row in report["sheets"]:
        if sha(Path(row["path"]).read_bytes()) != row["sha256"]:
            raise ValueError("Reviewed sheet changed")
        row["visual_review"] = "reviewed"
    report.update({"confirmed_east_asian_text_images": sorted(OBSERVATIONS),
                   "full_visual_review_complete": True,
                   "block_localized": False,
                   "native_format_geometry_proved": False})
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Recorded all 21 source reviews: 12 text-bearing images need translation/credit decisions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "record-review"])
    args = parser.parse_args()
    (prepare if args.action == "prepare" else record_review)()
