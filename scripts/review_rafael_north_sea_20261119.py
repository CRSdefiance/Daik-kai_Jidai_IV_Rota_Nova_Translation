"""Review Rafael's encounters with Lil and Hodram and the summons to Lisbon."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as pair
from scripts import register_rafael_first_voyage_debrief_20261119 as parent
from scripts import review_rafael_first_voyage_debrief_20261119 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, workflow = prior.base, prior.native, prior.stage, prior.workflow
TOKEN = prior.TOKEN
INTAKE = Path("work/rafael_departure_followup_intake_20261119")
ROOT = INTAKE / "rebound_candidate_v2"
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "north_sea_contextual_review_v4.json"
BLOCKS = ((49, 50, 51, 52), (), (), ())
paired = SimpleNamespace(base=base, native=native, stage=stage, parent=parent, ROOT=ROOT, SOURCE=SOURCE, BLOCKS=BLOCKS)

SCENES = {
    49: "Lil confronts Rafael at the Market over North Sea trade. Camille tries to keep the peace. Rafael realizes Lil is proposing a pact, and the shared conflict with Valdes gives both sides a reason to stand down.",
    50: "Lil concedes after Rafael prevails in the North Sea and hands him the key to reading the treasure map. Camille hurries her along. Lil hints at a change in her life that Rafael does not understand.",
    51: "Rafael is startled by Sera in a quiet place. Hodram interrupts the encounter and leaves with her. Rafael's idea that she might be a princess is his own speculation.",
    52: "A messenger relays Admiral Albuquerque's request for the company to return to Lisbon. Rafael wonders why the armed forces want them. The companion replies differ by speaker.",
}

# An empty final field keeps the complete existing command.
DECISIONS = {
    49: """5|Rafael hears a commotion at the Market and goes over to investigate.|Use the facility label Rafael sees in town.|Hm? What's all that noise at the Market? Let's go see.
