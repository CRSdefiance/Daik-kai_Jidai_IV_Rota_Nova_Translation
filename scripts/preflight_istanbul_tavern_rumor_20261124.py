"""Qualify the Tavern rumor and its shared Indian Ocean argument against the current release."""

from collections import Counter
from pathlib import Path
from struct import pack, unpack
from textwrap import wrap
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.tavern_continuation_runtime import BASE, INDIAN, REGION, REGION_TABLE
from scripts import observe_istanbul_facilities_20261124 as play
from scripts import stage_london_guild_display_20261124 as guild
from scripts import verify_athens_valencia_town_20261123 as athens
from scripts.compare_london_relic_wraps_20261123 import RegisteredRuntime, original_machine, providers
from scripts.probe_tavern_conversations_v764 import format_case
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write


ARM, COMMON = guild.ARM, guild.COMMON
PANELS, TOWN = athens.panels, athens.town
FOLDER = PANELS.OUT.parent
OUT = FOLDER / "istanbul_tavern_rumor_preflight_20261124.json"
SHEETS = OUT.with_suffix("")
RELEASE = play.active.RELEASE
KEY, REPORT, HOLD, END = 870, 863, 9600, 10400
TIP = "%s, a tip about a rare treasure. They say %s is stashed in %s."
PITCH = "You're in luck! I have an old map said to lead to legendary treasure."
REGIONS = ("the North Sea", "the Mediterranean", "Africa", "the Indian Ocean",
           "Southeast Asia", "East Asia", "the New World")
ACTUAL = ("Sir", "Black Rapier", REGIONS[1])
PINK = ("Ma'am", "Pink Apron", REGIONS[5])
HOLDS = (
    (4000, 51, "Barkeep", (), ("Welcome! What will you have?",),
     "The barkeep welcomes the customer and asks what they want.", "The brisk greeting makes room for the order menu."),
    (4800, 53, "Barkeep", (), ("5 coins.",),
     "The barkeep quotes five gold coins.", "The concise reply matches the amount charged for the first drink."),
    (5200, 821, "Barkeep", ("Hayreddin", "Alexandria", "pirate"),
     ("Hayreddin from Alexandria is", "a pirate with real pull here."),
     "The barkeep names a pirate from Alexandria who has influence in the area.",
     "Real pull conveys local clout in the barkeep's informal voice, with all three names and roles intact."),
    (5600, 55, "Barkeep", ("Faticia",), ("Hey, Faticia! We've got a customer!",),
     "The barkeep calls the hostess over to a customer.", "The familiar call preserves Faticia's name and introduces her next turn."),
    (6000, 56, "Faticia", (), ("On it!",),
     "Faticia answers that she heard and is coming.", "The quick acknowledgment answers the barkeep before the offer."),
    (6400, 59, "Faticia", (), ("How about one more drink?",),
     "Faticia invites the customer to have another drink.", "The friendly question works with the original Yes and No choices."),
    (6800, 826, "Faticia", (), ("Oh, can't handle another drink?",),
     "Faticia expresses teasing surprise at being turned down.", "The one-line tease fits the drinking joke without adding a character trait."),
    (8000, 852, "Charles Rochefort", ("314",), ("It looks like it'll cost 314 gold.", "Is that all right?"),
     "Charles estimates the charge and politely asks for approval.",
     "His measured question follows a complete price line and preserves his deferential voice."),
    (8400, 865, "Hodram Bergstrom", (), ("Drinks for everyone!",),
     "Hodram orders drinks for everyone in the Tavern.", "His short, direct announcement invites the barkeep to address the room."),
    (8800, 872, "Barkeep", ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",),
     "The barkeep says who bought the round and tells everyone to enjoy it.",
     "The spoken toast keeps the original payer, using the verified English surname binding."),
    (9200, 874, "Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
     "A patron reacts with surprise, thanks Hodram, and praises his generosity.",
     "The excited first line and informal compliment motivate the tip that follows."),
    (HOLD, KEY, "Patron", ACTUAL, ("Sir, here's a tip. They say a rare", "treasure called Black Rapier is", "hidden in the Mediterranean."),
     "The patron offers a useful tip. Rumor has it the named rare treasure is hidden in the named region.",
     "Stashed keeps the patron's casual voice and the sense that the treasure was hidden. They say keeps the reported location uncertain. The tip and item name stay together."),
)


