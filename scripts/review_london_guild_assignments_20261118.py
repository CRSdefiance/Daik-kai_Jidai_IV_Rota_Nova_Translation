"""Record the contextual review of the guild assignments and their resolutions."""

from collections import Counter
from pathlib import Path
import re

from scripts import prepare_london_guild_assignments_20261118 as paired


base = paired.base
SOURCE = paired.ROOT / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/london_guild_assignments_20261118_prose_v4.json")
HISTORY = (
    "rafael_B281_B300_integrated_final_review_v1.json",
    "hodram_B281_B300_integrated_final_review_v1.json",
    "lil361_B283_B298_integrated_final_review_v1.json",
    "maria359_B253_B274_integrated_final_review_v1.json",
)
RIDDLE = "When light and darkness stand in balance"
CLUE = "it too lies between light and darkness"
SUMMONS = "There you are! You're FA, right? The London guild's looking for you."
THANKS = "Come back in a month and I'll have a reward for you. Thanks again!"
LONDON_SHARE = "Your share in London rose slightly!"
LATITUDE = "Brilliant, FI! With the latitude, this shadow lets us calculate where it'll fall on either equinox!"
APPROVAL = "Well done, FA! I knew I could count on you."

# A missing replacement retains the current paragraph. Each note records the
# line's function and why the wording works or needs to change in the exchange.
REVIEW = {
    (0, 294): [
        ("The messenger spots Rafael, checks his surname, and says the London guild has been looking for him.", SUMMONS),
    ],
    (0, 295): [
        ("Keep the guildmaster's dropped subject and brisk opening. He has a job for Rafael.",),
        ("Keep the conversational setup, nearby ruins and the men's recent comings and goings.",),
        ("The priest tends the ruins and was driven out. Give the guildmaster one clear description of the activity he dismisses.", "They drove out the priest who tends the ruins. Now they're holding what looks like a festival and calling it a ritual..."),
        ("The townspeople are scared because they don't know what goes on there. The guildmaster suspects crime without saying it has occurred.", "Nobody knows what they're up to, and people are scared. For all we know, the place could be a den of criminals..."),
        ("Keep the pivot from suspicion to the actual job. Rafael is to learn who the men are.",),
        ("Keep the practical assurance that the map makes the ruins easy to locate.",),
        ("Keep the reason for the shortage and the informal 'We're all out' after it.",),
        ("The guildmaster thinks Amsterdam still has copies and acknowledges the inconvenience. Avoid making the detour sound like something he hates.", "I think Amsterdam still has some. Sorry to send you out of your way, but could you pick one up there?"),
        ("Keep Rafael's quick question and the established Stone Circle Map item name.",),
        ("The guildmaster recognizes the map, credits Rafael for coming prepared, and entrusts him with the job.",),
    ],
    (0, 296): [
        ("Keep the verse's three celestial bodies in motion and its two occurrences of light and darkness. The listener needs to recognize the exact clue later.", f"The sun, moon, and stars circle. {RIDDLE}, {CLUE}."),
        ("Keep the pause and Claudio's incredulous admiration at the accurate recitation.",),
        ("Rafael restates the equivalence and wonders what the pronoun refers to. Keep the location between the two forces.",),
        ("Keep Claudio's brisk inference and the open question tag. They are assembling to find the thing.",),
        ("Keep the more tentative version of the deduction and the distinction between the ritual and its goal.",),
        ("Keep Rafael thinking aloud. The location follows from their inference and is still imprecise.",),
        ("Keep Claudio's direct question. Nothing has established why the group hasn't already found it.",),
        ("Keep the first companion's measured deduction. The date controls when they can identify the hiding place.",),
        ("Keep the younger voice's quick realization with the short reference to 'then'.",),
        ("Keep the conclusion as a thought in progress and its trailing hesitation.",),
        ("Keep the abrupt interruption and the rough voice's 'till' as the deduction clicks.",),
        ("Keep the measured 'Ah' and the focus on the place becoming clear.",),
        ("Keep the child's uncertainty as a question. Avoid implying that the cult itself hid the object.", "So maybe they won't know where it's hidden until then?"),
        ("Keep the older speaker's methodical 'In other words' and slightly formal register.",),
        ("The speaker is fairly sure they are unable to find it yet. Use that inference as the bridge into the required date.", "They probably can't find it yet. I think the hiding place will become clear on that day."),
        ("Keep Rafael's brief acknowledgment before Claudio raises the issue of timing.",),
        ("Keep Claudio's mild pushback and plain 'haven't got a clue'. It invites the next reading of the riddle.",),
        ("Keep the quoted phrase word for word and let Rafael trail off as he considers it.",),
        ("Keep the exact clue followed by the spoken association from light and darkness to day and night.",),
        ("Preserve Rafael's sudden realization that sunrise and sunset are the two transitions. Use 'balance' again to keep the link to the clue.", "Oh! Of course! If light and darkness mean day and night, they'd be in balance at sunrise or sunset!"),
        ("Keep Rafael's confident inference from the cult gathering at night. Another branch voices it more cautiously.",),
        ("Keep the interruption, exact clue, and tentative substitution of day and night for light and darkness.",),
        ("Rafael echoes the balance clue as a question and tries sunrise. Make it sound like a thought spoken aloud.", "When are day and night in balance? Could it be sunrise?"),
        ("Keep both possibilities and the qualified preference for sunrise based on the nighttime gathering.",),
        ("Let Claudio praise the deduction, then spot the problem. Sunrise comes every day.",),
        ("Keep the brief assent. The problem is valid and the speaker is still thinking.",),
        ("Keep Rafael's realization that equal length gives two days a year. This is his reasoning in the story.",),
        ("Keep the repeated question and then the sudden understanding without naming the equinoxes before Rafael.",),
        ("Keep the short, more restrained realization in the alternate branch.",),
        ("Keep the named spring and fall equinoxes. The short opening exclamation is a deliberate beat before Rafael names the answer.",),
        ("Keep Claudio's eager suggestion to get there and find the thing first.",),
        ("Keep Rafael's familiar 'Clau' when he gently points out that the group arrives the night before.",),
        ("Keep the alternate reply more tentative than Rafael's. The timing makes getting there first difficult.",),
        ("Keep Claudio's reluctant concession and the full reasoning about why going a day early won't help.",),
        ("Keep Rafael's open question. They have solved part of the puzzle and haven't found a way around the group.",),
    ],
    (0, 297): [
        ("Keep the proprietor's brief welcome before she recognizes the subject of the inquiry.",),
        ("Keep her conversational follow-up about the specific ruins.",),
        ("The proprietor passes along a theory she heard from customers. Keep both uses and the uncertainty.",),
        ("Keep Rafael repeating both ideas to himself. This leads to his insight about the stones.",),
    ],
    (0, 298): [
        ("The line echoes the earlier verse exactly. Retain 'too' and both sides of the contrast.",),
        ("Keep Rafael's reconstruction of the theory about standing stones. His certainty here is part of his thought process.",),
        ("Rafael's pause gives way to a single excited realization. Use idiomatic English punctuation.", "Wait... I've got it!"),
        ("Keep Claudio's short, surprised question before Rafael explains the idea.",),
        ("The shadow's tip is what the clue may describe. Keep the proposed sundial conditional.", "It must mean the tip of a shadow at the ruins. If the stone pillars were a sundial, the shadow would tell us something!"),
        ("Keep the latitude, present shadow position, and either equinox. Rafael states the calculation with confidence.",),
        ("Keep the praise, live first-name address, latitude and present position. Put both equinoxes in one compact phrase.", LATITUDE),
        ("The alternate speaker reaches the same result and uses the same first-name control. Keep the wording consistent.", LATITUDE),
        ("Keep Claudio's surprised reaction to a calculation he hadn't expected to be possible.",),
        ("Keep Rafael ending the discussion by suggesting that they try it at the ruins.",),
    ],
    (0, 299): [
        ("Keep Rafael talking himself through this morning's position and the expected reach of the longest shadow.",),
        ("Keep the quiet start and the more formal alternate inference. The speaker is estimating the location.",),
        ("Keep the third version's 'Let's see' and the same physical calculation without adding a direction or distance.",),
        ("Keep Claudio's direct transition from the calculation to digging.",),
        ("Keep the two digging sounds on the original speakerless system panel.",),
        ("Keep Claudio's quick reaction before Rafael names what they found.",),
        ("Keep Rafael's discovery of a stone box. Its contents are still unknown.",),
        ("Keep Claudio's offer to open it and the effort sound on the same turn.",),
        ("Claudio thinks the box is empty at first. Keep that apparent contradiction so Rafael can correct it.",),
        ("Keep Rafael drawing attention to something Claudio missed before either identifies it.",),
        ("Keep Claudio's stammer and anticlimactic dismissal of the scrap of paper.",),
        ("Keep Rafael's surprise at the blank sheet. Its lack of writing matters for the handover.",),
        ("Keep Claudio's two beats of confusion and his disbelief that this is what the group wanted.",),
        ("Keep Rafael saying the discovery should stop the plan. He fears becoming a sacrifice without claiming the group saw them.",),
        ("Claudio shudders at the thought and suggests reporting back. Give his reaction one quick spoken beat.", "That gives me the creeps. Come on, let's get back to town and tell the guild."),
    ],
    (0, 300): [
        ("Keep the guildmaster's gratitude, his report of a successful resolution, and the brief reward handover.",),
        ("Keep the received-reward notice, 10,000 amount and explicit gold denomination.",),
        ("Keep the small London share increase in the speakerless notice.",),
        ("Keep Rafael asking about the parchment. It is still a mystery even though the job is finished.",),
        ("Keep the uncertain connection to a Proof of Conquest. The unfinished sentence leaves room for Claudio's reply.",),
        ("Keep Claudio's practical conclusion that a blank sheet gives them little to go on.",),
        ("Keep Rafael's certainty that the paper is old and his repeated conviction that there is a secret, without naming the secret.",),
    ],
    (1, 292): [
        ("Keep the guildmaster greeting Hodram as the person he hoped to see before asking a favor.",),
        ("The guildmaster expects disbelief and says sightings are frequent. Make his report sound conversational.", "You may not believe this, but a monster keeps showing up in these waters."),
        ("Keep Hodram's one-word echo. He's taken aback by the report.",),
        ("Keep the fishers' name for the creature and what it does. Use a straightforward verb for biting the ships.", "The fishermen call it a monster fish. It takes bites out of ships and sinks them."),
        ("The guildmaster cites several ships attacked already this year. Make him speak directly about what the creature did.", "It's already chewed through several ships this year."),
        ("Keep the guildmaster's belief that Hodram might be able to stop the beast and the direct request to hunt it.",),
        ("Hodram's reservation is whether he will encounter it. Make his short answer sound like his own assessment.", "It'll take luck just to run into it."),
        ("The guildmaster is willing to wait and is relying on Hodram. Replace the stiff wording and generic good-luck wish.", "I can wait. I'm counting on you."),
    ],
    (1, 293): [
        ("Keep his exuberance and conviction that Hodram's success proves his abilities.",),
        ("Keep the joke as anxious relief that there may only have been one.",),
        ("Keep Hodram's short, disbelieving response so the guildmaster can backpedal immediately.",),
        ("Keep the hasty denial and the quick change of subject to the reward.",),
        ("Keep the speakerless 70,000 gold reward notice and its conventional concise phrasing.",),
        ("Keep the market-share gain small and retain the port name Malacca.",),
        ("The guildmaster remembers a rumor after the reward. Let the moment sound like a change of subject.", "Oh, that reminds me. I heard an interesting rumor."),
        ("Keep the report tentative. The ruins reportedly survive intact far inland in the jungle.",),
        ("Keep Hodram's brief, slightly formal question. It suits his interest in the rumor.",),
        ("Keep the distinction between rumor and discovery, then the suggestion that Hodram might find the site.",),
    ],
    (2, 284): [
        ("The same messenger checks Lil's surname and reports an active search by the London guild. Match the parallel summonses.", SUMMONS),
    ],
    (2, 285): [
        ("Keep the guildmaster's pleased greeting and casual description of a small job.",),
        ("Keep about 200 barrels, two holds and the market as the delivery point.",),
        ("The market is short on stock after several large deals. Avoid suggesting that it can't source the wine. Payment comes from the market.", "After a string of big trades, they're short on wine. The market will pay you on delivery."),
    ],
    (2, 286): [
        ("Keep Lil's conversational reminder, the two holds, and the London market destination.",),
        ("The guildmaster urges a quick delivery. Keep the impatience without making it sound like a shouted command.", "Come on, get that wine to the market soon, will you?"),
    ],
    (2, 287): [
        ("The market trader recognizes the delivery as the wine they asked for. Make his question sound conversational.", "Oh, did you bring the wine?"),
        ("Keep the trader's brief thanks and his promised payment.",),
        ("Keep the precise speakerless payment of 8,000 gold coins.",),
        ("Keep the limited increase in London's market share.",),
        ("Keep Lil's unsentimental question about local demand. It's a natural cue for the trader's story.",),
        ("Keep the trader's distrust, the comparison to a festival, and the drinking group's unusually large wine purchases.",),
        ("Keep Lil's immediate interest in the location of the ruins.",),
        ("Keep the distance approximate and the assurance qualified by having a map.",),
        ("Keep the shortage, its cause and the trader's secondhand report about Amsterdam.",),
        ("Keep Lil showing the map and asking for confirmation.",),
        ("The trader starts to tease Lil after recognizing the map. Use the hesitant last beat and the following laugh to keep it friendly.", "Yeah, that's it! Wait, you're with that bunch too, are you...?"),
        ("The trader immediately laughs off the suggestion. Keep the quick reversal.", "Nah, of course not! Ha ha ha!"),
    ],
    (3, 253): [
        ("The messenger spots Maria and checks her surname before saying the London guild is looking for her. Match the other summonses.", SUMMONS),
    ],
    (3, 254): [
        ("The guildmaster describes severe scurvy among the navigators he employs. Lead with the job and make his concern conversational.", "I've got a job for you. Scurvy's hit our navigators hard."),
        ("Keep the reason for asking Maria in particular. Her company sails all over the world, so she may know a remedy.",),
        ("The guildmaster has heard of a remedy hidden somewhere near Africa. Keep its supposed instant effect as his report.", "They say there's a strange remedy hidden somewhere near Africa that cures scurvy on the spot. Ever heard of it?"),
        ("Keep Maria's courteous, hesitant admission that she doesn't know the remedy.",),
        ("The guildmaster still wants her to find it and only needs a loan. Keep the request and loan as complete thoughts.", "I see. Could you find it for us? We'd only need to borrow it."),
        ("Keep Maria's measured agreement to look for the remedy without promising a result.",),
        ("Keep his relief and warm, informal acknowledgment that he owes her a favor.",),
        ("Keep Maria's recognition and tentative identification in the variant where she already has the remedy.",),
        ("The guildmaster is impressed she already has it. Keep the surname token and admiring familiarity without inventing a title or relationship.", "You already have it? " + APPROVAL),
        ("Keep the request to borrow it, the crew's recovery as the condition, and one month as his estimate.",),
        ("Keep Maria's poised agreement. This makes the loan voluntary in both versions.",),
        ("Keep the guildmaster saying his good opinion of Maria was justified.",),
        ("Keep the exact Lime Drops item name and the speakerless notice that it was lent.",),
        ("Keep the promise of a reward, the one-month wait, and the reminder to return in one natural request.", THANKS),
    ],
    (3, 255): [
        ("Keep Maria tentatively identifying the item on the later handover path.",),
        ("Keep the guildmaster's delighted recognition and familiar approval, with the original surname token. Mirror the praise from the other path and give a long surname room to render.", "You found it! " + APPROVAL),
        ("He apologizes for the imposition and estimates a month. Restore that courtesy and let Maria's next turn give her consent.", "Sorry to impose. Could we keep it till our navigators are well again? A month or so should do it."),
        ("Keep Maria's poised agreement before the loan notice.",),
        ("Keep the identical item name and loan status from the other path.",),
        ("Keep the same reward and return instructions as the other loan path.", THANKS),
    ],
    (3, 256): [
        ("Keep Maria's open question about where to find the cure.",),
        ("Maria recognizes the particular Lime Drops as the remedy and plans to deliver them promptly. Keep the discovery as a thought spoken aloud.", "So the cure is Lime Drops. I'd better get them to the London guild."),
    ],
    (3, 257): [
        ("Keep Maria's estimate that it is about time to ask for the loaned Lime Drops back.",),
    ],
    (3, 258): [
        ("The guildmaster says Maria did him a great favor and that his navigators recovered. Keep his gratitude centered on the crew who were ill.", "Good to see you! You really helped us out. Our navigators are all back on their feet."),
        ("The reward is 20,000 gold coins. Restore the stated denomination.", "Received 20,000 gold coins."),
        ("Use the full player-facing share notice and preserve the small London increase.", LONDON_SHARE),
        ("Keep Maria's polite change of subject and her question about local ruins of note.",),
        ("Keep the ruins' rough distance, the map's usefulness and the guildmaster's warning. Give the warning a single coherent sentence.", "A little way from London, yes. Easy to find with a map. Only there's been an odd bunch hanging around there lately."),
        ("Keep Maria echoing 'odd' before asking more through her tone. She hasn't heard what the group has done yet.", "An odd bunch?"),
        ("Keep the ejected caretaker, creepy rites and the neighbors' reaction as something the guildmaster heard.",),
        ("Keep the companion's interested reaction and his practical question about the map.",),
        ("Keep the reason maps ran out and the tentative lead that another city may still sell them.",),
    ],
}

