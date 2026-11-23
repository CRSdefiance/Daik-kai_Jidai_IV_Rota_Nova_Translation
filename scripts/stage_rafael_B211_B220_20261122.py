"""Stage the complete B211–220 editorial packet with source-bound carried decisions."""

from collections import Counter
from types import FunctionType, SimpleNamespace

from scripts import pair_rafael_B211_B220_20261122 as paired
from scripts import review_rafael_B211_B213_20261122 as early
from scripts import review_rafael_B215_20261122 as medicine
from scripts import review_rafael_B216_B220_20261122 as late
from scripts import stage_rafael_B181_B187_20261121 as modal_writer
from scripts import stage_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = paired.base, paired.native, paired.parent
INITIAL_STAGE = paired.ROOT / "staged_B211_B220"
ROOT = paired.ROOT / "staged_B211_B220_v2"
ROM, PROOF = ROOT / "Rafael_B211_B220_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = paired.ROOT / "contextual_manuscript_B211_B220_v2.json", paired.PAIRED
CARRY = paired.ROOT / "earlier_decisions_B214_B219.json"
DRAFTS = (early.OUTPUT, medicine.OUTPUT, late.OUTPUT)
BLOCKS = (tuple(range(211, 221)), (), (), ())
TOKEN = early.precedent.TOKEN
NOTICES = {"DK4_MES_B213_R0081", "DK4_MES_B213_R0107", "DK4_MES_B215_R0092"}


def combined_manuscript():
    packet, prior = map(base.load, (SOURCE, CARRY))
    predecessor = base.digest(parent.ROM)
    source_hash = base.digest(SOURCE)
    assert packet["candidate_sha256"] == prior["candidate_sha256"] == predecessor
    assert prior["source_packet_sha256"] == source_hash
    reused = {row["id"]: row for row in prior["reused_records"]}
    assert len(reused) == 32 and not prior["pending_records"]
    drafts = list(map(base.load, DRAFTS))
    assert all(draft["previous_sha256"] == predecessor and draft["source_packet_sha256"] == source_hash for draft in drafts)
    fresh = {row["id"]: row for draft in drafts for row in draft["records"]}
    assert len(fresh) == 192 and not set(fresh) & set(reused)
    names = {row["actor_ID"]: row["progressive_nameplate"] for row in
             base.load(early.precedent.prior.CATALOGUE)["source_and_current_default_name_fields"]}
    normalize = FunctionType(early.precedent.normalize.__code__, early.precedent.normalize.__globals__ | {"WRAPS": {}})
    records = []
    for group in packet["groups"]:
        for pair in group["records"]:
            ident = pair["id"]
            if ident in fresh:
                row = fresh.pop(ident)
                assert all(row[key] == value for key, value in pair.items())
                records.append(row)
                continue
            evidence = reused.pop(ident)
            assert all(evidence[ref] == pair[ref] for ref in ("source_reference", "current_reference"))
            assert pair["block"] in (214, 219) and all(evidence["prior_review_gates"].values())
            text = " ".join(pair["current_English"].split())
            row = pair | dict(previous_English=text, english=text, protected_phrases=[], localization_note=evidence["localization_note"],
                decision="retention", review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
            entry = normalize(row, names)
            entry["earlier_contextual_decision"] = evidence
            records.append(entry)
    assert not fresh and not reused and len(records) == 224
    counts = Counter(row["change_class"] for row in records)
    assert counts == {"retention": 173, "wording": 45, "glyph": 1, "wrap-only": 5}
    doc = drafts[0] | dict(records=records, findings=dict(counts), contextual_decisions_reused=32,
        contextual_records_revisited=192, component_drafts={str(path): base.digest(path) for path in DRAFTS},
        earlier_decisions=dict(path=str(CARRY), sha256=base.digest(CARRY)))
    if MANUSCRIPT.exists():
        assert base.load(MANUSCRIPT) == doc
    else:
        base.save(MANUSCRIPT, doc)
    return doc


def main():
    manuscript = combined_manuscript()
    protected = [row for row in manuscript["records"] if row["source_selector"] in (None, 254)]
    assert len(protected) == 25
    changed = [row for row in protected if row["decision"] == "revision"]
    assert {row["id"] for row in changed} == NOTICES
    fe = {}
    for row in changed:
        body = row["english"].encode("ascii")
        old = bytes.fromhex(row["current_hex"])[1:]
        assert TOKEN.findall(body.decode("ascii")) == TOKEN.findall(old.decode("ascii")) == ["FI"]
        encoded = b"\xfe" + body
        stored = encoded + b" " * ((len(body) ^ len(old)) & 1)
        fe[row["id"]] = dict(source_reference=row["source_reference"], current_reference=row["current_reference"],
            compiled_hex=encoded.hex(), expected_stored_hex=stored.hex(),
            rows=[(0, 0, row["english"].replace("FI", "Rafael"))])
    source = checked_text(previous.compiler.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
        "    rebuild = rebuild_function()": "    rebuild = reviewed_rebuild(fe)",
    })
    scope = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS), reviewed_rebuild=modal_writer.rebuild_function, fe=fe,
    )
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), scope)
    scope["main"]()
    assert base.digest(INITIAL_STAGE / ROM.name) == base.digest(ROM)
    old, new = [base.load(root / PROOF.name) for root in (INITIAL_STAGE, ROOT)]
    for a, b in zip(old["groups"], new["groups"], strict=True):
        assert a["block"] == b["block"]
        strip_plans = lambda group: [{k: v for k, v in command.items() if k != "plan"} for command in group["commands"]]
        assert strip_plans(a) == strip_plans(b)
    base.save(ROOT / "rebound_identical_stage.json", dict(candidate_sha256=new["candidate_sha256"],
        revised_proof_sha256=base.digest(PROOF), initial_proof_sha256=base.digest(INITIAL_STAGE / PROOF.name),
        full_ROM_identical=True, stored_commands_identical=True, retained_wrap="DK4_MES_B213_R0022"))


if __name__ == "__main__":
    main()
