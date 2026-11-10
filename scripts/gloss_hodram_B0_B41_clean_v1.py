"""Seal all residual clean SC1 meanings before eligible existing-English intake."""
from copy import deepcopy
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_only_gloss_v1 import seal

ROOT = Path('work/Hodram_B0_B41_clean_20261107')
PACKET = ROOT/'clean_source_packet.json'
ORDINARY = ROOT/'all341_ordinary_clean_meanings_v1.json'
OUT = ROOT/'all394_clean_meanings_before_English_v1.json'

CONTEXT = {
0:'An Indian-tradition book prompts a hypothesis about Sera’s homeland. Hodram immediately questions that hypothesis because India is too far from Ottoman territory. Preserve speculation and the counterargument; do not establish her origin as fact.',
1:'The samurai reacts to Muramasa with awe at its eerie, almost absorbing gleam. This is an impression, not an enacted supernatural effect or proof of possession.',
2:'Gerhard recognizes a recovered object’s unchanged dull gleam and marvels that no one picked it up. Its identity is not spoken here; do not supply an unqualified item name.',
3:'Aziza rallies her pirates against FO and distributes command, maneuvering and cannon tasks among Snake, Angel and Dandy. Hodram identifies pirates and orders readiness despite Gerhard’s observation that their leader appears female. Preserve the foe-faction substitution and her confidence without inventing sexual excitement or a relationship.',
4:'Two conditional Aziza encounter openings: finally finding the target and demanding a resolution, or recognizing returning opponents and threatening FO with sinking. They are alternatives, not consecutive encounters.',
5:'Hodram confronts the intoxicated guild target addressed as ジュリアン・フェルメール over betraying his homeland for money. The target dismisses patriotism and threatens interference. Preserve hiccup/drinking sounds and contempt without making drunken speech incomprehensible.',
6:'Hodram accuses the target addressed as プレット・ペロー of repeated wrongdoing and murder. The target counters that Hodram cannot be wholly innocent. Hodram rejects this defense and attacks. The judgments belong to the speakers.',
7:'Gerhard demands that ジャン・ラムジオ stop illicit trade and surrender. The target asks for evidence; Hodram responds with the dirty-laundry/dust idiom and a forceful threat, followed by the target’s death threat. Do not turn the taunt into a genuine evidentiary finding.',
8:'Hodram confronts ジャコブ・ポルトゥント over lucrative smuggling. The target resents being lectured. Preserve the smugglers’ profit metaphor naturally.',
9:'Hodram challenges エルナン・ベリオ as a skilled opponent. The target boasts that everyone now flees, complains of boredom and accepts. Keep the reciprocal swagger.',
10:'Hodram attacks イスカル・ヤサール under royal orders. The target recognizes FA as an admiral and welcomes a worthy opponent. Do not add a royal name, nation or extra military rank.',
11:'A screeching opponent threatens sinking repeatedly; Gerhard announces his appearance and Hodram acknowledges the danger. Preserve manic cries and repetition without diagnosing illness or inventing an animal identity.',
12:'A victorious Barbarossa dismisses the opponents for now, demands Caribbean renown before another challenge and threatens pursuit to the world’s end if they reappear in the southern Mediterranean. Do not soften the threat or broaden the first location.',
15:'A complete captive-liberation and Sera discovery sequence, with alternate companions and FE narration/embedded unnamed-girl labels. One grounded ship is abandoned after the foe withdraws without deep pursuit. Hodram encounters a knife-wielding captive, tentatively infers aspects of her origins and social background, fails to communicate, frees willing captives and offers an unspecified better weapon. He accepts her freedom to refuse; she nods. Preserve tentative personal assumptions as assumptions, the offered weapon’s unspecified identity, the language barrier and conditional reactions. Do not invent romance, kinship, confirmed religion/ethnicity or a confirmed home country.',
16:'After victory, Hodram’s strict ambition gives way to Manuel’s lament for those lost at sea and a three-part sea/mother poem. The poem reports an unnamed foreign language using the same sound and writing, then reflects on enduring bonds. Hodram and Gerhard praise it; Manuel wishes people could accept everything as the sea does. Retain grief, refrain and reported-language uncertainty without inventing a language or musical composition.',
17:'Aziza’s defeated crew mutinies over lost profits and her private pursuit of her father’s Bloodstained Shamshir. Hodram’s conditional companions intervene; Al is particularly concerned. The mutineers demand exactly 1,000,000 gold. After rescue, Aziza explains that she grew up as a pirate’s daughter, her father died in an accident and the sword vanished with him, and she realizes she wanted his keepsake more than pirate greatness. She renounces piracy and accepts Hodram’s invitation. Keep conditional participants, her emotional progression, familial facts and gratitude without inventing romance, her father’s murder, a debt contract or a forced crew roster.',
18:'Two Aziza retreat outcomes: a promise to settle things next time, or defiant introduction of her full name while retreating. Hodram responds with dismissal or a promise to remember. Keep the alternatives separate.',
19:'Two Hodram retreat outcomes with Aziza’s taunts. Gerhard discourages accepting provocation; Hodram elsewhere respects her naval-command-level ability. Preserve the comparison as appraisal, not an actual appointment.',
20:'The drunken guild target is restrained for escort to São Jorge and curses until his outburst is cut off. Do not add a sentence, execution or unexplained injury.',
21:'Hodram orders the murderer bound securely and taken to Hangzhou. The prisoner complains of pain and claims remorse. Do not treat the claim as proven rehabilitation.',
22:'Hodram comments on the Basra guild’s difficulty with the illicit trader. The trader claims the area would be worse without him; Gerhard condemns the rationalization. Keep the self-serving claim separate from established fact.',
23:'The smuggler laments lost cargo. Hodram identifies it as stolen and tells him to worry about being taken to Calicut instead.',
24:'The boasting fighter claims he deliberately lost. Hodram will hand him to the Athens guild and orders quiet until then.',
25:'The royal target refuses to accept defeat and cries out. Hodram ends the mission and orders return to Stockholm to report to the sovereign. A dynamic companion finds an object aboard the enemy vessel; Hodram tentatively calls it loot and doubts it is merely a decorative plate. Do not name the object or infer death from the cry alone.',
26:'Two source utterances embedded in conditional pirate-fleet logic: Gerhard expects an anticipated person to appear soon; Hodram orders further pirate-fleet destruction in the same fashion. Do not infer a single continuous moment or identify the unnamed expected person without linked source context.',
27:'The screeching target repeats a curse; Hodram wants the Havana guild to take him off their hands quickly. The curse is spoken anger, not proof of magic.',
28:'Hodram expresses relief at finally defeating the target. Seven physical voice alternatives, sharing eight style slots, urge reporting promptly to the Malacca guild. Keep the destination and urgency through each voice.',
29:'Complete first sea-battle/tutorial exchange. Manuel recognizes Speyer’s Hanseatic cog; Gerhard notes limits on policing outside their own waters. The other fleet fires before answering the formal request to stop over suspected territorial intrusion. Hodram orders battle, Charles explains crossing the T and takes charge of gunnery, and FE notices instruct normal heading/sail controls, automatic fire in range, X-menu Deck access, battle-role assignments and automatic boarding at contact. Gerhard requests the marine post as boarding leader. Preserve tutorial mechanisms and UI terms after source-bound term qualification; do not add manual-fire buttons, an automatic steering mode, a different T maneuver or an invented firing cooldown.',
30:'Barbarossa encounter with ordinary/allied openings, Gerhard’s identification and eight dynamic warnings about the enormous fleet. The two-choice menu offers battle or withdrawal. Barbarossa threatens annihilation if challenged or praises withdrawal before further threats. His inherited Barbarossa name is described; do not treat every full-name component as a title or generalize the port man into a guildmaster.',
32:'Maldonado encounter: dynamic reports identify his fleet and numbers, he disparages Europeans from the margins of Europe, and Hodram rallies the crew. Apparent reinforcements from behind prompt conditional despair before their Escante flags are recognized. Two alternative allied speakers offer help and conditional companions express relief. Preserve the turn from fear to relief, optional speakers and distinct reinforcement source; no automatic betrayal or guaranteed battle result.',
33:'Escante praises FA and proposes retaining their existing agreement against troublesome English pirates. Gerhard privately urges acceptance because Espinosa in Africa is acting seriously and must be dealt with promptly. Accept/refuse branches receive different responses. Do not turn the agreement into an unconditional merger or vow of allegiance.',
34:'An opponent laughs at the audacity of an open challenge and wants entertainment. A conditional rough companion retorts that the opponent will lose and offers a wager. Preserve swagger without supplying an unstated sum.',
35:'An antagonistic Muslim speaker condemns successive nonbelievers and claims Indian Ocean routes for Muslims. Preserve this character’s religious antagonism and territorial claim as his speech, not neutral narration or a newly invented historical fact.',
36:'An antagonist infers that the Ming have hired southern foreigners and threatens anyone obstructing him. Preserve that cultural insult in its setting without inventing a named nationality, ethnicity or employer contract.',
37:'Gerhard identifies a slave ship; Hodram says human trafficking should be prohibited. Gerhard urges patrol action. A two-choice menu orders attack preparation or questions authority; Gerhard argues that the guilty vessel is a legitimate target regardless of pretext. Hodram orders an attack just before its port arrival; Charles is eager. Preserve the game characters’ claims and the jurisdiction objection, not a newly asserted universal historical statute or a new humanitarian speech.',
38:'Camille identifies Lil’s fleet; Lil believes Maria has attacked her. Camille reveals Coen’s disguised fleet and plan to pit them against each other, citing Maria’s warning. Hodram checks the report, targets the unidentified fleet and fires. The conspirators recognize FO and withdraw; Lil realizes her mistake. Preserve Maria/Camille approved names, the ruse, the full spoken Maria name for later qualification, native FO and each actor’s actual assignment. Do not turn Lil’s initial accusation into fact or make Maria an on-scene speaker.',
39:'An enemy fleet appears and its leader disparages southern foreigners while invoking Yamato spirit. Conditional companions react to the unfamiliar vessels; Hodram identifies iron-clad ships and optional Aziza is amazed. Keep the ship construction as spoken, not a modern steam ironclad classification.',
40:'Pasha’s ambush surrounds Hodram with many fleets. Hodram mocks the motley force and Pasha threatens public execution, but unexpected fire comes from town batteries apparently seized by someone else. Two foreign-language cries remain semantically opaque. Pasha orders one or two subordinate fleets to answer the fire while withdrawing; Hodram taunts him into replying. Preserve alternative subordinate orders, uncertain battery takeover, native FA and unintelligible cries without inventing the rescuers’ exact words or replacing a personal name with an unqualified rank.',
41:'Seven physical dynamic lookout voices announce a monstrous fish appearing, sharing eight style slots. Preserve fear, urgency and differing formality. Do not identify a species, whale, kraken or particular named crew member from the generic selector.',
}

