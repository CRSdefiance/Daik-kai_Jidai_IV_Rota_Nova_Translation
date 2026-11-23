"""Bind the Lil and Maria whole-scene decisions and run native preflight."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import re
from types import FunctionType

from scripts import cleanup_tavern_and_proof_exchanges_20261122 as checkpoint
from scripts import register_tavern_and_proof_exchanges_20261122 as parent
from scripts import review_tavern_and_proof_exchanges_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
established = template.established
ROOT = Path("work/analysis/lil_lessons_and_maria_scenes_20261122")
REVIEW, PREFLIGHT = ROOT / "contextual_review.json", ROOT / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("lil_lessons_and_maria_scenes_20261122.md")
CHOICES = {
    (2, 164, 0): ("Hear the advice or decline.", "Listen and Skip clearly distinguish the two branches of the ship-buying lesson."),
    (2, 166, 0): ("Ask Manuel to continue or decline.", "Please do answers the courteous offer and Decline labels the corresponding alternative succinctly."),
    (2, 167, 0): ("Accept the lesson or pass.", "The two colloquial answers suit Lil and identify each original branch."),
}
READABILITY = {
    (2, 164, 25): ("", "You're wrong because you're wrong!;The Earth doesn't have an edge.;Everybody knows that by now!",
                   "Give the circular retort its own beat. The reason, emphatic conclusion and appeal to common knowledge remain clear."),
    (2, 166, 20): ("", "Maybe some extra sails...;Or a different type of basic sail...",
                   "Keep Manuel's two distinct suggestions as he thinks aloud."),
    (2, 166, 52): ("", "your ship is crying.;Please take better care of her.",
                   "Keep the image that Camille echoes and the full request that follows it."),
    (2, 166, 68): ("", "He's amazing!;FI, we could use;someone like him aboard.",
                   "Camille's interjection and invitation stay clear with the original given-name substitution."),
    (2, 167, 71): ("Square sails are transverse sails. They're rigged across the ship.",
                   "Square sails are transverse sails.;They're rigged across the ship.",
                   "Introduce the sail type and immediately define the orientation as the Shipwright does."),
    (2, 167, 88): ("The upper sail is called a topsail. It's a small square sail rigged high on each mast.",
                   "The upper sail is called a topsail.;It's a small square sail;rigged high on each mast.",
                   "Keep the approved topsail term, then define its shape and position together."),
    (3, 36, 41): ("I'm only helping him! You're the pirate who runs China's underworld!",
                  "I'm only helping him!;You're the pirate;who runs China's underworld!",
                  "The counteraccusation stays in Lil's voice and keeps both her claims about Maria together."),
}
FINAL_READABILITY = READABILITY | {
    (2, 166, 5): ("Are the sails in the wrong place? No, maybe it's...",
                  "Are the sails in the wrong place?;No, maybe it's...",
                  "Manuel is thinking aloud about sail placement and immediately considers a different explanation."),
    (2, 166, 20): ("Maybe some extra sails... Or change the basic sail type...",
                   "Maybe some extra sails...;Or change the basic sail type...",
                   "Preserve the distinction between adding sails and changing their basic type. His unfinished alternatives sound like thoughts as they occur to him."),
    (2, 169, 156): ("Sailors from all over the world tell the women at the taverns their stories every day. They're bound to know something.",
                    "Sailors from all over the world;tell the women at the taverns;their stories every day.;They're bound to know something.",
                    "The explanation names who tells the stories and who hears them. Keep the conclusion whole and the daily frequency clear."),
}


def load_sections():
    pieces = re.split(r"^## SC([23]) B(\d+)\s*$", MANUSCRIPT.read_text(encoding="utf-8"), flags=re.M)
    assert not pieces.pop(0).strip() and len(pieces) % 3 == 0
    contexts, decisions = {}, {}
    for route, block, words in zip(pieces[::3], pieces[1::3], pieces[2::3], strict=True):
        key = int(route), int(block)
        assert key not in contexts
        contexts[key], decisions[key] = words.strip().split("\n\n", 1)
    return contexts, decisions


CONTEXT, DECISIONS = load_sections()
binding = checked_text(getsource(established.bind), {
    'and left[5]<207': 'and (left[5] < 207 or left[5] == 254)',
})
bind_scope = vars(established).copy()
exec(compile(binding, __file__ + "::progressive-and-retained-FE", "exec"), bind_scope)


def review():
    source = checked_text(getsource(template.contextual_review), {
        '    common = parse(FERNANDO)\n': '',
        '''        if block in (169, 136):
            aligned = {(i - int(route == 3 and i < 143)): value for i, value in common.items()}
            decisions = aligned | parse(ROUTE_TURNS[route])
            refinements = {i - int(route == 3 and i < 143): v for i, v in PARALLEL_REFINEMENTS.items()}
        else:
            decisions = parse(HODRAM[block])
            refinements = {}''': '        decisions = parse(DECISIONS[route, block])',
        'rows, _, _ = established.bind': 'rows, _, _ = bind_scope["bind"]',
        '''            if refined:
                replacement, protected, note = REFINEMENTS.get((route, block, ordinal),
                    refinements.get(ordinal, (replacement, protected, note)))''':
            '''            if refined:
                decisions_by_edition = FINAL_READABILITY if ROOT.name == "release" else READABILITY
                replacement, protected, note = decisions_by_edition.get((route, block, ordinal), (replacement, protected, note))''',
        '            ident = f"DK4_MES_B{block}_R{ordinal:04d}"':
            '            assert selector != 254 or change == "retention"\n            ident = f"DK4_MES_B{block}_R{ordinal:04d}"',
        'kind="progressive", speaker=names[selector], context=context, source_meaning=meaning,':
            'kind="system" if selector == 254 else "progressive", speaker=names.get(selector, "Speakerless panel"), context=context, source_meaning=meaning,',
        'assert len(checked) == 203 and len(choice_proofs) == 4':
            'assert len(checked) == 227 and len(choice_proofs) == 3 and sum(r["kind"] == "system" for r in checked) == 3',
        'wrap_queue_sha256=base.digest(queue.OUTPUT),': 'wrap_queue_sha256=base.digest(checkpoint.QUEUE), manuscript_sha256=base.digest(MANUSCRIPT),',
        'spoken turns and {len(choice_proofs) * 2} choice labels across five objects.':
            'dialogue and system records plus {len(choice_proofs) * 2} choice labels across eight scenes.',
    })
    scope = vars(template) | globals()
    exec(compile(source, __file__ + "::source-paired-review", "exec"), scope)
    scope["contextual_review"](ROOT.name in ("refined", "release"))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight"))
    cli.add_argument("--edition", choices=("initial", "refined", "release"), default="initial")
    args = cli.parse_args()
    if args.edition != "initial":
        ROOT = ROOT / args.edition
        REVIEW, PREFLIGHT = ROOT / REVIEW.name, ROOT / PREFLIGHT.name
    if args.action == "review":
        review()
    else:
        preflight = established.preflight
        FunctionType(preflight.__code__, preflight.__globals__ | globals())()
