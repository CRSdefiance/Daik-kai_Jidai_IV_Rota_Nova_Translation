"""Compile Hodram's quests and crew encounters, with two earlier figurehead wrap repairs."""

from collections import Counter
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_B261_B291_20261122 as paired
from scripts import stage_hodram_B201_B220_20261122 as modal_layout
from scripts import stage_hodram_B241_B260_20261122 as previous


parent = paired.build
base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
engine, ARCHIVE, logical_end = previous.engine, previous.ARCHIVE, previous.logical_end
DEFAULT_NAMES = previous.DEFAULT_NAMES
ROOT = paired.ROOT / "B261_B291_staged_v1"
SOURCE, OUTPUT = paired.ROOT / "paired_with_B243_figurehead_v1.json", paired.ROOT / "B261_B291_scoped_manuscript_v2.json"
ROM, PROOF = ROOT / "Hodram_B261_B291_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), (243, *paired.BLOCKS), (), ())
DRAFTS = [paired.ROOT / f"{span}_contextual_v1.json" for span in (
    "B261_B264", "B265_B280", "B281_B289", "B290", "B291")]
OPENING = paired.ROOT / "B261_B264_wrap_preflight_v1.json"
FIGURE = paired.ROOT / "B243_figurehead_wrap_followup_v1.json"
modal = engine.modal
FE_MACROS = {"DK4_MES_B243_R0163": "'s Spirit rose by 1!"}

REFINEMENTS = {
    '266_R0009': ("Julian Vermeer betrayed his native Portugal and sided with Spain. I hear he's working as a courier in the Mediterranean.", []),
    '268_R0012': ("Julian the courier... His fleet is in the Mediterranean, right?", ["in the Mediterranean, right?"]),
    '268_R0024': ("Catch that traitor Julian as soon as you can. I hear he's working as a courier in the Mediterranean.", []),
    '271_R0008': ("I-I'm telling you, I'm sorry...", []),
    '273_R0005': ("I've got a bounty for you. Bring in a man named Jean Ramusio.", []),
    '273_R0009': ("We were after him for smuggling. When we sent a force after him in India, he sent them packing.", []),
    '280_R0008': ("Tied up and still acting like a king. Unbelievable.", []),
    '281_R0012': ("I'd better stop Hernan. He's prowling the Mediterranean.", []),
    '282_R0019': ("The Arab pirate is Iscal Yasar. He's beaten many fleets sent after him. You are our last hope. I'm counting on you.", []),
    '283_R0016': ("This hardly repays what you've done for us, but I ask that you accept it.", []),
    '283_R0093': ("I don't know. When powerful people in so many countries are this desperate to find them, I doubt they're worthless...", []),
    '283_R0097': ("Then again, it wouldn't be the first time we all got caught up chasing a fantasy.", []),
    '284_R0006': ("Admiral, His Majesty wants to see you. Please return to Stockholm at once.", []),
    '286_R0031': ("The gang doesn't operate openly as a faction, and William himself hardly ever shows his face.", []),
    '287_R0077': ("They say our ancestors built the ruins to honor their warriors.", []),
    '287_R0096': ("Hold on. You're giving me too much credit. I can't take on a request like that...", []),
    '287_R0104': ("We ask anyone who looks strong enough, whoever comes along.", []),
    '287_R0125': ("First, you'll need a map to the ruins. Come see me when you have the Ancient City Map. I'll join you in the search.", []),
    '290_STYLE_3300_186': ("Admiral, we made it out of the woods! Those are the ruins, all right!", []),
    '291_R0119': ("Rrraah!!", []),
}


def bind_figurehead(group, followup):
    originals = group["records"]
    prior = {row["id"]:row for row in base.load(parent.REVIEW)["records"] if row["block"] == 243}
    requests = {row["id"]:row for row in followup["records"]}
    assert len(prior) == len(originals) == 36 and len(requests) == 2
    for original in originals:
        ident = original["id"]
        earlier = prior.pop(ident)
        assert all(earlier["review"].values()) and earlier["source_reference"] == original["source_reference"]
        registered = earlier["registered_reference"]
        prefix = f"{original['selector']:02x}" if original["native_command_word"] == 0x4000 else ""
        current_hex = prefix + original["current_reference"]["exact_body_hex"]
        assert current_hex == registered["exact_stored_hex"]
        assert all(registered[key] == original["current_reference"][key]
                   for key in ("archive_sha256", "block_sha256", "command_offset", "offset"))
        assert " ".join(original["current_English"].split()) == earlier["english"]
        row = original | dict(kind=earlier["kind"], route=1, speaker=earlier["speaker"],
            source_selector=original["selector"], native_slots=original["slots"],
            source_hex=earlier["source_hex"], current_hex=current_hex, previous_English=earlier["english"],
            english=earlier["english"], protected_phrases=[], context=earlier["context"],
            source_meaning=earlier["source_meaning"], localization_note=earlier["localization_note"],
            decision="retention", change_class="retention", decision_carried=True,
            previous_registered_reference=registered, review=earlier["review"].copy())
        if ident in requests:
            request = requests.pop(ident)
            assert request["registered_reference"] == registered and request["current_English"] == row["english"]
            assert request["source_hex"] == row["source_hex"]
            row.update(english=request["proposed_English"], decision="revision", change_class="wording",
                       decision_carried=False, localization_note=request["reason"], layout_followup=True,
                       prior_localization_note=row["localization_note"], review=row["review"] | {"formatting":False})
        yield row
    assert not prior and not requests


