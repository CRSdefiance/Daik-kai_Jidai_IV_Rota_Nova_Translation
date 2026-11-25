"""Revisit Rafael's complete exchanges in SC0 blocks 51 through 59."""

from collections import Counter
from pathlib import Path

from scripts import register_hodram_baltic_trade_20261121 as parent
from scripts import stage_london_guild_assignments_20261118 as planner
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_north_sea_africa_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
PRIOR = Path("translations/rafael_B51_B60_contextual_final_review_v1.json")

SCENES = {
    51: "Rafael pauses somewhere quiet and catches Sera's smile. Hodram interrupts the silent encounter and leads her away. Rafael is left guessing who she is and trying to place Hodram.",
    52: "A port worker recognizes Rafael by his company and relays Albuquerque's request to return to Lisbon. A sailor or Janus recommends complying, each in his own register.",
    53: "A sailor reminds Rafael about the summons. Rafael decides to go to the Palace and asks him to confirm the destination.",
    54: "A shopkeeper credits Fernan Silveira with Espinosa's defeat. Rafael's wry reply baffles him, and the news that the Governor's Office is moving sends Rafael straight to Sofala.",
    55: "Fernan congratulates Rafael, then reveals he has taken the governorship and Sofala's shares. He treats deducting his own gift as a joke. Claudio suspects he took the credit, and the crew persuades a reluctant Rafael to push back.",
    56: "Residents grateful for the end of Espinosa and Silveira's rule give Rafael a clue the town paid for. Arcadius recognizes its connection to the Proof of Conquest before the residents explain why they gave it to Rafael.",
    57: "Emilio falls through a rotten pier. Arcadius brings him fruit and flowers while he rests. Claudio first wants a share, then asks whether Arcadius would visit him too. He leaves the gift with Emilio and waits for Arcadius.",
    58: "Uddin identifies himself as the current or former company leader according to the branch. He credits Rafael's swift success in the Indian Ocean and entrusts him with the Evergreen Lotus Leaf. Rafael thanks him after the farewell.",
    59: "A port worker stops Rafael and warns him off Pereira's territory. Rafael returns the warning with guarded politeness after challenging the worker's point.",
}
BLOCKS = (tuple(SCENES), (), (), ())

