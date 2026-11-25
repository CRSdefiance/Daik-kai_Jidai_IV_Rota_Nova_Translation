"""Compare the staged name glyphs and legacy save against ordinary gameplay."""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STOP, machine
from scripts.stage_captain_name_latin_20261119 import ARM, PROOF_NAME, ROM_NAME, write
from scripts.verify_all_items_gallery_v535 import glyph_pixels
from scripts.verify_captain_name_storage_20261119 import ROUNDTRIP
from scripts.verify_rafael_custom_name_20261119 import (
    NAME,
    REPORT,
    ROM_HASH,
    digest,
    read,
    require_string,
    snapshot,
)

REGULAR = b"RafaelMaa"
BODY = b"Say, " + REGULAR + b"... what \n do you think of men who go to sea? "
EDITOR_COLOR, BODY_COLOR, LABEL_COLOR = (230, 230, 230), (0, 8, 0), (98, 97, 98)


def frame(report, n, navigation=False):
    kind = "_navigation.png" if navigation else "_cold_boot.png"
    png = [row for row in report["frames_captured"] if row["path"].endswith(kind)]
    _, picture = snapshot(png, n, "PNG_sha256")
    key = "read_only_pause_RAM_snapshots" if navigation else "read_only_capture_RAM_snapshots"
    memory, ram = snapshot(report[key], n, "sha256")
    with Image.open(picture["path"]) as photo:
        image = photo.convert("RGB")
    return image, memory, {"picture": picture, "read_only_RAM": ram}


def glyphs(font, image, text, origin, color, right):
    x0, y0 = origin
    expected = glyph_pixels(font, b"", (), text, x0, y0, 6)
    actual = {(x, y) for x in range(x0, right) for y in range(y0, y0 + 11) if image.getpixel((x, y)) == color}
    assert actual == expected, (text, origin, len(actual), len(expected))
    return {"text": text, "origin": origin, "ink_pixels": len(actual), "right_bound": right}


def changed_within(old, new, boxes):
    changes = [divmod(i, 256) for i, color in enumerate(ImageChops.difference(old, new).get_flattened_data())
               if color != (0, 0, 0)]
    assert changes and all(any(l <= x < r and t <= y < b for l, t, r, b in boxes) for y, x in changes)
    return len(changes)


def check_literal_macros(arm, memory):
    # Run the real formatter on a copy of the ordinary opening state, skipping its UI initialization call.
    cpu = machine(arm)
    cpu.mem_write(BASE, memory)
    release = 0x02600000
    destination = 0x02602000
    source = b"Say, FI... what \n do you think of men who go to sea? \0"
    hook = cpu.hook_add(UC_HOOK_CODE, lambda uc, *_: uc.reg_write(UC_ARM_REG_PC, STOP),
                        begin=0x020242CC, end=0x020242CC)
    names = (b"FIFI", b"F" * 15 + b"I", b"I" * 15 + b"F", "カFIゆ".encode("cp932"))
    try:
        for name in names:
            cpu.mem_write(0x022D5D44, (name + b"\0").ljust(17, b"\0"))
            cpu.mem_write(release, source)
            cpu.mem_write(destination - 8, b"\xA5" * 136)
            call(cpu, 0x242C8, (destination, release, 0x022D5D24), instruction_limit=400000)
            result = source.replace(b"FI", name, 1)
            assert bytes(cpu.mem_read(destination - 8, 136)) == b"\xA5" * 8 + result.ljust(128, b"\xA5")
    finally:
        cpu.hook_del(hook)
    return [n.hex() for n in names]


