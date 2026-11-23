"""Verify the next Rafael exchanges in a focused native controller replay."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_athens_and_maria_crew_20261122 as fixture
from scripts import stage_rafael_six_followup_exchanges_20261122 as stage
from scripts import verify_rafael_athens_and_maria_crew_20261122 as proof
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
GLYPH_PROOF = stage.ROOT / "glyph_and_sheet_verification.json"
SAMPLE = {0: (
    *((50, n) for n in (31, 49, 53, 86, 111, 119)),
    (52, 18),
    *((55, n) for n in (36, 44, 54, 67, 115, 178)),
    (57, 76), (57, 80),
    *((61, n) for n in (22, 75, 113)),
    (62, 5),
)}
scope = vars(fixture) | globals()
for name in ("receipt", "report_path", "run_file", "fixture", "play"):
    original = getattr(fixture, name)
    scope[name] = FunctionType(original.__code__, scope)
source = checked_text(getsource(fixture.verify), {
    '== 10': '== 3',
    'maria_existing_unlock_fixture=True, ': '',
    'athens_and_crew_verified_': 'rafael_followup_verified_',
    'and both original host transitions.': 'and the return to port.',
})
exec(compile(source, __file__ + "::controller-verification", "exec"), scope)
modal_source = checked_text(getsource(proof.check_modal), {
    'assert len(records) == 10 and sum(r["second_page"] for r in records) == 2':
        'assert len(records) == 3 and not any(r["second_page"] for r in records)',
    'Verified all ten modal pages, including both original two-page Maria sequences.':
        'Verified the three original Sofala and military-funds notices.',
})
modal_scope = vars(proof) | globals()
exec(compile(modal_source, __file__ + "::unchanged-modal-pages", "exec"), modal_scope)
check_glyphs = FunctionType(proof.check_glyphs.__code__,
    proof.check_glyphs.__globals__ | dict(stage=stage, OUTPUT=GLYPH_PROOF))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "formatting", "verify"))
    action = cli.parse_args().action
    if action == "replay":
        scope["fixture"](0)
        scope["play"](0)
    elif action == "formatting":
        check_glyphs()
        modal_scope["check_modal"]()
    else:
        scope["verify"]()