MEANINGS = {
0:'''6|Gerhard tentatively identifies the book as a record of ancient Indian traditions.
9|Hodram asks whether that would mean Sera’s homeland was an Indian-related kingdom.
12|He immediately objects that India is much too far from Ottoman territory.''',
1:'''6|The samurai marvels that this is the blade called Muramasa, with its ominous epithet.
10|He says its eerie gleam feels as though it could draw someone in.''',
2:'''6|Gerhard recognizes precisely the same dull gleam, little changed since he parted with the object.
10|He marvels that it survived without anyone picking it up; the utterance trails off.''',
3:'''6|Aziza points out FO’s fleet as the one encroaching on their territory.
9|Her sailors cheer their assent.
13|She orders everyone to battle stations and tells Snake to take command.
16|Snake gives a rough affirmative.
20|She tells Angel to move their ship to the enemy’s right rear.
23|Angel responds with exuberant, rough readiness.
26|She asks Dandy whether the cannon preparations are complete.
29|Dandy answers formally that they are ready.
33|Aziza laughs softly, thrilled, and rallies her men.
36|She says they will now decide whether she or FO deserves to rule this sea.
39|The sailors cheer loudly.
43|Hodram recognizes the other fleet as pirates.
47|Gerhard observes that the leader appears to be a woman.
51|Hodram says being a woman does not change that she is a pirate, and orders battle preparations.
55|Gerhard acknowledges.''',
4:'''43|Aziza says she has finally found them and will settle matters this time.
46|Her sailors cheer.
52|In the alternate opening, Aziza calls FO’s returning people incorrigible and threatens to send them to the sea’s depths this time.''',
5:'''5|Hodram orders the vessel to stop and asks whether its man is ジュリアン・フェルメール.
8|The man hiccups drunkenly and asks what of it.
11|Hodram says betraying one’s homeland for money is unforgivable.
14|The man drinks, exhales and sneers that homeland has nothing to do with making money; he threatens anyone obstructing his work.''',
6:'''5|Hodram identifies プレット・ペロー, says his face suggests much wrongdoing and refuses to leave a murderer at large.
8|The target resents his self-importance and says Hodram cannot have lived entirely without wrongdoing either.
11|Hodram concludes the man can only do wrong, says restraint is unnecessary and attacks.''',
7:'''5|Gerhard addresses ジャン・ラムジオ and demands he immediately stop illicit trade and surrender.
8|The target questions the accusation and asks whether they have evidence.
11|Hodram calls his very existence evidence, invokes dirt emerging if he is shaken and threatens to shake it out by force.
14|The target calls them unreasonable and offers to help them die if that is what they want.''',
8:'''6|Hodram identifies ジャコブ・ポルトゥント and says his profitable smuggling ends today.
9|The target indignantly rejects being lectured by someone like Hodram.''',
9:'''5|Hodram offers to fight エルナン・ベリオ, saying a skilled opponent should be a welcome change.
9|The target says it has been a long time since someone challenged him because everyone flees at full speed; great strength has its drawbacks.
12|He accepts, saying he too has long been bored.''',
10:'''7|Hodram identifies イスカル・ヤサール and announces an attack under royal orders, telling him to prepare.
11|The target recognizes Admiral FA and says he is a worthy opponent before attacking.''',
11:'''6|The screeching target asks who they are and whether they want to die, stretching the sounds grotesquely.
9|Gerhard says the target has finally appeared.
13|Hodram agrees this is indeed a dangerous opponent.
17|The target screeches and repeats three times that he will sink them.''',
12:'''5|Barbarossa laughs, asks whether they have learned their lesson and says he will let the matter rest at this much for now.
8|He says anyone seeking to defeat him must at least make a name in the Caribbean first.
12|He forbids another appearance in the southern Mediterranean, threatening pursuit to the world’s end and destruction if he sees them again.''',
15:'''11|Hodram orders all prisoners released.
17|Hodram curses in frustration.
21|Gerhard reports that the foe is withdrawing quickly without pursuing far, then notices something.
25|He reports one grounded ship.
29|Hodram infers it was abandoned and orders its interior checked.
35|Gerhard hesitantly calls the admiral over.
39|Hodram asks what is wrong.
43|Gerhard says they found someone who seems out of place aboard this ship.
46|Hodram reacts questioningly.
50|Gerhard says the person is this way.
56|FE narration likens the encountered person to a doll.
60|FE narration marks sudden shock.
64|Gerhard urgently cries out to the admiral about the woman; the thought is interrupted.
67|Hodram orders him to wait, grunts and says she seems to mistake him for a pirate or something similar.
73|FE shows silence.
77|Hodram says her reaction is understandable and reassures her that she is now free.
80|FE shows another silent response.
84|Hodram tentatively remarks that her features seem different from other African peoples.
87|Judging by her clothing, he doubts she is Muslim and speculates that she comes from a distinguished family.
91|FE shows silence again.
95|Hodram realizes they cannot communicate verbally.
107|Gerhard asks what to do, since they cannot return her without knowing where she was taken from.
113|Alternate Manuel asks the same practical question in his more conversational manner.
120|Hodram asks about the other captives.
130|Gerhard reports that all seem to want to be released where they are.
135|Alternate Charles reports the same desire for immediate release.
141|Hodram acknowledges that the captives cannot readily trust his people either and grants immediate release to everyone who wishes it.
151|Gerhard acknowledges the order.
157|Alternate Charles acknowledges it.
164|Hodram tells the girl she too may do as she likes; her knife will not protect her well in future, and he offers her an unspecified object.
168|The embedded foreign-girl label accompanies a startled questioning response.
171|Gerhard warns that giving her a weapon is dangerous because she might attack again.
175|Hodram says that if she wants to cut him, she may.
179|Gerhard protests by calling to his admiral.
183|The foreign girl gives an alarmed or emphatic silent reaction.
194|Conditional Manuel reacts with startled confusion.
201|Conditional Gerhard warns of danger.
205|The foreign girl is silent.
208|Hodram asks whether she does not want it.
212|The foreign girl nods in affirmation of that question.
215|After silence, Hodram gives a small amused exhale and accepts her answer.
226|Conditional Manuel privately expresses how startled he was.
233|Conditional Gerhard privately exhales in relief.''',
16:'''6|Gerhard remarks that they won.
10|Hodram says this much is expected of someone aiming to command the strongest fleet.
13|Gerhard remarks that he remains demanding.
17|Manuel mourns people who vanished into the sea, then reframes it as returning to the mother sea.
21|Hodram addresses Manuel with concern or attention.
25|Manuel proposes consoling the spirits of those who died.
28|Hodram reacts questioningly.
32|The poem likens sea and mother: familiar recurring ripples seem to awaken the now-distant memory of a mother’s heartbeat.
35|The refrain likens sea and mother again and reports that in a foreign land they may be expressed with the same sound and the same writing.
39|The final refrain places sea and mother within bonds that never disappear while one lives.
42|Hodram calls it a good poem, surprised that Manuel had such talent.
45|Gerhard agrees and expresses admiration.
49|Manuel says the sea accepts everything and wishes they could do the same.
52|Hodram falls silent.''',
17:'''6|Aziza acknowledges losing again, begins promising a next time and abruptly reacts.
9|Angel says apologetically but threateningly that she will have no next time.
12|Snake chuckles ominously.
16|Aziza demands that he repeat himself.
20|Angel asks whether she failed to hear.
24|He says no one there will follow her orders anymore.
27|Aziza curses and accuses them of betrayal.
30|Hodram observes a disturbance aboard the other vessel.
34|Gerhard reports that the woman pirate’s own followers appear to be surrounding her.
37|Hodram orders their ship brought closer.
41|Angel says their recent losses have earned no money and demands she take responsibility.
45|Aziza questions that demand.
49|Dandy asks why she keeps chasing FO around in the first place.
53|Snake says she has a reason she cannot tell everyone.
56|Aziza reacts in shock.
60|Snake says her true motive is recovering the Bloodstained Shamshir from FO because it is her father’s keepsake.
64|Aziza hesitates and denies that this was her intention.
68|Angel says she has been failing as a leader; no one wants a captain who earns no money, and she should prepare herself.
72|Gerhard warns Hodram that she will be killed if they do nothing.
76|Hodram says they cannot simply abandon her.
80|Al says he is going in.
84|Gerhard urgently warns him not to act rashly.
88|Snake tells the outsider to stay out of it.
91|Al tells the underlings not to get above themselves.
95|Angel says it is none of Al’s business and orders the others to dispose of both him and Aziza.
99|The samurai addresses Al respectfully and offers assistance.
103|Lil says she will fight too and condemns men who can only rely on superior numbers.
106|Charles proposes energetically blasting those people away.
110|Al challenges the pirates to come at him.
113|Aziza wonders why they are fighting for her when they were enemies moments before.
117|Angel curses and realizes the odds have turned against them.
121|Hodram says they have finally noticed.
125|Aziza addresses FI and FA as the admiral’s name, with a pause.
129|Snake asks whether Hodram has also come to save her.
133|Hodram asks what if he has.
137|Angel complains that everything is Aziza’s fault, yet they are suffering for it.
140|Hodram says they should be tired of complaining by now and suggests releasing her.
143|He asks whether they merely want Aziza gone.
146|Dandy notes that Hodram heard and says no one will follow her anymore.
149|Aziza is silent.
153|Hodram offers to take her into their care.
156|Aziza reacts with surprise.
160|Dandy refuses to hand her over for nothing.
164|Al indignantly questions demanding money.
168|Hodram restrains Al and asks the price of agreement.
171|Dandy demands exactly 1,000,000 gold.
176|Al tells Aziza to come with him.
180|Aziza is silent.
184|Angel says their business is done and bids them farewell roughly.
190|Aziza laments being betrayed by her crew, says she has fallen far and asks why they saved her.
193|Al says he could not leave her there.
197|Hodram says only a very inhumane person would refuse help in those circumstances.
200|The samurai asks why someone of her caliber has fallen into piracy.
204|Aziza says he overestimates her and she did not fall into it: she is a pirate’s daughter and her father was a pirate.
207|Hodram expresses interest.
211|Aziza says those pirates were her father’s men and she learned swordsmanship and piracy by imitating them as a child.
214|Gerhard asks what happened to her father.
218|She says he died in an accident; the sword was his treasure and disappeared with him.
222|Al identifies that sword as the Bloodstained Shamshir.
225|Aziza says she wanted to become a great pirate like her father and copied everything he did.
229|Learning they had the sword made her desperately want to obtain it, because then something would follow; she trails off.
232|Hodram reacts questioningly.
236|She thought it would prove she was closer to her father’s greatness, then laughs softly before qualifying that thought.
240|She admits realizing she really wanted her father’s keepsake more than she wanted to become a great pirate.
243|She considers abandonment understandable because she pursued something that brought no profit and thus angered the crew.
247|Al asks whether she still feels attached to piracy.
251|She says it was her father she pursued, not piracy, and she intends to leave the trade.
255|Al appeals to the admiral without spelling out the request.
259|Hodram says he understands Al and asks Aziza whether she will join his ship.
262|Aziza is grateful and promises to work hard because he saved her life.
266|She says they can simply call her Aziza.
269|The samurai says devotion to one’s benefactor is one way of life.
272|Hodram remarks that things will become lively again.''',
18:'''18|Aziza orders withdrawal for today and threatens to settle things next time.
21|Hodram dismisses her threat as empty talk she may indulge in.
27|In the alternate outcome she retreats for now but refuses submission and tells them to remember her full name, アズィーザ・ヌレンナハール.
31|Hodram says he will remember.''',
19:'''16|Hodram orders retreat for today.
20|Aziza taunts him for fleeing and being more cowardly than he looks.
23|Gerhard warns him not to rise to provocation.
27|Hodram says he knows and orders retreat.
33|Aziza notes that they escaped.
37|In another outcome Gerhard proposes withdrawing for now.
41|Hodram judges the pirate exceptional, with skill sufficient for a navy admiral.
45|Aziza mocks their expectation of winning and says to prepare for death at their next meeting.''',
20:'''9|Hodram orders compliance and says the prisoner must accompany them to São Jorge.
12|The prisoner curses, rejects being touched and has his next curse abruptly muffled or interrupted.''',
21:'''9|Hodram orders the prisoner bound securely and taken to Hangzhou.
12|The prisoner complains of pain and claims he is remorseful.''',
22:'''8|Hodram calls the man troublesome and understands why the Basra guild struggles with him.
11|The man pleads for leniency and claims the area would be in worse disorder without him.
15|Gerhard condemns the attempt to justify wrongdoing and calls him thoroughly contemptible.''',
23:'''9|The prisoner curses and laments his precious cargo.
12|Hodram says he should worry about being taken to Calicut rather than about stolen cargo.''',
24:'''9|The defeated fighter insists that he deliberately let them win.
12|Hodram says he will be handed to the Athens guild and must behave until then.''',
25:'''8|The opponent gives a pained cry, cannot accept that he lost and twice refuses recognition of defeat.
12|He gives another forceful pained cry.
16|Hodram declares the mission complete and orders return to Stockholm to report to the sovereign.
20|Dynamic companion208 announces finding something aboard the enemy ship.
26|Hodram tentatively identifies it as enemy loot, but doubts it is merely a decorative plate.''',
26:'''28|Gerhard says the awaited person ought to show themselves by now.
52|Hodram orders them to continue destroying pirate fleets one after another in the same way.''',
27:'''9|The target screeches in rage and repeats three times that he will curse them.
13|Hodram says they must have the Havana guild take him off their hands quickly.''',
28:'''5|Hodram says they have finally managed to defeat the target.''',
29:'''5|Manuel excitedly announces spotting the target.
9|Hodram asks whether it is Speyer’s ship.
13|Manuel identifies the Hanseatic cog design as unmistakable.
16|Gerhard says they cannot take enforcement action unless it is in their own country’s territorial waters.
19|Manuel is startled when the other ship suddenly fires.
22|Gerhard wonders what they intend and whether they have mistaken the fleet’s identity.
26|Hodram orders flag signaling.
30|Charles acknowledges and asks for the message.
34|Hodram dictates that the other fleet may have violated their territorial waters.
38|He requests that they stop so the circumstances can be investigated in detail.
41|Charles reacts with shock.
45|A sailor cries out in alarm.
49|Charles says it is no use: they do not seem willing even to look at the signals.
52|Hodram concludes the act is deliberate.
56|Gerhard says the foe intends to destroy them before trouble develops.
59|Hodram says there is then no need for restraint and orders all hands to battle readiness.
62|Speyer calls them a nuisance and orders his people to teach the hastily assembled inept fleet the terror of sea battle.
67|Hodram asks Charles for his tactical plan.
71|Charles recommends the standard T formation/tactic.
74|He proposes avoiding the enemy’s dangerous broadside range, going around to its bow or stern and pointing their own broadside toward it for a decisive volley.
77|Hodram approves and gives Charles complete responsibility for cannon fire.
81|Charles accepts; if Hodram maneuvers the vessel, he will direct the gunners.
85|Charles excitedly says it is finally time to test the new cannon’s power.
88|FE tutorial instructs controlling ship heading and sail orientation as during ordinary movement.
92|FE says cannon fire occurs automatically when the enemy vessel enters range.
95|Gerhard asks to be assigned to the marine post as boarding leader.
98|FE says navigator assignments should be changed for combat, using the Deck screen.
102|FE explains pressing X and selecting the Deck screen from the menu to display it.
106|FE says assignments to armed cannon stations, marine posts and the deck are useful in combat.
109|FE instructs selecting Gerhard and sending him to the marine post.
112|FE says ship contact automatically initiates boarding combat and Gerhard should excel as boarding leader.
116|Manuel urges the admiral to give the ship’s heading.''',
30:'''10|Barbarossa challenges the nearby fleet for approaching his territory and orders it out of the southern Mediterranean if it values its life.
13|Hodram identifies him as the formidable person mentioned by the port man.
16|Gerhard recognizes Barbarossa, confirming his suspicion.
19|Hodram asks whether he knows him.
23|Gerhard names バルバロッサ・ファーズル・ハイレディン and identifies him as an inheritor of the Barbarossa name associated with Algiers’ pirate chiefs.
26|Hodram judges him highly skilled from his appearance.
30|Gerhard agrees, calls him a monster figuratively and begins adding another point.
36|In the allied opening Barbarossa says alliance does not excuse intrusion and orders withdrawal from the southern Mediterranean.
40|Hodram again identifies the person mentioned by the port man.
43|Gerhard confirms that Barbarossa was indeed the subject.
81|On the battle branch Barbarossa laughs at their willingness to fight and threatens to kill them all without mercy.
88|On the withdrawal branch he laughs, calls it wise and says they need at least Caribbean renown before challenging him.
91|He forbids reappearance in the Mediterranean, threatening worldwide pursuit and destruction.''',
32:'''25|Maldonado tells his men to show these ignorant people from Europe’s fringes how things are done in the Caribbean.
55|Hodram orders them not to be intimidated, to do as they normally would and to prepare for battle.
81|Hodram reacts with surprise to the report of ships behind.
93|Conditional Manuel appeals to God.
106|A sailor despairingly says they cannot defeat so many.
111|Alternate Charles says logically they cannot defeat so many.
117|Hodram tells them to wait and asks about the flags.
132|One conditional ally says it is a fortunate meeting and offers reinforcement.
135|Hodram recognizes Escante’s forces.
145|A sailor expresses relieved rescue.
151|Alternate Manuel expresses the same relief.
163|Another conditional ally greets them casually, calls the meeting fortunate and offers help.
166|Hodram again recognizes Escante’s forces on this alternate branch.
176|A sailor expresses relief in that branch.
182|Alternate Manuel expresses relief in that branch.''',
33:'''5|Escante addresses FA, praises the performance and finds him dependable.
8|He says Maldonado is dealt with, but English pirates remain troublesome.
12|He asks whether their existing agreement can be maintained going forward.
15|Hodram is silent.
34|Gerhard privately says Espinosa in Africa has begun acting in earnest and must be dealt with urgently.
38|Hodram responds thoughtfully.
42|Gerhard privately advises accepting the offer for now.
63|After acceptance Escante says he looks forward to their continued achievements.
73|After refusal he expresses regret and hopes FA will not become an enemy.''',
34:'''6|The opponent laughs, admires the nerve of openly challenging him and demands a good fight for his amusement.
18|A rough companion calls him complacent and offers to bet that he will lose.''',
35:'''6|The speaker condemns the successive nonbelievers and claims the Indian Ocean routes for Muslims, with the source explicitly glossing the religious identity.''',
36:'''6|The speaker infers that the Ming hired southern foreigners, curses and threatens no mercy to obstructors.''',
37:'''6|Gerhard asks the admiral to look at something.
9|Hodram reacts questioningly.
13|Gerhard tentatively identifies a slave ship.
17|Hodram says human trafficking should be prohibited.
21|Gerhard says it is nonetheless still widespread and asks whether their patrol fleet can overlook it.
40|He argues that the foe has a guilty conscience, so whatever the pretext they have found a legitimate target to defeat openly.
43|Hodram considers the argument.
50|Hodram orders an attack exploiting the moment just before port entry and sends everyone to battle stations.
61|Charles chuckles and promises a spectacular attack.''',
38:'''6|Camille announces spotting Lil’s fleet.
10|Lil addresses Maria by her full spoken name and demands to know what grudge she has against her.
13|Hodram reacts with surprise to hearing Maria implicated.
17|Camille tells Lil that the fleet is Coen’s disguised force and warns her not to be fooled.
21|Lil recognizes Camille in surprise.
25|Camille says Coen’s scheme is to make Lil and Maria fight.
28|Lil questions the explanation and trails into confusion over what she thought she saw.
31|Hodram asks Camille whether this is true.
35|Camille says he knows Coen well and that Maria detected this plan and informed him.
39|Hodram accepts the explanation.
43|Hodram orders aiming at the unidentified fleet straight ahead.
47|Camille challenges Coen to reveal himself.
51|Hodram orders fire.
55|The dynamic gunner gives a forceful firing cry.
59|One adversary curses angrily.
63|Another recognizes FO, addresses Coen respectfully and warns that they are at a disadvantage.
66|Actor40 concludes this is as far as they can go and orders withdrawal; preserve the original actor assignment pending name binding.
70|Lil recognizes Coen and begins realizing what she has done or misunderstood.''',
39:'''5|A sailor reports an enemy fleet ahead.
9|The enemy disparages southern foreigners and vows to show them Yamato spirit.
21|Conditional Gerhard asks in shock what those ships are.
27|Alternate Manuel asks the same shocked question.
34|Hodram identifies ships clad with iron.
46|Conditional Aziza marvels that such vessels exist.''',
40:'''6|One ambusher orders them to stop.
11|Hodram reacts with surprise.
15|Another ambusher says regretfully or smugly that there is no escape.
19|Pasha laughs, addresses FA dismissively and declares that his heroic exploits end here.
27|Hodram says Pasha apparently has no intention of coexisting with him in the Mediterranean.
55|Hodram dismisses the force as a motley rabble and orders a breakthrough.
58|Pasha laughs at his insolence and asks whether he knows whom he is underestimating.
61|Hodram calls him an ill-mannered general.
65|Pasha announces a public execution for the presumptuous man and orders every ship to charge.
68|A sailor cries in alarm.
72|Pasha demands to know what happened.
76|A subordinate reports that the town is firing on them.
79|Pasha reacts in shock and demands an explanation.
82|Another subordinate does not know but says someone seems to have seized the town batteries.
88|Actor24 gives an opaque foreign-language cry represented by circles and crosses; its lexical meaning is not supplied.
92|Actor78 gives another opaque foreign-language cry represented by symbols; do not invent a translated command.
96|Hodram reacts in recognition or surprise at what he sees, without naming it.
100|A sailor gives a prolonged cry.
111|In one branch Pasha orders Mushari’s fleet to engage while he withdraws at full speed.
116|In another branch he orders both Mushari’s and Al-Najud’s fleets to engage while he withdraws at full speed.
125|Hodram mocks the abandoned public-execution threat and challenges Pasha to fight him.
129|Pasha grunts, accepts the challenge angrily and threatens a bloody end.''',
}

