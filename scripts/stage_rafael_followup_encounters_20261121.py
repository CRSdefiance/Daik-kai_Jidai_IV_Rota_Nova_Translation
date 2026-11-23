"""Stage Rafael's follow-up scenes with the validated mixed-object compiler."""

from types import FunctionType

from scripts import review_rafael_followup_encounters_20261121 as review
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v2"
ROM, PROOF = ROOT / "Rafael_Followup_Encounters_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT


def rebuild_function():
    rebuild = compiler.rebuild_function()
    env = rebuild.__globals__ | {"plan_progressive": review.plan_progressive}
    env["changed_speech"] = FunctionType(env["changed_speech"].__code__, env)
    env["changed_styles"] = FunctionType(env["changed_styles"].__code__, env)
    return FunctionType(rebuild.__code__, env)


if __name__ == "__main__":
    source = checked_text(compiler.source, {"stage.system.native_painter(ctx)": "current_fe_painter(ctx)"})
    scope = compiler.env | globals() | {"paired": review}
    exec(compile(source, __file__, "exec"), scope)
    scope["main"]()
