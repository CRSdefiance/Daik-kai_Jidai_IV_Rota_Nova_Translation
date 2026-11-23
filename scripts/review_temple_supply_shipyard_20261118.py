"""Review the remaining temple, supply and shipyard exchanges against their exact Japanese."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import bind_remaining_mosque_temple_shipyard_20261118 as paired
from scripts import review_jungle_caves_20261118 as binder
from scripts.source_locked_derivation_v5118 import checked_text

base, parent = paired.base, paired.latest
SOURCE = paired.OUT
SOURCE_SHA = "56f8cd274c2fb8611e3a336292f98b25ee290f32416b26d84bfa8b2818edfc59"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/temple_supply_shipyard_20261118_prose_v5.json")
BLOCKS = ((), *paired.original.BLOCKS[1:])

# Recheck the complete exchange before accepting or adjusting a draft. A None
# value explicitly retains the previously registered wording.
FINAL = {
    (1, 140): "Ah, I forgot it.",
    (1, 156): "Shallower than I thought. What a relief.",
    (1, 182): "Yes. I think you'll manage.",
    (1, 161): "That should have saved us quite a detour.",
    (1, 164): "This swamp looks impassable. Let's go back and try another way.",
    (1, 175): "I'll go partway with you. Your map should get you there.",
    (1, 188): "Never give the Proof of Conquest to anyone who means harm. Resist such desires yourself.",
    (1, 190): "Admiral, let's meet the clan guarding the map to the Proof. The village was far northeast of China, right?",
    (1, 191): "Admiral, let's hurry to meet the clan that guards the Proof's map. Their village lies far northeast of China.",
    (1, 192): "What's that clan like, Admiral? The one guarding the Proof's map. Way northeast of China, right? Let's go!",
    (1, 193): "Admiral, let's visit the Proof's map guardians before we forget. Their village is far northeast of China, right?",
    (1, 194): "Admiral, let's go see the clan with the map to the Proof. Their village is way northeast of China, right?",
    (1, 195): "Admiral, we'd best visit the clan guarding the Proof's map. Shall we head to that village far northeast of China?",
    (1, 196): "Admiral, aren't you curious who guards the map to the Proof? Let's visit their village way northeast of China!",
    (1, 197): "Admiral, I'm curious about the map to the Proof. Shall we visit its guardian clan? Far northeast of China, was it?",
    (1, 177): "Kublai's Greatsword... So this is the Yuan emperor's keepsake the monk at Kinkaku-ji asked us to find.",
    (1, 262): "Hah... Hah... Are we safe here now?",
    (2, 175): "I'll go partway with you. Your map should get you there.",
    (2, 280): "Traders from the Indian Ocean coast are holding a spice exhibition. Some spices will be for sale.",
    (2, 281): "As you know, Basra doesn't trade in spices. We'll have to get them from other towns.",
    (2, 282): "We're busy setting up the exhibition. We've barely got enough for the displays, so we'll be short of spices to sell.",
    (2, 329): "Admiral, look at this map! Seems there's a log bridge upstream. Bit of a walk, though...",
    (2, 332): "The map seems to show a log bridge upstream. It's quite a distance from here, though...",
    (2, 349): "What would you like me to do next?",
    (2, 357): "I'm back! I bought the tea and sugar!",
    (2, 190): "Admiral, let's see the clan guarding the map to the Proof. Their village is far northeast of China, right?",
    (2, 191): "Admiral, let's hurry to meet the clan guarding the Proof's map. They live far northeast of China.",
    (2, 192): "Admiral, what's that clan like? The one guarding the Proof's map. They live way northeast of China, right? Let's go!",
    (2, 193): "Admiral, before we forget, let's meet the clan guarding the Proof's map. Their village is far northeast of China, right?",
    (2, 194): "Admiral, let's meet the clan guarding the Proof's map. They live way northeast of China, right?",
    (2, 195): "Admiral, we'd best see the clan guarding the Proof's map. Shall we try that village far northeast of China?",
    (2, 196): "Admiral, who do you think guards the map to the Proof? Let's go to that village way northeast of China!",
    (2, 197): "I'm curious about the Proof's map. Shall we visit that clan, Admiral? Far northeast of China, was it?",
    (3, 381): "Ever heard of a carronade? New invention from Europe. Long range, plenty of power.",
    (3, 409): "Our couriers keep getting sunk by pirates before they've gone far. Useless lot!",
    (3, 376): "I'll help if I can. What is it?",
    (3, 390): "Then I'll advise on shipbuilding.",
    (3, 415): "Oh, I forgot the map. I'd better get one.",
    (3, 419): "This place... I can't shake the feeling we've passed this spot a few times already.",
    (3, 434): "Seriously? You're just going to wing it?",
    (3, 428): "Trust your instincts",
}
NOTES = {
    121: "Use the same plain choice label as Rafael when the party retraces its steps.",
    134: "Keep the elapsed day and only apparent crew fatigue in the same system notice.",
    139: "The stammer precedes the report of a sighting. The object stays unspecified.",
    161: "Hodram draws a tentative conclusion about the shortcut after crossing.",
    164: "The swamp looks impassable. Hodram chooses to return and take a different route.",
    175: "Sakura goes partway with the party. The rest of the journey depends on the map.",
    177: "Keep the approved item and temple titles, the Yuan emperor and the connection to the monk's request.",
    183: "Keep the icy sea, far northeast of China and the likely location of the clan.",
    188: "The monk gives a warning about others' intentions and about Hodram's own desires.",
    260: "The crew is tired and some sailors appear to have left the group.",
    280: "The merchants come from the Indian Ocean coast and intend to sell spices at the exhibition.",
    282: "Setting up the exhibition leaves too little time to procure stock to sell.",
    295: "The nutmeg is short. Several other prompts report an absent commodity.",
    297: "Keep Pimento as catalogued and make the one-shipment requirement explicit.",
    306: "The item came in recently and is supposedly valuable. The contact still can't price it.",
    329: "Keep the tentative map reading, the upstream log bridge and the distance.",
    337: "Lil has the group cross in order once she discovers the ferry.",
    345: "The immediate earlier errand identifies the rice. Lil sounds tired after getting it.",
    357: "Name the tea and sugar from the preceding reminders as Lil returns.",
    360: "The elder notices progress in humility and courtesy even though her politeness isn't yet sincere.",
    369: "Distinguish spending on the shopping from payment for the errands.",
    381: "Keep the shipwright's account of a newly invented European cannon with long range and power.",
    395: "The shipwright asks for help when someone becomes available and is prepared to wait.",
    406: "Charles explains the in-game drawing of the barrel, powder and shot in that order.",
    411: "The guildmaster thanks the party on the shipwright's behalf.",
    419: "The repeated path is a strong impression. The speaker still trails off thoughtfully.",
    428: "A command-style caption parallels the compass option and leads to Maria trusting her judgment.",
    431: "Maria uses the midday sun to back up the compass. Keep the conclusion provisional.",
    434: "Jam challenges Maria's hunch in conversational English, setting up Xien's dry comeback.",
}
PHRASES = (
    "shallower than I expected.", "What a relief.", "before we forget,", "before we forget.", "not that deep.", "quite a detour.", "Let's go back and try another way.", "I'll go partway with you.", "Your map should get you there.",
    "One day has passed.", "your map should get you there.",
    "Ah! That's the very thing!", "Kublai's Greatsword...", "at Kinkaku-ji",
    "the Yuan emperor's", "near the icy sea,", "far northeast of China.", "far northeast of China,",
    "way northeast of China.", "way northeast of China,", "far northeast of China?", "northeast of China!",
    "Proof of Conquest", "with evil intentions.", "Resist such desires yourself.", "to anyone who means harm.",
    "map to the Proof.", "the Proof's map", "guardian clan?",
    "without a map.", "kept my footing...", "I'm truly sorry.", "if we treat it quickly.",
    "The wolf's gone now.", "The wolf's gone now, too.", "seem to be missing.", "There it is, Admiral.", "safe here now?",
    "Indian Ocean coast", "a spice exhibition.", "will be for sale.", "doesn't trade in spices.", "other towns.",
    "enough for the displays.", "spices to sell.",
    "as soon as you can.", "the whole shipment", "with the rest.",
    "what it's worth.", "Take care out there.", "in a flood or something.",
    "a log bridge upstream.", "It's a ways off, though.", "Bit of a walk, though...", "Your sailors look tired.",
    "a ferry over there!", "one at a time.", "what would you like", "the tea and sugar!",
    "humility and courtesy.", "(Oh, forget it...)", "a little for your trouble.", "shipbuilding and gunnery?",
    "Ever heard of a carronade?", "New invention from Europe.", "Long range, plenty of power.",
    "withstand their cannon fire.", "before they've gone far.", "we've got you to thank for it.",
    "on behalf of the shipwright.", "Let me thank you", "I'd better get one.", "a few times already.", "Going by the midday sun,",
    "the compass is right.", "going to wing it?", "getting out of here.",
)


def main():
    assert base.digest(SOURCE) == SOURCE_SHA and not OUTPUT.exists()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["complete_source_current_binding"] and packet["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    histories = [paired.history_index.index_history(path) for path in paired.HISTORY]
    hashes = [base.digest(path) for path in paired.HISTORY]
    scope = vars(binder).copy()
    source = checked_text(getsource(binder.review_one), {
        "if word == 0x2100:": "if word in (0x2100, 0x2200):",
        "if word == 0x2100 else": "if word in (0x2100, 0x2200) else",
    })
    exec(compile(source, __file__ + "::source-locked-two-and-three-choice-binding", "exec"), scope)
    seen, records = set(), []
    for group in packet["groups"]:
        route, block = group["route"], group["block"]
        for raw in group["records"]:
            ordinal = raw["packet_ordinal"]
            key = route, ordinal
            if key in FINAL:
                seen.add(key)
            chosen = FINAL.get(key, raw["proposed_English"])
            gloss = raw["earlier_gloss"]
            individual = NOTES.get(ordinal, gloss)
            if 190 <= ordinal <= 197 and chosen:
                individual = f"Keep the distinct companion's emphasis and distinguish the map from the Proof. {gloss}"
            old = histories[route - 1][block, raw["source_offset"]]
            env = scope | {
                "NOTES": (individual,), "EDITS": { (1, route): chosen } if chosen else {}, "PHRASES": PHRASES,
            }
            review_one = FunctionType(scope["review_one"].__code__, env)
            item = review_one(raw, group, old, 1, paired.HISTORY[route - 1], hashes[route - 1])
            item["context"] = raw["earlier_exchange_context"]
            item["source_meaning"] = gloss
            if item["decision"] == "retention":
                item["localization_note"] = f"Current wording preserves this beat in the exchange. {individual}"
            item["packet_ordinal"] = ordinal
            records.append(item)
    assert seen == FINAL.keys()
    assert len(records) == len({(r["file_path"], r["id"]) for r in records}) == 351
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        source_packet=str(SOURCE), source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], clean_input_sha256=release["clean_input_sha256"],
        formatting_and_registration_pending=True, additional_review_credit=0, records=records))
    print(binder.binder.Counter((r["kind"], r["decision"]) for r in records))


if __name__ == "__main__":
    main()




