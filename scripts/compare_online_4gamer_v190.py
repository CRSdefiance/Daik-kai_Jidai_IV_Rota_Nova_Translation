"""Rank fetched frames against canonical screenshots; scores are not transcription proof."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/research/online_4gamer_sources")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BASE_SHA = "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"


def main():
    assert hashlib.sha256(BASE.read_bytes()).hexdigest() == BASE_SHA
    base = NdsImage.open(BASE)
    rows = []
    for folder in (ROOT, ROOT / "customization"):
        rows.extend(json.loads((folder / "images_fetch.json").read_text(encoding="utf-8")))
    sources = []
    for row in rows:
        if "path" not in row:
            continue
        path = Path(row["path"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        original = Image.open(path).convert("RGB")
        sources.append((row, original, original.resize((64, 48), Image.Resampling.BILINEAR)))
    selections = json.loads(Path("work/analysis/online_resource_pages_v189.json").read_text())
    paths = list(dict.fromkeys(s["path"] for page in selections["pages"] for s in page["screenshots"]))
    results = []
    previews = []
    for path in paths:
        data = base.read_file(path)
        original = PxlImage.from_bytes(data).render().convert("RGB")
        reduced = original.resize((64, 48), Image.Resampling.BILINEAR)
        ranked = []
        for row, full, thumb in sources:
            difference = ImageChops.difference(reduced, thumb)
            score = sum(ImageStat.Stat(difference).mean) / 3
            ranked.append((score, row, full))
        ranked.sort(key=lambda item: item[0])
        results.append({
            "path": path,
            "canonical_resource_sha256": hashlib.sha256(data).hexdigest(),
            "best_candidates": [dict(score_rgb_mae_64x48=score, **row) for score, row, _ in ranked[:4]],
            "exact_frame_verified": False,
            "ranking_is_not_source_authority": True,
        })
        previews.append((path, original, ranked[:4]))
    for start in range(0, len(previews), 6):
        sheet = Image.new("RGB", (1280, 6 * 218), "#333333")
        draw = ImageDraw.Draw(sheet)
        for index, (path, original, ranked) in enumerate(previews[start : start + 6]):
            y = index * 218
            draw.text((2, y + 2), Path(path).name + " canonical", fill="white")
            sheet.paste(original, (0, y + 22))
            for col, (score, row, full) in enumerate(ranked, 1):
                label = Path(row["path"]).parent.name + "/" + Path(row["path"]).name
                draw.text((col * 256 + 2, y + 2), f"{label} {score:.2f}", fill="white")
                sheet.paste(full.resize((256, 192), Image.Resampling.BILINEAR), (col * 256, y + 22))
        sheet.save(ROOT / f"matching_review_{start // 6}.png")
    report = {
        "canonical_base": str(BASE),
        "canonical_base_sha256": BASE_SHA,
        "comparison_method": "Mean RGB absolute error after bilinear reduction to 64x48; whole-frame candidate ranking only.",
        "screenshot_count": len(results),
        "archived_frame_count": len(sources),
        "results": results,
        "rom_changed": False,
        "no_unreadable_text_inferred_from_similar_frames": True,
    }
    (ROOT / "matching_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for row in results:
        best = row["best_candidates"][0]
        print(row["path"], best["path"], f"MAE={best['score_rgb_mae_64x48']:.2f}")


if __name__ == "__main__":
    main()
