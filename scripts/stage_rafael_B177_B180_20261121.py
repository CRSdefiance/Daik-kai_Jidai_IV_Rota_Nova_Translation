"""Stage Rafael's recruitment and tutorial dialogue with the original native choices."""

from types import SimpleNamespace

from scripts import review_rafael_B177_B180_20261121 as review
from scripts import stage_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.paired.native, review.paired.parent
ROOT = review.paired.ROOT / "staged_B177_B180"
ROM, PROOF = ROOT / "Rafael_B177_B180_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = review.OUTPUT, review.paired.PAIRED
BLOCKS = (tuple(range(177, 181)), (), (), ())
TOKEN = review.TOKEN


def main():
    manuscript = base.load(MANUSCRIPT)
    protected = [r for r in manuscript["records"] if r["source_selector"] in (None, 254)]
    assert len(protected) == 9 and all(r["decision"] == "retention" for r in protected)
    source = checked_text(previous.compiler.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
        "    rebuild = rebuild_function()": "    rebuild = reviewed_rebuild({})",
    })
    scope = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS), reviewed_rebuild=previous.rebuild_function,
    )
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
