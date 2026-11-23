"""Review whole exchanges around the next 21 paired phrase-wrap leads."""

from inspect import getsource

from scripts import prepare_all_routes_next_review_wraps_20261118 as pair
from scripts import review_rafael_early_phrase_wraps_20261118 as common
from scripts.source_locked_derivation_v5118 import checked_text

base, TOKEN, logical = common.base, common.TOKEN, common.logical
parent, ROOT, QUEUE = pair.parent, pair.ROOT, pair.QUEUE
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v2.json"

EXCHANGES = """
0,254|Rafael asks the priest about the figurehead. The priest explains why most people cannot take it and invites them to try.
26|Rafael finds the figure striking and asks about its history.|His curiosity gives the priest a reason to explain the statue's one known trait.
30|The priest knows no history but has a qualification.|The trailing thought prompts Julio.
33|Julio echoes the priest's unfinished qualification.|An exact echo of the priest's opening keeps the conversational handoff.
37|The figurehead can only be taken by people it likes.|Match the parallel Hodram wording and keep the personification.
41|Most people who tried taking it went home injured and empty-handed.|Both consequences are clear.
45|It somehow returns to the church after its owner dies.|The uncertainty and timing explain why the statue is still there.
49|Rafael finds the story strange.|The brief surprise sits between the explanation and invitation.
53|The priest asks if the party wants to try.|The courteous question opens the choice.
57|Julio objects and asks the Admiral to agree.|The anxious appeal fits Julio's immediate reaction.

0,256|A woman shares the paradox of the Lamenting Jar. Rafael asks who could have made it and grows skeptical as she speculates.
6|She greets Rafael by his given name and asks if he knows of the jar.|The familiar opening keeps the native name substitution and introduces the approved object name.
10|Rafael has not heard of it.|His repetition is a natural request for clarification.
15|She heard of a clay jar supposedly made before pottery was invented.|Keep the paradox exactly as the rumor presents it.
18|Rafael asks who could have made such a jar.|His direct question raises the mystery she enjoys.
22|She says the mystery is what makes the story interesting.|Two short beats carry her enthusiasm without a split subject.
26|She speculates that an advanced ancient civilization could have died out.|The tentative explanation keeps both the lost civilization and her uncertainty.
29|She suggests visitors from the sky left it.|Her increasingly fanciful suggestion sets up Rafael's reaction.
32|Rafael laughs awkwardly and asks whether the jar has been found.|His internal reaction preserves both disbelief and his outward courtesy.
36|She has no discovery to report but believes it is real.|Her conviction is clear without turning the rumor into fact.
39|Rafael doubts it.|His plain question closes the exchange.

0,261|A crewmate calls Rafael over to a peculiar object. A cracking sound interrupts his description and the statue speaks.
129|A crewmate calls the admiral over to a strange statue.|His warning and address give Rafael an immediate reason to respond.
132|Rafael asks where it is.|The short question keeps the motion of the scene.
137|The crewmate points it out and tentatively identifies it as a figurehead.|Keep his observation in one thought before the interruption.
144|The crewmate is alarmed by the cracking sound.|The stammer sets up the unexpected voice.

0,264|A woman greets Rafael then answers his question about famous ruins.
6|She greets the captain by his given name.|The greeting keeps the live name substitution and her familiar register.
10|She echoes his global search and says the town has no particularly famous ruins.|Keep the friendly qualification and match the parallel Hodram reply.

0,287|After Rafael collects the reward, the speaker mentions the nearby ruins and a map that was found. Rafael follows up about its location.
69|He has heard of an old kingdom's ruins near town and an illustrated map that points to them.|Restore the conversational opening and remove the artificial spaces between clauses.
72|Rafael asks where the map can be found.|Use the established map as the natural referent.
76|The speaker does not know where it is and suggests looking if Rafael is curious.|Keep his uncertainty and advice, with the question on a complete line.

1,302|The party decides whether to cross a sandstorm. Hodram gives a decisive order if they push in and a cautious assessment if they wait.
180|Hodram rejects waiting any longer and orders the party through the storm.|Keep both sentences and move the order onto its own line.
193|Hodram decides that pressing on is too dangerous and waits for the storm to end.|The qualified caution belongs to the alternate choice.

1,305|Hodram asks whether the mapped golden temple is by the place the woman plans to visit. She recognizes it and offers to guide them partway.
17|She assures him they will only look around.|The reassurance is distinct from the later offer of help.
20|Hodram remembers something related.|The hesitant lead-in keeps the change of subject.
24|He asks if the golden temple on the map is near there.|The map and distance are the two relevant details.
27|She recognizes the temple once she hears golden and says it is some distance away.|Give her realization room and keep the description on a complete line.
31|She offers to go partway and says the map will guide them afterward.|The two sentences make the limits of her offer clear.

1,310|The host welcomes Hodram, hesitates about the city gate and explains why she will tell him in confidence.
6|She greets him by name.|The native given-name token preserves her familiar welcome.
9|She confirms that he wants to know where the gate is.|The question sets up the restriction on what she can tell him.
13|She is supposed to keep the gate's location from foreigners.|Make the reference clear and retain her hesitation.
16|Foreign pressure has made the country's seclusion policy ineffectual, so she offers to tell him discreetly.|The political context stays in her own reasoning and the offer becomes conversational.

1,312|A woman remembers the rumor of an old illustrated map. Hodram asks where it is and she suggests looking for it.
6|She greets him by name and recalls what she meant to say.|The existing greeting gives the forgotten news a natural lead-in.
10|An old illustrated map was reportedly found and seems to show an old kingdom's ruins near town.|The report preserves the two degrees of uncertainty.
13|Hodram asks the map's present location.|His short inquiry moves the rumor toward an actionable clue.
16|She apologizes for not knowing and suggests he look for it.|Keep the friendly apology and put the suggestion together.

1,318|The guide plans a private approach to the ruins by small boat. After the trip the party has to continue overland and encounters Rafael.
63|The guide has arranged a small boat for the next stage.|The specific means of travel prepares the move onto land.
66|Only the party has permission and the sailors must not learn the ruins' location.|Both parts of the explanation remain clear.
79|The guide announces their arrival and proposes taking the land route from there.|Keep the travel transition and put the next instruction in one sentence.
82|Rafael is startled.|The brief reaction prepares the encounter.
94|Hodram recognizes Rafael from the Castor Company and asks why he is there.|The company and name identify who has appeared.
100|Hodram asks who is there in a different branch.|The short question preserves the alternate reaction.

2,133|Rafael recognizes the commander of Lil's company. Lil asks who he is and is astonished by his answer and apparent youth.
21|Rafael confirms Lil's identity and company.|Both native substitutions remain and the check is tentative.
26|Lil jokes about her fame then asks who Rafael is.|The joke makes her introduction warm and bold.
29|Rafael gives his full name and company before Lil reacts.|Keep both proper names whole and make the introduction sound spoken.
35|Lil is startled that he represents the Castor Company.|Her incomplete exclamation carries her surprise into the next turn.
38|Rafael reacts with confusion.|The silent question gives Lil room to say why.
43|Lil cannot believe someone that young is in charge.|The frank reaction preserves the setup for their banter.

2,136|Emilio fits the tablets together. Lil recognizes the chart, Emilio mishears her and she corrects him before they set out.
15|Emilio notices how to put the halves together.|The excited discovery lets him solve the immediate problem.
18|Lil confirms the fit.|Her exclamation rewards Emilio's discovery.
22|Lil thinks the assembled tablet might be a chart to Africa's Proof of Conquest.|The tentative identification sets up both the clue and the pun.
25|Emilio hears cheese tart and asks where it is because he wants some.|Keep the English mishearing that supports Lil's correction.
29|Lil corrects the misunderstanding and urges him to find the Proof of Conquest.|Keep the pun and use the complete approved name of the objective.

2,150|Clifford and the crew exchange greetings. Lil asks about his activities in the New World before turning to his alarming letter.
24|A crewmate recognizes Clifford.|The quick greeting makes the reunion immediate.
31|Clifford has heard of their success around the world.|His greeting leads into mutual acknowledgment.
42|Camille thanks Clifford and returns the compliment.|Keep his restrained courtesy before Lil's direct question.
48|Lil infers from Clifford's presence that he is expanding his influence in the New World.|Keep the inference a question and attach his name without a sparse lead line.
52|Clifford gives a qualified yes.|His hesitation motivates Lil to ask about the letter.
56|Lil read his letter and wants to know the problem.|The blunt inquiry moves the conversation on.
60|Clifford says there is trouble and names the presence of three powers.|Keep the number and the region as the context for his briefing.

2,151|Lil and Maldonado trade insults over New World commerce. He later resolves to drink again and turns his anger into ambition.
134|A crewmate recognizes Maldonado.|The quiet aside identifies the new arrival.
141|Maldonado recognizes Lil and realizes she intends to expand into the New World.|His accusatory conclusion sets up her dry reply.
145|Lil acknowledges it and greets her competition.|The polite words carry a deliberate barb.
148|He insults Lil and her small country and calls interference with Spanish trade outrageous.|Keep the insult that Lil repeats and the commercial claim he makes.
152|Lil takes offense at tiny and insists she can trade anywhere.|Keep the repeated adjective and make the outburst read without a break inside her rebuke.
164|Camille recognizes that another argument has started.|His resigned aside supplies the joke.
176|A crewmate expects the familiar escalation.|The wry response underlines Camille's reaction.
287|A crewmate objects to being restrained.|The blunt order fits the quarrel.
291|The reply asks him to stop for the sake of the tavern.|Keep the immediate reason he is restrained.
295|The frustrated crewmate swears.|The short mutter closes the confrontation.
305|Maldonado goes back for another drink and calls Lil an infuriating girl.|Preserve the other drink and his indignation before his calculation takes over.
308|He threatens to smash Lil's company and starts to see a possible benefit.|The native company substitution and false start keep the turn from anger to opportunity.
311|He hopes defeating her will win royal recognition and permission to expand.|The moth simile and the conditional keep it as his own calculation.
315|He imagines passing Escante and stammers with pleasure.|His private excitement lands as the payoff.

2,154|Lil wants to recruit someone she finds impressive. Camille reluctantly agrees and Lil teases him for being so accommodating.
75|Camille jokes that Lil judges men by how cool they are.|The first-name substitution, familiar critique and vocabulary joke establish their banter.
78|Lil brushes the critique off and wants to recruit him.|Her enthusiasm pulls Camille into the joke.
81|Camille sarcastically gives in.|His brief concession sets up her teasing response.
84|Lil laughs and needles Camille for being agreeable today.|Keep her laugh and a complete tag question.
87|Camille protests that Lil never listens in these situations.|The complaint gives her an easy opportunity to pretend not to hear him.
90|Lil pretends she cannot hear that.|The simple question and response convey the tease.
95|Lil calls to the man to wait.|The quick interruption closes the banter.

3,102|Xien tells Maria about the Guiding Staff. She says she is all right with him there, but wants to see the staff if the story is true.
106|Maria asks what Xien is proposing to look for.|Her question invites him to identify the staff.
110|Xien names the Guiding Staff.|The approved item name answers her directly.
114|Maria repeats part of the name uncertainly.|The echo prompts the explanation.
118|The staff supposedly guides its bearer toward good and is said to be in India.|Lead with the report and give the location its own beat.
122|Maria thanks Xien and tells him she is all right with him there.|The understated reassurance preserves her reliance on him.
126|Xien acknowledges her answer.|His brief reply leaves space for her reconsideration.
130|She would like to have it if it really guides people toward goodness.|The conditional preserves the difference between comfort and interest.

3,116|A new crewmate asks why people fear Maria. Ian distinguishes fear from her strict treatment of deeds and illustrates it with her judgment of a deserter.
7|A crewmate addresses Ian.|The familiar opener precedes a serious question.
11|Ian asks what he wants.|The brief answer keeps the opening conversational.
15|The crewmate asks if the admiral is really as frightening as people say.|The live name and his personal doubt motivate Ian's distinction.
24|Ian says the newcomer missed earlier events and describes Maria as strict in rewards and punishments.|Restore the stated distinction from being frightening and remove source padding from the visible prose.
30|An alternate speaker gives the same substance in a rougher register.|The casual syntax and vocabulary make this voice distinct from Ian.
36|Ian begins an account of a past incident.|The short lead-in turns the general point into an example.
54|The listener reacts to the reversal of the battle.|The outburst follows the two preserved panels of the account.
58|Maria had prepared a leadership post and gold for the man's victory.|The individual acts retain their importance to the later judgment.
61|She immediately sentenced him to death for desertion.|The quick reversal preserves the two charges being treated on their own merits.
64|The listener is quiet.|The silence leaves the result for Ian to explain.
68|Maria gave the gold to the family and promised a permanent pension.|Both forms of support show the promised reward taking effect.
72|The man thanked Maria in tears and accepted the sentence.|The ending keeps his gratitude and compliance.
82|Ian describes how frightening and sorrowful Maria looked.|His firsthand impression gives the opening question its emotional answer.
87|Yukihisa describes the same fear and sorrow formally.|His register preserves his manner in the alternate account.
93|The listener had never known what happened.|The quiet reaction follows the reflection on Maria.

3,129|Angelo admits he thought Bianca was missing. He recalls her telling him that his friends are his family and urging him to live for himself.
52|Angelo thought his sister was missing and searched worldwide.|The wording keeps the location broad and his belief personal.
55|Maria addresses Angelo quietly.|The short address conveys concern without filling the pause.
59|Angelo connects her words to his collapse with a fever.|The unfinished thought introduces his memory.
63|Bianca tells Angelo that the people with him are his family now and that he should live for himself.|Make the plural address clear and give her advice a complete line.
66|Maria listens silently.|Her pause lets Xien respond.
70|Xien says Bianca was a fine sister and cared for Angelo.|The simple sympathy leads into his advice.
74|Xien urges Angelo to keep living and live for his sister too.|The distinction between his own life and living also for her remains clear.

3,130|Maria questions Carlo's reading of a man's health. Carlo says he notices such things and invites her to come to the trade house the next morning.
88|Maria says the man did not look so unwell to her.|Her doubt is expressed tactfully before Carlo explains.
92|Carlo says most people would miss it and he is perceptive about health.|The explanation is important because he noticed something Maria missed.
96|Maria reacts privately.|The small internal response keeps Carlo's floor.
100|Carlo asks Maria to join him at the trade house the next morning and thinks he can make up for today.|Keep the place, specific time and tentative offer in readily spoken phrases.
103|Maria agrees immediately.|Her short acceptance sets up the following morning.
107|The speaker thanks Carlo for the day before.|The explicit time reference helps the transition.
111|Carlo asks after Adil.|The question confirms his concern.

3,140|Yifa pleads for a place aboard to train and prove her teacher wrong. Maria recognizes her ambition and sets conditions for taking her along.
108|Maria checks whether Yifa is serious about traveling the world.|The practical question shifts from the demonstration to her reasons.
112|Yifa wants to prove her teacher wrong and begs to see the world.|Her insistence preserves the motivation in her earlier account.
116|Maria acknowledges that wanting to prove someone wrong can help one grow and asks her name.|Her measured reply takes the young recruit seriously.
120|Yifa gives her name eagerly.|The exclamation answers Maria directly.
124|Maria requires Yifa to work as a full member of the crew and expect no special treatment.|State the work requirement plainly without implying a formal rank or status.
128|Yifa gladly accepts the conditions.|Her enthusiastic agreement fits the chance she asked for.
132|Yukihisa introduces himself and vows against a second lapse of guard.|His formal return to their sparring preserves the challenge.
135|Yifa teasingly challenges him to beat her Taoist art.|The reply resumes their rivalry.
"""
CONTEXT, NOTES, selections = {}, {}, [[], [], [], []]
for exchange in EXCHANGES.strip().split("\n\n"):
    header, *notes = exchange.splitlines()
    identity, context = header.split("|", 1)
    route, block = map(int, identity.split(","))
    assert block not in CONTEXT
    CONTEXT[block] = context
    NOTES[block] = "\n".join(notes)
    selections[route].append(block)
