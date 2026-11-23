"""Assemble the name and rumor review on the registered cumulative candidate."""

from inspect import getsource
from types import FunctionType

from scripts import review_naturalist_aliases_and_shield_20261119 as review
from scripts import stage_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = workflow.base, workflow.native, workflow.stage
parent, paired = review.parent, review.paired
ROOT = review.ROOT / "research_v3"
ROM = ROOT / "Naturalist_Aliases_and_Shield_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"


def plan_fe(row, painter, current_body):
    system = stage.system
    for _, lines, encoded in system.candidate_rows(row["english"], tuple(row["protected_phrases"])):
        body = encoded[1:]
        padded = body + b" " * ((len(body) - len(current_body)) % 2)
        normal, stored = painter(body), painter(padded)
        try:
            system.check_FE_rows(body, normal)
            system.check_FE_rows(padded, stored)
        except AssertionError:
            continue
        if normal["physical"] != stored["physical"] or system.visible_events(normal) != system.visible_events(stored):
            continue
        return body, dict(lines=lines, expected_native_pages=1, encoded_hex=encoded.hex())
    raise AssertionError(f"No byte-aligned FE layout for {row['id']}")


def rebuild_function():
    inherited = workflow.rebuild_function()
    scope = inherited.__globals__ | {"plan_fe": plan_fe}
    changed = checked_text(getsource(stage.changed_speech), {
        "plan_fe(row, painter)": "plan_fe(row, painter, raw_current[1:])",
    })
    exec(compile(changed, __file__ + "::parity-aware-FE", "exec"), scope)
    return FunctionType(inherited.__code__, scope)


def main():
    scope = workflow.env | globals()
    scope["catalogue_membership"] = FunctionType(workflow.env["catalogue_membership"].__code__, scope)
    FunctionType(workflow.env["main"].__code__, scope)()


if __name__ == "__main__":
    main()