12|Lil calls out sharply to get Rafael's attention.|The two exclamations make her entrance abrupt.|
15|Camille tells Lil again that she mustn't pick a fight.|Use his immediate admonition to show he is already trying to stop her.|Lil! I told you, no fighting!
20|Lil insists on confronting the issue openly and tells Camille to stay quiet.|Make her answer about speaking plainly and keep her dismissal of Camille.|You've gotta be straight about things like this! Camille, stay out of it.
32|Janus wonders about the unusually hostile mood.|His calm observation contrasts with Lil's shout.|
38|Rafael asks if she needs something from him.|Keep his ordinary politeness before Lil throws his wording back at him.|
43|Lil repeats Rafael's question indignantly and demands to know who authorized their trade.|Keep his phrase as the echo and include the whole crew in the accusation.|Need something?! Who told you people you could trade in the North Sea?
47|Clau threatens Lil in an exaggerated older-brother manner.|Keep his patronizing swagger and turn the drawn-out threat into a spoken challenge.|What's that, little lady? You really wanna get us mad?
51|Rafael apologetically admits he doesn't understand what's going on.|The stammering apology and plain request fit his attempt to cool things down.|
55|Lil calls Rafael stupid to his face.|The direct question gives Janus's response its bite.|
67|Janus laughs at Lil's harshness.|Keep his dry amusement at her insult.|
74|Lil warns she'll explain just once and tells him to listen.|The existing direct orders sound like Lil trying to take charge.|
77|Rafael acquiesces without matching Lil's aggression.|The timid reply fits the mismatch in their moods.|
82|Lil says people everywhere are trying to make a profit and local waters are no exception.|Keep her conversational setup and the reach of the claim.|
86|Camille asks Lil to think about how she is speaking.|Keep his gentle correction while Lil is worked up.|
90|Lil dismisses the correction and claims these waters as Argot Company territory.|Make the first line Lil's answer to Camille and keep the territorial claim and challenge.|I'm doing fine! Anyway, these waters are Argot Company territory. Got it?
93|Rafael offers an uncertain acknowledgment.|Keep the hesitation that provokes Lil's next question.|
98|Lil wonders whether Rafael is all right and really an admiral.|Keep both skeptical questions and her emphasis on his title.|
107|Clau eventually confirms Rafael's role.|Make it sound like a reluctant confirmation and leave the pause before it.|...Yeah, he is.
112|Janus calls Rafael a splendid admiral with relish.|Keep his dry overstatement against Clau's reluctant assent.|
118|Lil is deflated by Rafael's manner.|The terse complaint suits her disappointment at losing the argument she expected.|
122|Lil decides Rafael seems decent enough and offers to explain the situation.|Keep the shift from suspicion to reluctant willingness.|
126|Lil points to the size of the region they call the North Sea.|Her short tag draws Clau into the explanation.|
129|Clau agrees that the region is large.|Keep the brief acknowledgment so Lil can continue.|
142|Lil describes the naval man Hodram who currently moves around the north and forgets his surname.|Preserve the comic lapse without supplying the missing surname.|
158|Lil says Admiral Clifford controls the waters around England.|Keep her broad description of his territory and his rank.|
175|Lil says Martin Speyer of the Hanseatic League is barely keeping things together around Germany.|The dry final beat preserves her skepticism about his control.|
183|Lil wants her people to take most of the remaining areas eventually.|Keep this as her aim and preserve the extent of it.|
187|Rafael asks Lil if signing a town contract leaves everyone free to trade on fair terms.|Keep his respectful form of challenge and match the established trading-contract term.|I see. But Lil, once you sign a trading contract with a town, isn't trade fair for everyone?
192|Lil says she knows the rule and asks them to leave her company alone for a while.|The current wording gives her request the temporary limit she claims.|
196|Clau points out that the proposal suits Lil's own interests.|Keep his short sarcastic retort.|
200|Rafael begins to object and trails off.|Keep the unfinished thought Lil interrupts.|
205|Lil asks whether they have worldwide ambitions.|Keep this as a leading question before Rafael's straight answer.|
208|Rafael confirms Lil's assumption.|Keep the earnest directness that frustrates Lil.|
213|Lil says Rafael is taking the wind out of her argument.|Give her an audible frustrated reaction to his sincere agreement.|Ugh, how am I supposed to argue with you?
225|Janus affirms that the crew has a goal.|His measured reply keeps Lil on the subject.|
238|Lil proposes Africa or the New World to the west.|Both alternatives survive in her practical pitch.|
244|Lil invokes a wide world, the New World to the west, and mysteries in the far east.|Keep her enthusiasm and the separate geographic alternatives together; use lowercase for a relative direction.|It's a big world! Look past this sea. Sail west to the New World, or go solve some mysteries in the far east!
250|Rafael grants that Lil's suggestion is a possible way to look at things.|Keep his openness before Lil makes her request plain.|
255|Lil reiterates that she wants them to leave her people alone temporarily.|The existing demand keeps the time limit.|
259|Lil accepts that they might challenge her openly, then warns her side has a response in mind.|Use a loose threat in her voice and keep her final check for understanding.|If you want to take us on, that's different. We've got a few ideas of our own, you know. Got it?
262|Camille anxiously interrupts Lil.|Keep the stumble and his growing alarm.|
266|Rafael tentatively puts Lil's demand in the form of a pact.|The existing question shows him reading behind her bluster.|
271|Lil is surprised at Rafael's perception and objects to sounding as if she is begging for terms.|Keep her stumble, her surprise at his insight and her wounded pride.|W-what? How'd you pick up on that? You make it sound like we're the ones asking for a favor.
275|Rafael laughs and notices that Lil can't stand to lose.|The amused reaction and short tag fit his growing ease with her.|
279|Lil asks if Rafael is making fun of her.|Keep her defensive response and quick opening.|
283|Rafael politely denies mocking her.|Keep the disarming brevity that leads into the laugh.|
296|A companion chuckles under their breath.|Keep the subdued laugh between Rafael and Julio.|
311|Julio tells Rafael they may be better off earning money in another sea.|Keep his weary intervention and the live name.|
328|Lil asks if Spain's Valdes is their enemy.|Keep Valdes and the question she uses to find common ground.|
331|Rafael considers Spain's threat to Portuguese territory and agrees they're enemies.|Keep his moment of consideration and both political facts.|
336|Lil enthusiastically concludes they have a common enemy and should avoid fighting each other.|Keep the shared enemy and the way Lil talks herself into the conclusion.|Then we've got the same enemy! There's no sense in fighting each other. Right, of course!
343|Rafael gives a tentative acknowledgment.|Keep the uncertain reaction to Lil deciding for them.|
356|Janus understands that Lil wants them to look elsewhere.|His plain restatement keeps the diplomatic implication clear.|
363|Lil checks that they understand and cuts the meeting short because her people are also busy.|The quick goodbye suits the way she takes control of the end of the meeting.|
367|Camille calls after Lil and apologizes for the disturbance while leaving.|Keep his stammer, apology and second call as he follows her.|
381|A companion likens the change in mood to the aftermath of a typhoon.|The short storm metaphor lands just after Lil leaves.|
388|Clau dislikes the outcome but defers to Rafael and agrees to follow his decision.|Keep his loyalty while giving him a plain spoken promise.|I don't like it, FI, but it's your call. I'll go along with it.
392|Rafael decides to leave the region for later because he can't dislike Lil and thinks she could be frightening if angry.|Keep the distinction between his sympathy and his joking caution.|
405|A companion says the decision is wise as long as the North Sea is not the only region left.|Keep the route-dependent qualifier.|
409|Rafael decides to head elsewhere for now.|The simple conclusion closes the exchange without making it a permanent concession.|""",
    50: """6|Lil calls Rafael to a stop.|Keep the quick interruption.|
