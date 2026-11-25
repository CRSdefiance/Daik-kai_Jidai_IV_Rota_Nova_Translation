"""Compile the Rafael mosque sequence on the exact registered Overland ROM."""

from inspect import getsource

from scripts import review_rafael_mosque_20261118 as review
from scripts import stage_ruins_clues_and_guides_20261118 as inherited
from scripts.source_locked_derivation_v5118 import checked_text

previous = inherited.previous
base, native, stage, parent = inherited.base, inherited.native, inherited.stage, review.parent
paired = review
logical_end = stage.logical_end
ROOT = review.current.ROOT / "rafael_research_v1"
ROM = ROOT / "Rafael_Mosque_Rescue_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"


if __name__ == "__main__":
    source = checked_text(getsource(previous.main), {
        'for g in packet["groups"]}': 'for g in packet["groups"] if g["route"] == 0}',
        'Assembled all revised guild exchanges': 'Assembled the revised Rafael mosque exchanges',
    })
    scope = vars(previous) | globals() | {"rebuild_function": inherited.rebuild_function}
    exec(compile(source, __file__ + "::Rafael-only-owned-blocks", "exec"), scope)
    scope["main"]()
