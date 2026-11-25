"""Stage the 70 revised lines while preserving earlier accepted branches and labels."""

from inspect import getsource

from scripts import review_all_routes_final_flagged_wraps_20261118 as review
from scripts import stage_all_routes_next_phrase_wraps_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, paired = template.base, template.native, template.stage, template.paired
parent, ROOT = review.parent, review.ROOT / "research_v1"
ROM, PROOF = ROOT / "Lil_Maria_Flagged_Wraps_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
logical_end = template.logical_end

def selected_blocks():
    packet = base.load(review.SOURCE)
    return tuple(tuple(g["block"] for g in packet["groups"] if g["route"] == route) for route in range(4))


def verify_staged():
    proof = base.load(PROOF)
    expected = {f"/data/SC{i}.DK4": list(blocks) for i, blocks in enumerate(selected_blocks()) if blocks}
    assert proof["whole_parent_inverse"] and proof["candidate_sha256"] == base.digest(ROM)
    assert proof["changed_blocks"] == expected and sum(map(len, expected.values())) == 57
    assert proof["manuscript_sha256"] == base.digest(review.OUTPUT)


if __name__ == "__main__":
    review.BLOCKS = selected_blocks()
    src = checked_text(getsource(template.main), {
        'for i, blocks in enumerate(review.BLOCKS)}': 'for i, blocks in enumerate(review.BLOCKS) if blocks}',
    })
    scope = vars(template) | globals()
    exec(compile(src, __file__ + "::stage-lil-and-maria", "exec"), scope)
    scope["main"]()
    verify_staged()
