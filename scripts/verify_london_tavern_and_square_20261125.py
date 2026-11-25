"""Bind ordinary London Tavern and Square exchanges to clean and installed text."""

from inspect import getsource
from types import SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_london_tavern_gift_20261125 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, write


OUT = panels.OUT.with_name("london_tavern_and_square_current_20261125.json")
END = 14600
TAVERN = "London Tavern. Hodram buys a drink, declines the follow-up drink and tests both answers to the price for a round."
SQUARE = "London Square. Food, Spice, Gem and Textile Shop visits draw independent lines from the same shopkeeper."
HOLDS = {
    51: ((4250,), "Barkeep", (), ("Welcome! What will you have?",),
         "The barkeep greets the captain and asks what he wants.", "The familiar welcome leads directly to the order menu."),
    53: ((5100,), "Barkeep", (), ("5 coins.",),
         "The barkeep quotes five gold coins.", "The brief quote sounds like the same barkeep and matches the actual payment."),
    823: ((5350,), "Barkeep", ("Bristol",), ("Have you heard of a nearby town", "called Bristol?"),
         "The barkeep asks if Hodram knows a town named Bristol and mentions it is nearby.",
         "The complete question stays conversational and the town name and question mark appear together."),
    55: ((5600,), "Barkeep", ("Marie",), ("Hey, Marie! We've got a customer!",),
         "The barkeep calls Marie by name and tells her she has a customer.",
         "His call carries the energy of the next exchange while binding the same name that appears over her portrait."),
    56: ((5850,), "Marie", (), ("On it!",),
         "Marie answers the barkeep immediately.", "The quick reply answers the call before Marie addresses Hodram."),
    59: ((6100,), "Marie", (), ("How about one more drink?",),
         "Marie offers Hodram another drink.", "The friendly question leaves a clear choice and both buttons display."),
    826: ((6350,), "Marie", (), ("Oh, can't handle another drink?",),
          "Marie reacts with surprise and teases Hodram about his tolerance after he declines.",
          "The teasing question follows directly from No and keeps the object of her reaction clear without adding a relationship."),
    858: ((7100, 8850), "Manuel Almeida", ("303",), ("Would it be all right to spend", "about 303 gold?"),
          "Manuel estimates the round's cost and asks permission to spend it.",
          "The careful wording keeps the estimate and permission in one question. The amount stays with gold."),
    865: ((7350,), "Hodram Bergstrom", (), ("Drinks for everyone!",),
          "Hodram tells the barkeep to serve a drink to everyone there.",
          "The direct call fits his decisive response after approving the amount."),
    872: ((7600,), "Barkeep", ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",),
          "The barkeep says Bergstrom is paying and tells the room to enjoy itself.",
          "The public announcement makes the patron's later thanks clear. It uses the original surname binding."),
    874: ((7850,), "Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
          "The patron is surprised, thanks the captain and praises him for his generosity.",
          "The surprise and emphatic thanks lead naturally to the news he offers next."),
    880: ((8100,), "Patron", ("Clifford", "London"), ("Word is, Clifford has a fleet", "heading to London."),
          "The patron says on hearsay that Clifford's fleet is on its way to London.",
          "Word is keeps the news informal, and the destination and the fleet's direction stay together."),
    657: ((10350,), "Shopkeeper", (), ("You're a sailor, aren't you?", "Try the Market for bulk trade."),
          "The shopkeeper recognizes a sailor and suggests the Market for large transactions.",
          "The full question and tag share a line, then the shopkeeper gives a useful direction in one phrase."),
    658: ((11100, 11850, 13600), "Shopkeeper", (), ("Business? Oh, it's been all right.", "I'm hoping a good deal comes along."),
          "The shopkeeper says business has been passable and hopes for an opportunity to turn a profit.",
          "The echoed question, modest assessment and hopeful aside match a casual conversation about trade."),
    656: ((12600,), "Shopkeeper", (), ("We only sell retail.",),
          "The shopkeeper explains that this shop specializes in retail.",
          "The short reply states what the shop sells. The independently selected bulk-trade reply gives the explicit Market referral."),
    709: ((13100, 14100), "Shopkeeper", (), ("Clifford used to be a pirate. Now", "he's a naval admiral, and I hear", "the Queen's made him a knight."),
          "Despite his former piracy, Clifford is a naval admiral and is said to have received the title Sir from the Queen.",
          "Preserve the reversal from piracy to naval rank and keep the Queen's knighting as hearsay. The visible first line strands Now from the clause it introduces."),
}


