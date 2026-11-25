"""Bind editorial decisions for the sea-war, diplomacy, relic and letter exchanges."""

from collections import Counter
from pathlib import Path
import sys
from types import FunctionType

from scripts import register_story_phrase_continuity_20261118 as parent
from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts.review_london_guild_assignments_20261118 import TOKEN, base, logical

ROOT = Path("work/story_followup_exchanges_20261118")
SOURCE = ROOT / "paired_source.json"
SOURCE_SHA = "76fe04a1a1435aa5dffa7bbe5d1461ff1e4d61b554cd45f1e468b5acde463a9c"
OUTPUT = ROOT / "followup_prose_v3.json"
BLOCKS = ((143, 152, 163, 166, 221, 249), (240,), (237,), (210,))
GATES = ["source", "context", "localization", "naturalness", "formatting"]

# Source meaning, replacement paragraph, protected phrases, editorial reason.
TUTORIAL = {
    372: ("War can begin by attacking the fleet at sea or having the First Mate write a document at the guild.",
          "Right. Attack their fleet at sea, or have your First Mate write a declaration of war at the Guild.",
          ("attack their fleet at sea,", "your First Mate", "a declaration of war", "at the Guild."),
          "Keep both ways of starting a war and the first mate's and guild's roles."),
    375: ("Rafael says he follows.", None, (), "A short acknowledgment gives Fernan room to explain the effects."),
    380: ("Winning a sea battle against a wartime enemy lowers its reputation and slightly reduces its share in nearby towns.",
          None, (), "The registered one-page lesson gives both consequences and the war condition in a clear order."),
    383: ("Quickly securing a town contract lets the player oust the rival from that town by investing alone.",
          "Get a contract in a nearby town right away. After that, you can drive them out just by investing.",
          ("Get a contract", "right away.", "just by investing."),
          "Make the timing and the condition for investment clear."),
    387: ("Rafael realizes this also allows a contract in a town another faction controls completely.",
          "(Right! We could get a contract even in a town another faction controls completely!)",
          ("get a contract", "controls completely!"),
          "Keep the quick internal realization and full monopoly, which is the payoff of the tutorial."),
    392: ("Investment alone cannot dissolve the Espinosa Company.", None, (),
          "Fernan's short exception preserves the distinction between evicting a rival from one town and dissolving it."),
}
DIPLOMACY = {
    128: ("Duarte asks Rafael to consider his position as Portuguese governor of Indochina under the King of Spain.",
          None, (), "The current line lets Duarte state the diplomatic constraint in his direct voice."),
    131: ("Rafael asks whether helping people deemed dangerous would risk displeasing the King of Spain.",
          "So helping troublemakers like us would risk angering the King of Spain?",
          ("troublemakers like us", "the King of Spain?"),
          "Keep Rafael's pointed question and the royal title. He is testing what follows from Duarte's explanation."),
    136: ("Many livelihoods depend on Duarte, and caring for those people is the hard part of being governor.",
          None, (), "The three short statements keep Duarte's responsibilities personal and blunt."),
    140: ("Duarte might help if they take on Antony Kuhn, the Dutchman in Indonesia.",
          None, (), "Keep Duarte's scorn for Kuhn, the location and his tentative offer. He spells out its limit next."),
    144: ("World politics let him help fight Kuhn because Spain also considers him an enemy. Duarte cannot help in other matters.",
          "That's world politics for you. Kuhn is Spain's enemy, too, so I can help you defeat him. That's as far as my help goes.",
          ("That's world politics for you.", "Spain's enemy, too,", "That's as far as my help goes."),
          "Give the exception and the limit their own beats while keeping Duarte's matter-of-fact voice."),
}
LAMP = {
    5: ("Rafael still thinks the Patterned Cloth is the map to the Mediterranean Proof of Conquest.",
        "The Patterned Cloth is the map to the Proof of Conquest in the Mediterranean, right?",
        ("The Patterned Cloth", "Proof of Conquest", "in the Mediterranean, right?"), "Use both approved item names and keep the tentative question."),
    17: ("Janus has stared at the cloth and still cannot see a map.",
         "I've looked and looked, but it still doesn't look like a map.",
         ("I've looked and looked,", "look like a map."), "Janus's reply conveys the effort and the same conclusion without redundant verbal structure."),
    23: ("Clau cannot see well in the dark and asks for the nearby Brass Lamp.",
         None, ("Pass me that Brass Lamp.",), "Clau's clipped delivery fits his practical response. Keep his whole request together."),
    27: ("Rafael agrees with a little surprise.", None, (), "A brief, hesitant assent lets Clau take the lead."),
    32: ("Clau holds the lamp closer and can now see.", None, (), "The pause has a physical reason as he moves the lamp."),
    35: ("Rafael blurts out a warning that the cloth could burn, then sees the map.",
         None, (), "The stammer, urgent warning and sudden discovery track the action in order."),
    40: ("Rafael recognizes a map.", None, (), "The short trailing reaction lets the discovery register."),
    51: ("Rafael did not think of using heat from the Brass Lamp to make the image appear.",
         "I never thought the heat from the Brass Lamp would reveal the markings.",
         ("heat from the Brass Lamp", "reveal the markings."), "Keep the mechanism explicit and the Brass Lamp with the heat it supplies."),
    57: ("Janus realizes how the lamp was meant to be used and is surprised that heat exposed the image.",
         "So that's how we were meant to use the Brass Lamp. Who would have guessed the heat would reveal it?",
         ("use the Brass Lamp.", "Who would have guessed", "the heat would reveal it?"), "Keep Janus's realization and disbelief separate."),
    64: ("Clau stammers and claims it was a good idea.", None, (), "His sudden uncertainty makes Rafael's reply land."),
    73: ("Rafael says this was a good result for an accident.", None, (), "The dry understatement fits his friendly jab."),
    80: ("Arcadius agrees and repeats the remark about the lucky accident.",
         "Indeed. Quite good for an accident.", ("Quite good for an accident.",),
         "Preserve the deliberately repeated joke in Arcadius's more formal voice."),
    87: ("Clau has no answer.", None, (), "Keep the embarrassed hesitation after both friends call it an accident."),
    91: ("Now that they have the map, Rafael says the only thing left is to find the Mediterranean Proof of Conquest.",
         "All right! We have the map. Now we just have to find the Proof of Conquest in the Mediterranean!",
         ("All right! We have the map.", "Proof of Conquest", "in the Mediterranean!"),
         "End with Rafael's momentum and the approved item title. The map and Proof remain distinct."),
}
CROWN = {
    85: ("The king hears that showing the Pope the seven Proofs Rafael gathered will lead the Pope to press for restoration of Portuguese royal authority.",
         "I hear the Pope will back the Portuguese Crown's claim to rule again if we show him the seven Proofs of Conquest you found.",
         ("the Pope will back", "the Portuguese Crown's", "seven Proofs of Conquest"),
         "Keep the hearsay, the seven Proofs and the Pope's support for restored authority without promising the outcome."),
    88: ("Rafael is astonished.", None, (), "The formal, short reply fits his audience with the king."),
    96: ("The king calls Rafael a treasure of Portugal, a nation built on seafaring.", None, (),
         "The seafaring comparison and praise already carry the king's voice."),
    100: ("In the Portuguese king's name, Rafael is appointed viceroy over all Portugal's overseas trade territories, called the Estado.",
          "In the King of Portugal's name, you are now viceroy of the Estado, all our overseas trade territories!",
          ("the King of Portugal's name,", "viceroy of the Estado,", "overseas trade territories!"),
          "Keep the full royal title, new office, Portuguese term and complete territory scope."),
    103: ("Rafael is stunned and stammers at the appointment.", None, (), "The stammer and the form of address convey both surprise and deference."),
}
LETTER = {
    27: ("Yukihisa has heard of the renowned cursed Muramasa blades, considered a bane of Tokugawa, ruler of Japan. The swords face destruction.",
         "The fabled Muramasa blades carry a curse said to bring ill fortune to Tokugawa, ruler of Japan. They are marked for destruction.",
         ("fabled Muramasa blades", "ill fortune", "Tokugawa, ruler of Japan.", "marked for destruction."),
         "Keep the formal written voice, curse, target and threatened destruction."),
    30: ("A clan hostile to Tokugawa appears to have hidden one sword in East Asia, which Yukihisa wants the recipient to know.",
         "A clan that bears Tokugawa a grudge seems to have hidden one blade in East Asia. I thought you should have word of it.",
         ("Tokugawa a grudge", "one blade in East Asia.", "have word of it."),
         "Preserve who hid the sword, the hearsay qualifier and the report's formal tone."),
    33: ("Yukihisa is sure it is the blade he has searched for all these years. The letter ends with his full signature.",
         None, (), "Keep the signature on its own line. The intervening space marks the end of the letter."),
}
ARROW_OPEN = ("Cesare is indignant at the crew's neglected duties, then explains that Demon-Piercing Arrow is the grand name they keep saying.",
    "They should be working! Demon-Piercing Arrow, indeed! Oh, that's its name. Rather grand, isn't it?",
    ("They should be working!", "Demon-Piercing Arrow, indeed!", "Oh, that's its name.", "Rather grand, isn't it?"),
    "Keep Cesare's indignation, the moment he clarifies the name, and the dry judgment.")
