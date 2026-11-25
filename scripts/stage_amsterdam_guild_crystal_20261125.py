"""Apply the verified crystal pitch and replay its ordinary Guild exchange."""

from argparse import ArgumentParser
import sys
from types import FunctionType, SimpleNamespace

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_fleet_diversion_release_20261125 as checks
from scripts import headless_desmume_v193 as harness
from scripts import preflight_amsterdam_guild_crystal_20261125 as draft
from scripts import register_amsterdam_hodram_wraps_20261125 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write


ROOT, NATIVE, KEY = draft.ROOT, draft.OUT, draft.KEY
ROM, STORED, CAPTURE = ROOT / "Amsterdam_Guild_Crystal_STAGED.nds", ROOT / "stored_proof.json", ROOT / "paired"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE, QA = ROOT / "startup/capture/capture_report.json", ROOT / "qa_passed.xml"
panels, archive_tools = draft.review.panels, draft.town
OUT = draft.review.OUT.with_name("amsterdam_guild_crystal_paired_20261125.json")
MAP_REVIEW = OUT.with_name("lisbon_guild_shortfall_current_20261125.json")
BASE_CAPTURE = current.build.CAPTURE / "capture_report.json"
FINAL_FRAME = 26150
HOLD = 23750
MAP_HOLD = 23450


def stage():
    release, preflight, original = map(read, (current.RELEASE, NATIVE, draft.review.play.current.RELEASE))
    assert release["registry_sha256"] == digest(REGISTRY) and release["candidate_sha256"] == digest(current.ROM)
    assert release["clean_input_sha256"] == original["clean_input_sha256"] == digest(CLEAN)
    assert release["predecessor"]["candidate_sha256"] == preflight["candidate_sha256"] == original["candidate_sha256"]
    assert preflight["source_review"] == reference(draft.review.OUT) and preflight["ordinary_replay_pending"]
    candidate, prior = map(NdsImage.open, (current.ROM, original["candidate"]))
    old, incoming = map(archive_tools.files, (prior, candidate))
    assert old.keys() == incoming.keys() and {path for path in old if old[path] != incoming[path]} == {current.STORY}
    arm, archive = (incoming[path] for path in (current.ARM, current.COMMON))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] == original["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"] == original["target_COMMON_sha256"]
    font_path = "/GRP/KANJI.FNT"
    assert incoming[font_path] == old[font_path]
    row, = preflight["records"]
    assert row["message_ID"] == KEY and row["decision"] == "revision proposed"
    assert [tuple(layout["lines"]) for layout in preflight["native_layouts"]][1] == draft.LINES
    assert all(digest(item["path"]) == item["sha256"] for item in preflight["native_previews"])
    # Apply the exact bytes already passed by the current Guild renderer.
    directory = sha256(arm[archive_tools.DIRECTORY_OFFSET:archive_tools.TABLE_OFFSET]).hexdigest()
    records = archive_tools.owned_entries(archive, arm, directory)
    jp = NdsImage.open(CLEAN)
    clean = archive_tools.common_message_entries(jp.read_file(current.COMMON), jp.read_file(current.ARM))[KEY]
    assert clean.text.hex() == row["source_reference"]["exact_hex"]
    assert records[KEY].text.hex() == row["installed_reference"]["exact_hex"]
    proposed_text = bytes.fromhex(row["proposed_reference"]["exact_hex"])
    deployed, revised, slots = archive_tools.owned_deployment(archive, arm, records, {KEY: proposed_text})
    assert slots[KEY] == preflight["original_allocation"]
    assert {a.message_id for a, b in zip(records, revised, strict=True) if a != b} == {KEY}
    assert len(deployed) == len(archive) and sha256(deployed).hexdigest() == preflight["proposed_COMMON_sha256"]
    candidate.replace_file(current.COMMON, deployed)
    after = archive_tools.files(candidate)
    assert after.keys() == incoming.keys() and {path for path in after if after[path] != incoming[path]} == {current.COMMON}
    candidate.save(ROM)
    candidate.replace_file(current.COMMON, archive)
    assert sha256(candidate.rom.save()).hexdigest() == release["candidate_sha256"]
    write(STORED, dict(parent=reference(current.ROM), candidate=reference(ROM), proposal=reference(NATIVE),
        exact_parent_inverse=True, target_COMMON_sha256=sha256(deployed).hexdigest(),
        reused_native_preview_dependencies=dict(ARM9_sha256=release["target_ARM9_sha256"],
            COMMON_sha256=release["target_COMMON_sha256"], font_sha256=sha256(incoming[font_path]).hexdigest(),
            sole_parent_change=current.STORY),
        qualified_baseline=reference(BASE_CAPTURE), allocation=slots[KEY]))
    print("Staged only COMMON 3661 after matching every dependency of the native previews.")


