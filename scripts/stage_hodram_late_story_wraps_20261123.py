"""Apply the reviewed late Hodram exchanges with the verified native compiler."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_late_story_wraps_20261123 as paired
from scripts import register_hodram_late_midroute_wraps_20261123 as registered
from scripts import stage_hodram_late_midroute_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
BATCH = Path(".codex-release-work/hodram_late_story_wraps_20261123/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_Late_Story_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
MANUSCRIPT = paired.OUTPUT.with_name("working_review.md")
ARCHIVE = prior.ARCHIVE
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
parent = SimpleNamespace(ROM=registered.ROM, MANIFEST=registered.MANIFEST, RELEASE=registered.RELEASE,
    STARTUP_CAPTURE=registered.STARTUP_CAPTURE, guard_spec=registered.guard_spec,
    bind_registered_story_percent_guard=registered.bind_registered_story_percent_guard)
PROTECTION = {
    (181, 12): ["It's the color of passion.", "it takes me back to my youth.", "I was madly in love."],
    (185, 20): ["What a beautiful stone."],
    (186, 17): ["We'll see her in it soon.", "Other ladies will want one, too."],
    (197, 25): ["chili peppers", "A kind of spice, I'm told.", "our local food"],
    (201, 101): ["a celestial maiden", "What a foolish thought."],
    (204, 62): ["I won't feel right otherwise."],
    (205, 35): ["150,000 coins", "Meet me there, please."],
    (205, 87): ["This rope's still good.", "We can wait to replace it."],
    (211, 15): ["something besides food", "Now that's a surprise."],
    (212, 59): ["great sea battle", "lost her sword."],
    (214, 15): ["blade's tinged red", "drunk its fill of blood"],
    (214, 33): ["I can see why he'd do that.", "What became of the sword?"],
    (214, 36): ["where he hid it", "if we get the chance."],
    (215, 5): ["that little pond", "Is that...?"],
    (216, 32): ["That's wonderful!", "your favorite commander"],
    (218, 44): ["a disciple of Jesus", "one of the twelve.", "a place associated with him."],
    (218, 68): ["I shall write again if I hear more.", "Janus Pasar"],
    (218, 87): ["I won't object outright.", "Judas did repent in the end.", "It's your decision, Admiral."],
}

scope = vars(prior) | globals()
scope["proposals"] = FunctionType(prior.proposals.__code__, scope)
source = checked_text(getsource(prior.proposals), {"len(rows) == 25": "len(rows) == 22"})
exec(compile(source, __file__ + "::manuscript", "exec"), scope)
source = checked_text(getsource(prior.author), {
    "records, groups, captions, leads = [], [], [], set()": "records, groups, captions, styles, leads = [], [], [], [], set()",
    '            if row["native_command_word"] == 0x2100:\n                assert edit is None and block == 167':
        '''            if row["native_command_word"] == 0x4100:
                assert edit is None and block == 218 and selector == 208
                styles.append(entry | dict(slots=row["slots"], decision="retention"))
                continue
            if row["native_command_word"] in (0x2100, 0x2200):
                assert edit is None and block in (200, 201, 205, 216)''',
    'len(records) == 494 and len(captions) == 2 and len(groups) == 15':
        'len(records) == 259 and len(captions) == 22 and len(styles) == 7 and len(groups) == 17',
    'sum(row["kind"] == "system" for row in records) == 50': 'sum(row["kind"] == "system" for row in records) == 17',
    '{"retention":469, "wrap_only":1, "prose":24}': '{"retention":237, "prose":22}',
    'len(leads) == 20': 'len(leads) == 22',
    'records=records, retained_choice_labels=captions, counts=counts':
        'records=records, retained_choice_labels=captions, retained_style_variants=styles, counts=counts',
    'len(records)+len(captions)': 'len(records)+len(captions)+len(styles)',
})
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)
run = FunctionType(prior.run.__code__, scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    run(cli.parse_args().action)
