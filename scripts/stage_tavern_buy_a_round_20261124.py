"""Localize the Tavern's round command and its three linked Help surfaces."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType

from PIL import Image, ImageDraw
from dk4tool.dialogue.help_source_links import readable_source, source_links
from dk4tool.formats.ilnk import IlnkContainer
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import register_cartridge_title_20261123 as registration
from scripts import register_stockholm_recruiting_20261124 as parent
from scripts import stage_palace_help_20261120 as help_pages
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = Path(".codex-release-work/tavern_buy_a_round_v2_20261124")
ROM, STORED, PLAN, PREVIEW = (ROOT / n for n in ("Tavern_Buy_A_Round_STAGED.nds", "stored_proof.json", "help_plan.json", "tavern_help_native.png"))
PATCH, REBUILT, PATCH_PROOF = (ROOT / n for n in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
ARM, COMMON, HELP = help_pages.ARM, parent.COMMON, help_pages.HELP
BASE, SLOT = 0x02000000, 0x143BA0
LABEL = "Buy a Round"
MENU = {
    0x118BA4: ("ORDER_DRINK", "飲み物をたのむ", "Order Drink", "Order Drink", "Order one drink and speak with the Tavern staff."),
    0x118BB4: ("BUY_A_ROUND", "みんなにおごる", "Treat Everyone", LABEL, "Pay for drinks for the room. 'Buy a Round' is the idiomatic Tavern command and matches Gerhard's recruiting advice."),
    0x118BC4: ("RECRUIT_CREW", "水夫を集める", "Recruit Crew", "Recruit Crew", "Recruit sailors for the fleet. The concise command is clear beside the drink options."),
    0x118BD4: ("SCHEMES", "策謀の立案", "Schemes", "Schemes", "Open the available schemes. The plural heading covers several distinct actions."),
}
ARTICLES = {
    12: ("Tavern", "Recruit sailors and gather news here. Many towns in Arab cultural regions have no tavern for religious "
         "reasons. Sailors are harder to find there, so think twice before starting a battle. See [[13|Order Drink,]] "
         "[[14|Buy a Round,]] [[15|Recruit Crew,]] and [[16|Schemes.]]",
         "Match the Tavern command in the index and retain the four links, religious context and warning about replacing sailors."),
    14: ("Buy a Round (Tavern)", "Buy a round for everyone in the Tavern. You'll hear news about nearby towns and other factions, and you may "
         "get a tip about an item. Buy a round before choosing [[15|Recruit Crew]] to improve turnout.",
         "Use the same caption as the menu. The explanation preserves the room, kinds of information and recruiting benefit with a shorter final instruction."),
    15: ("Recruit Crew (Tavern)", "Recruit sailors for your fleet. Towns with higher Growth offer more recruits at once, but the fee is higher. "
         "Any extra recruits are dismissed on the spot. Buy a round first to improve turnout. Then use [[139|Assign Sailors]] "
         "to place the new recruits on your ships.", "Keep the wording and the Assign Sailors link. Set 'Buy a round first' together on the page."),
}
HELP_GLOSSES = {
    11: "Choose a building sign to run its town command. City-only commands require a City. The original list includes other town functions and ruins.",
    12: "Recruit and gather information at the Tavern. Religious restrictions leave many towns in Arab cultural regions without one, so replacing sailors is harder and starting fights is risky.",
    13: "Order a drink for five to ten gold. Learn about nearby towns or other factions. Knowledgeable women in city taverns may know where an item is hidden.",
    14: "Buy drinks for the people at the Tavern. Learn about towns or factions and sometimes items. Buying drinks before recruiting improves turnout.",
    15: "Town development raises both turnout and costs. Release surplus sailors on the spot. Buying drinks helps recruit, and the assignment command distributes sailors to ships.",
    16: "A strategist's idea permits a scheme for 1,000 gold. Attempts can fail. A rival is required, and all schemes except Forge Papers require a visited town where a rival holds share.",
}
RETENTIONS = {
    11: "The parent Help page identifies the Tavern with the correct link and retains the City-only rule.",
    13: "The article distinguishes a single drink from buying drinks for the room and keeps the price and the item clue.",
    16: "The article matches the Schemes command and keeps its cost, limits and four links.",
}


def source_ref(arm, field):
    pointer, = unpack_from("<I", arm, field)
    offset = pointer - BASE
    assert 0 <= offset < len(arm) - 16
    end = arm.index(0, offset, offset + 17)
    return dict(file_path=ARM, pointer_field=field + BASE, address=pointer, component_offset=offset,
                exact_C_string_hex=arm[offset:end + 1].hex(), component_sha256=sha256(arm).hexdigest())


def edit_menu(clean, before):
    original_slot = b"Treat Everyone\0\0"
    assert before[SLOT:SLOT + 16] == original_slot
    encoded = LABEL.encode("ascii")
    assert len(encoded) * 6 <= 72 and len(encoded) < len(original_slot)
    target = before[:SLOT] + encoded.ljust(16, b"\0") + before[SLOT + 16:]
    rows = []
    for field, (id, japanese, english, revised, reason) in MENU.items():
        refs = [source_ref(arm, field) for arm in (clean, before, target)]
        assert [bytes.fromhex(r["exact_C_string_hex"])[:-1].decode(codec)
                for r, codec in zip(refs, ("cp932", "ascii", "ascii"), strict=True)] == [japanese, english, revised]
        assert refs[1]["address"] == refs[2]["address"]
        if id == "BUY_A_ROUND":
            assert refs[0]["address"] == refs[1]["address"] == BASE + SLOT
            address = pack("<I", BASE + SLOT)
            assert [i for i in range(0, len(before) - 3, 4) if before[i:i + 4] == address] == [field]
        rows.append(dict(id=f"TAVERN_MENU_{id}", file_path=ARM, speaker="Tavern menu", context="Tavern actions following the Barkeep's greeting.",
            english=revised, previous_English=english, source_Japanese=japanese, source_meaning=reason.split(". ", 1)[0],
            localization_note=reason, decision="revision" if english != revised else "retention", review=dict.fromkeys(GATES, True),
            source_reference=refs[0], current_reference=refs[1], registered_reference=refs[2]))
    assert len(before) == len(target)
    return target, rows


def compile_help(raw):
    blocks = {source: IlnkContainer.parse(data).blocks for source, data in raw.items()}
    assert len(blocks["clean"]) == len(blocks["canonical"]) == 202 and len(blocks["current"]) == 217
    rows = []
    for topic, gloss in HELP_GLOSSES.items():
        entries = {name: parsed[topic] for name, parsed in blocks.items()}
        links = [r["topic_id"] for r in source_links(entries["clean"])]
        assert links == [r["topic_id"] for r in source_links(entries["current"])]
        source = help_pages.reference(raw["clean"], entries["clean"], topic)
        current = help_pages.reference(raw["current"], entries["current"], topic)
        old = readable_source(entries["current"])
        revision = topic in ARTICLES
        row = dict(id=f"HELP_TOPIC_{topic}", topic_id=topic, file_path=HELP, speaker="Help system",
            context="Tavern commands, their Help links, and the connection between buying a round and recruiting.",
            source_Japanese=readable_source(entries["clean"]), source_meaning=gloss, previous_English=old,
            source_reference=source, current_reference=current, original_link_IDs=links, current_continuations=[],
            decision="revision" if revision else "retention", review=dict.fromkeys(GATES, True) | {"formatting": not revision},
            **{f"{name}_source_hex": entry.hex() for name, entry in entries.items()})
        if revision:
            title, body, reason = ARTICLES[topic]
            row.update(heading=title, english=body, localization_note=reason, semantic_sections=[body],
                       semantic_section_reason="Preserve the original single article and its forward links.")
        else:
            row.update(english=" ".join(old.split()), localization_note=RETENTIONS[topic])
        rows.append(row)

    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", file_path=HELP,
        records=[row for row in rows if row["decision"] == "revision"],
        **{f"source_{name}_HELP_sha256": sha256(data).hexdigest() for name, data in raw.items()})
    compiler = help_pages.compiler
    body = checked_text(compiler.SOURCE, {
        "topics!=(set(range(133,202))-{181,184})": f"topics!={set(ARTICLES)!r}",
        "Exact remaining67 Help articles": "Exact Tavern round Help articles",
    })
    scope = compiler.plan_articles.__globals__.copy()
    wrap = scope["wrap"]
    keep = [["Arab", "cultural", "regions"], ["Buy", "a", "round", "first"], ["Buying", "a", "round"], ["higher", "Growth"]]
    scope["wrap"] = FunctionType(wrap.__code__, wrap.__globals__ | {"PHRASES": [*wrap.__globals__["PHRASES"], *keep]})
    exec(compile(body, __file__ + "::qualified-tavern-help-compiler", "exec"), scope)
    target, plan = scope["plan_articles"](manuscript, *raw.values(), require_formatting=False)
    final = IlnkContainer.parse(target).blocks
    assert len(final) == len(blocks["current"]) and set(plan["owned_topic_ids"]) == set(ARTICLES)
    assert {n for n, (a, b) in enumerate(zip(blocks["current"], final, strict=True)) if a != b} == ARTICLES.keys()
    assert len(plan["pages"]) == len(ARTICLES)
    for row in rows:
        topic = row["topic_id"]
        assert row["original_link_IDs"] == [entry["topic_id"] for entry in source_links(final[topic])]
        row["registered_reference"] = help_pages.reference(target, final[topic], topic) | {"exact_block_hex": final[topic].hex()}
    return target, plan, rows


def stage():
    assert not ROOT.exists()
    release = read(parent.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] and digest(release["manifest"]) == release["manifest_sha256"]
    clean, canonical, image = map(NdsImage.open, (CLEAN, help_pages.CANONICAL, parent.ROM))
    before = parent.build.native.files(image)
    raw = dict(clean=clean.read_file(HELP), canonical=canonical.read_file(HELP), current=before[HELP])
    assert sha256(before[ARM]).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(raw["current"]).hexdigest() == release["target_HELP_sha256"]
    target, menu = edit_menu(clean.read_file(ARM), before[ARM])
    target_help, plan, articles = compile_help(raw)
    assert registration.right_bound(target, release["right_bound_configuration"])["matched_repair_spans"] == 8
    image.replace_file(ARM, target)
    image.replace_file(HELP, target_help)
    after = parent.build.native.files(image)
    assert before.keys() == after.keys() and {k for k in after if after[k] != before[k]} == {ARM, HELP}
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, before[ARM])
    image.replace_file(HELP, before[HELP])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()

    adapter = help_pages.renderer
    scope = adapter.original.verify.__globals__.copy()
    exec(compile(adapter.ADAPTER, __file__ + "::qualified-original-help-parser", "exec"), scope)
    sheet = Image.new("RGB", (768, 385 * len(ARTICLES)), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, page in enumerate(plan["pages"]):
        proof, picture = scope["verify"](target, page)
        topic = page["topic_id"]
        row, = [r for r in articles if r["topic_id"] == topic]
        row["native_page"] = proof
        row["review"]["formatting"] = True
        lines = page["visible_lines"]
        if topic == 15:
            assert any("Buy a round first" in line for line in lines), lines
        assert page["page_count"] == 1 and max(map(len, lines)) <= 42
        draw.text((8, 385 * index + 6), f"Native Help {topic}", fill="white")
        sheet.paste(picture.resize((756, 360), Image.Resampling.NEAREST), (6, 385 * index + 24))
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    assert parent.build.native.files(NdsImage.open(ROM)) == after
    sheet.save(PREVIEW)
    write(PLAN, plan)
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        exact_complete_parent_inverse=True, changed_components=[ARM, HELP], changed_help_topics=sorted(ARTICLES),
        changed_ARM9_slot=dict(offset=SLOT, length=16, prior_hex=before[ARM][SLOT:SLOT + 16].hex(), target_hex=target[SLOT:SLOT + 16].hex()),
        target_ARM9_sha256=sha256(target).hexdigest(), target_HELP_sha256=sha256(target_help).hexdigest(),
        records=menu+articles, help_plan=reference(PLAN), visual=reference(PREVIEW)))
    print(f"Staged the Tavern command and {len(ARTICLES)} verified native Help pages. {digest(ROM)}", flush=True)


def check(action):
    receipt = read(STORED)
    proof = dict(candidate=str(ROM), candidate_sha256=receipt["candidate"]["sha256"],
        predecessor_sha256=receipt["previous"]["sha256"], clean_input_sha256=receipt["clean"]["sha256"])
    scope = vars(checks) | dict(RELEASE=parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
            patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    stage() if action == "stage" else check(action)