def collect():
    packet, carry, release, opening, followup = map(base.load,
        (paired.PACKET, paired.CARRY, parent.RELEASE, OPENING, FIGURE))
    candidate = base.digest(parent.ROM)
    assert candidate == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert base.digest(paired.PACKET) == carry["source_packet_sha256"] == opening["source_packet_sha256"]
    assert not carry["reused_records"] and len(carry["pending_records"]) == 335
    assert base.digest(parent.REVIEW) == followup["review_ledger_sha256"]
    assert base.digest(followup["checked_contact_sheet"]["path"]) == followup["checked_contact_sheet"]["sha256"]
    assert base.digest(DRAFTS[0]) == opening["contextual_draft_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]

    figurehead, = paired.pairing.source_and_current(parent, (243,))["groups"]
    combined = packet | dict(groups=[figurehead, *packet["groups"]],
                             original_packet_sha256=base.digest(paired.PACKET))
    if SOURCE.exists():
        assert base.load(SOURCE) == combined
    else:
        base.save(SOURCE, combined)
    drafts = list(map(base.load, DRAFTS))
    assert all(draft["source_packet_sha256"] == base.digest(paired.PACKET) for draft in drafts)
    by_id = {row["id"]:row for draft in drafts for row in draft["records"]}
    assert len(by_id) == sum(len(draft["records"]) for draft in drafts) == 335
    ordered = list(bind_figurehead(figurehead, followup))
    for group in packet["groups"]:
        for original in group["records"]:
            row = by_id.pop(original["id"])
            assert all(row[key] == value for key, value in original.items())
            ident = row["id"]
            short_id = ident.rsplit("_B", 1)[1]
            refinement = opening["refinements"].get(ident) or REFINEMENTS.get(short_id)
            if refinement:
                assert row["decision"] == "revision"
                english, phrases = refinement
                row.update(english=english, protected_phrases=phrases)
            ordered.append(row | {"route":1})
    assert not by_id and len(ordered) == 371

    planner = engine.assemble({}).__globals__["plan_progressive"]
    figure_plans = {row["id"]:row["native_layout_preflight"]["encoded_hex"] for row in followup["records"]}
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image, arm=image.read_file(native.ARM)))
    planned_FE = {}
    for row in ordered:
        if row["decision"] != "revision":
            continue
        prefix = int(row["kind"] in ("progressive", "system-FE"))
        old, clean = [bytes.fromhex(row[key])[prefix:] for key in ("current_hex", "source_hex")]
        if row["kind"] == "system-FE":
            assert row["id"] == "DK4_MES_B291_R0119"
            compiled, stored, rows, plane = modal_layout.plan_two_rows(row, old, painter, (row["english"],))
            planned_FE[row["id"]] = dict(compiled_hex=compiled.hex(), expected_hex=(b"\xfe"+stored).hex(),
                                          rows=rows, plane_sha256=native.digest(plane))
            continue
        try:
            _, plan = planner(row, row["source_selector"], old, clean)
        except (AssertionError, ValueError) as err:
            raise ValueError(f"Unable to plan {row['id']}") from err
        if row["id"] in figure_plans:
            assert plan["encoded_hex"] == figure_plans.pop(row["id"])
    assert not figure_plans

    findings = dict(Counter(row["change_class"] for row in ordered))
    assert findings == {"wording":145, "retention":226}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=candidate,
                previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE=planned_FE,
                source_and_draft_evidence={str(path):base.digest(path) for path in [*DRAFTS, paired.CARRY, OPENING, FIGURE]},
                contextual_records_revisited=337, contextual_decisions_reused=34, new_editorial_credit=0,
                status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


if __name__ == "__main__":
    original_main = previous.previous.previous.main
    FunctionType(original_main.__code__, original_main.__globals__ | globals())()
