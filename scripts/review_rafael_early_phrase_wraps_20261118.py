"""Review eight flagged wraps in the context of Rafael's complete exchanges."""

from collections import Counter
from pathlib import Path

from scripts import register_papal_states_titis_20261118 as parent
from scripts.review_papal_states_titis_20261118 import GATES, TOKEN, base, logical

ROOT = Path("work/rafael_early_phrase_wraps_20261118")
SOURCE = ROOT / "paired_source.json"
OUTPUT = ROOT / "contextual_review_v1.json"
BLOCKS = ((0, 9, 26, 36, 54, 60, 64, 67), (), (), ())
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"

# Each exchange was read against the clean Japanese and the installed English.
CONTEXT = {
    0: "Rafael recognizes Africa's Proof of Conquest. Clau celebrates and reacts to needing seven. The crew decides to head east into the Indian Ocean.",
    9: "Kurushima taunts the visitors and boasts about his armored ships. Rafael is curious, Aziza is amazed, and Clau prepares for trouble. Rafael stops him from attacking first.",
    26: "After the betrayal and rescue, Rafael asks about piracy. Aziza talks about her father and his sword, admits what she really wanted, and then accepts Rafael's invitation to sail with them.",
    36: "The lookout spots an unknown fleet. The crew goes from uncertainty to recognizing Hayreddin and understanding his importance at Gibraltar, then turns to getting through the encounter.",
    54: "A shopkeeper tells Rafael the story going around about Espinosa's defeat. News of the governor's move prompts Rafael to hurry away, leaving the shopkeeper puzzled.",
    60: "Pereira agrees to bet on Rafael. Rafael reveals that he must leave immediately for Europe and entrusts the region to Pereira. They discuss what happens with Kuhn, rivalry and the terms of the agreement.",
    64: "Charlotte introduces herself after the trade and explains how her Romani community came to the New World. Rafael's question about going back prompts her explanation. They part on a promise, and the crew decides to help the village.",
    67: "Charlotte hands over the latest goods. Rafael offers corn seed and worries about her load. Clau divides it and sends them off, then congratulates himself for helping.",
}

