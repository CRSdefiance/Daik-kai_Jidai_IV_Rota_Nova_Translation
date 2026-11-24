"""Stage the verified Palace paragraph, then replay the ordinary contract and Trade visit."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import headless_desmume_v193 as harness
from scripts import preflight_nagasaki_contract_wrap_20261124 as preflight
from scripts import register_cartridge_title_20261123 as template
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


market, town, KEY = preflight.market, preflight.town, preflight.KEY
parent, panels = market.played.current, market.panels
ARM, COMMON = parent.ARM, parent.COMMON
ROOT = Path(".codex-release-work/nagasaki_contract_wrap_20261124")
ROM, STORED = ROOT / "Nagasaki_Contract_Wrap_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPLAY = ROOT / "replay/capture/capture_report.json"
BEFORE = market.played.ROOT / "capture/capture_report.json"
SHEET, PAIRED = ROOT / "nagasaki_contract_paired.png", ROOT / "paired_gameplay.json"
HOLD = 8120


def stage():
    baseline, draft = map(read, (parent.RELEASE, preflight.OUT))
    assert digest(CLEAN) == baseline["clean_input_sha256"] and digest(REGISTRY) == baseline["registry_sha256"]
    assert digest(parent.ROM) == baseline["candidate_sha256"] == draft["candidate_sha256"]
    assert draft["key"] == KEY and draft["original_gameplay"] == reference(market.OUT)
    assert all(digest(row["path"]) == row["sha256"] for row in draft["sheets"])
    clean, image = map(NdsImage.open, (CLEAN, parent.ROM))
    source = market.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))[KEY]
    arm, prior = (image.read_file(path) for path in (ARM, COMMON))
    assert sha256(arm).hexdigest() == baseline["target_ARM9_sha256"]
    assert sha256(prior).hexdigest() == baseline["target_COMMON_sha256"]
    assert template.right_bound(arm, baseline["right_bound_configuration"])["matched_repair_spans"] == 8
    before = market.common_rows(prior, arm)
    assert panels.text_reference(source) == draft["original_dialogue"]["clean_reference"]
    assert panels.text_reference(before[KEY]) == draft["original_dialogue"]["installed_reference"]
    revised = bytes.fromhex(draft["proposed_storage_hex"])
    assert revised.decode("ascii").strip() == preflight.PROPOSAL
    assert all(b"%" not in text for text in (source.text, before[KEY].text, revised))
    assert len(revised) == len(before[KEY].text) and b"\n" not in revised
    common, entries, allocations = town.owned_deployment(prior, arm, before, {KEY: revised})
    assert [a.message_id for a, b in zip(before, entries, strict=True) if a != b] == [KEY]
    assert allocations[KEY] == draft["fixed_slot"] and allocations[KEY]["new_null_fields"] == 0
    image.replace_file(COMMON, common)
    payload = bytes(image.rom.save())
    image.replace_file(COMMON, prior)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(payload)
    stored = NdsImage.open(ROM)
    assert stored.read_file(COMMON) == common and stored.read_file(ARM) == arm
    final = market.common_rows(stored.read_file(COMMON), arm)[KEY]
    assert final.text == revised
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        target_COMMON_sha256=sha256(common).hexdigest(), target_ARM9_sha256=baseline["target_ARM9_sha256"],
        changed_message=KEY, exact_clean_source=panels.text_reference(source), exact_predecessor=panels.text_reference(before[KEY]),
        exact_installed=panels.text_reference(final), whole_parent_inverse=True, allocation=allocations[KEY],
        preflight=reference(preflight.OUT), candidate_layout=draft["native_cases"][1]["layout"]))
    print(f"Staged only COMMON {KEY}. {digest(ROM)}", flush=True)


def replay(stored):
    old = read(BEFORE)
    donor = old["battery_save_preloaded"]
    assert digest(ROM) == stored["candidate"]["sha256"] and digest(donor["source"]) == donor["source_sha256"]
    assert old["ROM_sha256"] == stored["previous"]["sha256"]
    REPLAY.parent.parent.mkdir()
    inputs = REPLAY.parent.parent / "inputs.json"
    write(inputs, old["scripted_input_schedule"])
    frames = sorted(panels.shots(old, "_navigation.png"))
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(REPLAY.parent), "--frames", str(old["frames"]),
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999", "--touchscreen",
            "--battery-save", donor["source"], "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = argv


def verify(stored):
    old, new = map(read, (BEFORE, REPLAY))
    assert old["ROM_sha256"] == stored["previous"]["sha256"] and new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert new["cold_boot"] and not new["callback_errors"] and not new["savestate_loaded"]
    assert not any(value for key, value in new.items() if key.startswith("synthetic_"))
    assert new["frames"] == old["frames"] and new["scripted_input_schedule"] == old["scripted_input_schedule"]
    donor = new["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    before, after = (panels.shots(run, suffix) for run, suffix in ((old, "_navigation.png"), (new, "_cold_boot.png")))
    assert before.keys() <= after.keys()
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ARM))
    unchanged = []
    for frame in sorted(before):
        a, b = (panels.picture(group[frame]) for group in (before, after))
        bbox = ImageChops.difference(a, b).getbbox()
        if frame != HOLD:
            assert bbox is None, (frame, bbox)
            unchanged.append(frame)
            continue
        assert bbox and 16 <= bbox[0] < bbox[2] <= 250 and 296 <= bbox[1] < bbox[3] <= 360
        ink = panels.exact_body(font, stored["candidate_layout"]["lines"], b)
        nameplate = panels.nameplate(font, "Daimyo", b)
        assert nameplate == panels.nameplate(font, "Daimyo", a)
        sheet = Image.new("RGB", (512, 124), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, screen) in enumerate((("Previous", a), ("Revised", b))):
            draw.text((i * 256 + 4, 3), label, fill="white")
            sheet.paste(screen.crop((0, 276, 256, 384)), (i * 256, 16))
        sheet.resize((1024, 248), Image.Resampling.NEAREST).save(SHEET)
    assert (set(market.GOODS) | {8520, 8920, 9720, 12520, 12920}) <= set(unchanged)
    write(PAIRED, dict(candidate_sha256=new["ROM_sha256"], previous_sha256=old["ROM_sha256"],
        before=reference(BEFORE), after=reference(REPLAY), stored=reference(STORED), sheet=reference(SHEET),
        unchanged_frames=unchanged, revised=after[HOLD], complete_body_pixels=ink, nameplate=nameplate, ordinary_saved_game=True))
    print(f"Verified the revised Palace question and {len(unchanged)} pixel-identical gameplay holds.")


def release_check(stored, action):
    proof = dict(candidate=str(ROM), candidate_sha256=stored["candidate"]["sha256"],
        predecessor_sha256=stored["previous"]["sha256"], clean_input_sha256=stored["clean"]["sha256"])
    scope = vars(checks) | dict(RELEASE=parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
            patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup", "replay", "verify"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action in ("replay", "verify"):
        globals()[action](read(STORED))
    else:
        release_check(read(STORED), action)