10|Rafael recognizes Lil after a moment.|His slight uncertainty fits the unexpected meeting.|
14|Lil is surprised he remembers and admits he ultimately got the better of her company.|Keep the comic change of topic and the concession.|
18|Rafael gives a small embarrassed thanks.|His modest answer prompts Lil to brush it off.|
23|Lil waves off the thanks and gives him the key to deciphering the treasure map.|Keep the object distinct from the map itself and preserve the gift.|
27|Rafael is surprised Lil will give it to him.|His disbelief keeps the exchange warm and slightly comic.|
31|Lil sighs and wonders how she lost to this person, then lets it go.|The dry self-directed remark keeps her playful frustration.|
37|Camille finds Lil and reminds her their preparations aren't finished.|Keep his urgency while leaving the purpose of the preparations unstated.|
40|Camille greets Rafael and checks his surname.|Keep the polite greeting and the live surname.|
44|Rafael stammers and checks that the speaker is Camille.|His politeness and uncertainty mirror the greeting.|
49|Camille jokingly wonders whether it counts as a reunion and laughs.|Preserve his uncertainty about what to call their previous encounter.|That's right. I guess this counts as seeing you again... Ha ha.
53|Camille asks whether Lil has been rude again.|The question recalls her earlier confrontational manner.|
57|Lil stretches her answer and says she only gave away the dye she no longer needs.|Keep her sing-song defense and refer to the dye she has just handed over.|
61|Camille realizes the addressed company leader now rules the North Sea and accepts that Lil passed the dye on.|Keep the title implicit in the respectful address, and preserve Rafael's new standing and the original surname.|
65|Rafael is puzzled and asks if something happened.|The direct question sets up Lil's backhanded answer.|
69|Lil starts to call Rafael dense, then makes it sound like a compliment to his easygoing nature.|Keep her audible self-correction.|
73|Lil says she now has something to live for beyond making money.|Keep the change personal and leave her new pursuit unstated.|
77|Rafael claims to understand.|The simple assent makes his later private thought funny.|
82|Lil asks if he has only just caught on.|Keep her playful exasperation at the delayed reaction.|It took you that long to catch on?!
86|Rafael admits privately he doesn't understand and offers congratulations out loud.|Preserve both the inner thought and his deliberately agreeable reply.|
91|Lil thanks Rafael.|Her familiar brevity contrasts with Camille's formal thanks.|
95|Camille thanks Rafael more politely.|Keep the different voice beside Lil's thanks.|
99|Lil asks whether Rafael brought a congratulatory gift.|Keep the casual teasing and the ambiguity about what they are celebrating.|
103|Rafael panics inwardly because he still doesn't know what Lil means.|Keep the stammer and the private realization.|
108|Camille tells Rafael to disregard the request, ushers Lil away and wishes him well.|Keep Camille's politeness, the original live given name and his quick return to leaving.|
111|Lil tells Rafael to do his best for their sake as well.|Keep the good-natured farewell and her indirect request.|
114|Rafael thanks both of them and promises to do his best to meet their expectations.|Keep both names and his sincere promise amid the joke.|
119|Rafael still wonders what the celebration was for.|Keep the private question as the closing joke.|""",
    51: """6|Rafael takes in the quiet and starts to do something he hasn't done in a while.|Keep the unfinished thought when he notices Sera.|