BLOCKS = tuple(tuple(route) for route in selections)

REVISIONS = {
    (254, 33): ("But?", ()),
    (254, 37): ("It only goes with people it likes.", ()),
    (256, 22): ("That's the mystery! That's what makes it fun.", ("That's the mystery!", "That's what makes it fun.")),
    (261, 137): ("Here. Looks like a figurehead...", ("Looks like a figurehead...",)),
    (264, 10): ("You travel the world to find ruins? I'm afraid none here are famous.", ("You travel the world to find ruins?", "I'm afraid none here are famous.")),
    (287, 69): ("Heard the news? There might be ruins of an old kingdom nearby. Someone found an illustrated map that shows the way.", ("Heard the news? There might be", "ruins of an old kingdom nearby.", "Someone found an illustrated map", "that shows the way.")),
    (287, 76): ("I couldn't tell you. Curious? Why not look for it?", ("I couldn't tell you.", "Curious? Why not look for it?")),
    (302, 180): ("We can't wait any longer. We're going through the storm.", ("We can't wait any longer.", "We're going through the storm.")),
    (305, 27): ("Golden? Oh, that temple! It's a ways off...", ("Golden? Oh, that temple!", "It's a ways off...")),
    (310, 13): ("I'm not supposed to tell foreigners where it is...", ("I'm not supposed to tell foreigners", "where it is...")),
    (310, 16): ("Foreign pressure has made our policy of isolation all but meaningless. All right. I'll tell you in confidence.", ("Foreign pressure", "our policy of isolation", "all but meaningless.", "I'll tell you in confidence.")),
    (312, 16): ("Sorry, I don't know. If you're curious, you could look.", ("Sorry, I don't know.", "If you're curious, you could look.")),
    (318, 79): ("We've arrived. We'll go on foot from here.", ("We've arrived.", "We'll go on foot from here.")),
    (133, 29): ("I'm Rafael Castor, with the Castor Company.", ("I'm Rafael Castor,", "with the Castor Company.")),
    (136, 29): ("Emilio. A chart, not a cheese tart. Let's find the Proof of Conquest!", ("Emilio. A chart, not a cheese tart.", "Let's find the Proof of Conquest!")),
    (150, 48): ("Clifford, are you expanding into the New World?", ("are you expanding", "into the New World?")),
    (151, 148): ("Hmph! A brat from tiny Holland! You dare meddle in Spanish trade?", ("Hmph! A brat from tiny Holland!", "You dare meddle in Spanish trade?")),
    (151, 152): ("Quit calling us tiny! How rude! I'll trade wherever I like!", ("Quit calling us tiny! How rude!", "I'll trade wherever I like!")),
    (151, 305): ("Tch! Back I go for another drink. That brat makes my blood boil!", ("Tch! Back I go for another drink.", "That brat makes my blood boil!")),
    (154, 84): ("Heh heh. Awfully agreeable today, aren't you, Camille?", ("Awfully agreeable today,", "aren't you, Camille?")),
    (102, 118): ("They say it guides whoever holds it to do what's right. I hear it's in India.", ("They say it guides", "whoever holds it", "to do what's right.", "I hear it's in India.")),
    (116, 24): ("You joined us later, so you wouldn't know. Scary isn't the word. She's strict about rewards and punishments.", ("so you wouldn't know.", "Scary isn't the word.", "about rewards and punishments.")),
    (129, 63): ("My sister said you're my family now. All of you. She told me to live for myself...", ("My sister said", "you're my family now.", "All of you.", "to live for myself...")),
    (130, 100): ("Will you come to the trade house with me tomorrow morning? I think I can make up for today.", ("Will you come to the trade house", "with me tomorrow morning?", "I think I can make up for today.")),
    (140, 124): ("If you sail with me, Yifa, you'll have to pull your weight. No special treatment.", ("If you sail with me, Yifa,", "you'll have to pull your weight.", "No special treatment.")),
}


