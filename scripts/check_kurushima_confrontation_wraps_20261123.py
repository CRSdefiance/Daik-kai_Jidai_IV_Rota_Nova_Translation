"""Verify the stored source bindings and replay the real Nagasaki confrontation."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import headless_desmume_v193 as emulator
from scripts import stage_kurushima_confrontation_wraps_20261123 as build
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check


review = build.observed
panels = review.panels
LAST = 6230
BEFORE = review.voyage.ROOT / "capture/capture_report.json"
AFTER = build.ROOT / "replay/capture/capture_report.json"
PAIRED = build.ROOT / "paired_confrontation.json"
NATIVE = build.ROOT / "native_pages.json"
SHEET = build.ROOT / "paired_kurushima_confrontation_1_20261123.png"
PREVIEW = build.ROOT / "kurushima_native_previews_1_20261123.png"


def replay(stored):
    earlier = build.read(BEFORE)
    assert earlier["ROM_sha256"] == stored["previous"]["sha256"] == build.digest(build.parent.ROM)
    assert build.digest(build.ROM) == stored["candidate"]["sha256"]
    donor = earlier["battery_save_preloaded"]
    assert build.digest(donor["source"]) == donor["source_sha256"]
    folder = AFTER.parent.parent
    folder.mkdir()
    inputs = folder / "ordinary_inputs.json"
    events = [row for row in earlier["scripted_input_schedule"] if row["start"] <= LAST]
    build.write(inputs, events)
    frames = sorted(frame for frame in panels.shots(earlier, "_navigation.png") if frame <= LAST)
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(AFTER.parent), "--frames", str(LAST),
            "--inputs-json", str(inputs), "--press-start", "-1", "--touchscreen", "--battery-save", donor["source"],
            "--capture-every", "999999", "--capture-at", *map(str, frames)]
        emulator.main()
    finally:
        sys.argv = argv


def native_pages(stored):
    release = build.read(build.parent.RELEASE)
    ctx = build.native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = build.NdsImage.open(build.ROM)
    assert build.digest(build.ROM) == stored["candidate"]["sha256"]
    arm, kanji = image.read_file(build.ARM), image.read_file("/GRP/KANJI.FNT")
    assert arm == ctx.arm and kanji == ctx.image.read_file("/GRP/KANJI.FNT")
    paint = panels.town.clipped_renderer(ctx)
    names, expand = build.renderer.current_names(ctx), build.renderer.expander()
    records = {row["id"]: row for row in stored["records"]}
    block = build.IlnkContainer.parse(image.read_file(build.STORY)).blocks[build.BLOCK]
    pages, views = [], []
    for command in stored["commands"]:
        for ident in command["record_ids"]:
            if ident not in stored["plans"]:
                continue
            raw = bytes.fromhex(command["stored"])
            at = command["stored_offset"]
            assert block[at:at + len(raw)] == raw
            result = build.renderer.paragraph(ctx, kanji, paint, expand, None, names, records[ident],
                raw[5:raw.index(0, 6)], stored["plans"][ident])
            for layout in result["layouts"]:
                page, = layout["pages"]
                assert page["native_independent_plane_equal"]
                physical = bytes.fromhex(page["native_plane_hex"])
                image = Image.new("RGB", (256, 384), (250, 245, 226))
                raster = Image.frombytes("L", (216, 64), bytes(12 if px else 245 for px in physical))
                image.paste(raster, (16, 296))
                views.append((f"{ident} / {layout['scope']}", image))
            pages.append(result)
    assert len(views) == 6 and len(pages) == 3
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": NATIVE})
    visual, = sheets("kurushima_native_previews", views, (0, 288, 256, 368))
    assert visual == build.reference(PREVIEW)
    build.write(NATIVE, dict(candidate_sha256=stored["candidate"]["sha256"], stored=build.reference(build.STORED),
        records=pages, visual=visual, complete_native_pages=len(views)))
    print("Verified six complete native pages, including default and three alternate captain-name widths.")


def verify(stored):
    earlier, after, native = map(build.read, (BEFORE, AFTER, NATIVE))
    assert after["ROM_sha256"] == native["candidate_sha256"] == stored["candidate"]["sha256"] == build.digest(build.ROM)
    assert earlier["ROM_sha256"] == stored["previous"]["sha256"]
    assert after["cold_boot"] and not after["savestate_loaded"] and not after["callback_errors"]
    assert not any(v for k, v in after.items() if k.startswith("synthetic_"))
    assert after["frames"] == LAST and after["scripted_input_schedule"] == [
        row for row in earlier["scripted_input_schedule"] if row["start"] <= LAST]
    for field in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
        assert earlier["battery_save_preloaded"][field] == after["battery_save_preloaded"][field]
    old, new = panels.shots(earlier, "_navigation.png"), panels.shots(after, "_cold_boot.png")
    frames = {n for n in old if n <= LAST}
    assert frames == set(after["exact_requested_capture_frames"]) <= new.keys()
    wanted = {frame: row for frame, row in zip(review.STORY_FRAMES, stored["records"], strict=True)
              if row["id"] in stored["plans"]}
    assert set(wanted) == {5230, 5430, 5630}
    results = {row["id"]: row for row in native["records"]}
    font = GameAsciiFont.from_arm9(build.NdsImage.open(build.ROM).read_file(build.ARM))
    checked, unchanged, views = [], [], []
    for frame in sorted(frames):
        a, b = (panels.picture(group[frame]) for group in (old, new))
        bounds = ImageChops.difference(a, b).getbbox()
        if frame in wanted:
            row = wanted[frame]
            layout = results[row["id"]]["layouts"][0]
            page, = layout["pages"]
            plane = bytes.fromhex(page["native_plane_hex"])
            assert mask_check(plane, 216, b)
            assert bounds and 16 <= bounds[0] < bounds[2] <= 232 and 296 <= bounds[1] < bounds[3] <= 360
            plate = panels.nameplate(font, row["speaker"], b)
            assert plate == panels.nameplate(font, row["speaker"], a)
            checked.append(dict(id=row["id"], frame=frame, before=old[frame], after=new[frame], diff_bounds=bounds,
                nameplate=plate, full_native_plane_sha256=build.sha256(plane).hexdigest(), lines=layout["lines"]))
            views.extend(((f"{frame} / previous", a), (f"{frame} / revised", b)))
        else:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
    assert LAST in unchanged
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": PAIRED})
    visual, = sheets("paired_kurushima_confrontation", views, (0, 272, 256, 380))
    assert visual == build.reference(SHEET)
    build.write(PAIRED, dict(candidate_sha256=after["ROM_sha256"], previous_sha256=earlier["ROM_sha256"],
        baseline=build.reference(BEFORE), replay=build.reference(AFTER), native=build.reference(NATIVE), visual=visual,
        revised_pages=checked, identical_control_frames=unchanged, ordinary_replay=True, sea_return_exact=True))
    print(f"Verified three revised pages and {len(unchanged)} exact control frames in ordinary gameplay.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("native_pages", "replay", "verify"))
    globals()[cli.parse_args().action](build.read(build.STORED))
