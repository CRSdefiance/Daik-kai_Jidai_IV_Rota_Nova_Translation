"""Review isolated tag questions and phrase breaks in their paired scenes."""

from collections import Counter

from scripts import prepare_story_tag_wraps_20261118 as pairs
from scripts.review_london_guild_assignments_20261118 import TOKEN, logical, base

SOURCE = pairs.EXTENDED
SOURCE_SHA = "a707ebae471d1422553d58b62a40728e148179aa57efa7167993806a83a29f55"
OUTPUT = pairs.ROOT / "story_tag_wraps_prose_v2.json"
GATES = ("source", "context", "localization", "naturalness", "formatting")

# Speaker, scene context, source meaning, English, protected phrases, review note.
DECISIONS = {
    (0, 49): ("Rafael", "Lil warns Rafael against confrontation. He sees an offer to ally, and she resents sounding like the one asking.",
        "Rafael chuckles and observes that Lil hates to lose.",
        "Heh. You hate losing, don't you?", ("You hate losing, don't you?",),
        "Rafael gently teases her, which prompts Lil to ask if he's making fun of her."),
    (0, 70): ("Maria", "Maria promises Rafael the assembly plan once the Kurushima faction is gone. He asks why he needs it.",
        "The plan is essential for finding East Asia's Proof. Maria asks whether it's a fair bargain.",
        "You'll need it to find the Proof of Conquest in East Asia. Not a bad deal, is it?",
        ("Proof of Conquest", "in East Asia.", "Not a bad deal, is it?"),
        "Use the approved full title and keep the region and the bargaining tag together."),
    (0, 82): ("Cristina", "Mivor ignores Cristina's anger and keeps pursuing her over an engagement arranged by their parents.",
        "Cristina emphatically complains that he just won't stop bothering her.",
        "You just WON'T leave me alone!", ("You just WON'T leave me alone!",),
        "Keep the emphasis and exasperation. An exclamation carries the complaint without an isolated tag."),
    (0, 84): ("Gerhard", "Gerhard offers to teach Rafael before he returns to sea. Rafael chooses whether to accept.",
        "Gerhard has something to teach before he goes to sea and asks whether Rafael will accept some special training.",
        "Before I go to sea, there's something I'd like to teach you. How about some special training?",
        ("Before I go to sea,", "I'd like to teach you.", "How about some special training?"),
        "Keep the timing and make the invitation sound like Gerhard. The full question stays together before the original choice."),
    (1, 85): ("Cristina", "Hodram offers Mivor passage. Cristina needles him about his fear of water, and he challenges them to a duel.",
        "She tells the others that Mivor can't swim and fears water, then taunts him about his inability to follow.",
        "He can't swim. He's terrified of water. You can't follow us, can you?",
        ("He's terrified of water.", "You can't follow us, can you?"),
        "Give Cristina the same taunt where the Japanese matches Lil's route. The setup and the dare each fit as a phrase."),
    (1, 147): ("Barkeep", "The barkeep recognizes the jar. Hodram and the crew discuss its contents before the barkeep explains its use against counterfeit gold.",
        "The barkeep has heard that the contents can dissolve any metal but gold.",
        "Hey, isn't that a Lotion Jar? I hear the stuff inside can dissolve any metal but gold. Amazing, isn't it?",
        ("isn't that a Lotion Jar?", "any metal but gold.", "Amazing, isn't it?"),
        "Keep the item's approved name, hearsay, gold exception and the barkeep's sense of wonder."),
    (1, 242): ("Francisca", "Francisca points Hodram to the wooden church outside the town. He realizes he overlooked it and agrees to visit.",
        "She thanks him warmly and asks him to come back.",
        "Thank you so much! Come again!", ("Come again!",),
        "Keep the warmth and invitation. The Japanese uses an invitation softened by a particle, which works without a separate English tag."),
    (2, 26): ("Clifford", "Lil apologizes after insulting Clifford, who takes it lightly and recognizes her by name.",
        "Clifford reassures Lil that he doesn't mind, then confirms her given name and surname.",
        "No harm done. Now, you're FI FA?", ("No harm done.", "FI FA?"),
        "Keep his easy manner. Both name fields and the question mark stay together, including at maximum width."),
    (2, 66): ("Lil", "An unfamiliar man reveals Camille's other name. Lil recognizes his connection and tests her conclusion that he is Camille's father.",
        "Lil says he should know the circumstances better than she and asks whether he is Camille's father.",
        "You know more about this than I do. You're his father, aren't you?",
        ("than I do.", "You're his father, aren't you?"),
        "Keep Lil's pointed challenge and tentative confirmation. The following answer establishes his relationship."),
    (2, 72): ("Cristina", "Lil asks whether Mivor will follow Cristina. Cristina taunts him about the water before he challenges the group to a duel.",
        "She tells the others that Mivor can't swim and fears water, then taunts him about his inability to follow.",
        "He can't swim. He's terrified of water. You can't follow us, can you?",
        ("He's terrified of water.", "You can't follow us, can you?"),
        "Keep the same wording as Hodram's parallel scene. Cristina shifts from telling the group to taunting Mivor directly."),
    (2, 129): ("Research Student", "The student is occupied when Lil approaches. He recognizes her as Dutch, says he is too, and tries to enlist her sympathy.",
        "He mutters that he's almost there, then asks whether she's Dutch.",
        "Ah, almost... Oh! You're Dutch, right?", ("You're Dutch, right?",),
        "Keep his interrupted thought and the sudden friendly recognition. Put the question on a single line."),
    (2, 151): ("Vasquez Maldonado", "After bullying the patrons, Vasquez threatens the barkeep over the bill. The barkeep waives it while the crew restrains each other.",
        "Vasquez reacts angrily to the bill and demands that the barkeep acknowledge whom he owes for living in peace.",
        "The bill?! Who do you think keeps you safe around here?!", ("keeps you safe around here?!",),
        "Keep the threat implicit in the question and leave the forced waiver to the barkeep's reply."),
    (2, 183): ("Shopkeeper", "The shopkeeper says few painting collectors have a good eye. A sailor laughs at his frankness before the shopkeeper asks for discretion.",
        "The shopkeeper catches himself and asks the sailor to keep his remark secret.",
        "Oops. Keep that between us, okay?", ("Keep that between us, okay?",),
        "Keep the moment of embarrassment, followed by a friendly request for discretion."),
    (2, 186): ("Owner", "The owner insists on sweeter food. The cook asks how to make it sweeter, and she puts the problem back on him.",
        "She tells the cook that working out the solution is his job.",
        "That's your job, isn't it?", ("That's your job, isn't it?",),
        "The cook's question supplies what the job is. Her whole retort now fits together."),
    (2, 215): ("Guard", "A guard interrupts the crew's discussion of Solomon's mines. He confirms the admiral's identity, thanks her for investing and offers a rumor.",
        "The guard politely addresses Lil by her admiral title and confirms her surname.",
        "Excuse me. Are you Admiral FA?", ("Are you Admiral FA?",),
        "Keep the source title and runtime surname. The polished question remains completely visible at maximum name width."),
    (2, 220): ("Lucia", "Julian compliments Lucia's eyes. She teases him about his flattery before he compares her to a legendary empress.",
        "Lucia welcomes Julian and says he is as good a talker as ever.",
        "Welcome, Julian. Smooth as ever.", ("Smooth as ever.",),
        "Retain the greeting and the affectionate teasing. The neighboring compliment makes clear what she means by smooth."),
    (3, 188): ("Guard", "A guard interrupts the crew's discussion of Solomon's mines. He confirms the admiral's identity, thanks her for investing and offers a rumor.",
        "The guard politely addresses Maria by her admiral title and confirms her surname.",
        "Excuse me. Are you Admiral FA?", ("Are you Admiral FA?",),
        "Use the same courteous greeting where the Japanese is identical. Keep both title and surname in the question."),
}


