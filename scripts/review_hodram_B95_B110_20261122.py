"""Review the lost blade, treasure rumors, and the priest's Proof of Conquest."""

from collections import Counter

from scripts import review_hodram_B91_B93_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B95_B110_contextual_v2.json"
COMBINED = ROOT / "B91_B110_contextual_v2.json"
GLYPHS = set()
CONTEXTS = {
    95: "The coast reminds Gerhard of a fight and the loss of a sword he carried for years. Hodram offers a more comforting possibility about who found it.",
    97: "Samwell asks what a nukenin is, then describes a rumored set of armor. Yukihisa takes an offhand remark as an insult before Hodram interrupts and both apologize.",
    100: "Charles's enthusiasm for amber puzzles the port worker. They find common ground when amber reminds him of a rumor about an island off the cape.",
    101: "Julio worries about his granddaughter Cristina. Hodram compares her to Athena, reminding Julio of the Minerva Shield and giving him a new reason to seek it.",
    102: "A crewmate turns a question about peacocks into a rumor about the Peacock Mail. Hodram is skeptical but says he will keep the distant location in mind.",
    103: "The same crewmate brings one last rumored treasure, then admits that tracking down clues has become tedious. He can only place the vest in the west of the New World.",
    104: "Janus tells Hodram about a Portuguese fleet in distress about twenty years earlier. He questions the telescope's alleged origin and guesses where it may have washed ashore.",
    105: "Emilio wants a meal as soon as they reach port. His quest for the world's best food leads to the rumor about Hestia's Pot before his appetite takes over again.",
    108: "Yukihisa asks to see the recovered Muramasa. Hodram credits his report, and the blade's unsettling glow leaves Yukihisa impressed.",
    109: "A girl has heard about the crew's search and points them toward the priest who might know something useful.",
    110: "A priest asks whether the crew seeks the Proof of Conquest, tests their resolve, explains the two Map Keys and offers a sword with a moral charge and blessing.",
}

