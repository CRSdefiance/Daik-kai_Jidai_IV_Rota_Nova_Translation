"""Store the execution-scene prose correction and two protected phrase wraps."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import review_hodram_execution_20261121 as author
from scripts import stage_moonlit_violin_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = author.base, author.native, author.parent
ROOT = Path("out/hodram_execution_work_20261121/staged")
ROM, PROOF = ROOT / "Hodram_Execution_STAGED.nds", ROOT / "stored_proof.json"
logical_end = prior.logical_end


def main():
    ROOT.parent.mkdir(parents=True, exist_ok=True)
    review = SimpleNamespace(BLOCKS=author.BLOCKS, SOURCE=author.SOURCE, OUTPUT=author.PROGRESSIVE,
                             TOKEN=author.TOKEN, logical=author.logical)
    program = checked_text(getsource(prior.main), {
        "Staged the two violin exchanges": "Staged the execution scene",
        'assert proof["changed_blocks"] == {"/data/SC0.DK4": [51], "/data/SC1.DK4": [143]}':
            'assert proof["changed_blocks"] == {"/data/SC1.DK4": [40]}',
    })
    scope = vars(prior) | globals() | dict(review=review)
    exec(compile(program, __file__ + "::store", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
