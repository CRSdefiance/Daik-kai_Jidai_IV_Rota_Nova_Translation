"""Stage the source-reviewed Hodram wrap fixes in B221–B260."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_remaining_wrap_leads_20261123 as paired
from scripts import register_observed_wrap_followups_20261123 as registered
from scripts import stage_hodram_late_story_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
BATCH = Path(".codex-release-work/hodram_b221_b260_wrap_fixes_20261123/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_B221_B260_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
MANUSCRIPT = paired.OUTPUT.with_name("b221_b260_review.md")
ARCHIVE = prior.ARCHIVE
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
parent = SimpleNamespace(ROM=registered.ROM, MANIFEST=registered.MANIFEST, RELEASE=registered.RELEASE,
    STARTUP_CAPTURE=registered.STARTUP_CAPTURE, guard_spec=registered.guard_spec,
    bind_registered_story_percent_guard=registered.bind_registered_story_percent_guard)
PROTECTION = {
    (221, 43): ["A weapon they might have used", "Just thinking about it", "right back to ancient times."],
    (224, 57): ["He's a giant in Islamic history.", "Repelling the Crusaders"],
    (225, 57): ["I got carried away.", "Shall we get back to work?"],
    (226, 56): ["interested in Asian history?"],
    (227, 26): ["The Medusa Shield was on my mind.", "They say it's in the Tasman Sea.", "Your eyes reminded me of it."],
    (229, 47): ["That's a stern lesson.", "We'd better stay on guard, then?"],
    (229, 57): ["linked to Attila.", "Only a rumor, mind you."],
    (231, 13): ["You know what an armadillo is?", "Heard its hide's harder than iron."],
    (232, 13): ["You know what a giant tortoise is?", "Heard its shell's harder than iron."],
    (237, 51): ["make a living", "on our own again.", "my great-grandfather's generation."],
    (238, 47): ["what made that sound", "a natural phenomenon."],
    (239, 33): ["Back in the Gupta dynasty, someone", "made a statue of a sacred beast.", "see the future!"],
    (240, 28): ["a master archer", "work with cannons.", "who's tending the ship?"],
    (240, 38): ["over a silly rumor!", "If it were that close,", "found it by now!"],
    (242, 32): ["I'm glad it's yours again."],
    (246, 15): ["Go see them while you're here.", "I'll give you directions."],
    (247, 6): ["Welcome, FI.", "Another lovely day, isn't it?"],
    (251, 110): ["What a beautiful figurehead.", "Just looking at it", "such a sense of peace..."],
    (254, 9): ["Ruins all over the world?", "We don't have any famous ones here."],
    (255, 10): ["Looking for ruins the world over?", "I'm afraid we have none of note."],
    (258, 5): ["Yuris should be here somewhere."],
    (258, 34): ["forgot all about my estate!", "would you take me back?"],
}

scope = prior.scope | globals()
proposal_source = checked_text(getsource(prior.prior.proposals), {"len(rows) == 25": "len(rows) == 29"})
exec(compile(proposal_source, __file__ + "::manuscript", "exec"), scope)
source = checked_text(prior.source, {
    '    edits = proposals()':
        '    packet = packet | {"groups":[g for g in packet["groups"] if 221 <= g["block"] <= 260]}\n'
        '    edits = proposals()',
    'block == 218 and selector == 208': 'block in (226, 238, 239, 252) and selector == 208',
    'block in (200, 201, 205, 216)': 'block in (224, 243, 251, 252)',
    'len(records) == 259 and len(captions) == 22 and len(styles) == 7 and len(groups) == 17':
        'len(records) == 310 and len(captions) == 11 and len(styles) == 37 and len(groups) == 22',
    'sum(row["kind"] == "system" for row in records) == 17': 'sum(row["kind"] == "system" for row in records) == 16',
    '{"retention":237, "prose":22}': '{"retention":281, "prose":29}',
    'len(leads) == 22': 'len(leads) == 29',
})
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)
run = FunctionType(prior.run.__code__, scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    run(cli.parse_args().action)