def observe(output):
    plan = read(output / PROOF_NAME)
    rom = output / ROM_NAME
    assert digest(rom.read_bytes()) == plan["candidate_sha256"]
    parent = read(REPORT)
    assert parent["ROM_sha256"] == ROM_HASH
    load = read(ROUNDTRIP / "continue/capture/capture_report.json")
    arm = NdsImage.open(rom).read_file(ARM)
    parent_arm = NdsImage.open(parent["ROM"]).read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    assert font == GameAsciiFont.from_arm9(parent_arm)
    reports = {mode: output / mode / "capture/capture_report.json" for mode in ("opening", "continue", "save")}
    runs = {mode: read(path) for mode, path in reports.items()}
    for mode, report in runs.items():
        assert report["ROM_sha256"] == plan["candidate_sha256"] and report["cold_boot"]
        assert not report["savestate_loaded"] and not report["callback_errors"]
        assert not report["hardware_device_verification"]
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
        donor = report.get("battery_save_preloaded")
        if mode == "opening":
            assert donor is None and report["scripted_input_schedule"] == parent["scripted_input_schedule"]
        else:
            assert donor["copied_byte_exact_before_cold_boot"]
            assert digest(Path(donor["source"]).read_bytes()) == donor["source_sha256"]
            assert digest(Path(donor["destination"]).read_bytes()) == donor["source_sha256"]
            assert donor["source_sha256"] == load["battery_save_preloaded"]["source_sha256"]
            assert report["scripted_input_schedule"][:4] == load["scripted_input_schedule"]
    cases = []
    pictures = {}
    for n in (2790, 3270, 5130, 5340, 6890, 7220):
        old_image, _, _ = frame(parent, n, True)
        image, memory, proof = frame(runs["opening"], n)
        row = {"frame": n, **proof}
        if n < 5130:
            assert image.tobytes() == old_image.tobytes()
            row["whole_frame_equal"] = True
        elif n == 5130:
            row["changed_pixels"] = changed_within(old_image, image, [(55, 244, 150, 257)])
            row["name"] = require_string(memory, 0x0218EF7C, REGULAR)
            row["glyphs"] = [glyphs(font, image, REGULAR.decode(), (60, 245), EDITOR_COLOR, 140)]
        elif n == 5340:
            row["changed_pixels"] = changed_within(old_image, image, [(89, 220, 198, 232)])
            row["name"] = require_string(memory, 0x02192E8C, REGULAR)
            row["glyphs"] = [glyphs(font, image, REGULAR.decode(), (89, 221), EDITOR_COLOR, 170)]
        elif n == 6890:
            row["changed_pixels"] = changed_within(old_image, image, [(16, 296, 244, 308)])
            row["dialogue"] = require_string(memory, 0x0218EDC8, BODY)
            row["glyphs"] = [glyphs(font, image, text, (16, y), BODY_COLOR, 244) for text, y in
                             (("Say, RafaelMaa... what", 297), ("do you think of men who go to sea?", 313))]
            row["isolated_extra_literal_macro_cases"] = check_literal_macros(arm, memory)
        else:
            row["changed_pixels"] = changed_within(old_image, image, [(14, 271, 154, 290)])
            row["speaker"] = require_string(memory, 0x022A4F78, REGULAR + b" Castor")
            row["reply"] = require_string(memory, 0x0218EDC8, b"Hmm... That's hard to answer... ")
            row["glyphs"] = [glyphs(font, image, "RafaelMaa Castor", (16, 277), LABEL_COLOR, 135)]
        cases.append(row)
        pictures["opening", n] = old_image, image
    for n in (2400, 3850):
        old_image, _, _ = frame(load, n, True)
        image, memory, proof = frame(runs["continue"], n)
        row = {"frame": n, **proof}
        if n == 2400:
            row["changed_pixels"] = changed_within(old_image, image, [(4, 116, 93, 138), (4, 200, 95, 215)])
            row["slot"] = require_string(memory, 0x02192410, REGULAR)
            row["untouched_card_read_buffer"] = require_string(memory, 0x02374F54, NAME)
            row["glyphs"] = [glyphs(font, image, REGULAR.decode(), origin, EDITOR_COLOR, 98)
                             for origin in ((25, 121), (8, 203))]
        else:
            assert image.tobytes() == old_image.tobytes()
            row["whole_town_frame_equal"] = True
            row["restored_actor"] = require_string(memory, 0x022D5D44, REGULAR)
            row["unchanged_surname"] = require_string(memory, 0x022D5D55, b"Castor")
        cases.append(row)
        pictures["continue", n] = old_image, image
    image, memory, proof = frame(runs["save"], 5080)
    cases.append({"frame": 5080, **proof, "saved_slot_glyphs": [
        glyphs(font, image, REGULAR.decode(), origin, EDITOR_COLOR, 98) for origin in ((25, 121), (8, 203))]})
    assert REGULAR + b"\0" in memory
    sheet = Image.new("RGB", (512, 520), "white")
    labels = ImageDraw.Draw(sheet)
    for row, (label, mode, n, box) in enumerate((
        ("Claudio’s dialogue", "opening", 6890, (0, 275, 256, 340)),
        ("Rafael’s nameplate", "opening", 7220, (0, 268, 256, 332)),
        ("Continue slot", "continue", 2400, (0, 79, 256, 240)),
    )):
        y = (0, 85, 170)[row]
        for column, photo in enumerate(pictures[mode, n]):
            x = column * 256
            labels.text((x + 4, y + 3), f"{label} - {('before', 'after')[column]}", fill="black")
            sheet.paste(photo.crop(box), (x, y + 20))
    labels.text((4, 358), "In-game Save slot", fill="black")
    sheet.paste(image.crop((0, 96, 256, 238)), (0, 378))
    picture = output / "name_glyph_comparison.png"
    sheet.save(picture)
    write(output / "ordinary_glyph_verification.json", {"candidate_sha256": plan["candidate_sha256"],
          "cases": cases, "reports": {str(p): digest(p.read_bytes()) for p in reports.values()},
          "sheet": str(picture), "sheet_sha256": digest(picture.read_bytes()),
          "battery_saves_unchanged": True, "hardware_verified": False})
    print(f"Verified {len(cases)} ordinary holds, literal FI expansions, and the preserved legacy save.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--output", type=Path, required=True)
    observe(cli.parse_args().output)
