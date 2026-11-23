"""Verify the revised Hodram candidate through ordinary and focused gameplay."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType
import sys

from scripts import observe_shared_town_dialogue_20261123 as observer
from scripts import replay_hodram_midroute_followups_20261123 as previous
from scripts import stage_hodram_recruitment_and_sails_20261123 as stage
from scripts import verify_rafael_athens_and_maria_crew_20261122 as checks
from scripts.source_locked_derivation_v5118 import checked_text

base, native, gameplay = stage.base, stage.native, previous.gameplay
menu, branch, fixture = previous.menu, previous.branch, previous.fixture
ROOT = stage.ROOT / "gameplay"
LIVE = ROOT / "verified_gameplay.json"
CHOICES = stage.ROOT / "original_choice_tables.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
BOOT, PROMPTS = previous.BOOT, {171: 12}
RESULTS = {171: ((62, 65, 68, 71), (29,))}
RUNS = {"b171_0": (171, 0), "b171_1": (171, 1)}
record_id = previous.record_id


def samples():
    draft = base.load(stage.REVIEW)
    focus = [row for row in draft["records"] if row["decision"] == "revision"
             and row["block"] != 158 and row["id"] != record_id(171, 71)]
    focus.extend(row for row in draft["records"] if row["kind"] == "system")
    return {1: tuple((row["block"], int(row["id"].rsplit("R", 1)[1])) for row in focus)}


def route_rom(route):
    return ROOT / f"route{route}" / "Hodram_Recruitment_And_Sails_FOCUSED_ONLY.nds"


def choice_paths(block):
    root = ROOT / f"b{block}_choice"
    return root, root / f"Hodram_B{block}_Choice_FOCUSED_ONLY.nds", root / "fixture.json"


def report(run):
    return ROOT / run / "capture/capture_report.json"


focus = previous.scope | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    focus[name] = FunctionType(previous.scope[name].__code__, focus)
exec(compile(previous.previous.prepare_source, __file__ + "::original-choice-commands", "exec"), focus)
branch_frames = FunctionType(branch.branch_frames.__code__, branch.branch_frames.__globals__ | globals())
play_choice = FunctionType(branch.play_choice.__code__, branch.play_choice.__globals__ | globals())


def formatting():
    if not GLYPHS.exists():
        FunctionType(checks.check_glyphs.__code__, checks.check_glyphs.__globals__ | globals()
            | dict(OUTPUT=GLYPHS))()
    if not stage.FE_PROOF.exists():
        source = checked_text(getsource(checks.check_modal), {
            'assert len(records) == 10 and sum(r["second_page"] for r in records) == 2':
                'assert len(records) == 4 and not any(r["second_page"] for r in records)',
            'Verified all ten modal pages, including both original two-page Maria sequences.':
                'Verified all four original crowd panels with the native modal consumer.',
        })
        scope = vars(checks) | globals()
        exec(compile(source, __file__ + "::crowd-panels", "exec"), scope)
        scope["check_modal"]()
    if not CHOICES.exists():
        source = checked_text(previous.checked.choice_source, {
            'len(choices) == 8': 'len(choices) == 2',
            'Verified all eight original choice captions, slots and complete objects.':
                'Verified both original sail-lesson choice captions and the complete object.',
        })
        scope = vars(previous.checked) | globals() | dict(CHOICES=CHOICES)
        exec(compile(source, __file__ + "::retained-sail-lesson-choices", "exec"), scope)
        scope["check_choices"]()


def ordinary():
    assert base.digest(stage.ROM) == base.load(stage.PROOF)["candidate_sha256"]
    schedule, frames, end, _, donor = observer.schedule("athens")
    folder = ROOT / "istanbul"
    folder.mkdir(parents=True)
    inputs = folder / "inputs.json"
    base.save(inputs, schedule)
    harness = fixture.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(folder / "capture"),
        "--frames", str(end), "--inputs-json", str(inputs), "--press-start", "-1",
        "--battery-save", donor["source"], "--touchscreen", "--capture-every", "999999",
        "--capture-at", *map(str, frames)]
    harness.main()


def verify_ordinary():
    path = report("istanbul")
    capture = base.load(path)
    schedule, _, end, reference, donor = observer.schedule("athens")
    assert capture["ROM_sha256"] == base.digest(stage.ROM) and capture["frames"] == end
    assert capture["scripted_input_schedule"] == schedule
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert capture["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert capture["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    targets = {row["id"]: row for row in base.load(stage.NATIVE)["records"] if row["block"] == 158 and row["layouts"]}
    unvisited = record_id(158, 158)
    source = {row["id"]: row for row in base.load(stage.REVIEW)["records"]}
    _, _, _, names = focus["display_context"]()
    frames = sorted(hold["frame"] for hold in capture["frames_captured"] if hold["frame"] >= 2950)
    found, pictures, visited = {}, [], set()
    for frame in frames:
        hold, screen = gameplay.screen(capture, frame)
        for ident, target in targets.items():
            if ident in visited:
                continue
            page, = target["layouts"][0]["pages"]
            if gameplay.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, screen):
                row = source[ident]
                gameplay.glyphs(names, screen, row["speaker"], (16, 277), gameplay.LABEL_COLOR, 226)
                found[ident] = previous.branch_fixture.observation(row, "istanbul", hold, target["command_offset"])
                pictures.append((f"Istanbul / {ident}", screen))
                visited.add(ident)
    assert set(targets) - visited == {unvisited}, (set(targets) - visited)
    hold, screen = gameplay.screen(capture, frames[-1])
    pictures.append(("Istanbul / after the original scene", screen))
    return list(found.values()), pictures, dict(original_input_reference=str(reference),
        donor_sha256=donor["source_sha256"], capture_sha256=base.digest(path),
        original_town_trigger=True, conditional_revision_unvisited=unvisited, exit=hold)


def verify():
    assert not LIVE.exists()
    focus["SAMPLES"] = samples()
    observations, pictures, reports, exits = focus["verify_excerpts"]()
    verify_branches = FunctionType(previous.verify_branches.__code__,
        previous.verify_branches.__globals__ | globals() | dict(checked=sys.modules[__name__]))
    more, choices, menu_reports, sheets = verify_branches()
    observations.extend(more)
    ordinary_observations, ordinary_pictures, ordinary_proof = verify_ordinary()
    for label, rows in (("focused_dialogue", pictures), ("ordinary_istanbul", ordinary_pictures)):
        for start in range(0, len(rows), 6):
            path, sha = gameplay.make_sheet(ROOT / f"{label}_{1 + start // 6}.png", rows[start:start + 6])
            sheets.append(dict(path=path, sha256=sha))
    revised = {row["id"] for row in base.load(stage.REVIEW)["records"] if row["decision"] == "revision"}
    assert revised - {row["id"] for row in observations + ordinary_observations} == {record_id(158, 158)}
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, report_sha256=reports | menu_reports, return_frames=exits,
        original_menu_choices=choices, sheets=sheets, initialized_excerpts=True,
        ordinary_story_observations=ordinary_observations, ordinary_story_evidence=ordinary_proof,
        hardware=False))
    print(f"Verified {len(observations)} focused holds, both sail lesson choices and {len(ordinary_observations)} ordinary holds.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "ordinary", "replay", "prepare_choice", "verify", *RUNS))
    action = cli.parse_args().action
    if action == "prepare_choice":
        focus["SAMPLES"] = samples()
        focus["prepare_choice"](171)
    elif action == "replay":
        focus["SAMPLES"] = samples()
        focus["replay"](1)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
