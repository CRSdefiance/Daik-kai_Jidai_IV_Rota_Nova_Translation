"""Review map and Proof terminology in the original conversations."""

from collections import Counter
from pathlib import Path
import sys
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_story_followup_20261118 as parent
from scripts.review_london_guild_assignments_20261118 import TOKEN, base, logical

ROOT = Path("work/regional_proof_dialogue_20261118")
SOURCE = ROOT / "paired_source.json"
SOURCE_SHA = "b9103011c1b965f9d03291b94ca26d6c356fd420e534747b41ba96370930ec10"
OUTPUT = ROOT / "regional_proof_prose_v3.json"
BLOCKS = ((41, 71, 153, 157, 160), (), (145, 153), (47, 298))
GATES = ["source", "context", "localization", "naturalness", "formatting"]


def keep(meaning, note):
    return meaning, None, (), note


CONTEXTS = {
    (0, 41): ("Clau asks Hans why they have no lead. Rafael asks where to look, and Hans explains the need for power and the trust of local people.", {
        26: ("Clau asks Hans whether they should have found a clue to the Proof said to be in Africa by now.",
             "Hans, isn't it about time we found a clue to the Proof of Conquest in Africa?",
             ("isn't it about time", "Proof of Conquest", "in Africa?"),
             "Use the established title in the opening question. Keep Clau's impatience and his concern about getting a lead."),
        29: keep("Hans says hurrying will achieve nothing.", "The short answer sounds like Hans and draws out Rafael's real question."),
        33: keep("Rafael asks how to find a clue.", "The hesitant transition gives Hans room to explain."),
        37: keep("Hans says someone who would rule the seas first needs enough power for the Proof to reveal itself.",
                 "Keep the personification and the general idea of power. The crew supplies several interpretations next."),
        40: keep("Clau asks if power means a big fleet.", "The practical guess contrasts with Hans's broader idea."),
        43: keep("Rafael wonders whether Hans means becoming a capable seafarer.", "The tentative wording suits a captain thinking about what he needs to learn."),
        55: keep("Janus suggests it might mean financial power.", "The short alternative works after the other two guesses."),
        69: keep("Julio suggests control of a large trading area.", "The brief question preserves a third interpretation without settling the matter."),
        75: keep("Hans says people interpret it differently. It could mean all of these.",
                 "The cautious conclusion keeps every option open and sets up his next condition."),
    }),
    (0, 71): ("Rafael's crew reacts after Kurushima's defeat. A town contact asks about the Proof and points them to Admiral Maria Li in Hangzhou.", {
        5: keep("Rafael reflects that Kurushima is gone.", "The short pause gives Clau room to look ahead."),
        10: keep("Clau thinks the defeat may make the East Asian Proof attainable.", "The region qualifies the shorthand, and the next speaker names the quest item in full."),
        13: keep("The contact notices that Kurushima is gone.", "The speaker echoes the news from outside the crew."),
        17: keep("Clau agrees with a pleased chuckle.", "The informal two beats preserve his voice."),
        27: keep("The contact asks if they are looking for the Proof of Conquest.", "The full title fits the direct question and establishes what the crew is seeking."),
        30: keep("Rafael confirms it and asks what the contact knows.", "His direct answer keeps the inquiry moving."),
        34: keep("The contact has heard that Admiral Li in Hangzhou may know something.", "Keep the rumor and both the title and location."),
        39: keep("Rafael politely asks where he can find Admiral Maria Li.", "The name and rank remain accurate."),
    }),
    (0, 153): ("The crew uses the liquid from the Lotion Jar to polish the Ancient Kingdom Coin. Part of its surface dissolves and a map appears.", {
        5: keep("Rafael notices that the Ancient Kingdom Coin is very dirty.", "His simple observation sets up the experiment."),
        9: keep("Clau proposes polishing it and points to the Lotion Jar.", "His suggestion names the second object without claiming he knows what it does."),
        12: keep("Rafael wonders what the liquid is and tries it anyway.", "The quick shift from hesitation to action fits his curiosity."),
        17: keep("Rafael voices the rubbing sound.", "The short sound conveys the action between his decision and the warning."),
        26: keep("Rafael panics, then notices something unexpected.", "The sudden change in reaction matches the discovery."),
        30: keep("A second pattern appears and Rafael thinks it looks like a map.", "The inference remains tentative."),
        40: ("Clau identifies the map to the Proof of Conquest in Southeast Asia and realizes the surface had to dissolve first.",
             "So the map leads to the Proof of Conquest in Southeast Asia! The surface had to dissolve first.",
             ("Proof of Conquest", "in Southeast Asia!", "The surface had to dissolve first."),
             "Name the destination and keep his quick, practical explanation of what happened to the coin."),
        46: ("Arcadius identifies the map to the Proof in Southeast Asia and observes that dissolving the surface reveals the image.",
             "The map to the Proof of Conquest in Southeast Asia! So the surface dissolves to reveal it...",
             ("Proof of Conquest", "in Southeast Asia!", "dissolves to reveal it..."),
             "Use the same quest name while giving Arcadius a more measured, trailing realization."),
        53: keep("Clau is glad they now know where to find the Southeast Asian Proof.", "The shorthand is clear immediately after the map is identified."),
        57: keep("Rafael is relieved that the entire coin did not dissolve.", "The quiet joke lands after Clau's enthusiasm."),
    }),
    (0, 157): ("Rafael fits the knife into the sheath. A flash startles him, he drops the knife, and the crew finds a map on its blade.", {
        5: keep("Rafael wonders what the Ceremonial Knife is used for.", "Keep the approved item name and his uncertain opening."),
        9: keep("Clau warns that even a small knife is still sharp and tells Rafael to put it away.", "The clipped warning sounds like Clau."),
        13: ("Rafael notices the Sun-Crest Sheath is the right size and decides to put the knife into it.",
             "Right. The Sun-Crest Sheath is just the right size. I'll put it in there...",
             ("The Sun-Crest Sheath", "the right size.", "I'll put it in there..."),
             "Make the immediate action and the correct sheath clear. The pause leaves room for the flash."),
        18: keep("Clau stammers in surprise at the light.", "The stammer and sudden exclamation follow the flash."),
        22: keep("Rafael is dazzled by the light.", "A two-word reaction fits the brief glare."),
        29: keep("The glare dies down, and Rafael wonders what it was.", "The relief comes before the question."),
        33: keep("Clau sees the knife on the ground.", "A short observation points Rafael to the next action."),
        37: keep("Rafael explains he dropped the knife in surprise.", "The admission follows naturally from Clau's observation."),
        41: keep("Rafael sees a map on the blade.", "The pause and the specific location make the detail legible."),
        46: ("Clau recognizes a map and is sure it leads to the Proof of Conquest in the New World.",
             "That's a map! It must show where to find the Proof of Conquest in the New World!",
             ("That's a map!", "Proof of Conquest", "in the New World!"),
             "Keep his excited inference. The map shows the way to the Proof."),
        49: keep("Rafael agrees they can now find the Proof but still finds what happened strange.", "The short name works after Clau's full identification."),
    }),
    (0, 160): ("The crew uses the Bamboo Assembly Plan to take the Tang Bamboo Craft apart and discovers a drawing inside. The variants recognize the drawing as a map.", {
        41: keep("Yifa denies breaking the craft and points to the Bamboo Assembly Plan.", "The immediate correction and the item name already work."),
        44: keep("Rafael realizes the plan shows how to take the craft apart and rebuild it.", "The line preserves both actions."),
        48: keep("Yifa is pleased and says she has disassembled it completely.", "Her enthusiasm supports Rafael's reaction."),
        51: keep("Rafael praises her dexterity and notices a drawing on the bamboo.", "The abrupt turn toward the drawing marks the discovery."),
        65: ("Janus tentatively recognizes a map and asks whether it could be the one to the East Asian Proof of Conquest.",
             "A map, perhaps... Could it lead to the Proof of Conquest in East Asia?",
             ("A map, perhaps...", "Proof of Conquest", "in East Asia?"),
             "Preserve Janus's tentative voice and name what the map leads to."),
        69: keep("Rafael agrees and says they should set out to look.", "The shift from speculation to action suits Rafael."),
        75: ("Yifa reacts with surprise, recognizes a map and realizes it leads to the Proof.",
             "Whoa! A map to the Proof!",
             ("A map to the Proof!",),
             "Use Yifa's excited reaction and explain what the map does. The source uses a short reference in this turn."),
        79: keep("Rafael credits Yifa and says to look for the Proof in East Asia.", "The reward is recognition for her work and a clear next destination."),
    }),
    (2, 145): ("Lil and Fernando try combining the Patterned Cloth and Brass Lamp. Heat reveals the map that Lil suspected was hidden.", {
        5: ("Lil suspects the Patterned Cloth might be the map to the Mediterranean Proof of Conquest.",
            "I think the Patterned Cloth might be the map to the Proof of Conquest in the Mediterranean.",
            ("the Patterned Cloth", "Proof of Conquest", "in the Mediterranean."),
            "Use the full item name with Lil's uncertainty intact."),
        9: keep("Fernando thinks the Brass Lamp is connected and the two items must be used together.", "His informal deduction gives Lil something to try without explaining the answer in advance."),
        13: keep("Lil lights the lamp and asks what to do next.", "The brief pause marks the action."),
        16: ("Fernando proposes a long-shot experiment to use heat to reveal something.",
             "It's a long shot. What if we warm the cloth and see what shows up?",
             ("It's a long shot.", "What if we warm the cloth", "see what shows up?"),
             "Let Fernando propose the heat without claiming he already knows what it will reveal."),
        19: ("Lil sees promise in his idea and starts to heat the Patterned Cloth.",
             "Heat it! That could work. Let's try heating the Patterned Cloth...",
             ("Heat it!", "That could work.", "Let's try heating", "the Patterned Cloth..."),
             "Keep the excited echo, agreement and unfinished thought as she tries it."),
        23: ("Lil is delighted to have found the map to the Mediterranean Proof and wants to look for it right away.",
             "The map to the Proof of Conquest in the Mediterranean! We did it! Come on, let's go find it!",
             ("We did it!", "Proof of Conquest", "in the Mediterranean!", "let's go find it!"),
             "Make the discovery and the next step clear while keeping Lil's enthusiasm."),
    }),
    (2, 153): ("Lil and Camille try the Lotion Jar on the Ancient Kingdom Coin. The coin reveals a map, and Lil says they still have work to do.", {
        5: keep("Lil starts from the possibility that the coin is a map to the Proof.", "The trailing inference gives Camille room to propose a missing step."),
        8: keep("Camille wonders whether another object is needed.", "His tentative question connects to Lil's next guess."),
        11: keep("Lil identifies the Lotion Jar but asks how to use it.", "The named object and the practical problem both stay clear."),
        14: keep("Camille suggests putting the coin in the jar.", "The short question fits the experiment and makes no promise."),
        18: keep("Lil agrees to try it.", "Her assent marks the action, not its outcome."),
        22: keep("Lil voices the sound of scrubbing.", "The playful repetition reads naturally while the coin is rubbed."),
        26: keep("The coin's surface dissolves, and Lil recognizes the drawing as a map.", "The excitement follows the physical change."),
        29: ("Camille identifies the map to the Southeast Asian Proof too and praises Lil by her given name.",
             "We've got the map to the Proof of Conquest in Southeast Asia, too! You're amazing, FI!",
             ("Proof of Conquest", "in Southeast Asia, too!", "You're amazing, FI!"),
             "Keep the additional map, the location, and Camille's personal praise with the original substitution."),
        33: keep("Lil tells Camille the map is only the start and urges him to find the Proof.", "Her practical response contrasts with his celebration and preserves the short name after the full title."),
    }),
    (3, 47): ("After the townspeople take Espinosa away, a shopkeeper offers Maria something Espinosa had and explains their hopes for the region.", {
        125: keep("Maria reacts without yet knowing what is being offered.", "The small puzzled response precedes the actual handover."),
        129: keep("The shopkeeper asks her to accept the item.", "The spare phrasing keeps the offer respectful."),
        136: keep("Maria asks what the item is.", "The short question gives the shopkeeper the next turn to explain."),
        140: ("The shopkeeper says Espinosa had the item and had long searched for Africa's Proof of Conquest as well. The townspeople prayed the Proof would never fall into his hands.",
              "Espinosa had this. He'd long sought Africa's Proof of Conquest, too. We prayed he'd never find it...",
              ("Espinosa had this.", "Africa's Proof of Conquest, too.", "We prayed he'd never find it..."),
              "Correct the title and distinguish the thing Espinosa had from the Proof the townspeople hoped he would never acquire."),
        143: keep("The shopkeeper says Maria is worthy of ruling these waters and asks her to find the treasure and bring peace and prosperity.", "The formal appeal and the two desired outcomes remain clear."),
        147: keep("Maria thanks them and promises to try to live up to their hopes.", "Her measured response preserves the difference between accepting their trust and guaranteeing an outcome."),
        157: keep("Xien tells Maria to look at the townspeople waving to her.", "The observation turns her attention to the crowd."),
        163: keep("Another companion politely points out the townspeople waving.", "Keep the same event in the alternate speaker's more formal address."),
        170: keep("Maria notices how different this is from her time in Ming.", "The reflective pause preserves her surprise."),
    }),
    (3, 298): ("A villager fears another seizure by overseas conquerors. Maria refuses to take the Proof by force. Xien warns that other conquerors may threaten the village, and the villager ultimately chooses to trust Maria.", {
        19: keep("The villager says he would rather die than hand it over.", "The direct refusal establishes the fear that shapes the exchange."),
        22: keep("Maria calms him and promises not to use force.", "Her controlled response sets up why his fear persists."),
        25: keep("The villager says people from across the ocean have spoken this way and then taken everything.", "The source's accusation and distrust stay intact."),
        29: keep("Maria realizes he sees her as another Western conqueror.", "Her quiet realization belongs before her decision to leave it."),
        33: keep("The villager falls silent.", "The pause leaves room for Maria to reconsider."),
        37: keep("Maria says they will give up the search here.", "The calm decision prompts Xien's startled question."),
        41: ("Xien calls Maria by her given name and asks if she will give up on the New World's Proof.",
             "FI! Are you giving up on the Proof of Conquest in the New World?",
             ("giving up on", "Proof of Conquest", "in the New World?"),
             "Keep his sharp address and disbelief. The full term makes clear what she is choosing to leave behind."),
        45: keep("Maria says they cannot force the locals to surrender the item.", "The reply states her reason plainly."),
        49: keep("Xien says other conquerors could take it by force and undo their work.", "The conditional warning preserves both the threat and the accumulated effort."),
        52: keep("Maria pauses before Xien adds his strongest reason.", "Her silence lets his warning develop."),
        56: keep("Xien says the villagers would also suffer if that happened.", "His emphasis shifts to the danger to the people."),
        59: keep("The villager asks whether they are threatening him.", "The question reveals how easily a warning sounds like another ultimatum."),
        62: keep("Maria denies that intent, then hesitates.", "The trailing objection leaves Xien room to explain."),
        65: keep("Xien says Escante's threat is gone but Spain is unlikely to give up on the New World.", "The distinction between Escante and Spain grounds his prediction."),
        68: keep("The villager asks what happened to Escante.", "His surprise opens the original alternatives about the outcome."),
        100: keep("The villager says he will trust Maria and prays that she brings true peace to this land.", "The change of heart remains his choice."),
        107: keep("Maria thanks him and promises to do all she can.", "The reply expresses commitment without promising success."),
    }),
}


