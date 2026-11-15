"""Prepare high-contrast controls for suspected off-screen Lil ending rows."""

import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/ending_pan_rows_v596")
PARENT = Path("out/all_routes_combined_v593_candidate.nds")
FILE = "/FLS/M31.fls"


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    original = NdsImage.open(PARENT)
    assert sha(PARENT.read_bytes()) == "d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642"
    source = original.read_file(FILE)
    assert source == NdsImage.open("work/clean.nds").read_file(FILE)
    movie = FlsArchive(source)
    tex = movie.texture(1)
    assert (tex.width, tex.height) == (256, 128)
    assert (movie.records[1][0] >> 16, movie.records[1][1] & 65535) == (256, 128)
    opaque = [n for n, rgba in enumerate(tex.palette) if rgba[3]]
    dark = min(opaque, key=lambda n: sum(tex.palette[n][:3]))
    bright = max(opaque, key=lambda n: sum(tex.palette[n][:3]))
    assert sum(tex.palette[bright][:3]) - sum(tex.palette[dark][:3]) > 500
    before = bytes(tex.indices)
    # Mark the first suspected off-screen row too, to test the raster boundary.
    for y in range(64, 128):
        for x in range(256):
            tex.indices[y * 256 + x] = bright if (y == 64 or (x // 8 + y // 8) % 2) else dark
    changed = [i for i, (a, b) in enumerate(zip(before, tex.indices, strict=True)) if a != b]
    assert changed and all(64 <= i // 256 < 128 for i in changed)
    output = movie.to_bytes()
    restored = FlsArchive(output)
    assert len(output) == len(source) and restored.records == movie.records
    for index in range(movie.count):
        a, b = FlsArchive(source).texture(index), restored.texture(index)
        assert (a.flags, a.width, a.height, a.palette) == (b.flags, b.width, b.height, b.palette)
        assert a.indices == b.indices if index != 1 else bytes(b.indices[:64 * 256]) == before[:64 * 256]
    original.replace_file(FILE, output)
    target = ROOT / "lil_lower_rows_RESEARCH_ONLY.nds"
    original.save(target)
    parent = NdsImage.open(PARENT)
    baseline = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    actual = NdsImage.open(target)
    final = {p: d for _, p, d in actual.iter_files()} | dict(actual.iter_components())
    assert baseline.keys() == final.keys() and [p for p in baseline if baseline[p] != final[p]] == [FILE]
    manifest = {"research_only": True, "not_playable_or_registered_release": True,
                "parent": str(PARENT), "parent_sha256": sha(PARENT.read_bytes()),
                "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
                "only_internal_file_changed": FILE, "texture": 1, "source_rows_owned": [64, 128],
                "changed_indices": len(changed), "changed_first_owned_row_indices": sum(i // 256 == 64 for i in changed),
                "marker_palette_indices": [dark, bright], "all_palettes_headers_extents_other_textures_exact": True,
                "source_movie_sha256": sha(source), "marked_movie_sha256": sha(output),
                "inputs": "work/analysis/endings_current_v583/lil_inputs.json", "captain": 2,
                "pause_at": 18000, "frames": 26600, "actual_display_not_yet_verified": True,
                "script_sha256": sha(Path(__file__).read_bytes())}
    target.with_suffix(".fixture.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared research-only lower-row control: {len(changed)} indices;V593 unchanged.")


if __name__ == "__main__":
    main()
