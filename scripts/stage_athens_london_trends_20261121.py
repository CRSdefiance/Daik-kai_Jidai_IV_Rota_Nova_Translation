"""Stage the reviewed Athens and London exchanges in both affected routes."""
from inspect import getsource
from pathlib import Path

from scripts import review_athens_london_trends_20261121 as review
from scripts import stage_moonlit_violin_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = Path("out/athens_london_trend_repairs_20261121/staged")
ROM, PROOF = ROOT / "Athens_London_Trend_Repairs_STAGED.nds", ROOT / "stored_proof.json"
logical_end = prior.logical_end


def main():
    ROOT.parent.mkdir(parents=True, exist_ok=True)
    program = checked_text(getsource(prior.main), {
        "Staged the two violin exchanges": "Staged the Athens and London exchanges",
        'assert proof["changed_blocks"] == {"/data/SC0.DK4": [51], "/data/SC1.DK4": [143]}':
            'assert proof["changed_blocks"] == {"/data/SC1.DK4": [185, 186], "/data/SC3.DK4": [154, 155]}',
    })
    scope = vars(prior) | globals()
    exec(compile(program, __file__ + "::store", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
