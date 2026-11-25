"""Review the six native voice prompts that ask for a diversion destination."""

from struct import unpack_from

from scripts import register_seoul_reika_20261125 as current
from scripts import stage_market_trade_dialogue_20261115 as native
from scripts import verify_riga_trade_deck_20261124 as review
from scripts import verify_tavern_strategist_followup_20261119 as schemes
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = review.OUT.with_name("fleet_diversion_questions_preflight_20261125.json")
TABLE = 0x02118300
BASE = 0x02000000
DRAFTS = {
    923: "Where do you want me to send 'em?",
    926: "Where would you have us send them?",
}
NOTES = {
    921: ("The speaker politely asks which town they should send the other fleet to.",
          "The direct first-person question suits the courteous adviser and reads in one line."),
    922: ("The speaker asks which town the player intends to send the fleet to.",
          "The informal question sounds like a quick planning exchange and keeps the whole destination question together."),
    923: ("The rougher speaker asks which town the player wants them to send the fleet to.",
          "The contraction keeps the unpolished voice. The question fits on one line without stranding the object and preposition."),
    924: ("The speaker considers aloud which town to send the fleet to.",
          "Shall keeps the speaker's measured deliberation and the complete question fits the panel."),
    925: ("The speaker asks conversationally which town the other fleet should go to.",
          "The simple question fits a quick exchange and points directly to the decision in the menu."),
    926: ("The speaker asks courteously where their group should send the fleet.",
          "Would you have us keeps the deliberate deference and the plural adviser voice. The entire question fits together."),
}


def main():
    release = read(current.RELEASE)
    assert digest(current.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    startup = read(release["own_registered_startup"])
    context = native.RegisteredRuntime(current.RELEASE, release["own_registered_startup"],
                                       captain=startup["actual_captain_getter"])
    clean = NdsImage.open(CLEAN)
    clean_arm, arm, archive = clean.read_file(current.ARM), context.arm, context.common
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    lo, hi = 0x02057104 - BASE, 0x02057190 - BASE
    assert clean_arm[lo:hi] == arm[lo:hi]
    assert unpack_from("<I", arm, 0x02057184 - BASE) == (TABLE,)
    keys = unpack_from("<8i", clean_arm, TABLE - BASE)
    assert keys == unpack_from("<8i", arm, TABLE - BASE) == (921, -1, 922, -1, 923, 924, 925, 926)
    source = native.common_message_entries(clean.read_file(current.COMMON), clean_arm)
    ownership = sha256(arm[native.DIRECTORY_OFFSET:native.TABLE_OFFSET]).hexdigest()
    stored = native.owned_entries(archive, arm, ownership)
    replacements = {key: b" " + draft.encode("ascii") for key, draft in DRAFTS.items()}
    patched, proposed, allocations = native.owned_deployment(archive, arm, stored, replacements)
    assert len(archive) == len(patched)
    assert {a.message_id for a, b in zip(stored, proposed, strict=True) if a.text != b.text} == DRAFTS.keys()
    target = native.with_components(context, arm, patched)
    kanji = context.image.read_file("/GRP/KANJI.FNT")
    formatter, effective_source = schemes.formatter()
    layout = schemes.machine(arm)
    layout.mem_write(BASE, context.raw)

    records, previews = [], []
    for key, (meaning, note) in NOTES.items():
        a, b, c = source[key], stored[key], proposed[key]
        assert b.text.startswith(b" ") and c.text.startswith(b" ")
        assert b"%" not in a.text + b.text + c.text and b"\n" not in c.text and c.text.isascii()
        passes = []
        versions = [("Current", context, b)]
        if key in DRAFTS:
            versions.append(("Proposed", target, c))
        for label, runtime, row in versions:
            cpu, pull, io = runtime.machine(arm, runtime.common, runtime.raw, runtime.plan)
            address = pull(0x5528C, key)
            assert bytes(cpu.mem_read(address, len(row.text) + 1)) == row.text + b"\0" and io.reads
            body = row.text.decode("ascii").strip()
            result = formatter(layout, dict(message_id=key, english=body, source_voice_table=TABLE,
                                            English_argument_source_indices=[]), ())
            formatted = bytes.fromhex(result["formatted_hex"])
            lines = result["lines"]
            assert " ".join(lines) == row.text.decode("ascii").strip()
            assert len(lines) == (2 if key in DRAFTS and label == "Current" else 1)
            if label == "Proposed" or key not in DRAFTS:
                assert not result["findings"]
            plane = schemes.native_portrait(arm, kanji, formatted, lines)
            previews.append((f"{key} {label}", plane))
            passes.append(result | dict(version=label, pages=1, complete_glyph_mask_sha256=sha256(plane).hexdigest()))
        english = c.text.decode("ascii").strip()
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=current.COMMON,
            speaker="Crew adviser selected by the native voice table",
            context="After the player selects Lure Fleet and an opposing faction, the adviser asks for the destination.",
            clean_Japanese=a.text.decode("cp932"), english=english, source_meaning=meaning, localization_note=note,
            source_reference=review.source_ref(a), current_reference=review.source_ref(b),
            installed_reference=review.source_ref(b), proposed_reference=review.source_ref(c),
            decision="revision_proposed" if key in DRAFTS else "retention", native_layouts=passes,
            review=dict.fromkeys(GATES, True) | {"formatting": key not in DRAFTS}))
    folder = current.ROM.parent.with_name("editorial_20261125_fleet_diversion_native")
    folder.mkdir(exist_ok=True)
    figures = native.portrait_sheets(folder, previews)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], translation_policy="natural-dialogue-v2",
                    target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=list(GATES),
                    voice_table=dict(address=TABLE, slot_values=keys, exact_code_sha256=sha256(arm[lo:hi]).hexdigest()),
                    original_formatter_parent=0x02053DB8, native_formatter_source_sha256=sha256(effective_source.encode()).hexdigest(),
                    records=records, proposed_COMMON_sha256=sha256(patched).hexdigest(), allocations=allocations,
                    native_previews=figures, all_placements_same_allocation=True, ordinary_gameplay=False,
                    scope="Offline native portrait pages. The separate no-eligible-town message and its renderer are outside this batch.",
                    registered=False, new_editorial_credit=0))
    print("Verified four retained and two revised diversion questions in eight native previews.")


if __name__ == "__main__":
    main()
