"""Verify the ordinary Tunis drink, round and rumor exchange."""

import json
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_tunis_tavern_20261125 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, write


OUT = panels.OUT.with_name("tunis_tavern_current_20261125.json")
ARCHIVED_DRAFTS = OUT.with_name("archived_dialogue_current_drafts_20261124.json")
END = 9440
HOLDS = {
    51: ((4820,), "Barkeep", (), ("Welcome! What will you have?",),
         "The barkeep welcomes the guest and asks what he will order.",
         "The quick greeting gives Hodram the floor and leads naturally into the menu."),
    53: ((5260, 5920, 7240), "Barkeep", (), ("5 coins.",),
         "The barkeep quotes five gold coins for the drink.",
         "The brief price fits the barkeep's delivery and matches each deduction shown after the conversation."),
    823: ((5480, 6140, 7460), "Barkeep", ("Algiers",), ("Have you heard of a nearby town", "called Algiers?"),
          "The barkeep asks whether the captain knows a nearby town by its name.",
          "The barkeep sounds conversational. Algiers and its question mark stay together, and nearby preserves the geographic clue."),
    852: ((6800, 8120), "Charles Rochefort", ("272",), ("It looks like it'll cost 272 gold.", "Is that all right?"),
          "Charles estimates the cost of buying a round and asks for the captain's approval.",
          "The deferential question fits Charles. Both clauses are complete on their own lines and the quote matches the charge."),
    865: ((8340,), "Hodram Bergstrom", (), ("Drinks for everyone!",),
          "Hodram tells the tavern to serve a round to everyone.",
          "A short public call suits Hodram and includes the whole room after he agrees to pay."),
    872: ((8560,), "Barkeep", ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",),
          "The barkeep announces who is treating the room and invites everyone to enjoy the drinks.",
          "Naming Bergstrom makes the reason for the patron's thanks clear. The existing optional address binding stays intact."),
    874: ((8780,), "Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
          "The patron is surprised, thanks the captain for the drink and calls him generous.",
          "The two exclamations carry the patron from surprise to gratitude before he offers a tip."),
    870: ((9000,), "Patron", ("Sir", "Black Rapier", "the Mediterranean"),
          ("Sir, a tip about a rare treasure.", "They say Black Rapier is stashed", "in the Mediterranean."),
          "The patron addresses the captain politely and passes on hearsay about a rare treasure in a named region.",
          "The salutation fits the approach, They say preserves uncertainty, and both the item name and the complete place phrase stay together."),
}
REQUESTS = (0, 51, 53, 823, 53, 823, 852, 53, 823, 852, 865, 872, 874, 870)
BALANCES = {4200: 7056, 5700: 7051, 6360: 7046, 7020: 7046, 7680: 7041, 9220: 6769, 9440: 6769}


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"]
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    assert max(frames) == END
    assert tuple(row["message_ID"] for row in calls[::2]) == REQUESTS
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands[0] == play.OPENING
    assert refs["donor"]["sha256"] == read(play.HISTORY)["battery_save_preloaded"]["source_sha256"]

    original, current = map(NdsImage.open, (CLEAN, active.ROM))
    source_arm, arm = (image.read_file(active.ARM) for image in (original, current))
    source = common_message_entries(original.read_file(active.COMMON), source_arm)
    installed = panels.common_rows(current.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    records, figures = [], []
    for key, (numbers, speaker, args, lines, meaning, reason) in HOLDS.items():
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == len(args) + (key == 872)
        assert en.text.count(b"%s") == len(args)
        assert (en.text % tuple(v.encode("ascii") for v in args)).decode("ascii").split() == " ".join(lines).split()
        observed = []
        for number in numbers:
            first, second = [row for row in calls if row["message_ID"] == key and 0 < number - row["frame"] <= 220]
            assert second == first | {"PC": 0x020534F4}
            observed.append(dict(capture=frames[number], requests=[first, second],
                body_ink_pixels=panels.exact_body(font, lines, screens[number]),
                nameplate=panels.nameplate(font, speaker, screens[number])))
        figures.append((f"{numbers[0]} / {speaker} / COMMON {key}", screens[numbers[0]]))
        saved = panels.text_reference(en) | dict(exact_hex=en.text.hex())
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker=speaker,
            context="Tunis Tavern. The barkeep offers a local tip after a paid drink, then the crew asks about buying a round.",
            clean_Japanese=ja.text.decode("cp932"), english=en.text.decode("ascii").strip(), source_meaning=meaning,
            source_reference=panels.text_reference(ja) | dict(exact_hex=ja.text.hex()), current_reference=saved,
            installed_reference=saved, decision="retention", localization_note=reason,
            review=dict.fromkeys(GATES, True), arguments=args, lines=lines, observations=observed))

    archived = []
    for row in read(ARCHIVED_DRAFTS)["records"]:
        key = row["message_ID"]
        assert key not in REQUESTS and row["original_display_ownership_open"]
        for table, name in ((source, "source_reference"), (installed, "installed_reference")):
            entry = table[key]
            assert panels.text_reference(entry) | {"exact_hex": entry.text.hex()} == row[name]
        archived.append(dict(message_ID=key, source_reference=row["source_reference"],
                             installed_reference=row["installed_reference"], display_owner_open=True))
    assert [row["message_ID"] for row in archived] == [284, 318, 750, 751, 752]

    choice = {number: [panels.find_mask(font, label, screens[number], bounds) for label, bounds in (
        ("No", (126, 359, 172, 377)), ("Yes", (196, 359, 237, 377)))] for number in (6800, 8120)}
    assert all(choice.values())
    wallets = {number: panels.find_mask(font, str(balance), screens[number], (78, 349, 136, 367))
               for number, balance in BALANCES.items()}
    assert all(wallets.values())
    assert BALANCES[7020] == BALANCES[6360] and BALANCES[7680] - BALANCES[9220] == 272
    end = panels.find_mask(font, "Tunis", screens[END], (58, 14, 152, 34))
    figures.extend((f"{number} / {description}", screens[number]) for number, description in (
        (7020, "Declined at 7046 gold"), (8120, "Accepted quote"), (9220, "After payment"), (END, "Town return")))
    batch = dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        release=reference(active.RELEASE), translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=records,
        evidence=refs, commands=commands, requests=calls, choices=choice, wallets=wallets, returned_to_Tunis=end,
        archived_drafts=reference(ARCHIVED_DRAFTS), archived_records=archived,
        unvisited=["Other Tunis patron rumors", "Tunis recruitment and strategist options"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(batch)
    sheets = panels.sheets_for("tunis_tavern_current_20261125", figures, crop=(0, 192, 256, 384))
    write(OUT, batch | {"figures": sheets})
    print("Verified 13 ordinary Tunis dialogue holds, both round choices and the final 6769-gold wallet.")


if __name__ == "__main__":
    main()
