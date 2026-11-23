"""Compile Rafael's departure and debrief with room for all original names."""

from inspect import getsource
from types import FunctionType

from scripts import review_rafael_first_voyage_debrief_20261119 as review
from scripts import stage_london_guild_assignments_20261118 as layout
from scripts import stage_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = review.base, review.native, review.stage, review.parent
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Rafael_Departure_and_Debrief_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end, paired = workflow.logical_end, review.paired
MAX_COMPANY_CELLS = 20


def rebuild_function():
    original = workflow.rebuild_function()
    longest = 'return text.replace("{MACRO:FA}", "W" * 16).replace("{MACRO:FI}", "W" * 16)'
    source = checked_text(getsource(layout.plan_progressive), {
        longest: longest + '.replace("{MACRO:FO}", "W" * MAX_COMPANY_CELLS)',
        "maximum_expanded_FI_FA_length=16)":
            "maximum_expanded_FI_FA_length=16, maximum_tested_FO_length=MAX_COMPANY_CELLS)",
    })
    scope = vars(layout) | globals()
    exec(compile(source, __file__ + "::company-display-budget", "exec"), scope)
    env = original.__globals__ | {"plan_progressive": scope["plan_progressive"]}
    for func in (stage.changed_speech, stage.changed_styles):
        env[func.__name__] = FunctionType(func.__code__, env)
    return FunctionType(original.__code__, env)


if __name__ == "__main__":
    env = workflow.env | globals()
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, env)
    FunctionType(workflow.env["main"].__code__, env)()
