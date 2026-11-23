"""Compile the contextual Hodram ruins and expedition batch and three earlier wrap repairs."""

from collections import Counter
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_B292_B310_20261122 as paired
from scripts import stage_hodram_B201_B220_20261122 as modal_layout
from scripts import stage_hodram_B261_B291_20261122 as previous


parent = paired.build
base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
engine, ARCHIVE, logical_end = previous.engine, previous.ARCHIVE, previous.logical_end
DEFAULT_NAMES, modal = previous.DEFAULT_NAMES, previous.modal
ROOT = paired.ROOT / "B292_B310_staged_v1"
SOURCE = paired.ROOT / "paired_with_B277_B283_B286_followups_v1.json"
OUTPUT = paired.ROOT / "B292_B310_scoped_manuscript_v1.json"
ROM, PROOF = ROOT / "Hodram_B292_B310_STAGED.nds", ROOT / "stored_proof.json"
EARLIER_BLOCKS = (277, 283, 286)
BLOCKS = ((), (*EARLIER_BLOCKS, *paired.BLOCKS), (), ())
DRAFTS = [paired.ROOT / f"{span}_contextual_v1.json" for span in (
    "B292_B293", "B294_B299", "B300_B303", "B304_B308", "B309_B310")]
OPENING = paired.ROOT / "B292_B293_wrap_preflight_v1.json"
FOLLOWUP = paired.ROOT / "B277_B283_B286_wrap_followup_v1.json"
FE_MACROS = {"DK4_MES_B309_R0174": " was injured."}
FE_REVISIONS = {"DK4_MES_B302_R0203", "DK4_MES_B304_R0137", "DK4_MES_B304_R0155", "DK4_MES_B309_R0280"}
REFINEMENTS = {
    "296_R0057": ("Don't worry. We'll make what we need ourselves.", []),
    "300_R0174": ("Nngh! I can't pull you out alone. Everyone, give me a hand!", []),
    "300_R0197": ("Hah, hah... FI, are you all right?", []),
    "302_STYLE_1786_62": ("This sandstorm shows no sign of letting up. Your orders, Admiral?", []),
    "302_STYLE_2582_176": ("We ought to be nearly through the desert...", []),
    "308_STYLE_8_192": ("Admiral, what's the clan guarding the map to the Proof like? Way northeast of China, right? Let's go see!", []),
    "308_STYLE_8_498": ("Admiral, about the Proof... Shall we hurry to see the clan that guards its map, in the village far northeast of China?", []),
    "308_STYLE_8_716": ("Admiral, I'm curious about the map to the Proof. Shall we visit the village of its guardians, far northeast of China?", []),
    "309_STYLE_2364_268": ("Hah, hah... We're safe here, right?", []),
    "310_R0016": ("Foreign pressure has all but ended our isolation policy. All right, I'll tell you. Keep it between us.", []),
}


def bind_wraps(groups, requests):
    prior = {row["id"]:row for row in base.load(parent.REVIEW)["records"] if row["block"] in EARLIER_BLOCKS}
    requests = {row["id"]:row for row in requests}
    assert len(prior) == sum(len(group["records"]) for group in groups) == 59 and len(requests) == 3
    for group in groups:
        for original in group["records"]:
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
                source_selector=original["selector"], native_slots=original["slots"], source_hex=earlier["source_hex"],
                current_hex=current_hex, previous_English=earlier["english"], english=earlier["english"],
                protected_phrases=[], context=earlier["context"], source_meaning=earlier["source_meaning"],
                localization_note=earlier["localization_note"], decision="retention", change_class="retention",
                decision_carried=True, previous_registered_reference=registered, review=earlier["review"].copy())
            if ident in requests:
                request = requests.pop(ident)
                assert request["registered_reference"] == registered and request["current_English"] == row["english"]
                assert request["source_hex"] == row["source_hex"]
                row.update(english=request["proposed_English"], decision="revision", change_class="wording",
                           decision_carried=False, layout_followup=True, localization_note=request["reason"],
                           prior_localization_note=row["localization_note"], review=row["review"] | {"formatting":False})
            yield row
    assert not prior and not requests


