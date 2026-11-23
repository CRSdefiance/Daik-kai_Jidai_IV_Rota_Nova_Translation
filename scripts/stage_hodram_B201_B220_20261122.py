"""Stage Hodram's encounters, item rumors, and letters on the registered base."""

from collections import Counter
from inspect import getsource
from types import SimpleNamespace

from scripts import pair_hodram_B201_B220_20261122 as paired
from scripts import stage_hodram_B181_B200_20261122 as previous


parent = paired.build
base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
engine, modal, ARCHIVE, logical_end = previous.engine, previous.modal, previous.ARCHIVE, previous.logical_end
DEFAULT_NAMES = previous.DEFAULT_NAMES
ROOT = paired.ROOT / "B201_B220_staged_v1"
SOURCE, OUTPUT = paired.PACKET, paired.ROOT / "B201_B220_scoped_manuscript_v1.json"
ROM, PROOF = ROOT / "Hodram_B201_B220_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), tuple(paired.BLOCKS), (), ())
DRAFTS = [paired.ROOT / f"{span}_contextual_v1.json" for span in (
    "B201_B203", "B204_B207", "B208_B210", "B211_B216", "B217_B220")]
REFINEMENTS = {
    "203_R0021": ("Indeed. He was a foreigner, but I respect him all the same.", ["was a foreigner,", "all the same."]),
    "204_R0040": ("It was no trouble. You still look pretty pale, though. You should rest for a while.",
                  ["no trouble.", "pretty pale, though.", "rest for a while."]),
    "205_R0098": ("No, really, I'm sorry. I hope you'll forgive us.", ["I'm sorry.", "forgive us."]),
    "208_R0068": ("Oh, no need to thank me. I'll take a spare instead. One figurehead per ship. Remember that.",
                  ["no need to thank me.", "I'll take a spare instead.", "One figurehead per ship.", "Remember that."]),
    "212_R0059": (None, ["sea battle there.", "lost it in the fighting."]),
    "213_R0027": ("Word has reached me of the Muramasa, the legendary cursed blade. This masterwork is said to bring ill fortune to Tokugawa, ruler of Japan. Efforts are under way to destroy such blades.",
                  ["the legendary cursed blade.", "bring ill fortune", "ruler of Japan.", "destroy such blades."]),
    "213_R0030": ("It appears that a clan with a grievance against Tokugawa has hidden one such blade somewhere in East Asia. For now, I send you these tidings.",
                  ["against Tokugawa", "one such blade", "somewhere in East Asia.", "I send you these tidings."]),
    "216_R0078": ("Ah, Zhuge Liang. Brilliant strategist. That memorial he wrote before the campaign always brings tears to my eyes. He's my second favorite, I'd say.",
                  ["Brilliant strategist.", "before the campaign", "brings tears to my eyes.", "I'd say."]),
    "217_R0042": (None, ["command many foreigners", "a gold seal", "that hero."]),
    "218_R0038": (None, ["endured persecution", "spreading their faith."]),
    "218_R0087": (None, ["rule it out entirely.", "repent in the end,", "to you, Admiral."]),
    "219_R0029": (None, ["the sacred sword Excalibur,", "calling to you", "where the king sleeps!"]),
}
TWO_ROW_PANELS = {
    "202_R0010": (("Any bad children here?", "Any bad children here?"),
                  "Give each repeated challenge its own row so the call reads as two complete beats."),
    "202_R0014": (("Any bad children here?", "Any bad children here?"),
                  "Repeat the exact two-beat call from the first panel."),
    "208_R0071": (("Take care.", "Jam Jack Ludwyan"),
                  "Set the signoff and name on separate rows as in the Japanese letter. Preserve Jam's approved full name."),
}
FE_MACROS = {
    "DK4_MES_B205_R0078": "Charm",
    "DK4_MES_B205_R0101": "Spirit",
    "DK4_MES_B207_R0081": "Charm",
}


def plan_two_rows(row, raw, painter, lines):
    assert row["english"] == " ".join(lines) and not TOKEN.findall(row["english"])
    expected = [(12 * i, 0, line) for i, line in enumerate(lines)]
    for body in modal.layout.candidates(row, -1, [(0, line) for line in lines]):
        stored = body + b" " * ((len(body) ^ len(raw)) & 1)
        try:
            actual, raster = modal.paint(painter, stored)
        except (AssertionError, ValueError):
            continue
        if actual == expected:
            return body, stored, actual, raster
    raise AssertionError((row["id"], expected))


def collect():
    packet, carry, release = map(base.load, (SOURCE, paired.CARRY, parent.RELEASE))
    assert base.digest(parent.ROM) == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert not carry["reused_records"] and carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(SOURCE) for doc in drafts)
    by_id = {row["id"]: row for doc in drafts for row in doc["records"]}
    assert len(by_id) == sum(len(doc["records"]) for doc in drafts) == 350
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
                           layout_refinement="Adjusted the paragraph and phrase protection after checking native line widths.")
            if short in TWO_ROW_PANELS:
                assert row["decision"] == "retention" and row["source_selector"] == 254
                lines, note = TWO_ROW_PANELS[short]
                row.update(decision="revision", change_class="wrap-only", protected_phrases=list(dict.fromkeys(lines)),
                           prior_retention_note=row["localization_note"], localization_note=note)
            if row["source_selector"] == 254 and row["decision"] == "revision":
                raw = bytes.fromhex(row["current_hex"])[1:]
                if short in TWO_ROW_PANELS:
                    old_rows, _ = modal.paint(painter, raw)
                    body, encoded, cells, raster = plan_two_rows(row, raw, painter, TWO_ROW_PANELS[short][0])
                    assert cells != old_rows
                else:
                    body, encoded, cells, raster = modal.plan(row | {"source_record_index": -1}, raw, painter)
                fe[ident] = dict(compiled_hex=body.hex(), expected_hex=(b"\xfe" + encoded).hex(),
                                 rows=cells, plane_sha256=native.digest(raster))
            ordered.append(row | {"route": 1})
    assert not by_id and len(fe) == 10
    findings = dict(Counter(row["change_class"] for row in ordered))
    assert findings == {"wording": 155, "wrap-only": 3, "retention": 192}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=release["candidate_sha256"],
                previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE=fe,
                source_and_draft_evidence={str(path): base.digest(path) for path in [*DRAFTS, paired.CARRY]},
                contextual_records_revisited=350, contextual_decisions_reused=0, new_editorial_credit=0,
                status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


if __name__ == "__main__":
    exec(compile(getsource(previous.main), __file__ + "::stored-rom", "exec"), globals())
    main()
