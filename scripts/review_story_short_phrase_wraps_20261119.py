"""Review the complete exchanges surrounding twelve newly found phrase breaks."""

from collections import Counter
from pathlib import Path

from scripts import prepare_story_short_phrase_wraps_20261119 as paired
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical

base, native, parent = paired.base, paired.native, paired.parent
ROOT, SOURCE = paired.ROOT, paired.SOURCE
OUTPUT = ROOT / "contextual_review_v3.json"
NAMES = Path("translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json")

EXCHANGES = {
    (0, 60): (0, """Keep the surprised recognition before the request for proof.
The direct question asks whether Rafael brought the promised Proof.
The separate key response explains what they found, with the Proof still ahead.
The quiet reaction follows the evidence Rafael presents.
Keep the prior promise and the discovery in East Asia.
The speaker verifies authenticity before inviting them along.
The short invitation moves the conversation to a private explanation.
Keep the possibility that he has explained his position before and the limit on helping openly.
Rafael's pause gives the speaker room to qualify his refusal.
The common enemies are Kuhn and Spain, and the conclusion sounds spoken.
The proposed agreement is a question. Rafael still asks about defeating both opponents together.
The blunt reply suits the speaker's resistance to oversimplifying the situation.
Rafael presses for the reason with a short question.
The speaker asks for a considered answer about the true enemy.
Rafael repeats the new distinction while considering it.
The first choice identifies Spain by its seizure of Portugal.
The second choice preserves hesitation and admits uncertainty."""),
    (0, 62): (0, """The formal gift praises Rafael's standing at sea and preserves his surname substitution.
The hesitant question leaves the artifact's connection to the Proof uncertain.
Thanks turns to surprise when the giver moves away.
The companion's clipped aside confirms the departure.
The sheath, missing blade and puzzled response explain what the party actually sees.
Rafael considers whether this is another map key and names the intended Proof.
The alternative voice is more certain that it is a key for deciphering the map.
The final voice agrees and eagerly claims the prospect of treasure in the New World."""),
    (0, 87): (0, """Keep Zipangu and Rafael's interest in its unfamiliar culture.
Clau's dismissive reaction to the hairstyles gives Julio a reason to correct him.
Julio's patient response recognizes that standards differ by culture.
The short reluctant assent closes the first exchange.
The stranger calls out a question about the party being foreigners.
Kurushima treats the reported swagger as a provocation. The claim remains his.
Clau recognizes trouble and addresses Rafael through the native name substitution.
Rafael suggests ignoring them, with the thought trailing off.
Julio's maxim about avoiding trouble supplies the setup for his later reply.
The alleged victim cries out to his boss before the accusation.
Kurushima accuses the party of deliberate contact and alleges a broken bone.
Rafael's stammer and protest reverse the claim of who ran into whom.
Clau stops arguing and explains why. The given name remains a substitution.
Julio wryly observes how quickly the trouble they wanted to avoid found them.
The henchman deliberately reframes the exchange as an invitation to fight.
Kurushima names himself, theatrically draws out his refusal and gives the order.
The henchman's assent keeps the quick escalation.
Rafael's questions convey how outnumbered the party is without guessing a count.
Clau accepts the fight and tells the older man to get behind him.
The stranger's formal offer interrupts the threat.
The short puzzled response clears room for the newcomer.
His restrained instruction fits the decisive intervention that follows.
The henchman's challenge keeps the samurai role and prejudice in the character's voice.
Yukihisa claims the judgment of right and wrong for himself.
Kurushima's insult and order preserve his anger.
The henchman's terse answer leads directly into the fight.
The scream is a reaction to the fight, with its cause left to the action.
The drawn-out cry conveys how soundly the henchman has been beaten.
Kurushima threatens a future reckoning as he leaves.
Using the back of the blade and cutting no one both matter to Yukihisa's conduct.
Rafael stammers that he couldn't see the sword move. Keep his admiration.
Clau's second stammer agrees with Rafael and gives them a brief shared reaction.
Julio expresses wonder in his own voice.
Yukihisa apologizes formally for what they saw in his country.
Rafael reassures him with gratitude for the rescue.
Yukihisa courteously infers that they travel the world.
The formal request leaves the choice to Rafael.
Seeing more of the world supplies his motive.
Rafael welcomes him while stating how long they may be away from Japan.
Yukihisa intends to leave and test himself. Keep the motivation in his voice.
The welcome and given-name and surname substitutions keep the introduction intact.
His formal introduction uses the established full name."""),
    (0, 127): (0, """Julio gives Ceuta as the next destination before explaining the controls.
The short invitation shifts from discussion to moving the ship.
Julio first tells Rafael to check his heading.
Keep both the crew instruction and the explanation of the direction.
The speakerless text introduces both control methods and calls the control the D-Pad.
Use the same D-Pad label and keep the alternative touch input clear.
Restore automatic sail adjustment to the best angle and keep the flagship as the stop control.
Julio checks understanding before the two choices.
The first option confidently accepts the explanation.
The second option expresses worry about the wind without choosing a new destination.
Julio's encouragement answers the confident option.
Turn Rafael's trailing tag into a complete question. He knows how to choose a course and worries about making headway.
The headwind explains Rafael's concern. The tailwind to Ceuta is why Julio reassures him.
Rafael still sounds uncertain and asks if the plan will work.
Julio's proverb and Lisbon fallback reassure Rafael without promising success.
Sickness, rats and leaks are possibilities on a long voyage.
Name the problems Julio was just talking about and retain his advice to put in promptly.
The help panel explains recovery at a town using the conditions just introduced.
The southeast heading and the exact Route Map label close the lesson."""),
    (0, 226): (0, """The straightforward delivery announces a letter from Janus.
The more formal delivery uses the same sender and event.
The casual announcement addresses the admiral and identifies Janus.
The personal delivery keeps the letter clearly for the player.
The rough voice's contraction keeps the voice distinct.
The familiar announcement puts the address at the end.
The youthful call separates the greeting from the letter.
Janus formally identifies where he is writing from.
The account recalls repeated persecution and the missionaries' work.
Keep Janus's stated disinterest in faith and his curiosity about one story.
The sword's connection to Judas and the report of its location remain hearsay.
The letter explains why the betrayal affects the object's reputation.
Janus thinks the blade worth finding and distinguishes it from its owner's deeds.
Manuel's expected reaction belongs to Janus's aside and is appropriately tentative.
Preserve the blank line and the signature separately from the farewell.
Rafael connects the disregard for provenance to what he knows about Janus.
Manuel qualifies his position and leaves the decision to the admiral. Keep the closing phrase whole."""),
    (0, 282): (0, """Rafael reminds himself of the need to defeat Plett promptly.
The second speaker asks for Plett's capture with the same urgency. Keep the timing phrase together."""),
    (1, 49): (0, """Lil greets the returning visitor with immediate recognition.
The Proof is important to the region. Her playful refusal sets up a trade.
Hodram's pause gives Lil the floor to name her condition.
The potential exchange remains conditional on one object.
Keep Lil's excitement about the named wristband and her uncertainty about the name.
Keep the New World clue, the return condition and the playful farewell.
This branch expresses surprise that the item is already in hand and asks to see it.
Her excitement about the wristband keeps the trade offer spontaneous.
The affirmative choice accepts the trade.
The negative choice rejects the trade at this point.
Her emphatic acceptance and warning about changing one's mind suit the successful branch.
Her surprised question is a reaction to the refusal. Proof naturally refers to what she already identified.
Hodram's hesitant reply distinguishes the refusal from lack of interest.
Her renewed demand follows the realization that he does want the Proof.
The excitement and farewell close the trade in her voice.
The system records the item actually handed over and retains the exact item name."""),
    (1, 78): (0, """The drawn-out growl opens the first confrontation.
The exclamation leaves Hodram's first reaction in the action.
Escante's broken complaint preserves how close he thinks he came to ruling the New World.
Hodram identifies him in a shout.
Escante's refusal and threat preserve his fixation on his own empire.
The ironic greeting preserves the surname substitution and conciliatory surface.
Hodram's short reply leaves space for Escante's admission.
Escante acknowledges the defeat in a deliberately formal register.
The pause lets him turn from the admission to his disappointment.
His laugh and repetition keep the loss of his imagined empire personal.
The unfinished accusation directs his frustration at Hodram.
Hodram's shock interrupts the attack.
Gerhard's urgent warning addresses the admiral.
Escante's first shocked reaction follows the intervention.
The cry conveys a physical reaction without adding a detail about the wound.
His stammer preserves the sudden fear that he might die there.
The last gasp ends his speech.
Hodram lets the moment pass in silence.
Gerhard asks about Hodram's safety and injury with two urgent questions.
The short reassuring reply answers Gerhard directly.
Hodram's pity and incredulous question respond to Escante's claim. Keep the people and their right to accept or reject him.
Gerhard's notice turns their attention to what Escante has concealed in his clothes."""),
    (3, 106): (0, """The Ming government's recognition is still unofficial. Preserve the surname substitution and the uncertainty.
Maria doubts that recognition could change anything at this point.
Keep the speaker's claim about his English connections and the offense he takes at the supposed favor.
The reply explains that Maria's success and popularity are putting pressure on officials.
Maria's pause gives room for the condition.
The official audience cares about standing, and the intermediary directs them to the evidence.
The object helps decipher a map and its purpose is still reported to them.
Maria repeats the unexpected reference to a treasure map.
Keep the report that the treasure is proof of East Asian rule and the authorities' condition for accepting it as a permit.
Maria's recognition names the Proof with its established wording.
The reported competition from Western powers supplies the urgency of the warning.
Maria can identify the diagram's form but cannot interpret it on its own."""),
    (3, 126): (0, """Xien notices the possible fit and asks Maria through the given-name substitution.
Maria observes that the blade and sheath match in size.
Xien advances a possibility and proposes a test.
His cry registers the unexpected effect before he tries to explain it.
Maria's question follows the blinding flash and identifies Xien.
Xien is unsure what happened, describes the glow and tells her it's safe to look.
Maria sees the map on the blade and asks when it appeared.
Xien expresses his bewilderment without making a claim about its cause.
Maria recognizes the map with surprise and names both the Proof and the New World.
Xien repeats the sequence that puzzled him and admits he cannot explain it."""),
}

