"""Exercise the conditional Fleet Info destination with a one-byte fleet fixture."""

import json
import sys
from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import headless_desmume_v193 as harness
from scripts import stage_missionary_destination_20261123 as build
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write
from scripts.verify_assigned_fleet_detail_20261123 import OUT as ASSIGNED, find_mask
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = build.ROOT
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in (
    "translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPORT, SHEET = ROOT / "missionary_destination_check.json", ROOT / "missionary_destination_1_20261123.png"
FRAMES = (10600, 11000, 11400, 11600)
PAUSE = 11800
SLOT = 114
FLEET_INDEX = 57


def populate(arm, raw, supplied):
    assert supplied == SLOT and len(raw) == 0x400000
    staged, parent = map(read, (build.STORED, build.parent.RELEASE))
    arm_hash = sha256(arm).hexdigest()
    assert arm_hash in (parent["target_ARM9_sha256"], staged["target_ARM9_sha256"])
    cpu, get = get_machine(arm, raw)
    fleet = get(0xCB1A8) + 4 + FLEET_INDEX * 0x84
    assert get(0x36914, fleet) == 1 and get(0x36948, fleet) == 0
    table = build.word(raw, fleet)
    name = get(build.word(raw, table + 8) - build.BASE, fleet)
    assert bytes(cpu.mem_read(name, 13)) == b"Manuel Fleet\0"
    address = fleet + 0x3F
    offset = address - build.BASE
    assert raw[offset] == 7
    changed = raw[:offset] + bytes([SLOT]) + raw[offset + 1:]
    assert len(changed) == len(raw) and changed[:offset] == raw[:offset] and changed[offset + 1:] == raw[offset + 1:]
    return changed, dict(fixture="only the destination byte of Manuel Fleet", fleet_index=FLEET_INDEX,
        address=address, changes=[dict(address=address, before=7, after=SLOT)], ARM9_sha256=arm_hash,
        before_RAM_sha256=sha256(raw).hexdigest(), after_RAM_sha256=sha256(changed).hexdigest())


def original_capture():
    binding = read(ASSIGNED)["trials"]["packed_report"]["evidence"][0]
    assert reference(binding["path"]) == binding
    return binding, read(binding["path"])


def play(version):
    _, old = original_capture()
    donor = old["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    parent, staged = map(read, (build.parent.RELEASE, build.STORED))
    rom, sha = (build.ROM, staged["candidate_sha256"]) if version == "revised" else (
        Path(parent["candidate"]), parent["candidate_sha256"])
    assert digest(rom) == sha
    folder = ROOT / version
    folder.mkdir()
    inputs = folder / "inputs.json"
    write(inputs, [entry for entry in old["scripted_input_schedule"] if entry["start"] <= PAUSE])
    commands = [
        dict(destination_fixture=SLOT, until=12000, buttons=["A"], duration=8),
        dict(until=12200, touch=[91, 164], duration=8), dict(until=12400, buttons=["A"], duration=8),
        dict(until=12600, buttons=["B"], duration=8), dict(until=12800, buttons=["B"], duration=8),
        dict(stop=True),
    ]
    source = checked_text(getsource(harness.main), {
        "if 'regional_finance_display' in command:": "if 'destination_fixture' in command:",
        """                    from scripts.native_regional_finance_v617 import (
                        populate as populate_regional_finance,
                    )""": "                    populate_regional_finance = DESTINATION_FIXTURE",
        "populate_regional_finance(arm, before, command['regional_finance_display'])":
            "populate_regional_finance(arm, before, command['destination_fixture'])",
        "Synthetic three-word regional financial display applied; monthly or earned values are not verified.":
            "Focused Fleet Info test supplied destination 114 in one byte.",
        "synthetic_regional_financial_display_fixtures": "synthetic_fleet_destination_fixtures",
    })
    scope = vars(harness) | dict(DESTINATION_FIXTURE=populate)
    exec(compile(source, __file__ + "::one-destination-byte", "exec"), scope)
    argv, stdin = sys.argv, sys.stdin
    try:
        sys.stdin = StringIO("".join(json.dumps(row) + "\n" for row in commands))
        sys.argv = [__file__, "--rom", str(rom), "--out", str(folder / "capture"), "--frames", "13000",
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
            "--battery-save", donor["source"], "--touchscreen", "--pause-at", str(PAUSE),
            "--allow-regional-finance-fixtures", "--capture-at", *map(str, FRAMES)]
        scope["main"]()
    finally:
        sys.argv, sys.stdin = argv, stdin
    assert digest(donor["source"]) == donor["source_sha256"]


def compare():
    staged = read(build.STORED)
    original_binding, control = original_capture()
    paths = [ROOT / version / "capture/capture_report.json" for version in ("current", "revised")]
    current, revised = map(read, paths)
    assert current["ROM_sha256"] == staged["predecessor_sha256"]
    assert revised["ROM_sha256"] == staged["candidate_sha256"] == digest(build.ROM)
    assert current["scripted_input_schedule"] == revised["scripted_input_schedule"] == control["scripted_input_schedule"]
    fixtures = []
    for run in (current, revised):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"] and run["frames"] == 12800
        assert [key for key, rows in run.items() if key.startswith("synthetic_") and rows] == ["synthetic_fleet_destination_fixtures"]
        observed, = run["synthetic_fleet_destination_fixtures"]
        assert observed["frame"] == PAUSE and observed["fleet_index"] == FLEET_INDEX
        assert observed["changes"] == [dict(address=observed["address"], before=7, after=SLOT)]
        assert run["battery_save_preloaded"]["source_sha256"] == control["battery_save_preloaded"]["source_sha256"]
        fixtures.append(observed)
    a, b, control_frames = (shots(run, "_navigation.png") for run in (current, revised, control))
    assert picture(a[PAUSE]).tobytes() == picture(b[PAUSE]).tobytes() == picture(control_frames[PAUSE]).tobytes()
    arm = NdsImage.open(build.ROM).read_file(build.ARM)
    font = GameAsciiFont.from_arm9(arm)
    regions, figures = [], []
    for n in (12000, 12400, 12600):
        older, newer = picture(a[n]), picture(b[n])
        bounds = ImageChops.difference(older, newer).getbbox()
        assert bounds and 76 <= bounds[0] < bounds[2] <= 246 and 240 <= bounds[1] < bounds[3] <= 260
        mask = find_mask(font, "To: Missionary", newer, (76, 240, 246, 260))
        regions.append(dict(frame=n, full_label=mask, difference_bounds=bounds, current=a[n], revised=b[n]))
        figures.extend(((f"{n} previous", older), (f"{n} revised", newer)))
    assert picture(a[12800]).tobytes() == picture(b[12800]).tobytes() == picture(control_frames[12800]).tobytes()
    ordinary_a, ordinary_b = (shots(run, "_cold_boot.png") for run in (current, revised))
    assert all(picture(ordinary_a[n]).tobytes() == picture(ordinary_b[n]).tobytes() for n in FRAMES)
    sheet = Image.new("RGB", (1040, 189 * 3), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (label, screen) in enumerate(figures):
        x, y = 520 * (i % 2) + 4, 189 * (i // 2)
        draw.text((x, y + 4), label, fill="white")
        crop = screen.crop((0, 235, 256, 316))
        sheet.paste(crop.resize((512, 162), Image.Resampling.NEAREST), (x, y + 22))
    sheet.save(SHEET)
    write(REPORT, dict(candidate_sha256=staged["candidate_sha256"], predecessor_sha256=staged["predecessor_sha256"],
        focus_fixture=fixtures, prepared_save=control["battery_save_preloaded"]["source_sha256"],
        ordinary_controller_navigation_after_fixture=True, naturally_reached_destination_114=False, views=regions,
        exact_controls=[*FRAMES, PAUSE, 12800], exact_return_to_fleet_list=True,
        visual=reference(SHEET), earlier_order_replay=original_binding, evidence=[reference(p) for p in paths]))
    print("Verified complete Missionary glyphs and three actual panel states with the supplied destination.")


def main(action):
    if action in ("current", "revised"):
        play(action)
        return
    if action == "compare":
        compare()
        return
    stage, parent = map(read, (build.STORED, build.parent.RELEASE))
    proof = stage | dict(candidate=str(build.ROM), clean_input_sha256=parent["clean_input_sha256"])
    scope = vars(checks) | dict(RELEASE=build.parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT,
                                STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(build.ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("current", "revised", "compare", "patch", "startup"))
    main(cli.parse_args().action)
