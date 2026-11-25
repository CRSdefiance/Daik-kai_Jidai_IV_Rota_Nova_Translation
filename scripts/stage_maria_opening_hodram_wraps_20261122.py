"""Compile the reviewed Maria opening and Hodram wrap repairs together."""

from collections import Counter
import json
from types import SimpleNamespace

from scripts import review_maria_opening_hodram_wraps_20261122 as review
from scripts.source_locked_derivation_v5118 import checked_text


parent, native, base, engine = review.parent, review.native, review.base, review.engine
compiler = parent.writer.compiler
ROOT = review.ROOT/"staged"
ROM, PROOF = ROOT/"Maria_Opening_Hodram_Wraps_STAGED.nds", ROOT/"stored_proof.json"
MANUSCRIPT = review.ROOT/"scoped_manuscript_v1.json"
BLOCKS = ((),review.HODRAM_BLOCKS,(),tuple(review.DECISIONS))
POLISH = {
    "DK4_MES_B3_R0005": (None, "Kurushima's existing direct challenge already preserves the name substitution and his resolve to settle it today."),
    "DK4_MES_B4_R0041": ("You thought I'd go along with that nonsense? You really underestimated me.",
        "Maria is offended that he thought she would go along with his plan. Her second sentence makes the source's accusation of underestimating her explicit."),
    "DK4_MES_B14_R0005": ("That's Admiral FA for you! I guess you didn't need me to back you up, huh?",
        "Lil praise and her joking suggestion that the admiral did not need help stay distinct. The source gives the surname substitution and no shared affiliation."),
    "DK4_MES_B14_R0009": ("You were a big help. Thank you, really.",
        "Maria assures Lil that her help mattered and thanks her sincerely, setting up Lil's claim that they are even."),
}


def reconcile_plans(actual,draft,plans):
    staged = {ident:plan for group in actual["groups"] for ident,plan in group["plans"].items()}
    styles = {r["id"] for r in draft["records"] if r["kind"]=="actor-style"}
    assert staged.keys()==plans.keys()|styles and not plans.keys()&styles
    assert {ident:staged[ident] for ident in plans}==json.loads(json.dumps(plans))


def main():
    assert not ROOT.exists()
    draft, layout, release = map(base.load,(review.DRAFT,review.LAYOUT,parent.RELEASE))
    assert base.digest(review.DRAFT)==layout["draft_sha256"]
    assert layout["candidate_sha256"]==release["candidate_sha256"]==base.digest(parent.ROM)
    lookup = {(row["route"], row["id"]):row for row in draft["records"]}
    assert len(lookup)==171 and len(layout["plans"])==47
    plans = layout["plans"].copy()
    for ident, (wording,note) in POLISH.items():
        row = lookup[3,ident]
        assert row["decision"]=="revision" and ident in plans
        row.update(english=wording or row["previous_English"],localization_note=note,
                   change_class="wording" if wording else "retention",decision="revision" if wording else "retention")
        plans.pop(ident)
        plans.update(review.maria.preflight([row]))
    draft.update(encoder="dialogue-relocatable-v1",previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"],planned_FE={},
        findings=dict(Counter(row["change_class"] for row in draft["records"])),
        previous_contextual_draft_sha256=base.digest(review.DRAFT),preliminary_layout_sha256=base.digest(review.LAYOUT))
    if MANUSCRIPT.exists():
        assert base.load(MANUSCRIPT)==draft
    else:
        base.save(MANUSCRIPT,draft)
    scope = compiler.env | globals() | dict(review=SimpleNamespace(OUTPUT=MANUSCRIPT,SOURCE=review.PACKET),
        paired=SimpleNamespace(BLOCKS=BLOCKS),draft=draft,assemble=engine.assemble)
    program = checked_text(engine.program, {"if g[\"block\"] in paired.BLOCKS[1]":
                                            "if g[\"block\"] in paired.BLOCKS[g[\"route\"]]"})
    exec(compile(program,__file__+"::registered-mixed-story-scopes","exec"),scope)
    scope["main"]()
    actual = base.load(PROOF)
    assert actual["whole_parent_inverse"] and set(actual["changed_blocks"])=={"/data/SC1.DK4","/data/SC3.DK4"}
    reconcile_plans(actual,draft,plans)
    print(draft["findings"],flush=True)


if __name__=="__main__":
    main()

