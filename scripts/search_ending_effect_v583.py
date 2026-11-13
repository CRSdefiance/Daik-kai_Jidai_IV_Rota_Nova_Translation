"""Find all46 original M30 streak pixels without treating transparency as black."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/endings_current_v583")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/endings_current_v583_hodram")


def source_points(rom):
    texture = FlsArchive(rom.read_file("/FLS/M30.fls")).texture(4)
    assert (texture.width, texture.height) == (256, 64)
    points = [(i % 256, i // 256, tuple(v >> 3 for v in texture.palette[n][:3]))
              for i, n in enumerate(texture.indices) if n]
    assert len(points) == 46
    assert {c for _, _, c in points} == {(18, 18, 18), (22, 22, 22)}
    return points


def matches(image, points):
    raw = image.convert("RGB").crop((0, 0, 256, 192)).point(lambda v: v >> 3).tobytes()
    ax, ay, anchor = next(p for p in points if p[2] == (22, 22, 22))
    needle, start, result = bytes(anchor), 0, []
    while (at := raw.find(needle, start)) >= 0:
        start = at + 1
        if at % 3:
            continue
        pixel = at // 3
        left, top = pixel % 256 - ax, pixel // 256 - ay
        if not all(0 <= left + x < 256 and 0 <= top + y < 192 for x, y, _ in points):
            continue
        if all(raw[((top + y) * 256 + left + x) * 3:((top + y) * 256 + left + x) * 3 + 3] == bytes(color)
               for x, y, color in points):
            result.append([left, top])
    return result


def main():
    rom = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    points = source_points(rom)
    found = []
    for frame in range(12000, 14001):
        path = CAPTURE / f"frame_{frame:06d}_cold_boot.png"
        if not path.exists():
            raise ValueError(f"Dense effect search requires every native frame: missing {frame}")
        with Image.open(path) as image:
            locations = matches(image, points)
        if locations:
            found.append({"frame": frame, "path": str(path), "PNG_sha256": sha(path.read_bytes()),
                          "all46_original_opaque_source_points_exact_at_origins": locations})
    result = {"source_movie": "/FLS/M30.fls", "texture": 4, "source_points": points,
              "dense_search_window": [12000, 14000], "full_source_streak_matches": found,
              "transparent_background_not_assumed_black": True,
              "full_background_composition_and_internal_GPU_alpha_not_claimed": True}
    (ROOT / "M30_effect_search.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print({"matches": len(found), "first": found[:1], "last": found[-1:]})


if __name__ == "__main__":
    main()
