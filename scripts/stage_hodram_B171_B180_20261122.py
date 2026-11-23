"""Stage the Proofs, Yifa, Crown and pirate exchanges in the cumulative ROM."""

from collections import Counter
from inspect import getsource
from types import SimpleNamespace

from scripts import register_hodram_B161_B170_20261122 as parent
from scripts import review_hodram_B171_B172_20261122 as first
from scripts import review_hodram_B173_B175_20261122 as second
from scripts import review_hodram_B176_B180_20261122 as third
from scripts import stage_hodram_B161_B170_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
modal, ARCHIVE, logical_end = previous.modal, previous.ARCHIVE, previous.logical_end
paired = third.paired
ROOT = paired.ROOT / "B171_B180_staged_v2"
SOURCE, OUTPUT = paired.PACKET, paired.ROOT / "B171_B180_scoped_manuscript_v2.json"
ROM, PROOF = ROOT / "Hodram_B171_B180_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), tuple(paired.BLOCKS), (), ())
DEFAULT_NAMES = previous.DEFAULT_NAMES
DRAFTS = [review.OUTPUT for review in (first, second, third)]
FLEET_PANEL = "DK4_MES_B179_R0010"
FLEET_NAMES = ("Bergstrom Fleet", "I Fleet", "ABCDEFGHIJKLMNO Fleet", "ABCDEFGHIJKLMNOP Fleet")
FLEET_TEXT = ("You're with FO.", "Fancy meeting you here.")
REFINEMENTS = {
    "172_R0260": ("No, no! I've made up my mind. I'm coming! Don't worry. I'll put what I know to good use.", ["made up my mind.", "to good use."]),
    "173_R0058": ("But Admiral FI, you could call yourself master of the seas and mean it. What a feat that would be for us!", ["But Admiral FI,", "master of the seas"]),
    "174_R0135": ("Yifa, this is a navy ship. Do you still want to come aboard?", ["this is a navy ship.", "want to come aboard?"]),
    "175_R0056": ("I can't take her back. Breaking our country's ban on leaving is a grave offense. Our school has expelled her.",
                  ["take her back.", "ban on leaving", "expelled her."]),
    "176_R0015": ("That's enough to give you a toothache.", ["a toothache."]),
    "176_R0019": ("Huh? That usually makes you smile. You still like me, don't you?", ["usually makes you smile.", "You still like me, don't you?"]),
    "176_R0073": ("Sorry, I didn't see you. Welcome.", []),
    "178_R0042": ("Mihwa, it was FI who found the Silla Gold Crown.", ["the Silla Gold Crown."]),
    "178_R0074": ("My grandfather sailed all over the world. His stories made me want to see it for myself...",
                  ["all over the world.", "see it for myself..."]),
    "178_R0086": ("We don't sail for adventure, but we do travel all over the world.", ["sail for adventure,", "all over the world."]),
    "179_R0055": ("Don't butt in. Get back!", ["Don't butt in.", "Get back!"]),
    "179_R0065": ("My pride won't let me kill you here!", ["kill you here!"]),
    "179_R0072": ("We take pride in being pirates. You're a man of the sea. You know what I mean. We'll settle this at sea!",
                  ["pride in being pirates.", "a man of the sea.", "settle this at sea!"]),
    "179_R0080": ("Then say your prayers! ...Huh?", ["say your prayers!"]),
    "179_R0099": ("You'll find out someday. Move out, boys!", ["You'll find out someday.", "Move out, boys!"]),
}


