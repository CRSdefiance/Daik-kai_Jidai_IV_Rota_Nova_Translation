"""Compile the reviewed ruin and map-guide exchanges over the registered candidate."""

from types import FunctionType

from scripts import review_ruins_clues_and_guides_20261118 as review
from scripts import stage_london_guild_assignments_20261118 as previous


paired = review.current
base, native, stage, parent = previous.base, previous.native, previous.stage, review.parent
logical_end = stage.logical_end
ROOT = paired.ROOT / "research_v3"
ROM = ROOT / "Ruins_Clues_And_Guides_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"


def plan_fe(row, painter):
    for _, lines, raw in stage.system.candidate_rows(row["english"], row["protected_phrases"]):
        try:
            stage.system.check_FE_rows(raw[1:], painter(raw[1:]))
        except AssertionError:
            continue
        return raw[1:], dict(lines=lines, expected_native_pages=1, encoded_hex=raw.hex())
    raise ValueError(f"No complete native FE layout for {row['id']}")


def rebuild_function():
    scope = vars(stage) | {"plan_progressive": previous.plan_progressive, "plan_fe": plan_fe}
    for function in (stage.changed_speech, stage.changed_styles, stage.rebuild):
        scope[function.__name__] = FunctionType(function.__code__, scope)
    return scope["rebuild"]


if __name__ == "__main__":
    build = FunctionType(previous.main.__code__, vars(previous) | globals())
    build()
