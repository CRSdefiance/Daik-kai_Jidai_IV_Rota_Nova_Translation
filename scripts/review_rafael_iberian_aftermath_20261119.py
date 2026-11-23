"""Reread Rafael's summons, the Sofala dispute, and the adjacent crew exchanges."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_rafael_north_sea_20261119 as parent
from scripts import review_rafael_first_voyage_debrief_20261119 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, workflow, TOKEN = previous.base, previous.native, previous.stage, previous.workflow, previous.TOKEN
ROOT = Path("work/rafael_iberian_aftermath_20261119")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((53, 54, 55, 56, 57, 58), (), (), ())
paired = SimpleNamespace(base=base, native=native, stage=stage, parent=parent, ROOT=ROOT, SOURCE=SOURCE, BLOCKS=BLOCKS)
SCENES = {
    53: "A sailor reminds Rafael that the Portuguese forces sent for them. Rafael confirms where to go.",
    54: "A local repeats the story going around about Silveira and Espinosa. What interests Rafael is the news that the governor's office is moving to Sofala.",
    55: "Fernan claims credit with Albuquerque, announces his appointment, takes Rafael's Sofala shares and boasts that he deducted his own gift. An irritated crew rallies behind Rafael's decision to pursue the region.",
    56: "Two locals thank Rafael's company and give him the clue they pooled their money to acquire. They explain that an adventurer had intended to sell it to Espinosa.",
    57: "Emilio hurts his leg at the pier. Arcadius's visit changes the teasing between him and Clau. Clau declines the food so Emilio can have it and waits for Arcadius outside.",
    58: "Uddin congratulates Rafael and gives him a clue to the Indian Ocean Proof. The original alternatives distinguish whether Uddin still leads his company and whether Rafael thanks him aloud.",
}

# Source index, meaning, decision, and optional replacement.
DECISIONS = {
    53: """6|A sailor recalls the military summons and asks what the admiral wants to do.|Keep the deferential address and practical question. The earlier summons already explains who requested it.|
10|Rafael thinks he should go and checks whether to go to the palace.|Keep Rafael's tentative decision and use the facility name he can select.|Guess we should go. To the Palace, right?
14|The sailor confirms the destination.|The short answer is natural after the question.|""",
    54: """5|A local asks whether Rafael heard the news.|The abrupt call sets up Rafael's polite confusion.|