def plan_fleet(row, raw, painter):
    assert row["id"] == FLEET_PANEL and TOKEN.findall(raw.decode("ascii")) == ["FO"]
    before, _ = modal.paint(painter, raw.replace(b"FO", FLEET_NAMES[2].encode("ascii")))
    assert [text for _,_,text in before] == [
        "You... from ABCDEFGHIJKLMNO Fleet. N", "ever", "expected to meet here."]
    shape = [(0, FLEET_TEXT[0]), (6, FLEET_TEXT[1])]
    for compiled in modal.layout.candidates(row, -1, shape):
        stored = compiled + b" " * ((len(compiled) ^ len(raw)) & 1)
        cases = []
        for name in FLEET_NAMES:
            expanded = stored.replace(b"FO", name.encode("ascii"))
            try:
                rows, plane = modal.paint(painter, expanded)
            except (AssertionError, ValueError):
                break
            expected = [(12 * i, text.replace("FO", name)) for i,text in enumerate(FLEET_TEXT)]
            if [(y,text) for y,_,text in rows] != expected or rows[0][1] != 0:
                break
            if any(x not in (0,6) or x + 6 * len(text) > 222 for _,x,text in rows):
                break
            cases.append(dict(name=name, rows=rows, expanded_hex=expanded.hex(), plane_sha256=native.digest(plane)))
        if len(cases) == len(FLEET_NAMES):
            return dict(compiled_hex=compiled.hex(), expected_hex=(b"\xfe"+stored).hex(),
                        rows=cases[0]["rows"], plane_sha256=cases[0]["plane_sha256"],
                        prior_long_name_rows=before, width_cases=cases)
    raise AssertionError((FLEET_PANEL, "No verified two-row fleet expansion"))


carried = checked_text(getsource(previous.carried_row), {
    'prior["block"] == 167': 'prior["block"] == 171',
    'context=third.CONTEXTS[167]': 'context=first.CONTEXTS[171]',
})
exec(compile(carried, __file__ + "::sail-lesson-carry", "exec"), globals())


def collect():
    packet, carry, release = map(base.load, (SOURCE, paired.CARRY, parent.RELEASE))
    assert base.digest(parent.ROM) == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(SOURCE) for doc in drafts)
    rows = {row["id"]: row for doc in drafts for row in doc["records"]}
    earlier = {row["id"]: row for row in carry["reused_records"]}
    assert len(rows) == sum(len(doc["records"]) for doc in drafts) == 288
    assert len(earlier) == 27 and not rows.keys() & earlier.keys()
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image,arm=image.read_file(native.ARM)))
    ordered, fe = [], {}
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
                row.update(english=wording, protected_phrases=phrases,
                           layout_refinement="Adjusted phrase protection after the first width check.")
            if short == "173_R0138":
                row["formatting_retention_reason"] = ("The first page completes the advice about gift-giving. "
                    "The second sets apart Mikhail's excuse about winning a woman's heart and leaves room for Hodram's joke.")
            if ident == FLEET_PANEL:
                assert row["kind"] == "system-FE" and row["decision"] == "retention"
                row.update(english=" ".join(FLEET_TEXT), protected_phrases=list(FLEET_TEXT),
                    decision="revision", change_class="wording", prior_retention_note=row["localization_note"],
                    localization_note="The pirate recognizes the original fleet name and expresses surprise at meeting them. "
                    "Finish the identification before the greeting to keep the whole phrase visible with a long fleet name.")
            if row["kind"] == "system-FE" and row["decision"] == "revision":
                raw = bytes.fromhex(row["current_hex"])[1:]
                if ident == FLEET_PANEL:
                    fe[ident] = plan_fleet(row,raw,painter)
                else:
                    body, expected, cells, raster = modal.plan(row | {"source_record_index": -1},raw,painter)
                    fe[ident] = dict(compiled_hex=body.hex(),expected_hex=(b"\xfe"+expected).hex(),
                                     rows=cells,plane_sha256=native.digest(raster))
            ordered.append(row | {"route":1})
    assert not rows and not earlier and len(fe)==12
    findings = dict(Counter(r["change_class"] for r in ordered))
    assert findings == {"wording": 119, "retention": 196}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
        source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE=fe,
        source_and_draft_evidence={str(path): base.digest(path) for path in [*DRAFTS,paired.CARRY]},
        contextual_records_revisited=288, contextual_decisions_reused=27, new_editorial_credit=0,
        status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


if __name__ == "__main__":
    launch = getsource(previous.main)
    exec(compile(launch, __file__ + "::stored-rom", "exec"), globals())
    staging = previous.staging
    main()

