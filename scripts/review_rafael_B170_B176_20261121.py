"""Record a contextual reread of the Carlo, Cristina, Samwell, and Jam exchanges."""

from collections import Counter
from pathlib import Path

from scripts import pair_rafael_B170_B176_20261121 as paired
from scripts.review_rafael_east_asia_followup_20261121 import TOKEN


base = paired.base
PACKET = paired.PAIRED.with_name("paired_source_registered_candidate_v2.json")
OUTPUT = paired.ROOT / "contextual_decisions_B170_B176_v4.json"
CATALOGUE = Path("translations/editorial_checkpoints/SharedText_20261110_v1/default_actor_names_current_20261120_v1.json")

# Each row is source index, optional replacement, protected phrases, and reason.
DECISIONS = {
    170: """
5|||Carlo opens with a usual quantity of cinnamon, signaling a familiar trading routine.
9|||Rafael privately wonders if another customer got there first. The idiomatic question fits the trade-house entrance.
14|||Adil readily gives the total and starts the price discussion.
18|||Carlo's quick question gives Adil a chance to explain without accusing him outright.
22|What? It's the same as always.|same as always.|Adil acts surprised and passes the new price off as usual.
25|||Carlo laughs and uses Adil's name before challenging him with knowledge of what he paid.
28|Now, hold on...||Adil cuts in uneasily before Carlo makes his case.
32|With this year's harvest and local demand, I'd say you can do a little better.|local demand;a little better.|Carlo cites the harvest and local demand to make a polite case for a lower price.
36|||The alternative seller and the wry appeal to the absence of any obligation turn the conversation into a genuine negotiation.
40|Urgh... A-all right. You've got me there.||Adil gives in with a stammer, as if he recognizes that Carlo has the better argument again.
44|||Carlo's questioning tone marks the turn from bargaining to concern about Adil's health.
47|What is it now, Carlo? You got another complaint about my business?|another complaint|Adil mistakes Carlo's concern for another criticism of his trading practices.
50|I'm serious. You're running a fever. Get some rest tonight, all right?|running a fever.|Carlo reassures Adil that this is a genuine concern and urges an early night.
53|||Adil starts to brush it off, then notices he actually feels a chill.
56|See? I'll come back for my order tomorrow. You should close up for the day.|close up for the day.|Carlo puts off settling the order and gives Adil a concrete reason to close early.
59|||Adil reluctantly accepts the advice and apologizes directly to the other customers.
65|||Carlo acknowledges the inconvenience and checks what the group came for.
68|||Rafael asks how Carlo recognized the owner's illness. The question carries no invented medical detail.
72|||Carlo points to Adil's complexion without presenting his observation as a formal diagnosis.
84|||Fernando makes the compliment into a boast about himself, giving Rafael a reason to question it.
90|...(Is Fernando really that observant?)||Rafael's private doubt answers Fernando's boast. Naming him clarifies the target of the joke.
95|Most people wouldn't have noticed. I'm just quick to pick up on it when someone's unwell.|when someone's unwell.|Carlo explains why he is unusually attentive to how people feel, setting up the later family conversation.
99|||Rafael takes in the answer before Carlo offers practical help.
104|||Carlo names the established Market destination and offers to make up for the group's delay.
107|Thanks. We'll be there.||Rafael accepts the offer for the group.
112|||The innkeeper recognizes Carlo and starts with warm thanks on the following day.
116|How's Adil doing?||Carlo asks after Adil immediately.
120|He's resting at home today, just to be on the safe side.|on the safe side.|The precaution is the innkeeper's explanation, with no claim that Adil has recovered.
123|||Carlo's wish for a quick recovery fits the concern he showed the previous day.
127|||Her exasperation and unfinished thought give the measure of her worry without identifying a family relationship.
131|||She catches herself talking and gives her own grateful assessment of what Carlo did for Adil.
135|That's kind of you. Thank these travelers, too. They put off their trading until today.|put off their trading|Carlo redirects her thanks toward the travelers who agreed to lose a day of business.
139|Oh dear, I'm sorry we kept you waiting. It's nothing much, but... would you take this?|would you take this?|The innkeeper apologizes and modestly offers the item without identifying it.
145|||Carlo thanks her and lets the travelers trade first, using the question about their hurry as a courtesy.
149|||Adil returns in high spirits and apologizes for the inconvenience.
152|||The innkeeper's abrupt exclamation signals surprise and annoyance at seeing Adil out of bed.
156|||Carlo is startled to see Adil against his advice and tells him he should be resting.
159|Hmph! Look at me. I'm fit as ever. On a day this good for business, you expect me to stay in bed?|I'm fit as ever.|Adil indignantly defends his decision, using the good trading day as his excuse.
163|||The innkeeper's exasperated reply fits the familiar exchange without inventing a relationship.
167|Ha ha. You've got plenty of energy, I'll give you that. Just take it easy today.|Just take it easy today.|Carlo is reassured by how Adil is acting and still urges him to take care.
171|I'll be back, maybe tomorrow. Please look after these travelers.|maybe tomorrow.;look after these travelers.|Carlo defers his own business, leaves tomorrow tentative, and asks Adil to attend to the waiting travelers.
174|||Carlo's farewell gives equal weight to family and health, setting up Rafael's invitation and the reason behind it.
177|...||Rafael's silent beat stays on its own panel with the surrounding ASCII punctuation.
183|||Rafael hesitates before calling Carlo back.
188|||Carlo turns back with a simple prompt.
192|||Rafael starts tentatively and asks Carlo to sail with him as a genuine invitation.
197|||The direct question fits Carlo's surprise after what sounded like a farewell.
201|You've got a knack for trade, and you look out for people. I admire that.|you look out for people.|Rafael values Carlo's skill and the kindness he has just witnessed.
206|You haggled pretty well yesterday.||Claudio backs up Rafael's assessment with an easy compliment to Carlo. The complete thought replaces an eight-character opening row.
209|||Carlo modestly attributes his skill to years as a merchant.
213|You're a merchant! Then you know your way around market prices, don't you?|market prices, don't you?|Rafael follows up with an eager question about the specific skill he can see helping the crew.
217|||Claudio's quick recognition picks up the bargaining thread without claiming a formal qualification.
221|||Julio adds a brief note of admiration before Carlo goes quiet.
225|...||Carlo's standalone hesitation uses the same ellipsis as the neighboring dialogue.
229|Hey, Carlo. Rather stay ashore? Would your family mind if you left?|Rather stay ashore?|Claudio wonders why Carlo hesitates and asks if his family might be against him sailing. The familiar address fits the known person.
232|||Carlo's admission interrupts the comfortable exchange. Keep the loss and the one-year interval explicit.
235|...||Rafael has no answer after hearing of the loss. Use the same punctuation as the surrounding dialogue.
241||I was so wrapped up in work...;I didn't take proper care of her.|Carlo explains that his daughter caught the illness and that his absorption in work kept him from caring for her. Keep his hesitation and admission intact on separate rows.
244|||Carlo describes the delayed treatment and losing both his daughter and wife in a few plain, painful sentences.
248|||Rafael's use of Carlo's name conveys solicitude without making the familiar Japanese address imply kinship.
253|...I'd put my work before my family. It felt hollow after that. I've put people's health first ever since.|before my family.;people's health first|Carlo recognizes the emptiness of the work he prioritized and explains the lasting change in what matters to him.
256|||Rafael understands why Carlo paid attention to the shopkeeper and leaves the thought unfinished.
261|...Have you thought about going home?|about going home?|Rafael gently asks whether Carlo will go back to his hometown.
266|||Carlo names Venice and explains why fond memories make it impossible to live there alone.
270|...||Rafael pauses after Carlo explains why he cannot go home. Preserve the standalone pause with standard punctuation.
275|||Rafael's repeated invitation is more earnest this time and states that he needs Carlo.
280|||Carlo has still not decided, which gives Rafael a chance to tell Claudio what he hopes to learn.
284|||Rafael confides what he sees in Carlo, using his familiar name for Claudio.
289|||Claudio relents quietly after hearing Rafael's reasons.
293|...||Carlo's quiet response leaves room for Julio to speak. Use consistent ASCII punctuation.
297|||Julio proposes that all of them become Carlo's new family. This is the exchange's explicit offer of kinship.
301|||Rafael immediately takes up the idea and gives Carlo the decision.
305|...Thank you, everyone. I never dreamed you'd say that.|I never dreamed|Carlo's gratitude comes from being offered a place with the crew and a new family.
308|||Claudio treats the decision as settled and lightens the moment by reminding Carlo they also value his trading skill.
312|||Carlo introduces himself by his full approved name and accepts the new relationship and place aboard.
""",
    171: """
5|Whew. I think we had a little too much to drink.|too much to drink.|Rafael feels the amount he has had and opens the setup for Claudio's defense of drinking.
10|||The claim about men of the sea and the immediate example of Cristina set up Rafael's literal correction.
13|||Rafael catches the contradiction and says Claudio has had too much, setting the scene's teasing tone.
17|||Cristina admits her own drinking and reacts to the music before anyone comments on it.
22|||Rafael hears the music start and describes its fire without naming the dance before Claudio does.
27|||Claudio feels the music's pull and admits it plainly.
31|||Cristina recognizes the tune and excuses herself, leaving the reason for stepping away implicit.
34|||Rafael starts to call her back without finishing the thought.
39|||Claudio calls after her with a crass guess. Privy conveys his directness without contemporary slang.
44|||The first patron reacts to Cristina's dancing. Restore the separate source heading above the cheer.
47|||The second patron responds with praise of both her appearance and her dancing. Keep his separate heading above the response.
52|||Rafael is openly impressed and addresses Cristina directly.
57|||Claudio is briefly at a loss for words before the patrons cheer again.
61|||Both patrons join the repeated cheer. Put the collective label on its own line and preserve the lengthened final Bravo.
64|||Keep the standalone sound of applause after the cheers, with no invented speaker.
68|||Cristina says the song got her to dance, and her affection for it makes the response personal.
71|...Cristina, you were incredible. You looked so good out there.|you were incredible.|Rafael follows his first exclamation with sincere, slightly awkward praise rather than sounding like a second announcer.
76|||Cristina accepts the praise and admits it embarrasses her a little.
80|||Claudio's mock formality in calling Cristina a fine swordswoman has the edge Rafael reacts to. He explicitly names flamenco here.
84|...||Cristina lets the remark hang before Rafael objects. Render the deliberate silence using standard punctuation.
88|||Rafael calls Claudio by his nickname and rebukes his tone directly.
92|I didn't mean to insult you. I thought all you ever did was practice with that sword. You seemed pretty dull to me.|I didn't mean to insult you.|Claudio's defensive explanation stays blunt and gives Cristina a reason to be surprised at what he used to think.
95|||Cristina's quick question lets Claudio hear how his explanation landed.
99|||Claudio's short, hesitant apology makes the ensuing acceptance sincere.
103|You've won me over. I used to think of you as the old man's granddaughter. From now on, you're one of us.|You've won me over.;you're one of us.|Claudio openly changes how he sees Cristina. He acknowledges her established kinship with Julio and welcomes her in her own right.
""",
    172: """
6|||Rafael's amazement leads naturally to Claudio identifying what blocked the road.
11|||Claudio's exclamation keeps the animal, its posture, and its location in their comic order.
14|||Julio compares the street with home in a brief observation that adds no details about either place.
19|Come on over! See anything you like? Everything here's first-rate!|Everything here's first-rate!|Samwell calls out to customers as a vendor before he realizes who the travelers are.
22|Well, I don't get many customers like you. You're travelers, aren't you?|aren't you?|Samwell turns from his sales pitch to a quick, curious guess.
25|||His abrupt request and matter-of-fact boredom with elephants make the invitation funny. He says he wants to see other countries.
28|H-huh? That's a little sudden. We are sailors, but... What are you good at?|What are you good at?|Rafael is caught off guard and asks for relevant skills before he considers taking a stranger aboard.
33|||Samwell's throat clearing and confident boast fit his later self-congratulation. The practical question answers Rafael.
36|Hmm, cooking... We do have someone who can cook already.|can cook already.|Rafael thinks it over and recalls the crew already has a cook. The pause leaves room for a second offer.
40|I'm good with my hands, too. I bet I could work as a shipwright. Maybe even make maps!|work as a shipwright.|Samwell presents both the shipwright and mapmaking as things he thinks he could do.
44|||Samwell lists quick learning and good instincts as his reasons for confidence and affirms his own pitch.
48|||Claudio cuts through the boasts by asking about real experience.
51|Not a bit!||Samwell answers without embarrassment. The confident admission provokes Claudio's disbelief.
55|||Claudio is briefly dumbfounded at the direct answer.
59|||Julio's plain observation draws out the contrast between boasting and experience without dismissing the young man.
62|What's so strange about that? I'm young. Give me a chance and I'll pick it up in no time. I told you, I've got good instincts. Ahem!|good instincts.|Samwell appeals to youth, adaptability and instincts, then punctuates his own argument.
65|||Rafael is already persuaded by Samwell's attitude and speaks simply.
69|||Claudio reminds Rafael that the admiral should think through a recruitment decision.
73|He's right. You're being a little hasty here.|a little hasty here.|Samwell unexpectedly agrees with Claudio, creating the joke on Rafael's reversal.
76|||Rafael catches the contradiction and reminds Samwell who asked to be hired.
81|||Samwell wants Rafael to see what he can do before taking his abilities on trust.
85|||Rafael hands Samwell the initiative by asking what he wants to do.
90|Go on. Test me.||Samwell openly asks for a chance to prove himself.
94|||Rafael asks for specifics before committing to the test.
99|I'll cook something for you. If everyone likes it, I pass. How's that?|If everyone likes it, I pass.|Samwell offers to make one unnamed dish and makes unanimity about the taste his proposed test.
103|||Rafael agrees to the audition and invites Samwell to start.
110|||Samwell thanks them for waiting and serves the dish without naming it.
114|What's this? Looks pretty strange. It's nothing nasty, is it? (Munch, munch.)|is it?|Claudio voices his suspicion and starts eating anyway. Retain the comic sound of chewing.
118|||The stretch in good and the repeated praise preserve Claudio's abrupt change of heart.
121|||Rafael agrees plainly and adds his own praise for the taste.
126|Oh, that's good. Hm. Appearances can fool you, can't they?|can't they?|Julio agrees, then gently remarks that appearances give a poor guide to someone's ability.
129|||Samwell uses a natural English rendering of the hidden-claw proverb while putting on a conspicuously proud air.
133|||Claudio points out the contradiction in Samwell quoting it about himself.
137|||Rafael checks for agreement and proposes that Samwell join them.
141|I did it! I'm Samwell da Khan. Glad to be joining you!|Samwell da Khan.|Samwell celebrates passing, introduces himself with the full spoken name, and looks forward to joining the group.
""",
    173: """
5|||The sailor wakes Rafael in a panic, stumbles over the ship, and gets the news out.
8|Mmm... What is it? It's so early...||Rafael's sleepy response carries the morning timing and builds contrast with the sailor's urgency.
12|||Claudio hears the news clearly and cannot yet believe it.
23|||Arcadius qualifies her response and recognizes the seriousness if the report is true.
29|It is! Come to the departure office, quick!|departure office, quick!|The sailor insists and asks the group to come to the established office immediately.
32|||Seeing the empty berth makes Rafael move from disbelief to the repeated confirmation that the ship is gone.
36|||The sailor stammers in panic and asks what they should do.
48|||Arcadius soberly confirms what they see, keeping her comparatively measured voice.
54|||Claudio demands to know what happened, prompting the worker's account.
58|||The worker calls urgently for the admiral's attention.
62|It's bad! Early this morning I saw some skinny young guy fiddling with the ship all by himself. And then...|skinny young guy;all by himself.|The worker gives the time, the man's build and the fact he was alone, then pauses before the outcome.
66|||The worker's separate punch line reports that the stranger sailed straight out of port.
70|Hey! You can't just say he sailed right out like it's nothing!|like it's nothing!|Claudio takes issue with the casual way the worker puts it rather than asking for the event again.
81|||Arcadius admires the feat at the wrong moment, giving Claudio something specific to snap at.
84|Quit admiring him! We don't have time to stand here and marvel!|Quit admiring him!|Claudio interrupts Arcadius's admiration and calls for urgency.
91|||The worker explains why he assumed the man was checking the ship and didn't expect a departure.
95|||Rafael finds the assumption reasonable and absolves the worker without turning it into an official decision.
99|||Rafael wonders how unusual the stranger must be to sail on his own, anticipating his reaction to Jam.
103|||Claudio calls for a search around town and vows to catch the ship thief.
""",
    174: """
6|||The worker's casual separate follow-up reports that the ship still seems to be away.
""",
    175: """
6|||This separate conditional follow-up gives the same news in the same worker voice. The native reference stays distinct.
""",
    176: """
5|||The port worker repeats Rafael's title in excitement and reports that the ship is back.
8|||Rafael's two short exclamations make his surprise clear.
13|||The worker points to the ship and insists there can be no mistake.
18|Yahoo! Nothing like the open sea! Look how far it goes!|the open sea!|Jam celebrates the sea's breadth in exuberant bursts without bluntly repeating similar adjectives.
22|Whew, I've been having a blast since sunup. What a beautiful day! Yahoo!|since sunup.|Jam is pleased with both the morning's outing and the good day. Keep his signature cheer.
25|||Rafael's private surprise registers that Jam exceeds even the earlier report.
30|||Claudio rebukes Jam in a direct voice and identifies the specific wrongdoing.
34|||Jam's feigned confusion leads to the absurd claim that he found the ship lying around.
37|||Claudio contests that exact claim as he would the excuse for taking a small object.
40|||Jam makes the ship look lonely and abandoned in his own account, and insists the story is true.
44|||Jam praises his own kindness, spells his first name aloud and ends with his familiar cheer.
47|You took it because you found it? But how'd you get it moving all by yourself?|all by yourself?|Rafael stays on the odd logic just long enough to ask about the feat that actually interests him.
52|||Jam gives an uninformative description of his actions and admits he winged it, then cheers.
55|||Rafael is openly impressed by the feat, which raises Claudio's frustration.
60|||Claudio spells out how reckless it was and asks what Jam would have done had the ship sunk.
64|||Jam dismisses the concern with a click of the tongue and insists on sharing his own wisdom.
68|Where there's a will, there's a way! Yahoo! If it's OK by me, it's OK!|there's a way!|Use the familiar proverb Rafael echoes later and keep Jam's self-serving logic and audible OK flourish.
79|||Fernando recognizes immediately that the newcomer will be trouble.
86|||Rafael repeats the exact proverb with a doubtful little pause.
91|Of course it worked! I'm the one who did it. Here's another one. Live large, live short!|I'm the one who did it.;Live large, live short!|Jam claims his own success and gives his deliberately bombastic version of living a big, fiercely short life.
95|Keep my head down just to live a long, dull life? I'd be bored out of my skull!|bored out of my skull!|Jam derides the opposite life of keeping one's head down to make it last longer.
98|||Claudio stops trying to reason with Jam and asks Rafael whether to turn him over to the guards.
102|||Rafael rejects the guard option and instead proposes that they recruit Jam.
106|Whoa, FI. Has his idiocy rubbed off on you, too?|rubbed off on you|Claudio's insult is aimed at Jam's behavior and now teasingly includes Rafael.
109|Come on, he sailed a whole ship by himself! That's incredible. Jam, right?|a whole ship by himself!|Rafael defends his respect for the feat and checks the stranger's name before inviting him.
114|||Rafael turns straight to Jam with a simple offer to sail with him.
119|Hmm. Do I go or don't I? What to do... Just a moment! Hang on. I'll decide in two seconds!|Just a moment!;in two seconds!|Jam drags out the decision theatrically. Keep the spoken English flourish and the exact promised two seconds.
122|||Jam gives an emphatic signal that he has decided after the brief hold.
126|||Rafael asks for the answer as if the hesitation was sincere.
131|Yep. I've decided. I won't go! See you around! Have a good voyage!|Have a good voyage!|Jam pretends to refuse, then commits to the joke by giving them a full farewell.
135|||Rafael's disbelief and stammer give Jam exactly the reaction he wanted.
140|||Jam reveals the trick and keeps the French flourish as its own beat before the admission.
143|||Rafael repeats the revelation in disbelief without explaining the joke on Jam's behalf.
148|||Jam accepts with enthusiasm, gives his full spoken introduction, and closes with his signature cheer.
""",
}

