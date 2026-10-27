"""Check remaining archive-discovered official image URLs for readable sources.

Fetch current publisher-hosted bytes only. Historical archive timestamps provide
discovery provenance, not proof that today's bytes match the archived capture.
No ROM, source transcript or translation is changed by this research.
"""

import argparse
import io
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageSequence

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/research/publisher_archive_images_v231")
INDEX = Path("work/research/online_4gamer_sources/archive_index.json")
PREVIOUS = Path("work/research/online_4gamer_sources/publisher_archive/fetch.json")


def official_url(original):
    parsed = urlsplit(original)
    if parsed.hostname != "www.gamecity.ne.jp" or not parsed.path.startswith("/dol/game/"):
        raise ValueError("Archive URL leaves the verified publisher subtree")
    return urlunsplit(("https", "www.gamecity.ne.jp", parsed.path, parsed.query, ""))


def fetch(row):
    result = {"archive_timestamp": row[1], "original_url": row[2],
              "historical_digest": row[5], "historical_length": int(row[6]),
              "requested_url": official_url(row[2])}
    try:
        request = Request(result["requested_url"], headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=12) as response:
            data = response.read(8 * 1024 * 1024 + 1)
            final = response.url
        if len(data) > 8 * 1024 * 1024:
            raise ValueError("Image exceeds bounded source research size")
        if urlsplit(final).hostname not in {"www.gamecity.ne.jp", "gamecity.ne.jp"}:
            raise ValueError("Redirect leaves publisher host")
        decoded = Image.open(io.BytesIO(data))
        decoded.load()
        filename = urlsplit(result["requested_url"]).path.replace("/", "_").lstrip("_")
        path = ROOT / filename
        path.write_bytes(data)
        frames = []
        for index, frame in enumerate(ImageSequence.Iterator(decoded)):
            preview = ROOT / f"{filename}_frame{index:03d}.png"
            frame.convert("RGB").save(preview)
            frames.append({"frame": index, "path": preview.as_posix(), "sha256": sha(preview.read_bytes())})
        result.update({"status": "fetched-current-publisher-image", "resolved_url": final,
                       "path": path.as_posix(), "sha256": sha(data), "bytes": len(data),
                       "dimensions": list(decoded.size), "frame_count": len(frames), "frames": frames,
                       "current_bytes_not_asserted_equal_to_historical_capture": True})
    except (OSError, ValueError) as error:
        result.update({"status": "unavailable", "error": f"{type(error).__name__}: {error}"})
    return result


def sheets(results, prefix="archive_sources"):
    frames = [(row, frame) for row in results if row["status"].startswith("fetched") for frame in row["frames"]]
    output = []
    for start in range(0, len(frames), 8):
        page = Image.new("RGB", (1000, 600), "#303030")
        draw = ImageDraw.Draw(page)
        group = frames[start:start + 8]
        for index, (row, frame) in enumerate(group):
            image = Image.open(frame["path"]).convert("RGB")
            image.thumbnail((244, 266))
            x, y = index % 4 * 250, index // 4 * 300
            draw.text((x + 2, y + 2), f"{start + index} {Path(row['path']).name[-27:]}", fill="white")
            draw.text((x + 2, y + 14), f"{row['dimensions']} f{frame['frame']}", fill="white")
            page.paste(image, (x, y + 30))
        path = ROOT / f"{prefix}_{start // 8}.png"
        page.save(path)
        output.append({"path": path.as_posix(), "sha256": sha(path.read_bytes()),
                       "sources": [{"URL": row["resolved_url"], "frame": frame["frame"], "preview": frame["path"]}
                                   for row, frame in group], "visual_review_complete": False})
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-small", action="store_true", help="Also inspect every small navigation/border/button image in the recovered index.")
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    seen = {official_url(row["original_url"]) for row in previous if row.get("path") and not row.get("error")}
    # JPEGs include scenery/character/game screenshots. Larger GIFs can contain
    # screenshot composites; small navigation/button/spacer assets are recorded
    # as exclusions rather than silently called searched screenshots.
    candidates = [row for row in index[1:] if official_url(row[2]) not in seen
                  and (args.include_small or urlsplit(row[2]).path.lower().endswith((".jpg", ".jpeg", ".png"))
                       or (row[3] == "image/gif" and int(row[6]) >= 4000))]
    skipped = [row for row in index[1:] if row not in candidates]
    cached_path = ROOT / "source_inventory.json"
    cached = json.loads(cached_path.read_text(encoding="utf-8"))["results"] if cached_path.is_file() else []
    cached = {row["requested_url"]: row for row in cached if row.get("path")
              and sha(Path(row["path"]).read_bytes()) == row.get("sha256")}
    results = [cached[official_url(row[2])] for row in candidates if official_url(row[2]) in cached]
    pending = [row for row in candidates if official_url(row[2]) not in cached]
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(fetch, row): row for row in pending}
        for job in as_completed(jobs):
            row = job.result()
            results.append(row)
            print(json.dumps({"done": len(results), "total": len(candidates), "URL": row["requested_url"],
                              "status": row["status"], "dimensions": row.get("dimensions")}), flush=True)
            # Persist completed work while later bounded requests remain live.
            (ROOT / "fetch_progress.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    results.sort(key=lambda row: row["requested_url"])
    result = {"format": "dk4-publisher-source-image-research-v231", "index_sha256": sha(INDEX.read_bytes()),
              "archive_URLs": len(index) - 1, "previously_fetched_URLs": len(seen),
              "additional_candidates": len(candidates), "results": results,
              "small_images_included": args.include_small, "new_network_requests": len(pending),
              "skipped": [{"original_URL": row[2], "reason": "previously fetched" if official_url(row[2]) in seen else "small navigation/button/spacer source"}
                          for row in skipped],
              "review_sheets": sheets(results), "exact_screenshot_matches_not_yet_reviewed": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "source_inventory.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"additional_candidates": len(candidates), "fetched": sum(row['status'].startswith('fetched') for row in results),
                      "unavailable": sum(row['status'] == 'unavailable' for row in results), "sheets": len(result['review_sheets'])}))


if __name__ == "__main__":
    main()
