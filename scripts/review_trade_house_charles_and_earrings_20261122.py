"""Bind the four whole-exchange reviews and apply registered native preflight."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import cleanup_rafael_confrontations_and_maria_wraps_20261122 as checkpoint
from scripts import register_rafael_confrontations_and_maria_wraps_20261122 as parent
from scripts import review_lil_lessons_and_maria_scenes_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
established, template = precedent.established, precedent.template
bind_scope = precedent.bind_scope
ROOT = Path("work/analysis/trade_house_charles_and_earrings_20261122/refined")
REVIEW, PREFLIGHT = ROOT / "contextual_review.json", ROOT / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("trade_house_charles_and_earrings_20261122.md")
READABILITY, FINAL_READABILITY = {}, {}
CHOICES = {
    (1, 210, 0): ("Acknowledge the information pitch or press him for its relevance.",
                  "Got it and So what? preserve the contrasting levels of interest and their original order."),
    (1, 210, 1): ("Accept the offer or object to the cost.",
                  "I'll take them! and Pricey still express the direct commitment and distinct objection to the price."),
}
sections = checked_text(getsource(precedent.load_sections), {"[23]": "[01]"})
namespace = vars(precedent) | globals()
exec(compile(sections, __file__ + "::sections", "exec"), namespace)
CONTEXT, DECISIONS = namespace["load_sections"]()


def review():
    ROOT.parent.mkdir(exist_ok=True)
    source = checked_text(getsource(precedent.review), {
        'len(checked) == 227 and len(choice_proofs) == 3 and sum(r["kind"] == "system" for r in checked) == 3':
            'len(checked) == 119 and len(choice_proofs) == 2 and all(r["kind"] == "progressive" for r in checked)',
        'across eight scenes': 'across four scenes',
    })
    scope = vars(precedent) | globals()
    exec(compile(source, __file__ + "::whole-exchange-review", "exec"), scope)
    scope["review"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight"))
    if cli.parse_args().action == "review":
        review()
    else:
        preflight = established.preflight
        FunctionType(preflight.__code__, preflight.__globals__ | globals())()