def collect(release):
    capture = checked_text(getsource(panels.capture), {
        '    assert all(r["validation_passed"] for r in journal["commands_received"])':
            '''    rejected = [r for r in journal["commands_received"] if not r["validation_passed"]]
    assert rejected == [dict(frame=4600, command=dict(until=4850, buttons=["Down"], duration=8),
                             validation_passed=False, rejected_before_any_input_or_fixture="Invalid buttons")]
    assert not any(r["start"] == 4601 and r.get("buttons") == ["Down"] for r in report["scripted_input_schedule"])''',
    })
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    exec(compile(capture, __file__ + "::ordinary-London", "exec"), scope)
    return scope["capture"](play.ROOT.name, release)


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    frames, calls, refs = collect(release)
    assert max(frames) == END
    assert refs["donor"]["sha256"] == read(play.prior.HISTORY)["battery_save_preloaded"]["source_sha256"]
    ordered = sorted((frame, key) for key, row in HOLDS.items() for frame in row[0])
    assert [row["message_ID"] for row in calls[::2]] == [key for _, key in ordered]
    paired = dict()
    for (frame, key), (get, copy) in zip(ordered, zip(calls[::2], calls[1::2], strict=True), strict=True):
        assert get["message_ID"] == key and 0 < frame - get["frame"] < 500
        assert get["PC"] == 0x0205528C and copy == get | {"PC": 0x020534F4}
        paired[frame] = (get, copy)
    original, current = map(NdsImage.open, (CLEAN, active.ROM))
    original_arm, arm = (rom.read_file(active.ARM) for rom in (original, current))
    ja = common_message_entries(original.read_file(active.COMMON), original_arm)
    en = panels.common_rows(current.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    records, figures = [], []
    for key, (numbers, speaker, args, lines, meaning, reason) in HOLDS.items():
        source, installed = ja[key], en[key]
        assert source.text.count(b"%s") == len(args) + (key == 872)
        assert installed.text.count(b"%s") == len(args)
        expanded = installed.text % tuple(word.encode("ascii") for word in args)
        assert expanded.decode("ascii").split() == " ".join(lines).split()
        observations = []
        for frame in numbers:
            observations.append(dict(capture=frames[frame], requests=paired[frame],
                glyph_ink_pixels=panels.exact_body(font, lines, screens[frame]),
                complete_nameplate=panels.nameplate(font, speaker, screens[frame])))
        figures.append((f"{numbers[0]} / COMMON {key} / {speaker}", screens[numbers[0]]))
        saved = panels.text_reference(installed) | dict(exact_hex=installed.text.hex())
        decision = "revision needed" if key == 709 else "retention"
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=active.COMMON,
            speaker=speaker, context=TAVERN if key in (51, 53, 823, 55, 56, 59, 826, 858, 865, 872, 874, 880) else SQUARE,
            clean_Japanese=source.text.decode("cp932"), source_meaning=meaning, english=" ".join(installed.text.decode("ascii").split()),
            source_reference=panels.text_reference(source) | dict(exact_hex=source.text.hex()), current_reference=saved,
            installed_reference=saved, localization_note=reason, decision=decision,
            review=dict.fromkeys(GATES, True) | {"formatting": key != 709}, arguments=args, lines=lines,
            observations=observations))
    choices = {frame: [panels.find_mask(font, text, screens[frame], bounds) for text, bounds in
        (("No", (126, 359, 172, 377)), ("Yes", (196, 359, 237, 377)))] for frame in (6100, 7100, 8850)}
    balances = {3200: 40659, 6600: 40654, 8350: 40351, 9100: 40351, 9350: 40351}
    wallets = {frame: panels.find_mask(font, str(amount), screens[frame], (78, 349, 136, 367))
               for frame, amount in balances.items()}
    assert 40659 - 40654 == 5 and 40654 - 40351 == 303
    assert all(wallets.values()) and all(all(choice) for choice in choices.values())
    returned = panels.find_mask(font, "London", screens[9350], (48, 10, 121, 34))
    assert returned
    for frame, label in ((6850, "Buy a Round"), (9350, "London town after Tavern"), (14600, "Square menu after Textile Shop")):
        figures.append((f"{frame} / {label}", screens[frame]))
    batch = dict(candidate_sha256=release["candidate_sha256"], release=reference(active.RELEASE),
        ordinary_gameplay=True, translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=records, evidence=refs,
        requests=calls, choices=choices, wallets=wallets, returned_to_London=returned,
        dialogue_holds=len(ordered), text_retentions=15, wrap_findings=[709], ROM_changed=False, new_editorial_credit=0,
        unvisited=["Marie's handoff of Rainbow Marbles", "Other London Tavern rumors", "Square Trends submenu"])
    retentions = [row for row in records if row["decision"] == "retention"]
    assert len(retentions) == batch["text_retentions"]
    validate_natural_dialogue_batch(batch | {"records": retentions})
    sheets = panels.sheets_for("london_tavern_and_square_current_20261125", figures)
    write(OUT, batch | dict(sheets=sheets))
    print("Verified 20 ordinary London holds. Retained 15 texts and identified one Square rumor wrap.")


if __name__ == "__main__":
    main()
