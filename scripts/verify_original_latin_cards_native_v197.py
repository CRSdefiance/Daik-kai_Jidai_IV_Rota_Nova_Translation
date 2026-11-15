"""Compare complete original Latin lettering with unmodified cold-boot output."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def native5(color):
    return tuple((value * 31 + 127) // 255 for value in color[:3])


def main():
    root = Path("work/emulation_v193/v190_latin_opening_fine")
    evidence_path = root / "capture_report.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert evidence["ROM_sha256"] == "9ccff57aec0326722b89b85877fb5be23e63dc466022b1f7c2e0a984ccdd9424"
    assert evidence["cold_boot"] and not evidence["savestate_loaded"] and not evidence["callback_errors"]
    assert not evidence["scripted_input_schedule"]
    clean = FlsArchive(NdsImage.open("work/clean.nds").read_file("/FLS/M28.fls"))
    current = FlsArchive(NdsImage.open("out/all_routes_combined_v190_candidate.nds").read_file("/FLS/M28.fls"))
    frames = {row["frame"]: row for row in evidence["frames_captured"]}
    cases = []
    for texture, frame, dx, dy, names in (
        (22, 1520, 6, 97, ["Rafael Castor"]),
        (46, 2080, 12, 167, ["Hoodlum Joakim Bergstrom"]),
        (71, 2680, 6, 100, ["Camille Overijssel", "Lil Argot"]),
    ):
        source, target = clean.texture(texture), current.texture(texture)
        assert (source.width, source.height, source.palette, source.indices) == (
            target.width, target.height, target.palette, target.indices)
        source_image = source.render()
        capture = frames[frame]
        frame_path = Path(capture["path"])
        assert sha(frame_path.read_bytes()) == capture["PNG_sha256"]
        actual = Image.open(frame_path).convert("RGB")
        points = [(x, y, native5(source_image.getpixel((x, y))))
                  for y in range(source.height) for x in range(source.width)
                  if any(source_image.getpixel((x, y))[:3])]
        assert all(0 <= x + dx < 256 and 0 <= y + dy < 192 for x, y, _ in points)
        assert all(native5(actual.getpixel((x + dx, y + dy))) == color for x, y, color in points)
        bounds = [min(x for x, _, _ in points) + dx, min(y for _, y, _ in points) + dy,
                  max(x for x, _, _ in points) + dx + 1, max(y for _, y, _ in points) + dy + 1]
        cases.append({"texture_index": texture, "names": names, "frame": frame,
                      "frame_path": frame_path.as_posix(), "frame_sha256": capture["PNG_sha256"],
                      "native5_exact_glyph_and_outline_pixels": len(points),
                      "source_nonblack_pixel_count": len(points), "origin": [dx, dy],
                      "complete_visible_lettering_bounds": bounds,
                      "leading_and_trailing_source_glyphs_included": True})
    # Later animation frames alter ten dim pixels on the last surname edge.
    # Save this observation rather than treating one exact frame as proof of
    # every temporal effect or excluding those pixels from the exact comparison.
    source = clean.texture(71).render()
    later = Image.open(Path(frames[2720]["path"])).convert("RGB")
    differences = [{"source_x": x, "source_y": y,
                    "source_native5": list(native5(source.getpixel((x, y)))),
                    "later_native5": list(native5(later.getpixel((x + 6, y + 100))))}
                   for y in range(source.height) for x in range(source.width)
                   if any(source.getpixel((x, y))[:3]) and
                   native5(source.getpixel((x, y))) != native5(later.getpixel((x + 6, y + 100)))]
    report = {"format": "dk4-native-original-latin-name-card-proof-v1",
              "ROM_sha256": evidence["ROM_sha256"], "capture_report": evidence_path.as_posix(),
              "capture_report_sha256": sha(evidence_path.read_bytes()),
              "cold_boot": True, "savestate_loaded": False, "callback_errors": [],
              "cases": cases, "all_complete_source_letters_and_outlines_match_at_selected_frames": True,
              "later_Camille_surname_edge_observation": {"frame": 2720, "differences": differences,
                                                         "temporal_cause_not_yet_classified": True},
              "limits": "Exact complete selected-frame lettering and bounds, not hardware acceptance or proof of every animated crop/alpha/frame.",
              "ROM_changed": False, "goal_complete": False}
    path = Path("work/analysis/original_latin_cards_native_v197.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exact_cases": len(cases), "exact_nonblack_pixels": sum(c["source_nonblack_pixel_count"] for c in cases),
                      "later_edge_differences_recorded": len(differences), "ROM_changed": False}))


if __name__ == "__main__":
    main()