def collect():
    packet, carry, release, opening, followup = map(base.load,
        (paired.PACKET, paired.CARRY, parent.RELEASE, OPENING, FOLLOWUP))
    candidate = base.digest(parent.ROM)
    assert candidate == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert base.digest(paired.PACKET) == carry["source_packet_sha256"] == opening["source_packet_sha256"]
    assert not carry["reused_records"] and len(carry["pending_records"]) == 380
    assert base.digest(parent.REVIEW) == followup["review_ledger_sha256"]
    for item in followup["records"]:
        sheet = item["checked_contact_sheet"]
        assert base.digest(sheet["path"]) == sheet["sha256"]
    assert base.digest(DRAFTS[0]) == opening["contextual_draft_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]

    prior_groups = paired.pairing.source_and_current(parent, EARLIER_BLOCKS)["groups"]
    combined = packet | dict(groups=[*prior_groups, *packet["groups"]],
                             original_packet_sha256=base.digest(paired.PACKET))
    if SOURCE.exists():
        assert base.load(SOURCE) == combined
    else:
        base.save(SOURCE, combined)
    drafts = list(map(base.load, DRAFTS))
    assert all(draft["source_packet_sha256"] == base.digest(paired.PACKET) for draft in drafts)
    by_id = {row["id"]:row for draft in drafts for row in draft["records"]}
    assert len(by_id) == sum(len(draft["records"]) for draft in drafts) == 380
    ordered = list(bind_wraps(prior_groups, followup["records"]))
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
    assert not by_id and len(ordered) == 439

    planner = engine.assemble({}).__globals__["plan_progressive"]
    prior_plans = {r["id"]:r["native_layout_preflight"]["encoded_hex"] for r in followup["records"]}
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image, arm=image.read_file(native.ARM)))
    planned_FE = {}
    for row in ordered:
        if row["decision"] != "revision":
            continue
        ident = row["id"]
        prefix = int(row["kind"] in ("progressive", "system-FE"))
        old, clean = [bytes.fromhex(row[key])[prefix:] for key in ("current_hex", "source_hex")]
        if row["kind"] == "system-FE":
            assert ident in FE_REVISIONS
            compiled, stored, rows, plane = modal_layout.plan_two_rows(row, old, painter, (row["english"],))
            planned_FE[ident] = dict(compiled_hex=compiled.hex(), expected_hex=(b"\xfe"+stored).hex(),
                                     rows=rows, plane_sha256=native.digest(plane))
            continue
        try:
            _, plan = planner(row, row["source_selector"], old, clean)
        except (AssertionError, ValueError) as err:
            raise ValueError(f"Unable to plan {ident}") from err
        if row["kind"] == "actor-style":
            assert plan["expected_native_pages"] == 1, (ident, plan["lines"])
        if ident in prior_plans:
            assert plan["encoded_hex"] == prior_plans.pop(ident)
        if row["english"] == row["previous_English"]:
            row.update(change_class="wrap-only")
    assert not prior_plans and set(planned_FE) == FE_REVISIONS

    findings = dict(Counter(row["change_class"] for row in ordered))
    assert sum(count for key,count in findings.items() if key != "retention") == 115
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=candidate,
                previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE=planned_FE,
                source_and_draft_evidence={str(path):base.digest(path) for path in [*DRAFTS, paired.CARRY, OPENING, FOLLOWUP]},
                contextual_records_revisited=383, contextual_decisions_reused=56, new_editorial_credit=0,
                status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


if __name__ == "__main__":
    original_main = previous.previous.previous.previous.main
    FunctionType(original_main.__code__, original_main.__globals__ | globals())()
