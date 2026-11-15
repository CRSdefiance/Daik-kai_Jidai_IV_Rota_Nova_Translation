"""Complete the394 contextual decisions, preserving the32 saved tutorial rows exactly."""
from collections import Counter
from copy import deepcopy
from pathlib import Path

from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT
from scripts.draft_hodram_B0_B41_clean_v1 import OUT as DRAFTS
from scripts.review_hodram_B29_tutorial_contextual_v1 import OUT as TUTORIAL
from scripts.review_hodram_B231_B250_contextual_v1 import mark_macros

CURRENT=ROOT/'current_v1/current_effective.json'
OBJECTS=ROOT/'current_objects_v1/current_objects.json'
OUT=Path('translations/hodram_B0_B41_contextual_review_v1.json')

# R retains the current effective paragraph; C uses the independent draft unless
# a scoped refinement below supplies the final logical paragraph.
ORDINARY={
0:'''6|C|Restore Indian cultural/geographic traditions; Hindu invents a particular religious identification.
9|C|Restore a question about an Indian-related kingdom, not a confirmed Hindu identity or homeland.
12|C|Keep the counterargument explicitly about India being too far from Ottoman territory, not merely outside it.''',
1:'''6|R|The hesitant recognition naturally conveys Yukihisa’s awe and uses the registered Muramasa title.
10|R|Draws one in is a natural figurative description of the eerie gleam, not a claim that a magical effect actually occurs.''',
2:'''6|C|Restore his parting with the object without asserting that he accidentally lost it; keep the recognizable dull gleam.
10|C|Preserve the surprise that nobody picked it up, rather than ruling out anyone ever noticing or finding it.''',
3:'''6|C|Make Aziza’s rival-fleet identification conversational and preserve the FO substitution without a literal fleet-is-FO construction.
9|R|Aye is a natural nautical cheer in response to Aziza’s rally and need not be replaced with Yeah.
13|C|Restore idiomatic battle stations and take command instead of the clipped battle/command fragments.
16|R|Aye is a natural brief, confident acknowledgment of Snake’s command assignment.
20|C|Restore the enemy’s right rear, not just an unspecified position behind it.
23|R|The two exuberant assurances naturally express Angel’s enthusiastic readiness without inventing a task.
26|R|The complete gun-readiness question is natural and matches the independent draft.
29|R|Ready naturally and respectfully answers the preceding complete question; Dandy’s answer does not need padding into a longer sentence.
33|R|The thrill, chuckle and rough you dogs address naturally express Aziza’s piratical excitement without sexualizing it.
36|C|Preserve the personal rivalry between Aziza and FO with a natural challenge; do not substitute her fleet for her as the named rival.
39|R|The louder nautical cheer naturally answers the captain’s challenge and preserves its emphasis.
43|R|Pirates is a natural, dry identification after observing the rival fleet; a new voiced pause is unnecessary.
47|C|Preserve Gerhard’s tentative observation that the leader appears female.
51|R|The complete, decisive reply and battle order already preserve Hodram’s response and distinguish piracy from the leader’s gender.
55|R|The conventional acknowledgment naturally closes Gerhard’s readiness exchange.''',
4:'''43|R|The clipped found-you challenge is natural for Aziza’s forceful reencounter and preserves settling matters this time.
46|R|The nautical cheer naturally supports this alternate encounter opening.
52|C|Use a natural sinking threat rather than commanding FO to sink, retaining the native faction substitution.''',
5:'''5|C|Make the stop order and identity confirmation sound like direct speech while retaining Julian Vermeer.
8|R|The hiccup and contemptuous So what naturally answer the identity challenge in the drunken target’s voice.
11|R|The complete formal condemnation suits Hodram; gold is the game’s money, not a new treasure or payment detail.
14|C|Make the drinking, dismissal of homeland and threat of consequences conversational, rather than the abstract homeland-means-nothing-to-profit slogan.''',
6:'''5|C|Use registered Plett and replace the unnatural face-bears-crimes construction with Hodram’s own accusatory judgment.
8|C|Make the retort a natural challenge to Hodram’s moral superiority rather than the clipped sinned-once formulation.
11|C|Restore a natural conclusion and attack call instead of three disconnected judgment labels.''',
7:'''5|R|The complete, urgent command naturally demands an end to illicit trade and surrender; no synonym change is necessary.
8|C|Echo the accusation as a natural Illegal question and preserve the demand for proof.
11|C|Adapt the dust/dirty-dealings idiom into a voiced coercive accusation without certifying legal evidence.
14|C|Restore the natural death threat and the claim that the pursuers refuse to listen, rather than telegraphic Want death.''',
8:'''6|R|The complete accusation and sweet-days metaphor naturally convey enjoying smuggling profits and their impending end.
9|R|The indignant lecture rejection is idiomatic and conveys contempt without inventing a legal right or rank.''',
9:'''5|C|Make the reciprocal challenge sound spoken rather than calling a skilled foe welcome as an abstract label.
9|C|Restore full conversational boasting about challengers fleeing and the drawbacks of strength.
12|C|Replace Bored long enough with a natural acknowledgment of boredom and acceptance of the fight.''',
10:'''7|C|Preserve the complete Iscal Yasar identification and royal-order challenge in natural direct speech.
11|R|The admiral recognition, worthy-foe appraisal and short challenge naturally suit the duel opening; FA remains a native substitution.''',
11:'''6|C|Localize the screeching, stretched taunt as an English vocal performance rather than romanized Kikiki followed by flat questions.
9|C|Make Gerhard’s sighting a natural spoken announcement rather than stage-like at-last-he-appears narration.
13|C|Use a natural deadpan danger assessment instead of the stiff this-foe formulation.
17|C|Restore the repeated personal sinking threat rather than the disconnected commands Sink.''',
12:'''5|C|Restore the natural threat of letting the opponents off for now instead of This time enough.
8|R|The challenge and Caribbean-renown requirement are complete, idiomatic and appropriately mocking.
12|C|Restore the southern Mediterranean and the full pursuit/destruction threat, not an unnamed southern sea and truncated ending.''',
15:'''11|C|Restore releasing all prisoners in a natural complete order.
17|R|The conventional curse matches the explicitly cursed source reaction.
21|C|Preserve withdrawal without deep pursuit, rather than promising no pursuit at all; keep the quick pullout and discovery reaction.
25|R|The complete grounding report naturally identifies the one ship without adding an unspoken ship type or cause.
29|R|The concise inference and inspection order are natural captain’s speech and preserve the uncertain abandonment.
35|R|The hesitant address naturally requests Hodram’s attention before Gerhard explains the discovery.
39|R|The curt What is a natural response to Gerhard’s hesitant summons, not an incomplete information label.
43|C|Preserve seems out of place rather than definitively asserting the person does not belong aboard.
46|C|Replace the full-width question glyph with a natural questioning reaction; native glyph checking remains.
50|R|Over here naturally directs the admiral toward the discovered person.
56|R|The fragment is intentional first-impression narration and preserves the doll comparison without assigning the thought to a new speaker.
60|C|Preserve the startled two-mark reaction with consistent ASCII glyphs.
64|R|The interrupted Sir/The woman alarm naturally preserves Gerhard’s unfinished warning during the attack.
67|C|Keep the physical grunt and tentative pirate-or-something misidentification; the source does not confirm her thought.
73|C|Preserve the wordless response with ASCII periods rather than a mixed-width ellipsis.
77|C|Make the reassurance compassionate and natural, rather than issuing Be calm as a command.
80|C|Preserve the second wordless response with ASCII periods.
84|C|Make the appearance observation spoken and tentative; do not convert it into a confirmed ethnicity.
87|C|Preserve tentative clothing/religious inference and distinguished family background without inventing formal nobility.
91|C|Preserve this wordless response with consistent ASCII punctuation.
95|C|Restore the shared language barrier, not the ambiguous isolated statement Cannot understand.
107|C|Give Gerhard a natural formal question about what to do and preserve the practical obstacle to taking her home.
113|C|Distinguish Manuel’s conversational voice from the identical formal current Gerhard line while preserving the same obstacle.
120|C|Make the question about the remaining captives a natural spoken follow-up.
130|C|Preserve the tentative report of the prisoners’ wishes rather than declaring their wishes as omniscient fact.
135|C|Preserve the alternate companion’s tentative report and conversational voice.
141|C|Keep Hodram’s empathetic inference about distrust and grant release to those who wish it in natural speech.
151|R|The acknowledgment naturally answers the release order in this conditional Gerhard turn.
157|R|The alternate acknowledgment naturally answers the same release order in Charles’s voice.
164|C|Make the offer natural, preserve the girl’s freedom to choose and leave the better weapon unnamed.
168|C|Use the neutral source-based Foreign Girl label, not Strange girl implying oddness; preserve the startled response.
171|R|The complete warning naturally states the weapon risk and possible renewed attack without asserting an attack is certain.
175|C|Repair the contradictory second-/third-person construction Cut me if she wishes while preserving Hodram’s acceptance of her choice.
179|R|Sir naturally conveys Gerhard’s respectful alarm without adding a new rank.
183|C|Retain the neutral anonymous-girl label and the emphatic silent reaction.
194|C|Use ASCII punctuation for Manuel’s questioning shock.
201|R|Watch out is an idiomatic warning at the observed movement; no new threat is named.
205|C|Preserve the foreign-girl descriptor consistently with the other embedded labels and keep the silence.
208|R|The short spoken question naturally checks whether she refuses the offered weapon.
212|C|Use a consistent neutral anonymous label and preserve the nod as a stage action, not spoken dialogue.
215|C|Restore the small amused exhale and acceptance rather than the more resigned So be it.
226|R|The parenthesized reaction naturally conveys Manuel’s private surprise after the weapon scare.
233|R|The conventional parenthesized exhale naturally conveys Gerhard’s private relief.''',
16:'''6|R|We won is a natural complete result acknowledgment in Gerhard’s voice.
10|C|Restore the ambition to build the strongest fleet, expressed naturally rather than the abstract future-top-fleet label.
13|R|The brief Strict as ever aside naturally comments on Hodram’s demanding response.
17|C|Make the lament natural English while preserving lives lost and the consoling mother-sea image without adding a casualty count.
21|R|The name and pause naturally express Hodram’s attention or concern for Manuel.
25|C|Preserve comforting the departed spirits, not substituting a different ceremony of honoring them.
28|C|Replace the full-width question glyph with a natural questioning reaction.
32|C|Restore the repeated small ripples, nostalgia and distant maternal heartbeat in natural poetic prose.
35|C|Preserve the unnamed foreign-language claim as hearsay and its writing/sound comparison without choosing a language.
39|C|Make the final refrain natural and preserve lifelong enduring bonds plus the source poem’s closing quotation.
42|C|Make Hodram’s surprise and praise conversational rather than isolated Surprising/Never knew labels.
45|R|The brief assent and admiration naturally follow Hodram’s praise in Gerhard’s formal voice.
49|R|The complete acceptance image and gentle wish naturally close Manuel’s poem; its elevated voice is appropriate.
52|C|Preserve the longer reflective silence with six ASCII periods, not mixed-width ellipses.''',
17:'''6|R|The curse, loss admission, interrupted next-time boast and startled ending naturally lead into the mutiny.
9|C|Restore Angel’s sarcastic apologetic lead and rough conversational threat of no next time.
12|R|The low repeated chuckle naturally conveys Snake’s menace; exact laugh-syllable counts need not be copied.
16|R|The angry demand to repeat the remark is complete, natural and identical to the draft.
20|C|Give Angel a natural rough echo question rather than formal Could not hear.
24|R|The complete refusal of her authority naturally states the crew’s mutiny without adding a named participant.
27|R|The explicit curse and betrayal accusation naturally convey Aziza’s anger.
30|C|Make Hodram’s observation a natural spoken sentence rather than the label Noise over there.
34|C|Preserve the tentative observation of the woman pirate surrounded by her own men.
37|C|Order approaching the other vessel, not the more specific unproved alongside maneuver.
41|R|The complete loss/profit complaint and demand for accountability naturally motivate the mutiny.
45|R|The shocked Answer echo naturally repeats Angel’s preceding demand without needing a full explanatory question.
49|R|The conversational challenge naturally asks why she pursues FO; the faction macro is preserved.
53|R|The sneering reason-hiding question naturally conveys Snake’s accusation and implied secret.
56|C|Preserve the three-mark shocked response with ASCII punctuation.
60|C|Use the registered Bloodstained Shamshir title and preserve the father’s keepsake accusation plus FO.
64|C|Keep Aziza’s hesitant unfinished denial rather than turning it into a clean completed explanation.
68|C|Restore failing leadership/profitability without inventing that she has grown emotionally soft; make the warning spoken.
72|R|Gerhard’s complete warning preserves the danger of imminent killing without asserting that it happens.
76|R|The complete moral decision naturally states that Hodram cannot abandon her.
80|C|Make Al’s immediate decision to intervene sound like his own terse speech, not the formal Let us go.
84|R|The stammer and formal caution naturally fit Gerhard’s alarm at Al’s haste.
88|C|Preserve the explicit outsider dismissal in a natural rough warning.
91|C|Restore the warning against underlings getting cocky, not a different physical Back off command.
95|C|Keep the command targeting Aziza and this one outsider, not an invented plural group before others join.
99|R|The deliberately formal offer suits Yukihisa’s composed swordsman voice and preserves Al without an invented honorific rank.
103|C|Preserve Cristina’s condemnation of ganging up as contemptible, not a different assertion that such men are weak.
106|R|Charles’s exuberant fine loud boom line naturally conveys his source enthusiasm and proposed explosive assistance.
110|R|The direct challenge is natural for Al and preserves the invitation to attack him.
113|R|The breathless question and remembered enmity naturally express Aziza’s disbelief, leaving the source’s implied addressee open.
117|R|The stammered curse and unfavorable-odds report are idiomatic in Angel’s rough voice.
121|C|Make Hodram’s dry recognition question conversational instead of the stiff At last you see.
125|R|The two native name substitutions and pause exactly preserve Aziza’s surprised recognition.
129|R|The complete questioning recognition naturally asks whether Hodram also came to rescue her.
133|R|The guarded rhetorical challenge is natural; we refers to the already-present rescuers, not new participants.
137|C|Preserve the complaint’s interrupted ending and rough voice without completing an unspoken outcome.
140|R|The complete dry rebuke and release proposal naturally fit Hodram negotiating with the mutineers.
143|R|The clear confirmation question naturally isolates their wish to have Aziza gone.
146|R|The acknowledgment that he overheard and the refusal to follow her are natural, complete statements.
149|C|Preserve Aziza’s silence with ASCII periods.
153|R|The decisive formal offer naturally proposes taking Aziza with them and does not invent a relationship.
156|C|Preserve the three-mark surprise using ASCII punctuation.
160|C|Make the refusal to hand her over free explicitly about price; she is not free is unnecessarily ambiguous here.
164|R|The short Money echo naturally conveys Al’s indignation at the ransom demand.
168|R|The complete restraint and price question naturally fit Hodram’s controlled negotiation.
171|C|Preserve exactly 1,000,000 while using the established gold currency and a naturally spoken price.
176|R|The name and terse come invitation naturally fit Al’s restrained concern.
180|C|Preserve Aziza’s wordless response with ASCII punctuation.
184|C|Restore a rough farewell after the transaction, not the invented command Go.
190|C|Restore Aziza’s self-directed sense of having sunk low and make her rescue question conversational.
193|C|Restore Al’s personal inability to leave her in danger rather than the impersonal obligation fragment Had to help.
197|R|The complete brute/abandon judgment naturally expresses Hodram’s humane reason without inventing a modern speech.
200|C|Use a natural formal question retaining the moral assumption that piracy is a fall, which Aziza then rejects.
204|C|Make Aziza reject that assumption naturally and preserve her explicit pirate-father relationship.
207|R|Oh is a natural interested response to the newly disclosed family history.
211|C|Preserve the father’s crew and learning by observation without forcing the Japanese’s omitted imitation object to mean him or them exclusively.
214|R|The natural question about her father prompts the death disclosure without assuming Gerhard already knows his fate.
218|C|Restore the sword as her father’s treasured object and its disappearance with him, while keeping his explicitly accidental death.
222|C|Use the registered Bloodstained Shamshir title in Al’s recognition.
225|C|Replace journal-like My dream/His every deed narration with Aziza’s personal conversational ambition.
229|C|Make the recollection personal and preserve the unfinished if-I-obtained-it thought without inventing a messenger.
232|C|Preserve Hodram’s questioning silence with ASCII punctuation.
236|C|Repair the broken prove-being-like construction and preserve Aziza’s tentative proof of approaching her father’s example.
240|C|Restore her first-person realization and the keepsake’s emotional value instead of distant third-person narration.
243|C|Not profitable to pursue does not mean worthless relic; preserve the keepsake’s personal value and her understanding of the crew’s anger.
247|C|Make Al’s personal question sound like restrained speech rather than the literary Still yearn fragment.
251|C|Restore her intention to leave piracy, not an unsupported declaration that the departure is already complete.
255|C|Restore the trailing respectful appeal that Hodram recognizes as a request to invite Aziza.
259|C|Make Hodram’s acknowledgment idiomatic while retaining the good invitation to sail with them.
262|C|Preserve grateful energetic service after being saved, without suggesting a financial repayment contract for the ransom.
266|R|The complete familiar-name invitation is natural and does not invent romance or another relationship.
269|R|The formal worthy-path reflection suits Yukihisa; savior refers to the explicit lifesaving rescue, not a divine identity.
272|C|Restore the prospective lively-ship remark as natural speech, not the label Livelier now.''',
18:'''18|C|Make Aziza’s withdrawal and next-time threat sound like a spoken captain’s order rather than a formal schedule.
21|R|Boast away is a natural curt dismissal of the threat in Hodram’s dry voice.
27|C|Restore defiant refusal to submit and the full-name introduction naturally without adding a curse to the source grunt.
31|R|Noted is an idiomatic deadpan acknowledgment of the remember-my-name challenge, not an incomplete information label.''',
19:'''16|R|The complete deliberate withdrawal declaration naturally fits Hodram’s command voice.
20|R|The short question and taunting comparison are natural for Aziza and preserve the cowardice insult.
23|C|Restore not rising to provocation, rather than merely not answering it verbally.
27|C|Preserve Hodram’s already knowing the danger of provocation rather than newly acknowledging instruction.
33|C|Restore the escaped opponents as the subject; the isolated Escaped can misleadingly sound like her own escape.
37|C|Restore Gerhard’s proposal to withdraw, not an apparent order to his admiral.
41|R|The complete appraisal naturally compares Aziza’s ability to naval admiralship without actually appointing her.
45|R|The complete contemptuous question and next-encounter death threat naturally preserve Aziza’s intent.''',
20:'''9|C|Restore the already-captured man’s behavior instruction and the registered San Jorge destination, not a new surrender demand.
12|R|The curses, hands-off protest and muffled cutoff naturally convey the unruly prisoner; no injury is invented.''',
21:'''9|C|Restore secure binding and the complete Hangzhou escort order rather than an allocation-like destination fragment.
12|C|Make the pained, stammered claim of remorse natural; the text does not certify true rehabilitation.''',
22:'''8|C|Restore the guild’s ongoing difficulty and a natural hands-full idiom, not a past claim that it suffered.
11|R|The complete self-serving plea naturally claims the region would be worse without him; it remains the prisoner’s claim.
15|R|The rhetorical question and disgust are natural for Gerhard and localize his contempt without copying the Japanese idiom literally.''',
23:'''9|R|The stammered curse and possessive cargo lament naturally convey the smuggler’s distress.
12|C|Make the admonishment spoken and remove the unproved back-to-Calicut travel history.''',
24:'''9|C|Restore a natural I-let-you-win boast instead of the unnatural planned-let-you-win assertion.
12|C|Make the custody and behavior instruction grammatical spoken English while preserving the Athens guild.''',
25:'''8|R|The pained cry, incredulous self-question and refusal to accept defeat are natural for the proud target.
12|R|The extended pain cry is a natural vocalization and does not by itself assert death.
16|C|Make the mission completion, Stockholm return and report a coherent captain’s announcement rather than three chopped labels.
20|C|Preserve that the object was found aboard the enemy ship, not just an unspecified aboard.
26|C|Preserve apparent loot and the tentative unusual decorative-plate observation without naming the object.''',
26:'''28|R|The complete expectant statement is natural for Gerhard and leaves the unnamed awaited person unidentified.
52|C|Preserve continuing to defeat pirate fleets in succession without enlarging it into every pirate fleet or mandatory sinking.''',
27:'''9|C|Use a vocal cry rather than the spoken stage direction Screech, preserving the three repeated curses without asserting magic.
13|R|The complete handover order naturally preserves urgency and the Havana guild destination without inventing a prison sentence.''',
28:'''5|C|Make the relief at defeating the target spoken and unambiguous rather than At last defeated.''',
30:'''10|C|Preserve approaching the claimed waters rather than falsely asserting entry, and keep the southern Mediterranean.
13|C|Preserve the port-man callback without inventing a madman diagnosis or a specific warning not read in this utterance.
16|C|Make Gerhard’s recognition natural and avoid inventing a specific earlier fear.
19|R|The natural identity-familiarity question exactly matches the independent draft.
23|C|Restore Fazul in the source full name and the carried-on Barbarossa name without inventing a formal title or family succession.
26|C|Preserve apparent skill without asserting an unspoken veteran service history.
30|C|Make the monster comparison and unfinished additional point conversational.
36|C|Keep the alliance exception and explicit southern Mediterranean demand in this independent opening.
40|C|Preserve the alternate port-man callback without the unqualified madman label.
43|R|The recognition naturally identifies Barbarossa as the previously mentioned man.
81|C|Make the willingness-to-fight question, laugh and no-mercy threat natural rather than the clipped Oh battle then.
88|R|The complete approving mockery and Caribbean-renown challenge are idiomatic in Barbarossa’s boastful voice.
91|C|Repair the truncated world’s-end threat and preserve pursuit and destruction in the Mediterranean reappearance condition.''',
32:'''25|C|Make Maldonado’s contemptuous Caribbean challenge sound spoken while preserving the Europe-fringes insult.
55|C|Restore an idiomatic fight-as-usual reassurance and rally rather than the awkward Battle as always.
81|R|The shocked question naturally answers the unexpected rear-approach report and matches the draft.
93|R|The brief appeal to God naturally expresses Manuel’s fear and matches the draft.
106|R|The stammered complete despair naturally preserves the generic sailor’s judgment of the enemy numbers.
111|R|The logically-qualified despair preserves Charles’s distinctive analytical humor and the source numbers concern.
117|R|The short interruption and flag question naturally begin the shift from panic to recognition.
132|R|The complete good-timing and assistance offer suit Escante’s measured diplomatic voice.
135|C|Use the idiomatic possessive in the recognition of Escante’s forces.
145|C|Make the sailor’s stammered relief sound like a voiced reaction rather than the label Saved.
151|C|Make Manuel’s conditional relief a natural personal reaction while retaining this separate branch.
163|C|Differentiate Juan’s friendly casual reinforcement offer from Escante’s formal alternate offer.
166|C|Use the idiomatic possessive in the alternate recognition of Escante’s forces.
176|C|Restore a natural complete relief cry in this alternate sailor branch.
182|C|Restore a natural complete relief cry in this alternate Manuel branch.''',
33:'''5|C|Make Escante’s personal confidence and praise conversational rather than the label Most reliable.
8|C|Keep Maldonado dealt with without implying a confirmed death; the English-pirate nuisance remains.
12|C|Express the continuing-agreement offer as a natural open request rather than a ritual proclamation.
15|C|Preserve Hodram’s silence with ASCII punctuation.
34|R|The complete private warning naturally preserves Espinosa, Africa, acting in earnest and urgency.
38|R|The short thoughtful response naturally conveys Hodram considering the advice; new pause notation is unnecessary.
42|R|The complete private suggestion naturally recommends accepting this offer at this juncture without adding a permanent pledge.
63|C|Restore Escante’s own anticipation of their accomplishments rather than a passive demand for performance.
73|R|The regret and wish not to become enemies naturally preserve the diplomatic refusal response and its veiled warning.''',
34:'''6|R|The grandiose laugh, admiration of open challenge and demand for amusement naturally suit Espinosa’s taunting voice.
18|C|Make Fernando’s scorn and wager a natural voiced retort rather than the literal happy-creature and Betting fragment.''',
35:'''6|C|Restore Indian Ocean routes, not Hindustan; preserve the antagonist’s explicit Muslim identity and hostile religious claim as his speech.''',
36:'''6|C|Make the Ming/foreigner accusation a natural threat while preserving the cultural southern-barbarian epithet and explicit curse without inventing nationality.''',
37:'''6|R|The respectful look-over-there prompt is natural and conveys the requested attention.
9|C|Replace the full-width question glyph with a natural questioning reaction.
13|R|The complete tentative slave-ship identification is idiomatic and preserves seems.
17|C|Keep the prohibition as Hodram’s expectation or belief, not a universal certified historical legal fact.
21|C|Make Gerhard’s patrol-duty objection conversational while preserving widespread trafficking and the question about overlooking it.
40|C|Localize the prey/open-attack argument as fair game without inventing a new legal ruling or humanitarian speech.
43|R|The thoughtful acknowledgment naturally marks Hodram considering the argument.
50|C|Restore the precise just-before-port tactical window and a natural battle-stations command.
61|C|Localize Charles’s excited flamboyance as a natural show-making quip instead of Let us be flashy.''',
38:'''6|R|The excited sighting is natural and exactly matches the independent draft.
10|R|The complete accusation naturally expresses Lil’s mistaken belief, preserving Maria Huamei Li without making the accusation a fact.
13|R|The name and questioning pause naturally convey Hodram’s surprise and match the draft.
17|C|Use registered Kuhn and restore a disguised fleet, not merely a decoy, while preserving Camille’s urgent warning.
21|R|The surprised approved-name recognition is natural and matches the draft.
25|C|Use Kuhn consistently while retaining the existing natural sentence describing the scheme.
28|R|The complete question and trailing confused But reaction naturally preserve Lil’s disbelief without an invented explanation.
31|C|Replace the mismatched full-width initial I while preserving the otherwise good question and approved Camille.
35|C|Restore Camille’s personal familiarity and Maria informing him, not the invented purpose of sending word to warn Lil.
39|C|Restore reception of the explanation as I see rather than Yes claiming independent confirmation.
43|C|Use a clear gunnery order preserving the forward unidentified target and its unknown allegiance.
47|C|Correct Kuhn’s spelling while retaining the good reveal-yourself challenge.
51|C|Use the natural naval gunfire command Fire.
55|R|The brief forceful vocalization naturally accompanies the firing response and adds no words or named gunner.
59|R|The explicit curse is a natural hostile reaction; no extra profanity is needed.
63|C|Preserve shocked FO recognition, use Kuhn consistently and keep a disadvantage rather than declaring hopelessly outmatched.
66|R|The clipped abort-and-withdraw command is natural for the original actor40 and does not remap the speaker.
70|C|Correct Kuhn and make Lil’s interrupted self-realization natural without completing what she has not said.''',
39:'''5|C|Restore the fleet sighting ahead, not just undirected enemy ships.
9|C|Preserve the cultural southern-barbarian insult and Yamato spirit in a natural direct battle challenge.
21|R|The startled singular ship question is natural; Japanese does not require the draft’s plural, and no new number is established.
27|R|The alternate startled singular ship question is natural and preserves the distinct optional speaker.
34|R|Ironclad naturally describes the iron-covered vessel; the word adds no steam engine, modern armament or new ship mechanics.
46|C|Restore Aziza’s amazement that such a ship exists rather than the incomplete That ship label.''',
40:'''6|R|Halt is a natural forceful interception command and preserves the source order.
11|C|Preserve the two-mark shock reaction using ASCII punctuation.
15|R|The complete smug no-escape statement naturally conveys the ambusher’s taunt.
19|R|The theatrical heroic-tale threat naturally mocks FA’s exploits without declaring an actual death; FA stays a substitution.
27|R|The complete pointed coexistence statement suits Hodram’s diplomatic sarcasm and preserves the Mediterranean.
55|R|The deadpan mob judgment and breakthrough order naturally convey dismissing the motley force.
58|R|The grandiose arrogance/mocking challenge naturally fits Pasha’s pompous anger.
61|R|The intentional deadpan noun-phrase aside naturally judges Pasha’s manners and preserves the explicit general description.
65|C|Restore the public execution threat needed by Hodram’s later callback, using natural English.
68|R|The prolonged alarm cry naturally conveys the sailor’s panic without inventing a wound or death.
72|R|The short shocked question naturally demands an explanation of the sudden disruption.
76|R|The complete urgent town-gunfire report is natural and preserves the source of incoming shots.
79|R|The three urgent questions naturally convey Pasha’s surprise, confusion and demand for a cause.
82|C|Preserve uncertainty about someone taking the batteries, not a definitively observed takeover.
88|R|This deliberately opaque foreign cry is source-script text, not malformed English; retain its symbols/punctuation and qualify its own native glyph consumer.
92|C|Remove the invented N-nooo translation and preserve the source’s opaque foreign cry without assigning it a lexical command or refusal.
96|C|Make the startled unfinished recognition a natural open question without naming what Hodram sees.
100|R|The extended cry naturally preserves alarm or pain without asserting a fatal outcome.
111|C|Restore ordering Mushari’s fleet to return fire and full-speed withdrawal, not an unspecified cover maneuver.
116|C|Restore both named fleets, use registered Arnajud and preserve the separate full-speed withdrawal branch.
125|R|The poised public-execution callback and entertain-me challenge are natural combat sarcasm in this exchange, not a new entertainment scene.
129|C|Make Pasha’s acceptance and bloody threat natural spoken English rather than the literal command Cough up blood.''',
}

