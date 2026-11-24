"""Stage one Square reply and replay the same ordinary Tunis navigation."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import ImageChops

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import preflight_tunis_shop_advice_20261124 as review
from scripts import register_cartridge_title_20261123 as continuity
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


trend, played, panels, KEY = review.trend, review.played, review.panels, review.KEY
ROOT = Path(".codex-release-work/tunis_shop_advice_20261124")
ROM, STORED = ROOT / "Tunis_Shop_Advice_STAGED.nds", ROOT / "stored_proof.json"
BEFORE = played.ROOT / "capture/capture_report.json"
AFTER = ROOT / "replay/capture/capture_report.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PAIRED = ROOT / "paired_gameplay.json"
END = 10200
MENU_BLINKS = {7000: (86, 270, 186, 288), 7800: (86, 270, 186, 288),
               8600: (86, 238, 186, 266), 9400: (86, 238, 186, 266)}
MENU_PALETTE = {(0, 165, 172), (57, 56, 57)}


def stage():
    parent, proof = map(read, (played.RELEASE, review.OUT))
    assert parent["candidate_sha256"] == proof["candidate_sha256"] == digest(parent["candidate"])
    assert parent["clean_input_sha256"] == proof["source_sha256"] == digest(trend.CLEAN)
    assert digest(trend.base.REGISTRY) == parent["registry_sha256"]
    assert sum(len(sheet["messages"]) for sheet in proof["proposed_sheets"]) == 124
    assert all(reference(sheet["path"])["sha256"] == sheet["sha256"] for sheet in proof["proposed_sheets"])
    image = NdsImage.open(parent["candidate"])
    arm, common = (image.read_file(path) for path in (trend.ARM, trend.COMMON))
    assert trend.digest(arm) == parent["target_ARM9_sha256"] == proof["unchanged_ARM9_sha256"]
    assert continuity.right_bound(arm, parent["right_bound_configuration"])["matched_repair_spans"] == 8
    rows = trend.owned_entries(common, arm, trend.digest(arm[trend.DIRECTORY_OFFSET:trend.TABLE_OFFSET]))
    selected, = [row for row in proof["records"] if row["decision"] == "revision"]
    assert selected["message_ID"] == KEY and rows[KEY].text.hex() == selected["current_hex"]
    new, installed, allocation = trend.owned_deployment(common, arm, rows, {KEY: bytes.fromhex(selected["proposed_hex"])})
    assert trend.digest(new) == proof["proposed_COMMON_sha256"] and allocation[KEY] == proof["allocation"]
    assert {a.message_id for a, b in zip(rows, installed, strict=True) if a.text != b.text} == {KEY}
    initial = trend.files(image)
    image.replace_file(trend.COMMON, new)
    updated = trend.files(image)
    assert initial.keys() == updated.keys() and {key for key in initial if initial[key] != updated[key]} == {trend.COMMON}
    binary = bytes(image.rom.save())
    image.replace_file(trend.COMMON, common)
    assert bytes(image.rom.save()) == Path(parent["candidate"]).read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    assert NdsImage.open(ROM).read_file(trend.COMMON) == new
    write(STORED, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=parent["candidate_sha256"],
        clean_input_sha256=parent["clean_input_sha256"], target_ARM9_sha256=trend.digest(arm), target_COMMON_sha256=trend.digest(new),
        source_preflight=reference(review.OUT), whole_parent_inverse=True, changed_message=KEY, allocation=allocation[KEY]))
    print(f"Staged only COMMON {KEY}. {digest(ROM)}", flush=True)


def replay(stored):
    prior = read(BEFORE)
    assert prior["ROM_sha256"] == stored["predecessor_sha256"] and digest(ROM) == stored["candidate_sha256"]
    donor = prior["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    inputs = ROOT / "replay_inputs.json"
    write(inputs, prior["scripted_input_schedule"])
    frames = sorted({row["frame"] for row in prior["frames_captured"]})
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(AFTER.parent), "--frames", str(END),
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999", "--touchscreen",
            "--battery-save", donor["source"], "--capture-at", *map(str, frames)]
        played.replay.harness.main()
    finally:
        sys.argv = argv


def verify(stored):
    prior, current, native = map(read, (BEFORE, AFTER, review.OUT))
    assert digest(ROM) == stored["candidate_sha256"] == current["ROM_sha256"]
    assert prior["ROM_sha256"] == stored["predecessor_sha256"] and native["candidate_sha256"] == prior["ROM_sha256"]
    assert current["cold_boot"] and not current["savestate_loaded"] and not current["callback_errors"]
    assert not any(value for label, value in current.items() if label.startswith("synthetic_"))
    assert current["frames"] == END and current["scripted_input_schedule"] == prior["scripted_input_schedule"]
    assert current["battery_save_preloaded"]["source_sha256"] == prior["battery_save_preloaded"]["source_sha256"]
    old = panels.shots(prior, "_navigation.png")
    new = {row["frame"]: row for row in current["frames_captured"] if row["frame"] in old}
    assert set(old) == set(new)
    font = review.GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(trend.ARM))
    match, = [row for row in native["native_proposed_cases"] if row["goods"] == "Whale Meat"]
    unchanged, changed, blinks = [], [], []
    for frame in sorted(old):
        a, b = (panels.picture(group[frame]) for group in (old, new))
        compared = b
        if frame in MENU_BLINKS:
            x0, y0, x1, y1 = MENU_BLINKS[frame]
            compared = b.copy()
            pixels = 0
            for x in range(x0, x1):
                for y in range(y0, y1):
                    before_color, after_color = a.getpixel((x, y)), b.getpixel((x, y))
                    if before_color != after_color:
                        assert {before_color, after_color} == MENU_PALETTE
                        compared.putpixel((x, y), before_color)
                        pixels += 1
            assert pixels > 0
            blinks.append(dict(frame=frame, rect=MENU_BLINKS[frame], differing_background_pixels=pixels))
        bounds = ImageChops.difference(a, compared).getbbox()
        if review.HOLDS.get(frame) != KEY:
            assert bounds is None, (frame, bounds)
            if frame not in MENU_BLINKS:
                unchanged.append(frame)
            else:
                assert frame == 7000
            continue
        assert bounds and 16 <= bounds[0] < bounds[2] <= 250 and 296 <= bounds[1] < bounds[3] <= 360
        name = panels.nameplate(font, "Shopkeeper", b)
        assert name == panels.nameplate(font, "Shopkeeper", a)
        ink = panels.exact_body(font, match["lines"], b)
        changed.append(dict(frame=frame, capture=new[frame], complete_body_ink=ink, nameplate=name, bounds=bounds))
    assert len(changed) == 4 and END in unchanged
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": PAIRED},
                          argdefs=panels.sheets_for.__defaults__)
    figures = [(f"{label} / {frame}", panels.picture(group[frame]))
               for frame in (5800, 7800, 8600, 9400) for label, group in (("Before", old), ("Revised", new))]
    write(PAIRED, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        before=reference(BEFORE), after=reference(AFTER), stored=reference(STORED), dialogue_holds=changed,
        unchanged_frames=unchanged, shop_selection_blinks=blinks, ordinary_saved_game=True,
        sheets=sheets("paired_tunis_shop_advice", figures)))
    print(f"Verified four revised shopkeeper replies and {len(unchanged)} unchanged gameplay holds.")


def release_check(stored, action):
    scope = vars(checks) | dict(RELEASE=played.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(stored)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=stored["clean_input_sha256"], candidate=reference(ROM),
            patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "replay", "verify", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action in ("replay", "verify"):
        globals()[action](read(STORED))
    else:
        release_check(read(STORED), action)
