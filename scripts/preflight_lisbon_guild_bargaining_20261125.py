"""Check complete purchase and sale bargaining phrases in the native queue."""

from struct import unpack_from

from scripts import stage_market_trade_dialogue_20261115 as native
from scripts import verify_lisbon_guild_bargaining_20261125 as review
from scripts import verify_tavern_strategist_followup_20261119 as renderer
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


current = review.play.current
OUT = review.OUT.with_name("lisbon_guild_bargaining_preflight_20261125.json")
WORK = current.ROM.parent.with_name("editorial_20261125_guild_bargaining_preflight")
DRAFTS = {
    1080: (0x02118160, "That's steep. Can't you do better?", ("That's steep. Can't you do better?",),
           "Julio says the asking price is high and presses the Guildmaster to lower it.",
           "The brief complaint and pointed question sound like Julio and stay together on one line."),
    1092: (0x02118140, "Eh? Can't you see what it's worth? Take a closer look!",
           ("Eh? Can't you see what it's worth?", "Take a closer look!"),
           "Julio is incredulous that the Guildmaster has undervalued the item and tells him to look more closely.",
           "The rhetorical question keeps Julio's challenge and the short command completes the reply on its own line."),
}


def main():
    release = read(current.RELEASE)
    assert digest(current.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    startup = read(release["own_registered_startup"])
    ctx = native.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=startup["actual_captain_getter"])
    image = NdsImage.open(CLEAN)
    clean_arm, arm, archive = image.read_file(current.ARM), ctx.arm, ctx.common
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = native.common_message_entries(image.read_file(current.COMMON), clean_arm)
    owner = sha256(arm[native.DIRECTORY_OFFSET:native.TABLE_OFFSET]).hexdigest()
    prior = native.owned_entries(archive, arm, owner)
    payloads = {key: b" " + words.encode("ascii") for key, (_, words, _, _, _) in DRAFTS.items()}
    patched, revised, slots = native.owned_deployment(archive, arm, prior, payloads)
    assert len(archive) == len(patched)
    assert {a.message_id for a, b in zip(prior, revised, strict=True) if a.text != b.text} == DRAFTS.keys()
    candidate = native.with_components(ctx, arm, patched)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    formatter, effective_source = renderer.formatter()
    layout = renderer.machine(arm)
    layout.mem_write(review.BASE, ctx.raw)
    records, pages = [], []
    for key, (table, words, expected, meaning, note) in DRAFTS.items():
        pos = table - review.BASE
        assert arm[pos:pos + 32] == clean_arm[pos:pos + 32] and unpack_from("<8i", arm, pos)[5] == key
        ja, en, draft = source[key], prior[key], revised[key]
        assert en.text.startswith(b" ") and draft.text.startswith(b" ")
        assert all(b"%" not in row.text for row in (ja, en, draft))
        checks = []
        for version, row, runtime in (("Current", en, ctx), ("Proposed", draft, candidate)):
            cpu, get, io = runtime.machine(arm, runtime.common, runtime.raw, runtime.plan)
            address = get(0x5528C, key)
            assert io.reads and bytes(cpu.mem_read(address, len(row.text) + 1)) == row.text + b"\0"
            body = row.text.decode("ascii").strip()
            formatted = formatter(layout, dict(message_id=key, english=body, source_voice_table=table,
                                               English_argument_source_indices=[]), ())
            lines = formatted["lines"]
            assert " ".join(lines) == body and all(lines)
            if version == "Proposed":
                assert tuple(lines) == expected and not formatted["findings"]
            raw = bytes.fromhex(formatted["formatted_hex"])
            plane = renderer.native_portrait(arm, kanji, raw, lines)
            pages.append((f"{key} {version}", plane))
            checks.append(formatted | dict(version=version, complete_glyph_mask_sha256=sha256(plane).hexdigest(), pages=1))

        def exact(row):
            return review.panels.text_reference(row) | {"exact_hex": row.text.hex()}

        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=current.COMMON, speaker="Julio Erneco",
            context="The Lisbon Guildmaster states the item price. An assigned Purser challenges the quote before the revised amount and settlement.",
            clean_Japanese=ja.text.decode("cp932"), english=words, source_meaning=meaning, localization_note=note,
            source_reference=exact(ja), current_reference=exact(en), installed_reference=exact(en), proposed_reference=exact(draft),
            decision="revision_proposed", native_layouts=checks, review=dict.fromkeys(GATES, True) | {"formatting": False}))
    WORK.mkdir(exist_ok=True)
    figures = native.portrait_sheets(WORK, pages)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE),
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=records, original_formatter_parent=0x02053DB8,
        native_formatter_source_sha256=sha256(effective_source.encode()).hexdigest(), proposed_COMMON_sha256=sha256(patched).hexdigest(),
        allocations=slots, native_previews=figures, all_placements_same_allocation=True, ordinary_gameplay=False,
        registered=False, new_editorial_credit=0))
    print("Verified four queued native pages and both in-place dialogue proposals.")


if __name__ == "__main__":
    main()
