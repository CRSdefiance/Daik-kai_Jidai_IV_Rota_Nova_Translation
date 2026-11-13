"""Prepare source-bound tags for the third original Hodram pan tile."""

import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/hodram_pan_tags_v597")
PARENT = Path("out/all_routes_combined_v593_candidate.nds")
FILE = "/FLS/M30.fls"
DONOR = Path("work/analysis/ending_caller_v537/hodram-ending-test-only.dsv")
INPUTS = Path("work/analysis/ending_photo_markers_v594/hodram_inputs.json")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(PARENT), NdsImage.open("work/clean.nds")
    assert sha(PARENT.read_bytes()) == "d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642"
    source = current.read_file(FILE)
    assert source == clean.read_file(FILE)
    arm = current.read_file("/__arm9__.bin")
    ranges = ((0xFD4F8, 0xFDC60), (0xFEB28, 0xFF9C8), (0x100390, 0x1003CC))
    assert all(arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi] for lo, hi in ranges)
    assert sha(DONOR.read_bytes()) == "83fe3317eee3bca21b70be69bf34febd12d3aea09a83e75003b1f848d5fea937"
    movie = FlsArchive(source)
    tex = movie.texture(3)
    assert (tex.width, tex.height, movie.records[3][0] >> 16, movie.records[3][1] & 65535) == (256, 128, 256, 128)
    tex.render().save(ROOT / "M30_texture3_original_full.png")
    original = bytes(tex.indices)
    opaque = [n for n, rgba in enumerate(tex.palette) if rgba[3]]
    dark = min(opaque, key=lambda n: sum(tex.palette[n][:3]))
    bright = max(opaque, key=lambda n: sum(tex.palette[n][:3]))
    assert sum(tex.palette[bright][:3]) - sum(tex.palette[dark][:3]) > 500
    tags, owned = [], set()
    for tag, (left, top) in enumerate(((24, 0), (88, 16), (160, 32), (40, 48),
                                        (104, 64), (184, 80), (16, 96), (224, 112))):
        for y in range(16):
            for x in range(16):
                border = min(x, y, 15 - x, 15 - y) < 2
                bit = (tag >> ((x - 2) // 2 % 3)) & 1
                at = (top + y) * 256 + left + x
                tex.indices[at] = bright if border or bit ^ (y // 4 & 1) else dark
                owned.add(at)
        tags.append({"id": tag, "source_rect": [left, top, left + 16, top + 16],
                     "within_native_header": True, "marker_indices": [dark, bright]})
    changes = {n for n, (a, b) in enumerate(zip(original, tex.indices, strict=True)) if a != b}
    assert changes and changes <= owned
    output = movie.to_bytes()
    result = FlsArchive(output)
    assert result.records == movie.records and len(output) == len(source)
    for index in range(movie.count):
        a, b = FlsArchive(source).texture(index), result.texture(index)
        assert (a.flags, a.width, a.height, a.palette) == (b.flags, b.width, b.height, b.palette)
        if index != 3:
            assert a.indices == b.indices
    baseline = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    current.replace_file(FILE, output)
    target = ROOT / "hodram_pan_tile3_tags_RESEARCH_ONLY.nds"
    current.save(target)
    reopened = NdsImage.open(target)
    final = {p: d for _, p, d in reopened.iter_files()} | dict(reopened.iter_components())
    assert baseline.keys() == final.keys() and [p for p in baseline if baseline[p] != final[p]] == [FILE]
    manifest = {"research_only": True, "not_playable_or_registered_release": True,
                "parent": str(PARENT), "parent_sha256": sha(PARENT.read_bytes()),
                "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
                "only_internal_file_changed": FILE, "texture": 3, "tags": tags,
                "native_dimensions": [256, 128], "stored_dimensions": [256, 128],
                "changed_source_indices": len(changes), "only_declared_tag_pixels_owned": True,
                "all_headers_palettes_extents_other_textures_timeline_and_code_exact": True,
                "source_movie_sha256": sha(source), "marked_movie_sha256": sha(output),
                "source_save": str(DONOR), "source_save_sha256": sha(DONOR.read_bytes()),
                "inputs": str(INPUTS), "inputs_sha256": sha(INPUTS.read_bytes()),
                "captain": 1, "pause_at": 3000, "frames": 14600,
                "source_exact_code_ranges": [{"offset": [lo, hi], "sha256": sha(arm[lo:hi])} for lo, hi in ranges],
                "actual_display_not_yet_verified": True, "script_sha256": sha(Path(__file__).read_bytes())}
    target.with_suffix(".fixture.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared tile3 tag control: {len(changes)} source indices;V593 unchanged.")


if __name__ == "__main__":
    main()