def main():
    assert not OUTPUT.exists() and base.digest(SOURCE) == SOURCE_SHA
    packet, parent = map(base.load, (SOURCE, pairs.parent.RELEASE))
    assert packet["candidate_sha256"] == parent["candidate_sha256"] == base.digest(pairs.parent.ROM)
    assert base.digest(base.REGISTRY) == parent["registry_sha256"]
    rows = []
    for group in packet["groups"]:
        route, block, path = group["route"], group["block"], group["file_path"]
        wanted = pairs.LEADS[route][block]
        [r] = [row for row in group["records"] if row["current_offset"] == wanted]
        speaker, context, meaning, english, phrases, note = DECISIONS[route, block]
        assert Counter(TOKEN.findall(english)) == Counter(TOKEN.findall(r["Japanese"]))
        assert Counter(TOKEN.findall(english)) == Counter(TOKEN.findall(r["current_English"]))
        assert r["native_command_word"] == 0x4000 and english.isascii()
        source_hex = bytes([r["selector"]]).hex() + r["source_body_hex"]
        current_hex = bytes([r["selector"]]).hex() + r["current_body_hex"]
        src, old = (dict(file_path=path, block=block, offset=r[f"{side}_offset"],
                         command_offset=r[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                         exact_stored_hex=encoded) for side, encoded in (("source", source_hex), ("current", current_hex)))
        src["record_index"] = r["source_record_index"]
        rows.append(dict(id=f"DK4_MES_B{block}_R{r['source_record_index']:04}", route=route, block=block, file_path=path,
                         source_reference=src, current_reference=old, source_hex=source_hex, current_hex=current_hex,
                         source_selector=r["selector"], native_slots=[], native_command_word=0x4000, kind="progressive",
                         Japanese=r["Japanese"], previous_English=logical(r["current_English"]), english=english,
                         speaker=speaker, context=context, source_meaning=meaning, localization_note=note,
                         protected_phrases=list(phrases), decision="revision",
                         review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert len(rows) == len(DECISIONS) == 17
    draft = dict(source_packet_sha256=SOURCE_SHA, previous_sha256=parent["candidate_sha256"],
                 previous_registry_sha256=parent["registry_sha256"], translation_policy="natural-dialogue-v2",
                 target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=list(GATES),
                 records=rows, new_coverage_credit=0,
                 formatting_and_registration_pending=True)
    base.save(OUTPUT, draft)
    print("Reviewed 17 question-tag and phrase-wrap records against the clean Japanese.", flush=True)


if __name__ == "__main__":
    main()
