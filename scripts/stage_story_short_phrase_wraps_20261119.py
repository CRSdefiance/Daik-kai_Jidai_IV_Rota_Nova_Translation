"""Compile the revised phrase groups with the registered story loaders."""

from inspect import getsource
from types import FunctionType

from scripts import review_story_short_phrase_wraps_20261119 as review
from scripts import stage_london_guild_assignments_20261118 as workflow
from scripts import stage_story_tag_wraps_20261118 as catalogue
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage = workflow.base, workflow.native, workflow.stage
parent, paired = review.parent, review.paired
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Story_Short_Phrase_Wraps_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = stage.logical_end


def rebuild_function():
    scope = vars(stage) | {"plan_progressive": workflow.plan_progressive}
    fe = checked_text(getsource(stage.plan_fe), {
        "phrases(paragraph)": 'tuple(row["protected_phrases"])',
    })
    exec(compile(fe, __file__ + "::FE-phrases", "exec"), scope)
    for f in (stage.changed_speech, stage.changed_styles):
        scope[f.__name__] = FunctionType(f.__code__, scope)
    source = checked_text(getsource(stage.rebuild), {
        "        if w == SPEECH:": "        if w == SPEECH and owners:",
        "        elif w == STYLE:": "        elif w == STYLE and owners:",
        "        elif w in MENU:": "        elif w in MENU and owners:",
        "            else:\n                assert old == now":
            "            elif w not in (SPEECH, STYLE, *MENU):\n                assert old == now",
    })
    exec(compile(source, __file__ + "::only-reviewed-speech", "exec"), scope)
    return scope["rebuild"]


source = checked_text(getsource(workflow.main), {
    "    final = native.files(target)": "    final = native.files(target)\n    catalogue_membership(ctx.arm, initial, final)",
    "Assembled all revised guild exchanges with exact relative branches and whole-ROM inverse.":
        "Staged all revised story phrases with exact relative branches and whole-ROM inverse.",
})
env = vars(workflow) | globals()
env["catalogue_membership"] = FunctionType(catalogue.catalogue_membership.__code__, env)
exec(compile(source, __file__ + "::cumulative-story-blocks", "exec"), env)


if __name__ == "__main__":
    env["main"]()