# Each line records one decision. An empty replacement keeps the prose and
# revisits its layout only when phrases are specified.
DECISIONS = """
51 6|It's nice and quiet here. All right. It's been a while...|All right.|Restore Rafael's ease and leave his intended activity unspoken.
51 18|||The brief inward reaction fits the silent approach.
51 24|||The gesture conveys Sera's friendly smile without implying recognition.
51 28|||The puzzled pause leads naturally to Rafael's private question.
51 32|||Retain the speakerless pause between looks.
51 37|||Hodram calls her by the established name. The single name works as an interruption.
51 41|||Rafael reacts inwardly to the name he just heard.
51 46|||Sera recognizes Hodram in a brief greeting.
51 50|||The question followed by self-correction preserves Hodram's suspicion and quick dismissal.
51 54|||Rafael's silence gives Hodram room to size him up.
51 59|||The thoughtful sound conveys appraisal without explaining it.
51 63|||Sera's question is just his name, which gives Hodram room to answer abruptly.
51 67|||Hodram's concise direction suits the way he cuts the encounter short.
51 71|||Sera's direct acknowledgment lets the pair leave without exposition.
51 75|...She was beautiful. A princess, maybe? I wonder where she's from.|A princess, maybe?;I wonder where she's from.|Make the questions read as private thoughts while keeping princess strictly Rafael's speculation.
51 86||the Swedish navy...?|Keep Rafael's tentative recognition and the Swedish navy together.
52 5|||The worker's casual recognition preserves the company substitution.
52 9|||Rafael's polite reply follows a moment of confusion.
52 14|||The worker's clipped confirmation fits his casual opening.
52 18|Admiral Albuquerque of the Portuguese military asked me to tell you to head back to Lisbon if I saw you.|the Portuguese military;back to Lisbon|Make it clear Albuquerque instructed the worker and wanted Rafael sent back to Lisbon if found.
52 21||want with us?|Rafael understands the request and wonders what the military wants. Keep the question ending together.
52 31|||The sailor's contractions fit his practical suggestion to head back.
52 36|||Janus's measured phrasing preserves the more formal counterpart.
53 6|Oh, Admiral. The Portuguese military summoned us, remember? What do you want to do?|The Portuguese military;summoned us, remember?;What do you want to do?|Give the sailor a conversational opening and let the reminder lead to his question.
53 10||To the Palace, right?|Keep the destination and Rafael's quick request for confirmation on one line if they fit.
53 14|||The plain confirmation answers the question directly.
54 5|||The shopkeeper grabs Rafael's attention with a brisk question.
54 9|||Rafael's short response is a natural invitation to explain.
54 14||the infamous Espinosa!|Keep the lively rumor and its infamous target together.
54 18|||Rafael's dry remark suggests he knows more than the shopkeeper without explaining it.
54 23|Huh? You're an odd one. Anyway, I'd rather have Silveira than Espinosa. That man was nothing but trouble.|I'd rather have Silveira;That man was nothing|Preserve the worker's confusion, his comparative preference and his reason.
54 26|||The hedged agreement lets Rafael keep his reservations to himself.
54 31||is moving to Sofala...|Preserve the hearsay and place name. Keep the destination with the transfer.
54 35|The Governor's Office for Africa... In Sofala?! I've got to go. Thanks for telling me!|In Sofala?!;I've got to go.;Thanks for telling me!|Keep the realization, urgency and thanks. Capitalize the established facility.
54 40|||The call after Rafael and the irritated question preserve the shopkeeper's comic reaction.
55 5|||Fernan opens with hearty familiarity and the given-name substitution.
55 8|||Rafael addresses Fernan by rank, then privately realizes how quickly he arrived.
55 12|You all did splendid work! I've already reported it to His Excellency Albuquerque. You haven't a thing to worry about.|You all did splendid work!;reported it;His Excellency Albuquerque.;to worry about.|Restore the collective praise and give Fernan the confident assurance that makes the reveal sting.
55 15|||Rafael's uncertain response leaves Fernan room to continue.
55 20|I turned him down, you understand. But His Excellency insisted...|you understand.;His Excellency insisted...|Keep the self-serving disclaimer and the pause before the revelation.
55 24|||The incredulous boast and laughter convey Fernan's performance.
55 28|||The short outburst is Rafael's immediate shock.
55 36|||The system notice communicates the loss of all player shares to the named company.
55 40|That's just the way luck goes. No hard feelings, eh? Ha ha ha!|the way luck goes.;No hard feelings, eh?|Fernan's breezy dismissal underlines how little the loss costs him.
55 44|Here's your reward from His Excellency Albuquerque. My appointment gift? I already took it out of your reward.|Here's your reward;My appointment gift?;out of your reward.|Set up and deliver the joke in Fernan's voice. He withholds his own congratulatory gift.
55 47|Of course, if you insist on giving me another gift, I won't object. Ha ha ha!|giving me another gift,;I won't object.|Make clear Fernan is open to receiving a second gift after already taking the first.
55 54|||The displayed amount is 3,000 and the ellipsis colors the deflated reward.
55 58|||Rafael's blunt private reaction conveys the sting of being outplayed.
55 63||Did Commander Albuquerque;really decide all this?|Keep Rafael's question and the rank of address. Carry the entire challenge together.
55 67|Tch. That bastard badgered him into it. I bet he lied and took all the credit for beating Espinosa.|badgered him into it.;I bet he lied;all the credit|Claudio is convinced Fernan pressured Albuquerque. Keep the lying and credit theft as Claudio's suspicions.
55 78|He's even shrewder than I thought. Admiral FI, surely we can't let this go!|than I thought.;Admiral FI,;we can't let this go!|Janus is surprised by Fernan's skill and asks Rafael to act. Preserve the title and given-name call.
55 90|||The sailor announces a new target before Rafael understands what the crew means.
55 95|||Arcadius delivers the alternative in a more composed voice.
55 102|||Rafael's question leaves space for the others to explain.
55 115|Silveira! Now you've got me taking this seriously!|taking this seriously!|Restore Fernando's emphatic decision to get serious after Silveira's maneuver.
55 121|We can't just sit here and take it!||The sailor insists on acting in response to being cheated.
55 132|||Jam's emphatic invocation and whoop fit his relish for the challenge.
55 138|||Claudio throws his support behind the retaliation in a short call.
55 142|Y-yeah. I don't want to fight my fellow Portuguese, but I'd hate to back down even more.|my fellow Portuguese,;back down even more.|Carry both sides of Rafael's reluctance and his eventual choice to stand his ground.
55 154|||Cristina's direct address carries the angry outburst.
55 168||these old bones.;all we've got!|Keep Julio's old-bones joke, the given-name substitution and his change to encouragement.
55 174||wipe that smirk;from Silveira's face!|The idiom keeps the sailor's intent to humble Silveira. Keep the target with his reaction where possible.
55 178|||Rafael thanks the group and states their new goal after hearing them out.
55 182|||Claudio's concise rally drives straight into the sailor's reply.
55 186|||The sailor's short affirmative closes the rally.
56 5|||The shopkeeper recognizes Rafael as the head of the named company.
56 9|||The port worker's doubled call and excitement motivate Rafael's question.
56 12|||Rafael checks who they mean and asks what they need.
56 17||Espinosa and Silveira;ran the place.|The worker contrasts the old powers with life now. Keep their names together.
56 21|||The shopkeeper echoes the worker and gives credit directly to the whole company.
56 24|||Rafael's blush gives his reaction the modest tone of the Japanese.
56 28|Crooked merchants ran things for so long, we nearly forgot how to trust anybody.|Crooked merchants ran things;how to trust anybody.|The worker connects years of crooked rule to the loss of trust in conversational English.
56 32|||The abrupt pivot to the reason they called him preserves the comic interruption.
56 36|||Rafael's hesitant acknowledgment explains the next request to pay attention.
56 41||Here, take this.|Keep the worker's prodding and the handover phrase together.
56 46|||Rafael asks what he has just been handed.
56 58||a Proof of Conquest?!|The incomplete surmise reads as recognition of the clue. Keep the title together.
56 62|||The repeated question word conveys Rafael's sudden excitement.
56 66||sell it to Espinosa;for a fortune.|The shopkeeper names the attempted sale and the high price.
56 69|Trying to make a fortune by telling that devil where to find a Proof of Conquest! Can you believe it?|that devil;where to find;a Proof of Conquest!|Preserve the port worker's outrage at the buyer, motive and information being sold.
56 72|||Rafael's stammer expresses disbelief at being offered it.
56 77|The whole town chipped in. We made him sell it to us so we could give it to you.|The whole town chipped in.;we could give it to you.|Keep the natural opening and put the coercion and the purpose of the purchase in one sentence.
56 81|||Rafael's short thanks fits the gift and the residents' expectations.
56 89|There. It's yours now. Do us all proud.|It's yours now.;Do us all proud.|Confirm the handover and keep the request to do well for everyone.
56 92|||Rafael's immediate assent takes the charge seriously.
56 97|||The port worker reinforces the shopkeeper's request with direct encouragement.
57 5|||Emilio's cry announces the fall before the others see what happened.
57 10|E-Emilio! Are you all right?!|Are you all right?!|Recover Rafael's startled stammer and keep the question intact.
57 14|||Claudio checks the pier and infers the cause in a short aside.
57 17|||Emilio's drawn-out cry conveys immediate pain.
57 22|||Arcadius asks to inspect the injury without alarming Emilio further.
57 26|||The softer cry keeps Emilio's pain present while Arcadius looks.
57 30|We'd better keep it still. Let's get you to the inn so you can rest.|keep it still.;Let's get you to the inn;so you can rest.|Give the crew a practical instruction and preserve the inn as the place to rest.
57 33|||The offer of help gives way to Claudio's unguarded complaint about Emilio's weight.
57 40|||Rafael moves from relief about the injury to noticing Arcadius.
57 45|||Claudio notices the flowers and wonders what Arcadius is up to.
57 48|||Rafael adds the fruit to Claudio's observation.
57 53|||The birthday guess follows naturally from flowers and fruit.
57 57|||Claudio calls out and guesses a party in his own casual voice.
57 60|||Arcadius's baffled response prompts Claudio to explain his assumption.
57 64|I saw you with flowers and something that looked good. Come on, let me try some!|I saw you with flowers;let me try some!|Give Claudio an easy lead from what he saw to his greedy request.
57 68|||Arcadius gently corrects the misunderstanding and identifies the visit's purpose.
57 71|||Rafael asks why with the same surprise Claudio is showing.
57 76|Honestly, what did you think I was doing?||Give Arcadius a mildly incredulous reply to both the party guess and Rafael's surprise.
57 80|We finally get some time in town, and he's stuck indoors. I thought he'd be bored, so I'm going to see him.|he's stuck indoors.;I thought he'd be bored,;going to see him.|Keep Arcadius's consideration for Emilio and his reason for visiting.
57 83|||Claudio's small acknowledgment gives Arcadius room to continue.
57 87||Emilio likes sweets, remember?;fresh ones at sea.|Keep the reason for the fruit and Arcadius's thoughtful reason for finding fresh flowers.
57 91||Would you visit me too; if something happened?|Preserve the tentative turn from Emilio's situation to Claudio's own question.
57 95||We're crewmates, aren't we?|Arcadius answers warmly. Keep the relationship and tag together.
57 99|||Claudio's stammer preserves the effect of being reassured.
57 103|||The stammer and quick change of subject show Claudio waving off his concern.
57 106||Want to come with me,;some of that fruit.|Keep Arcadius's invitation and its playful callback to Claudio's earlier request.
57 109|||Claudio gives up the fruit and asks Arcadius to give all of it to Emilio.
57 113|||The little hesitation marks Arcadius's acceptance of Claudio's refusal.
57 116|||Arcadius asks about the leg before offering the gift.
57 119|Wow, food! Thanks, Arcadius! Did you know I love flowers?|Did you know I love flowers?|Emilio's excited thanks and delight in the flowers resolve Arcadius's uncertainty.
57 122|I didn't know. I'm glad you like them. Have as much fruit as you like.|I'm glad you like them.;as much fruit as you like.|Give Arcadius a warm answer and keep the invitation to help himself.
57 126|||Emilio's exuberant reply matches the excitement of his thanks.
57 132|||Arcadius uses the familiar Clau and is surprised to find Claudio waiting.
57 135|Y-yeah. Come on. Let's catch up with the others.|Come on.;Let's catch up with the others.|Keep Claudio's awkward acknowledgment and his quick suggestion to rejoin the group.
57 139|||Arcadius's quiet agreement follows the understated reunion.
57 143|||The last silence leaves Claudio's reaction unstated.
58 5|||Uddin politely checks Rafael's identity using the original surname substitution.
58 14|||Rafael's unfinished question invites Uddin to introduce himself.
58 25|||First person and the past tense preserve the former-leader branch.
58 30|||First person and the present tense preserve the continuing-leader branch.
58 38|||Rafael recognizes Uddin and addresses him by rank.
58 45|You took the Indian Ocean by storm. I wouldn't expect any less from you, Admiral FA.|the Indian Ocean;I wouldn't expect any less;Admiral FA.|The idiom conveys Rafael's rapid ascendancy. Preserve Uddin's respectful surname address.
58 50|||Rafael's stammer and appeal to luck convey genuine modesty.
58 54|No need to be so modest. Maybe it's fate.|Maybe it's fate.|Keep Uddin's gentle response and his view of Rafael's rise.
58 57||my final duty;the Indian Ocean.|Uddin formally presents the gift as his final duty in the region. Keep his existing role description.
58 63|||The single exclamation is Rafael's silent surprise before the item is named.
58 68|This is the Evergreen Lotus Leaf. They say it shows the way to the Proof of Conquest for the Indian Ocean.|This is the Evergreen Lotus Leaf.;shows the way;the Proof of Conquest;for the Indian Ocean.|Identify the established item and preserve the reported nature of its use.
58 72|||Rafael realizes that the large leaf itself is a map.
58 76|I believe the Proof of Conquest for the Indian Ocean is a book called the Rigveda.|I believe;the Proof of Conquest;for the Indian Ocean;a book called the Rigveda.|Preserve Uddin's qualified identification and the established name of the book.
58 79|||Rafael repeats the book's name as he takes in the information.
58 84|||Uddin's dignified parting wish preserves his courteous register.
58 95|||Claudio's faint surprise and casual address contrast with Uddin's formality.
58 99|||Rafael's quiet repetition preserves the pause before his farewell.
58 106|||The thanks and farewell follow Uddin's departure and retain Rafael's respect.
59 5|||The abrupt summons and rank fit the way the worker stops Rafael.
59 8|||Rafael asks whether he is being addressed.
59 13|Yeah, you. Don't you know whose turf this is? Duarte Pereira, the Portuguese governor of Indochina.|whose turf this is?;Duarte Pereira,;governor of Indochina.|Keep the threat in the worker's voice, then identify Pereira by his original title.
59 17|||Rafael's clipped reply challenges the premise that he should be intimidated.
59 22|Keep your head down. Best he doesn't notice you.|Best he doesn't notice you.|The worker warns Rafael to avoid drawing Pereira's attention.
59 26|||The pause and guarded thanks let Rafael close the exchange politely.
"""


