"""Restore complete native crew prompts and tavern conversations in B11/B12."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    870: ("%s, here's a tip. Rumor has it a rare treasure called %s is hidden in %s.", "Addresses the first substituted name, offers an interesting tip and reports a rumor that the second substituted rare treasure is hidden at the third substituted location."),
    871: ("Bravo! Clap, clap, clap! That's %s's great %s for you!", "Exclaims and claps in admiration, praising the great second substituted role/person belonging to the first substituted affiliation. Actual substituted values require runtime classification."),
    873: ("%s, with your skills, I'm sure you'll find it.", "Expresses confidence that someone as capable as the substituted person will find the treasure."),
    874: ("Whoo! Really?! Thanks! You're a class act! That's generous of you!", "An enthusiastic, colloquial thank-you, praising style and generosity. Iki is localized as being a class act, not a new rank or kinship."),
    875: ("%s, there's something I'd like to tell you...", "Politely addresses the substituted person and hesitantly says there is something to tell them."),
    883: ("Admiral, we don't have enough money.", "A direct, polite crew report of insufficient money."),
    884: ("Admiral, looks like we're short of money.", "An informal voice says it looks as though money is insufficient."),
    885: ("Um... Admiral, we don't have enough money.", "A hesitant, polite report of insufficient money."),
    886: ("Admiral, we're short on cash.", "An informal, emphatic report of insufficient money."),
    887: ("We haven't the money, Admiral.", "An older voice reports insufficient money."),
    921: ("Which town should I send them to?", "Politely asks which town to send the selected party toward; source does not specify gender or ownership."),
    922: ("Which town do you want them to visit?", "An informal voice asks which town the player intends to have the selected party visit."),
    923: ("Which town am I sending them to?", "A rough, informal voice asks which town the selected party should be sent toward."),
    931: ("Which town gets the rumor?", "An informal voice asks which town to spread the rumor in."),
    932: ("Which town should I spread the rumor in?", "An older, polite voice asks which town to spread the rumor in."),
    933: ("Who should we turn against each other?", "A polite voice asks which parties to make quarrel or fall out with each other."),
    938: ("Who do you want to get fighting?", "An informal voice asks who to make fight."),
    939: ("Who shall we turn against each other?", "An older, polite voice asks which parties to make quarrel or fall out with each other."),
    940: ("Lure %s's fleet to %s, right?", "Confirms luring the first substituted party's fleet to the second substituted place."),
    941: ("You want me to lure %s's fleet to %s, correct?", "More formally confirms luring the first substituted party's fleet to the second substituted place."),
    942: ("Take %s's fleet out to %s, right?", "An informal confirmation of taking the first substituted party's fleet out to the second substituted place; distinct from the lure wording of the other variants."),
    976: ("Which town's broker shall we bribe?", "An older voice asks in which town to bribe the broker."),
    977: ("Which town's broker do we bribe?", "A youthful voice asks in which town to bribe the broker."),
    978: ("In %s, we're bribing %s's broker, right?", "Confirms bribing the broker identified by two nested source substitutions, interpreted from the preceding town-selection prompt as place then affiliation; live values and hierarchy must be checked."),
    985: ("With this many customers, we can't talk privately. Let's come back another day.", "With so many customers, a confidential discussion is impossible; politely proposes returning another day."),
    986: ("Admiral, it's too crowded for a private talk. Let's try another day.", "An informal crew voice tells the admiral that the many customers seem to prevent a private discussion; proposes another day."),
    992: ("Listen to my song. It's called fado. La la la...", "Invites the player to listen to her song, identifies its genre as fado, and sings la la la. The musical effect is conveyed by prose ellipsis."),
    993: ("I fall in love so easily. It always ends badly for me, though.", "The speaker falls in love readily, and that always leads to failure for her."),
    1014: ("Tired, aren't you? I'll indulge your whims... just a little.", "A teasing voice asks if the player is tired and offers to indulge their wishes to a limited degree. Playful elongated pronunciation is localized as a teasing pause."),
    1015: ("Men sail, women keep house? That's outdated. In this new era, shouldn't women enter public life, too?", "Rejects the outdated idea that men go to sea and women guard the home; asks whether women should also advance into society in the coming/new era."),
    1017: ("Sailors are so wonderful! Have you ever seen dolphins? What about whales?", "Admires sailors, then asks if the player has seen dolphins and whales."),
    1018: ("Tell me about pirates! What kind of ships do they sail? Are they really strong?", "Asks to hear pirate stories, what kinds of ships pirates use, and whether they are strong as expected."),
    1019: ("Animals are being hunted for their fur lately. Why do people do such cruel things?", "Animals have recently been hunted for fur; the speaker wonders why people do something so cruel."),
    1028: ("By the way, did you know there's a village near %s where you can get supplies?", "A polite voice asks if the player knows of a resupply village around the substituted location."),
    1029: ("Oh, have you heard? There's a village near %s where you can get supplies.", "A colloquial voice asks if the player knows of a resupply village around the substituted location."),
    1030: ("They say an unfamiliar fleet is anchored at %s.", "An informal voice reports hearsay that an unfamiliar fleet is anchored at the substituted place."),
    1031: ("An unidentified fleet is heading for %s.", "A polite report that an unidentified fleet is heading toward the substituted place."),
    1032: ("Some mysterious fleet is headed for %s.", "A rough, colloquial voice reports a fleet of unknown identity heading toward the substituted place."),
    1033: ("An unidentified fleet is anchored at %s.", "A polite report that an unidentified fleet is anchored at the substituted place."),
}


REVISIONS = {
    870: "%s, here's a tip: the rare treasure %s is said to be hidden in %s.",
    874: "Whoo! Really?! Thanks so much! You're a class act! How generous!",
    875: "%s, I have something to tell you...",
    884: "Admiral, we seem short on money.",
    885: "Um... Admiral, we're short of money.",
    922: "Which town are we sending them to?",
    932: "Which town should hear the rumor?",
    933: "Who should we set at odds?",
    939: "Who shall we set at odds?",
    941: "We're to lure %s's fleet to %s. Is that correct?",
    978: "In %s, bribe %s's broker. Is that your order?",
    986: "Admiral, it seems we can't talk privately with so many customers. Let's come back another day.",
    1015: "Men sail, women keep house? That's outdated! In this new era, women should enter public life too, don't you think?",
    1017: "Sailors are so wonderful! Seen any dolphins? Any whales?",
    1018: "Tell me about pirates! What are their ships like? Are they really powerful?",
    1028: "By the way, a village near %s can supply you. Did you know?",
    1029: "Heard the news? A village near %s has supplies for you.",
    1031: "An unknown fleet is bound for %s.",
    1032: "Some strange fleet is headed to %s.",
    1033: "An unknown fleet is anchored at %s.",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v108_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] in {11, 12}}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B11/B12 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Crew voice or tavern contact",
            "context": f"Independent native message {message_id}, COMMON B{source.block} R{source.record_index}; treasure rumor, crew assignment/report, confidential meeting or tavern conversation. Packed neighbors are separate entries and voice variants.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source prose preserves uncertainty, rumor, hesitation, polite/informal variants, command intent, gratitude, playful tone, private-meeting conditions, song genre, timing and resupply. All printf substitutions retain source order. Bribe and title substitutions retain contextual interpretation pending live values; no fixed names or ranks are invented. Reserved I/F use existing full-width Latin glyphs. Native repack and all previews require review.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b11_b12_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B11/B12 entries; formatting pending")


if __name__ == "__main__":
    main()
