"""Stage the treasure rumors and letters with the verified Janus signature repair."""

from collections import Counter
from inspect import getsource
from types import SimpleNamespace

from scripts import pair_hodram_B221_B240_20261122 as paired
from scripts import stage_hodram_B181_B200_20261122 as previous


parent = paired.build
base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
engine, ARCHIVE, logical_end = previous.engine, previous.ARCHIVE, previous.logical_end
DEFAULT_NAMES = previous.DEFAULT_NAMES
ROOT = paired.ROOT / "B221_B240_staged_v1"
SOURCE, OUTPUT = paired.ROOT / "paired_with_B218_signature_v1.json", paired.ROOT / "B221_B240_scoped_manuscript_v1.json"
ROM, PROOF = ROOT / "Hodram_B221_B240_STAGED.nds", ROOT / "stored_proof.json"
NO_TEXT = {222, 235}
BLOCKS = ((), (218, *(block for block in paired.BLOCKS if block not in NO_TEXT)), (), ())
DRAFTS = [paired.ROOT / f"{span}_contextual_v1.json" for span in ("B221_B223", "B224_B229", "B230_B234", "B236_B240")]
OPENING_PREFLIGHT = paired.ROOT / "B221_B223_wrap_preflight_v1.json"
SIGNATURE = paired.ROOT / "B218_R0068_janus_signature_followup_v1.json"
SIGNATURE_ID = "DK4_MES_B218_R0068"
REFINEMENTS = {
    "224_R0047": ("I've heard the same. They came for the wealth of this region, didn't they? They looted and slaughtered as they went. Nothing was off limits.", []),
    "224_R0061": ("He fought humanely, treated prisoners and civilians with decency, and offered fair terms for peace. He was a fine man who never stooped to dirty tricks.",
                  ["with decency,", "terms for peace.", "dirty tricks."]),
    "225_R0027": ("He belonged to a once-mighty clan. But a rival defeated them again and again, driving them to ruin.",
                  ["a once-mighty clan.", "again and again,", "driving them to ruin."]),
    "225_R0040": ("To think a man so brave came from this small country in the East... I feel I've glimpsed the true spirit of the East.",
                  ["country in the East...", "the true spirit of the East."]),
    "226_R0031": ("It was about Timur, who carried on the line of the declining Mongol Empire roughly two hundred years ago and built a vast empire from Central to Western Asia.",
                  ["the declining Mongol Empire", "roughly two hundred years ago", "Central to Western Asia."]),
    "226_R0034": ("The book says he wore mail so sturdy that arrows bounced off it and swords and spears chipped their blades on it.",
                  ["arrows bounced off it", "their blades on it."]),
    "237_R0064": ("Admiral, there may be something to this. If we found an item a pope once treasured, it would be quite a discovery.",
                  ["something to this.", "a pope once treasured,", "quite a discovery."]),
    "238_R0035": ("Badly outmatched, the merchant ships tried to flee, but the pirates were faster. It seemed only a matter of time before they were all lost.",
                  ["Badly outmatched,", "tried to flee,", "the pirates were faster."]),
    "240_R0028": ("They say it makes you a master with a bow. The men ask if it'll work on cannons. And who's tending the ship? Nobody!",
                  ["with a bow.", "on cannons.", "tending the ship?"]),
}


def bind_prior_letter(group, followup):
    previous_rows = {r["id"]: r for r in base.load(parent.REVIEW)["records"] if r["block"] == 218}
    assert len(previous_rows) == len(group["records"]) == 17
    for original in group["records"]:
        ident = original["id"]
        prior = previous_rows.pop(ident)
        assert all(prior["review"].values()) and prior["source_reference"] == original["source_reference"]
        raw = prior["registered_reference"]
        prefix = f"{original['selector']:02x}" if original["native_command_word"] == 0x4000 else ""
        before = prefix + original["current_reference"]["exact_body_hex"]
        assert before == raw["exact_stored_hex"]
        assert all(raw[k] == original["current_reference"][k]
                   for k in ("archive_sha256", "block_sha256", "command_offset", "offset"))
        assert " ".join(original["current_English"].split()) == prior["english"]
        row = original | dict(kind=prior["kind"], route=1, speaker=prior["speaker"],
            source_selector=original["selector"], native_slots=original["slots"],
            source_hex=prior["source_hex"], current_hex=before, previous_English=prior["english"],
            english=prior["english"], protected_phrases=[], context=prior["context"],
            source_meaning=prior["source_meaning"], localization_note=prior["localization_note"],
            decision="retention", change_class="retention", decision_carried=True,
            previous_registered_reference=raw, review=prior["review"].copy())
        if ident == SIGNATURE_ID:
            ask = followup["decision"]
            assert ask["registered_reference"] == raw and ask["english"] == row["english"]
            row.update(decision="revision", change_class="wrap-only", decision_carried=False,
                protected_phrases=ask["protected_phrases"], localization_note=ask["localization_note"],
                review=ask["review"], prior_retention_note=prior["localization_note"],
                deliberate_break_reason="The native letter gives the signoff and signature distinct rows.")
        yield row
    assert not previous_rows


