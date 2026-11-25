"""Build and replay the source-reviewed item rumor in its original COMMON slot."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import register_cartridge_title_20261123 as template
from scripts import verify_athens_valencia_town_20261123 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


parent, panels, town = review.current, review.panels, review.town
ARM, COMMON, KEY = review.ARM, review.COMMON, review.KEY
ROOT = Path(".codex-release-work/athens_item_rumor_20261124")
ROM, STORED = ROOT / "Athens_Item_Rumor_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPLAY = ROOT / "replay/capture/capture_report.json"
BEFORE = review.run.ROOT / "athens/capture/capture_report.json"
SHEET, PAIRED = ROOT / "athens_item_rumor_paired_1_20261123.png", ROOT / "paired_athens_item_rumor.json"
HOLD, END = 6320, 6840


def stage():
    assert not ROOT.exists()
    packet, preflight = map(read, (review.OUT, review.PREFLIGHT))
    release, ctx, cpu, _, raster, kanji = review.context()
    assert digest(REGISTRY) == release["registry_sha256"]
    assert preflight["checked_names"] == 218 and preflight["recorded_gameplay"] == reference(review.OUT)
    assert packet["candidate_sha256"] == preflight["candidate_sha256"] == release["candidate_sha256"]
    assert all(digest(r["path"]) == r["sha256"] for r in preflight["sheets"])
    clean = NdsImage.open(CLEAN)
    jp = review.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))[KEY]
    before = review.common_rows(ctx.common, ctx.arm)
    target, = [r for r in packet["records"] if r["message_ID"] == KEY]
    assert before[KEY].text.hex() == target["installed_hex"] and jp.text.hex() == target["source_hex"]
    assert sha256(ctx.arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(ctx.common).hexdigest() == release["target_COMMON_sha256"]
    assert template.right_bound(ctx.arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    draft, = [r for r in preflight["drafts"] if r["text"] == preflight["selected_template"]]
    new_text = bytes.fromhex(draft["stored_hex"])
    assert len(new_text) == len(before[KEY].text) and new_text.count(b"%s") == jp.text.count(b"%s") == 1
    assert new_text.startswith(b" ") and b"\n" not in new_text and b"\r" not in new_text
    common, entries, allocation = town.owned_deployment(ctx.common, ctx.arm, before, {KEY: new_text})
    assert [a.message_id for a, b in zip(before, entries, strict=True) if a != b] == [KEY]
    assert entries[KEY].text == new_text and allocation[KEY]["new_null_fields"] == 0
    ctx.image.replace_file(COMMON, common)
    binary = bytes(ctx.image.rom.save())
    ctx.image.replace_file(COMMON, ctx.common)
    assert bytes(ctx.image.rom.save()) == Path(release["candidate"]).read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    opened = NdsImage.open(ROM)
    assert opened.read_file(COMMON) == common and opened.read_file(ARM) == ctx.arm
    actual = review.common_rows(opened.read_file(COMMON), ctx.arm)[KEY]
    assert actual.text == new_text
    display, plane = review.render(cpu, raster, ctx.arm, kanji, KEY, actual.text, (review.ITEM,))
    predicted, = [r["layout"] for r in draft["layouts"] if r["name"] == review.ITEM]
    assert display == predicted
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        changed_message=KEY, exact_clean_source=panels.text_reference(jp),
        exact_predecessor=panels.text_reference(before[KEY]), exact_installed=panels.text_reference(actual),
        whole_parent_inverse=True, allocation=allocation[KEY], candidate_layout=display, native_plane_hex=plane.hex(),
        target_COMMON_sha256=sha256(common).hexdigest(), target_ARM9_sha256=release["target_ARM9_sha256"],
        source_review=reference(review.OUT), preflight=reference(review.PREFLIGHT),
        selected_template=draft["text"], all_item_name_cases=len(draft["layouts"]), split_item_names=draft["split_item_names"]))
    print(f"Staged only COMMON {KEY}. {digest(ROM)}", flush=True)


def replay(stored):
    assert digest(ROM) == stored["candidate"]["sha256"]
    old = read(BEFORE)
    assert old["ROM_sha256"] == stored["previous"]["sha256"]
    donor = old["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    REPLAY.parent.parent.mkdir()
    inputs = REPLAY.parent.parent / "inputs.json"
    write(inputs, [r for r in old["scripted_input_schedule"] if r["start"] <= END])
    frames = [r["frame"] for r in old["frames_captured"] if r["frame"] <= END]
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(REPLAY.parent), "--frames", str(END),
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
            "--touchscreen", "--battery-save", donor["source"], "--capture-at", *map(str, frames)]
        review.run.replay.harness.main()
    finally:
        sys.argv = argv


def verify(stored):
    old, new = map(read, (BEFORE, REPLAY))
    assert old["ROM_sha256"] == stored["previous"]["sha256"]
    assert new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert new["cold_boot"] and not new["callback_errors"] and not new["savestate_loaded"]
    assert not any(value for key, value in new.items() if key.startswith("synthetic_"))
    assert new["frames"] == END and new["scripted_input_schedule"] == [r for r in old["scripted_input_schedule"] if r["start"] <= END]
    assert old["battery_save_preloaded"]["source_sha256"] == new["battery_save_preloaded"]["source_sha256"]
    frames = [{r["frame"]: r for r in run["frames_captured"] if r["frame"] <= END} for run in (old, new)]
    assert frames[0].keys() == frames[1].keys()
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ARM))
    plane = bytes.fromhex(stored["native_plane_hex"])
    unchanged = []
    for frame in sorted(frames[0]):
        a, b = (panels.picture(group[frame]) for group in frames)
        bounds = ImageChops.difference(a, b).getbbox()
        if frame != HOLD:
            assert bounds is None, (frame, bounds)
            unchanged.append(frame)
            continue
        assert bounds and 16 <= bounds[0] < bounds[2] <= 250 and 296 <= bounds[1] < bounds[3] <= 360
        assert panels.mask_check(plane, 228, b)
        name = panels.nameplate(font, "Myrine", b)
        assert name == panels.nameplate(font, "Myrine", a)
        sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": PAIRED})
        sheet, = sheets("athens_item_rumor_paired", [("Previous / Myrine", a), ("Revised / Myrine", b)], (0, 272, 256, 380))
    assert END in unchanged
    assert sheet == reference(SHEET)
    write(PAIRED, dict(candidate_sha256=new["ROM_sha256"], previous_sha256=old["ROM_sha256"], before=reference(BEFORE),
        after=reference(REPLAY), stored=reference(STORED), sheet=sheet, unchanged_frames=unchanged,
        revised=frames[1][HOLD], nameplate=name, whole_page_sha256=sha256(plane).hexdigest(), ordinary_saved_game=True))
    print(f"Verified Myrine's revised rumor and {len(unchanged)} exact context and transition frames.")


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
