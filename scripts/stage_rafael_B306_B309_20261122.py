"""Stage the reviewed Istanbul remedy exchanges against the registered Rafael ROM."""

from inspect import getsource
from types import SimpleNamespace

from scripts import review_rafael_B306_B309_20261122 as review
from scripts import stage_rafael_B221_B240_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, TOKEN = review.base, review.paired.parent.native, review.paired.parent, prior.TOKEN
first, previous = prior.first, prior.previous
ROOT = review.ROOT / "staged_B306_B309"
ROM, PROOF = ROOT / "Rafael_B306_B309_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = review.ROOT / "contextual_manuscript_B306_B309.json", review.PAIRED
DRAFTS, CARRIES = (review.OUTPUT,), (review.CARRY,)
BLOCKS = (tuple(review.DECISIONS), (), (), ())
PREFLIGHT = review.ROOT / "format_preflight_B306_B309_v2.json"
rebuild_function = prior.rebuild_function

compose = checked_text(getsource(prior.combined_manuscript), {
    'and not d["pending_records"]': '',
    'for row in proof["reused_records"]}': 'for row in proof["reused_records"] if row["block"] in BLOCKS[0]}',
    'len(reused) == 48': 'len(reused) == 8',
    'len(fresh) == 222': 'len(fresh) == 53',
    '    for group in packet["groups"]:': '    for group in packet["groups"]:\n        if group["block"] not in BLOCKS[0]:\n            continue',
    ' and pair["block"] in (225, 226, 240)': '',
    'len(records) == 270': 'len(records) == 61',
    '{"retention": 208, "wording": 60, "glyph": 2}': '{"retention": 44, "wording": 17}',
    'contextual_records_revisited=222': 'contextual_records_revisited=53',
    'contextual_decisions_reused=48': 'contextual_decisions_reused=8',
})
scope = vars(prior) | globals()
exec(compile(compose, __file__ + "::source-bound-manuscript", "exec"), scope)


def main():
    manuscript = scope["combined_manuscript"]()
    assert all(row["kind"] == "progressive" for row in manuscript["records"])
    source = checked_text(previous.compiler.source, {
        '    painter = stage.system.native_painter(ctx)': '    painter = None',
        'for g in packet["groups"]}': 'for g in packet["groups"] if g["block"] in paired.BLOCKS[0]}',
    })
    compiler = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE), paired=SimpleNamespace(BLOCKS=BLOCKS))
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), compiler)
    compiler["main"]()
    preflight = base.load(PREFLIGHT)
    assert preflight["draft_sha256"] == base.digest(review.OUTPUT)
    assert preflight["candidate_sha256"] == manuscript["previous_sha256"]
    stored = base.load(PROOF)
    revised = {row["id"] for row in manuscript["records"] if row["decision"] == "revision"}
    assert set(preflight["progressive"]) == revised
    assert stored["changed_blocks"] == {"/data/SC0.DK4": [306, 307, 308, 309]}
    for group in stored["groups"]:
        for ident, plan in group["plans"].items():
            expected = preflight["progressive"][ident]
            assert plan["lines"] == expected["lines"]
            assert plan["encoded_hex"][2:] == expected["planned_body_hex"]


if __name__ == "__main__":
    main()
