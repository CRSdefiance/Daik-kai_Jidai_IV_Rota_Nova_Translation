"""Compile the reviewed Hamburg exchange under the registered story layout rules."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import review_hamburg_ceramics_cross_route_20261120 as review
from scripts import stage_naturalist_aliases_and_shield_20261119 as aligned
from scripts import stage_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Hamburg_Ceramics_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
parent, paired = review.parent, review.paired
base, native = workflow.base, workflow.native


def current_fe_painter(ctx):
    from scripts.ruin_puzzle_fe_20261118 import fe, font

    earlier = font.old_FE
    assert base.digest(earlier.PROOF) == "8e5a09901540460452de462da6524fc52d599bd46d3a3d95d77919079e2f90ab"
    assert base.digest(earlier.PRIOR) == "3666fc972b56e1cbdda90ffbbe2bd0c972b391190a0862a9006f6ef585755b0e"
    # The old ROM is absent. Its sealed FE receipt identifies the original
    # descriptor proof. The rebound oracle still executes the current painter
    # and compares every glyph and canary against the independent model.
    source = checked_text(getsource(font.make_painter), {
        "sha(NdsImage.open('out/all_routes_combined_v4749_candidate.nds').read_file('/__arm9__.bin'))":
            "HISTORICAL_FE_ARM9_SHA",
    })
    env = vars(font) | dict(CURRENT_ARM9=native.digest(ctx.arm),
        HISTORICAL_FE_ARM9_SHA="d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa")
    # The derived painter's own namespace must carry the archived identity.
    source = checked_text(source, {
        "'CURRENT_ARM9':CURRENT_ARM9}":
            "'CURRENT_ARM9':CURRENT_ARM9,'HISTORICAL_FE_ARM9_SHA':HISTORICAL_FE_ARM9_SHA}",
    })
    exec(compile(source, __file__ + "::receipt-bound-current-FE", "exec"), env)
    make = FunctionType(fe.make_source_painter.__code__, vars(fe) |
                        dict(CURRENT_ARM9=native.digest(ctx.arm), ASCII_painter=env["make_painter"]))
    return make(ctx.image)[0]


if __name__ == "__main__":
    env = workflow.env | globals()
    catalogue_env = env | {"stage": workflow.stage}
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, catalogue_env)
    env["rebuild_function"] = aligned.rebuild_function
    env["stage"] = SimpleNamespace(system=SimpleNamespace(native_painter=current_fe_painter))
    FunctionType(workflow.env["main"].__code__, env)()
