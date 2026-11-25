"""Review story wraps in context and preserve wording that already reads well."""

from collections import Counter

from scripts import prepare_story_phrase_continuity_20261118 as packet
from scripts.review_london_guild_assignments_20261118 import TOKEN, base, logical

SOURCE = packet.SOURCE
SOURCE_SHA = "6701ca2fb5cd123dea9b841070f9f65d18e42dcecf051cf101e35e80d0c0cc42"
OUTPUT = packet.ROOT / "phrase_continuity_prose_v3.json"
GATES = ("source", "context", "localization", "naturalness", "formatting")

# The selected turns use their clean source record index. A missing draft keeps
# the existing words; an empty phrase list keeps the existing stored layout too.
ARROW = ("Cesare Tony", "The crew's neglect of work prompts Cesare to explain the legend, then complain that the sailors wonder whether it would help their gunnery.",
    "An angel is said to have used the Demon-Piercing Arrow to strike down a demon.",
    "Legend has it an angel used the Demon-Piercing Arrow to strike down a demon, sir.",
    ("Demon-Piercing Arrow", "strike down a demon, sir."),
    "Keep the story as hearsay and Cesare's deferential cadence. Use the same reading across the three matching replies.")
INCENSE = ("Verisa", "Verisa recognizes the visitor and introduces a censer rumored to improve her fortune-telling.",
    "She asks if the visitor knows the Goryeo celadon censer and says it is rumored to be somewhere in East Asia.",
    None, ("Goryeo Incense Burner?", "It's celadon.", "it's somewhere in East Asia."),
    "The approved item name, material, given-name greeting and uncertainty all read well. Keep the regional clue and its contraction intact.")