DECISIONS = {
    95: """
5|||Gerhard recognizes the place and his thought trails off. The short opening gives Hodram a reason to ask.
8|||Hodram asks directly what affected Gerhard and uses his approved given name.
12|It just brought back an old memory...|an old memory...|Gerhard brushes off the concern and says the place stirred a memory. The hesitation leaves Hodram to ask again.
15|||Hodram's small prompt leaves the floor with Gerhard.
19|||Gerhard lost his own sword during an earlier fight with pirates near here. The current line keeps the location and cause.
22|||Hodram echoes the mention of a sword. His terse question lets Gerhard describe it.
26|Just an old Katzbalger, but it handled far better than it looked. I carried it for years and grew quite fond of it.|an old Katzbalger,;far better than it looked.;grew quite fond of it.|Gerhard names the blade, recalls its unexpectedly good handling, and says he carried and treasured it for years.
29|That's a shame. You never found it?|That's a shame.;You never found it?|Hodram sympathizes with the loss and asks whether Gerhard ever recovered it.
32|I looked everywhere... One of the local fishers probably found it and sold it for next to nothing.|local fishers;next to nothing.|Gerhard could not find the blade and guesses that a local fishing worker might have sold it cheaply. The line remains speculation.
35|Maybe someone who knows a good sword found it and is taking care of it.|knows a good sword;taking care of it.|Hodram suggests someone who appreciates the sword might be looking after it, offering comfort rather than news.
38|You rarely come across a blade like that. It would ease my mind to know it's with someone who appreciates it.|a blade like that.;ease my mind;someone who appreciates it.|Gerhard says such a sword is rare and would feel some relief if it were being used by someone who knew its worth.
""",
    97: """
5|||Samwell addresses the admiral and asks about the unfamiliar term nukenin. The current spelling leaves Yukihisa to explain it.
9|||Hodram repeats the term as a question. The short echo fits his unfamiliarity.
13|Someone who used to be a ninja.|used to be a ninja.|Yukihisa says a nukenin is someone who was formerly a ninja. The plain definition fits the follow-up joke.
17|||Samwell first acts as if he understands and then asks what a ninja is. The pause is part of the joke.
20|They're from a clan in Japan that specializes in working unseen.|a clan in Japan;working unseen.|Yukihisa explains that they're a group in Japan skilled in covert activity. He does not reduce them to spies himself.
23|||Samwell paraphrases the explanation as Japanese spies and asks if Yukihisa has met one. Keep this as Samwell's interpretation.
27|||Yukihisa says he has never met one and cites their rule for a ninja whose identity is exposed. Keep it as his account of the code.
31|||Samwell reacts with his Italian exclamation. The expression fits his voice and the surprise of the preceding answer.
35|Leaving a ninja clan can cost you your life. A nukenin who escapes pursuit must be extraordinarily skilled.|can cost you your life.;escapes pursuit;extraordinarily skilled.|Yukihisa describes the mortal risk of leaving and reasons that escape from the clan requires unusual skill.
38|||Yukihisa asks why Samwell brought up a nukenin. His direct question moves the exchange from people to the item.
42|Well, I heard something about their outfit.|about their outfit.|Samwell narrows the rumor to the clothes associated with this kind of ninja.
46|It's a renegade ninja's all-black outfit. They call it Ninja Garb. It's supposed to be armor.|all-black outfit.;They call it Ninja Garb.;supposed to be armor.|Samwell gives the key appearance and the established name. He treats its use as armor as a claim he heard.
50|||Yukihisa is surprised by the armor claim. The one word invites the details.
54|||Samwell says he does not know the details but has heard it is very light and tough. Keep both properties qualified.
57|That's the first I've heard of such a thing.|the first I've heard;such a thing.|Yukihisa is surprised by the object and says he has never heard of it. The more complete reply fits his register.
60|||Hodram notes that even Yukihisa, who is from Japan, has not heard of it. His reflection does not establish anything further about the rumor.
63|||Yukihisa formally apologizes for not knowing. Samwell's next response shows why that is unnecessary.
67|||Samwell tells him he has nothing to apologize for. The current line keeps the immediate reassurance.
70|||Yukihisa wants to object and trails off. Keep the brief hesitation.
74|I'm the one who brought it up. You're a funny one, Yukihisa.|the one who brought it up.;a funny one, Yukihisa.|Samwell points out that he brought it up himself and calls Yukihisa funny. The ambiguous word sets up Yukihisa's objection.
77|||Yukihisa repeats the word funny and challenges the perceived insult. His formal threat is in his own voice.
81|||Samwell pushes back and asks what Yukihisa will do. The direct question keeps his provocation.
85|Both of you, stop. This isn't worth fighting over.|Both of you, stop.;worth fighting over.|Hodram intervenes with both crewmates. He says the dispute is too trivial for a fight.
89|||Yukihisa apologizes after Hodram intervenes. His formality contrasts with Samwell's reply.
93|||Samwell apologizes and takes responsibility. The short answers let the conflict end without a lecture.
96|||Yukihisa returns to the black armor and says that, if it exists, it will be in Japan. The qualification stays in place.
99|||Hodram agrees that Japan is the most likely place, without treating the rumor as confirmed.
103|That's what I think, too. Let's look when we have some time.|That's what I think, too.;when we have some time.|Samwell agrees and suggests searching when they have time. It stays an optional investigation.
""",
    100: """
5|||The port worker recognizes amber as something they're trading. The existing plain question suits him.
9|We do. When I look at amber's glow, I feel drawn into the distant past...|amber's glow,;the distant past...|Charles confirms the trade and describes how the glow invites his imagination into the distant past.
13|Huh? What are you talking about?|What are you talking about?|The port worker is puzzled by Charles's sudden change in register.
17|||Charles explains that amber is ancient tree resin hardened and transformed into something used as a gemstone. The existing language keeps his enthusiasm.
21|See the bee in this amber? It's slept for thousands of years in a little sepia world. How mysterious...|this amber?;for thousands of years;little sepia world.|Charles points out the bee and poetically describes its thousands of years in a tiny world. The image and estimate belong to his explanation.
24|||The port worker asks how he knows such complicated things. The English avoids a literal familiarity that would imply a relationship.
27|Science. It uses human reason to shed a little light on the wonders of the world, even the ones we can't yet explain.|human reason;the wonders of the world,;can't yet explain.|Charles describes science as human inquiry into wonders beyond present understanding. The explanation remains earnest enough to puzzle his listener.
30|That went right over my head. Oh, speaking of amber...|went right over my head.;speaking of amber...|The port worker is lost but remembers a rumor once their conversation returns to amber.
34|||Charles asks what amber made him remember. The short prompt fits.
38|||The port worker gives the location as one of several islands off the cape and calls the amber-like glow hearsay. Keep the limited directions.
41|It glows like amber? Maybe it's a mineral vein...|glows like amber?;a mineral vein...|Charles echoes the color and guesses it could be a mineral vein. Keep it as speculation.
45|||The port worker says he doesn't know the cause and has only heard a rumor. The short reply fits his manner.
49|I see. Thanks for telling me. You've piqued my scientific curiosity.|Thanks for telling me.;my scientific curiosity.|Charles thanks him for going to the trouble and says the rumor has caught his scientific interest.
""",
    101: """
5|||Julio sighs before Hodram asks what's wrong. The existing cue keeps the opening wordless.
9|||Hodram respectfully asks what's troubling Julio. The address carries respect without claiming kinship.
13|||Julio says he is worried about his granddaughter. Their family relationship is explicit.
17|||Hodram names Cristina as the person he means and leaves room for him to answer.
21|||Julio says he wonders how she's doing and jokingly corrects doting parent to grandfather. The original correction is the joke.
24|||Hodram calls Cristina more capable than most men and compares her to Athena. Keep the strong compliment in his own voice.
27|||Julio asks who Athena is. The name is enough to show what he didn't follow.
31|||Hodram gives the Roman equivalent Minerva. The quick comparison leads to Julio's recollection.
34|||Julio thinks he may have heard that long ago but is uncertain about stories of the gods. Keep the qualification.
37|||Julio fumbles the name Minerva but thinks it sounds familiar. The existing incomplete name sounds like his attempt to recall it.
40|Anyway, you don't have to worry about Cristina.|worry about Cristina.|Hodram returns the discussion to reassuring Julio about Cristina.
43|I'm grateful you trust her, Admiral. To me, she's still my granddaughter. Try to see it from an old man's side.|you trust her, Admiral.;still my granddaughter.;an old man's side.|Julio appreciates that Hodram trusts Cristina but asks him to understand a grandfather's concern.
46|||Hodram leaves Julio a quiet beat after the personal appeal.
50|||Julio suddenly remembers what the name meant to him. The existing exclamation changes the mood.
53|||Hodram's wordless question gives Julio room to identify the object.
57|||Julio thinks the name was the Minerva Shield. Preserve the established item title and the uncertain recollection.
60|A legendary piece of armor, said to lie somewhere around the Mediterranean. Or was it the Black Sea? I never looked for it in earnest, but...|piece of armor,;the Mediterranean.;the Black Sea?;in earnest, but...|Julio remembers two possible regions and that he did not search seriously before. The account is hearsay and his location uncertain.
63|You say Cristina's like Minerva? Now I really want to find that shield. If it's real, I'd like her to have it...|Cristina's like Minerva?;find that shield.;I'd like her to have it...|Julio explains why the comparison renews his interest. He wants Cristina to have the shield if it exists.
66|||Hodram respectfully starts to respond and leaves the thought unspoken. Keep his brief reaction.
70|Sorry for rambling. Forget the old man's nonsense. I'd better get back to work.|Sorry for rambling.;get back to work.|Julio dismisses his own musings and decides it is time to work again. His self-deprecation fits the exchange.
74|||Julio reminds the admiral to return to work too. The short afterthought fits him.
78|||Hodram quietly agrees. The trailing response closes on Julio's shift back to work.
""",
    102: """
5|||The crewmate asks the admiral for a moment before bringing up the rumor. The next exchange intentionally starts the same way.
9|||Hodram's short response allows the crewmate to continue.
13|||The crewmate admires peacocks and asks whether Hodram would want to see one. Keep the broad curiosity before the item is named.
16|||Hodram guesses immediately that this is another rumor. His brief question anticipates the reveal.
20|||The crewmate admits it and names the Peacock Mail. Keep the approved title.
23|||Hodram predicts the mail will be made out of peacock feathers. His assumption is what the next line corrects.
26|Close! So close! It's mail with peacock tail feathers on the back.|mail with peacock tail feathers;on the back.|The crewmate celebrates how close the guess was and explains the feathers are attached at the back.
30|||Hodram doubts the mail looks very strong. His skepticism tees up the supposed effect.
34|They say the sight of it can stop the enemy in their tracks. That's supposed to be its biggest advantage.|stop the enemy in their tracks.;biggest advantage.|The crewmate says the spectacle is rumored to make enemies freeze. Keep the effect as hearsay.
38|||Hodram hesitates but asks where it is. The English keeps the reluctant interest.
41|They say it's on a little island far, far, far southeast of the Cape of Good Hope. That's all I could find out.|far, far, far;the Cape of Good Hope.;all I could find out.|The crewmate gives only a small island far southeast of the cape. Preserve the distance emphasis and limited clue.
45|That's hardly enough to find it.|hardly enough to find it.|Hodram judges the clue too broad to locate the object. The short reply fits his skepticism.
48|||The crewmate still wants to see it and guesses it will be unlike anything they've seen. Keep the eagerness and conjecture.
52|||Hodram agrees to keep it in mind and warns the crewmate against expecting results.
55|||The crewmate already understands. The repeated acknowledgment keeps the casual response.
""",
    103: """
5|||The familiar request for a moment repeats the opening of the preceding rumor. Preserve the callback.
9|||Hodram gives the same brief acknowledgment as before.
13|||The crewmate suggests looking for the Jaguar God's Vest. The approved title stays exact and motivates Hodram's surprise.
17|||Hodram reacts with a short question before the crewmate explains the item's name.
21|Just what it sounds like. They say a jaguar god lives in the vest, and it's somewhere in the New World.|a jaguar god;in the vest,;in the New World.|The crewmate says the title refers to a god said to dwell in the vest and gives the New World as its rumored location.
25|||Hodram asks if this is another recently heard rumor. The short question keeps the recurring setup.
28|||The crewmate says yes and that this is the last one. His answer gives Hodram a reason to follow up.
31|||Hodram asks why there won't be more. His brief question leads into the joke about boredom.
35|||The crewmate says researching the locations takes effort and that he's already bored with it. Keep both reasons.
38|I lose interest pretty fast. I like animals, but what fun are they if I can't cook them? If I hear anything by chance, I'll tell you.|lose interest pretty fast.;if I can't cook them?;by chance,|The crewmate says he loses interest quickly, jokes about wanting to cook the animals, and promises to pass on anything he happens to hear.
41|||Hodram allows his explanation and returns to the question of where in the New World the vest might be. The current pivot works.
45|Probably on the west side of the New World.|west side of the New World.|The crewmate guesses the western part of the New World. Keep the geographic scope as wide as he gives it.
48|||Hodram says the area remains wide and asks for a narrower clue. The concise reply preserves his frustration.
51|||The crewmate apologizes that he found out nothing further and asks Hodram to keep it in mind. The existing plain delivery fits.
54|||Hodram laughs and agrees. The short response keeps his resignation affectionate.
""",
    104: """
5|||Janus asks whether Hodram has heard about the Portuguese fleet's disaster near here, roughly twenty years ago. Keep both qualifications.
9|That's the first I've heard of it.|first I've heard of it.|Hodram says the story is new to him. The direct answer gives Janus room to explain.
13|Its admiral supposedly had a telescope that could see incredibly far. Even the moon's bumps and hollows came into focus.|see incredibly far.;bumps and hollows|Janus describes the rumored telescope and says people claimed it revealed the uneven surface of the moon.
16|||Hodram is impressed by the claimed capability. The one-word response fits.
20|||Janus gives the rumored maker as Aristarchus and identifies him as a brilliant Hellenistic astronomer. The claim remains hearsay.
24|||Hodram questions whether it could be true. The brief question sets up Janus's own skepticism.
28|||Janus doubts people could polish lenses that precisely at the time. The wording keeps this as his judgment about the claim.
32|||Janus does not know whether the attribution is true and says the Aristarchus Telescope was named for him. Keep the approved title.
35|||Hodram prompts him to get to the point. The short question fits his familiarity with Janus.
39|||Janus uses the currents to infer that the telescope may have washed up along this coast. Keep the good chance and uncertainty.
42|Hm. Sounds like it's worth looking for.|worth looking for.|Hodram cautiously concludes the possibility merits a search.
""",
    105: """
5|||Emilio announces that they've reached port and asks to eat immediately. The breathless invitation fits his recurring habit.
8|||Hodram points out that Emilio says the same thing every time they reach port. Keep the direct address.
11|||Emilio defends the importance of eating and says he is looking for something. The existing distinction sets up his next reply.
15|||Hodram repeats that Emilio is looking for something. His puzzled echo leaves Emilio room to say what.
19|||Emilio calls it the best food in the world. The short superlative turns the conversation.
23|||Hodram asks who could decide what counts as the best and how to judge it. The existing set of questions reads naturally.
27|||Emilio confidently says his own criterion is food made in Hestia's Pot. Preserve the approved title and personal certainty.
30|||Hodram echoes the item's name as a question, before Emilio expands on it.
34|||Emilio says the goddess of the hearth had it made and places it far across the sea south of Greece, all on hearsay.
37|That's why I can't wait to try the food shops around Greece. Can we go get something to eat now?|food shops around Greece.;something to eat now?|Emilio explains why he is eager to try the shops near Greece and brings the conversation back to eating immediately.
""",
    108: """
5|||Yukihisa has heard the admiral finally found Muramasa and asks respectfully for a glimpse. Keep the existing item name.
8|Of course. Without your report, I'd never have found it.|Without your report,;never have found it.|Hodram agrees and credits Yukihisa's report for making the discovery possible.
12|||Yukihisa repeats that he's looking at Muramasa. The pause and repeated lead-in fit his awe.
16|||Yukihisa describes the blade's eerie light and imagines it drawing him in. Keep the impression in his voice.
20|What a sight.|What a sight.|Yukihisa gratefully acknowledges what he has just seen. The quiet exclamation follows his awe.
""",
    109: """
7|||The girl checks the rumor that they are seeking mysterious treasures scattered around the world. Her current opening keeps it as hearsay.
10|||She suggests asking the knowledgeable priest at the nearby church. Keep the possibility of a useful answer rather than a promise.
""",
    110: """
5|||The priest asks whether they've come seeking the Proof of Conquest. The direct question keeps his formal speech and the approved term.
15|||This actorless reaction is a wordless question. Keep the source control and the ordinary question glyph.
19|||The priest allows that he may be mistaken. Keep the uncertainty while Hodram considers the question.
23|||Hodram asks what the Proof of Conquest is. The existing phrasing keeps his lack of knowledge.
27|...They say it passes into the hands of the one who rules the seas.|into the hands;the one who rules the seas.|The priest says it is reputed to go to the ruler of the seas. The pause and hearsay remain.
31|||Gerhard echoes the phrase about ruling the seas and calls the story interesting.
34|||Hodram thinks the story may connect to their purpose and politely asks for more. The current wording keeps that tentative conclusion.
40|||Hodram directly asks whether the priest knows anything else. The short inquiry lets the priest test their resolve.
47|The road to finding the Proof is hard. I tell only those truly committed. Are you prepared for it?|finding the Proof;only those truly committed.;Are you prepared for it?|The priest warns that the search is difficult, says he will speak only to people who are committed, and asks about their resolve.
51|If it belongs to the one who rules the seas, I'll face any trial to claim it.|the one who rules the seas,;I'll face any trial|Hodram takes the stated condition seriously and declares he will face any trial to obtain the Proof.
55|||The priest accepts the answer and proceeds to share what he knows. Keep the formal brevity.
59|All I know is that the map to the Proof is useless until you bring two Map Keys together.|the map to the Proof;two Map Keys together.|The priest states the limit of his knowledge and says the two keys are required together for the map to be useful.
63|||The priest emphasizes that either key by itself means nothing. Preserve that separate explanation.
66|||The priest says keys can be in ruins or held by unexpected people, and the crew may have realized this already. Keep both possibilities.
69|||This actorless silence follows the explanation. Preserve its separate source control and pause.
73|||The priest tells Hodram to take a sword. The short English passes over the object without naming it.
80|||The priest charges them to overcome the trials before them and help people in need. Keep both duties.
83|||The priest urges generosity to the poor, restraint from greed, an end to strife at its source, and peace. The formal parallel commands preserve all four parts.
87|||The priest closes by asking for God's protection for them. Keep the blessing in his voice.
""",
}

review = checked_text(previous.review, {"len(records) == 58": "len(records) == 151"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


def combine():
    first, later = map(base.load, (previous.OUTPUT, OUTPUT))
    for field in ("previous_sha256", "source_packet_sha256", "prior_contextual_receipt_sha256", "review_gates"):
        assert first[field] == later[field]
    records = first["records"] + later["records"]
    assert len(records) == len({row["id"] for row in records}) == 209
    result = first | dict(records=records, findings=dict(Counter(row["change_class"] for row in records)),
                          component_manuscripts={str(p): base.digest(p) for p in (previous.OUTPUT, OUTPUT)})
    base.save(COMBINED, result)
    print("Combined 209 contextual decisions.", result["findings"])


if __name__ == "__main__":
    scope["main"]()
    combine()