EXTRA={
'SC1_B28_STYLE_36_0':('C','Restore the polite cooperative report proposal, not an order to the admiral.'),
'SC1_B28_STYLE_36_46':('C','Restore this restrained voice’s necessity statement rather than another bare command.'),
'SC1_B28_STYLE_36_82':('C','Restore the informal shared report proposal and haste.'),
'SC1_B28_STYLE_36_120':('C','Restore rough, impatient speech rather than the formal Let us register.'),
'SC1_B28_STYLE_36_166':('R','The authoritative, urgent report command naturally suits this emphatic register and keeps the guild destination.'),
'SC1_B28_STYLE_36_210':('C','Restore haste and a conversational contraction for the simple lively proposal.'),
'SC1_B28_STYLE_36_254':('R','The polite next-action proposal naturally follows victory and suits this affable register; no artificial age or dialect is needed.'),
'SC1_B30_STYLE_662_0':('R','The clear huge-fleet alarm and urgent precaution naturally convey retreat for safety; no literal timer is asserted.'),
'SC1_B30_STYLE_662_54':('R','The restrained mighty-fleet observation and precaution naturally preserve this measured safety warning.'),
'SC1_B30_STYLE_662_100':('C','Use a natural conversational negative question rather than the stiff Should we not construction.'),
'SC1_B30_STYLE_662_160':('R','The complete respectful recommendation already naturally conveys the huge fleet and advice to retreat.'),
'SC1_B30_STYLE_662_206':('R','The rough clipped exclamation and retreat precaution naturally fit this register without adding a curse.'),
'SC1_B30_STYLE_662_262':('R','The measured great-fleet appraisal and wisest-retreat judgment naturally preserve the calculated advice.'),
'SC1_B30_STYLE_662_314':('C','Restore lively panic and a contraction rather than formal let us in the simple excited voice.'),
'SC1_B30_STYLE_662_362':('R','The affable precaution and emphatic fleet appraisal naturally preserve the safety advice without inventing an escape countdown.'),
'SC1_B32_STYLE_10_0':('R','The conventional lookout report is natural and preserves Maldonado’s fleet identity.'),
'SC1_B32_STYLE_10_38':('C','Restore a natural possessive and voiced discovery report.'),
'SC1_B32_STYLE_10_78':('C','Make the forceful identification grammatical and preserve the fleet’s owner.'),
'SC1_B32_STYLE_10_114':('R','The excited recognition is natural in this light register and preserves the fleet’s name.'),
'SC1_B32_STYLE_280_0':('R','The complete report naturally conveys a considerable accompanying force.'),
'SC1_B32_STYLE_280_32':('R','The understated noun-phrase report naturally answers the just-identified fleet’s size in this restrained voice.'),
'SC1_B32_STYLE_280_58':('R','The excited quantity report is natural with ships already established as the referent.'),
'SC1_B32_STYLE_280_88':('R','The short surprised ship-count exclamation is natural and needs no padded subject.'),
'SC1_B32_STYLE_280_114':('R','The clipped accompanying-force report is natural in the rough lookout register.'),
'SC1_B32_STYLE_280_144':('C','Give a voiced force observation instead of a vague quantity fragment with a tacked-on dialect tag.'),
'SC1_B32_STYLE_280_172':('R','The simple quantity exclamation is natural in immediate response to the enemy fleet.'),
'SC1_B32_STYLE_280_190':('R','Fair-sized faithfully renders the source’s moderate considerable quantity and suits a composed voice; do not inflate it into an overwhelming armada.'),
'SC1_B32_STYLE_596_0':('R','The standard astern lookout report naturally conveys additional ships approaching from behind.'),
'SC1_B32_STYLE_596_34':('R','The stammer and clipped more-from-astern warning naturally convey panic and direction.'),
'SC1_B32_STYLE_596_74':('C','Make approach from behind clear rather than the ambiguous more-coming-astern phrase.'),
'SC1_B32_STYLE_596_112':('C','Give this forceful voice a clear additional-ships-behind report without identifying an unrecognized faction.'),
'SC1_B32_STYLE_596_146':('R','The alarm cry and more-from-astern warning are natural and preserve direction without guessing hostile identity.'),
'SC1_B40_STYLE_284_0':('R','The complete stammered encirclement report naturally conveys panic and multiple fleets in this formal voice.'),
'SC1_B40_STYLE_284_46':('R','The terse complete-word alarm naturally conveys encirclement and fleet numbers without requiring every source stutter to be copied.'),
'SC1_B40_STYLE_284_88':('R','The opening cry and short urgent reports naturally convey this expressive voice’s panic.'),
'SC1_B40_STYLE_284_144':('R','The shocked questioning alarm and many-fleets exclamation naturally preserve this physical voice.'),
'SC1_B40_STYLE_284_188':('C','Restore many fleets, not a single vast fleet, while preserving the rough panicked register.'),
'SC1_B40_STYLE_284_232':('C','Preserve the alarming number of fleets rather than collapsing it into one vast fleet.'),
'SC1_B40_STYLE_284_276':('R','The simple encirclement and quantity cries naturally convey the lively panic without invented child biography.'),
'SC1_B40_STYLE_284_316':('C','Preserve many fleets and this voice’s alarm rather than substituting a single vast fleet.'),
'SC1_B41_STYLE_10_0':('C','Use a natural appearance alarm without implying a unique previously identified monster fish.'),
'SC1_B41_STYLE_10_36':('R','The short cry and noun alert work naturally like Shark; no species, named monster or extra dialogue is invented.'),
'SC1_B41_STYLE_10_62':('C','Keep the frightened, stammered appearance report and a generic monster fish rather than implying prior identification.'),
'SC1_B41_STYLE_10_104':('R','The forceful respectful noun alert naturally conveys sudden appearance without an extra invented curse.'),
'SC1_B41_STYLE_10_140':('R','The terse respectful lookout alarm naturally conveys the discovery; an invented old-person dialect is unnecessary.'),
'SC1_B41_STYLE_10_166':('R','The excited pointing alert naturally makes the appearance clear without romanizing an elongated Japanese cry.'),
'SC1_B41_STYLE_10_200':('C','Restore this polite complete appearance report rather than duplicating another voice’s clipped noun alert.'),
'SC1_B30_CHOICE_1100_0':('C','Preserve battle preparations as the chosen order, not an already issued charge.'),
'SC1_B30_CHOICE_1100_1':('R','The standard withdrawal choice is natural and preserves this branch’s action.'),
'SC1_B33_CHOICE_414_0':('R','The conventional assent naturally accepts the continuing agreement and matches the draft.'),
'SC1_B33_CHOICE_414_1':('R','No is an idiomatic complete refusal of this offer; it needs no forced expansion.'),
'SC1_B37_CHOICE_216_0':('C','Preserve the attack-preparation order, not just an immediate attack label.'),
'SC1_B37_CHOICE_216_1':('C','Use a natural tentative jurisdiction objection; overstepping carries the authority sense in this patrol context.'),
}

