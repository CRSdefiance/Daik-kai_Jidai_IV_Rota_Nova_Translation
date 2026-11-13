"""Fetch an actually linked beta gallery and rank exact screenshot candidates."""

import io
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image, ImageChops, ImageDraw, ImageStat

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_online_4gamer_v190 import Links, fetch

ROOT = Path("work/research/online_beta_sources_v244")
GALLERY = "https://www.4gamer.net/shots/daikoukaionline/"


def page(url):
    try:
        data, final = fetch(url)
        parser = Links()
        parser.feed(data.decode("euc_jp", errors="replace"))
        name = "page_" + sha(url.encode())[:12] + ".html"
        path = ROOT / name
        path.write_bytes(data)
        return {"url": url, "resolved_url": final, "path": str(path), "sha256": sha(data),
                "links": sorted({urljoin(final, p).replace("http://www.4gamer.net", "https://www.4gamer.net")
                                 for p in parser.links}),
                "images": sorted({urljoin(final, p) for p in parser.images})}
    except (OSError, ValueError) as error:
        return {"url": url, "error": str(error)}


def picture(url):
    try:
        data, final = fetch(url)
        path = ROOT / ("image_" + sha(url.encode())[:12] + Path(url).suffix)
        path.write_bytes(data)
        image = Image.open(io.BytesIO(data)).convert("RGB")
        return {"url": url, "resolved_url": final, "path": str(path), "sha256": sha(data),
                "dimensions": list(image.size)}
    except (OSError, ValueError) as error:
        return {"url": url, "error": str(error)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    discovery = json.loads((ROOT / "beta_gallery_discovery.json").read_text(encoding="utf-8"))
    first = {"url": discovery["url"], "links": discovery["links"], "images": discovery["images"],
             "path": str(ROOT / "beta_gallery.html"), "sha256": discovery["sha256"]}
    assert sha(Path(first["path"]).read_bytes()) == first["sha256"]
    indexes = [first]
    queue = {u for u in first["links"] if u.startswith(GALLERY) and "/pages/" not in u}
    done = {first["url"]}
    while queue - done:
        batch = sorted(queue - done)
        assert len(done) + len(batch) <= 10
        rows = list(ThreadPoolExecutor(max_workers=4).map(page, batch))
        done.update(batch)
        indexes.extend(rows)
        for row in rows:
            queue.update(u for u in row.get("links", []) if u.startswith(GALLERY)
                         and "/pages/" not in u and u.endswith(".html"))
    page_urls = sorted({u for row in indexes for u in row.get("links", [])
                        if u.startswith(GALLERY + "pages/") and u.endswith(".html")})
    pages = list(ThreadPoolExecutor(max_workers=4).map(page, page_urls))
    image_urls = {u for row in pages for u in row.get("images", [])
                  if "/shots/daikoukaionline/images/" in u and u.lower().endswith(".jpg")}
    extra = json.loads((ROOT / "page_discovery.json").read_text(encoding="utf-8"))
    for row in extra:
        image_urls.update(u for u in row.get("images", []) if u.endswith(".jpg")
                          and ("/dol/report/image/" in u or "/news/image/2004.11/" in u))
    images = list(ThreadPoolExecutor(max_workers=4).map(picture, sorted(image_urls)))
    clean = NdsImage.open("work/clean.nds")
    targets = {n: PxlImage.from_bytes(clean.read_file(f"/_pxl/online/Online{n}.pxl")).render().convert("RGB")
               for n in (24, 27, 31, 33)}
    ranks = {}
    for n, target in targets.items():
        rows = []
        mini = target.resize((64, 48))
        for row in images:
            if "error" in row:
                continue
            assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
            image = Image.open(row["path"]).convert("RGB")
            score = sum(ImageStat.Stat(ImageChops.difference(mini, image.resize((64, 48)))).mean) / 3
            rows.append({"source": row, "RGB_MAE_64x48": score})
        rows.sort(key=lambda r: r["RGB_MAE_64x48"])
        ranks[n] = rows[:5]
        panels = [(f"Native Online{n}", target)] + [(f"MAE {r['RGB_MAE_64x48']:.1f}",
                                                    Image.open(r["source"]["path"]).convert("RGB"))
                                                   for r in rows[:5]]
        sheet = Image.new("RGB", (3 * 320, 2 * 276), "#dedede")
        draw = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(panels):
            x, y = i % 3 * 320, i // 3 * 276
            draw.text((x + 3, y + 3), label, fill="black")
            image.thumbnail((320, 248))
            sheet.paste(image, (x, y + 24))
        sheet.save(ROOT / f"Online{n}_ranked_review.png")
    sheets = []
    successful = [r for r in images if "error" not in r]
    for first_index in range(0, len(successful), 12):
        batch = successful[first_index:first_index + 12]
        sheet = Image.new("RGB", (960, ((len(batch) + 2) // 3) * 276), "#dedede")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(batch):
            image = Image.open(row["path"]).convert("RGB")
            image.thumbnail((320, 248))
            x, y = i % 3 * 320, i // 3 * 276
            draw.text((x + 3, y + 3), Path(row["url"]).name, fill="black")
            sheet.paste(image, (x, y + 24))
        path = ROOT / f"all_source_review_{first_index // 12}.png"
        sheet.save(path)
        sheets.append({"path": str(path), "sha256": sha(path.read_bytes()), "sources": batch})
    inventory = {"format": "dk4-online-beta-source-search-v244", "indexes": indexes,
                 "image_pages": pages, "images": images, "all_source_sheets": sheets,
                 "ranks": ranks, "similarity_is_candidate_ranking_not_identity_or_transcript": True,
                 "visual_review_pending": True, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "source_inventory.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"gallery_indexes": len(indexes), "image_pages": len(pages),
                      "downloaded_images": len(successful), "errors": len(images) - len(successful),
                      "full_collection_sheets": len(sheets), "ranking_sheets": len(ranks)}))


if __name__ == "__main__":
    main()
