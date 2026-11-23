"""Record contextual decisions for Rafael's Al, Angelo and Ian encounters."""

from collections import Counter

from scripts import review_rafael_B166_followup_20261121 as previous


BASE = previous.parent.base
ROOT, PACKET, CATALOGUE = previous.ROOT, previous.PACKET, previous.CATALOGUE
SOURCE_REVIEWS = {
    167: previous.SOURCE_REVIEW,
    168: previous.SOURCE_REVIEW.with_name("rafael_B168_B169_integrated_final_review_v1.json"),
    169: previous.SOURCE_REVIEW.with_name("rafael_B168_B169_integrated_final_review_v1.json"),
}
OUTPUT = ROOT / "B167_B169_contextual_decisions_v2_final_candidate.json"
CONTEXTS = {
    167: "Rafael overhears Al's dismissal as a bodyguard. Al rejects Rafael's polite approach and insists that he is a mercenary. Claudio offers him a chance to use his skills at sea without pretending there is no risk. Al recognizes what Claudio is doing and accepts.",
    168: "Angelo is looking for work as a navigator. He mistakes Rafael for a boy on the crew and trades insults with Claudio before apologizing. Claudio and Rafael invite him aboard. Angelo later explains the economics of trading outside the established Mediterranean routes.",
    169: "Ian is harassed at work and is dismissed after defending himself. The same man returns with a group and tries to retaliate. Rafael helps Ian, recognizes his skill, and invites him to sail. Ian accepts as an experienced navigator who is out of work.",
}