def collect():
    packet, carry, release, signature, opening = map(base.load,
        (paired.PACKET, paired.CARRY, parent.RELEASE, SIGNATURE, OPENING_PREFLIGHT))
    assert {group["block"] for group in packet["groups"] if not group["records"]} == NO_TEXT
    candidate = base.digest(parent.ROM)
    assert candidate == packet["candidate_sha256"] == release["candidate_sha256"] == signature["candidate_sha256"]
    assert carry["source_packet_sha256"] == base.digest(paired.PACKET) and not carry["reused_records"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert signature["registered_review_sha256"] == base.digest(parent.REVIEW)
    assert base.digest(signature["gameplay"]["path"]) == signature["gameplay"]["PNG_sha256"]
    assert opening["review_sha256"] == base.digest(DRAFTS[0])
    preceding, = paired.pairing.source_and_current(parent, (218,))["groups"]
    combined = packet | dict(groups=[preceding, *packet["groups"]], original_packet=str(paired.PACKET),
                             original_packet_sha256=base.digest(paired.PACKET))
    if SOURCE.exists():
        assert base.load(SOURCE) == combined
    else:
        base.save(SOURCE, combined)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(paired.PACKET) for doc in drafts)
    by_id = {r["id"]: r for doc in drafts for r in doc["records"]}
    assert len(by_id) == sum(len(doc["records"]) for doc in drafts) == 274
    refinements = REFINEMENTS | {r["id"].partition("_B")[2]: (r["refined_english"], r["protected_phrases"])
                                for r in opening["records"] if "refined_english" in r}
    ordered = list(bind_prior_letter(preceding, signature))
    planner = engine.assemble({}).__globals__["plan_progressive"]
    for group in packet["groups"]:
        for original in group["records"]:
            row = by_id.pop(original["id"])
            assert all(row[k] == v for k, v in original.items())
            short = row["id"].partition("_B")[2]
            if short in refinements:
                assert row["decision"] == "revision"
                english, phrases = refinements[short]
                row.update(english=english, protected_phrases=phrases,
                           layout_refinement="Reviewed the phrase following preliminary native wrapping.")
            ordered.append(row | {"route": 1})
    assert not by_id
    for row in ordered:
        if row["decision"]!="revision":
            continue
        prefix = int(row["kind"]=="progressive")
        old, clean = [bytes.fromhex(row[k])[prefix:] for k in ("current_hex", "source_hex")]
        try:
            _, planned = planner(row, row["source_selector"], old, clean)
        except (AssertionError, ValueError) as err:
            raise ValueError(f"Unable to plan {row['id']}") from err
        if row["id"] == SIGNATURE_ID:
            assert planned["encoded_hex"] == signature["native_layout_preflight"]["encoded_hex"]
        if row["id"] == "DK4_MES_B226_R0048":
            assert planned["lines"][-1] == "Ian Dukov"
    findings = dict(Counter(r["change_class"] for r in ordered))
    assert findings == {"wording": 122, "wrap-only": 1, "glyph": 3, "retention": 165}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=candidate,
                previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE={},
                source_and_draft_evidence={str(path):base.digest(path) for path in [*DRAFTS, paired.CARRY, SIGNATURE, OPENING_PREFLIGHT]},
                contextual_records_revisited=275, contextual_decisions_reused=16, new_editorial_credit=0,
                status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


if __name__ == "__main__":
    exec(compile(getsource(previous.main), __file__ + "::stored-rom", "exec"), globals())
    main()