9|Rafael asks what the local means.|The short response prompts the news.|
14|The local reports that Fernan Silveira beat the notorious Espinosa.|Keep the gossip framed as something heard and preserve both names.|
18|Rafael realizes how the events are being reported.|The understatement shows his doubts without making him argue with the local.|
23|The local thinks Rafael is hard to understand, then says Silveira is preferable to the troublemaking Espinosa.|Keep the speaker's casual judgment and the comparison in an American register.|Huh? You're an odd one. Anyway, I'd take Silveira over Espinosa. That man was nothing but trouble.
26|Rafael says the local may be right.|The pause and qualification show his reservations.|
31|The local heard that the governor's office is being moved to Sofala.|Keep the news as hearsay and preserve the destination.|
35|Rafael repeats the two parts of the news, realizes he must go, and thanks the local.|The startled repetition makes the new destination unmistakable. Keep the thanks before he rushes away.|The governor's office for Africa... In Sofala?! I've got to go. Thanks for telling me!
40|The local calls after Rafael and wonders what just happened.|The brief complaint follows Rafael's abrupt departure.|""",
    55: """5|Fernan addresses Rafael by his given name and congratulates him.|Keep the paternal-sounding familiarity without supplying a family relationship.|
8|Rafael greets Admiral Fernan and is surprised he got here so quickly.|Keep rank, name and the private thought that signals his surprise.|
12|Fernan praises the crew and says he has already made his report to Albuquerque, so there is nothing to worry about.|Keep Albuquerque's form of address and let Fernan's self-satisfaction come through in the abrupt reassurance.|That's some fine work you did! I've already made my report to His Excellency Albuquerque. Nothing for you to worry about.
15|Rafael acknowledges Fernan without enthusiasm.|The hesitant reply leaves Fernan free to keep talking.|
20|Fernan says he turned the offer down until Albuquerque insisted.|Keep his self-serving account and the pause before revealing the appointment.|
24|Fernan announces he has been put in charge as governor of Africa and laughs.|Keep his show of modesty about the position and the triumph in his laugh.|They made me governor of Africa, of all things! Ha! Ha ha!
28|Rafael is shocked.|The direct reaction gives the following notice room to land.|
36|The game reports that Silveira Company took all the player's shares in Sofala.|Name the party and make the ownership of the lost shares explicit. Retain the original system panel and emphasis.|Silveira Company took all your shares in Sofala!
40|Fernan calls the outcome a matter of luck, tells Rafael not to take it badly, and laughs.|Make the laugh and brushing dismissal sound spoken without adding a threat.|Just the way luck goes. No hard feelings, eh? Ha ha ha!
44|Fernan gives Albuquerque's reward and says he already took a gift for his appointment out of it.|Keep the attribution and the joke about helping himself before anyone could offer. Give the punch line its own sentence.|Here's your reward from His Excellency Albuquerque. As for an appointment gift, I took mine out of your reward.
47|Fernan says he will happily accept another gift and laughs again.|The existing mock-politeness follows his deduction naturally.|
54|The game reports a reward of 3,000 gold coins.|Keep the amount, the unusual trailing pause after the theft, and the separate system control.|
58|Rafael realizes Fernan got the better of them.|The unusually sharp reaction follows exactly what was taken from them.|
63|Rafael wonders whether Commander Albuquerque really made this decision.|Keep Rafael's doubt and the source's commander address.|
67|Clau suspects Fernan pressured Albuquerque and lied to claim credit for beating Espinosa.|The current accusation keeps Clau's contempt and leaves his theory explicitly speculative.|
78|Janus admits Fernan was more capable than expected and says the admiral can't let this go.|Keep the live address and Janus's considered indignation.|
90|A sailor says the admiral now has his next target.|The existing energetic address keeps the push to act.|
95|Arcadius says the next goal is decided.|His measured reply contrasts with the louder alternatives.|
102|Rafael is surprised at the response.|The short question keeps his reaction open for the crew to explain.|
115|A crew member says Silveira has finally made him take this seriously.|The direct threat is in character and keeps his sudden resolve.|
121|A sailor says it makes no sense to stay silent about this.|Keep his determination to respond.|
132|Jam says God may forgive Silveira but he won't, then whoops.|Preserve the reference to God and the comic outburst.|
138|Clau says they ought to do it.|His brief assent keeps the crew's exchange moving.|
142|Rafael reluctantly agrees. He dislikes fighting other Portuguese but dislikes backing down even more.|The present wording preserves the tension between solidarity and taking a stand.|
154|A crew member refuses to forgive Silveira.|The existing direct outburst matches her anger.|
168|Julio says he will have to put his old body to work again and calls on Rafael to make an effort.|Use his wry complaint and keep the live given name. Give the call its whole clause.|Well, so much for resting these old bones. FI, let's give it all we've got!
174|A sailor urges the crew to hit back and take Silveira down a peg.|Keep the natural idiom and his readiness to act.|
178|Rafael thanks everyone and commits to prevailing in Africa.|Keep the escalation of ambition and his gratitude to the crew.|
182|Clau is ready to go.|His short response punctuates Rafael's decision.|
186|A sailor answers in agreement.|Keep the affirmative nautical reply.|""",
    56: """5|A local recognizes the head of the player's company.|Keep the company substitution and use a direct question that sounds like a local calling across the street.|Hey! You run FO?
9|Another local is glad Rafael turned up and calls him over.|The quick pair of exclamations gives the interruption energy.|
12|Rafael wonders if they mean him and asks what's going on.|Keep his polite uncertainty as both locals try to get his attention.|
17|A local says times are better than when Espinosa and Silveira were doing as they pleased.|Ground the improvement in their freedom from the two men and keep the local's familiar voice.|Things sure are better than when Espinosa and Silveira ran the place.
21|The other local agrees and credits Rafael's company.|Keep the explicit thanks on behalf of the town.|
24|Rafael is embarrassed by the compliment.|His puzzled modesty fits the other speakers' praise.|
28|A local says the years of crooked merchants nearly made people forget how to trust.|The existing wording keeps the lost trust as a near outcome, not something already gone.|
32|The other local agrees, then remembers why they called Rafael over.|Keep the mid-thought interruption before the handover.|
36|Rafael gives a brief acknowledgment.|It gives the local a reason to ask him to pay attention.|
41|A local asks Rafael to pay attention and hands him the item.|The current direct instruction and short handover work in sequence.|
46|Rafael wonders what he has been handed.|The brief question precedes the possible identification.|
58|Arcadius suspects a connection with a Proof of Conquest.|Keep the possibility, preserve the established title, and let the surprise come naturally.|Wait... Is this a clue to a Proof of Conquest?!
62|Rafael stammers and asks where they found it.|The existing repetition shows his sudden interest.|
66|A local says an adventurer was offering it to Espinosa for a high price.|Keep the proposed sale separate from what ended up happening.|
69|The other local can't believe someone would reveal a Proof's location to Espinosa for money.|Keep the moral outrage and the full title together. The seller was trying to get paid; no sale to Espinosa occurred.|Imagine selling that devil the whereabouts of a Proof of Conquest! Some nerve.
72|Rafael stammers and asks if he is really allowed to take it.|Keep his surprise and the giver's authority to offer it.|Y-you really want me to have it?
77|A local says the whole town paid together and compelled the man to sell so they could give it to Rafael.|Keep the combined contribution, pressure and purpose.|
81|Rafael thanks them.|The direct gratitude is appropriate after their explanation.|
89|A local confirms the handover and asks Rafael to do his best for everyone.|Keep the completed transfer and the expectation that he will act for the town.|
92|Rafael accepts the responsibility.|The brisk affirmation fits the handover.|
97|A local tells Rafael they are counting on him.|The current promise of support ends the exchange naturally.|""",
    57: """5|Emilio cries out in alarm.|The drawn-out cry begins the accident without preempting its cause.|
10|Rafael calls to Emilio and asks whether he is hurt.|The repeated exclamation gives his alarm appropriate urgency.|
14|Clau realizes the pier timber had rotted.|Make the cause the condition of the pier rather than implying the entire pier disappeared.|Huh. The pier must've been rotten.
17|Emilio cries out in pain.|The emphatic sound follows the fall.|
22|Arcadius asks to look at the injury.|The short request fits his calm response.|
26|Emilio is still in pain.|Keep the quieter cry as Arcadius examines him.|
30|Arcadius cautions against movement and suggests letting Emilio rest at the inn.|Keep the practical advice and destination.|
33|Clau grudgingly helps Emilio up and is surprised by his weight.|Give Clau a natural offer to hold on and leave the stammer where he feels the weight.|All right, Emilio. Grab on. Ugh! Y-you're heavy!
40|Rafael is relieved Emilio wasn't badly hurt and notices Arcadius.|Keep the emotional change from relief to curiosity.|
45|Clau wonders what Arcadius is doing buying flowers.|His quick question sets up Rafael noticing the fruit.|
48|Rafael points out that Arcadius also has fruit.|The spare observation works as a response to Clau.|
53|Clau wonders whether it is someone's birthday.|The existing guess sets up the misunderstanding without supplying a reason.|
57|Clau asks Arcadius if he's having a party today.|The familiar approach and casual guess suit Clau.|
60|Arcadius is puzzled by the question.|Use the usual American reaction to a surprising question.|Huh?
64|Clau says he saw flowers and appetizing food and wants some immediately.|Keep his playful entitlement and make it sound spoken.|You had flowers and something that looked good. Come on, let me try some!
68|Arcadius says the flowers and food are for his visit to Emilio.|Put the visit and the purpose of the purchases together, so the misunderstanding ends clearly.|Oh, those? They're for Emilio. I'm going to see how he's doing.
71|Rafael asks why Arcadius is visiting Emilio.|Keep the brief puzzled question.|
76|Arcadius is exasperated that they don't see the point of the visit.|The light rebuke precedes his patient explanation.|
80|Arcadius reasons Emilio must be bored because the others get time in town while he can't go out.|Keep his inference about Emilio and the reason for visiting.|
83|Clau takes this in.|The short response gives the change in his attitude room to register.|
87|Arcadius recalls Emilio likes sweets and says fresh flowers are unavailable at sea, whether Emilio likes them or not.|Keep the uncertainty about Emilio's tastes and the reason fresh flowers are a treat.|Emilio likes sweets, remember? I don't know if he likes flowers, but you can't get fresh ones at sea.
91|Clau tentatively asks whether Arcadius would come if something happened to him.|Keep the vulnerability under his usual bravado.|
95|Arcadius says of course, since they are companions.|Keep the reassuring question and crew relationship explicit without adding any other relationship.|
99|Clau stammers and agrees.|The awkward answer preserves the moment without explaining it.|
103|Clau denies anything is wrong and urges Arcadius to go ahead.|The existing stumble and redirection sound like him recovering from embarrassment.|
106|Arcadius invites Claudio to come along and suggests he might get some fruit.|Use his full spoken name and let the joke about the fruit refer back to the earlier request.|All right... Want to come with me, Claudio? You might get to try some of that fruit.
109|Clau declines and asks Arcadius to give all of it to Emilio, who will be glad.|His understated generosity works after the earlier demand for food.|
113|Arcadius accepts the refusal and excuses himself.|The pauses preserve his hesitation.|
116|Arcadius asks Emilio whether his leg still hurts and offers the food and flowers.|Keep his concern and the unassuming offer.|Does your leg still hurt, Emilio? I brought you a little something.
119|Emilio is delighted by the food, thanks Arcadius, and asks if he knew he liked flowers.|The current answer keeps the pleasantly surprising question.|
122|Arcadius didn't know, is glad Emilio likes the flowers, and invites him to eat plenty.|The wording preserves his pleasure and the warm encouragement.|
126|Emilio responds with delight.|The short cheer gives the exchange a bright ending.|
132|Arcadius calls Claudio by his nickname and asks if he waited.|The shorter name fits the quieter moment; the question leaves his motive unstated.|
135|Clau awkwardly confirms he waited and suggests they go join the others.|The stammer conveys that he is still off balance. Keep his suggestion practical.|
139|Arcadius quietly agrees.|The understated reply holds the scene's change in mood.|
143|Clau remains silent.|Keep the final silence rather than explaining how he feels.|""",
    58: """5|Uddin confirms he is speaking to the admiral by surname.|Keep the source's live surname and the title, with a calm question.|
14|Rafael is startled and asks who has approached him.|The unfinished question leaves room for Uddin's self-identification.|
25|Uddin identifies himself as the former head of the Uddin Company.|Preserve the past tense in this variant.|
30|Uddin identifies himself as the head of the Uddin Company.|Preserve the present tense in this variant.|
38|Rafael recognizes Admiral Uddin.|The short recognition uses the approved title and name.|
45|Uddin commends the admiral for gaining control in the Indian Ocean so quickly.|Keep the speed, sweep, and live surname. Give Uddin a composed compliment.|You took the Indian Ocean in no time. I wouldn't expect any less from you, Admiral FA.
50|Rafael stammers, attributing his success to luck.|The current modesty leaves room for Uddin to disagree.|
54|Uddin says such modesty isn't necessary and considers whether fate was at work.|Keep the distinction between Rafael's claim of luck and Uddin's speculation about fate.|
57|Uddin hands over an item as his final duty as the person overseeing the Indian Ocean.|The current line keeps this his own account of his role, without inventing an appointed rank.|
63|Rafael registers wordless surprise.|Keep the one-character reaction and speaker.|
68|Uddin gives the item's name and reports that it indicates the location of the Indian Ocean Proof.|Keep the established item name whole and leave its function as reported.|The Evergreen Lotus Leaf. They say it'll show you where to find the Proof of Conquest for the Indian Ocean.
72|Rafael realizes the large leaf serves as a map.|The current discovery is short and carries the surprise.|
76|Uddin expects the Indian Ocean Proof of Conquest to be a book called the Rigveda.|Keep the work's name, its form as a book, and Uddin's qualification.|
79|Rafael repeats the name of the work.|The short echo gives him time to absorb the information.|
84|Uddin hopes the Proof will be worthy of Rafael, then takes his leave.|Keep his generous wish and formal farewell.|
95|Clau is surprised to find Uddin a decent older man.|Use an American spoken reaction while keeping Clau's casual appraisal.|Huh. He's a decent old guy.
99|Rafael trails off after addressing Uddin.|Keep the subdued address in this short variant.|
106|Rafael addresses Uddin, thanks him for everything, and says goodbye.|Keep the full farewell distinct from the shorter version.|""",
}