def exact_entry(row):
    return PANELS.text_reference(row) | dict(exact_hex=row.text.hex())


def ordinary(source, before, installed, release, font):
    capture = FunctionType(PANELS.capture.__code__, vars(PANELS) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent)))
    frames, calls, evidence = capture(play.ROOT.name, release)
    assert max(frames) == END and len(calls) == 2 * len(HOLDS)
    assert {284, 318, 750, 751, 752}.isdisjoint(x["message_ID"] for x in calls)
    screens = {frame: PANELS.picture(shot) for frame, shot in frames.items()}
    records = []
    for (frame, key, speaker, args, lines, meaning, reason), (got, copied) in zip(HOLDS, zip(calls[::2], calls[1::2], strict=True), strict=True):
        assert got["message_ID"] == key and got["PC"] == 0x0205528C and copied == got | {"PC": 0x020534F4}
        assert 0 < frame - got["frame"] < 400
        jp, old, new = source[key], before[key], installed[key]
        assert jp.text.count(b"%s") == len(args) + (key == 872)
        assert old.text.count(b"%s") == new.text.count(b"%s") == len(args)
        expanded = old.text.decode("ascii") % args
        assert expanded.split() == " ".join(lines).split()
        contextual = ("Hodram orders a drink, receives the Barkeep's rumor and declines Faticia's offer. "
                      "He buys a round, then the patron thanks him and offers a tip.")
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker=speaker, context=contextual,
            clean_Japanese=jp.text.decode("cp932"), english=new.text.decode("ascii").strip(), source_meaning=meaning,
            localization_note=reason, decision="revision" if key == KEY else "retention", review=dict.fromkeys(GATES, True),
            source_reference=exact_entry(jp), current_reference=exact_entry(old), proposed_reference=exact_entry(new),
            hold=dict(frame=frame, capture=frames[frame], lines=list(lines), arguments=args, requests=[got, copied],
                      native_body_pixels=PANELS.exact_body(font, lines, screens[frame]),
                      nameplate=PANELS.nameplate(font, speaker, screens[frame]))))
    wallet = {frame: PANELS.find_mask(font, total, screens[frame], (55, 348, 139, 366))
              for frame, total in ((3200, "8371"), (7200, "8366"), (10000, "8052"))}
    assert 8371 - 5 == 8366 and 8366 - 314 == 8052
    return_to_town = PANELS.find_mask(font, "Istanbul", screens[END], (16, 13, 133, 32))
    return records, dict(evidence=evidence, requests=calls, wallet=wallet, return_to_town=return_to_town,
                         ordinary_gameplay=True, unvisited=["Indian Ocean rumors in ordinary play",
                                                            "Other Tavern item draws", "Handheld display"])


def proposed_arm(clean_arm, arm):
    start = guild.PITCH
    end = start + guild.SIZE
    previous = arm[start:end]
    previous_text, _, previous_tail = previous.partition(b"\0")
    assert " ".join(previous_text.decode("ascii").split()) == guild.PITCH_ENGLISH
    assert not any(previous_tail)
    assert clean_arm[start:end].split(b"\0")[0].decode("cp932") == read(guild.PITCH_PRIOR)["original_preamble_Japanese"]
    assert arm[0x5C458:0x5C45C] == pack("<I", BASE + start)
    assert arm[0x5C1BC:0x5C1C0] == assemble(f"bl {guild.PITCH_WRAPPER}", 0x0205C1BC)
    lines = wrap(PITCH, width=35, break_long_words=False, break_on_hyphens=False)
    pitch = "\n ".join(lines).encode("ascii")
    region = REGIONS[3].encode("ascii") + b"\0"
    allocation = pitch + b"\0" + region
    assert len(lines) == 2 and len(allocation) == guild.SIZE
    pointer = REGION_TABLE - BASE + 12
    relocated = BASE + start + len(pitch) + 1
    assert arm[pointer:pointer + 4] == pack("<I", INDIAN)
    assert arm[INDIAN - BASE:].split(b"\0")[0] == b"reasure."
    for site in (0x020582BC, 0x02059968):
        assert arm[site - BASE:site - BASE + 4] == assemble(f"bl {REGION}", site)
    entries = ((start, allocation), (pointer, pack("<I", relocated)))
    new = bytearray(arm)
    edits = []
    for address, data in entries:
        old = arm[address:address + len(data)]
        assert old != data
        new[address:address + len(data)] = data
        edits.append(dict(offset=address, previous_hex=old.hex(), installed_hex=data.hex()))
    return bytes(new), edits, pitch, lines, relocated


