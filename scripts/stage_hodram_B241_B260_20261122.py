"""Stage Hodram's ruins and guild exchanges with the one-page convoy letter."""

from collections import Counter
from inspect import getsource
from types import SimpleNamespace

from scripts import pair_hodram_B241_B260_20261122 as paired
from scripts import stage_hodram_B201_B220_20261122 as modal_layout
from scripts import stage_hodram_B221_B240_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


parent = paired.build
base, native, compiler, TOKEN = previous.base, previous.native, previous.compiler, previous.TOKEN
engine, ARCHIVE, logical_end = previous.engine, previous.ARCHIVE, previous.logical_end
modal = engine.modal
DEFAULT_NAMES = previous.DEFAULT_NAMES
ROOT = paired.ROOT / "B241_B260_staged_v1"
SOURCE, OUTPUT = paired.ROOT / "paired_with_B238_convoy_v1.json", paired.ROOT / "B241_B260_scoped_manuscript_v1.json"
ROM, PROOF = ROOT / "Hodram_B241_B260_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), (238, *paired.BLOCKS), (), ())
DRAFTS = [paired.ROOT / f"{span}_contextual_v1.json" for span in (
    "B241_B242", "B243", "B244_B250", "B251_B252", "B253_B260")]
OPENING_PREFLIGHT = paired.ROOT / "B241_B243_wrap_preflight_v1.json"
CONVOY = paired.ROOT / "B238_R0035_convoy_page_followup_v1.json"
CONVOY_ID = "DK4_MES_B238_R0035"
ICE_ROWS = {
    "DK4_MES_B252_R0009": (
        "A vessel is filled to the brim", "with water. A piece of ice floats",
        "on the surface. When the ice melts,", "what happens to the water level?",
    ),
    "DK4_MES_B252_R0012": (
        "Press the front stone for a rise.", "Press the left stone for a fall.",
        "Press the right stone for no change.",
    ),
}
FE_MACROS = {
    "DK4_MES_B243_R0163": "'s Spirit rose by 1!",
    "DK4_MES_B251_R0085": "'s Luck rose by 1!",
    "DK4_MES_B251_R0113": "'s Charm rose by 1!",
}
REFINEMENTS = {
    "DK4_MES_B251_R0053": (
        "It's a magnificent figurehead. Mounting it might bring us luck. But should we take it without asking?",
        ["a magnificent figurehead.", "might bring us luck.", "without asking?"],
    ),
}

prior_letter = checked_text(getsource(previous.bind_prior_letter), {
    "bind_prior_letter": "bind_convoy",
    'r["block"] == 218': 'r["block"] == 238',
    'len(group["records"]) == 17': 'len(group["records"]) == 16',
    "SIGNATURE_ID": "CONVOY_ID",
    'ask["english"] == row["english"]': 'ask["previous_English"] == row["english"]',
    'row.update(decision="revision", change_class="wrap-only", decision_carried=False,':
        'row.update(decision="revision", change_class="wording", decision_carried=False, english=ask["english"],',
    'review=ask["review"], prior_retention_note=prior["localization_note"],\n'
    '                deliberate_break_reason="The native letter gives the signoff and signature distinct rows.")':
        'review=ask["review"], prior_localization_note=prior["localization_note"])',
})
exec(compile(prior_letter, __file__ + "::exact-convoy-carry", "exec"), globals())


def collect():
    packet, carry, release, convoy, opening = map(base.load,
        (paired.PACKET, paired.CARRY, parent.RELEASE, CONVOY, OPENING_PREFLIGHT))
    candidate = base.digest(parent.ROM)
    assert candidate == packet["candidate_sha256"] == release["candidate_sha256"] == convoy["candidate_sha256"]
    assert carry["source_packet_sha256"] == base.digest(paired.PACKET) and not carry["reused_records"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert convoy["registered_review_sha256"] == base.digest(parent.REVIEW)
    assert all(base.digest(h["path"]) == h["PNG_sha256"] for h in convoy["gameplay"])
    assert all(base.digest(path) == sha for path, sha in opening["drafts"].items())
    preceding, = paired.pairing.source_and_current(parent, (238,))["groups"]
    combined = packet | dict(groups=[preceding, *packet["groups"]], original_packet=str(paired.PACKET),
                             original_packet_sha256=base.digest(paired.PACKET))
    if SOURCE.exists():
        assert base.load(SOURCE) == combined
    else:
        base.save(SOURCE, combined)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(paired.PACKET) for doc in drafts)
    by_id = {r["id"]: r for doc in drafts for r in doc["records"]}
    assert len(by_id) == sum(len(doc["records"]) for doc in drafts) == 224
    ordered = list(bind_convoy(preceding, convoy))
    for group in packet["groups"]:
        for original in group["records"]:
            row = by_id.pop(original["id"])
            assert all(row[k] == v for k, v in original.items())
            ident = row["id"]
            if ident in REFINEMENTS:
                english, phrases = REFINEMENTS[ident]
                assert row["decision"] == "revision"
                row.update(english=english, protected_phrases=phrases)
            if ident in ICE_ROWS:
                assert row["decision"] == "revision" and row["source_selector"] == 254
                row.update(english=" ".join(ICE_ROWS[ident]), protected_phrases=[],
                           layout_refinement="Keep the inscription's questions and choices in clear, ordered phrases.")
            ordered.append(row | {"route": 1})
    assert not by_id and len(ordered) == 240
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image, arm=image.read_file(native.ARM)))
    planner = engine.assemble({}).__globals__["plan_progressive"]
    fe = {}
    for row in ordered:
        if row["decision"] != "revision":
            continue
        prefix = int(row["kind"] in ("progressive", "system-FE"))
        old, clean = [bytes.fromhex(row[k])[prefix:] for k in ("current_hex", "source_hex")]
        ident = row["id"]
        if ident in ICE_ROWS:
            body, encoded, cells, raster = modal_layout.plan_two_rows(row, old, painter, ICE_ROWS[ident])
            fe[ident] = dict(compiled_hex=body.hex(), expected_hex=(b"\xfe" + encoded).hex(),
                             rows=cells, plane_sha256=native.digest(raster))
            continue
        assert row["source_selector"] != 254
        try:
            _, planned = planner(row, row["source_selector"], old, clean)
        except (AssertionError, ValueError) as err:
            raise ValueError(f"Unable to plan {ident}") from err
        if ident == CONVOY_ID:
            assert planned["encoded_hex"] == convoy["native_layout_preflight"]["encoded_hex"]
    findings = dict(Counter(r["change_class"] for r in ordered))
    assert findings == {"wording": 84, "retention": 156}
    return dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                target_locale="en-US", review_gates=drafts[0]["review_gates"], previous_sha256=candidate,
                previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                source_packet_sha256=base.digest(SOURCE), records=ordered, findings=findings, planned_FE=fe,
                source_and_draft_evidence={str(path):base.digest(path) for path in [*DRAFTS, paired.CARRY, CONVOY, OPENING_PREFLIGHT]},
                contextual_records_revisited=225, contextual_decisions_reused=15, new_editorial_credit=0,
                status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")


if __name__ == "__main__":
    exec(compile(getsource(previous.previous.main), __file__ + "::stored-rom", "exec"), globals())
    main()
