"""Stage the Hodram recruitment scenes and their unchanged tutorial menus."""

from collections import Counter
from types import SimpleNamespace

from scripts import register_hodram_B151_B160_20261122 as parent
from scripts import review_hodram_B161_B163_20261122 as first
from scripts import review_hodram_B164_B166_20261122 as second
from scripts import review_hodram_B167_B168_20261122 as third
from scripts import review_hodram_B169_B170_20261122 as fourth
from scripts import stage_hodram_B151_B160_20261122 as staging


base, native, compiler, TOKEN = staging.base, staging.native, staging.compiler, staging.TOKEN
modal, ARCHIVE, logical_end = staging.modal, staging.ARCHIVE, staging.logical_end
paired = fourth.paired
ROOT = paired.ROOT / "B161_B170_staged_v1"
SOURCE, OUTPUT = paired.PACKET, paired.ROOT / "B161_B170_scoped_manuscript_v1.json"
ROM, PROOF = ROOT / "Hodram_B161_B170_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), tuple(paired.BLOCKS), (), ())
DEFAULT_NAMES = staging.DEFAULT_NAMES
DRAFTS = [review.OUTPUT for review in (first, second, third, fourth)]
OPAQUE = "DK4_MES_B168_R0096"
REFINEMENTS = {
    "161_R0056": ("A little. You danced beautifully. No wonder Mivor's taken with you.", ["taken with you."]),
    "168_R0195": ("She washed up on the beach. She'd been abandoned, remember?", ["washed up on the beach.", "abandoned, remember?"]),
    "168_R0202": ("Proof... Any ideas, Cesare?", ["Any ideas, Cesare?"]),
    "168_R0317": (None, ["for your own good."]),
    "169_R0092": ("I'd say he's courting her.", ["courting her."]),
    "170_R0184": ("Well... We were going to look for some while we're out sailing.", ["look for some", "out sailing."]),
}


def carried_row(row, prior):
    assert all(prior[key] == value for key, value in row.items())
    assert prior["block"] == 167 and row["native_command_word"] == 0x4000
    assert all(prior["prior_review_gates"].values())
    assert row["current_reference"]["block_sha256"] == prior["previous_registered_reference"]["block_sha256"]
    prefix = f"{row['selector']:02x}"
    english = " ".join(row["current_English"].split())
    return prior | dict(kind="progressive", source_selector=row["selector"], native_slots=row["slots"],
        source_hex=prefix + row["source_reference"]["exact_body_hex"],
        current_hex=prefix + row["current_reference"]["exact_body_hex"],
        previous_English=english, english=english, protected_phrases=[],
        context=third.CONTEXTS[167], decision="retention", change_class="retention",
        review=prior["prior_review_gates"].copy(), decision_carried=True)


def collect():
    packet, carry, release = map(base.load, (SOURCE, paired.CARRY, parent.RELEASE))
    assert base.digest(parent.ROM) == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(SOURCE) for doc in drafts)
    rows = {row["id"]: row for doc in drafts for row in doc["records"]}
    earlier = {row["id"]: row for row in carry["reused_records"]}
    assert len(rows) == sum(len(doc["records"]) for doc in drafts) == 270
    assert len(earlier) == 41 and not rows.keys() & earlier.keys()
    ordered = []
    for group in packet["groups"]:
        for original in group["records"]:
            ident = original["id"]
            if ident in earlier:
                row = carried_row(original, earlier.pop(ident))
            else:
                row = rows.pop(ident)
                assert all(row[key] == value for key, value in original.items())
            short = ident.partition("_B")[2]
            if short in REFINEMENTS:
                wording, phrases = REFINEMENTS[short]
                assert row["decision"] == "revision"
                row.update(english=wording or row["english"], protected_phrases=phrases,
                           layout_refinement="Adjusted phrase protection after the width check.")
            if short == "163_R0030":
                row["formatting_retention_reason"] = "The alarmed answer is a single beat before the urgent instruction, which fits whole on the second line."
            if short == "169_R0143":
                row.update(decision="revision", change_class="wrap-only",
                    protected_phrases=["Pick up on things like that", "your opponent's moves."],
                    prior_retention_note=row["localization_note"],
                    localization_note="Use the width of the first row to keep the observation together before its application to the opponent.")
            ordered.append(row | {"route":1})
    assert not rows and not earlier
    assert all(r["decision"] == "retention" for r in ordered if r["kind"] in {"system-FE","typed-choice-label"})
    findings = dict(Counter(r["change_class"] for r in ordered))
    assert findings == {"wording": 103, "wrap-only": 1, "retention": 207}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
        source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE={},
        source_and_draft_evidence={str(path): base.digest(path) for path in [*DRAFTS, paired.CARRY]},
        contextual_records_revisited=270, contextual_decisions_reused=41, new_editorial_credit=0,
        status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


def main():
    assert not PROOF.exists()
    draft = collect()
    if OUTPUT.exists():
        assert base.load(OUTPUT) == draft
    else:
        base.save(OUTPUT, draft)
    print(draft["findings"], flush=True)
    scope = compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=OUTPUT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS), draft=draft, assemble=staging.staging.assemble,
    )
    exec(compile(staging.staging.program, __file__ + "::stored-script-and-inverse", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == len(BLOCKS[1])
    assert stored["changed_blocks"] == {ARCHIVE: sorted({r["block"] for r in draft["records"] if r["decision"]=="revision"})}


if __name__ == "__main__":
    main()

