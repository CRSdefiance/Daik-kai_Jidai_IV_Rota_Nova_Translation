"""Replay the ordinary Riga sequence and verify the three changed dialogue holds."""

import sys
from argparse import ArgumentParser

from PIL import Image, ImageChops, ImageDraw

from scripts import headless_desmume_v193 as harness
from scripts import stage_riga_recruitment_20261124 as stage
from scripts import verify_riga_tavern_20261124 as baseline
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write

RUN = stage.ROOT / "ordinary_replay"
BEFORE = baseline.play.ROOT / "capture/capture_report.json"
AFTER = RUN / "capture_report.json"
OUT = stage.ROOT / "paired_gameplay.json"
SHEET = stage.ROOT / "riga_recruitment_paired.png"
CHANGED = {12000: (1042, 49), 13200: (71, 120), 15200: (71, 15)}
panels = baseline.panels


def replay():
    original, edit, evidence = map(read, (BEFORE, stage.OUT, baseline.OUT))
    assert original["ROM_sha256"] == evidence["candidate_sha256"] == edit["predecessor_sha256"]
    assert edit["candidate_sha256"] == digest(stage.ROM)
    donor = original["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == evidence["donor"]["sha256"]
    RUN.mkdir()
    inputs = RUN / "inputs.json"
    write(inputs, original["scripted_input_schedule"])
    frames = sorted(panels.shots(original, "_navigation.png"))
    args = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(stage.ROM), "--out", str(RUN), "--frames", str(baseline.END),
                    "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
                    "--press-start", "-1", "--capture-every", "999999", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = args


def verify():
    before, after, edit = map(read, (BEFORE, AFTER, stage.OUT))
    assert before["ROM_sha256"] == edit["predecessor_sha256"]
    assert after["ROM_sha256"] == edit["candidate_sha256"] == digest(stage.ROM)
    assert before["scripted_input_schedule"] == after["scripted_input_schedule"]
    assert before["frames"] == after["frames"] == baseline.END
    for report in (before, after):
        assert report["cold_boot"] and not report["callback_errors"] and not report["savestate_loaded"]
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert before["battery_save_preloaded"]["source_sha256"] == after["battery_save_preloaded"]["source_sha256"]
    old = panels.shots(before, "_navigation.png")
    new = panels.shots(after, "_cold_boot.png")
    assert old.keys() <= new.keys()
    image = NdsImage.open(stage.ROM)
    font = baseline.prior.GameAsciiFont.from_arm9(image.read_file(stage.ARM))
    specs = {row["message_id"]: row["cases"] for row in edit["records"]}
    unchanged, revised = [], []
    sheet = Image.new("RGB", (1024, 720), "#263238")
    draw = ImageDraw.Draw(sheet)
    for frame in sorted(old):
        a, b = (panels.picture(items[frame]) for items in (old, new))
        bounds = ImageChops.difference(a, b).getbbox()
        if frame not in CHANGED:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
            continue
        assert bounds and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 360, (frame, bounds)
        key, value = CHANGED[frame]
        case, = (row for row in specs[key] if row["count"] == value)
        ink = panels.exact_body(font, case["lines"], b)
        speaker = panels.nameplate(font, baseline.GERHARD, b)
        buttons = [panels.find_mask(font, label, b, box) for label, box in
                   (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
        y = len(revised) * 240
        for index, (label, screen) in enumerate((("Before", a), ("Revised", b))):
            x = index * 512
            draw.text((x + 4, y + 4), f"{label} / {key} / {value}", fill="white")
            sheet.paste(screen.crop((0, 274, 256, 384)).resize((512, 220), Image.Resampling.NEAREST), (x, y + 20))
        revised.append(dict(frame=frame, message_id=key, count=value, lines=case["lines"], bounds=bounds,
                            before=old[frame], after=new[frame], pixels=ink, nameplate=speaker, choices=buttons))
    assert len(revised) == len(CHANGED) and baseline.END in unchanged
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=edit["candidate_sha256"], predecessor_sha256=edit["predecessor_sha256"],
                    ordinary_gameplay=True, before=reference(BEFORE), after=reference(AFTER),
                    revised=revised, unchanged_frames=unchanged, sheets=[reference(SHEET)]))
    print(f"Verified {len(revised)} revised Riga holds and {len(unchanged)} matching gameplay frames.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "verify"))
    globals()[parser.parse_args().action]()