PHRASES = {
    (53, 10): ("To the Palace, right?",),
    (54, 35): ("In Sofala?!", "I've got to go.", "Thanks for telling me!"),
    (55, 12): ("His Excellency Albuquerque.", "Nothing for you to worry about."),
    (55, 24): ("governor of Africa,",),
    (55, 40): ("No hard feelings, eh?",),
    (55, 44): ("His Excellency Albuquerque.", "I took mine out of your reward."),
    (55, 168): ("these old bones.", "all we've got!"),
    (56, 17): ("ran the place.",),
    (56, 58): ("a Proof of Conquest?!",),
    (56, 69): ("a Proof of Conquest!", "Some nerve."),
    (57, 64): ("Come on, let me try some!",),
    (57, 68): ("I'm going to see how he's doing.",),
    (57, 87): ("likes sweets,", "he likes flowers,", "fresh ones at sea."),
    (57, 106): ("some of that fruit.",),
    (58, 45): ("the Indian Ocean", "in no time.", "Admiral FA."),
    (58, 68): ("Evergreen Lotus Leaf.", "Proof of Conquest", "the Indian Ocean."),
}


def main():
    packet = base.load(SOURCE)
    groups = {g["block"]: g for g in packet["groups"]}
    assert groups.keys() == DECISIONS.keys()
    exchanges, edits = {}, {}
    for block, prose in DECISIONS.items():
        rows = [line.split("|") for line in prose.splitlines()]
        assert [int(n) for n, *_ in rows] == [r["source_record_index"] for r in groups[block]["records"]]
        exchanges[0, block] = 0, "\n".join(f"{meaning}|{reason}" for _, meaning, reason, _ in rows)
        edits.update({(0, block, int(n)): (english, PHRASES.get((block, int(n)), ()))
                      for n, _, _, english in rows if english})
    implementation = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n'
            '                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=SCENES[block], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | dict(exchanges=exchanges, EDITS=edits)
    exec(compile(implementation, __file__ + "::iberian-aftermath", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
