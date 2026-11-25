"""Record the contextual pass on Yifa, Sanghyeon, the crown, and Aziza."""

from collections import Counter

from scripts import pair_rafael_B181_B200_20261121 as paired
from scripts import review_rafael_B170_B176_20261121 as prior


base, TOKEN = prior.base, prior.TOKEN
OUTPUT = paired.ROOT / "contextual_decisions_B181_B187_v3.json"
BLOCKS = tuple(range(181, 188))
WRAPS = {
    "DK4_MES_B186_R0079": (["right in front of Julian.", "give it to her myself!"],
        "Keep Claudio's accusation together and give the quoted boast its own final line."),
    "DK4_MES_B186_R0111": (["Her charm", "different from yours, Mihwa."],
        "Keep Julian's comparison intact across two rows. The contrast in charm is what Mihwa pounces on."),
}

DECISIONS = {
    181: """
5|||Claudio tells Rafael someone seems to have been watching. Keep the personal substitution and the uncertainty.
9|||Rafael asks if Claudio really thinks so, giving him room to explain his feeling.
14|I've got a bad feeling about this. Let's get back to the ship early today.|bad feeling about this.|Claudio shifts from suspicion to a practical suggestion to leave early.
19|||Yifa seizes on the word ship and asks whether they are sailors. Her familiar address creates no family tie.
23|||Claudio's exclamation conveys how suddenly Yifa has appeared near them.
27|||Rafael stammers at the surprise and manages to answer her question before asking why.
32|||Yifa calls it her good luck, tries to talk her way aboard, and says she's in a bind without explaining it yet.
35|...Well, this is sudden.||Rafael is taken aback at the unexpected request before Yifa gives the reason.
40|I ran away from my teacher. If I get caught, I'm in big trouble. Come on, let's go!|If I get caught,|Yifa gives the reason for her hurry, then tries to act as if the sailors have already agreed.
43|||Claudio rejects the assumption and asks why it is their problem.
46|||Rafael declines gently and names the concern that she is treating sailing as a diversion.
50|Just for fun?! Oh, come on! You're looking down on me because I'm a kid!|because I'm a kid!|Yifa takes his concern as a dismissal of her ability based on how young she looks.
54|I'm serious! I really do want to be a sailor!|want to be a sailor!|Keep the emphatic repetition and her specific goal in two short outbursts.
58|||Rafael gives her a chance to explain the reason she wants to go to sea.
63|||Yifa's direct, eager answer states her ambition to see the world.
67|||Keep travel, training and growing stronger together with her spirited intention to prove herself to her teacher.
71|||Claudio catches the reference to getting stronger and asks what she's training in.
74|||The brief boast preserves the established name for her tradition, Taoist arts.
78|||Claudio echoes the term in surprise. The punctuation keeps his comic disbelief.
82|I believe you mean it. Remember what I said? This voyage is serious for us, too.|This voyage is serious|Rafael acknowledges her resolve and repeats that the crew takes the voyage seriously.
87|Life aboard is tougher than you think. If you get sick of it, you can't just get off halfway through.|halfway through.|Rafael explains the difficulty of the work and the practical limit of being at sea. He is trying to make her consider the commitment.
92|||Yifa confidently cites her training and says she can do any job aboard.
96|||Rafael tries to object before Yifa interrupts with a challenge.
101|||Yifa identifies Rafael's doubt, points out Claudio, and sets the condition that she should come along if she beats him.
105|||Claudio is skeptical of the proposed match and gives her a chance to back out.
108|||Yifa gives an energetic warning to start the demonstration.
111|||Claudio reluctantly agrees and warns her about getting hurt.
114|||The shout is a pause and sound effect before the anticlimax and surprise.
118|||Retain Claudio's wordless confusion immediately after the shout.
122|||Rafael privately asks whether she actually did anything.
127|||Yifa springs the surprise with a quick shout timed to the opening.
132|||Claudio's shout turns into a baffled question rather than conceding a defeat.
136|||Yifa claims that what just happened was her paralysis technique. The exchange leaves its effectiveness in dispute.
139|||Rafael reacts with a stammered exclamation, which Claudio immediately pushes back on.
144|||Claudio says she caught him off guard and refuses to credit it as a technique.
147|Still, getting that close to Clau is pretty impressive.|getting that close to Clau|Rafael praises Yifa's ability to approach Claudio, without confirming her claimed technique.
152|||Claudio is irritated that Rafael is impressed and cuts off the discussion by telling him to leave.
155|||Yifa calls after them and asks whether they will take her after all.
158|||Rafael hesitates before Claudio interrupts to move him along.
163|||Claudio insists they leave and addresses Rafael with the original given-name substitution.
166|All right, all right. Quit pulling my arm. You really do have a temper...|Quit pulling my arm.|Rafael gives in, complains about being pulled and gets in a final remark about Claudio's temper.
""",
    182: """
5|What a mess. I knew that bad feeling meant trouble.|bad feeling meant trouble.|Claudio ties the earlier unease to having been embarrassed by Yifa.
9|||Yifa's giggle and quick admission make her reappearance playful.
13|||Claudio stammers as he realizes she has caught up with them again.
17|Ahem! That's another one of the Taoist arts!|the Taoist arts!|Yifa offers the same claim for following them unnoticed and takes obvious pride in it.
21|||Rafael marvels that he never noticed her, giving Claudio a reason to defend himself.
25|||Claudio blames the crowd and says failing to notice her is unsurprising.
28|||Yifa treats his explanation as another excuse about the earlier encounter.
32|||The short, sharp reply shows that the teasing has struck a nerve.
44|||Julio openly teases Claudio for being bested by a young girl and laughs at his embarrassment.
47|||Claudio snaps back at Julio. The familiar insult points to age rather than supplying a family relationship.
54|||Yifa turns back to the real purpose of catching up and asks whether Rafael considered her request.
58|||Rafael quietly asks if she truly intends to go to sea, shifting from objection to listening.
63|||Yifa's immediate confidence confirms that she has made up her mind.
75|||Julio takes her resolve at face value and says so plainly.
82|...I remember wanting people to see I could hold my own, too.|hold my own, too.|Rafael sees his earlier desire to be recognized as capable in Yifa's determination.
87|||Rafael makes the invitation himself, then realizes that he never asked her name.
91|||Yifa answers with her given name and an exclamation, closing the recruitment on her enthusiasm.
""",
    183: """
10|||An unidentified respectful address breaks into Rafael's quiet moment.
14|...||Keep Rafael's silence while the voice comes nearer. Use the surrounding ASCII ellipsis.
19|||The respectful address becomes specific when the voice says the substituted given name.
23|||Rafael responds drowsily before understanding who is there.
28|||Sanghyeon apologizes for appearing without warning and reassures Rafael that he means no harm.
31|||His formal introduction gives the shared teacher and his seniority in training. Preserve the established name and the distinction between their roles.
35|I heard you'd taken Yifa aboard. I came to pay my respects and have a word with you, if I may.|taken Yifa aboard.;if I may.|Sanghyeon states what brought him and politely asks to speak. The known arrangement is that Rafael took Yifa aboard.
39|||Rafael leaves his question incomplete as he works out the visitor's relationship to Yifa.
44|I am ashamed to say it, but I failed to guide Yifa properly. That's why she grew up so unruly.|failed to guide Yifa properly.|Sanghyeon places the blame for her lack of restraint on his own shortcomings as a senior student.
47|||He lists leaving the mountain without permission and leaving the country, both within her effort to escape training.
51|||He says Yifa probably does not know the rule and describes it as applying to the people of their country.
55|||Rafael asks whether the visit is intended to take Yifa home.
59|Even if I wanted to, I couldn't. She broke the law. It's a grave offense. Our school expelled her.|It's a grave offense.;Our school expelled her.|Sanghyeon says he cannot take her back. He explains the seriousness of breaking the law and the school's expulsion in complete thoughts.
62|||The formal tie has ended. This leaves his personal concern, explained in the next line, intact.
65|||Keep the source's comparison to a brother and sister raised together. This is their closeness and shared upbringing.
68|She still has so much to learn. I worry she'll make a scene in front of other people.|She still has so much to learn.|Sanghyeon's worry is about her conduct before others, following his description of her lack of experience.
72|||He recognizes that he is asking a great deal and asks Rafael to guide her conduct.
75|||He makes the continued training and obedience to their teacher a further request rather than assuming Rafael has accepted it.
78|||His polite plea to take good care of her closes the visit.
81|Was that a dream? It felt so real...|It felt so real...|Rafael doubts what he just experienced because of how vivid it seemed.
85|||Yifa bursts in with a greeting and starts to call for departure before she senses someone.
88|||The standalone exclamation preserves the interruption and leaves cause to the following panel.
92|||Rafael asks what brought her to a sudden stop.
97|I can feel him! The senior student I trained with!|senior student|Yifa senses the presence of the person she trained with. She leaves Rafael to supply his name in the next reply.
101|||Rafael recognizes her description and asks whether she means Sanghyeon.
105|||Yifa is surprised he knows and immediately asks where the man is, using a familiar form of address in the source.
109|||Rafael reports the dream, Sanghyeon's explanation of their training relationship, and his name.
113|||Yifa briefly repeats the unexpected explanation before giving her own.
117|||Yifa says Sanghyeon's name to herself. The brief recognition carries her affection.
121|||Yifa explains why he could not leave the mountain and how she believes he came anyway.
125|His arts? Th-that was one of his techniques?|one of his techniques?|Rafael echoes the explanation with surprise and asks whether the visit was an example of that training.
129|||Rafael relays the advice about the teacher's instructions and adds Sanghyeon's concern for her.
134|||Yifa affectionately laughs at Sanghyeon's continuing concern as she recognizes his familiar manner.
138|||Rafael notices her reaction and gives her room to respond.
142|||Yifa promises to train hard out of consideration for Sanghyeon.
146|||Rafael accepts her training while reminding her of the work she owes the crew.
150|||Yifa is sure she can do both. Keep the quick reassurance at the end of the exchange.
""",
    184: """
7|||Julian's extravagance about living for Mihwa's smile establishes his style before the smile fails to appear.
11|||Mihwa's familiar response does not yet reveal why she's distracted.
15|||Rafael privately recognizes Julian's type without imposing a nationality or a relationship.
19|||Julian expects the familiar reaction, so the sudden question about whether she still likes him lands as comic insecurity.
23|||Mihwa reassures him and explains that his talk normally cheers her up, then trails off.
27|There's something I want more than anything. Lately I can't get it out of my head, day or night...|day or night...|Mihwa changes the subject to the object occupying her thoughts. Keep the day-and-night intensity.
31|||Julian says the troubled look doesn't suit Mihwa and asks what she wants so badly.
35|||Mihwa supplies the approved item name and describes its mystery and value as something she heard.
39|Sounds expensive... Can I even afford it? Where do they sell it?|Where do they sell it?|Julian jumps from the price to the practical question of where to buy it.
42|||Mihwa says it's apparently not for sale and that Seoul is only a location she heard about.
45|||Julian repeats the problem, then rushes to a confident inference without stating a location.
48|||Mihwa asks whether he has a lead rather than supplying one.
52|||Julian makes an extravagant offer to find the named crown quickly and bring back her smile.
56|||The compliment turns into a question about a date if he gets the crown. Keep his expectation in the tag.
59|||Mihwa teases him for getting ahead of himself and agrees only to think about it.
63|||Julian calls her response a promise and rushes off to Seoul. The joke depends on his interpretation.
66|||Mihwa starts to encourage him and realizes he has already left.
69|||Rafael hesitates before interrupting the private exchange he overheard.
74|||Mihwa welcomes the newcomers and apologizes for overlooking them.
77|That crown you were talking about... What exactly is the Silla Gold Crown?|Silla Gold Crown?|Rafael follows up on the object he just overheard her name.
81|||Mihwa remembers its reputation for beauty but has forgotten the explanation she heard.
85|||Claudio takes an interest and asks for Rafael's reaction by his substituted given name.
88|A little. We don't even know what it looks like, and Julian's already gone looking for it.|Julian's already gone|Rafael gives the two reasons for hesitating, their lack of details and Julian's head start.
93|I'd be happy to get it from you, too. Don't you think I'm worth a gift?|worth a gift?|Mihwa opens the hunt to Rafael and playfully presses him with a question about giving her a present.
96|||Claudio accepts that invitation much more readily than Rafael, giving Rafael the reason to comment on him.
99|(Clau's so easy to talk into things.) All right, let's look for it. You said Seoul, right?|Clau's so easy;Seoul, right?|Rafael remarks inwardly on Claudio's susceptibility, then agrees to the search and checks the location.
103|||Mihwa repeats that she only heard it was in Seoul and has no precise location.
107|Let's head for Seoul. We can ask the locals once we're there.|ask the locals|Claudio suggests using local information after they reach the city.
111|||Rafael thinks they might happen upon Julian while searching. He makes no prediction about what Julian found.
""",
    185: """
6|||Rafael asks Claudio for a starting point in the search and names the item consistently.
11|||Claudio thinks it over briefly and suggests asking around.
14|||Reika's short greeting welcomes the group before Claudio asks his question.
18|||Claudio asks casually whether Reika has heard of the named crown.
21|||Reika confirms hearing about it and asks why they are interested.
24|We're looking for it. Can you tell us anything about it?|anything about it?|Rafael explains the purpose of their visit and asks whether she can help.
28|Is everybody looking for the Silla Gold Crown these days? Somebody just asked me the same thing.|Silla Gold Crown;the same thing.|Reika jokes about a fashion for looking for it and gives the actual evidence that another person asked just before them.
32|||Claudio recognizes a possible match and asks whether the person was a smooth talker.
35|Well, I couldn't tell if he wanted information or if he was trying to flirt with me.|flirt with me.|Reika describes her impression, keeping both possibilities open.
38|||Rafael offers Julian as a possibility and names Hangzhou as the earlier meeting place.
43|||Reika cannot remember his name and only thinks he went to the Tomb of King Muryeong. Preserve both qualifications.
46|||Claudio repeats the exact named site in surprise, prompting Reika to explain it.
50|||Reika places the historic site nearby and says she has heard the crown is there.
54|||Claudio concludes that Julian may be ahead and urges Rafael to hurry without confirming Reika's guess.
""",
    186: """
12|||On Julian's gift path he greets Rafael by the original substitution and thanks him for Seoul.
15|||Mihwa asks whether they know each other, leaving Julian to explain the connection.
19|||Julian credits the party as the first to find the crown in his gift path.
22|They were so moved by my deep love for you, Mihwa, that they let me have it. Wasn't that kind of them?|Wasn't that kind of them?|Julian flatters Mihwa and casts the gift as proof that the party approved of his devotion.
26|||Mihwa is briefly confused by his explanation before the crown's beauty takes her attention.
30|||Julian formally gives it to Mihwa and says he has fulfilled his promise to find her the gift.
33|||Mihwa is excited and promises that she will treasure it for life.
36|||Rafael takes pleasure in Julian's success without claiming a reward.
41|Thank you. I really do owe it to you. How can I ever repay you?|How can I ever repay you?|Julian thanks Rafael openly and tries to decide how to return the favor.
45|||Rafael stammers as he waves off Julian's offer of repayment.
50|||Julian explicitly values honor and says he cannot ignore a favor he owes. His sincerity follows the earlier showmanship.
57|Mihwa! Are you here?||Rafael calls urgently for Mihwa on his own route to presenting the crown.
62|||Mihwa welcomes him and asks why he is in such a hurry.
65|||Rafael gets as far as showing the gift and leaves Mihwa to recognize it.
70|||Mihwa stumbles over the recognition, identifies the crown and thanks Rafael for finding it for her.
74|||Rafael modestly deflects the thanks, opening the way for Claudio's teasing.
79|||Claudio repeats Rafael's exact declaration about giving Mihwa the crown himself. This makes sense of his shyness now.
82|||Mihwa thanks Rafael enthusiastically, then asks about Julian's absence.
87|||Rafael explains that they met Julian at the moment they found the named object and leaves Claudio to add what happened next.
91|||Claudio says Julian left for an unspecified place, setting up his sudden return.
95|||Julian announces his presence as soon as they wonder where he is.
99|||Mihwa notes that Rafael's group got to the crown first this time.
102|||Julian acknowledges the outcome and immediately redirects attention to his devotion during the trip to Seoul.
108|||Claudio brings up Reika and calls her attractive to put Julian on the spot in front of Mihwa.
111|||Julian agrees without hesitation and compares their distinct charms, inviting Mihwa's reaction.
114|||Mihwa stretches out Julian's name and accuses him of moving quickly with women. Keep the conspicuously drawn-out name.
117|||Julian insists there is no need for jealousy and says he asked Reika only about the crown.
121|||Julian returns to the party's speed and says that reaching Seoul left him exhausted.
125|||Julian asks plainly how they found the exact object so quickly. The title and closing question fit together on the second row.
128|||Claudio takes his ship's speed to Seoul for granted, giving Julian the missing explanation.
131|||Hearing the word ship, Julian suddenly realizes the group might be sailors.
134|||Rafael confirms it in his usual unassuming manner.
139|||Julian explains his tiredness by saying that he ran all the way to Seoul, an admission Claudio finds hard to believe.
142|||Claudio's private reaction lets the absurd comparison between running and sailing stand on its own.
145|||Julian takes the news as fate before explaining what he thinks it means.
149|||Rafael asks what prompted Julian's sudden excitement.
154|Don't you see? Finding the Silla Gold Crown was my chance to set out and see the world!|Silla Gold Crown|Julian interprets the search as the opportunity that finally brought him to traveling.
158|||Claudio stammers in surprise while Julian rushes on.
162|||Julian explicitly asks to go with them so he can see the world too.
165|||Claudio jokes that Julian may only want to charm women in other countries. Keep the question tag intact.
168|||Julian briefly indulges the joke, then explains the real reason he has wanted to sail since childhood. His grandfather is explicitly his relative.
171|What's the world like? What about my grandfather's birthplace? I want to find out. That's why I want to go.|my grandfather's birthplace?;I want to find out.;That's why I want to go.|Julian wants to discover both the wider world and his grandfather's birthplace. The earnest curiosity follows his earlier banter.
174|||Rafael infers that Julian knows something about navigation from his grandfather and asks for confirmation.
179|||Julian confirms that he has navigation knowledge and promises not to hold them back.
182|||Rafael's direct invitation turns the conversation into an acceptance.
187|||Julian then remembers Mihwa and addresses her separately.
191|||Mihwa gives him a simple prompt to finish asking his question.
195|||Julian treats their proposed date as if it were assured, consistent with his earlier reaction.
199|||Mihwa points to his imminent departure as the practical reason the date cannot happen now.
202|||Julian promises to bring back an even lovelier gift and asks again about a date for when he returns.
206|||Mihwa reacts with amused exasperation and says she will be waiting. Keep her answer at that level of commitment.
209|||Claudio ends with dry amusement at the unusual new crewmate the party has gained.
""",
    187: """
6|||Claudio recognizes Aziza and blurts out his fear without naming her aloud first.
10|||Rafael supplies her established full name, with recognition framed as a question.
15|FO, I take it. Fancy meeting you here.|FO, I take it.|Aziza identifies Rafael's company and notes the unlikely meeting. The full company substitution fits before the comma, including the period in the default company name.
19|||Claudio recognizes that the people around them are Aziza's and warns Rafael with the original name token.
23|Heh. The closer I look, the cuter you get, boy.|the cuter you get, boy.|Aziza lingers on Rafael's looks in a teasing, condescending way before offering him a drink.
26|||Aziza proposes a drink to get acquainted. It sounds unhurried even as the other pirates close in.
29|...||Rafael falls silent at the offer. Use the same ellipsis glyph as the neighboring progressive lines.
34|||Snake grasps for the moths-to-a-flame expression and orders the others to surround them.
38|||Rafael privately weighs the danger of him and Claudio facing so many pirates.
43|||Claudio stammers as he asks what the pirates intend.
47|||Angel taunts them for being frightened and recalls the defeat on their earlier encounter.
51|||Aziza interrupts Angel and sends the others back. The quick commands establish her authority before Claudio comments on it later.
55|||Angel's startled apology shows how quickly he obeys her.
59|||Rafael's hesitant punctuation conveys confusion at being spared, before Aziza supplies the reason.
64|||Aziza says they still have a score to settle and treats dying here as a waste of the confrontation she wants.
68|||Claudio is baffled by her approach and asks what to make of her.
72|||Aziza identifies herself as a pirate and states plainly where she means to settle the dispute.
75|I'll give you this much today. You stood your ground, even surrounded like this. How's that?|You stood your ground,|Aziza gives Rafael limited praise for standing his ground in the face of the numbers around him and presses him for a response.
79|||Rafael answers as an admiral and explains why he cannot run away.
83|||Aziza approves of the answer and praises his nerve in the same familiar, condescending address.
87|||She asks his name directly after deciding he has guts.
91|||Rafael gives the original given-name and surname substitutions in their source order, with normal English name spacing.
96|I'll remember that name and face. We'll meet again... next time at sea.|that name and face.;next time at sea.|Aziza gives the encounter a deliberate farewell and repeats the setting for their next meeting. Keep her first thought together.
100|||Aziza notices the sword and starts a separate thought about it.
104|||Rafael's short question gives Aziza room to say what caught her attention.
109|||Aziza admires the sword, says it would suit her better, and playfully threatens to claim it someday. Keep the threat conditional in time.
113|||Rafael stammers as he asks what she means. He has no clearer understanding of her interest yet.
118|||Aziza drops the subject and tells the pirates to leave with her, maintaining command of the scene.
121|||Angel promptly acknowledges the order, contrasting with his earlier challenge.
125|||Claudio marvels that the pirates obey a word from her, supporting his later judgment of her authority.
129|...Whew. We're safe.||Rafael exhales with relief once the pirates have left.
134|||Claudio admits his fear and says he now understands why she leads the pirates.
138|||Rafael shares Claudio's impression and asks whether pride explains her choice to settle the dispute at sea.
143|||Claudio agrees tentatively and gives the practical concern of being chased by someone like her.
147|...||Rafael's standalone pause comes before Claudio decides there's no sense worrying now. Use the same ASCII ellipsis.
152|||Claudio sets the worry aside without claiming the danger has disappeared.
155|||Rafael's quiet assent closes the encounter, leaving their uncertainty intact.
""",
}


