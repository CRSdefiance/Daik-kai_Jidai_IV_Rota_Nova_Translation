"""Pin the 42 reviewed portrait previews; native format/usage remain unproved."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import CANONICAL_BASELINE_SHA256

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v177_candidate.nds")
CANDIDATE_SHA = "a5dba05534ec334167d0ffd9f506050f35ca11555eaa38cd5d1a17fbf3034d45"
BLOCK_SHA = "8fcdf8829cce4f1cdc967a983327343bfe92279437df84c4877b606fe4f7817c"
OUT = Path("work/qa/embedded_raw_v176/portrait13")


def main():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256:
        raise ValueError("Wrong canonical source")
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError("Wrong V177 candidate")
    base, current = [NdsImage.open(p) for p in (BASE, CANDIDATE)]
    source = IlnkContainer.parse(base.read_file("/GRP/SLACKIMG.DK4")).blocks[13]
    saved = IlnkContainer.parse(current.read_file("/GRP/SLACKIMG.DK4")).blocks[13]
    if sha(source) != BLOCK_SHA or source != saved or len(source) != 42 * 320 * 240 * 2:
        raise ValueError("Original portrait extent/bytes differ")
    report = json.loads((OUT / "inventory.json").read_text(encoding="utf-8"))
    if report["source_block_sha256"] != BLOCK_SHA or len(report["records"]) != 42:
        raise ValueError("Preview inventory differs")
    reconstructed = bytearray()
    for index, row in enumerate(report["records"]):
        offset = index * 153600
        raw = source[offset:offset + 153600]
        if (
            row["index"] != index or row["raw_offset"] != offset
            or row["raw_bytes"] != len(raw) or row["raw_sha256"] != sha(raw)
            or (row["width"], row["height"]) != (320, 240)
        ):
            raise ValueError("Portrait partition/source lock differs")
        words = [v for v, in struct.iter_unpack("<H", raw)]
        if any(v & 0x8000 for v in words):
            raise ValueError("Unexpected high color bits")
        pixels = bytes(channel for v in words for channel in bgr555(v)[:3])
        image = Image.open(row["preview"]).convert("RGB")
        if image.size != (320, 240) or image.tobytes() != pixels:
            raise ValueError("Reviewed preview differs from source words")
        reconstructed.extend(struct.pack("<76800H", *words))
        row.update({
            "preview_sha256": sha(Path(row["preview"]).read_bytes()),
            "visual_review": "full-320x240-preview-reviewed-in-unscaled-six-image-sheet",
            "observed_japanese_caption": False,
            "observed_content": (
                "Character portrait; existing Latin El Gato wording on apron retained."
                if index == 6 else
                "Character portrait, clothes and decorative motifs; no Japanese caption observed."
            ),
            "original_block_byte_exact_in_v177": True,
            "native_geometry_proved": False,
        })
    if bytes(reconstructed) != source:
        raise ValueError("Full source-word roundtrip differs")
    sheets = []
    for index in range(7):
        path = OUT / f"sheet_{index}.png"
        if Image.open(path).size != (984, 536):
            raise ValueError("Reviewed full-size sheet dimensions differ")
        sheets.append({"path": str(path), "sha256": sha(path.read_bytes()),
                       "visual_review": "reviewed", "portrait_indices": list(range(index * 6, index * 6 + 6))})
    report.update({
        "candidate": str(CANDIDATE), "candidate_sha256": CANDIDATE_SHA,
        "canonical_source_sha256": CANONICAL_BASELINE_SHA256,
        "sheets": sheets,
        "whole_block_words_consumed": True, "RGB555_roundtrip_exact": True,
        "classification": "42 coherent BGR555 portrait previews under a 320x240 partition hypothesis",
        "limits": [
            "All source words were inspected as coherent portrait images; no Japanese caption was observed.",
            "320x240 partition and BGR555 interpretation are not proved by a mapped native loader or metadata.",
            "This review does not clear the archive, runtime palette/alpha/crops or other unclassified blocks.",
        ],
    })
    (OUT / "inventory.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    decisions_path = Path("translations/contextual_graphics_decisions_v177.json")
    decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
    for row in decisions["records"]:
        raw = base.read_file(row["path"])
        if sha(raw) != row["source_sha256"] or current.read_file(row["path"]) != raw:
            raise ValueError("Reviewed contextual art changed")
        row["original_file_byte_exact_in_v177"] = True
    decisions.update({"candidate": str(CANDIDATE), "candidate_sha256": CANDIDATE_SHA})
    decisions_path.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Pinned 42 reviewed portraits and six unchanged contextual art decisions to exact V177.")


if __name__ == "__main__":
    main()