ARROW_ABILITY = ("It is rumored to grant remarkable archery skill. The sailors wonder if that extends to cannons and neglect maintaining the ship.",
    "It makes you a master archer, or so they say. The men wonder if it works on cannons. No one's tending the ship!",
    ("It makes you a master archer,", "works on cannons.", "No one's tending the ship!"),
    "Keep the rumor about the bow, the crew's guess about cannons and the consequence on deck. Give the complaint a full line.")
ARROW_WORK = ("Cesare says cannon practice would be more useful than speculating about the arrow.",
    "Cannon practice would do them more good than all this idle chatter!",
    ("Cannon practice", "all this idle chatter!"),
    "Keep the crew's actual alternative and Cesare's voice. The next turn moves on to the reports about the islands.")
ARROW_CONTEXT = "Cesare complains about the sailors' gossip, identifies the Demon-Piercing Arrow, relays the legend and explains why they should be practicing at the guns."
ARROWS = (
    (249, (15, 20, 23, 27, 31, 34), "Rafael's startled question and stammer elicit the legend."),
    (240, (14, 18, 21, 24, 28, 31), "Hodram asks what the arrow is. Cesare's compact answer carries the legend."),
    (237, (15, 19, 22, 25, 29, 32), "Lil asks what the item is and gives Cesare space to clarify."),
    (210, (13, 17, 20, 24, 28, 31), "Maria tells Cesare to slow down and asks him what the arrow is."),
)
CONTEXTS = {
    (0, 143): (TUTORIAL, "Fernan teaches Rafael how to turn a wartime naval victory into a local trade contract."),
    (0, 152): (DIPLOMACY, "Rafael tests the limits of Duarte's offer under Spanish authority, and Duarte names the one adversary he can help fight."),
    (0, 163): (LAMP, "The crew doubts the cloth is a map until Clau brings the lamp close. The heat reveals the image, and they joke that he stumbled on it."),
    (0, 166): (CROWN, "The King of Portugal explains what might happen after showing the Pope the Proofs of Conquest and then appoints Rafael viceroy."),
    (0, 221): (LETTER, "Yukihisa's formal letter reports the threatened destruction of the Muramasa blades, one hidden sword and his personal interest."),
}
for route, (block, ids, question_note) in enumerate(ARROWS):
    first, intro, question, legend, ability, work = ids
    CONTEXTS[route, block] = ({
        first: ("The captain reacts briefly to Cesare's dismissal of the rumors.", None, (), "Keep the brief cue that prompts Cesare to explain."),
        intro: ARROW_OPEN,
        question: ("The captain asks what Cesare is talking about.", None, (), question_note),
        legend: ("An angel reportedly used the arrow to strike down a demon.", None, (),
                 "The installed wording states the legend as hearsay in Cesare's polite register. Hodram's wording answers the item question directly with a pronoun."),
        ability: ARROW_ABILITY,
        work: ARROW_WORK,
    }, ARROW_CONTEXT)

