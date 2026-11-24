"""Replay the ordinary Syracuse Market path on the staged digit correction."""

import sys
from argparse import ArgumentParser

from PIL import Image, ImageChops, ImageDraw

from scripts import headless_desmume_v193 as harness
from scripts import stage_price_info_digits_20261124 as build
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


observed = build.observed
panels = observed.panels
RUN = build.ROOT / "ordinary_replay"
BEFORE = observed.play.ROOT / "capture/capture_report.json"
AFTER = RUN / "capture_report.json"
OUT = build.ROOT / "paired_gameplay.json"
SHEET = build.ROOT / "price_info_digits_paired.png"
HOLD = 13700


def replay():
    previous, stored, baseline = map(read, (BEFORE, build.STORED, observed.OUT))
    assert previous["ROM_sha256"] == baseline["candidate_sha256"] == stored["predecessor_sha256"]
    assert digest(build.ROM) == stored["candidate_sha256"]
    RUN.mkdir()
    inputs = RUN / "inputs.json"
    write(inputs, previous["scripted_input_schedule"])
    donor = previous["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == baseline["original_battery_save"]["sha256"]
    frames = sorted(panels.shots(previous, "_navigation.png"))
    args = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(RUN), "--frames", str(observed.END),
                    "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
                    "--press-start", "-1", "--capture-every", "999999", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = args


def verify():
    a, b, stored = map(read, (BEFORE, AFTER, build.STORED))
    assert a["ROM_sha256"] == stored["predecessor_sha256"]
    assert b["ROM_sha256"] == stored["candidate_sha256"] == digest(build.ROM)
    assert a["scripted_input_schedule"] == b["scripted_input_schedule"] and a["frames"] == b["frames"] == observed.END
    for report in (a, b):
        assert report["cold_boot"] and not report["callback_errors"] and not report["savestate_loaded"]
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert a["battery_save_preloaded"]["source_sha256"] == b["battery_save_preloaded"]["source_sha256"]
    old, new = panels.shots(a, "_navigation.png"), panels.shots(b, "_cold_boot.png")
    assert old.keys() <= new.keys()
    unchanged = []
    quote = None
    clean, actual = (NdsImage.open(path) for path in (build.parent.ROM, build.ROM))
    kanji = actual.read_file("/GRP/KANJI.FNT")
    assert kanji == clean.read_file("/GRP/KANJI.FNT")
    for frame in sorted(old):
        before, after = (panels.picture(group[frame]) for group in (old, new))
        bounds = ImageChops.difference(before, after).getbbox()
        if frame != HOLD:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
            continue
        assert bounds and 84 <= bounds[0] < bounds[2] <= 225 and 243 <= bounds[1] < bounds[3] <= 275
        source = observed.map_quote(before, clean.read_file(build.ARM), kanji)
        target = observed.map_quote(after, actual.read_file(build.ARM), kanji, compact=True)
        quote = dict(frame=frame, previous=source, revised=target, bounds=bounds)
        sheet = Image.new("RGB", (1056, 194), "#263238")
        labels = ImageDraw.Draw(sheet)
        for index, (label, screen) in enumerate((("Before", before), ("Regular digits", after))):
            x = index * 528
            labels.text((x + 8, 8), label, fill="white")
            crop = screen.crop((64, 235, 240, 291))
            sheet.paste(crop.resize((528, 168), Image.Resampling.NEAREST), (x, 26))
        sheet.save(SHEET)
    assert quote and observed.END in unchanged
    write(OUT, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        ordinary_gameplay=True, before=reference(BEFORE), after=reference(AFTER), quote=quote,
        unchanged_frames=unchanged, sheets=[reference(SHEET)]))
    print(f"Verified the complete regular-digit fee quote and {len(unchanged)} matching gameplay frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    globals()[cli.parse_args().action]()