DECISIONS = {
    (0, 52, 18): ("Port Worker", "A port worker recognizes Rafael and passes on a message. Rafael wonders what the military wants.",
        "Admiral Albuquerque of the Portuguese regular military asked the worker to tell Rafael to return to Lisbon if he saw him.",
        None, (),
        "The short line keeps the admiral's title and name together. The worker's role as an intermediary and the recall to Lisbon stay clear."),
    (0, 58, 76): ("Abraham Uddin", "Abraham gives Rafael a lotus leaf and explains what it may lead to. Rafael repeats the name of the book.",
        "The Indian Ocean's Proof of Conquest should be a book called the Rigveda.",
        None, (),
        "The speaker's uncertainty, item class and title are correct. The existing lines keep both proper names intact and avoid cramming the possessive and the title onto one line."),
    (0, 93, 68): ("Rafael", "Emilio is still demanding his banana. Rafael diverts him with local food, which works once he offers to pay.",
        "Rafael suggests that he and Emilio try the town specialty.",
        None, (),
        "The friendly invitation fits the switch away from the banana. The short opening keeps the local specialty together as the punch of the offer."),
    (0, 143, 380): ("Fernan Silveira", "Fernan teaches Rafael how to start a war and use local market share to obtain a port contract. This line explains the effect of a naval victory.",
        "Defeating a faction you are at war with in a sea battle lowers its reputation and slightly reduces its share in towns near the battle.",
        "When you're at war, a win at sea costs your enemy reputation and a little market share in nearby towns.",
        ("a win at sea", "a little market share", "in nearby towns."),
        "Keep the war condition, naval victory, reputation effect, slight loss and local radius together as a short lesson."),
    (0, 152, 128): ("Duarte Pereira", "Duarte explains why his position under the Spanish king constrains him. Rafael understands that openly backing them could draw the king's ire.",
        "Duarte asks Rafael to see his position as Portugal's governor of Indochina, now bound to obey the King of Spain.",
        "See it from my side. As Portugal's governor of Indochina, I have to answer to the King of Spain now.",
        ("See it from my side.", "governor of Indochina,", "the King of Spain"),
        "Keep both the Portuguese office and Spanish authority without breaking after a contraction."),
    (0, 152, 136): ("Duarte Pereira", "Duarte explains his responsibility for his people before naming the narrower help he can offer against Kuhn.",
        "Many people's livelihoods depend on Duarte. A governor has to take care of them, and that is the hard part.",
        "People count on me to get by. I've got to look after them. That's the hard part of this job.",
        ("People count on me to get by.", "I've got to look after them.", "That's the hard part of this job."),
        "Keep Duarte's blunt explanation of responsibility and give the conclusion a full phrase."),
    (0, 176, 68): ("Jam Ludwyan", "Jam shrugs off criticism over the ship with a proverb and declares himself satisfied. Rafael repeats the proverb in disbelief.",
        "Jam boasts that determination can get things done and says everything is fine because he says so.",
        None, ("Where there's a will,", "there's a way!", "It's OK if I say it's OK!"),
        "Keep the recognizable proverb and exuberance. Its two balanced halves are a natural place to wrap."),
    (0, 186, 125): ("Julian Lopes", "Julian asks how the others beat him to a relic. The answer reveals that they sailed there, which surprises him.",
        "Julian asks how they found the Silla Gold Crown so quickly.",
        None, (),
        "The quick question sounds like Julian and keeps the full relic name on one line. A rewording just to use the first line would flatten his cadence."),
    (0, 243, 13): ("Carlo Sinat", "Rafael has never heard of Herophilus. Carlo explains who he was before mentioning a remedy for exhausted sailors.",
        "Herophilus was an ancient physician who wrote the oldest medical book in the world.",
        "Herophilus was a doctor long ago. He wrote the oldest medical book in the world.",
        ("Herophilus was a doctor long ago.", "in the world."),
        "State the profession in ordinary speech, then keep the book's distinction as Carlo explains it."),
    (0, 249, 27): ARROW,
    (0, 252, 53): ("Rafael", "Rafael sees through the swindler's supposed treasure and realizes it is the missing rose ornament. The barkeep reacts to the glass.",
        "Rafael confirms that the ornament is glass and concludes it must belong to the girl.",
        "I knew it! It's glass. This has to be her rose!",
        ("It's glass.", "her rose!"),
        "Keep the sudden recognition, the material and whose ornament he believes it is."),
    (0, 303, 31): ("Rafael", "Rafael and Claudio work out that an earlier clue means the Indian Ocean's Proof. Rafael realizes which object to look for first.",
        "The party must first find the Proof of Conquest for the Indian Ocean.",
        "So we have to find the Proof of Conquest for the Indian Ocean first!",
        ("Proof of Conquest", "the Indian Ocean first!"),
        "Use the established full title and keep the search order and the region."),
    (0, 322, 65): ("Sakura", "Rafael describes a foreign place and its wine. Sakura wants to compare it with sake, and Rafael offers to bring her some.",
        "Sakura asks how wine tastes, expects it differs from Japanese sake and says she would love to try it.",
        None, ("What does wine taste like?", "It's different from sake, isn't it?", "I'd love to try it!"),
        "Keep the cultural comparison and Sakura's curiosity. Her whole question about sake belongs on one line."),
    (1, 240, 21): ("Hodram", "A frustrated Cesare names the item amid a complaint. Hodram asks what it is, giving Cesare room to tell the legend.",
        "Hodram has lost the thread and asks what the Demon-Piercing Arrow is.",
        None, ("What's the Demon-Piercing Arrow?",),
        "Keep Hodram's understated interruption and the complete item question."),
    (1, 251, 9): ("Hodram", "Hodram sees a statue before the others notice it and asks whether they sense its unusual warmth.",
        "Hodram asks if the others sense anything from the statue, something like a strange warmth.",
        "Look at this statue. Do you feel that strange warmth, too?",
        ("Look at this statue.", "that strange warmth, too?"),
        "A direct question keeps the sensation immediate and preserves the others' surprise."),
    (1, 294, 47): ("Gerhard Adernkatz", "The party stops at a forest they cannot cross without a map. Gerhard infers that the terrain explains why nobody noticed what was there.",
        "The density of the forest would explain why the place has gone unnoticed until now.",
        "No wonder nobody's found it before.",
        ("No wonder nobody's found it before.",),
        "Keep the inference tentative and natural in Gerhard's reply to Hodram."),
    (1, 314, 10): INCENSE,
    (2, 92, 24): ("Lil", "Julio worries about his granddaughter Cristina. Lil reassures him and compares Cristina to Athena, which he asks her to explain.",
        "Lil teases Julio for being proud, reassures him that Cristina is dependable and compares her to Athena reborn.",
        None, ("No one's more dependable.", "She's like Athena reborn!"),
        "The reassurance and comparison already sound like Lil. Keep each short thought together."),
    (2, 133, 35): ("Lil", "Rafael identifies himself and his company. Lil is startled that someone his age commands it.",
        "Lil reacts with disbelief and asks whether Rafael is from the Castor Company.",
        "What?! The Castor Company?!",
        ("The Castor Company?!",),
        "Echo his identification with Lil's surprise. The company name stays consistent with Rafael's preceding line."),
    (2, 237, 25): ARROW,
    (2, 248, 18): ("Guildmaster", "Lil tries to recall where the village is. The guildmaster asks about the survey and gives directions from this port.",
        "The guildmaster asks how the survey of Leveque village went and says Leveque is far east of this town, across the Indian Ocean.",
        "How's the Leveque survey going? It's far east of here, across the Indian Ocean.",
        ("How's the Leveque survey going?", "It's far east of here,", "across the Indian Ocean."),
        "Restore this port as the point of reference and keep the ocean name with the crossing."),
    (2, 317, 10): INCENSE,
    (3, 61, 63): ("Charles Rochefort", "The shipwright calls Charles away from his experiments. Charles tries to put off the interruption until Maria introduces herself.",
        "Charles recognizes the older man, asks him to come back later and says he is busy and close to proving his theory.",
        "Oh, it's you. Can it wait? I'm busy. I'm close to proving my theory...",
        ("Can it wait?", "I'm busy.", "I'm close to proving my theory..."),
        "Keep his impatience and the thought trailing off. The short sentences give him a distracted cadence."),
    (3, 61, 112): ("Charles Rochefort", "Maria introduces herself and Xien. Charles now likes the sound of the venture and introduces himself.",
        "Charles thinks it sounds fun, gives his full name and says he is pleased to meet them.",
        None, ("I'm Charles Jean Rochefort.", "Pleased to meet you!"),
        "The shift to enthusiasm works. Keep his given names and surname with the introduction."),
    (3, 174, 22): ("Carlo Sinat", "A trader asks 300,000 gold for unusual mast rope. Carlo intervenes and puts a much lower ceiling on the price.",
        "Even for special mast rope the price is absurd. Carlo says 30,000 gold is the most it is worth.",
        "No mast rope is worth that much, special or not. 30,000 gold, tops.",
        ("No mast rope is worth that much,", "30,000 gold, tops."),
        "Keep the contrast with the previous asking price, including the exact amount and what is being bought."),
    (3, 209, 35): ("Jam Ludwyan", "Jam describes a statue that might predict the future, then wonders whether it would help him beat Fernando at gambling.",
        "Jam admits the story sounds suspicious. He thinks anything might happen in India, so it could be true.",
        "Sounds fishy, right? But this is India. Nothing would surprise me here. It might be true.",
        ("Sounds fishy, right?", "Nothing would surprise me here."),
        "Restore Jam's personal reaction to the place and keep the tale uncertain."),
    (3, 209, 63): ("Fernando Dias", "Fernando reacts to Jam's letter and its idea of beating him at gambling. Maria laughs and considers looking for the statue.",
        "Fernando scoffs that even with that thing, Jam is five hundred years too early to beat him.",
        "Ha! He'll need another five hundred years to beat me, even with that thing!",
        ("five hundred years", "even with that thing!"),
        "Keep the specific comic exaggeration and the insult aimed at Jam's chances."),
    (3, 210, 24): ARROW,
    (3, 286, 9): INCENSE,
    (3, 295, 4): ("Guildmaster", "The guildmaster looks unusually grave and turns to Maria before explaining the attacks by an unidentified ship.",
        "He addresses Maria by surname and says she is the only person he can ask for this help.",
        "FA, I need a favor. You're the only one I can ask.",
        ("I need a favor.", "You're the only one I can ask."),
        "The request is implicit in the source and explicit in the next turn. Keep the surname and the seriousness of his reliance on her."),
    (3, 298, 91): ("Villager", "The villager recognizes Maria after hearing what happened to Escante's forces. Xien wonders how far the story has spread.",
        "The villager is startled that Maria is the woman admiral from the East.",
        "What?! You're the woman admiral from the East?",
        ("You're the woman admiral", "from the East?"),
        "Keep the recognition, the title and the reason she stands out in the account the villager heard."),
}