PHRASE_GROUPS = (
    "You're FA, right?", "The London guild's looking for you.", "calling it a ritual...", "in Amsterdam",
    "light and darkness", "stand in balance", "it too lies", "sunrise or sunset", "in balance",
    "this shadow", "on either equinox!", "the tip of a shadow", "With the latitude,", "where it'll fall",
    "who looks after the ruins.", "who these men are.", "keep a calendar", "tell the time.",
    "the longest shadow", "only need to borrow it.", "did you bring the wine?",
    "on the spot.", "gold coins.",
    "our navigators are well again?", "come back in a month",
    "short on wine.", "hanging around there", "back on their feet.", "You may not believe this,",
    "keeps showing up", "a monster fish.", "Ever heard of it?", "Scurvy's hit our navigators hard.",
    "We'd only need to borrow it.", "Only there's been", "it for us.", "day and night",
    "what looks like a festival", "the stone pillars", "tell the guild.", "several ships",
    "on delivery.", "Well done, FA!", "I knew I could count on you.", "helped us out.", "Come on,",
)
TOKEN = re.compile(r"(?<![A-Z])(?:FI|FA|FO|FU)(?![A-Z])")


def logical(text):
    return " ".join(text.split())


def index_history(path):
    doc = base.load(path)
    return {(r["block"], r["source_reference"]["offset"]): r for r in doc["records"]}


