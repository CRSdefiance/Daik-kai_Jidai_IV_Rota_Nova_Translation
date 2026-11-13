"""Seal individual meanings for all400 clean objects before consulting eligible English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_only_gloss_v1 import seal

ROOT=Path('work/Hodram_B311_B324_clean_20261107')
PACKET=ROOT/'clean_source_packet.json';SCOPE=ROOT/'clean_intake_scope_v1.json'
ORDINARY=ROOT/'all151_ordinary_clean_meanings.json';OUT=ROOT/'all400_clean_meanings_before_English_v1.json'

CONTEXT={
311:'A complete map-gated dark-forest expedition. Companions hear something; a rock threatens from behind. Left/right route and brush choices include a dead end, ducking into brush, silence and checking whether everyone is safe. A snake frightens a companion; another branch reports the rock rolling down the left path. The party flees, pants, complains, shows apparent sailor fatigue, receives a stern encouragement and eventually reaches safety. Do not invent a deliberate trap, deaths, a rockslide or the gender/identity of an unresolved dynamic companion.',
312:'Speaker205 greets FI and remembers information left unsaid: a recently found ancient pictorial map apparently locates ruins of an old kingdom near this town. Hodram asks where the map is; the speaker does not know and suggests searching if interested. Preserve the reported uncertainty and distinguish discovering the map from already visiting the ruins. The source location field is metadata, not a surname.',
313:'A map-gated desert expedition encounters scorpions, with fight/drive-off/flee choices. Both successful forceful responses have companions reporting that the scorpions fled, not confirmed deaths. Hodram can be injured and need a one-day treatment stop; quiet retreat includes dropped baggage, alarm, a sailor cry and apparent sailor injury. The captain orders a quick dash and the destination eventually appears. Preserve separate outcomes, prompt-treatment urgency, source curses only where present, and generic bodily cries without inventing unconsciousness or death.',
314:'Speaker204 asks FI about a Goryeo celadon incense burner reportedly somewhere in East Asia and its reputed benefit for divination. The speaker wishes to try it, then warns of pirates active nearby and recommends proper equipment. Source selector0 supplies the two mild responses despite this being the SC1 archive; do not silently replace that speaker with Hodram, infer kinship, or turn a regional field into a surname. Source/runtime speaker binding remains required.',
315:'The return exchange thanks the visitor for the incense burner: the speaker reports more accurate divination and offers a fortune reading in thanks. After inviting the visitor to sit and two silences, the speaker gives a ruins lead far inland from this town, deep in the desert, saying the object sought should be there. Keep this as the character’s divination, not a guaranteed game reward or proof of supernatural fact. No payment or romance is stated.',
316:'A complete map-gated wooded expedition meets fog and a dead end. Choices include continuing despite fog or waiting for it to clear, then cutting through trees anyway or searching for a way around. Responses differ in obedience, skepticism, enthusiasm and safety judgment. A fork/path can be found; another route brings apparent sailor fatigue. Two silent FE pauses grow longer, exactly one day passes, the fog seems clear and the captain orders departure. Preserve tentative weather observations and do not turn a way around into a named secret passage.',
317:'A map-gated jungle expedition concerns humidity and party exhaustion, finds a cave, and offers feeling the way forward or lighting a fire. In darkness the captain feels something, a companion warns of a huge snake and a threatened party member, and Samwell panics with a specific Indian-python identification followed by uncertainty. Retreat brings apparent sailor injury and an uncertain emergence near ruins. Lighting produces a huge bat swarm; some voices warn that passage is impossible or recoil, while Hodram presses on and apparent fatigue can follow. Keep the source uncertainty, comic taxonomic aside and different route outcomes; do not add snake bites, swallowed victims, vampire bats or a specified torch.',
318:'A local guide first requires a map, then explains that the ruins apparently are not on this island and a sea crossing is needed. A small boat is prepared; the guide says only the party is qualified and asks that sailors not learn the ruins’ location. After a one-day crossing they continue overland and encounter Rafael, with recognition and unknown-person alternatives. Rafael was asked to search but got lost. Hodram’s quoted indiscriminate recruitment refers to clean B287R104, where the requester admits asking strong-looking people at random. The guide explains joining because no word came from the searchers. Rafael blames his own inadequacy; they agree to cooperate and find the ruins. Do not infer that all recognition alternatives occur consecutively, that absent searchers died, or that this generic Villager must be the same individual as every other use of actor179.',
319:'Speaker206 relays a customer’s story about a respected monk from this town who went to the northern continent to spread his faith, found a village far north in the New World and then went missing. The speaker wonders what happened, hopes the people there grew fond of him and asks the captain to inquire if traveling north. Hodram gives a terse uncertain response. Preserve hearsay, the existing village rather than founding a settlement, and the absence of a named religious order, abbot rank or exact village name.',
320:'A village resident asks the unfamiliar visitors’ origin. Hodram identifies Sweden in northern Europe; the resident has never heard of it and infers a distant journey. The resident has heard of a sextant that locates a vessel at sea without landmarks and proposes a barter, keeping the promised return gift a surprise until the sextant is brought. Do not name the gift, claim ownership is already established, or add a formal village-chief title.',
321:'The paired barter return: a village resident acknowledges the requested sextant and offers an unnamed object in exchange; the FE result states that the sextant was handed over. Preserve the transfer direction and do not add money, a named reward or retention of the instrument.',
322:'A companion announces disembarking the survey party. Two alternative FE funding notices state either all available money or exactly1000 gold coins were provided as initial funds. A sailor announces the investigation is beginning and requests a report to the Sofala guild. Funds are supplied to the expedition, not a reward paid to the player; the text does not establish a particular result, discovery, death or report timing.',
323:'A village resident asks whether this is the object the visitors sought, reflects on a long wait and the day finally arriving, then decides to trust them and offers it. Keep the object unidentified in the spoken text and the solemn progression. Do not combine this generic resident automatically with the sextant barter or name a Proof, ore or royal rank without source evidence.',
324:'A complete village account links the missing monk to devoted care during a deadly illness. His medicine quickly relieved symptoms; the witness recalls alchemy removing mineral poison from drinking water, with imperfect secondhand understanding. Conditional Lil/Charles responses identify the Alchemy book and Charles’s excited interest in rumored New World experimental material and precious metal. Hodram cuts short the explanation. The witness then reveals that the monk fell ill from the same local water, hid it, distributed all his medicine and died, praising him as God’s messenger. The party is asked to inherit the research and seek an unseen ore believed to exist somewhere. Hodram promises; Charles’s optional enthusiasm prompts a dry offer of fleet command in the region where the ore is found and freedom to research. Preserve grief, reported knowledge, conditional participation and the explicitly sourced command offer; do not invent contagious transmission, a specific toxin/metal, canonization, burial, kinship or a modern five-star naval rank.',
}

MEANINGS={
311:'''84|Hodram reacts with a questioning sound.
113|A sailor gives a long frightened cry.
117|Hodram orders everyone to run.
156|Hodram orders them to dive into the brush beside the path; no particular side is stated here.
172|The dynamic208 companion is silent.
176|Hodram urgently checks whether everyone is safe.
180|A sailor gives an informal drawn-out affirmative response.
185|The dynamic208 companion is silent in another route outcome.
189|Hodram urgently checks whether everyone is safe in the alternate outcome.
193|A sailor gives the same informal affirmative response.
239|Hodram urgently asks what is wrong.
270|A sailor cries out in fear and urges flight.
274|The dynamic214 companion pants or wheezes breathlessly; express the vocal sound rather than a medical diagnosis.
278|A sailor cries that they have had enough and do not want more of this.
284|The sailors appear fatigued; the statement is tentative.
290|Hodram says only a little farther remains and sternly tells the party not to complain or lose heart.
323|Hodram expresses relief at having escaped danger.
327|A sailor says the incident was a real fright.''',
312:'''6|Speaker205 greets FI and says there was something to tell him that was completely forgotten.
10|An ancient pictorial map was reportedly found recently; it apparently indicates ruins of an old kingdom near this town.
13|Hodram expresses interest and asks where that map is.
16|The speaker apologizes for not knowing that much and suggests looking for it if interested.''',
313:'''65|Hodram says heat is unavoidable in a desert and orders the party onward.
68|A sailor stammers a startled cry.
92|Hodram orders calm.
96|The sailor hesitantly objects and asks what Hodram intends to do.
115|Hodram tells the others to leave it to him and gives a forceful effort cry.
139|Hodram tells the others to leave it to him and says he will drive the creatures off.
162|Hodram gives a short strained or pained exclamation, without an explicit curse.
189|Hodram curses and admits letting his guard down.
228|FI was injured; the party stays exactly one day for treatment. The notice does not guarantee complete recovery.
236|Hodram apologizes and says he is all right now.
242|Hodram orders a quiet retreat and tells the party not to provoke the creatures needlessly.
275|A heavy thud is heard; the next turn identifies dropped baggage, not an explosion or death.
279|A sailor exclaims at the baggage falling; no amount of cargo or permanent loss is specified.
303|A sailor gives a harsh cry of pain or alarm.
331|Hodram orders the party to run through quickly.
336|A sailor appears to have been injured; exact number and type of injury are not stated.
355|A sailor excitedly judges that they seem to have arrived.''',
314:'''6|Speaker204 welcomes the visitor.
10|The speaker asks FI whether he knows of a Goryeo celadon incense burner reportedly somewhere in East Asia.
14|The object is said to make divination much more accurate; the speaker longs to try it once.
30|Source selector0 responds with mild, noncommittal interest.
35|The speaker remembers another point.
39|Pirates appear to have been active nearby lately; the speaker recommends properly preparing equipment.
43|Source selector0 expresses surprise, finds the situation dangerous, thanks the speaker and promises caution.
47|The speaker gives a casual farewell.''',
315:'''6|The speaker warmly welcomes the visitor again.
10|The incense burner received from the visitor has reportedly made the speaker’s divination more accurate; a fortune reading is offered in thanks.
14|The speaker invites the visitor to sit there.
18|The diviner is silent during the reading.
22|The captain-role speaker is silent.
26|There are ruins far inland from this town, deep in the desert; the speaker confidently predicts that the object sought is there.''',
316:'''104|Hodram proposes trying to advance for the time being.
144|Hodram insists on advancing even if they must cut a path through the trees.
174|The sailors appear fatigued.
179|Hodram orders a search for a way around.
214|Hodram judges moving in the present conditions dangerous and considers waiting until the fog clears.
243|A silent system-panel pause.
247|A further, visibly longer silent system-panel pause.
254|Exactly one day passes.
258|Hodram judges that the fog seems clear and orders departure.''',
317:'''63|Hodram exhales at the humidity and worries about the party’s exhaustion.
89|Hodram says it is darker than expected, trailing off.
93|The dynamic208 companion hesitantly addresses the admiral.
108|Hodram dismisses the concern and orders continued movement.
113|The captain-role speaker reacts in surprise to the feel of something, leaving its identity unfinished.
116|The dynamic208 companion warns the admiral of a huge snake and cries out about a party member, without completing the description of what happens.
127|Samwell panics, names an Indian python and then privately questions the identification; retain the comic uncertainty.
133|Hodram recognizes the danger and orders everyone to retreat.
141|A sailor appears injured; no death or precise injury is stated.
147|Hodram asks where they are now, after a pause.
176|Hodram decides to light a fire or flame, trailing into the action; no torch or lamp is named.
180|Hodram exclaims, asks whether the creatures are bats and remarks on the very large swarm.
206|Hodram orders the party to ignore the distraction and continue forward.
214|The sailors appear fatigued.''',
318:'''12|The guide first asks the party to obtain the map leading to the ruins.
44|The guide hesitantly reveals that the map apparently places the ruins somewhere other than this island.
48|Hodram reacts with sharp surprise.
54|The guide says crossing the sea is necessary.
59|Hodram concludes they should return to the port.
63|The guide says a small boat is already prepared and plans to continue in it; propulsion is not stated.
66|The guide says only the visitors’ group is qualified and requests that sailors not learn the ruins’ location.
75|Exactly one day passes.
79|The guide announces arrival and proposes continuing overland from there.
82|Rafael gives a surprised, slightly hesitant reaction.
94|Hodram recognizes Rafael of the Castor company and asks why he is here; no family or new command relationship is added by kun.
100|In an alternative recognition state, Hodram asks who the other person is.
109|Rafael says the person with Hodram asked him to search for the ruins, and that he lost his way en route.
114|Hodram dryly observes that Rafael too was among the indiscriminately recruited searchers; this echoes B287’s strong-looking-people remark.
117|The guide apologizes and says lack of word from the searchers led to joining the expedition personally; no searcher’s death is stated.
121|Rafael instead blames his own inadequacy, with an apologetic trailing reservation.
125|Hodram accepts the situation and proposes cooperating in the search.
128|The guide agrees.
132|Rafael agrees and invites them to search together.
136|The guide excitedly announces that the sought ruins have been found there.
165|Hodram says he is coming now.''',
319:'''5|Speaker206 warmly welcomes the visitor.
9|The speaker asks whether the visitor has been to a village far to the north in the New World.
13|According to a customer, a respected monk from this town once went to the northern continent to spread his faith.
17|The monk reportedly went missing after finding that village; the speaker wonders whether something happened.
21|Hodram gives a terse expression of uncertainty.
25|The monk was reportedly a very virtuous person; the speaker hopes those among whom he preached grew fond of him.
28|If the captain has occasion to travel north, the speaker asks him to inquire about the monk’s whereabouts.''',
320:'''5|The village resident remarks that the visitors look unfamiliar and asks where they are from.
8|Hodram identifies Sweden in northern Europe as his origin.
12|The resident has not heard of the place and concludes the visitors have come a great distance.
16|The resident thinks they must possess the useful instrument called a sextant and asks for confirmation.
20|Hodram reacts with surprise.
24|The resident has heard that the instrument reveals one’s position even at sea without landmarks, while leaving the account somewhat vague.
28|The resident asks the visitors to give them the sextant in exchange for something good.
31|Hodram repeats the promised good thing as a question.
35|The resident keeps the return gift a surprise until the sextant is brought.''',
321:'''6|The resident acknowledges that the sextant has been brought and offers this unnamed object in exchange.
14|The sextant is handed over; it is not received by the player in this result.''',
322:'''71|All available money is provided as initial funding; this is expenditure, not a received reward.
76|Exactly1000 gold coins are provided as initial funding in the other funding outcome.
83|A sailor announces that the investigation begins now and asks for a report to the Sofala guild; completion or success is not stated.''',
323:'''6|The resident asks whether this is what the party came to seek.
10|After a long wait, the resident says the awaited day has finally come; no number of years is given.
13|The resident decides to trust the visitors and asks them to accept the offered, unnamed object.''',
324:'''5|The village witness is surprised that the visitors know of the respected monk.
9|Hodram asks whether the witness knows him.
13|The monk could not bear the villagers’ suffering and nursed them devotedly; his care kept the village from being entirely wiped out.
16|Drinking the monk’s medicine quickly relieved the illness; the witness calls it a miracle.
20|Hodram asks whether the monk had medical knowledge.
24|The witness recalls the monk calling it alchemy, vaguely describing removal of mineral poison from the drinking water; retain the secondhand uncertainty.
28|The witness identifies the monk as the author of the book being shown.
39|In one conditional Lil response, she gives a startled cry and begins to suspect what the book is, leaving the thought unfinished.
58|In another conditional Lil response, she recognizes it as the book Charles had mentioned and celebrates finally finding it.
65|In Charles’s conditional sequence, he exclaims at the Alchemy book and his surprise at finding it in such a place.
69|Hodram asks Charles what is wrong, after a pause.
73|Charles says he recently heard a rumor that a new experimental material had been discovered in the New World.
77|Charles had learned that the Alchemy book was needed to obtain that material, but leaves the explanation unfinished.
81|Charles insists that it is surely a clue to some precious metal and begins muttering about needing to learn how to use it; no particular metal is identified.
84|Hodram apologetically cuts him short because there is no time now for the explanation.
90|Hodram returns to asking where the monk is now.
94|The witness falls silent.
98|The dynamic208 companion gives a questioning reaction.
102|The monk fell ill like the villagers after drinking the local water; person-to-person contagion is not stated.
105|Despite his illness, the monk concealed it and distributed all his own medicine to the villagers.
109|The monk eventually died; the witness reveres him as a true messenger of God, without giving a formal canonized title.
112|The captain-role speaker is silent.
116|The witness asks whether the book may be entrusted to the visitors.
119|The captain-role speaker questions what entrusting it means.
123|The book contains secrets of an ore that no one has seen before.
126|The witness believes deposits of the ore must exist somewhere in the world.
129|The villagers seek someone to inherit the monk’s research and ask the party to search for the ore.
133|Hodram promises that he will definitely find it.
144|In Charles’s optional conclusion, he eagerly promises a thorough investigation.
148|Hodram dryly acknowledges Charles’s enthusiasm: if the new ore is found, he will give him fleet command in that region and freedom to research to his heart’s content. Preserve the explicitly supported command offer without importing a modern five-star rank.''',
}

# Each offset identifies one physical source string. Aliased style slots remain
# one physical editorial object and receive precisely the same source meaning.
STYLE={
(311,24):'''0|Politely warn the admiral that proceeding farther without a map is impossible.
40|Warn the admiral that going onward without a map is reckless.
82|Conversationally tell the admiral that without a map they do not know where to go.
132|Elegantly say that without a map they cannot tell how to proceed.
182|Bluntly say that they cannot go farther without a map.
220|In an older register, say that without a map they do not know where to go.
270|Youthfully tell the admiral that without a map they do not know where to go.
324|Formally say that advancing without a map is impossible.''',
(311,436):'''0|Politely observe that the forest is very dark.
28|Describe the forest as densely overgrown, trailing off.
46|Note that the forest is very dark even though it is daytime.
74|Elegantly remark that it is very dark inside the forest.
98|Bluntly observe that the forest is very dark.
118|In an older register, describe the forest as densely overgrown.
140|Youthfully say it is pitch-dark inside the forest, like nighttime.
172|Formally describe the forest as densely overgrown, trailing off.''',
(311,654):'''0|Hesitantly ask the admiral whether he hears something.
28|Conversationally ask the admiral whether he hears something.
52|Elegantly tell the admiral that something can be heard, with questioning intonation.
78|Bluntly alert the admiral that something can be heard.
102|In an older register, ask the admiral whether he hears something.
126|Youthfully tell the admiral that something can be heard, trailing off.''',
(311,838):'''0|A startled warning that a rock is coming from behind.
26|A startled cry to look behind, without naming the danger in this physical string.
44|A startled warning of a large rock behind them.
74|A shrill frightened cry to look behind.
96|A blunt startled warning of a rock behind them.
120|A youthful stammered shout to look behind.
138|Warn that a rock is falling toward them from behind.''',
(311,1124):'''0|Urgently announce a dead end.
20|A startled cry followed by discovering a dead end.
46|Exclaim that this route will not work because it is a dead end.
70|Bluntly shout that it is a dead end.
88|In an older register, say this is bad because the route is a dead end.
114|Youthfully lament that it is a dead end.''',
(311,1460):'''0|A questioning reaction to something noticed.
6|An elegantly surprised questioning reaction.''',
(311,1500):'''0|A long frightened scream.
18|A long shrill frightened scream.''',
(311,1578):'''0|Stammer a warning about a snake.
14|Urgently identify a huge snake.
28|Conversationally stammer that it is a snake.
46|Elegantly stammer that a snake is there.
68|A blunt stammered snake warning.
80|An older-register stammered snake warning.
96|A drawn-out youthful snake alarm.
116|Formally announce that this time the threat is a snake.''',
(311,1918):'''0|In relief, report that the rock rolled down the left-hand path.
34|Directly report that the rock rolled down the left-hand path.
68|Celebrate their luck because the rock rolled left.
104|Elegantly report that the rock went down the left-hand path.
130|Bluntly report that the rock rolled left.
156|In an older register, report that it rolled down the left-hand path.
190|Youthfully report that the rock went down the left-hand path.''',
(311,2220):'''0|Call the admiral’s attention to something over there.
24|Call the admiral’s attention to something there, with urgent emphasis.
50|In an older register, call the admiral’s attention to something over there.
74|Youthfully call the admiral’s attention to something over there.''',
(313,24):'''0|Politely warn the admiral that lacking a map will cause them to lose their way.
40|Directly warn the admiral that lacking a map will cause them to lose their way.
72|Conversationally warn the admiral that they will get lost without a map.
108|Elegantly warn the admiral that they will get lost without a map.
148|Bluntly warn the admiral that they will get lost without a map.
188|In an older register, warn the admiral that they will get lost without a map.
226|Youthfully warn the admiral that they will get lost without a map.
268|Formally warn the admiral that they will lose their way without a map.''',
(313,376):'''0|Politely remark that it really is hot.
18|Conversationally draw out the complaint about how hot it is.
34|Bluntly remark that it really is hot.
50|Give an older-register complaint about the heat.
60|Give a youthful groan and complaint about the heat.''',
(313,546):'''0|Stammer an urgent warning to the admiral about a group of scorpions.
28|A startled cry identifying a group of scorpions.
54|A shrill startled cry and stammered scorpion alarm.
80|Bluntly stammer a warning to the admiral about a very large number of scorpions.
112|In an older register, stammer a warning to the admiral about a group of scorpions.
140|A youthful frightened cry identifying scorpions.''',
(313,856):'''0|Report that the scorpions fled and praise the admiral’s dependability.
56|Exclaim that they fled and praise the admiral’s ability.
88|Conversationally report that they fled and praise how dependable the admiral is.
136|Bluntly report that they fled and praise the admiral’s dependability.
182|In an older register, report that they fled and praise the admiral’s dependability.
234|Youthfully report that they fled and give drawn-out admiration for the admiral.
278|Formally report that they fled and praise the admiral’s dependability.''',
(313,1252):'''0|Report that the scorpions fled and praise the admiral’s dependability in the alternate successful response.
56|Exclaim that they fled and praise the admiral’s ability.
88|Conversationally report that they fled and praise how dependable the admiral is.
136|Bluntly report that they fled and praise the admiral’s dependability.
182|In an older register, report that they fled and praise the admiral’s dependability.
234|Youthfully report that they fled and give drawn-out admiration for the admiral.
278|Formally report that they fled and praise the admiral’s dependability.''',
(313,1624):'''0|Urgently ask whether the admiral is all right.
28|Conversationally ask whether the admiral is all right.
50|Bluntly ask whether the admiral is all right.
74|A youthful urgent cry to the admiral, without a complete welfare question.''',
(313,1756):'''0|State that immediate treatment is necessary.
24|Urgently say first aid must be given quickly.
48|An alarm followed by the need for urgent treatment.
78|Bluntly say first aid must be given quickly.
100|In an older register, insist that urgent treatment is necessary.
124|Formally insist that immediate treatment is necessary.''',
(313,2118):'''0|Tell everyone they are setting out and repeatedly urge quiet, careful movement.
40|Directly tell everyone to go and repeatedly urge quiet movement.
80|Conversationally tell everyone they are leaving and repeatedly urge quiet movement.
118|Elegantly tell everyone they are leaving and repeatedly urge quiet movement.
158|In an older register, tell everyone to go and repeatedly urge quiet movement.
202|Youthfully call everyone to go and repeatedly urge quiet movement.''',
(313,2472):'''0|A sudden realization that something has gone wrong.
16|A startled cry.
24|A blunt exclamation that the situation is bad.
34|An exclamation on realizing an unfortunate mistake.''',
(313,2556):'''0|Stammer a welfare question and urge the injured person to hold on.
34|Directly ask whether the person is all right and urge them to hold on.
62|Conversationally stammer a welfare question and urge the person to hold on.
92|Bluntly call to the person, ask if they are all right and urge them to hold on.
126|In an older register, stammer a welfare question and urge them to hold on.
158|Formally stammer a welfare question and urge them to hold on.''',
(316,24):'''0|Politely warn that without a map they seem likely to get lost.
36|Directly warn the admiral that they will get lost without a map.
68|Conversationally warn the admiral that they will get lost without a map.
104|Elegantly say they think they will get lost without a map.
140|Bluntly warn the admiral that they will get lost without a map.
176|In an older register, warn the admiral that they will get lost without a map.
214|Youthfully ask the admiral to prepare a map.
240|Formally warn the admiral that they will lose their way without a map.''',
(316,348):'''0|Politely suggest setting out.
22|Ask whether they should get going.
40|Energetically suggest going.
56|Elegantly suggest setting out.
80|Bluntly propose setting out.
100|In an older register, cheerfully call for an energetic departure.
124|A youthful all-aboard style departure call, not an actual train reference.''',
(316,520):'''0|Politely observe that fog is developing.
20|Formally observe that fog is developing.
40|Conversationally observe that fog is developing.
56|Elegantly note that the weather has turned foggy.
76|Bluntly observe that the fog has become very thick.
96|Give an older-register observation that fog is developing.
114|Youthfully remark on how very foggy it is.''',
(316,754):'''0|Politely judge that the route appears to be a dead end.
26|A trailing realization that this is a dead end.
42|Conversationally lament finding a dead end.
66|Elegantly observe that it is a dead end, trailing off.
82|In an older register, judge that this appears to be a dead end.
108|Youthfully lament finding a dead end.
132|Formally express mild surprise at finding a dead end.''',
(316,1010):'''0|Agree to try the captain’s instruction.
14|Politely propose giving it a try.
32|Conversationally complain that the instruction is reckless or absurd, then agree to try.
72|Elegantly agree to try.
86|Bluntly embrace continuing all the way.
112|In an older register, complain that the captain asks too much but agree to try for now.
152|Youthfully complain that it is absurd, then resolve to go anyway.''',
(316,1310):'''0|Excitedly report finding a fork in the path to the admiral.
30|Directly report finding a fork in the path to the admiral.
58|Conversationally say that looking carefully reveals a fork in the path.
94|Elegantly tell the admiral that a path leads this way.
122|Bluntly tell the admiral that a path leads this way.
150|In an older register, suggest they seem able to advance this way.
182|Youthfully call the admiral over this way.
210|Formally express surprise at a path being here.''',
(316,1634):'''0|Agree that the captain’s proposed course seems better.
28|Conversationally agree that this is the good choice.
42|Elegantly agree that this is the good choice.
56|Bluntly agree and propose doing that.
78|In an older register, judge that there is no other choice.
104|Youthfully agree and propose doing that.
126|Formally judge that this course is safer.''',
(316,1916):'''0|Politely report that the destination is coming into view.
18|Conversationally report that it is coming into view.
32|Directly report that it is coming into view.
46|Youthfully report that it is coming into view with questioning intonation.''',
(317,24):'''0|Warn the admiral that wandering aimlessly through such a jungle is dangerous.
52|Conversationally insist that wandering aimlessly through such a jungle is impossible.
106|Elegantly warn that wandering aimlessly through such a jungle is dangerous.
156|Bluntly refuse the prospect of wandering aimlessly through such a jungle.
214|In an older register, warn that wandering aimlessly through such a jungle is dangerous.
266|Youthfully warn that walking through such a jungle without even a map is dangerous.
326|Formally warn that wandering aimlessly through such a jungle is dangerous.''',
(317,446):'''0|Casually ask whether they should set off.
16|Politely suggest going.
36|Energetically call for an enthusiastic start.
62|Elegantly suggest going.
84|Bluntly call for departure.
100|Give an older-register departure call.''',
(317,654):'''0|Observe with surprise that a cave exists in such a place, trailing off.
24|Youthfully express surprise at finding a cave.''',
(317,1114):'''0|After hesitant pauses, admit uncertainty but judge that they seem near the ruins.
46|After pauses, cautiously judge that they are near the ruins.
76|Conversationally hesitate over the location, admit uncertainty and ask whether they may be near the ruins.
142|Elegantly hesitate and judge that they seem near the ruins.
180|Bluntly react in surprise and ask whether this is near the ruins.
230|In an older register, react in surprise, think and conclude they seem to have emerged near the ruins.
286|Youthfully hesitate over the location, admit confusion, guess they are near the ruins and celebrate their luck.
370|Formally ponder the location and judge that they seem near the ruins.''',
(317,1648):'''0|Urgently warn that there are too many bats.
18|Conversationally lament that there are too many bats.
38|Give a shrill cry and tell the admiral that this number is not normal.
82|Bluntly warn that there are too many bats.
100|In an older register, tell the admiral that advancing while dealing with so many bats is impossible.
170|Youthfully scream at the bats and recoil from how creepy they are.''',
(317,1974):'''0|Celebrate the admiral’s success and having escaped the jungle.
44|Urgently announce that they have made it out of the jungle.
66|Conversationally celebrate with the admiral that they have escaped the jungle.
102|Elegantly express relief at having escaped the jungle.
132|Bluntly celebrate with the admiral that they have escaped the jungle.
168|In an older register, celebrate having escaped the jungle.
202|Formally celebrate with the admiral that they have managed to escape the jungle.''',
(317,2252):'''0|Politely tell the admiral that they appear to have reached the ruins.
28|Conversationally identify this as the ruins to the admiral.
50|Elegantly identify this as the ruins to the admiral.
70|Bluntly identify this as the ruins to the admiral.
92|In an older register, tell the admiral that they appear to have reached the ruins.
120|Youthfully identify the ruins to the admiral.
142|Formally tell the admiral that they have finally reached the ruins.''',
(318,96):'''0|Politely express disbelief that an ancient city once existed in such a place.
56|Trail off in surprise at an ancient city having existed in such a place.
92|Conversationally marvel that an ancient city existed in such a place.
128|Elegantly marvel that an ancient city once existed here, trailing off.
166|Bluntly marvel that an ancient city existed in such a place, trailing off.
208|In an older register, find it hard to believe an ancient city existed in such a place.
266|Youthfully marvel that even such a place once had a town; this source variant does not explicitly say ancient city.
310|Formally marvel that an ancient city existed in such a place, trailing off.''',
(318,1420):'''0|Politely tell the admiral that the ruins have been found.
28|Conversationally tell the admiral that the ruins have been found.
54|Elegantly identify the ruins over there to the admiral.
74|Bluntly judge that the ruins seem to have been found.
104|In an older register, judge that the ruins seem to have been found.
134|Youthfully identify those as the ruins to the admiral, with confirming intonation.
166|Formally judge that the ruins seem to have been found.''',
(322,8):'''0|Announce that the survey party will now be disembarked.
26|Conversationally announce disembarking the survey party.
48|Bluntly announce disembarking the survey party.
70|In an older register, announce disembarking the survey party.
90|Youthfully draw out the announcement that the survey party is being disembarked.
112|Formally announce that the survey party will now be disembarked.''',
}

CAPTIONS={(311,1086):['Take the left path.','Take the right path.'],
    (311,1306):['Choose the brush on the left.','Choose the brush on the right.'],
    (313,782):['Deal with the scorpions by force.','Drive the scorpions off.','Flee from the scorpions.'],
    (316,674):['Advance despite the fog.','Wait for the fog to clear.'],
    (316,934):['Continue despite the dead end, cutting through if needed.','Search for a way around.'],
    (317,764):['Feel the way forward in darkness.','Light a fire for illumination; no specific torch or lamp is named.']}

def parse(text):
    values=[line.split('|',1) for line in text.strip().splitlines()]
    out={int(k):v for k,v in values};assert len(out)==len(values)
    return out

def main():
    assert not ORDINARY.exists() and not OUT.exists()
    scope,packet,styles,menus=map(load,[SCOPE,PACKET,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json'])
    assert scope['total_editorial_objects']==400 and scope['source_key_overlap_with_completed_credit']==0
    assert (styles['object_count'],styles['physical_alternatives'],styles['style_alias_slots'])==(38,236,304)
    assert (menus['object_count'],menus['caption_count'])==(6,13)
    assert {(o['block'],o['offset']) for o in styles['objects']}==set(STYLE)
    style_meanings={k:parse(v) for k,v in STYLE.items()}
    for key,meanings in style_meanings.items():
        rows=[r for r in styles['records'] if (r['block'],r['source_command_offset'])==key]
        obj=next(o for o in styles['objects'] if (o['block'],o['offset'])==key)
        offsets={r['source_reference']['offset']-(obj['offset']+20) for r in rows}
        assert offsets==meanings.keys(),(key,offsets,meanings.keys())
        assert sorted(i for r in rows for i in r['source_style_indices'])==list(range(8))
    seal(PACKET,ORDINARY,MEANINGS,CONTEXT,Path(__file__))
    ordinary=load(ORDINARY)['records'];assert len(ordinary)==151
    rows=[]
    for original in ordinary:
        row=deepcopy(original);row.update(exchange_context=CONTEXT[row['block']],source_only_not_final_English=True);rows.append(row)
    for original in styles['records']:
        row=deepcopy(original);key=(row['block'],row['source_command_offset'])
        meaning=style_meanings[key][int(row['id'].rsplit('_',1)[1])]
        row.update(source_meaning=meaning,exchange_context=CONTEXT[row['block']],
            personality_voice_notes=[dict(source_index=i,source_meaning=meaning) for i in row['source_style_indices']],
            same_source_aliases_not_assigned_invented_characters=True,source_only_not_final_English=True);rows.append(row)
    for original in menus['records']:
        row=deepcopy(original);row.update(source_meaning=CAPTIONS[(row['block'],row['source_command_offset'])][row['source_index']],
            exchange_context=CONTEXT[row['block']],source_only_not_final_English=True);rows.append(row)
    assert len(rows)==400 and len({r['id'] for r in rows})==400
    save(OUT,dict(records=rows,records_count=400,ordinary_speeches=151,physical_personality_alternatives=236,typed_captions=13,
        complete_exchange_contexts=CONTEXT,source_meanings=400,remaining_meanings=0,English_drafts=0,current_story_English_compared=0,
        all_source_meanings_read_as_complete_exchanges_before_existing_English=True,
        no_current_English_dialogue_consulted_for_eligible_records=True,source_first_not_new_editorial_completion_credit=True,
        source_names_are_clean_metadata_not_native_consumer_orfinal_localization_approval=True,
        linked_clean_B287_recruitment_context_read_without_reopening_credited_English=True,
        explicit_source_selector0_preserved_in_B314_andB318=True,final_item_names_andplace_terms_require_scoped_binding=True,
        all_five_review_gates_pending=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [PACKET,SCOPE,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',ROOT/'clean_name_fields.json',Path(__file__)]}))
    print('Sealed400 clean meanings across14 complete blocks; no eligible current English consulted and no new credit.')

if __name__=='__main__':main()
