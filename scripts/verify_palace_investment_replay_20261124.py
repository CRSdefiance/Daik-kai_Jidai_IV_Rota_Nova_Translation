"""Replay both served Palace branches and verify the changed dialogue holds."""

import sys
from argparse import ArgumentParser

from PIL import Image, ImageChops, ImageDraw

from scripts import headless_desmume_v193 as harness
from scripts import register_tunis_palace_refusal_20261124 as tunis_release
from scripts import stage_palace_investment_wording_20261124 as stage
from scripts import verify_riga_town_services_20261124 as riga
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write

OUT = stage.ROOT / "paired_gameplay.json"
SHEET = stage.ROOT / "palace_investment_paired.png"
panels = riga.panels
HOLDS = {"riga": {5600: (1160, None)}, "tunis": {14600: (1151, "Bergstrom"), 15400: (1160, None)}}


def baseline(city, edit, *, historical=False):
    if city == "riga":
        receipt = read(riga.OUT)
        assert receipt["candidate_sha256"] == edit["predecessor_sha256"]
        path, = (r for r in receipt["evidence"] if r["path"].endswith("capture_report.json"))
        expected, suffix = edit["predecessor_sha256"], "_navigation.png"
    elif not historical:
        path = reference(stage.ROOT / "tunis_parent/capture_report.json")
        expected, suffix = edit["predecessor_sha256"], "_cold_boot.png"
        _, old, _ = baseline(city, edit, historical=True)
        actual = read(path["path"])
        assert actual["scripted_input_schedule"] == old["scripted_input_schedule"]
        assert actual["battery_save_preloaded"]["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    else:
        release = read(tunis_release.RELEASE)
        receipt = read(tunis_release.VERIFY / "paired_gameplay.json")
        assert release["candidate_sha256"] == receipt["candidate_sha256"] and receipt["ordinary_saved_game"]
        path, expected, suffix = receipt["after"], release["candidate_sha256"], "_cold_boot.png"
    assert digest(path["path"]) == path["sha256"]
    capture = read(path["path"])
    assert capture["ROM_sha256"] == expected
    return path, capture, panels.shots(capture, suffix)


def replay(city, *, predecessor=False):
    edit = read(stage.OUT)
    _, old, frames = baseline(city, edit, historical=city == "tunis")
    assert edit["candidate_sha256"] == digest(stage.ROM)
    donor = old["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    candidate = stage.parent.ROM if predecessor else stage.ROM
    assert digest(candidate) == edit["predecessor_sha256" if predecessor else "candidate_sha256"]
    store = stage.ROOT / (f"{city}_parent" if predecessor else city)
    store.mkdir()
    inputs = store / "inputs.json"
    write(inputs, old["scripted_input_schedule"])
    original = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(candidate), "--out", str(store), "--frames", str(old["frames"]),
                    "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
                    "--press-start", "-1", "--capture-every", "999999", "--capture-at", *map(str, sorted(frames))]
        harness.main()
    finally:
        sys.argv = original


def verify():
    edit = read(stage.OUT)
    image = NdsImage.open(stage.ROM)
    font = riga.tools.GameAsciiFont.from_arm9(image.read_file(stage.ARM))
    specs = {row["message_id"]: row["cases"] for row in edit["records"]}
    figures, routes = [], {}
    for city, changed in HOLDS.items():
        old_ref, old, before = baseline(city, edit)
        new_path = stage.ROOT / city / "capture_report.json"
        new = read(new_path)
        assert digest(stage.ROM) == new["ROM_sha256"] == edit["candidate_sha256"]
        assert new["frames"] == old["frames"] and new["scripted_input_schedule"] == old["scripted_input_schedule"]
        for report in (old, new):
            assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
            assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
            assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        assert old["battery_save_preloaded"]["source_sha256"] == new["battery_save_preloaded"]["source_sha256"]
        after = panels.shots(new, "_cold_boot.png")
        assert before.keys() <= after.keys()
        unchanged, revised = [], []
        for frame in sorted(before):
            a, b = (panels.picture(rows[frame]) for rows in (before, after))
            box = ImageChops.difference(a, b).getbbox()
            if frame not in changed:
                assert box is None, (city, frame, box)
                unchanged.append(frame)
                continue
            assert box and 16 <= box[0] < box[2] <= 250 and 296 <= box[1] < box[3] <= 360, (city, frame, box)
            k, address = changed[frame]
            case, = [row for row in specs[k] if row["address"] == address]
            lines = case["layout"]["lines"]
            mask = panels.exact_body(font, lines, b)
            nameplate = panels.nameplate(font, "King", b)
            assert nameplate == panels.nameplate(font, "King", a)
            revised.append(dict(frame=frame, message_id=k, address=address, lines=lines, pixel_bounds=box,
                                complete_body=mask, nameplate=nameplate, previous=before[frame], candidate=after[frame]))
            figures.append((city.title(), k, a, b))
        assert {r["frame"] for r in revised} == set(changed) and new["frames"] in unchanged
        routes[city] = dict(previous=old_ref, candidate=reference(new_path), revised=revised, unchanged_frames=unchanged)
    sheet = Image.new("RGB", (1024, 240 * len(figures)), "#263238")
    draw = ImageDraw.Draw(sheet)
    for y, (city, key, before, after) in enumerate(figures):
        top = y * 240
        for x, (label, screen) in enumerate((("Previous", before), ("Candidate", after))):
            left = x * 512
            draw.text((left + 4, top + 4), f"{city} / {key} / {label}", fill="white")
            sheet.paste(screen.crop((0, 274, 256, 384)).resize((512, 220), Image.Resampling.NEAREST), (left, top + 20))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=edit["candidate_sha256"], predecessor_sha256=edit["predecessor_sha256"],
        ordinary_gameplay=True, routes=routes, sheets=[reference(SHEET)],
        changed_holds=len(figures), unchanged_holds=sum(len(r["unchanged_frames"]) for r in routes.values())))
    print(f"Verified {len(figures)} changed Palace dialogue holds and {sum(len(r['unchanged_frames']) for r in routes.values())} matching companion frames.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("riga", "tunis", "tunis-parent", "verify"))
    picked = parser.parse_args().action
    if picked == "verify":
        verify()
    elif picked == "tunis-parent":
        replay("tunis", predecessor=True)
    else:
        replay(picked)