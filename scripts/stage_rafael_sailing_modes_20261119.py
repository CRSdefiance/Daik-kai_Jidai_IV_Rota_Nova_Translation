"""Stage the sailing lesson with separate progressive, FE, and typed-choice handling."""

from inspect import getsource
from types import FunctionType

from scripts import review_rafael_sailing_modes_20261119 as review
from scripts import stage_london_guild_assignments_20261118 as workflow
from scripts import stage_story_tag_wraps_20261118 as catalogue
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = workflow.base, workflow.native, workflow.stage
parent, paired = review.parent, review
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Rafael_Sailing_Modes_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = stage.logical_end


def rebuild_function():
    env = vars(stage) | {"plan_progressive": workflow.plan_progressive}
    fe = checked_text(getsource(stage.plan_fe), {
        "phrases(paragraph)": 'tuple(row["protected_phrases"])',
    })
    exec(compile(fe, __file__ + "::FE-phrases", "exec"), env)
    for fn in (stage.changed_speech, stage.rebuild):
        env[fn.__name__] = FunctionType(fn.__code__, env)
    return env["rebuild"]


source = checked_text(getsource(workflow.main), {
    "    final = native.files(target)":
        "    final = native.files(target)\n    catalogue_membership(ctx.arm, initial, final)",
    "Assembled all revised guild exchanges with exact relative branches and whole-ROM inverse.":
        "Staged both sailing lesson paths with typed-choice bytes and exact relative branches.",
})
env = vars(workflow) | globals()
env["catalogue_membership"] = FunctionType(catalogue.catalogue_membership.__code__, env)
exec(compile(source, __file__ + "::cumulative-story-block", "exec"), env)

if __name__ == "__main__":
    env["main"]()
    receipt = base.load(PROOF)
    assert receipt["whole_parent_inverse"] and receipt["changed_blocks"] == {"/data/SC0.DK4": [46]}
