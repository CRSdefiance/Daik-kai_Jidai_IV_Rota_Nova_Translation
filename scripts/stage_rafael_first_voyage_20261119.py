"""Compile the first-voyage dialogue using the registered story relocation workflow."""

from inspect import getsource

from scripts import review_rafael_first_voyage_20261119 as review
from scripts import stage_rafael_deck_lesson_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, template = workflow.base, workflow.native, workflow.stage, workflow.template
parent, logical_end = review.parent, workflow.logical_end
ROOT = review.ROOT / "research_v1"
ROM = ROOT / "Rafael_First_Voyage_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"

source = checked_text(getsource(workflow.main), {
    'assert receipt["whole_parent_inverse"] and receipt["changed_blocks"] == {"/data/SC0.DK4": [43]}':
        'assert receipt["whole_parent_inverse"] and receipt["changed_blocks"] == {"/data/SC0.DK4": [42]}',
})
env = vars(workflow) | globals()
exec(compile(source, __file__ + "::source-locked-relocation", "exec"), env)

if __name__ == "__main__":
    env["main"]()