def main():
    packet = base.load(SOURCE)
    assert packet["complete_source_current_binding"] and len(packet["groups"]) == len(REVIEW)
    registered = base.load(paired.parent.RELEASE)
    assert registered["candidate_sha256"] == packet["candidate_sha256"]
    histories = [Path("translations") / name for name in HISTORY]
    lookups = [index_history(path) for path in histories]
    hashes = [base.digest(path) for path in histories]
    records = []
    for group in packet["groups"]:
        route, block = group["route"], group["block"]
        notes = REVIEW[route, block]
        for raw, (note, *new) in zip(group["records"], notes, strict=True):
            prior = lookups[route][block, raw["source_offset"]]
            word = raw["native_command_word"]
            prefix = bytes([raw["selector"]]).hex() if word == paired.stage.SPEECH else ""
            source_hex = prefix + raw["source_body_hex"]
            current_hex = prefix + raw["current_body_hex"]
            assert prior["source_hex"] == source_hex and all(prior["review"].values())
            previous = logical(raw["current_English"])
            text = new[0] if new else previous
            assert text.isascii() and logical(text) == text
            assert Counter(TOKEN.findall(raw["Japanese"])) == Counter(TOKEN.findall(text))
            decision = "revision" if text != previous else "retention"
            kind = ("system-FE" if raw["selector"] == 254 else "typed-choice-label"
                    if word in paired.stage.MENU else "progressive")
            source_ref = dict(file_path=raw["file_path"], block=block, offset=raw["source_offset"],
                command_offset=raw["source_command_offset"], archive_sha256=group["source_archive_sha256"],
                exact_stored_hex=source_hex, record_index=raw["source_record_index"])
            current_ref = dict(file_path=raw["file_path"], block=block, offset=raw["current_offset"],
                command_offset=raw["current_command_offset"], archive_sha256=group["current_archive_sha256"],
                exact_stored_hex=current_hex)
            if kind == "typed-choice-label":
                source_ref["source_index"] = current_ref["source_index"] = raw["slots"][0]
            records.append(dict(id=prior["id"], route=route, block=block, file_path=raw["file_path"],
                source_reference=source_ref, current_reference=current_ref, source_hex=source_hex,
                current_hex=current_hex, source_selector=raw["selector"], native_command_word=word,
                native_slots=raw["slots"], speaker=prior["speaker"], kind=kind, Japanese=raw["Japanese"],
                source_meaning=note, context=group["context"], localization_note=note, previous_English=previous,
                english=text, decision=decision, protected_phrases=[p for p in PHRASE_GROUPS if p.lower() in text.lower()],
                earlier_ledger=str(histories[route]), earlier_ledger_sha256=hashes[route],
                historical_layout_matches_current=prior["planned_integrated_reference"]["exact_stored_hex"] == current_hex,
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    assert len(records) == 151 and len({(r["file_path"], r["id"]) for r in records}) == len(records)
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        previous_sha256=registered["candidate_sha256"], previous_registry_sha256=registered["registry_sha256"],
        clean_input_sha256=packet["clean_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        formatting_and_registration_pending=True, additional_review_credit=0, records=records)
    assert not OUTPUT.exists()
    base.save(OUTPUT, result)
    print(dict(Counter((r["kind"], r["decision"]) for r in records)))


if __name__ == "__main__":
    main()