def main():
    paired, selected = map(base.load, (SOURCE, ROOT / "selected_wrap_leads.json"))
    assert selected["paired_source_sha256"] == base.digest(SOURCE)
    assert selected["queue_sha256"] == base.digest(QUEUE)
    assert selected["candidate_sha256"] == paired["candidate_sha256"]
    assert len(selected["records"]) == 21
    selected_keys = {(row["block"], row["source_record_index"]) for row in selected["records"]}
    assert selected_keys <= REVISIONS.keys()
    old_review = base.load(parent.REVIEW)
    parallel = {(row["block"], row["source_reference"]["record_index"]): row for row in old_review["records"]
                if (row["block"], row["source_reference"]["record_index"]) in {(243, 36), (255, 10)}}
    for new_key, pair_key in (((254, 37), (243, 36)), ((264, 10), (255, 10))):
        group, = [group for group in paired["groups"] if group["block"] == new_key[0]]
        row, = [row for row in group["records"] if row["source_record_index"] == new_key[1]]
        assert row["source_body_hex"] == parallel[pair_key]["source_hex"][2:]
        assert REVISIONS[new_key][0] == parallel[pair_key]["english"]
    source = checked_text(getsource(common.main), {
        "len(resolved) == 8": "len(resolved) == 21",
        "assert english != previous and english.isascii()": "assert (english != previous or phrases) and english.isascii()",
        'finding="prose" if key in REVISIONS else "retention",':
            'finding=("wrap" if english == previous else "prose") if key in REVISIONS else "retention",',
    })
    scope = vars(common) | globals()
    exec(compile(source, __file__ + "::contextual-review-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
