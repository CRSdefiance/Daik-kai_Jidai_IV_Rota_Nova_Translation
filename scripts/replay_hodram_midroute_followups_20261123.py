"""Replay the revised Hodram panels and original resupply, trade, and story choices."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_hodram_early_and_midroute_wraps_20261122 as previous
from scripts import replay_rafael_midroute_exchanges_20261122 as branch
from scripts import stage_hodram_midroute_followups_20261123 as stage
from scripts import verify_hodram_midroute_followups_20261123 as checked
from scripts.source_locked_derivation_v5118 import checked_text

base, native, menu = stage.base, stage.native, previous.menu
gameplay = menu.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
ARCHIVE = "/data/SC1.DK4"
PROMPTS = {132: 96, 135: 9, 136: 9, 140: 103}
RESULTS = {
    132: ((110,), (151,)),
    135: ((24, 28, 32, 35), (45,)),
    136: ((24, 27, 31, 35, 38), (44,)),
    140: ((118,), (123,)),
}
RUNS = {f"b{block}_{slot}": (block, slot) for block in RESULTS for slot in range(2)}
BOOT = previous.prior.INPUTS[1]
record_id, branch_fixture, fixture = branch.record_id, branch.branch_fixture, branch.fixture


def samples():
    context = {"DK4_MES_B100_R0038", "DK4_MES_B110_R0047", "DK4_MES_B123_R0051", "DK4_MES_B132_R0145"}
    excerpt_exclusions = {record_id(block, ordinal) for block, groups in RESULTS.items()
                          for ordinal in (PROMPTS[block], *(o for group in groups for o in group))}
    draft = base.load(stage.REVIEW)
    return {1: tuple((r["block"], int(r["id"].rsplit("R",1)[1])) for r in draft["records"]
        if (r["decision"] == "revision" and r["id"] not in excerpt_exclusions) or r["id"] in context)}


def route_rom(route):
    return ROOT / f"route{route}" / "Hodram_Midroute_Followups_FOCUSED_ONLY.nds"


def report(run):
    return ROOT / run / "capture/capture_report.json"


def choice_paths(block):
    folder = ROOT / f"b{block}_choice"
    return folder, folder / f"Hodram_B{block}_Choice_FOCUSED_ONLY.nds", folder / "fixture.json"


scope = previous.scope | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    inherited = previous.scope[name]
    scope[name] = FunctionType(inherited.__code__, scope)
exec(compile(previous.prepare_source, __file__ + "::exact-original-choice-suffix", "exec"), scope)
branch_frames = FunctionType(branch.branch_frames.__code__, branch.branch_frames.__globals__ | globals())
play_choice = FunctionType(branch.play_choice.__code__, branch.play_choice.__globals__ | globals())
source = checked_text(getsource(branch.verify_branches), {
    'bodies = {(0, r["id"])': 'bodies = {(1, r["id"])',
    'modals = {(0, r["id"])': 'modals = {(1, r["id"])',
    'bodies[0, row["id"]]': 'bodies[1, row["id"]]',
    'f"SC0 B{block}': 'f"SC1 B{block}',
    'rafael_midroute_menus_': 'hodram_midroute_menus_',
})
exec(compile(source, __file__ + "::menu-outcome-verifier", "exec"), globals())


def verify():
    scope["SAMPLES"] = samples()
    observations, pictures, reports, exits = scope["verify_excerpts"]()
    branches, choices, menu_reports, menu_sheets = verify_branches()
    observations.extend(branches)
    reports.update(menu_reports)
    sheets = []
    for offset in range(0, len(pictures), 6):
        name, digest = gameplay.make_sheet(ROOT / f"hodram_midroute_excerpts_{1+offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=name, sha256=digest))
    draft = base.load(stage.REVIEW)
    assert {r["id"] for r in draft["records"] if r["decision"] == "revision"} <= {r["id"] for r in observations}
    assert len(choices) == 8
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, report_sha256=reports, return_frames=exits, original_menu_choices=choices,
        sheets=sheets + menu_sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(observations)} focused holds and all eight original choice outcomes.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "prepare_choices", "verify", *RUNS))
    action = cli.parse_args().action
    scope["SAMPLES"] = samples()
    if action == "replay":
        scope["replay"](1)
    elif action == "prepare_choices":
        for block in PROMPTS:
            scope["prepare_choice"](block)
    elif action in RUNS:
        play_choice(action)
    else:
        verify()