HEADINGS = {
    "DK4_MES_B171_R0044": ("＜客１＞", "Patron 1:"),
    "DK4_MES_B171_R0047": ("＜客２＞", "Patron 2:"),
    "DK4_MES_B171_R0061": ("＜客１＞＜客２＞", "Patrons:"),
}


def main():
    packet = base.load(PACKET)
    assert packet["candidate_sha256"] == base.digest(paired.parent.ROM)
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    names = {r["actor_ID"]: r["progressive_nameplate"]
             for r in base.load(CATALOGUE)["source_and_current_default_name_fields"]}
    records = []
    for group in packet["groups"]:
        block = group["block"]
        decisions = [line.split("|", 3) for line in DECISIONS[block].strip().splitlines()]
        assert len(decisions) == len(group["records"])
        for row, (index, replacement, protected, note) in zip(group["records"], decisions, strict=True):
            assert int(index) == int(row["id"][-4:])
            selector = row["selector"]
            old = " ".join(row["current_English"].split())
            english = replacement or old
            heading = HEADINGS.get(row["id"])
            if heading:
                assert selector == 254 and row["Japanese"].splitlines()[0] == heading[0]
                assert english.startswith(heading[1] + " ")
            assert TOKEN.findall(english) == TOKEN.findall(old) == TOKEN.findall(row["Japanese"])
            phrases = protected.split(";") if protected else []
            assert note and row["earlier_source_meaning"]
            assert all(phrase.casefold() in english.casefold() for phrase in phrases)
            reflow = heading or (selector == 254 and english == old and bool(phrases))
            decision = "revision" if english != old or reflow else "retention"
            change_class = ("wrap-only" if reflow else "glyph" if old and not old.isascii() and english == "..."
                            else "wording" if decision == "revision" else "retention")
            record = dict(id=row["id"], file_path=row["file_path"], route=0, block=block,
                source_record_index=int(index), source_selector=selector, native_command_word=0x4000, native_slots=[],
                source_reference=row["source_reference"], current_reference=row["current_reference"],
                source_hex=f"{selector:02x}" + row["source_reference"]["exact_body_hex"],
                current_hex=f"{selector:02x}" + row["current_reference"]["exact_body_hex"],
                Japanese=row["Japanese"], previous_English=old, english=english,
                speaker=names[selector] if selector != 254 else "System panel",
                context=row["earlier_context"], source_meaning=row["earlier_source_meaning"],
                localization_note=note, finding=note, protected_phrases=phrases, decision=decision,
                change_class=change_class, kind="system-FE" if selector == 254 else "progressive",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
            if heading:
                record["source_heading"], record["english_heading"] = heading
            records.append(record)
    assert len(records) == 190
    findings = Counter(row["change_class"] for row in records)
    release = base.load(paired.parent.RELEASE)
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(PACKET), source_packet_sha256=base.digest(PACKET),
        earlier_glosses=str(paired.EARLIER), earlier_glosses_sha256=base.digest(paired.EARLIER),
        records=records, findings=dict(findings), new_editorial_credit=0,
        status="Contextual review complete. Stored formatting, gameplay and release checks pending."))
    print(f"Reviewed {len(records)} records. {dict(findings)}")


if __name__ == "__main__":
    main()
