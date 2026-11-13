"""Recover actually linked contemporary press/guide images for exact matching."""

import io
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_online_4gamer_v190 import Links, fetch

ROOT = Path("work/research/online_press_sources_v273")


def page(url):
    try:
        data, final = fetch(url)
        path = ROOT / ("page_" + sha(url.encode())[:12] + ".html")
        path.write_bytes(data)
        parser = Links(); parser.feed(data.decode("shift_jis", errors="replace"))
        return {"url": url, "resolved_url": final, "path": str(path), "sha256": sha(data),
                "links": [urljoin(final, v) for v in parser.links],
                "images": [urljoin(final, v) for v in parser.images]}
    except (OSError, ValueError) as error:
        return {"url": url, "error": str(error)}


def picture(url):
    try:
        data, final = fetch(url)
        image = Image.open(io.BytesIO(data)); image.load()
        path = ROOT / ("image_" + sha(url.encode())[:12] + Path(url).suffix)
        path.write_bytes(data)
        return {"url": url, "resolved_url": final, "path": str(path), "sha256": sha(data),
                "dimensions": list(image.size)}
    except (OSError, ValueError) as error:
        return {"url": url, "error": str(error)}


def main():
    ROOT.mkdir(exist_ok=True)
    discovery = json.loads((ROOT / "discovery.json").read_text(encoding="utf-8"))
    review = discovery[0]
    urls = {u for u in review["links"] if u.startswith("https://game.watch.impress.co.jp/docs/20050316/dai") and u != review["url"]}
    for guide in discovery[1:]:
        urls.update(u for u in guide["links"] if "/guide/index" in u and "#" not in u)
    pages = list(ThreadPoolExecutor(max_workers=4).map(page, sorted(urls)))
    images = {u for row in pages + discovery for u in row.get("images", [])
              if u.lower().endswith((".jpg", ".jpeg", ".gif", ".png"))
              and ("/20050316/" in u or "sinario" in u or "scenario" in u)}
    photos = list(ThreadPoolExecutor(max_workers=4).map(picture, sorted(images)))
    usable = [r for r in photos if "path" in r and r["dimensions"][0] >= 200 and r["dimensions"][1] >= 120]
    sheets = []
    for start in range(0, len(usable), 12):
        sheet = Image.new("RGB", (1024, 816), "#333333"); draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(usable[start:start + 12]):
            x, y = index % 4 * 256, index // 4 * 272
            pic = Image.open(row["path"]).convert("RGB"); pic.thumbnail((248, 240))
            draw.text((x + 4, y + 2), f"{start + index}: {row['dimensions']}", fill="white")
            sheet.paste(pic, (x + 4, y + 24))
        path = ROOT / f"source_review_{start // 12}.png"; sheet.save(path)
        sheets.append({"path": str(path), "sha256": sha(path.read_bytes()), "first_index": start})
    result = {"format": "dk4-press-source-inventory-v273", "initial_discovery": discovery,
              "linked_pages": pages, "images": photos, "review_candidates": usable, "sheets": sheets,
              "all_URLs_from_actual_links_or_image_attributes": True,
              "no_ROM_or_translation_changed": True, "exact_four_target_transcripts": "pending-review"}
    (ROOT / "inventory.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(pages), "images": len(photos), "usable": len(usable), "sheets": len(sheets)}))


if __name__ == "__main__":
    main()