def regional_cases(ctx, arm, proposed, original, second, pitch, pitch_lines, edits):
    exact, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    revised, rget, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    sweep, _, _ = original_machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    for row in edits:
        at = row["offset"]
        old, new = (bytes.fromhex(row[key]) for key in ("previous_hex", "installed_hex"))
        assert ctx.raw[at:at + len(old)] == old
        assert arm[at:at + len(new)] == new
        for cpu in (revised, sweep):
            assert bytes(cpu.mem_read(BASE + at, len(old))) == old
            cpu.mem_write(BASE + at, new)

    def string(cpu, address):
        return bytes(cpu.mem_read(address, 64)).partition(b"\0")[0].decode("ascii")

    def terms(cpu, call):
        strings = []
        for key in range(7):
            obj = call(REGION - BASE, key)
            assert obj == REGION_TABLE + 4 * key
            pointer, = unpack("<I", bytes(cpu.mem_read(obj, 4)))
            strings.append(string(cpu, pointer))
        return strings

    before_regions = terms(exact, get)
    after_regions = terms(revised, rget)
    assert before_regions == [*REGIONS[:3], "reasure.", *REGIONS[4:]]
    assert after_regions == list(REGIONS)
    items, _ = providers(exact, get)
    root = get(0xCB190)
    members = [(row["name"], get(0x4A3F0, root + 4 + 20 * row["index"])) for row in items]
    assert len(members) == 218 and {region for _, region in members} == {*range(7), 8}
    domain = [(gender, name, after_regions[index]) for name, index in members if index < 7 for gender in ("Sir", "Ma'am")]
    assert ACTUAL in domain and PINK in domain

    def layout(cpu, key, template, args):
        assert template[:1] == b" " and template.count(b"%s") == len(args)
        found = format_case(cpu, dict(message_id=key, english=template[1:].decode("ascii")), [arg.encode("ascii") for arg in args])
        assert "four_row_width_bound" not in found["findings"] and all(found["lines"])
        return found

    counts = Counter()
    cases = []
    for args in domain:
        _, title, region = args
        old = layout(sweep, KEY, original, args)
        new = layout(sweep, KEY, proposed, args)
        counts["previous_split_item_names"] += not any(title in line for line in old["lines"])
        counts["revised_split_item_names"] += not any(title in line for line in new["lines"])
        counts["previous_split_rare_treasure"] += not any("rare treasure" in line for line in old["lines"])
        counts["revised_split_rare_treasure"] += not any("rare treasure" in line for line in new["lines"])
        counts["revised_split_region_names"] += not any(region in line for line in new["lines"])
        counts["revised_weak_line_ends"] += "weak_line_end" in new["findings"]
        counts["revised_short_final_rows"] += "short_final_row" in new["findings"]
        if args[0] == "Sir":
            layout(sweep, REPORT, second, (title, region))
        cases.append(dict(arguments=args, previous=old, proposed=new))
    assert not any(value for key, value in counts.items() if key.startswith("revised_")), counts
    layout_pitch = guild.layout_function()(revised, pitch, guild.PITCH_ID, ())
    assert layout_pitch["lines"] == pitch_lines and not layout_pitch["findings"]

    raster, _, _ = TOWN.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    show = [(f"{KEY} current / {ACTUAL[1]}", layout(exact, KEY, original, ACTUAL)),
            (f"{KEY} proposed / {ACTUAL[1]}", layout(revised, KEY, proposed, ACTUAL)),
            (f"{KEY} proposed / {PINK[1]}", layout(revised, KEY, proposed, PINK))]
    for region in (REGIONS[3], REGIONS[-1]):
        boundary = max((args for args in domain if args[2] == region), key=lambda args: sum(map(len, args)))
        show += [(f"{KEY} proposed / {boundary[1]}", layout(revised, KEY, proposed, boundary)),
                 (f"{REPORT} corrected region / {boundary[1]}", layout(revised, REPORT, second, boundary[1:]))]
    show.append(("Guild map pitch / proposed", layout_pitch))
    figures = []
    for title, row in show:
        raw = bytes.fromhex(row["formatted_hex"])
        plane, glyphs = TOWN.render_portrait(raster, arm, kanji, raw)
        assert [glyph["code"] for glyph in glyphs] == TOWN.glyph_codes(raw)
        assert all(0 <= glyph["x"] < 228 and 0 <= glyph["y"] < 64 for glyph in glyphs)
        figures.append((title, plane))
    return dict(previous=before_regions, proposed=after_regions, item_count=len(members), tested_cases=len(cases),
                other_rumor_region_cases=len(cases) // 2, exact_cases=cases, counts=dict(counts),
                pitch_layout=layout_pitch, samples=show), figures