REFINE={
(0,12):'But India is much too far from Ottoman territory...',
(15,113):"What do we do? We can't take her home if we don't know where she's from.",
(16,17):"...Lives lost to the sea. Or perhaps I should say they've returned to the mother sea...",
(16,52):'......',
(17,34):"That pirate's own men seem to have surrounded her.",
(17,56):'!!!',
(17,91):"...Don't get cocky, lackeys.",
(17,103):"Count me in! Men who have to gang up on someone are the worst!",
(17,137):"Tch. This is all her fault. Why are we the ones...?",
(17,156):'!!!',
(17,200):'Something has puzzled me... Why would someone of your skill stoop to piracy?',
(17,204):"You think too highly of me. ...I didn't stoop to anything. I'm a pirate's daughter. My father was a pirate.",
(17,211):"Those pirates were my father's men. I grew up learning swordplay and the pirate trade by watching and copying.",
(17,255):'Sir...',
(17,259):"Al, I know what you're going to say. Aziza, will you sail with us?",
(27,9):"Aaaah! You...! I'll curse you! I'll curse you! I'll curse you!",
(28,5):"We've finally dealt with it.",
(30,13):"So that's the fellow the man at the port was talking about.",
(30,23):'Barbarossa Fazul Hayreddin... He carries on the Barbarossa name, synonymous with the pirate chiefs of Algiers.',
(30,40):"So that's the fellow the man at the port was talking about.",
(32,163):"Hey, good timing! We'll lend you a hand!",
(33,5):"Well done, {MACRO:FA}. A fine performance. You're someone I can rely on.",
(33,8):'Maldonado is dealt with, but English pirates remain a nuisance.',
(34,18):"Ha! Dream on, fool. I'll bet you're going to lose!",
(35,6):'More infidels, one after another! The routes across the Indian Ocean belong to us Muslims!',
(36,6):"So the Ming hired southern barbarians! Damn them! I'll show no mercy to anyone in my way!",
(37,17):'I thought slave trading was forbidden.',
(37,40):"They have plenty to hide. Whatever our pretext, they're fair game.",
(38,25):'Kuhn plans to make you and Maria fight each other!',
(38,47):'Kuhn! Reveal yourself!',
(38,63):"Is that {MACRO:FO}?! Kuhn, sir, we're at a disadvantage!",
(38,70):"That's... Kuhn?! Then I...!",
(39,9):"Southern barbarians! I'll show you the spirit of Yamato!",
(39,46):'I never knew a ship like that existed...',
(40,65):"We'll execute this upstart in public! All ships, charge!",
(40,92):'○×ーッ！！',
(40,96):'Is that...?!',
}