LIL = (
    (19, """The companion urgently tells Lil to apologize and uses her given-name substitution.
Her stumbling apology contrasts the famous Clifford with the ordinary-looking man in front of her.
The sharp call uses the original given-name substitution.
Clifford dismisses the offense and checks both parts of Lil's name through the original substitutions.
Lil's surprise invites him to explain how he knows her.
His occupation accounts for how he hears things. Keep the scope general.
Lil asks about her company through the original substitution and leaves the threat unresolved.
Clifford dismisses the indiscriminate violence as a rumor in his own defense.
Lil's skepticism remains audible in the pause.
Clifford leaves belief to Lil and repeats what he wants from the meeting.
Lil's short question asks what he wants to discuss.
The invitation changes the setting and specifies that they'll talk over dinner.
The comic response catches the mention of dinner alone.
Clifford promises to host them and calls them his guests.
Lil's assent accepts the invitation.
Clifford confirms the evening appointment.
Lil shares her excitement with Camille and imagines the mansion. Keep the guess in her voice."""),
    (98, """Lil says she still isn't sure she can trust Clifford.
Clifford appeals to his status as an English gentleman as his own defense.
Lil challenges the relevance of that status.
The companion points out that words alone prove nothing.
Clifford offers the Crimson Dye as a token. Keep the full item name together.
Lil's puzzled question gives him room to explain the object.
Clifford keeps the rumored function distinct from his proposal to join forces.
The companion tentatively reasons that they have to trust him for now.
Lil's hesitation gives weight to her agreement.
Clifford welcomes the decision in his own familiar voice.
He asks her to limit interference in the New World and calls the people there his prey.
The tavernkeeper holds the Crimson Dye. Keep the full item name and precise meeting place.
Lil agrees but keeps her unequivocal warning about betrayal."""),
)

