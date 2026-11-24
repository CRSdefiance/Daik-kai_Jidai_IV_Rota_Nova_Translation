"""Replay the edited Genoa panels through their original choices and transitions."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from scripts import headless_desmume_v193 as harness
from scripts import stage_genoa_dialogue_20261123 as build
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_moonlit_violin_20261121 import bytes_for


ROOT = build.ROOT / "ordinary_genoa"
CAPTURE = ROOT / "capture/capture_report.json"
REPORT, SHEET = ROOT / "paired_genoa_gameplay.json", ROOT / "paired_genoa_gameplay.png"
CHANGED = dict(zip(build.IDS, (13900, 15300, 4200), strict=True))
CONTROLS = (3500, 3800, 4000, 4400, 5600, 5800, 6100, 9700, 13500, 13700, 14100, 15100, 15500, 17600, 17850, 18100)
FRAMES = sorted(set(CHANGED.values()) | set(CONTROLS))


def inputs():
    ledger = read(build.gameplay.OUT)["ordinary_gameplay"]["genoa"]["evidence"]
    source, donor = ledger["capture"], ledger["donor"]
    assert digest(source["path"]) == source["sha256"] and digest(donor["path"]) == donor["sha256"]
    history = read(source["path"])
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert history["battery_save_preloaded"]["source_sha256"] == donor["sha256"]
    schedule = [item for item in history["scripted_input_schedule"] if item["start"] <= FRAMES[-1]]
    return source, history, donor, schedule


def replay():
    proof = read(build.STORED)
    assert reference(build.ROM) == proof["staged"]
    _, _, donor, schedule = inputs()
    ROOT.mkdir()
    commands = ROOT / "inputs.json"
    write(commands, schedule)
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(build.ROM), "--out", str(CAPTURE.parent),
                    "--frames", str(FRAMES[-1]), "--inputs-json", str(commands),
                    "--press-start", "-1", "--touchscreen", "--battery-save", donor["path"],
                    "--capture-every", "999999", "--capture-at", *map(str, FRAMES)]
        harness.main()
    finally:
        sys.argv = argv
    assert digest(donor["path"]) == donor["sha256"]


def verify():
    source, old, donor, schedule = inputs()
    stored, run = map(read, (build.STORED, CAPTURE))
    assert old["ROM_sha256"] == stored["predecessor"]["sha256"]
    assert run["ROM_sha256"] == stored["staged"]["sha256"] == digest(build.ROM)
    assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
    assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
    assert run["scripted_input_schedule"] == schedule and run["frames"] == FRAMES[-1]
    assert run["exact_requested_capture_frames"] == FRAMES
    assert run["battery_save_preloaded"]["source_sha256"] == donor["sha256"]
    before, after = shots(old, "_navigation.png"), shots(run, "_cold_boot.png")
    controls = []
    for frame in CONTROLS:
        assert picture(before[frame]).tobytes() == picture(after[frame]).tobytes(), frame
        controls.append(dict(frame=frame, predecessor=before[frame], candidate=after[frame]))

    image = NdsImage.open(build.ROM)
    arm = image.read_file(build.ARM)
    blocks = IlnkContainer.parse(image.read_file(build.STORY)).blocks
    kanji = image.read_file("/GRP/KANJI.FNT")
    font = GameAsciiFont.from_arm9(arm)
    render = build.gameplay.town.clipped_renderer(SimpleNamespace(arm=arm, image=image))
    rows = {row["id"]: row for row in read(build.gameplay.OUT)["ordinary_gameplay"]["genoa"]["story"]}
    pictures, pages = [], []
    for change in stored["changed"]:
        ident, frame, start = change["id"], CHANGED[change["id"]], change["command_offset"]
        raw = bytes.fromhex(change["after_hex"])
        assert blocks[change["block"]][start:start + len(raw)] == raw
        body = bytes_for(raw)
        page, = render(arm, kanji, body)["pages"]
        assert page["native_independent_plane_equal"]
        plane = bytes.fromhex(page["native_plane_hex"])
        previous, current = picture(before[frame]), picture(after[frame])
        assert sha256(plane).hexdigest() == change["page_sha256"]
        assert build.gameplay.mask_check(plane, 216, current), (ident, frame)
        bbox = ImageChops.difference(previous, current).getbbox()
        assert bbox and 16 <= bbox[0] < bbox[2] <= 232 and 296 <= bbox[1] < bbox[3] <= 360
        name = rows[ident]["speaker"]
        plate = build.gameplay.nameplate(font, name, current)
        assert plate == build.gameplay.nameplate(font, name, previous)
        pictures.append((ident, previous, current))
        pages.append(dict(id=ident, frame=frame, speaker=name, complete_nameplate=plate,
            candidate=after[frame], predecessor=before[frame], stored_command_hex=raw.hex(),
            complete_native_mask=change["page_sha256"], changed_ink_bounds=bbox, single_page=True))

    sheet = Image.new("RGB", (1040, len(pictures) * 242), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (ident, before_page, after_page) in enumerate(pictures):
        for j, (label, screen) in enumerate((("Previous", before_page), ("Revised", after_page))):
            x, y = j * 520 + 4, i * 242
            draw.text((x, y + 2), f"{ident} / {label}", fill="white")
            panel = screen.crop((0, 272, 256, 380)).resize((512, 216), Image.Resampling.NEAREST)
            sheet.paste(panel, (x, y + 20))
    sheet.save(SHEET)
    write(REPORT, dict(candidate_sha256=run["ROM_sha256"], predecessor_sha256=old["ROM_sha256"],
        ordinary_controller_and_stylus_inputs=True, changed_pages=pages, unchanged_control_frames=controls,
        observed_choices=["Yes...", "Ask what you don't know"], observed_tavern_return=True,
        previous_capture=source, revised_capture=reference(CAPTURE), donor=donor, visual=reference(SHEET)))
    print(f"Verified all {len(pages)} revised Genoa pages and {len(controls)} unchanged control frames.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    replay() if cli.parse_args().action == "replay" else verify()
