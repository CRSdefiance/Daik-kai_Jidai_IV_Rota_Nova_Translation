"""Verify the two revised bargaining holds against their ordinary predecessor."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_lisbon_guild_bargaining_20261125 as replay
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


draft, baseline = replay.draft, replay.draft.review
panels = baseline.panels
OUT = draft.OUT.with_name("lisbon_guild_bargaining_paired_20261125.json")
SHEET = OUT.with_suffix(".png")
ADVANCE = (224, 360, 240, 376)
BODY = (16, 296, 245, 360)


def main():
    proposed = read(replay.STAGED)
    previous, next_path = replay.play.ROOT / "capture/capture_report.json", replay.CAPTURE / "capture_report.json"
    old, new, original, preflight = map(read, (previous, next_path, baseline.OUT, draft.OUT))
    assert old["ROM_sha256"] == original["candidate_sha256"] == proposed["parent"]["sha256"]
    assert new["ROM_sha256"] == proposed["candidate"]["sha256"] == digest(replay.ROM)
    assert original["ordinary_gameplay"] and proposed["exact_parent_inverse"]
    assert proposed["proposal"] == reference(draft.OUT) and preflight["all_placements_same_allocation"]
    assert original["source_replay"]["capture"] == reference(previous)
    for field in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "frames"):
        assert old[field] == new[field]
    for run in (old, new):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(v for key, v in run.items() if key.startswith("synthetic_"))
    prior_donor, donor = (run["battery_save_preloaded"] for run in (old, new))
    assert prior_donor["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    a, b = panels.shots(old, "_navigation.png"), panels.shots(new, "_cold_boot.png")
    assert set(a) == set(replay.FRAMES) and set(a) <= set(b)
    unchanged = sorted(set(a) - set(replay.REVISED_HOLDS))
    original_rom, new_rom = map(NdsImage.open, (replay.current.ROM, replay.ROM))
    arm = new_rom.read_file(replay.current.ARM)
    assert arm == original_rom.read_file(replay.current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    by_id = {row["message_ID"]: row for row in preflight["records"]}
    rows, previews = [], []
    for n in replay.FRAMES:
        left, right = panels.picture(a[n]), panels.picture(b[n])
        diff = ImageChops.difference(left, right)
        if n in unchanged:
            assert diff.getbbox() is None, (n, diff.getbbox())
            continue
        key = replay.REVISED_HOLDS[n]
        current, revised = by_id[key]["native_layouts"]
        assert current["version"] == "Current" and revised["version"] == "Proposed"
        bloom = []
        for frame, layout in ((left, current), (right, revised)):
            panel = panels.exact_body(font, layout["lines"], frame)
            name = panels.nameplate(font, "Julio Erneco", frame)
            bloom.append(dict(body_glyph_pixels=panel, nameplate=name))
        assert bloom[0]["nameplate"] == bloom[1]["nameplate"]
        diff.paste((0, 0, 0), ADVANCE)
        change = diff.getbbox()
        assert change and BODY[0] <= change[0] < change[2] <= BODY[2] and BODY[1] <= change[1] < change[3] <= BODY[3]
        rows.append(dict(message_ID=key, frame=n, baseline=a[n], installed=b[n], proposed_lines=revised["lines"],
                         changed_body_bounds=change, before_after_checks=bloom))
        previews += [(f"{key} current", left), (f"{key} proposed", right)]
    sheet = Image.new("RGB", (1024, 816), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (label, frame) in enumerate(previews):
        x, y = (i % 2) * 512, (i // 2) * 408
        draw.text((x + 10, y + 7), label, fill="white")
        sheet.paste(frame.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x, y + 22))
    sheet.save(SHEET)
    write(OUT, dict(candidate=proposed["candidate"], parent=proposed["parent"], revised_holds=rows,
        exact_companion_frames=unchanged, baseline=reference(baseline.OUT), proposal=reference(draft.OUT),
        replay=reference(next_path), baseline_capture=reference(previous), sheet=reference(SHEET),
        observed_wallets={frame: original["state"][str(frame)]["wallet"] for frame in (37300, 40660, 42820)},
        ordinary_gameplay=True))
    print("Verified both revised Guild holds and 23 pixel-exact companion screens.")


if __name__ == "__main__":
    main()
