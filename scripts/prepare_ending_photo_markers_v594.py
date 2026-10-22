"""Prepare explicitly marked research counterparts for original ending photos."""

import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/ending_photo_markers_v594")
PARENT = Path("out/all_routes_combined_v593_candidate.nds")
CASES = ((1, "hodram", 30, 5, 14600), (3, "maria", 32, 4, 11200))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, previous, clean = [NdsImage.open(p) for p in (PARENT, Path("out/all_routes_combined_v581_candidate.nds"), Path("work/clean.nds"))]
    assert sha(PARENT.read_bytes()) == "d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642"
    arm, old_arm = [r.read_file("/__arm9__.bin") for r in (current, previous)]
    assert sha(arm) == "869431ccc3de5436ef9b33f9f3807d28c298be57cc757c2ee4c3618fba82651e"
    changes = [n for n, (a, b) in enumerate(zip(arm, old_arm, strict=True)) if a != b]
    assert len(changes) == 15 and all(0x12FFFC <= n < 0x130014 for n in changes)
    prior = json.loads(Path("work/analysis/endings_current_v583/fixture_provenance.json").read_text(encoding="utf-8"))
    ranges = []
    for row in prior["original_code_ranges"]:
        lo, hi = row["offset"]
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
        ranges.append(row)
    for lo, hi in ((0xFD4F8, 0xFDC60), (0xFEB28, 0xFEFCC), (0x100390, 0x1003CC), (0xDFA88, 0xDFD00)):
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
        ranges.append({"offset": [lo, hi], "sha256": sha(arm[lo:hi]), "exact_clean": True})
    baseline = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    results = []
    for captain, label, number, index, frame_limit in CASES:
        path = f"/FLS/M{number}.fls"
        source = current.read_file(path)
        assert source == previous.read_file(path) == clean.read_file(path)
        movie = FlsArchive(source)
        tex = movie.texture(index)
        before = bytes(tex.indices)
        width, height = movie.records[index][0] >> 16, movie.records[index][1] & 65535
        assert (tex.width, tex.height, width, height) == (256, 256, 256, 256 if captain == 1 else 192)
        opaque = [n for n in range(1, len(tex.palette)) if tex.palette[n][3]]
        dark = min(opaque, key=lambda n: sum(tex.palette[n][:3]))
        bright = max(opaque, key=lambda n: sum(tex.palette[n][:3]))
        assert sum(tex.palette[bright][:3]) - sum(tex.palette[dark][:3]) > 500
        positions = [(32, 32), (96, 64), (160, 96), (64, 128), (128, 160), (216, 176), (216, 216), (8, 224)]
        tags, owned = [], set()
        for tag, (left, top) in enumerate(positions):
            for y in range(16):
                for x in range(16):
                    border = x < 2 or x >= 14 or y < 2 or y >= 14
                    bit = (tag >> ((x - 2) // 2 % 3)) & 1
                    value = bright if border or (bit ^ (y // 4 & 1)) else dark
                    at = (top + y) * 256 + left + x
                    tex.indices[at] = value
                    owned.add(at)
            tags.append({"id": tag, "source_rect": [left, top, left + 16, top + 16],
                         "within_native_header": top + 16 <= height,
                         "marker_indices": [dark, bright]})
        changed = [n for n, (a, b) in enumerate(zip(before, tex.indices, strict=True)) if a != b]
        assert set(changed) <= owned and changed
        try:
            output = movie.to_bytes()
        except ValueError as error:
            raise ValueError(f"Marker control cannot fit original slot for {label}: {error}") from error
        saved = FlsArchive(output)
        assert len(output) == len(source) and saved.records == movie.records
        for i in range(movie.count):
            a, b = FlsArchive(source).texture(i), saved.texture(i)
            assert (a.flags, a.width, a.height, a.palette) == (b.flags, b.width, b.height, b.palette)
            if i != index:
                assert a.indices == b.indices
        rom = NdsImage.open(PARENT)
        rom.replace_file(path, output)
        target = ROOT / f"{label}_photo_markers_RESEARCH_ONLY.nds"
        rom.save(target)
        actual = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
        assert [p for p in baseline if baseline[p] != actual[p]] == [path]
        old_case = next(row for row in prior["cases"] if row["captain"] == captain)
        inputs = json.loads(Path(old_case["inputs"]).read_text(encoding="utf-8"))
        inputs = [row for row in inputs if row["start"] <= frame_limit]
        input_path = ROOT / f"{label}_inputs.json"
        input_path.write_text(json.dumps(inputs, indent=2) + "\n", encoding="utf-8")
        donor = Path(old_case["source_save"])
        assert sha(donor.read_bytes()) == old_case["source_save_sha256"]
        manifest = {"research_only": True, "not_playable_or_registered_release": True,
                    "parent": str(PARENT), "parent_sha256": sha(PARENT.read_bytes()),
                    "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
                    "only_internal_file_changed": path, "texture": index, "tags": tags,
                    "native_dimensions": [width, height], "stored_dimensions": [256, 256],
                    "changed_source_indices": len(changed), "only_eight_declared16x16_tags_owned": True,
                    "all_headers_palettes_extents_other_textures_and_timeline_exact": True,
                    "source_movie_sha256": sha(source), "marked_movie_sha256": sha(output),
                    "captain": captain, "label": label, "frames": frame_limit, "pause_at": 3000,
                    "inputs": str(input_path), "source_save": str(donor), "source_save_sha256": sha(donor.read_bytes()),
                    "source_and_marked_ARM9_exact": True, "actual_display_not_yet_verified": True}
        target.with_suffix(".fixture.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        results.append(manifest)
    proof = {"candidate": str(PARENT), "candidate_sha256": sha(PARENT.read_bytes()),
             "verified_ARM9_sha256": sha(arm), "ARM9_vs_V581_only15_room_data_bytes": changes,
             "source_exact_original_code_ranges": ranges, "cases": results,
             "production_ROM_or_patch_modified": False, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "fixture_manifest.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("Prepared two original-photo marker research controls;V593 and patch unchanged;original ending fixture guards source-checked.")


if __name__ == "__main__":
    main()