def main():
    assert not OUTPUT.exists()
    packet, release, previous_review = map(base.load, (SOURCE, parent.RELEASE, PRIOR))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    decisions = {}
    for line in DECISIONS.strip().splitlines():
        key, english, phrases, note = line.split("|")
        block, number = map(int, key.split())
        assert (block, number) not in decisions
        decisions[block, number] = english, tuple(p.strip() for p in phrases.split(";") if p.strip()), note
    earlier = {(r["block"], r["source_reference"]["offset"]): r for r in previous_review["records"]}
    records, plans, failures = [], {}, []
    for group in packet["groups"]:
        block = group["block"]
        if block not in SCENES:
            continue
        for entry in group["records"]:
            number, selector = entry["source_record_index"], entry["selector"]
            old = earlier.pop((block, entry["source_offset"]))
            assert entry["Japanese"] == old["source_Japanese"] and old["source_selector"] == selector
            assert all(old["review"].values()) and entry["native_command_word"] == 0x4000
            jp, en = (bytes.fromhex(entry[f"{side}_body_hex"]) for side in ("source", "current"))
            prefix = bytes([selector])
            assert old["source_hex"] == (prefix + jp).hex()
            replacement, phrases, reason = decisions.pop((block, number))
            current = logical(entry["current_English"])
            english = replacement or current
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            refs = {side: dict(file_path=group["file_path"], block=block, offset=entry[f"{side}_offset"],
                               command_offset=entry[f"{side}_command_offset"],
                               archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                               exact_hex=(prefix + value).hex())
                    for side, value in (("source", jp), ("current", en))}
            changed = bool(replacement or phrases)
            row = dict(id=old["id"], file_path=group["file_path"], route=0, block=block, source_record_index=number,
                       native_command_word=0x4000, native_slots=[], source_selector=selector,
                       kind="system-FE" if selector == 254 else "progressive",
                       source_reference=refs["source"], current_reference=refs["current"],
                       source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                       Japanese=entry["Japanese"], previous_English=current, english=english,
                       speaker="Fernan Silveira" if selector == 35 else old["speaker"], context=SCENES[block],
                       source_meaning=old["source_meaning"], localization_note=reason,
                       protected_phrases=list(phrases), decision="revision" if changed else "retention",
                       finding="prose and wrap" if replacement else "wrap" if phrases else "retention",
                       review=dict.fromkeys(GATES, True) | {"formatting": not changed})
            if changed:
                assert selector != 254 and all(phrase in english for phrase in phrases), (row["id"], english, phrases)
                try:
                    body, plan = planner.plan_progressive(row, selector, en, jp)
                except (ValueError, AssertionError) as error:
                    failures.append((row["id"], english, phrases, str(error)))
                else:
                    if body.rstrip(b" ") == en.rstrip(b" "):
                        assert not replacement, row["id"]
                        row.update(decision="retention", finding="retention")
                        row["review"]["formatting"] = True
                    else:
                        plans[row["id"]] = plan
            records.append(row)
    assert len(records) == 146 and len(earlier) == 103 and not decisions
    assert not failures, failures
    summary = dict(Counter(r["decision"] for r in records))
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                         target_locale="en-US", review_gates=GATES, previous_sha256=packet["candidate_sha256"],
                         previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                         source_packet_sha256=base.digest(SOURCE), earlier_contextual_reviews={str(PRIOR): base.digest(PRIOR)},
                         records=records, plans=plans, decisions=summary,
                         findings=dict(Counter(r["finding"] for r in records)), new_editorial_credit=0,
                         status="Contextual review complete. Changed text awaits native formatting approval."))
    print(f"Reviewed {len(records)} records. {summary}.")


if __name__ == "__main__":
    main()