def main():
    packet, release = map(base.load, (paired.PAIRED, paired.parent.RELEASE))
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    assert packet["candidate_sha256"] == base.digest(paired.parent.ROM)
    catalogue = base.load(prior.CATALOGUE)["source_and_current_default_name_fields"]
    names = {r["actor_ID"]: r["progressive_nameplate"] for r in catalogue}
    records = []
    groups = [item for item in packet["groups"] if item["block"] in BLOCKS]
    for group in groups:
        block = group["block"]
        rows = [s.split("|", 3) for s in DECISIONS[block].strip().splitlines()]
        for raw, (index, replacement, protected, note) in zip(group["records"], rows, strict=True):
            assert int(index) == int(raw["id"][-4:])
            selector = raw["selector"]
            old = " ".join(raw["current_English"].split())
            text = replacement or old
            phrases = protected.split(";") if protected else []
            assert all(p.casefold() in text.casefold() for p in phrases)
            assert TOKEN.findall(text) == TOKEN.findall(old) == TOKEN.findall(raw["Japanese"])
            decision = "revision" if text != old else "retention"
            kind = "system-FE" if selector == 254 else "progressive"
            change = "glyph" if old == "…" and text == "..." else "wording" if decision == "revision" else "retention"
            retention_reason = None
            if raw["id"] in WRAPS:
                assert decision == "retention"
                retention_reason = note
                phrases, note = WRAPS[raw["id"]]
                assert all(p in text for p in phrases)
                decision, change = "revision", "wrap-only"
            original, installed = [f"{selector:02x}" + raw[side + "_reference"]["exact_body_hex"] for side in ("source", "current")]
            records.append(raw | dict(route=0, source_selector=selector, native_command_word=0x4000, native_slots=[],
                source_hex=original, current_hex=installed, previous_English=old, english=text, kind=kind,
                speaker=names[selector] if kind == "progressive" else "System panel",
                contextual_speaker=raw["earlier_speaker"], context=raw["earlier_context"],
                source_meaning=raw["earlier_source_meaning"], protected_phrases=phrases, localization_note=note,
                finding=note, decision=decision, change_class=change, prose_retention_reason=retention_reason,
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    assert len(records) == 227 and sum(r["source_selector"] == 254 for r in records) == 13
    counts = Counter(r["change_class"] for r in records)
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(paired.PAIRED), source_packet_sha256=base.digest(paired.PAIRED),
        records=records, findings=dict(counts), new_editorial_credit=0,
        status="Contextual review complete. Stored formatting, gameplay and release checks pending."))
    print(f"Reviewed {len(records)} records. {dict(counts)}")


if __name__ == "__main__":
    main()
