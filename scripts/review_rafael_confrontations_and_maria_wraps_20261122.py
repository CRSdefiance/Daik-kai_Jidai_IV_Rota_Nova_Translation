"""Review three Rafael scenes and bind two observed Maria wrap repairs."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import cleanup_camille_and_maria_reveals_20261122 as checkpoint
from scripts import register_camille_and_maria_reveals_20261122 as parent
from scripts import review_lil_lessons_and_maria_scenes_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
established, template = precedent.established, precedent.template
bind_scope = precedent.bind_scope
ROOT = Path("work/analysis/rafael_confrontations_and_maria_wraps_20261122/refined")
REVIEW, PREFLIGHT = ROOT / "contextual_review.json", ROOT / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("rafael_confrontations_and_maria_wraps_20261122.md")
OBSERVED = checkpoint.FOLLOWUP
CHOICES, READABILITY, FINAL_READABILITY = {}, {}, {}

sections = checked_text(getsource(precedent.load_sections), {"[23]": "[03]"})
namespace = vars(precedent) | globals()
exec(compile(sections, __file__ + "::sections", "exec"), namespace)
CONTEXT, DECISIONS = namespace["load_sections"]()


def review():
    ROOT.parent.mkdir(exist_ok=True)
    source = checked_text(getsource(precedent.review), {
        'len(checked) == 227 and len(choice_proofs) == 3 and sum(r["kind"] == "system" for r in checked) == 3':
            'len(checked) == 207 and not choice_proofs and sum(r["kind"] == "system" for r in checked) == 5',
        'across eight scenes': 'across four scenes',
    })
    scope = vars(precedent) | globals()
    exec(compile(source, __file__ + "::whole-exchange-review", "exec"), scope)
    scope["review"]()
    observed = base.load(OBSERVED)
    checked = base.load(REVIEW)
    assert observed["candidate_sha256"] == checked["candidate_sha256"]
    assert [row["id"] for row in observed["rows"]] == ["DK4_MES_B36_R0034", "DK4_MES_B36_R0049"]
    for lead in observed["rows"]:
        row, = (r for r in checked["records"] if r["route"] == 3 and r["id"] == lead["id"])
        assert row["change_class"] == "wrap_only" and row["english"] == row["previous_English"] == lead["wording"]
        for ref in ("source_reference", "current_reference"):
            assert row[ref]["exact_command_hex"] == lead[ref]["exact_command_hex"]
        assert any(lead["protected_phrase_to_check"] in phrase for phrase in row["protected_phrases"])
        hold = lead["focused_replay_hold"]
        assert base.digest(hold["path"]) == hold["PNG_sha256"]


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight"))
    if cli.parse_args().action == "review":
        review()
    else:
        preflight = established.preflight
        FunctionType(preflight.__code__, preflight.__globals__ | globals())()