# A blank replacement retains the active translation. Phrases guide the formatter.
DECISIONS = {
    167: """
5|||Al distinguishes the job he was hired to do from the errands his employer demands.
9|||Rafael's wordless reaction lets the argument continue without interrupting it.
14|||The employer calls Al lazy and cites the wages as a reason to expect obedience.
17|If you want someone who'll jump whenever you say so, hire somebody softer. I put my life on the line for this job.|my life on the line|Al resists blind obedience and points out what he risks as a guard.
21|||The patron's rhetorical question mocks Al for being good only at fighting.
25|Fine. I'll hire someone who can follow orders. Get out of my sight!|Get out of my sight!|The employer takes Al's challenge literally, dismissing him in anger.
31|||Al refuses to be intimidated and throws the decision back at his employer.
35|That Al! Just because he's good in a fight, he thinks he can do whatever he wants.|good in a fight|The attendant attributes Al's arrogance to his fighting ability.
39|||The employer calls Al insolent and orders his attendant to find a replacement immediately.
42|||The attendant agrees, then hesitantly points out how hard it will be to find anyone as strong as Al.
46|||The employer answers that overcoming that obstacle is the attendant's responsibility.
50|||Rafael seizes on the description of Al's strength and sees it as an asset to the crew.
54|||Claudio calls out Rafael's optimism and how easy he thinks recruitment will be.
63|||Claudio anticipates the difficulty of persuading Al in this variant.
68|||Julio expresses the same doubt in his more measured voice in the alternate response.
74|||Rafael insists they have to ask before making assumptions about Al's willingness.
79|||Rafael indicates Al to the others and approaches him tentatively.
83|||Al's curt first question shows he has no existing relationship with Rafael.
87|I have an offer for you. We could use someone with your strength.|someone with your strength.|Rafael mentions the skill that prompted the invitation and still sounds more polite than Al.
91|||Al first wonders privately if it is a job, then says Rafael seems to recognize what he is worth.
95|(He's certainly sure of himself, isn't he?)|isn't he?|Claudio privately reacts with dry disbelief at Al's confidence.
98|Y-yes. You look like you could handle yourself. Right, Clau?|Right, Clau?|Rafael starts awkwardly, refers to Al's build without overpraising him, and asks Claudio to agree.
103|||Claudio asks whether Al has any sailing experience to go with his strength.
107|||Al names his profession and makes clear that his fighting ability has always supported him.
110|||Rafael asks what a mercenary does when there is no fighting.
114|||Al explains that bodyguard work is plentiful in unsettled times.
117|What about right now?||Rafael asks about Al's current situation before Al points out they saw him fired.
122|||Al says he lost the guard job, refuses to become a sailor, and closes the conversation if they have nothing else to offer.
125|||Claudio takes the refusal at face value and ends the exchange politely.
130|||Rafael calls after Claudio and breaks off his apology to Al as they leave.
140|||Claudio's brief reaction confirms his earlier prediction in this variant.
144|Wait! What did you see coming? I don't understand at all!|What did you see coming?|Rafael asks what was obvious to Claudio and admits he missed it.
148|||Claudio explains why his friend's deferential approach made Al more arrogant.
153|||Julio makes the alternate prediction explicit in his own response.
157|||Claudio starts explaining what he and Julio understand about Al.
161|||Rafael expresses frustration that both companions understand something he does not.
166|||Julio addresses Rafael as admiral and gives the same advice as Claudio in a distinct voice.
173|||Rafael hesitates, then asks his companion what to do.
177|||Claudio realizes Rafael is still set on recruiting Al.
180|||Rafael gives both practical reasons he wants Al on their side.
185|||Claudio affectionately calls him simple and volunteers to speak for them.
188|||Al sounds impatient when they return to try again.
192|If you stay here, when will you get to use that strength you're so proud of? Walking around town doesn't take much muscle.|Walking around town|Claudio points out what Al stands to miss if he stays, using a concrete example.
195|||Al gives a quick, indignant challenge as Claudio pushes back.
199|||Claudio offers both a chance to demonstrate his skill and opponents strong enough to make it worthwhile.
203|...||Al takes a beat to consider the offer. The pause can use the surrounding dialogue's ellipsis.
207|||Claudio leaves Al a way to refuse while provoking his pride about fighting at sea.
210|||Al sees through Claudio's tactic, confirms they need his strength, and accepts on his own terms.
214|||Claudio treats the agreement as settled before asking Al to introduce himself.
217|||Al gives the short name first, then the approved full spoken name.
""",
    168: """
5|||Angelo calls out to Rafael under the mistaken impression he is a boy.
9|||Rafael asks who Angelo is addressing without immediately taking offense.
14|Yeah, you. You're on the crew, right? A powder monkey or something? I was wondering if you needed a navigator.|powder monkey|Angelo talks down to Rafael and reveals why he approached the ship.
18|I'd like to see the captain. Though I doubt a word from a deckhand like you would get me very far! Ha ha!|a deckhand like you|He dismisses Rafael's ability to introduce him. Deckhand is his assumption about Rafael's low position.
22|||Angelo brushes off the introduction when he decides Rafael cannot help him.
26|||Claudio insults Angelo as part of the quarrel. The taunt establishes the word Angelo repeats, with no claim about Angelo's identity.
30|||Angelo throws the taunt back at Claudio and uses the earrings as his rejoinder.
33|||Claudio explains the earrings as the warrior's sign he says they are, then challenges Angelo.
37|||Angelo needles Claudio about using his muscles before his head.
41|||Claudio is furious. Let the threat cut off before Rafael intervenes.
45|||Rafael brings the argument to a halt with Claudio's nickname.
50|I'm no kid. I'm FI FA, and I'm the admiral of this ship.|FI FA;admiral of this ship.|Rafael corrects the mistaken rank and introduces himself with both substitutions.
55|||Angelo's Italian exclamation conveys his shock at Rafael's rank.
59|Oh. I was out of line. I'm sorry. Can you forgive me?|I'm sorry.|Angelo drops the taunting voice as soon as he realizes his mistake.
62|Huh? Oh, no. I should apologize too. My friend was out of line...|My friend was out of line...|Rafael apologizes for his companion's words rather than speaking for him.
67|||Claudio says directly that Rafael has no reason to apologize.
70|||Rafael's interrupted objection leaves room for Angelo to take responsibility.
75|No, he's right. When I see someone dull... I mean, someone hard at work, I can't help teasing them. I'm sorry.|someone hard at work|Angelo catches himself making the same mistake again and apologizes.
78|||Claudio finds Angelo odd and asks why he made the remark if he was going to apologize.
82|||Angelo acknowledges his conduct and starts to leave.
85|||Claudio calls after him as abruptly as he challenged him a moment earlier.
89|||Angelo's wordless reaction leaves Claudio to explain why he stopped him.
93|You said you wanted to be a navigator, right?|navigator, right?|Claudio returns to Angelo's reason for approaching the ship.
96|||Angelo confirms his interest but is still unsure what Claudio wants.
100|||Claudio warms to the idea and invites Rafael to agree, using the runtime name.
103|||Rafael makes the invitation based on his enthusiasm for company aboard.
107|||Angelo stammers because he does not expect them to accept him after his conduct.
110|||Claudio confirms the invitation and gives his approved full name.
114|||Angelo thinks they are odd too and offers his approved full name in return.
117|So, Angelo. If you want to navigate for us, I take it you're good at it?|you're good at it?|Rafael checks Angelo's confidence in his skills after inviting him to join.
122|||Claudio treats Angelo's willingness to argue with him as proof of his nerve.
126|||Angelo shrugs off the praise without taking it as a serious assessment of his sailing.
130|||Rafael welcomes Angelo personally and uses his given name.
134|Thanks, Admiral! I look forward to sailing with you!|sailing with you!|Angelo returns the welcome and acknowledges Rafael's rank.
154|By the way, Admiral, if you want to make real money trading, you can't keep making little deals around the Mediterranean.|real money trading|Angelo shifts into advice about profit and the limitations of trading locally.
158|||Rafael asks why he should move beyond routes he already knows.
171|Well now! You do know a thing or two!|a thing or two!|Julio recognizes Angelo's knowledge before he explains the details.
174|||Rafael's wordless confusion lets Angelo explain what makes Julio agree.
182|The trade routes here are well established, so they look promising. But the big powers have already built up the region. There's little left in it for us.|well established|Angelo explains why promising routes offer few opportunities to newcomers.
186|||Rafael connects the advice to the game's high contract fees and investment costs.
190|||Angelo names Africa and the New World and explains why a small investment can pay better there.
193|||The advice keeps both the novelty of the goods and the expected profit from bringing them to Europe on a round trip.
196|||Rafael realizes Angelo understands trade as well as navigation.
200|||Angelo plays down his knowledge by crediting other sailors.
211|No, he's quite right.||Julio endorses the advice directly.
214|||Julio explains how market share limits sale quantities even after buying a ship and adding cargo holds.
220|||Rafael draws the comparison with earlier Portuguese voyages and chooses Africa as the first destination.
""",
    169: """
7|||The barkeep gives the first ordinary work instruction and calls Ian by name.
11|||Ian acknowledges the work matter-of-factly. The comment about his appearance comes from another table.
16|||The admirer identifies Ian and speaks openly about his beauty.
20|||Her companion questions whether Ian is a man. Keep the rudeness in his speech.
24|||She tells him to lower his voice because Ian might hear.
28|||Ian's private frustration makes clear that he has heard comments like these repeatedly.
31|||The barkeep gives Ian another work instruction while the patrons are watching.
35|||Ian's delayed assent carries his growing discomfort through the routine.
39|||The admirer is thrilled that Ian delivered her drink himself.
42|What are you so happy about? Tch. This is getting old.|This is getting old.|Her companion is annoyed by the attention she is giving Ian.
45|||The barkeep calls Ian again and gives him a destination for the delivery.
48|||Ian acknowledges the instruction without commenting on the patrons.
52|||The patron addresses Ian as a lady to provoke him and orders him to pour a drink.
55|...||Ian leaves the first provocation unanswered. Keep his silence in the surrounding dialogue font.
59|||The patron continues pressing Ian about his looks despite his silence.
62|...||Ian's second silence establishes that he is trying not to react. Keep the pause in the surrounding dialogue font.
66|||The patron questions Ian's gender and comments on his fair skin with a leering laugh.
70|||Ian gives an immediate, unambiguous order that the patron stop touching him.
74|||The cry of pain shows Ian has resisted the unwanted contact.
78|||The patron starts to curse Ian after being hurt. The stammer preserves his surprise.
82|||Ian realizes he may be in trouble for confronting the patron.
86|||The patron invokes his status as a customer to excuse his anger.
90|...I apologize.||Ian forces himself to speak formally in the patron's presence.
94|||Rafael politely asks for a drink, calling the barkeep away from the confrontation without claiming kinship.
99|||The barkeep acknowledges the order and asks Ian for a private word.
102|||The barkeep prepares Ian for dismissal by saying the job does not suit him.
106|||Ian addresses the barkeep respectfully. The Japanese familiar form does not establish a family relationship.
110|||The barkeep says he is tired of trouble and raises handling patrons without drawing a sword.
114|||The barkeep fires Ian directly, in a more regretful tone than Al's employer.
118|||Ian accepts the decision with a pause and without bargaining.
122|With a face that striking and skin that fair, he stands out around here. I wonder why he's working here.|stands out around here.|Rafael reacts to Ian's appearance and wonders about his circumstances.
135|||Julio answers with a broad observation about where life leads people, without drawing a conclusion about Ian.
142|||Claudio sees a mismatch between tavern work and Ian's reserved manner.
145|||Rafael asks whether they should approach him.
151|||Ian's private reaction establishes that he has no money and is unsure what he will do after losing his job.
154|||The ship offshore reminds Ian of where he wants to return. He does not identify the ship as his own.
158|||The same patron repeats the unwanted form of address to establish his role in the earlier incident.
161|!||Ian's short surprise remains wordless and uses the surrounding dialogue font.
165|||The patron notes Ian is alone, then calls his men over.
169|...||Ian assesses the danger during the pause. Use consistent punctuation without adding words.
173|||The patron explicitly wants revenge for being humiliated earlier.
176|||Ian realizes he cannot fight everyone and identifies the apparent leader as his best chance.
181|||The leader berates his men for taking so long against a single opponent.
184|||The attacker's sexual harassment remains part of the threat. Ian gives no sign of welcoming it.
188|Hah, hah... (I can't get anywhere near him on my own!)|on my own!|Ian runs out of breath and privately realizes he cannot reach the leader alone.
191|||The leader thinks Ian is weakening and urges his men to finish the fight.
194|||The patron stammers when he realizes someone else has arrived.
198|||Rafael explains why he stepped in and asks if Ian is willing to accept his help.
202|Damn it. I only fight when I can win. You haven't heard the last of me!|the last of me!|The patron retreats when the situation turns and promises retaliation in his own words.
207|||Rafael comments on Ian's beauty once he is close enough to see him clearly.
212|...||Ian's silence follows another comment on his looks, using the ordinary ellipsis.
216|You just noticed? You're a little slow, aren't you?|aren't you?|Claudio teases Rafael for only now noticing what others already saw.
227|||Julio tentatively speculates about Ian's origins from his complexion. The story has not confirmed the guess.
234|...What does it matter how I look?||Ian mutters his frustration with being judged by appearance.
237|||Claudio notices Ian's tension and tries to ease it.
241|No, I was talking to myself. Sorry. Thank you. You saved my life.|You saved my life.|Ian clarifies that his remark was private, then thanks his rescuers directly.
245|||Rafael is relieved they were in time and hesitates before asking a favor.
250|||Ian offers to help within his abilities in a courteous register.
254|||Rafael invites Ian to sail with them and names the world voyage.
258|||Ian is surprised by the offer and waits to hear why Rafael made it.
262|||Rafael bases the invitation on Ian's skill in the fight.
266|||Rafael identifies his rank and that he leads a fleet in a modest way.
270|...||Ian's silence leads Rafael to wonder whether the invitation was too sudden. Keep that pause in the surrounding dialogue font.
274|||Rafael worries that his abrupt invitation was strange and keeps the uncertain tag.
279|||Ian welcomes the offer before explaining that he is a navigator out of work.
283|||Claudio jokes about women falling for Ian. The remark is his speculation, not an account of Ian's past.
286|||Rafael rebukes Claudio for his rudeness rather than agreeing with the joke.
291|||Ian brushes off Claudio's comment, then formally asks to sail with the fleet and gives his approved name.
""",
}


