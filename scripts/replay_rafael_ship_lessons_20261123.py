"""Verify the staged ship lessons with focused cold boots and native display checks."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_refitting_and_sailing_20261123 as current
from scripts import replay_rafael_basra_and_map_keys_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
stage = SimpleNamespace(
    ROOT=current.STAGED, ROM=current.ROM, PROOF=current.PROOF, NATIVE=current.NATIVE,
    REVIEW=current.REVIEW, FE_PROOF=current.STAGED / "unchanged_FE_pages.json",
    base=base, native=native, parent=current.parent, established=current.prior.established,
    typed=current.prior.typed, Path=Path, compiler_scope=current.compiler_scope,
)
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
EXCERPTS = ROOT / "verified_excerpts.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES = stage.ROOT / "original_choice_tables.json"
PROMPTS = {180: 13}
RESULTS = {180: ((63,), (31,))}
RUNS = {f"b180_choice{slot}": (180, slot) for slot in range(2)}
record_id = prior.record_id


def sample():
    draft = base.load(stage.REVIEW)
    return {0: tuple(
        (row["block"], int(row["id"].rsplit("R", 1)[1]))
        for row in draft["records"] if row["decision"] == "revision" or row["source_selector"] == 254
    )}


report = FunctionType(prior.report.__code__, globals())


def choice_paths(block):
    folder = ROOT / f"b{block}_sailing_choice"
    return folder, folder / f"Rafael_B{block}_Choice_FOCUSED_ONLY.nds", folder / "fixture.json"


branch_frames = FunctionType(prior.branch_frames.__code__, prior.branch_frames.__globals__ | globals())
play_choice = FunctionType(prior.play_choice.__code__, prior.play_choice.__globals__ | globals())
branch_scope = prior.branch_scope | globals()
exec(compile(prior.previous.prepare_source, __file__ + "::original-sail-choice", "exec"), branch_scope)

excerpt_scope = prior.excerpt_scope | globals() | dict(LIVE=EXCERPTS)
excerpt_scope["scope"] = excerpt_scope
for name in ("receipt", "report_path", "run_file", "play"):
    inherited = prior.excerpt_scope[name]
    excerpt_scope[name] = FunctionType(inherited.__code__, excerpt_scope)
fixture_source = checked_text(prior.fixture_source, {
    "Rafael_Basra_And_Map_Keys_FOCUSED_ONLY.nds": "Rafael_Ship_Lessons_FOCUSED_ONLY.nds",
})
excerpt_verify = checked_text(prior.excerpt_verify, {
    'r["layouts"] and r["id"] != record_id(146, 34)': 'r["layouts"]',
    "rafael_basra_excerpt_": "rafael_ship_lessons_excerpt_",
    "including both original market-share notices": "including the original armor notice",
})
for code in (fixture_source, excerpt_verify):
    exec(compile(code, __file__ + "::focused-excerpts", "exec"), excerpt_scope)


def formatting():
    glyphs = prior.display.verification.glyphs
    FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    original = prior.display.verification
    code = checked_text(getsource(original.check_modal), {
        'len(records) == 10 and sum(r["second_page"] for r in records) == 2':
            'len(records) == 1 and not records[0]["second_page"]',
        'Verified all ten modal pages, including both original two-page Maria sequences.':
            'Verified the original extra-armor modal panel.',
    })
    context = vars(original) | dict(stage=stage)
    exec(compile(code, __file__ + "::extra-armor-notice", "exec"), context)
    context["check_modal"]()
    code = checked_text(getsource(prior.display.check_choices), {
        "len(choices) == 5": "len(choices) == 6",
        "Verified all five original choice captions, slots and complete objects.":
            "Verified all six original captions and their exact choice tables.",
    })
    context = vars(prior.display) | dict(stage=stage, CHOICES=CHOICES)
    exec(compile(code, __file__ + "::unchanged-choice-captions", "exec"), context)
    context["check_choices"]()


def verify():
    excerpt_scope["SAMPLE"] = sample()
    if not EXCERPTS.exists():
        excerpt_scope["verify"]()
    code = checked_text(getsource(prior.previous.verify_branches), {
        "rafael_midroute_menus_": "rafael_ship_lessons_menus_",
    })
    context = vars(prior.previous) | globals() | dict(checked=SimpleNamespace(CHOICES=CHOICES))
    exec(compile(code, __file__ + "::native-choice-outcomes", "exec"), context)
    holds, choices, reports, sheets = context["verify_branches"]()
    excerpts = base.load(EXCERPTS)
    assert excerpts["candidate_sha256"] == base.digest(stage.ROM) and len(choices) == 2
    base.save(LIVE, dict(excerpts=excerpts, choice_holds=holds, choices=choices,
                        choice_reports=reports, choice_sheets=sheets, natural_story_activation=False, hardware=False))
    print(f"Verified both sailing-lesson outcomes and {len(holds)} original choice-path holds.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("formatting", "replay", "prepare_choice", "verify", *RUNS))
    action = parser.parse_args().action
    if action == "prepare_choice":
        branch_scope["prepare_choice"](180)
    elif action == "replay":
        excerpt_scope["SAMPLE"] = sample()
        excerpt_scope["fixture"](0)
        excerpt_scope["play"](0)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
