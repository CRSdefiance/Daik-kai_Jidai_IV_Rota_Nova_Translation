"""Bind the reveal scenes to the active ROM and verify the proposed native layouts."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import cleanup_lil_lessons_and_maria_scenes_20261122 as checkpoint
from scripts import register_lil_lessons_and_maria_scenes_20261122 as parent
from scripts import review_lil_lessons_and_maria_scenes_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
established = precedent.established
ROOT = Path("work/analysis/camille_and_maria_reveals_20261122")
REVIEW, PREFLIGHT = ROOT / "contextual_review.json", ROOT / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("camille_and_maria_reveals_20261122.md")
CONTEXT, DECISIONS = FunctionType(precedent.load_sections.__code__, vars(precedent) | {"MANUSCRIPT": MANUSCRIPT})()
CHOICES = {}
READABILITY = {
    (2, 65, 198): ("", "I never imagined;I'd see my son again here.", "Let the hesitant address lead into the unexpected reunion. Keep I'd with the verb and the explicit relationship."),
    (2, 127, 57): ("Luck's one thing. Watching closely gives you insight. You need both to win.",
                   "Luck's one thing.;Watching closely gives you insight.;You need both to win.",
                   "Preserve the distinction between luck and observation and let each point land clearly."),
    (3, 19, 188): ("Those men were my father's crew. I grew up copying them, learning how to fight with a sword and live as a pirate.",
                   "my father's crew.;I grew up copying them,;learning how to fight with a sword;live as a pirate.",
                   "Aziza recounts learning by imitating the crew. Keep her two kinds of learning clear."),
    (3, 36, 45): ("", "You don't know what Kuhn's;really like...;He plans to use you;for all you're worth,;then get rid of you.",
                  "Keep the original idiom intact. Give the opening enough room and carry her warning through the consequence."),
}
FINAL_READABILITY = READABILITY
template = precedent.template
bind_scope = precedent.bind_scope


def verify_inputs():
    receipt = base.load(checkpoint.FOLLOWUP)
    assert receipt["candidate_sha256"] == base.digest(parent.ROM)
    assert receipt["formatting_proposal_pending"] and receipt["source_words_still_approved"]
    assert [(r["id"], r["proposed_protected_phrase"]) for r in receipt["rows"]] == [
        ("DK4_MES_B36_R0037", "the people of Southeast Asia."), ("DK4_MES_B36_R0045", "for all you're worth,")]
    for row in receipt["rows"]:
        assert base.digest(row["initialized_replay_hold"]["path"]) == row["initialized_replay_hold"]["PNG_sha256"]
    return receipt


def review():
    observed = verify_inputs()
    source = checked_text(getsource(precedent.review), {
        'len(checked) == 227 and len(choice_proofs) == 3 and sum(r["kind"] == "system" for r in checked) == 3':
            'len(checked) == 192 and not choice_proofs and sum(r["kind"] == "system" for r in checked) == 1',
        'across eight scenes': 'across six scenes',
        '''        '    common = parse(FERNANDO)\\n': '',''':
            '''        '    common = parse(FERNANDO)\\n': '',
        '    ROOT.mkdir(exist_ok=True)': ''' + repr('''    for earlier in observed["rows"]:
        row, = (r for r in checked if r["file_path"] == "/data/SC3.DK4" and r["id"] == earlier["id"])
        assert row["decision"] == "revision" and row["english"] == row["previous_English"] == earlier["wording"]
        assert row["source_reference"]["exact_command_hex"] == earlier["source_reference"]["exact_command_hex"]
        assert row["current_reference"]["exact_command_hex"] == earlier["current_reference"]["exact_command_hex"]
        assert earlier["proposed_protected_phrase"] in row["protected_phrases"]
    ROOT.mkdir(exist_ok=True)''') + ',',
        'scope = vars(template) | globals()': 'scope = vars(template) | globals() | {"observed": observed}',
    })
    scope = vars(precedent) | globals() | {"observed": observed}
    exec(compile(source, __file__ + "::six-scene-review", "exec"), scope)
    scope["review"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight"))
    cli.add_argument("--refined", action="store_true")
    args = cli.parse_args()
    if args.refined:
        ROOT = ROOT / "refined"
        REVIEW, PREFLIGHT = ROOT / REVIEW.name, ROOT / PREFLIGHT.name
    if args.action == "review":
        review()
    else:
        preflight = established.preflight
        FunctionType(preflight.__code__, preflight.__globals__ | globals())()
