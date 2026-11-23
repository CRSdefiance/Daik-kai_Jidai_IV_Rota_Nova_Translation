"""Compile Hodram's town conversations, market notices, and bargaining scene."""

from collections import Counter
from types import SimpleNamespace

from scripts import register_hodram_B171_B180_20261122 as parent
from scripts import review_hodram_B181_B182_B188_20261122 as first
from scripts import review_hodram_B183_B190_20261122 as second
from scripts import review_hodram_B191_B199_20261122 as third
from scripts import review_hodram_B200_20261122 as fourth
from scripts import stage_hodram_B131_B150_20261122 as engine
from scripts import stage_hodram_B161_B170_20261122 as previous


base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
modal, ARCHIVE, logical_end = previous.modal, previous.ARCHIVE, previous.logical_end
paired = fourth.paired
ROOT = paired.ROOT / "B181_B200_staged_v1"
SOURCE, OUTPUT = paired.PACKET, paired.ROOT / "B181_B200_scoped_manuscript_v1.json"
ROM, PROOF = ROOT / "Hodram_B181_B200_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), tuple(paired.BLOCKS), (), ())
DEFAULT_NAMES = previous.DEFAULT_NAMES
DRAFTS = [review.OUTPUT for review in (first, second, third, fourth)]
CHARM_PANEL = "DK4_MES_B200_R0045"
FORECASTS = {
    "181_R0037": "Tomatoes may catch on in Genoa.",
    "182_R0051": "Wheat may catch on in Amsterdam.",
    "184_R0073": "Fragrances may catch on in Lisbon.",
    "185_R0039": "Rubies may catch on in Athens.",
    "186_R0062": "Gemstones may catch on in London.",
    "197_R0059": "Chili peppers may catch on in Seoul.",
}
REFINEMENTS = {
    "182_R0013": (None, ["that much better", "bake it yourself?"]),
    "183_R0013": ("It's fine. But wine's what everybody drinks now. Wine!", ["wine's what", "everybody drinks now."]),
    "189_R0026": (None, ["it's this cold,", "want a fur coat."]),
    "193_R0049": (None, ["worth keeping!", "short on cash.", "talk to them?"]),
    "199_R0024": (None, ["have to ask?"]),
    "200_R0074": (None, ["cut the price in half", "marked it way up.", "at least twice more.)"]),
    "200_R0306": (None, ["somebody else!"]),
}
WRAPS = {
    "186_R0005": (["getting engaged!"], "Let the exclamation run into the news while keeping the engagement phrase whole."),
    "189_R0006": (["goes right through you."], "Keep the description of the cold whole and use the first row for the start of the next clause."),
    "195_R0064": (["it's sold out,", "it's too late."], "Use the first row for the warning's condition and keep the consequence intact."),
    "197_R0037": (["for dinner tonight."], "Keep the dinner phrase together and use the open room after her quick reaction."),
}


def collect():
    packet, carry, release = map(base.load, (SOURCE, paired.CARRY, parent.RELEASE))
    assert base.digest(parent.ROM) == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert not carry["reused_records"] and carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(SOURCE) for doc in drafts)
    by_id = {row["id"]: row for doc in drafts for row in doc["records"]}
    assert len(by_id) == sum(len(doc["records"]) for doc in drafts) == 284
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image, arm=image.read_file(native.ARM)))
    ordered, fe = [], {}
    for group in packet["groups"]:
        for original in group["records"]:
            ident = original["id"]
            row = by_id.pop(ident)
            assert all(row[key] == value for key, value in original.items())
            short = ident.partition("_B")[2]
            if short in REFINEMENTS:
                assert row["decision"] == "revision"
                wording, phrases = REFINEMENTS[short]
                row.update(english=wording or row["english"], protected_phrases=phrases,
                           layout_refinement="Adjusted phrase protection after checking the native line widths.")
            if short in WRAPS:
                assert row["decision"] == "retention" and "\n" in row["current_English"]
                phrases, note = WRAPS[short]
                row.update(decision="revision", change_class="wrap-only", protected_phrases=phrases,
                           prior_retention_note=row["localization_note"], localization_note=note)
            if short == "190_R0040":
                row["formatting_retention_reason"] = "The repeated instruction gets its own beat before the owner's send-off and laugh."
            if short in FORECASTS:
                assert row["kind"] == "system-FE" and row["decision"] == "retention"
                forecast = FORECASTS[short]
                row.update(english=forecast, protected_phrases=[forecast],
                           decision="revision", change_class="wording", prior_retention_note=row["localization_note"],
                           localization_note="Use the shared forecast wording for the likelihood stated in Japanese and keep the product and destination on one row.")
                raw = bytes.fromhex(row["current_hex"])[1:]
                body, expected, cells, raster = modal.plan(row | {"source_record_index": -1}, raw, painter)
                assert cells == [(0, 0, forecast)], (ident, cells)
                fe[ident] = dict(compiled_hex=body.hex(), expected_hex=(b"\xfe" + expected).hex(),
                                 rows=cells, plane_sha256=native.digest(raster))
            ordered.append(row | {"route": 1})
    assert not by_id and len(fe) == len(FORECASTS)
    findings = dict(Counter(r["change_class"] for r in ordered))
    assert findings == {"wording": 68, "wrap-only": 4, "retention": 212}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=release["candidate_sha256"],
                previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE=fe,
                source_and_draft_evidence={str(path): base.digest(path) for path in [*DRAFTS, paired.CARRY]},
                contextual_records_revisited=284, contextual_decisions_reused=0, new_editorial_credit=0,
                status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


def main():
    assert not PROOF.exists()
    draft = collect()
    if OUTPUT.exists():
        assert base.load(OUTPUT) == draft
    else:
        base.save(OUTPUT, draft)
    print(draft["findings"], flush=True)
    scope = compiler.env | globals() | dict(review=SimpleNamespace(OUTPUT=OUTPUT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS), draft=draft, assemble=engine.assemble)
    exec(compile(engine.program, __file__ + "::stored-script-and-inverse", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == len(BLOCKS[1])
    assert stored["changed_blocks"] == {ARCHIVE: sorted({r["block"] for r in draft["records"] if r["decision"] == "revision"})}


if __name__ == "__main__":
    main()
