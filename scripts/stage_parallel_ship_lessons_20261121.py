"""Relocate Cesare's three reviewed exchanges over the registered Hodram candidate."""
from inspect import getsource

from scripts import review_parallel_ship_lessons_20261121 as review
from scripts.stage_hodram_alexandria_tutorial_20261121 import compiler, plan_progressive as plan_story
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v1"
ROM, PROOF = ROOT / "Alexandria_Parallel_Ship_Lessons_STAGED.nds", ROOT / "stored_proof.json"


def plan_progressive(row, selector, current, original):
    if (row["route"], row["source_record_index"]) == (2, 140) and current.count(10) < 4:
        # Match the proven two-paragraph lesson at the exact original fact boundary.
        current += b"\n" * (4 - current.count(10))
    return plan_story(row, selector, current, original)


if __name__ == "__main__":
    source = checked_text(compiler.source, {
        "painter = stage.system.native_painter(ctx)": "painter = None",
        'assert manuscript["previous_sha256"] == packet["candidate_sha256"] == base.digest(parent.ROM)':
            'binding = base.load(review.BINDING)\n'
            '    assert binding["packet_sha256"] == base.digest(review.SOURCE)\n'
            '    assert manuscript["previous_sha256"] == binding["candidate_sha256"] == base.digest(parent.ROM)',
    })
    scope = compiler.env | globals() | {"paired": review}
    rebuild = checked_text(getsource(compiler.rebuild_function), {"workflow.plan_progressive": "plan_progressive"})
    exec(compile(rebuild, __file__ + "::rebuild", "exec"), scope)
    exec(compile(source, __file__, "exec"), scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"]
    assert proof["changed_blocks"] == {"/data/SC0.DK4": [177], "/data/SC2.DK4": [164], "/data/SC3.DK4": [135]}