def main():
    packet = BASE.load(PACKET)
    assert packet["candidate_sha256"] == BASE.digest(previous.parent.ROM)
    names = {
        r["actor_ID"]: r["progressive_nameplate"]
        for r in BASE.load(CATALOGUE)["source_and_current_default_name_fields"]
    }
    token, logical = previous.parent.stage.review.TOKEN, previous.parent.stage.review.logical
    records = []
    for block, decisions in DECISIONS.items():
        group, = [g for g in packet["groups"] if g["block"] == block]
        glosses = {
            r["source_record_index"]: r for r in BASE.load(SOURCE_REVIEWS[block])["records"] if r["block"] == block
        }
        entries = [line.split("|", 3) for line in decisions.strip().splitlines()]
        assert [int(e[0]) for e in entries] == [r["source_record_index"] for r in group["records"]]
        for row, (index, replacement, protected, note) in zip(group["records"], entries, strict=True):
            gloss = glosses.pop(int(index))
            assert gloss["source_Japanese"] == row["Japanese"]
            assert gloss["source_hex"] == f"{row['selector']:02x}" + row["source_body_hex"]
            current = logical(row["current_English"])
            english = replacement or current
            phrases = protected.split(";") if protected else []
            assert token.findall(english) == token.findall(row["Japanese"])
            assert english and note and all(phrase.casefold() in english.casefold() for phrase in phrases)
            records.append({
                "id": gloss["id"],
                "block": block,
                "file_path": group["file_path"],
                "source_record_index": int(index),
                "source_reference": previous.source_reference(row, group, "source"),
                "current_reference": previous.source_reference(row, group, "current"),
                "source_selector": row["selector"],
                "speaker": names[row["selector"]],
                "Japanese": row["Japanese"],
                "source_meaning": gloss["source_meaning"],
                "context": CONTEXTS[block],
                "previous_English": current,
                "english": english,
                "protected_phrases": phrases,
                "localization_note": note,
                "decision": "revision" if english != current else "retention",
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
            })
        assert not glosses
    assert len(records) == 165
    assert not OUTPUT.exists()
    BASE.save(OUTPUT, {
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "candidate_sha256": packet["candidate_sha256"], "paired_source": str(PACKET),
        "paired_source_sha256": BASE.digest(PACKET),
        "status": "Contextual review complete. Native formatting, gameplay and registration pending.",
        "prior_source_glosses": {str(p): BASE.digest(p) for p in set(SOURCE_REVIEWS.values())},
        "records": records,
    })
    print(f"Reviewed {len(records)} dialogue records. {dict(Counter(r['decision'] for r in records))}")


if __name__ == "__main__":
    main()
