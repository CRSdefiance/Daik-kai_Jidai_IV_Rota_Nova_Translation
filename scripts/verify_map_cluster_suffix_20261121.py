"""Check complete live map-marker text and the measured six-pixel font layout."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_map_cluster_suffix_20261121 as stage


base = stage.base
ROOT = stage.ROOT / "playback"
REPORT = ROOT / "capture/capture_report.json"
PROOF = ROOT / "verified.json"
SHEET = ROOT / "world_map_label_comparison.png"
INK = (0, 8, 0)
CELL = 6
BOX = (60, 214, 224, 242)


def ink_mask(font, words):
    mask = set()
    for index, sign in enumerate(words):
        pixels = font.decode(sign)
        mask.update((index * CELL + x, y) for y in range(11) for x in range(CELL) if pixels.getpixel((x, y)))
    return mask


def capture_mask(font, image, words, bounds=BOX):
    left, top, right, bottom = bounds
    ink = {(x, y) for y in range(top, bottom) for x in range(left, right) if image.getpixel((x, y)) == INK}
    ideal = ink_mask(font, words)
    dx = min(x for x, _ in ink) - min(x for x, _ in ideal)
    dy = min(y for _, y in ink) - min(y for _, y in ideal)
    expected = {(x + dx, y + dy) for x, y in ideal}
    assert ink == expected, (words, len(ink), len(expected), len(ink ^ expected))
    assert left < dx and dx + len(words) * CELL < right and top < dy and dy + 11 < bottom
    return dict(text=words, origin=[dx, dy], complete_exact_ink=len(ink))


def main():
    assert not PROOF.exists()
    staged = base.load(stage.PROOF)
    old_trace = base.load(stage.context.ROOT / "playback.json")
    old_path = Path(old_trace["report"])
    old, new = map(base.load, (old_path, REPORT))
    assert base.digest(old_path) == old_trace["report_sha256"]
    assert old["ROM_sha256"] == staged["predecessor_sha256"] and new["ROM_sha256"] == staged["candidate_sha256"] == base.digest(stage.ROM)
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] and r["frames"] == 11801 for r in (old, new))
    for key in ("core_options", "scripted_input_schedule", "exact_requested_capture_frames"):
        assert old[key] == new[key]
    assert all(old["battery_save_preloaded"][k] == new["battery_save_preloaded"][k]
               for k in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"))
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.native.ARM))
    frames = [{r["frame"]: r for r in version["frames_captured"]} for version in (old, new)]
    assert frames[0].keys() == frames[1].keys()
    changed, unchanged, exact, comparisons = [], [], [], []
    expected_markers = {5000: "Syracuse", 6000: "Manuel Fleet", 11800: "Manuel Fleet", 11801: "Manuel Fleet"}
    for n in sorted(frames[0]):
        pair = [Image.open(version[n]["path"]).convert("RGB") for version in frames]
        for version in frames:
            assert base.digest(version[n]["path"]) == version[n]["PNG_sha256"]
        delta = ImageChops.difference(*pair).getbbox()
        if delta is None:
            unchanged.append(n)
            continue
        assert n in expected_markers and 212 <= delta[1] < delta[3] <= 270, (n, delta)
        changed.append(dict(frame=n, changed_rectangle=delta))
        comparisons.append((n, *[panel.crop((0, 211, 256, 271)) for panel in pair]))
        label = expected_markers[n]
        bounds = (102, 228, 204, 246) if n == 5000 else BOX
        masks = [capture_mask(font, image, label + ending, bounds)
                 for image, ending in zip(pair, (" etc.", " + more"), strict=True)]
        coordinate = None
        if n == 5000:
            coordinate = [capture_mask(font, image, "N  37 E  14", (102, 248, 204, 266)) for image in pair]
            assert coordinate[0]["complete_exact_ink"] == coordinate[1]["complete_exact_ink"]
        exact.append(dict(frame=n, before=masks[0], after=masks[1], unchanged_coordinate=coordinate))
    assert {r["frame"] for r in exact} == expected_markers.keys() and 10600 in unchanged

    logical_examples = [bytes.fromhex(r["expected_exact"])[:-1].decode("ascii") for r in staged["native_cases"][-5:]]
    assert all(text.endswith(" + more") and len(text) * CELL + 8 <= 256 for text in logical_examples)
    comparisons = [row for row in comparisons if row[0] != 11801]
    sheet = Image.new("RGB", (1024, 142 * len(comparisons) + 45 * len(logical_examples)), "#242d35")
    notes = ImageDraw.Draw(sheet)
    height = 0
    for n, old_crop, new_crop in comparisons:
        for i, crop in enumerate((old_crop, new_crop)):
            notes.text((4 + i * 512, height + 2), ("Before" if i == 0 else "After") + f" at frame {n}", fill="white")
            sheet.paste(crop.resize((512, 120), Image.Resampling.NEAREST), (i * 512, height + 18))
        height += 142
    for text in logical_examples:
        label = Image.new("RGB", (len(text) * CELL + 8, 17), "white")
        for x, y in ink_mask(font, text):
            label.putpixel((x + 4, y + 3), INK)
        sheet.paste(label.resize((label.width * 2, 34), Image.Resampling.NEAREST), (8, height + 3))
        height += 45
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], original_replay=str(old_path),
        revised_replay=str(REPORT), compared_frames=len(frames[0]), unchanged_frames=unchanged,
        changed_frames=changed, complete_live_masks=exact, ordinary_world_map_controls=True,
        existing_copied_fleet_save=True, hardware=False, verified_cell_advance=CELL,
        offline_width_examples=[dict(text=text, text_width=len(text) * CELL, preview_width=8 + len(text) * CELL)
                                for text in logical_examples],
        evidence={str(p): base.digest(p) for p in (old_path, REPORT, SHEET, stage.PROOF)},
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET))))
    print(f"Verified complete World Map masks and {len(unchanged)} identical replay frames.")


if __name__ == "__main__":
    main()
