"""Build, replay and verify the regional Tavern repair in its existing allocations."""

from argparse import ArgumentParser
from pathlib import Path
import sys
from types import FunctionType

from PIL import ImageChops

from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import headless_desmume_v193 as harness
from scripts import preflight_istanbul_tavern_rumor_20261124 as review
from scripts import register_cartridge_title_20261123 as continuity
from scripts import stage_tunis_shop_advice_20261124 as shared
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


ARM, COMMON, panels = review.ARM, review.COMMON, review.PANELS
played = review.play
played.RELEASE = review.RELEASE
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_istanbul_tavern_rumor")
ROM, STORED = ROOT / "Istanbul_Tavern_Rumor_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = [ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json")]
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
BEFORE = played.ROOT / "capture/capture_report.json"
AFTER = ROOT / "replay/capture/capture_report.json"
LONDON_HISTORY = Path(".codex-release-work/london_guild_display_20261124/ordinary_replay/capture_report.json")
LONDON_HOLD, LONDON_END, END = 4800, 5600, review.END
PAIRED = ROOT / "paired_gameplay.json"
SHEET = ROOT / "paired_istanbul_tavern_1_20261123.png"


def stage():
    parent, proof = map(read, (review.RELEASE, review.OUT))
    assert digest(review.REGISTRY) == parent["registry_sha256"]
    assert parent["candidate_sha256"] == proof["candidate_sha256"] == digest(parent["candidate"])
    assert parent["clean_input_sha256"] == proof["source_sha256"] == digest(review.CLEAN)
    assert all(digest(sheet["path"]) == sheet["sha256"] for sheet in proof["proposed_sheets"])
    image = NdsImage.open(parent["candidate"])
    arm, common = (image.read_file(path) for path in (ARM, COMMON))
    assert sha256(arm).hexdigest() == proof["current_ARM9_sha256"] == parent["target_ARM9_sha256"]
    assert sha256(common).hexdigest() == parent["target_COMMON_sha256"]
    clean_arm = NdsImage.open(review.CLEAN).read_file(ARM)
    changed_arm, edits, _, _, _ = review.proposed_arm(clean_arm, arm)
    assert edits == proof["exact_ARM9_edits"] and sha256(changed_arm).hexdigest() == proof["proposed_ARM9_sha256"]
    assert continuity.right_bound(changed_arm, parent["right_bound_configuration"])["matched_repair_spans"] == 8
    rows = review.athens.common_rows(common, arm)
    row, = [item for item in proof["records"] if item.get("message_ID") == review.KEY]
    assert row["current_reference"] == review.exact_entry(rows[review.KEY])
    replacement = bytes.fromhex(row["proposed_reference"]["exact_hex"])
    new, installed, allocation = review.guild.owned_deployment(common, changed_arm, rows, {review.KEY: replacement})
    assert sha256(new).hexdigest() == proof["proposed_COMMON_sha256"] and allocation[review.KEY] == proof["allocation"]
    assert [b.message_id for a, b in zip(rows, installed, strict=True) if a != b] == [review.KEY]
    assert review.exact_entry(installed[review.KEY]) == row["proposed_reference"]
    image.replace_file(ARM, changed_arm)
    image.replace_file(COMMON, new)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert sha256(image.rom.save()).hexdigest() == parent["candidate_sha256"]
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    finished = NdsImage.open(ROM)
    assert finished.read_file(ARM) == changed_arm and finished.read_file(COMMON) == new
    write(STORED, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=parent["candidate_sha256"],
        clean_input_sha256=parent["clean_input_sha256"], target_ARM9_sha256=sha256(changed_arm).hexdigest(),
        target_COMMON_sha256=sha256(new).hexdigest(), source_preflight=reference(review.OUT),
        whole_parent_inverse=True, changed_message=review.KEY, exact_ARM9_edits=edits,
        allocation=allocation[review.KEY], paired_ordinary_gameplay_pending=True))
    print(f"Staged COMMON {review.KEY} and two source-bound ARM9 data spans. {digest(ROM)}", flush=True)


def capture(report, rom, target, end, frames):
    donor = report["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"]
    assert not (target / "capture_report.json").exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    inputs = target.parent / "inputs.json"
    write(inputs, [row for row in report["scripted_input_schedule"] if row["start"] <= end])
    original = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(rom), "--out", str(target), "--frames", str(end),
            "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
            "--battery-save", donor["source"], "--touchscreen", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = original


