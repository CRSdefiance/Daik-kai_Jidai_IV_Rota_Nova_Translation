"""Check both facility substitutions for the proposed Market refusal reflow."""

from pathlib import Path

from scripts import register_claudio_opening_wrap_20261124 as current
from scripts import stage_market_trade_dialogue_20261115 as native
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = evidence.OUT.with_name("ceuta_contract_refusal_preflight_20261124.json")
ROOT = current.ROM.parent.with_name("editorial_20261124_ceuta_contract_refusal_preflight")
PRIOR = Path("releases/all_routes_editorial_20261115_market_trade_dialogue_candidate/verification/registered_review.json")
KEY = 761
DRAFT = "Sorry. Once you sign a contract at the %s, come back."
FACILITIES = ("Palace", "Governor's Office")
EXPECTED = {
    "Palace": ("Sorry. Once you sign a contract", "at the Palace, come back."),
    "Governor's Office": ("Sorry. Once you sign a contract at", "the Governor's Office, come back."),
}


def main():
    rel = read(current.RELEASE)
    assert digest(REGISTRY) == rel["registry_sha256"] and digest(CLEAN) == rel["clean_input_sha256"]
    startup = read(rel["own_registered_startup"])
    ctx = native.RegisteredRuntime(current.RELEASE, rel["own_registered_startup"], captain=startup["actual_captain_getter"])
    clean = NdsImage.open(CLEAN)
    source_arm = clean.read_file(current.ARM)
    source = native.common_message_entries(clean.read_file(current.COMMON), source_arm)[KEY]
    assert sha256(ctx.arm).hexdigest() == rel["target_ARM9_sha256"] and sha256(ctx.common).hexdigest() == rel["target_COMMON_sha256"]
    records = native.owned_entries(ctx.common, ctx.arm, digest_range(ctx.arm))
    old = records[KEY]
    former, = (r for r in read(PRIOR)["records"] if r["message_ID"] == KEY)
    assert source.text.hex() == former["source_hex"] and old.text.hex() == former["staged_hex"]
    assert all(ctx.arm[lo:hi] == source_arm[lo:hi] for lo, hi in ((0xBA318, 0xBA334), (0xBA41C, 0xBA42C)))
    lab_checks = native.context_cases(ctx.arm)["contract_facility_cases"]
    assert {bytes.fromhex(row["argument_hex"]).decode("ascii") for row in lab_checks} == set(FACILITIES)

    candidate_body = b" " + DRAFT.encode("ascii")
    assert all(body.count(b"%") == body.count(b"%s") == 1 for body in (source.text, old.text, candidate_body))
    assert b"\n" not in candidate_body
    deployed, rebound, slots = native.owned_deployment(ctx.common, ctx.arm, records, {KEY: candidate_body})
    assert len(deployed) == len(ctx.common)
    assert [a.message_id for a, b in zip(records, rebound, strict=True) if a.text != b.text] == [KEY]
    target = native.with_components(ctx, ctx.arm, deployed)
    raster, _, _ = native.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    figures, checks = [], {}
    for label, runtime, body in (("Current", ctx, old.text), ("Proposed", target, candidate_body)):
        cpu, getter, io = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
        address = getter(0x5528C, KEY)
        assert bytes(cpu.mem_read(address, len(body) + 1)) == body + b"\0" and io.reads
        for facility in FACILITIES:
            raw, lines = native.native_layout(cpu, body, KEY, (facility,), parent=0x02054014)
            assert " ".join(lines) == body.decode("ascii").strip() % facility
            assert sum(facility in line for line in lines) == 1
            if label == "Proposed":
                assert tuple(lines) == EXPECTED[facility]
                assert lines[-1].endswith(facility + ", come back.")
            ink, _ = native.render_portrait(raster, ctx.arm, kanji, raw)
            checks[label, facility] = dict(version=label, facility=facility, lines=lines,
                formatted_hex=raw.hex(), complete_glyph_mask_sha256=sha256(ink).hexdigest(), pages=1)
            figures.append((f"{label} - {facility}", ink))
    ROOT.mkdir(exist_ok=True)
    sheet, = native.portrait_sheets(ROOT, figures)
    write(OUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=list(GATES), parent_candidate_sha256=rel["candidate_sha256"],
        proposed_COMMON_sha256=sha256(deployed).hexdigest(), one_owned_allocation=slots[KEY],
        native_facility_arg_cases=lab_checks, both_substitutions=list(checks.values()), native_preview=sheet,
        records=[dict(id="COMMON_MESSAGE_761", message_ID=KEY, file_path=current.COMMON, speaker="Trader",
            context="When Hodram selects Trade without a contract, the trader apologizes and says where to sign before returning.",
            source_meaning="Sorry, please come back after making a contract at the named facility.",
            clean_Japanese=source.text.decode("cp932"), english=DRAFT, current_english=old.text.decode("ascii").strip(),
            localization_note="The apology starts the refusal. The condition keeps the contract and where to sign it. Both facility names and the invitation to return fit on the final line.",
            decision="revision_proposed", source_reference=evidence.source_ref(source), current_reference=evidence.source_ref(old),
            proposed_reference=evidence.source_ref(rebound[KEY]), review=dict.fromkeys(GATES, True) | {"formatting": False})],
        offline_only=True, paired_gameplay_pending=True, registered=False, new_editorial_credit=0,
        prior_review=reference(PRIOR)))
    print("Verified four native portrait masks and both facility substitutions for the proposed Market refusal.")


def digest_range(arm):
    return sha256(arm[native.DIRECTORY_OFFSET:native.TABLE_OFFSET]).hexdigest()


if __name__ == "__main__":
    main()
