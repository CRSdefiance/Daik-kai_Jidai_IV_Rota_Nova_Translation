"""Review original town quests and stage only source-bound progressive dialogue changes."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import register_town_trend_exchanges_20261115 as parent
from scripts import stage_town_trend_exchanges_20261115 as native
from scripts.source_locked_derivation_v5118 import checked_text

base, layout = native.base, native.layout
ROOT = Path("work/town_quest_exchanges_20261115_v2")
ROM, STORED = ROOT / "Town_Quest_Exchanges_RESEARCH_ONLY.nds", ROOT / "staged.json"
MANUSCRIPT = native.MANUSCRIPT.with_name("town_quest_exchanges_20261115_v2.json")
BLOCKS = {
    "book": (209, 201, 197, 170),
    "prophecy": (225, 217, 213, 186),
    "sextant_request": (339, 320, 331, 299),
    "sextant_delivery": (340, 321, 332, 300),
}
CONTEXT = {
    "book": "An Alluring Woman offers Ian a book for 8,500 gold and calls him handsome. He asks the admiral to decide. On purchase, he buys the book but rebuffs her romantic teasing. A direct refusal ends the sale. If left to decide, he wishes he could pay but cannot; she gives him the book and later disappears. He dismisses his own speculation about her identity.",
    "prophecy": "An old man asks to see an unnamed object and recognizes the gold seal foretold by Kublai Khan. His family has awaited the ruler of the seas since their retainer ancestor received the emperor's instructions. The protagonist doubts the claim. The old man trusts his judgment and tells the crew where to look for the emperor's greatsword.",
    "sextant_request": "A village elder asks where the traveler came from. Reacting to the long voyage, he assumes the crew has a sextant. He has heard what it can do and offers a surprise in exchange. The traveler asks what the reward is; the elder tells them to bring the instrument.",
    "sextant_delivery": "After the crew brings the instrument, the elder acknowledges it and offers the promised exchange. The system confirms the handover without identifying the reward in this text.",
}
NOTES = {
    "book": (
        "Her quick call flatters Ian and draws him into the sale.",
        "He is surprised that she means him. The short reply leaves room for her pitch.",
        "She asks whether he'll buy the book for exactly 8,500 gold.",
        "Ian asks what it is before the offer goes to the admiral.",
        "She describes an Indian classic about love between a celestial maiden and a sage, then renews her sales pitch. The title is unspoken.",
        "Ian refers the decision to the admiral. Preserve the title explicitly present in the source.",
        "Ian accepts the purchase. This precedes the romantic exchange.",
        "She teases him with the possibility of finding love with a celestial maiden himself.",
        "Ian politely rebuffs her romantic suggestion after accepting the book.",
        "She treats his rebuff as a waste because she finds him handsome. Keep the playful disappointment.",
        "On direct refusal he politely declines the book.",
        "She accepts the refusal and plans to find another buyer.",
        "When the decision is left to Ian, he would like to buy it but personally lacks the money.",
        "She acknowledges this before Ian apologizes. Keep the pause brief.",
        "He apologizes for disappointing her. His courtesy motivates the next turn.",
        "She answers by giving him the book. Keep her spur-of-the-moment generosity.",
        "His abrupt surprise makes the gift feel unexpected.",
        "She laughs and wishes she could fall in love with someone like him next time. Keep the playful timing and the future wish.",
        "Ian stammers as he realizes she is gone.",
        "He wonders whether she was a celestial maiden, then dismisses his own speculation.",
        "The game confirms one point of Charm for Ian. Preserve the registered modal and numerical result.",
    ),
    "prophecy": (
        "He politely addresses a passerby without assigning a relationship.",
        "The protagonist acknowledges the address in their own voice.",
        "He asks to see something the protagonist carries, leaving it unnamed.",
        "The protagonist asks what he means, echoing the old man's gesture.",
        "He points out the same unnamed object. A short demonstrative fits the reply.",
        "He recognizes the object and confirms the legend aloud.",
        "The protagonist gives a brief puzzled reaction before the account begins.",
        "The story dates Kublai Khan's rule of the mainland to more than 300 years earlier.",
        "Even a great emperor eventually faces death. Keep the measured turn toward the last instructions.",
        "The emperor tells his retainer that the ruler of the oceans will arrive in two hundred years. The quotation continues in the next panel.",
        "The sea king commands many foreigners and carries a gold seal from territory outside the emperor's rule. The emperor orders his sword given to the hero.",
        "The speaker's family descends from that retainer and has waited for the sea king.",
        "The old man formally welcomes the long-awaited arrival in the present.",
        "The protagonist doubts the prophecy with their own degree of surprise, courtesy or bluntness.",
        "The companion openly doubts the identification. Retain Lil's runtime name token where Camille addresses her.",
        "The old man trusts his eyes and insists the protagonist is the awaited sea king.",
        "He directs the crew south of the Shandong Peninsula. The sword should be there.",
        "He entrusts the greatsword to the protagonist and takes his leave. The dialogue does not announce an immediate acquisition.",
    ),
    "sextant_request": (
        "The elder remarks that the face is unfamiliar and asks where the traveler comes from.",
        "Each captain names their own home. Preserve the geographic detail and route difference.",
        "The elder reacts to the unfamiliar or far-off home. Only Rafael's route mentions Portugal bringing guns.",
        "He infers the crew must own a sextant. Keep his conversational confirmation tag together.",
        "The captain's startled response leaves the elder to explain the rumor.",
        "He has heard that a sextant tells you where you are at sea even with no landmarks. The explanation remains hearsay.",
        "He asks them to part with the sextant and offers an unspecified reward.",
        "The captain echoes the offer with curiosity.",
        "The elder withholds the reward's identity until they bring the sextant.",
    ),
    "sextant_delivery": (
        "The elder recognizes they brought it and presents something in exchange.",
        "The game confirms that the player handed over the Sextant. Keep the item and direction of transfer.",
    ),
}

# Each key uses the source turn order. Actor-specific retorts remain route-specific.
BOOK = {
    (0, 2): ("Care to buy this book for 8,500 gold?", ("for 8,500 gold?",)),
    (1, 2): ("Care to buy this book for 8,500 gold?", ("for 8,500 gold?",)),
    (3, 2): ("Care to buy this book for 8,500 gold?", ("for 8,500 gold?",)),
    (0, 4): ("It's an Indian classic about a celestial maiden and a sage who fall in love. Interested?", ("an Indian classic", "a celestial maiden and a sage", "who fall in love.")),
    (1, 4): ("It's an Indian classic. A celestial maiden and a sage fall in love. Interested?", ("It's an Indian classic.", "A celestial maiden and a sage", "fall in love.")),
    (3, 4): ("It's an Indian classic about a celestial maiden and a sage who fall in love. What do you say?", ("an Indian classic", "a celestial maiden and a sage", "who fall in love.")),
    (3, 6): ("We'll take it.", ()),
    (0, 9): ("Oh, what a shame. A handsome man like you, too.", ("A handsome man like you, too.",)),
    (1, 9): ("Such a shame. A handsome man like you!", ("A handsome man like you!",)),
    (3, 9): ("Oh, what a shame. A handsome man like you!", ("A handsome man like you!",)),
    (0, 11): (None, ("someone else to buy it.",)),
    (1, 11): ("A shame. I'll find another buyer.", ("I'll find another buyer.",)),
    (3, 11): ("That's a shame. I'll find another buyer.", ("I'll find another buyer.",)),
    (0, 17): (None, ("Heh heh...", "a man like you.")),
    (1, 17): (None, ("Hee hee...", "a man like you.")),
    (3, 17): ("Hee hee... Next time, I'd like to fall for a man like you.", ("Hee hee...", "fall for a man like you.")),
    (0, 19): ("A celestial maiden? Heh... What am I thinking?", ("A celestial maiden?", "What am I thinking?")),
    (1, 19): ("A celestial maiden? Heh... What am I thinking?", ("A celestial maiden?", "What am I thinking?")),
    (3, 19): ("A celestial maiden? Heh... What am I thinking?", ("A celestial maiden?", "What am I thinking?")),
}
PROPHECY = {
    (0, 4): (None, ("That, right there.",)),
    (1, 4): ("That one.", ()),
    (3, 4): ("That one.", ()),
    (1, 6): ("?", ()),
    (0, 8): ("But even a great emperor must leave this world someday...", ("a great emperor", "this world someday...")),
    (3, 8): ("But even that great emperor's time came to an end...", ("that great emperor's", "came to an end...")),
    (0, 9): ('He told his retainer, "Two hundred years from now, the ruler of the oceans shall come here.', ("He told his retainer,", "Two hundred years from now,", "the ruler of the oceans")),
    (3, 9): ('He told his retainer, "Two hundred years from now, the ruler of the oceans shall come to this land.', ("He told his retainer,", "Two hundred years from now,", "the ruler of the oceans")),
    (0, 10): ('"The king of the seas shall command many foreigners and bear a gold seal from a land I could not rule. Give my sword to that hero."', ("shall command many foreigners", "bear a gold seal", "from a land I could not rule.", "Give my sword to that hero.")),
    (0, 11): (None, ("from that retainer.", "the king of the sea.")),
    (3, 11): ("Our ancestor was that retainer. We've awaited the Sea King...", ("Our ancestor was that retainer.", "We've awaited the Sea King...")),
    (0, 13): ("Me? Ruler of the seas?", ("Ruler of the seas?",)),
    (0, 14): ("Him? He's the one an emperor foretold 300 years ago? No way!", ("300 years ago?", "No way!")),
    (3, 13): ("Sir, you must be mistaken. I'm no ruler of the seas.", ("you must be mistaken.", "I'm no ruler of the seas.")),
    (0, 15): (None, ("the king of the sea.",)),
    (1, 15): ("No. I know what I see. You truly are the Sea King.", ("I know what I see.", "You truly are the Sea King.")),
    (3, 15): ("No. I know what I see. You truly are the Sea King.", ("I know what I see.", "You truly are the Sea King.")),
    (0, 16): ("The emperor's greatsword should be south of the Shandong Peninsula. Search there.", ("The emperor's greatsword", "south of the Shandong Peninsula.", "Search there.")),
    (1, 16): ("The emperor's greatsword should be south of the Shandong Peninsula. Search there.", ("The emperor's greatsword", "south of the Shandong Peninsula.", "Search there.")),
    (3, 16): ("The emperor's greatsword should be south of the Shandong Peninsula. Search there.", ("The emperor's greatsword", "south of the Shandong Peninsula.", "Search there.")),
}
PROPHECY[1, 10] = PROPHECY[3, 10] = PROPHECY[0, 10]
SEXTANT = {
    (0, 0): (None, ("Where are you from?",)),
    (2, 0): (None, ("Where have you come from?",)),
    (3, 0): (None, ("Where are you from?",)),
    (0, 2): (None, ("You've come a long way!",)),
    (0, 3): (None, ("a sextant, haven't you?",)),
    (1, 3): ("Ah, now I see. You've got one of those handy sextants, don't you?", ("sextants, don't you?",)),
    (2, 3): (None, ("a sextant, don't you?",)),
    (3, 3): (None, ("a sextant, don't you?",)),
    (0, 5): (None, ("out at sea,", "even with no landmarks.")),
    (1, 5): ("I've heard it can tell you where you are at sea, even with no landmarks. Something like that.", ("where you are at sea,", "even with no landmarks.", "Something like that.")),
    (2, 5): ("I've heard it can tell you where you are at sea, even with no landmarks. Something like that.", ("where you are at sea,", "even with no landmarks.", "Something like that.")),
    (3, 5): ("I hear it shows where you are at sea, even without landmarks.", ("at sea, even without landmarks.",)),
    (0, 6): ("Would you part with that sextant? I'll trade you something nice.", ("Would you part with that sextant?", "I'll trade you something nice.")),
    (1, 6): ("Could we have that sextant? I'll trade you something good.", ("Could we have that sextant?", "I'll trade you something good.")),
    (2, 6): ("Could we have that sextant? I'll trade you something good.", ("Could we have that sextant?", "I'll trade you something good.")),
    (3, 6): ("Could we have that sextant? I'll trade you something good.", ("Could we have that sextant?", "I'll trade you something good.")),
}
REVISIONS = {"book": BOOK, "prophecy": PROPHECY, "sextant_request": SEXTANT, "sextant_delivery": {
    (0, 0): (None, ("take this in exchange.",)),
    (1, 0): (None, ("take this in exchange.",)),
    (2, 0): (None, ("take this in exchange.",)),
    (3, 0): (None, ("take this in exchange.",)),
}}
CHOICE_REASONS = (
    "The admiral chooses to buy the book.",
    "The admiral declines the purchase.",
    "The admiral leaves the decision to Ian, which can lead to the gift exchange.",
)
PREVIOUS_LIL = {
    "book": "translations/lil_B197_contextual_final_review_v1.json",
    "prophecy": "translations/lil_B213_contextual_final_review_v1.json",
}
SPEAKERS = {0: "Rafael", 1: "Hodram", 2: "Lil", 3: "Maria", 5: "Claudio", 9: "Camille", 21: "Ian",
            161: "Elder", 169: "Alluring Woman", 170: "Old Man", 254: "System notice"}


def checked_choices(route, block, source, current):
    source, = [c for c in source if c["word"] == 0x2200]
    current, = [c for c in current if c["word"] == 0x2200]

    def labels(c):
        raw = bytes.fromhex(c["whole_command_hex"])
        # The engine indexes the three NUL-terminated strings from bytes 4, 6 and 8.
        offsets = (8, *(8 + k for k in unpack_from("<2H", raw, 4)))
        return [(c["offset"] + off, raw[off:raw.index(0, off)]) for off in offsets]

    rows = []
    for index, ((ja_offset, ja), (en_offset, en), meaning) in enumerate(
            zip(labels(source), labels(current), CHOICE_REASONS, strict=True)):
        assert en and en.isascii() and len(en) <= 14
        rows.append(dict(file_path=f"/data/SC{route}.DK4", block=block, option=index,
            source_offset=ja_offset, current_offset=en_offset, source_hex=ja.hex(), current_hex=en.hex(),
            Japanese=ja.decode("cp932"), english=en.decode("ascii"), decision="retention",
            context=CONTEXT["book"], source_meaning=meaning, localization_note=meaning,
            source_command=source, current_command=current))
    assert tuple(r["Japanese"] for r in rows) == ("買おう", "買わない", "任せる")
    return rows


def review_block(group, route, block, ja, old, stock_arm, arm, inventory):
    source_cmd, source = native.raw_speeches(stock_arm, ja, inventory)
    current_cmd, current = native.raw_speeches(arm, old, inventory)
    assert [r["word"] for r in source_cmd] == [r["word"] for r in current_cmd]
    refs = native.references(source_cmd, source), native.references(current_cmd, current)
    assert len(source) == len(current) == len(NOTES[group]) - (group == "prophecy" and route in (1, 3))
    rows = []
    for index, (left, right) in enumerate(zip(*refs, strict=True)):
        turn = index + int(group == "prophecy" and route in (1, 3) and index >= 14)
        j, e = [bytes.fromhex(r["raw_hex"]) for r in (left, right)]
        selector = j[0]
        assert selector == e[0] and left["complete_preamble_hex"] == right["complete_preamble_hex"]
        previous = " ".join(e[1:].decode("cp932").split())
        choice = REVISIONS[group].get((route, turn))
        revised, protected = choice or (None, ())
        marker = f"{{SPEAKER:{selector:02X}}}" if selector != 254 else "{SYSTEM}"
        note = NOTES[group][turn]
        row = dict(file_path=f"/data/SC{route}.DK4", block=block, route=route, group=group, turn=turn,
            id=f"DK4_MES_B{block}_R{left['record_index']:04d}", kind="system-FE" if selector == 254 else "progressive",
            speaker=SPEAKERS[selector], source_selector=selector, Japanese=j[1:].decode("cp932"),
            previous_English=previous, english=marker + (revised or previous), decision="retention",
            source_reference=left | dict(block_sha256=native.digest(ja)),
            current_reference=right | dict(block_sha256=native.digest(old)),
            source_hex=left["raw_hex"], current_hex=right["raw_hex"], source_meaning=note,
            localization_note=note, context=CONTEXT[group], review=dict.fromkeys(native.GATES, True))
        if route == 2 and group in PREVIOUS_LIL:
            row["earlier_context_review"] = PREVIOUS_LIL[group]
            assert not choice
        if choice:
            assert selector != 254
            for token in (b"FI", b"FA", b"FO", b"FU", b"%"):
                assert token not in j[1:] and token not in e[1:]
            norm = layout.prior.layout.norm
            pairs = [(norm(a), norm(b)) for phrase in protected for a, b in zip(phrase.split(), phrase.split()[1:])]
            try:
                plan = layout.plan_record(row | dict(protected_pairs=pairs))
                assert all(any(p.casefold() in line.casefold() for line in plan["lines"]) for p in protected)
                packet = bytes.fromhex(plan["encoded_hex"])
                assert packet[0] == selector and len(packet) <= len(e)
                row.update(target_hex=packet.ljust(len(e), b" ").hex(), automatic_layout=plan,
                           trailing_blank_bytes=len(e)-len(packet))
                layout.fit_storage_padding(row)
            except (AssertionError, ValueError) as error:
                raise ValueError((group, route, turn, len(e)-1, row["english"])) from error
            if row["target_hex"] != row["current_hex"]:
                row["decision"] = "revision"
        rows.append(row)
    choices = checked_choices(route, block, source_cmd, current_cmd) if group == "book" else []
    return rows, choices, current_cmd


def load_exchanges():
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(native.CLEAN)
    stock_arm = clean.read_file(native.ARM)
    inventory, _, _ = native.scoped_inventory()
    groups = {}
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        source, current = [native.IlnkContainer.parse(i.read_file(path)).blocks for i in (clean, ctx.image)]
        for group, route_blocks in BLOCKS.items():
            block = route_blocks[route]
            groups[route, block] = review_block(group, route, block, source[block], current[block],
                                                stock_arm, ctx.arm, inventory)
    return release, ctx, inventory, groups


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release, ctx, inventory, groups = load_exchanges()
    before = native.files(ctx.image)
    records = [r for rows, _, _ in groups.values() for r in rows]
    choices = [c for _, menus, _ in groups.values() for c in menus]
    assert len(records) == 198 and len(choices) == 12
    changed = dict(native.transform(ctx.image, records))
    config = base.load(parent.MANIFEST)["relocations"][native.ARM]["reviewed_name_integration"]["catalog"]
    paths = [f"/data/SC{r}.DK4" for r in range(4)]
    banks = lambda assets: [native.IlnkContainer.parse(assets[path]).blocks for path in paths]
    new = banks(before | changed)
    assert native.catalogue(ctx.arm, config, banks(before)) == native.catalogue(ctx.arm, config, new)
    for (route, block), (rows, _, current) in groups.items():
        parsed, texts = native.raw_speeches(ctx.arm, new[route][block], inventory)
        fields = ("offset", "word", "native_extent", "ancestor_0100_offsets")
        assert all(all(a[k] == b[k] for k in fields) for a, b in zip(current, parsed, strict=True))
        speech = [r["current_reference"] for r in rows if r["decision"] == "revision"]
        nested = {r["command_offset"] for r in speech}
        nested.update(at for r in speech for at in r["ancestors"])
        # The stored inverse verifies every byte of the enclosing conditional bodies.
        # Their parsed outer command bytes include the changed speech payloads.
        assert all(a["whole_command_hex"] == b["whole_command_hex"] for a, b in zip(current, parsed, strict=True)
                   if a["offset"] not in nested)
        for row, target in zip(rows, native.references(parsed, texts), strict=True):
            assert target["raw_hex"] == row.get("target_hex", row["current_hex"])
            assert target["complete_preamble_hex"] == row["current_reference"]["complete_preamble_hex"]
            row["staged_reference"] = target | dict(block_sha256=native.digest(new[route][block]))
    edited = [r for r in records if r["decision"] == "revision"]
    # Existing payloads are bound above. Re-run the complete native contract on
    # the new text, including the ASCII replacement for Hodram's wide question mark.
    validator = checked_text(getsource(layout.native_validation), {
        "('before', 'current_hex'), ('after', 'target_hex')": "('after', 'target_hex'),",
    })
    env = vars(layout).copy()
    exec(compile(validator, __file__ + "::revised-progressive-validation", "exec"), env)
    rendered = env["native_validation"](ctx, edited)
    previews = []
    for row in edited:
        pages = row["after_native"]["pages"]
        lines = [line for page in pages for line in native.visible_lines(page)]
        assert lines == row["automatic_layout"]["lines"], (row["id"], lines)
        for page in pages:
            previews.append((f"SC{row['route']} {row['id'].split('_B')[1]} {page['page']}/{len(pages)}",
                             bytes.fromhex(page["native_plane_hex"])))
    assert rendered and previews
    for path, payload in changed.items():
        ctx.image.replace_file(path, payload)
    after = native.files(ctx.image)
    assert {path for path in before if before[path] != after[path]} == changed.keys()
    ROOT.mkdir(parents=True)
    ctx.image.save(ROM)
    for path in changed:
        ctx.image.replace_file(path, before[path])
    assert bytes(ctx.image.rom.save()) == parent.ROM.read_bytes()
    sheets = FunctionType(layout.contact_sheets.__code__, vars(layout) | dict(ROOT=ROOT))(previews)
    candidate = base.digest(ROM)
    base.save(MANUSCRIPT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(native.GATES), candidate_sha256=candidate,
        previous_sha256=release["candidate_sha256"], records=records, retained_menu_options=choices))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release["candidate_sha256"],
        target_ARM9_sha256=native.digest(ctx.arm), target_story_archive_sha256={p: native.digest(x) for p, x in changed.items()},
        whole_parent_inverse=True, sheets=sheets, preview_count=len(previews), manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f"{len(edited)} changed records, {len(records)-len(edited)} retentions, {len(choices)} menu retentions, {len(previews)} native pages.")


if __name__ == "__main__":
    main()
