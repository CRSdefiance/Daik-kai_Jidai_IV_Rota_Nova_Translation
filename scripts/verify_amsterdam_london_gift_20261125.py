"""Verify the ordinary Rainbow Marbles purchase, voyage and both Tavern choices."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts.aggregate_barmaid_gameplay_v780 import actual_state
from scripts import verify_amsterdam_hodram_arrival_20261125 as story
from scripts.verify_market_gameplay_v753 import state
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


play, panels = story.play, story.panels
OUT = story.OUT.with_name("amsterdam_london_gift_current_20261125.json")
ITEM_NAMES = Path("translations/all_item_names_arm9_v1.json")
TAVERN = "London Tavern. On the first paid second drink Marie meets Hodram. With the gift in inventory she notices it on the next two visits. Hodram declines her first request and agrees the second time."
GUILD = "Amsterdam Guild. The Guildmaster gives his stock pitches, asks which item to buy and quotes the selected price before the handoff."
VOYAGE = "Ordinary voyage between London and Amsterdam. Auto Move declines both routes. The fleet reaches each port by manual sailing and resupplies in Amsterdam."
CASES = {
    644: (((5750, ()), (36750, ())), "Manuel Almeida", ("There isn't a route to that port.",), VOYAGE,
          "No sailing route connects the selected port.", "The plain refusal explains why Auto Move returns to the route menu."),
    1290: (((10800, ()),), "Gerhard Adernkatz", ("Admiral, port in sight!",), VOYAGE,
           "Gerhard calls the admiral's attention to a visible town.", "The brisk lookout call precedes the discovery without naming the port early."),
    70: (((11300, ("Amsterdam",)), (45710, ("London",))), "Manuel Almeida", ("Shall we stop at %s?",), VOYAGE,
         "Manuel asks whether to call at the named port.", "The courteous question fits Manuel and displays both port substitutions in full before Yes or No."),
    49: (((34100, ("256",)),), "Port Worker", ("Want to resupply for %s gold?",), VOYAGE,
         "The port worker asks whether to resupply for the quoted sum.", "The direct question sounds like the worker and matches the settled 256-gold charge."),
    608: (((42770, ("water",)), (43020, ("food",))), "Manuel Almeida", ("We've run out of %s!",), VOYAGE,
          "The named supply is exhausted.", "The urgent one-line warning preserves the two distinct resources and their observed sequence."),
    609: (((44290, ()),), "Sailor", ("Ugh... My head's spinning...", "I'm so hungry... I can't go on..."), VOYAGE,
          "The sailor is dizzy and hungry and says he cannot go on.", "The halting phrases keep the sailor's worsening condition in his own voice."),
    62: (((22850, ()),), "Guildmaster", ("Need something?",), GUILD,
         "The Guildmaster asks what the visitor needs.", "The short welcome invites Hodram to say what he came for before the Buy and Sell menu."),
    3661: (((23750, ()),), "Guildmaster", ("It's a crimson crystal. Hold it up", "to the light. The story goes you'll", "see a star pattern inside."), GUILD,
           "The Guildmaster describes a crimson crystal. Looking through it is said to reveal a star-shaped pattern.",
           "The color and hearsay work. The display separates the instruction from 'to the light' and breaks 'you'll see'. Keep the viewpoint explicit in the reflow."),
    1071: (((24050, ()), (25250, ())), "Guildmaster", ("Which one would you like?",), GUILD,
           "The Guildmaster asks which of the wares the player wants.", "The question hands the choice to the player and makes sense again after the purchase."),
    1073: (((24650, ("1500",)),), "Guildmaster", ("Want to buy it for %s coins?",), GUILD,
           "The Guildmaster states the selected item's price and asks whether to buy it.", "The full amount and question fit together and precede the separate Yes or No."),
    1074: (((24950, ()),), "Guildmaster", ("Thanks for your business!",), GUILD,
           "The Guildmaster thanks the customer for the sale.", "The familiar closing line marks the purchase before the stock list changes."),
    827: (((49010, ("Hodram",)),), "Marie", ("%s, huh? Cheers! Glad we met.",), TAVERN,
          "Marie repeats the visitor's name and toasts their acquaintance.", "The casual repetition and toast keep the first meeting distinct from the later gift."),
    829: (((51410, ()), (55310, ())), "Marie", ("Oh, what's that?",), TAVERN,
          "Marie notices the object and asks what it is.", "One quick question carries the surprise and gives Hodram the floor."),
    831: (((51710, ("Rainbow Marbles",)), (55610, ("Rainbow Marbles",))), "Hodram Bergstrom", ("It's called %s.",), TAVERN,
          "Hodram names the object Marie has noticed.", "His plain answer keeps the complete object name and leads into her compliment."),
    834: (((52010, ()), (55910, ())), "Marie", ("How lovely!",), TAVERN,
          "Marie says the object is lovely.", "The brief admiration belongs between learning its name and Hodram's next question."),
    836: (((52310, ()), (56210, ())), "Hodram Bergstrom", ("Do you like it?",), TAVERN,
          "Hodram asks whether Marie likes the object.", "The question gives her room to ask about the gift without promising it."),
    839: (((52610, ()), (56510, ())), "Marie", ("Could this be for me?",), TAVERN,
          "Marie tentatively asks if Hodram intends it for her.", "The tentative question leaves both choices open and appears before ownership changes."),
    841: (((52910, ()),), "Marie", ("I see... I'm sorry. That was", "selfish of me."), TAVERN,
          "Marie absorbs the refusal and apologizes for having been selfish.", "The pause and self-directed apology preserve her disappointment while leaving the player free to return."),
    840: (((56810, ()),), "Marie", ("Really? I'm so happy! Thank you.", "I'll treasure it!"), TAVERN,
          "Marie is delighted, thanks Hodram and promises to treasure the gift.", "The response builds from disbelief to gratitude. Her promise occupies its own line before the transfer."),
}


def snapshots(report, arm):
    frames = {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
    expected = {
        24350: (40659, 0, 4, 0), 24950: (40659, 0, 4, 0),
        25250: (39159, 0, 0, 4), 34450: (38903, 0, 0, 4), 46010: (38903, 0, 0, 4),
        49310: (38888, 1, 0, 4), 52610: (38873, 1, 0, 4), 52910: (38873, 1, 0, 4),
        53210: (38873, 1, 0, 4), 56510: (38858, 1, 0, 4), 56810: (38858, 1, 0, 4),
        57110: (38858, 2, 6, 0), 57410: (38858, 2, 6, 0),
    }
    result = []
    for frame, target in expected.items():
        saved = frames[frame]
        raw = Path(saved["path"]).read_bytes()
        assert saved["read_only_export"] and saved["bytes"] == len(raw) == 0x400000
        assert sha256(raw).hexdigest() == saved["sha256"]
        wallet, marie = state(arm, raw)["cash"], actual_state(arm, raw, 0)
        actual = (wallet, marie["original_relationship_stage"], marie["original_gift_owner_kind"], marie["gift_availability_mask"])
        assert actual == target and marie["actor_ID"] == 187 and marie["gift_item_ID"] == 128
        assert marie["original_gift_owner_detail"] == (2 if actual[2] == 4 else 0)
        result.append(dict(frame=frame, funds=wallet, gift=marie, read_only_RAM=saved))
    return result


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(active.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    capture = FunctionType(panels.capture.__code__, vars(panels) | {"observed": SimpleNamespace(ROOT=play.ROOT.parent)})
    shots, calls, evidence = capture(play.ROOT.name, release)
    report = read(evidence["capture"]["path"])
    assert max(shots) == report["frames"] == 57410
    assert evidence["donor"]["sha256"] == read(play.london.HISTORY)["battery_save_preloaded"]["source_sha256"]
    image, source = map(NdsImage.open, (active.ROM, CLEAN))
    arm, ja_arm = (i.read_file(active.ARM) for i in (image, source))
    current = panels.common_rows(image.read_file(active.COMMON), arm)
    clean = common_message_entries(source.read_file(active.COMMON), ja_arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {frame: panels.picture(shot) for frame, shot in shots.items()}
    records, figures = [], []
    for key, (holds, speaker, templates, context, meaning, note) in CASES.items():
        src, en = clean[key], current[key]
        evidence_rows, substitutions = [], []
        for frame, args in holds:
            lines = tuple((line % args) if "%" in line else line for line in templates)
            assert src.text.count(b"%s") == en.text.count(b"%s") == len(args)
            assert (en.text % tuple(arg.encode("ascii") for arg in args)).decode("ascii").split() == " ".join(lines).split()
            first = max((row for row in calls if row["message_ID"] == key and row["PC"] == 0x0205528C
                         and 0 < frame - row["frame"] < 600), key=lambda row: row["frame"])
            second, = [row for row in calls if row == first | {"PC": 0x020534F4}]
            evidence_rows.append(dict(capture=shots[frame], lines=lines,
                body_ink=panels.exact_body(font, lines, screens[frame]),
                nameplate=panels.nameplate(font, speaker, screens[frame]), requests=[first, second]))
            substitutions.append(args)
        ref = panels.text_reference(en) | dict(exact_hex=en.text.hex())
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=active.COMMON, context=context,
            speaker=speaker, source_meaning=meaning, clean_Japanese=src.text.decode("cp932"),
            english=" ".join(en.text.decode("ascii").split()), localization_note=note, arguments=substitutions,
            source_reference=panels.text_reference(src) | dict(exact_hex=src.text.hex()), current_reference=ref,
            installed_reference=ref, observations=evidence_rows, decision="wrap revision needed" if key == 3661 else "retention",
            review=dict.fromkeys(GATES, True) | {"formatting": key != 3661}))
        figures.append((f"COMMON {key} / {holds[0][0]}", screens[holds[0][0]]))
    choices = {frame: [panels.find_mask(font, label, screens[frame], box) for label, box in
        (("No", (126, 359, 172, 377)), ("Yes", (196, 359, 237, 377)))] for frame in (11300, 24650, 34100, 45710, 52610, 56510)}
    town = panels.find_mask(font, "London", screens[57410], (48, 10, 121, 34))
    assert town and all(all(v) for v in choices.values())
    item_name, = [r for r in read(ITEM_NAMES)["records"] if r["id"] == "DK4_ITEM_POINTER_128"]
    assert item_name["english"] == "Rainbow Marbles"
    description = current[2943]
    catalogue = dict(item_ID=128, item_name="Rainbow Marbles", quoted_gold=1500, capture=shots[24350],
        description_common_ID=2943, source_Japanese=clean[2943].text.decode("cp932"), english=description.text.decode("ascii"),
        source_reference=panels.text_reference(clean[2943]), installed_reference=panels.text_reference(description),
        name_record=item_name, item_names_reference=reference(ITEM_NAMES))
    assert any(r["message_ID"] == 2943 and 0 < 24350 - r["frame"] < 300 for r in calls)
    story_review = [read(path) for path in (story.OUT, story.APOLOGY_OUT)]
    for packet in story_review:
        assert packet["candidate_sha256"] == release["candidate_sha256"]
        for row in packet["records"]:
            shot = row["capture"]
            assert all(shot[key] == shots[shot["frame"]][key] for key in ("path", "PNG_sha256"))
    stages = snapshots(report, arm)
    shelves = [(24350, "Rainbow Marbles in Guild stock"), (25550, "Stock after purchase"), (57410, "London town after the gift")]
    figures.extend((f"{frame} / {text}", screens[frame]) for frame, text in shelves)
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        records=records, current_release=reference(active.RELEASE), evidence=evidence, item=catalogue,
        ownership_and_wallets=stages, ordinary_return_to_London=town, choice_glyphs=choices, all_common_requests=calls,
        story_reviews=[reference(story.OUT), reference(story.APOLOGY_OUT)],
        paired_story_holds=sum(packet["held_panels"] for packet in story_review),
        new_editorial_credit=0, ROM_changed=False)
    validate_natural_dialogue_batch(batch | {"records": [r for r in records if r["decision"] == "retention"]})
    write(OUT, batch | dict(sheets=panels.sheets_for("amsterdam_london_gift_20261125", figures)))
    print("Verified the purchase, both gift choices, delayed transfer and ordinary return to London.")


if __name__ == "__main__":
    main()
