"""Verify both reflowed Clifford rumor panels against ordinary London play."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_london_square_rumor_20261125 as stage
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


panels = stage.review.panels
OUT = stage.review.OUT.with_name("london_square_rumor_paired_20261125.json")
SHEET = OUT.with_suffix(".png")


def main():
    prior_path = stage.play.ROOT / "capture/capture_report.json"
    next_path = stage.CAPTURE / "capture_report.json"
    old, new, stored, native, source = map(read, (prior_path, next_path, stage.STAGED, stage.NATIVE, stage.review.OUT))
    assert old["ROM_sha256"] == source["candidate_sha256"] == stored["parent"]["sha256"]
    assert new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(stage.ROM)
    assert source["ordinary_gameplay"] and stored["exact_parent_inverse"]
    assert stored["proposal"] == reference(stage.NATIVE) and source["evidence"]["capture"] == reference(prior_path)
    for field in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "frames"):
        assert old[field] == new[field]
    for run in (old, new):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(v for key, v in run.items() if key.startswith("synthetic_"))
    previous_donor, donor = (run["battery_save_preloaded"] for run in (old, new))
    assert previous_donor["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    a, b = panels.shots(old, "_navigation.png"), panels.shots(new, "_cold_boot.png")
    assert set(a) == set(stage.FRAMES) and set(a) <= set(b)
    arm = NdsImage.open(stage.ROM).read_file(stage.current.ARM)
    assert arm == NdsImage.open(stage.current.ROM).read_file(stage.current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    record, = native["records"]
    layouts = record["native_layouts"]
    assert [tuple(row["lines"]) for row in layouts] == [stage.OLD, stage.LINES]
    companion, revised, pairs = [], [], []
    for frame in stage.FRAMES:
        before, after = panels.picture(a[frame]), panels.picture(b[frame])
        difference = ImageChops.difference(before, after)
        if frame not in stage.CHANGED:
            assert difference.getbbox() is None, (frame, difference.getbbox())
            companion.append(frame)
            continue
        previous_ink = panels.exact_body(font, stage.OLD, before)
        new_ink = panels.exact_body(font, stage.LINES, after)
        nameplate = panels.nameplate(font, "Shopkeeper", after)
        assert panels.nameplate(font, "Shopkeeper", before) == nameplate
        difference.paste((0, 0, 0), (224, 360, 240, 376))
        bounds = difference.getbbox()
        assert bounds and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 360
        revised.append(dict(frame=frame, before=a[frame], after=b[frame], body_delta_bounds=bounds,
                            prior_body_ink=previous_ink, new_body_ink=new_ink, nameplate=nameplate))
        pairs.append((frame, before, after))
    sheet = Image.new("RGB", (1024, 242 * len(pairs)), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, (frame, before, after) in enumerate(pairs):
        y = index * 242
        for column, (label, screen) in enumerate((("Before", before), ("Candidate", after))):
            x = column * 512
            draw.text((x + 8, y + 2), f"{frame} / {label}", fill="white")
            sheet.paste(screen.crop((0, 272, 256, 380)).resize((512, 216), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    write(OUT, dict(candidate=stored["candidate"], parent=stored["parent"], ordinary_gameplay=True,
        revised_holds=revised, exact_companion_frames=companion, source_review=reference(stage.review.OUT),
        preflight=reference(stage.NATIVE), baseline=reference(prior_path), replay=reference(next_path), sheet=reference(SHEET)))
    print(f"Both London Square rumor holds passed with {len(companion)} pixel-exact companion screens.")


if __name__ == "__main__":
    main()