EDITS = {
    (0, 60, 44): ("I may have told you this before, but someone in my position can't help you openly.",
                  ("can't help you openly.",)),
    (0, 62, 46): ("Yeah, I'll bet it is! That treasure in the New World is as good as ours!",
                  ("That treasure in the New World", "is as good as ours!")),
    (0, 87, 87): ("Well, that didn't take long. So much for staying out of trouble.",
                  ("Well, that didn't take long.", "for staying out of trouble.")),
    (0, 127, 23): ("Use the D-Pad to point the ship, or touch the screen in the direction you want to sail.",
                   ("Use the D-Pad to point the ship,", "in the direction you want to sail.")),
    (0, 127, 26): ("The stylus automatically sets the sails at the best angle. Touch the flagship to stop.",
                   ("at the best angle.", "Touch the flagship to stop.")),
    (0, 127, 49): ("I can set our course, but can we move if the wind doesn't catch the sails right?",
                   ("I can set our course,", "doesn't catch the sails right?")),
    (0, 127, 54): ("It's hard to sail into the wind. But we'll have a tailwind to Ceuta, so we should be fine.",
                   ("It's hard to sail into the wind.", "a tailwind to Ceuta,", "so we should be fine.")),
    (0, 127, 73): ("Most of that can't be fixed at sea. Head for port as soon as you can.",
                   ("Most of that can't be fixed at sea.", "Head for port as soon as you can.")),
    (0, 127, 77): ("If one of these problems comes up, stop at a town to recover.",
                   ("stop at a town to recover.",)),
    (0, 226, 88): ("Well... I'm not entirely opposed. Judas did repent in the end. I'll leave it up to you, Admiral.",
                   ("Judas did repent in the end.", "I'll leave it up to you, Admiral.")),
    (0, 282, 27): (None, ("that outlaw Plett", "as soon as you can.")),
    (1, 49, 33): ("I hear it's in the New World. Bring it back. Then this is yours. Bye-bye!",
                  ("I hear it's in the New World.", "Bring it back.", "Then this is yours.")),
    (1, 78, 93): ("Escante... You pitiful man. Did you really think the people of the New World would accept you as their king?",
                  ("the New World", "accept you as their king?")),
    (2, 26, 196): (None, ("that's up to you.", "I'd like to talk to you.")),
    (2, 26, 614): ("Then how about the Crimson Dye as a token of friendship?",
                   ("Then how about the Crimson Dye", "as a token of friendship?")),
    (2, 26, 647): ("I'd rather you didn't meddle in the New World. The lot holed up there are my prey. Don't fight them on your own.",
                   ("in the New World.", "The lot holed up there are my prey.", "Don't fight them on your own.")),
    (2, 26, 650): ("The tavernkeeper in Amsterdam has the Crimson Dye. Go see him.",
                   ("The tavernkeeper in Amsterdam", "has the Crimson Dye.")),
    (3, 106, 34): ("They say the treasure on that map proves who rules East Asia. Find it, and it counts as a permit.",
                   ("the treasure on that map", "who rules East Asia.", "Find it, and it counts as a permit.")),
    (3, 126, 37): ("This is... the map to the Proof of Conquest for the New World!",
                   ("the Proof of Conquest", "for the New World!")),
}