def main():
    assert not OUTPUT.exists() and base.digest(SOURCE) == SOURCE_SHA
    paired, release = map(base.load, (SOURCE, packet.parent.RELEASE))
    assert paired["candidate_sha256"] == release["candidate_sha256"] == base.digest(packet.parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    records, found = [], set()
    for group in paired["groups"]:
        route, block, path = group["route"], group["block"], group["file_path"]
        for row in group["records"]:
            if row["current_offset"] not in packet.LEADS[route][block]:
                continue
            idx, selector = row["source_record_index"], row["selector"]
            key = route, block, idx
            speaker, context, meaning, draft, phrases, note = DECISIONS[key]
            assert key not in found
            found.add(key)
            previous = logical(row["current_English"])
            english = draft if draft is not None else previous
            decision = "prose" if english != previous else "wrap" if phrases else "retention"
            assert Counter(TOKEN.findall(english)) == Counter(TOKEN.findall(row["Japanese"]))
            assert Counter(TOKEN.findall(english)) == Counter(TOKEN.findall(previous))
            assert english.isascii() and row["native_command_word"] == 0x4000
            src, old = (dict(file_path=path, block=block, archive_sha256=group[f"{side}_archive_sha256"],
                offset=row[f"{side}_offset"], command_offset=row[f"{side}_command_offset"],
                exact_stored_hex=bytes([selector]).hex() + row[f"{side}_body_hex"]) for side in ("source", "current"))
            src["record_index"] = idx
            records.append(dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block,
                kind="progressive", native_command_word=0x4000, source_selector=selector, native_slots=[],
                source_reference=src, current_reference=old, source_hex=src["exact_stored_hex"], current_hex=old["exact_stored_hex"],
                Japanese=row["Japanese"], previous_English=previous, english=english, context=context, speaker=speaker,
                source_meaning=meaning, localization_note=note, protected_phrases=list(phrases), finding=decision,
                decision="retention" if decision == "retention" else "revision",
                review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert found == DECISIONS.keys() and len(found) == 31
    counts = dict(Counter(r["finding"] for r in records))
    base.save(OUTPUT, dict(source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=records, decisions=counts,
        new_coverage_credit=0, formatting_and_registration_pending=True))
    print(counts)


if __name__ == "__main__":
    main()
