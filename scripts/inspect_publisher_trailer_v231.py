"""Inspect every trailer frame; keep visual similarity separate from source proof."""

import json
from pathlib import Path

import av
from PIL import Image, ImageChops, ImageDraw, ImageStat

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/research/publisher_archive_images_v231")
OUT = ROOT / "trailer_frames"
SOURCE = ROOT / "tgs2004_movie_source.json"
ORIGINALS = Path("work/analysis/graphics_preservation_v225/online_source_request")


def page(panels, path, columns=4):
    width = max(image.width for _, image in panels)
    height = max(image.height for _, image in panels) + 22
    rows = (len(panels) + columns - 1) // columns
    result = Image.new("RGB", (width * columns, height * rows), "#303030")
    draw = ImageDraw.Draw(result)
    for index, (label, image) in enumerate(panels):
        x, y = index % columns * width, index // columns * height
        draw.text((x + 2, y + 2), label, fill="white")
        result.paste(image, (x, y + 20))
    result.save(path)


def frame_image(frame):
    converted = frame.to_rgb()
    plane = converted.planes[0]
    return Image.frombytes("RGB", (converted.width, converted.height), bytes(plane),
                           "raw", "RGB", plane.line_size)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    path = Path(source["path"])
    if sha(path.read_bytes()) != source["sha256"]:
        raise ValueError("Publisher video source identity differs")
    targets = {number: Image.open(ORIGINALS / f"Online{number}_original_native.png").convert("RGB")
               for number in (24, 27, 31, 33)}
    mini = {number: image.resize((64, 48)) for number, image in targets.items()}
    best, samples = {number: [] for number in targets}, []
    next_sample, count = 0.0, 0
    first_time, final_time = None, 0.0
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        metadata = {"codec": stream.codec_context.name, "width": stream.codec_context.width,
                    "height": stream.codec_context.height, "average_rate": str(stream.average_rate),
                    "sample_aspect_ratio": str(stream.sample_aspect_ratio), "PyAV_version": av.__version__}
        for index, frame in enumerate(container.decode(video=0)):
            image = frame_image(frame)
            time = float(frame.time) if frame.time is not None else index / float(stream.average_rate)
            if first_time is None:
                first_time = time
            elapsed = time - first_time
            final_time = elapsed
            small = image.resize((64, 48))
            for number, target in mini.items():
                stats = ImageStat.Stat(ImageChops.difference(target, small))
                error = sum(stats.mean) / 3
                rank = best[number]
                if len(rank) < 5 or error < rank[-1]["mean_RGB_error"]:
                    candidate = {"decoded_frame": index, "seconds": elapsed, "mean_RGB_error": error,
                                 "image": image.copy()}
                    rank.append(candidate)
                    rank.sort(key=lambda row: row["mean_RGB_error"])
                    del rank[5:]
            if elapsed >= next_sample:
                saved = OUT / f"sample_{len(samples):03d}_{index:05d}.png"
                image.save(saved)
                samples.append({"decoded_frame": index, "seconds": elapsed,
                                "path": saved.as_posix(), "sha256": sha(saved.read_bytes())})
                next_sample += 2
            count += 1
    sheets = []
    for start in range(0, len(samples), 12):
        group = samples[start:start + 12]
        saved = OUT / f"timeline_{start // 12}.png"
        page([(f"{row['seconds']:.1f}s f{row['decoded_frame']}", Image.open(row["path"]).convert("RGB"))
              for row in group], saved)
        sheets.append({"path": saved.as_posix(), "sha256": sha(saved.read_bytes()), "samples": group,
                       "visual_review_complete": False})
    matches = []
    for number, ranks in best.items():
        panels = [(f"Original Online{number}", targets[number])]
        for index, row in enumerate(ranks):
            image = row.pop("image")
            saved = OUT / f"Online{number}_candidate_{index}_{row['decoded_frame']:05d}.png"
            image.save(saved)
            row.update(path=saved.as_posix(), sha256=sha(saved.read_bytes()))
            panels.append((f"{row['seconds']:.2f}s MAE{row['mean_RGB_error']:.2f}", image))
        saved = OUT / f"Online{number}_comparison.png"
        page(panels, saved, columns=3)
        matches.append({"resource": number, "candidates": ranks, "sheet": saved.as_posix(),
                        "sheet_sha256": sha(saved.read_bytes()), "exact_source_match": None})
    result = {"format": "dk4-publisher-trailer-frame-source-search-v231",
              "video_source": source, "video_metadata": metadata, "complete_decoded_frames_compared": count,
              "duration_decoded_seconds": final_time, "samples": samples, "timeline_sheets": sheets,
              "candidate_comparisons": matches,
              "similarity_is_only_candidate_ranking_not_transcription_or_identity_proof": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "trailer_review_inventory.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"video": metadata, "decoded_frames": count, "duration_seconds": final_time,
                      "timeline_sheets": len(sheets), "candidate_sheets": len(matches)}))


if __name__ == "__main__":
    main()