EXTRA = {
'SC1_B28_STYLE_36_0':'A polite, brisk companion proposes immediately reporting to the Malacca guild.',
'SC1_B28_STYLE_36_46':'A restrained companion says they must report to the Malacca guild promptly.',
'SC1_B28_STYLE_36_82':'An informal companion urges quickly reporting to the Malacca guild.',
'SC1_B28_STYLE_36_120':'A rough companion urges getting to the Malacca guild and reporting without delay.',
'SC1_B28_STYLE_36_166':'An elderly-voiced companion urges immediate reporting to the Malacca guild.',
'SC1_B28_STYLE_36_210':'A youthful companion urges quickly telling the Malacca guild.',
'SC1_B28_STYLE_36_254':'An affable, mature companion proposes going to report promptly to the Malacca guild.',
'SC1_B30_STYLE_662_0':'A polite companion exclaims at the huge fleet and says flight is safer.',
'SC1_B30_STYLE_662_54':'A restrained companion marvels at the immense fleet and says retreat is safer.',
'SC1_B30_STYLE_662_100':'A startled conversational companion asks whether they should flee from the huge fleet.',
'SC1_B30_STYLE_662_160':'An animated companion addresses the admiral and recommends fleeing the huge fleet.',
'SC1_B30_STYLE_662_206':'A rough companion exclaims at the enormous fleet and says flight is safer.',
'SC1_B30_STYLE_662_262':'An elderly-voiced companion calls the fleet immense and withdrawal the wiser course.',
'SC1_B30_STYLE_662_314':'A youthful companion exclaims at the number of ships, rejects the odds and urges flight.',
'SC1_B30_STYLE_662_362':'An affable mature companion remarks on the huge fleet and the safety of retreat.',
'SC1_B30_CHOICE_1100_0':'The player orders preparations for battle.',
'SC1_B30_CHOICE_1100_1':'The player chooses to withdraw for now.',
'SC1_B32_STYLE_10_0':'A formal lookout reports spotting Maldonado’s fleet.',
'SC1_B32_STYLE_10_38':'A conversational polite lookout reports finding Maldonado’s fleet.',
'SC1_B32_STYLE_10_78':'A forceful lookout announces spotting Maldonado’s fleet.',
'SC1_B32_STYLE_10_114':'A youthful lookout excitedly recognizes Maldonado’s fleet.',
'SC1_B32_STYLE_280_0':'A polite lookout urgently reports that he has brought a considerable force.',
'SC1_B32_STYLE_280_32':'A restrained lookout reports a considerable accompanying force.',
'SC1_B32_STYLE_280_58':'A conversational lookout urgently reports many accompanying ships.',
'SC1_B32_STYLE_280_88':'An animated lookout reports many accompanying ships.',
'SC1_B32_STYLE_280_114':'A rough lookout reports a considerable accompanying force.',
'SC1_B32_STYLE_280_144':'An elderly-voiced lookout remarks on a considerable accompanying force.',
'SC1_B32_STYLE_280_172':'A youthful lookout exclaims that there are many of them.',
'SC1_B32_STYLE_280_190':'An affable mature lookout reports a considerable accompanying force with urgency.',
'SC1_B32_STYLE_596_0':'A polite lookout warns the admiral that ships are also approaching from behind.',
'SC1_B32_STYLE_596_34':'A frightened lookout stammers a warning to the admiral that ships have come from behind too.',
'SC1_B32_STYLE_596_74':'A rough lookout warns the admiral of ships arriving from behind as well.',
'SC1_B32_STYLE_596_112':'A forceful lookout warns the admiral of ships arriving from behind as well.',
'SC1_B32_STYLE_596_146':'A youthful lookout cries in alarm at more ships appearing behind them.',
'SC1_B33_CHOICE_414_0':'The player agrees to retain the existing arrangement.',
'SC1_B33_CHOICE_414_1':'The player refuses the offer.',
'SC1_B37_CHOICE_216_0':'The player orders attack preparations.',
'SC1_B37_CHOICE_216_1':'The player questions whether intervention would exceed their authority.',
'SC1_B40_STYLE_284_0':'A polite companion stammers that they are surrounded by an enormous number of fleets.',
'SC1_B40_STYLE_284_46':'A restrained companion reports encirclement and then stammers at the immense number of fleets.',
'SC1_B40_STYLE_284_88':'A startled conversational companion cries out and stammers that they are surrounded by immense forces.',
'SC1_B40_STYLE_284_144':'An animated companion reacts questioningly to the encirclement and stammers over the great fleet numbers.',
'SC1_B40_STYLE_284_188':'A rough companion stammers that they are surrounded by an enormous number of fleets.',
'SC1_B40_STYLE_284_232':'An elderly-voiced companion stammers at the encirclement and great fleet numbers.',
'SC1_B40_STYLE_284_276':'A youthful companion says they have been surrounded and there are very many enemies.',
'SC1_B40_STYLE_284_316':'An affable mature companion stammers over encirclement and great fleet numbers.',
'SC1_B41_STYLE_10_0':'A polite lookout urgently addresses the admiral and announces a monstrous fish appearing.',
'SC1_B41_STYLE_10_36':'A youthful lookout cries out that a monstrous fish is there.',
'SC1_B41_STYLE_10_62':'A frightened, feminine-voiced lookout cries out, stammers that it has appeared and identifies a monstrous fish.',
'SC1_B41_STYLE_10_104':'A rough lookout urgently tells the admiral that a monstrous fish has appeared.',
'SC1_B41_STYLE_10_140':'An elderly-voiced lookout stammers to the admiral about a monstrous fish.',
'SC1_B41_STYLE_10_166':'An exuberant or frightened youthful lookout gives a prolonged cry announcing a monstrous fish.',
'SC1_B41_STYLE_10_200':'An affable mature lookout addresses the admiral and reports a monstrous fish appearing.',
}