EXTRA_REFINE={
'SC1_B30_STYLE_662_100':"What a huge fleet! Shouldn't we retreat?!",
'SC1_B32_STYLE_596_74':'Admiral, more ships have come up behind us!',
'SC1_B32_STYLE_596_112':'Admiral! More ships behind us!',
'SC1_B40_STYLE_284_232':"W-we're surrounded! There are so many fleets!",
'SC1_B40_STYLE_284_316':"W-we're surrounded! A-an enormous number of fleets!",
'SC1_B41_STYLE_10_0':'Admiral! A monster fish has appeared!',
'SC1_B41_STYLE_10_62':'Eek! Th-there it is! A monster fish!',
'SC1_B41_STYLE_10_200':'Admiral! A monster fish has appeared!',
'SC1_B37_CHOICE_216_1':"Wouldn't that be overstepping...?",
}


def main():
    assert not OUT.exists()
    drafts,current,objects,tutorial=map(load,(DRAFTS,CURRENT,OBJECTS,TUTORIAL))
    assert drafts['records_count']==394 and tutorial['records_count']==32
    assert current['records']==341 and objects['native_style_getter_cases']==56
    assert current['runtime']==objects['runtime']
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    assert len(bound)==394
    decisions={}
    for b,text in ORDINARY.items():
        parsed=[line.split('|',2) for line in text.strip().splitlines()]
        assert len(parsed)==len({int(n) for n,_,_ in parsed})
        decisions.update({(b,int(n)):(kind,reason) for n,kind,reason in parsed})
    preserved={r['id']:r for r in tutorial['records']}
    rows=[];seen=set()
    for original in drafts['records']:
        if original['id'] in preserved:
            rows.append(deepcopy(preserved[original['id']]))
            continue
        row=deepcopy(original);old=bound[row['id']]
        assert all(row[k]==old[k] for k in ('source_reference','source_hex','source_Japanese'))
        if row['id'].startswith('DK4_'):
            key=(row['block'],row['source_reference']['record_index'])
            kind,reason=decisions.pop(key)
            revised=REFINE.get(key,original['english'])
        else:
            kind,reason=EXTRA[row['id']];seen.add(row['id'])
            revised=EXTRA_REFINE.get(row['id'],original['english'])
        assert kind in ('R','C') and reason
        before=mark_macros(old['current_comparison_paragraph'],row)
        english=before if kind=='R' else revised
        assert (english==before)==(kind=='R'),(row['id'],kind,english)
        assert english.strip()==english and not any(t in english for t in ('\n','\r','{LB','{ALIGN','{PAD}','\t','%'))
        assert all(english.count('{MACRO:'+m+'}')==row.get('source_macros',{}).get(m,0) for m in ('FI','FA','FO'))
        if not english.isascii():assert row['id'] in ('DK4_MES_B40_R0088','DK4_MES_B40_R0092')
        row.update(current_reference=old['current_reference'],current_hex=old['current_hex'],
            current_stored_English=old['current_stored_text'],current_English=before,
            current_effective_hex=old['current_effective_hex'],current_catalogue_selected=old['current_catalogue_selected'],
            current_reference_ROM=current['current_ROM'],current_reference_ROM_sha256=current['current_ROM_sha256'],
            independent_draft_English=original['english'],english=english,
            editorial_decision='retention' if kind=='R' else 'revision',editorial_finding=reason,
            retention_reason=reason if kind=='R' else None,localization_note=reason,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            whole_exchange_read_aloud_review=True,current_English_conversation_comparison_pending=False,
            source_first_draft_not_final_comparison_approval=False,
            scoped_names_terms_controls_glyphs_andall_display_checks_pending=True,
            fresh_native_visual_stored_gameplay_andregistered_integration_pending=True,new_credit=0)
        if (row['block'],row.get('source_reference',{}).get('record_index'))==(17,211):
            row['source_meaning']='Those pirates served Aziza’s father; she learned swordsmanship and piracy by watching and copying from childhood. This sentence does not specify only him or only his men as the imitation object.'
            row['source_meaning_refinement_reason']='Do not resolve an omitted source object unnecessarily; the later turn explicitly states she imitated her father.'
        if row['id']=='DK4_MES_B40_R0092':
            row['source_meaning']='Actor78 gives the source’s opaque symbol-based foreign cry with a prolonged ending. No lexical refusal, command or translated words are supplied.'
        rows.append(row)
    assert not decisions and seen==set(EXTRA) and len(rows)==len({r['id'] for r in rows})==394
    assert all(next(r for r in rows if r['id']==k)==v for k,v in preserved.items())
    counts=Counter(r['editorial_decision'] for r in rows)
    assert sum(counts.values())==394
    glyphs=[]
    for row in rows:
        old=bytes.fromhex(row['current_effective_hex']).decode('cp932')
        if any('\uff01'<=c<='\uff5e' or c=='…' for c in old) and row['english'].isascii():
            glyphs.append(dict(id=row['id'],previous=old,proposed=row['english'],fresh_native_glyph_check_pending=True))
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',records=rows,records_count=394,
        counts=dict(counts),four_prose_gates_pass=394,formatting_gate_pending=394,
        preserved_tutorial_decisions=32,preserved_tutorial_sha256=digest(TUTORIAL),all32_tutorial_rows_exact=True,
        ordinary_speeches=341,physical_style_alternatives=47,typed_captions=6,
        complete_exchange_blocks=drafts['complete_exchange_blocks'],current_reference=str(CURRENT),
        current_reference_sha256=digest(CURRENT),current_objects=str(OBJECTS),current_objects_sha256=digest(OBJECTS),
        exact_existing_native_context_reuse=current['exact_native_context_reuse'],
        glyph_consistency_targets=glyphs,intentional_source_script_opaque_cries=['DK4_MES_B40_R0088','DK4_MES_B40_R0092'],
        all394_clean_first_drafts_sealed_before_current_intake=True,
        no_ordinary_manual_breaks_padding_oralignment=True,
        source_names_terms_anddistinct_display_consumers_still_require_scoped_review=True,
        native_current_text_checks_not_new_gameplay=True,no_new_English_gameplay_orformatted_page_approval=True,
        registered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in (DRAFTS,CURRENT,OBJECTS,TUTORIAL,ROOT/'current_binding_verification_v1.json',Path(__file__))}))
    print(dict(records=394,counts=dict(counts),preserved_tutorial_rows=32,glyph_targets=len(glyphs),formatting_pending=394,new_credit=0))


if __name__=='__main__':main()