# The first field is the clean-source reading. The second explains the retention
# or the proposed adaptation in this specific conversation.
NOTES = {
    0: """
5|Rafael realizes this is Africa's Proof of Conquest.|The pause carries his amazement. The full name occupies one line, before Clau celebrates.
10|Clau celebrates finally achieving it.|The short outburst gives the reveal an immediate answer.
20|Clau marvels that they need as many as seven.|The question keeps his incredulity and the exact count.
25|Arcadius calmly confirms collecting seven.|The direct confirmation plays against Clau's reaction.
32|Rafael asks which region's Proof they should seek next.|The open question preserves both the item and the choice of region.
37|Clau says adventurers have to push on and proposes going east.|The tag and invitation keep Clau's enthusiasm and their current heading.
48|Julio names the Indian Ocean as the next venture.|The short reply lands as an enthusiastic confirmation.
55|Rafael considers the Indian Ocean and decides to go.|The pause before agreement preserves the decision beat.
""",
    9: """
9|Kurushima laughs and threatens to wreck the foreigners' puny ships.|The boasts and laughs bookend a specific threat to the ships.
13|Kurushima boasts loudly that his iron-armored ships are invincible.|The compressed boast follows his cackle and identifies the feature that surprises the crew.
17|Rafael wonders aloud whether these ships are also maneuverable.|The tentative interruption and comparison continue his curiosity about ship design.
30|Aziza is amazed that such ships exist.|The broken-off reaction lets her surprise play before Clau interrupts.
36|Clau objects that nobody told him their opponents had iron-armored warships.|Leading with the ships makes his interruption immediate and gives both thoughts one line.
40|Rafael speculates that these may be one of the ship types Xien described.|The wording keeps the idea tentative and names his source.
45|Clau thinks this is no time to take it easy, then calls for focus.|The objection and move from talk to action suit his impatience.
49|Rafael stops Clau because attacking first would make them look like pirates.|The stammer and unfinished ending keep his anxious objection.
""",
    26: """
217|Aziza is shaken by her crew's betrayal and asks why Rafael saved her.|Her self-reproach precedes the guarded question.
220|Al says the situation left little choice.|The terse answer fits his delivery and leaves Clau room to add his own.
224|Clau says they couldn't leave her there.|The contraction and plain wording keep his instinctive reply.
228|Rafael cites her help at the Basra tavern and asks permission to ask about piracy.|The location and the reciprocity stay explicit in a tactful question.
232|Aziza says her father was a pirate, so she is a pirate's daughter.|She states her identity bluntly after a pause.
235|The men served her father and she learned swordplay and piracy by watching.|Preserves the men's connection and her practical apprenticeship.
239|Rafael hesitantly asks about her father.|The short question gives Aziza control of how much she says.
244|He died in an accident and the sword he owned disappeared with him.|Both facts stay separate and the trailing pause leaves room for Al.
248|Al identifies the Bloodstained Shamshir.|The artifact title remains intact.
251|Rafael understands why she remarked on his fine sword.|The reference to her prior praise links this exchange to the earlier one.
255|Aziza wanted to be a great pirate like her father and imitated him in everything.|The repetition of her father is deliberate and prepares her change of heart.
259|Hearing that the crew had the sword made her determined to get it, for a reason she hesitates to say.|The opening causal clause stays intact. Aziza still trails off before Rafael's silence.
262|Rafael listens in silence.|Preserve the silent turn before Aziza finishes the thought.
267|She thought having it would prove she was closer to being like her father, then reconsiders.|The little laugh and the trailing reversal carry the turn into her admission.
271|She realizes her real wish was for a keepsake from her father.|The wording preserves the distinction between a memento and ambition.
275|She accepts why her crew abandoned her over a pursuit that brought them no money.|The crew's anger remains understandable to her without excusing the betrayal.
279|Al asks whether piracy still holds any appeal for her.|The blunt question gives Aziza room to answer directly.
283|Aziza says it was her father she was after and she plans to quit piracy.|The repeated pursuit phrasing connects her explanation to the sword and keeps the metaphor.
287|Rafael invites her to join them, saying life at sea suits her better.|The warm offer is framed as fit for the sea with no imposed loyalty.
292|Aziza asks if they are really willing to take her.|The broken phrasing carries her uncertainty about the invitation.
295|Rafael answers immediately in the affirmative.|The short reassurance supports the preceding invitation.
300|She thanks them and promises to work hard because they saved her life.|The debt motivates what she says here and Clau's echo later.
304|She tells them to call her Aziza.|The direct invitation to use her name marks the thaw.
307|Clau repeats that she calls Rafael her lifesaver.|The tease keeps the native given-name substitution.
310|Rafael thinks she overstates it, says they helped each other, and welcomes Aziza.|His modest deflection recalls Basra and gives her an unambiguous welcome.
""",
    36: """
5|A lookout tells the admiral ships that appear hostile are in sight.|The warning preserves the role address and uncertainty.
16|Janus asks what fleet it is.|The question keeps the lookout's sighting unresolved.
23|Clau guesses they might be pirates.|The one-word question works as a quick guess.
27|Rafael hopes they are not in trouble.|The understated worry is spoken in his usual register.
39|If the ships are pirates, a fight is unavoidable.|The conditional and certainty fit together on one line without revealing their identity too early.
46|Julio recognizes Algiers pirates and wonders if a particular man is there.|His growing recognition stays tentative until he names Hayreddin.
49|Rafael asks about the Algiers pirates.|The echo lets Julio give the needed explanation.
54|They operate from the North African coast and raid near Algiers.|The two geographical details stay distinct.
66|Janus confirms the fleet really is pirates.|The quick echo gives Clau a cue to react.
73|Clau reacts to an immediate difficulty.|The outburst keeps the timing and his frustration.
77|Julio recognizes Barbarossa Hayreddin.|The brief recognition ends with the established full name.
80|Rafael asks how strong he is.|The simple question keeps the perspective of a captain still learning.
85|Hayreddin's men stand out for strength and ruthlessness.|The existing idiom preserves the comparison to other Algiers pirates.
89|Clau cannot believe it.|The short interjection works in the escalation.
93|The strongest current Mediterranean power, the Ottoman Turks, is rumored to be involved.|The two sentences keep present power and reported involvement distinct.
97|Clau pictures men at the entrance and their boss at the far end.|The nautical geography stays a colloquial reaction without adding a military post.
101|Trading in the Mediterranean first requires dealing with the man who controls Gibraltar.|The condition and specific strait remain clear.
113|Janus sighs about the difficulties ahead.|The brief aside keeps his measured reaction.
120|Julio says their immediate priority is getting through the encounter.|He moves the talk from future trade to survival.
123|Clau asks how they'll get through it.|Echoing Julio ends on the practical question.
""",
    54: """
5|The shopkeeper calls out and asks whether Rafael heard.|The two short calls suit a stranger starting a rumor exchange.
9|Rafael asks what he means.|The one-word prompt keeps his surprise.
14|The shopkeeper reports hearing that Fernan Silveira defeated the infamous Espinosa.|Keep the report as hearsay. Use Fernan's name and the shopkeeper's colloquial register.
18|Rafael realizes this is the version going around.|The pause and restrained reply fit his reaction to the reported version.
23|The puzzled shopkeeper nonetheless prefers Silveira to Espinosa, who did bad things.|The asides sound conversational and keep his personal comparison.
26|Rafael agrees only tentatively.|The existing hesitation answers the comparison.
31|The shopkeeper hears the governor's office is being moved to Sofala.|The rumor remains hearsay, with the office kept together and the destination intact.
35|Rafael recognizes the African governor's office and Sofala, thanks the man and rushes to go.|The repeated realizations build urgency without assigning a relationship.
40|The shopkeeper calls after him and wonders what happened.|The trailing surprise fits Rafael's sudden exit.
""",
    60: """
255|Pereira lets out a small laugh.|The pause leads into his open amusement.
259|Pereira laughs, calls Rafael remarkable and admits he is impressed.|This response keeps both the humor and the change of attitude.
263|Pereira decides to bet on Rafael and tells him to leave the rest to him.|The gambling metaphor fits the former resistance and new trust.
267|Rafael accepts and asks Pereira to take care of it.|The more personal acceptance keeps the request and leads into Pereira's question.
273|Pereira wants to know what Rafael means.|The quick question invites the reveal.
277|Rafael says they will leave Southeast Asia immediately.|The short phrasing keeps the timing and region within one native line.
281|Pereira asks what follows.|The brief prompt makes Rafael spell out the plan.
285|Rafael heads to Europe to defeat Spain's Valdes.|The existing line preserves both destination and opponent.
289|Pereira double-checks what he heard.|The question sounds like disbelief in context.
293|Rafael says Spain could permanently strip Portugal's royal family of succession rights and time is short.|The hypothetical preserves his strategic reasoning and the urgency.
297|Pereira agrees, then bluntly asks whether Kuhn comes later.|The question keeps Kuhn distinct from Valdes and prompts the clarification.
301|Rafael explicitly trusts the governor of Indochina, who oversees the region.|The title is source-stated and the transfer of responsibility is clear.
306|Pereira understands he is being asked to guard their rear.|The idiom fits the military context and admits Rafael's logic.
309|Trusting him with the region lets Rafael devote their strength to facing Valdes.|The handoff and its practical consequence remain linked.
314|Pereira laughs at finding himself already part of Rafael's strategy.|The game-piece metaphor carries his mixture of amusement and surprise.
318|He accepts and asks what happens if he drives Kuhn out himself.|The conditional leaves the outcome open.
322|Rafael already has the key to the Proof and can cede the region's trading rights.|The two distinct objectives remain clear.
327|Pereira bristles at potential pity and says Rafael can take the region and beat him later.|The bravado follows the offer and keeps the rivalry alive.
330|Rafael stammers a protest.|The cut-off response sets up Pereira's appeal to competition.
335|Pereira invokes fair business and free competition.|The two questions maintain his point without treating the outcome as predetermined.
338|Rafael tentatively agrees and starts to object.|The stammer follows his surprise without finishing his thought.
343|Pereira demands that Rafael defeat Valdes and asks for agreement.|The firm instruction follows his acceptance of the rivalry.
346|Rafael readily agrees.|The decisive response fits his commitment.
354|Pereira reflects that these people might indeed restore Portugal.|The repetition keeps the quiet turn from banter to belief.
""",
    64: """
283|Rafael has not asked her name yet, gives his own and asks hers.|The introductions remain conversational and preserve Rafael's name substitution.
287|Charlotte repeats Rafael's name and gives hers.|The short reply preserves the reciprocal introduction and substituted name.
290|Rafael asks why they built on such barren land.|The question opens the story while retaining his genuine puzzlement.
295|Charlotte identifies her community as Romani and says they traveled across Europe.|Clear self-identification and past travel introduce her history in her own voice.
298|She remembers walking hard to keep up while holding her mother's hand.|The specific memory makes the past personal without embellishment.
301|They were offered a chance to settle in the New World.|The line keeps the offer open and does not invent its source.
305|The offer promised abundant gold and vast fertile land said to be untouched.|The hearsay matters as Charlotte later describes what they found.
309|They talked it over, pooled the little money they had and chose to cross.|Pooling their last coins keeps the financial stakes and collective choice.
313|Her parents and community initially hoped for land and their own village.|The trailing thought lets the promise sound like their hopes.
316|Their hope soon turned to despair.|The succinct reversal gives her next line room to explain.
319|Indiscriminate digging found no gold and there was barren land everywhere.|The two details follow the specific promises and keep her disillusionment.
322|Rafael condemns conning people out of their money.|His angry response follows the broken promises and keeps the financial motive.
326|They were devastated but encouraged one another and decided to build a village.|The revision gives Charlotte a more conversational voice and keeps their decision.
330|Growing food was difficult because they had never owned land, and it remained difficult.|The two sentences keep the ongoing struggle and its specific cause.
333|Rafael asks if the hardships ever made them consider returning to their country.|Keep the assumed country explicit so Charlotte's correction still answers him directly.
337|Charlotte says the Romani have no country of their own to return to.|The opening echo and plain answer preserve both the correction and its weight.
340|People blamed the Romani for missing things or spreading illnesses.|The two examples expose the prejudice in Charlotte's own account.
343|People across Europe looked at them with disgust.|The blunt simile preserves the dehumanization she recalls.
347|Rafael is silent.|The silent reply leaves room for the account to continue.
352|Two or three years ago they finally grew enough to sustain themselves and felt the village was theirs.|The time, self-sufficiency and emphasis on belonging all survive.
355|A ship stopped about a year ago and barter began bringing new goods.|The time and chance encounter give a clear lead into trade.
358|People often buy their goods for a pittance and they feel they have little choice.|The example and lack of alternatives explain their reaction to Rafael's help.
363|Charlotte tells Rafael she was happy he helped her.|The hesitancy and native name substitution keep it personal.
367|She never expected anyone to help her.|The existing line explains her emotional reaction plainly.
370|Rafael realizes his first approach had hurt her.|His simple acknowledgment follows her account without adding a claim about intent.
375|Charlotte acknowledges his good intentions and says she should have thanked him for helping.|Restore the distinction between reassuring Rafael and admitting she owed him thanks.
379|She asks if he will come back.|The direct question shifts from the past to a possible future visit.
383|He assures her he will.|The spoken assurance fits the tender close.
388|She asks for confirmation.|The short question leaves space for his promise.
392|He promises to return.|The firm promise answers her directly.
397|She insists he keep it and says she will wait.|The friendly insistence matches her anticipation.
401|He agrees and says goodbye.|The compressed farewell follows the promise.
406|She calls after him to keep the promise.|The final repetition is present in the source and works as she leaves.
410|Rafael realizes she left and only then notices Clau.|The two beats preserve the sudden shift to the crew.
414|Clau admits the story made him tear up.|His casual outburst keeps the humor gentle and the feeling clear.
418|Arcadius regrets what she went through in Europe and the New World.|The wording keeps sympathy and both settings.
422|Rafael realizes Arcadius also heard.|The echo links Arcadius's presence to Clau's.
427|Arcadius apologizes and says he did not mean to listen in.|The polite apology preserves his curiosity without excusing it.
439|Rafael compares it to the threat of Spain annexing Portugal and losing his own place.|The threatened annexation and his personal reaction remain distinct.
444|He realizes they have never had a place where they belonged.|The explicit history gives his realization its weight.
451|Clau urgently asks Rafael if they can do anything.|The native given-name substitution makes the appeal direct.
455|Arcadius suggests finding a way to help the village develop even if it takes time.|The measured answer leaves the timing open and gives the crew a goal.
458|Rafael agrees to do it.|The compact agreement ends the decision beat.
""",
    67: """
5|Charlotte presents the current delivery.|The short handoff keeps the delivery distinct from the gift Rafael is about to offer.
9|Rafael thanks her, then hesitantly says he has something to give her.|The slight pause and separate complete thought give the gift its own beat.
14|Charlotte asks what it is.|Her brief prompt draws out his explanation.
18|Rafael offers corn seed and hopes it could become a new trade good.|The specific seed and possible benefit stay clear.
23|Charlotte is touched that Rafael is always kind to her and trails off.|The pause preserves gratitude and the native name substitution.
26|Rafael gets flustered and says a new trade good would help them too.|The stammer and practical explanation fit his modest reply.
31|She agrees, thanks him and says everyone will be glad.|The wording keeps the village's reaction and her own thanks.
34|Rafael is pleased but notices she is carrying a lot.|His shift to the heavy load motivates what Clau does next.
38|Charlotte says working in the fields has made her strong enough.|The ordinary description keeps both her competence and the reason.
41|Rafael starts to object.|The cut-off turn lets Clau take over.
46|Clau tells Rafael to walk Charlotte back.|The imperative and live name substitution fit his nudging role.
49|Rafael is taken aback.|His brief reaction lets Charlotte object.
54|She feels it would be imposing and insists she can manage.|The polite refusal and invitation to look follow her confident account.
57|Clau tells her not to worry and asks for the load.|His brusque encouragement suits taking action without ceremony.
60|Clau divides the load and deliberately makes Rafael's part heavier.|The specific gag depends on the native given name and remains intact.
64|He finishes the division and hands over a share.|The direct wording follows his busy aside.
67|Rafael protests in surprise and calls out to Clau.|The exclamations work as a flustered response.
71|Charlotte apologizes and asks whether it is heavy.|The short question keeps her concern and the immediate setup.
74|Rafael insists emphatically that it is not heavy.|The emphatic denial is the comic answer to her concern.
78|Rafael says he will go and starts to ask Clau to handle things there.|The unfinished request allows Clau to interrupt.
82|Clau tells Rafael to leave things to him and hurries them along.|The familiar encouragement completes the invitation to leave.
85|Clau sighs at their awkwardness.|The colloquial aside expresses his exasperation without adding a relationship.
88|Clau thinks Rafael falls short in the details and needs him around.|The familiar brag fits the joke, preserving the captain's substituted name.
""",
}
REVISIONS = {
    (0, 5): ("So this is it... Africa's Proof of Conquest!", ("So this is it...", "Africa's Proof of Conquest!")),
    (9, 36): ("Ironclad warships?! Nobody told me!", ("Ironclad warships?!", "Nobody told me!")),
    (26, 259): ("So when I heard you had his sword, I had to have it. I thought...", ("you had his sword,", "I had to have it.", "I thought...")),
    (36, 39): ("Pirates would mean a fight for sure.", ("a fight for sure.",)),
    (54, 14): ("Word is Fernan Silveira took down the infamous Espinosa!", ("Fernan Silveira", "the infamous Espinosa!")),
    (54, 31): ("I hear the governor's office is moving to Sofala...", ("the governor's office", "is moving to Sofala...")),
    (60, 267): ("Yes. I'm counting on you!", ()),
    (60, 277): ("We're leaving Southeast Asia now.", ("Southeast Asia",)),
    (64, 326): ("We were all devastated, but we kept each other going and decided to build a village.", ("kept each other going", "build a village.")),
    (64, 333): ("Didn't you ever think about going back to your country when things got that bad?", ("Didn't you ever think about", "going back to your country", "when things got that bad?")),
    (64, 375): ("You meant well. I should've thanked you for helping me.", ("for helping me.",)),
    (67, 9): ("Thanks. Charlotte... I've got something for you.", ("Thanks. Charlotte...", "I've got something for you.")),
}