def main():
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    ctx = RegisteredRuntime(RELEASE, release["own_registered_startup"], captain=3)
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = guild.common_message_entries(clean.read_file(COMMON), clean_arm)
    del clean
    before = athens.common_rows(ctx.common, ctx.arm)
    arm, edits, pitch, lines, relocated = proposed_arm(clean_arm, ctx.arm)
    assert guild.play.active.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    previous = before[KEY].text
    assert previous == b" %s, here's a tip. They say a rare treasure called %s is hidden in %s."
    proposal = (b" " + TIP.encode("ascii")).ljust(len(previous), b" ")
    assert len(proposal) == len(previous) and proposal.count(b"%s") == previous.count(b"%s") == 3
    assert b"\n" not in proposal and b"\0" not in proposal
    common, installed, allocation = guild.owned_deployment(ctx.common, arm, before, {KEY: proposal})
    assert [new.message_id for old, new in zip(before, installed, strict=True) if old != new] == [KEY]
    records, gameplay = ordinary(source, before, installed, release, GameAsciiFont.from_arm9(ctx.arm))
    native, figures = regional_cases(ctx, arm, proposal, previous, before[REPORT].text, pitch, lines, edits)
    native_before = native["samples"][0][1]["lines"]
    assert native_before == list(HOLDS[-1][4])
    pitch_source = clean_arm[guild.PITCH:guild.PITCH + guild.SIZE].split(b"\0")[0]
    pitch_previous = ctx.arm[guild.PITCH:guild.PITCH + guild.SIZE].split(b"\0")[0]
    records.append(dict(id="ARM9_GUILD_TREASURE_PITCH", file_path=ARM, speaker="Guildmaster", english=PITCH,
        clean_Japanese=pitch_source.decode("cp932"), previous_English=guild.PITCH_ENGLISH,
        context="The Guildmaster offers Hodram an old map rumored to lead to legendary treasure.",
        source_meaning="The Guildmaster calls the player lucky, says he has an old map, and describes its reputed lead.",
        localization_note="I have fits the Guildmaster's sales pitch and preserves the existing map, possession and hearsay. Its two rows leave a complete independent string for the restored Tavern region.",
        source_reference=dict(offset=guild.PITCH, exact_hex=pitch_source.hex()),
        current_reference=dict(offset=guild.PITCH, exact_hex=pitch_previous.hex()),
        proposed_reference=dict(offset=guild.PITCH, exact_hex=pitch.hex()), decision="revision", review=dict.fromkeys(GATES, True)))
    SHEETS.mkdir(exist_ok=True)
    output = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=records, candidate_sha256=release["candidate_sha256"],
        source_sha256=release["clean_input_sha256"], current_ARM9_sha256=sha256(ctx.arm).hexdigest(),
        proposed_ARM9_sha256=sha256(arm).hexdigest(), proposed_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation[KEY], exact_ARM9_edits=edits,
        region_provider=dict(relocated_address=relocated, previous_address=INDIAN, position=3,
                             original_caller_sites=[0x020582BC, 0x02059968], exact_ui_names_unchanged=True),
        native=native, ordinary_gameplay=gameplay, proposed_sheets=TOWN.portrait_sheets(SHEETS, figures),
        current_ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(output)
    write(OUT, output)
    print(f"Checked {len(HOLDS)} ordinary Tavern holds, {native['tested_cases']} tip layouts, "
          f"and all seven private region labels. Proposed source-bound COMMON and ARM9 edits.", flush=True)


if __name__ == "__main__":
    main()