def main():
    assert not OUTPUT.exists()
    packet = base.load(SOURCE)
    release = base.load(parent.RELEASE)
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    names = {n["actor_ID"]: n["current_consumers"][0]["text"] for n in base.load(NAMES)["records"]}
    evidence = {p.as_posix(): base.digest(p) for p in (SOURCE, NAMES, parent.RELEASE)}
    records = []
    edits_seen = set()
    for group in packet["groups"]:
        route, block, path = group["route"], group["block"], group["file_path"]
        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)
        for start, prose in excerpts:
            notes = prose.splitlines()
            raw_rows = group["records"][start:start+len(notes)]
            assert len(notes) == len(raw_rows)
            for raw, note in zip(raw_rows, notes, strict=True):
                idx, word, selector = (raw[k] for k in ("source_record_index", "native_command_word", "selector"))
                key = route, block, idx
                proposed, phrases = EDITS.get(key, (None, ()))
                previous = logical(raw["current_English"])
                english = proposed or previous
                change = key in EDITS
                if change:
                    assert word == 0x4000 and english.isascii()
                    assert TOKEN.findall(raw["Japanese"]) == TOKEN.findall(english) == TOKEN.findall(previous)
                    edits_seen.add(key)
                kind = ("typed-choice-label" if selector is None else "system-FE" if selector == 254 else
                        "progressive" if word == 0x4000 else "style")
                speaker = "Choice" if selector is None else "System" if selector == 254 else names.get(selector, "Native voice alternative")
                prefix = bytes((selector,)).hex() if word == 0x4000 else ""
                src, cur = (dict(file_path=path, block=block, offset=raw[f"{side}_offset"],
                    command_offset=raw[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                    exact_stored_hex=prefix+raw[f"{side}_body_hex"]) for side in ("source", "current"))
                src["record_index"] = idx
                if selector is None:
                    src["source_index"] = cur["source_index"] = raw["slots"][0]
                records.append(dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block,
                    kind=kind, source_selector=selector, native_command_word=word, native_slots=raw["slots"],
                    source_reference=src, current_reference=cur, source_hex=src["exact_stored_hex"],
                    current_hex=cur["exact_stored_hex"], Japanese=raw["Japanese"], previous_English=previous, english=english,
                    speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,
                    protected_phrases=list(phrases), decision="revision" if change else "retention",
                    finding=("wrap" if previous == english else "prose") if change else "retention",
                    review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert edits_seen == EDITS.keys()
    assert len({(r["file_path"], r["id"]) for r in records}) == len(records)
    counts = Counter(r["finding"] for r in records)
    base.save(OUTPUT, dict(source_packet_sha256=base.digest(SOURCE), previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2",
        target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=GATES, records=records,
        counts=dict(counts), prior_evidence=evidence, new_coverage_credit=0, formatting_and_registration_pending=True))
    print(f"Saved {len(records)} contextual decisions: {dict(counts)}")


if __name__ == "__main__":
    main()
