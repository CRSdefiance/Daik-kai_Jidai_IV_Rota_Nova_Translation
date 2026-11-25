"""Stage the two Lisbon repairs with the registered sparse scene workflow."""
from inspect import getsource
from pathlib import Path

from scripts import review_lisbon_fragrance_wraps_20261121 as author
from scripts import stage_moonlit_violin_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = author.base, author.native, author.parent
ROOT = Path("out/lisbon_fragrance_wraps_20261121/staged")
ROM, PROOF = ROOT / "Lisbon_Fragrance_Wraps_STAGED.nds", ROOT / "stored_proof.json"
logical_end = prior.logical_end


def main():
    ROOT.parent.mkdir(parents=True, exist_ok=True)
    program = checked_text(getsource(prior.main), {
        "Staged the two violin exchanges": "Staged the complete Lisbon fragrance exchange",
        'assert proof["changed_blocks"] == {"/data/SC0.DK4": [51], "/data/SC1.DK4": [143]}':
            'assert proof["changed_blocks"] == {"/data/SC1.DK4": [184]}',
    })
    scope = vars(prior) | globals() | {"review": author}
    exec(compile(program, __file__ + "::store", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()

