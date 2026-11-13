"""Fetch linked original promotional frames; never modify translated ROM assets."""

import argparse
import hashlib
import io
import json
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, UnidentifiedImageError

ROOT = Path("work/research/online_4gamer_sources")
GALLERY = "https://www.4gamer.net/store/shots/daikoukai_ol/"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img" and "src" in attrs:
            self.images.append(attrs["src"])


def fetch(url):
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as response:
        return response.read(), response.url


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def page(url):
    try:
        data, final = fetch(url)
        path = ROOT / ("page_" + url.rsplit("/", 1)[1])
        path.write_bytes(data)
        parser = Links()
        parser.feed(data.decode("shift_jis", errors="replace"))
        images = [urljoin(url, src) for src in parser.images if src.lower().endswith(".jpg")]
        return {
            "url": url,
            "resolved_url": final,
            "path": str(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "images": images,
        }
    except (OSError, URLError, ValueError) as error:
        return {"url": url, "error": str(error)}


def image(url):
    try:
        data, final = fetch(url)
        decoded = Image.open(io.BytesIO(data))
        decoded.load()
        path = ROOT / url.rsplit("/", 1)[1]
        path.write_bytes(data)
        return {
            "url": url,
            "resolved_url": final,
            "path": str(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "dimensions": list(decoded.size),
        }
    except (OSError, URLError, ValueError, UnidentifiedImageError) as error:
        return {"url": url, "error": str(error)}


def main():
    global ROOT, GALLERY
    parser = argparse.ArgumentParser()
    parser.add_argument("--second-gallery", action="store_true")
    args = parser.parse_args()
    if args.second_gallery:
        ROOT = ROOT / "customization"
        GALLERY = "https://www.4gamer.net/store/shots/daikoukai_ol_2/"
    ROOT.mkdir(parents=True, exist_ok=True)
    pages = []
    indexes = []
    for name in ("index.html", "index_2.html"):
        url = GALLERY + name
        data, final = fetch(url)
        path = ROOT / ("gallery_" + name)
        path.write_bytes(data)
        parser = Links()
        parser.feed(data.decode("shift_jis", errors="replace"))
        pages.extend(urljoin(url, link) for link in parser.links if "pages/" in link)
        indexes.append({"url": url, "resolved_url": final, "sha256": hashlib.sha256(data).hexdigest()})
    pages = list(dict.fromkeys(pages))
    with ThreadPoolExecutor(max_workers=6) as pool:
        page_rows = list(pool.map(page, pages))
    save_json(ROOT / "pages_fetch.json", page_rows)
    urls = list(dict.fromkeys(url for row in page_rows for url in row.get("images", [])))
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(image, urls))
    save_json(ROOT / "images_fetch.json", rows)
    for start in range(0, len(rows), 15):
        sheet = Image.new("RGB", (1280, 642), "#333333")
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(rows[start : start + 15]):
            x, y = index % 5 * 256, index // 5 * 214
            if "path" not in row:
                draw.text((x + 2, y + 2), "FETCH FAILED", fill="red")
                continue
            decoded = Image.open(row["path"])
            decoded.thumbnail((256, 192))
            sheet.paste(decoded, (x, y + 20))
            draw.text((x + 2, y + 2), Path(row["path"]).name, fill="white")
        sheet.save(ROOT / f"gallery_contact_{start // 15}.png")
    report = {
        "purpose": "Original screenshot research only; frame matching and exact transcription remain separate.",
        "indexes": indexes,
        "page_count": len(page_rows),
        "image_count": sum("path" in row for row in rows),
        "failures": [row for row in page_rows + rows if "error" in row],
        "translation_authority": "Visual game source, only when the exact ROM frame is matched.",
        "rom_changed": False,
    }
    save_json(ROOT / "research_fetch.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
