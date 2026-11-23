"""Apply the five violin-scene revisions using the registered script reassembler."""

from inspect import getsource
from types import FunctionType

from scripts import review_moonlit_violin_20261121 as review
from scripts import stage_all_routes_next_phrase_wraps_20261118 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage = earlier.base, earlier.native, earlier.stage
parent = review.parent
ROOT = review.ROOT / "staged"
ROM, PROOF = ROOT / "Moonlit_Violin_STAGED.nds", ROOT / "stored_proof.json"
logical_end = earlier.logical_end


def main():
    previous = earlier.prior.precedent
    build = previous.env["main"]
    settings = build.__globals__ | globals() | {"paired": review, "company": earlier.company}
    rebuild = checked_text(getsource(previous.rebuild_function), {
        "precedent.plan_progressive": "company.plan_progressive",
    })
    exec(compile(rebuild, __file__ + "::progressive", "exec"), settings)
    settings["catalogue_membership"] = FunctionType(previous.catalogue_membership.__code__, settings)
    program = checked_text(previous.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
        "Staged 17 source-bound wraps with exact catalogue ownership, branches and whole-ROM inverse.":
            "Staged the two violin exchanges with exact catalogue ownership, branches and whole-ROM inverse.",
    })
    exec(compile(program, __file__ + "::deploy", "exec"), settings)
    settings["main"]()
    proof = base.load(PROOF)
    assert proof["changed_blocks"] == {"/data/SC0.DK4": [51], "/data/SC1.DK4": [143]}
    assert proof["whole_parent_inverse"] and proof["candidate_sha256"] == base.digest(ROM)


if __name__ == "__main__":
    main()