def main():
    assert not OUTPUT.exists() and base.digest(SOURCE) == SOURCE_SHA
    data, release = map(base.load, (SOURCE, parent.RELEASE))
    assert data["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    actors = base.load(Path("translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json"))["records"]
    found, records = set(), []
    for group in data["groups"]:
        route, block, path = group["route"], group["block"], group["file_path"]
        context, choices = CONTEXTS[route, block]
        for row in group["records"]:
            idx, selector = row["source_record_index"], row["selector"]
            if idx not in choices:
                continue
            key = route, block, idx
            assert key not in found and row["native_command_word"] == 0x4000
            found.add(key)
            meaning, proposal, phrases, note = choices[idx]
            previous = logical(row["current_English"])
            english = previous if proposal is None else proposal
            macros = TOKEN.findall(english)
            assert english.isascii() and macros == TOKEN.findall(previous) == TOKEN.findall(row["Japanese"])
            finding = "retention" if proposal is None else "prose"
            source, current = (dict(file_path=path, block=block, offset=row[f"{side}_offset"],
                command_offset=row[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                exact_stored_hex=bytes([selector]).hex() + row[f"{side}_body_hex"]) for side in ("source", "current"))
            source["record_index"] = idx
            records.append(dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block,
                kind="progressive", native_command_word=0x4000, source_selector=selector, native_slots=[],
                source_reference=source, current_reference=current, source_hex=source["exact_stored_hex"], current_hex=current["exact_stored_hex"],
                Japanese=row["Japanese"], previous_English=previous, english=english, context=context,
                speaker=actors[selector]["current_consumers"][0]["text"], source_meaning=meaning, localization_note=note,
                protected_phrases=list(phrases), finding=finding, decision="retention" if proposal is None else "revision",
                review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert found == {(r, b, i) for (r, b), (_, choices) in CONTEXTS.items() for i in choices}
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
