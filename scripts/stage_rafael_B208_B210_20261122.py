"""Stage the reviewed Rafael bargaining, book seller, and Namahage encounters."""

from types import SimpleNamespace

from scripts import review_rafael_B208_B210_20261122 as review
from scripts import stage_rafael_B181_B187_20261121 as modal_writer
from scripts import stage_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.paired.native, review.paired.parent
ROOT = review.paired.ROOT / "staged_B208_B210_v2"
ROM, PROOF = ROOT / "Rafael_B208_B210_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = review.OUTPUT, review.paired.PAIRED
BLOCKS = (tuple(review.DECISIONS), (), (), ())
TOKEN = review.precedent.TOKEN
CHARM = "DK4_MES_B208_R0046"


def main():
    manuscript = base.load(MANUSCRIPT)
    protected = [row for row in manuscript["records"] if row["source_selector"] in (None, 254)]
    assert len(protected) == 23
    changed, = [row for row in protected if row["decision"] == "revision"]
    assert changed["id"] == CHARM
    body = changed["english"].encode("ascii")
    old = bytes.fromhex(changed["current_hex"])[1:]
    assert TOKEN.findall(body.decode("ascii")) == TOKEN.findall(old.decode("ascii")) == ["FI"]
    encoded = b"\xfe" + body
    stored = encoded + b" " * ((len(body) ^ len(old)) & 1)
    fe = {CHARM: dict(source_reference=changed["source_reference"], current_reference=changed["current_reference"],
                     compiled_hex=encoded.hex(), expected_stored_hex=stored.hex(),
                     rows=[(0, 0, changed["english"].replace("FI", "Rafael"))])}
    source = checked_text(previous.compiler.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
        "    rebuild = rebuild_function()": "    rebuild = reviewed_rebuild(fe)",
        'g for g in packet["groups"]}': 'g for g in packet["groups"] if g["block"] in BLOCKS[0]}',
    })
    scope = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS), reviewed_rebuild=modal_writer.rebuild_function, fe=fe,
    )
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