def main():
    assert not OUTPUT.exists()
    packet, release, queue = map(base.load, (SOURCE, parent.RELEASE, QUEUE))
    assert packet["candidate_sha256"] == queue["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    actors = base.load(Path("translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json"))["records"]
    open_wraps = {(r["file_path"], r["block"], r["offset"]): r for r in queue["records"]
                  if r["disposition"] == "open editorial lead"}
    records, used, resolved = [], set(), []
    for group in packet["groups"]:
        route, block, path = (group[k] for k in ("route", "block", "file_path"))
        decisions = {int(i): (meaning, note) for i, meaning, note in
                     (line.split("|", 2) for line in NOTES[block].strip().splitlines())}
        dialogue = {data["source_record_index"]: data for data in group["records"]}
        assert decisions.keys() <= dialogue.keys()
        for idx, (meaning, note) in decisions.items():
            data = dialogue[idx]
            selector = data["selector"]
            assert data["native_command_word"] == 0x4000 and data["slots"] == []
            previous = logical(data["current_English"])
            key = (block, idx)
            english, phrases = REVISIONS.get(key, (previous, ()))
            if key in REVISIONS:
                used.add(key)
                assert english != previous and english.isascii()
            assert TOKEN.findall(english) == TOKEN.findall(previous) == TOKEN.findall(data["Japanese"])
            source, current = (dict(file_path=path, block=block, offset=data[f"{side}_offset"],
                    command_offset=data[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                    exact_stored_hex=bytes([selector]).hex() + data[f"{side}_body_hex"]) for side in ("source", "current"))
            source["record_index"] = idx
            row = dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block, kind="progressive",
                native_command_word=0x4000, source_selector=selector, native_slots=[], source_reference=source,
                current_reference=current, source_hex=source["exact_stored_hex"], current_hex=current["exact_stored_hex"],
                Japanese=data["Japanese"], previous_English=previous, english=english, context=CONTEXT[block],
                speaker=actors[selector]["current_consumers"][0]["text"], source_meaning=meaning, localization_note=note,
                protected_phrases=list(phrases), finding="prose" if key in REVISIONS else "retention",
                decision="revision" if key in REVISIONS else "retention", review=dict.fromkeys(GATES, True) | {"formatting": False})
            if lead := open_wraps.get((path, block, current["offset"])):
                assert lead["stored_body_hex"] == data["current_body_hex"] and key in REVISIONS
                row["wrap_lead"] = lead["findings"]
                resolved.append(row["id"])
            records.append(row)
    assert used == REVISIONS.keys() and len(resolved) == 8
    counts = dict(Counter(row["finding"] for row in records))
    base.save(OUTPUT, dict(source_packet_sha256=base.digest(SOURCE), previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=GATES, records=records, decisions=counts,
        resolved_wrap_leads=resolved, new_coverage_credit=0, formatting_and_registration_pending=True))
    print(counts)


if __name__ == "__main__":
    main()
