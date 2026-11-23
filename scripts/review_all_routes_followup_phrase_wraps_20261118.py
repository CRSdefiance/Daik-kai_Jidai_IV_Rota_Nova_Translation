"""Review the next seventeen wrap leads with their clean story context."""

from inspect import getsource

from scripts import register_all_routes_next_phrase_wraps_20261118 as parent
from scripts import review_rafael_early_phrase_wraps_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, TOKEN, logical, GATES = prior.base, prior.TOKEN, prior.logical, prior.GATES
ROOT = parent.stage.ROOT.parent.with_name("all_routes_followup_phrase_wraps_20261118")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v1.json"
BLOCKS = ((184, 186, 220, 225), (17, 79, 91, 238), (20, 25, 66, 72), (13, 33, 39, 41))
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
CONTEXT = {
    184: "Mihwa lets Julian run off to look for the Silla Gold Crown, then playfully invites Rafael into the search. Clau takes the bait while Rafael is skeptical.",
    186: "Rafael returns the Silla Gold Crown. Mihwa teases Julian about losing the race, and Julian answers with extravagant affection. Clau mentions Reika and the conversation turns to how each group traveled.",
    220: "An older man tells Cristina she reminds him of a formidable pirate. He suggests that she look for the pirate's sword and gives the Caribbean lead while admitting how little he knows.",
    225: "The older man recognizes the seal and recounts the prophecy entrusted to his ancestor. Rafael doubts he is the person foretold, while the man insists and gives the location of the emperor's sword.",
    17: "Aziza explains why her father's sword mattered. She wanted to be a great pirate like him, then realizes she wanted a keepsake. Hodram responds by offering her a place aboard.",
    79: "Hayreddin describes his defeat and the Ottoman demand for his submission. He gives Hodram the token Pasha sent him and leaves him with a stern warning about defeat.",
    91: "A sailor tests whether Hodram believes in miracles. Fernando objects to the insult, but the sailor apologizes and offers the charm to a captain who believes. The typed choice and result notices keep their original ownership.",
    238: "In a letter, Charles reports what sailors said about the Spanish convoy, a mysterious roar, and its escape. He separates the story from what is known and suggests an investigation.",
    20: "Hayreddin warns Lil away from his waters, including when they are technically allies. Gerhard recognizes him and the crew weighs its options against the superior fleet.",
    25: "The crew reacts to Speyer's downfall. Fernando sympathizes with the loss, but Lil remembers that Speyer tried to destroy her company.",
    66: "Lil realizes Kuhn is Camille's father. Kuhn asks how much she knows and starts to leave. Camille calls out to him, confirming the relationship in his own words.",
    72: "Cristina describes the engagement their parents arranged. Mivor tries to explain his feelings, but she cuts him off and asks Julio about the ship. Lil offers her a place aboard.",
    13: "Maria helps Lil get out of danger. Lil is grateful but hates relying on rescue, so she resolves to get stronger. Camille and Maria encourage her.",
    33: "After a victory the crew praises Maria's plan. The banter about her severity and ability gives way to discussing Richard's connections and the others' pasts.",
    39: "Nagarpur mourns his ruined fortune. Xien is surprised to see him still there, and Maria explains that she no longer considers him a threat.",
    41: "Maria delegates negotiations and the town project. She cannot stay in Ming and set aside her other obligations. The threat from the government and the amount needed remain specific.",
}
NOTES = {
    184: """
81|Mihwa only remembers being told the crown was gorgeous.|The playful admission does not add knowledge about the object.
85|Clau's curiosity is piqued and he asks Rafael what he thinks.|The response and name substitution preserve his growing interest.
88|Rafael is curious but points out their ignorance and Julian's head start.|Both objections give Mihwa a reason to tempt him.
93|Mihwa would accept the crown from Rafael too and asks if she is worth a gift.|Keep the playful dare about a gift while giving each thought a clean line.
96|Clau says they cannot back out after that.|The tag closes his attempt to get Rafael to agree.
99|Inwardly Rafael thinks Clau is easy to persuade; aloud he agrees and asks about Seoul.|The aside keeps his skepticism separate from the decision.
103|Mihwa heard Seoul but does not know precisely where.|The distinction between the city and the location is clear.
107|Clau proposes going to Seoul and asking around there.|The practical suggestion answers the imprecise clue.
111|Rafael suggests running into Julian on the way.|The possibility recalls Julian's early departure.
""",
    186: """
82|Mihwa thanks them for the gift and asks what happened to Julian.|The gratitude and sudden question give the reveal its cue.
87|Rafael explains they had just found the crown when Julian appeared.|The exact title and sequence are both preserved.
91|Clau says Julian then took off.|The colloquial report leaves his destination unknown.
95|Julian calls out that he is right there.|The direct call interrupts the explanation.
99|Mihwa tells Julian the others beat him to the prize this time.|Keep the competitive tease and the reference to this occasion in one spoken line.
102|Julian admits that result and says he thought of Mihwa throughout the journey.|His boast about his love preserves the joke after his defeat.
108|Clau asks about Reika and calls her beautiful too.|His remark introduces the next misunderstanding.
111|Julian says Reika's appeal is different from Mihwa's.|The comparison makes Mihwa's reaction intelligible.
114|Mihwa draws out his name and calls him quick to make advances.|The teasing reproach and exaggerated name fit the exchange.
117|Julian rejects the jealousy and claims he only asked about the crown.|The defense keeps the exact topic of his question.
""",
    220: """
25|Cristina asks if her face resembles the pirate.|Her specific question leads naturally into the comparison.
28|The man means her bearing and apparent strength.|The contrast between face and manner carries forward.
32|Cristina wants to live up to the comparison by becoming stronger.|Her answer motivates the sword lead.
36|He suggests searching for the pirate's treasured sword.|The invitation introduces the object without guaranteeing a reward.
40|Cristina repeats the object in surprise.|The echo invites an explanation.
44|It is the sword the pirate is said to have used, and its worth is unknown.|Keep the rumor and his uncertainty in separate, ordinary sentences.
48|Cristina is interested and asks where the sword is.|The question moves naturally from value to location.
51|The man says it is in the Caribbean.|The short answer gives the only broad location.
55|Cristina repeats the Caribbean.|The brief echo gives him room to elaborate.
59|Tradition says the pirate lost the sword while fighting in a large Caribbean sea battle.|The account stays reported and puts the loss in the battle.
62|Cristina asks what else he knows.|The short prompt conveys that the clue is too broad.
66|He knows no more.|The answer preserves his limited information.
70|Cristina asks how she is supposed to find it on that basis.|The plain objection fits her impatience.
73|He has no further facts and merely thinks she can find it.|The wording preserves confidence in Cristina without inventing a location.
""",
    225: """
34|Kublai Khan ruled the continent more than 300 years before this account.|The name, number and speaker's reverence remain clear.
38|The emperor eventually faced death.|The existing line carries the storyteller's solemn transition.
41|He told a retainer the ruler of the oceans would come in two hundred years.|The time is anchored to the emperor's quoted speech.
45|The figure will command foreigners, bear a gold seal from an unconquered land and receive the emperor's sword.|The conditions stay distinct and inside the prophecy.
48|The man descends from the retainer and his family awaited the prophesied ruler.|Keep the ancestry explicit and let the waiting stand as its own sentence.
51|He believes the prophesied figure has finally arrived.|The emphatic greeting carries the conclusion without proving the prophecy true.
55|Rafael is surprised to be called ruler of the seas.|The short question is consistent with his disbelief.
60|Clau refuses to believe the prophecy refers to Rafael.|He cites the ancient prediction first, then objects in his own register.
63|The old man insists he has recognized the king of the sea.|His confidence remains the speaker's claim.
66|He says to search south of the Shandong Peninsula.|The place and direction remain intact.
69|He entrusts the sword to Rafael and takes his leave.|The farewelling turn ends the clue.
""",
    17: """
211|Aziza learned swordplay and piracy watching her father's men.|The relation to the men and how she learned both skills remain clear.
214|A crew member asks where her father is.|The brief question lets Aziza reveal the loss herself.
218|Her father died in an accident and his treasured sword disappeared with him.|The two facts stay separate and preserve her hesitation.
222|Al identifies the Bloodstained Shamshir.|The exact item title ties the confession to the object.
225|Aziza wanted to be a great pirate like her father and copied his ways.|The ambition and imitation stay distinct.
229|She wanted the sword as soon as she heard they had it and begins to explain why.|Use the Rafael wording for the same thought. Aziza still trails off before Hodram reacts.
232|Hodram reacts with a quiet question.|The small interruption leaves Aziza in control of the story.
236|Aziza thought the sword would show she was closer to being like her father.|Her pause and backward look set up what she realized.
240|She really wanted a keepsake more than she wanted greatness as a pirate.|The plain contrast makes the confession clear.
243|She understands why the crew abandoned her over an unprofitable pursuit.|Her reasoning stays sympathetic without endorsing the betrayal.
247|Al asks whether she still wants to be a pirate.|The brief question opens her decision.
251|Aziza decides to leave piracy because it was her father she was pursuing.|The existing metaphor connects back to her pursuit of the sword.
255|Al addresses Hodram with respect.|The short address prompts Hodram's invitation without inventing rank language beyond the context.
259|Hodram anticipates Al and invites Aziza to sail with them.|The direct invitation fits his authority and preserves Al's role.
262|Aziza is grateful and promises to work hard because she owes him her life.|The debt motivates her offer to work.
""",
    79: """
67|Hayreddin meant to hold out for two or three years and show the pirates' pride.|Keep the unrealized plan and its specific duration.
71|A trusted subordinate betrayed him and Pasha took him by surprise.|The sequence explains his condition and shame before his father.
75|Hodram listens silently.|Keep the pause as Hayreddin decides what to say next.
79|Hayreddin sees no point in telling him more.|The terse dismissal fits his wounded pride.
83|He offers the token Pasha sent as proof of submission and says he cannot stand it.|The object, symbolic purpose and anger all stay explicit.
90|He warns Hodram to avoid disgrace if he loses.|Put the warning in one line without turning it into a prediction of defeat.
""",
    91: """
27|The sailor finds a captain who believes in miracles unusual and seems to doubt his reliability.|Keep the provocation that prompts Fernando to defend Hodram.
31|Fernando sharply objects to how the man addresses his admiral.|Use Fernando's already reviewed wording from Rafael's route for this same rebuke.
34|The sailor asks whether he is wrong.|The one-line retort sustains the dispute.
38|Fernando reacts indignantly.|The brief exclamation leaves the sailor room to reverse his criticism.
42|The sailor says disbelievers can end up shipwrecked and says Hodram is better off.|The surprise reverses the earlier insult without claiming every skeptic was wrecked.
46|Fernando is puzzled.|His short reaction gives the sailor the next turn.
50|The man apologizes for shouting and explains he did not mean to insult the captain.|The apology prepares the true reason for asking.
54|Fernando still finds him strange.|The aside fits his confusion.
58|The man was looking for a captain who believes in miracles to take the object.|The wording prepares the reveal of the charm.
61|The man has stopped people as ships arrived and this is the hundredth person.|Match the checked Rafael turn for the same repeated action and exact count.
65|Fernando asks what the object is.|The short question draws out the explanation.
69|The item is a bullet pendant said to bring miracles.|The approved title and reported claim are clear.
72|Hodram asks if he is truly being given such a valuable object.|His terse question preserves regard for the gift.
75|The sailor offers the charm willingly because he is no longer fit to go to sea.|The explanation makes the personal significance clear.
78|Hodram accepts with gratitude.|Concise and formal enough for his reply.
""",
    238: """
27|Charles is in West Africa and heard a strange account from sailors there.|The writer's whereabouts and the story's source stay clear.
31|Pirates attacked a Spanish convoy going from the New World to West Africa.|The origin, destination and attack are distinct.
35|The convoy was outmatched and could not outrun the pirates.|The longer explanation keeps the attempted escape and threat of total loss.
38|Far west of Lisbon, witnesses heard what they described as an unearthly roar.|The distance, location and hearsay remain specific.
41|The sound stirred the sailors to fight the pirates and hold their own.|The lion image and inexplicable change suit the account.
44|The convoy held out until the Spanish navy happened by; the pirates scattered and it escaped.|Use clear sentences for the chance arrival, scattering, and narrow escape.
47|Charles says the sound is unknown and may have a natural explanation.|The uncertainty prevents converting the story into a proved phenomenon.
50|Charles thinks an investigation could be worthwhile and signs the letter.|The suggestion and proper signature preserve the letter's function.
57|Hodram doubts the story but considers the effect on the crew worth investigating.|The measured interest distinguishes his reaction from belief.
""",
    20: """
5|Hayreddin warns the approaching fleet that it is trespassing.|The shout and explicit territorial claim set up the ultimatum.
13|He threatens harm unless they leave the southern Mediterranean.|Both the consequence and the region are spoken.
18|He says the alliance does not permit trespassing and again demands that they leave.|Preserve the conditional warning and put the geographic command together.
33|Gerhard recognizes Hayreddin Barbarossa.|The shouted name gives the pirate a reason to recognize Gerhard.
36|Hayreddin recognizes Gerhard as a pirate hunter.|The role is stated in the source and leads into the crew's reaction.
47|Lil recognizes the Pirate King and is impressed by the number of fleets.|Her surprise and the scale are distinct.
52|Lil reacts to the number of fleets in the alternate branch.|Keep this as the shorter alternative.
67|Camille asks Lil to turn back for now.|The name substitution and temporary advice stay in the choice lead-in.
""",
    25: """
14|Camille feels sorry for Speyer.|The short remark gives Fernando the opening to sympathize.
29|Fernando thinks Speyer will regret losing his business over a pointless quarrel.|Keep the cost of the feud and Fernando's sympathy in complete thoughts.
35|Lil says Speyer brought it on himself by trying to ruin her company.|Her short reply counters the sympathy while preserving the company substitution.
""",
    66: """
92|Kuhn realizes Lil has not heard what he expected her to know.|The tentative conclusion invites Lil to ask what he means.
96|Lil asks what Kuhn is talking about.|Her direct reply follows his assumption.
102|Lil asks if it is Camille's real name and says Camille left.|The distinction between the name and the departure stays explicit.
105|Lil thinks Camille's father would know more than she does.|The question introduces exactly the relationship Lil believes.
109|Kuhn asks if Lil knows of his relation to Camille.|Keep it a question about what she knows. Camille confirms the specific relationship in his own voice shortly after.
113|Lil quietly confirms that she does.|The pause softens her direct answer.
117|Kuhn acknowledges what she said.|The brevity preserves his reluctance to explain.
124|He excuses himself and says goodbye.|His polite exit creates the opening for Camille's call.
128|Camille calls Kuhn Dad.|The explicit relationship is spoken by the source character himself.
132|Lil recognizes Camille.|The brief echo preserves her surprise.
""",
    72: """
83|Cristina says their fathers arranged things without consulting her.|The clear objection gives context for the engagement.
87|Cristina says she is apparently engaged to him and makes light of his oddness.|The aside conveys her disbelief without rewriting the arrangement.
90|Julio acknowledges it.|The brief answer is exactly what irritates Cristina.
94|Cristina objects to Julio taking it so calmly.|The echo gives her irritation a natural English beat.
98|Julio remarks on Mivor's pale appearance.|The understated observation keeps his response in character.
101|Mivor denies speaking from parental instruction and says he really cares for Cristina.|Keep his stammer and earnest feelings, with the instruction referring to the parents just discussed.
105|Cristina complains that her parents want her to give up swords and settle down.|The stated wish and her frustration remain in her voice.
108|Julio says that sounds like Herald and wonders if he raised him wrong.|The reply preserves the existing family context and Julio's regret.
111|Mivor tries to get a word in.|His small interruption gives Cristina an immediate reason to cut him off.
115|Cristina tells him to keep quiet and redirects the talk to the ship.|The quick rebuke and genuine question fit the sharper turn.
119|Julio remembers his offer and says he hoped she'd join him.|The repetition feels like a return to his earlier subject.
123|Lil asks the skilled swordswoman to sail with her grandfather.|The established skill and invitation stay plain.
135|Fernando jokes that any adventure needs a beautiful woman.|The existing boast sets up Lil's reaction.
139|Lil quietly asks what he said.|The sharp change in tone is preserved without adding an insult.
146|Cristina asks Julio who the visitors are.|The familial address is explicitly in the source.
""",
    13: """
10|Camille says they are lucky to be alive and thanks Maria for saving them.|The relief contrasts with Lil's earlier anger.
19|Maria downplays the rescue and warns that the attackers might still be nearby.|The advice retains uncertainty and caution.
23|Lil is silent.|Keep the quiet reaction before her own thanks.
28|Lil thanks Maria and acknowledges the danger.|Her hesitation and the short admission fit the near miss.
31|Maria again reassures them and cautions them to be careful.|The alternative wording stays modest and clear.
35|Lil is embarrassed to keep needing rescue and vows to get stronger.|Keep the embarrassment as well as the defiant promise.
39|Camille encourages Lil.|The short answer supports her resolve.
43|Maria approves of Lil's attitude.|The small laugh and praise end the moment warmly.
""",
    33: """
60|The sailor greets Xien and announces their return.|The familiar address suits his exuberance without adding kinship.
63|Xien heard it was a great victory.|The report gives the participants room to explain.
67|The fleet followed Maria's plan and took the windward position in the narrow bay.|The plan, location and name substitution preserve the tactical point.
70|The enemy appeared where Maria predicted, to the crew's surprise.|The admiral and her name stay explicit in his excited report.
73|A crewman calls it a brilliant stratagem.|The compact praise conveys approval.
77|Xien concludes that Maria has done well.|The quiet reaction contrasts with the younger sailor's enthusiasm.
80|The sailor finds Maria frightening but admires her all the same.|Keep his colloquial praise and balance it against his fear.
83|A crewman says they owe Maria their lives.|The gratitude gives the banter weight.
86|Xien dislikes Richard and says he behaves like Maria's adviser without being useful on a ship.|The existing complaint keeps both his criticism and Richard's self-importance.
90|Richard's connections back in England let them operate in Ming waters.|The existing causal explanation keeps the political and regional details.
93|Xien notes the sailor has no equivalent connections in France.|His contrast sets up the reply about exile.
96|The sailor says he took the blame for someone else's crime and cannot return.|The boastful closing threat suits his account without naming a perpetrator.
""",
    39: """
4|Nagarpur laments losing his money, company and fleet.|The repetition preserves his shock and the three losses.
8|Xien recognizes Nagarpur and asks why he is still there.|Keep the wording and start the question on its own line.
11|Maria says a cashless Nagarpur is no longer a threat.|Her reply identifies why his defeat matters to the crew.
15|Xien quietly agrees.|The short assent gives way to the next reaction.
27|Another speaker mocks him as all appearances.|The blunt idiom preserves the taunt.
34|Nagarpur recognizes the speaker and reacts angrily.|His startled response precedes Maria's reply about money.
37|Maria tells him money cannot solve everything and he has learned it painfully.|The wording preserves both the lesson and her sharp question.
41|Nagarpur growls.|The isolated outburst lets Xien intervene.
45|Xien tells him to calm down and agrees with Maria.|The native name substitution keeps her role clear.
48|Nagarpur is terrified of poverty and begs for money.|The repeated plea is the payoff to Maria's criticism.
52|Xien says words are wasted on him.|The short aside fits the final hopeless reaction.
""",
    41: """
20|Maria asks what else the aide wants.|The question hands him the second request.
24|The aide asks to take charge of building the town.|The request follows the assignment to negotiate.
27|Xien asks whether he would be in charge.|The question leaves room to raise doubts about his ability.
39|A crewman asks if he can handle the work.|The direct objection prompts the reason Maria cannot do it herself.
45|The aide says Maria cannot stay in Ming solely to build the town.|The geographic place and full-time burden remain clear.
49|Maria agrees she cannot stay because she still has other obligations.|State what she cannot do and preserve the sense that many tasks remain.
53|The aide reports rumors of suspicious moves by the Ming government.|The language keeps the risk reported, not certain.
57|Maria reacts in alarm.|The brief reaction sets up the aide's plan.
61|The aide will investigate and deal with the government while Maria keeps sailing.|The division of duties stays explicit.
64|Maria agrees to leave the work to him.|Her response resolves the delegation.
67|He asks for 500,000 after negotiations to fund construction.|The amount and order are both intact.
70|Maria agrees to prepare the funds.|Repeating the amount confirms the agreement.
73|The aide will begin negotiations at once and asks for the funds to be brought to Hangzhou.|The location and separate timing are clear.
""",
}
REVISIONS = {
    (184, 93): ("I'd gladly take it from you, too. Aren't I worth a present?", ("I'd gladly take it from you, too.", "Aren't I worth a present?")),
    (186, 99): ("They beat you this time, Julian.", ()),
    (220, 44): ("Yes. They say she used it. I don't know what it's worth.", ("Yes. They say she used it.", "I don't know what it's worth.")),
    (225, 48): ("That retainer was my ancestor. We awaited the king of the sea.", ("That retainer was my ancestor.", "We awaited the king of the sea.")),
    (17, 229): ("So when I heard you had his sword, I had to have it. I thought...", ("you had his sword,", "I had to have it.", "I thought...")),
    (79, 90): ("If you lose, lose with dignity.", ()),
    (91, 31): ("Watch your mouth! That's our admiral!", ("Watch your mouth!", "That's our admiral!")),
    (91, 61): ("I ask whenever a ship comes in. You're the hundredth.", ("I ask whenever a ship comes in.", "You're the hundredth.")),
    (238, 44): ("They held out for a while. Then the Spanish navy happened by. The pirates scattered. The convoy managed to escape.", ("They held out for a while.", "Then the Spanish navy happened by.", "The pirates scattered.", "The convoy managed to escape.")),
    (20, 18): ("Allies or not, these are my waters. Leave the southern Mediterranean!", ("Allies or not, these are my waters.", "Leave the southern Mediterranean!")),
    (25, 29): ("A stupid feud cost him his company. He's bound to have regrets.", ("A stupid feud cost him his company.", "He's bound to have regrets.")),
    (66, 109): ("Then you know how we're related?", ()),
    (72, 101): ("I-it isn't because they told me to. I do care for you, Cristina...", ("I-it isn't because they told me to.", "I do care for you, Cristina...")),
    (72, 115): ("Quiet, you! Did you say a ship?", ()),
    (13, 35): ("I can't keep getting rescued. It's embarrassing. I'll get stronger. Just watch!", ("I can't keep getting rescued.", "It's embarrassing.", "I'll get stronger. Just watch!")),
    (33, 80): ("She's terrifying. Pretty great, though, huh?", ("She's terrifying.", "Pretty great, though, huh?")),
    (39, 8): ("Oh, that's Nagarpur... What's he still doing here?", ("Oh, that's Nagarpur...", "What's he still doing here?")),
    (41, 49): ("You're right... I can't stay. I still have so much to do...", ("You're right... I can't stay.", "I still have so much to do...")),
}


def main():
    source = checked_text(getsource(prior.main), {
        "len(resolved) == 8": "len(resolved) == 17",
        "assert english != previous and english.isascii()": "assert (english != previous or phrases) and english.isascii()",
        'finding="prose" if key in REVISIONS else "retention",':
            'finding=("wrap" if english == previous else "prose") if key in REVISIONS else "retention",',
    })
    scope = vars(prior) | globals()
    exec(compile(source, __file__ + "::contextual-review-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