def capture():
    stored, baseline = map(read, (STORED, BASE_CAPTURE))
    assert stored["qualified_baseline"] == reference(BASE_CAPTURE) and stored["candidate"] == reference(ROM)
    assert baseline["ROM_sha256"] == stored["parent"]["sha256"] == digest(current.ROM)
    assert baseline["cold_boot"] and not baseline["savestate_loaded"] and not baseline["callback_errors"]
    assert not any(value for key, value in baseline.items() if key.startswith("synthetic_"))
    donor = baseline["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    frames = sorted(n for n in panels.shots(baseline, "_cold_boot.png") if 21350 <= n <= FINAL_FRAME)
    assert HOLD in frames and frames[-1] == FINAL_FRAME
    inputs = ROOT / "inputs_crystal.json"
    write(inputs, [e for e in baseline["scripted_input_schedule"] if e["start"] <= FINAL_FRAME])
    saved = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(CAPTURE), "--frames", str(FINAL_FRAME),
                    "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                    "--battery-save", donor["source"], "--touchscreen", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = saved


def verify():
    replay_path = CAPTURE / "capture_report.json"
    stored, previous, new, preflight = map(read, (STORED, BASE_CAPTURE, replay_path, NATIVE))
    assert stored["qualified_baseline"] == reference(BASE_CAPTURE)
    assert previous["ROM_sha256"] == stored["parent"]["sha256"] and new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert stored["exact_parent_inverse"] and stored["proposal"] == reference(NATIVE)
    for key in ("core_DLL_sha256", "core_options"):
        assert previous[key] == new[key]
    expected = [e for e in previous["scripted_input_schedule"] if e["start"] <= FINAL_FRAME]
    assert new["frames"] == FINAL_FRAME and new["scripted_input_schedule"] == expected
    for run in (previous, new):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
    a, b = (run["battery_save_preloaded"] for run in (previous, new))
    assert a["source_sha256"] == b["source_sha256"] == digest(b["source"])
    old, staged = (panels.shots(run, "_cold_boot.png") for run in (previous, new))
    companions = sorted(n for n in old if 21350 <= n <= FINAL_FRAME and n != HOLD)
    assert {HOLD, *companions} <= set(staged)
    for n in companions:
        delta = ImageChops.difference(panels.picture(old[n]), panels.picture(staged[n])).getbbox()
        assert delta is None, (n, delta)
    left, right = (panels.picture(shots[HOLD]) for shots in (old, staged))
    before, after = (layout["lines"] for layout in preflight["native_layouts"])
    arm = NdsImage.open(ROM).read_file(current.ARM)
    assert arm == NdsImage.open(current.ROM).read_file(current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    seen = [panels.exact_body(font, lines, screen) for lines, screen in ((before, left), (after, right))]
    nameplate = panels.nameplate(font, "Guildmaster", left)
    assert nameplate == panels.nameplate(font, "Guildmaster", right)
    map_row, = [row for row in read(MAP_REVIEW)["records"] if row["id"] == "ARM9_GUILD_TREASURE_PITCH"]
    map_screen = panels.picture(staged[MAP_HOLD])
    assert MAP_HOLD in companions and panels.nameplate(font, "Guildmaster", map_screen) == nameplate
    map_ink = panels.exact_body(font, map_row["lines"], map_screen)
    for ref, component in ((map_row["source_reference"], NdsImage.open(CLEAN).read_file(current.ARM)),
                           (map_row["installed_reference"], arm)):
        raw, offset = bytes.fromhex(ref["exact_hex"]), ref["offset"]
        assert component[offset:offset + len(raw)] == raw
    delta = ImageChops.difference(left, right)
    delta.paste((0, 0, 0), (224, 360, 240, 376))
    bounds = delta.getbbox()
    assert bounds and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 360
    sheets = panels.sheets_for("amsterdam_guild_crystal_paired_20261125", [("Before", left), ("Candidate", right)])
    write(OUT, dict(candidate=stored["candidate"], parent=stored["parent"], ordinary_gameplay=True,
        proposal=stored["proposal"], baseline=reference(BASE_CAPTURE), replay=reference(replay_path),
        revised_hold=dict(frame=HOLD, before=old[HOLD], after=staged[HOLD], body_bounds=bounds, ink=seen, nameplate=nameplate),
        retained_map_pitch=dict(frame=MAP_HOLD, capture=staged[MAP_HOLD], ink=map_ink, source_review=reference(MAP_REVIEW)),
        exact_companion_frames=companions, sheet=sheets[0]))
    print(f"Verified the revised crystal line and {len(companions)} pixel-exact companion frames.")


def check_release(action):
    args = SimpleNamespace(draft=SimpleNamespace(current=current), PROOF=STORED, ROM=ROM)
    scope = vars(checks) | dict(stage=args, PATCH=PATCH, REBUILT=REBUILT,
                                PATCH_PROOF=PATCH_PROOF, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(checks.main.__code__, scope)(action)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "capture", "verify", "patch", "startup"))
    action = parser.parse_args().action
    if action in ("patch", "startup"):
        check_release(action)
    else:
        {"stage": stage, "capture": capture, "verify": verify}[action]()