18|Rafael reacts inwardly on noticing her.|Keep the brief private reaction.|
24|Sera offers a small smile.|Keep the silent action in parentheses and the original speaker.|
28|Rafael silently wonders who she is.|Keep both his uncertainty and the thought boundary.|
32|The scene holds in silence.|Keep the original speakerless pause and layout.|
37|Hodram addresses Sera by name.|Keep the simple interruption.|
41|Rafael reacts silently to the interruption.|Keep the brief question in parentheses.|
46|Sera recognizes Hodram and greets him by name.|Keep her short familiar response and approved name.|
50|Hodram asks about Rafael, then answers his own question about whether Sera knows him.|Preserve his quick assessment and the distance he keeps.|
54|Rafael stays silent.|Keep his pause as Hodram sizes him up.|
59|Hodram acknowledges the moment wordlessly.|Keep the reserved sound.|
63|Sera asks after Hodram by name.|Keep her quiet prompt.|
67|Hodram says they are leaving.|Keep his concise direction.|
71|Sera assents.|Keep her direct answer.|
75|Rafael thinks Sera is beautiful and speculates that she might be a foreign princess.|Keep his speculation in his own voice without implying she has a title.|
86|Rafael tries to place the man beside her as someone from the Swedish navy.|Keep the unfinished recollection and leave the identification tentative.|""",
    52: """5|The messenger asks if Rafael is with the named company.|Use a straightforward call and keep the live company name inside the question. His clipped question fits on one line even with a long company name.|Hey, you with FO?
9|Rafael is surprised but confirms the affiliation.|Keep the polite, puzzled answer.|
14|The messenger confirms his suspicion.|Keep the short response before the message.|
18|The messenger says Admiral Albuquerque of the regular Portuguese forces asked him to tell Rafael to return to Lisbon if their paths crossed.|Keep the rank, Portugal, Lisbon as home and the messenger's role. Remove the wide padding inside the current announcement.|Admiral Albuquerque of the Portuguese military told me to pass this along if I saw you. He wants you back home in Lisbon.
21|Rafael wonders what the Portuguese forces want with the crew.|Keep his uncertainty and the group as the object of the summons.|
31|One companion says there's little choice and suggests returning for now.|Keep the colloquial phrasing for this companion's voice.|
36|The other companion says there's little choice and proposes returning for now.|Keep the more measured wording in this alternate reply.|""",
}
PROTECTED = {
    (49, 20): ("Camille, stay out of it.",),
    (49, 43): ("the North Sea?",),
    (49, 244): ("Look past this sea.", "the New World,", "the far east!"),
    (49, 259): ("that's different.", "Got it?"),
    (49, 336): ("fighting each other.", "Right, of course!"),
    (49, 388): ("I'll go along with it.",),
    (52, 18): ("Admiral Albuquerque", "back home in Lisbon."),
}


def main():
    if not SOURCE.exists():
        scope = vars(pair) | dict(parent=parent, ROOT=ROOT, BLOCKS=BLOCKS,
                                  CONTEXT=("Rafael's North Sea encounters and summons to Lisbon.",))
        FunctionType(pair.main.__code__, scope)()
    packet = base.load(SOURCE)
    groups = {g["block"]: g for g in packet["groups"] if g["block"] in DECISIONS}
    previous = {g["block"]: g for g in base.load(INTAKE / SOURCE.name)["groups"]}
    for block, group in groups.items():
        for key in ("source_block_sha256", "current_block_sha256", "records"):
            assert group[key] == previous[block][key]
    exchanges, edits = {}, {}
    for block, prose in DECISIONS.items():
        rows = [line.split("|") for line in prose.splitlines()]
        assert [int(n) for n, *_ in rows] == [r["source_record_index"] for r in groups[block]["records"]]
        exchanges[0, block] = 0, "\n".join(f"{meaning}|{reason}" for _, meaning, reason, _ in rows)
        edits.update({(0, block, int(n)): (english, PROTECTED.get((block, int(n)), ()))
                      for n, _, _, english in rows if english})
    implementation = checked_text(getsource(workflow.main), {
        '    for group in packet["groups"]:': '    for group in groups.values():',
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n'
            '                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=SCENES[block], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | dict(groups=groups, exchanges=exchanges, EDITS=edits)
    exec(compile(implementation, __file__ + "::North-Sea-dialogue", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