def main():
    assert not OUT.exists()
    seal(PACKET, ORDINARY, MEANINGS, {n:CONTEXT[n] for n in MEANINGS}, __file__)
    ordinary, styles, menus = map(load, (ORDINARY, ROOT/'clean_style_objects.json', ROOT/'clean_choice_objects.json'))
    assert len(ordinary['records']) == 341 and len(styles['records']) == 47 and len(menus['records']) == 6
    extra = styles['records']+menus['records']
    assert {r['id'] for r in extra} == set(EXTRA) and len(extra) == 53
    rows = deepcopy(ordinary['records'])
    for original in extra:
        assert original['earlier_English_unconsulted']
        rows.append({**deepcopy(original), 'source_meaning':EXTRA[original['id']],
            'whole_exchange_context':CONTEXT[original['block']],
            'source_read_with_all_previous_andfollowing_speeches_in_block':True,
            'clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending':True})
    assert len(rows) == len({r['id'] for r in rows}) == 394
    save(OUT,dict(records=rows, records_count=394, ordinary_speeches=341,
        physical_personality_alternatives=47, typed_caption_records=6,
        complete_blocks=sorted(CONTEXT), source_contexts=CONTEXT,
        all_source_meanings_read_as_complete_exchanges_before_existing_English=True,
        source_gloss_not_final_English=True, all_five_editorial_gates_still_pending=True,
        independent_drafts_pending=True, scoped_names_andterms_pending=True,
        tutorial_priority_blocks=[29], new_credit=0, full_goal_complete=False,
        evidence={str(p):digest(p) for p in (PACKET,ORDINARY,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',Path(__file__))}))
    print('Sealed 394 source meanings in 39 complete exchanges; existing English unconsulted; no new credit.')


if __name__ == '__main__':
    main()