def london_report(label):
    directory = "candidate_retry" if label == "candidate" else label
    return ROOT / "london" / directory / "capture" / "capture_report.json"


def replay(stored):
    original = read(BEFORE)
    assert original["ROM_sha256"] == stored["predecessor_sha256"]
    assert digest(ROM) == stored["candidate_sha256"]
    capture(original, ROM, AFTER.parent, END, panels.shots(original, "_navigation.png"))


def london(stored, label):
    report = read(LONDON_HISTORY)
    parent = read(review.RELEASE)
    assert stored["predecessor_sha256"] == parent["candidate_sha256"] == digest(parent["candidate"])
    assert stored["candidate_sha256"] == digest(ROM)
    frames = [n for n in panels.shots(report, "_cold_boot.png") if n <= LONDON_END]
    assert LONDON_HOLD in frames and LONDON_END in frames
    rom = parent["candidate"] if label == "parent" else ROM
    capture(report, rom, london_report(label).parent, LONDON_END, frames)


def compare(stored, font, before, after, suffix, hold, lines, speaker):
    old, new = map(read, (before, after))
    assert old["ROM_sha256"] == stored["predecessor_sha256"]
    assert new["ROM_sha256"] == stored["candidate_sha256"] == digest(ROM)
    assert old["frames"] == new["frames"] and old["scripted_input_schedule"] == new["scripted_input_schedule"]
    assert old["core_DLL_sha256"] == new["core_DLL_sha256"] and old["core_options"] == new["core_options"]
    for run in (old, new):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
        donor = run["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert old["battery_save_preloaded"]["source_sha256"] == new["battery_save_preloaded"]["source_sha256"]
    old_frames, new_frames = panels.shots(old, suffix), panels.shots(new, "_cold_boot.png")
    unchanged = []
    for frame, previous in old_frames.items():
        if frame == hold:
            continue
        assert previous["framebuffer_sha256"] == new_frames[frame]["framebuffer_sha256"], frame
        unchanged.append(frame)
    a, b = (panels.picture(group[hold]) for group in (old_frames, new_frames))
    bounds = ImageChops.difference(a, b).getbbox()
    assert bounds and 16 <= bounds[0] < bounds[2] <= 250 and 296 <= bounds[1] < bounds[3] <= 360
    nameplate = panels.nameplate(font, speaker, b)
    assert nameplate == panels.nameplate(font, speaker, a)
    return dict(before=reference(before), after=reference(after), frame=hold, complete_body_ink=panels.exact_body(font, lines, b),
                nameplate=nameplate, bounds=bounds, unchanged_frames=unchanged), (a, b)


def verify(stored):
    proof = read(review.OUT)
    native = proof["native"]
    assert proof["candidate_sha256"] == stored["predecessor_sha256"]
    arm = NdsImage.open(ROM).read_file(ARM)
    assert sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    font = review.GameAsciiFont.from_arm9(arm)
    actual, = [case["proposed"] for case in native["exact_cases"] if case["arguments"] == list(review.ACTUAL)]
    tavern, tavern_figures = compare(stored, font, BEFORE, AFTER, "_navigation.png",
                                     review.HOLD, actual["lines"], "Patron")
    guild, guild_figures = compare(stored, font, london_report("parent"), london_report("candidate"),
                                   "_cold_boot.png", LONDON_HOLD, native["pitch_layout"]["lines"], "Guildmaster")
    assert END in tavern["unchanged_frames"] and LONDON_END in guild["unchanged_frames"]
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=PAIRED),
                        argdefs=panels.sheets_for.__defaults__)
    sheets = draw("paired_istanbul_tavern", list(zip(
        ("Patron / previous", "Patron / revised", "Guildmaster / previous", "Guildmaster / revised"),
        (*tavern_figures, *guild_figures), strict=True)))
    assert sheets == [reference(SHEET)]
    write(PAIRED, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        ordinary_saved_game=True, tavern=tavern, guild=guild, sheets=sheets, source_preflight=reference(review.OUT)))
    print(f"Both revised dialogue holds and {len(tavern['unchanged_frames']) + len(guild['unchanged_frames'])} companion frames passed.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "replay", "london-parent", "london-candidate", "verify", "startup", "patch"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    elif action in ("patch", "startup"):
        FunctionType(shared.release_check.__code__, vars(shared) | globals())(read(STORED), action)
    elif action.startswith("london-"):
        london(read(STORED), action.split("-")[1])
    else:
        globals()[action](read(STORED))