def main():
    assert not OUTPUT.exists() and base.digest(SOURCE) == SOURCE_SHA
    data, release = map(base.load, (SOURCE, parent.RELEASE))
    assert data["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    actors = base.load(Path("translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json"))["records"]
    found, records = set(), []
    for group in data["groups"]:
        route, block, path = group["route"], group["block"], group["file_path"]
        choices, context = CONTEXTS[route, block]
        for row in group["records"]:
            idx, selector = row["source_record_index"], row["selector"]
            if idx not in choices:
                continue
            assert (route, block, idx) not in found and row["native_command_word"] == 0x4000
            found.add((route, block, idx))
            meaning, proposed, phrases, note = choices[idx]
            previous = logical(row["current_English"])
            english = previous if proposed is None else proposed
            assert english.isascii() and not TOKEN.search(english) and not TOKEN.search(row["Japanese"])
            finding = "prose" if english != previous else "wrap" if phrases else "retention"
            source, current = (dict(file_path=path, block=block, offset=row[f"{side}_offset"],
                command_offset=row[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                exact_stored_hex=bytes([selector]).hex() + row[f"{side}_body_hex"]) for side in ("source", "current"))
            source["record_index"] = idx
            name = actors[selector]["current_consumers"][0]["text"]
            records.append(dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block,
                kind="progressive", native_command_word=0x4000, source_selector=selector, native_slots=[],
                source_reference=source, current_reference=current, source_hex=source["exact_stored_hex"],
                current_hex=current["exact_stored_hex"], Japanese=row["Japanese"], previous_English=previous,
                english=english, context=context, speaker=name, source_meaning=meaning, localization_note=note,
                protected_phrases=list(phrases), finding=finding, decision="retention" if finding=="retention" else "revision",
                review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert found == {(r,b,i) for (r,b),(choices,_) in CONTEXTS.items() for i in choices}
    counts = dict(Counter(r["finding"] for r in records))
    base.save(OUTPUT, dict(source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=GATES, records=records, decisions=counts,
        new_coverage_credit=0, formatting_and_registration_pending=True))
    print(counts)


if __name__ == "__main__":
    if sys.argv[1:] == ["--pair"]:
        scope = vars(paired) | dict(ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=("Rafael", "Hodram", "Lil", "Maria"), parent=parent)
        FunctionType(paired.main.__code__, scope)()
        assert base.digest(SOURCE) == SOURCE_SHA
    else:
        assert not sys.argv[1:]
        main()
